# Copyright (c) 2025, RTE (https://www.rte-france.com)
#
# This file is part of the Antares project.

from __future__ import annotations

import logging
import shutil
import subprocess
import zipfile
from pathlib import Path

import pandas as pd
import pytest

from .antares_env import AntaresPaths


logger = logging.getLogger(__name__)


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


def get_antares_objective_function_value(file_name: Path) -> float | None:
    """Read an objective function value from annualSystemCost.txt (EXP line)."""
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
    """Unzip the Antares study zip into zip_folder and return the study directory."""
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


def copy_model_library(paths: AntaresPaths, gems_study_path: Path, library_filename: str) -> None:
    """
    Install a model library into <study>/input/model-libraries.
    If a symlink (even dangling) already exists at that path, it is removed first.
    """
    source_file = paths.repo_root / "libraries" / library_filename
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


def get_gems_study_objective(paths: AntaresPaths, study_dir: Path) -> float:
    """Run GEMS (Antares modeler) and return the objective value."""
    logger.info("Running Antares modeler with study directory: %s", study_dir)

    subprocess.run(
        [str(paths.antares_modeler_bin), str(study_dir)],
        capture_output=True,
        text=True,
        check=False,  # keep behavior: do not raise, but output might still be useful later
        cwd=str(paths.antares_modeler_bin.parent),
    )

    logger.info("Getting GEMS study objective")

    output_dir = study_dir / "output"
    result_files = [
        f for f in output_dir.iterdir()
        if f.is_file() and f.name.startswith("simulation_table")
    ]

    if not result_files:
        raise FileNotFoundError(f"Result file not found in {output_dir}")

    return get_gems_objective_function_value(result_files[-1])


def get_antares_study_objective(paths: AntaresPaths, study_dir: Path) -> float:
    """Run Antares solver and return the objective value from annualSystemCost.txt."""
    logger.info("Running Antares Simulator with study directory: %s", study_dir)

    try:
        subprocess.run(
            [str(paths.antares_solver_bin), str(study_dir), "--linear-solver=coin"],
            capture_output=True,
            text=True,
            check=True,
            cwd=str(paths.antares_solver_bin.parent),
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

    logger.info("Antares study objective (EXP) = %s", exp_value)
    return exp_value
