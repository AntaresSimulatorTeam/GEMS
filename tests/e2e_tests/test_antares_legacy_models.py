# Copyright (c) 2025, RTE (https://www.rte-france.com)
#
# This file is part of the Antares project.

import logging
import shutil
import subprocess
from pathlib import Path
import zipfile

import pandas as pd
import pytest

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------------
current_dir = Path(__file__).resolve().parents[2]
studies_folder = current_dir / "resources" / "e2e_studies" / "antares_legacy_models"
thermal_cluster_studies_path = studies_folder / "test_thermal_clusters"
sts_studies_path = studies_folder / "test_sts"

antares_root = current_dir / "antares-9.3.2-Ubuntu-22.04"
antares_solver_bin = antares_root / "bin" / "antares-solver"
antares_modeler_bin = antares_root / "bin" / "antares-modeler"

OBJECTIVE_ATOL = 1e-4


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def get_gems_objective_function_value(file_name: Path) -> float:
    """Read an objective function value from a CSV/TSV file produced by GEMS."""
    match file_name.suffix:
        case ".csv":
            df = pd.read_csv(file_name, usecols=["output", "value"])
        case ".tsv":
            df = pd.read_csv(file_name, sep="\t", usecols=["output", "value"])
        case _:
            raise ValueError(f"Invalid file format: {file_name.suffix}")

    result = df.query("output == 'OBJECTIVE_VALUE'")["value"]
    return float(result.iloc[0])

def get_antares_objective_function_value(file_name: Path) -> float:
    """Read an objective function value from txt file."""
    exp_value: float | None = None
    with file_name.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("EXP"):  # e.g. "EXP  :  5.5088e+06"
                parts = line.split(":")
                if len(parts) >= 2:
                    exp_value = float(parts[1].strip())
                    break
    return exp_value


def copy_zip_folder(
    zip1_name: str,
    zip2_name: str,
    source_dir: Path,
    tmp_root: Path,
) -> Path:
    """Copy two zip files into tmp/folder_name and return the target folder."""
    target_folder = tmp_root
    target_folder.mkdir(parents=True, exist_ok=True)

    for name in (zip1_name, zip2_name):
        src = source_dir / name
        if not src.is_file():
            pytest.fail(f"ZIP file not found: {src}")
        shutil.copy(src, target_folder)

    return target_folder


def unzip_studies(zip_folder: Path) -> tuple[Path, Path]:
    """Unzip the two zip files in zip_folder and return their study directories."""
    zip_files = sorted(zip_folder.glob("*.zip"))
    if len(zip_files) != 2:
        pytest.fail(f"Expected 2 zip files, found {len(zip_files)} in {zip_folder}")

    extracted_paths: list[Path] = []

    for zip_path in zip_files:
        study_dir = zip_folder / zip_path.stem
        try:
            with zipfile.ZipFile(zip_path, "r") as z:
                # Let the archive create its own internal top-level folder
                z.extractall(zip_folder)
        except Exception as e:
            pytest.fail(f"Unzipping failed for {zip_path}: {e}")

        extracted_paths.append(study_dir)

    extracted_paths.sort()
    return extracted_paths[0], extracted_paths[1]


def copy_file_to_gems_study(gems_study_path: Path) -> None:
    """Copy antares_legacy_models.yml into input/model-libraries of the GEMS study."""
    source_file = current_dir / "libraries" / "antares_legacy_models.yml"
    if not source_file.is_file():
        pytest.fail(f"Source file does not exist: {source_file}")

    target_folder = gems_study_path / "input" / "model-libraries"
    if not target_folder.is_dir():
        pytest.fail(f"GEMS study is missing required folder: {target_folder}")

    target_path = target_folder / source_file.name
    try:
        shutil.copy(source_file, target_path)
    except Exception as e:
        pytest.fail(f"Failed to copy {source_file} to {target_path}: {e}")


def get_gems_study_objective(study_dir: Path) -> float:
    """Run GEMS (Antares modeler) and return the objective value."""
    logger.info(f"Running Antares modeler with study directory: {study_dir}")

    try:
        subprocess.run(
            [str(antares_modeler_bin), str(study_dir)],
            capture_output=True,
            text=True,
            check=False,
            cwd=str(antares_modeler_bin.parent),
        )
    except subprocess.CalledProcessError as e:
        raise Exception(f"Antares modeler failed with error: {e}") from e

    logger.info("Getting GEMS study objective")

    output_dir = study_dir / "output"
    result_files = [
        f
        for f in output_dir.iterdir()
        if f.is_file() and f.name.startswith("simulation_table")
    ]

    if not result_files:
        raise FileNotFoundError(f"Result file not found in {output_dir}")

    return get_gems_objective_function_value(result_files[-1])


def get_antares_study_objective(study_dir: Path) -> float:
    """Run Antares solver and return the objective value from annualSystemCost.txt."""
    logger.info(f"Running Antares Simulator with study directory: {study_dir}")

    try:
        subprocess.run(
            [str(antares_solver_bin), str(study_dir), "--linear-solver=coin"],
            capture_output=True,
            text=True,
            check=True,
            cwd=str(antares_solver_bin.parent),
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

    subdirs = sorted(d for d in output_dir.iterdir() if d.is_dir())
    if not subdirs:
        raise FileNotFoundError(f"No subdirectories found in {output_dir}")

    result_file = subdirs[0] / "annualSystemCost.txt"
    if not result_file.is_file():
        raise FileNotFoundError(f"Result file not found: {result_file}")
    
    exp_value = get_antares_objective_function_value(file_name=result_file)

    if exp_value is None:
        raise ValueError(f"Could not find EXP line in {result_file}")

    logger.info(f"Antares study objective (EXP) = {exp_value}")
    return exp_value


# -----------------------------------------------------------------------------
# Fixtures
# -----------------------------------------------------------------------------
@pytest.fixture(scope="function", autouse=True)
def check_antares_binaries() -> None:
    """Check if Antares binaries are available before running tests."""
    if not antares_root.is_dir():
        pytest.skip(
            "Antares binaries not found. Please download them from "
            "https://github.com/AntaresSimulatorTeam/Antares_Simulator/releases"
        )


@pytest.fixture(scope="session")
def tmp_root() -> Path:
    """Create tmp directory once and delete it after all tests."""
    tmp = current_dir / "tmp"
    try:
        tmp.mkdir(exist_ok=True)
    except Exception as e:
        pytest.fail(f"Failed to create temporary directory {tmp}: {e}")

    yield tmp  # give to tests

    # after all tests, delete tmp entirely
    shutil.rmtree(tmp, ignore_errors=True)


@pytest.fixture(scope="function", autouse=True)
def clean_tmp(tmp_root: Path) -> None:
    """Clean the contents of tmp before each test."""
    for item in tmp_root.iterdir():
        if item.is_dir():
            shutil.rmtree(item, ignore_errors=True)
        else:
            item.unlink(missing_ok=True)

# -----------------------------------------------------------------------------
# Parametrized tests
# -----------------------------------------------------------------------------
@pytest.mark.parametrize(
    "antares_zip, gems_zip, source_dir",
    [
        ("Antares-Simulator-Thermal-Test.zip", "GEMS-Thermal-Test.zip", thermal_cluster_studies_path),
        ("Antares-Simulator-STS-Test.zip",    "GEMS-STS-Test.zip",    sts_studies_path),
    ],
)
def test_study_equivalence(
    tmp_root: Path,
    antares_zip: str,
    gems_zip: str,
    source_dir: Path,
) -> None:
    # Prepare zips in tmp
    target_folder = copy_zip_folder(
        zip1_name=antares_zip,
        zip2_name=gems_zip,
        source_dir=source_dir,
        tmp_root=tmp_root,
    )

    # Unzip Antares and GEMS studies
    antares_path, gems_path = unzip_studies(target_folder)

    # Copy library into GEMS study
    copy_file_to_gems_study(gems_path)

    # Compute objectives
    gems_objective = get_gems_study_objective(gems_path)
    antares_objective = get_antares_study_objective(antares_path)

    logger.info(f"GEMS objective    : {gems_objective}")
    logger.info(f"Antares objective : {antares_objective}")

    # Sanity checks
    assert (target_folder / antares_zip).exists()
    assert (target_folder / gems_zip).exists()
    assert antares_path.is_dir()
    assert gems_path.is_dir()

    # Objectives close within absolute tolerance
    assert gems_objective == pytest.approx(antares_objective, abs=OBJECTIVE_ATOL)
