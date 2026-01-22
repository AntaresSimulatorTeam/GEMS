import logging
from pathlib import Path

import pytest

from .env import OBJECTIVE_ATOL, EnvironmentPaths
from .utils import (
    copy_model_library,
    copy_study_dir_to_tmp,
    get_gems_study_objective,
)

logger = logging.getLogger(__name__)


def prepare_and_run_doc_study(
    paths: EnvironmentPaths,
    tmp_root: Path,
    study_name: str,
    library_filename: str,
) -> float:
    """
    Copy a documentation study into tmp, install its required model library,
    run the modeler, and return the objective.
    """
    gems_path = copy_study_dir_to_tmp(
        study_name=study_name,
        source_dir=paths.doc_examples_path,
        tmp_root=tmp_root,
        preserve_symlinks=True,  # doc examples may contain symlinks
    )

    copy_model_library(paths, gems_path, library_filename)

    obj = get_gems_study_objective(paths, gems_path)
    logger.info("[%s] Using %s -> objective: %s", study_name, library_filename, obj)
    return obj


@pytest.mark.parametrize(
    "study_name, library_filename, expected_objective",
    [
        ("QSE_1_Adequacy", "basic_models_library.yml", 7990.0),
        ("QSE_2_Unit_Commitment", "antares_legacy_models.yml", 817550.0),
    ],
)
def test_doc_qse_examples(tmp_root, paths, study_name: str, library_filename: str, expected_objective: float) -> None:
    gems_objective = prepare_and_run_doc_study(
        paths=paths,
        tmp_root=tmp_root,
        study_name=study_name,
        library_filename=library_filename,
    )

    assert gems_objective == pytest.approx(expected_objective, abs=OBJECTIVE_ATOL)
