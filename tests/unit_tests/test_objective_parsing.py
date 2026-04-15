from __future__ import annotations

import logging
from pathlib import Path

import pytest

from tests.e2e_tests.utils import get_gems_objective_function_value

logger = logging.getLogger(__name__)


def _write_tmp_csv(tmp_path: Path, content: str, filename: str = "result.csv") -> Path:
    p = tmp_path / filename
    p.write_text(content, encoding="utf-8")
    return p


def _write_tmp_tsv(tmp_path: Path, content: str, filename: str = "result.tsv") -> Path:
    p = tmp_path / filename
    p.write_text(content, encoding="utf-8")
    return p


def test_csv_objective_extraction(tmp_path: Path) -> None:
    csv = _write_tmp_csv(
        tmp_path,
        "output,value\nOBJECTIVE_VALUE,12345.67\nSOME_OTHER,999\n",
    )
    assert get_gems_objective_function_value(csv) == pytest.approx(12345.67)


def test_tsv_objective_extraction(tmp_path: Path) -> None:
    tsv = _write_tmp_tsv(
        tmp_path,
        "output\tvalue\nOBJECTIVE_VALUE\t7990.0\nSOME_OTHER\t0\n",
    )
    assert get_gems_objective_function_value(tsv) == pytest.approx(7990.0)


def test_csv_objective_zero(tmp_path: Path) -> None:
    csv = _write_tmp_csv(tmp_path, "output,value\nOBJECTIVE_VALUE,0.0\n")
    assert get_gems_objective_function_value(csv) == pytest.approx(0.0)


def test_csv_objective_negative(tmp_path: Path) -> None:
    csv = _write_tmp_csv(tmp_path, "output,value\nOBJECTIVE_VALUE,-500.0\n")
    assert get_gems_objective_function_value(csv) == pytest.approx(-500.0)


def test_unsupported_extension_raises(tmp_path: Path) -> None:
    bad = tmp_path / "result.txt"
    bad.write_text("output,value\nOBJECTIVE_VALUE,1.0\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid file format"):
        get_gems_objective_function_value(bad)
