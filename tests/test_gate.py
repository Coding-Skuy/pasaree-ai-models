"""Uji gerbang QA rilis (PSR-AI-003): rilis diblokir bila evaluasi di bawah ambang."""
import re
from pathlib import Path

import kurasi.eval as ev
from kurasi.gate import cek_rilis, main
from kurasi.model import VERSI_MODEL

ROOT = Path(__file__).resolve().parent.parent


def test_gate_lulus_pada_kondisi_sekarang():
    assert cek_rilis(ROOT) == []
    assert main([str(ROOT)]) == 0


def test_gate_memblokir_bila_evaluasi_gagal(monkeypatch):
    asli = ev.evaluasi

    def buruk():
        h = asli()
        h["penuh"] = dict(h["penuh"], skor_min=69)
        h["lulus"] = False
        return h

    monkeypatch.setattr("kurasi.gate.evaluasi", buruk)
    masalah = cek_rilis(ROOT)
    assert masalah and any("evaluasi" in m for m in masalah)
    assert main([str(ROOT)]) == 1


def test_gate_memblokir_bila_model_card_tanpa_versi(tmp_path):
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "MODEL_CARD.md").write_text("# kosong\n", encoding="utf-8")
    (tmp_path / "eval").mkdir()
    (tmp_path / "eval" / "metrics.md").write_text(ev.render_metrics(ev.evaluasi()), encoding="utf-8")
    assert any("versi model" in m for m in cek_rilis(tmp_path))


def test_gate_memblokir_bila_metrics_md_usang(tmp_path):
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "MODEL_CARD.md").write_text(f"Versi model: {VERSI_MODEL}\n", encoding="utf-8")
    (tmp_path / "eval").mkdir()
    (tmp_path / "eval" / "metrics.md").write_text("usang\n", encoding="utf-8")
    assert any("metrics.md" in m for m in cek_rilis(tmp_path))


def test_model_card_memuat_bagian_wajib_dan_versi_cocok():
    teks = (ROOT / "docs" / "MODEL_CARD.md").read_text(encoding="utf-8")
    for judul in ("Tujuan", "Masukan", "Keluaran", "Batas", "Metrik evaluasi", "Versi model"):
        assert re.search(rf"^##\s+{judul}", teks, re.M), judul
    assert f"`{VERSI_MODEL}`" in teks
    assert "kurator manusia" in teks


def test_versi_pyproject_sama_dengan_versi_model():
    assert f'version = "{VERSI_MODEL}"' in (ROOT / "pyproject.toml").read_text(encoding="utf-8")
