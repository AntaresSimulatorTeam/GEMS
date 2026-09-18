# Copyright (c) 2026, RTE (https://www.rte-france.com)
#
# This file is part of the Antares project.

from __future__ import annotations

import logging
from pathlib import Path

import pytest

from .env import OBJECTIVE_ATOL
from .utils import execute_notebook_in_docker, get_notebook_objective, get_pypsa_objective

logger = logging.getLogger(__name__)

NETWORK_FILE = "pypsa-eur/resources/networks/base_s_1_elec.nc"
NOTEBOOK_FILE = "tutorial_pypsa_eur_gemspy.ipynb"
DOCKERFILE = "docker-tuto-pypsa-gems/Dockerfile_PyPSA_GemsPy"
IMAGE_TAG = "my-pypsa-gemspy-tuto"
NOTEBOOK_IN_CONTAINER = "/workspace/tutorial_pypsa_eur_gemspy.ipynb"


def test_pypsa_eur_objective_matches_gems(
    paths,
    tmp_root: Path,
) -> None:
    """Build the tutorial Docker image, execute the notebook inside it, and verify
    the GEMS objective matches the PyPSA objective within OBJECTIVE_ATOL.

    Reference: doc/getting-started/tutorial-two-pypsa-eur/E2E_TESTS_REQUIREMENTS.md

    PyPSA objective = n.objective + n.objective_constant:
      - n.objective          : LP variable costs (extendable generators)
      - n.objective_constant : fixed capital costs of non-extendable generators
    GEMS counts both, so both must be included on the PyPSA side.
    """
    tutorial_dir = paths.pypsa_eur_tutorial_path
    network_path = tutorial_dir / NETWORK_FILE

    if not network_path.is_file():
        pytest.skip(f"PyPSA-Eur network not found: {network_path}")

    pypsa_obj = get_pypsa_objective(network_path)
    logger.info("PyPSA objective: %.6f €", pypsa_obj)

    executed_notebook = tmp_root / NOTEBOOK_FILE
    execute_notebook_in_docker(
        dockerfile=tutorial_dir / DOCKERFILE,
        context=tutorial_dir,
        image_tag=IMAGE_TAG,
        notebook_in_container=NOTEBOOK_IN_CONTAINER,
        volumes=[
            # Network data (read-only, same as docker-compose)
            f"{tutorial_dir}/pypsa-eur/resources:/workspace/pypsa-eur/resources:ro",
            # pypsa_models.yml workaround: converter wheel omits this file
            f"{paths.repo_root}/libraries/pypsa_models.yml"
            ":/usr/local/lib/python3.12/site-packages/resources/pypsa_models/pypsa_models.yml:ro",
        ],
        output_path=executed_notebook,
    )

    gems_obj = get_notebook_objective(executed_notebook)
    logger.info("GEMS  objective: %.6f €", gems_obj)

    assert gems_obj == pytest.approx(pypsa_obj, rel=OBJECTIVE_ATOL)
