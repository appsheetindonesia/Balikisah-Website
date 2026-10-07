#!/usr/bin/env python
"""Uji regresi konversi tautan Google Drive (tempel + simpan + bake).

Dijalankan otomatis di akhir setiap python .freebuff/build_site.py
(hook di main()) atau mandiri:  python .freebuff/test_drive_links.py

Cara kerja:
  1. Ekstrak fungsi JS asli (normalizePhotoLink + normalizeDriveLinksInText)
     dari index.html hasil build, jalankan di Node.js dengan skenario
     tempel (payload papan klip) dan simpan (field body + meta).
     Skrip JS sementara ditulis ke folder tmp sistem dan dihapus setelah uji —
     tidak ada jejak skrip uji di folder proyek maupun artefak build.
  2. Pastikan wiring editor tetap terpasang (paste body/Ringkasan/SEO,
     deteksi di collectEntry, impor runtime).
  3. Uji normalize_drive_links() dari build_site.py (jalur bake).
Keluar kode != 0 bila ada kegagalan.

Mode --verbose: saat ada kegagalan, isi fungsi JS hasil ekstrak (beserta
harness ujinya) dicetak ke output untuk diagnosis.
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(os.path.dirname(ROOT), "index.html")

# ---------------------------------------------------------------- wiring ---
# String wajib yang harus tetap ada di index.html; kalau salah satu hilang
# berarti salah satu kait tempel/simpan/impor tidak sengaja terhapus.
WIRING = [
    ("paste isi artikel", "wireDrivePaste(body)"),
    ("paste Ringkasan", "wireDrivePaste(excerpt)"),
    ("paste Judul SEO", "wireDrivePaste(elSeoTitle)"),
    ("paste Deskripsi SEO", "wireDrivePaste(elSeoDesc)"),
    ("paste Bio", "wireDrivePaste(elBio)"),
    ("deteksi simpan: isi", "normalizeDriveLinksInText(body.value)"),
    ("deteksi simpan: meta", "[excerpt, elSeoTitle, elSeoDesc, elBio].forEach"),
    ("tulis balik field meta", "el.value = r.text"),
    ("impor runtime articles", "normalizeDriveLinksInText(a[k])"),
    ("pesan tempel", "ditempel sebagai URL gambar lh3."),
    ("pesan simpan", "tautan Google Drive diubah ke URL gambar lh3."),
    ("peringatan live editor", "artDriveBad"),
    ("fungsi pencari tautan tanpa ID", "function findBadDriveLinks(text)"),
    ("pesan simpan: Drive tanpa ID", "tautan Drive tanpa ID valid tidak bisa"),
]


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


# ------------------------------------------------------------- kasus JS ---
JS_PASTE = r"""
var assert = require("assert");
var fails = 0;
function t(label, fn){
  try { fn(); console.log("PASS tempel: " + label); }
  catch (e) { fails++; console.log("FAIL tempel: " + label + " :: " + e.message); }
}
var ID = "1AbCdEfGhIjKlMnOpQrStUvWxYz01";
var LH3 = "https://lh3.googleusercontent.com/d/" + ID + "=w1600";
t("URL polos /file/d/", function(){
  var r = normalizeDriveLinksInText("https://drive.google.com/file/d/" + ID + "/view?usp=sharing");
  assert.strictEqual(r.count, 1); assert.strictEqual(r.text, LH3);
});
t("bentuk open?id=", function(){
  var r = normalizeDriveLinksInText("https://drive.google.com/open?id=" + ID);
  assert.strictEqual(r.count, 1); assert.strictEqual(r.text, LH3);
});
t("markdown gambar", function(){
  var r = normalizeDriveLinksInText("![candi](https://drive.google.com/file/d/" + ID + "/view)");
  assert.strictEqual(r.count, 1);
  assert.strictEqual(r.text, "![candi](" + LH3 + ")");
});
t("markdown tautan", function(){
  var r = normalizeDriveLinksInText("[lihat](https://drive.google.com/file/d/" + ID + "/view)");
  assert.strictEqual(r.count, 1);
  assert.strictEqual(r.text, "[lihat](" + LH3 + ")");
});
t("titik kalimat dipertahankan", function(){
  var r = normalizeDriveLinksInText("Buka https://drive.google.com/file/d/" + ID + "/view.");
  assert.strictEqual(r.count, 1); assert.strictEqual(r.text, "Buka " + LH3 + ".");
});
t("lh3 sudah jadi tidak dihitung", function(){
  var r = normalizeDriveLinksInText(LH3);
  assert.strictEqual(r.count, 0); assert.strictEqual(r.text, LH3);
});
t("URL non-Drive dibiarkan", function(){
  var r = normalizeDriveLinksInText("https://example.com/foto.jpg");
  assert.strictEqual(r.count, 0); assert.strictEqual(r.text, "https://example.com/foto.jpg");
});
t("Drive tanpa ID dibiarkan", function(){
  var raw = "https://drive.google.com/drive/folders/abcdef1234567";
  var r = normalizeDriveLinksInText(raw);
  assert.strictEqual(r.count, 0); assert.strictEqual(r.text, raw);
});
t("campuran 2 Drive + 1 non-Drive", function(){
  var r = normalizeDriveLinksInText(
    "a https://drive.google.com/file/d/" + ID + "/view b https://example.com c https://drive.google.com/open?id=" + ID + "2");
  assert.strictEqual(r.count, 2);
  assert.ok(r.text.indexOf("drive.google.com") < 0);
  assert.ok(r.text.indexOf("https://example.com") > -1);
});
"""
JS_SAVE = r"""
function t2(label, fn){
  try { fn(); console.log("PASS simpan: " + label); }
  catch (e) { fails++; console.log("FAIL simpan: " + label + " :: " + e.message); }
}
function simulateSave(fields){
  var total = 0;
  var stored = fields.map(function(v){
    var r = normalizeDriveLinksInText(v);
    total += r.count;
    return r.text;
  });
  return {stored: stored, total: total};
}
t2("isi + 4 field meta terkonversi, hitungan gabungan", function(){
  var res = simulateSave([
    "Isi bersih tanpa Drive.",
    "Ringkasan https://drive.google.com/file/d/" + ID + "A/view",
    "SEO https://drive.google.com/file/d/" + ID + "B/view",
    "Deskripsi https://drive.google.com/open?id=" + ID + "C",
    "Bio (https://drive.google.com/file/d/" + ID + "D/view)."
  ]);
  assert.strictEqual(res.total, 4);
  res.stored.forEach(function(v){ assert.ok(v.indexOf("drive.google.com") < 0); });
  assert.ok(res.stored[4].indexOf(").") > -1);
});
t2("idempoten: simpan ulang tidak menambah hitungan", function(){
  var first = simulateSave(["x https://drive.google.com/file/d/" + ID + "/view"]);
  var second = simulateSave(first.stored);
  assert.strictEqual(first.total, 1);
  assert.strictEqual(second.total, 0);
});
t2("tanpa Drive = tanpa perubahan", function(){
  var src = ["judul", "ringkasan biasa", "https://example.com"];
  var res = simulateSave(src);
  assert.strictEqual(res.total, 0);
  assert.deepStrictEqual(res.stored, src);
});
t2("deteksi: Drive tanpa ID (folder) -> bad, teks utuh", function(){
  var r = normalizeDriveLinksInText("Lihat https://drive.google.com/drive/folders/Abc123XYZ789 ini");
  assert.strictEqual(r.count, 0);
  assert.strictEqual(r.bad.length, 1);
  assert.ok(r.text.indexOf("drive/folders/Abc123XYZ789") > -1);
});
t2("deteksi: lh3 valid tidak dihitung bad", function(){
  var r = normalizeDriveLinksInText(LH3 + " dan teks");
  assert.strictEqual(r.count, 0);
  assert.strictEqual(r.bad.length, 0);
});
t2("deteksi: campuran 1 valid + 1 tanpa ID", function(){
  var r = normalizeDriveLinksInText(
    "https://drive.google.com/file/d/" + ID + "/view lalu https://drive.google.com/uc?export=view");
  assert.strictEqual(r.count, 1);
  assert.strictEqual(r.bad.length, 1);
  assert.ok(r.text.indexOf("lh3.googleusercontent.com") > -1);
  assert.ok(r.text.indexOf("https://drive.google.com/uc?export=view") > -1);
});
console.log(fails ? ("JS FAILURES: " + fails) : "JS ALL PASSED");
process.exit(fails ? 1 : 0);
"""


# ------------------------------------------------- uji sisi build (Python) ---
def run_build_side_tests(failures):
    sys.path.insert(0, ROOT)
    try:
        import build_site
    except Exception as e:  # PIL dsb — bagian dari build, jadi gagal = gagal
        failures.append("import build_site gagal: %s" % e)
        return 0
    checks = []
    ID = "1BakeTest0123456789abcdefghijklmnop"
    lh3 = "https://lh3.googleusercontent.com/d/" + ID + "=w1600"
    txt, n = build_site.normalize_drive_links(
        "https://drive.google.com/file/d/%s/view" % ID)
    checks.append(("bake: /file/d/ -> lh3", txt == lh3 and n == 1))
    txt, n = build_site.normalize_drive_links(
        "Akhir kalimat https://drive.google.com/file/d/%s/view." % ID)
    checks.append(("bake: titik dipertahankan", txt == "Akhir kalimat " + lh3 + "." and n == 1))
    txt, n = build_site.normalize_drive_links(
        "https://drive.google.com/open?id=" + ID)
    checks.append(("bake: bentuk ?id=", txt == lh3 and n == 1))
    raw = "https://drive.google.com/drive/folders/abcdef1234567"
    txt, n = build_site.normalize_drive_links(raw)
    checks.append(("bake: Drive tanpa ID dibiarkan", txt == raw and n == 0))
    txt, n = build_site.normalize_drive_links(None)
    checks.append(("bake: bukan string aman", txt is None and n == 0))
    for label, ok in checks:
        print(("PASS " if ok else "FAIL ") + label)
        if not ok:
            failures.append("build-side: " + label)
    return len(checks)
def run(index_path=None, verbose=False):
    """Jalankan seluruh uji. Keluar dengan kode 1 bila ada kegagalan.

    verbose=True (atau argumen --verbose): bila ada kegagalan, isi fungsi JS
    hasil ekstrak + harness ujinya dicetak agar penyebab kegagalan terlihat.
    """
    index_path = index_path or INDEX
    failures = []
    if not os.path.isfile(index_path):
        print("FAIL index.html tidak ditemukan: %s" % index_path)
        sys.exit(1)
    with open(index_path, encoding="utf-8") as fh:
        src = fh.read()

    # 1) wiring tempel + simpan + impor
    for label, needle in WIRING:
        ok = needle in src
        print(("PASS " if ok else "FAIL ") + "wiring: " + label)
        if not ok:
            failures.append("wiring hilang: " + label)

    # 2) fungsi JS asli dijalankan di Node.js
    js_src = ""
    try:
        js_src = (extract_function(src, "normalizePhotoLink") + "\n" +
                  extract_function(src, "normalizeDriveLinksInText") + "\n" +
                  JS_PASTE + JS_SAVE)
    except ValueError as e:
        failures.append("ekstraksi fungsi JS gagal: %s" % e)
    if js_src:
        # Tulis skrip JS sementara ke folder tmp SISTEM (bukan di dalam proyek)
        # dan hapus setelah uji selesai supaya tidak ada jejak skrip uji pada
        # artefak/folder proyek.
        import shutil
        import tempfile
        tmp_dir = tempfile.mkdtemp(prefix="bk_drive_test_")
        js_path = os.path.join(tmp_dir, "test_drive_links.js")
        try:
            with open(js_path, "w", encoding="utf-8") as fh:
                fh.write(js_src)
            try:
                p = subprocess.run(["node", js_path], capture_output=True,
                                   text=True, encoding="utf-8", errors="replace")
            except OSError as e:
                p = None
                failures.append("node tidak bisa dijalankan: %s" % e)
            if p is not None:
                if p.stdout:
                    print(p.stdout, end="")
                if p.returncode != 0:
                    failures.append("skrip JS gagal (exit %s): %s" % (
                        p.returncode, (p.stderr or "").strip()[:300]))
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

    # 3) jalur bake di build_site.py
    run_build_side_tests(failures)

    if failures:
        print("test_drive_links: GAGAL (%d)" % len(failures))
        for f in failures:
            print("  - " + f)
        if verbose and js_src:
            print()
            print("=== MULAI fungsi JS hasil ekstrak + harness uji "
                  "(dari %s) ===" % os.path.basename(index_path))
            for no, line in enumerate(js_src.splitlines(), 1):
                print("%4d | %s" % (no, line))
            print("=== AKHIR fungsi JS hasil ekstrak ===")
        sys.exit(1)
    print("test_drive_links: LULUS — tempel, simpan, wiring, dan bake OK")


if __name__ == "__main__":
    # Pemakaian:
    #   python .freebuff/test_drive_links.py [path-index.html] [--verbose]
    args = [a for a in sys.argv[1:] if a != "--verbose"]
    run(index_path=args[0] if args else None,
        verbose="--verbose" in sys.argv[1:])
