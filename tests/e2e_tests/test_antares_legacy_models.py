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

doc_examples_path = current_dir / "resources" / "Documentation_Examples" / "QSE"

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


def copy_antares_zip_to_tmp(*, zip_name: str, source_dir: Path, tmp_root: Path) -> Path:
    """Copy an Antares study ZIP to tmp_root and return the copied ZIP path."""
    src = source_dir / zip_name
    if not src.is_file():
        pytest.fail(f"Antares ZIP file not found: {src}")

    dst = tmp_root / zip_name
    shutil.copy(src, dst)
    return dst


def copy_study_dir_to_tmp(
    *,
    study_name: str,
    source_dir: Path,
    tmp_root: Path,
    preserve_symlinks: bool,
) -> Path:
    """
    Copy a study directory (source_dir/study_name) into tmp_root/study_name.
    Returns the copied study path.
    """
    src = source_dir / study_name
    if not src.is_dir():
        pytest.fail(f"Study folder not found: {src}")

    dst = tmp_root / study_name
    if dst.exists():
        shutil.rmtree(dst, ignore_errors=True)

    shutil.copytree(src, dst, symlinks=preserve_symlinks)
    return dst


def unzip_antares_study(zip_folder: Path, antares_zip_name: str) -> Path:
    """
    Unzip the Antares study zip into zip_folder and return the study directory.
    """
    zip_path = zip_folder / antares_zip_name
    if not zip_path.is_file():
        pytest.fail(f"Antares ZIP file not found in tmp: {zip_path}")

    try:
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(zip_folder)
    except Exception as e:
        pytest.fail(f"Unzipping failed for {zip_path}: {e}")

    study_dir = zip_folder / zip_path.stem
    if not study_dir.is_dir():
        pytest.fail(f"Antares study directory not found after unzip: {study_dir}")

    return study_dir


def copy_model_library(gems_study_path: Path, library_filename: str) -> None:
    """
    Install a model library into <study>/input/model-libraries.
    If a symlink (even dangling) already exists at that path, it is removed first.
    """
    source_file = current_dir / "libraries" / library_filename
    if not source_file.is_file():
        pytest.fail(f"Library source file does not exist: {source_file}")

    target_folder = gems_study_path / "input" / "model-libraries"
    target_folder.mkdir(parents=True, exist_ok=True)

    target_path = target_folder / library_filename

    # If it's a dangling symlink, exists() may be False, so check is_symlink() too
    if target_path.is_symlink() or target_path.exists():
        target_path.unlink()

    shutil.copy(source_file, target_path)
    assert target_path.is_file(), f"Library was not installed correctly: {target_path}"


def get_gems_study_objective(study_dir: Path) -> float:
    """Run GEMS (Antares modeler) and return the objective value."""
    logger.info(f"Running Antares modeler with study directory: {study_dir}")

    # NOTE: check=False to avoid raising, but you may still want to inspect stdout/stderr
    subprocess.run(
        [str(antares_modeler_bin), str(study_dir)],
        capture_output=True,
        text=True,
        check=False,
        cwd=str(antares_modeler_bin.parent),
    )

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


def prepare_and_run_doc_study(tmp_root: Path, study_name: str, library_filename: str) -> float:
    """
    Copy a documentation study into tmp, install its required model library,
    run the modeler, and return the objective.
    """
    gems_path = copy_study_dir_to_tmp(
        study_name=study_name,
        source_dir=doc_examples_path,
        tmp_root=tmp_root,
        preserve_symlinks=True,  # doc examples may contain symlinks
    )

    copy_model_library(gems_path, library_filename)

    obj = get_gems_study_objective(gems_path)
    logger.info(f"[{study_name}] Using {library_filename} -> objective: {obj}")
    return obj


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
# Tests
# -----------------------------------------------------------------------------
@pytest.mark.parametrize(
    "antares_zip, gems_study, source_dir",
    [
        ("Antares-Simulator-Thermal-Test.zip", "GEMS-Thermal-Test", thermal_cluster_studies_path),
        ("Antares-Simulator-STS-Test.zip", "GEMS-STS-Test", sts_studies_path),
    ],
)
def test_study_equivalence(
    tmp_root: Path,
    antares_zip: str,
    gems_study: str,
    source_dir: Path,
) -> None:
    # Copy Antares zip + GEMS study into tmp
    copy_antares_zip_to_tmp(zip_name=antares_zip, source_dir=source_dir, tmp_root=tmp_root)

    # These e2e studies are regular dirs (no symlinks expected); keep old behavior
    gems_path = copy_study_dir_to_tmp(
        study_name=gems_study,
        source_dir=source_dir,
        tmp_root=tmp_root,
        preserve_symlinks=False,
    )

    # Install required library
    copy_model_library(gems_path, "antares_legacy_models.yml")

    # Unzip Antares study and run solver
    antares_path = unzip_antares_study(tmp_root, antares_zip)

    gems_objective = get_gems_study_objective(gems_path)
    antares_objective = get_antares_study_objective(antares_path)

    logger.info(f"GEMS objective    : {gems_objective}")
    logger.info(f"Antares objective : {antares_objective}")

    assert gems_objective == pytest.approx(antares_objective, abs=OBJECTIVE_ATOL)


def test_doc_qse_1_adequacy(tmp_root: Path) -> None:
    gems_objective = prepare_and_run_doc_study(
        tmp_root=tmp_root,
        study_name="QSE_1_Adequacy",
        library_filename="basic_models_library.yml",
    )

    assert gems_objective == pytest.approx(7990.0, abs=OBJECTIVE_ATOL)



def test_doc_qse_2_unit_commitment(tmp_root: Path) -> None:
    gems_objective = prepare_and_run_doc_study(
        tmp_root=tmp_root,
        study_name="QSE_2_Unit_Commitment",
        library_filename="antares_legacy_models.yml",
    )

    assert gems_objective == pytest.approx(817550.0, abs=OBJECTIVE_ATOL)
