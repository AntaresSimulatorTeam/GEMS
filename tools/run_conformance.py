#!/usr/bin/env python3
"""Conformance runner for the GEMS input-file schemas.

    python tools/run_conformance.py                # schema self-check + conformance corpus
    python tools/run_conformance.py --real         # + real example files from upstream/ clones

Only `jsonschema` and `PyYAML` are used, and YAML is read with `yaml.safe_load` exclusively.
Nothing from the cloned repositories is imported or executed; their files are only read as data.
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS_DIR = ROOT / "schemas"
# Layout of the GEMS repository keeps the corpus under schemas/conformance; this workspace keeps it at the top.
CORPUS_DIR = SCHEMAS_DIR / "conformance" if (SCHEMAS_DIR / "conformance").is_dir() else ROOT / "conformance"
UPSTREAM_DIR = ROOT / "upstream"
KNOWN_REAL = CORPUS_DIR / "real-examples-known.yml"

ALL_KINDS = ("model-library", "system", "optim-config", "system-for-view", "taxonomy", "catalog", "view-config")
# Only the kinds whose schema file exists are checked, so that the schemas can be added one at a time.
KINDS = tuple(k for k in ALL_KINDS if (SCHEMAS_DIR / f"{k}.schema.yml").is_file())
# Repos whose real files must validate (authoritative sources) vs. the others (informational).
PRIMARY_REPOS = ("GEMS", "GemsPy")
OTHER_REPOS = ("Antares_Simulator", "AntaREST", "GEMS-ViewsBuilder", "PyPSA-to-GEMS-Converter")


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_validators() -> dict[str, Draft202012Validator]:
    docs = {p.name: load_yaml(p) for p in sorted(SCHEMAS_DIR.glob("*.schema.yml"))}
    registry = Registry()
    for name, doc in docs.items():
        Draft202012Validator.check_schema(doc)  # the schema itself must be a valid draft 2020-12 schema
        registry = registry.with_resource(doc["$id"], Resource(doc, DRAFT202012))
    return {
        kind: Draft202012Validator(docs[f"{kind}.schema.yml"], registry=registry)
        for kind in KINDS
    }


def flatten(err: ValidationError) -> Iterator[ValidationError]:
    yield err
    for sub in err.context or ():
        yield from flatten(sub)


def pointer(err: ValidationError) -> str:
    return "".join(f"/{p}" for p in err.absolute_path)


def errors_of(validator: Draft202012Validator, instance: Any) -> list[ValidationError]:
    out: list[ValidationError] = []
    for err in validator.iter_errors(instance):
        out.extend(flatten(err))
    return out


@dataclass
class Result:
    label: str
    ok: bool
    detail: str = ""


# ---------------------------------------------------------------- conformance corpus
def run_corpus(validators: dict[str, Draft202012Validator]) -> list[Result]:
    results: list[Result] = []
    for kind in KINDS:
        manifest_path = CORPUS_DIR / kind / "manifest.yml"
        manifest = load_yaml(manifest_path)
        cases = manifest["cases"]
        listed = {c["file"] for c in cases}
        on_disk = {
            str(p.relative_to(CORPUS_DIR / kind))
            for p in (CORPUS_DIR / kind).rglob("*.yml")
            if p.name != "manifest.yml"
        }
        for stray in sorted(on_disk - listed):
            results.append(Result(f"{kind}/{stray}", False, "file is not listed in manifest.yml"))
        for case in cases:
            label = f"{kind}/{case['file']}"
            path = CORPUS_DIR / kind / case["file"]
            if not path.is_file():
                results.append(Result(label, False, "listed file does not exist"))
                continue
            instance = load_yaml(path)
            errs = errors_of(validators[kind], instance)
            if case["valid"]:
                if errs:
                    first = errs[0]
                    results.append(
                        Result(label, False, f"expected valid, got {pointer(first)!r}: {first.message[:140]}")
                    )
                else:
                    results.append(Result(label, True))
                continue
            expect = case.get("expect")
            if not expect or "path" not in expect or not case.get("reason"):
                results.append(Result(label, False, "invalid case needs `expect.path` and `reason` in manifest"))
                continue
            if not errs:
                results.append(Result(label, False, "expected invalid, but the file validates"))
                continue
            matching = [
                e
                for e in errs
                if pointer(e) == expect["path"]
                and ("keyword" not in expect or e.validator == expect["keyword"])
            ]
            if matching:
                results.append(Result(label, True))
            else:
                seen = sorted({f"{pointer(e) or '/'} [{e.validator}]" for e in errs})[:6]
                results.append(
                    Result(
                        label,
                        False,
                        f"no error at {expect['path']!r}"
                        + (f" with keyword {expect['keyword']!r}" if "keyword" in expect else "")
                        + f"; got {seen}",
                    )
                )
    return results


# ---------------------------------------------------------------- real example files
def classify(path: Path, instance: Any) -> str | None:
    name = path.name
    if name in ("system-for-views.yml", "system-for-view.yml"):
        return "system-for-view"
    if name == "optim-config.yml" or "optim-config" in path.parent.parts:
        return "optim-config"
    if isinstance(instance, dict) and set(instance) == {"library"}:
        return "model-library"
    if isinstance(instance, dict) and set(instance) == {"system"}:
        return "system"
    if isinstance(instance, dict) and len(instance) == 1:
        # GEMS ViewsBuilder inputs: taxonomy.yml, catalog files, view configuration files.
        for root in ("taxonomy", "catalog", "view"):
            if root in instance:
                return "view-config" if root == "view" else root
    return None


def discover_real(repos: tuple[str, ...]) -> tuple[list[tuple[str, Path, str]], list[Path]]:
    found: list[tuple[str, Path, str]] = []
    dangling: list[Path] = []
    seen: set[Path] = set()
    for repo in repos:
        base = UPSTREAM_DIR / repo
        if not base.is_dir():
            continue
        for p in sorted(base.rglob("*")):
            if p.suffix not in (".yml", ".yaml") or any(x in p.parts for x in (".git", ".github", "node_modules")):
                continue
            if p.is_symlink() and not p.exists():
                dangling.append(p)
                continue
            real = p.resolve()
            if real in seen:
                continue
            seen.add(real)
            try:
                instance = load_yaml(p)
            except yaml.YAMLError:
                continue
            kind = classify(p, instance)
            if kind:
                found.append((repo, p, kind))
    return found, dangling


def run_real(validators: dict[str, Draft202012Validator]) -> tuple[list[Result], list[str]]:
    known = load_yaml(KNOWN_REAL) or {}
    known_files: dict[str, dict] = {e["file"]: e for e in known.get("known_failures", [])}
    results: list[Result] = []
    report: list[str] = []
    still_failing: set[str] = set()
    for group, repos in (("primary", PRIMARY_REPOS), ("other", OTHER_REPOS)):
        found, dangling = discover_real(repos)
        report.append(f"[{group}] {len(found)} real files classified, {len(dangling)} dangling symlinks skipped")
        for d in dangling:
            report.append(f"    skipped dangling symlink: {d.relative_to(UPSTREAM_DIR)}")
        for repo, p, kind in found:
            if kind not in validators:
                continue
            rel = str(p.relative_to(UPSTREAM_DIR))
            errs = errors_of(validators[kind], load_yaml(p))
            if not errs:
                if rel in known_files:
                    results.append(Result(rel, False, "listed as known failure but now validates: update real-examples-known.yml"))
                else:
                    results.append(Result(rel, True))
                continue
            still_failing.add(rel)
            first = min(errs, key=lambda e: len(list(e.absolute_path)))
            msg = f"[{kind}] {pointer(first) or '/'}: {first.message[:120]}"
            if rel in known_files:
                results.append(Result(rel, True, f"KNOWN FAILURE ({known_files[rel]['class']}, {known_files[rel]['ref']}): {msg}"))
            else:
                results.append(Result(rel, False, f"UNEXPECTED FAILURE {msg}"))
    for rel in known_files:
        if rel not in still_failing and not any(r.label == rel for r in results):
            results.append(Result(rel, False, "listed as known failure but file not found"))
    return results, report


def main() -> int:
    global UPSTREAM_DIR, PRIMARY_REPOS, OTHER_REPOS
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--real", action="store_true", help="also validate real example files from upstream/ clones")
    ap.add_argument("-v", "--verbose", action="store_true", help="print passing cases too")
    ap.add_argument("--real-root", type=Path, help="directory holding the repositories to scan (default: upstream/)")
    ap.add_argument("--repos", nargs="+", help="sub-directories of --real-root to scan; all of them must validate (use '.' for the root itself)")
    args = ap.parse_args()
    if args.real_root:
        UPSTREAM_DIR = args.real_root.resolve()
    if args.repos:
        PRIMARY_REPOS, OTHER_REPOS = tuple(args.repos), ()

    validators = build_validators()
    print(f"schemas OK: {', '.join(KINDS)} (draft 2020-12 metaschema check passed)")

    failed = 0
    corpus = run_corpus(validators)
    for r in corpus:
        if not r.ok or args.verbose:
            print(("PASS " if r.ok else "FAIL ") + r.label + (f"  -- {r.detail}" if r.detail else ""))
    bad = [r for r in corpus if not r.ok]
    failed += len(bad)
    print(f"corpus: {len(corpus) - len(bad)}/{len(corpus)} cases behave as declared")

    if args.real:
        real, report = run_real(validators)
        for line in report:
            print(line)
        known = [r for r in real if r.ok and r.detail]
        for r in real:
            if not r.ok:
                print(f"FAIL {r.label}  -- {r.detail}")
            elif r.detail:
                print(f"KNOWN {r.label}  -- {r.detail}")
            elif args.verbose:
                print(f"PASS {r.label}")
        bad_real = [r for r in real if not r.ok]
        failed += len(bad_real)
        clean = [r for r in real if r.ok and not r.detail]
        print(f"real files: {len(clean)} validate, {len(known)} known failures (documented), {len(bad_real)} unexpected")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
