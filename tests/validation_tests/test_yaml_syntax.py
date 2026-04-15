from __future__ import annotations

import logging
from pathlib import Path

import pytest
import yaml

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[2]
SEARCH_DIRS = [REPO_ROOT / "libraries", REPO_ROOT / "resources"]


def collect_yaml_files() -> list[Path]:
    files: list[Path] = []
    for search_dir in SEARCH_DIRS:
        if search_dir.is_dir():
            for pattern in ("*.yml", "*.yaml"):
                for path in search_dir.rglob(pattern):
                    # Skip dangling symlinks (point to non-existent targets)
                    if path.is_symlink() and not path.exists():
                        logger.warning("Skipping dangling symlink: %s", path)
                        continue
                    files.append(path)
    return sorted(files)


@pytest.mark.parametrize("yaml_file", collect_yaml_files(), ids=lambda p: str(p.relative_to(REPO_ROOT)))
def test_yaml_syntax(yaml_file: Path) -> None:
    with yaml_file.open("r", encoding="utf-8") as f:
        yaml.safe_load(f)
