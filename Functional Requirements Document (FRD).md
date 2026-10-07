# Functional Requirements Document (FRD)

> **Project:** BaliKisah.com
> **Status:** Baseline v1.0
> **Tanggal:** 5 Oktober 2026
> **Dokumen terkait:** [PRD](Product%20Requirements%20Document%20(PRD)%2018%20Section.md) · [UIRD](User%20Interface%20Requirements%20Document%20(UIRD).md) · [TRD](Technical%20Requirements%20Document%20(TRD).md) · [QRD](Quality%20Requirements%20Document%20(QRD).md) · [SRS](Software%20Requirements%20Specification%20(SRS).md)

---

## 1. Konvensi Penulisan

| Notasi | Arti |
|---|---|
| **FRD-nn** | Identitas kebutuhan fungsional |
| **SHALL** | Wajib dipenuhi |
| **SHOULD** | Sangat disarankan, boleh dikesampingkan dengan alasan |
| **MAY** | Opsional |
| **P0 / P1 / P2** | Prioritas |

---

## 2. Modul: Beranda (Home)

| ID | Requirement | Prioritas |
|---|---|---|
| **FRD-01.1** | Sistem **SHALL** menampilkan satu artikel unggulan (hero) dengan gambar, judul, ringkasan, penulis, tanggal, dan waktu baca. | P0 |
| **FRD-01.2** | Sistem **SHALL** menampilkan grid artikel terbaru, minimal 6 artikel, diurutkan `publishedAt` menurun. | P0 |
| **FRD-01.3** | Sistem **SHALL** menampilkan seksi "Paling Populer" dengan kontrol Previous / Next yang dapat dioperasikan keyboard. | P0 |
| **FRD-01.4** | Sistem **SHALL** menampilkan seksi "Bacaan Lanjut" dengan minimal 4 artikel. | P0 |
| **FRD-01.5** | Sistem **SHOULD** menampilkan blok kategori unggulan minimal 3 kategori. | P1 |
| **FRD-01.6** | Carousel **SHALL** berhenti autoplay bila pengguna berinteraksi, saat dokumen tersembunyi, atau saat `prefers-reduced-motion` aktif. | P0 |
| **FRD-01.7** | Tombol Previous/Next **SHALL** memiliki `aria-label` deskriptif dan state disabled di batas carousel. | P0 |

> **Perbaikan konten (terverifikasi di live):** judul seksi berbahasa Inggris `Hottest Articles` dan `Read More`, serta subjudul `Discover the latest trending articles. Don't miss out!` dan `Explore our archive of articles, interviews, and creative projects` **SHALL** diterjemahkan ke Bahasa Indonesia: `Paling Populer` dan `Bacaan Lanjut`.

---

## 3. Modul: Arsip Kategori

| ID | Requirement | Prioritas |
|---|---|---|
| **FRD-02.1** | Sistem **SHALL** menyediakan halaman arsip untuk setiap kategori di `/kategori/{slug}`. | P0 |
| **FRD-02.2** | Halaman arsip **SHALL** menampilkan eyebrow `Kategori archive`, H1 nama kategori, garis pemisah, dan chip filter — urutan persis sesuai [UIRD §3.2](User%20Interface%20Requirements%20Document%20(UIRD).md). | P0 |
| **FRD-02.3** | Sistem **SHALL** menampilkan chip untuk setiap kategori anak atau tag yang relevan. | P0 |
| **FRD-02.4** | Chip aktif **SHALL** ditandai dengan `aria-pressed="true"` dan fill aksen `#8F5432`. | P0 |
| **FRD-02.5** | Filter chip **SHALL** bekerja tanpa muat ulang halaman penuh (progressive enhancement: URL tetap dapat dibagikan). | P0 |
| **FRD-02.6** | Filter chip **SHALL** tersimpan pada URL sebagai query parameter (`?filter=slug`) agar dapat dibagikan dan di-bookmark. | P0 |
| **FRD-02.7** | Sistem **SHALL** menampilkan 4 kolom kartu pada viewport ≥ 1280 px, 3 kolom pada 1024–1279 px, 2 kolom pada 768–1023 px, dan 1 kolom pada < 640 px. | P0 |
| **FRD-02.8** | Judul kartu **SHALL** dibatasi 2 baris dan ringkasan 3 baris dengan ellipsis. | P0 |
| **FRD-02.9** | Thumbnail pada kategori sejarah/babad **SHALL** diberi filter sepia `sepia(.45) saturate(.85) contrast(.96) brightness(1.03)`. | P0 |
| **FRD-02.10** | Halaman **SHALL** menampilkan pagination; bila jumlah halaman > 7, halaman tengah diganti elipsis. | P0 |
| **FRD-02.11** | Kategori tanpa artikel **SHALL** menampilkan empty state yang informatif, bukan halaman kosong. | P1 |
| **FRD-02.12** | Filter chip **SHALL** dapat dioperasikan dengan keyboard (`Tab`, `Enter`, `Space`). | P0 |

---

## 4. Modul: Halaman Artikel

| ID | Requirement | Prioritas |
|---|---|---|
| **FRD-03.1** | Sistem **SHALL** menampilkan breadcrumb `Beranda / Kategori / Judul`. | P0 |
| **FRD-03.2** | Sistem **SHALL** menampilkan H1 artikel, penulis, tanggal terbit, waktu baca, dan kategori. | P0 |
| **FRD-03.3** | Bila artikel diperbarui setelah terbit, sistem **SHALL** menampilkan `Diperbarui pada {tanggal}`. | P1 |
| **FRD-03.4** | Sistem **SHALL** menampilkan gambar utama dengan rasio 16:9 dan `object-fit: cover`. | P0 |
| **FRD-03.5** | Badan artikel **SHALL** memiliki lebar baca maksimum 720 px dan `line-height` 1,75. | P0 |
| **FRD-03.6** | Sistem **SHALL** menampilkan minimal 3 artikel terkait di akhir artikel. | P0 |
| **FRD-03.7** | Sistem **SHALL** menampilkan blok berbagi (salin tautan, WhatsApp, Facebook, X). | P1 |
| **FRD-03.8** | Sistem **SHALL** menyertakan `Article` JSON-LD yang lengkap (headline, image, datePublished, dateModified, author, publisher). | P0 |
| **FRD-03.9** | Sistem **SHALL** menyertakan `BreadcrumbList` JSON-LD. | P0 |
| **FRD-03.10** | Navigasi keyboard di dalam artikel **SHALL** melewati blok iklan (tabindex `-1`). | P0 |
| **FRD-03.11** | Artikel yang slug-nya tidak ditemukan **SHALL** mengembalikan 404 dengan halaman kustom. | P0 |
| **FRD-03.12** | Gambar di dalam badan artikel **SHALL** memiliki `loading="lazy"` kecuali gambar pertama. | P0 |

---

## 5. Modul: Pencarian

| ID | Requirement | Prioritas |
|---|---|---|
| **FRD-04.1** | Sistem **SHALL** menyediakan pencarian internal di header (desktop) dan di dalam drawer (mobile). | P0 |
| **FRD-04.2** | Halaman hasil `?q=` **SHALL** menampilkan judul, ringkasan, dan tautan artikel. | P0 |
| **FRD-04.3** | Hasil **SHALL** diberi penanda kategori dan tanggal. | P0 |
| **FRD-04.4** | Input pencarian **SHALL** di-debounce 300 ms. | P0 |
| **FRD-04.5** | Hasil kosong **SHALL** menampilkan saran kategori dan Articles Populer. | P1 |
| **FRD-04.6** | Pencarian **SHALL** dapat difilter per kategori bila tersedia > 1 kategori. | P2 |
| **FRD-04.7** | Halaman hasil **SHALL** memiliki `noindex` untuk mencegah fragmentasi indeks. | P1 |

---

## 6. Modul: Artikel Terkait & Penemuan

| ID | Requirement | Prioritas |
|---|---|---|
| **FRD-05.1** | Sistem **SHALL** menentukan artikel terkait berdasarkan skor: kategori sama (40%) + kesamaan tag (30%) + kedekatan waktu terbit (15%) + popularitas (15%). | P0 |
| **FRD-05.2** | Sistem **SHALL** menampilkan "Topik Populer" sesuai data footer live: Hidden Gem Bali, Tradisi Bali, Pura Bali, Makanan Khas, Itinerary Bali, Warisan Budaya Bali. | P0 |
| **FRD-05.3** | Artikel **SHALL** menampilkan breadcrumb yang dapat diklik di setiap halaman dalam. | P0 |
| **FRD-05.4** | Sistem **SHOULD** menampilkan "Artikel terbaru" di akhir artikel untuk melanjutkan penelusuran. | P1 |

---

## 7. Modul: Halaman Statis

| ID | Requirement | Prioritas |
|---|---|---|
| **FRD-06.1** | Sistem **SHALL** menyediakan halaman statis: Tentang Kami, Kebijakan Privasi, Syarat dan Ketentuan, Disclaimer, FAQ, Hubungi Kami. | P0 |
| **FRD-06.2** | Halaman statis **SHALL** memakai template yang sama dengan palet dan tipografi utama. | P0 |
| **FRD-06.3** | Halaman FAQ **SHALL** memakai markup `FAQPage` JSON-LD. | P1 |
| **FRD-06.4** | Halaman legal **SHALL** menampilkan tanggal pembaruan terakhir. | P0 |
| **FRD-06.5** | Halaman Hubungi Kami **SHALL** menyediakan formulir dengan validasi dan konfirmasi. | P1 |
| **FRD-06.6** | Formulir kontak **SHALL** tidak memakai CAPTCHA yang merusak aksesibilitas — gunakan CAPTCHA tak terlihat bila wajib. | P1 |

---

## 8. Modul: Navigasi & Struktur Global

| ID | Requirement | Prioritas |
|---|---|---|
| **FRD-08.1** | Header **SHALL** menampilkan logo di kiri, navigasi di kanan, dan CTA `Hubungi Kami` paling kanan — sesuai [UIRD §3.1](User%20Interface%20Requirements%20Document%20(UIRD).md). | P0 |
| **FRD-08.2** | Navigasi **SHALL** memuat 8 tautan dengan urutan persis seperti balikisah.com: `Home`, `Budaya`, `Tradisi`, `Kuliner`, `Sejarah`, `Wisata`, `Tips Traveling`, `Tentang Kami` — **label final dikonfirmasi 7 Okt 2026** ([UIRD §16](User%20Interface%20Requirements%20Document%20(UIRD).md) UIRD-06). `Home` → beranda, `Tentang Kami` → halaman tentang, enam label kategori → arsip kategori bernama via target internal `kategori:<Nama>`. | P0 |
| **FRD-08.3** | Menu utama **SHALL TIDAK** memakai chevron (**0 chevron**), persis seperti live. Chevron hanya boleh dipakai item yang benar-benar membuka daftar (`kategori`/`tag`/`penulis`/`arsip`/`dokumen`/`kontak`). | P0 |
| **FRD-08.4** | Pada viewport ≤ 1024 px, navigasi desktop **SHALL** digantikan drawer mobile yang dapat ditutup dengan `Esc` atau klik scrim. | P0 |
| **FRD-08.5** | Drawer **SHALL** mengunci scroll body saat terbuka dan mengembalikan fokus ke tombol pemicu saat ditutup. | P0 |
| **FRD-08.6** | Footer **SHALL** menampilkan tiga kolom: `Lebih Dekat`, `Eksplor balikisah.com`, `Topik Populer`, dan baris copyright. | P0 |
| **FRD-08.7** | Sistem **SHALL** menyediakan halaman 404 kustom yang konsisten secara visual. | P0 |
| **FRD-08.8** | Sistem **SHALL** menyediakan tombol "Kembali ke atas" pada halaman panjang. | P2 |
| **FRD-08.9** | Skip-to-content link **SHALL** ada sebagai elemen fokus pertama. | P0 |
| **FRD-08.10** | Halaman default **SHALL** adalah Beranda; arsip kategori **SHALL** tetap dapat diakses sebagai halaman tema. (**dikonfirmasi 5 Okt 2026**) | P0 |
| **FRD-08.11** | Footer **SHALL** memakai varian terang (ivory + hairline) sesuai UIRD §3.6. (**dikonfirmasi 5 Okt 2026**) | P1 |

---

## 9. Modul: Manajemen Konten

| ID | Requirement | Prioritas |
|---|---|---|
| **FRD-09.1** | Editor **SHALL** dapat membuat, mengubah, dan mengarsipkan artikel, kategori, tag, penulis, dan media. | P0 |
| **FRD-09.2** | Sistem **SHALL** mendukung status: `draft`, `review`, `scheduled`, `published`, `archived`. | P0 |
| **FRD-09.3** | Sistem **SHALL** mendukung penjadwalan terbit. | P1 |
| **FRD-09.4** | Sistem **SHALL** memvalidasi kelengkapan artikel sebelum terbit (kategori, ringkasan, gambar utama). | P0 |
| **FRD-09.5** | Sistem **SHALL** tidak mengizinkan perubahan slug tanpa membuat redirect 301. | P0 |
| **FRD-09.6** | Sistem **SHALL** mencatat riwayat perubahan artikel. | P1 |
| **FRD-09.7** | Sistem **SHOULD** menyediakan pratinjau artikel sebelum terbit. | P1 |
| **FRD-09.8** | Sistem **SHALL** generating gambar thumbnail pada ukuran yang dibutuhkan. | P1 |
| **FRD-09.9** | Gambar utama artikel **SHALL** dapat diisi dari **tautan** `http(s)` tanpa mengunggah berkas. | P0 |
| **FRD-09.10** | Tautan Google Drive `/file/d/<ID>/view` atau `?id=<ID>` **SHALL** dinormalisasi otomatis ke URL gambar langsung. | P1 |
| **FRD-09.11** | Sistem **SHOULD** menyediakan unggah foto ke Google Drive pengelola (scope `drive.file`, akses "siapa saja yang punya tautan") dan memasang tautannya ke artikel. | P1 |
| **FRD-09.12** | Foto dari berkas lokal **SHALL** diperkecil ke maksimum 1600 px sebelum disimpan, disertai keterangan bahwa foto itu hanya tersimpan di browser pengguna. | P1 |
| **FRD-09.13** | Peta foto **SHALL** dapat diekspor/diimpor sebagai `photos.json` agar dapat di-bake ke halaman statis. | P2 |

---

## 10. Modul: SEO & Metadata

| ID | Requirement | Prioritas |
|---|---|---|
| **FRD-10.1** | Setiap halaman **SHALL** memiliki `<title>` unik ≤ 60 karakter. | P0 |
| **FRD-10.2** | Setiap halaman **SHALL** memiliki meta description 140–160 karakter. | P0 |
| **FRD-10.3** | Setiap halaman **SHALL** memiliki canonical absolut self-referencing. | P0 |
| **FRD-10.4** | Setiap halaman **SHALL** memiliki Open Graph lengkap. | P0 |
| **FRD-10.5** | Sistem **SHALL** menghasilkan `sitemap.xml` yang otomatis dan mencakup seluruh halaman terindeks. | P0 |
| **FRD-10.6** | `robots.txt` **SHALL** mengizinkan perayapan penuh dan mendaftarkan sitemap. | P0 |
| **FRD-10.7** | Atribut `lang` **SHALL** bernilai `id-ID`. | P0 |
| **FRD-10.8** | Halaman kategori **SHALL** menyertakan `CollectionPage` JSON-LD. | P1 |
| **FRD-10.9** | Perubahan URL lama **SHALL** menghasilkan redirect 301 permanen. | P0 |
| **FRD-10.10** | Sistem **SHALL** mengembalikan 404 (bukan 200) untuk URL tidak dikenal. | P0 |

> **Kondisi live terverifikasi:** `lang="ID"`, canonical `http://`, dan tidak ada JSON-LD. Ketiganya adalah temuan yang harus diperbaiki pada tahap R0.

---

## 11. Modul: Analytics & Monitoring

| ID | Requirement | Prioritas |
|---|---|---|
| **FRD-11.1** | Sistem **SHALL** mengirim `page_view`, `scroll_depth`, dan `outbound_click` ke GA4. | P0 |
| **FRD-11.2** | Verifikasi Search Console **SHALL** dikonfigurasi dan diverifikasi. | P0 |
| **FRD-11.3** | Sistem **SHALL** melaporkan Core Web Vitals melalui `web-vitals` library. | P1 |
| **FRD-11.4** | Sistem **SHALL** mencatat error klien ke layanan monitoring tanpa mengirim data pribadi. | P1 |
| **FRD-11.5** | Analytics **SHALL** tidak memblokir render (dimuat setelah interaksi atau `requestIdleCallback`). | P0 |
| **FRD-11.6** | Halaman legal (privasi, syarat dan ketentuan) **SHALL** dikecualikan dari pelacakan analitik yang invasif. | P1 |

---

## 12. Modul: Newsletter

| ID | Requirement | Prioritas |
|---|---|---|
| **FRD-12.1** | Formulir newsletter **SHALL** berada di footer dan di akhir artikel. | P1 |
| **FRD-12.2** | Sistem **SHALL** memvalidasi alamat email dan menampilkan pesan kesalahan yang jelas. | P1 |
| **FRD-12.3** | Setelah berhasil, sistem **SHALL** menampilkan konfirmasi tanpa memuat ulang halaman. | P1 |
| **FRD-12.4** | Sistem **SHALL** menyimpan persetujuan pengguna sesuai kebijakan privasi. | P1 |
| **FRD-12.5** | Formulir **SHALL** dapat dioperasikan penuh dengan keyboard. | P1 |

---

## 13. Modul: Monetisasi

| ID | Requirement | Prioritas |
|---|---|---|
| **FRD-15.1** | Sistem **SHALL** menyediakan slot iklan 728×90, 300×250, dan 336×280. | P1 |
| **FRD-15.2** | Slot iklan **SHALL** tidak muncul di atas lipatan pada viewport < 1024 px. | P0 |
| **FRD-15.3** | Slot iklan **SHALL** tidak boleh disruptsi layout (wadah dengan dimensi tetap). | P0 |
| **FRD-15.4** | Konten bersponsor **SHALL** diberi label `Sponsored` / `Iklan` yang terlihat. | P0 |
| **FRD-15.5** | Slot iklan **SHALL** tidak disruptsi navigasi keyboard (tabindex `-1` + `aria-hidden`). | P0 |
| **FRD-15.6** | Kepadatan iklan **SHALL** dibatasi maksimal 1 slot per 300 px tinggi halaman artikel. | P1 |

---

## 14. Modul: Aksesibilitas Pendukung

| ID | Requirement | Prioritas |
|---|---|---|
| **FRD-17.1** | Setiap halaman **SHALL** memiliki tepat satu H1. | P0 |
| **FRD-17.2** | Semua kontrol interaktif **SHALL** dapat dicapai dan dioperasikan dengan keyboard. | P0 |
| **FRD-17.3** | Fokus **SHALL** selalu terlihat dan tidak pernah dihapus tanpa pengganti. | P0 |
| **FRD-17.4** | Semua gambar informatif **SHALL** memiliki `alt`; gambar dekoratif `alt=""`. | P0 |
| **FRD-17.5** | Filter chip **SHALL** melaporkan perubahan status secara konsisten melalui `aria-pressed`. | P0 |
| **FRD-17.6** | Drawer dan modal **SHALL** mengelola fokus (`focus trap` + kembalikan fokus). | P0 |
| **FRD-17.7** | Sistem **SHALL** menghormati `prefers-reduced-motion`. | P0 |
| **FRD-17.8** | Breadcrumb **SHALL** memakai `<nav aria-label="Breadcrumb">`. | P1 |

---

## 15. Persyaratan Non-Fungsional Ringkas

Dirinci di [QRD §2](Quality%20Requirements%20Document%20(QRD).md). Ringkas:

| ID | Target |
|---|---|
| NFR-01 | LCP < 2,5 s (p75) |
| NFR-02 | INP < 200 ms |
| NFR-03 | CLS < 0,1 |
| NFR-04 | TTFB < 800 ms |
| NFR-05 | Uptime 99,9% |
| NFR-06 | WCAG 2.1 AA |

---

## 16. Matriks Traceability Ringkas

| Requirement Sumber | Requirement Turunan | Modul |
|---|---|---|
| MRQ-01 | FRD-02, FRD-03 | Kategori & Artikel |
| MRQ-02 | FRD-02.3, FRD-05.1 | Arsip & Discovery |
| MRQ-03 | FRD-01.7, FRD-06.1 | Copy & Statis |
| MRQ-04 | FRD-03.3, CE-04 | Artikel |
| MRQ-05 | FRD-04, FRD-05 | Discovery |
| MRQ-06 | FRD-02.7, FRD-17 | Responsif & A11y |
| MRQ-07 | FRD-15 | Monetisasi |
| MRQ-08 | UIRD §1–§9 | UI |

---

## 17. Definition of Done

Sebuah fungsionalitas dianggap selesai bila:

1. ✅ Seluruh requirement terkait terimplementasi.
2. ✅ UAT fungsional disetujui pemilik produk.
3. ✅ NFR terkait ([QRD](Quality%20Requirements%20Document%20(QRD).md)) terverifikasi.
4. ✅ Tidak ada regresi pada halaman yang sudah ada.
5. ✅ SEO check lulus untuk halaman yang terdampak.
6. ✅ Dokumentasi pengguna diperbarui bila perlu.