# Kontrak serving skor kurasi, versi 1

Status: USULAN untuk disepakati dengan `pasaree-backend-service` (belum ada endpoint skor di `docs/api/openapi.yaml` backend). Implementasi: `src/kurasi/serving.py`. Keputusan: [ADR-0002](../decisions/ADR-0002-kontrak-serving-berversi.md).

## Pola pemanggilan

Backend Rust menjalankan `python -m kurasi.serving` sebagai proses internal (worker) dan bicara JSON-lines lewat stdin/stdout: satu permintaan per baris, satu respons per baris. Tidak ada port jaringan. Klien (web/app) tidak pernah memanggil Python; mereka hanya memakai API Rust (bila backend memilih menampilkannya, itu endpoint backend dengan JWT audiens `pasaree`).

## Permintaan

```json
{"versi_kontrak": "1", "id_permintaan": "01J...", "produk": {"nama": "Sambal Bawang Mbok D 150 g", "harga_idr": 25000, "stok": 40, "jumlah_foto": 3, "ada_titik_serah": true}}
```

- `versi_kontrak` wajib `"1"`. `id_permintaan` opsional (string, dikembalikan apa adanya untuk korelasi).
- `produk` memuat tepat lima field; tipe ketat (`harga_idr`, `stok`, `jumlah_foto` integer, bukan float/boolean/string). Field lain ditolak.
- Uang integer IDR tanpa sen. Tidak ada PII, ID pengguna, atau data kas.

## Respons

```json
{"versi_kontrak": "1", "versi_model": "0.2.0", "id_permintaan": "01J...", "skor": 100, "rekomendasi": "tayang", "alasan": [], "gerbang": [], "keputusan_final": "kurator_manusia"}
```

- `rekomendasi`: `tayang` | `tinjau kurator`. `gerbang`: subset `harga|stok|foto|titik_serah`.
- `keputusan_final` selalu `kurator_manusia`; backend tidak boleh tayang/takedown otomatis hanya dari skor.

## Galat

Masukan tidak valid menghasilkan satu baris `{"versi_kontrak": "1", "galat": {"kode": "kontrak_tidak_valid", "pesan": "..."}}`; proses tetap hidup. Backend memetakan ke `422` bila perlu.

## Versi

Perubahan kompatibel mundur (menambah field respons) tetap versi `1`; penambahan field masukan wajib, perubahan tipe/arti, atau penghapusan field menaikkan `versi_kontrak` (ADR baru + pembaruan SRS). Backend harus memeriksa `versi_kontrak` dan `versi_model` pada respons dan menyimpannya bersama keputusan kurasi untuk jejak audit.
