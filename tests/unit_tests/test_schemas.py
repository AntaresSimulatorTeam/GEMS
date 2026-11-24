"""Conformance of the JSON Schemas in `schemas/` (see schemas/README.md).

Runs the conformance corpus and validates the real files of this repository (`libraries/`, `resources/`)
through the same runner as `tools/run_conformance.py`.
"""

import importlib.util
import sys
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[2]


def _load_runner() -> Any:
    spec = importlib.util.spec_from_file_location(
        "run_conformance", ROOT / "tools" / "run_conformance.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses look the module up by name
    spec.loader.exec_module(module)
    return module


runner = _load_runner()


def test_schemas_are_valid_draft_2020_12() -> None:
    assert set(runner.build_validators()) == set(runner.KINDS)


def test_conformance_corpus_behaves_as_declared() -> None:
    results = runner.run_corpus(runner.build_validators())
    failures = [f"{r.label}: {r.detail}" for r in results if not r.ok]
    assert not failures, "\n".join(failures)


def test_real_files_of_this_repository_validate() -> None:
    if not runner.KINDS:
        pytest.skip("no kind schema yet")
    runner.UPSTREAM_DIR = ROOT
    runner.PRIMARY_REPOS, runner.OTHER_REPOS = ("libraries", "resources"), ()
    results, _ = runner.run_real(runner.build_validators())
    assert results, "no real file was found"
    failures = [f"{r.label}: {r.detail}" for r in results if not r.ok]
    assert not failures, "\n".join(failures)


@pytest.mark.parametrize("name", ["common", *runner.KINDS])
def test_schema_files_declare_id_and_version(name: str) -> None:
    doc = runner.load_yaml(ROOT / "schemas" / f"{name}.schema.yml")
    assert doc["$id"].endswith(f"/{name}.schema.yml")
    assert doc["x-schema-version"]
