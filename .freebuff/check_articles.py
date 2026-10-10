#!/usr/bin/env python
"""Self-check konversi artikel: apa yang benar-benar dilarang verify_chrome.py?

verify_chrome.py memindai "chrome" = seluruh index.html DI LUAR
<article class="doc">, dengan pola kemunculan label lama (lihat LABELS di
verify_chrome.py). Yang relevan di sini:

    BaliKisah  -> re.compile(r"BaliKisah")              (tanpa \b, case-sensitive)
    Bali Kisah -> re.compile(r"bali[ \t\r]+kisah", re.I)
    Kenajaan   -> re.compile(r"kenajaan", re.I)
    Contact us -> re.compile(r"contact[ \t]+us", re.I)
    Contact    -> hanya cocok bila sendirian di antara > dan < (tag HTML)

Catatan penting: "balikisah.com" (domain yang BENAR) TIDAK cocok dengan pola
"BaliKisah" (case-sensitive) maupun "bali[ \t\r]+kisah" (menuntut spasi di
antara Bali dan kisah) — jadi domain yang benar justru sudah aman. Regex
case-insensitive dengan \b akan salah menandainya (karena "." = batas kata),
maka self-check ini memakai pola yang sama persis dengan verify_chrome.py.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTICLES = os.path.join(ROOT, ".freebuff", "articles.json")
INDEX = os.path.join(ROOT, "index.html")

# Pola salinan dari verify_chrome.py (LABELS) — harus tetap sinkron.
CHECKS = [
    ("Contact us", re.compile(r"contact[ \t]+us", re.I)),
    # 'Contact' sendirian hanya relevan di HTML, tidak di teks markdown.
    ("Bali Kisah", re.compile(r"bali[ \t\r]+kisah", re.I)),
    ("BaliKisah", re.compile(r"BaliKisah")),          # case-sensitive
    ("Kenajaan", re.compile(r"kenajaan", re.I)),
]

# Arti salah: isi artikel mengandung teks yang verify_chrome akan tolak.
import json


def load_articles():
    with open(ARTICLES, encoding="utf-8") as fh:
        return json.load(fh)


def scan_articles(arts):
    hits = []
    for a in arts:
        src = "\n".join([a.get("title", ""), a.get("excerpt", ""), a.get("body", "")])
        for name, pat in CHECKS:
            for m in pat.finditer(src):
                hits.append((a.get("title", "?")[:60], name, src[max(0, m.start() - 40):m.end() + 40]))
    return hits


def scan_index_baked():
    """Bagian yang benar-benar ter-bake di index.html (POSTS/ARTICLES JSON)."""
    with open(INDEX, encoding="utf-8") as fh:
        html = fh.read()
    # Hanya blok JSON artikel yang di-embed, bukan seluruh file.
    blocks = re.findall(r"var (?:ARTICLES|POSTS) = (?:\(function\(\)\{[^\n]*\n\s*var baked = )?(\[.*?\]);", html, re.S)
    blob = "\n".join(blocks)
    hits = []
    for name, pat in CHECKS:
        for m in pat.finditer(blob):
            hits.append((name, blob[max(0, m.start() - 40):m.end() + 40]))
    return hits, blob


def main():
    if not os.path.isfile(ARTICLES):
        sys.exit("articles.json tidak ada — jalankan import_articles.py dulu")

    arts = load_articles()
    art_hits = scan_articles(arts)
    print("diperiksa: %d artikel di articles.json" % len(arts))

    if art_hits:
        print("\nGAGAL — teks dilarang di articles.json:")
        for title, name, ctx in art_hits[:20]:
            print("  [%s] %s\n     ...%s..." % (name, title, ctx.replace("\n", " ")))
        sys.exit(1)
    print("  articles.json: BERSIH (Contact us / Bali Kisah / BaliKisah / Kenajaan)")

    if os.path.isfile(INDEX):
        idx_hits, blob = scan_index_baked()
        print("  blok JSON ter-bake di index.html: %d karakter" % len(blob))
        if idx_hits:
            print("\nGAGAL — teks dilarang di blok ter-bake index.html:")
            for name, ctx in idx_hits[:20]:
                print("  [%s] ...%s..." % (name, ctx.replace("\n", " ")))
            sys.exit(1)
        print("  blok ter-bake index.html: BERSIH")

    print("\nHASIL: LULUS — isi artikel tidak memuat label lama yang dilarang chrome.")


if __name__ == "__main__":
    main()
