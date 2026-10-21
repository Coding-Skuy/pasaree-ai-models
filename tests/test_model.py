"""Uji skor bantu kurasi (PSR-AI-002). Aturan dari piagam kurasi §4 (asumsi dicatat di MODEL_CARD)."""
import dataclasses

import pytest

from kurasi.model import BATAS_TAYANG, ProdukKurasi, skor_kurasi

PENUH = ProdukKurasi(nama="Sambal Bawang Mbok D 150 g", harga_idr=25000, stok=40, jumlah_foto=3, ada_titik_serah=True)


def ubah(**kw):
    return dataclasses.replace(PENUH, **kw)


def test_lapak_penuh_tayang_skor_100():
    h = skor_kurasi(PENUH)
    assert h["skor"] == 100
    assert h["rekomendasi"] == "tayang"
    assert h["alasan"] == []
    assert h["gerbang"] == []


def test_tanpa_foto_di_bawah_ambang():
    h = skor_kurasi(ubah(jumlah_foto=0))
    assert h["skor"] < BATAS_TAYANG
    assert h["rekomendasi"] == "tinjau kurator"
    assert "tanpa foto" in h["alasan"]


def test_tanpa_titik_serah_di_bawah_ambang():
    h = skor_kurasi(ubah(ada_titik_serah=False))
    assert h["skor"] < BATAS_TAYANG
    assert h["rekomendasi"] == "tinjau kurator"


@pytest.mark.parametrize("kw", [{"harga_idr": 0}, {"harga_idr": -500}, {"stok": 0}, {"stok": -1}])
def test_harga_atau_stok_tidak_layak_tidak_tayang(kw):
    assert skor_kurasi(ubah(**kw))["rekomendasi"] == "tinjau kurator"


def test_harga_bukan_kelipatan_500_mengurangi_tapi_masih_tayang():
    h = skor_kurasi(ubah(harga_idr=25100))
    assert h["skor"] == 90
    assert h["rekomendasi"] == "tayang"


def test_harga_float_ditolak_sebagai_tidak_valid():
    assert skor_kurasi(ubah(harga_idr=25000.5))["rekomendasi"] == "tinjau kurator"
    assert skor_kurasi(ubah(harga_idr=True))["rekomendasi"] == "tinjau kurator"


def test_judul_tanpa_berat_isi_dan_terlalu_pendek():
    assert skor_kurasi(ubah(nama="Sambal Bawang Enak"))["skor"] == 92
    assert skor_kurasi(ubah(nama="Sambal"))["skor"] == 80


def test_foto_melebihi_6_dikurangi():
    assert skor_kurasi(ubah(jumlah_foto=7))["skor"] == 90


def test_skor_selalu_0_sampai_100():
    h = skor_kurasi(ProdukKurasi(nama="", harga_idr=-1, stok=-1, jumlah_foto=0, ada_titik_serah=False))
    assert 0 <= h["skor"] <= 100


def test_deterministik():
    assert skor_kurasi(PENUH) == skor_kurasi(PENUH)
