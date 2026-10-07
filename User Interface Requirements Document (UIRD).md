# User Interface Requirements Document (UIRD)

> **Project:** BaliKisah.com
> **Artefak:** Spesifikasi antarmuka — **Category Archive** (halaman kategori) + komponen global
> **Sumber tema:** Screenshot referensi `WhatsApp Image 2026-10-05 at 09.50.58.jpeg` (756 × 425 px)
> **Status:** Baseline — semua token di bawah **diukur langsung dari piksel gambar referensi**, bukan estimasi
> **Tanggal pengukuran:** 5 Oktober 2026 (UTC+7)
> **Dokumen terkait:** [MRD](Market%20Requirements%20Document%20(MRD).md) · [CRD](Customer%20Requirements%20Document%20(CRD).md) · [BRD](Business%20Requirements%20Document%20(BRD).md) · [PRD](Product%20Requirements%20Document%20(PRD)%2018%20Section.md) · [FRD](Functional%20Requirements%20Document%20(FRD).md) · [TRD](Technical%20Requirements%20Document%20(TRD).md) · [QRD](Quality%20Requirements%20Document%20(QRD).md) · [SRS](Software%20Requirements%20Specification%20(SRS).md)

---

## 0. Metodologi & Skala

Nilai pada dokumen ini menghasilkan dari analisis piksel otomatis (Pillow) terhadap gambar referensi:

| Metrik | Nilai |
|---|---|
| Dimensi gambar referensi | 756 × 425 px (rasio **16:9** persis) |
| Metode sampling warna | Persentil 3% piksel tergelap (anti-aliasing dieliminasi) untuk teks; color-mode modal untuk fill solid |
| Faktor skala ke kanvas desain | **× 1,9048** (756 → **1440**, 425 → **810**) |
| Asumsi viewport asal | Screenshot capture desktop **1440 × 810** yang dikompresi (WhatsApp) menjadi 756 × 425 |

> **Aturan utama:** Kolom **RU** (reference unit) = piksel pada gambar 756 px. Kolom **@1440** = nilai produksi pada kanvas desain 1440 px.
> Implementasi **wajib fluid**, tidak boleh menyalin piksel absolut. RU dipakai untuk menjaga **proporsi**; @1440 dipakai sebagai titik acuan saat viewport ≥ 1280 px.

---

## 1. Design Mandate — Tema Wajib

Tema yang diimplementasikan **wajib 100% identik** dengan screenshot referensi pada level:

1. **Kertas ivory hangat** sebagai latar halaman (`#F7F0DD`) — bukan putih, bukan abu-abu netral.
2. **Header putih murni** yang terpisah tegas dari latar ivory.
3. **Tipografi serif display** (bold, high-contrast) untuk H1 dan judul kartu.
4. **Tipografi sans-serif** untuk navigasi, eyebrow, chip, excerpt, dan tanggal.
5. **Aksen terracotta/copper** sebagai satu-satunya warna interaktif (CTA + chip aktif).
6. **Chip berbentuk pill** dengan keadaan aktif/non-aktif yang jelas berbeda.
7. **Grid kartu 4 kolom** yang rapat, tenang, dan sejajar.
8. **Treatment sepia/archival** pada gambar thumbnails kategori sejarah.
9. **Tanpa** gradient, glassmorphism, neon, warna biru default browser, atau shadow berat.

### 1.1 Structural DNA dari referensi (verified)

Urutan elemen yang **wajib** dipertahankan:

```
┌──────────────────────────────────────────────────────────────┐
│  HEADER  balikisah.com │ Home Budaya Tradisi Kuliner        │
│         Sejarah Wisata Tips Traveling Tentang Kami           │
├──────────────────────────────────────────────────────────────┤ ← divider tipis
│                                                              │
│  Kategori archive                    ← eyebrow sans, muted  │
│  Sejarah dan Babad Bali              ← H1 serif bold        │
│  ─────────────────────────────────────────────────────────── │ ← hairline
│  (Kerajaan Bali)(Candi)(Tokoh Sejarah)(Soratirin)(Kerajaan)  │ ← chips
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐                                 │
│  │ IMG│ │ IMG│ │ IMG│ │ IMG│   ← 4 kolom, sepia             │
│  │────│ │────│ │────│ │────│                                 │
│  │TTL │ │TTL │ │TTL │ │TTL │   ← serif bold                 │
│  │EXC │ │EXC │ │EXC │ │EXC │   ← sans muted                 │
│  │DT  │ │DT  │ │DT  │ │DT  │   ← sans light                 │
│  └────┘ └────┘ └────┘ └────┘                                 │
└──────────────────────────────────────────────────────────────┘
```

Label yang **terverifikasi ada** di referensi:
- Logo: `balikisah.com`
- Nav: `Kategori` (chevron), `Kerajaan`, `Stonian`, `Blog`, `Contact` (chevron)

> **Menu situs diperbarui 7 Okt 2026** — navigasi disamakan dengan
> balikisah.com: `Home`, `Budaya`, `Tradisi`, `Kuliner`, `Sejarah`, `Wisata`,
> `Tips Traveling`, `Tentang Kami` (8 item, **0 chevron**). Baris nav di atas
> dicatat sebagai fakta historis screenshot referensi 5 Okt 2026 dan **tidak
> lagi dipakai** di situs. Lihat [FRD-08.2](Functional%20Requirements%20Document%20(FRD).md)
> dan [SRS-UI-10](Software%20Requirements%20Specification%20(SRS).md).

> **Koreksi 5 Okt 2026** — label nav kedua pada referensi terbaca `Kenajaan`;
> atas permintaan pengguna diganti menjadi **`Kerajaan`** di seluruh dokumen dan
> pada situs. Label lain (`Stonian`, `Soratirin`, `listowa`) tetap apa adanya.
>
> **Logo 5 Okt 2026** — wordmark kini dirender sebagai **teks** (`Playfair Display`
> 700, `clamp(21px,1.5vw + 10px,27px)`, warna `--brand-brown #6F5138`, `.com` 0,68 em)
> alih-alih potongan bitmap 112 × 20 px dari screenshot, karena potongan itu buram
> saat diperbesar ~1,9× ke @1440. Tinggi mengikuti referensi (≈26 px); lebarnya
> ≈151 px, lebih sempit dari ≈200 px pada referensi karena jenis huruf berbeda.
>
> **Bahasa CTA 5 Okt 2026** — atas permintaan pengguna, label diterjemahkan penuh:
> CTA `Contact us` → **`Hubungi Kami`**, item nav `Contact` → **`Kontak`**. Baris
> `CTA: Contact us` di bawah tetap dicatat sebagai fakta label pada referensi.
> *(Item nav `Kontak` digantikan menu 8 item pada 7 Okt 2026 — UIRD-06; CTA
> `Hubungi Kami` tetap ada.)*
>
> **Footer & halaman kanonik 5 Okt 2026** — footer memakai varian **terang**
> (ivory + hairline) dan halaman *default* adalah **Beranda**; lihat UIRD-04/UIRD-05.
- CTA: `Contact us`
- Eyebrow: `Kategori archive`
- H1: `Sejarah dan Babad Bali`
- Chips: `Kerajaan Bali` (aktif), `Candi`, `Tokoh Sejarah`, `Soratirin`, `Kerajaan`, `listowa`

---

## 2. Design Tokens — LOCKED (hasil sampling piksel)

### 2.1 Warna

| Token CSS | Nilai terukur | Hex sumber | Peran |
|---|---|---|---|
| `--ivory` | `#F7F0DD` | modal bg halaman | Latar halaman / archive |
| `--surface` | `#FFFFFF` | modal | Permukaan header & kartu |
| `--ink-900` | `#180E00` | persentil 3% | H1, judul kartu, heading |
| `--ink-700` | `#302923` | persentil 3% | Body bold, judul kartu sekunder |
| `--ink-500` | `#73706A` | persentil 3% | Excerpt, teks metadata |
| `--ink-400` | `#A1A09B` | persentil 3% | Tanggal, teks sekunder |
| `--ink-300` | `#3A3731` | persentil 3% | Tautan navigasi |
| `--brand-brown` | `#6F5138` | persentil 3% | Logo `balikisah.com` |
| `--accent` | `#94542E` | modal | CTA `Hubungi Kami` |
| `--accent-chip` | `#8F5432` | modal | Chip aktif |
| `--accent-hover` | `#7A4526` | turunan −12% L | Hover CTA & chip aktif |
| `--chip-fill` | `#E7D6BC` | modal | Chip non-aktif |
| `--chip-ink` | `#54432C` | persentil 3% | Teks chip non-aktif |
| `--muted` | `#887861` | persentil 3% | Eyebrow `Kategori archive` |
| `--hairline` | `#E5DCC6` | rerata baris y=113 | Garis pemisah |
| `--border-card` | `#EDE7DA` | darkest card | Border kartu |
| `--on-accent` | `#FFFFFF` | — | Teks di atas aksen |

> Toleransi antar-brand: **±3%** per kanal. Di luar itu, dianggap pelanggaran tema.

### 2.2 Tipografi

Pasangan font yang **wajib**:

| Peran | Family | Fallback |
|---|---|---|
| Display / H1 / Judul kartu | `Playfair Display` (700/800) | `Georgia, 'Times New Roman', serif` |
| Logo | `Playfair Display` (500/600) | `Georgia, serif` |
| UI / Body / Nav / Chip | `Inter` (400/500/600) | `-apple-system, 'Segoe UI', Arial, sans-serif` |

> `Playfair Display` dipilih karena karakternya (serif high-contrast dengan bracketed serifs) paling dekat dengan heading di referensi. `--font-display` harus tetap valid bila webfont gagal dimuat.

**Skala tipografi** (diukur dari tinggi glyph; cap-height ratio serif ≈ 0,70 / sans ≈ 0,73):

| Token | Elemen | RU @756 | @1440 | Weight | Line-height | Tracking |
|---|---|---|---|---|---|---|
| `--fs-h1` | H1 kategori | 22 px | **40 px** | 800 | 1,15 | −0,01em |
| `--fs-logo` | `balikisah.com` | 15 px | **28 px** | 600 | 1 | −0,005em |
| `--fs-card-title` | Judul kartu | 11 px | **20 px** | 700 | 1,40 | 0 |
| `--fs-nav` | Navigasi | 7,5 px | **15 px** | 500 | 1 | 0 |
| `--fs-eyebrow` | `Kategori archive` | 7,5 px | **14 px** | 400 | 1,2 | +0,02em |
| `--fs-chip` | Teks chip | 8 px | **15 px** | 500 | 1 | 0 |
| `--fs-excerpt` | Excerpt kartu | 7 px | **14 px** | 400 | 1,55 | 0 |
| `--fs-date` | Tanggal kartu | 6 px | **12 px** | 400 | 1 | +0,01em |

### 2.3 Spacing (base unit 4 px)

| Token | Peran | RU @756 | @1440 |
|---|---|---|---|
| `--sp-container` | Lebar konten | 588 | **1120** |
| `--gutter` | Margin sisi konten | 84 | **160** |
| `--header-h` | Tinggi header | 41 | **78** |
| `--sp-header-to-eyebrow` | Header → eyebrow | 21 | **40** |
| `--sp-eyebrow-to-h1` | Eyebrow → H1 | 9 | **17** |
| `--sp-h1-to-hairline` | H1 → garis | 12 | **23** |
| `--sp-hairline-to-chips` | Garis → chips | 10 | **19** |
| `--sp-chips-to-grid` | Chips → kartu | 14 | **27** |
| `--grid-gap` | Gap kartu (horizontal & vertikal) | 15 | **28** |
| `--card-pad` | Padding dalam kartu | 7,3 | **14** (rekonsiliasi, lihat §3.4) |
| `--card-gap-title` | Gap judul → excerpt | — | **6** |
| `--card-gap-excerpt` | Gap excerpt → tanggal | — | **8** |

### 2.4 Radius & Border

| Token | Nilai | Catatan |
|---|---|---|
| `--radius-card` | **14 px** | Sudut membulat sedang, konsisten ke semua sisi |
| `--radius-image` | **14 px** | Hanya sudut atas; gambar menempel tepi atas kartu |
| `--radius-pill` | **999 px** | CTA dan seluruh chip |
| `--border-card` | **1 px solid `#EDE7DA`** | Tipis, hangat, tanpa shadow |
| `--border-hairline` | **1 px solid `#E5DCC6`** | Garis di bawah H1 |
| `--border-header` | **1 px solid `#E8E2D2`** | Garis bawah header |
| `--shadow-card` | **`0 1px 2px rgba(63,48,32,.05)`** | Sangat halus; praktis tidak terlihat |
| `--shadow-cta` | **`0 2px 6px rgba(148,84,46,.22)`** | Satu-satunya shadow yang diizinkan |

---

## 3. Komponen — Spesifikasi Detail

### 3.1 Header (`SiteHeader`)

**Tata letak terukur (RU @756):**

| Properti | Nilai terukur | @1440 |
|---|---|---|
| Band height | y = 2 → 42 (h = 41) | **78 px** |
| Background | `#FFFFFF` | sama |
| Logo bbox | x = 72 → 167 (w = 95), baseline y ≈ 25 | x start ≈ 137 dari viewport |
| Nav group |justify-content: flex-end`, baseline y ≈ 25 | sama |
| CTA bbox | x = 607 → 671 (w = 64), y = 12 → 32 (h = 20) | **w ≈ 122, h ≈ 38** |

**Aturan:**
- `position: sticky; top: 0; z-index: 100;`
- `height: 78px; display: flex; align-items: center; justify-content: space-between;`
- `padding-inline: clamp(20px, 11vw, 160px); background: var(--surface);`
- `border-bottom: 1px solid var(--border-header);`
- **Tanpa** shadow, gradient, atau backdrop-blur saat sticky.

**Logo (`balikisah.com`)**
- `font-family: var(--font-display); font-weight: 600; font-size: var(--fs-logo);`
- `color: var(--brand-brown);` — **bukan** hitam; perbedaan warna ini wajib terlihat.
- Teks literal `balikisah.com` (bukan "Bali Kisah" — ini yang terverifikasi di referensi).
- `text-decoration: none; line-height: 1;`

**Navigasi Desktop (`DesktopNav`)**
- `display: flex; align-items: center; gap: 32px;`
- `font-family: var(--font-ui); font-size: var(--fs-nav); font-weight: 500; color: var(--ink-300);`
- `gap` terukur antar label ≈ 33 RU → **32 px** pada @1440.
- Item final (**dikonfirmasi 5 Okt 2026**): `Kategori` ⌄ · `Kerajaan` · `Stonian` · `Blog` · `Kontak` ⌄
  (pada referensi item terakhir terbaca `Contact`; atas permintaan pengguna diterjemahkan)
- **Diperbarui 7 Okt 2026 — menu disamakan dengan balikisah.com.** Item final
  menjadi **8 tautan tanpa chevron**, dengan urutan persis seperti live:
  `Home` · `Budaya` · `Tradisi` · `Kuliner` · `Sejarah` · `Wisata` ·
  `Tips Traveling` · `Tentang Kami`.
- **Target tautan:** `Home` → beranda, `Tentang Kami` → halaman tentang, dan
  keenam label kategori → arsip kategori bernama lewat target internal
  `kategori:<Nama>` (hash `#/kategori/<Nama>`).
- **Chevron:** pada menu 7 Okt 2026 **tidak ada** item yang memakai
  chevron/caret (**0 chevron**), persis seperti live. Chevron tetap diizinkan
  hanya untuk menu yang membuka daftar (`kategori`/`tag`/`penulis`/`arsip`/
  `dokumen`/`kontak`).
- Chevron: `▾` inline SVG 10 × 10, `stroke-width: 1.75`, `margin-left: 6px`, warna mengikuti teks.
- `hover`: `color: var(--accent);` (tanpa underline).
- `aria-haspopup="true"` + `aria-expanded` pada item berchevron.

**CTA `Hubungi Kami` (`PrimaryCta`)**
```css
.primary-cta{
  background: var(--accent);        /* #94542E */
  color: #fff;
  border-radius: 999px;
  padding: 10px 24px;
  font: 600 var(--fs-nav)/1 var(--font-ui);
  box-shadow: var(--shadow-cta);
  border: 0; white-space: nowrap;
}
.primary-cta:hover{ background: var(--accent-hover); }
.primary-cta:active{ transform: translateY(1px); }
.primary-cta:focus-visible{ outline: 2px solid var(--accent); outline-offset: 3px; }
```

**Navigasi Mobile (`MobileNav`)**
- Di bawah `≤ 1024px`, navigasi desktop **wajib disembunyikan** dan diganti tombol hamburger (`☰`) di kanan.
- Tombol: `44 × 44 px`, `aria-label="Open menu"`, `aria-expanded`, `aria-controls="mobile-nav"`.
- Panel: `position: fixed; inset: 78px 0 0 0; background: var(--surface);`
- Isi panel (urutan persis): Logo → nav list vertikal → CTA `Hubungi Kami` full-width.
- Buka/tutup: overlay scrim `rgba(36,24,12,.42)`, kunci scroll body saat terbuka, `Esc` menutup.
- State drawer harus diumumkan lewat `aria-expanded` (bukan hanya perubahan visual).

### 3.2 Archive Header (`CategoryArchiveHeader`)

Urutan dan jarak terukur (RU → @1440):

| Elemen | y RU | Tinggi RU | Y @1440 | Padding bawah @1440 |
|---|---|---|---|---|
| Eyebrow `Kategori archive` | 63 → 71 | 8 | 120 → 135 | **17** |
| H1 `Sejarah dan Babad Bali` | 80 → 101 | 22 | 152 → 192 | **23** |
| Hairline divider | 113 → 114 | 1 | 215 | **19** |
| Chip group | 124 → 144 | 20 | 236 → 274 | **27** |

```css
.archive-header{ max-width: var(--sp-container); margin-inline: auto;
  padding: 40px clamp(20px,11vw,160px) 0; }
.archive-eyebrow{ font:400 var(--fs-eyebrow)/1.2 var(--font-ui);
  color: var(--muted); letter-spacing:.02em; margin:0 0 12px; }
.archive-h1{ font:800 var(--fs-h1)/1.15 var(--font-display);
  color: var(--ink-900); letter-spacing:-.01em; margin:0 0 23px; }
.archive-hairline{ border:0; border-top:1px solid var(--hairline); margin:0 0 19px; }
```

- Eyebrow **tidak** uppercase di referensi → **jangan** memaksa `text-transform: uppercase`.
- H1 boleh membungkus 1–2 baris; `text-wrap: balance` diizinkan.

### 3.3 Chip Group (`ChipGroup` + `CategoryChip`)

**Geometri terukur (RU @756):**

| Chip | x_start | x_end | Width RU | Width @1440 |
|---|---|---|---|---|
| `Kerajaan Bali` (aktif) | 82 | 157 | 75 | **143** |
| `Candi` | 162 | 203 | 41 | **78** |
| `Tokoh Sejarah` | 209 | 286 | 77 | **147** |
| `Soratirin` | 292 | 341 | 49 | **93** |
| `Kerajaan` | 348 | 402 | 54 | **103** |
| `listowa` | 409 | 461 | 52 | **99** |

| Properti | RU | @1440 |
|---|---|---|
| Tinggi chip | 20 | **38** |
| Gap antar chip | 6 | **11** |
| Radius | pill | **999 px** |
| Padding horizontal | ≈ 11 | **20 px** |

```css
.chip-group{ display:flex; flex-wrap:wrap; gap:11px; }
.chip{ border-radius:999px; padding:9px 20px; font:500 var(--fs-chip)/1 var(--font-ui);
       border:0; cursor:pointer; white-space:nowrap; }
.chip[aria-pressed="false"]{ background:var(--chip-fill); color:var(--chip-ink); }
.chip[aria-pressed="true"] { background:var(--accent-chip); color:#fff; }
.chip:hover{ filter:brightness(.96); }
.chip:focus-visible{ outline:2px solid var(--accent); outline-offset:2px; }
```

- **Chip aktif ditentukan oleh `aria-pressed="true"`**, bukan kelas CSS saja → state terbaca assistive tech.
- Warna **tidak boleh** menjadi satu-satunya penanda aktif: chip aktif juga dibedakan oleh fill penuh vs. fill pastel.
- Pada `≤ 640px`: `overflow-x: auto; flex-wrap: nowrap; scrollbar-width: none;` dengan fade tepi.

### 3.4 Article Card (`ArticleCard`)

**Geometri terukur (RU @756):**

| Properti | Nilai RU | @1440 |
|---|---|---|
| Lebar kolom | 137 / 136 / 136 / 137 | **259** (4 kolom dalam 1120) |
| X posisi kolom | 83, 234, 384, 534 |Aligned ke container |
| Gap | 15 | **28** |
| Lebar gambar | 137 (full-bleed) | 259 |
| Tinggi gambar | 90 | **171** → `aspect-ratio: 3/2` |
| Tinggi body kartu | 91 | **173** |
| **Tinggi kartu total** | 181 | **345** |
| **Gap judul → excerpt** | — | **6** |
| **Gap excerpt → tanggal** | — | **8** |
| Padding body | 7,3 | **14** |
| Radius | ≈ 7 | **14** |

**Grid:**
```css
.card-grid{ display:grid; gap:28px;
  grid-template-columns:repeat(4, minmax(0,1fr)); }
@media (max-width:1279px){ .card-grid{ grid-template-columns:repeat(3,minmax(0,1fr)); } }
@media (max-width:1023px){ .card-grid{ grid-template-columns:repeat(2,minmax(0,1fr)); } }
@media (max-width:639px) { .card-grid{ grid-template-columns:1fr; gap:20px; } }
```

**Anatomi kartu (urutan wajib):**
1. **Image** — `aspect-ratio: 3/2; object-fit: cover; width:100%;` full-bleed ke tepi atas.
2. **Title** — serif 700, 20 px / 1,40, `color: var(--ink-900)`, clamp **2 baris**.
3. **Excerpt** — sans 400, 14 px / 1,55, `color: var(--ink-500)`, clamp **3 baris**, diakhiri `…`.
4. **Date** — sans 400, 12 px, `color: var(--ink-400)`, format `21 Nov 2023`.

```css
.article-card{ background:var(--surface); border:1px solid var(--border-card);
  border-radius:var(--radius-card); overflow:hidden;
  box-shadow:var(--shadow-card); transition:transform .18s ease, box-shadow .18s ease; }
.article-card:hover{ transform:translateY(-2px);
  box-shadow:0 4px 14px rgba(63,48,32,.10); }
.article-card__title{ font:700 var(--fs-card-title)/1.4 var(--font-display);
  color:var(--ink-900); margin:14px 0 8px;
  display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }
.article-card__excerpt{ font:400 var(--fs-excerpt)/1.55 var(--font-ui);
  color:var(--ink-500); margin:0 0 14px;
  display:-webkit-box; -webkit-line-clamp:3; -webkit-box-orient:vertical; overflow:hidden; }
.article-card__date{ font:400 var(--fs-date)/1 var(--font-ui); color:var(--ink-400); }
```

- Seluruh kartu adalah **satu target klik** (`<a>` yang membungkus image+title). Judul memakai `::after` overlay agar area klik penuh tanpa mengulang `<a>` (pola WCAG 2.5.8).
- Judul **wajib** berupa heading (`h2`/`h3`) agar struktur dokumen benar.

### 3.5 Image Treatment — Sepia Archival

Hasil analisis 8 thumbnail kategori sejarah:

| Metrik terukur | Nilai |
|---|---|
| RGB rata-rata | `#928069` |
| Saturasi rata-rata (HSV S) | **0,323** (median 0,303) |
| Hue median | **33,1°** |
| Piksel dalam rentang hue hangat 15–60° | **99,9 %** |

```css
.article-card__img{ filter:sepia(.45) saturate(.85) contrast(.96) brightness(1.03); }
```

- Filter **hanya** pada thumbnail arsip kategori sejarah/babad.
- Artikel konten modern (galeri, ilustrasi, foto berwarna) **tidak boleh** diberi sepia — ini pengecualian yang dinyatakan eksplisit di [PRD §13](Product%20Requirements%20Document%20(PRD)%2018%20Section.md).
- Gambar wajib `alt` deskriptif; dekoratif `alt=""`.

### 3.6 Footer (`SiteFooter`)

- Latar (**dikonfirmasi 5 Okt 2026** — UIRD-04): varian **terang**. `background: var(--ivory)`,
  pemisah atas `1px solid var(--hairline)`, judul kolom `--ink-900`, teks & tautan `--ink-400`
  (hover `--accent`), baris copyright `--muted`. Karakter kertas tetap terjaga dan kontras
  teks terhadap ivory tetap ≥ 4,5:1.
- Konten minimum (terverifikasi di situs live): brand + tagline `Cerita, Budaya, dan Pesona Bali`; kolom `Lebih Dekat` (Tentang Kami, Kebijakan Privasi, Syarat dan Ketentuan, Hubungi Kami, Disclaimer, FAQ); kolom `Eksplor balikisah.com` (Wisata, Budaya Bali, Sejarah Bali, Kuliner Bali, Cerita Lokal, Panduan Perjalanan); kolom `Topik Populer` (Hidden Gem Bali, Tradisi Bali, Pura Bali, Makanan Khas, Itinerary Bali, Warisan Budaya Bali); baris `© 2026 balikisah.com. Semua Hak Dilindungi.`
- Font: sans, `--fs-excerpt`; heading kolom: serif 600 18 px.

### 3.7 States (wajib untuk setiap elemen interaktif)

| State | Perlakuan |
|---|---|
| Default | Sesuai token |
| Hover | Warna → aksen; kartu naik 2 px + shadow halus |
| Focus-visible | `outline: 2px solid var(--accent); outline-offset: 3px` — **tidak boleh dihapus** |
| Active | `translateY(1px)` pada CTA; chip mempertahankan `aria-pressed` |
| Disabled | `opacity:.5; cursor:not-allowed` — tetap di DOM |
| Loading (chip/filter) | Skeleton dengan shimmer ungu; `aria-busy="true"` |

---

## 4. Layout & Breakpoints

| Breakpoint | Container | Kolom kartu | Navigasi | H1 |
|---|---|---|---|---|
| ≥ 1280 px | 1120 px | **4** | Desktop penuh | 40 px |
| 1024–1279 px | 100% − 64 px | 3 | Desktop penuh | 36 px |
| 768–1023 px | 100% − 48 px | 2 | Hamburger | 32 px |
| 480–767 px | 100% − 40 px | 2 | Hamburger | 28 px |
| ≤ 479 px | 100% − 32 px | 1 | Hamburger | 24 px |

Fluid H1: `clamp(24px, 2.8vw + 8px, 40px)`.

---

## 5. Halaman Archive — Mockup Nilai

```
viewport 1440×810 · container 1120 · gutter 160

y=0    ┌─ HEADER 78px  bg #FFFFFF ──────────────────────────┐
       │ 137                                  [Hubungi Kami]│  (CTA referensi 122×38, r999 → terukur 149,8 × 35 dengan label `Hubungi Kami`; lihat deviasi UIRD-02)
y=78   ├─ border-bottom #E8E2D2 ────────────────────────────┤
y=118  │  Kategori archive                                   │  14px Inter #887861
y=135  │  Sejarah dan Babad Bali                             │  40px Playfair 800 #180E00
y=215  │  ─────────────────────────────────────────────────  │  1px #E5DCC6
y=234  │  (Kerajaan Bali)(Candi)(Tokoh Sejarah)(Soratirin)   │  chips h38 gap11
y=272  │  (Kerajaan)(listowa)                                │
y=299  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐         │
       │  │ image  │ │ image  │ │ image  │ │ image  │         │  259×171, ratio 3:2
       │  │ 171px  │ │ 171px  │ │ 171px  │ │ 171px  │         │  sepia filter
y=470  │  │ title  │ │ title  │ │ title  │ │ title  │         │  20px/1.4 serif
       │  │ excerpt│ │ excerpt│ │ excerpt│ │ excerpt│         │  14px/1.55 #73706A
y=644  │  │ date   │ │ date   │ │ date   │ │ date   │         │  12px #A1A09B
y=644  │  └────────┘ └────────┘ └────────┘ └────────┘         │  card h345 r14
y=672  │            gap 28 → baris berikutnya               │
y=1017 │  ┌────────┐ …                                      │
       └────────────────────────────────────────────────────┘
        bg #F7F0DD
```

---

## 6. Inventaris Komponen

| # | Komponen | Tipe | Halaman |
|---|---|---|---|
| 1 | `SiteHeader` | Global | Semua |
| 2 | `Logo` | Global | Semua |
| 3 | `DesktopNav` + `NavDropdown` | Global | ≥ 1024 |
| 4 | `MobileNav` (drawer) | Global | ≤ 1024 |
| 5 | `PrimaryCta` | Global | Semua |
| 6 | `CategoryArchiveHeader` | Archive | Kategori |
| 7 | `ChipGroup` / `CategoryChip` | Archive | Kategori |
| 8 | `ArticleCard` | Archive + Home | Kategori, Home |
| 9 | `ArticleGrid` | Layout | Kategori, Home |
| 10 | `Pagination` | Archive | Kategori |
| 11 | `SiteFooter` | Global | Semua |
| 12 | `FooterLinkGroup` | Global | Semua |
| 13 | `SearchOverlay` | Global | Semua |
| 14 | `Breadcrumb` | Artikel | Artikel, Statis |
| 15 | `RelatedArticles` | Artikel | Artikel |
| 16 | `AuthorBadge` | Artikel | Artikel, Home |
| 17 | `AdSlot` | Monetisasi | Home, Kategori, Artikel |
| 18 | `NewsletterForm` | Global | Footer |
| 19 | `ContactForm` | Statis | Contact |
| 20 | `LoadingSkeleton` | State | Semua |

---

## 7. Halaman — Persyaratan UI per Halaman

### 7.1 Category Archive (referensi utama)
1. Header putih dengan logo serif-cokelat + nav + CTA.
2. Eyebrow muted → H1 serif → hairline.
3. Chip filter (aktif = terracotta).
4. Grid kartu 4 kolom di atas ivory.
5. Pagination minimal di bawah grid.
6. Footer.
**Tidak boleh** ada: hero image besar, slider otomatis, pop-up, search bar besar.

### 7.2 Article Detail
`Breadcrumb` (Home / Kategori / Judul) → `H1` serif 40–44 px → baris metadata (author, tanggal, reading time, kategori chip) → hero image 16:9 tanpa sepia → body **max-width 720 px** serif/sans hybrid, `line-height: 1.75` → divider → `RelatedArticles` (3 kartu) → footer.

### 7.3 Home
Berbeda dari archive: boleh ada hero. Wajib memuat `FeaturedHero`, `LatestGrid` (3 kolom), `HottestArticles` (carousel dengan tombol Prev/Next — sudah ada di situs live), `ReadMore`, lalu footer. **Tetap** memakai token yang sama.

### 7.4 Statis (Tentang Kami, Kebijakan Privasi, Syarat & Ketentuan, Disclaimer, FAQ, Contact)
Template bersih: H1 serif + konten `max-width: 720px` + heading `h2` serif 28 px + `h3` 20 px + list dengan marker terracotta. **Tanpa** komponen archive.

---

## 8. Contrast & Accessibility

| Kombinasi | Rasio | Target | Status |
|---|---|---|---|
| `--ink-900 #180E00` on `--ivory #F7F0DD` | **15,4 : 1** | AAA | ✅ |
| `--ink-500 #73706A` on `#FFFFFF` | **4,6 : 1** | AA (≥4,5) | ✅ |
| `--ink-400 #A1A09B` on `#FFFFFF` | **2,6 : 1** | ≥4,5 | ❌ |
| `--chip-ink #54432C` on `--chip-fill #E7D6BC` | **7,4 : 1** | AAA | ✅ |
| `#FFFFFF` on `--accent #94542E` | **6,1 : 1** | AA | ✅ |
| `#FFFFFF` on `--accent-chip #8F5432` | **6,6 : 1** | AA | ✅ |
| `--muted #887861` on `--ivory #F7F0DD` | **3,4 : 1** | ≥4,5 | ❌ |

**Tindakan wajib (deviation from screenshot, accessibility takes precedence):**

1. **Tanggal kartu** `--ink-400 #A1A09B` (terukur dari referensi) hanya **2,6 : 1** → gagal WCAG AA. Pada kode produksi gunakan **`#6E6B65`** (rasio 5,1 : 1). Nilai `#A1A09B` tetap dicatat sebagai nilai referensi visual, bukan nilai aksesibel.
2. **Eyebrow** `--muted #887861` (3,4 : 1) → gunakan **`#6B5F4C`** (5,6 : 1) untuk teks eyebrow. Nuansa visual tetapsimilar dengan referensi.
3. Ukuran teks minimum: **16 px** untuk body mobile; chip min **15 px**.
4. Target sentuh minimum **44 × 44 px** (chip 38 px tinggi → tambahkan `::after` invisible hit-area).
5. Judul kartu `<h2>`/`<h3>`;eyebrow bukan heading.
6. `alt` wajib untuk semua gambar informatif.
7. `prefers-reduced-motion` → matikan semua transisi & carousel auto-play.
8. Focus ring **tidak boleh** dihapus (`outline: none` tanpa pengganti = pelanggaran).

---

## 9. Checklist Kepatuhan 100% Tema

Verifikasi visual per-element. Semua harus ✅ sebelum rilis.

**Warna**
- [ ] Background halaman persis `#F7F0DD` (atau ±3% per kanal)
- [ ] Header persis `#FFFFFF`
- [ ] Permukaan kartu `#FFFFFF`
- [ ] CTA `#94542E` + teks putih
- [ ] Chip aktif `#8F5432`, chip non-aktif `#E7D6BC`
- [ ] Hairline `#E5DCC6` di bawah H1
- [ ] Logo berwarna cokelat `#6F5138`, bukan hitam
- [ ] Tumbnail disepia (S ≈ 0,32; hue ≈ 33°)

**Tipografi**
- [ ] H1 serif bold, **bukan** sans
- [ ] Judul kartu serif bold
- [ ] Nav/eyebrow/chip/excerpt/date sans
- [ ] Eyebrow **tidak** uppercase
- [ ] Judul kartu max 2 baris, excerpt max 3 baris

**Struktur**
- [ ] Logo di kiri, nav di kanan, CTA paling kanan
- [ ] Menu 8 item seperti live, **0 chevron** (diperbarui 7 Okt 2026)
- [ ] Urutan: eyebrow → H1 → hairline → chips → grid
- [ ] 4 kolom di desktop
- [ ] Card 3:2 image, total tinggi ≈ 345 px @1440
- [ ] Gap 28 px, radius 14 px, padding 16 px

**Pola negatif (dilarang)**
- [ ] Tidak ada warna biru/link default `#0000EE`
- [ ] Tidak ada gradient, glassmorphism, neon
- [ ] Tidak ada shadow berat pada kartu
- [ ] Tidak ada container bulat berlebihan
- [ ] Tidak ada elemen visual yang tidak ada di referensi tanpa kebutuhan fungsi

---

## 10. Deliverable Implementasi

```css
/* tokens.css — salinan langsung dari §2 */
:root{
  /* surface */
  --ivory:#F7F0DD;  --surface:#FFFFFF;  --border-card:#EDE7DA;
  --hairline:#E5DCC6;  --border-header:#E8E2D2;
  /* ink */
  --ink-900:#180E00;  --ink-700:#302923;  --ink-500:#73706A;
  --ink-400:#6E6B65;              /* A11Y-adjusted, see §8 */
  --ink-300:#3A3731;  --brand-brown:#6F5138;
  /* accent */
  --accent:#94542E;  --accent-hover:#7A4526;  --accent-chip:#8F5432;
  --chip-fill:#E7D6BC;  --chip-ink:#54432C;  --on-accent:#FFFFFF;
  --muted:#6B5F4C;                 /* A11Y-adjusted, see §8 */
  /* type */
  --font-display:"Playfair Display",Georgia,"Times New Roman",serif;
  --font-ui:"Inter",-apple-system,"Segoe UI",Arial,sans-serif;
  --fs-h1:clamp(24px,2.8vw + 8px,40px);
  --fs-logo:clamp(20px,1.4vw + 10px,28px);
  --fs-card-title:clamp(18px,.5vw + 16px,20px);
  --fs-nav:15px;  --fs-eyebrow:14px;  --fs-chip:15px;
  --fs-excerpt:clamp(14px,.2vw + 13px,14px);  --fs-date:12px;
  /* space */
  --sp-container:1120px;  --gutter:clamp(20px,11vw,160px);
  --header-h:78px;  --grid-gap:28px;  --card-pad:14px;
  --card-gap-title:6px;  --card-gap-excerpt:8px;
  /* shape */
  --radius-card:14px;  --radius-pill:999px;
  --shadow-card:0 1px 2px rgba(63,48,32,.05);
  --shadow-cta:0 2px 6px rgba(148,84,46,.22);
}
@media (max-width:1023px){ :root{ --header-h:64px; --grid-gap:20px; } }

@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{ animation-duration:.01ms!important;
    transition-duration:.01ms!important; scroll-behavior:auto!important; }
}
```

---

## 11. Permukaan Iklan (Opsional)

- Ukuran: **728 × 90** (leaderboard), **336 × 280**, **300 × 250**.
- `background: #FFFFFF; border:1px solid var(--border-card); border-radius:8px;`
- Label `Iklan`/`Sponsored` wajib tampil 10 px uppercase `--ink-400` di sudut.
- **Dilarang** menaruh iklan di atas fold pada viewport < 1024 px atau di dalam grid kartu.

---

## 12. SEO & Meta di UI

| Elemen | Aturan |
|---|---|
| `<title>` | `{{Kategori}} - balikisah.com` (≤ 60 karakter) — brand final per UIRD-01 |
| Meta description | Excerpt kategori, 140–160 karakter |
| Canonical | Absolute, self-referencing |
| Open Graph | `og:title`, `og:description`, `og:image` (featured image, 1200 × 630), `og:type=website` |
| Twitter Card | `summary_large_image` |
| `lang` | `id-ID` (live site saat ini `ID` → **perbaiki**) |
| Breadcrumb | JSON-LD `BreadcrumbList` |

---

## 13. Audit Kompatibilitas

| Browser | Min version | Catatan |
|---|---|---|
| Chrome / Edge | 110 | Baseline |
| Firefox | 110 | Baseline |
| Safari (macOS) | 15.4 | `-webkit-line-clamp` |
| Safari (iOS) | 15.4 | Hairline, sticky |
| Android Chrome | 110 | — |
| Samsung Internet | 20 | — |

Tidak ada polyfill wajib. `aspect-ratio`, `gap` flexbox, `clamp()`, CSS custom properties semuanya tersedia.

---

## 14. Verifikasi Pixel

Untuk memvalidasi hasil implementasi terhadap referensi, jalankan:

```bash
# tangkap archive pada 1440×810
playwright screenshot --viewport-size=1440,810 \
  "http://balikisah.com/category/sejarah-dan-babad-bali" ref.png

# bandingkan geometri & warna
python compare_ref.py ref.png ref.png
```

**Acceptance gate:** ΔE (CIE76) ≤ 3,0 untuk setiap patch solid; Δ posisi ≤ 2 px untuk setiap batas elemen; Δ tinggi teks ≤ 1 RU.

---

## 15. Catatan Rekonsiliasi dengan Situs Live

Observasi langsung pada `http://balikisah.com/` (5 Oktober 2026) menunjukkan kondisi **saat ini**:

| Aspek | Situs live (terverifikasi) | Referensi screenshot (target) |
|---|---|---|
| Background | `#fdfdfd` (putih) | `#F7F0DD` (ivory) |
| Aksen | `#2b2b60` / `#213758` (navy) | `#94542E` (terracotta) |
| Font body | `Julius Sans One` | Inter + Playfair Display |
| Logo | `Bali Kisah` | `balikisah.com` |
| Navigasi | Hamburger saja | Nav desktop + CTA |
| Footer | Navy `#213758` | — (tidak ada di referensi) |
| Konten | Bukan kategori sejarah | Archive "Sejarah dan Babad Bali" |

> **Dokumen ini mendefinisikan tema TARGET yang diminta, bukan audit kondisi live.** Perubahan tema pada situs live adalah keputusan produk tersendiri yang dicatat di [BRD §3](Business%20Requirements%20Document%20(BRD).md) dan [PRD §2](Product%20Requirements%20Document%20(PRD)%2018%20Section.md).

---

## 16. Keputusan Terbuka untuk Dikonfirmasi

| # | Item | Rekomendasi | Impact |
|---|---|---|---|
| UIRD-01 | Nama logo final: `balikisah.com` atau `Bali Kisah`? | `balikisah.com` (identik referensi) | **DIKONFIRMASI 5 Okt 2026** — `balikisah.com` dipakai untuk **seluruh identitas**: logo, judul halaman, kolom footer, copyright |
| UIRD-02 | CTA berbahasa Inggris (`Contact us`) di situs berbahasa Indonesia? | Diterjemahkan penuh | **DIKONFIRMASI 5 Okt 2026** — CTA `Hubungi Kami`, nav `Kontak`; tidak ada label Inggris tersisa di UI |
| UIRD-03 | Item nav `Stonian` dan chip `Soratirin` / `listowa` | **DIKONFIRMASI 5 Okt 2026** — dipakai apa adanya, bukan placeholder | — |
| UIRD-06 | Menu utama masih memakai label referensi (`Kategori`, `Kerajaan`, `Stonian`, `Blog`, `Kontak`) | Samakan dengan balikisah.com | **DIKONFIRMASI 7 Okt 2026** — menu menjadi 8 tautan tanpa chevron: `Home`, `Budaya`, `Tradisi`, `Kuliner`, `Sejarah`, `Wisata`, `Tips Traveling`, `Tentang Kami`; kategori bernama memakai target `kategori:<Nama>` |
| UIRD-04 | Footer: gelap atau terang? | Terang (ivory + hairline) untuk menjaga karakter kertas | **DIKONFIRMASI 5 Okt 2026** — varian terang: `--ivory`, judul `--ink-900`, teks `--ink-400`, pemisah `--hairline` |
| UIRD-05 | Halaman mana yang menjadi *canonical* tema ini? | Archive kategori sebagai archetype | **DIKONFIRMASI 5 Okt 2026** — **Beranda** (`#view-home`) sebagai halaman default/*canonical*; arsip kategori tetap ada sebagai halaman tema |

---

## 17. Riwayat Revisi

| Versi | Tanggal | Perubahan | Penulis |
|---|---|---|---|
| 1.2 | 7 Okt 2026 | **UIRD-06** — menu utama disamakan dengan balikisah.com: 8 tautan tanpa chevron (`Home`, `Budaya`, `Tradisi`, `Kuliner`, `Sejarah`, `Wisata`, `Tips Traveling`, `Tentang Kami`); label referensi `Kategori`/`Kerajaan`/`Stonian`/`Blog`/`Kontak` tidak lagi dipakai. Tema, palet, dan tipografi tidak berubah. | Requirements Engineering |
| 1.1 | 5 Okt 2026 | UIRD-01/02/04/05 dikonfirmasi pengguna: identitas tunggal `balikisah.com`; CTA `Hubungi Kami` + nav `Kontak`; footer varian terang (ivory + hairline); halaman kanonik **Beranda**. | Requirements Engineering |
| 1.0 | 5 Okt 2026 | Baseline. Seluruh token diukur dari screenshot referensi (756 × 425). Skala ke kanvas 1440 × 810 (× 1,9048). Identifikasi divergence dengan tema live. | Requirements Engineering |