# This test runs the documentation tutorial 3 notebook "Investment".
# It checks that the objective values match those in the pre-executed notebook.

import logging

import pytest

from .env import OBJECTIVE_ATOL
from .utils import (
    copy_study_dir_to_tmp,
    get_gems_study_objective,
    get_notebook_objective,
)

logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "study_name, notebook_simulation_index",
    [
        ("case_no_battery", 0),
        ("case_with_battery", 1),
    ],
)
def test_doc_tutorial_3_investment(
    tmp_root,
    paths,
    study_name: str,
    notebook_simulation_index: int,
) -> None:
    notebook_objective = get_notebook_objective(
        paths.tutorial_investment_notebook_path, notebook_simulation_index
    )
    logger.info(
        "[%s] notebook objective (simulation #%d): %s",
        study_name,
        notebook_simulation_index,
        notebook_objective,
    )

    gems_path = copy_study_dir_to_tmp(
        study_name=study_name,
        source_dir=paths.tutorial_investment_doc_path,
        tmp_root=tmp_root,
        preserve_symlinks=False,
    )

    modeler_objective = get_gems_study_objective(paths, gems_path)
    logger.info("[%s] modeler objective: %s", study_name, modeler_objective)

    assert modeler_objective == pytest.approx(notebook_objective, abs=OBJECTIVE_ATOL)
