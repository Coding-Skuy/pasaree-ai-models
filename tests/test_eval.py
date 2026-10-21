"""Uji evaluasi (PSR-AI-002): kriteria penerimaan dari issue dan ADR-0001 butir 2."""
from pathlib import Path

from kurasi.eval import AMBANG_PENUH_MIN, contoh_lapak_penuh, evaluasi, render_metrics
from kurasi.model import BATAS_TAYANG

METRICS = Path(__file__).resolve().parent.parent / "eval" / "metrics.md"


def test_ada_20_contoh_penuh_dan_semua_minimal_70():
    contoh = contoh_lapak_penuh()
    assert len(contoh) == 20
    h = evaluasi()
    assert h["penuh"]["jumlah"] == 20
    assert h["penuh"]["skor_min"] >= AMBANG_PENUH_MIN == BATAS_TAYANG
    assert h["penuh"]["tayang"] == 20


def test_tanpa_foto_atau_titik_serah_selalu_di_bawah_70():
    h = evaluasi()
    assert h["tanpa_foto"]["skor_maks"] < BATAS_TAYANG
    assert h["tanpa_titik_serah"]["skor_maks"] < BATAS_TAYANG
    assert h["tanpa_foto"]["jumlah"] == h["tanpa_titik_serah"]["jumlah"] == 20


def test_evaluasi_lulus():
    assert evaluasi()["lulus"] is True


def test_metrics_md_sinkron_dengan_evaluasi():
    assert METRICS.read_text(encoding="utf-8") == render_metrics(evaluasi())
