from __future__ import annotations

import logging
from pathlib import Path

import pytest

from tests.e2e_tests.env import _read_antares_version

logger = logging.getLogger(__name__)


def test_read_antares_version_parses_correctly(tmp_path: Path) -> None:
    (tmp_path / "dependencies.json").write_text(
        '{"antares_simulator_version": "9.3.2"}\n', encoding="utf-8"
    )
    assert _read_antares_version(tmp_path) == "9.3.2"


def test_read_antares_version_extra_keys_ignored(tmp_path: Path) -> None:
    (tmp_path / "dependencies.json").write_text(
        '{"antares_simulator_version": "9.4.0", "gems_language_version": "1.0.0"}\n',
        encoding="utf-8",
    )
    assert _read_antares_version(tmp_path) == "9.4.0"


def test_read_antares_version_missing_key_raises(tmp_path: Path) -> None:
    (tmp_path / "dependencies.json").write_text('{"some_other_key": "1.0"}\n', encoding="utf-8")
    with pytest.raises(ValueError, match="antares_simulator_version not found"):
        _read_antares_version(tmp_path)
