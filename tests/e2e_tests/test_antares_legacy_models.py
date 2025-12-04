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
import zipfile

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

def unzip_studies(zip_folder: Path) -> tuple[Path, Path]:
    zip_files = list(zip_folder.glob("*.zip"))
    if len(zip_files) != 2:
        pytest.fail(f"Expected 2 zip files, found {len(zip_files)} in {zip_folder}")

    extracted_paths = []

    for zip_path in zip_files:
        # Example: Antares-Simulator-Thermal-Test.zip → "Antares-Simulator-Thermal-Test"
        study_dir = zip_folder / zip_path.stem

        try:
            with zipfile.ZipFile(zip_path, "r") as z:
                # Let the archive create its internal top-level folder
                z.extractall(zip_folder)
        except Exception as e:
            pytest.fail(f"Unzipping failed for {zip_path}: {e}")

        extracted_paths.append(study_dir)

    # Consistent order (e.g. Antares first, GEMS second)
    extracted_paths.sort()
    return extracted_paths[0], extracted_paths[1]

def copy_file_to_gems_study(gems_study_path: Path) -> Path:

    source_file = current_dir / "libraries" / "antares_legacy_models.yml"
    if not source_file.is_file():
        pytest.fail(f"Source file does not exist: {source_file}")

    # Required folder structure (must already exist in the extracted study)
    target_folder = gems_study_path / "input" / "model-libraries"

    # Fail if required folder is missing
    if not target_folder.is_dir():
        pytest.fail(f"GEMS study is missing required folder: {target_folder}")

    # Target file path
    target_path = target_folder / source_file.name

    try:
        shutil.copy(source_file, target_path)
    except Exception as e:
        pytest.fail(f"Failed to copy {source_file} to {target_path}: {e}")

    return target_path

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

    # Unzip Antares and GEMS studies
    antares_path, gems_path = unzip_studies(target_folder)

    copied = copy_file_to_gems_study(gems_path)

    # basic sanity checks
    assert (target_folder / antares_study).exists()
    assert (target_folder / gems_study).exists()
    assert antares_path.is_dir()
    assert gems_path.is_dir()
    assert copied.exists()
