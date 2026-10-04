# pasaree-ai-models

Model kurasi Marketplace Pasaree. Divisi Pasaree (Marketplace), org Coding-Skuy. Template Opsi A.

Rujukan utama: [Pasaree-TownHall](https://github.com/Coding-Skuy/Pasaree-TownHall) — baca `lapak/00-piagam-kurasi.md` dan `katalog/10-model-data.md`.

## Peran

- Kurasi pendaftaran lapak dan tayang produk: kelengkapan data, foto, harga wajar, stok masuk akal, titik serah terisi.
- Skor bantu kurator manusia. Keputusan akhir tetap manusia sesuai piagam kurasi.
- Tidak menilai rasa atau higiene dapur. Higiene pangan mengikuti jalur Pawonee/Pedaree.

## Struktur

```
src/kurasi/model.py      Stub skor kurasi aturan jelas
docs/MODEL_CARD.md       Kartu model, batas, dan evaluasi
```

## Mulai Cepat

1. Pasang Python 3.12.
2. Buat lingkungan virtual lalu `pip install -e .`.
3. Jalankan `python -m kurasi.model` untuk contoh skor.
