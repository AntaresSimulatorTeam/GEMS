import logging
import shutil
from pathlib import Path

import pytest

from .env import get_paths


# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)


@pytest.fixture(scope="session")
def paths():
    """Session-wide access to repo/studies/binaries paths."""
    return get_paths()


@pytest.fixture(scope="function", autouse=True)
def check_antares_binaries(paths) -> None:
    """Check if Antares binaries are available before running tests."""
    if not paths.antares_root.is_dir():
        pytest.skip(
            "Antares binaries not found. They are expected at: "
            f"{paths.antares_root} (CI downloads/extracts them in the workflow)."
        )


@pytest.fixture(scope="session")
def tmp_root(paths) -> Path:
    """Create tmp directory once and delete it after all tests."""
    tmp = paths.repo_root / "tmp"
    tmp.mkdir(exist_ok=True)

    yield tmp

    shutil.rmtree(tmp, ignore_errors=True)


@pytest.fixture(scope="function", autouse=True)
def clean_tmp(tmp_root: Path) -> None:
    """Clean the contents of tmp before each test."""
    for item in tmp_root.iterdir():
        if item.is_dir():
            shutil.rmtree(item, ignore_errors=True)
        else:
            item.unlink(missing_ok=True)
