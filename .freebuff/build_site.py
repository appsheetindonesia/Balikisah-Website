#!/usr/bin/env python
"""
Build a self-contained static preview of the BaliKisah redesign.

Outputs: D:\\Balikisah website\\index.html  (single file, no server required)

What it does:
  1. Crops the archival card thumbnails straight out of the reference screenshot
     so the rendered archive can be compared pixel-for-pixel. The wordmark is
     rendered as text in the shell, not as a bitmap crop.
  2. Renders the nine requirement documents to HTML with python-markdown.
  3. Emits one self-contained index.html implementing the UIRD theme
     (beranda / arsip kategori / artikel / dokumen).

Usage:  python .freebuff/build_site.py
"""
import base64
import html as html_mod
import io
import json
import os
import re
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(ROOT, "WhatsApp Image 2026-10-05 at 09.50.58.jpeg")
OUT = os.path.join(ROOT, "index.html")

DOCS = [
    ("UIRD", "User Interface Requirements Document (UIRD).md",
     "User Interface Requirements Document"),
    ("PRD", "Product Requirements Document (PRD) 18 Section.md",
     "Product Requirements Document (18 Section)"),
    ("MRD", "Market Requirements Document (MRD).md",
     "Market Requirements Document"),
    ("CRD", "Customer Requirements Document (CRD).md",
     "Customer Requirements Document"),
    ("BRD", "Business Requirements Document (BRD).md",
     "Business Requirements Document"),
    ("FRD", "Functional Requirements Document (FRD).md",
     "Functional Requirements Document"),
    ("TRD", "Technical Requirements Document (TRD).md",
     "Technical Requirements Document"),
    ("QRD", "Quality Requirements Document (QRD).md",
     "Quality Requirements Document"),
    ("SRS", "Software Requirements Specification (SRS).md",
     "Software Requirements Specification"),
]


def data_uri(img, fmt="PNG", quality=88):
    buf = io.BytesIO()
    if fmt == "JPEG":
        img.convert("RGB").save(buf, "JPEG", quality=quality, optimize=True)
        mime = "image/jpeg"
    else:
        img.save(buf, fmt, optimize=True)
        mime = "image/" + fmt.lower()
    return f"data:{mime};base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def crop(uri):
    im = Image.open(uri).convert("RGB")
    # Row 1 of the reference grid, measured in RU (@756px frame)
    boxes = [(83, 158, 219, 247), (234, 158, 369, 247),
             (384, 158, 519, 247), (534, 158, 670, 247)]
    cards = [data_uri(im.crop(b), "JPEG") for b in boxes]
    # Row 2 is clipped by the bottom of the screenshot; keep the visible band.
    row2 = [(83, 352, 219, 424), (234, 352, 369, 424),
            (384, 352, 519, 424), (534, 352, 670, 424)]
    cards += [data_uri(im.crop(b), "JPEG") for b in row2]
    # Whole reference frame, for the side-by-side comparison view.
    whole = data_uri(im, "JPEG", 92)
    return cards, whole


def load_photos():
    """Foto artikel opsional dari .freebuff/photos.json (judul -> URL gambar).

    Isinya dihasilkan tombol "Ekspor photos.json" pada view Kelola Foto di situs.
    """
    path = os.path.join(ROOT, ".freebuff", "photos.json")
    if not os.path.isfile(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        sys.exit("photos.json harus berisi objek JSON {judul artikel: url}")
    bad = [k for k, v in data.items() if not isinstance(v, str)]
    if bad:
        sys.exit("photos.json: setiap nilai harus string URL, bermasalah: " + ", ".join(bad))
    return data


MODULES = ["mod_blog.js", "mod_article.js", "mod_admin.js"]


def load_modules():
    """Bundel modul fitur (pencarian/arsip/widget, artikel, dasbor) ke __MODULES__.

    Tiap modul berdiri sendiri dan hanya butuh window.BK; bila satu gagal, sisanya
    tetap jalan. Berkasnya di-embed apa adanya sehingga tidak ada request jaringan.
    """
    parts = []
    for name in MODULES:
        path = os.path.join(ROOT, ".freebuff", name)
        if not os.path.isfile(path):
            sys.exit("modul tidak ditemukan: .freebuff/%s" % name)
        with open(path, encoding="utf-8") as fh:
            parts.append("/* --- %s --- */\n%s" % (name, fh.read().rstrip("\n")))
    return "\n".join(parts)


def load_posts():
    """Artikel bawaan dari .freebuff/posts.json.

    Satu-satunya sumber artikel contoh: build menyuntiknya ke halaman sebagai
    __POSTS__, dan memakainya lagi untuk menulis rss.xml + sitemap.xml sehingga
    kedua berkas itu selalu sinkron dengan yang tampil di situs.
    """
    path = os.path.join(ROOT, ".freebuff", "posts.json")
    if not os.path.isfile(path):
        sys.exit("posts.json tidak ditemukan di .freebuff/")
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, list) or not data:
        sys.exit("posts.json harus berupa daftar artikel yang tidak kosong")
    for i, item in enumerate(data):
        if not isinstance(item, dict) or not item.get("t"):
            sys.exit("posts.json: item %d tidak valid (butuh kunci 't' = judul)" % i)
    return data


_DRIVE_URL_RE = re.compile(r"""https?://(?:drive|docs)\.google\.com/[^\s)\]'\"<>]+""")
_DRIVE_PATH_ID_RE = re.compile(r"/file/d/([A-Za-z0-9_-]{10,})")
_DRIVE_QUERY_ID_RE = re.compile(r"[?&]id=([A-Za-z0-9_-]{10,})")


def normalize_drive_links(text):
    """Tautan Google Drive apa pun -> URL gambar lh3 (parity dengan
    normalizeDriveLinksInText() di situs: dipakai saat impor articles.json).
    Mengembalikan (teks_baru, jumlah_penggantian)."""
    if not isinstance(text, str) or "google.com" not in text:
        return text, 0
    count = 0

    def repl(m):
        nonlocal count
        raw = m.group(0)
        trail = ""
        tm = re.search(r"[.,;:!?]+$", raw)
        if tm:
            trail = tm.group(0)
            raw = raw[: -len(trail)]
        idm = _DRIVE_PATH_ID_RE.search(raw) or _DRIVE_QUERY_ID_RE.search(raw)
        if not idm:
            return raw + trail  # Drive tanpa ID: dibiarkan
        count += 1
        return "https://lh3.googleusercontent.com/d/" + idm.group(1) + "=w1600" + trail

    return _DRIVE_URL_RE.sub(repl, text), count


def load_articles():
    """Artikel opsional dari .freebuff/articles.json (daftar objek artikel).

    Isinya dihasilkan tombol "Ekspor articles.json" pada panel admin (Dasbor Redaksi).
    Setiap item: {title, cat, author, excerpt, body, date, photo}.
    """
    path = os.path.join(ROOT, ".freebuff", "articles.json")
    if not os.path.isfile(path):
        return []
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, list):
        sys.exit("articles.json harus berupa daftar JSON")
    for i, item in enumerate(data):
        if not isinstance(item, dict) or not item.get("title"):
            sys.exit("articles.json: item %d tidak valid (butuh kunci 'title')" % i)
        # Tautan Google Drive di isi/ringkasan/foto -> URL gambar lh3,
        # supaya hasil bake setara dengan hasil simpan di editor.
        for key in ("body", "excerpt", "photo"):
            if isinstance(item.get(key), str):
                item[key], _ = normalize_drive_links(item[key])
    return data


def render_docs():
    try:
        import markdown
    except ImportError:
        sys.exit("python-markdown is required: pip install markdown")
    out = []
    for key, fname, title in DOCS:
        path = os.path.join(ROOT, fname)
        with open(path, encoding="utf-8") as fh:
            src = fh.read()
        body = markdown.markdown(
            src,
            extensions=["tables", "fenced_code", "toc", "attr_list"],
            extension_configs={"toc": {"toc_depth": "2-3"}},
        )
        out.append(
            f'<article class="doc" id="doc-{key}" data-key="{key}">{body}</article>'
        )
    return "\n".join(out)


SITE_URL = "https://balikisah.com"

MONTHS_ID = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "mei": 5, "jun": 6,
    "jul": 7, "agu": 8, "ags": 8, "aug": 8, "sep": 9, "okt": 10,
    "oct": 10, "nov": 11, "des": 12, "dec": 12,
}
MONTHS_EN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
             "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def slugify(text):
    """Cermin dari slugify() di site_shell.html (harus sama persis)."""
    import unicodedata
    t = (text or "").strip().lower()
    t = unicodedata.normalize("NFD", t)
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t or "artikel"


def parse_date(text):
    """'21 Nov 2023' -> (2023, 11, 21); None bila tidak bisa dibaca."""
    m = re.match(r"^\s*(\d{1,2})\s+([A-Za-z]+)\.?\s+(\d{4})\s*$", text or "")
    if not m:
        return None
    day, name, year = int(m.group(1)), m.group(2).lower(), int(m.group(3))
    month = MONTHS_ID.get(name[:3])
    if not month or not (1 <= day <= 31):
        return None
    return year, month, day


def rfc822(text):
    """Tanggal RSS (RFC 822). Bila tak terbaca, pakai waktu build."""
    import email.utils
    import datetime
    d = parse_date(text)
    if d:
        stamp = datetime.datetime(d[0], d[1], d[2], 7, 0, 0,
                                  tzinfo=datetime.timezone(datetime.timedelta(hours=8)))
        return email.utils.format_datetime(stamp)
    return email.utils.formatdate()


def iso_date(text):
    """Tanggal ISO untuk sitemap; tanpa jam."""
    d = parse_date(text)
    return "%04d-%02d-%02d" % d if d else ""


def norm_tags(raw):
    if isinstance(raw, str):
        raw = raw.split(",")
    return [str(t).strip() for t in (raw or []) if str(t).strip()]


def feed_items(posts, articles):
    """Gabungan artikel bawaan + hasil ekspor admin, dengan slug unik.

    Meniru rebuildArt() di halaman: artikel admin menggantikan artikel bawaan
    yang judulnya sama, artikel di Sampah dan yang belum terbit tidak ikut.
    """
    merged, index = [], {}
    for p in posts:
        item = {"title": p.get("t") or "", "cat": p.get("c") or "Kerajaan",
                "author": p.get("author") or "Subrata",
                "excerpt": p.get("e") or "", "date": p.get("d") or "",
                "body": p.get("body") or "", "tags": norm_tags(p.get("tags")),
                "photo": None, "status": "publish", "trashed": False}
        index[item["title"]] = len(merged)
        merged.append(item)
    for a in articles:
        if not a.get("title"):
            continue
        item = {"title": a["title"], "cat": a.get("cat") or "Kerajaan",
                "author": a.get("author") or "Redaksi",
                "excerpt": a.get("excerpt") or "", "date": a.get("date") or "",
                "body": a.get("body") or "", "tags": norm_tags(a.get("tags")),
                "photo": a.get("photo"),
                "status": a.get("status") or "publish",
                "trashed": bool(a.get("trashed"))}
        if item["title"] in index:
            merged[index[item["title"]]] = item
        else:
            merged.append(item)
    # Hanya artikel yang benar-benar terbit ikut ke feed/sitemap.
    merged = [m for m in merged if not m["trashed"] and m["status"] == "publish"]
    used = {}
    for item in merged:
        base = slug = slugify(item["title"])
        n = 2
        while slug in used:
            slug = "%s-%d" % (base, n)
            n += 1
        used[slug] = 1
        item["slug"] = slug
    return merged


def xml_safe(text):
    """Escape untuk XML + buang karakter kontrol yang tidak sah."""
    text = "".join(c for c in (text or "")
                   if c in "\t\n\r" or ord(c) >= 32)
    return (text.replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace('"', "&quot;"))


def write_rss(items):
    """rss.xml (RSS 2.0) di root workspace — fitur feed ala WordPress."""
    latest = items[0]["date"] if items else ""
    rows = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">',
        '  <channel>',
        '    <title>balikisah.com — Sejarah dan Babad Bali</title>',
        '    <link>%s/</link>' % SITE_URL,
        '    <description>Berbagi informasi, wawasan, dan panduan ',
        '      terpercaya seputar Bali dan Indonesia.</description>',
        '    <language>id-ID</language>',
        '    <lastBuildDate>%s</lastBuildDate>' % rfc822(latest),
        '    <atom:link href="%s/rss.xml" rel="self" type="application/rss+xml"/>'
        % SITE_URL,
    ]
    for it in items:
        url = "%s/?post=%s" % (SITE_URL, it["slug"])
        desc = xml_safe(it["excerpt"])
        if not desc.strip():
            desc = xml_safe(" ".join(it["body"].split())[:280])
        rows += [
            '    <item>',
            '      <title>%s</title>' % xml_safe(it["title"]),
            '      <link>%s</link>' % url,
            '      <guid isPermaLink="true">%s</guid>' % url,
            '      <pubDate>%s</pubDate>' % rfc822(it["date"]),
            '      <author>noreply@balikisah.com (%s)</author>'
            % xml_safe(it["author"]),
            '      <category>%s</category>' % xml_safe(it["cat"]),
            '      <description>%s</description>' % desc,
            '    </item>',
        ]
    rows += ['  </channel>', '</rss>', '']
    path = os.path.join(ROOT, "rss.xml")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(rows))
    return path


def write_sitemap(items):
    """sitemap.xml: beranda + arsip kategori + setiap artikel ber-slug."""
    rows = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
            '  <url><loc>%s/</loc><changefreq>daily</changefreq></url>' % SITE_URL,
            '  <url><loc>%s/#/kategori</loc><changefreq>weekly</changefreq></url>'
            % SITE_URL]
    for it in items:
        rows.append('  <url><loc>%s/?post=%s</loc>%s</url>'
                    % (SITE_URL, it["slug"],
                       ("<lastmod>%s</lastmod>" % iso_date(it["date"]))
                       if iso_date(it["date"]) else ""))
    cats, tags, authors, months, seen_c, seen_t, seen_a, seen_m = [], [], [], [], set(), set(), set(), set()
    for it in items:
        if it["cat"] and it["cat"] not in seen_c:
            seen_c.add(it["cat"])
            cats.append(it["cat"])
        if it["author"] and it["author"] not in seen_a:
            seen_a.add(it["author"])
            authors.append(it["author"])
        for tag in it["tags"]:
            if tag and tag not in seen_t:
                seen_t.add(tag)
                tags.append(tag)
        d = parse_date(it["date"])
        if d:
            key = "%04d-%02d" % (d[0], d[1])
            if key not in seen_m:
                seen_m.add(key)
                months.append(key)
    for cat in cats:
        rows.append('  <url><loc>%s/#/kategori/%s</loc><changefreq>weekly</changefreq></url>'
                    % (SITE_URL, slugify(cat)))
    for tag in tags:
        rows.append('  <url><loc>%s/#/tag/%s</loc><changefreq>weekly</changefreq></url>'
                    % (SITE_URL, slugify(tag)))
    for who in authors:
        rows.append('  <url><loc>%s/#/penulis/%s</loc><changefreq>weekly</changefreq></url>'
                    % (SITE_URL, slugify(who)))
    for key in sorted(months, reverse=True):
        rows.append('  <url><loc>%s/#/arsip/%s</loc><changefreq>monthly</changefreq></url>'
                    % (SITE_URL, key))
    rows.append('  <url><loc>%s/#/kategori</loc><changefreq>weekly</changefreq></url>' % SITE_URL)
    rows += ['</urlset>', '']
    path = os.path.join(ROOT, "sitemap.xml")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(rows))
    return path


def count_sitemap_urls():
    """Jumlah <url> di sitemap.xml yang baru saja ditulis."""
    path = os.path.join(ROOT, "sitemap.xml")
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read().count("<url>")
    except OSError:
        return 0


def write_robots():
    """robots.txt + referensi sitemap, seperti pengaturan SEO WordPress."""
    body = "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE_URL
    path = os.path.join(ROOT, "robots.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
    return path


def main():
    if not os.path.isfile(REF):
        sys.exit(f"reference image not found: {REF}")
    cards, whole = crop(REF)
    docs_html = render_docs()
    photos = load_photos()

    with open(os.path.join(ROOT, ".freebuff", "site_shell.html"),
              encoding="utf-8") as fh:
        shell = fh.read()

    articles = load_articles()
    posts = load_posts()
    # Foto cover yang ikut exporting articles.json ikut di-bake sebagai foto
    # permanen, supaya tautan Drive tidak hilang saat situs dibangun ulang.
    for item in articles:
        url = item.get("photo")
        if isinstance(url, str) and url and item.get("title") and item["title"] not in photos:
            photos[item["title"]] = url
    # Foto dari posts.json (judul -> photo) juga ikut dipakai sebagai default.
    for p in posts:
        url = p.get("photo")
        if isinstance(url, str) and url and p.get("t") and p["t"] not in photos:
            photos[p["t"]] = url

    modules = load_modules()
    page = (shell
            .replace("__MODULES__", modules)
            .replace("__PHOTO_MAP__", json.dumps(photos, ensure_ascii=False))
            .replace("__POSTS__", json.dumps(posts, ensure_ascii=False))
            .replace("__ARTICLES__", json.dumps(articles, ensure_ascii=False))
            .replace("__CARD_IMG__", json_array(cards))
            .replace("__REF_IMG__", whole)
            .replace("__DOCS__", docs_html)
            .replace("__DOC_KEYS__", json_array([d[0] for d in DOCS]))
            .replace("__DOC_TITLES__", json_array([d[2] for d in DOCS])))

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(page)

    size = os.path.getsize(OUT)
    # Feed + sitemap dibangun dari sumber yang sama dengan halaman, jadi
    # artikel admin (bila articles.json ada) ikut muncul di keduanya.
    items = feed_items(posts, articles)
    write_rss(items)
    write_sitemap(items)
    write_robots()
    print(f"wrote {OUT}")
    print(f"  {size/1024:.0f} KB, {len(cards)} card images inlined")
    print("  rss.xml %d item, sitemap.xml %d url, robots.txt"
          % (len(items), count_sitemap_urls()))
    print("  %s di-embed (__MODULES__)" % ", ".join(MODULES))
    if posts:
        print("  %d artikel bawaan dari .freebuff/posts.json" % len(posts))
    if photos:
        inline = sum(1 for v in photos.values() if v.startswith("data:"))
        print("  %d foto dari photos.json%s" % (
            len(photos),
            " (%d data URL - index.html membengkak)" % inline if inline else ""))
    if articles:
        print("  %d artikel dari articles.json (baked permanen)" % len(articles))

    # Uji regresi konversi tautan Drive (tempel + simpan + bake) — berjalan
    # otomatis setiap build; gagal membuat exit kode build jadi non-zero.
    import test_drive_links
    test_drive_links.run(index_path=OUT)

    # Uji regresi editor (tab dasbor + urutan field + mode demo Drive) —
    # berjalan otomatis setiap build; gagal membuat exit kode build non-zero.
    import test_editor_regression
    test_editor_regression.run(index_path=OUT)

    # Uji tata letak responsif (tanpa overflow horizontal + label nav tidak
    # melipat di lebar ponsel/tablet/desktop). Dilewati dengan exit 0 bila
    # tidak ada browser headless di sistem ini.
    import test_layout_responsive
    test_layout_responsive.run(index_path=OUT)


def json_array(items):
    import json
    return json.dumps(items)


if __name__ == "__main__":
    main()