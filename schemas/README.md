# GEMS input-file schemas (draft 0.1.0)

JSON Schemas (draft 2020-12), authored in YAML, meant to be the single source of truth for validating
GEMS input files in all the Antares projects. **Status: first draft for review.** Only the GEMS unit tests run these
schemas; no other project uses them yet.

| Schema | Validates | Status |
|---|---|---|
| `schemas/model-library.schema.yml` | `input/model-libraries/*.yml`, `libraries/*.yml` | draft |
| `schemas/common.schema.yml` | shared `$defs`, referenced with `$ref` | draft |

## Layout

```text
schemas/                 the schemas (*.schema.yml), one per file kind + common
schemas/conformance/
  <kind>/valid/          files that must validate
  <kind>/invalid/        files that must fail
  <kind>/manifest.yml    per file: valid?, source (real file + commit, or hand-written), and for invalid
                         files the expected failing JSON-pointer path, keyword and reason
  real-examples-known.yml  real files of this repository that do not validate, with class and reason
schemas/DISCREPANCIES.md what each project treats as mandatory / optional / different, with file:line
schemas/NOT_COVERED.md   rules JSON Schema cannot express, and where the schemas are looser/stricter
tools/run_conformance.py the runner (jsonschema + PyYAML, yaml.safe_load only)
tests/unit_tests/test_schemas.py   runs the runner in CI
```

## Running the checks

```bash
uv run python -m pytest tests/unit_tests/test_schemas.py -v
uv run python tools/run_conformance.py                                              # schemas + corpus
uv run python tools/run_conformance.py --real --real-root . --repos libraries resources  # + files of this repo
```

The runner checks that each schema is a valid draft 2020-12 schema, that every corpus file behaves as its
manifest says (an invalid file must fail *at the declared path*), and with `--real` validates the real YAML
files. It fails when a real file fails that is not listed in `schemas/conformance/real-examples-known.yml`,
or when a listed file starts to validate, so the list cannot rot. Nothing is imported or executed from
the scanned files; they are read with `yaml.safe_load`.

## Versioning

* The set of schema files is versioned together with semver; every file carries `x-schema-version`.
* `$id` embeds the git tag that is meant to publish the set, for example
  `https://raw.githubusercontent.com/AntaresSimulatorTeam/GEMS/schemas-v0.1.0/schemas/system.schema.yml`.
  The tag does not exist yet; the base URL is a proposal (open question), not a fact.
* While `0.x`: any change that makes a previously (in)valid file (in)valid bumps the minor, anything else
  (descriptions, annotations, corpus) the patch. From `1.0`: tightening = major, loosening = minor.
* `x-status: provisional` marks schemas whose shape is unsettled.
* `x-discrepancy: [ID]` on a keyword points to the row of DISCREPANCIES.md that explains why projects differ.
  They are annotations: validators ignore them.
* The language itself is versioned by the GEMS documentation release (`AGENTS.md` rule 6); this draft
  describes the docs at `9c52d63`. Tying schema versions to documentation releases is an open question.

## How a consumer pins and uses the schemas

1. **Pin**: copy or vendor the `schemas/*.schema.yml` files of one tag into the project (they must stay
   side by side: the `$ref`s are relative, `common.schema.yml#/$defs/...`). Record the tag in the project.
2. **Validate**: load the YAML with a *safe* loader, then validate the resulting object against the schema
   of its kind, with the schemas registered so that `$ref` resolves.

   ```python
   import yaml
   from jsonschema import Draft202012Validator
   from referencing import Registry, Resource
   from referencing.jsonschema import DRAFT202012

   docs = {n: yaml.safe_load(open(f"schemas/{n}.schema.yml")) for n in
           ("common", "model-library", "system", "optim-config", "system-for-view",
           "taxonomy", "catalog", "view-config")}
   registry = Registry().with_resources(
       [(d["$id"], Resource(d, DRAFT202012)) for d in docs.values()])
   validator = Draft202012Validator(docs["system"], registry=registry)
   errors = sorted(validator.iter_errors(yaml.safe_load(open("input/system.yml"))), key=str)
   ```

3. **Other languages**: the schemas are plain JSON Schema; a project that has no YAML-capable validator
   converts the YAML schema and the instance to JSON first (build step). For TypeScript an Ajv build with
   2020-12 support would be needed; for C++ a JSON Schema library over the converted files. I have not
   tested either.
4. **Test your own fixtures**: run the consumer's own example files through the schema in CI, and, for
   projects with their own parser (GemsPy pydantic, AntaREST pydantic, Simulator `checkFields`), run the
   `conformance/` corpus through that parser too and compare with each manifest. Every disagreement is
   either a bug in the schema, a bug in the project, or a new row in DISCREPANCIES.md.
5. **Never copy a schema and edit it locally**: if a rule is wrong, change it in GEMS so that all projects
   see it.

## Proposed rollout

0. **Before anything else**, settle the open questions of the report (at least: `description`
   on `system`, `boolean` vs `binary`, the id naming rule, the optim-config dialects). Until then a project
   adopting the schemas would adopt the unresolved conflicts as well.
1. **GemsPy and AntaREST CI first**. They are the two projects with typed models of these files, so they
   can run the corpus against their own pydantic models and expose every disagreement early. AntaREST also
   validates what it writes (`system.yml`, libraries; today it writes an empty `optim-config.yml`).
2. **Then**: GEMS (CI on `libraries/` and `resources/` is done by `tests/unit_tests/test_schemas.py`; one stale file is a known failure),
   Antares_Simulator (cucumber study resources and `checkFields` whitelists), GEMS-ViewsBuilder (its test
   inputs; it reads `system-for-view` with GemsPy), PyPSA-to-GEMS-Converter (validate the study it writes,
   after fixing `model_libraries` and `resolution-mode`). antares-datamanager-front and
   antares-datamanager-generator when they start to read or write these files (they do not today).
3. **Finally generate the antares-doc reference** from the schemas (field tables from `properties`,
   `description`, `required`, `default` text and `x-discrepancy` notes), so that the doc stops being a
   second, hand-written copy. This needs the schemas to be stable (non-provisional) first.
