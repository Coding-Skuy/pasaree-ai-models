"""Gerbang QA rilis (PSR-AI-003): keluar kode 1 (rilis diblokir) bila syarat tak terpenuhi.

Syarat: evaluasi lulus ambang; eval/metrics.md sinkron; docs/MODEL_CARD.md memuat nomor versi model.
Pakai: `python -m kurasi.gate [akar-repo]`.
"""
import sys
from pathlib import Path

from .eval import evaluasi, render_metrics
from .model import VERSI_MODEL


def cek_rilis(akar: Path) -> list[str]:
    masalah: list[str] = []
    h = evaluasi()
    if not h["lulus"]:
        masalah.append(
            f"evaluasi di bawah ambang (penuh min={h['penuh']['skor_min']}, "
            f"tanpa foto maks={h['tanpa_foto']['skor_maks']}, tanpa titik serah maks={h['tanpa_titik_serah']['skor_maks']})"
        )
    metrics = akar / "eval" / "metrics.md"
    if not metrics.exists() or metrics.read_text(encoding="utf-8") != render_metrics(h):
        masalah.append("eval/metrics.md hilang atau usang; jalankan `python -m kurasi.eval`")
    kartu = akar / "docs" / "MODEL_CARD.md"
    if not kartu.exists() or f"`{VERSI_MODEL}`" not in kartu.read_text(encoding="utf-8"):
        masalah.append(f"docs/MODEL_CARD.md tidak memuat versi model `{VERSI_MODEL}`")
    return masalah


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    akar = Path(argv[0]) if argv else Path(__file__).resolve().parents[2]
    masalah = cek_rilis(akar)
    for m in masalah:
        print(f"GERBANG GAGAL: {m}", file=sys.stderr)
    print("Gerbang QA: " + ("LULUS" if not masalah else "RILIS DIBLOKIR"))
    return 1 if masalah else 0


if __name__ == "__main__":
    raise SystemExit(main())
