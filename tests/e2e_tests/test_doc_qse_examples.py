import logging
from pathlib import Path

import pytest

from .antares_env import OBJECTIVE_ATOL, AntaresPaths
from .antares_utils import (
    copy_model_library,
    copy_study_dir_to_tmp,
    get_gems_study_objective,
)

logger = logging.getLogger(__name__)


def prepare_and_run_doc_study(
    paths: AntaresPaths,
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


def test_doc_qse_1_adequacy(tmp_root, paths) -> None:
    gems_objective = prepare_and_run_doc_study(
        paths=paths,
        tmp_root=tmp_root,
        study_name="QSE_1_Adequacy",
        library_filename="basic_models_library.yml",
    )

    assert gems_objective == pytest.approx(7990.0, abs=OBJECTIVE_ATOL)


def test_doc_qse_2_unit_commitment(tmp_root, paths) -> None:
    gems_objective = prepare_and_run_doc_study(
        paths=paths,
        tmp_root=tmp_root,
        study_name="QSE_2_Unit_Commitment",
        library_filename="antares_legacy_models.yml",
    )

    assert gems_objective == pytest.approx(817550.0, abs=OBJECTIVE_ATOL)
