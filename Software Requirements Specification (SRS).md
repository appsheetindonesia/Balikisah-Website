# Software Requirements Specification (SRS)

> **Project:** BaliKisah.com
> **Status:** Baseline v1.0
> **Tanggal:** 5 Oktober 2026
> **Dokumen induk:** [PRD](Product%20Requirements%20Document%20(PRD)%2018%20Section.md)
> **Dokumen terkait:** [MRD](Market%20Requirements%20Document%20(MRD).md) · [CRD](Customer%20Requirements%20Document%20(CRD).md) · [BRD](Business%20Requirements%20Document%20(BRD).md) · [UIRD](User%20Interface%20Requirements%20Document%20(UIRD).md) · [FRD](Functional%20Requirements%20Document%20(FRD).md) · [TRD](Technical%20Requirements%20Document%20(TRD).md) · [QRD](Quality%20Requirements%20Document%20(QRD).md)

---

## 1. Pendahuluan

### 1.1 Definisi

Sistem **BaliKisah Content Platform** adalah situs web editorial yang menyajikan dan mengelola konten tentang Bali dan Nusantara dalam Bahasa Indonesia.

### 1.2 Ruang Lingkup Dokumen

Dokumen ini adalah spesifikasi formal tingkat sistem. Rincian antarmuka ada di [FRD](Functional%20Requirements%20Document%20(FRD).md), rincian visual di [UIRD](User%20Interface%20Requirements%20Document%20(UIRD).md), dan rincian teknis di [TRD](Technical%20Requirements%20Document%20(TRD).md).

### 1.3 Definisi, Akronim, dan Singkatan

| Istilah | Definisi |
|---|---|
| CMS | Content Management System |
| SSG / ISR | Static Site Generation / Incremental Static Regeneration |
| CWV | Core Web Vitals (LCP, INP, CLS) |
| WCAG | Web Content Accessibility Guidelines |
| A11Y | Accessibility |
| P0/P1/P2 | Prioritas tinggi / sedang / rendah |
| RU | Reference Unit — piksel pada gambar referensi 756 px |

---

## 2. Deskripsi Sistem

### 2.1 Perspektif Produk

BaliKisah.com adalah situs **publishing-only**: pembaca hanya mengonsumsi, tidak berinteraksi selain pencarian, filter, dan newsletter. Tidak ada login, tidak ada profil pengguna, tidak ada transaksi.

### 2.2 Fungsi Sistem

| Kode | Fungsi | Deskripsi |
|---|---|---|
| F-10 | Content Presentation | Menyajikan artikel, kategori, dan halaman statis |
| F-20 | Navigation & Discovery | Membantu pembaca menemukan konten |
| F-30 | Search | Pencarian internal |
| F-40 | Content Management | Membuat dan mengelola konten |
| F-50 | SEO & Metadata | Menyediakan sinyal untuk mesin pencari |
| F-60 | Analytics | Mengukur perilaku dan kinerja |
| F-70 | Engagement | Newsletter dan berbagi |

### 2.3 Pengguna Sistem

| Peran | Keterangan | Akses |
|---|---|---|
| **Pembaca** | Pengunjung tidak terautentikasi | Baca, cari, filter, newsletter |
| **Editor** |Managing konten | Tambah, ubah, terjadwalkan artikel |
| **Admin** | Pengelola sistem | Konfigurasi, pengguna, backup |
| **Perayapan** | Crawler mesin pencari | Akses seluruh halaman terindeks |

### 2.4 KOperand

| # | Koperand | Peran |
|---|---|---|
| 1 | Server web / platform hosting | Menyajikan situs |
| 2 | CDN | Cache dan optimasi |
| 3 | Headless CMS | Menyimpan konten |
| 4 | Object storage | Menyimpan media |
| 5 | GA4 + Search Console | Menganalisis |
| 6 | Penyedia email (newsletter) | Mengirim surel |

### 2.5 Batasan

| ID | Batasan |
|---|---|
| L-01 | Bahasa hanya Bahasa Indonesia pada fase 1 |
| L-02 | Tidak ada autentikasi pembaca |
| L-03 | Platform-static-first; input dinamis terbatas pada pencarian dan formulir |
| L-04 | Maksimal ± 2.000 artikel per tahun |

### 2.6 Asumsi

| ID | Asumsi |
|---|---|
| A-01 | Headless CMS tersedia sebagai sumber konten |
| A-02 | Tim kecil (1–3 orang) |
| A-03 | Konten tersedia sepanjang masa proyek |
| A-04 | Server memadai |

---

## 3. Kebutuhan Fungsional Tingkat Sistem

Format: `SRS-F-nn`.

### 3.1 Content Presentation

| ID | Requirement |
|---|---|
| **SRS-F-101** | Sistem SHALL menampilkan artikel dengan judul, ringkasan, isi, gambar utama, penulis, tanggal terbit, waktu baca, dan kategori. |
| **SRS-F-102** | Sistem SHALL menampilkan arsip kategori dengan H1, chip filter, dan grid kartu 4 kolom pada desktop. |
| **SRS-F-103** | Sistem SHALL menampilkan halaman statis (tentang, privasi, syarat, disclaimer, FAQ, kontak). |
| **SRS-F-104** | Sistem SHALL menampilkan halaman 404 kustom untuk URL tidak dikenal. |
| **SRS-F-105** | Sistem SHALL menampilkan halaman kosong yang informatif untuk kategori tanpa artikel. |
| **SRS-F-106** | Sistem SHALL menampilkan pembacaan hingga 2 baris untuk judul dan 3 baris untuk ringkasan pada kartu. |
| **SRS-F-107** | Sistem SHALL menerapkan filter sepia pada thumbnail kategori sejarah/babad. |
| **SRS-F-108** | Sistem SHALL menampilkan lebar baca maksimum 720 px pada badan artikel. |

### 3.2 Navigation & Discovery

| ID | Requirement |
|---|---|
| **SRS-F-201** | Sistem SHALL menampilkan header dengan logo di kiri, navigasi di kanan, dan CTA paling kanan. |
| **SRS-F-202** | Sistem SHALL menyediakan drawer navigasi pada viewport ≤ 1024 px yang dapat ditutup dengan `Esc` atau klik scrim. |
| **SRS-F-203** | Sistem SHALL mengelola fokus pada drawer: focus trap saat terbuka, pengembalian fokus saat ditutup. |
| **SRS-F-204** | Sistem SHALL menyediakan breadcrumb pada halaman artikel dan halaman statis. |
| **SRS-F-205** | Sistem SHALL menampilkan minimal 3 artikel terkait pada akhir artikel. |
| **SRS-F-206** | Sistem SHALL menampilkan blok Topik Populer sesuai konfigurasi. |
| **SRS-F-207** | Sistem SHALL menyediakan skip-to-content link sebagai elemen fokus pertama. |
| **SRS-F-208** | Sistem SHALL menyediakan pagination pada arsip kategori dengan elipsis bila halaman > 7. |

### 3.3 Search

| ID | Requirement |
|---|---|
| **SRS-F-301** | Sistem SHALL menyediakan input pencarian di header desktop dan drawer mobile. |
| **SRS-F-302** | Sistem SHALL menampilkan hasil pada URL `?q=` agar dapat dibagikan. |
| **SRS-F-303** | Sistem SHALL menandai hasil dengan kategori dan tanggal. |
| **SRS-F-304** | Sistem SHALL melakukan debounce 300 ms pada input pencarian. |
| **SRS-F-305** | Sistem SHALL menampilkan saran bila hasil kosong. |
| **SRS-F-306** | Sistem SHALL menandai halaman hasil dengan `noindex`. |

### 3.4 Content Management

| ID | Requirement |
|---|---|
| **SRS-F-401** | Sistem SHALL mendukung CRUD untuk artikel, kategori, tag, penulis, dan media. |
| **SRS-F-402** | Sistem SHALL mendukung status `draft`, `review`, `scheduled`, `published`, `archived`. |
| **SRS-F-403** | Sistem SHALL memvalidasi kelengkapan artikel sebelum terbit. |
| **SRS-F-404** | Sistem SHALL tidak mengizinkan perubahan slug tanpa redirect 301. |
| **SRS-F-405** | Sistem SHALL mencatat riwayat perubahan artikel. |
| **SRS-F-406** | Sistem SHALL menyediakan pratinjau sebelum terbit. |

### 3.5 SEO & Metadata

| ID | Requirement |
|---|---|
| **SRS-F-501** | Sistem SHALL menyediakan `<title>` unik ≤ 60 karakter per halaman. |
| **SRS-F-502** | Sistem SHALL menyediakan meta description 140–160 karakter per halaman. |
| **SRS-F-503** | Sistem SHALL menyediakan canonical absolut self-referencing. |
| **SRS-F-504** | Sistem SHALL menyertakan JSON-LD `Article`, `BreadcrumbList`, `WebSite`, dan `Person`. |
| **SRS-F-505** | Sistem SHALL menghasilkan `sitemap.xml` otomatis dan lengkap. |
| **SRS-F-506** | Sistem SHALL menyajikan `robots.txt` yang wajar dan mendaftarkan sitemap. |
| **SRS-F-507** | Sistem SHALL menyajikan Open Graph dan Twitter Card lengkap. |
| **SRS-F-508** | Sistem SHALL menggunakan `lang="id-ID"`. |
| **SRS-F-509** | Sistem SHALL mengembalikan 404 untuk URL tidak dikenal, bukan 200. |
| **SRS-F-510** | Sistem SHALL mengarahkan URL lama dengan redirect 301 permanen. |

### 3.6 Analytics

| ID | Requirement |
|---|---|
| **SRS-F-601** | Sistem SHALL mengirim `page_view`, `scroll_depth`, `outbound_click` ke GA4. |
| **SRS-F-602** | Sistem SHALL melaporkan Core Web Vitals. |
| **SRS-F-603** | Sistem SHALL tidak memblokir render saat memuat analytics. |
| **SRS-F-604** | Sistem SHALL dikecualikan dari pelacakan invasif pada halaman legal. |

### 3.7 Engagement & Monetization

| ID | Requirement |
|---|---|
| **SRS-F-701** | Sistem SHALL menyediakan formulir newsletter di footer dan akhir artikel. |
| **SRS-F-702** | Sistem SHALL memvalidasi alamat email dan menampilkan konfirmasi tanpa muat ulang. |
| **SRS-F-703** | Sistem SHALL menyediakan tombol berbagi (salin tautan, WhatsApp, Facebook, X). |
| **SRS-F-704** | Sistem SHALL menyediakan slot iklan 728×90, 300×250, 336×280. |
| **SRS-F-705** | Sistem SHALL tidak menampilkan iklan di atas lipatan pada viewport < 1024 px. |
| **SRS-F-706** | Sistem SHALL melabeli konten bersponsor secara terlihat. |

---

## 4. Kebutuhan Non-Fungsional Tingkat Sistem

Format: `SRS-NF-nn`.

### 4.1 Performa

| ID | Requirement | Metrik |
|---|---|---|
| **SRS-NF-101** | Waktu muat halaman utama | LCP < 2,5 s (p75 mobile) |
| **SRS-NF-102** | Responsivitas interaksi | INP < 200 ms |
| **SRS-NF-103** | Stabilitas visual | CLS < 0,1 |
| **SRS-NF-104** | Respons server | TTFB < 800 ms |
| **SRS-NF-105** | Ukuran JavaScript first-load | ≤ 120 KB (gzip) |
| **SRS-NF-106** | Rasio cache | ≥ 90% |

### 4.2 Keandalan

| ID | Requirement |
|---|---|
| **SRS-NF-201** | Ketersediaan ≥ 99,9% per bulan |
| **SRS-NF-202** | Tingkat error 5xx < 0,05% |
| **SRS-NF-203** | Pemulihan (rollback) < 15 menit |

### 4.3 Keamanan

| ID | Requirement |
|---|---|
| **SRS-NF-301** | Seluruh halaman disajikan via HTTPS dengan HSTS |
| **SRS-NF-302** | 6 security headers terpasang (lihat [TRD §9](Technical%20Requirements%20Document%20(TRD).md)) |
| **SRS-NF-303** | Nol kerentanan dependency kritis |
| **SRS-NF-304** | Input formulir disanitasi (anti-XSS) |
| **SRS-NF-305** | Backup harian basis data konten, retensi 30 hari |
| **SRS-NF-306** | Tidak menyimpan data pribadi di sisi klien |

### 4.4 Aksesibilitas

| ID | Requirement |
|---|---|
| **SRS-NF-401** | WCAG 2.1 level AA |
| **SRS-NF-402** | Rasio kontras teks ≥ 4,5:1 |
| **SRS-NF-403** | 100% kontrol dapat dioperasikan keyboard |
| **SRS-NF-404** | 100% gambar informatif memiliki alt |
| **SRS-NF-405** | Fokus selalu terlihat |
| **SRS-NF-406** | `prefers-reduced-motion` dihormati |

### 4.5 Kompatibilitas

| ID | Requirement |
|---|---|
| **SRS-NF-501** | Mendukung 2 versi terakhir Chrome, Firefox, Safari, Edge |
| **SRS-NF-502** | Mendukung viewport 320 – 2560 px |
| **SRS-NF-503** | Konten artikel tetap terbaca tanpa JavaScript |

---

## 5. Model Data

### 5.1 Entitas

```
Article (id PK, slug UQ, title, excerpt, body, coverImageId FK,
         categoryId FK, status, readingTime, publishedAt, updatedAt, seoMeta)
Category (id PK, slug UQ, name, description, parentId FK, order, coverImageId FK)
Tag (id PK, slug UQ, name)
ArticleTag (articleId FK, tagId FK) — junction
Author (id PK, slug UQ, name, bio, avatarUrl, socialLinks)
Media (id PK, url, alt, width, height, credits)
Page (id PK, slug UQ, title, body, type, updatedAt)
```

### 5.2 Relasi

```
Category ──1:N──> Article ──N:1──> Author
Category ──1:N──> Category (self, parent-child)
Article  ──N:M──> Tag
Article  ──N:1──> Media (coverImage)
```

### 5.3 Kendala Integritas

| ID | Kendala |
|---|---|
| CI-01 | `slug` unik per entitas dan immutable setelah terbit |
| CI-02 | `status` harus berada dalam enum yang ditentukan |
| CI-03 | Jika `status = published`, maka `publishedAt` harus terisi dan ≤ waktu sekarang |
| CI-04 | Setiap artikel memiliki tepat satu `categoryId` yang tidak null |
| CI-05 | `excerpt` maksimal 300 karakter |
| CI-06 | `title` maksimal 200 karakter |
| CI-07 | Relasi kategori induk tidak boleh membentuk siklus |

---

## 6. Antarmuka Eksternal

| ID | Antarmuka | Tipe | Metode |
|---|---|---|---|
| EI-01 | Headless CMS REST API | Input | HTTPS GET (build-time) |
| EI-02 | Object storage (gambar) | Input/Output | HTTPS |
| EI-03 | GA4 Measurement Protocol | Output | HTTPS POST |
| EI-04 | Search Console API | Output | HTTPS (manual/periodic) |
| EI-05 | Penyedia email newsletter | Output | HTTPS POST |
| EI-06 | CDN edge | Output | HTTPS |
| EI-07 | Iklan (jika aktif) | Output | Skrip pihak ketiga |
| EI-08 | Sentry (monitoring) | Output | HTTPS POST |

> **Catatan privasi:** EI-07 (iklan pihak ketiga) berpotensi melanggar privasi. Wajib menggunakan skrip yang tidak menyimpan data pribadi, dan disdain Betrieb ada Persetujuan.

---

## 7. Persyaratan Antarmuka Pengguna

Rincian penuh di [UIRD](User%20Interface%20Requirements%20Document%20(UIRD).md). Ringkasan formal:

| ID | Requirement |
|---|---|
| **SRS-UI-01** | Latar halaman `#F7F0DD`; header dan permukaan kartu `#FFFFFF`. |
| **SRS-UI-02** | Aksen interaktif `#94542E`; chip aktif `#8F5432`. |
| **SRS-UI-03** | Judul memakai serif (Playfair Display); UI memakai sans (Inter). |
| **SRS-UI-04** | Container 1120 px pada ≥ 1280 px. |
| **SRS-UI-05** | Grid 4 / 3 / 2 / 1 kolom pada 1280 / 1024 / 768 / < 640 px. |
| **SRS-UI-06** | Kartu: radius 14 px, border 1 px, tanpa shadow berat. |
| **SRS-UI-07** | Rasio gambar kartu 3:2. |
| **SRS-UI-08** | Filter chip berbentuk pill dengan `aria-pressed`. |
| **SRS-UI-09** | URL logo adalah `balikisah.com` — **DIKONFIRMASI 5 Okt 2026**; berlaku untuk seluruh identitas (logo, judul halaman, kolom footer, copyright). |
| **SRS-UI-10** | Label navigasi `Home`, `Budaya`, `Tradisi`, `Kuliner`, `Sejarah`, `Wisata`, `Tips Traveling`, `Tentang Kami` (**8 item, 0 chevron**) — **DIKONFIRMASI 7 Okt 2026**, disamakan dengan balikisah.com. CTA `Hubungi Kami` tetap ada di header. Label referensi `Kategori`/`Kerajaan`/`Stonian`/`Blog`/`Kontak` tidak lagi dipakai. |
| **SRS-UI-11** | Footer memakai varian terang: `--ivory` dengan pemisah `--hairline`, judul `--ink-900`, teks `--ink-400` — **DIKONFIRMASI 5 Okt 2026**. |
| **SRS-UI-12** | Halaman default/*canonical* adalah **Beranda**; arsip kategori tetap tersedia sebagai halaman tema — **DIKONFIRMASI 5 Okt 2026**. |

---

## 8. Skenario Operasi

| ID | Skenario | Rangkaian langkah |
|---|---|---|
| SC-01 | Pembaca menemukan artikel | Landing → Cari → Hasil → Artikel → Related |
| SC-02 | Pembaca menjelajah kategori | Beranda → Kategori → Chip filter → Artikel |
| SC-03 | Editor menerbitkan artikel | Login CMS → Tulis → Validasi → Terbitkan → Rebuild/ISR |
| SC-04 | Editor menjadwalkan artikel | Tulis → Atur tanggal → Status `scheduled` → Auto-publish |
| SC-05 | Pengunjung mesin pencari | Crawl → Ikuti sitemap → Baca halaman → Indeks |
| SC-06 | Pembaca berlangganan | Artikel/footer → Isi email → Submit → Konfirmasi |
| SC-07 | RilisFailure | Deploy gagal → Rollback → Verifikasi |
| SC-08 | Insiden keamanan | Deteksi → Mitigasi → Patch → Post-mortem |

---

## 9. Matriks Traceability Lengkap

### 9.1 Pasar → Produk

| ID | Sumber | Turunan |
|---|---|---|
| MRQ-01 | [MRD §7](Market%20Requirements%20Document%20(MRD).md) | SRS-F-102, SRS-F-103 |
| MRQ-02 | [MRD §7](Market%20Requirements%20Document%20(MRD).md) | SRS-F-205, SRS-F-208 |
| MRQ-03 | [MRD §7](Market%20Requirements%20Document%20(MRD).md) | SRS-F-508, SRS-F-102 |
| MRQ-04 | [MRD §7](Market%20Requirements%20Document%20(MRD).md) | SRS-F-103 |
| MRQ-05 | [MRD §7](Market%20Requirements%20Document%20(MRD).md) | SRS-F-301…306 |
| MRQ-06 | [MRD §7](Market%20Requirements%20Document%20(MRD).md) | SRS-NF-401…406, SRS-NF-502 |
| MRQ-07 | [MRD §7](Market%20Requirements%20Document%20(MRD).md) | SRS-F-704…706 |
| MRQ-08 | [MRD §7](Market%20Requirements%20Document%20(MRD).md) | SRS-UI-01…08 |

### 9.2 Pelanggan → Produk

| ID | Sumber | Turunan |
|---|---|---|
| CRQ-01 | [CRD §2](Customer%20Requirements%20Document%20(CRD).md) | SRS-F-301…306, SRS-F-205 |
| CRQ-02 | [CRD §2](Customer%20Requirements%20Document%20(CRD).md) | SRS-NF-502, SRS-UI-05 |
| CRQ-03 | [CRD §2](Customer%20Requirements%20Document%20(CRD).md) | SRS-F-101, SRS-F-508 |
| CRQ-04 | [CRD §2](Customer%20Requirements%20Document%20(CRD).md) | SRS-F-205, SRS-F-206 |
| CRQ-05 | [CRD §2](Customer%20Requirements%20Document%20(CRD).md) | SRS-F-703 |
| CRQ-06 | [CRD §2](Customer%20Requirements%20Document%20(CRD).md) | SRS-F-701, SRS-F-702 |
| CRQ-07 | [CRD §2](Customer%20Requirements%20Document%20(CRD).md) | SRS-F-705 |
| CRQ-08 | [CRD §2](Customer%20Requirements%20Document%20(CRD).md) | Tidak ada (fase 2) |

### 9.3 Bisnis → Produk

| ID | Sumber | Turunan |
|---|---|---|
| BN-01 | [BRD §2](Business%20Requirements%20Document%20(BRD).md) | SRS-F-501…510 |
| BN-02 | [BRD §2](Business%20Requirements%20Document%20(BRD).md) | SRS-F-205, SRS-F-206 |
| BN-03 | [BRD §2](Business%20Requirements%20Document%20(BRD).md) | SRS-UI-01…08 |
| BN-04 | [BRD §2](Business%20Requirements%20Document%20(BRD).md) | SRS-F-401…406 |
| BN-05 | [BRD §2](Business%20Requirements%20Document%20(BRD).md) | SRS-F-704…706 |
| BN-06 | [BRD §2](Business%20Requirements%20Document%20(BRD).md) | SRS-F-701, SRS-F-702 |

### 9.4 Requirement → Verifikasi

| ID | Metode verifikasi | Sumber |
|---|---|---|
| SRS-F-101…108 | E2E + visual | [QRD §3](Quality%20Requirements%20Document%20(QRD).md) |
| SRS-F-201…208 | E2E + manual keyboard | [QRD §3](Quality%20Requirements%20Document%20(QRD).md) |
| SRS-F-301…306 | E2E | [QRD §3.1](Quality%20Requirements%20Document%20(QRD).md) |
| SRS-F-401…406 | Manual (CMS) | [FRD §9](Functional%20Requirements%20Document%20(FRD).md) |
| SRS-F-501…510 | Rich Results Test + Search Console | [TRD §7](Technical%20Requirements%20Document%20(TRD).md) |
| SRS-F-601…604 | GA4 DebugView | [TRD §10](Technical%20Requirements%20Document%20(TRD).md) |
| SRS-F-701…706 | E2E | [QRD §3.1](Quality%20Requirements%20Document%20(QRD).md) |
| SRS-NF-101…106 | Lighthouse CI + CrUX | [TRD §6](Technical%20Requirements%20Document%20(TRD).md) |
| SRS-NF-201…203 | UptimeRobot | [QRD §6](Quality%20Requirements%20Document%20(QRD).md) |
| SRS-NF-301…306 | Security audit | [TRD §9](Technical%20Requirements%20Document%20(TRD).md) |
| SRS-NF-401…406 | axe + manual | [UIRD §8](User%20Interface%20Requirements%20Document%20(UIRD).md) |
| SRS-NF-501…503 | Playwright matrix | [UIRD §13](User%20Interface%20Requirements%20Document%20(UIRD).md) |
| SRS-UI-01…08 | Visual diff | [QRD §3.2](Quality%20Requirements%20Document%20(QRD).md) |

### 9.5 Asumsi → Dampak

| Asumsi | Dampak bila salah |
|---|---|
| A-01 Headless CMS tersedia | SRS-F-401…406 tidak dapat diimplementasikan |
| A-02 Tim kecil | Cakupan R4–R5 mundur |
| A-03 Konten tersedia | SRS-F-103 tidak terisi |
| A-04 Server memadai | SRS-NF-101…104 tidak tercapai |

---

## 10. Temuan Audit terhadap Implementasi Saat Ini

Ditemukan melalui inspeksi langsung `http://balikisah.com/` (5 Oktober 2026):

| # | Temuan | Requirement yang dilanggar | Prioritas |
|---|---|---|---|
| A-01 | Skema `http://` | SRS-NF-301 | **P0** |
| A-02 | `lang="ID"` | SRS-F-508 | **P1** |
| A-03 | Tanpa JSON-LD | SRS-F-504 | **P1** |
| A-04 | Tailwind runtime CDN | SRS-NF-105, SRS-NF-103 | **P0** |
| A-05 | 23 family font | SRS-NF-105 | **P0** |
| A-06 | Logo `Bali Kisah` (bukan `balikisah.com`) | SRS-UI-09 | **SELESAI 5 Okt 2026** — diputuskan `balikisah.com` |
| A-07 | Navigasi hanya hamburger | SRS-F-201 | **P1** |
| A-08 | Teks Inggris tidak diterjemahkan | SRS-F-103 (en) | **P1** |
| A-09 | Penulis tunggal | SRS-F-401 (model) | **P2** |
| A-10 | Histats (pihak ketiga) | SRS-NF-301 (privasi) | **P1** |

---

## 11. Persyaratan Verifikasi & Validasi

| ID | Persyaratan |
|---|---|
| VV-01 | Setiap requirement fungsional diuji minimal satu test. |
| VV-02 | Uji validasi konten: artikel tanpa kategori ditolak_system. |
| VV-03 | Uji validasi tampilan: UAT visual oleh pemilik produk. |
| VV-04 | Uji aksesibilitas: audit otomatis + manual keyboard. |
| VV-05 | Uji performa: Lighthouse CI pada setiap PR. |
| VV-06 | Uji keamanan: audit dependency + verification headers. |
| VV-07 | Uji regresi SEO: monitoring Search Console 14 hari setelah rilis. |

---

## 12. lampiran — Glossary Istilah Konten Bali

| Istilah | Arti |
|---|---|
| **Babad** | Naskah sejarah tradisional Bali |
| **Kerajaan** | Sistem pemerintahan pada masa Hindu-Buddha di Bali |
| **Subak** | Sistem irigasi tradisional Bali yang diakui UNESCO |
| **Tri Hita Karana** | Filsafat keseimbangan manusia, alam, dan Dewa |
| **Melasti** | Ritual penyucian sebelum Hari Raya Nyepi |
| **Pura** | Tempat pemujaan di Bali |
| **Ongkos** | Biaya (dalam bahasa Bali) |
| **Banjar** | Sistem pemerintahan desa tradisional Bali |

---

## 13. Riwayat Revisi

| Versi | Tanggal | Perubahan | Penulis |
|---|---|---|---|
| 1.0 | 5 Okt 2026 | Baseline. Disusun dari audit langsung situs live + dokumen induk. | Requirements Engineering |

---

**Dokumen selesai.** For full detail, refer to the linked documents in the header.
**Trilingual note:** Dokumen ini disusun dalam Bahasa Indonesia dengan istilah teknis English (standar industri). Istilah kunci tetap dalam Bahasa Indonesia agar konsisten dengan [PRD §6](Product%20Requirements%20Document%20(PRD)%2018%20Section.md).