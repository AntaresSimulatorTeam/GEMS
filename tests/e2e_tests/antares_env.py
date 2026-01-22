# Copyright (c) 2025, RTE (https://www.rte-france.com)
#
# This file is part of the Antares project.

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


OBJECTIVE_ATOL = 1e-4


@dataclass(frozen=True)
class AntaresPaths:
    repo_root: Path
    studies_folder: Path
    thermal_cluster_studies_path: Path
    sts_studies_path: Path
    doc_examples_path: Path

    antares_root: Path
    antares_solver_bin: Path
    antares_modeler_bin: Path


def get_paths() -> AntaresPaths:
    """
    Central place for:
    - repo paths
    - studies paths
    - Antares binaries paths (assuming they are extracted in repo root)
    """
    repo_root = Path(__file__).resolve().parents[2]

    studies_folder = repo_root / "resources" / "e2e_studies" / "antares_legacy_models"
    thermal_cluster_studies_path = studies_folder / "test_thermal_clusters"
    sts_studies_path = studies_folder / "test_sts"

    doc_examples_path = repo_root / "resources" / "Documentation_Examples" / "QSE"

    antares_root = repo_root / "antares-9.3.2-Ubuntu-22.04"
    antares_solver_bin = antares_root / "bin" / "antares-solver"
    antares_modeler_bin = antares_root / "bin" / "antares-modeler"

    return AntaresPaths(
        repo_root=repo_root,
        studies_folder=studies_folder,
        thermal_cluster_studies_path=thermal_cluster_studies_path,
        sts_studies_path=sts_studies_path,
        doc_examples_path=doc_examples_path,
        antares_root=antares_root,
        antares_solver_bin=antares_solver_bin,
        antares_modeler_bin=antares_modeler_bin,
    )
