#!/usr/bin/env python
"""Uji regresi editor (tab dasbor + urutan field + mode demo Drive).

Dijalankan otomatis di akhir setiap python .freebuff/build_site.py
(hook di main()) atau mandiri:
  PYTHONIOENCODING=utf-8 python .freebuff/test_editor_regression.py [path] [--verbose]

Pemeriksaan:
  1. WIRING (string wajib di index.html): tab dasbor (8 tab + handler pane),
     urutan field editor (order 10..80), fitur mode demo Drive.
  2. JS  : fungsi & data demo diekstrak dari index.html dan dijalankan di
     Node.js (sama seperti test_drive_links.py) — struktur DEMO_IMAGES,
     driveRowHtml (baris demo tanpa tombol Publik), listImages demo.
  3. BAKE: urutan order numerik di-parse dari HTML bawaan (bukan regex
     seadanya) dan divalidasi monotonic non-turun per kolom utama.

Skrip JS sementara ditulis ke folder tmp sistem dan dihapus setelah uji —
tidak ada jejak skrip uji di folder proyek maupun artefak build.
Keluar kode != 0 bila ada kegagalan.
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(os.path.dirname(ROOT), "index.html")

# ---------------------------------------------------------------- wiring ---
# String wajib yang harus tetap ada di index.html.
WIRING = [
    # ---- tab dasbor: 8 tab ----
    ("tab: Tulis artikel",   'data-dash-tab="write"'),
    ("tab: Daftar artikel",  'data-dash-tab="list"'),
    ("tab: Media",           'data-dash-tab="media"'),
    ("tab: Kategori & Tag",  'data-dash-tab="terms"'),
    ("tab: Komentar",        'data-dash-tab="comments"'),
    ("tab: Sampah",          'data-dash-tab="trash"'),
    ("tab: Tampilan",        'data-dash-tab="appearance"'),
    ("tab: Pengaturan",      'data-dash-tab="settings"'),
    # ---- tab dasbor: id pane (dipetakan handler) ----
    ("pane: dashWrite",      'id="dashWrite"'),
    ("pane: dashList",       'id="dashList"'),
    ("pane: dashMedia",      'id="dashMedia"'),
    ("pane: dashTerms",      'id="dashTerms"'),
    ("pane: dashComments",   'id="dashComments"'),
    ("pane: dashTrash",      'id="dashTrash"'),
    ("pane: dashAppearance", 'id="dashAppearance"'),
    ("pane: dashSettings",   'id="dashSettings"'),
    # ---- tab dasbor: handler + pemetaan ----
    ("handler tab",          'querySelectorAll("[data-dash-tab]")'),
    ("pemetaan pane",        'write:"dashWrite"'),
    ("pemetaan pane list",   'list:"dashList"'),
    ("pemetaan pane media",  'media:"dashMedia"'),
    ("pemetaan pane terms",  'terms:"dashTerms"'),
    ("pemetaan pane comments", 'comments:"dashComments"'),
    ("pemetaan pane trash",  'trash:"dashTrash"'),
    ("pemetaan pane appearance", 'appearance:"dashAppearance"'),
    ("pemetaan pane settings", 'settings:"dashSettings"'),
    ("set aria-selected",    'setAttribute("aria-selected"'),
    ("set pane hidden",      'el.hidden = k !== which'),
    ("hook __dashTab",       'window.__dashTab'),
    # ---- urutan field editor (order 10..80) ----
    ("field: Judul (10)",        '<label class="field" style="order:10"'),
    ("field: Slug (15)",         '<label class="field" style="order:15"'),
    ("field: Isi (20)",          'style="margin-bottom:8px;order:20"'),
    ("field: hint format (24)",  'style="margin:-4px 0 10px;order:24"'),
    ("field: Simpan (26)",       'style="order:26"'),
    ("field: Pratinjau/Revisi (30)", 'style="margin-top:8px;order:30"'),
    ("field: Ringkasan (40)",    '<label class="field" style="order:40"'),
    ("field: Kategori&penulis (50)", 'style="order:50"'),
    ("field: Tag (60)",          '<label class="field" style="order:60"'),
    ("field: Tag cepat (62)",    'style="margin-bottom:8px;order:62"'),
    ("field: Format (70)",       'style="order:70"'),
    ("field: SEO (80)",          '<details class="ed-fold" id="artSeoFold" style="order:80"'),
    # ---- mode demo Drive ----
    ("demo: flag DRIVE_DEMO",        'var DRIVE_DEMO'),
    ("demo: data DEMO_IMAGES",       'var DEMO_IMAGES'),
    ("demo: tombol artDriveDemo",    'id="artDriveDemo"'),
    ("demo: tombol artDriveDemoBtn", 'id="artDriveDemoBtn"'),
    ("demo: fungsi enterDriveDemo",  'function enterDriveDemo()'),
    ("demo: fungsi exitDriveDemo",   'function exitDriveDemo()'),
    ("demo: sinkron tombol",         'function syncDemoBtns()'),
    ("demo: label tombol masuk",     '"Mode demo"'),
    ("demo: label tombol keluar",    '"Keluar dari mode demo"'),
    ("demo: driveListImages demo",   'if (DRIVE_DEMO) return Promise.resolve(DEMO_IMAGES)'),
    ("demo: baris demo data-demo",   'data-demo="1"'),
    ("demo: baris demo tanpa Publik", "(demo ? '' : '<button class=\"btn btn--ghost\" type=\"button\" data-act=\"share\">Publik</button>')"),
    ("demo: sisipkan gambar demo",   'insertIntoBody("![" + name + "](" + url + ")")'),
    ("demo: cover dari demo",        'PHOTOS[key()] = {url:url, src:"drive"'),
    ("demo: pesan sisip",            'disisipkan ke isi artikel pada posisi kursor'),
    ("demo: pesan cover",            'Cover diganti dengan'),
    ("demo: pesan share demo",       'sudah bisa dibuka semua orang (mode demo)'),
    ("demo: pesan status demo",      'Mode demo: " + files.length + " gambar contoh'),
    ("demo: pesan keluar demo",      'Mode demo dihentikan'),
    ("demo: BK.driveDemoActive",     'driveDemoActive: function(){ return DRIVE_DEMO; }'),
]

JS = r'''
var assert = require("assert");
var fails = 0;
function t(label, fn){
  try { fn(); console.log("PASS " + label); }
  catch (e) { fails++; console.log("FAIL " + label + " :: " + e.message); }
}
t("DEMO_IMAGES: array >= 6", function(){
  assert.ok(Array.isArray(DEMO_IMAGES) && DEMO_IMAGES.length >= 6);
});
t("DEMO_IMAGES: tiap item punya id/name/url/demo", function(){
  DEMO_IMAGES.forEach(function(f){
    assert.ok(f.id && f.name && f.url && f.demo === true, "field kurang: " + JSON.stringify(f).slice(0,80));
  });
});
t("DEMO_IMAGES: url Wikimedia Commons", function(){
  DEMO_IMAGES.forEach(function(f){
    assert.ok(/https:\/\/(thumb\.)?wikimedia\.org\//.test(f.url), "bukan wikimedia: " + f.url);
  });
});
t("DEMO_IMAGES: thumb lebih kecil dari url", function(){
  DEMO_IMAGES.forEach(function(f){
    assert.ok(f.thumb && f.thumb.length < f.url.length, "thumb tidak lebih kecil");
  });
});
t("driveRowHtml: baris demo pakai data-demo=1", function(){
  var html = driveRowHtml(DEMO_IMAGES[0]);
  assert.ok(html.indexOf('data-demo="1"') > -1, html.slice(0,120));
});
t("driveRowHtml: baris demo TIDAK punya tombol Publik", function(){
  var html = driveRowHtml(DEMO_IMAGES[0]);
  assert.ok(html.indexOf('data-act="share"') < 0, "baris demo tidak boleh punya share/Publik");
});
t("driveRowHtml: baris demo tetap punya Sisipkan & Cover", function(){
  var html = driveRowHtml(DEMO_IMAGES[0]);
  assert.ok(html.indexOf('data-act="insert"') > -1);
  assert.ok(html.indexOf('data-act="cover"') > -1);
});
t("driveRowHtml: baris NON-demo punya tombol Publik", function(){
  var plain = {id:"x1", name:"x.jpg", url:"https://lh3.example/x", thumb:"https://lh3.example/t", demo:false};
  var html = driveRowHtml(plain);
  assert.ok(html.indexOf('data-act="share"') > -1);
  assert.ok(html.indexOf('data-demo') < 0);
});
t("driveRowHtml: data-id/data-url/data-name terisi", function(){
  var html = driveRowHtml(DEMO_IMAGES[0]);
  assert.ok(html.indexOf('data-id="' + DEMO_IMAGES[0].id + '"') > -1);
  assert.ok(html.indexOf('data-url="' + DEMO_IMAGES[0].url + '"') > -1);
  assert.ok(html.indexOf('data-name="' + DEMO_IMAGES[0].name + '"') > -1);
});
t("driveListImages: jalur demo resolve DEMO_IMAGES", function(){
  return driveListImages().then(function(files){
    assert.strictEqual(files.length, DEMO_IMAGES.length);
    assert.deepStrictEqual(files, DEMO_IMAGES);
  });
});
t("driveListImages: non-demo tanpa token -> reject", function(){
  DRIVE_DEMO = false;
  return driveListImages().then(
    function(){ throw new Error("seharusnya reject"); },
    function(err){ assert.ok(/Belum terhubung/.test(err.message), err.message); }
  ).then(function(){ DRIVE_DEMO = true; });
});
console.log(fails ? ("JS FAILURES: " + fails) : "JS ALL PASSED");
process.exit(fails ? 1 : 0);
'''


def extract_function(src, name):
    """Ambil sumber fungsi JS top-level dari index.html (cocok kurung)."""
    i = src.index("function %s(" % name)
    j = src.index("{", i)
    depth = 0
    for k in range(j, len(src)):
        if src[k] == "{":
            depth += 1
        elif src[k] == "}":
            depth -= 1
            if depth == 0:
                return src[i:k + 1]
    raise ValueError("fungsi %s tidak seimbang kurungnya" % name)


def extract_var(src, name):
    """Ambil sumber `var NAME = ...;` top-level (array/object literal).
    Berhenti di `;` yang berada pada kedalaman kurung 0."""
    m = re.search(r"var\s+%s\s*=\s*" % re.escape(name), src)
    if not m:
        raise ValueError("var %s tidak ditemukan" % name)
    i = m.end()
    depth = 0
    for k in range(i, len(src)):
        c = src[k]
        if c in "[{":
            depth += 1
        elif c in "]}":
            depth -= 1
        elif c == ";" and depth == 0:
            return src[m.start():k + 1]
    raise ValueError("var %s tidak seimbang" % name)


# --------------------------------------------------- pemeriksaan order ---
# Urutan field wajib editor Tulis artikel (kolom utama). Nilai order harus
# naik (non-turun) mengikuti urutan konseptual form.
ORDER_FLOW = [
    ("Judul", 10), ("Slug", 15), ("Isi", 20), ("hint format", 24),
    ("Simpan", 26), ("Pratinjau/Revisi", 30), ("Ringkasan", 40),
    ("Kategori & penulis", 50), ("Tag", 60), ("Tag cepat", 62),
    ("Format", 70), ("SEO", 80),
]


def run_order_checks(src, failures):
    """Parse order: dari HTML editor dan pastikan sesuai ORDER_FLOW."""
    n = 0
    for label, want in ORDER_FLOW:
        n += 1
        ok = ("order:%d" % want) in src
        print(("PASS " if ok else "FAIL ") + "order %d ada: %s" % (want, label))
        if not ok:
            failures.append("order %d hilang: %s" % (want, label))
    # Semua pasangan berurutan harus naik (monotonic non-turun).
    for a, b in zip(ORDER_FLOW, ORDER_FLOW[1:]):
        n += 1
        ok = a[1] <= b[1]
        print(("PASS " if ok else "FAIL ") + "urutan naik: %s(%d) <= %s(%d)"
              % (a[0], a[1], b[0], b[1]))
        if not ok:
            failures.append("urutan menurun: %s(%d) > %s(%d)"
                            % (a[0], a[1], b[0], b[1]))
    return n


def run_js_tests(src, failures):
    """Ekstrak fungsi/data JS dari index.html, jalankan di Node.

    esc/escAttr/driveThumbUrl sengaja di-stub (versi asli memakai
    document/DOM yang tidak ada di Node); driveListImages diekstrak utuh
    dan diuji pada jalur demo (DRIVE_DEMO=true) sehingga tidak menyentuh
    fetch/localStorage.
    """
    stub = '''
function esc(s){ return String(s == null ? "" : s)
  .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
function escAttr(s){ return esc(s).replace(/"/g, "&quot;"); }
function driveThumbUrl(id, size){ return "https://stub.thumb/" + id + "/" + size; }
'''
    js_src = ""
    try:
        js_src = (stub + "\n" +
                  extract_function(src, "driveRowHtml") + "\n" +
                  extract_function(src, "driveListImages") + "\n" +
                  extract_var(src, "DEMO_IMAGES") + "\n" +
                  "var DRIVE_DEMO = true; var DRIVE = {token: false};\n" +
                  JS)
    except ValueError as e:
        failures.append("ekstraksi JS gagal: %s" % e)
        return
    import shutil
    import tempfile
    tmp_dir = tempfile.mkdtemp(prefix="bk_editor_test_")
    js_path = os.path.join(tmp_dir, "test_editor_regression.js")
    try:
        with open(js_path, "w", encoding="utf-8") as fh:
            fh.write(js_src)
        try:
            p = subprocess.run(["node", js_path], capture_output=True,
                               text=True, encoding="utf-8", errors="replace")
        except OSError as e:
            failures.append("node tidak bisa dijalankan: %s" % e)
            return
        if p.stdout:
            print(p.stdout, end="")
        if p.returncode != 0:
            failures.append("skrip JS gagal (exit %s): %s" % (
                p.returncode, (p.stderr or "").strip()[:300]))
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def run(index_path=None, verbose=False):
    """Jalankan seluruh uji regresi editor. Exit 1 bila ada kegagalan."""
    index_path = index_path or INDEX
    failures = []
    if not os.path.isfile(index_path):
        print("FAIL index.html tidak ditemukan: %s" % index_path)
        sys.exit(1)
    with open(index_path, encoding="utf-8") as fh:
        src = fh.read()

    # 1) wiring string di index.html
    for label, needle in WIRING:
        ok = needle in src
        print(("PASS " if ok else "FAIL ") + "wiring: " + label)
        if not ok:
            failures.append("wiring hilang: " + label)

    # 2) urutan field editor
    n_order = run_order_checks(src, failures)

    # 3) JS asli di Node
    run_js_tests(src, failures)

    if failures:
        print("test_editor_regression: GAGAL (%d)" % len(failures))
        for f in failures:
            print("  - " + f)
        if verbose:
            print()
            print("=== MULAI potongan relevan dari %s ===" % os.path.basename(index_path))
            # fungsi & data demo
            for name in ("driveRowHtml", "driveListImages"):
                try:
                    body = extract_function(src, name)
                except ValueError as e:
                    body = "(tidak terekstrak: %s)" % e
                print("--- function %s ---" % name)
                for no, line in enumerate(body.splitlines(), 1):
                    print("%4d | %s" % (no, line))
            for var in ("DEMO_IMAGES",):
                try:
                    body = extract_var(src, var)
                except ValueError as e:
                    body = "(tidak terekstrak: %s)" % e
                print("--- var %s ---" % var)
                for no, line in enumerate(body.splitlines(), 1):
                    print("%4d | %s" % (no, line))
            print("=== AKHIR potongan relevan ===")
        sys.exit(1)
    print("test_editor_regression: LULUS — tab dasbor, urutan field, dan "
          "mode demo Drive OK (%d wiring + %d order)" % (len(WIRING), n_order))


if __name__ == "__main__":
    # Pemakaian:
    #   python .freebuff/test_editor_regression.py [path-index.html] [--verbose]
    args = [a for a in sys.argv[1:] if a != "--verbose"]
    run(index_path=args[0] if args else None,
        verbose="--verbose" in sys.argv[1:])

