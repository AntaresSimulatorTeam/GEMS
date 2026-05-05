# Copyright (c) 2025, RTE (https://www.rte-france.com)
#
# This file is part of the Antares project.

import json
from pathlib import Path


def define_env(env):
    """MkDocs macros hook — exposes version variables from dependencies.json."""
    deps_file = Path(__file__).parent / "dependencies.json"
    data = json.loads(deps_file.read_text(encoding="utf-8"))
    for key, value in data.items():
        env.variables[key] = value
