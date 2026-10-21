"""Skor bantu kurasi aturan jelas untuk Pasaree (PSR-AI-002).

Skor hanya membantu kurator manusia. Keputusan tayang/takedown tetap kurator
(piagam kurasi §6). Model tidak menilai rasa, keamanan pangan, atau keaslian merek.
"""
import re
from dataclasses import dataclass

VERSI_MODEL = "0.2.0"
BATAS_TAYANG = 70
# Batas skor bila ada gerbang wajib yang gagal; harus < BATAS_TAYANG.
PLAFON_GERBANG = 65

# Bobot (jumlah = 100).
_BOBOT_JUDUL_PANJANG = 12
_BOBOT_JUDUL_BERAT = 8
_BOBOT_HARGA_VALID = 15
_BOBOT_HARGA_KELIPATAN = 10
_BOBOT_STOK = 15
_BOBOT_FOTO = 20
_BOBOT_TITIK_SERAH = 20

_POLA_BERAT_ISI = re.compile(r"\d+\s*(kg|g|gr|ml|l|pcs|paket)\b", re.IGNORECASE)


@dataclass
class ProdukKurasi:
    nama: str
    harga_idr: int
    stok: int
    jumlah_foto: int
    ada_titik_serah: bool


def _int_murni(x) -> bool:
    return isinstance(x, int) and not isinstance(x, bool)


def skor_kurasi(p: ProdukKurasi) -> dict:
    """Kembalikan skor 0-100, alasan, gerbang yang gagal, dan rekomendasi.

    Aturan (piagam kurasi §4): judul 10-80 karakter memuat berat/isi; harga IDR
    integer > 0 kelipatan Rp500; stok > 0 (stok 0 otomatis non-tayang); 1-6 foto;
    titik serah terisi. Gerbang wajib (foto, titik serah, harga valid, stok > 0)
    membatasi skor di bawah ambang sehingga produk tak lolos hanya karena aspek lain penuh.
    """
    skor = 0
    alasan: list[str] = []
    gerbang: list[str] = []

    nama = (p.nama or "").strip()
    if 10 <= len(nama) <= 80:
        skor += _BOBOT_JUDUL_PANJANG
    else:
        alasan.append("judul harus 10-80 karakter")
    if _POLA_BERAT_ISI.search(nama):
        skor += _BOBOT_JUDUL_BERAT
    else:
        alasan.append("judul belum memuat berat/isi")

    if _int_murni(p.harga_idr) and p.harga_idr > 0:
        skor += _BOBOT_HARGA_VALID
        if p.harga_idr % 500 == 0:
            skor += _BOBOT_HARGA_KELIPATAN
        else:
            alasan.append("harga bukan kelipatan Rp500")
    else:
        alasan.append("harga tidak valid")
        gerbang.append("harga")

    if _int_murni(p.stok) and p.stok > 0:
        skor += _BOBOT_STOK
    else:
        alasan.append("stok kosong atau tidak valid")
        gerbang.append("stok")

    if not _int_murni(p.jumlah_foto) or p.jumlah_foto <= 0:
        alasan.append("tanpa foto")
        gerbang.append("foto")
    elif p.jumlah_foto <= 6:
        skor += _BOBOT_FOTO
    else:
        skor += _BOBOT_FOTO // 2
        alasan.append("foto melebihi 6")

    if p.ada_titik_serah is True:
        skor += _BOBOT_TITIK_SERAH
    else:
        alasan.append("titik serah kosong")
        gerbang.append("titik_serah")

    if gerbang:
        skor = min(skor, PLAFON_GERBANG)
    skor = max(0, min(100, skor))
    return {
        "skor": skor,
        "alasan": alasan,
        "gerbang": gerbang,
        "rekomendasi": "tayang" if skor >= BATAS_TAYANG else "tinjau kurator",
    }


if __name__ == "__main__":
    contoh = ProdukKurasi(nama="Sambal Bawang 250g", harga_idr=25000, stok=40, jumlah_foto=3, ada_titik_serah=True)
    print(skor_kurasi(contoh))
