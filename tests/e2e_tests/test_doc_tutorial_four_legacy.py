# This test validates the antares legacy to GEMS converter tutorial (tutorial 4) against
# hardcoded reference values extracted from a pre-executed tutorial-legacy-converter.ipynotebook.

import pytest

from .env import OBJECTIVE_ATOL
from .utils import get_notebook_objective

# Reference values

REF_OBJECTIVE = 1e-4  # TODO: to be filled €


def test_objective(paths) -> None:
    notebook = paths.tutorial_legacy_converter_notebook_path
    value = get_notebook_objective(notebook, simulation_index=0)
    assert value == pytest.approx(REF_OBJECTIVE, rel=OBJECTIVE_ATOL)
