# This test validates the investment tutorial (tutorial 3) against hardcoded
# reference values extracted from a pre-executed tutorial-invest.ipynb.

import json
import re

import pytest

from .env import OBJECTIVE_ATOL, OBJECTIVE_RTOL
from .utils import get_notebook_objective

# Reference values

REF_OBJECTIVE_NO_BATTERY = 5.1798466667e05  # €
REF_OBJECTIVE_WITH_BATTERY = 4.9312414493e05  # €

REF_P_THERMAL_NO_BATTERY = 375.0  # MW
REF_P_THERMAL_WITH_BATTERY = 375.0  # MW
REF_P_BATTERY_WITH_BATTERY = 90.33  # MW

def get_notebook_p_installed(notebook_path, candidate: str, match_index: int = 0) -> float:
    """Return the Nth p_installed value for a given candidate from a pre-executed notebook."""
    with notebook_path.open(encoding="utf-8") as f:
        nb = json.load(f)

    pattern = re.compile(
        rf"candidate {re.escape(candidate)} - p_installed\s*=\s*([\d.e+\-]+)\s*MW"
    )
    values = []
    for cell in nb["cells"]:
        if cell["cell_type"] != "code":
            continue
        for output in cell.get("outputs", []):
            text = "".join(output.get("text", []))
            for m in pattern.finditer(text):
                values.append(float(m.group(1)))

    if match_index >= len(values):
        raise ValueError(
            f"match_index {match_index} out of range: "
            f"found {len(values)} p_installed value(s) for '{candidate}' in {notebook_path}"
        )
    return values[match_index]


def test_no_battery_objective(paths) -> None:
    nb = paths.tutorial_investment_notebook_path
    value = get_notebook_objective(nb, simulation_index=0)
    assert value == pytest.approx(REF_OBJECTIVE_NO_BATTERY, rel=OBJECTIVE_RTOL)


def test_with_battery_objective(paths) -> None:
    nb = paths.tutorial_investment_notebook_path
    value = get_notebook_objective(nb, simulation_index=1)
    assert value == pytest.approx(REF_OBJECTIVE_WITH_BATTERY, rel=OBJECTIVE_RTOL)


def test_no_battery_p_thermal(paths) -> None:
    nb = paths.tutorial_investment_notebook_path
    value = get_notebook_p_installed(nb, "thermal", match_index=0)
    assert value == pytest.approx(REF_P_THERMAL_NO_BATTERY, abs=OBJECTIVE_ATOL)


def test_with_battery_p_thermal(paths) -> None:
    nb = paths.tutorial_investment_notebook_path
    value = get_notebook_p_installed(nb, "thermal", match_index=1)
    assert value == pytest.approx(REF_P_THERMAL_WITH_BATTERY, abs=OBJECTIVE_ATOL)


def test_with_battery_p_battery(paths) -> None:
    nb = paths.tutorial_investment_notebook_path
    value = get_notebook_p_installed(nb, "battery", match_index=0)
    assert value == pytest.approx(REF_P_BATTERY_WITH_BATTERY, rel=OBJECTIVE_RTOL)
