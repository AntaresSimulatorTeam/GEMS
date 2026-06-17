# This test validates the investment tutorial (tutorial 3) against hardcoded
# reference values extracted from a pre-executed tutorial-invest.ipynotebook.

import pytest

from .env import OBJECTIVE_ATOL
from .utils import get_notebook_objective, get_notebook_p_installed

# Reference values

REF_OBJECTIVE_NO_BATTERY = 5.1798466667e05  # €
REF_OBJECTIVE_WITH_BATTERY = 4.9312414493e05  # €

REF_P_THERMAL_NO_BATTERY = 375.0  # MW
REF_P_THERMAL_WITH_BATTERY = 375.0  # MW
REF_P_BATTERY_WITH_BATTERY = 90.33  # MW



def test_no_battery_objective(paths) -> None:
    notebook = paths.tutorial_investment_notebook_path
    value = get_notebook_objective(notebook, simulation_index=0)
    assert value == pytest.approx(REF_OBJECTIVE_NO_BATTERY, rel=OBJECTIVE_ATOL)


def test_with_battery_objective(paths) -> None:
    notebook = paths.tutorial_investment_notebook_path
    value = get_notebook_objective(notebook, simulation_index=1)
    assert value == pytest.approx(REF_OBJECTIVE_WITH_BATTERY, rel=OBJECTIVE_ATOL)


def test_no_battery_p_thermal(paths) -> None:
    notebook = paths.tutorial_investment_notebook_path
    value = get_notebook_p_installed(notebook, "thermal", match_index=0)
    assert value == pytest.approx(REF_P_THERMAL_NO_BATTERY, abs=OBJECTIVE_ATOL)


def test_with_battery_p_thermal(paths) -> None:
    notebook = paths.tutorial_investment_notebook_path
    value = get_notebook_p_installed(notebook, "thermal", match_index=1)
    assert value == pytest.approx(REF_P_THERMAL_WITH_BATTERY, abs=OBJECTIVE_ATOL)


def test_with_battery_p_battery(paths) -> None:
    notebook = paths.tutorial_investment_notebook_path
    value = get_notebook_p_installed(notebook, "battery", match_index=0)
    assert value == pytest.approx(REF_P_BATTERY_WITH_BATTERY, rel=OBJECTIVE_ATOL)
