## Ringkasan perubahan
Jelaskan secara singkat apa yang diubah dan mengapa.

## Tipe perubahan
- [ ] Perbaikan bug
- [ ] Fitur baru
- [ ] Refaktor
- [ ] Dokumentasi
- [ ] Tweak/style
- [ ] Lainnya (jelaskan)

## Perubahan berkas utama
Sebut file/file kunci (mis. src/js, index.html, .freebuff/*.py, dll).

## Checklist sebelum merge
- [ ] Saya menjalankan `python .freebuff/build_site.py` dan **tidak mengubah artefak yang ter-commit kecuali memang perlu** (jika artefak diubah, commit bersamaan). Atau saya **tidak menyentuh sumber** sehingga artefak tetap identik.
- [ ] Memastikan hash artefak cocok (step "Cek drift artifacts terhadap hasil build") — tidak membiarkan `index.html/rss.xml/sitemap.xml/robots.txt` basi.
- [ ] Menjalankan test suite yang relevan (`test_drive_links.py`, `test_editor_regression.py`, `test_layout_responsive.py`) bila mengubah kode terkait.
- [ ] `verify_docs.py` / `verify_chrome.py` masih lulus bila ada perubahan UI/struktural.
- [ ] Tidak menyertakan file lokal (.freebuff/tmp/*, node_modules, *.log) ke dalam commit.
- [ ] Memperbarui dokumentasi di `.freebuff/run.md` jika ada perubahan prosedur build/CI.
- [ ] Branch mutakhir dengan `main` (`strict` aktif).

## Bukti (opsional)
Lampirkan screenshot, log ringkas, atau alasan mengapa skip pengecekan tertentu (hanya bila benar-benar aman).

## Catatan tambahan
Hal lain yang perlu diperhatikan reviewer (backward compat, risiko, dsb).
