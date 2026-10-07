# Customer Requirements Document (CRD)

> **Project:** BaliKisah.com
> **Status:** Baseline v1.0
> **Tanggal:** 5 Oktober 2026
> **Basis:** Observasi langsung situs live + pain point pasar (lihat [MRD §2](Market%20Requirements%20Document%20(MRD).md))
> **Dokumen terkait:** [MRD](Market%20Requirements%20Document%20(MRD).md) · [BRD](Business%20Requirements%20Document%20(BRD).md) · [PRD](Product%20Requirements%20Document%20(PRD)%2018%20Section.md) · [UIRD](User%20Interface%20Requirements%20Document%20(UIRD).md) · [FRD](Functional%20Requirements%20Document%20(FRD).md) · [QRD](Quality%20Requirements%20Document%20(QRD).md)

---

## 1. Ringkasan Pelanggan

Pelanggan BaliKisah.com adalah pembaca digital yang:

- Mencari **informasi tepercaya** tentang Bali dan Nusantara.
- Datang terutama dari **pencarian organik** (Google, Discover).
- Membaca di **ponsel** lebih sering daripada desktop.
- Mencari jawaban cepat **dan** kadang membaca panjang.
- Mudah **terganggu** — mudah teralihkan oleh media sosial.

Implikasi utama: **produk harus berfungsi baik dalam 3 detik pertama**, dan konten harus dapat dipindai sebelum dibaca.

---

## 2. Kebutuhan Pelanggan (CRQ)

| ID | Kebutuhan Pelanggan | Prioritas | Terpetakan ke |
|---|---|---|---|
| **CRQ-01** | Menemukan artikel yang relevan dalam beberapa detik | P0 | Pencarian internal, filter kategori |
| **CRQ-02** | Membaca comfortable di layar kecil | P0 | Responsive, tipografi, target sentuh |
| **CRQ-03** | Merasakan kontennya kredibel dan tidak mengada-ada | P1 | Atribusi sumber, nama penulis, tanggal |
| **CRQ-04** | Melanjutkan bacaan ke artikel terkait | P1 | Related articles, trending |
| **CRQ-05** | Menyimpan atau dibagikan artikel | P2 | Share buttons, permalink |
| **CRQ-06** | Mendapatkan pembaruan tentang topik favorit | P2 | Newsletter, kategori follow |
| **CRQ-07** | Tidak diganggu iklan yang berlebihan | P1 | Kepadatan iklan terkendali |
| **CRQ-08** | Berpindah antara bahasa Indonesia dan Inggris | P3 | Language switcher |

---

## 3. Persona

### P1 —arkdownita, 28, tourist planner *(primer)*

| Aspek | Detail |
|---|---|
| **Konteks** | Karyawan Bandung, merencanakan liburan 4 hari di Bali bulan depan |
| **Kebutuhan** | Itinerary siap pakai, tempat yang benar-benar Baton, harga masuk yang masuk akal |
| **Frustrasi** | Blog lama recommending tempat yang sudah tutup; tidak tahu mana yang ramah keluarga |
| **Sukses berarti** | Punya rencana lengkap dalam 30 menit |
| **Perilaku** | Mencari di Google → klik 3 hasil → baca 2 → booking |

### P2 — Rangga, 35, history & culture enthusiast *(sekunder)*

| Aspek | Detail |
|---|---|
| **Konteks** | Dosen sejarah lokal, ingin memahami babad dan silsilah |
| **Kebutuhan** | Kedalaman sumber, kronologi jelas, referensi |
| **Frustrasi** | Artikel pendek tanpa sumber, klaimHQ yang tidak jelas |
| **Sukses berarti** | Menemukan sumber yang bisa ia rujuk di kelas |
| **Perilaku** | Baca panjang, bookmark, bagikan ke grup riset |

### P3 — Sarah, 41, expatriate / family visitor *(sekunder)*

| Aspek | Detail |
|---|---|
| **Konteks** | Tinggal di Bali, membawa anak dan mencari aktivitas aman serta edukatif |
| **Kebutuhan** | Konten ramah anak, opsi halal, halal info |
| **Frustrasi** | Konten tidak sesuai kondisi lapangan terbaru |
| **Sukses berarti** | Menemukan aktivitas yang benar-benar berjalan |
| **Perilaku** | Baca cepat, cek tanggal pembaruan |

### P4 — Dita, 21, student *(tersier)*

| Aspek | Detail |
|---|---|
| **Konteks** | Mahasiswa, tugas eskursi / makalah |
| **Kebutuhan** | Ringkasan, definisi, daftar |
| **Frustrasi** | Teks terlalu panjang, jargon tanpa konteks |
| **Sukses berarti** | Info ringkas untuk tugas |
| **Perilaku** | Copy-paste, simpan PDF |

---

## 4. Pain Points & Kebutuhan Emosional

| # | Pain point | Kebutuhan emosional | Solusi produk |
|---|---|---|---|
| PP-1 | "Informasi ini benar atau karangan?" | **Kepercayaan** | Atribusi sumber, nama penulis, tanggal |
| PP-2 | "Sudah basi, kapok." | **Kepastian** | Tanggal pembaruan, catatan review |
| PP-3 | "Bahasanya berantakan." | **Kemudahan** | Bahasa Indonesia konsisten |
| PP-4 | "Loading lama di HP." | **Kelancaran** | Core Web Vitals, lazy loading |
| PP-5 | "Iklan mana-mana." | **Ketenangan** | Batas kepadatan iklan |
| PP-6 | "Nggak ada next article-nya." | **Keter Continuance** | Related articles, read more |

---

## 5. Customer Journey

```
 awareness         discovery           consumption          retention
 ─────────         ──────────          ─────────────        ──────────
 Google            Beranda /          Artikel /             Newsletter,
 Discover          Pencarian          Kategori              Bookmark,
 Social            internal           (mobile)              Share

 Pain: "Banyak    Pain: "Mana yang   Pain: "Susah cari    Pain: "Kadang
 artikel, mana    relevan?"          info penting"       _delete_
 yang beda?"                           "Iklan ganggu"
       ↓                 ↓                  ↓                  ↓
 Need: Otoritas   Need: Filter &    Need: Struktur &     Need: Update
 & editorial      pencarian cepat    mobile-first         & kanal sendiri
```

---

## 6. Use Cases

| ID | Use case | Pelanggan | Alur |
|---|---|---|---|
| UC-01 | Mencari itinerary | P1 | Search → artikel → share |
| UC-02 | Jelajah kategori sejarah | P2 | Kategori → chip filter → artikel |
| UC-03 | Baca artikel panjang | P2 | Artikel → related → artikel 2 |
| UC-04 | Cari kuliner halal | P3 | Kategori Kuliner → filter → artikel |
| UC-05 | Riset tugas | P4 | Search → ringkasan → save |
| UC-06 | Kembalivia bookmark | P1 | Bookmark → artikel (tidak berubah) |

---

## 7. Customer Constraints & Preferensi

| Constraint | Dampak produk |
|---|---|
| Mayoritas trafik dari mobile | Prioritaskan mobile-first |
| Bahasa Indonesia | Copy dan UI dalam bahasa Indonesia |
| Koneksi tidak stabil di beberapa daerah | Core Web Vitals penting; gunakan lazy loading |
| Preferensi privasi | Jangan paksa login; opsional |
| Ads dianggap mengganggu | Density kontrol |

---

## 8. Willingness & Pain Prioritization

| Prioritas | Pain | Alasan |
|---|---|---|
| **Tertinggi** | Kredibilitas (PP-1) | Mendasari seluruh model konten |
| **Tinggi** | Kecepatan + mobile (PP-4) | Retensi langsung |
| **Tinggi** | Struktur navigasi (PP-6) | Meninggalkan situs bila konten tidak berlanjut |
| **Sedang** | Bahasa (PP-3) | Persepsi profesionalitas |
| **Sedang** | Iklan (PP-5) | Toleransi rendah |
| **Rendah** | Share (PP-2) | Nice-to-have |

---

## 9. Success Metrics dari Sisi Pelanggan

| Metrik | Definisi | Target |
|---|---|---|
| Task success rate | % sesi yang mencapai tujuan (artikel dibaca ≥ 75%) | ≥ 40% |
| Search success | % pencarian yang menghasilkan klik | ≥ 60% |
| Return rate | % pengguna kembali dalam 30 hari | ≥ 25% |
| Complaint rate | Keluhan (tidak ada formulir, tapi sinyal negatif) | Minimal |
| NPS | Nilai kepuasan | ≥ 40 |

---

## 10. Voice & Language Requirements

| Aspek | Aturan |
|---|---|
| Bahasa | Bahasa Indonesia baku; istilah Inggris hanya jika umum |
| Nadanya | Hangat, edukatif, tidak menggurui |
| Hindari | Bahasa **Inggris yang tidak diterjemahkan** — live saat ini masih memuat `Hottest Articles`, `Read More`, `Contact us`; **keputusan 5 Okt 2026:** situs ini memakai CTA `Hubungi Kami`. **Diperbarui 7 Okt 2026:** nav `Kontak` tidak lagi dipakai karena menu disamakan dengan balikisah.com menjadi 8 tautan (`Home`, `Budaya`, `Tradisi`, `Kuliner`, `Sejarah`, `Wisata`, `Tips Traveling`, `Tentang Kami`) — lihat [UIRD §16](User%20Interface%20Requirements%20Document%20(UIRD).md) UIRD-06 |
| Kalimat | Pendek, aktif, tanpa jargon tanpa konteks |

---

## 11. Asumsi yang Perlu Dikonfirmasi

| # | Asumsi | Cara validasi |
|---|---|---|
| A-01 | Mayoritas trafik dari mobile | Google Analytics |
| A-02 | Pembaca vieram dari organic search | Analytics + Search Console |
| A-03 | Bahasa Inggris adalah kebutuhan nyata | Survei singkat |
| A-04 | Kebiasaan membaca ulang menjadi driver retensi | Analytics |

---

## 12. Definition of Customer Success

Pelanggan dianggap sukses jika:

- ✅ Menemukan artikel relevan ≤ 10 detik sejak landing.
- ✅ Membaca ≥ 75% dari satu artikel tanpa?_interrupt_ iklan di dalam.
- ✅ Klik minimal satu artikel terkait sebelum keluar.
- ✅ Merekam artikel untuk dibaca ulang.