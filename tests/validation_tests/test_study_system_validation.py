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
        parsed = LibraryFile.model_validate(raw)
        registry[parsed.library.id] = parsed
    return registry


def collect_system_files() -> list[Path]:
    return sorted(RESOURCES_DIR.rglob("system.yml"))


@pytest.mark.parametrize(
    "system_file",
    collect_system_files(),
    ids=lambda p: str(p.relative_to(REPO_ROOT)),
)
def test_component_model_references(system_file: Path) -> None:
    library_registry = _build_library_registry()

    with system_file.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    parsed = SystemFile.model_validate(raw)
    system = parsed.system

    for component in system.components:
        parts = component.model.split(".", 1)
        assert len(parts) == 2, (
            f"{system_file}: component '{component.id}' model '{component.model}' "
            "must be in format 'library_id.model_id'"
        )
        library_id, model_id = parts
        assert library_id in library_registry, (
            f"{system_file}: component '{component.id}' references unknown library "
            f"'{library_id}'. Known libraries: {sorted(library_registry)}"
        )
        lib = library_registry[library_id].library
        model_ids = {m.id for m in lib.models}
        assert model_id in model_ids, (
            f"{system_file}: component '{component.id}' references unknown model "
            f"'{model_id}' in library '{library_id}'. Known models: {sorted(model_ids)}"
        )


@pytest.mark.parametrize(
    "system_file",
    collect_system_files(),
    ids=lambda p: str(p.relative_to(REPO_ROOT)),
)
def test_connection_component_references(system_file: Path) -> None:
    with system_file.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    parsed = SystemFile.model_validate(raw)
    system = parsed.system

    component_ids = {c.id for c in system.components}

    for conn in system.connections:
        assert conn.component1 in component_ids, (
            f"{system_file}: connection references unknown component1 '{conn.component1}'. "
            f"Known components: {sorted(component_ids)}"
        )
        assert conn.component2 in component_ids, (
            f"{system_file}: connection references unknown component2 '{conn.component2}'. "
            f"Known components: {sorted(component_ids)}"
        )


@pytest.mark.parametrize(
    "system_file",
    collect_system_files(),
    ids=lambda p: str(p.relative_to(REPO_ROOT)),
)
def test_connection_port_references(system_file: Path) -> None:
    library_registry = _build_library_registry()

    with system_file.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    parsed = SystemFile.model_validate(raw)
    system = parsed.system

    # Build component -> port set mapping
    component_ports: dict[str, set[str]] = {}
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
        component_ports[component.id] = {p.id for p in model_def.ports}

    for conn in system.connections:
        for comp_id, port_id in [(conn.component1, conn.port1), (conn.component2, conn.port2)]:
            if comp_id not in component_ports:
                continue
            assert port_id in component_ports[comp_id], (
                f"{system_file}: connection references port '{port_id}' on component "
                f"'{comp_id}', but that model only defines ports: "
                f"{sorted(component_ports[comp_id])}"
            )
