"""
Tests for mathematical expression syntax in GEMS model library files.

Validates:
  - Constraints have exactly one comparison operator (=, <=, >=)
  - All identifiers in expressions resolve to known parameters or variables
  - Variable bound expressions only reference parameters (not decision variables)
  - No direct port.field references in constraint expressions (use sum_connections())
  - Port-field definitions reference valid port and field IDs
  - sum_connections() calls reference valid port.field pairs
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
LIBRARIES_DIR = REPO_ROOT / "libraries"

# Tokens valid in expressions that are not model identifiers.
# Includes built-in functions: sum, sum_connections, min, max, ceil, floor, expec
# and the time index keyword: t
_KEYWORDS = frozenset({"sum", "sum_connections", "min", "max", "ceil", "floor", "expec", "t"})


# ---------------------------------------------------------------------------
# Expression helpers
# ---------------------------------------------------------------------------


def _strip_sum_connections(expression: str) -> str:
    """Remove sum_connections(port.field) tokens before identifier extraction.

    Port and field IDs inside sum_connections are not parameters or variables,
    so they must be excluded from identifier validation.
    """
    return re.sub(
        r"sum_connections\(\s*[a-zA-Z_][a-zA-Z0-9_]*\s*\.\s*[a-zA-Z_][a-zA-Z0-9_]*\s*\)",
        "",
        expression,
    )


def _extract_identifiers(expression: Any) -> set[str]:
    """Extract non-keyword word tokens from an expression string."""
    cleaned = _strip_sum_connections(str(expression))
    tokens = re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", cleaned)
    return {tok for tok in tokens if tok not in _KEYWORDS}


def _count_comparisons(expression: Any) -> int:
    """Count comparison operators (<=, >=, standalone =) in an expression."""
    return len(re.findall(r"<=|>=|(?<![<>])=", str(expression)))


def _extract_sum_connections_refs(expression: Any) -> list[tuple[str, str]]:
    """Return (port_id, field_id) pairs for every sum_connections() call."""
    return re.findall(
        r"sum_connections\(\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\.\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\)",
        str(expression),
    )


# ---------------------------------------------------------------------------
# Library loading and model introspection
# ---------------------------------------------------------------------------


def _load_libraries() -> list[tuple[str, dict[str, Any]]]:
    """Return list of (filename, library_dict) for all library YAML files."""
    result = []
    for lib_file in sorted(LIBRARIES_DIR.glob("*.yml")):
        with lib_file.open("r", encoding="utf-8") as fh:
            raw = yaml.safe_load(fh)
        if raw and "library" in raw:
            result.append((lib_file.name, raw["library"]))
    return result


def _known_ids(model: dict[str, Any]) -> frozenset[str]:
    """Return all parameter and variable IDs defined in a model."""
    params = {p["id"] for p in model.get("parameters") or []}
    variables = {v["id"] for v in model.get("variables") or []}
    return frozenset(params | variables)


def _param_ids(model: dict[str, Any]) -> frozenset[str]:
    """Return only parameter IDs defined in a model (not decision variables).

    Used for bound expression validation: per the GEMS spec, variable bounds
    must only reference parameters and constants, not decision variables.
    """
    return frozenset(p["id"] for p in model.get("parameters") or [])


def _port_field_ids(library: dict[str, Any], port_type_id: str) -> frozenset[str]:
    """Return field IDs for a port-type in a library."""
    for pt in library.get("port-types") or []:
        if pt["id"] == port_type_id:
            return frozenset(f["id"] for f in pt.get("fields") or [])
    return frozenset()


def _port_type_of(model: dict[str, Any], port_id: str) -> str | None:
    """Return the port-type ID for a given port in a model."""
    for port in model.get("ports") or []:
        if port["id"] == port_id:
            value = port.get("type")
            return str(value) if value is not None else None
    return None


# ---------------------------------------------------------------------------
# Test-case builders  (evaluated once at collection time)
# ---------------------------------------------------------------------------

_LIBRARIES: list[tuple[str, dict[str, Any]]] = _load_libraries()


def _constraint_cases() -> list[tuple[str, str, str, Any]]:
    """(lib_name, model_id, constraint_id, expression) for every constraint."""
    cases = []
    for lib_name, library in _LIBRARIES:
        for model in library.get("models") or []:
            for section in ("constraints", "binding-constraints"):
                for c in model.get(section) or []:
                    cases.append((lib_name, model["id"], c["id"], c["expression"]))
    return cases


def _expression_cases() -> list[tuple[str, str, str, Any, frozenset[str]]]:
    """(lib_name, model_id, location_label, expression, known_ids) for expressions
    that may reference both parameters and variables.

    Variable bounds are intentionally excluded — they are tested separately in
    test_variable_bound_uses_only_parameters, which enforces the stricter rule
    that bounds must only reference parameters (not decision variables).
    """
    cases = []
    for lib_name, library in _LIBRARIES:
        for model in library.get("models") or []:
            known = _known_ids(model)
            model_id = model["id"]

            for section in ("constraints", "binding-constraints"):
                for c in model.get(section) or []:
                    cases.append(
                        (lib_name, model_id, f"{section}[{c['id']}]", c["expression"], known)
                    )

            for oc in model.get("objective-contributions") or []:
                cases.append(
                    (lib_name, model_id, f"objective[{oc['id']}]", oc["expression"], known)
                )

            for pfd in model.get("port-field-definitions") or []:
                label = f"port-field-definitions[{pfd['port']}.{pfd['field']}]"
                cases.append((lib_name, model_id, label, pfd["definition"], known))

    return cases


def _bound_expression_cases() -> list[tuple[str, str, str, Any, frozenset[str]]]:
    """(lib_name, model_id, label, expression, param_ids) for every variable bound expression.

    Per the GEMS spec, variable bounds may only reference parameters and constants —
    not decision variables — because bounds are fixed at problem-construction time.
    """
    cases = []
    for lib_name, library in _LIBRARIES:
        for model in library.get("models") or []:
            params_only = _param_ids(model)
            model_id = model["id"]
            for var in model.get("variables") or []:
                for bound in ("lower-bound", "upper-bound"):
                    val = var.get(bound)
                    if val is not None and not isinstance(val, (int, float)):
                        label = f"variables[{var['id']}].{bound}"
                        cases.append((lib_name, model_id, label, val, params_only))
    return cases


def _direct_port_ref_cases() -> list[tuple[str, str, str, Any, frozenset[str]]]:
    """(lib_name, model_id, location, expression, model_port_ids) for all constraint
    expressions in models that declare at least one port.

    Only models with ports are included — models without ports cannot have
    direct port field references.
    """
    cases = []
    for lib_name, library in _LIBRARIES:
        for model in library.get("models") or []:
            model_port_ids = frozenset(p["id"] for p in model.get("ports") or [])
            if not model_port_ids:
                continue
            for section in ("constraints", "binding-constraints"):
                for c in model.get(section) or []:
                    label = f"{section}[{c['id']}]"
                    cases.append((lib_name, model["id"], label, c["expression"], model_port_ids))
    return cases


def _port_field_def_cases() -> list[tuple[str, str, str, str, frozenset[str], frozenset[str]]]:
    """(lib_name, model_id, pfd_port, pfd_field, model_port_ids, valid_field_ids)."""
    cases = []
    for lib_name, library in _LIBRARIES:
        for model in library.get("models") or []:
            model_port_ids = frozenset(p["id"] for p in model.get("ports") or [])
            for pfd in model.get("port-field-definitions") or []:
                pt_id = _port_type_of(model, pfd["port"])
                valid_fields = _port_field_ids(library, pt_id) if pt_id else frozenset()
                cases.append(
                    (
                        lib_name,
                        model["id"],
                        pfd["port"],
                        pfd["field"],
                        model_port_ids,
                        valid_fields,
                    )
                )
    return cases


def _sum_connections_cases() -> list[
    tuple[str, str, str, str, str, frozenset[str], frozenset[str]]
]:
    """(lib_name, model_id, constraint_id, port_id, field_id, model_port_ids, valid_field_ids)."""
    cases = []
    for lib_name, library in _LIBRARIES:
        for model in library.get("models") or []:
            model_port_ids = frozenset(p["id"] for p in model.get("ports") or [])
            for section in ("constraints", "binding-constraints"):
                for c in model.get(section) or []:
                    for port_id, field_id in _extract_sum_connections_refs(c["expression"]):
                        pt_id = _port_type_of(model, port_id)
                        valid_fields = _port_field_ids(library, pt_id) if pt_id else frozenset()
                        cases.append(
                            (
                                lib_name,
                                model["id"],
                                c["id"],
                                port_id,
                                field_id,
                                model_port_ids,
                                valid_fields,
                            )
                        )
    return cases


_CONSTRAINT_CASES = _constraint_cases()
_EXPRESSION_CASES = _expression_cases()
_BOUND_EXPRESSION_CASES = _bound_expression_cases()
_DIRECT_PORT_REF_CASES = _direct_port_ref_cases()
_PORT_FIELD_DEF_CASES = _port_field_def_cases()
_SUM_CONNECTIONS_CASES = _sum_connections_cases()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "lib_name, model_id, constraint_id, expression",
    _CONSTRAINT_CASES,
    ids=[f"{c[0]}::{c[1]}::{c[2]}" for c in _CONSTRAINT_CASES],
)
def test_constraint_has_single_comparison(
    lib_name: str,
    model_id: str,
    constraint_id: str,
    expression: Any,
) -> None:
    """Every constraint expression must contain exactly one comparison operator."""
    count = _count_comparisons(expression)
    assert count == 1, (
        f"{lib_name} / model '{model_id}' / constraint '{constraint_id}': "
        f"expected exactly 1 comparison operator (=, <=, >=), found {count} "
        f"in: {expression!r}"
    )


@pytest.mark.parametrize(
    "lib_name, model_id, location, expression, known",
    _EXPRESSION_CASES,
    ids=[f"{c[0]}::{c[1]}::{c[2]}" for c in _EXPRESSION_CASES],
)
def test_expression_identifiers_are_defined(
    lib_name: str,
    model_id: str,
    location: str,
    expression: Any,
    known: frozenset[str],
) -> None:
    """Every identifier in an expression must be a declared parameter or variable."""
    used = _extract_identifiers(expression)
    undefined = used - known
    assert not undefined, (
        f"{lib_name} / model '{model_id}' / {location}: "
        f"undefined identifier(s) {sorted(undefined)!r} in expression: {expression!r}\n"
        f"Declared identifiers: {sorted(known)!r}"
    )


@pytest.mark.parametrize(
    "lib_name, model_id, label, expression, param_ids",
    _BOUND_EXPRESSION_CASES,
    ids=[f"{c[0]}::{c[1]}::{c[2]}" for c in _BOUND_EXPRESSION_CASES],
)
def test_variable_bound_uses_only_parameters(
    lib_name: str,
    model_id: str,
    label: str,
    expression: Any,
    param_ids: frozenset[str],
) -> None:
    """Variable bound expressions must only reference parameters, not decision variables.

    Bounds are fixed at problem-construction time, so they cannot depend on
    the values of decision variables.
    """
    used = _extract_identifiers(expression)
    non_params = used - param_ids
    assert not non_params, (
        f"{lib_name} / model '{model_id}' / {label}: "
        f"bound expression may only reference parameters, but found non-parameter "
        f"identifier(s) {sorted(non_params)!r} in: {expression!r}. "
        f"Declared parameters: {sorted(param_ids)!r}"
    )


@pytest.mark.parametrize(
    "lib_name, model_id, location, expression, model_port_ids",
    _DIRECT_PORT_REF_CASES,
    ids=[f"{c[0]}::{c[1]}::{c[2]}" for c in _DIRECT_PORT_REF_CASES],
)
def test_no_direct_port_field_in_constraints(
    lib_name: str,
    model_id: str,
    location: str,
    expression: Any,
    model_port_ids: frozenset[str],
) -> None:
    """Constraint expressions must not reference port fields directly.

    Direct port field usage (e.g. balance_port.flow) in a constraint is not
    permitted. Use sum_connections(balance_port.flow) instead, even when only
    a single component is connected to the port.
    """
    cleaned = _strip_sum_connections(str(expression))
    refs = re.findall(r"([a-zA-Z_][a-zA-Z0-9_]*)\.([a-zA-Z_][a-zA-Z0-9_]*)", cleaned)
    invalid = [f"{port_id}.{field_id}" for port_id, field_id in refs if port_id in model_port_ids]
    assert not invalid, (
        f"{lib_name} / model '{model_id}' / {location}: "
        f"direct port field reference(s) {invalid!r} are not allowed in constraint "
        f"expressions. Use sum_connections() instead."
    )


@pytest.mark.parametrize(
    "lib_name, model_id, pfd_port, pfd_field, model_port_ids, valid_fields",
    _PORT_FIELD_DEF_CASES,
    ids=[f"{c[0]}::{c[1]}::{c[2]}.{c[3]}" for c in _PORT_FIELD_DEF_CASES],
)
def test_port_field_definition_references_valid_port_and_field(
    lib_name: str,
    model_id: str,
    pfd_port: str,
    pfd_field: str,
    model_port_ids: frozenset[str],
    valid_fields: frozenset[str],
) -> None:
    """Port-field definitions must reference a port declared in the model,
    and a field declared on that port's type."""
    assert pfd_port in model_port_ids, (
        f"{lib_name} / model '{model_id}': port-field-definition references "
        f"port '{pfd_port}' which is not declared in this model. "
        f"Declared ports: {sorted(model_port_ids)!r}"
    )
    if valid_fields:
        assert pfd_field in valid_fields, (
            f"{lib_name} / model '{model_id}': port-field-definition on port "
            f"'{pfd_port}' references field '{pfd_field}', "
            f"but valid fields for this port type are: {sorted(valid_fields)!r}"
        )


@pytest.mark.parametrize(
    "lib_name, model_id, constraint_id, port_id, field_id, model_port_ids, valid_fields",
    _SUM_CONNECTIONS_CASES,
    ids=[f"{c[0]}::{c[1]}::{c[2]}::sum_connections({c[3]}.{c[4]})" for c in _SUM_CONNECTIONS_CASES],
)
def test_sum_connections_references_valid_port_and_field(
    lib_name: str,
    model_id: str,
    constraint_id: str,
    port_id: str,
    field_id: str,
    model_port_ids: frozenset[str],
    valid_fields: frozenset[str],
) -> None:
    """sum_connections() must reference a port declared in the model,
    and a field declared on that port's type."""
    assert port_id in model_port_ids, (
        f"{lib_name} / model '{model_id}' / constraint '{constraint_id}': "
        f"sum_connections() references port '{port_id}' which is not declared "
        f"in this model. Declared ports: {sorted(model_port_ids)!r}"
    )
    if valid_fields:
        assert field_id in valid_fields, (
            f"{lib_name} / model '{model_id}' / constraint '{constraint_id}': "
            f"sum_connections() references field '{field_id}' on port '{port_id}', "
            f"but valid fields for this port type are: {sorted(valid_fields)!r}"
        )
