# This test runs the antares legacy to GEMS converter tutorial (tutorial 4): it converts the
# sample legacy study, runs the Antares modeler on the result, and checks that the objective
# matches the one saved in the pre-executed notebook.

import logging

import pytest

from .env import OBJECTIVE_ATOL
from .utils import copy_study_dir_to_tmp, get_gems_study_objective, get_notebook_objective

logger = logging.getLogger(__name__)

LEGACY_STUDY_NAME = "antares_legacy_study_for_converter_tutorial"
LEGACY_LIBRARY_NAME = "antares_legacy_models.yml"


@pytest.mark.parametrize("notebook_simulation_index", [0])
def test_doc_tutorial_4_legacy_converter(tmp_root, paths, notebook_simulation_index: int) -> None:
    from antares.craft import read_study_local
    from antares_gems_converter.input_converter.src.converter import AntaresStudyConverter
    from antares_gems_converter.input_converter.src.logger import Logger

    notebook_objective = get_notebook_objective(
        paths.tutorial_legacy_converter_notebook_path, notebook_simulation_index
    )
    logger.info(
        "notebook objective (simulation #%d): %s", notebook_simulation_index, notebook_objective
    )

    legacy_path = copy_study_dir_to_tmp(
        study_name=LEGACY_STUDY_NAME,
        source_dir=paths.tutorial_legacy_converter_dir,
        tmp_root=tmp_root,
        preserve_symlinks=False,
    )
    output_root = tmp_root / "converter_output"

    study = read_study_local(legacy_path)
    converter = AntaresStudyConverter(
        study_input=study,
        logger=Logger("e2e_legacy_converter", study.path),
        mode="full",
        output_folder=output_root,
        lib_paths=[str(paths.repo_root / "libraries" / LEGACY_LIBRARY_NAME)],
        models_to_convert=["load", "wind", "thermal", "link"],
    )
    converter.process_all()

    # The modeler needs a parameters.yml, with the same time scope as the notebook.
    gems_path = output_root / LEGACY_STUDY_NAME
    (gems_path / "parameters.yml").write_text(
        "solver: coin\nsolver-logs: false\nsolver-parameters: THREADS 1\n"
        "no-output: false\nfirst-time-step: 0\nlast-time-step: 167\n",
        encoding="utf-8",
    )

    modeler_objective = get_gems_study_objective(paths, gems_path)
    logger.info("modeler objective: %s", modeler_objective)

    assert modeler_objective == pytest.approx(notebook_objective, rel=OBJECTIVE_ATOL)
