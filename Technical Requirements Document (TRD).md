# Technical Requirements Document (TRD)

> **Project:** BaliKisah.com
> **Status:** Baseline v1.0
> **Tanggal:** 5 Oktober 2026
> **Dokumen terkait:** [PRD](Product%20Requirements%20Document%20(PRD)%2018%20Section.md) · [FRD](Functional%20Requirements%20Document%20(FRD).md) · [QRD](Quality%20Requirements%20Document%20(QRD).md) · [UIRD](User%20Interface%20Requirements%20Document%20(UIRD).md)

---

## 1. Ringkasan Arsitektur

BaliKisah.com adalah situs editorial **statis-first dengan prerender**. Arsitektur dipilih agar:

- Core Web Vitals terpenuhi tanpa pekerjaan berat di server.
- Biaya hosting minimal dankumuldtif.
- Content aman dari serangan umum (tidak ada input dinamis di server).

```
Browser
  │
  ├── CDN (Cloudflare)  ── cache aset statis + HTML
  │        │
  │        ├── /_next/static/*   (hash, cache 1 tahun, immutable)
  │        ├── assets/*          (gambar, font)
  │        └── HTML dokumen      (ISR / SSG)
  │
CMS (headless)  ──build──▶  Output statis  ──deploy──▶  CDN
```

---

## 2. Kondisi Teknis Saat Ini (terverifikasi)

Diperiksa langsung melalui DOM dan DevTools pada `http://balikisah.com/`:

| Aspek | Nilai terverifikasi | Penilaian |
|---|---|---|
| Framework | Tidak teridentifikasi; pola DOM WordPress + Tailwind CDN | ⚠️ perlu konfirmasi |
| CSS delivery | `cdn.tailwindcss.com` (Tailwind CDN, runtime compile) | ❌ **Berat** |
| Font loading | 3 stylesheet Google Fonts: **23 family** dimuat | ❌ **Berlebihan** |
| Font body | `Julius Sans One` | ⚠️ Non-standar |
| Font | `Inter`, `Libertinus Mono`, `Manufacturing Consent` | ❌ Tidak dipakai |
| Analytics | Histats + Cloudflare Insights | ⚠️ Histats pihak ketiga |
| Skema | `http://` | ❌ Bukan HTTPS |
| `lang` | `ID` | ❌ Bukan `id-ID` |
| Structured data | Tidak ada JSON-LD | ❌ Hilang |
| Container | `--main-width: 1100px` | ✅ Wajar |

### 2.1 Temuan Kritis

| # | Temuan | Dampak | Prioritas |
|---|---|---|---|
| T-01 | Tailwind dimuat lewat CDN runtime compiler | Perfomansi, CLS, tanpa cache | **P0** |
| T-02 | 23 family font diunduh bersamaan | Payload +100 KB, render blocking | **P0** |
| T-03 | Bukan HTTPS | Sinyal keamanan dan kepercayaan | **P0** |
| T-04 | Tanpa JSON-LD | Kehilangan rich result | **P1** |
| T-05 | Histats (skrip pihak ketiga) | Privasi, performa, Consent Mode | **P1** |
| T-06 | `lang="ID"` | Sinyal relevansi lokal ke mesin pencari | **P1** |
| T-07 | Tanpa `alt` pada beberapa gambar ikon | Aksesibilitas | **P2** |

---

## 3. Stack Target

| Lapisan | Pilihan | Alasan |
|---|---|---|
| **Framework** | Next.js 15 (App Router) | SSG/ISR, image optimization bawaan, routing file-based |
| **Styling** | Tailwind CSS 4 (build-time) + CSS variables | Token design dari [UIRD §2](User%20Interface%20Requirements%20Document%20(UIRD).md), tanpa runtime compile |
| **Content** | Headless CMS (WordPress REST, Strapi, atau Sanity) | Struktur konten kaya; WordPress sudah dipakai |
| **Database konten** | Bawaan CMS | Hindari basis data terpisah |
| **Search** | Client-side index untuk < 2.000 artikel; FigJam/Algolia bila lebih |-phase |
| **Hosting** | Cloudflare Pages / Vercel | Edge, otomatis, mudah |
| **CDN** | Cloudflare | Cache, WAF, optimasi gambar |
| **Font** | `next/font` self-host, hanya 2 family | Hilangkan 21 family |
| **Analytics** | GA4 + Search Console | Standar industri |
| **Images** | AVIF/WebP, `next/image` | Format modern, lazy loading |

> **Catatan:** migrasi stack WordPress ke Next.js adalah keputusan besar. Bila tidak مطلikan, **minimal** memperbaiki T-01, T-02, T-03 (build-time CSS, self-host font, HTTPS) yang menghasilkan sebagian besar perbaikan.

---

## 4. Struktur Proyek

```
balikisah/
├── src/
│   ├── app/
│   │   ├── layout.tsx              # Root layout, header, footer
│   │   ├── page.tsx                # Beranda
│   │   ├── kategori/[slug]/page.tsx
│   │   ├── [slug]/page.tsx          # Artikel
│   │   ├── cari/page.tsx
│   │   ├── tentang-kami/page.tsx
│   │   ├── kebijakan-privasi/page.tsx
│   │   ├── syarat-ketentuan/page.tsx
│   │   ├── disclaimer/page.tsx
│   │   ├── faq/page.tsx
│   │   ├── hubungi-kami/page.tsx
│   │   ├── sitemap.ts
│   │   ├── robots.ts
│   │   └── not-found.tsx
│   ├── components/
│   │   ├── layout/  (SiteHeader, DesktopNav, MobileNav, PrimaryCta, SiteFooter)
│   │   ├── archive/ (CategoryArchiveHeader, ChipGroup, CategoryChip, ArticleGrid, Pagination)
│   │   ├── article/ (ArticleCard, AuthorBadge, RelatedArticles, ShareButtons, Breadcrumb)
│   │   └── ui/      (AdSlot, NewsletterForm, LoadingSkeleton, SearchOverlay)
│   ├── content/     # Koleksi konten (MDX / JSON)
│   ├── lib/         # search, related, seo, schema
│   └── styles/      # tokens.css (UIRD §2), globals.css
├── public/
│   ├── images/      # Featured, 1200×630 OG
│   └── fonts/       # Playfair Display, Inter (self-host, woff2)
├── next.config.mjs
└── package.json
```

---

## 5. Strategi Rendering

| Route | Strategi | Alasan |
|---|---|---|
| `/` | ISR (revalidate 3600) | Diperbarui hourly |
| `/kategori/[slug]` | ISR (revalidate 3600) | Diperbarui hourly |
| `/[slug]` | SSG + on-demand revalidate | Stable |
| `/cari?q=` | Dinamis (server component) | Query-dependent |
| `/tentang-kami`, dll. | SSG | Stable |
| `/sitemap.xml` | Generate | Otomatis |

**ISR** dipilih agar artikel baru tampil tanpa rebuild penuh.

---

## 6. Budget Performa

### 6.1 Core Web Vitals (p75, mobile)

| Metrik | Target | Ambang gagal |
|---|---|---|
| **LCP** | < 2,5 s | > 4,0 s |
| **INP** | < 200 ms | > 500 ms |
| **CLS** | < 0,1 | > 0,25 |
| **TTFB** | < 800 ms | > 1.800 ms |

### 6.2 Budget Aset

| Aset | Budget | Catatan |
|---|---|---|
| HTML (aktual) | ≤ 60 KB (gzip) | Tanpa data excess |
| CSS total | ≤ 35 KB (gzip) | Critical inline |
| JS total | ≤ 120 KB (gzip) | First-load |
| JS thirds-party | ≤ 50 KB (gzip) | Analytics |
| Font | ≤ 90 KB (2 woff2 subset) | Self-host |
| Hero image | ≤ 120 KB | AVIF |
| Card image | ≤ 40 KB | AVIF, 400w |
| Total first-load | ≤ 350 KB (gzip) | — |

### 6.3 Strategi Pemuatan

| Elemen | Strategi |
|---|---|
| Font | `next/font` + `font-display: swap` + preload hanya yang dipakai |
| CSS kritikal | Inline; sisanya async |
| Gambar di atas lipatan | `priority`, `fetchpriority="high"`, preload |
| Gambar lain | `loading="lazy"`, `decoding="async"` |
| JavaScript | Minimal; komponen islands; `requestIdleCallback` untuk non-kritis |
| Analytics | Dimuat setelah consent atau `afterInteractive` |
| Font eksternal | **Dihapus total** (hanya 2 family, self-host) |

---

## 7. SEO Teknik

| ID | Requirement | Implementasi | Status live |
|---|---|---|---|
| TR-SEO-01 | HTTPS + redirect | Edge redirect `http→https` | ❌ belum |
| TR-SEO-02 | `lang="id-ID"` | `<html lang="id-ID">` | ❌ `ID` |
| TR-SEO-03 | Canonical absolut | `metadataBase` + `alternates.canonical` | ✅ ada |
| TR-SEO-04 | Sitemap otomatis | `app/sitemap.ts` | ❌ perlu cek |
| TR-SEO-05 | `robots.txt` | `app/robots.ts` | ❌ perlu cek |
| TR-SEO-06 | `Article` JSON-LD | `lib/schema` | ❌ tidak ada |
| TR-SEO-07 | `BreadcrumbList` JSON-LD | `lib/schema` | ❌ tidak ada |
| TR-SEO-08 | `WebSite` + `Person` | `lib/schema` | ❌ tidak ada |
| TR-SEO-09 | Open Graph image 1200×630 | Generate per artikel | ❌ perlu cek |
| TR-SEO-10 | Redirect 301 | Peta URL lama | ❌ perlu cek |
| TR-SEO-11 | Redirect otomatis | `generateStaticParams` + `_redirects` | — |
| TR-SEO-12 | Pagination `rel=next/prev` | Head link | — |

---

## 8. Aksesibilitas Teknis

| ID | Requirement |
|---|---|
| TR-A11Y-01 | HTML semantik: `<header> <nav> <main> <article> <footer>` |
| TR-A11Y-02 | Skip link menuju `#main-content` |
| TR-A11Y-03 | `focus-visible` global, tidak pernah dihapus |
| TR-A11Y-04 | `aria-pressed` pada filter chip |
| TR-A11Y-05 | `aria-expanded` + `focus trap` pada drawer mobile |
| TR-A11Y-06 | `role="region"` + `aria-label` pada carousel |
| TR-A11Y-07 | Gambar: `alt` deskriptif atau `alt=""` dekoratif |
| TR-A11Y-08 | `@media (prefers-reduced-motion: reduce)` |
| TR-A11Y-09 | Kontras teks ≥ 4,5:1 (lihat [UIRD §8](User%20Interface%20Requirements%20Document%20(UIRD).md)) |

---

## 9. Keamanan

| ID | Requirement |
|---|---|
| TR-SEC-01 | HTTPS penuh dengan HSTS (`max-age=31536000; includeSubDomains`) |
| TR-SEC-02 | Redirect `http → https` di edge |
| TR-SEC-03 | `Content-Security-Policy` ketat (default-src 'self') |
| TR-SEC-04 | `X-Content-Type-Options: nosniff` |
| TR-SEC-05 | `Referrer-Policy: strict-origin-when-cross-origin` |
| TR-SEC-06 | `X-Frame-Options: DENY` |
| TR-SEC-07 | Sanitasi input formulir kontak (anti-XSS) |
| TR-SEC-08 | Rate limiting pada endpoint formulir |
| TR-SEC-09 | Backup harian basis data konten (retensi 30 hari) |
| TR-SEC-10 |dependencies audit otomatis (npm audit, Dependabot) |
| TR-SEC-11 | Tidak menyimpan data pribadi di client |

**Header keamanan yang akan diterapkan:**

```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
X-Frame-Options: DENY
Permissions-Policy: camera=(), microphone=(), geolocation=()
Content-Security-Policy: default-src 'self'; script-src 'self' https://www.googletagmanager.com; style-src 'self' 'unsafe-inline' https://fonts.gstatic.com; img-src 'self' data: https:; connect-src 'self' https://*.google-analytics.com; font-src 'self'
```

---

## 10. Analytics & Monitoring

| Aspek | Tool | Catatan |
|---|---|---|
| Web analytics | GA4 | Standar; ganti Histats |
| Pencarian | Google Search Console | Wajib |
| Core Web Vitals | `web-vitals` library | Dilaporkan ke GA4 + RUM |
| Error monitoring | Sentry (free tier) | Error klien & server |
| Uptime | UptimeRobot | Pemantauan 5 menit |
| Log | Cloudflare Analytics | Akses |

> **Histats** (`s10.histats.com`) adalah skrip pihak ketiga yang menambah permintaan pihak ketiga dan berpotensi privasi. **Rekomendasi: migrasi ke GA4** setelah persetujuan. Interim: tambahkan `Consent Mode` dan muat setelah interaksi.

---

## 11. Deployment

| Aspek | Konfigurasi |
|---|---|
| Platform | Cloudflare Pages (atau Vercel) |
| Branch | `main` = produksi; `dev` = preview |
| Build | `npm ci && npm run build` |
| Preview | URL unik per branch/PR |
| Rollback | Redeploy commit sebelumnya (< 2 menit) |
| Environment | `NODE_ENV=production` |
| Secret | Disimpan di platform, bukan di repo |

**Pipeline:**

```
push/PR
  → lint
  → typecheck
  → test (unit + e2e)
  → build
  → Lighthouse CI (assert LCP < 2.5s, CLS < 0.1)
  → deploy preview
  → merge ke main → deploy produksi
```

---

## 12. Tooling

| Kategori | Tool |
|---|---|
| Package manager | npm / pnpm |
| Lint | ESLint + Prettier |
| Type safety | TypeScript strict |
| Test unit | Vitest |
| Test E2E | Playwright |
| Lighthouse | `@lhci/cli` |
| Format | Prettier |
| Git hooks | Husky + lint-staged |

---

## 13. Konten & Media Pipeline

| Aspek | Requirement |
|---|---|
| Format | Markdown / MDX, frontmatter |
| Gambar | Diunggah ke storage; varian AVIF/WebP |
| Ukuran | Featured 1200×630, OG 1200×630, card 400×267 (3:2) |
| Format | AVIF (utama), WebP (fallback), JPEG (fallback akhir) |
| Lazy | Semua kecuali gambar pertama |
| Font | Self-host, woff2, subset Latin |

---

## 14. Risiko Teknis

| # | Risiko | Dampak | Mitigasi |
|---|---|---|---|
| TR-01 | Migrasi ke Next.js besar | Tinggi | Fasa; mulai dari perbaikan CSS/font/HTTPS |
| TR-02 | WordPress API sebagai sumber konten | Sedang | Contract test, cache |
| TR-03 | Search tanpa indeks | Sedang | Client-side index untuk < 2.000 artikel |
| TR-04 | Gambar lama resolusi rendah | Sedang | Audit dan penggantian bertahap |
| TR-05 | Logika parsing rapuh | Rendah | Unit test |
| TR-06 | CSP memblokir analytics | Sedang | Uji di staging, allowlist teliti |

---

## 15. Definition of Done (Teknis)

Implementasi dianggap selesai bila:

1. ✅ Lighthouse: Performance ≥ 90, Accessibility ≥ 95, SEO ≥ 95, Best Practices ≥ 90.
2. ✅ Core Web Vitals hijau di CrUX (p75).
3. ✅ Tidak ada error console di produksi.
4. ✅ Tidak ada broken link.
5. ✅ Validasi Rich Results lulus untuk `Article` dan `Breadcrumb`.
6. ✅ Audit keamanan (dependency + header) bersih.
7. ✅ TypeScript strict tanpa error.
8. ✅ Test coverage ≥ 70% pada logika inti.