# Metrik Evaluasi Skor Bantu Kurasi

Versi model: 0.2.0. Dibuat oleh `python -m kurasi.eval`; jangan sunting manual.
Data: 20 contoh produk SINTETIS (asumsi; bukan data lapak nyata). Sumber aturan: piagam kurasi §3-§4.

| Kelompok | Jumlah | Skor min | Skor maks | Skor rata | Rekomendasi tayang | Syarat |
|---|---|---|---|---|---|---|
| Terisi penuh | 20 | 100 | 100 | 100.0 | 20 | semua skor >= 70 |
| Tanpa foto | 20 | 65 | 65 | 65.0 | 0 | semua skor < 70 |
| Tanpa titik serah | 20 | 65 | 65 | 65.0 | 0 | semua skor < 70 |

Hasil gerbang QA: LULUS.

Catatan: skor hanya membantu. Keputusan tayang tetap kurator manusia.
