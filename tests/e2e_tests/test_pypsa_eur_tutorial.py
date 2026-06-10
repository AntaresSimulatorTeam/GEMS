# Copyright (c) 2026, RTE (https://www.rte-france.com)
#
# This file is part of the Antares project.

from __future__ import annotations

import logging

import pytest

from tests.e2e_tests.env import OBJECTIVE_ATOL
from .utils import get_notebook_objective, get_pypsa_objective

logger = logging.getLogger(__name__)

NETWORK_FILE = "pypsa-eur/resources/networks/base_s_1_elec.nc"
NOTEBOOK_FILE = "tutorial_pypsa_eur.ipynb"


def test_pypsa_eur_objective_matches_gems(
    paths,
) -> None:
    """GEMS objective from the tutorial notebook must match the PyPSA objective within OBJECTIVE_ATOL (1e-4 €).

    Reference: doc/getting-started/tutorial-two-pypsa-eur/E2E_TESTS_REQUIREMENTS.md

    PyPSA objective = n.objective + n.objective_constant:
      - n.objective          : LP variable costs (extendable generators)
      - n.objective_constant : fixed capital costs of non-extendable generators
    GEMS counts both, so both must be included on the PyPSA side.
    """
    network_path = paths.pypsa_eur_tutorial_path / NETWORK_FILE
    notebook_path = paths.pypsa_eur_tutorial_path / NOTEBOOK_FILE

    if not network_path.is_file():
        pytest.skip(f"PyPSA-Eur network not found: {network_path}")
    if not notebook_path.is_file():
        pytest.skip(f"Tutorial notebook not found: {notebook_path}")

    # Get PyPSA objective from the network (objective + objective_constant)
    pypsa_obj = get_pypsa_objective(network_path)
    logger.info("PyPSA objective: %.6f €", pypsa_obj)

    # GEMS objective from jupyter notebook output
    gems_obj = get_notebook_objective(notebook_path)
    logger.info("GEMS  objective: %.6f €", gems_obj)

    assert gems_obj == pytest.approx(pypsa_obj, rel=OBJECTIVE_ATOL)
