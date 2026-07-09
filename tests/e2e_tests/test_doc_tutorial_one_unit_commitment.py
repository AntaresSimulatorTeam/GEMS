# This test runs the documentation the first tutorial notebook "Unit Commitment"
# It checks that the objective values match those in the pre-executed notebook.

import logging
import shutil
from pathlib import Path

import pytest

from .env import OBJECTIVE_ATOL, EnvironmentPaths
from .utils import (
    copy_model_library,
    copy_study_dir_to_tmp,
    get_gems_study_objective,
    get_notebook_objective,
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
        preserve_symlinks=True,
    )

    copy_model_library(paths, gems_path, library_filename)

    obj = get_gems_study_objective(paths, gems_path)
    logger.info("[%s] Using %s -> objective: %s", study_name, library_filename, obj)
    return obj


def install_tutorial_library(paths: EnvironmentPaths, gems_study_path: Path) -> None:
    """Copy gemspy_tutorial_library.yml from the shared library into the study's model-libraries."""
    source = (
        paths.repo_root
        / "doc"
        / "examples"
        / "notebooks"
        / "tutorial-one-unit-commitment"
        / "unit-commitment-with-gemspy"
        / "gemspy_tutorial_library.yml"
    )

    target_folder = gems_study_path / "input" / "model-libraries"
    target_folder.mkdir(parents=True, exist_ok=True)
    target = target_folder / "gemspy_tutorial_library.yml"
    if target.is_symlink() or target.exists():
        target.unlink()
    shutil.copy(source, target)


@pytest.mark.parametrize(
    "study_name, notebook_simulation_index",
    [
        # second simulation run — after adding wind_farm and solar_farm
        ("step-two-with-renewables", 1),
        # third simulation run — thermal_gen replaced by 10-unit thermal_gen_UC
        ("step-three-unit-commitment", 2),
    ],
)
def test_doc_tutorial_1_unit_commitment(
    tmp_root,
    paths,
    study_name: str,
    notebook_simulation_index: int,
) -> None:
    notebook_objective = get_notebook_objective(
        paths.tutorial_notebook_path, notebook_simulation_index
    )
    logger.info(
        "[%s] notebook objective (simulation #%d): %s",
        study_name,
        notebook_simulation_index,
        notebook_objective,
    )

    gems_path = copy_study_dir_to_tmp(
        study_name=study_name,
        source_dir=paths.tutorial_doc_examples_path,
        tmp_root=tmp_root,
        preserve_symlinks=False,
    )
    install_tutorial_library(paths, gems_path)
    modeler_objective = get_gems_study_objective(paths, gems_path)
    logger.info("[%s] modeler objective: %s", study_name, modeler_objective)

    assert modeler_objective == pytest.approx(notebook_objective, abs=OBJECTIVE_ATOL)
