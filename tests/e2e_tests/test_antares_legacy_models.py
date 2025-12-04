# Copyright (c) 2025, RTE (https://www.rte-france.com)
#
# See AUTHORS.txt
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# SPDX-License-Identifier: MPL-2.0
#
# This file is part of the Antares project.

import logging
import math
import shutil
import subprocess
from pathlib import Path
from ..utilis import get_objective_value

import pytest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

current_dir = Path(__file__).resolve().parents[2]
studies_folder = current_dir / "resources" / "e2e_studies" / "antares_legacy_models"
thermal_cluster_studies_path = studies_folder / "test_thermal_clusters"


# ---------------------------------------------------------------------------
# Helper: copy two zip files into tmp/folder_name
# ---------------------------------------------------------------------------
def copy_zip_folder(
    folder_name: str,
    zip1_name: str,
    zip2_name: str,
    source_dir: Path,
    tmp_root: Path,
) -> Path:
    target_folder = tmp_root / folder_name
    target_folder.mkdir(parents=True, exist_ok=True)

    zip1 = source_dir / zip1_name
    zip2 = source_dir / zip2_name

    if not zip1.is_file():
        pytest.fail(f"ZIP file not found: {zip1}")
    if not zip2.is_file():
        pytest.fail(f"ZIP file not found: {zip2}")

    shutil.copy(zip1, target_folder)
    shutil.copy(zip2, target_folder)

    return target_folder


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture(scope="function", autouse=True)
def check_antares_binaries() -> None:
    """Check if Antares binaries are available before running tests."""
    antares_dir = current_dir / "antares-9.3.2-Ubuntu-22.04"
    if not antares_dir.is_dir():
        pytest.skip(
            "Antares binaries not found. Please download them from "
            "https://github.com/AntaresSimulatorTeam/Antares_Simulator/releases"
        )


@pytest.fixture(scope="function", autouse=True)
def create_tmp() -> Path:
    """Create a temporary directory and abort the test if creation fails."""
    tmp = current_dir / "tmp"

    try:
        tmp.mkdir(exist_ok=True)
    except Exception as e:
        pytest.fail(f"Failed to create temporary directory {tmp}: {e}")

    return tmp


# ---------------------------------------------------------------------------
# Test
# ---------------------------------------------------------------------------
def test_thermal_clusters(create_tmp: Path) -> None:
    antares_study = "Antares-Simulator-Thermal-Test.zip"
    gems_study = "GEMS-Thermal-Test.zip"

    # create_tmp is the root tmp folder; we create a subfolder for this test
    target_folder = copy_zip_folder(
        folder_name="thermal_clusters",
        zip1_name=antares_study,
        zip2_name=gems_study,
        source_dir=thermal_cluster_studies_path,
        tmp_root=create_tmp,
    )

    # basic sanity checks
    assert (target_folder / antares_study).exists()
    assert (target_folder / gems_study).exists()
