from __future__ import annotations

import logging
from pathlib import Path

import pytest

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[2]
LIBRARIES_DIR = REPO_ROOT / "libraries"
VERSIONS_DIR = REPO_ROOT / "versions"


def collect_library_files() -> list[Path]:
    return sorted(LIBRARIES_DIR.glob("*.yml"))


@pytest.mark.parametrize("lib_file", collect_library_files(), ids=lambda p: p.name)
def test_library_has_version_file(lib_file: Path) -> None:
    version_file = VERSIONS_DIR / f"{lib_file.stem}.txt"
    assert version_file.is_file(), (
        f"Missing version file for library '{lib_file.name}': "
        f"expected '{version_file.relative_to(REPO_ROOT)}'"
    )
    content = version_file.read_text(encoding="utf-8").strip()
    assert content, f"Version file '{version_file.relative_to(REPO_ROOT)}' is empty"


@pytest.mark.parametrize("lib_file", collect_library_files(), ids=lambda p: p.name)
def test_library_has_changelog(lib_file: Path) -> None:
    changelog = LIBRARIES_DIR / f"CHANGELOG-{lib_file.stem}.md"
    assert changelog.is_file(), (
        f"Missing changelog for library '{lib_file.name}': "
        f"expected '{changelog.relative_to(REPO_ROOT)}'"
    )
    content = changelog.read_text(encoding="utf-8").strip()
    assert content, f"Changelog '{changelog.relative_to(REPO_ROOT)}' is empty"
