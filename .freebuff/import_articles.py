#!/usr/bin/env python
"""Konversi artikel balikisah.com (HTML) -> articles.json (markdown-lite situs).

Sumber: GET https://balikisah.com/json?page=N  ->  [{title,label,image,body,date,link,meta}]
Tujuan: .freebuff/articles.json  ->  [{title,cat,author,excerpt,body,date,photo}]

Body situs dirender dengan markdown-lite (renderBody/inlineMd di site_shell.html),
JADI HTML dari API tidak bisa dipakai mentah — akan di-escape jadi teks.
Script ini mengubahnya jadi markdown-lite:
  <h2> -> "## ", <h3> -> "### ", <strong> -> ** **, <p> -> paragraf,
  <ul><li> -> "- ", <a href> -> [teks](url), <br> -> baris baru, <img> -> ![alt](url).
"""
import html as html_mod
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, ".freebuff", "tmp_all.json")
OUT = os.path.join(ROOT, ".freebuff", "articles.json")

# Bulan Inggris (API) -> Indonesia (format "21 Nov 2023" yang dipakai situs)
MONTHS = {
    "Jan": "Jan", "Feb": "Feb", "Mar": "Mar", "Apr": "Apr", "May": "Mei",
    "Jun": "Jun", "Jul": "Jul", "Aug": "Agu", "Sep": "Sep", "Oct": "Okt",
    "Nov": "Nov", "Dec": "Des",
}

AUTHOR = "Redaksi"

# Identitas situs (UIRD-01): seluruh chrome wajib memakai balikisah.com.
# Artikel sumber kadang memakai variasi lama yang dilarang verify_chrome.py.
#
# Kenapa tidak cukup satu regex: "balikisah.com" (domain yang BENAR) dan
# "Bali Kisah" (variasi lama) menjadi sama kalau huruf besar/kecil dan spasi
# diabaikan. Jadi domain yang benar DILINDUNGI dulu sebagai placeholder, baru
# variasi lama disamakan, lalu placeholder dikembalikan. Tanpa langkah ini
# hasilnya menjadi "balikisah.com.com".
IDENTITY_OK = "balikisah.com"
IDENTITY_KEEP = "@@BK_KEEP@@"

IDENTITY_FIX = [
    (re.compile(r"\bBaliKisah\b", re.I), "balikisah.com"),
    (re.compile(r"\bBali[ \t\r\n]+Kisah\b", re.I), "balikisah.com"),
    (re.compile(r"\bKenajaan\b", re.I), "Kerajaan"),
    (re.compile(r"\bContact[ \t]+us\b", re.I), "Hubungi Kami"),
]

CATEGORY_MAP = {
    "Cerita Lokal": "Tradisi",
    "Panduan Perjalanan": "Tips Traveling",
    "Liburan": "Wisata",
}


BAD_LABEL = re.compile(r"BaliKisah", re.S)
BAD_SPACED = re.compile(r"bali[ \t\r\n]+kisah", re.I)
BAD_KENAJAAN = re.compile(r"kenajaan", re.I)
BAD_CONTACT = re.compile(r"contact[ \t]+us", re.I)


def bad_labels(text):
    """Daftar (nama, konteks) label lama yang dilarang.

    Sengaja memakai pola yang SAMA dengan verify_chrome.py: 'BaliKisah'
    case-sensitive (tanpa \b) dan 'bali kisah' dengan spasi. Regex dengan \b
    harus dihindari — titik di 'balikisah.com' ikut dihitung batas kata,
    sehingga domain yang BENAR salah ditandai.
    """
    found = []
    for name, pat in (("BaliKisah", BAD_LABEL), ("Bali Kisah", BAD_SPACED),
                      ("Kenajaan", BAD_KENAJAAN), ("Contact us", BAD_CONTACT)):
        m = pat.search(text or "")
        if m:
            found.append((name, text[max(0, m.start() - 40):m.end() + 40]))
    return found


def fix_identity(text):
    """Samakan identitas situs. verify_chrome.py GAGAL bila 'BaliKisah' /
    'Bali Kisah' / 'Kenajaan' muncul di chrome (termasuk isi artikel) di luar
    span pemetaan <code>LAMA</code> -> <code>PENGGANTI</code>."""
    if not text:
        return text
    guarded = re.sub(re.escape(IDENTITY_OK), IDENTITY_KEEP, text, flags=re.I)
    for pat, repl in IDENTITY_FIX:
        guarded = pat.sub(repl, guarded)
    return guarded.replace(IDENTITY_KEEP, IDENTITY_OK)


def conv_date(raw):
    """'3, Oct, 2026, 19:09:09' -> '3 Okt 2026' (dibiarkan bila tak terbaca)."""
    m = re.match(r"^\s*(\d{1,2}),\s*([A-Za-z]{3})[a-z]*,?\s+(\d{4})", raw or "")
    if not m:
        return ""
    day, mon, year = m.group(1), m.group(2).title(), m.group(3)
    return "%s %s %s" % (day, MONTHS.get(mon, mon), year)


def strip_tags(text):
    """Buang tag HTML yang tidak dikenali (mis. <span>, <div>) tapi pertahankan isi."""
    return re.sub(r"</?(?:span|div|section|figure|figcaption|table|thead|tbody|tr|td|th|small|font|u|sup|sub)[^>]*>", "", text)


def inline(text):
    """Isi inline (dipakai di dalam heading/li) — buang tag sisa saja."""
    t = re.sub(r"<[^>]+>", "", text or "")
    return html_mod.unescape(t).strip()


def html_to_md(src):
    """HTML artikel -> markdown-lite yang bisa dirender renderBody()."""
    if not src:
        return ""
    t = strip_tags(src)

    # 1) Gambar dulu (sebelum <a> menelan URL di src/href).
    t = re.sub(r"<img[^>]*\bsrc=[\"']([^\"']+)[\"'][^>]*>",
               lambda m: "![gambar](%s)" % m.group(1).strip(), t, flags=re.I)

    # 2) Tautan: <a href="...">teks</a>
    def link_repl(m):
        url, label = m.group(1).strip(), m.group(2)
        label = re.sub(r"<[^>]+>", "", label).strip()
        if not label:
            label = url
        return "[%s](%s)" % (label, url)
    t = re.sub(r"<a[^>]*\bhref=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", link_repl, t,
               flags=re.I | re.S)

    # 3) Judul (h4 ke bawah diperlakukan sama dengan h3 di renderBody).
    t = re.sub(r"<h2[^>]*>(.*?)</h2>", lambda m: "\n## " + inline(m.group(1)) + "\n", t, flags=re.I | re.S)
    t = re.sub(r"<h3[^>]*>(.*?)</h3>", lambda m: "\n### " + inline(m.group(1)) + "\n", t, flags=re.I | re.S)
    t = re.sub(r"<h[45][^>]*>(.*?)</h[45]>", lambda m: "\n### " + inline(m.group(1)) + "\n", t, flags=re.I | re.S)

    # 4) Bentuk inline.
    t = re.sub(r"<strong[^>]*>(.*?)</strong>", lambda m: "**" + inline(m.group(1)) + "**", t, flags=re.I | re.S)
    t = re.sub(r"<b[^>]*>(.*?)</b>", lambda m: "**" + inline(m.group(1)) + "**", t, flags=re.I | re.S)
    # <em>/<i> TIDAK punya padanan markdown-lite (hanya **tebal**), jadi teksnya
    # dipertahankan polos agar tidak muncul tanda bintang literal.
    t = re.sub(r"</?(?:em|i)>", "", t, flags=re.I)

    # 5) Daftar -> "- ". Daftar bernomor tidak didukung renderBody (hanya "- "),
    #    jadi nomor dipertahankan sebagai teks di depan item.
    t = re.sub(r"<ol[^>]*>", "\n", t, flags=re.I)
    t = re.sub(r"</ol>", "\n", t, flags=re.I)
    t = re.sub(r"<ul[^>]*>", "\n", t, flags=re.I)
    t = re.sub(r"</ul>", "\n", t, flags=re.I)
    t = re.sub(r"<li[^>]*>(.*?)</li>", lambda m: "- " + inline(m.group(1)) + "\n", t, flags=re.I | re.S)

    # 6) Paragraf.
    t = re.sub(r"<p[^>]*>", "\n", t, flags=re.I)
    t = re.sub(r"</p>", "\n", t, flags=re.I)

    # 7) Baris / blockquote.
    t = re.sub(r"<br\s*/?>", "\n", t, flags=re.I)
    t = re.sub(r"<blockquote[^>]*>", "\n> ", t, flags=re.I)
    t = re.sub(r"</blockquote>", "\n", t, flags=re.I)

    # 8) Sisa tag apa pun dibuang, entitas HTML dikembalikan jadi karakter.
    t = re.sub(r"<[^>]+>", "", t)
    t = html_mod.unescape(t)

    # 9) Rapikan: 3+ baris baru jadi 2, buang spasi ekstra per baris.
    t = re.sub(r"[ \t]+\n", "\n", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return "\n".join(l.rstrip() for l in t.split("\n")).strip()


def main():
    if not os.path.isfile(SRC):
        sys.exit("sumber tidak ditemukan: .freebuff/tmp_all.json (jalankan pengambilan dulu)")
    with open(SRC, encoding="utf-8") as fh:
        raw = json.load(fh)

    out, seen = [], set()
    for a in raw:
        title = (a.get("title") or "").strip()
        if not title or title in seen:
            continue
        seen.add(title)

        # Kategori = token pertama dari label (mis. "Kuliner, Budaya Bali, Tradisi")
        label = (a.get("label") or "").strip()
        cat = label.split(",")[0].strip() or "Sejarah"
        cat = CATEGORY_MAP.get(cat, cat)

        body = html_to_md(a.get("body") or "")
        if not body:
            continue  # artikel tanpa isi tidak berguna

        # Ringkasan = meta dari API; kalau kosong, potong dari body.
        excerpt = (a.get("meta") or "").strip()
        if not excerpt:
            excerpt = " ".join(body.split())[:180]

        image = (a.get("image") or "").strip()

        out.append({
            "title": fix_identity(title),
            "cat": cat,
            "author": AUTHOR,
            "excerpt": fix_identity(excerpt),
            "body": fix_identity(body),
            "date": conv_date(a.get("date")),
            "photo": image if re.match(r"^https?://", image) else "",
        })

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
        fh.write("\n")

    # Ringkasan supaya bisa diperiksa cepat.
    from collections import Counter
    print("ditulis: %s" % OUT)
    print("  %d artikel, %d karakter isi total" % (len(out), sum(len(a["body"]) for a in out)))
    print("  kategori: %s" % dict(Counter(a["cat"] for a in out)))
    print("  dengan tanggal: %d/%d" % (sum(1 for a in out if a["date"]), len(out)))
    print("  dengan foto: %d/%d" % (sum(1 for a in out if a["photo"]), len(out)))

    # Tiga self-check yang wajib kosong; kalau tidak, keluaran tidak dipakai.
    joined = lambda a: a["title"] + a["excerpt"] + a["body"]
    leftover = [a["title"] for a in out if re.search(r"<(?:p|h2|h3|li|ul|ol|a|strong|em)\b", a["body"])]
    bad = [(a["title"], h[0], h[1]) for a in out for h in bad_labels(joined(a))]
    broken = [a["title"] for a in out
              if "balikisah.com.com" in joined(a) or IDENTITY_KEEP in joined(a)]
    print("  sisa tag HTML di body: %s" % (leftover or "TIDAK ADA"))
    print("  label lama (UIRD-01/02) tersisa: %s" % (bad or "TIDAK ADA"))
    print("  URL rusak / placeholder bocor: %s" % (broken or "TIDAK ADA"))
    # Kuantitas tautan balikisah.com yang tetap utuh (bukan 0, bukan .com.com)
    ok_links = sum(joined(a).count("balikisah.com") for a in out)
    print("  kemunculan 'balikisah.com' utuh: %d" % ok_links)
    if leftover or bad or broken:
        for name, title, ctx in [(b[1], b[0], b[2]) for b in bad[:10]]:
            print("   GAGAL [%s] %s ...%s..." % (name, title, " ".join(ctx.split())))
        sys.exit("konversi tidak bersih — perbaiki sebelum build")


if __name__ == "__main__":
    main()
