"""Check the cross-file references of a GEMS study folder.

Usage::

    python schemas/check_study.py path/to/study [--json] [--no-schema]

The study folder holds ``parameters.yml`` and an ``input/`` directory (``system.yml``,
``optim-config.yml``, ``model-libraries/``, ``data-series/``, taxonomy / catalog / view files).

Each finding carries the id of the relationship (see ``gems-relationships.json``) it comes from.
Relationships marked ``derived`` there (expression names, time-scope coverage of data series) are
not checked here. Exit status is 1 when at least one error is found.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml

SCHEMAS_DIR = Path(__file__).resolve().parent
SERIES_EXTENSIONS = (".csv", ".txt", ".tsv")  # .csv for the Antares Modeler, .txt/.tsv for GemsPy


@dataclass(frozen=True)
class Finding:
    severity: str  # "error" | "warning"
    relationship: str
    file: str
    message: str


class Study:
    """The YAML files of a study, indexed by kind."""

    def __init__(self, root: Path, extra_dirs: tuple[Path, ...] = ()) -> None:
        self.root = root
        self.extra_dirs = extra_dirs
        self.input = root / "input" if (root / "input").is_dir() else root
        self.docs: dict[Path, Any] = {}
        self.extra_paths: set[Path] = set()
        self.libraries: list[tuple[Path, dict]] = []
        self.taxonomies: list[tuple[Path, dict]] = []
        self.catalogs: list[tuple[Path, dict]] = []
        self.views: list[tuple[Path, dict]] = []
        self.system: tuple[Path, dict] | None = None
        self.optim_config: tuple[Path, dict] | None = None
        self.parameters: tuple[Path, dict] | None = None
        self.parse_errors: list[Finding] = []
        self._load()

    def rel(self, path: Path) -> str:
        return str(path.relative_to(self.root)) if path.is_relative_to(self.root) else str(path)

    def _load(self) -> None:
        paths = sorted(self.root.rglob("*.yml"))
        extras = sorted(
            p for extra in self.extra_dirs for p in extra.rglob("*.yml") if p not in paths
        )
        self.extra_paths = set(extras)
        paths += extras
        for path in paths:
            try:
                doc = yaml.safe_load(path.read_text(encoding="utf-8"))
            except yaml.YAMLError as exc:
                self.parse_errors.append(
                    Finding("error", "yaml", self.rel(path), f"invalid YAML: {exc}")
                )
                continue
            self.docs[path] = doc
            if not isinstance(doc, dict):
                continue
            in_study = path.is_relative_to(self.root)
            if in_study and path.name == "system.yml" and "system" in doc:
                self.system = (path, doc["system"] or {})
            elif in_study and path.name == "optim-config.yml":
                self.optim_config = (path, doc)
            elif path == self.root / "parameters.yml":
                self.parameters = (path, doc)
            else:
                for key, bucket in (
                    ("library", self.libraries),
                    ("taxonomy", self.taxonomies),
                    ("catalog", self.catalogs),
                    ("view", self.views),
                ):
                    if isinstance(doc.get(key), dict):
                        bucket.append((path, doc[key]))

    def data_series_dir(self) -> Path:
        return self.input / "data-series"

    def scenario_groups(self) -> set[str] | None:
        path = self.data_series_dir() / "modeler-scenariobuilder.dat"
        if not path.is_file():
            return None
        groups = set()
        for line in path.read_text().splitlines():
            match = re.match(r"\s*([^,#=\s]+)\s*,\s*\d+\s*=\s*\d+", line)
            if match:
                groups.add(match.group(1))
        return groups


def _items(node: dict, key: str) -> list[dict]:
    value = node.get(key) or []
    return [x for x in value if isinstance(x, dict)]


def _ids(node: dict, key: str) -> set[str]:
    return {x.get("id") for x in _items(node, key) if "id" in x}


class Checker:
    def __init__(self, study: Study) -> None:
        self.study = study
        self.findings: list[Finding] = list(study.parse_errors)
        self.lib_by_id: dict[str, dict] = {}
        self.study.libraries = self._relevant_libraries()
        self.models: dict[str, dict] = {}  # "<library>.<model>" -> model
        self.port_types: dict[str, dict] = {}
        for _path, lib in study.libraries:
            if "id" in lib:
                self.lib_by_id[lib["id"]] = lib
            for model in _items(lib, "models"):
                self.models[f"{lib.get('id')}.{model.get('id')}"] = model
            for pt in _items(lib, "port-types"):
                self.port_types[pt.get("id")] = pt
        self.component_model: dict[str, str] = {}

    def _relevant_libraries(self) -> list[tuple[Path, dict]]:
        """Study libraries, plus those of extra folders that the system uses (study copy wins)."""
        own = [(p, lib) for p, lib in self.study.libraries if p not in self.study.extra_paths]
        wanted: set[str] = set()
        if self.study.system is not None:
            system = self.study.system[1]
            wanted |= {c.get("model", "").split(".", 1)[0] for c in _items(system, "components")}
            listed = system.get("model-libraries") or system.get("model_libraries") or ""
            wanted |= {x.strip() for x in listed.split(",") if x.strip()}
        have = {lib.get("id") for _, lib in own}
        extra = [
            (p, lib)
            for p, lib in self.study.libraries
            if p in self.study.extra_paths and lib.get("id") in wanted and lib.get("id") not in have
        ]
        return own + extra

    def add(self, severity: str, rel: str, path: Path | None, message: str) -> None:
        self.findings.append(Finding(severity, rel, self.study.rel(path) if path else "-", message))

    def error(self, rel: str, path: Path | None, message: str) -> None:
        self.add("error", rel, path, message)

    def warn(self, rel: str, path: Path | None, message: str) -> None:
        self.add("warning", rel, path, message)

    def run(self) -> list[Finding]:
        self.library_internal()
        self.system_checks()
        self.taxonomy_checks()
        self.catalog_and_view_checks()
        self.optim_config_checks()
        return self.findings

    # --- library -----------------------------------------------------------------------------
    def library_internal(self) -> None:
        if not self.study.libraries and self.study.system is not None:
            self.warn(
                "system-uses-library",
                None,
                "no model library found in the study folder; use --libs DIR for libraries kept elsewhere",
            )
        for path, lib in self.study.libraries:
            for model in _items(lib, "models"):
                mid = f"{lib.get('id')}.{model.get('id')}"
                ports = {p.get("id"): p for p in _items(model, "ports")}
                for port in ports.values():
                    if port.get("type") not in self.port_types:
                        self.error(
                            "port-uses-port-type",
                            path,
                            f"{mid}: port '{port.get('id')}' has unknown type '{port.get('type')}'",
                        )
                defined: dict[str, set[str]] = {}
                for pfd in _items(model, "port-field-definitions"):
                    port_id, field = pfd.get("port"), pfd.get("field")
                    if port_id not in ports:
                        self.error(
                            "port-field-definition-port",
                            path,
                            f"{mid}: port-field-definition refers to unknown port '{port_id}'",
                        )
                        continue
                    defined.setdefault(port_id, set()).add(field)
                    pt = self.port_types.get(ports[port_id].get("type"))
                    if pt is not None and field not in _ids(pt, "fields"):
                        self.error(
                            "port-field-definition-field",
                            path,
                            f"{mid}: port '{port_id}' (type '{pt.get('id')}') has no field '{field}'",
                        )
                for port_id, fields in defined.items():
                    pt = self.port_types.get(ports[port_id].get("type"))
                    missing = (_ids(pt, "fields") - fields) if pt else set()
                    if missing:
                        self.warn(
                            "port-field-definition-field",
                            path,
                            f"{mid}: port '{port_id}' does not define field(s) {sorted(missing)} (required by the docs, not enforced by GemsPy)",
                        )
            for pt in _items(lib, "port-types"):
                ac = pt.get("area-connection")
                if isinstance(ac, dict):
                    for key, field in ac.items():
                        if field is not None and field not in _ids(pt, "fields"):
                            self.error(
                                "hybrid-port-type-fields",
                                path,
                                f"port type '{pt.get('id')}': area-connection.{key} names unknown field '{field}'",
                            )
            if lib.get("taxonomy") and lib["taxonomy"] not in {
                t.get("id") for _, t in self.study.taxonomies
            }:
                report = self.error if self.study.taxonomies else self.warn
                report(
                    "library-taxonomy",
                    path,
                    f"library '{lib.get('id')}' refers to unknown taxonomy '{lib['taxonomy']}'",
                )

    # --- system ------------------------------------------------------------------------------
    def system_checks(self) -> None:
        if self.study.system is None:
            return
        path, system = self.study.system
        listed = [
            x.strip()
            for x in (system.get("model-libraries") or system.get("model_libraries") or "").split(
                ","
            )
            if x.strip()
        ]
        for lib_id in listed:
            if lib_id not in self.lib_by_id:
                self.error(
                    "system-uses-library",
                    path,
                    f"model-libraries lists '{lib_id}' but no such library was found",
                )
        series_dir = self.study.data_series_dir()
        groups = self.study.scenario_groups()
        components = {c.get("id"): c for c in _items(system, "components")}
        for cid, comp in components.items():
            model_ref = comp.get("model", "")
            model = self.models.get(model_ref)
            if model is None:
                self.error(
                    "component-instantiates-model",
                    path,
                    f"component '{cid}': unknown model '{model_ref}'",
                )
                continue
            self.component_model[cid] = model_ref
            lib_id = model_ref.split(".", 1)[0]
            if listed and lib_id not in listed:
                self.warn(
                    "component-instantiates-model",
                    path,
                    f"component '{cid}': library '{lib_id}' is not in model-libraries",
                )
            self.check_parameters(path, cid, comp, model, series_dir)
            declared_props = _ids(model, "properties")
            given_props = _ids(comp, "properties")
            for missing in sorted(declared_props - given_props):
                self.error(
                    "component-property-declared",
                    path,
                    f"component '{cid}': property '{missing}' declared by {model_ref} has no value",
                )
            if (
                comp.get("scenario-group")
                and groups is not None
                and comp["scenario-group"] not in groups
            ):
                self.error(
                    "component-scenario-group",
                    path,
                    f"component '{cid}': scenario-group '{comp['scenario-group']}' not found in modeler-scenariobuilder.dat",
                )
        for i, conn in enumerate(_items(system, "connections")):
            ptypes = []
            for side in ("1", "2"):
                cid, port_id = conn.get(f"component{side}"), conn.get(f"port{side}")
                if cid not in components:
                    self.error(
                        "connection-component", path, f"connection #{i}: unknown component '{cid}'"
                    )
                    ptypes.append(None)
                    continue
                model = self.models.get(self.component_model.get(cid, ""))
                port = (
                    next((p for p in _items(model, "ports") if p.get("id") == port_id), None)
                    if model
                    else None
                )
                if model is not None and port is None:
                    self.error(
                        "connection-port",
                        path,
                        f"connection #{i}: component '{cid}' ({self.component_model[cid]}) has no port '{port_id}'",
                    )
                ptypes.append(port.get("type") if port else None)
            if None not in ptypes and ptypes[0] != ptypes[1]:
                self.error(
                    "connection-port-types-match",
                    path,
                    f"connection #{i}: port types differ ('{ptypes[0]}' vs '{ptypes[1]}')",
                )
        self.hybrid_checks(path, system, components)
        self.integer_strategy_checks(path, components)

    def check_parameters(
        self,
        path: Path,
        cid: str,
        comp: dict,
        model: dict,
        series_dir: Path,
    ) -> None:
        mid = self.component_model[cid]
        declared = {p.get("id"): p for p in _items(model, "parameters")}
        given = {p.get("id"): p for p in _items(comp, "parameters")}
        for pid, p in given.items():
            decl = declared.get(pid)
            if decl is None:
                self.error(
                    "component-parameter-declared",
                    path,
                    f"component '{cid}': '{pid}' is not a parameter of {mid}",
                )
                continue
            for flag in ("time-dependent", "scenario-dependent"):
                if p.get(flag) and not decl.get(flag):
                    self.error(
                        "component-parameter-flags-within-model",
                        path,
                        f"component '{cid}', parameter '{pid}': {flag} is true but {mid} declares it false",
                    )
            dynamic = bool(p.get("time-dependent") or p.get("scenario-dependent"))
            value = p.get("value")
            if dynamic:
                if not isinstance(value, str) or not any(
                    (series_dir / f"{value}{ext}").is_file() for ext in SERIES_EXTENSIONS
                ):
                    self.error(
                        "component-parameter-value-is-series",
                        path,
                        f"component '{cid}', parameter '{pid}': data series '{value}' (.csv/.txt/.tsv) not found in {self.study.rel(series_dir)}",
                    )
            elif isinstance(value, str):
                self.error(
                    "component-parameter-value-is-series",
                    path,
                    f"component '{cid}', parameter '{pid}': value '{value}' must be a number when neither flag is true",
                )
        for pid in sorted(set(declared) - set(given)):
            self.error(
                "component-parameter-declared",
                path,
                f"component '{cid}': parameter '{pid}' of {mid} has no value",
            )

    def hybrid_checks(self, path: Path, system: dict, components: dict[str, dict]) -> None:
        for key in ("area-connections", "thermal-capacity-connections"):
            for i, entry in enumerate(_items(system, key)):
                cid, port_id = entry.get("component"), entry.get("port")
                model = self.models.get(self.component_model.get(cid, ""))
                if cid not in components:
                    self.error(
                        "hybrid-area-connection", path, f"{key}[{i}]: unknown component '{cid}'"
                    )
                elif model is not None:
                    port = next((p for p in _items(model, "ports") if p.get("id") == port_id), None)
                    if port is None:
                        self.error(
                            "hybrid-area-connection",
                            path,
                            f"{key}[{i}]: component '{cid}' has no port '{port_id}'",
                        )
                    else:
                        pt = self.port_types.get(port.get("type"), {})
                        needed = (
                            "area-connection"
                            if key == "area-connections"
                            else "thermal-capacity-connection"
                        )
                        if needed not in pt:
                            self.error(
                                "hybrid-area-connection"
                                if needed == "area-connection"
                                else "hybrid-thermal-connection",
                                path,
                                f"{key}[{i}]: port type '{port.get('type')}' declares no {needed}",
                            )

    def integer_strategy_checks(self, path: Path, components: dict[str, dict]) -> None:
        heuristics: dict[str, set[str]] = {}
        if self.study.optim_config is not None:
            for m in _items(self.study.optim_config[1], "models"):
                heuristics[m.get("id")] = {h.get("id") for h in _items(m, "heuristics")}
        for cid, comp in components.items():
            strategy = comp.get("integer-strategy")
            if isinstance(strategy, dict) and strategy.get("id") == "heuristic":
                model = self.component_model.get(cid)
                if model is None:
                    continue
                if strategy.get("heuristic-id") not in heuristics.get(model, set()):
                    report = self.error if self.study.optim_config is not None else self.warn
                    report(
                        "component-integer-strategy-heuristic",
                        path,
                        f"component '{cid}': no '{strategy.get('heuristic-id')}' heuristic configured for {model} in optim-config.yml",
                    )

    # --- taxonomy ----------------------------------------------------------------------------
    def used_models(self) -> dict[str, dict]:
        if self.study.system is None:
            return self.models
        used = set(self.component_model.values())
        return {k: v for k, v in self.models.items() if k in used}

    def taxonomy_checks(self) -> None:
        by_id = {t.get("id"): t for _, t in self.study.taxonomies}
        for path, tax in self.study.taxonomies:
            cats = _ids(tax, "categories")
            for cat in _items(tax, "categories"):
                parent = cat.get("parent-category")
                if parent and parent not in cats:
                    self.error(
                        "taxonomy-parent",
                        path,
                        f"category '{cat.get('id')}': unknown parent-category '{parent}'",
                    )
        for path, lib in self.study.libraries:
            tax = by_id.get(lib.get("taxonomy"))
            for model in _items(lib, "models"):
                cat_id = model.get("taxonomy-category")
                if cat_id is None:
                    continue
                mid = f"{lib.get('id')}.{model.get('id')}"
                if tax is None:
                    if self.study.taxonomies and lib.get("taxonomy") is None:
                        self.warn(
                            "model-taxonomy-category",
                            path,
                            f"{mid}: taxonomy-category '{cat_id}' but the library declares no taxonomy",
                        )
                    continue
                cat = next((c for c in _items(tax, "categories") if c.get("id") == cat_id), None)
                if cat is None:
                    self.error(
                        "model-taxonomy-category",
                        path,
                        f"{mid}: unknown taxonomy-category '{cat_id}'",
                    )
                    continue
                for key in (
                    "variables",
                    "parameters",
                    "ports",
                    "constraints",
                    "binding-constraints",
                    "extra-outputs",
                    "properties",
                ):
                    for missing in sorted(_ids(cat, key) - _ids(model, key)):
                        self.error(
                            "model-taxonomy-category",
                            path,
                            f"{mid}: category '{cat_id}' requires {key} '{missing}'",
                        )

    # --- catalog / view ----------------------------------------------------------------------
    def catalog_and_view_checks(self) -> None:
        taxes = {t.get("id"): t for _, t in self.study.taxonomies}
        metrics_by_catalog: dict[str, set[str]] = {}
        used = self.used_models()
        for path, cat in self.study.catalogs:
            metrics_by_catalog[cat.get("id")] = {
                m.get("id") for m in _items(cat, "metrics-definition")
            }
            tax = taxes.get(cat.get("taxonomy"))
            if tax is None:
                self.error(
                    "catalog-taxonomy",
                    path,
                    f"catalog '{cat.get('id')}': unknown taxonomy '{cat.get('taxonomy')}'",
                )
                continue
            cats = _ids(tax, "categories")
            loc = (cat.get("location") or {}).get("taxonomy-category")
            if loc not in cats:
                self.error(
                    "catalog-location-category", path, f"unknown location taxonomy-category '{loc}'"
                )
            for metric in _items(cat, "metrics-definition"):
                for term in _items(metric, "terms"):
                    tcat = term.get("taxonomy-category")
                    if tcat not in cats:
                        self.error(
                            "metric-term-category",
                            path,
                            f"metric '{metric.get('id')}': unknown taxonomy-category '{tcat}'",
                        )
                        continue
                    for mid, model in used.items():
                        if model.get("taxonomy-category") != tcat:
                            continue
                        if term.get("output-id") not in _ids(model, "extra-outputs"):
                            self.error(
                                "metric-term-output",
                                path,
                                f"metric '{metric.get('id')}': {mid} has no extra-output '{term.get('output-id')}'",
                            )
                        lp = term.get("location-ports")
                        if lp is not None and lp not in _ids(model, "ports"):
                            self.error(
                                "metric-term-location-port",
                                path,
                                f"metric '{metric.get('id')}': {mid} has no port '{lp}'",
                            )
        for path, view in self.study.views:
            listed = {c.get("id") for c in _items(view, "catalog")}
            for cid in sorted(listed - metrics_by_catalog.keys()):
                self.error(
                    "view-catalog", path, f"view '{view.get('id')}': unknown catalog '{cid}'"
                )
            for m in _items(view, "metrics"):
                cat_id, _, metric_id = str(m.get("id", "")).partition(".")
                if cat_id not in listed:
                    self.error(
                        "view-metric",
                        path,
                        f"metric '{m.get('id')}': catalog '{cat_id}' is not listed in view.catalog",
                    )
                elif cat_id in metrics_by_catalog and metric_id not in metrics_by_catalog[cat_id]:
                    self.error(
                        "view-metric",
                        path,
                        f"metric '{m.get('id')}': catalog '{cat_id}' defines no metric '{metric_id}'",
                    )
            all_cats = (
                set().union(*(_ids(t, "categories") for t in taxes.values())) if taxes else set()
            )
            for scope in _items(view, "scope"):
                loc = (
                    (scope.get("location") or {}).get("taxonomy-category")
                    if isinstance(scope.get("location"), dict)
                    else None
                )
                if loc and taxes and loc not in all_cats:
                    self.error(
                        "view-location-category",
                        path,
                        f"unknown location taxonomy-category '{loc}'",
                    )
                cal = scope.get("calendar")
                if cal and not (self.study.input / f"{cal}.csv").is_file():
                    self.error(
                        "view-calendar",
                        path,
                        f"calendar file '{cal}.csv' not found in {self.study.rel(self.study.input)}",
                    )

    # --- optim-config ------------------------------------------------------------------------
    def optim_config_checks(self) -> None:
        if self.study.optim_config is None:
            return
        path, cfg = self.study.optim_config
        playlist = (cfg.get("scenario-scope") or {}).get("playlist-file")
        if playlist and not (path.parent / playlist).is_file():
            self.error("scenario-scope-playlist", path, f"playlist-file '{playlist}' not found")
        used = set(self.component_model.values())
        for entry in _items(cfg, "models"):
            mid = entry.get("id")
            model = self.models.get(mid)
            if model is None:
                self.error("optim-config-model", path, f"unknown model '{mid}'")
                continue
            if self.study.system is not None and mid not in used:
                self.error(
                    "optim-config-model",
                    path,
                    f"model '{mid}' is not instantiated by any component",
                )
            for c in _items(entry.get("out-of-bounds-processing") or {}, "constraints"):
                self.require(
                    path,
                    "optim-config-constraint",
                    mid,
                    "constraint",
                    c.get("id"),
                    _ids(model, "constraints") | _ids(model, "binding-constraints"),
                )
            decomp = entry.get("model-decomposition") or {}
            for c in _items(decomp, "constraints"):
                self.require(
                    path,
                    "optim-config-constraint",
                    mid,
                    "constraint",
                    c.get("id"),
                    _ids(model, "constraints") | _ids(model, "binding-constraints"),
                )
            for v in _items(decomp, "variables"):
                self.require(
                    path,
                    "optim-config-variable",
                    mid,
                    "variable",
                    v.get("id"),
                    _ids(model, "variables"),
                )
            for o in _items(decomp, "objective-contributions"):
                self.require(
                    path,
                    "optim-config-objective",
                    mid,
                    "objective contribution",
                    o.get("id"),
                    _ids(model, "objective-contributions"),
                )
            for h in _items(entry, "heuristics"):
                for el in _items(h, "inputs") + _items(h, "outputs"):
                    kind = el.get("type", "parameter")
                    pool = (
                        _ids(model, "parameters")
                        if kind == "parameter"
                        else _ids(model, "variables")
                    )
                    self.require(
                        path, "optim-config-heuristic-element", mid, kind, el.get("id"), pool
                    )

    def require(
        self, path: Path, rel: str, model: str, what: str, ident: str | None, pool: set[str]
    ) -> None:
        if ident not in pool:
            self.error(rel, path, f"model '{model}' has no {what} '{ident}'")


def schema_findings(study: Study) -> list[Finding]:
    """Validate each file against its JSON Schema (requires ``jsonschema``)."""
    try:
        import jsonschema
    except ImportError:
        return [
            Finding(
                "warning", "schema", "-", "jsonschema not installed: structural validation skipped"
            )
        ]
    out: list[Finding] = []

    def validate(kind: str, path: Path, doc: Any) -> None:
        schema = json.loads((SCHEMAS_DIR / f"gems-{kind}.schema.json").read_text())
        for err in jsonschema.Draft202012Validator(schema).iter_errors(doc):
            where = "/".join(map(str, err.absolute_path)) or "<root>"
            out.append(Finding("error", "schema", study.rel(path), f"{where}: {err.message[:160]}"))

    for kind, bucket in (
        ("library", study.libraries),
        ("taxonomy", study.taxonomies),
        ("catalog", study.catalogs),
        ("view-config", study.views),
    ):
        for path, _ in bucket:
            validate(kind, path, study.docs[path])
    for kind, item in (
        ("system", study.system),
        ("optim-config", study.optim_config),
        ("parameters", study.parameters),
    ):
        if item is not None:
            validate(kind, item[0], study.docs[item[0]])
    return out


def check_study(root: Path, schema: bool = True, libs: tuple[Path, ...] = ()) -> list[Finding]:
    study = Study(root, libs)
    findings = Checker(study).run()
    if schema:
        findings = schema_findings(study) + findings
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("study", type=Path, help="root folder of the study")
    parser.add_argument("--json", action="store_true", help="print findings as JSON")
    parser.add_argument(
        "--libs",
        type=Path,
        action="append",
        default=[],
        metavar="DIR",
        help="extra folder holding model libraries / taxonomies kept outside the study (repeatable)",
    )
    parser.add_argument(
        "--no-schema", action="store_true", help="skip JSON Schema validation of each file"
    )
    args = parser.parse_args(argv)
    if not args.study.is_dir():
        sys.stderr.write(f"not a directory: {args.study}\n")
        return 2
    findings = check_study(args.study, schema=not args.no_schema, libs=tuple(args.libs))
    if args.json:
        sys.stdout.write(json.dumps([asdict(f) for f in findings], indent=2) + "\n")
    else:
        for f in findings:
            sys.stdout.write(f"{f.severity.upper():7} [{f.relationship}] {f.file}: {f.message}\n")
        errors = sum(f.severity == "error" for f in findings)
        sys.stdout.write(f"{errors} error(s), {len(findings) - errors} warning(s)\n")
    return 1 if any(f.severity == "error" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
