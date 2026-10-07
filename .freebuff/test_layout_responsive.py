#!/usr/bin/env python
"""Uji regresi tata letak responsif: tanpa overflow horizontal + label nav
tidak melipat, di lebar ponsel / tablet / desktop — ditambah sapuan overflow
untuk SETIAP view pada lebar ponsel.

Dijalankan otomatis di akhir setiap python .freebuff/build_site.py (hook di
main()) atau mandiri:  python .freebuff/test_layout_responsive.py

Cara kerja:
  Halaman index.html dimuat di dalam <iframe> pada Chrome headless, lalu
  iframe itu dipersempit/dilebarkan ke tiap lebar uji. Iframe dipakai karena
  Chrome membatasi lebar jendela minimum ~500 px sehingga lebar ponsel
  (390 px) tidak bisa dicapai dengan --window-size; iframe memberi layout
  viewport sungguhan (window.innerWidth ikut berubah).
  Skrip pembungkus sementara ditulis ke folder tmp SISTEM dan dihapus setelah
  uji — tidak ada jejak di folder proyek maupun artefak build.

Yang diperiksa:

  A. Per lebar (390 / 768 / 1024 / 1280 / 1440 px) pada halaman awal:
     1. overflow  — documentElement.scrollWidth > clientWidth (ada elemen yang
                    memaksa halaman melebar, memunculkan scroll horizontal).
     2. lipatan   — tiap label nav yang TERLIHAT harus setinggi satu baris
                    (>= 1 px). Diukur dengan Range.getClientRects() sehingga
                    benar-benar menghitung baris teks, bukan offsetHeight.
     3. label nav — pada lebar desktop (>= 1024 px) 8 label wajib terlihat,
                    pada lebar ponsel (< 1024 px) digantikan laci mobile.

  B. Sapuan SETIAP view pada 390 dan 402 px (jumlah view = len(VIEW_STEPS)):
     Situs punya 10 view (#view-*) sementara A hanya mengukur halaman awal,
     jadi view yang jarang dibuka (mis. Kelola Foto) tidak pernah diperiksa.
     Tiap view dibuka lewat PINTU MASUK ASLINYA — klik `[data-goto]`, klik
     `[data-blog]`, submit `[data-search-form]`, atau `BK.go()` — supaya
     konten yang diukur benar-benar ter-render (grid artikel, hasil cari,
     dasbor), bukan view kosong yang pasti lolos. Setelah itu diukur
     documentElement.scrollWidth - clientWidth.
     Ini menangkap kelas bug yang lolos ketika hanya satu halaman diuji:
     `select` di panel Drive tanpa aturan `width` memakai lebar intrinsik opsi
     terpanjang (424 px), memaksa panel 461 px → overflow 104 px pada 390 px.
     Tiap view juga wajib benar-benar TAMPIL dan (untuk view berisi daftar
     artikel) memuat minimal `minPosts` kartu, supaya pemeriksaan tidak
     berubah jadi lolos-semata karena kontennya tidak ter-render.
     View yang tidak bisa dibuka tanpa login (admin) ditandai `optional` dan
     dilaporkan sebagai LEWAT — bukan PASS.
     Meta-check: setiap `#view-*` yang ada di dokumen harus punya langkah di
     VIEW_STEPS; menambah view baru tanpa menyapunya membuat uji GAGAL.

Keluar kode != 0 bila ada kegagalan. Bila Chrome tidak ada, uji DILEWATI
(exit 0) dengan pesan jelas — kegagalan lingkungan bukan regresi kode.

Mode --verbose: saat ada kegagalan, seluruh data pengukuran per lebar dan per
view dicetak untuk diagnosis.
"""
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(os.path.dirname(ROOT), "index.html")

# Lebar uji untuk pemeriksaan halaman awal: ponsel, tablet, desktop kecil/besar.
VIEWPORTS = [390, 768, 1024, 1280, 1440]

# Lebar uji untuk sapuan SETIAP view (ponsel kecil dan ponsel 402 px).
MOBILE_VIEWPORTS = [390, 402]

# Di bawah lebar ini navigasi desktop disembunyikan dan diganti laci mobile
# (lihat aturan .site-nav / .nav-toggle di site_shell.html).
MOBILE_MAX = 1024
EXPECTED_NAV_ITEMS = 8

# Cara membuka tiap view. `how`:
#   go     — window.BK.go(view) (view alat: archive/404/compare/docs/photo/admin)
#   click  — klik elemen pertama yang cocok dengan `sel` (jalur data-goto/data-blog)
#   submit — isi input pencarian lalu kirim event submit ke [data-search-form]
# Opsi per langkah:
#   minPosts  — jumlah minimal elemen `[data-post]` di dalam view (bukti konten
#               benar-benar ter-render). 0 = tidak diperiksa.
#   optional  — view boleh tidak tampil (mis. butuh login) → dilaporkan LEWAT.
VIEW_STEPS = [
    {"view": "home", "how": "go", "minPosts": 8},
    {"view": "archive", "how": "click", "sel": '[data-goto="archive"]'},
    # Kategori "Budaya" (tautan nav pertama) kosong di data contoh sehingga
    # daftarnya cuma empty-state; dipakai kategori berisi artikel + pintu
    # alternatif supaya daftar berisi benar-benar terukur.
    {"view": "blog", "how": "click",
     "sel": '[data-goto="blog"][data-blog="kategori"][data-key="Candi"]',
     "alt": ['[data-goto="blog"][data-blog="kategori"][data-key="Tokoh Sejarah"]',
             '[data-goto="blog"][data-blog][data-key="Kerajaan"]'],
     "minPosts": 1},
    {"view": "search", "how": "submit", "q": "Bali", "minPosts": 1},
    {"view": "article", "how": "click", "sel": '[data-goto="article"][data-post]', "minPosts": 1},
    {"view": "404", "how": "go"},
    {"view": "compare", "how": "click", "sel": '[data-goto="compare"]'},
    {"view": "docs", "how": "click", "sel": '[data-goto="docs"]'},
    {"view": "photo", "how": "click", "sel": '[data-goto="photo"]'},
    {"view": "admin", "how": "go", "optional": True},
]
STEP_BY_VIEW = {s["view"]: s for s in VIEW_STEPS}

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
]

# --------------------------------------------------------------- harness ---
# Skrip ini berjalan DI DALAM halaman pembungkus. Ia memuat index.html di
# iframe, lalu (A) mengumpulkan angka pengukuran tiap lebar pada halaman awal,
# dan (B) menyapu seluruh view pada lebar ponsel. Hasilnya ditaruh di
# document.title sebagai "RESULT<json>". Semua langkah berjalan sinkron
# (klik/`BK.go` memproses DOM seketika), jadi tidak ada timer tambahan yang
# bisa melewati --virtual-time-budget.
WRAPPER = r"""<!doctype html>
<html><head><meta charset="utf-8"><title>pending</title></head>
<body style="margin:0">
<iframe id="f" style="width:390px;height:900px;border:0"></iframe>
<script>
var VIEWPORTS = __VIEWPORTS__;
var MOBILE_WIDTHS = __MOBILEWIDTHS__;
var VIEW_STEPS = __VIEWSTEPS__;
var SESSION_KEY = "balikisah.admin.session";
var f = document.getElementById("f");
var notes = [];

function visibleScope(doc) {
  // Situs punya beberapa view (#view-*); hanya satu yang tidak hidden.
  // Semua pengukuran harus dibatasi ke view itu, karena header/laci view
  // lain tetap ada di DOM tetapi tidak ter-render.
  var views = doc.querySelectorAll("[id^='view-']");
  for (var i = 0; i < views.length; i++) {
    var v = views[i];
    if (v.hasAttribute("hidden")) continue;
    if (v.getClientRects().length) return v;
  }
  return doc;
}

/* Elemen terlebar yang melewati batas layout — hanya dipakai untuk diagnosis
   saat overflow > 0. Anak dari kontainer ber-overflow (mis. slider promo
   `overflow-x:auto`) ikut terhitung, jadi ini petunjuk, bukan vonis. */
function worstGuess(scope, lim) {
  var els = scope.querySelectorAll("*"), best = null;
  for (var i = 0; i < els.length; i++) {
    var e = els[i], r = e.getBoundingClientRect();
    if (!r.width) continue;
    var over = Math.round(r.right - lim);
    if (over <= 0) continue;
    if (best && over <= best.over) continue;
    var cls = (typeof e.className === "string" ? e.className : "").trim();
    best = { over: over, tag: e.tagName.toLowerCase(), id: e.id || "",
             cls: cls ? cls.split(/\s+/).slice(0, 3).join(" ") : "",
             w: Math.round(r.width), right: Math.round(r.right) };
  }
  return best;
}

function measureWidths() {
  var doc = f.contentDocument, win = f.contentWindow, out = [];
  var scope = visibleScope(doc);
  var navLinks = scope.querySelectorAll(".site-nav a");
  var toggle = scope.querySelector(".nav-toggle");
  var drawer = scope.querySelector(".mobile-nav");

  for (var i = 0; i < VIEWPORTS.length; i++) {
    var w = VIEWPORTS[i];
    f.style.width = w + "px";
    var de = doc.documentElement;
    var row = {
      w: w, innerWidth: win.innerWidth,
      clientWidth: de.clientWidth, scrollWidth: de.scrollWidth,
      overflow: de.scrollWidth - de.clientWidth,
      navVisible: 0, navWrapped: [],
      drawerVisible: 0, drawerWrapped: [],
      toggleVisible: false
    };

    // (a) nav desktop yang benar-benar terlihat
    for (var j = 0; j < navLinks.length; j++) {
      var a = navLinks[j];
      if (win.getComputedStyle(a).display === "none") continue;
      if (!a.getClientRects().length) continue;
      row.navVisible++;
      var r = doc.createRange(); r.selectNodeContents(a);
      if (r.getClientRects().length > 1) {
        row.navWrapped.push({ t: a.textContent.trim(), lines: r.getClientRects().length });
      }
    }

    // (b) tombol hamburger terlihat?
    if (toggle) {
      row.toggleVisible = (win.getComputedStyle(toggle).display !== "none" &&
                           toggle.getClientRects().length > 0);
    }

    // (c) laci mobile: buka sementara, ukur, lalu kembalikan `hidden`
    //     supaya tidak mengotori pengukuran lebar berikutnya.
    if (drawer) {
      var wasHidden = drawer.hasAttribute("hidden");
      if (wasHidden) drawer.removeAttribute("hidden");
      var dl = drawer.querySelectorAll("a");
      for (var k = 0; k < dl.length; k++) {
        var m = dl[k];
        if (win.getComputedStyle(m).display === "none") continue;
        if (!m.getClientRects().length) continue;
        row.drawerVisible++;
        var mr = doc.createRange(); mr.selectNodeContents(m);
        if (mr.getClientRects().length > 1) {
          row.drawerWrapped.push({ t: m.textContent.trim(), lines: mr.getClientRects().length });
        }
      }
      if (wasHidden) drawer.setAttribute("hidden", "");
    }
    out.push(row);
  }
  return out;
}

/* Jumlah kartu artikel di KONTEN UTAMA view (tautan sidebar/widget tidak
   dihitung) — dipakai sebagai bukti daftar benar-benar ter-render dan tidak
   diam-diam kosong, yang akan membuat pemeriksaan overflow jadi hampa. */
function countPosts(doc, view) {
  var v = doc.getElementById("view-" + view);
  if (!v) return 0;
  var all = v.querySelectorAll("[data-post]"), n = 0;
  for (var i = 0; i < all.length; i++) {
    if (!all[i].closest("aside, .widget")) n++;
  }
  return n;
}

/* Satu pintu masuk. Kembalikan "" bila berhasil, atau pesan alasan bila
   pintunya tidak ditemukan. `sel` kosong berarti jalur BK.go. */
function doStep(step, doc, win, sel) {
  if (sel) {
    var el = doc.querySelector(sel);
    if (!el) return "pintu masuk tidak ditemukan: " + sel;
    el.click();
    return "";
  }
  if (step.how === "go") {
    if (!win.BK || typeof win.BK.go !== "function") return "window.BK.go tidak tersedia";
    win.BK.go(step.view);
    return "";
  }
  if (step.how === "submit") {
    var form = doc.querySelector("[data-search-form]");
    if (!form) return "form pencarian [data-search-form] tidak ditemukan";
    var inp = form.querySelector("input[name=s], input[type=search]");
    if (!inp) return "input pencarian tidak ditemukan";
    inp.value = step.q || "";
    form.dispatchEvent(new win.Event("submit", { bubbles: true, cancelable: true }));
    return "";
  }
  return "jenis langkah tidak dikenal: " + step.how;
}

/* Buka satu view lewat pintu masuk aslinya. Bila `alt` diberikan dan daftar
   utama masih kosong, coba pintu alternatif (namanya ditulis ke `usedSel`
   supaya pesan kegagalan menyebut pintu yang benar-benar dipakai). */
function runStep(step, doc, win) {
  var sels = step.sel ? [step.sel].concat(step.alt || []) : [null];
  var lastErr = "";
  for (var i = 0; i < sels.length; i++) {
    var err = doStep(step, doc, win, sels[i]);
    if (err) { lastErr = err; continue; }
    step.usedSel = sels[i] || (step.how + ":" + step.view);
    lastErr = "";
    if (countPosts(doc, step.view) >= (step.minPosts || 1)) break;
  }
  return lastErr;
}

function measureView(step, doc, win, w) {
  var de = doc.documentElement, lim = de.clientWidth;
  var v = doc.getElementById("view-" + step.view);
  var shown = !!(v && !v.hasAttribute("hidden") && v.getClientRects().length);
  var row = {
    w: w, view: step.view, visible: shown,
    clientWidth: lim, scrollWidth: de.scrollWidth,
    overflow: de.scrollWidth - lim,
    posts: countPosts(doc, step.view),
    nodes: v ? v.querySelectorAll("*").length : 0,
    entry: step.usedSel || "",
    shownView: (visibleScope(doc).id || ""),
    worst: null
  };
  if (shown && row.overflow > 0) row.worst = worstGuess(v, lim);
  return row;
}

function sweepViews() {
  var doc = f.contentDocument, win = f.contentWindow, out = [];
  /* Dasbor hanya tampil setelah login; isi kunci sesi di localStorage iframe
     supaya view admin ikut terukur. Kunci dihapus lagi di akhir. */
  var seeded = false;
  try {
    if (!win.localStorage.getItem(SESSION_KEY)) {
      win.localStorage.setItem(SESSION_KEY, "layout-test");
      seeded = true;
    }
  } catch (e) {
    notes.push("localStorage tidak bisa ditulis: view admin kemungkinan dilewati");
  }

  for (var i = 0; i < MOBILE_WIDTHS.length; i++) {
    var w = MOBILE_WIDTHS[i];
    f.style.width = w + "px";
    for (var s = 0; s < VIEW_STEPS.length; s++) {
      var step = VIEW_STEPS[s];
      var err = "";
      try { err = runStep(step, doc, win); }
      catch (e) { err = "langkah melempar error: " + e; }
      var row = measureView(step, doc, win, w);
      if (err) row.err = err;
      out.push(row);
    }
  }

  if (seeded) { try { win.localStorage.removeItem(SESSION_KEY); } catch (e) {} }

  /* Daftar view yang benar-benar ada di dokumen — dipakai Python untuk
     memastikan tidak ada view baru yang luput dari sapuan. */
  var found = [];
  var views = doc.querySelectorAll(".view");
  for (var k = 0; k < views.length; k++) {
    if (views[k].id) found.push(views[k].id.replace(/^view-/, ""));
  }
  return { rows: out, found: found };
}

function finish() {
  var payload = { widths: measureWidths(), views: [], foundViews: [], notes: notes };
  try {
    var swept = sweepViews();
    payload.views = swept.rows;
    payload.foundViews = swept.found;
  } catch (e) {
    notes.push("sapuan view gagal: " + e);
  }
  document.title = "RESULT" + JSON.stringify(payload);
}

f.onload = function () {
  var fonts = f.contentDocument.fonts;
  if (fonts && fonts.ready && fonts.ready.then) {
    fonts.ready.then(function () { setTimeout(finish, 150); });
  } else {
    setTimeout(finish, 400);
  }
};
f.src = __SRC__;
</script></body></html>
"""


def find_chrome():
    """Kembalikan path browser headless pertama yang ada, atau None."""
    for cand in CHROME_CANDIDATES:
        if os.path.isfile(cand):
            return cand
    for name in ("google-chrome", "chromium", "chromium-browser", "chrome"):
        found = shutil.which(name)
        if found:
            return found
    for pattern in (r"C:\Program Files\*\Application\chrome.exe",
                    r"C:\Program Files\*\Application\msedge.exe"):
        hits = glob.glob(pattern)
        if hits:
            return hits[0]
    return None


def run_chrome(chrome, index_path, timeout=180):
    """Muat index.html di iframe Chrome headless; kembalikan data pengukuran.

    Mengembalikan (payload, error). payload=None bila pengukuran gagal.
    payload = {"widths": [...], "views": [...], "foundViews": [...], "notes": [...]}
    """
    tmp_dir = tempfile.mkdtemp(prefix="bk_layout_test_")
    try:
        wrapper_path = os.path.join(tmp_dir, "wrap.html")
        src = "file:///" + os.path.abspath(index_path).replace("\\", "/")
        html = (WRAPPER
                .replace("__VIEWPORTS__", json.dumps(VIEWPORTS))
                .replace("__MOBILEWIDTHS__", json.dumps(MOBILE_VIEWPORTS))
                .replace("__VIEWSTEPS__", json.dumps(VIEW_STEPS))
                .replace("__SRC__", json.dumps(src)))
        with open(wrapper_path, "w", encoding="utf-8") as fh:
            fh.write(html)
        url = "file:///" + wrapper_path.replace("\\", "/")
        # Profil terisolasi di dalam tmp_dir: tanpa ini Chrome headless memakai
        # profil sementara bersama, yang bisa bentrok dengan Chrome lain yang
        # sedang jalan (handler crashpad gagal membuat berkas → halaman tidak
        # pernah dimuat → "tidak menghasilkan data pengukuran"). Ikut terhapus
        # di finally, jadi uji ini tetap tidak meninggalkan jejak.
        profile_dir = os.path.join(tmp_dir, "profile")
        # Anggaran waktu virtual dinaikkan karena sapuan view menambah
        # pekerjaan; nilai ini hanya membatasi waktu VIRTUAL (timer), bukan
        # waktu nyata, jadi biayanya nyaris nol.
        cmd = [chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
               "--allow-file-access-from-files", "--force-device-scale-factor=1",
               "--user-data-dir=" + profile_dir,
               "--window-size=1600,1000", "--virtual-time-budget=30000",
               "--dump-dom", url]
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=timeout)
        dom = proc.stdout or ""
        marker = dom.find("RESULT")
        if marker < 0:
            tail = (proc.stderr or "").strip().splitlines()
            return None, ("Chrome tidak menghasilkan data pengukuran "
                          "(rc=%s)%s" % (proc.returncode,
                                         (": " + tail[-1]) if tail else ""))
        raw = dom[marker + len("RESULT"):]
        raw = raw.split("</title>")[0]
        return json.loads(raw), None
    except (subprocess.TimeoutExpired, ValueError, OSError) as exc:
        return None, "pengukuran gagal: %s" % exc
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def fmt_worst(w):
    """Ringkas elemen terlebar untuk pesan kegagalan."""
    name = (w.get("tag") or "?")
    if w.get("id"):
        name += "#" + w["id"]
    if w.get("cls"):
        name += "." + w["cls"].replace(" ", ".")
    return "%s (lebar %dpx, tepi kanan %dpx, lebih %+dpx)" % (
        name, w.get("w", 0), w.get("right", 0), w.get("over", 0))


def check_widths(rows, failures):
    """A. Pemeriksaan per lebar pada halaman awal (nav, laci, overflow)."""
    for row in rows:
        w = row["w"]
        desktop = w > MOBILE_MAX   # .site-nav disembunyikan pada max-width:1024px

        # 1) tidak ada overflow horizontal
        if row["overflow"] > 0:
            msg = ("lebar %dpx: overflow horizontal %+dpx "
                   "(scrollWidth %d > clientWidth %d)"
                   % (w, row["overflow"], row["scrollWidth"], row["clientWidth"]))
            print("FAIL " + msg)
            failures.append(msg)
        else:
            print("PASS lebar %dpx: tanpa overflow horizontal (scrollWidth %d)"
                  % (w, row["scrollWidth"]))

        # 2) tidak ada label nav yang melipat (desktop maupun laci mobile)
        bad_wrap = row["navWrapped"] + row["drawerWrapped"]
        if bad_wrap:
            for item in bad_wrap:
                msg = ("lebar %dpx: label melipat -> %r (%d baris)"
                       % (w, item["t"], item["lines"]))
                print("FAIL " + msg)
                failures.append(msg)
        else:
            print("PASS lebar %dpx: tidak ada label nav yang melipat "
                  "(desktop %d, laci %d)"
                  % (w, row["navVisible"], row["drawerVisible"]))

        # 3) mode navigasi harus tepat di batas breakpoint
        if desktop:
            if row["navVisible"] != EXPECTED_NAV_ITEMS:
                msg = ("lebar %dpx: nav desktop menampilkan %d label, "
                       "seharusnya %d" % (w, row["navVisible"], EXPECTED_NAV_ITEMS))
                print("FAIL " + msg)
                failures.append(msg)
            if row["toggleVisible"]:
                msg = ("lebar %dpx: tombol hamburger masih tampil padahal "
                       "nav desktop aktif" % w)
                print("FAIL " + msg)
                failures.append(msg)
        else:
            if row["navVisible"] != 0:
                msg = ("lebar %dpx: nav desktop masih terlihat (%d label) "
                       "padahal harus diganti laci mobile" % (w, row["navVisible"]))
                print("FAIL " + msg)
                failures.append(msg)
            if not row["toggleVisible"]:
                msg = "lebar %dpx: tombol hamburger tidak tampil" % w
                print("FAIL " + msg)
                failures.append(msg)
            if row["drawerVisible"] < EXPECTED_NAV_ITEMS:
                msg = ("lebar %dpx: laci mobile hanya %d label, seharusnya >= %d"
                       % (w, row["drawerVisible"], EXPECTED_NAV_ITEMS))
                print("FAIL " + msg)
                failures.append(msg)


def check_view_coverage(found_views, failures):
    """A.2 Meta: setiap #view-* di dokumen harus punya langkah di VIEW_STEPS."""
    swept = sorted(STEP_BY_VIEW)
    found = sorted(set(found_views))
    if not found:
        msg = "daftar view kosong — pengukuran tidak sah"
        print("FAIL " + msg)
        failures.append(msg)
        return
    extra = [v for v in found if v not in STEP_BY_VIEW]
    missing = [v for v in swept if v not in found]
    if extra:
        msg = ("view belum disapu oleh uji: %s — tambahkan langkah di VIEW_STEPS"
               % ", ".join(extra))
        print("FAIL " + msg)
        failures.append(msg)
    if missing:
        msg = ("langkah VIEW_STEPS menunjuk view yang tidak ada di dokumen: %s"
               % ", ".join(missing))
        print("FAIL " + msg)
        failures.append(msg)
    if not extra and not missing:
        print("PASS cakupan view: %d view di dokumen tersapu semuanya"
              % len(found))


def check_views(view_rows, failures, skipped):
    """B. Sapuan overflow setiap view pada lebar ponsel."""
    passed = 0
    for row in view_rows:
        step = STEP_BY_VIEW.get(row["view"], {})
        tag = "%dpx view-%s" % (row["w"], row["view"])

        if row.get("err"):
            msg = "%s: %s" % (tag, row["err"])
            print("FAIL " + msg)
            failures.append(msg)
            continue

        if not row["visible"]:
            if step.get("optional"):
                msg = ("%s: dilewati, view tidak tampil (tampil: %s) — "
                       "butuh login?" % (tag, row["shownView"] or "?"))
                print("LEWAT " + msg)
                skipped.append(msg)
            else:
                msg = ("%s: view tidak tampil setelah pintunya dijalankan "
                       "(tampil: %s)" % (tag, row["shownView"] or "?"))
                print("FAIL " + msg)
                failures.append(msg)
            continue

        if row["overflow"] > 0:
            msg = ("%s: overflow horizontal %+dpx (scrollWidth %d > clientWidth %d)"
                   % (tag, row["overflow"], row["scrollWidth"], row["clientWidth"]))
            if row.get("worst"):
                msg += " — elemen terlebar: " + fmt_worst(row["worst"])
            print("FAIL " + msg)
            failures.append(msg)
            continue

        need = step.get("minPosts", 0)
        if row["posts"] < need:
            msg = ("%s: hanya %d kartu artikel di konten utama, seharusnya "
                   ">= %d (pintu: %s) — konten tidak ter-render?"
                   % (tag, row["posts"], need, row.get("entry") or "?"))
            print("FAIL " + msg)
            failures.append(msg)
            continue

        passed += 1
        print("PASS %s: tanpa overflow horizontal (scrollWidth %d, %d kartu "
              "artikel, %d elemen)"
              % (tag, row["scrollWidth"], row["posts"], row["nodes"]))
    return passed


def run(index_path=None, verbose=False):
    # Jalankan seluruh uji. Keluar dengan kode 1 bila ada kegagalan.
    index_path = index_path or INDEX
    failures = []
    skipped = []
    if not os.path.isfile(index_path):
        print("FAIL index.html tidak ditemukan: %s" % index_path)
        sys.exit(1)

    chrome = find_chrome()
    if not chrome:
        print("LEWATI: browser headless tidak ditemukan di sistem ini "
              "(Chrome/Edge/Chromium). Uji tata letak tidak dijalankan.")
        print("test_layout_responsive: LULUS (dilewati)")
        return

    payload, err = run_chrome(chrome, index_path)
    if payload is None:
        print("FAIL " + err)
        print("test_layout_responsive: GAGAL (1)")
        sys.exit(1)

    rows = payload.get("widths") or []
    view_rows = payload.get("views") or []
    if not rows or not view_rows:
        print("FAIL data pengukuran tidak lengkap (widths %d, views %d)"
              % (len(rows), len(view_rows)))
        print("test_layout_responsive: GAGAL (1)")
        sys.exit(1)

    # A. halaman awal per lebar + cakupan view
    check_widths(rows, failures)
    check_view_coverage(payload.get("foundViews") or [], failures)

    # B. sapuan setiap view pada lebar ponsel
    n_view_pass = check_views(view_rows, failures, skipped)

    if failures:
        print("test_layout_responsive: GAGAL (%d)" % len(failures))
        for f in failures:
            print("  - " + f)
        if verbose:
            print()
            print("=== MULAI data pengukuran per lebar (verbatim) ===")
            for row in rows:
                print(json.dumps(row, ensure_ascii=False))
            print("=== MULAI data pengukuran per view (verbatim) ===")
            for row in view_rows:
                print(json.dumps(row, ensure_ascii=False))
            print("=== AKHIR data pengukuran ===")
        sys.exit(1)

    tail = ""
    if skipped:
        tail = " (%d dilewati)" % len(skipped)
    print("test_layout_responsive: LULUS — %d lebar bersih + %d pemeriksaan "
          "view bersih (%d view x %d lebar ponsel)%s"
          % (len(rows), n_view_pass, len(STEP_BY_VIEW),
             len(MOBILE_VIEWPORTS), tail))
    if verbose:
        print()
        print("=== data pengukuran per view (verbatim) ===")
        for row in view_rows:
            print(json.dumps(row, ensure_ascii=False))


if __name__ == "__main__":
    # Pemakaian:
    #   python .freebuff/test_layout_responsive.py [path-index.html] [--verbose]
    args = [a for a in sys.argv[1:] if a != "--verbose"]
    run(index_path=args[0] if args else None,
        verbose="--verbose" in sys.argv[1:])
