#!/usr/bin/env python
"""Replace demo copy blocks in site_shell.html with correct Indonesian prose.

Rewrites whole regions (rather than patching single tokens) so nothing can be
left half-replaced. Run once; idempotent.
"""
import re
import sys

P = ".freebuff/site_shell.html"

POSTS_NEW = '''  var POSTS = [
    {t:"Kerajaan Bali Sejarah Babad Bali",
     e:"Kerajaan ini berdiri selama beberapa abad, dan tidak sedikit pun dari catatan yang ada dapat diabaikan sebagai sekadar dongeng.",
     d:"21 Nov 2023", c:"Kerajaan Bali"},
    {t:"Candi dan Pura Kerajaan Babad Bali",
     e:"Bangunan suci candi dan pura tersebar di seluruh penjuru Bali, membentuk lanskap sakral yang masih utuh hingga kini.",
     d:"20 Nov 2023", c:"Candi"},
    {t:"Tokoh Sejarah Bali dalam Babad",
     e:"Peran seorang raja di Bali. Tokoh ini dikenal bukan hanya lewat namanya, tetapi juga menentukan arah kebijakan kerajaan.",
     d:"19 Nov 2023", c:"Tokoh Sejarah"},
    {t:"Namunan Botar dalam Sejarah dan Babad Bali",
     e:"Kumpulan kata yang tetap merujuk pada peristiwa masa lalu, membentuk lapisan makna yang tidak selalu tampak pada pembacaan pertama.",
     d:"18 Nov 2023", c:"listowa"},
    {t:"Soratirin: Jalan Lain Menuju Singgasana",
     e:"Soratirin menjelaskan asal-usul kerajaan sampai pada tataran wibawa di kidul, bukan sekadar simbol atau totem.",
     d:"17 Nov 2023", c:"Soratirin"},
    {t:"Candi Belerang dan Candi Suci di Bali",
     e:"Berderet candi yang berdiri rapi dengan pagar yang jelas, menandai batas-batas suci yang masih dijaga hingga kini.",
     d:"16 Nov 2023", c:"Candi"},
    {t:"Kerajaan di Tepi Goa: Batas dan Perbatasan",
     e:"Wilayah pedalaman yang dikelilingi tahura dan bertahan hingga kini, menjadi bukti cara kerajaan mengatur batas wilayah.",
     d:"15 Nov 2023", c:"Kerajaan"},
    {t:"Tokoh-Tokoh yang Mengubah Arah Sejarah",
     e:"Menyusuri kumpulan tokoh yang biasanya hanya disebut sekilas, padahal menentukan arah sejarah sebuah kerajaan.",
     d:"14 Nov 2023", c:"Tokoh Sejarah"}
  ];
'''

PROSE_NEW = '''    <div class="prose">
      <p>Kerajaan di Bali berdiri selama beberapa abad, dan tidak sedikit pun dari catatan
      yang ada dapat diabaikan sebagai sekadar dongeng. Yang tersisa hari ini bukan hanya
      nama-nama penguasa, melainkan juga tata ruang yang masih bisa dibaca.</p>

      <p>Jejak kerajaan di Bali tidak berhenti sebagai catatan tertulis. Ia terus hidup dalam
      struktur desa, tata ruang pura, dan cara masyarakat membagi air di tanah subak.</p>

      <h2>Kenapa Kerajaan Bali Penting?</h2>
      <p>Kedudukan Bali sebagai pusat kekuasaan tidak lahir seketika. Ia terbentuk melalui
      hubungan panjang antara pusat-pusat kekuasaan di nusantara dan komunitas lokal yang
      mempertahankan identitasnya sendiri.</p>

      <blockquote>Menurut naskah babad, urutan kerajaan tidak selalu dicatat dengan cara yang
      sama di setiap wilayah. Karena itu, pembaca sebaiknya merujuk pada beberapa sumber
      bila membandingkan satu peristiwa.</blockquote>

      <p>Ketika peristiwa-peristiwa besar mulai dicatat, catatan tertulis menjadi penting.
      Dua atau lebih sumber kemudian saling diperiksa untuk membentuk gambaran yang lebih utuh.</p>

      <h2>Babad sebagai Sumber</h2>
      <p>Babad bukan sekadar daftar raja. Ia adalah cara penulisan sejarah yang menolak
      kelaziman sumber yang lazim dipakai, sehingga memuat nilai, budi, dan penilaian moral dari zamannya.</p>

      <ul>
        <li>Silsilah penguasa dan hubungan kerabat.</li>
        <li>Peristiwa penting dan konflik antar daerah.</li>
        <li>Upacara dan tempat yang berkaitan dengan peristiwa.</li>
      </ul>

      <h2>Warisan yang Masih Terlihat</h2>
      <p>Jejak kerajaan hari ini dapat ditemukan pada candi, goa, serta tata letak desa
      tradisional yang masih dipertahankan hingga kini.</p>
    </div>
'''

HERO_SUB = '''        <p class="section__sub" style="margin:0 0 16px">Cari inspirasi liburan romantis di Bali? Temukan
          rekomendasi tempat paling puitis, aktivitas berdua yang unik, dan sunset terbaik
          di pulau dewata.</p>'''


def main():
    src = open(P, encoding="utf-8").read()

    src, n = re.subn(r"  var POSTS = \[.*?\n  \];\n", POSTS_NEW, src, flags=re.S)
    if n != 1:
        sys.exit(f"POSTS block not replaced (n={n})")

    src, n = re.subn(r'    <div class="prose">.*?\n    </div>\n', PROSE_NEW, src, flags=re.S)
    if n != 1:
        sys.exit(f"prose block not replaced (n={n})")

    src = re.sub(r'        <p class="section__sub" style="margin:0 0 16px">.*?</p>\n',
                 HERO_SUB + "\n", src, flags=re.S)

    src = re.sub(r'<p class="section__sub">Karya terbaru.*?</p>\n',
                 '<p class="section__sub">Karya terbaru dari redaksi Bali Kisah</p>\n', src)

    src = src.replace("  POSTS.forEach(function(p,i){ p.chip = p.c; });\n", "")

    open(P, "w", encoding="utf-8").write(src)

    out = open(P, encoding="utf-8").read()
    cjk = [(i, l) for i, l in enumerate(out.split("\n"), 1)
           if re.search(r'[\u3000-\u9fff\uff00-\uffef]', l)]
    print(f"blocks replaced OK; CJK lines remaining: {len(cjk)}")
    for i, l in cjk:
        print("  ", i, l[:120])


if __name__ == "__main__":
    main()