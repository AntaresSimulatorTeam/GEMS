"""Check that the GEMS YAML files of this repository validate against ``schemas/``."""

import json
from pathlib import Path

import pytest
import yaml

jsonschema = pytest.importorskip("jsonschema")

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "schemas"

# Known deviations, kept here so that the schemas stay strict for new files.
# `time-dependant` is a typo for `time-dependent` (rejected by GemsPy as well).
KNOWN_INVALID = {
    "libraries/basic_models_library.yml",
    "resources/Documentation_Examples/QSE/QSE_1_Adequacy/input/model-libraries/basic_models_library.yml",
}


def _schema(name: str) -> dict:
    return json.loads((SCHEMAS / f"gems-{name}.schema.json").read_text())


def _gems_yaml_files() -> list[tuple[str, Path]]:
    found = []
    for folder in ("libraries", "resources", "doc"):
        for path in sorted((ROOT / folder).rglob("*.yml")):
            if path.name == "system.yml":
                found.append(("system", path))
            elif path.name == "parameters.yml":
                found.append(("parameters", path))
            elif path.name == "optim-config.yml":
                found.append(("optim-config", path))
            elif "library" in (yaml.safe_load(path.read_text()) or {}):
                found.append(("library", path))
    return found


@pytest.mark.parametrize("name", sorted(p.name[5:-12] for p in SCHEMAS.glob("gems-*.schema.json")))
def test_schema_is_valid(name: str) -> None:
    jsonschema.Draft202012Validator.check_schema(_schema(name))


@pytest.mark.parametrize(
    ("kind", "path"),
    _gems_yaml_files(),
    ids=lambda v: str(v.relative_to(ROOT)) if isinstance(v, Path) else v,
)
def test_repository_yaml_matches_schema(kind: str, path: Path) -> None:
    if str(path.relative_to(ROOT)) in KNOWN_INVALID:
        pytest.xfail("known deviation from the language specification")
    data = yaml.safe_load(path.read_text())
    jsonschema.validate(data, _schema(kind))
