import logging
import shutil

import pytest

from .env import OBJECTIVE_ATOL
from .utils import copy_model_library, copy_study_dir_to_tmp, get_antares_study_objective

logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "study_name, library_filename, expected_objective",
    [
        # Unsupplied energy only: (60 MW load x 168 h - 2320 MWh GEMS wind) x 50000 EUR/MWh.
        # Without the GEMS area-connection, the objective would be 10080 x 50000 = 5.04e8.
        ("Hybrid_Study", "basic_models_library.yml", 3.88e8),
    ],
)
def test_doc_hybrid_study(
    tmp_root, paths, study_name: str, library_filename: str, expected_objective: float
) -> None:
    study_path = copy_study_dir_to_tmp(
        study_name=study_name,
        source_dir=paths.hybrid_doc_examples_path,
        tmp_root=tmp_root,
        preserve_symlinks=True,  # the study library is a symlink to libraries/
    )
    copy_model_library(paths, study_path, library_filename)
    # Drop outputs from local runs, so that the objective is read from this run
    shutil.rmtree(study_path / "output", ignore_errors=True)

    antares_objective = get_antares_study_objective(paths, study_path)
    logger.info("[%s] objective: %s", study_name, antares_objective)

    assert antares_objective == pytest.approx(expected_objective, abs=OBJECTIVE_ATOL)
