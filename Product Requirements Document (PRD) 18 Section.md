# Product Requirements Document (PRD)

> **Project:** BaliKisah.com
> **Status:** Baseline v1.0
> **Tanggal:** 5 Oktober 2026
> **Struktur:** 18 seksi
> **Dokumen terkait:** [MRD](Market%20Requirements%20Document%20(MRD).md) · [CRD](Customer%20Requirements%20Document%20(CRD).md) · [BRD](Business%20Requirements%20Document%20(BRD).md) · [UIRD](User%20Interface%20Requirements%20Document%20(UIRD).md) · [FRD](Functional%20Requirements%20Document%20(FRD).md) · [TRD](Technical%20Requirements%20Document%20(TRD).md) · [QRD](Quality%20Requirements%20Document%20(QRD).md) · [SRS](Software%20Requirements%20Specification%20(SRS).md)

---

## 1. Document Control

| Field | Value |
|---|---|
| Nama produk | BaliKisah.com |
| Versi dokumen | 1.0 (Baseline) |
| Tanggal | 5 Oktober 2026 |
| Penulis | Requirements Engineering |
| Pemangku | Pemilik Produk **[menunggu]** |
| Konteks | Rebuild / Requirement disusun untuk produk yang sudah ada dan berjalan di `balikisah.com` |

**Riwayat revisi**

| Versi | Tanggal | Perubahan |
|---|---|---|
| 1.0 | 5 Okt 2026 | Baseline pertama, disusun dari observasi situs live + screenshot referensi |

---

## 2. Product Overview

BaliKisah.com adalah **media editorial digital** berbahasa Indonesia yang menyajikan cerita, budaya, sejarah, wisata, kuliner, dan warisan budaya Bali serta Nusantara.

**Fungsi inti:** membuat pembaca menemukan, memahami, dan menyimpan konten tepercaya tentang Bali.

**Produk ini bukan:** OTA, portal berita, media sosial, atau toko.

### 2.1 Kondisi Terverifikasi saat Ini

| Aspek | Kondisi live (terverifikasi) | Target |
|---|---|---|
| Tema | Navy `#2b2b60`, latar `#fdfdfd` | Ivory `#F7F0DD`, aksen terracotta `#94542E` |
| Font | `Julius Sans One` | Playfair Display + Inter |
| Logo | `Bali Kisah` | `balikisah.com` |
| Navigasi | Hamburger saja | Nav desktop + CTA + mobile drawer |
| Skema | `http://` | `https://` |
| `lang` | `ID` | `id-ID` |
| Structured data | Tidak ada | JSON-LD lengkap |
| Bahasa UI | Campur ID/EN | Konsisten Bahasa Indonesia |
| Penulis | Tunggal (`Subrata`) | Multi-penulis |
| Container | `1100px` | `1120px` |

---

## 3. Problem Statement

Pembaca tidak memiliki sumber tepercaya berbahasa Indonesia yang mengmenggabungkan resejarah, budaya, dan praktis perjalanan Bali dalam satu tempat yang rapi, cepat, dan layak disimpan.

**Dampak bisnis:** tanpa otoritas dan struktur, traffic organik tidak tumbuh dan monetisasi tidak mungkin.

---

## 4. Goals & Non-Goals

### 4.1 Goals

| ID | Tujuan | Ukuran |
|---|---|---|
| G-01 | Traffic organik | +300% dalam 12 bulan |
| G-02 | Keterlibatan | Pages/session ≥ 1,8 |
| G-03 | Otoritas | Backlink natural ≥ 15 |
| G-04 | Kualitas | Koreksi editorial ≤ 1% |
| G-05 | Performa | Core Web Vitals seluruhnya hijau |
| G-06 | Monetisasi | Revenue/session ≥ Rp 1.500 |

### 4.2 Non-Goals (untuk 12 bulan ke depan)

- Membangun aplikasi mobile native.
- Menyediakan transaksi atau booking.
- Membuat video orisinal.
- Jadi portal berita breaking news.
-versi bahasa Inggris penuh.

---

## 5. Target Users & Segments

Rincian persona ada di [CRD §3](Customer%20Requirements%20Document%20(CRD).md). Ringkasan:

| Segmen | Peran dalam produk | Halaman utama |
|---|---|---|
| **Wisatawan domestik** | Pengguna inti, volume terbesar | Beranda, Wisata, Itinerary |
| **Pembaca berbasis pencarian** |-landed langsung dari Google | Artikel, Kategori |
| **Penikmat budaya** | Pembaca dalam, dwell time panjang | Sejarah, Budaya, Tradisi |
| **Pelajar** | Sesi pendek, tinggi bounce | Artikel, Daftar |
| **Wisatawan mancanegara** | Pasar sekunder | Artikel, Info praktis |

---

## 6. Language & Localization

| Kebutuhan | Keputusan | Catatan |
|---|---|---|
| Bahasa utama | Bahasa Indonesia | Seluruh UI dan konten |
| Metadata | `lang="id-ID"` | Live saat ini `ID` → **perbaiki** |
| Nama kategori | Bahasa Indonesia | Yang sudah konsisten di live |
| Istilah Inggris | Hanya jika umum (itinerary, hidden gem, UNESCO) | Glossarium internal |
| Judul CTA | `Hubungi Kami` (**dikonfirmasi 5 Okt 2026**) | Live & referensi memakai `Contact us`; atas permintaan pengguna diterjemahkan penuh |
| Tanggal | Format Indonesia | `21 Nov 2023` |
| Angka | Format Indonesia | Pemisah ribuan titik |
| Mata uang | Rupiah | Contoh: Rp 1.500.000 |

> **Temuan:** halaman live memuat teks Inggris yang tidak diterjemahkan — `Hottest Articles`, `Read More`, `Discover the latest trending articles`, `Explore our archive of articles…`. Ini akan ditangani pada [FRD §9](Functional%20Requirements%20Document%20(FRD).md).

---

## 7. Information Architecture

```
Beranda
├── Kategori
│   ├── Budaya
│   ├── Tradisi
│   ├── Sejarah
│   │   └── Sub: Kerajaan · Tokoh · Candi · Babad
│   ├── Wisata
│   │   └── Sub: Hidden Gem · Itinerary ·family · Bali Utara
│   ├── Kuliner
│   │   └── Sub: Tradisional · Halal · Spesial
│   ├── Cerita Lokal
│   └── Warisan Budaya
├── Artikel (/{slug})
├── Pencarian (/cari?q=)
├── Tag (/{tag})
├── Kolom Perspektif / Blog
├── Kerajaan (indeks khusus)
├── Halaman Statis
│   ├── Tentang Kami
│   ├── Kebijakan Privasi
│   ├── Syarat dan Ketentuan
│   ├── Disclaimer
│   ├── FAQ
│   └── Hubungi Kami
└── Topik Populer
    ├── Hidden Gem Bali · Tradisi Bali · Pura Bali
    ├── Makanan Khas · Itinerary Bali · Warisan Budaya Bali
```

> **Catatan:** referensi visual pada [UIRD](User%20Interface%20Requirements%20Document%20(UIRD).md) memakai label navigasi `Kategori`, `Kerajaan`, `Stonian`, `Blog`, `Contact`. Label `Stonian`, `Soratirin`, dan `listowa` **merupakan placeholder yang perlu dikonfirmasi** — lihat [UIRD §16](User%20Interface%20Requirements%20Document%20(UIRD).md).
>
> **Pembaruan 7 Okt 2026 (PD-09):** menu utama tidak lagi memakai label
> referensi di atas; navigasi disamakan dengan balikisah.com menjadi 8 tautan
> tanpa chevron (`Home`, `Budaya`, `Tradisi`, `Kuliner`, `Sejarah`, `Wisata`,
> `Tips Traveling`, `Tentang Kami`).

---

## 8. Core User Journeys

### Journey A — Pencarian (P1)
```
Google → Beranda → Cari "itinerary bali 3 hari"
       → Hasil → Artikel → Related → Baca 2 artikel → Bookmark
```

### Journey B — Jelajah Arsip (P2)
```
Beranda → Kategori "Sejarah"
       → Archive "Sejarah dan Babad Bali"
       → Chip filter "Tokoh Sejarah"
       → Daftar kartu → Artikel → Related → Selesai
```

### Journey C — Retensi (P4)
```
Baca artikel → Newsletter signup → Buka email 7 hari
            → Baca artikel baru → Kembali
```

---

## 9. Feature Scope

### 9.1 Fase 1 — Wajib (MVP)

| ID | Fitur | Prioritas | Trace |
|---|---|---|---|
| F-01 | Beranda: hero, latest, trending, read more | P0 | FRD-01 |
| F-02 | Arsip kategori + chip filter | P0 | FRD-02 |
| F-03 | Halaman artikel lengkap | P0 | FRD-03 |
| F-04 | Pencarian internal | P0 | FRD-04 |
| F-05 | Artikel terkait | P0 | FRD-05 |
| F-06 | Halaman statis | P0 | FRD-06 |
| F-07 | Pagination | P0 | FRD-07 |
| F-08 | Header & footer global | P0 | FRD-08 |
| F-09 | Sitemap + robots + schema | P0 | FRD-10 |
| F-10 | Analytics & monitoring | P0 | FRD-11 |

### 9.2 Fase 2 — Penting

| ID | Fitur | Prioritas | Trace |
|---|---|---|---|
| F-11 | Newsletter signup | P1 | FRD-12 |
| F-12 | Tag index | P1 | FRD-13 |
| F-13 | Halaman penulis | P1 | FRD-14 |
| F-14 | Konten bersponsor (berlabel) | P1 | FRD-15 |
| F-15 | Breadcrumb + JSON-LD | P1 | FRD-16 |

### 9.3 Fase 3 — Nanti

| ID | Fitur | Prioritas |
|---|---|---|
| F-16 | Pencarian lanjutan (filter, sort) | P2 |
| F-17 | Bookmark pembaca (tanpa login) | P2 |
| F-18 | Mode gelap | P2 |
| F-19 | Komentar | P2 |
| F-20 | Versi bahasa Inggris | P2 |

---

## 10. Functional Summary

Rincian ada di [FRD](Functional%20Requirements%20Document%20(FRD).md). Ringkas:

1. **Konten** — CRUD artikel, kategori, tag, media, penulis.
2. **Navigasi** — header, menu, breadcrumb, footer, sitemap XML.
3. **Discovery** — pencarian, filter, related, trending, topik populer.
4. **Engagement** — newsletter, share, baca terkait.
5. **Administrasi** — analytics, konfigurasi, editorial calendar.

---

## 11. Content & Editorial Standards

| ID | Standar |
|---|---|
| CE-01 | Setiap artikel memiliki kategori utama dan minimal 1 tag |
| CE-02 | Ringkasan 140–160 karakter |
| CE-03 | Minimal 800 kata untuk artikel fitur |
| CE-04 | Klaim faktual wajib punya sumber atau kalimat penafian |
| CE-05 | Tidak ada Sterilized konten yang memerlukan peringatan |
| CE-06 | Tanggal revise dicatat bila konten diperbarui |
| CE-07 | Gambar wajib punya alt deskriptif dan credits bila perlu |
| CE-08 | Nama orang, tempat, dan dynasty harus konsisten |

**Rujukan klaim budaya (bukan fakta):**
> "Menurut[nama sumber], …" atau "Cara-cara ini bervariasi antar wilayah."

---

## 12. User Interface Requirements

Rincian lengkap ada di [UIRD](User%20Interface%20Requirements%20Document%20(UIRD).md).

Ringkasan:

| Aspek | Nilai |
|---|---|
| Tema | Ivory hangat + aksen terracotta |
| Font | Playfair Display (display) + Inter (UI) |
| Latar halaman | `#F7F0DD` |
| Aksen | `#94542E` |
| Header | Putih, logo kiri, nav kanan, CTA |
| Kartu | 4 kolom, radius 14 px, border tipis, tanpa shadow berat |
| Treatment gambar | Sepia pada arsip sejarah |

---

## 13. Data & Content Model

### 13.1 Entitas Utama

| Entitas | Field inti |
|---|---|
| **Article** | `id, slug, title, excerpt, body, coverImage, categoryId, tags[], authorId, publishedAt, updatedAt, status, readingTime` |
| **Category** | `id, slug, name, description, parentId, coverImage, order` |
| **Tag** | `id, slug, name, usageCount` |
| **Author** | `id, name, slug, bio, avatar, socialLinks[]` |
| **Media** | `id, url, alt, width, height, credits` |
| **Page** | `id, slug, title, body, type` (legal / about / faq) |

### 13.2 Relasi

```
Category 1 ──< Article >── 1 Author
    │                        │
    └──< Article >──< Tag    └──< Article >──< Article (related)
```

### 13.3 Aturan Data

| ID | Aturan |
|---|---|
| D-01 | `slug` unik dan immutable setelah terbit |
| D-02 | `status ∈ {draft, review, scheduled, published, archived}` |
| D-03 | `publishedAt ≤ now()` bila `status = published` |
| D-04 | Setiap artikel punya tepat 1 kategori utama |
| D-05 | Halaman legal memerlukan `updatedAt` |

---

## 14. SEO Requirements

| ID | Kebutuhan | Status live |
|---|---|---|
| S-01 | `<title>` unik per halaman, ≤ 60 karakter | Ada |
| S-02 | Meta description 140–160 karakter | Ada (beranda) |
| S-03 | Canonical self-referencing | Ada (beranda) |
| S-04 | JSON-LD `Article`, `BreadcrumbList`, `WebSite`, `Person` | ❌ **tidak ada** |
| S-05 | `sitemap.xml` yang ter-update otomatis | ❌ perlu verifikasi |
| S-06 | `robots.txt` wajar | ❌ perlu verifikasi |
| S-07 | Open Graph + Twitter Card | ❌ perlu verifikasi |
| S-08 | Struktur heading hierarkis (satu H1/halaman) | Ada |
| S-09 | Internal linking antar artikel | Ada |
| S-10 | Gambar punya alt | Ada |
| S-11 | Skema `https://` | ❌ **saat ini `http://`** |
| S-12 | `hreflang` bila ada multi-bahasa | N/A (fase 2) |

---

## 15. Non-Functional Summary

Rincian ada di [QRD](Quality%20Requirements%20Document%20(QRD).md).

| Kategori | Target utama |
|---|---|
| Performa | LCP < 2,5 s, INP < 200 ms, CLS < 0,1 |
| Keandalan | 99,9% uptime |
| Keamanan | HTTPS, headers keamanan, backup harian |
| Aksesibilitas | WCAG 2.1 AA |
| Responsif | 320 – 2560 px |
| Kompatibilitas | 2 versi terakhir browser utama |

---

## 16. Analytics & Success Metrics

| ID | Metrik | Tool | Target |
|---|---|---|---|
| A-01 | Organic sessions | GA4 | +300% |
| A-02 | Search CTR | Search Console | ≥ 3% |
| A-03 | Pages/session | GA4 | ≥ 1,8 |
| A-04 | Returning users | GA4 | ≥ 25% |
| A-05 | Index rate | Search Console | ≥ 85% |
| A-06 | Revenue/session | GA4 + ad dash | ≥ Rp 1.500 |
| A-07 | LCP | CrUX / RUM | < 2,5 s |
| A-08 | Newsletter signups | Form tracking | ≥ 500/bulan |

**Alat terverifikasi saat ini:** Histats + Cloudflare Insights. **Rekomendasi:** GA4 + Search Console sebagai standar ([TRD §7](Technical%20Requirements%20Document%20(TRD).md)).

---

## 17. Risks & Mitigations

| # | Risiko | Dampak | Mitigasi | Trace |
|---|---|---|---|---|
| PR-01 | Tema baru menurunkan UX di luar yang diharapkan | Tinggi | Pengujian A/B sebelum penuh | UIRD |
| PR-02 | Migrasi merusak SEO | Tinggi | Peta URL + redirect 301 + validasi | FRD-10 |
| PR-03 | Volume konten turun kualitas | Tinggi | Standar editorial & review | CE-01…08 |
| PR-04 | Core Web Vitals turun | Sedang | Budget performa di CI | QRD |
| PR-05 | Placeholder label terbawa ke produksi | Sedang | Konfirmasi sebelum coding | UIRD-03 |
| PR-06 | Bahasa campuran | Sedang | Copy guide | §6 |
| PR-07 | Ketergantungan pada satu penulis | Sedang | Rekrutmen kontributor | BRD |
| PR-08 | Iklan merusak UX | Sedang | Density control | BRD §5 |

---

## 18. Release Plan & Acceptance

### 18.1 Tahapan Rilis

| Tahap | Cakupan | Kriteria |
|---|---|---|
| **R0 — Fondasi** | HTTPS, analytics, schema, sitemap | Tidak ada regresi traffic |
| **R1 — Tema** | Migrasi tema ivory/terracotta | UAT visual lolos [UIRD §9](User%20Interface%20Requirements%20Document%20(UIRD).md#9-checklist-kepatuhan-100-tema) |
| **R2 — Arsip** | Category archive + chip filter | UAT fungsional lolos |
| **R3 — Discovery** | Pencarian, related, trending | NFR hijau |
| **R4 — Monetisasi** | Slot iklan, label sponsored | Density control aktif |
| **R5 — Polish** | Newsletter, tag, penulis | — |

### 18.2 Acceptance Criteria (Produk)

Produk dianggap **diterima** jika:

1. ✅ Seluruh fitur F-01…F-10 (Fase 1) berfungsi sesuai [FRD](Functional%20Requirements%20Document%20(FRD).md).
2. ✅ Seluruh NFR di [QRD §2](Quality%20Requirements%20Document%20(QRD).md) terpenuhi.
3. ✅ UI lolos checklist 100% tema di [UIRD §9](User%20Interface%20Requirements%20Document%20(UIRD).md#9-checklist-kepatuhan-100-tema).
4. ✅ Tidak ada regresi SEO: URL lama tetap 200, sitemap lengkap, schema valid.
5. ✅ Tidak ada broken link (> 0,5%).
6. ✅ WCAG 2.1 AA terverifikasi.
7. ✅ Analytics terverifikasi setelah 7 hari rilis.

### 18.3 Out of Scope Confirmation

Fitur berikut **tidak** termasuk dalam rilis ini dan dicatat sebagai backlog: booking, aplikasi native, video original, forum, komentar, mode gelap, bahasa Inggris.

---

## Lampiran A — Ringkasan Keputusan Pending

| ID | Keputusan | Dampak | Status |
|---|---|---|---|
| PD-01 | Nama logo: `balikisah.com` atau `Bali Kisah`? | Tinggi | **DIKONFIRMASI 5 Okt 2026** — `balikisah.com` untuk seluruh identitas situs |
| PD-02 | CTA: `Contact us` atau `Hubungi Kami`? | Sedang | **DIKONFIRMASI 5 Okt 2026** — `Hubungi Kami` (tetap ada di header; label nav `Kontak` tidak lagi dipakai sejak PD-09) |
| PD-03 | Label nav `Stonian`, chip `Soratirin`/`listowa` — placeholder? | — | **DIKONFIRMASI 5 Okt 2026** — dipakai apa adanya, bukan placeholder |
| PD-04 | Migrasi tema live: ya atau tidak? | Sangat tinggi | Menunggu |
| PD-05 | Target monetisasi awal | Sedang | Menunggu |
| PD-06 | Timeline rilis | Tinggi | Menunggu |
| PD-07 | Sumber foto artikel: tautan, berkas lokal, atau unggah ke Google Drive? | Sedang | **DITAMBAHKAN 5 Okt 2026** — ketiganya didukung; unggah Drive butuh OAuth Client ID milik pengelola |
| PD-08 | Label nav `Kerajaan` (pada referensi terbaca `Kenajaan`) | Rendah | **DIKONFIRMASI 5 Okt 2026** — dikoreksi atas permintaan pengguna |
| PD-09 | Menu utama masih memakai label referensi (`Kategori`, `Kerajaan`, `Stonian`, `Blog`, `Kontak`) | Tinggi | **DIKONFIRMASI 7 Okt 2026** — menu disamakan dengan balikisah.com: 8 tautan tanpa chevron; enam label kategori memakai target internal `kategori:<Nama>` |
| PD-09 | Warna footer: gelap atau terang? | Sedang | **DIKONFIRMASI 5 Okt 2026** — varian **terang** (ivory + hairline `--hairline`), sesuai karakter kertas UIRD |
| PD-10 | Halaman kanonik/default tema | Sedang | **DIKONFIRMASI 5 Okt 2026** — **Beranda**; arsip kategori tetap tersedia dan tetap menjadi halaman acuan pengukuran |