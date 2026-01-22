import logging

import pytest

from .env import OBJECTIVE_ATOL
from .utils import (
    copy_antares_zip_to_tmp,
    copy_model_library,
    copy_study_dir_to_tmp,
    get_antares_study_objective,
    get_gems_study_objective,
    unzip_antares_study,
)

logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "antares_zip, gems_study, source_dir_attr",
    [
        ("Antares-Simulator-Thermal-Test.zip", "GEMS-Thermal-Test", "thermal_cluster_studies_path"),
        ("Antares-Simulator-STS-Test.zip", "GEMS-STS-Test", "sts_studies_path"),
    ],
)
def test_study_equivalence(tmp_root, paths, antares_zip: str, gems_study: str, source_dir_attr: str) -> None:
    source_dir = getattr(paths, source_dir_attr)

    # Copy Antares zip + GEMS study into tmp
    copy_antares_zip_to_tmp(zip_name=antares_zip, source_dir=source_dir, tmp_root=tmp_root)

    # These e2e studies are regular dirs (no symlinks expected)
    gems_path = copy_study_dir_to_tmp(
        study_name=gems_study,
        source_dir=source_dir,
        tmp_root=tmp_root,
        preserve_symlinks=False,
    )

    # Install required library
    copy_model_library(paths, gems_path, "antares_legacy_models.yml")

    # Unzip Antares study and run solver
    antares_path = unzip_antares_study(tmp_root, antares_zip)

    gems_objective = get_gems_study_objective(paths, gems_path)
    antares_objective = get_antares_study_objective(paths, antares_path)

    logger.info("GEMS objective    : %s", gems_objective)
    logger.info("Antares objective : %s", antares_objective)

    assert gems_objective == pytest.approx(antares_objective, abs=OBJECTIVE_ATOL)
