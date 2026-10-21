# Kartu Model Kurasi Pasaree

## Versi model

Nomor versi model saat ini: `0.2.0` (konstanta `VERSI_MODEL` di `src/kurasi/model.py`; wajib sama dengan `pyproject.toml`). Versi kontrak serving: `1` (lihat [kontrak](contracts/skor-kurasi-v1.md)). Setiap perubahan aturan/bobot menaikkan versi model, memperbarui `eval/metrics.md`, dan menambah baris CHANGELOG. Jenis model: aturan jelas berbobot (tanpa pelatihan statistik).

## Tujuan

Membantu kurator manusia menilai kelengkapan data lapak dan produk sebelum tayang (piagam kurasi §3-§4). Skor hanya bantu; tidak mengambil keputusan tayang atau takedown.

## Masukan

nama (judul produk), harga IDR integer, stok, jumlah foto, status titik serah (boolean). Data berasal dari katalog/lapak yang diberikan `pasaree-backend-service`; tidak ada data armada, gudang, atau kas.

## Keluaran

Skor 0-100, daftar `alasan`, daftar `gerbang` yang gagal, dan rekomendasi `tayang` (skor >= 70) atau `tinjau kurator`. Keputusan akhir selalu kurator manusia (piagam kurasi §6); respons serving membawa `keputusan_final: "kurator_manusia"`.

## Aturan skor

| Aspek | Bobot | Aturan |
|---|---|---|
| Judul | 12 + 8 | panjang 10-80; memuat berat/isi (mis. `150 g`) |
| Harga | 15 + 10 | integer IDR > 0; kelipatan Rp500 |
| Stok | 15 | > 0 (stok 0 otomatis non-tayang) |
| Foto | 20 | 1-6 foto (lebih dari 6 setengah bobot) |
| Titik serah | 20 | terisi |

Gerbang wajib: foto, titik serah, harga valid, stok > 0. Bila ada yang gagal, skor dibatasi 65 sehingga rekomendasi selalu `tinjau kurator`.

## Batas

- Tidak menilai rasa, keamanan pangan, higiene dapur, izin PIRT/BPOM, alergen, tanggal kedaluwarsa, atau keaslian merek/foto.
- Tidak memeriksa kewajaran harga pasar; hanya format harga.
- Asumsi (dokumen v1.0.0 masih templat): bobot angka, ambang 70, dan plafon gerbang 65 adalah pilihan tim AI, belum disahkan Dewan Kurasi. Sumber aturan: `lapak/00-piagam-kurasi.md` dan `katalog/10-model-data.md` di Pasaree-TownHall.
- Python tidak diekspos langsung ke klien; serving lewat API Rust.

## Metrik evaluasi

Rincian di [`eval/metrics.md`](../eval/metrics.md) (data sintetis 20 contoh, bukan data lapak nyata). Ringkas: 20 contoh terisi penuh skor 100 (semua tayang); tanpa foto dan tanpa titik serah skor 65 (di bawah 70). Ambang: penuh >= 70, tanpa foto/titik serah < 70.

## Gerbang rilis (QA gate)

`python -m kurasi.gate` keluar dengan kode 1 (rilis diblokir) bila evaluasi di bawah ambang, `eval/metrics.md` usang, atau kartu ini tidak memuat nomor versi model.
