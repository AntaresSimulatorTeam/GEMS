from __future__ import annotations

import logging
from pathlib import Path

import pytest
import yaml

from .schemas.gems_schema import LibraryFile

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[2]
LIBRARIES_DIR = REPO_ROOT / "libraries"


def collect_library_files() -> list[Path]:
    return sorted(LIBRARIES_DIR.glob("*.yml"))


@pytest.mark.parametrize("lib_file", collect_library_files(), ids=lambda p: p.name)
def test_port_type_consistency(lib_file: Path) -> None:
    with lib_file.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    parsed = LibraryFile.model_validate(raw)
    lib = parsed.library

    defined_port_type_ids = {pt.id for pt in lib.port_types}

    for model in lib.models:
        for port in model.ports:
            assert port.type in defined_port_type_ids, (
                f"{lib_file.name}: model '{model.id}' port '{port.id}' "
                f"references undefined port-type '{port.type}'. "
                f"Defined port-types: {sorted(defined_port_type_ids)}"
            )
