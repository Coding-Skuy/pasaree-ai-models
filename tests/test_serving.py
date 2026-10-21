"""Uji kontrak serving skor kurasi v1 (PSR-AI-003)."""
import io
import json

import pytest

from kurasi.model import VERSI_MODEL
from kurasi.serving import KontrakError, VERSI_KONTRAK, jalankan_jsonl, skor

PRODUK = {"nama": "Sambal Bawang Mbok D 150 g", "harga_idr": 25000, "stok": 40, "jumlah_foto": 3, "ada_titik_serah": True}


def req(**kw):
    p = dict(PRODUK)
    p.update(kw)
    return {"versi_kontrak": VERSI_KONTRAK, "id_permintaan": "01JABC", "produk": p}


def test_respons_memuat_versi_dan_keputusan_manusia():
    r = skor(req())
    assert r["versi_kontrak"] == VERSI_KONTRAK == "1"
    assert r["versi_model"] == VERSI_MODEL
    assert r["id_permintaan"] == "01JABC"
    assert r["skor"] == 100 and r["rekomendasi"] == "tayang"
    assert r["keputusan_final"] == "kurator_manusia"
    assert set(r) == {"versi_kontrak", "versi_model", "id_permintaan", "skor", "rekomendasi", "alasan", "gerbang", "keputusan_final"}


def test_tanpa_foto_tinjau_kurator():
    assert skor(req(jumlah_foto=0))["rekomendasi"] == "tinjau kurator"


@pytest.mark.parametrize("mutasi", [
    lambda r: r.update(versi_kontrak="2"),
    lambda r: r.pop("produk"),
    lambda r: r["produk"].pop("stok"),
    lambda r: r["produk"].update(harga_idr=25000.5),
    lambda r: r["produk"].update(harga_idr="25000"),
    lambda r: r["produk"].update(ada_titik_serah="ya"),
    lambda r: r["produk"].update(nama=123),
    lambda r: r["produk"].update(ekstra="x"),
    lambda r: r.update(id_permintaan=5),
])
def test_masukan_tidak_valid_ditolak(mutasi):
    r = req()
    mutasi(r)
    with pytest.raises(KontrakError):
        skor(r)


def test_jsonl_satu_respons_per_baris_dan_galat_tidak_menghentikan():
    masuk = io.StringIO(json.dumps(req()) + "\nbukan json\n" + json.dumps(req(jumlah_foto=0)) + "\n")
    keluar = io.StringIO()
    jalankan_jsonl(masuk, keluar)
    baris = [json.loads(x) for x in keluar.getvalue().splitlines()]
    assert len(baris) == 3
    assert baris[0]["skor"] == 100
    assert baris[1]["galat"]["kode"] == "kontrak_tidak_valid"
    assert baris[2]["rekomendasi"] == "tinjau kurator"


def test_tidak_ada_pendengar_jaringan():
    import kurasi.serving as s
    sumber = open(s.__file__, encoding="utf-8").read()
    for kata in ("import socket", "http.server", "import requests", "urllib.request"):
        assert kata not in sumber
