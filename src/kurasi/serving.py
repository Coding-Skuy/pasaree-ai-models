"""Kontrak serving skor kurasi v1 (PSR-AI-003).

Dipanggil HANYA oleh `pasaree-backend-service` (Rust) sebagai proses internal lewat
JSON-lines stdin/stdout. Python tidak membuka port dan tidak diekspos ke klien.
Kontrak: docs/contracts/skor-kurasi-v1.md. Perubahan bentuk = bump VERSI_KONTRAK + ADR baru.
"""
import json
import sys
from typing import TextIO

from .model import VERSI_MODEL, ProdukKurasi, skor_kurasi

VERSI_KONTRAK = "1"

_FIELD_PRODUK = {"nama": str, "harga_idr": int, "stok": int, "jumlah_foto": int, "ada_titik_serah": bool}


class KontrakError(ValueError):
    """Masukan melanggar kontrak v1."""


def _tipe_ok(nilai, tipe) -> bool:
    if tipe is int:
        return isinstance(nilai, int) and not isinstance(nilai, bool)
    return isinstance(nilai, tipe)


def validasi(req: object) -> ProdukKurasi:
    if not isinstance(req, dict):
        raise KontrakError("permintaan harus objek JSON")
    if req.get("versi_kontrak") != VERSI_KONTRAK:
        raise KontrakError(f"versi_kontrak harus '{VERSI_KONTRAK}'")
    allowed = {"versi_kontrak", "id_permintaan", "produk"}
    extra = set(req) - allowed
    if extra:
        raise KontrakError(f"field tidak dikenal: {sorted(extra)}")
    if "id_permintaan" in req and not isinstance(req["id_permintaan"], str):
        raise KontrakError("id_permintaan harus string")
    produk = req.get("produk")
    if not isinstance(produk, dict):
        raise KontrakError("produk wajib objek")
    if set(produk) != set(_FIELD_PRODUK):
        raise KontrakError(f"field produk harus tepat {sorted(_FIELD_PRODUK)}")
    for k, t in _FIELD_PRODUK.items():
        if not _tipe_ok(produk[k], t):
            raise KontrakError(f"produk.{k} harus bertipe {t.__name__}")
    return ProdukKurasi(**produk)


def skor(req: dict) -> dict:
    p = validasi(req)
    h = skor_kurasi(p)
    return {
        "versi_kontrak": VERSI_KONTRAK,
        "versi_model": VERSI_MODEL,
        "id_permintaan": req.get("id_permintaan"),
        "skor": h["skor"],
        "rekomendasi": h["rekomendasi"],
        "alasan": h["alasan"],
        "gerbang": h["gerbang"],
        "keputusan_final": "kurator_manusia",
    }


def jalankan_jsonl(masuk: TextIO, keluar: TextIO) -> None:
    """Satu permintaan JSON per baris -> satu respons JSON per baris; galat tidak menghentikan proses."""
    for baris in masuk:
        baris = baris.strip()
        if not baris:
            continue
        try:
            hasil = skor(json.loads(baris))
        except (json.JSONDecodeError, KontrakError) as e:
            hasil = {"versi_kontrak": VERSI_KONTRAK, "galat": {"kode": "kontrak_tidak_valid", "pesan": str(e)}}
        keluar.write(json.dumps(hasil, ensure_ascii=False) + "\n")
        keluar.flush()


if __name__ == "__main__":
    jalankan_jsonl(sys.stdin, sys.stdout)
