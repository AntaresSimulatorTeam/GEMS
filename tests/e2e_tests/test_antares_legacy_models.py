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
from ..utilis import get_objective_value

import pytest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

current_dir = Path(__file__).resolve().parents[2]
studies_folder = current_dir / "resources" / "e2e_studies" / "antares_legacy_models"
thermal_cluster_studies_path = studies_folder / "test_thermal_clusters"
sts_studies_path = studies_folder / "test_sts"


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

def get_gems_study_objective(study_dir: Path) -> float:

    modeler_bin = current_dir / "antares-9.3.2-Ubuntu-22.04" / "bin" / "antares-modeler"

    logger.info(f"Running Antares modeler with study directory: {study_dir}")

    try:
        subprocess.run(
            [str(modeler_bin), str(study_dir)],
            capture_output=True,
            text=True,
            check=False,
            cwd=str(modeler_bin.parent),
        )

    except subprocess.CalledProcessError as e:
        raise Exception(f"Antares modeler failed with error: {e}")

    logger.info("Getting GEMS study objective")

    output_dir = study_dir / "output"
    result_file = [f for f in output_dir.iterdir() if f.is_file() and f.name.startswith("simulation_table")]

    if result_file:
        return get_objective_value(result_file[-1])

    raise FileNotFoundError(f"Result file not found in {output_dir}")


def get_antares_study_objective(study_dir: Path) -> float:

    antares_bin = current_dir / "antares-9.3.2-Ubuntu-22.04" / "bin" / "antares-solver"

    logger.info(f"Running Antares Simulator with study directory: {study_dir}")

    try:
        subprocess.run(
            [str(antares_bin), str(study_dir), "--linear-solver=coin"],
            capture_output=True,
            text=True,
            check=True,                     # raise if Antares fails
            cwd=str(antares_bin.parent),
        )
    except subprocess.CalledProcessError as e:
        logger.error("Antares Simulator failed")
        logger.error(e.stdout)
        logger.error(e.stderr)
        raise Exception(f"Antares Simulator failed with error: {e}") from e

    logger.info("Getting Antares study objective")

    output_dir = study_dir / "output"
    if not output_dir.is_dir():
        raise FileNotFoundError(f"Output directory not found: {output_dir}")

    # Take the first subdirectory in output/, whatever its name is
    subdirs = [d for d in output_dir.iterdir() if d.is_dir()]
    if not subdirs:
        raise FileNotFoundError(f"No subdirectories found in {output_dir}")

    first_output = sorted(subdirs)[0]
    result_file = first_output / "annualSystemCost.txt"

    if not result_file.is_file():
        raise FileNotFoundError(f"Result file not found: {result_file}")

    # Parse EXP value from annualSystemCost.txt
    exp_value: float | None = None
    with result_file.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # Example line: "EXP  :  5.5088e+06"
            if line.startswith("EXP"):
                parts = line.split(":")
                if len(parts) >= 2:
                    value_str = parts[1].strip()
                    exp_value = float(value_str)   # convert to float
                    break

    if exp_value is None:
        raise ValueError(f"Could not find EXP line in {result_file}")

    logger.info(f"Antares study objective (EXP) = {exp_value}")
    return exp_value

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

    gems_objective = get_gems_study_objective(gems_path)
    antares_objective = get_antares_study_objective(antares_path)

    logger.info("GEMS Study objective: "  + str(gems_objective))
    logger.info("Antares Study objective: "  + str(antares_objective))

    # basic sanity checks
    assert (target_folder / antares_study).exists()
    assert (target_folder / gems_study).exists()
    assert antares_path.is_dir()
    assert gems_path.is_dir()
    assert copied.exists()
    assert gems_objective == pytest.approx(antares_objective, abs=1e-4)

def test_sts(create_tmp: Path) -> None:
    antares_study = "Antares-Simulator-STS-Test.zip"
    gems_study = "GEMS-STS-Test.zip"
 
    # create_tmp is the root tmp folder; we create a subfolder for this test
    target_folder = copy_zip_folder(
        folder_name="sts",
        zip1_name=antares_study,
        zip2_name=gems_study,
        source_dir=sts_studies_path,
        tmp_root=create_tmp,
    )
 
    # Unzip Antares and GEMS studies
    antares_path, gems_path = unzip_studies(target_folder)
 
    copied = copy_file_to_gems_study(gems_path)
 
    gems_objective = get_gems_study_objective(gems_path)
    antares_objective = get_antares_study_objective(antares_path)
 
    logger.info("GEMS Study objective: "  + str(gems_objective))
    logger.info("Antares Study objective: "  + str(antares_objective))
 
    # basic sanity checks
    assert (target_folder / antares_study).exists()
    assert (target_folder / gems_study).exists()
    assert antares_path.is_dir()
    assert gems_path.is_dir()
    assert copied.exists()
    assert gems_objective == pytest.approx(antares_objective, abs=1e-4)