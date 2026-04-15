from __future__ import annotations

import logging
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from tests.e2e_tests.utils import copy_study_dir_to_tmp

logger = logging.getLogger(__name__)


def test_copy_study_dir_copies_contents(tmp_path: Path) -> None:
    source_dir = tmp_path / "studies"
    source_dir.mkdir()
    study_dir = source_dir / "TestStudy"
    study_dir.mkdir()
    (study_dir / "system.yml").write_text("system:\n  id: test\n", encoding="utf-8")

    dest_root = tmp_path / "dest"
    dest_root.mkdir()

    result = copy_study_dir_to_tmp(
        study_name="TestStudy",
        source_dir=source_dir,
        tmp_root=dest_root,
        preserve_symlinks=False,
    )

    assert result == dest_root / "TestStudy"
    assert (result / "system.yml").is_file()
    assert (result / "system.yml").read_text(encoding="utf-8") == "system:\n  id: test\n"


def test_copy_study_dir_missing_source_fails(tmp_path: Path) -> None:
    source_dir = tmp_path / "studies"
    source_dir.mkdir()

    # copy_study_dir_to_tmp calls pytest.fail() which raises BaseException
    with pytest.raises(BaseException):
        copy_study_dir_to_tmp(
            study_name="NonExistentStudy",
            source_dir=source_dir,
            tmp_root=tmp_path / "dest",
            preserve_symlinks=False,
        )


def test_copy_study_dir_overwrites_existing(tmp_path: Path) -> None:
    source_dir = tmp_path / "studies"
    source_dir.mkdir()
    study_dir = source_dir / "TestStudy"
    study_dir.mkdir()
    (study_dir / "system.yml").write_text("new", encoding="utf-8")

    dest_root = tmp_path / "dest"
    dest_root.mkdir()
    # Pre-populate destination with stale data
    stale = dest_root / "TestStudy"
    stale.mkdir()
    (stale / "old_file.txt").write_text("stale", encoding="utf-8")

    copy_study_dir_to_tmp(
        study_name="TestStudy",
        source_dir=source_dir,
        tmp_root=dest_root,
        preserve_symlinks=False,
    )

    assert not (dest_root / "TestStudy" / "old_file.txt").exists()
    assert (dest_root / "TestStudy" / "system.yml").read_text(encoding="utf-8") == "new"


def test_copy_model_library_installs_file(tmp_path: Path) -> None:
    from unittest.mock import patch
    from tests.e2e_tests.utils import copy_model_library
    from tests.e2e_tests.env import EnvironmentPaths

    repo_root = tmp_path / "repo"
    libraries_dir = repo_root / "libraries"
    libraries_dir.mkdir(parents=True)
    lib_file = libraries_dir / "basic_models_library.yml"
    lib_file.write_text("library:\n  id: basic_models_library\n", encoding="utf-8")

    study_dir = tmp_path / "study"
    study_dir.mkdir()

    paths = EnvironmentPaths(
        repo_root=repo_root,
        studies_folder=repo_root / "resources",
        thermal_cluster_studies_path=repo_root / "resources",
        sts_studies_path=repo_root / "resources",
        doc_examples_path=repo_root / "resources",
        antares_root=repo_root / "antares",
        antares_solver_bin=repo_root / "antares" / "bin" / "antares-solver",
        antares_modeler_bin=repo_root / "antares" / "bin" / "antares-modeler",
    )

    copy_model_library(paths, study_dir, "basic_models_library.yml")

    installed = study_dir / "input" / "model-libraries" / "basic_models_library.yml"
    assert installed.is_file()
    assert "basic_models_library" in installed.read_text(encoding="utf-8")
