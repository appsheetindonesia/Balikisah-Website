# Run Doc — Bali Kisah Dokumen

## Mode: standalone HTML (NO SERVER)

Workspace ini berisi dokumen (.md), bukan aplikasi. Tidak ada `package.json`,
tidak ada lockfile, tidak ada framework, tidak ada dependency runtime.

Tidak ada dev server yang perlu dijalankan, tidak ada port, tidak ada pid.
File yang dibuka browser adalah:

```
D:\Balikisah website\index.html   (~705 KB, self-contained, single file)
```

Preview didaftarkan dengan `register_preview` memakai `htmlPath` absolut ke
`index.html` — **tanpa proses, tanpa port, tanpa pid**. Semua CSS, JS, gambar
(base64), dan 9 dokumen (hasil render python-markdown) sudah inline di dalam
satu file — tidak ada request jaringan kecuali font Google bila pengguna
mengaktifkannya. Setelah `index.html` dibangun ulang, tab pratinjau cukup
di-reload untuk melihat versi terbaru (sumber file tetap terbaca).

### Navigasi antar view (5 Okt 2026)

Bar pratinjau gelap di atas halaman sudah **dihapus** atas permintaan pengguna:
menu situs sendiri yang dipakai untuk berpindah view — logo & `Stonian` ->
beranda, `Kategori`/`Kenajaan` -> arsip, `Blog` -> artikel, `Kontak` -> dokumen.
View alat (Bandingkan, Dokumen, Kelola Foto) dijangkau lewat strip kecil
`.demo-nav` di ujung tiap view (bertanda `aria-current` sesuai view aktif), dan
pencarian dokumen kini berada di sidebar view Dokumen bersama tautan
`Kembali ke arsip`.

### Panel admin — tulis artikel & unggah foto (5 Okt 2026)

Di pojok kanan atas setiap header ada tombol **Admin** (`data-admin-toggle`). Klik membuka
dialog login (demo sisi klien — bukan proteksi produksi; nama + sandi apa pun ≥4 karakter).
Setelah login, muncul:

- **Panel admin** tipis di bawah header, semua view.
- **View Dasbor Redaksi** (`view-admin`, dijangkau lewat tombol panel / link demo-nav "Admin"):
  - Tab **Tulis artikel**: judul, kategori, penulis, ringkasan, isi; panel foto cover yang
    bisa diisi dari berkas komputer / tautan / Google Drive (pakai mesin `PHOTOS` yang sama
    dengan view Kelola Foto).
  - Tab **Daftar artikel**: artikel yang pernah disimpan, dengan tombol Edit / Hapus.
- Artikel yang disimpan masuk `localStorage` (`balikisah.articles.v1`) dan langsung
  tampil di kartu arsip, beranda, dan daftar terkait. Tombol **Ekspor articles.json**
  menghasilkan `.freebuff/articles.json`; jalankan `build_site.py` untuk mem-bake permanen
  (placeholder `__ARTICLES__`) — dibaca build dan langsung muncul di `index.html` tanpa
  perlu login.

Catatan: halaman artikel (`view-article`) masih statis; artikel admin tampil lewat kartu
(dengan foto cover) di arsip/beranda. "Unggah ke Drive" dari dasbor memakai koneksi Drive
yang sama dengan view Kelola Foto (butuh `pmClientId` di-connect dulu).

### Keputusan UIRD yang sudah dikonfirmasi (5 Okt 2026)

Empat keputusan yang tadinya menggantung di UIRD §16 kini **ditutup** dan sudah
diterapkan ke situs + dokumen (UIRD §16, PRD Lampiran A PD-01/02/09/10, SRS
SRS-UI-09..12, FRD FRD-08.1/08.2/08.3 + FRD-08.10/08.11):

| # | Keputusan | Terapan di situs |
|---|---|---|
| UIRD-01 | Identitas `balikisah.com` untuk **semuanya** | wordmark, `<title>`, kolom `Eksplor balikisah.com`, baris copyright |
| UIRD-02 | Bahasa CTA = Indonesia penuh | CTA `Hubungi Kami`, nav `Kontak` (tidak ada label Inggris tersisa) |
| UIRD-04 | Footer **terang** | `background: var(--ivory)`, judul `--ink-900`, teks `--ink-400`, pemisah `--hairline` (kontras 4,7-16,8:1) |
| UIRD-05 | Halaman kanonik = **Beranda** | `#view-home` aktif saat muat; `#view-archive` disembunyikan |

Deviasi yang timbul karena keputusan ini (logo teks, `Kenajaan`->`Kerajaan`,
`Contact`->`Kontak`, kotak CTA 122x38 -> 149,8x35, footer terang) dicatat sebagai
daftar "deviasi yang disengaja" di view **Bandingkan** dan di UIRD §5/§16.

Sejak 5 Okt 2026 view Bandingkan juga **menandai langsung** titik-titik deviasi
pada gambar referensi: pin bernomor 1–4 (logo, nav ke-2, nav terakhir, kotak
CTA) plus legenda pintas di bawah gambar dengan nomor yang sama seperti butir
daftar. Pin diletakkan dengan persentase koordinat gambar referensi
(756 × 425) sehingga tetap menempel saat gambar mengecil; butir 5–6 (footer,
halaman default) tidak tampak di gambar dan ditandai sebagai chip redup.
Hover pada chip/butir menyorot pin terkait.

## Cara mereproduksi artefak

Artefak yang *uncommitted* dan dibutuhkan checkout baru:

1. **Prasyarat**: Python 3.13 (atau lebih baru) di PATH.
2. **Dependency**: hanya `markdown` (dipakai `build_site.py`).
   Pillow hanya dibutuhkan untuk crop gambar dari referensi, dan hasilnya
   sudah tertanam sebagai base64 di dalam `index.html`, jadi **tidak perlu
   reinstall** bila hanya ingin membuka pratinjau.

   ```bash
   python -m pip install markdown
   ```

3. **Gambar referensi**: `WhatsApp Image 2026-10-05 at 09.50.58.jpeg` (756×425)
   adalah sumber semua token terukur. File ini wajib ada di checkout.

4. **Build ulang** — jalankan dari root workspace:

   ```bash
   python .freebuff/build_site.py
   ```

   Skrip ini: memotong logo + 8 thumbnail kartu + frame referensi dari JPEG,
   merender 9 file `.md` dengan python-markdown, lalu menyuntikkannya ke
   `.freebuff/site_shell.html` melalui placeholder `__LOGO__`, `__CARD_IMG__`,
   `__REF_IMG__`, `__DOCS__`, `__DOC_KEYS__`, `__DOC_TITLES__`.

   Selalu build ulang setelah mengubah dokumen ATAU `site_shell.html`.

5. **Verifikasi rutin: dokumen + chrome situs** (jalankan setiap selesai
   mengubah dokumen ATAU `site_shell.html`):

   ```bash
   python .freebuff/build_site.py && python .freebuff/verify_docs.py
   ```

   Build dulu supaya `index.html` selalu sesuai shell terbaru, baru verifikasi (termasuk
   pemeriksaan chrome atas artefak hasil build).

   Sembilan pemeriksaan. Delapan atas 9 dokumen: nama file, UTF-8, karakter
   asing (CJK/Hangul/Cyrillic), tautan silang, anchor internal, urutan 18
   bagian PRD, integritas baris tabel, dan pagar kode + token UIRD. Yang
   kesembilan menurunkan `verify_chrome.py` untuk memeriksa label lama pada
   chrome situs. Keluar dengan status 0 hanya bila semuanya bersih.

   ### Pemeriksaan label lama (chrome situs)

   ```bash
   python .freebuff/verify_chrome.py                # atas index.html
   python .freebuff/verify_chrome.py --self-test    # menguji alatnya sendiri
   ```

   **Chrome** = seluruh `index.html` di luar `<article class="doc">`; isi 9
   artikel dokumen sengaja memuat label lama sebagai fakta referensi, jadi
   diabaikan. Lima label dipantau beserta penggantinya:
   `Contact us` -> `Hubungi Kami`, `Contact` -> `Kontak`,
   `Bali Kisah`/`BaliKisah` -> `balikisah.com`, `Kenajaan` -> `Kerajaan`.

   Sebuah kemunculan hanya lolos bila berada di dalam pemetaan utuh
   `<code>LAMA</code> -> <code>PENGGANTI</code>` (bentuk baris "deviasi yang
   disengaja" di view Bandingkan). Regresi di tombol, nav, judul, atau footer
   tidak berbentuk begitu, sehingga tampil sebagai
   `GAGAL [label] baris N: ...konteks...` dan keluar dengan status 1 —
   yang langsung menggagalkan `verify_docs.py`.

   `--self-test` membuktikan alat bekerja dua arah tanpa mengubah artefak:
   chrome bersih harus LULUS, sedangkan label yang disuntikkan (CTA, nav,
   logo, camelCase, `Kenajaan`, atau pemetaan tanpa tanda panah) harus GAGAL.

6. **Buka** `index.html` di browser, atau daftarkan ulang lewat
   `register_preview` dengan `htmlPath` absolut yang sama
   (`D:\Balikisah website\index.html`). Tidak ada server/port yang perlu
   dihidupkan; `register_preview` menyajikan berkas itu langsung dan
   memuat ulang dari sumber saat berkas berubah.

   Catatan tema: bila tema webview mengikuti `prefers-color-scheme: dark`,
   situs memuat dalam mode gelap (perilaku otomatis yang benar). Untuk
   memaksa mode terang pada pratinjau, klik tombol ◐ di header atau set
   `localStorage["balikisah.theme"] = "light"`.

## Kelola Foto (fitur baru, 5 Okt 2026)

View keenam di toolbar pratinjau, **Kelola Foto**, mengatur sumber foto tiap artikel:

1. **Tautan** — tempel URL gambar atau tautan Google Drive
   (`/file/d/<ID>/view`, `?id=<ID>`); tautan Drive dinormalisasi otomatis ke
   `https://lh3.googleusercontent.com/d/<ID>=w1600`. Tautan Dropbox `?dl=0`
   diubah ke `?raw=1`.
2. **Berkas lokal** — diperkecil ke maks. 1600 px (JPEG kualitas 0,85) lalu
   disimpan di `localStorage` browser. Bersifat lokal: tidak ikut ke `index.html`.
3. **Upload ke Google Drive** — OAuth implicit via Google Identity Services,
   scope `drive.file`, unggah multipart ke Drive API, lalu izin `anyone:reader`.
   Butuh **OAuth Client ID** (Web application) dari pengelola dan origin
   pratinjau (mis. `http://127.0.0.1:59613`) didaftarkan sebagai
   *Authorized JavaScript origin*; Google Drive API harus aktif di project itu.

Agar permanen untuk semua pembaca: klik **Ekspor photos.json**, simpan sebagai
`.freebuff/photos.json` (objek `{judul artikel: url}`), lalu jalankan
`python .freebuff/build_site.py`. Build akan menyuntik peta itu sebagai
`__PHOTO_MAP__` dan mencetak jumlah foto yang di-bake.

View lama (arsip, beranda, artikel, bandingkan, dokumen) tidak berubah; foto
bawaan tetap hasil crop dari screenshot referensi selama belum ada override.

## Halaman artikel per slug (5 Okt 2026)

`view-article` tadinya satu halaman statis. Sekarang isinya dirakit dari data
setiap artikel — yang bawaan maupun yang ditulis admin di Dasbor Redaksi —
sehingga setiap artikel punya alamatnya sendiri:

- **Slug** = judul yang dibersihkan (`slugify()`): huruf kecil, tanda baca jadi
  `-`, diakritik dibuang, duikat diberi akhiran angka (`-2`). Disimpan di
  `ART[i].slug` oleh `assignSlugs()` setiap `rebuildArt()`.
- **Alamat**: `?post=<slug>` (tulis lewat `history.replaceState`) atau
  `#/post/<slug>` (cadangan bila `replaceState` ditolak, mis. berkas `file://`).
  Saat muat, `slugFromLocation()` membaca keduanya; `hashchange` juga
  didengarkan. Pindah ke view lain menghapus parameter lewat `clearPostParam()`.
  Slug yang tidak dikenal jatuh ke artikel bawaan pertama.
- **Kartu** menyertakan `data-post="<slug>"`; klik kartu memanggil
  `openArticle(slug)` → `renderArticle(slug)` + `show("article")`.
- **`renderArticle()`** mengisi `#artHeadCrumb` (Beranda / kategori / judul),
  `#artHeadTitle`, `#artHeadMeta` (penulis · tanggal · lama baca), `#artHeadHero`
  (foto cover, sama dengan yang dipakai kartu), `#artHeadProse`, dan
  `#relatedGrid` (4 artikel, bila memungkinkan kategori sama). `document.title`
  ikut berubah.
- **Isi** ditulis dengan markdown-lite (`renderBody()`): baris kosong = paragraf,
  `## `/`### ` = judul, `> ` = kutip, `- `/`* ` = daftar, `![alt](url)` = gambar
  (baris sendiri dibungkus `<figure>`), `[teks](https://…)` = tautan, `**tebal**`.
  Semua teks di-escape dulu; URL gambar hanya diterima kalau `http(s)` atau
  `data:image`, dan tautan Google Drive otomatis dinormalkan lewat
  `normalizePhotoLink()`. Artikel tanpa isi memakai `BODY_DEFAULT` (isi lama).
- Cover yang gagal dimuat menampilkan catatan di `#artImgNote`, supaya penulis
  tahu apakah tautannya salah atau berkas Drive-nya belum dibagikan publik.

## Ambil gambar dari Google Drive (bukan hanya unggah)

Dasbor Redaksi gained blok **Ambil gambar dari Google Drive**
(`#artDriveBrowse` → `#artDrivePicker`):

1. Sambungkan Google Drive dulu di view Kelola Foto (butuh OAuth Client ID).
2. Tombol **Pilih gambar dari Drive** memanggil `driveListImages()` —
   `files.list` dengan `q="mimeType contains 'image/' and trashed = false"`,
   ditambah `'<FolderID>' in parents` bila Folder ID diisi, diurutkan
   `modifiedTime desc`, 60 berkas pertama.
3. Tiap baris punya tiga aksi: **Publik** (`driveShare()` → izin
   `anyone:reader`), **Sisipkan** (menyisipkan `![nama](url)` pada posisi kursor
   di `#artBody`), dan **Cover** (pasang `PHOTOS[judul]`, segarkan pratinjau).
4. **Cakupan akses** (`#pmScope`): `drive.file` (hanya berkas milik aplikasi
   ini — pilihan paling sempit) atau `drive.readonly` (baca seluruh Drive).
   Pilihan disimpan di `localStorage` `balikisah.drive.scope`. Kalau
   `files.list` ditolak 403, pesan error menyebut opsi sambungkan ulang dengan
   cakupan `drive.readonly`.

Foto Drive yang sudah menjadi publik bisa dibuka lewat
`https://lh3.googleusercontent.com/d/<ID>=w1600`; berkas privat akan gagal
dimuat, dan halaman artikel memberi tahu lewat catatan di atas.

**Batasan yang belum teruji:** jalur OAuth Google (login, `files.list`,
`permissions`) belum pernah dijalankan sungguhan karena tidak ada OAuth Client
ID di lingkungan ini. Yang sudah diuji: keadaan "belum terhubung" (pesan
benar), normalisasi tautan Drive, URL thumbnail, dan kedua aksi baris
(Sisipkan/Cover) memakai baris contoh. `build_site.py` kini menggabungkan field
`photo` dari `articles.json` ke peta foto yang di-bake, sehingga tautan Drive
tetap permanen di `index.html` setelah ekspor.

## Perbaikan editor Tulis artikel (oktober 2026)

Perbaikan setelah laporan "fungsi menulis artikel masih berantakan" +
"ambil foto dari Google Drive belum berjalan":

1. **Glyph toolbar** — tombol `data-md` di markup shell memakai literal
   `\u201d` / `\u1f517` (escape JS di dalam HTML, jadi tampil apa adanya).
   Diganti karakter asli: `“”` `• •` `🔗` `🖼` `―`. Opsi "Judul A–Z"
   di `#listSort` ikut diperbaiki.
2. **Tag cepat kosong** — `renderTagPick()` cuma dipanggil saat ganti tab;
   kini ikut dipanggil di `window.__editorSync` (mod_admin), jadi chip tag
   langsung terisi saat editor dibuka. `.chips--pick` diberi `min-height`
   supaya barisnya tidak kolaps.
3. **Lipatan SEO** — `#artSeoFold` dapat `margin-top:4px` supaya tidak
   menempel rapat di bawah "Tag cepat".
4. **Pratinjau isi kosong** — `.ed-prev` kini punya `min-height:120px` dan
   pesan placeholder lewat `::before` saat `.prose:empty`.
5. **Drive dari dalam editor** — tombol `#artDriveBrowse` dan
   `#artPhotoDrive` (Unggah ke Drive) tidak lagi hanya menampilkan error
   merah di `#artState`. Mereka memanggil `showDriveConnect()` yang membuka
   `#artDrivePicker` + blok `#artDriveConnect` berisi kolom Client ID
   (`#artDriveCid`, prefilled dari `balikisah.drive.clientId`), tombol
   **Hubungkan sekarang** (`connectDrive()` langsung dari editor), tautan
   ke panel Kelola Foto, dan pengingat fallback: tempel tautan
   `drive.google.com/file/d/…` di kolom "Atau tautan / Google Drive".
   Ada juga tombol **Panduan koneksi** (`#artDriveOpenSetup`).
6. Pesan sukses simpan memakai `&` biasa (sebelumnya `&amp;` tampil literal
   karena `setStatus` memakai `textContent`).

Diuji di browser: glyph toolbar benar, 15 chip tag tampil, lipatan SEO
terpisah, pratinjau kosong menampilkan placeholder, klik Drive memblok
koneksi + pesan tepat, `artState` bersih, simpan artikel sukses, konsol
tanpa error. OAuth sungguhan tetap belum teruji (tanpa Client ID).

## Mode demo Drive (oktober 2026)

OAuth Google tidak bisa diuji tanpa Client ID, jadi alur "ambil foto dari
Drive" kini punya mode demo yang berjalan penuh tanpa OAuth:

1. **Aktivasi** — di editor Tulis artikel, blok Drive punya tombol
   **Mode demo** (`#artDriveDemo`, di samping "Pilih gambar dari Drive")
   dan tombol **Coba mode demo** (`#artDriveDemoBtn`) di dalam blok
   koneksi (`#artDriveConnect`). Keduanya memakai `enterDriveDemo()`.
2. **Sumber gambar** — `DEMO_IMAGES` di `site_shell.html`: 6 foto pura
   di Bali dari Wikimedia Commons (bebas pakai), dilayani lewat
   `thumb.wikimedia.org` (1280px untuk isi/cover, 500px untuk thumbnail).
   Bentuk barisnya sama dengan hasil Drive sungguhan: `{id, name, when,
   url, thumb, demo:true}`.
3. **Alur teruji penuh** — tombol **Sisipkan** menyisipkan
   `![nama.jpg](url)` ke `#artBody` (kursor) dan memicu event `input`
   supaya pratinjau + penghitung ikut tersinkron; tombol **Cover**
   menulis `PHOTOS[key]={url,src:"drive"…}`, memperbarui pratinjau foto,
   dan mengisi kolom tautan. Tombol **Publik** disembunyikan untuk baris
   demo (tidak perlu share).
4. **Keluar** — tombol yang sama berubah label menjadi "Keluar dari mode
   demo" (`exitDriveDemo()`), blok koneksi tampil kembali. "Panduan
   koneksi" saat demo aktif juga keluar dari demo. Mengklik "Hubungkan
   sekarang" otomatis mematikan demo. Status demo (`DRIVE_DEMO`) hanya
   sesi — tidak disimpan di localStorage.
5. **Lintas panel** — panel Media (`#mediaDrive`) ikut memakai demo saat
   aktif (`BK.driveDemoActive()`), dan tombol "Unggah ke Drive" memberi
   pesan ramah bahwa unggah butuh koneksi sungguhan. Baris media memakai
   `f.thumb || driveThumbUrl(f.id,400)` supaya thumbnail demo benar.

Diuji di browser (tanpa OAuth): daftar 6 gambar muncul + thumbnail termuat,
Sisipkan menambah markdown di body dan pratinjau menampilkan `<img>`,
Cover memperbarui `#artPhotoPrev` (termuat) + kolom tautan, keluar/masuk
demo dari kedua tombol berfungsi, panel Media mengisi 6 gambar contoh,
konsol tanpa error. Data uji dibersihkan dari localStorage.

## Tata letak form Tulis artikel (oktober 2026)

Disusun ulang ala editor WordPress, tanpa memindahkan ID apa pun (JS tetap
aman):

1. **Urutan field** — kolom utama kini flex column dengan nilai `order`
   inline: Judul (10) → Tautan permanen/slug (15) → Isi artikel + toolbar
   (20) → petunjuk format (24) → baris Simpan (26, termasuk notifikasi draf
   `#artDraftState`) → Pratinjau & Revisi (30) → lalu meta bawah: Ringkasan
   (40) → Kategori & penulis (50) → Tag + tag cepat (60/62) → Format &
   pembaruan (70) → lipatan SEO (80). Setiap bagian meta punya judul
   pemisah `.ed-sec__h` (garis atas + huruf kapital).
2. **Sidebar Publikasi** — blok **Status** (pill Terbit/Draf/Terjadwal/
   Privat + tanggal terbit) dipindah dari kolom utama ke sidebar, persis di
   bawah heading "Publikasi" dan di atas tombol aksi/ foto cover — seperti
   kotak Publish WordPress.
3. **Bug tab dasbor (penting)** — CSS lama hanya menampilkan pane dengan
   atribut literal `hidden="false"`, tapi JS memakai `el.hidden = boolean`
   yang MENGHAPUS atribut → setelah sekali klik tab, pane aktif jadi
   `display:none` (tidak terlihat). Diperbaiki dengan
   `.dash__pane:not([hidden]){display:block}`. Posisi turun-an `#artDraftState`
   dan kotak `draft-restore` juga diberi `order` (26/25) supaya tetap dekat
   tombol Simpan.
4. **Mobile (≤640px)** — tab dasbor jadi scroll horizontal (`nowrap` +
   `overflow-x:auto`), tombol toolbar min 34×32px (target sentuh), tombol
   `.btn-row .btn` melebar (flex 1), baris Drive (`dp-row`) wrap dengan tombol
   aksi selebar penuh, padding dasbor dirapatkan. ≤940px sidebar menumpuk
   di bawah kolom utama (aturan lama, tetap berlaku).

5. **Kontras mode gelap** — diukur dengan rasio WCAG: input kolom utama
   (slug/tag/penulis) sebelumnya 1.1–2.2:1 (teks terang di atas putih,
yaris tak terbaca), tab dasbor/pill status/ghost button/chip 2.19:1.
   Ditambah aturan `html[data-theme="dark"]` untuk `.field input/select`
kolom utama, `.dash__tab`, `.ed-status__pill`, `.chips--pick button`, dan
   `.btn--ghost` → kini 7.57–11.74:1. Mode terang tidak berubah
   (18.74:1 input, 14.31:1 ghost, 4.94:1 tab) karena aturan dibatasi
   selektor `[data-theme="dark"]`.

Diuji di browser: 1440×900 (grid 762px+320px, sidebar di kanan, status di
atas foto cover, jarak judul→slug 34px) dan 390×844 (1 kolom, tanpa
overflow horizontal, urutan field sama, tab scroll). Semua pane
(write/list/media/terms) tampil-normal saat tab diklik; alur mode demo
Drive + simpan artikel tetap sukses; konsol tanpa error. Data uji dibersihkan.

## Normalisasi tautan Google Drive di isi artikel (oktober 2026)

Semua tautan Google Drive yang berakhir di isi artikel otomatis menjadi URL
gambar lh3 (`https://lh3.googleusercontent.com/d/<ID>=w1600`):

1. **Saat menempel** — event `paste` pada `#artBody` memanggil
   `normalizeDriveLinksInText()` (baru, di dekat `normalizePhotoLink`):
   tautan `/file/d/<ID>/…` dan `?id=<ID>` (drive/docs.google.com) diganti
   sebelum masuk textarea, lengkap dengan pesan status "N tautan Google
   Drive ditempel sebagai URL gambar lh3.". Tanda baca di akhir kalimat
   dipertahankan; tautan non-Drive dan lh3 yang sudah jadi tidak disentuh.
2. **Saat menyimpan** — `collectEntry()` (dipakai Simpan + Simpan draf)
   menjalankan normalisasi yang sama ke `body.value` sebelum entri
   disimpan, memicu event `input` (pratinjau ikut tersinkron), lalu pesan
   sukses simpan ditambah catatan "N tautan Google Drive diubah ke URL
   gambar lh3." (`driveFixNote()`). Jaring pengaman untuk jalur ketik
   manual, draf lama, dan impor.
3. **Race draf** — `clearDraft()` kini ikut `clearTimeout(draftTimer)`
   supaya autosave 1.2 detik tidak menulis ulang draf setelah simpan
   (sebelumnya draf bisa muncul lagi setelah tombol Simpan).
4. Render halaman artikel tetap memakai `safeImageUrl()` →
   `normalizePhotoLink()`, jadi tautan lama yang tersimpan pun tampil
   benar tanpa migrasi.

Diuji di browser: tempel URL polos & markdown `![…](…)` → keduanya jadi
lh3 di textarea + pesan status; simpan dengan 2 tautan Drive terketik →
isi tersimpan bersih (0 sisa `drive.google.com`), catatan muncul, non-Drive
diabaikan, tanda kalimat utuh; simpan tanpa tautan Drive → tanpa catatan;
halaman artikel menampilkan `<img>` lh3; draf tidak muncul ulang setelah
simpan (1.5 detik tunggu); konsol tanpa error. Data uji dibersihkan.

## Render URL gambar lh3 telanjang (oktober 2026)

Sebelumnya hanya `![alt](url)` yang jadi gambar; URL lh3 polos di isi
artikel tampil sebagai teks biasa. Kini:

1. **`inlineMd()` di-refactor** memakai teknik placeholder: potongan HTML
   yang sudah jadi (`<img>` hasil `![]()`, `<a>` hasil `[teks](…)`) diparkir
   dulu supaya langkah berikutnya tidak memprosesnya dobel (URL di dalam
   `src="…"`/`href="…"` tidak bisa kena regex telanjang).
2. **URL telanjang → `<img>`** — pola: `lh3.googleusercontent.com/d/<ID>[=suffix]`
   dan tautan Drive/Docs mentah (`/file/d/…`, `?id=…`) → `safeImageUrl()`
   (konversi lh3) lalu jadi `<img class="prose__img">`. Tanda baca di akhir
   kalimat dipertahankan; tanda kurung tidak tertelan (kelas karakter
   mengecualikan `)`); URL tanpa ID/ketidakdikenalan dibiarkan sebagai teks.
3. **Baris yang hanya berisi URL gambar** menjadi `<figure>` (sama seperti
   baris `![]()`); di tengah paragraf menjadi `<img>` inline dalam `<p>`;
   ikut berfungsi di dalam daftar `- ` dan kutipan `>`.
4. **Yang tidak berubah**: `[teks](lh3)` tetap tautan, `![](lh3)` tetap
   gambar dengan alt, URL non-gambar (mis. example.com) tetap teks biasa.
5. Pratinjau editor ikut otomatis karena memakai `BK.renderBody()` yang sama.

Diuji di browser (9 kasus render + pratinjau + halaman artikel): figure
baris telanjang, img inline dalam kalimat, daftar & kutipan, anchor utuh,
markdown-img utuh, Drive mentah → lh3, tanda kalimat/kurung utuh, URL
non-gambar tetap teks, placeholder tidak bocor; pratinjau editor dan
halaman artikel tersimpan keduanya menampilkan 2 `<img>` lh3; konsol
tanpa error. Data uji dibersihkan.

## Normalisasi Drive di Ringkasan/SEO + impor articles.json (oktober 2026)

Perluasan dari normalisasi isi artikel (lihat atas) ke kolom meta dan
jalur impor:

1. **Saat menyimpan** — `collectEntry()` kini juga menjalankan
   `normalizeDriveLinksInText()` pada Ringkasan (`#artExcerpt`), Judul SEO
   (`#artSeoTitle`), Deskripsi meta (`#artSeoDesc`), dan Bio penulis
   (`#artBio`); hitungan digabung ke catatan "N tautan Google Drive
   diubah ke URL gambar lh3.". Field yang berubah memicu event `input`
   supaya penghitung karakter ikut sinkron.
2. **Saat menempel** — helper `wireDrivePaste(el)` dipakai untuk `#artBody`
   + keempat field meta di atas (splicing di posisi kursor, sama seperti
   perilaku tempel bawaan).
3. **Impor runtime** — `importAll()` di `mod_admin.js` (tombol "Impor
   seluruh situs") memetakan tiap artikel: `body`, `excerpt`, `seoTitle`,
   `seoDesc`, `authorBio` dinormalisasi via `BK.normalizeDriveLinksInText`
   (baru diekspor dari shell), toast dilengkapi jumlah konversi; penghitung
   `window.__importDriveFixes` di-reset tiap impor agar tidak basi.
4. **Impor build** — `build_site.py` punya `normalize_drive_links()`
   (padanan Python: regex `/file/d/<ID>` dan `?id=<ID>` → lh3) yang
   dijalankan `load_articles()` pada field `body`, `excerpt`, `photo` dari
   `.freebuff/articles.json` sebelum di-bake — tanda baca akhir dipertahankan,
   Drive tanpa ID dibiarkan.

Diuji di browser: tempel Drive ke Ringkasan → + pesan; ketik 3 URL mentah
di kolom SEO lalu Simpan → entri tersimpan semuanya lh3, catatan "3 tautan"
+ isi tidak tersentuh; impor `balikisah-situs.json` berisi 5 URL mentah →
`BK.ARTICLES` bersih + toast "Impor selesai. 5 tautan …" + tersimpan ke
localStorage. Diuji di build: `articles.json` sementara (4 URL, termasuk
titik akhir & field foto) → `index.html` berisi 4 lh3 dan 0 sisa URL Drive
mentah (assert exit 0); berkas sementara dihapus dan build dijalankan ulang
(kembali ke keadaan semula, `verify_docs`+`verify_chrome` exit 0).
Konsol tanpa error; data uji dibersihkan.

## Uji regresi konversi tautan Drive (oktober 2026)

Skrip `.freebuff/test_drive_links.py` memeriksa konversi tautan Google
Drive — jalur **tempel** dan **simpan** — di setiap build:

1. **Otomatis tiap build** — hook di akhir `build_site.py main()` memanggil
   `test_drive_links.run(index_path=OUT)` setelah `index.html` ditulis;
   gagal = exit kode build jadi non-zero. Mandiri:
   `PYTHONIOENCODING=utf-8 python .freebuff/test_drive_links.py`
   `[path-index.html] [--verbose]`.
2. **Wiring (11 cek string di index.html)** — `wireDrivePaste(body/excerpt/
   elSeoTitle/elSeoDesc/elBio)`, `normalizeDriveLinksInText(body.value)`
   di `collectEntry`, loop meta `[excerpt, elSeoTitle, elSeoDesc, elBio]`,
   `el.value = r.text`, pemetaan impor runtime `normalizeDriveLinksInText(a[k])`,
   dan pesan status tempel/simpan — salah satu kait terhapus = uji gagal.
3. **Fungsi JS asli di Node** — `normalizePhotoLink` +
   `normalizeDriveLinksInText` diekstrak dari `index.html` (bukan disalin)
   lalu dijalankan via `node`: 9 kasus tempel (URL polos, `?id=`, markdown
   gambar/tautan, titik kalimat, lh3 sudah jadi, non-Drive, Drive tanpa ID,
   campuran) + 3 kasus simpan (4 field meta + hitungan gabungan, idempoten,
   tanpa Drive = tanpa perubahan). **Skrip JS sementara ditulis ke folder
   tmp SISTEM** (`tempfile.mkdtemp(prefix="bk_drive_test_")`) — bukan di
   dalam proyek — dan **dihapus setelah uji** (`finally: shutil.rmtree`),
   jadi tidak ada jejak skrip uji di folder proyek maupun di artefak build
   (index.html/rss.xml/sitemap.xml/robots.txt tidak memuat string uji apa pun).
4. **Jalur bake** — `build_site.normalize_drive_links()` diuji (path id,
   `?id=`, titik dipertahankan, Drive tanpa ID, non-string).
5. **Terbukti bisa gagal** — uji negatif pada salinan sementara: (a) hapus
   satu string wiring → exit 1 + `FAIL wiring: paste Ringkasan`;
   (b) rusak fungsi hasil ekstrak → exit 1 + 8 kasus JS `FAIL`.
   Artefak asli tidak disentuh.
6. **Mode `--verbose`** — saat ada kegagalan, isi fungsi JS hasil ekstrak
   (`normalizePhotoLink` + `normalizeDriveLinksInText`) beserta harness ujinya
   dicetak dengan nomor baris (`  1 | ...`) untuk diagnosis, lalu exit 1.
   Tanpa kegagalan, flag ini tidak mengubah output. Pemakaian:
   `python .freebuff/test_drive_links.py [path-index.html] --verbose`.
   Terbukti: pada salinan dengan konversi dimatikan → exit 1, 11 FAIL JS,
   dump 153 baris bernomor muncul; tanpa flag → exit 1 tanpa dump.
   Sekaligus diperbaiki: argumen posisi path `index.html` kini benar-benar
   dipakai (sebelumnya diabaikan sehingga uji selalu membaca index utama).

## Uji regresi editor (oktober 2026)

Skrip baru `.freebuff/test_editor_regression.py` — pola sama dengan
`test_drive_links.py` (wiring string + JS asli di Node + `--verbose`),
menutup tiga area editor:

1. **Tab dasbor** — 8 tab (`data-dash-tab`: write/list/media/terms/comments/
   trash/appearance/settings), 8 id pane `dash*`, handler klik
   `querySelectorAll("[data-dash-tab]")`, pemetaan pane lengkap,
   `aria-selected`, `el.hidden = k !== which`, hook `window.__dashTab`.
2. **Urutan field editor** — 12 titik order (10 Judul → 15 Slug → 20 Isi →
   24 hint → 26 Simpan → 30 Pratinjau/Revisi → 40 Ringkasan → 50 Kategori &
   penulis → 60 Tag → 62 Tag cepat → 70 Format → 80 SEO) dicek ada +
   monotonic non-turun (23 cek).
3. **Mode demo Drive** — wiring: flag `DRIVE_DEMO`, data `DEMO_IMAGES`,
   tombol `artDriveDemo`/`artDriveDemoBtn`, fungsi masuk/keluar demo, label
   tombol, pesan status, `BK.driveDemoActive`; JS di Node: struktur
   `DEMO_IMAGES` (≥6, semua field, URL Wikimedia, thumb < url),
   `driveRowHtml` (baris demo = `data-demo="1"` **tanpa** tombol Publik,
   tetap punya Sisipkan+Cover; baris non-demo punya Publik),
   `driveListImages` jalur demo resolve `DEMO_IMAGES` & non-demo tanpa
   token → reject. `esc`/`escAttr`/`driveThumbUrl` di-stub di Node (aslinya
   memakai DOM).

Total: **60 wiring + 23 order + 11 JS = 94 cek**, semua LULUS pada build
terbaru. Hook di akhir `build_site.py main()` — build exit non-zero bila
uji ini gagal. Mandiri:
`PYTHONIOENCODING=utf-8 python .freebuff/test_editor_regression.py
[path-index.html] [--verbose]`.

Terbukti bisa gagal (uji negatif pada salinan, artefak asli utuh):
(a) tab media dihapus → exit 1 `wiring hilang: tab: Media`;
(b) `driveRowHtml` dikorupsi (demo jadi punya share) → exit 1 FAIL JS;
(c) `driveListImages` demo dirusak → exit 1. Mode `--verbose` mencetak
`driveRowHtml`/`driveListImages`/`DEMO_IMAGES` bernomor baris. Skrip JS
sementara ke tmp sistem, dihapus `finally` — nol residu di proyek/artefak.

Hasil saat ini: 29 cek LULUS (11 wiring + 12 JS + 5 bake + ringkasan),
build exit 0 dengan output uji tercetak di akhir build.

## Peringatan tautan Drive tanpa ID (oktober 2026)

Tautan Drive/Docs yang tidak punya ID valid (folder, `/uc?export=…`,
`/file/<id>` tanpa `/d/`) tidak bisa diubah ke lh3 — kini diberi peringatan
di beberapa titik:

1. **Live di editor** — `findBadDriveLinks()` (baru) menghitung tautan
   tanpa ID pada isi artikel, Ringkasan, Judul/Deskripsi SEO, dan Bio;
   baris `#artDriveBad` (order 27, tepat di bawah catatan draf) muncul
   merah "⚠ N tautan Google Drive tanpa ID valid …" dan hilang otomatis
   begitu tautannya diperbaiki/dihapus (event `input` tiap field).
2. **Saat tempel** — `normalizeDriveLinksInText()` kini mengembalikan
   `bad[]`; pesan tempel menyebut jumlah tautan tak-terkonversi, tone `err`
   bila ada (teks tetap dimasukkan apa adanya supaya tidak ada data hilang).
3. **Saat menyimpan** — hitungan `bad` dari semua field digabung;
   pesan simpan/draf ditambah "N tautan Drive tanpa ID valid tidak bisa
   diubah (butuh bentuk /file/d/<ID>/view atau ?id=<ID>)." dengan tone `err`.
4. **Foto cover tidak lagi bocor** — `artPhotoApply` menolak `drive-unknown`
   (tone err, tidak menyimpan), dan `collectEntry()` tidak lagi memasukkan
   photoUrl invalid / Drive-tanpa-ID ke `PHOTOS` (sebelumnya URL rusak
   tetap tersimpan sebagai cover saat Simpan).
5. **Cakupan build** — `test_drive_links.py` ikut diperluas: 3 wiring baru
   (`artDriveBad`, `findBadDriveLinks`, pesan simpan tanpa-ID) + 3 kasus JS
   (folder→bad teks utuh, lh3 bukan bad, campuran 1 valid + 1 bad) = 35 cek.

Diuji di browser: peringatan live menghitung 2→3→1 saat field diperbaiki,
lenyap saat bersih, tidak muncul utk lh3/URL biasa; tempel tanpa ID → pesan
err + teks utuh, tempel campuran → dua pesan (lh3 + bad); simpan dgn bad di
Deskripsi SEO → catatan + tone err; foto cover Drive-tanpa-ID ditolak dan
photoUrl rusak tidak tersimpan ke PHOTOS saat simpan; konsol tanpa error;
data uji dibersihkan. Build + 35 cek uji exit 0.

## Menu navigasi seperti balikisah.com (oktober 2026)

Menu utama diubah agar meniru struktur navigasi situs live https://balikisah.com
**tanpa menyentuh tema** (warna, tipografi, bentuk CTA, dsb. tetap sama):

- `MENU_DEFAULT` (site_shell.html) kini 8 item, persis label & urutan live:
  `Home`, `Budaya`, `Tradisi`, `Kuliner`, `Sejarah`, `Wisata`, `Tips Traveling`,
  `Tentang Kami`.
- Target baru `kategori:<Nama>` didukung `menuItemHtml()` → merender
  `data-goto="blog" data-blog="kategori" data-key="<Nama>"`, jadi klik langsung
  membuka arsip kategori itu (hash `#/kategori/<Nama>`, mis.
  `#/kategori/Tips%20Traveling`). `Home` → beranda, `Tentang Kami` → halaman
  tentang (`data-goto="compare"`).
- `allCategories()` ikut mendaftarkan kategori yang dirujuk menu bernama walau
  belum ada artikelnya, supaya tautan tidak 404 dan tetap muncul di indeks
  kategori. Chip arsip lama (Kerajaan Bali/Candi/Tokoh Sejarah/listowa/
  Soratirin/Kerajaan) tidak berubah; total kategori jadi 12.
- Chevron hanya untuk menu yang membuka daftar (`kategori`/`tag`/`penulis`/
  `arsip`/`dokumen`/`kontak`); tautan kategori bernama dibiarkan polos seperti
  live (8 item → 0 chevron).
- Editor menu (Dasbor → Tampilan) menampilkan `Kategori: <Nama>` untuk target
  bernama, menerima entri `Label | kategori:Nama Kategori` (case nama
  dipertahankan), dan `datalist` preset tetap dari `MENU_ROUTE_LABEL`.
> Catatan dokumen: `SRS-UI-10`/`FRD-08.2`/`UIRD §16` masih mencatat label nav
> lama (`Kategori`, `Kerajaan`, `Stonian`, `Blog`, `Kontak`) yang dikonfirmasi
> 5 Okt 2026. Permintaan terbaru (menu seperti balikisah.com) menggantikannya;
> dokumen requirement belum ikut diperbarui. `verify_chrome.py`/`verify_docs.py`
> tetap LULUS karena tidak memeriksa label nav ini.

- Spasi nav dirapatkan bertahap (gap 32→20/16/12/9/6 px; lebar input pencarian
  120→104/88/74 px) dan pencarian disembunyikan ≤1080px seperti sebelumnya,
  supaya 8 tautan muat tanpa overflow di 1280–1920px; di ≤1024px tetap laci
  mobile berisi 8 item + CTA `Hubungi Kami`. Tidak ada perubahan warna/ukuran
  font/bentuk tombol.

Diuji di browser (Chrome, localStorage `balikisah.menu.v1` dikosongkan):
8 `.site-nav` + 4 `.mobile-nav` identik & berurutan, 0 chevron, tidak overflow
pada 1440/1366/1280/1025/390 px; klik `Sejarah`/`Tips Traveling` membuka
`#/kategori/...` dengan judul+crumb benar; deep-link `#/kategori/Budaya`
langsung merender; `Tentang Kami` → view about; indeks kategori berisi 12
kategori; editor Tampilan menunjukkan 8 entri dengan label rute benar;
konsol bersih.

## Tema 100% mengikuti balikisah.com (oktober 2026)

Seluruh token desain kini memakai palet & font dari situs live
(https://balikisah.com). Nilai diambil dari variabel `--color-*` pada halaman
live ditambah warna kelas Tailwind yang terukur (`#ebd9c2`, `#f4ecdc`,
`#141d26`, `#1a1007`, `#c69238`, dst.).

Token (`:root` di `site_shell.html`) vs live:

| Token | Sebelum | Sekarang (= live) |
|---|---|---|
| `--ivory` (latar) | `#F7F0DD` | `#FAF5EB` |
| `--ink-900` (teks) | `#180E00` | `#281C12` |
| `--ink-700` | `#302923` | `#45372B` |
| `--ink-500` (excerpt) | `#73706A` | `#726252` |
| `--ink-400` (tanggal) | `#6E6B65` | `#8C827A` |
| `--ink-300` (nav) | `#3A3731` | `#141D26` |
| `--accent` / `--brand-brown` | `#94542E` / `#6F5138` | `#854D27` |
| `--accent-hover` | `#7A4526` | `#6C3B1A` |
| `--accent-chip` | `#8F5432` | `#854D27` |
| `--chip-fill` (chip non-aktif) | `#E7D6BC` | `#F4ECDC` |
| `--chip-ink` | `#54432C` | `#854D27` |
| `--hairline` / `--border-card` | `#E5DCC6` / `#EDE7DA` | `#EBD9C2` |
| `--font-ui` | Inter | **Plus Jakarta Sans** |
| `--sp-container` | 1120px | 1100px |
| `--radius-card` | 14px | 12px |

Token baru yang ditambahkan: `--gold #C69238` (aksen sekunder / garis
footer), `--gold-soft #E6B358`, `--footer-bg #1A1007`, `--bg-soft #F4ECDC`,
`--border-soft #E2D7CB`.

Perubahan komponen (agar sama seperti live):

- **Header** menyatu dengan latar halaman `#FAF5EB` (bukan bilah putih),
  garis bawah `#EBD9C2`.
- **Footer** gelap `#1A1007` dengan garis atas emas 4px `#C69238`; judul putih,
  tautan `#CFBFB0`.
- **Judul seksi** memakai garis aksen kiri 4px `#854D27` + padding-left 15px
  (meniru `.component-title` live).
- **Kartu** latar putih, border `#EBD9C2`, radius 12px, bayangan `rgba(40,28,18,.04)`.
- Semua isian krem lama (`#FFFDF7/#FFFDF6/#FFFDF8`, `#F3EADA`, `#F7F1E1`,
  `#F1E9D6`, `#E4D9BF`, `#D9CDB2`, `#E0D6BE`, `#FBF6EA`) dipetakan ulang ke
  putih / `#F4ECDC` / `#EBD9C2`.
- Tabel `SWATCHES` (view Bandingkan) memakai nilai token baru.
- Mode gelap tetap berjalan; token baru (`--gold`, `--bg-soft`, `--footer-bg`,
  `--border-soft`) juga didefinisikan pada blok `html[data-theme="dark"]`.

Diuji di browser (Chrome, skema warna dipaksa terang): latar `rgb(250,245,235)`,
teks `rgb(40,28,18)`, CTA `rgb(133,77,39)`, border kartu `rgb(235,217,194)`,
footer `rgb(26,16,7)` + garis `4px rgb(198,146,56)`, nav `rgb(20,29,38)`,
font Plus Jakarta Sans, judul Playfair Display — semuanya **sama persis**
dengan nilai live yang diukur. Mode gelap & view kategori diuji ulang; konsol
bersih. `build_site.py` + 35 cek regresi Drive exit 0, `verify_docs.py` dan
`verify_chrome.py` LULUS, 2 blok `<script>` lolos parse.

> Catatan: palet lama (`#F7F0DD`, `#94542E`, `#6F5138`) masih muncul di dalam
> teks 9 dokumen requirement yang disematkan di view Dokumen. Itu *isi dokumen*
> (fakta referensi UIRD), bukan tema UI, jadi sengaja dibiarkan.

## Susunan beranda mengikuti balikisah.com (oktober 2026)

Urutan section beranda kini sama seperti halaman live:

1. **Hero** artikel unggulan (tetap ada, konten dinamis dari artikel `featured`).
2. **Ticker "Terkini"** — kotak putih ber-border dengan badge cokelat + 8 judul
   terbaru berjalan (animasi `bkticker` 30s, berhenti saat hover, dimatikan
   bila `prefers-reduced-motion`).
3. **Kalender tradisi Bali** — 4 sel (Saptawara/urip-tri, Pancawara/neptu,
   Wuku Pawukon, Tahun Saka), dihitung dari tanggal hari ini (baseline
   Soma–Kliwon 1 Jan 2025; hanya untuk demo).
4. **"Arsip Sejarah Terkini"** — judul bergaya `.component-title` (bar aksen
   kiri + tautan "Lihat Semua" uppercase), grid 2 kolom kartu + **sidebar
   sticky "Populer Minggu Ini"** (3 artikel terpopuler berdasar views,
   lengkap chip kategori + meta penulis).
5. **"Galeri Situs Suci"** — band putih full-width; kartu 4 kolom dengan foto
   bulat 96px, chip kategori, judul Playfair, kutipan 3 baris; diisi dari
   kategori Candi lalu sisanya (maks 8).
6. **"Tokoh Ksatria Bali"** — 4 kartu membulat dengan foto bulat, peran
   uppercase, dan hover terangkat; diisi dari kategori Tokoh Sejarah.
7. **Footer gelap** dengan garis emas (dari langkah palet).

Semua bagian memakai palet/token live (lihat seksi palet di atas) dan tetap
responsif (1 kolom di ponsel, 2–4 kolom sesuai lebar). Klik kartu/tautan
memakai `data-goto`/`data-post` biasa sehingga tetap membuka halaman artikel.

Diuji di browser: urutan section benar, ticker 8 item beranimasi & bisa
diklik, kalender terisi (mis. Wraspati/Kliwon/Matal/1948), 8 kartu arsip,
3 kartu populer, 8 kartu galeri, kartu tokoh dari kategori Tokoh Sejarah;
klik galeri & sidebar membuka halaman artikel; konsol bersih; build + 35 cek
regresi Drive exit 0; verify_docs/verify_chrome LULUS.

## Perapian menu atas (oktober 2026)

Keluhan: label menu dua kata (`Tips Traveling`, `Tentang Kami`) melipat jadi
2 baris di header — akar masalahnya gutter header tema lama (`clamp(20px,
11vw,160px)` ≈ 158px per sisi) menyisakan ruang nav terlalu sempit.

Perbaikan (mengikuti cara live, container `max-width:1200px` + padding kecil):

- `.site-header__inner`: `max-width:1280px`, `padding-inline:24px`, gap kolom
  20px (sebelumnya `--wrap-max` ≈ 1437px dengan padding 158px/sisi).
- `.site-nav a` diberi `white-space:nowrap` — label selalu satu baris.
- Tier gap nav dirapikan ulang: 18px (default) → 14px ≤1440 → 11px ≤1366 →
  8px ≤1310 → 6px + input pencarian disembunyikan ≤1160 (ikon tetap, seperti
  live yang hanya menampilkan kolom cari di layar besar).
- `.mobile-nav a`: padding 13px 0, border bawah, `white-space:nowrap` — item
  drawer rapi dan konsisten.
- Footer/konten lain TIDAK diubah (masih pakai `--gutter`/`--wrap-max`).

Diuji: 1440/1366/1280/1150px → semua 8 label satu baris, tanpa overflow
horizontal; drawer mobile 8 item satu baris + CTA; konsol bersih; build +
regresi Drive exit 0; verify_docs/verify_chrome LULUS; 2 blok script lolos
parse.

## Catatan

- Windows console encoding: jalankan python yang mencetak non-ASCII dengan
  `PYTHONIOENCODING=utf-8`, karena stdout default adalah cp1252.
- `.freebuff/fix_copy.py` adalah skrip sekali jalan (sudah diterapkan, idempoten)
  untuk membersihkan teks contoh pada demo. Tidak perlu dijalankan ulang.
- Urutan rutin yang disarankan setiap kali menyentuh dokumen atau shell:
  `python .freebuff/build_site.py` lalu `python .freebuff/verify_docs.py`
  (build dulu, supaya pemeriksaan chrome melihat artefak terbaru).
  Setiap build kini **otomatis** menjalankan `test_drive_links.py`
  (bagian “Uji regresi konversi tautan Drive”) — build exit non-zero bila
  uji gagal; `node` harus tersedia di PATH.

## Parity tampilan dengan balikisah.com (oktober 2026)

Analisis ulang situs live (DOM ter-render, bukan tebakan) lalu penyelarasan
desain + struktur. **Ruang lingkup: tampilan & struktur 100% sama, konten tetap
milik proyek** (8 artikel demo). Konten live tidak diimpor karena berasal dari
API JSON miliknya sendiri (`/json?page=…`) dan thumbnail pencarian Bing —
mengimpor berarti menambah dependensi jaringan yang dilarang permintaan.

Yang diselaraskan (nilai terukur dari live):

| Aspek | Live | Sebelumnya di proyek | Sesudah |
|---|---|
| Font body | `'Julius Sans One'` (dipaksa `body{…!important}`) | Plus Jakarta Sans | `--font-ui` = Julius Sans One |
| Warna teks body | `#111827` | `#281C12` | `--body-ink:#111827` |
| Font editorial | Playfair Display | sama | sama |
| Footer kolom 1 `h3` | 24px (text-2xl) | 20px | 24px |
| Footer kolom lain `h3` | 18px (text-lg) | 20px | 18px |
| Tautan footer | 12px, `#CFBFB0` | 14px | 12px |
| Footer dalam | `max-w-1200` + `px-6`, `pt-6 pb-6` | `--wrap-max`/`--gutter` | 1200px, padding 24px |
| Footer bar | garis atas `white/15`, rata tengah | rgba .12, kiri | sesuai live |
| Tagline footer | "Cerita, Budaya, dan Pesona Bali" (`#E6B358`) | tidak ada | ditambahkan |
| Slider promo gelap | "Kisah Utama Pekan Ini" + tombol geser | **tidak ada** | ditambahkan |

### Bagian baru: promo gelap "Kisah Utama Pekan Ini"

Live menampilkan kotak gelap bergradien (`#382417` → `#2a1a10` → `#1a0f08`,
border `#4a3322`, radius 16px) berisi 6 kartu yang bisa digeser, dengan tombol
panah bulat. Ditambahkan sebagai `.home-promo` di dalam kolom utama arsip,
berisi `#homePromo` (diisi `renderHomeExtras()`, pool = `PUBLISHED.slice(2)`
dilengkapi dari awal supaya tetap 6 kartu meski artikel hanya 8) dan tombol
`#promoPrev`/`#promoNext` yang menggeser `scrollLeft` sebesar 296px.

### Bug tata letak yang ikut diperbaiki

`min-width:0` pada `.home-arsip__main` / `.home-arsip__grid > *` dan
`.home-promo`. Tanpa itu, slider 6×280px memaksa halaman melebar ke 913px di
viewport 390px (overflow horizontal). Sesudah perbaikan: `scrollWidth` 373px <
390px, tanpa overflow.

### Penyimpangan yang disengaja (dipertahankan sesuai aturan proyek)

1. **Identitas.** Live memakai label footer "Bali Kisah"/"BaliKisah.com";
   proyek tetap `balikisah.com` karena keputusan UIRD-01 dan
   `verify_chrome.py` melarang label itu muncul di chrome situs. Ini sempat
   memicu kegagalan verifikasi saat disalin mentah — diselaraskan kembali.
2. **Header.** Live memakai logo gambar (imagekit), tanpa tombol CTA, dan
   ikon pencarian tanpa kolom input. Proyek mempertahankan wordmark teks,
   kolom pencarian, CTA `Hubungi Kami`, dan tombol Admin karena itu perilaku
   fungsional yang sudah ada dan tidak boleh dihapus (syarat #3).
3. **Navigasi.** Label & urutan nav sudah identik dengan live; tautan
   kategori bernama tetap memakai rute internal proyek.

### Verifikasi

`build_site.py` exit 0 (128 PASS/0 FAIL), `verify_docs.py` LULUS exit 0,
`verify_chrome.py` LULUS exit 0. Di browser (1440×900 & 390×844): font body
Julius Sans One, warna body `rgb(17,24,39)`, footer 4 kolom dengan h3 24/18px
dan tautan 12px, latar footer `rgb(26,16,7)` + garis `4px rgb(198,146,56)`,
slider promo 6 kartu dengan gambar termuat + panah menggeser
(0 → 419 → 123), tanpa overflow horizontal di kedua lebar, mode gelap tetap
berjalan (body `rgb(21,18,12)`), konsol tanpa error.

### Sinkronisasi dokumen kebutuhan ke menu baru (7 Okt 2026)

Sembilan dokumen kebutuhan diperbarui agar pernyataan normatif nav mengikuti
menu situs saat ini (8 tautan balikisah.com: `Home`, `Budaya`, `Tradisi`,
`Kuliner`, `Sejarah`, `Wisata`, `Tips Traveling`, `Tentang Kami`):

- **UIRD** — baris nav pada diagram §1.1 dan daftar item final §3.1 diperbarui;
  ditambah catatan sejarah screenshot referensi, keputusan baru **UIRD-06**,
  entri riwayat revisi **1.2**, dan item checklist "menu 8 item, 0 chevron".
- **FRD** — `FRD-08.2` (daftar label) dan `FRD-08.3` (chevron → 0 chevron).
- **SRS** — `SRS-UI-10` label nav baru.
- **PRD** — catatan di §7 ditambah rujukan PD-09; baris **PD-09** baru di
  Lampiran A; PD-02 diberi keterangan bahwa label nav `Kontak` tidak lagi dipakai.
- **CRD** — baris "Hindari" diperbarui (CTA `Hubungi Kami` tetap; nav `Kontak`
  digantikan menu 8 item).

**Yang sengaja TIDAK diubah** (agar tetap sebagai catatan sejarah yang benar,
bukan dihapus):

1. Baris nav **di dalam diagram** §1.1 — diberi keterangan "fakta historis
   screenshot referensi 5 Okt 2026, tidak lagi dipakai".
2. Tabel geometri chip (`Kerajaan Bali`, `Candi`, `Tokoh Sejarah`, `Soratirin`,
   `Kerajaan`, `listowa`) di §3.3 — itu pengukuran chip kategori, bukan menu.
3. Token palet lama (`#F7F0DD`, `#94542E`, `#6F5138`, …) — wajib tetap ada
   karena `verify_docs.py` cek 8 memverifikasi 24 token itu di UIRD.

Verifikasi: `verify_docs.py` LULUS exit 0 (140 tautan, 142 anchor, 24/24 token,
0 baris tabel rusak), `verify_chrome.py` LULUS exit 0, build exit 0 dengan
130 PASS/0 FAIL. `UIRD-06`, `PD-09`, dan `SRS-UI-10` versi baru terbukti sudah
ter-embed di `index.html` setelah build ulang.

## Uji regresi tata letak responsif (oktober 2026)

Skrip baru `.freebuff/test_layout_responsive.py` — memastikan situs **tidak
memunculkan scroll horizontal** dan **label nav tidak melipat** di lebar
ponsel / tablet / desktop.

1. **Otomatis tiap build** — hook di akhir `build_site.py main()` memanggil
   `test_layout_responsive.run(index_path=OUT)` setelah uji editor; gagal =
   exit kode build non-zero. Mandiri:
   `python .freebuff/test_layout_responsive.py [path-index.html] [--verbose]`.
2. **Cara mengukur** — `index.html` dimuat di dalam `<iframe>` pada Chrome
   headless, lalu iframe dipersempit ke 5 lebar: **390, 768, 1024, 1280,
   1440 px**. Iframe dipakai karena Chrome membatasi lebar jendela minimum
   ~500 px sehingga `--window-size=390` tetap menghasilkan viewport 500 px;
   iframe memberi layout viewport sungguhan (`window.innerWidth` ikut
   berubah). Halaman pembungkus sementara ditulis ke folder tmp SISTEM
   (`tempfile.mkdtemp(prefix="bk_layout_test_")`) dan dihapus `finally:`,
   jadi tidak ada residu di proyek maupun artefak build.
3. **Tiga pemeriksaan per lebar** (5 lebar x 3 = **15 cek**):
   - **overflow** — `documentElement.scrollWidth > clientWidth`.
   - **lipatan** — tiap label nav yang terlihat diukur dengan
     `Range.getClientRects()`; hasil > 1 rect = teks melipat, dilaporkan
     beserta nama labelnya.
   - **mode navigasi** — pada lebar > 1024 px harus ada **8 label desktop**
     dan tombol hamburger tersembunyi; pada ≤ 1024 px nav desktop harus
     hilang, tombol hamburger tampil, dan laci mobile (yang di-`hidden`,
     dibuka sementara lalu ditutup lagi oleh harness) memuat ≥ 8 label.
4. **Pengukuran dibatasi ke view aktif** — situs punya beberapa `#view-*`
   dan hanya satu yang tidak `hidden`; tanpa pembatasan ini header view lain
   (juga 8 nav) membuat hitungan label salah.
5. **Terbukti bisa gagal** (uji negatif pada salinan sementara, artefak asli
   utuh): (a) `#homeHero{min-width:2500px}` → exit 1, `overflow horizontal
   +2125px` di 5 lebar; (b) `white-space:normal` + `max-width:44px` pada
   `.site-nav a` → exit 1, `label melipat -> 'Tips Traveling' (2 baris)`;
   (c) satu item menu dihapus → exit 1, `laci mobile hanya 7 label`;
   (d) `.nav-toggle{display:none}` → exit 1, `tombol hamburger tidak tampil`.
   Catatan: `max-width` sempit **tanpa** melepas `white-space:nowrap` tetap
   LULUS — memang benar, karena `nowrap` membuat pelipatan mustahil.
6. **Mode `--verbose`** — saat gagal, seluruh data pengukuran per lebar
   dicetak verbatim (JSON) untuk diagnosis; tanpa kegagalan tidak mengubah
   output.
7. **Bila browser tidak ada** — uji **DILEWATI** dengan pesan jelas dan
   exit 0, karena ketiadaan Chrome/Edge di suatu mesin bukan regresi kode.
   Browser dicari pada daftar path umum Windows/macOS/Linux lalu `PATH`.

### Sapuan tiap view pada 390/402 px (lanjutan, 7 Okt 2026)

Uji di atas hanya mengukur halaman awal (`view-home`), sehingga view yang
jarang dibuka tidak pernah diperiksa — itulah sebabnya bug `select` panel
Drive di view Kelola Foto (overflow 104 px pada 390 px) bisa lolos selama ini.
Sekarang tiap build juga menyapu **seluruh 10 view** pada **390 dan 402 px**:

- Tiap view dibuka lewat **pintu masuk aslinya**, bukan sekadar dilepas
  atribut `hidden`-nya: klik `[data-goto]`, klik `[data-blog]`, submit
  `[data-search-form]`, atau `BK.go()`. Alasannya: kalau hanya `hidden` yang
  dilepas, grid artikel / hasil cari / dasbor tetap kosong sehingga
  pemeriksaan overflow-nya hampa.
- View yang butuh login (`admin`) diberi kunci sesi sementara di
  `localStorage` iframe (dihapus lagi di akhir) supaya dasbornya ikut terukur
  (576 elemen). Bila tetap tidak bisa dibuka, dilaporkan **LEWAT** — tidak
  pernah dihitung PASS.
- Setiap view wajib benar-benar TAMPIL, dan view berisi daftar wajib memuat
  minimal `minPosts` kartu artikel di **konten utama** (tautan sidebar/widget
  tidak dihitung). Tanpa syarat ini, kategori kosong + widget "Paling Dibaca"
  membuat pemeriksaan lolos tanpa mengukur apa pun — ini benar-benar terjadi
  saat uji ini pertama ditulis (kategori "Budaya" ternyata kosong), sehingga
  pintu masuknya diganti ke kategori berisi artikel (`Candi`) plus dua pintu
  alternatif yang dicoba otomatis bila daftarnya kosong.
- **Meta cakupan**: setiap `#view-*` yang ada di dokumen harus punya langkah di
  `VIEW_STEPS`; menambah view baru tanpa menyapunya (atau menghapus view yang
  masih disapu) membuat uji GAGAL — jumlah view tidak bisa diam-diam berkurang.
- Pesan kegagalan menyebut angka dan elemen pelakunya, mis.
  `FAIL 390px view-photo: overflow horizontal +102px (scrollWidth 477 >
  clientWidth 375) — elemen terlebar: div.panel (lebar 461px, tepi kanan
  477px, lebih +102px)`.

**Uji negatif** (dijalankan pada salinan sementara; artefak asli tidak
tersentuh) — membuktikan uji ini benar-benar bisa gagal:

| Perubahan pada salinan | Hasil | Tercapai |
| --- | --- | --- |
| fix `select` Drive dibatalkan (bug lama dikembalikan) | FAIL `390px view-photo +102px`, `402px +90px`, pelaku `div.panel` 461px | ya, exit 1 |
| `.bp-card{min-width:900px}` | FAIL `view-blog: overflow +541px`, pelaku `article.bp-card` | ya, exit 1 |
| `id="view-admin"` diubah | `LEWAT` utk view-admin di 390+402 px + FAIL cakupan view | ya, exit 1 |
| `index.html` apa adanya | LULUS | ya, exit 0 |

Selain itu `--user-data-dir` kini diarahkan ke profil sementara **di dalam**
`tmp_dir` uji. Tanpa itu Chrome headless memakai profil sementara bersama dan
pernah gagal membuat berkas crashpad → halaman tidak dimuat → uji melaporkan
"Chrome tidak menghasilkan data pengukuran" (kegagalan lingkungan yang
menyesatkan, bukan regresi).

Hasil saat ini: **31 cek** LULUS (5 lebar x 2 + 1 cakupan view + 10 view x 2
lebar ponsel), build exit 0 dengan **159 PASS / 0 FAIL**. (Sebelum sapuan view:
15 cek / 138 PASS.)

## Hero beranda ala balikisah.com (oktober 2026)

Hero lama (kartu putih: teks di kiri, foto 3:2 di kanan, tombol CTA
`Baca selengkapnya`) diganti dengan susunan live:

- **Kartu utama** — `<a class="home-hero__card">` berisi foto `object-fit:cover`
  tinggi **370 px** di dalam kotak radius **16 px** berlatar `--footer-bg`
  (#1A1007), dengan judul + ringkasan **menumpuk di atas foto** lewat
  `.home-hero__scrim` (gradien `to top` hitam .85 → .4 → transparan).
  Di bawah judul ada garis pemisah `rgba(255,255,255,.2)` dan baris meta:
  nama penulis dalam pill `rgba(0,0,0,.4)` uppercase + tanggal, warna
  `--border-card` (#EBD9C2) — semua nilai terukur dari live.
- **Kolom kanan** — `#heroSideList` berisi **3 berita pendamping** sebagai
  baris ringkas (`.hero-side`): foto 96×96 radius 12 + judul Playfair 18px
  (maks 2 baris) + chip kategori + meta penulis/tanggal. Lebar kolom 420 px
  (≥768 px) / 460 px (≥1024 px), persis seperti live.
- **Responsif** — <768 px kartu menumpuk di atas kolom kanan (`flex-direction:
  column`), kartu tidak lagi dibatasi 620 px. Pada 390 px: tinggi foto tetap
  370 px, judul 2 baris, **tanpa overflow horizontal**.
- **Perilaku** — seluruh kartu (kartu utama dan tiap baris samping) adalah
  tautan yang membuka halaman artikel (`data-goto="article"` +
  `data-post="<slug>"`), sama seperti live. Foto memakai mesin `PHOTOS` yang
  ada (`data-photo-key` + `BK.syncPhotos`), jadi override foto admin tetap
  berlaku.

`renderHomeFeatured()` (mod_blog.js) kini juga mengisi `#heroAuthor`,
`#heroDate`, dan merender `#heroSideList` (unggulan dikecualikan, 3 sisanya).
ID lama `heroCta`/`heroTitle`/`heroText`/`heroImg`/`homeHero` dipertahankan
supaya tidak ada kait JS yang putus; `heroCta` berubah dari `<button>` menjadi
`<a>` pembungkus kartu.

Diuji di browser (1440×900 & 390×844): latar kartu `rgb(26,16,7)`, radius
16 px, foto 370 px `object-fit:cover` termuat, badan teks `absolute` `bottom:24px`,
scrim gradien benar, judul putih Playfair, ringkasan `rgb(207,191,176)`, meta
penulis + tanggal terisi, 3 kartu samping dengan foto 96 px, klik kartu utama
→ `?post=kerajaan-bali-sejarah-babad-bali`, klik kartu samping →
`?post=candi-dan-pura-kerajaan-babad-bali`, tanpa overflow, konsol bersih.
Build exit 0 (140 PASS/0 FAIL), `verify_docs` + `verify_chrome` LULUS.

## Header disamakan dengan balikisah.com (7 Okt 2026)

Permintaan pengguna: "bagian ini buat seperti contoh berikut ini" pada `<header>`
(proyek) versus `<header>` live.

### Nilai terukur dari live (bukan perkiraan)

| Aspek | Live | Sebelumnya di proyek | Sekarang |
|---|---|
| Susunan | `brand` kiri, `nav` tengah, `aksi` kanan | logo, nav, CTA, admin (tanpa grup) | `__brand` / `__nav` / `__actions` |
| Container | `max-w-1200` + `px-4` | 1280px + 24px | **1200px + 16px** |
| Tinggi | 80px desktop / 64px mobile | 78px / 64px | **80px / 64px** |
| Garis bawah | tidak ada (`border:0`) | hairline `#EBD9C2` | **tidak ada** |
| `position` | `static` | `sticky` | **`relative`** (jangkar panel cari) |
| Gap nav | 4px | 18px (bertingkat) | **4px** |
| Tautan nav | 14px/700 `#141d26`, padding `8px 16px` | 15px/500 | **14px/700, `8px 16px`** |
| Ikon cari | bulat 40x40 `#854D27`, tanpa kotak input | kotak input inline | **ikon bulat 40x40 + panel melayang** |
| Toggle mobile | bulat 40px `bg #F4ECDC` `text #854D27` | 44px tanpa latar | **40px bulat `--chip-fill`/`--accent`** |
| Laci | panel 320px + tombol silang bulat | hanya daftar tautan | **+ tombol silang bulat** |

### Perubahan

- **Struktur** — kedelapan `<header class="site-header">` ditulis ulang menjadi
  `__brand` (hamburger + logo) | `__nav` | `__actions` (cari, CTA, admin);
  toggle mode gelap disuntikkan ke `__actions` oleh `ensureChrome()`.
- **Nav statis** — label lama (`Kategori`, `Kerajaan`, `Stonian`, `Blog`,
  `Kontak`) di markup sumber diganti label live (8 tautan). Sebelumnya label
  benar hanya setelah `applyMenu()` berjalan; kini benar tanpa JS juga.
- **Pencarian** — kotak input inline diganti panel melayang di bawah header
  (`.site-search[hidden]`), dibuka `[data-search-toggle]`, ditutup Esc/klik luar.
- **Laci** — delapan laci `mobileNav…` (satu per view), masing-masing berpasangan
  dengan `navToggle…`; `view-search` sebelumnya punya hamburger tanpa laci dan
  `mobileNav4` nyasar di dalam `view-photo` — keduanya diperbaiki.
- **CTA** — tetap ada (UIRD-02), tampil di desktop, disembunyikan di bawah
  1200px (selalu ada di laci). Live sendiri tidak punya CTA di header.

### Dua bug yang ditemukan saat verifikasi

1. `applyMenu()` menulis ulang `innerHTML` laci, sehingga tombol silang dan CTA
   ikut terhapus. Keduanya sekarang diselamatkan dan dipasang kembali.
2. Handler pencarian semula mencari panel di `header.nextElementSibling`, padahal
   panel berada **di dalam** header. Diperbaiki menjadi `header.querySelector`.

### Verifikasi

- Build **exit 0** — 140 PASS / 0 FAIL (termasuk 10 uji tata letak responsif).
- `verify_docs.py` LULUS exit 0; `verify_chrome.py` LULUS exit 0.
- Di browser 1280px dan 1440px: container 1200px/padding 16px, tinggi 80px,
  nav 8 tautan gap 4px padding 8px 16px (10px di <1500px), ikon cari & toggle
  40x40 bulat, CTA tampil di 1440px, tanpa overflow, konsol bersih.
- Di 390px: tinggi 64px, nav disembunyikan, hamburger bulat `#F4ECDC`,
  laci 8 tautan + tombol silang yang berfungsi, tanpa overflow.
- Kedelapan view ber-header punya nav 8 tautan, laci berpasangan, panel cari,
  dan toggle tema. `view-docs`/`view-compare` memang tanpa header situs
  (sejak awal) dan tetap punya `demo-nav` sendiri.

### Perataan `Tokoh Ksatria Bali` di mobile (7 Okt 2026)

Pada tampilan ponsel (<768px) heading & kicker `.home-tokoh__head`
diset `text-align:left` — mengikuti foto acuan live yang memosisikan
bagian ini rata kiri, bukan center. Hanya heading yang diubah; kartu
masih 2 kolom dan isi kartu tetap `text-align:center` (sesuai foto).
Di tablet/desktop (≥768px) kembali `text-align:center`.

Aturan:
```css
@media (max-width:767px){.home-tokoh__head{text-align:left}}
```

### Ruang kosong kiri/kanan di mobile dipangkas (7 Okt 2026)

Keluhan: di ponsel konten terlihat ke tengah sehingga banyak ruang kosong di
kiri dan kanan (foto acuan: iPhone 402 px). Penyebabnya **padding horizontal**,
bukan `max-width` — `max-width:1200px` tentu tidak membatasi pada 402px.

Temuan dari CSS (`site_shell.html`):

| Sumber | Sebelum (402px) | Keterangan |
| --- | --- | --- |
| `--gutter:clamp(20px,11vw,160px)` (baris 59) | 44,2 px/sisi | 11vw pada 402px; dipakai `.section`, `.archive`, `.blog`, `.article-page`, `.dash`, `.pm`, `.demo-nav`, `.mobile-nav` |
| `.section` + `.home-wrap` menumpuk (arsip) | 44,2 + 16 = **60,2 px/sisi** | ganda; kolom konten tinggal ±282px → "Arsip Sejarah Terkini" & "Lihat Semua" patah 2 baris |
| Live | **16 px/sisi** | semua container live memakai `mx-auto px-4` |

Perbaikan (satu blok `@media (max-width:767px)`, desktop/tablet tidak tersentuh):

```css
@media (max-width:767px){
  :root{--gutter:16px}                      /* = px-4 ala live */
  .section.home-arsip{padding-left:0;padding-right:0}  /* hilangkan padding ganda */
  .mobile-nav{padding:24px 24px 40px}       /* laci tetap p-6 seperti live */
  .pm__cols > *{min-width:0}                /* bug lama: select tanpa aturan lebar */
  .scope-row .field{min-width:0}
  .scope-row select{width:100%;max-width:100%}
}
```

Catatan bug tambahan yang sekalian diperbaiki: `select#pmScope` tidak punya
aturan `width` (hanya `.field input` yang 100%), sehingga lebar intrinsiknya
mengikuti opsi terpanjang ("drive.readonly …" ≈ 424px) dan memaksa panel Drive
di view Kelola Foto melebar 461px → **scroll horizontal 104px** pada 390px
(sebelum perubahan gutter malah 131px). Kini semua view bersih.

#### Verifikasi

- Build **exit 0** — 138 PASS / 0 FAIL; `verify_docs.py` exit 0;
  `verify_chrome.py` exit 0.
- 402px (tanpa scrollbar, seperti mode perangkat): kolom konten **370px**
  (kiri 16 / kanan 16), `Arsip Sejarah Terkini` **1 baris**, `Lihat Semua`
  **1 baris**, `scrollWidth-clientWidth = 0`.
- 390px: kolom konten **358px** (kiri 16 / kanan 16), kedua judul 1 baris,
  tanpa overflow. Hero, ticker, kalender, galeri, tokoh semuanya 358px.
- Bandingkan dengan live pada lebar layout yang sama (385px): kolom live
  `353px`, proyek `353px` — identik. Pada layout 373px keduanya sama-sama
  `341px` (live pun patah 2 baris di situ).
- 11 view pada 390px (`home`, `archive`, `article`, `blog`, `search`, `admin`,
  `photo`, `404`, `compare`, `docs`, dll.): semuanya tanpa overflow horizontal.
- Desktop 1440px tidak berubah: `--gutter` tetap `clamp(20px,11vw,160px)`,
  `.section.home-arsip` padding `158,4px`, `.home-wrap` `16px`,
  `.mobile-nav` `158,4px`, `.pm__cols` tetap 2 kolom
  (`minmax(290px,368px) 1fr`), `.scope-row .field` tetap `min-width:200px`,
  `select` tetap `width:auto`. Tidak ada aturan baru di luar ≤767px.
- 768px juga tidak berubah (`--gutter` 84,48px, tanpa overflow).


### Tombol `Hubungi Kami` di header dihapus (7 Okt 2026)

Permintaan: hapus tombol `Hubungi Kami` di header (masukan pada elemen
`.site-header__actions .primary-cta` di view artikel). Header situs kini
**tanpa CTA sama sekali** — sama seperti balikisah.com, yang hanya punya ikon
pencarian di sisi kanan.

| Lokasi | Sebelum | Sesudah |
| --- | --- | --- |
| 8 header (`.site-header__actions`) | 8 tombol | **0** |
| 8 laci mobile (`.mobile-nav`) | 8 tombol | **8** (tetap) |
| Footer kolom "Lebih Dekat" | 1 tautan | tetap (ini tautan footer, bukan tombol header) |

Yang diubah di `site_shell.html`:

1. 8 baris `<button class="primary-cta" type="button">Hubungi Kami</button>`
   di dalam `.site-header__actions` dihapus (indentasi 8 spasi; versi laci
   berindentasi 4 spasi sehingga tidak ikut terhapus).
2. Aturan mati `@media (max-width:1199px){.site-header__actions .primary-cta{display:none}}`
   dihapus karena tidak ada lagi elemen yang cocok.
3. Komentar anggaran lebar nav diperbarui dengan angka **terukur** tanpa CTA:
   brand 151 + aksi (tema, cari, admin) 183 + nav 790 (@padding 16px) = 1124px
   masih muat di konten 1168px (viewport >= 1200px); pada viewport 1025px
   inner 1009px dan brand/aksi menyusut ke 142/133 sehingga dengan nav 694px
   totalnya 970px. Tier `padding:8px 10px` (<=1499px) **tetap dipakai** karena
   tanpa itu header meluber pada rentang viewport sempit itu.

Catatan: tombol CTA laci ikut diselamatkan `applyMenu()` (variabel `cta`),
jadi menghapusnya dari header tidak mengubah perilaku menu admin.

#### Verifikasi (preview 60929, `index.html` dibangun ulang)

- 1440px: 8 header dengan **0** CTA, 8 laci dengan **1** CTA, `.site-header__actions`
  = toggle tema + ikon cari + admin, tanpa overflow, grid beranda tetap 8 kartu.
- 1025px (kasus tersempit untuk nav desktop): nav 8 tautan tanpa lipatan,
  brand 142 + nav 694 + aksi 133 = 969 <= 1009, tanpa overflow, tinggi header 80px.
- 390px: laci dibuka lewat `#navToggle2` -> 8 tautan + CTA `Hubungi Kami`
  (133 x 35 px, `display:block`), tombol silang menutup laci, tanpa overflow.
- `verify_chrome.py` exit 0 (label lama tetap tidak ada; verifier ini memantau
  *label lama*, bukan keberadaan tombol CTA).
- Build exit 0 — **159 PASS / 0 FAIL**; `verify_docs.py` exit 0.

#### Konflik dengan UIRD-02 (belum diselesaikan)

`User Interface Requirements Document (UIRD).md` masih menyatakan CTA
`Hubungi Kami` dengan **kotak referensi 122 x 38** di dalam gambar wireframe
HEADER (baris ~427) dan keputusan UIRD-02 ("CTA `Hubungi Kami`", dikonfirmasi
5 Okt 2026). Dokumen **tidak** diubah oleh perubahan ini: masih menjadi
persyaratan tertulis sampai pemilik produk memutuskan lain. Opsi yang tersedia:
(a) biarkan — kebutuhan CTA terlayani di laci mobile, (b) hapus juga CTA laci,
(c) perbarui UIRD-02 + wireframe agar header resmi tanpa CTA.

### Gutter tablet 768–1023px dipangkas (lanjutan, 7 Okt 2026)

Permintaan: pemangkasan padding seluler yang sama diterapkan pada rentang
tablet 768–1023px, agar gutter 84–112px per sisi hilang.

Perubahan: **satu baris** — blok `@media (max-width:767px)` di
`site_shell.html` (baris ~514) diubah menjadi `@media (max-width:1024px)`.
Semua isinya sudah berupa nilai tetap (bukan turunan dari lebar), jadi tidak
ada aturan baru:

```css
@media (max-width:1024px){               /* sebelumnya max-width:767px */
  :root{--gutter:16px}                   /* was: 11vw = 84px @768, 112px @1023 */
  .section.home-arsip{padding-left:0;padding-right:0}
  .mobile-nav{padding:24px 24px 40px}
  .pm__cols > *{min-width:0}
  .scope-row .field{min-width:0}
  .scope-row select{width:100%;max-width:100%}
}
```

Ambang 1024px dipilih supaya **sama dengan ambang mode navigasi**
(`.site-nav` disembunyikan pada `max-width:1024px`, `MOBILE_MAX = 1024` di
`test_layout_responsive.py`): selama laci mobile yang tampil, gutter-nya 16px.
Aturan `@media (max-width:767px){.home-tokoh__head{text-align:left}}` **tidak**
ikut diperluas — perataan heading tokoh tetap khusus ponsel.

Angka "sebelum" bukan ingatan: pada tiap lebar, state lama direproduksi di
preview (`--gutter` dikembalikan ke `clamp(20px,11vw,160px)` + padding
`.section.home-arsip` dipulihkan lewat `<style>` sementara), diukur, lalu
dilepas lagi — sesudah probe kolom kembali ke nilai "sesudah" (768px: 719px,
1023px: 975px), jadi tidak ada state yang tertinggal.

| Lebar (layout) | `--gutter` sebelum | sesudah | Kolom arsip sebelum -> sesudah |
| --- | --- | --- | --- |
| 768px (751) | 84,48px/sisi | **16px** | 550 -> **719px** (+31%) |
| 1023px (1007) | 112,53px/sisi | **16px** | 750 -> **975px** (+30%) |
| 1024px (1007) | 112,64px/sisi | **16px** | 750 -> **975px** (layout sama dengan 1023) |

Nilai gutter 16px adalah konstanta (bukan clamp), jadi seluruh rentang
768–1024 pasti 16px; yang diukur di browser adalah 768 dan 1023/1024.

#### Verifikasi

- 768px: `--gutter` 16px; `.archive`/`.blog`/`.article-page`/`.site-footer__bar`
  16px; `.section.home-arsip` 0 (padding dalam `.home-wrap` 16px → bersih 16px);
  laci mobile tetap 24px (p-6 ala live); kolom konten 719px (dari 551px);
  tanpa overflow; heading tokoh tetap `center` di 768px.
- 1024px: gutter 16px, nav desktop tersembunyi + hamburger tampil (konsisten),
  tanpa overflow, `Arsip Sejarah Terkini` 1 baris.
- 1025px (di luar jangkauan): kembali `clamp(20px,11vw,160px)` = 112,787px,
  nav desktop tampil, tanpa overflow.
- 1440px: tidak berubah — gutter clamp, `.archive`/`.blog`/`.section.home-arsip`
  158,4px, `.pm__cols` tetap 2 kolom (`minmax(290px,368px) 1fr`),
  `.scope-row .field` tetap `min-width:200px`, laci 158,4px, tinggi header 80px.
- 390px: perilaku ponsel utuh — gutter 16px, arsip bersih 16px, laci 24px,
  heading tokoh rata kiri, `Arsip Sejarah Terkini` + `Lihat Semua` masing-masing
  1 baris pada layout 390px.
- Build **exit 0 — 159 PASS / 0 FAIL** (termasuk `lebar 768px` dan
  `lebar 1024px: tanpa overflow`); `verify_chrome.py` exit 0; `verify_docs.py`
  exit 0.

#### Sisi tajam yang tersisa

Pada 1024 -> 1025px gutter melompat 16px -> 112,787px, sehingga kontainer
tingkat view (`.archive`, `.blog`, `.article-page`, `.pm`, `.dash`,
`.site-footer__bar`) menyusut **975 -> 783px (-192px)** dan kolom arsip beranda
menyusut **975 -> 751px (-224px)** hanya karena 1px perbedaan viewport.
Lompatan ini memang batas "desktop" yang diminta tidak diubah; kalau ingin
dihaluskan, langkahnya adalah tier baru di 1025–1300px dengan gutter kecil
(mis. `clamp(16px,4vw,48px)`).

### Model lebar desktop disamakan dengan balikisah.com (7 Okt 2026)

Permintaan: container 1200px + padding 16px ala live, agar konten memakai
lebar penuh alih-alih gutter 158px.

**Ukur DOM live dulu (1440px)** — ternyata live memakai TIGA lebar container,
bukan satu:

| Bagian live | Kelas | max-width terukur | isi (content) |
| --- | --- | --- | --- |
| Header | `max-w-[1200px] mx-auto px-4` | **1200px** | **1168px** |
| Section konten | `max-w-1200 mx-auto px-4` | **1100px** | **1068px** |
| Footer | `max-w-[1200px] mx-auto px-6` | **1200px** | **1152px** |

`max-w-1200` (tanpa bracket) ternyata di-override jadi **1100px** di build live,
sedangkan `max-w-[1200px]` benar-benar 1200px. Karena itu target kolom konten
adalah **1068px**, bukan 1168px: percobaan pertama perubahan ini memakai
`--sp-container:1168px` (asumsi 1200px) dan meleset 100px terlalu lebar —
dikoreksi setelah mengukur (lihat tabel di bawah).

Perubahan di `site_shell.html`:

```css
--sp-container:1068px;   /* was 1100px; = 1100px container live - 2*16px */
--gutter:16px;           /* was clamp(20px,11vw,160px) -> 158,4px @1440px */
--wrap-max:calc(var(--sp-container) + 2 * var(--gutter));   /* = 1100px */
```

plus `.home-wrap` dan `.home-hero__grid`: `max-width:1200px` -> `1100px`
(section beranda di live memakai container 1100px yang sama), dan grid arsip
`2fr 1fr` -> **12 kolom dengan isi 8 + 4** (`lg:grid-cols-12 gap-8` ala live):

```css
@media (min-width:1024px){
  .home-arsip__grid{grid-template-columns:repeat(12,minmax(0,1fr));gap:32px}
  .home-arsip__main{grid-column:span 8}
  .home-arsip__grid > .home-side{grid-column:span 4}
}
```

`.section.home-arsip{padding-inline:0}` yang dulu khusus ≤1024px kini berlaku
**semua lebar** (`.section` hanya dipakai section ini, terverifikasi: satu
`class="section home-arsip"` di seluruh berkas), sehingga section arsip selebar
section beranda lain. Header (1200/16) dan footer (1200/24) tidak diubah —
keduanya sudah sama dengan live.

#### Paritas terukur @1440px (proyek vs live)

| Elemen | Live | Proyek |
| --- | --- | --- |
| Isi section konten | 1068px | **1068px** |
| Isi header | 1168px | **1168px** |
| Kartu hero | 592px (cap 620px) | **592px** |
| Kolom arsip utama | 701px | **701px** |
| Kolom sidebar arsip | 335px | **335px** |
| Isi footer | 1152px | 1152px (tidak diubah) |

Sebelum perubahan: gutter 158,4px/sisi, kolom konten view 1100px, section
beranda 1168px, section arsip 1068px (tidak konsisten satu halaman).

#### Verifikasi

- Build **exit 0 — 159 PASS / 0 FAIL**; `verify_chrome.py` exit 0;
  `verify_docs.py` exit 0.
- 1440px: `--gutter` 16px, `--wrap-max` 1100px, isi section 1068px, header
  1168px, hero 592px, arsip 701/335 (12 kolom), galeri 4 kolom, tokoh 4 kolom,
  tanpa overflow.
- 1024px: container penuh (1007px), arsip 640/304 (12 kolom), nav laci aktif,
  tanpa overflow.
- 768px: tidak berubah dari verifikasi sebelumnya — gutter 16px, kolom 719px,
  `.archive`/`.article-page` 16px, laci 24px, galeri 3 kolom, tanpa overflow.
- 390px (layout 390px): gutter 16px, kolom arsip 358px, `Arsip Sejarah
  Terkini` + `Lihat Semua` tetap 1 baris, heading tokoh rata kiri, tanpa
  overflow.
- Catatan: `.article-page` tetap `max-width:calc(720px + 2*var(--gutter))` =
  752px (kolom baca 720px) — tidak ikut melebar, sesuai desain live untuk
  halaman artikel.

#### Konsekuensi yang perlu diketahui

- Kolom konten **view** (`.archive`, `.blog`, `.pm`, `.dash`, `.compare`, 404)
  kini 1068px — sebelumnya 1100px, jadi 32px lebih sempit tetapi pinggirnya
  bersih (gutter 158 -> 16).
- Section beranda (ticker, kalender, galeri, tokoh) 1168 -> 1068px karena live
  memang 1100px container-nya; kalau ingin lebih lebar dari live, tinggal naikkan
  `--sp-container`.
- Isi header (1168px) lebih lebar 100px daripada isi section (1068px) — ini
  persis model live, bukan kekeliruan.

### Tier perampingan padding nav dipersempit (7 Okt 2026)

Permintaan: desktop lebar memakai `padding:8px 16px` persis seperti live, tanpa
membuat header meluber di viewport sempit.

Sebelumnya `@media (max-width:1499px){.site-nav a{padding:8px 10px}}` — jadi
hampir semua desktop (termasuk 1280 dan 1440) memakai 10px, padahal live 16px.
Sekarang ambangnya **1199px**, sehingga seluruh desktop di atas itu memakai
nilai live.

**Angka anggaran lebar header** (diukur di preview, header tanpa CTA):

| Komponen | Lebar |
| --- | --- |
| Brand `balikisah.com` | 151px (clamp → 142px @1025) |
| Nav 8 tautan @`8px 16px` | **790px** (74/84/82/88/87/80/135/132) |
| Nav 8 tautan @`8px 10px` | 694px |
| Aksi (tema + cari + admin) | 183px (133px @1025) |
| Inner header (max-width) | 1200px |

Dengan 16px totalnya 1124px, jadi muat selama inner >= 1124px — dan inner
mencapai 1200px penuh mulai viewport ~1236px (1200 + scrollbar Chrome 36px).
Di bawah itu ruang brand boleh menyusut sendiri karena lebarnya
`clamp(21px,1.5vw + 10px,27px)` (mengambang), sehingga 1199px masih aman.
Karena itu batasnya 1199px — **sama dengan ambang yang sudah dipakai untuk
berhentinya nav desktop**: pada `<=1199px` nav memang diramping, pada `>1199px`
(desktop lebar) padding-nya persis live.

```css
/* was: @media (max-width:1499px) */
@media (max-width:1199px){.site-nav a{padding:8px 10px}}
```

Aturan tidak dihapus seluruhnya karena tanpanya header benar-benar meluber:
`padding 16px` pada 1100px membuat aksi melimpah **+56px** keluar header dan
menimpa ikon admin (pada 1025px +131px) walaupun halaman tetap tidak scroll
horizontal — luapan yang tidak terdeteksi uji overflow halaman.

#### Verifikasi (resize viewport sungguhan)

| Viewport | Padding nav | Inner | Nav | Total | Luapan | Overflow |
| --- | --- | --- | --- | --- | --- | --- |
| 1025px | **10px** | 1009 | 694 | 970 | -7 | 0 |
| 1100px | **10px** | 1050 | 694 | 1028 | -16 | 0 |
| 1199px | **16px** | 1183 | 790 | 1075 | -16 | 0 |
| 1200px | **16px** | 1183 | 790 | 1075 | -16 | 0 |
| 1280px | **16px** | 1200 | 790 | 1124 | -16 | 0 |
| 1440px | **16px** | 1200 | 790 | 1124 | -16 | 0 |

- 8 label nav terlihat & tidak ada yang melipat di semua lebar uji; header
  tidak meluber di satu pun (luapan negatif = masih ada sisa ruang).
- 768px: nav disembunyikan (`display:none`), hamburger tampil, laci 8 tautan
  dengan tombol silang, header 64px, tanpa overflow — perilaku laci tidak
  berubah oleh tier ini.
- 390px: tidak berubah — gutter 16px, kolom arsip 358px, `Arsip Sejarah
  Terkini` + `Lihat Semua` masing-masing 1 baris, heading tokoh rata kiri,
  tanpa overflow.
- Build **exit 0 — 159 PASS / 0 FAIL** (termasuk `lebar 1280px`/`1440px`:
  tanpa overflow + tidak ada label nav melipat); `verify_chrome.py` exit 0;
  `verify_docs.py` exit 0.

#### Catatan metode (penting untuk pengukuran berikutnya)

Media query **tidak** ikut berubah bila lebar viewport dipalsukan lewat
`documentElement.style.width` — `matchMedia` memakai lebar viewport asli,
sehingga pengukuran seperti itu melaporkan nilai tier yang salah (sempat
membuat tier 16px tampak "tidak berpengaruh" di semua lebar). Semua angka di
tabel atas diambil dengan `preview_resize` sungguhan.

#### Sisa ruang yang belum diramping

Tier 1199px lebih konservatif dari yang secara teknis diperlukan: 16px masih
muat sampai viewport ~1124px. Jadi pada 1124-1199px link memakai 10px padahal
bisa 16px. Menurunkannya ke ~1124px akan menambah segmen desktop yang persis
live, tetapi memakai margin lebih tipis terhadap variasi lebar scrollbar
antarbrowser (Windows 36px, macOS 0px) — sengaja dipilih aman.

### Latar #FAF5EB di semua halaman (7 Okt 2026)

Permintaan: "latar semua halaman buat dengan warna ini #FAF5EB".

**Temuan: mode terang sudah memakai #FAF5EB sejak awal** — token
`--ivory:#FAF5EB` (baris 22) dan `body{background:var(--ivory)}` (baris 89).
Yang membuat permintaan ini muncul adalah **mode gelap otomatis**: inisialisasi
tema memakai `prefers-color-scheme` OS sebagai default ketika belum ada
pilihan tersimpan, dan perangkat yang bermode gelap (terverifikasi
`prefersDark:true`) membuka situs dengan latar **#15120C** (terukur, bukan
dugaan). Itulah yang terlihat "bukan #FAF5EB".

**Perubahan** (satu blok, `site_shell.html` baris ~4979): default tema tidak
lagi membaca preferensi OS — selalu terang, latar #FAF5EB:

```js
(function(){
  /* Default SELALU terang: latar #FAF5EB di semua halaman. ... */
  var saved = "";
  try { saved = localStorage.getItem(THEME_KEY) || ""; } catch (e) {}
  document.documentElement.setAttribute("data-theme", saved === "dark" ? "dark" : "light");
})();
```

Konsekuensi yang disengaja:

- Setiap halaman selalu terbuka dengan latar #FAF5EB, di perangkat apa pun.
- Mode gelap **tetap ada** — tombol "Ganti mode gelap/terang" di header masih
  berfungsi dan pilihannya diingat (`localStorage.balikisah.theme`). Pengunjung
  yang sudah pernah memilih gelap tetap mendapat gelap.
- PRD mencantumkan mode gelap sebagai backlog "tidak termasuk dalam rilis ini"
  (baris 395); F-18 tetap P2. Kalau mau dihapus total (tombol + 24 aturan CSS),
  itu keputusan terpisah — konflik UIRD/PRD-nya serupa dengan kasus CTA.

Catatan lingkungan: preview ini berjalan dengan OS bermode gelap, jadi kebetulan
jadi reproduksi alami bug-nya; perbaikan diverifikasi di kondisi itu.

#### Verifikasi

- **10 dari 10 view** (`home`, `archive`, `article`, `blog`, `search`, `admin`,
  `photo`, `404`, `compare`, `docs`) terukur `body` background **#FAF5EB**
  (set 10 nilai identik) — dengan OS masih bermode gelap.
- Tanpa `localStorage.balikisah.theme`, reload → `data-theme="light"`,
  body `#FAF5EB` (sebelum perbaikan: `dark` / `#15120C`).
- Tombol tema: klik → `dark` / `#15120C` + tersimpan `balikisah.theme=dark`;
  klik lagi → `light` / `#FAF5EB`. Fungsi gelap utuh.
- Hanya ada **satu** `prefers-color-scheme` tersisa di artefak — di dalam
  komentar penjelas, bukan kode fungsional.
- Catatan kecil: `documentElement` melaporkan `backgroundColor:#000000`
  (transparent → disarikan sebagai #000000 oleh getComputedStyle), tapi yang
  terlihat adalah body #FAF5EB di atasnya; bukan masalah visual.
- Build **exit 0 — 159 PASS / 0 FAIL**; `verify_chrome.py` exit 0;
  `verify_docs.py` exit 0.

#### Belum diubah: panel/kartu putih di atas latar #FAF5EB

Permintaan ini dibaca sebagai "latar halaman", jadi kartu/panel `--surface`
(#FFFFFF) dibiarkan: kalender, kartu artikel, panel Populer, galeri, TOC,
panel admin, docs (putih penuh), dsb. (48 elemen terukur >250px). Itu pola
kartu di atas latar, mirip live. Kalau maksudnya semua permukaan ikut #FAF5EB
(halus tapi kontras kartu hilang), ubah `--surface:#FFFFFF` → `#FAF5EB` di
token terang — satu baris, semua kartu ikut.

### Latar halaman diganti ke #F6EFDC (7 Okt 2026)

Permintaan: "warna latar ganti ke ini #f6efdc". Menggantikan #FAF5EB yang
dipakai sejak awal (hasil menyalin live).

**Yang diubah di `site_shell.html`** (3 tempat, harus tetap sinkron):

1. Token `--ivory:#FAF5EB` → **`#F6EFDC`** (baris 22). Ini satu-satunya sumber
   warna latar: `body{background:var(--ivory)}` (baris 89) dan header
   `background:var(--ivory)` (baris 126) ikut otomatis.
2. Daftar palet view Bandingkan: `["--ivory","#FAF5EB","Latar halaman"]` →
   `["--ivory","#F6EFDC","Latar halaman"]` supaya swatch tidak menampilkan
   nilai lama.
3. `<meta name="theme-color">`: `"#FFFFFF"` → **`"#F6EFDC"`**. Sebelumnya bilah
   peramban ponsel diwarnai putih padahal latar halaman ivory — sekarang
   warnanya sama dengan halaman.

**Tidak diubah** (sengaja, supaya perubahan tetap satu variabel):

- `--surface:#FFFFFF` (kartu, header-atas-kartu, panel) — permintaan menyebut
  latar, jadi kontras kartu di atas latar tetap ada. 48 elemen >250px masih
  putih: kalender, kartu artikel, panel Populer, galeri, TOC, panel admin, docs.
- Warna gelap: `html[data-theme="dark"] --ivory:#15120C` tetap; mode gelap
  masih bisa dipilih lewat tombol tema.

#### Bug yang ketemu sambil memverifikasi (diperbaiki)

`<meta name="theme-color">` hanya disegarkan oleh `__uxSync`
(scroll/resize/ganti view), **tidak** saat tombol tema ditekan. Terukur:
setelah klik ke gelap, meta masih `#F6EFDC` padahal body sudah `#15120C`.
Ditambahkan satu baris di `applyTheme()`: `if (window.__themeColor) window.__themeColor();`
(lalu `themeColor()` dipanggil; definisinya ada di blok setelahnya, tapi saat
fungsi itu jalan `window.__themeColor` sudah ada, jadi guard-nya aman).
Warna gelap disamakan dengan `--ivory` gelap: `#14110C` → `#15120C`.

#### Verifikasi

| Pemeriksaan | Hasil |
| --- | --- |
| 10 view (`home`, `archive`, `article`, `blog`, `search`, `admin`, `photo`, `404`, `compare`, `docs`) | semua `body` background **#F6EFDC** (1 nilai unik) |
| Token `--ivory` terhitung | `#F6EFDC` |
| OS bermode gelap + tanpa pilihan tersimpan | tetap terbuka **terang** `#F6EFDC` (default terang dari perbaikan sebelumnya) |
| Tombol tema → gelap | body `#15120C`, meta `#15120C` (cocok), tersimpan di localStorage |
| Tombol tema → terang lagi | body `#F6EFDC`, meta `#F6EFDC` (cocok) |
| Swatch view Bandingkan | `Latar halaman #F6EFDC` |
| Overflow horizontal | 0 |
| Build | **exit 0 — 159 PASS / 0 FAIL** |
| `verify_chrome.py` / `verify_docs.py` | exit 0 / exit 0 |

Catatan: satu-satunya `#FAF5EB` tersisa di artefak adalah warna **teks** di
`.toast` (baris 1096) di atas panel gelap `#241808` — bukan latar halaman.
Kontrasnya terhadap latar baru hanya berubah ~1,5% terang, tidak berdampak.

#### Divergensi dengan dokumen kebutuhan

Dokumen menyebut latar halaman **`#F7F0DD`**, bukan `#FAF5EB` maupun `#F6EFDC`:

- SRS-UI-01 (baris 298): "Latar halaman `#F7F0DD`; header dan permukaan kartu `#FFFFFF`."
- UIRD (baris 32, 108, 502, 508, 567): `--ivory #F7F0DD` termasuk perhitungan
  kontras (mis. `--ink-900 on #F7F0DD` = 15,4:1).
- PRD (baris 261): "Latar halaman `#F7F0DD`."

Dokumen **tidak** diubah. Jadi sekarang ada tiga angka: dokumen `#F7F0DD`,
live `#FAF5EB`, dan situs `#F6EFDC` (permintaan terbaru). `#F6EFDC` adalah
yang paling dekat ke dokumen dari ketiganya, tetapi tetap bukan nilai yang
tertulis.

**Kontras teks terhadap latar (dihitung dengan rumus WCAG, bukan perkiraan):**

| Teks | #F7F0DD (dok) | #FAF5EB (lama) | #F6EFDC (baru) | AA 4,5:1 |
| --- | --- | --- | --- | --- |
| `--ink-900 #281C12` | 14,59 | 15,28 | **14,46** | lolos |
| `--ink-300 #141D26` | 14,97 | 15,67 | **14,83** | lolos |
| `--body-ink #111827` | 15,60 | 16,33 | **15,46** | lolos |
| `--accent #854D27` | 5,98 | 6,26 | **5,93** | lolos |
| `--ink-500 #726252` | 5,15 | 5,39 | **5,11** | lolos |
| `--muted #887861` | 3,76 | 3,94 | **3,73** | gagal (sudah gagal sebelum ini) |
| `--ink-400 #8C827A` | 3,30 | 3,46 | **3,27** | gagal (sudah gagal sebelum ini) |

Perubahan ini menurunkan semua rasio sedikit (~1,2 menit poin), tetapi **tidak
ada teks yang melewati ambang 4,5:1**: yang tadinya gagal tetap gagal
(`--muted` 3,94 → 3,73 dan `--ink-400` 3,46 → 3,27), yang tadinya lolos tetap
lolos (terendahnya `--ink-500` 5,39 → 5,11). Dua yang gagal itu masalah lama
(teks tanggal/eyebrow berukuran kecil) dan tidak disebabkan perubahan ini;
memperbaikinya perlu menggelapkan `--muted`/`--ink-400`, terpisah dari tugas
ini.

Catatan: angka di tabel ini sebelumnya saya tulis dari ingatan dan **salah**
(tertulis `--ink-300: 14,9 → 14,3` dan `--ink-500: 4,3 → 4,1`); versi di atas
dihitung ulang dengan rumus luminansi WCAG.
