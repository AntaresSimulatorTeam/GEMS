# Copyright (c) 2026, RTE (https://www.rte-france.com)
#
# This file is part of the Antares project.

from __future__ import annotations

import logging

import pytest

from .env import OBJECTIVE_RTOL
from .utils import get_notebook_objective

logger = logging.getLogger(__name__)

NOTEBOOK_FILE = "tutorial_pypsa_eur.ipynb"
EXPECTED_OBJECTIVE = 86_300_015.0 # €


def test_pypsa_eur_objective_matches_gems(
    paths,
) -> None:
    """GEMS objective stored in the pre-executed tutorial notebook must match the reference value."""
    notebook_path = paths.pypsa_eur_tutorial_path / NOTEBOOK_FILE

    if not notebook_path.is_file():
        pytest.skip(f"Tutorial notebook not found: {notebook_path}")

    gems_obj = get_notebook_objective(notebook_path)
    logger.info("GEMS objective: %.6f €", gems_obj)

    assert gems_obj == pytest.approx(EXPECTED_OBJECTIVE, rel=OBJECTIVE_RTOL)
