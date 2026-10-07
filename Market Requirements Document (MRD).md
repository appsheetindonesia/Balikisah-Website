# Market Requirements Document (MRD)

> **Project:** BaliKisah.com
> **Domain:** `balikisah.com`
> **Status:** Baseline v1.0 — disusun berdasarkan observasi langsung situs live (5 Oktober 2026, UTC+7)
> **Bahasa produk:** Bahasa Indonesia (utama), Inggris (sekunder)
> **Dokumen terkait:** [CRD](Customer%20Requirements%20Document%20(CRD).md) · [BRD](Business%20Requirements%20Document%20(BRD).md) · [PRD](Product%20Requirements%20Document%20(PRD)%2018%20Section.md) · [UIRD](User%20Interface%20Requirements%20Document%20(UIRD).md) · [FRD](Functional%20Requirements%20Document%20(FRD).md) · [TRD](Technical%20Requirements%20Document%20(TRD).md) · [QRD](Quality%20Requirements%20Document%20(QRD).md) · [SRS](Software%20Requirements%20Specification%20(SRS).md)

---

## 0. Dasar Dokumen & Status Bukti

Seluruh klaim tentang kondisi BaliKisah.com di bawah **diverifikasi langsung** pada `http://balikisah.com/` melalui inspeksi DOM, computed style, dan tangkapan layar. Klaim yang belum terverifikasi ditandai **[ASUMSI]**.

**Fakta terverifikasi dari situs live:**

| Aspek | Nilai terverifikasi |
|---|---|
| Title | `Bali Kisah` |
| Meta description | "BaliKisah.com menyajikan cerita Bali, budaya, sejarah, wisata, kuliner, dan warisan Indonesia untuk mengenal pesona Nusantara lebih dekat." |
| Atribut `lang` | `ID` |
| Canonical | `http://balikisah.com/` (skema **http**, bukan https) |
| Lebar container | `--main-width: 1100px` |
| Font body | `Julius Sans One`, sans-serif |
| Palet live | Aksen `#2b2b60`, latar `#fdfdfd`, footer `#213758` |
| Penyajian CSS | Tailwind melalui CDN (`cdn.tailwindcss.com`) |
| Analytics | Histats (`histats.com`) + Cloudflare Insights |
| Structured data | **Tidak ada JSON-LD** di beranda |
| Penulis | Tunggal: `Subrata` |
| Format metadata | `04, Oktober, 2026, 16:11:32 — 5 min read` |
| Struktur footer | `Lebih Dekat` · `Eksplor Bali Kisah` · `Topik Populer` |
| Section beranda | Featured hero · Latest grid · `Hottest Articles` (carousel) · `Read More` |
| Kategori terobservasi | Budaya, Tradisi, Kuliner, Sejarah, Wisata, Cerita Lokal, Warisan Budaya |

> **Catatan penting:** Tema pada screenshot referensi ([UIRD](User%20Interface%20Requirements%20Document%20(UIRD).md)) **berbeda total** dari tema live saat ini. UIRD mendefinisikan tema **target**; dokumen ini menilai posisi pasar secara keseluruhan.

---

## 1. Ringkasan Eksekutif

BaliKisah.com adalah media editorial digital berbahasa Indonesia yang mencakup Bali dan Nusantara: **budaya, sejarah, wisata, kuliner, cerita lokal, dan warisan budaya**.

P Empirical yang relevan:

- **Permintaan tinggi dan stabil.** Pencarian "??"SC dan *"travel intent"* berlabel "Bali" di Indonesia merupakan permintaan evergreen yang tidak musim.
- **Konten budaya adalah niche dengan persaingan luas tetapi otoritas tipis.** Banyak situsWITNESS, sedikit yang membangun otoritas tematik.
- **BaliKisah sudah memiliki pijakan yang nyata:** domain aktif, konsistensi publikasi harian, dan arsitektur kategori yang sudah terbentuk.

Peluangnya ada, tetapi **persaingannya ketat**. Diferensiasi yang menentukan bukan jumlah artikel, melainkan **konsistensi editorial, otoritas sumber, dan pengalaman baca**.

---

## 2. Masalah Pasar

| # | Masalah | Dampak |
|---|---|---|
| MP-1 | Informasi Bali tersebar di blog pribadi, OTA, media sosial, dan video pendek yang tidak tervalidasi | Pembaca sulit memisahkan informasi akurat dari mitos |
| MP-2 | Konten budaya sering ditulis dengan klaim spekulatif tanpa atribusi sumber | Kepercayaan pembaca rendah; risiko reputasi |
| MP-3 | Situs beritalungenSuccessfullydestination tidak memiliki struktur arsip yang dapat dijelajahi | Pembaca hanya bisa mendarat satu halaman, tidak bisa membaca beruntun |
| MP-4 | Bahasa campuran (Indonesia dan Inggris) tanpa konsistensi | Terlihat kurang profesional; menyulitkan audiens yang dituju |
| MP-5 | Informasi perjalanan cepat basi (harga, jam buka, akses) | Pembaca yang kembali tidak menemukan informasi valid |

**Tesis pasar:** Pasar tidak kekurangan konten. Pasar kekurangan **konten yang dapat dipercaya, terstruktur, dan Failing diperbarui secara berkala**.

---

## 3. Peluang Pasar

| Peluang | Analisis |
|---|---|
| **Evergreen SEO** | Artikel sejarah dan budaya tidak basi dalam 3–5 tahun. Schema `Article`, `BreadcrumbList`, dan `Person` belum dipakai di situs live — ini peluang cepat bernilai tinggi. |
| **Topical cluster** | Tujuh kategori live dapat diperkuat menjadi struktur pilar dan klaster yang saling mengunci lewat internal linking. |
| **Konsistensi terbit** | Riwayat timestamp menunjukkan 1–2 artikel per hari (28 Sept – 4 Okt 2026). Ini aset bila taksonominya dikelola. |
| **Monetisasi berlapis** | Iklan display → afiliasi → konten bersponsor → kemitraan pariwisata → produk digital. |
| **Kepercayaan** | Klaim budaya yang diberi sumber eksplisit menjadi pembeda yang murah dan sulit ditiru. |

---

## 4. Segmen Target

| Segmen | Kebutuhan | Konten prioritas | Ukuran relatif |
|---|---|---|---|
| **Wisatawan domestik** | Inspirasi dan perencanaan cepat | Wisata, itinerary, kuliner, hidden gem | ★★★★★ |
| **Pembaca berbasis pencarian** | Jawaban langsung | FAQ, listicle, how-to, glosarium | ★★★★★ |
| **Penikmat budaya** | Kedalaman dan konteks | Tradisi, sejarah, filosofi, seni | ★★★★☆ |
| **Mahasiswa/pelajar** | Referensi ringkas | Sejarah, tokoh, peninggalan | ★★★☆☆ |
| **Wisatawan mancanegara** | Konteks dan panduan praktis | Culture, history, practical guides | ★★★☆☆ |
| **Pembaca cerita** | Narasi yang menarik | Cerita lokal, legenda, profil tokoh | ★★★☆☆ |

Profil persona lengkap ada di [CRD §3](Customer%20Requirements%20Document%20(CRD).md).

---

## 5. Lanskap Kompetitif

| Arketipe kompetitor | Kekuatan | Peluang untuk BaliKisah |
|---|---|---|
| OTA (Traveloka, Tiket, Agoda) | Jaringan dan otoritas domain | Konten dangkal,commercial, minim konteks budaya |
| Travel blog besar | Volume dan backlink | Kualitas tidak konsisten, cenderung clickbait |
| Media nasional | Otoritas redaksional | Fokus nasional, porsi Bali terbatas |
| Platform UGC (TripAdvisor, Google) | Ulasan langsung dari pengguna | Konteks budaya dangkal |
| Video pendek (TikTok, YouTube) | Jangkauan sangat luas | Tidak dalam, sulit dijadikan rujukan |
| Content farm generik | Volume sangat tinggi | Kepercayaan rendah, mudah terdeteksi |

**Keunggulan kompetitif yang harus dibangun:**

1. **Disiplin editorial** — setiap klaim faktual memiliki sumber.
2. **Arsip yang dalam** — kategori → subkategori → artikel → artikel terkait.
3. **Identitas visual yang kuat** — tema editorial hangat yang berbeda dari kebanyakan situs pariwisata.

---

## 6. Positioning

**Pernyataan positioning:**

> *BaliKisah.com adalah media digital yang mempertemukan pembaca dengan cerita, budaya, sejarah, wisata, kuliner, dan kehidupan Bali serta Nusantara — lewat konten yang tepercaya, terstruktur, dan layak disimpan.*

**Wilayah merek:** `hangat` · `editorial` · `tepercaya` · `budaya` · `ramah`

**Anti-positioning:** bukan OTA, bukan portal berita, bukan blog pemburu backlink, bukan pabrik konten AI.

---

## 7. Kebutuhan Pasar (MRQ)

| ID | Kebutuhan Pasar | Prioritas | Sumber |
|---|---|---|---|
| **MRQ-01** | Cakupan kategori yang lengkap dan seimbang: budaya, sejarah, wisata, kuliner, cerita lokal, warisan budaya | P0 | [PRD §5](Product%20Requirements%20Document%20(PRD)%2018%20Section.md) |
| **MRQ-02** | Arsip yang dapat dijelajahi: kategori → tag → artikel terkait | P0 | [PRD §7](Product%20Requirements%20Document%20(PRD)%2018%20Section.md) |
| **MRQ-03** | Konsistensi bahasa Indonesia di seluruh antarmuka dan konten | P0 | [PRD §6](Product%20Requirements%20Document%20(PRD)%2018%20Section.md) |
| **MRQ-04** | Kredibilitas sumber: atribusi dan klarifikasi ketidakpastian | P1 | [PRD §11](Product%20Requirements%20Document%20(PRD)%2018%20Section.md) |
| **MRQ-05** | Temukan cepat: pencarian internal, artikel terkait, topik populer | P1 | [FRD](Functional%20Requirements%20Document%20(FRD).md) |
| **MRQ-06** | Pembacaan nyaman di perangkat kecil (mobile-first) | P0 | [QRD §3](Quality%20Requirements%20Document%20(QRD).md) |
| **MRQ-07** | Monetisasi tanpa merusak pengalaman baca | P2 | [BRD §5](Business%20Requirements%20Document%20(BRD).md) |
| **MRQ-08** | Identitas visual editorial yang khas dan konsisten | P1 | [UIRD](User%20Interface%20Requirements%20Document%20(UIRD).md) |

---

## 8. Model Pasar & Monetisasi

| Fase | Sumber revenues | Deskripsi |
|---|---|---|
| **Fase 1** | Iklan display | Slot iklan pada beranda dan halaman artikel |
| **Fase 2** | Afiliasi | Booking atau paket wisata dengan pelacakan |
| **Fase 3** | Konten bersponsor | Artikel bersponsor dengan label terlihat jelas |
| **Fase 4** | Kemitraan pariwisata | Kerja sama dengan hotel atau DMC |
| **Fase 5** | Produk digital | Panduan premium, ebook, paket itinerary |

Prinsip yang mengikat: **monetisasi tidak boleh mengorbankan [MRQ-06](#7-kebutuhan-pasar-mrq)**.

---

## 9. Metrik Keberhasilan Pasar

| Kategori | Metrik | Target 12 bulan |
|---|---|---|
| **Jangkauan** | Organic sessions | +300% dibanding baseline |
| **Jangkauan** | Persentase halaman terindeks | ≥ 85% dari total terbit |
| **Penemuan** | Search CTR | ≥ 3% |
| **Keterlibatan** | Halaman per sesi | ≥ 1,8 |
| **Keterlibatan** | Kedalaman gulir > 75% | ≥ 35% sesi |
| **Pengulangan** | Returning users | ≥ 25% |
| **Konten** | Artikel terbit | ≥ 300 |
| **Monetisasi** | Pendapatan per sesi | ≥ Rp 1.500 |
| **Kualitas** | Tingkat koreksi editorial | ≤ 1% artikel |

---

## 10. Risiko Pasar & Mitigasi

| # | Risiko | Dampak | Mitigasi |
|---|---|---|---|
| RK-01 | Konten generik sehingga otoritas rendah | Tinggi | Standar editorial wajib dan tinjauan manusia |
| RK-02 | Klaim budaya tidak terverifikasi | Tinggi | Daftar periksa fakta dan attributable “menurut sumber” |
| RK-03 | Ketergantungan penuh pada organic search | Sedang | Bangun newsletter dan kanal milik sendiri |
| RK-04 | Iklan merusak pengalaman baca | Sedang | Batas kepadatan iklan dan pemuatan lambat |
| RK-05 | Konten saling kanibal (duplikasi topik) | Sedang | Kalender editorial dan pemeriksaan canonical |
| RK-06 | Bahasa campuran Indonesia dan Inggris | Sedang | panduan gaya bahasa tunggal |
| RK-07 | Narasi budaya keliru atau menyinggung | Tinggi | Moderasi dan penafian yang jelas |

---

## 11. Strategi Konten Pasar

### 11.1 Struktur Pilar dan Klaster

```
Pilar: SEJARAH BALI
├─ Kerajaan (Bali, Majapahit, Gelgel)
├─ Tokoh (Mpu Kuturan, Ngurah Rai, ...)
├─ Candi dan Peninggalan
└─ Babad dan Naskah

Pilar: WISATA BALI
├─ Hidden Gem
├─ Itinerary
├─ Family Friendly
└─ Bali Utara (Buleleng, Lovina)

Pilar: KULINER BALI
├─ Halal
├─ Tradisional
├─ Sate Lilit, Babi Guling, Ayam Betutu
└─ Nasi Jinggo

Pilar: BUDAYA DAN TRADISI
├─ Melasti, Nyepi
├─ Naga dan Ukiran
├─ Tri Hita Karana
└─ Warisan UNESCO

Pilar: CERITA LOKAL
└─ Lintas Nusantara (Toraja, Dayak, Papua)
```

### 11.2 Kontribusi tiap Pilar

| Pilar | Kontribusi traffic | Nilai komersial |
|---|---|---|
| Wisata dan Itinerary | 40% | Sedang (iklan, afiliasi) |
| Sejarah dan Babad | 25% | Tinggi (otoritas) |
| Kuliner | 20% | Sedang |
| Budaya dan Tradisi | 10% | Tinggi (merek) |
| Cerita Lokal | 5% | Rendah |

---

## 12. Peluang Ekspansi Pasar

| Arah | Penjelasan | Horizont |
|---|---|---|
| **Bahasa Inggris** | Versi Inggris untuk pasar global | 6 bulan |
| **Newsletter** | Membangun lalu lintas milik sendiri | 3 bulan |
| **Progressive Web App** | PWA lebih dulu, native bila perlu | 12 bulan |
| **Video** | YouTube untuk dokumentasi ceremoni | 9 bulan |
| **Produk digital** | Panduan premium dan merchandise | 12 bulan |
| **API konten** | Lisensi konten ke pihak ketiga | 18 bulan |

---

## 13. Keunggulan Jangka Panjang

1. **Arsip** — semakin panjang, semakin sulit ditiru. Akumulasi konten historis bersifat komulatif.
2. **Otoritas sumber** — rujukan yang diakui media lain.
3. **Identitas visual** — tema yang kuat dan konsisten menghasilkan pengenalan merek.
4. **Arsip data** — catatan perubahan seperti harga dan jadwal yang sudah diverifikasi ulang.

---

## 14. Asumsi & Keputusan yang Menunggu

| # | Asumsi / Keputusan | Dampak | Status |
|---|---|---|---|
| AS-01 | Fokus pasar adalah pembaca Indonesia, bahasa Indonesia | Tinggi | Dikonfirmasi |
| AS-02 | Monetisasi utama: display advertising | Sedang | **[ASUMSI]** perlu konfirmasi |
| AS-03 | Artikel terkait dikurasi secara manual | Sedang | **[ASUMSI]** perlu konfirmasi |
| AS-04 | Migrasi ke tema ivory dan terracotta | Tinggi | Menunggu persetujuan |
| AS-05 | Versi bahasa Inggris akan dibangun | Sedang | Perencanaan |

---

## 15. Definisi Keberhasilan Pasar

Pasar dianggap berhasil jika:

- ✅ Seluruh konten lolos **Standar Editorial** yang ditetapkan.
- ✅ Tujuh pilar kategori terpenuhi dengan masing-masing minimal 15 artikel.
- ✅ Organic traffic tumbuh konsisten selama tiga bulan berturut-turut.
- ✅ Tidak ada kebijakan monetisasi yang menurunkan kualitas pengalaman baca.
- ✅ Konten mulai dianggap layak rujukan oleh media lain (backlink natural).