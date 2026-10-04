"""Stub skor kurasi aturan jelas untuk Pasaree."""
from dataclasses import dataclass


@dataclass
class ProdukKurasi:
    nama: str
    harga_idr: int
    stok: int
    jumlah_foto: int
    ada_titik_serah: bool


def skor_kurasi(p: ProdukKurasi) -> dict:
    """Kembalikan skor 0-100 beserta alasan. Aturan jelas, bukan model final."""
    skor = 100
    alasan = []
    if len(p.nama.strip()) < 8:
        skor -= 20
        alasan.append("nama terlalu pendek")
    if p.harga_idr <= 0:
        skor -= 30
        alasan.append("harga tidak valid")
    if p.stok < 0:
        skor -= 20
        alasan.append("stok tidak valid")
    if p.jumlah_foto == 0:
        skor -= 20
        alasan.append("tanpa foto")
    if not p.ada_titik_serah:
        skor -= 30
        alasan.append("titik serah kosong")
    return {"skor": max(skor, 0), "alasan": alasan, "rekomendasi": "tayang" if max(skor, 0) >= 70 else "tinjau kurator"}


if __name__ == "__main__":
    contoh = ProdukKurasi(nama="Sambal Bawang 250g", harga_idr=25000, stok=40, jumlah_foto=3, ada_titik_serah=True)
    print(skor_kurasi(contoh))
