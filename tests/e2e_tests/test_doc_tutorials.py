import json
import logging
import re
import shutil
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
        preserve_symlinks=True,
    )

    copy_model_library(paths, gems_path, library_filename)

    obj = get_gems_study_objective(paths, gems_path)
    logger.info("[%s] Using %s -> objective: %s", study_name, library_filename, obj)
    return obj


def get_notebook_objective(notebook_path: Path, simulation_index: int) -> float:
    """
    Extract the Nth objective value from the pre-executed notebook cell outputs.

    Scans code cells in order for lines matching 'Objective value: <float>'
    and returns the value at simulation_index (0-based).
    """
    with notebook_path.open(encoding="utf-8") as f:
        nb = json.load(f)

    objectives = []
    for cell in nb["cells"]:
        if cell["cell_type"] != "code":
            continue
        for output in cell.get("outputs", []):
            text = "".join(output.get("text", []))
            match = re.search(r"Objective value:\s*([\d.e+\-]+)", text)
            if match:
                objectives.append(float(match.group(1)))

    if simulation_index >= len(objectives):
        raise ValueError(
            f"Simulation index {simulation_index} out of range: "
            f"found {len(objectives)} objective(s) in {notebook_path}"
        )

    return objectives[simulation_index]


def install_tutorial_library(paths: EnvironmentPaths, gems_study_path: Path) -> None:
    """Copy tuto_antares_legacy_models.yml from the shared library into the study's model-libraries."""
    source = (
        paths.repo_root
        / "doc"
        / "getting-started"
        / "Tutorial_1_Unit_Commitment"
        / "Tutorial_Unit_Commitment_with_GemsPy"
        / "tuto_antares_legacy_models.yml"
    )

    target_folder = gems_study_path / "input" / "model-libraries"
    target_folder.mkdir(parents=True, exist_ok=True)
    target = target_folder / "tuto_antares_legacy_models.yml"
    if target.is_symlink() or target.exists():
        target.unlink()
    shutil.copy(source, target)


@pytest.mark.parametrize(
    "study_name, notebook_simulation_index",
    [
        # second simulation run — after adding wind_farm and solar_farm
        ("Tutorial_1_Step2_With_Renewables", 1),
        # third simulation run — thermal_gen replaced by 10-unit thermal_gen_UC
        ("Tutorial_1_Step3_Unit_Commitment", 2),
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
        preserve_symlinks=True,
    )
    install_tutorial_library(paths, gems_path)
    modeler_objective = get_gems_study_objective(paths, gems_path)
    logger.info("[%s] modeler objective: %s", study_name, modeler_objective)

    assert modeler_objective == pytest.approx(notebook_objective, abs=OBJECTIVE_ATOL)
