from __future__ import annotations

import logging
from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from .schemas.gems_schema import LibraryFile

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[2]
LIBRARIES_DIR = REPO_ROOT / "libraries"


def collect_library_files() -> list[Path]:
    return sorted(LIBRARIES_DIR.glob("*.yml"))


@pytest.mark.parametrize("lib_file", collect_library_files(), ids=lambda p: p.name)
def test_library_schema(lib_file: Path) -> None:
    with lib_file.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    try:
        parsed = LibraryFile.model_validate(raw)
    except ValidationError as exc:
        pytest.fail(f"Schema validation failed for {lib_file.name}:\n{exc}")

    lib = parsed.library
    assert lib.id, f"{lib_file.name}: library.id is empty"

    for model in lib.models:
        assert model.id, f"{lib_file.name}: a model is missing its id"

    for pt in lib.port_types:
        assert pt.id, f"{lib_file.name}: a port-type is missing its id"
