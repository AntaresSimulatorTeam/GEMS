# Copyright (c) 2025, RTE (https://www.rte-france.com)
#
# This file is part of the Antares project.


import json
import shutil
import site
from pathlib import Path


def define_env(env):
    """MkDocs macros hook — exposes version variables from dependencies.json."""
    deps_file = Path(__file__).parent / "dependencies.json"
    data = json.loads(deps_file.read_text(encoding="utf-8"))
    for key, value in data.items():
        env.variables[key] = value

    _ensure_pypsa_models_yml()


def _ensure_pypsa_models_yml() -> None:
    """Copy pypsa_models.yml to site-packages when the PyPI wheel omits it.

    pypsa-to-gems-converter 0.0.1 does not bundle resources/ in its wheel.
    GemsStudyWriter.copy_library_yml looks for the file at
    <site-packages>/resources/pypsa_models/pypsa_models.yml, so we place it
    there before mkdocs-jupyter executes the tutorial notebook.
    """
    src = (
        Path(__file__).parent
        / "doc"
        / "examples"
        / "notebooks"
        / "tutorial-two-pypsa-eur"
        / "pypsa_models.yml"
    )
    if not src.exists():
        return
    for sp in site.getsitepackages():
        dest = Path(sp) / "resources" / "pypsa_models" / "pypsa_models.yml"
        if not dest.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, dest)
