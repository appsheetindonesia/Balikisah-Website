#!/usr/bin/env python
"""Verifikasi chrome situs: label lama tidak boleh muncul lagi.

Chrome = seluruh index.html DI LUAR <article class="doc"> (9 artikel dokumen).
Dokumen sengaja memuat label lama sebagai fakta referensi, jadi isinya
diabaikan; yang diperiksa hanya chrome (header, nav, hero, kartu, footer,
view alat, JS/label UI).

Label lama yang dipantau (UIRD-01/UIRD-02, dikonfirmasi 5 Okt 2026):

    Contact us -> Hubungi Kami
    Contact    -> Kontak
    Bali Kisah -> balikisah.com
    BaliKisah  -> balikisah.com
    Kenajaan   -> Kerajaan

Pengecualian (satu-satunya): kemunculan diizinkan hanya bila berada di dalam
span pemetaan yang utuh, yaitu <code>LABEL LAMA</code> lalu tanda panah (-> atau
&rarr;) dan <code>LABEL PENGGANTI</code> (boleh didahului <strong> dan catatan
dalam kurung). Hanya daftar "deviasi yang disengaja" di view Bandingkan yang
berbentuk begitu; regresi di tombol/nav/judul/footer tidak pernah cocok karena
pola pemetaan menuntut keempat bagian itu berurutan.

Pakai:
    python .freebuff/verify_chrome.py [path/index.html]
    python .freebuff/verify_chrome.py --self-test

Keluar 0 bila chrome bersih, 1 bila ada label lama atau artefak tak terbaca.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_TARGET = os.path.join(ROOT, "index.html")

ARTICLE = re.compile(r'<article class="doc"[^>]*>.*?</article>', re.S)

ARROW = r"(?:\u2192|&rarr;)"
NOTE = r"(?:\([^<>()]*\)\s*)?"          # catatan opsional, mis. "(referensi)"
CODEL = r"<code>\s*"


def mapping(label, new_label, case_insensitive=True):
    """Span dokumentasi <code>lama</code> -> <code>baru</code> yang diizinkan."""
    pattern = (CODEL + re.escape(label) + r"\s*</code>\s*" + NOTE + ARROW +
               r"\s*(?:<strong>)?\s*" + CODEL + re.escape(new_label) +
               r"\s*</code>")
    return re.compile(pattern, re.I if case_insensitive else 0)


# (label lama, pola kemunculan di chrome, span pemetaan yang seluruhnya diizinkan)
LABELS = [
    ("Contact us", re.compile(r"contact[ \t]+us", re.I),
     mapping("Contact us", "Hubungi Kami")),
    ("Contact", re.compile(r">[ \t\r]*contact[ \t\r]*<", re.I),
     mapping("Contact", "Kontak")),
    ("Bali Kisah", re.compile(r"bali[ \t\r]+kisah", re.I),
     mapping("Bali Kisah", "balikisah.com")),
    ("BaliKisah", re.compile(r"BaliKisah"),
     mapping("BaliKisah", "balikisah.com", case_insensitive=False)),
    ("Kenajaan", re.compile(r"kenajaan", re.I),
     mapping("Kenajaan", "Kerajaan")),
]

ASCII_MAP = {
    "\u2014": "-", "\u2013": "-", "\u2192": "->", "\u00d7": "x",
    "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
    "\u00a9": "(c)", "\u2026": "...", "\u00a0": " ",
}


def ascii_safe(text):
    for src, dst in ASCII_MAP.items():
        text = text.replace(src, dst)
    return text.encode("ascii", "backslashreplace").decode("ascii")


def context(chrome, start, end, pad=70):
    snippet = chrome[max(0, start - pad):end + pad]
    return ascii_safe(re.sub(r"\s+", " ", snippet)).strip()


def scan(html):
    """-> (panjang chrome, jumlah artikel, daftar kemunculan).

    Artikel dokumen diganti hanya pada karakter non-newline supaya offset dan
    nomor baris tetap sama dengan index.html asli.
    """
    def blank_non_newlines(match):
        return re.sub(r"[^\n]", "", match.group(0))

    chrome = ARTICLE.sub(blank_non_newlines, html)
    articles = len(ARTICLE.findall(html))

    allowed = []
    for label, _rx, map_rx in LABELS:
        allowed.extend((m.start(), m.end(), label) for m in map_rx.finditer(chrome))

    hits = []
    taken = []
    for label, rx, _map_rx in LABELS:
        for m in rx.finditer(chrome):
            if any(a <= m.start() < b for a, b in taken):
                continue  # sudah tertangkap label yang lebih spesifik
            taken.append((m.start(), m.end()))
            inside = [a_label for a, b, a_label in allowed
                      if a <= m.start() and m.end() <= b]
            hits.append({
                "label": label,
                "line": chrome.count("\n", 0, m.start()) + 1,
                "ctx": context(chrome, m.start(), m.end()),
                "ok": bool(inside),
                "via": inside[0] if inside else None,
            })
    chrome_len = len(ARTICLE.sub("", html))
    return chrome_len, articles, hits


def report(target, chrome_len, articles, hits):
    bad = [h for h in hits if not h["ok"]]
    excused = [h for h in hits if h["ok"]]
    print("chrome situs: %s" % ascii_safe(target))
    print("   %d artikel dokumen diabaikan; %d karakter chrome diperiksa"
          % (articles, chrome_len))
    for h in excused:
        print("   diabaikan: [%s] baris %d -- bagian dari pemetaan \"%s\""
              % (h["label"], h["line"], h["via"]))
    for h in bad:
        print("   GAGAL [%s] baris %d: ...%s..." % (h["label"], h["line"], h["ctx"]))
    if bad:
        print("HASIL: GAGAL (%d kemunculan label lama di chrome)" % len(bad))
        print("   Label lama hanya boleh tampil di dalam pemetaan utuh")
        print("   <code>LAMA</code> -> <code>PENGGANTI</code>; perbaiki label UI-nya")
        print("   atau tambahkan pemetaannya secara sengaja.")
        return 1
    print("HASIL: LULUS (%d label dipantau, %d pemetaan terdokumentasi)"
          % (len(LABELS), len(excused)))
    return 0


def self_test():
    doc = ('<article class="doc" id="doc-x"><p>Referensi: logo <code>Bali Kisah</code>, '
           'nav <code>Kenajaan</code>, CTA <code>Contact us</code>.</p></article>')
    base = ('<header><a>Kontak</a></header><h1>balikisah.com</h1>'
            '<ul><li>Nav <code>Kenajaan</code> (referensi) \u2192 '
            '<strong><code>Kerajaan</code></strong>; <code>Contact</code> \u2192 '
            '<code>Kontak</code></li>'
            '<li>CTA <code>Contact us</code> (kotak 122 x 38) \u2192 '
            '<strong><code>Hubungi Kami</code></strong></li></ul>')
    good = doc + base
    cases = [
        ("bersih: artikel + daftar pemetaan", good, 0),
        ("CTA lama kembali", good.replace("<header>", "<header><button>Contact us</button>"), 1),
        ("label nav Contact kembali", good.replace("<a>Kontak</a>", '<a href="#">Contact</a>'), 1),
        ("logo lama kembali", good.replace("<h1>balikisah.com</h1>", "<h1>Bali Kisah</h1>"), 1),
        ("nama camelCase lama", good.replace("<h1>balikisah.com</h1>", "<h1>BaliKisah.com</h1>"), 1),
        ("nav Kenajaan kembali",
         good.replace("<a>Kontak</a>", "<nav>Kenajaan</nav><a>Kontak</a>"), 1),
        ("pemetaan tanpa tanda panah",
         good.replace("(kotak 122 x 38) \u2192 ", ""), 1),
        ("label di samping pemetaan (HTML satu baris)",
         good.replace("</li><li>CTA", '<button>Contact us</button></li><li>CTA'), 1),
    ]
    broken = 0
    for name, text, expected in cases:
        _len, articles, hits = scan(text)
        got = len([h for h in hits if not h["ok"]])
        ok = (got == expected and articles == 1)
        broken += 0 if ok else 1
        print("   %s self-test: %s (harap %d, dapat %d)"
              % ("OK  " if ok else "RUSAK", name, expected, got))
    print("HASIL SELF-TEST: %s" % ("LULUS" if not broken else "GAGAL"))
    return 1 if broken else 0


def main(argv):
    flags = {a for a in argv[1:] if a.startswith("--")}
    paths = [a for a in argv[1:] if not a.startswith("--")]
    if "--self-test" in flags:
        return self_test()
    target = paths[0] if paths else DEFAULT_TARGET
    if not os.path.isfile(target):
        print("GAGAL: tidak ada %s -- jalankan dulu: python .freebuff/build_site.py"
              % ascii_safe(target))
        return 1
    try:
        html = open(target, encoding="utf-8").read()
    except (OSError, UnicodeDecodeError) as exc:
        print("GAGAL: tidak bisa membaca %s (%s)" % (ascii_safe(target), exc))
        return 1
    chrome_len, articles, hits = scan(html)
    if articles == 0:
        print("GAGAL: penanda <article class=\"doc\"> tidak ditemukan di %s -- "
              "chrome tidak bisa dipisahkan dari artikel dokumen."
              % ascii_safe(target))
        return 1
    return report(target, chrome_len, articles, hits)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
