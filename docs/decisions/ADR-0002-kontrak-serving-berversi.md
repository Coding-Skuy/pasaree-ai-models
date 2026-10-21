# ADR-0002 — Kontrak serving skor kurasi berversi dan gerbang rilis

Status: Diusulkan | Tanggal: 2026-10-21

## Konteks

ADR-0001 mengunci bahwa serving lewat API Rust dan rilis diblokir bila evaluasi gagal. Kontrak serving belum ada di `pasaree-backend-service/docs/api/openapi.yaml`, dan dokumen SRS v1.0.0 masih templat, sehingga bentuk kontrak diturunkan dari AGENTS.md, piagam kurasi, dan model data katalog.

## Keputusan

1. Kontrak v1 (masukan lima field produk, keluaran skor/rekomendasi/alasan/gerbang/versi) didefinisikan di `docs/contracts/skor-kurasi-v1.md` dan diterapkan di `kurasi.serving`.
2. Transport internal: proses Python yang dijalankan backend Rust, JSON-lines stdin/stdout. Tidak ada listener jaringan sehingga Python tak dapat terekspos ke klien. Alternatif (HTTP internal) ditunda; bila dipilih, wajib ADR baru dan jaringan privat.
3. Dua nomor versi: `versi_kontrak` (bentuk data) dan `versi_model` (aturan/bobot, ada di model card). Backend menyimpan keduanya per keputusan kurasi.
4. Gerbang rilis `python -m kurasi.gate`: gagal bila evaluasi di bawah ambang, `eval/metrics.md` usang, atau model card tanpa nomor versi. Dipasang sebagai langkah CI pada siklus berikutnya.
5. Respons selalu `keputusan_final: kurator_manusia`; skor tidak memicu tayang/takedown otomatis.

## Konsekuensi

- Backend perlu menyepakati dan mencatat kontrak ini di openapi/ADR miliknya sebelum integrasi (belum disepakati, tertulis sebagai usulan).
- Bobot dan ambang masih asumsi tim AI; pengesahan Dewan Kurasi diperlukan sebelum rilis produksi.
- Menaikkan versi kontrak/model menuntut ADR baru, pembaruan model card, metrik, dan CHANGELOG.
