"""Tests of ``schemas/check_study.py`` on small synthetic studies."""

import importlib.util
import sys
from pathlib import Path

import pytest
import yaml

SCRIPT = Path(__file__).resolve().parents[2] / "schemas" / "check_study.py"
spec = importlib.util.spec_from_file_location("check_study", SCRIPT)
assert spec is not None and spec.loader is not None
check_study = importlib.util.module_from_spec(spec)
sys.modules["check_study"] = check_study
spec.loader.exec_module(check_study)

LIBRARY = {
    "library": {
        "id": "lib",
        "port-types": [{"id": "flow", "fields": [{"id": "f"}]}],
        "models": [
            {
                "id": "bus",
                "ports": [{"id": "p", "type": "flow"}],
                "binding-constraints": [
                    {"id": "balance", "expression": "sum_connections(p.f) = 0"}
                ],
            },
            {
                "id": "load",
                "parameters": [{"id": "load", "time-dependent": True, "scenario-dependent": False}],
                "ports": [{"id": "p", "type": "flow"}],
                "port-field-definitions": [{"port": "p", "field": "f", "definition": "-load"}],
                "properties": [{"id": "carrier"}],
            },
        ],
    }
}

SYSTEM = {
    "system": {
        "id": "s",
        "model-libraries": "lib",
        "components": [
            {"id": "bus", "model": "lib.bus"},
            {
                "id": "load",
                "model": "lib.load",
                "parameters": [
                    {
                        "id": "load",
                        "time-dependent": True,
                        "scenario-dependent": False,
                        "value": "demand",
                    }
                ],
                "properties": [{"id": "carrier", "value": "elec"}],
            },
        ],
        "connections": [{"component1": "bus", "port1": "p", "component2": "load", "port2": "p"}],
    }
}


def _write(root: Path, system: dict, library: dict = LIBRARY, series: bool = True) -> Path:
    (root / "input" / "model-libraries").mkdir(parents=True)
    (root / "input" / "data-series").mkdir()
    (root / "input" / "system.yml").write_text(yaml.safe_dump(system))
    (root / "input" / "model-libraries" / "lib.yml").write_text(yaml.safe_dump(library))
    if series:
        (root / "input" / "data-series" / "demand.csv").write_text("1\n2\n")
    return root


def _relationships(root: Path) -> set[str]:
    findings = check_study.check_study(root, schema=False)
    return {f.relationship for f in findings if f.severity == "error"}


def test_valid_study(tmp_path: Path) -> None:
    assert _relationships(_write(tmp_path, SYSTEM)) == set()


def test_missing_series(tmp_path: Path) -> None:
    root = _write(tmp_path, SYSTEM, series=False)
    assert _relationships(root) == {"component-parameter-value-is-series"}


@pytest.mark.parametrize(
    ("mutate", "expected"),
    [
        (lambda s: s["components"][1].update(model="lib.nope"), "component-instantiates-model"),
        (lambda s: s.update(**{"model-libraries": "other"}), "system-uses-library"),
        (lambda s: s["connections"][0].update(component2="ghost"), "connection-component"),
        (lambda s: s["connections"][0].update(port1="zzz"), "connection-port"),
        (
            lambda s: s["components"][1]["parameters"].append({"id": "x", "value": 1}),
            "component-parameter-declared",
        ),
        (lambda s: s["components"][1].pop("properties"), "component-property-declared"),
        (
            lambda s: s["components"][1]["parameters"][0].update(
                **{"time-dependent": False}, value="demand"
            ),
            "component-parameter-value-is-series",
        ),
    ],
)
def test_broken_reference(tmp_path: Path, mutate, expected: str) -> None:
    system = yaml.safe_load(yaml.safe_dump(SYSTEM))
    mutate(system["system"])
    assert expected in _relationships(_write(tmp_path, system))


def test_port_types_must_match(tmp_path: Path) -> None:
    library = yaml.safe_load(yaml.safe_dump(LIBRARY))
    library["library"]["port-types"].append({"id": "other", "fields": [{"id": "f"}]})
    library["library"]["models"][1]["ports"][0]["type"] = "other"
    library["library"]["models"][1]["port-field-definitions"][0]["port"] = "p"
    assert "connection-port-types-match" in _relationships(_write(tmp_path, SYSTEM, library))


def test_optim_config_unknown_element(tmp_path: Path) -> None:
    root = _write(tmp_path, SYSTEM)
    cfg = {
        "models": [
            {
                "id": "lib.bus",
                "out-of-bounds-processing": {"constraints": [{"id": "nope", "mode": "drop"}]},
            }
        ]
    }
    (root / "input" / "optim-config.yml").write_text(yaml.safe_dump(cfg))
    assert _relationships(root) == {"optim-config-constraint"}


def test_cli_exit_status(tmp_path: Path) -> None:
    root = _write(tmp_path, SYSTEM)
    assert check_study.main([str(root), "--no-schema"]) == 0
    (root / "input" / "data-series" / "demand.csv").unlink()
    assert check_study.main([str(root), "--no-schema"]) == 1
