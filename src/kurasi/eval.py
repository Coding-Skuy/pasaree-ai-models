"""Evaluasi skor bantu kurasi (PSR-AI-002). Menulis `eval/metrics.md`.

Data contoh SINTETIS (asumsi: belum ada data lapak nyata; tidak ada data keluar repo).
Jalankan: `python -m kurasi.eval` untuk menulis ulang eval/metrics.md.
"""
import dataclasses
from pathlib import Path

from .model import BATAS_TAYANG, VERSI_MODEL, ProdukKurasi, skor_kurasi

AMBANG_PENUH_MIN = BATAS_TAYANG  # 20 contoh penuh harus skor >= 70
AMBANG_KURANG_MAKS = BATAS_TAYANG  # tanpa foto / tanpa titik serah harus skor < 70

_PRODUK = [
    ("Sambal Bawang Mbok D", 150, "g", 25000),
    ("Keripik Tempe Renyah", 200, "g", 18500),
    ("Madu Hutan Asli", 250, "ml", 65000),
    ("Teh Rosela Kering", 100, "g", 22000),
    ("Bumbu Rendang Instan", 120, "g", 15000),
    ("Kopi Arabika Giling", 250, "g", 55000),
    ("Abon Sapi Gurih", 100, "g", 48000),
    ("Dodol Garut Original", 300, "g", 30000),
    ("Rempeyek Kacang", 250, "g", 20000),
    ("Sirup Jahe Merah", 500, "ml", 35000),
    ("Gula Aren Cetak", 500, "g", 28000),
    ("Kerupuk Udang Mentah", 500, "g", 42000),
    ("Bawang Goreng Renyah", 150, "g", 17000),
    ("Telur Asin Brebes", 6, "pcs", 24000),
    ("Paket Hampers Lebaran", 1, "paket", 150000),
    ("Minyak Kelapa Murni", 250, "ml", 38000),
    ("Sagu Mutiara Putih", 400, "g", 12500),
    ("Cabai Rawit Segar", 250, "g", 14000),
    ("Tahu Bakso Beku", 10, "pcs", 32000),
    ("Kecap Manis Rumahan", 600, "ml", 26000),
]


def contoh_lapak_penuh() -> list[ProdukKurasi]:
    """20 contoh produk terisi penuh (judul + berat/isi, harga kelipatan 500, stok, foto, titik serah)."""
    hasil = []
    for i, (nama, jumlah, satuan, harga) in enumerate(_PRODUK):
        hasil.append(ProdukKurasi(
            nama=f"{nama} {jumlah} {satuan}",
            harga_idr=harga,
            stok=10 + i * 3,
            jumlah_foto=1 + (i % 6),
            ada_titik_serah=True,
        ))
    return hasil


def _ringkas(skor: list[int], rekom: list[str]) -> dict:
    return {
        "jumlah": len(skor),
        "skor_min": min(skor),
        "skor_maks": max(skor),
        "skor_rata": round(sum(skor) / len(skor), 1),
        "tayang": sum(1 for r in rekom if r == "tayang"),
    }


def _hitung(items: list[ProdukKurasi]) -> dict:
    hasil = [skor_kurasi(p) for p in items]
    return _ringkas([h["skor"] for h in hasil], [h["rekomendasi"] for h in hasil])


def evaluasi() -> dict:
    penuh = contoh_lapak_penuh()
    r_penuh = _hitung(penuh)
    r_foto = _hitung([dataclasses.replace(p, jumlah_foto=0) for p in penuh])
    r_serah = _hitung([dataclasses.replace(p, ada_titik_serah=False) for p in penuh])
    lulus = (
        r_penuh["jumlah"] == 20
        and r_penuh["skor_min"] >= AMBANG_PENUH_MIN
        and r_foto["skor_maks"] < AMBANG_KURANG_MAKS
        and r_serah["skor_maks"] < AMBANG_KURANG_MAKS
    )
    return {"versi_model": VERSI_MODEL, "penuh": r_penuh, "tanpa_foto": r_foto, "tanpa_titik_serah": r_serah, "lulus": lulus}


def render_metrics(h: dict) -> str:
    def baris(nama, k, syarat):
        return f"| {nama} | {k['jumlah']} | {k['skor_min']} | {k['skor_maks']} | {k['skor_rata']} | {k['tayang']} | {syarat} |"

    return "\n".join([
        "# Metrik Evaluasi Skor Bantu Kurasi",
        "",
        f"Versi model: {h['versi_model']}. Dibuat oleh `python -m kurasi.eval`; jangan sunting manual.",
        "Data: 20 contoh produk SINTETIS (asumsi; bukan data lapak nyata). Sumber aturan: piagam kurasi §3-§4.",
        "",
        "| Kelompok | Jumlah | Skor min | Skor maks | Skor rata | Rekomendasi tayang | Syarat |",
        "|---|---|---|---|---|---|---|",
        baris("Terisi penuh", h["penuh"], f"semua skor >= {AMBANG_PENUH_MIN}"),
        baris("Tanpa foto", h["tanpa_foto"], f"semua skor < {AMBANG_KURANG_MAKS}"),
        baris("Tanpa titik serah", h["tanpa_titik_serah"], f"semua skor < {AMBANG_KURANG_MAKS}"),
        "",
        f"Hasil gerbang QA: {'LULUS' if h['lulus'] else 'GAGAL'}.",
        "",
        "Catatan: skor hanya membantu. Keputusan tayang tetap kurator manusia.",
        "",
    ])


def tulis_metrics(path: Path | None = None) -> Path:
    path = path or Path(__file__).resolve().parents[2] / "eval" / "metrics.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_metrics(evaluasi()), encoding="utf-8")
    return path


if __name__ == "__main__":
    print(f"Menulis {tulis_metrics()}")
