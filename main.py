# Copyright (c) 2025, RTE (https://www.rte-france.com)
#
# This file is part of the Antares project.

from pathlib import Path


def define_env(env):
    """MkDocs macros hook — exposes variables from the versions/ directory."""
    versions_file = Path(__file__).parent / "versions" / "antares-simulator.txt"
    for line in versions_file.read_text().splitlines():
        key, _, value = line.partition("=")
        if key.strip():
            env.variables[key.strip().lower()] = value.strip()
