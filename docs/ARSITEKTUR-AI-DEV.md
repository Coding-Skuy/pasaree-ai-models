# Arsitektur AI-dev pasaree-ai-models

Dokumen tambahan untuk `versions/v1.0.0/docs/40-TECHSTACK.md` dan `60-BLAST-RADIUS.md` (kedua file itu beku v1.0.0 dan hanya berisi ringkasan; jangan ditimpa). Rujukan versi: [Pasaree-TownHall v1.0.0](https://github.com/Coding-Skuy/Pasaree-TownHall/blob/main/platform/versions/v1.0.0/CHANGELOG.md).

## Matriks stack dan fitur

| Aspek | Terkunci | Catatan |
|---|---|---|
| Training | Python >=3.12 | `pyproject.toml` |
| Serving | lewat API Rust (`pasaree-backend-service`) | Python tidak diekspos langsung ke klien |
| Dokumentasi | model card + metrik eval + nomor versi model | wajib per rilis |
| Evaluasi | `eval/metrics.md` | rilis diblokir bila di bawah ambang |

Larangan: serving model langsung ke klien; menilai rasa/keamanan pangan/keaslian merek; data di luar katalog dan lapak.

| Masukan | Sumber | Keluaran |
|---|---|---|
| nama, harga IDR integer, stok, jumlah foto, status titik serah | DB `pasaree` via backend | skor 0-100 + rekomendasi `tayang` atau `tinjau kurator` |

## Blast radius

Batas context repo (townhall-roadmap §2: komisi 8% transparan, escrow T+1; katalog jujur; fulfillment wajib via trip Lumbung).

Boleh disentuh:

- Kode training/evaluasi, model card, artefak model berversi.
- Membaca data katalog/lapak yang diberikan backend Pasaree.

Dilarang:

- DB divisi lain; data armada/gudang/kas.
- Mengambil keputusan tayang/takedown otomatis.
- Menilai higiene dapur (jalur Pawonee/Pedaree).

Kontrak dikonsumsi:

- Data katalog/lapak dari `pasaree-backend-service`.

Kontrak diproduksi:

- Skor kurasi melalui API serving Rust (kontrak berversi).

Catatan: Pasaree tidak mengonsumsi modul `:shared:pantry-resep` (milik Pawonee). Failure utama: kontrak berubah tanpa update SRS, test tidak mengikuti acceptance criteria, rollback tidak siap. Rollback: revert commit repo ini dan kembali ke kontrak Pasaree-TownHall v1.0.0.
