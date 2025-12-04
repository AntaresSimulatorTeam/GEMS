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

# Pytest fixture to check for Antares binaries
@pytest.fixture(scope="function", autouse=True)
def check_antares_binaries() -> None:
    """Check if Antares binaries are available before running tests."""
    antares_dir = current_dir / "antares-9.3.2-Ubuntu-22.04"
    if not antares_dir.is_dir():
        pytest.skip(
            "Antares binaries not found. Please download them from https://github.com/AntaresSimulatorTeam/Antares_Simulator/releases"
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



