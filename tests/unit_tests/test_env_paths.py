from __future__ import annotations

import logging
from pathlib import Path

import pytest

from tests.e2e_tests.env import _read_antares_version

logger = logging.getLogger(__name__)


def test_read_antares_version_parses_correctly(tmp_path: Path) -> None:
    versions_dir = tmp_path / "versions"
    versions_dir.mkdir()
    (versions_dir / "antares-simulator.txt").write_text(
        "ANTARES_SIMULATOR_VERSION=9.3.2\n", encoding="utf-8"
    )
    assert _read_antares_version(tmp_path) == "9.3.2"


def test_read_antares_version_ignores_comments(tmp_path: Path) -> None:
    versions_dir = tmp_path / "versions"
    versions_dir.mkdir()
    (versions_dir / "antares-simulator.txt").write_text(
        "# This is a comment\nANTARES_SIMULATOR_VERSION=9.4.0\n", encoding="utf-8"
    )
    assert _read_antares_version(tmp_path) == "9.4.0"


def test_read_antares_version_missing_key_raises(tmp_path: Path) -> None:
    versions_dir = tmp_path / "versions"
    versions_dir.mkdir()
    (versions_dir / "antares-simulator.txt").write_text(
        "SOME_OTHER_KEY=1.0\n", encoding="utf-8"
    )
    with pytest.raises(ValueError, match="ANTARES_SIMULATOR_VERSION not found"):
        _read_antares_version(tmp_path)


def test_read_antares_version_strips_whitespace(tmp_path: Path) -> None:
    versions_dir = tmp_path / "versions"
    versions_dir.mkdir()
    (versions_dir / "antares-simulator.txt").write_text(
        "ANTARES_SIMULATOR_VERSION=  9.3.2  \n", encoding="utf-8"
    )
    assert _read_antares_version(tmp_path) == "9.3.2"
