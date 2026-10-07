# Quality Requirements Document (QRD)

> **Project:** BaliKisah.com
> **Status:** Baseline v1.0
> **Tanggal:** 5 Oktober 2026
> **Dokumen terkait:** [PRD](Product%20Requirements%20Document%20(PRD)%2018%20Section.md) · [FRD](Functional%20Requirements%20Document%20(FRD).md) · [TRD](Technical%20Requirements%20Document%20(TRD).md) · [UIRD](User%20Interface%20Requirements%20Document%20(UIRD).md)

---

## 1. Prinsip Mutu

1. **Performa adalah kualitas.** Pelanggan yang menunggu 4 detik sudah pergi.
2. **Konten adalah produk.** Mutu editorial setara mutu perangkat lunak.
3. **Aksesibilitas bukan tambahan.** WCAG 2.1 AA adalah syarat penerimaan.
4. **SEO adalah kualitas.** Halaman rusak adalah bug.
5. **Terukur, bukan perasaan.** Setiap target punya angka dan cara ukur.

---

## 2. Atribut Kualitas & Metrik

### 2.1 Performa

| ID | Atribut | Metrik | Target | Cara ukur |
|---|---|---|---|---|
| Q-P-01 | Kecepatan muat | LCP (p75 mobile) | **< 2,5 s** | CrUX / Lighthouse CI |
| Q-P-02 | Responsif | INP (p75) | **< 200 ms** | CrUX |
| Q-P-03 | Stabilitas layout | CLS (p75) | **< 0,1** | CrUX |
| Q-P-04 | Respons server | TTFB | **< 800 ms** | Lighthouse / curl |
| Q-P-05 | Ukuran halaman | HTML gzip | **≤ 60 KB** | CI budget check |
| Q-P-06 | Ukuran bundle | JS first-load gzip | **≤ 120 KB** | CI budget check |
| Q-P-07 | Rasio cache | Cache hit rate | **≥ 90%** | Cloudflare analytics |

### 2.2 Keandalan

| ID | Atribut | Metrik | Target |
|---|---|---|---|
| Q-R-01 | Ketersediaan | Uptime | **≥ 99,9%** (per bulan) |
| Q-R-02 | Error rate | 5xx response | **< 0,05%** request |
| Q-R-03 | Pemulihan | Recovery time (bila gagal) | **< 15 menit** |
| Q-R-04 | Tanpa broken link | Link check | **0 broken** (toleransi 0,5% pada link eksternal) |
| Q-R-05 | Build reproducibility | Build sukses | **100%** |

### 2.3 Keamanan

| ID | Atribut | Metrik | Target |
|---|---|---|---|
| Q-S-01 | Transport | HTTPS | **100% halaman**, HSTS aktif |
| Q-S-02 | Headers | Security headers | **6 dari 6** terpasang |
| Q-S-03 | Dependencies | Kerentanan kritis | **0** |
| Q-S-04 | Input safety | XSS pada formulir | **0** |
| Q-S-05 | Secrets | Kebocoran kredensial di repo | **0** |
| Q-S-06 | Backup | Backup harian | **Berhasil 100%**, retensi 30 hari |

### 2.4 Aksesibilitas

| ID | Atribut | Metrik | Target |
|---|---|---|---|
| Q-A-01 | Standar | WCAG | **2.1 level AA** |
| Q-A-02 | Audit otomatis | axe / Lighthouse | **0 serious, 0 critical** |
| Q-A-03 | Kontras teks | Rasio kontras | **≥ 4,5:1** |
| Q-A-04 | Keyboard | Kontrol tanpa mouse | **100%** |
| Q-A-05 | Struktur heading | Hierarchy | **Valid** di semua halaman |
| Q-A-06 | Alt text | Gambar informatif | **100%** |
| Q-A-07 | Motion | `prefers-reduced-motion` | **Dihormati** |

> **Temuan dari pengukuran referensi:** warna tanggal kartu `#A1A09B` (2,6:1) dan eyebrow `#887861` (3,4:1) di [UIRD §8](User%20Interface%20Requirements%20Document%20(UIRD).md) **gagal AA**. Implementasi produksi wajib memakai nilai yang sudah dikoreksi (`#6E6B65`, `#6B5F4C`). Ini adalah penyimpangan yang disengaja dari referensi demi aksesibilitas.

### 2.5 Kompatibilitas

| ID | Atribut | Target |
|---|---|---|
| Q-C-01 | Browser | 2 versi terakhir Chrome, Firefox, Safari, Edge |
| Q-C-02 | Perangkat | 320 – 2560 px |
| Q-C-03 | Input | Keyboard, mouse, sentuh |
| Q-C-04 | Browser tanpa JS | Konten artikel tetap dapat dibaca (progressive enhancement) |

### 2.6 Kualitas Konten

| ID | Atribut | Metrik | Target |
|---|---|---|---|
| Q-CN-01 | Kelengkapan | Artikel lolos checklist | **100%** |
| Q-CN-02 | Koreksi | Artikel yang dikoreksi | **≤ 1%** |
| Q-CN-03 | Kredibilitas | Klaim fakta bersumber | **100%** |
| Q-CN-04 | Bahasa | Konsistensi bahasa Indonesia | **100%** |
| Q-CN-05 | Freshness | Artikel > 24 bulan diperbarui | **≥ 50%** |

### 2.7 SEO

| ID | Atribut | Metrik | Target |
|---|---|---|---|
| Q-SEO-01 | Index rate | Halaman terindeks ÷ terbit | **≥ 85%** |
| Q-SEO-02 | Schema valid | Rich Results Test | **Tanpa error** |
| Q-SEO-03 | Metadata | Halaman dengan title + description unik | **100%** |
| Q-SEO-04 | Redirect | URL lama | **301, bukan 404** |
| Q-SEO-05 | Sitemap | Kelengkapan | **100% halaman terindeks** |

### 2.8 Keamanan Konten & Editorial

| ID | Atribut | Target |
|---|---|---|
| Q-CE-01 | Kredibilitas klaim budaya | 100% punya sumber atau penafian |
| Q-CE-02 | Right context | Konten sensitif diberi konteks |
| Q-CE-03 | Tanpa konten membingungkan | Penafian harus jelas dan tidak bertentangan |
| Q-CE-04 | Hak cipta | 100% gambar berlisensi atau milik sendiri |

---

## 3. Strategi Pengujian

| Level | Jenis | Alat | Cakupan | Cakupan |
|---|---|---|---|---|
| **Unit** | Fungsi murni (related, seo, schema) | Vitest | Logika inti | ≥ 70% |
| **Integration** | Komponen UI | Vitest + Testing Library | Komponen kunci | — |
| **E2E** | Alur pengguna | Playwright | 12 alur kritikal | 100% passed |
| **Visual** | Regresi UI | Playwright + screenshot | Halaman kunci | — |
| **Performa** | Lighthouse CI | @lhci/cli | Setiap PR | Threshold |
| **Aksesibilitas** | axe otomatis | axe-core | Setiap halaman | 0 serious |
| **Aksesibilitas manual** | Keyboard, screen reader | Manual | Rilis | 100% |
| **Keamanan** | Dependency + header | npm audit, custom | Setiap build | 0 kritis |
| **Lintas browser** | Smoke | Playwright matrix | Rilis | 4 browser |

### 3.1 Alur Kritis untuk E2E

| ID | Alur |
|---|---|
| E2E-01 | Buka beranda → klik kategori → chip filter → buka artikel |
| E2E-02 | Cari artikel → buka hasil → baca |
| E2E-03 | Buka artikel → klik related → artikel kedua |
| E2E-04 | Buka mobile drawer → navigasi → tutup dengan `Esc` |
| E2E-05 | Form newsletter: validasi error → sukses |
| E2E-06 | 404 untuk slug tidak dikenal |
| E2E-07 | Navigasi keyboard pada chip filter |
| E2E-08 | Sitemap XML valid |
| E2E-09 | Redirect URL lama → 301 |
| E2E-10 | Ganti bahasa attribute `lang="id-ID"` |

### 3.2 Pengujian Visual (Penting untuk Tema)

Karena tema adalah inti produk, pengujian visual **wajib**:

```bash
# screenshot setiap halaman kunci pada 1440×810 dan 390×844
npx playwright test visual.spec.ts --update-snapshots
```

Baseline: `__screenshots__/1440x810/`, `__screenshots__/390x844/`.
Diff threshold: **≤ 0,1%** piksel berbeda. Perubahan warna yang disengaja (misalnya koreksi kontras) harus di-exempt.

---

## 4. Standar Kode

| Aspek | Standar |
|---|---|
| TypeScript | `strict: true`, tanpa `any` tanpa alasan tertulis |
| Lint | ESLint + Prettier, error = build gagal |
| Aksesibilitas | `eslint-plugin-jsx-a11y` aktif |
| Commit | Conventional Commits |
| Coverage | ≥ 70% pada logika inti |
| Review | Minimal 1 approval untuk perubahan pada routing, schema, atau keamanan |

---

## 5. Quality Gates (Gerbang Rilis)

Rilis **ditolak** bila salah satu gagal:

| Gate | Threshold | Failing |
|---|---|---|
| Unit test | 100% pass | ≥ 1 gagal |
| E2E test | 100% pass pada 12 alur | ≥ 1 gagal |
| Lighthouse Performance | ≥ 90 | < 90 |
| Lighthouse Accessibility | ≥ 95 | < 95 |
| Lighthouse SEO | ≥ 95 | < 95 |
| axe serious/critical | 0 | ≥ 1 |
| Dependency audit | 0 kritis | ≥ 1 kritis |
| TypeScript | 0 error | ≥ 1 error |
| Typecheck | 0 error | ≥ 1 error |
| Bundle budget | ≤ JS 120 KB | Melebihi |
| Visual diff | ≤ 0,1% | Melebihi |
| Rich Results | 0 error | ≥ 1 error |

---

## 6. Monitoring Produksi

| Aspek | Alat | Alarm |
|---|---|---|
| Uptime | UptimeRobot | 2× gagal berturut-turut |
| Error rate | Sentry | > 1% error dalam 5 menit |
| Core Web Vitals | RUM / CrUX | Turun > 10% dari baseline |
| Traffic anomali | GA4 | Turun > 30% WoW |
| Search errors | Search Console | Peningkatan > 20% |
| Broken link | Link checker mingguan | ≥ 3 baru |

**Respons insiden:**

| Severity | Contoh | Target respons |
|---|---|---|
| P1 | Situs down | < 15 menit |
| P2 | Fitur inti rusak | < 1 jam |
| P3 | Kesalahan kecil | < 1 hari kerja |
| P4 | Permintaan enhancement | Backlog |

---

## 7. Standar Editorial (Ringkas)

Rincian di [PRD §11](Product%20Requirements%20Document%20(PRD)%2018%20Section.md).

Checklist sebelum terbit:

- [ ] Kategori utama dipilih
- [ ] Ringkasan 140–160 karakter
- [ ] Minimal 800 kata (artikel fitur)
- [ ] Klaim faktual memiliki sumber
- [ ] Gambar punya alt + credits bila perlu
- [ ] Nama orang/tempat konsisten
- [ ] Bahasa Indonesia konsisten
- [ ] Title ≤ 60 karakter
- [ ] Slug ≤ 75 karakter, lowercase, mengandung tanda hubung

---

## 8. Acceptance Criteria Per Delivery

| Tahap (PRD R0–R5) | Kriteria mutu |
|---|---|
| **R0** | HTTPS 100%, schema valid, GA4 terverifikasi, tidak ada regresi traffic |
| **R1** | Checklist UIRD §9 100% ✅, visual diff ≤ 0,1%, Lighthouse ≥ 90/95/95 |
| **R2** | 12 alur E2E lulus, chip filter berfungsi, pagination benar |
| **R3** | Pencarian berfungsi, related akurat, sitemap lengkap |
| **R4** | Density iklan terkendali, tidak ada CLS dari iklan |
| **R5** | Newsletter berfungsi, tag & penulis berfungsi |

---

## 9. Matriks Traceability Ringkas

| Atribut | Requirement Sumber | Target |
|---|---|---|
| Performa | TRD §6, NFR-01…04 | LCP < 2,5 s, INP < 200 ms, CLS < 0,1 |
| Keandalan | TRD §11 | 99,9% uptime |
| Keamanan | TRD §9 | 6 header, 0 kerentanan kritis |
| Aksesibilitas | FRD-17, UIRD §8 | WCAG 2.1 AA, kontras ≥ 4,5:1 |
| SEO | FRD-10, TRD §7 | Index ≥ 85%, schema valid |
| Konten | PRD §11 | Koreksi ≤ 1% |
| Kompatibilitas | UIRD §13 | 2 versi terakhir, 320–2560 px |

---

## 10. Definition of Quality Done

- [ ] Semua quality gates [§5](#5-quality-gates-gerbang-rilis) hijau.
- [ ] Monitoring terpasang dan alarm diuji.
- [ ] Dokumentasi mutakhir (README, CHANGELOG).
- [ ] Handoff ke tim berikutnya selesai.
- [ ] Aset rollback tersedia.