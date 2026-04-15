from __future__ import annotations

import logging
from pathlib import Path

import pytest
import yaml

from .schemas.gems_schema import LibraryFile, SystemFile

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[2]
LIBRARIES_DIR = REPO_ROOT / "libraries"
RESOURCES_DIR = REPO_ROOT / "resources"


def _build_library_registry() -> dict[str, LibraryFile]:
    registry: dict[str, LibraryFile] = {}
    for lib_file in LIBRARIES_DIR.glob("*.yml"):
        with lib_file.open("r", encoding="utf-8") as f:
            raw = yaml.safe_load(f)
        registry_entry = LibraryFile.model_validate(raw)
        registry[registry_entry.library.id] = registry_entry
    return registry


def collect_system_files() -> list[Path]:
    return sorted(RESOURCES_DIR.rglob("system.yml"))


@pytest.mark.parametrize(
    "system_file",
    collect_system_files(),
    ids=lambda p: str(p.relative_to(REPO_ROOT)),
)
def test_parameter_completeness(system_file: Path) -> None:
    library_registry = _build_library_registry()

    with system_file.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    parsed = SystemFile.model_validate(raw)
    system = parsed.system

    for component in system.components:
        parts = component.model.split(".", 1)
        if len(parts) != 2:
            continue
        library_id, model_id = parts
        if library_id not in library_registry:
            continue

        lib = library_registry[library_id].library
        model_def = next((m for m in lib.models if m.id == model_id), None)
        if model_def is None:
            continue

        defined_param_ids = {p.id for p in model_def.parameters}
        for comp_param in component.parameters:
            assert comp_param.id in defined_param_ids, (
                f"{system_file}: component '{component.id}' sets parameter "
                f"'{comp_param.id}' which is not defined in model "
                f"'{component.model}'. Defined parameters: {sorted(defined_param_ids)}"
            )
