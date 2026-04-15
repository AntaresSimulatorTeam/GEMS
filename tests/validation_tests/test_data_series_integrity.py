from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import pytest
import yaml

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[2]
RESOURCES_DIR = REPO_ROOT / "resources"


def _is_string_value(value: Any) -> bool:
    return isinstance(value, str)


def collect_system_files() -> list[Path]:
    return sorted(RESOURCES_DIR.rglob("system.yml"))


@pytest.mark.parametrize(
    "system_file",
    collect_system_files(),
    ids=lambda p: str(p.relative_to(REPO_ROOT)),
)
def test_data_series_integrity(system_file: Path) -> None:
    data_series_dir = system_file.parent / "data-series"

    with system_file.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    system_raw = raw.get("system", {})
    components = system_raw.get("components", []) or []

    for component in components:
        comp_id = component.get("id", "<unknown>")
        params = component.get("parameters", []) or []
        for param in params:
            time_dependent = param.get("time-dependent", False)
            value = param.get("value")
            if time_dependent and _is_string_value(value):
                # String value references a CSV file in data-series/
                csv_path = data_series_dir / f"{value}.csv"
                assert csv_path.is_file(), (
                    f"{system_file}: component '{comp_id}' parameter "
                    f"'{param.get('id')}' references data series '{value}', "
                    f"but '{csv_path.relative_to(REPO_ROOT)}' does not exist"
                )
