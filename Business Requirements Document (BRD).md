# Business Requirements Document (BRD)

> **Project:** BaliKisah.com
> **Status:** Baseline v1.0
> **Tanggal:** 5 Oktober 2026
> **Dokumen terkait:** [MRD](Market%20Requirements%20Document%20(MRD).md) · [CRD](Customer%20Requirements%20Document%20(CRD).md) · [PRD](Product%20Requirements%20Document%20(PRD)%2018%20Section.md) · [UIRD](User%20Interface%20Requirements%20Document%20(UIRD).md) · [FRD](Functional%20Requirements%20Document%20(FRD).md) · [TRD](Technical%20Requirements%20Document%20(TRD).md) · [QRD](Quality%20Requirements%20Document%20(QRD).md) · [SRS](Software%20Requirements%20Specification%20(SRS).md)

---

## 1. Tujuan Bisnis

Membangun dan mengelola BaliKisah.com sebagai **properti media digital** dengan:

1. Audiens organik yang berkelanjutan.
2. Otoritas tematik pada topik Bali dan Nusantara.
3. Jalur monetisasi yang sehat tanpa mengorbankan kualitas baca.
4. Aset konten yang semakin bernilai seiring waktu.

---

## 2. Tujuan & Inisiatif Bisnis

| ID | Tujuan | Inisiatif | Prioritas |
|---|---|---|---|
| BN-01 | Meningkatkan visibilitas organik | SEO teknis, schema, internal linking | P0 |
| BN-02 | Meningkatkan konsumsi multi-artikel | Related articles, read more, trending | P0 |
| BN-03 | Memperkuat positioning merek | Identitas visual editorial yang konsisten | P1 |
| BN-04 | Membangun library konten evergreen | Kalender editorial berbasis pilar | P0 |
| BN-05 | Menyiapkan inventaris monetisasi | Struktur slot iklan tanpa mengorbankan UX | P1 |
| BN-06 | Membangun audiens milik sendiri | Newsletter | P2 |

---

## 3. Scope

### 3.1 In Scope

- Website editorial publik: beranda, arsip kategori, artikel, statis.
- Taksonomi: kategori, tag, artikel terkait.
- SEO: on-page, teknis, structured data.
- Analitik: GA4, Search Console, pelacakan basics.
- Manajemen konten: alur kerja editorial, penjadwalan.
- Monetisasi: iklan display (fase awal).
- **[REVISI — perlu persetujuan]** Migrasi tema ke identitas editorial ivory dan terracotta sesuai [UIRD](User%20Interface%20Requirements%20Document%20(UIRD).md).

### 3.2 Out of Scope (fase awal)

- Marketplace atau booking engine.
- Transaksi hotel, tiket, atau paket.
- Ulasan marketplace buatan pengguna (UGC rating).
- Forum komunitas atau feed sosial native.
- Aplikasi native (mobile app).
- Video original (fase berikutnya).

---

## 4. Business Rules

| ID | Aturan | Alasan |
|---|---|---|
| BR-01 | Setiap artikel wajib memiliki satu kategori utama | Taksonomi & navigasi |
| BR-02 | Setiap artikel wajib memiliki judul, slug, ringkasan, gambar utama, penulis, tanggal terbit, dan isi | Kualitas & SEO |
| BR-03 | Artikel budaya dan sejarah wajib lolos pemeriksaan faktual | Kredibilitas |
| BR-04 | URL artikel stabil setelah terbit; perubahan slug wajib redirect 301 | SEO |
| BR-05 | Dilarang memuat konten berhak cipta tanpa izin | Legal |
| BR-06 | Dilarang memuat klaim budaya tanpa sumber atau konteks | Reputasi |
| BR-07 | Konten berbahasa Inggris harus ditandai jelas bila ada | Kejelasan |
| BR-08 | Artikel harus ditinjau sebelum terbit | Mutu |
| BR-09 | Slug harus lowercase, mengandung tanda hubung, maksimal 75 karakter | SEO & URL cleanliness |

---

## 5. Model Pendapatan

| Fase | Sumber | Kapan | Catatan |
|---|---|---|---|
| **1** | Iklan display | Bulan 0–6 | Slot 728×90, 300×250, 336×280 |
| **2** | Afiliasi | Bulan 6–12 | Booking/paket; tracking wajib |
| **3** | Konten bersponsor | Bulan 9–15 | Label "Sponsored" wajib terlihat |
| **4** | Kemitraan pariwisata | Bulan 12+ | Kerja sama dengan hotel/DMC |
| **5** | Produk digital | Bulan 12+ | Panduan premium |

**Prinsip:** Tidak ada slot iklan di atas lipatan (above-the-fold) pada viewport < 1024 px ([UIRD §11](User%20Interface%20Requirements%20Document%20(UIRD).md)).

---

## 6. KPI Framework

| Area | KPI | Definisi | Target |
|---|---|---|---|
| **Akuisisi** | Organic sessions | Sesi dari mesin pencari | +300% YoY |
| **Akuisisi** | Impressions | Tayangan di Search Console | +250% YoY |
| **Akuisisi** | Search CTR | Klik ÷ impressions | ≥ 3% |
| **Keterlibatan** | Pages/session | Halaman ÷ sesi | ≥ 1,8 |
| **Keterlibatan** | Engaged session | Sesi > 60s atau > 50% gulir | ≥ 65% |
| **Retensi** | Returning users | Pengguna kembali 30 hari | ≥ 25% |
| **Konten** | Artikel terbit | Jumlah publikasi | ≥ 300/tahun |
| **Konten** | Index rate | Halaman terindeks ÷ terbit | ≥ 85% |
| **Monetisasi** | RPM | Pendapatan ÷ 1000 tayangan | ≥ Rp 5.000 |
| **Monetisasi** | Revenue/session | Pendapatan ÷ sesi | ≥ Rp 1.500 |
| **Kualitas** | Koreksi editorial | Artikel yang dikoreksi ÷ terbit | ≤ 1% |
| **Kualitas** | Broken links | Tautan rusak ÷ total | ≤ 0,5% |

---

## 7. Proyeksi Pendapatan

*[ASUMSI]* — angka berikut memerlukan konfirmasi model bisnis sebelum dipakai sebagai target.

| Skenario | Sesi/bulan (Bulan 12) | Revenue/sesi | Revenue/bulan |
|---|---|---|---|
| **Konservatif** | 150.000 | Rp 500 | Rp 75 juta |
| **Moderat** | 500.000 | Rp 1.500 | Rp 750 juta |
| **Agresif** | 2.000.000 | Rp 2.000 | Rp 4 miliar |

---

## 8. Struktur Tim & Governance

| Peran | Tanggung jawab |
|---|---|
| **Pemilik Produk** | Menetapkan tujuan, prioritas, anggaran |
| **Editor** | Standar konten, peninjauan, kalender editorial |
| **SEO/Content Strategist** | Taksonomi, keyword, pertumbuhan pencarian |
| **Engineering** | Keandalan, performa, keamanan, rilis |
| **Kontributor/Freelance** | Menulis artikel sesuai brief dan standar |

**Alur keputusan:**
- Kekontenannya → Editor
- Prioritas fitur → Pemilik Produk
- Kebutuhan teknis → Engineering
- Perubahan desain → consult UIRD, persetujuan Pemilik Produk

---

## 9. Roadmap Bisnis

| Kuartal | Fokus |
|---|---|
| **Q4 2026** | Stabilisasi, schema, perbaikan UX mobile |
| **Q1 2027** | Migrasi tema, redesign arsip kategori |
| **Q2 2027** | Newsletter, perbaikan internal linking |
| **Q3 2027** | Monetisasi afiliasi |
| **Q4 2027** | Ekspansi bahasa Inggris (uji coba) |

---

## 10. Risiko Bisnis

| # | Risiko | Dampak | Mitigasi |
|---|---|---|---|
| RB-01 | Ketergantungan pada satu sumber traffic (search) | Tinggi | Newsletter, kanal lain |
| RB-02 | Kualitas konten menurun saat volume naik | Tinggi | Standar editorial & review |
| RB-03 | Iklan menurunkan retensi | Sedang | Density control |
| RB-04 | Perubahan algoritma search | Tinggi | Diversifikasi & kualitas |
| RB-05 | Ketergantungan pada satu penulis membatasi kredibilitas | Sedang | Tambah kontributor |
| RB-06 | Klaim budaya keliru merusak reputasi | Tinggi | Review fakta & penafian |

---

## 11. Asumsi & Keputusan Menunggu

| # | Asumsi | Impact | Status |
|---|---|---|---|
| A-BR-01 | Monetisasi utama = iklan display | Sedang | **[ASUMSI]** |
| A-BR-02 | Tidak ada patokan modal yang ditentukan | Tinggi | **[ASUMSI]** |
| A-BR-03 | Tim kecil (1–3 orang) | Sedang | **[ASUMSI]** |
| A-BR-04 | Migrasi ke tema baru disetujui | Tinggi | **Menunggu** |
| A-BR-05 | Bahasa Inggris bukan prioritas 12 bulan | Sedang | Plan |

---

## 12. Business Acceptance Criteria

Sistem dianggap layak secara bisnis jika:

- ✅ Mampu menerbitkan konten secara terstruktur (kategori, tag, penulis, tanggal).
- ✅ Menyediakan mekanisme discovery yang kuat (kategori, related, trending).
- ✅ Analytics terpasang dan terverifikasi (GA4 + Search Console).
- ✅ SEO dasar terpenuhi (schema, canonical, meta, sitemap).
- ✅ Tidak ada pemuatan lambat yang mengganggu (Core Web Vitals hijau).
- ✅ Struktur monetisasi siap diaktifkan.