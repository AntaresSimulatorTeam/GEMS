# Developer Guidelines

This document defines the **standard development, branching, versioning, CI/CD, and release workflow** across all official GEMS ecosystem repositories.

---

## Repositories in Scope

| Repository | Purpose |
|---|---|
| [GEMS](https://github.com/AntaresSimulatorTeam/GEMS) | Language specification, model libraries, documentation |
| [AntaresLegacyModels-to-GEMS-Converter](https://github.com/AntaresSimulatorTeam/AntaresLegacyModels-to-GEMS-Converter) | Converts Antares legacy studies to GEMS format |
| [PyPSA-to-GEMS-Converter](https://github.com/AntaresSimulatorTeam/PyPSA-to-GEMS-Converter) | Converts PyPSA networks to GEMS format |
| [GemsPy](https://github.com/AntaresSimulatorTeam/GemsPy) | Python interpreter for the GEMS Language |

---

## Local Setup

This project uses [uv](https://docs.astral.sh/uv/getting-started/installation/) for dependency management.

> **Rule:** Whenever you change dependencies in `pyproject.toml`, regenerate the lock file with `uv lock` and commit the updated `uv.lock` in the same PR. The lock file must always be in sync with `pyproject.toml`.

### GEMS setup

```bash
git clone https://github.com/AntaresSimulatorTeam/GEMS.git
cd GEMS
uv sync --group dev        # install all dev dependencies
uv run pytest tests/unit_tests -v
```

### PyPSA Converter setup

```bash
git clone https://github.com/AntaresSimulatorTeam/PyPSA-to-GEMS-Converter.git
cd PyPSA-to-GEMS-Converter
uv sync
uv run pytest tests/unit_tests -v
```

### AntaresLegacy Converter setup

```bash
git clone https://github.com/AntaresSimulatorTeam/AntaresLegacyModels-to-GEMS-Converter.git
cd AntaresLegacyModels-to-GEMS-Converter
uv sync
uv run pytest -v
```

### GemsPy setup

```bash
git clone https://github.com/AntaresSimulatorTeam/GemsPy.git
cd GemsPy
uv sync
uv run pytest tests/ -v
# Optional: install solver dependencies for solver-specific tests
uv sync --group solvers
```

---

## 1. Starting a Change

Every change **must start from a tracked GitHub Issue** in the relevant repository.

The issue must describe:

- purpose of the change
- compatibility impact
- applicable process ID (see Section 3)

PR's without an associated issue are only allowed for trivial documentation fixes or emergency hotfixes.

---

## 2. Branch Management

### Core Branches

All repositories use the same `main`-only branching model.

| Branch | Role |
|---|---|
| `main` | Single integration and release branch. All development PRs and release PRs target `main`. Direct commits are not allowed. |

### Working Branch Types

| Type | Purpose |
|---|---|
| `feature/...` | New functionality |
| `bugfix/...` | Bug fixes |
| `refactor/...` | Internal restructuring |
| `perf/...` | Performance improvements |
| `docs/...` | Documentation changes |
| `chore/...` | Maintenance, dependency updates |
| `release/vX.Y.Z` | Release preparation — version bumps and changelog updates |
| `hotfix/vX.Y.Z` | Urgent post-release corrections |

### Naming Convention

```text
<branch-type>/<short-description>

feature/add-sts-model
bugfix/fix-thermal-parameter-mapping
chore/update-antares-craft-dependency
```

All branches are created from `main` across all repositories.

---

## 3. Process IDs and Issue Templates

Each repository defines named governance processes. When opening an issue, select the applicable process template.

### GEMS Process IDs

| Process | Trigger | Template |
|---|---|---|
| **DOC-01** | New Antares-Simulator release affecting the GEMS Language definition | `doc-01.yml` |
| **DOC-02** | Internal documentation improvement | `doc-02.yml` |
| **LT-01** | New Antares-Simulator release affecting model libraries or taxonomies | `lt-01.yml` |
| **LT-02** | Internal library or taxonomy bug fix or improvement | `lt-02.yml` |
| **LT-03** | New model library or taxonomy | `lt-03.yml` |

### PyPSA-to-GEMS-Converter

| Process | Trigger | Template |
|---|---|---|
| **P2G-01** | New Antares-Simulator release | `p2g-01.yml` |
| **P2G-02** | Internal change or model library update | `p2g-02.yml` |
| **P2G-03** | New PyPSA release | `p2g-03.yml` |

### AntaresLegacyModels-to-GEMS-Converter

| Process | Trigger | Template |
|---|---|---|
| **A2G-01** | New Antares-Simulator release | `a2g-01.yml` |
| **A2G-02** | Internal change or model library update | `a2g-02.yml` |
| **A2G-03** | New antares-craft release | `a2g-03.yml` |
| **A2G-04** | New GemsPy release | `a2g-04.yml` |

### GemsPy

| Process | Trigger | Template |
|---|---|---|
| **GP-01** | New GEMS Language version requiring interpreter updates | `gp-01.yml` |
| **GP-02** | Internal bug fix, feature, or code improvement | `gp-02.yml` |

Each template includes a step-by-step process checklist, versioning steps, and validation requirements.

---

## 4. Pull Request Rules

### Workflow

All repositories:

1. Create a branch from `main`
2. Implement the change
3. Open a PR targeting `main`, linked to the issue
4. Apply labels (see Section 5)
5. Pass CI and code review
6. Squash and merge

### PR Title Format

```text
[PR] <id>: <short description> <process-id>

[PR] 001: Add STS model support A2G-02
[PR] 002: Adapt converter to new PyPSA API P2G-03
[PR] 003: Update Antares legacy thermal model A2G-01
```

### PR Description

Each PR must include:

```markdown
## Process ID
A2G-02 | P2G-01 | N/A

## Description
What changed and why.

## Impact Analysis
Affected modules. Breaking changes or backward-compatible?

## Checklist
- [ ] Tests pass
- [ ] pyproject.toml version bumped if converter logic changed
```

### Merge Strategy

| Target | Strategy | Who |
|---|---|---|
| `main` | Squash & Merge | All PRs across all repositories |

### Squash Commit Message

When merging with **Squash & Merge**, GitHub pre-fills the commit message with every individual commit title from the branch. **Always replace this with a manually written message before confirming the merge.**
Auto-generated concatenations like `fix comments, fix comments` or `fix(ruff): fix linting` add noise and make the git log unreadable.

Use one of the two formats below depending on the size of the PR:

**Option A — Flat bullet list** (suitable for most PRs):

```text
feat(scope): short description of what the PR delivers

- One line per logical change, scoped but not over-granular
- Skip pure fixup commits — if it wouldn't go in a changelog, leave it out

Co-authored-by: Name <email>
```

**Option B — Structured sections** (suitable for larger PRs with many concerns):

```text
feat(scope): short description of what the PR delivers

## Summary
High-level description of what this PR achieves.

## Key Changes
- Notable implementation changes

## Testing
- What was tested or added

## Fixes & Cleanup
- Minor fixes, dependency updates, removed files

Co-authored-by: Name <email>
```

The first line follows the [Conventional Commits](https://www.conventionalcommits.org/) format: `<type>(<scope>): <description>`. Common types are `feat`, `fix`, `docs`, `refactor`, `chore`, `perf`, `test`.

---

## 5. Labels

Every PR must carry at least one label from each group.

### Change Type

| Label | Meaning |
|---|---|
| `type:feature` | New feature |
| `type:bugfix` | Bug fix |
| `type:refactor` | Internal restructuring |
| `type:performance` | Performance improvement |
| `type:documentation` | Documentation changes |
| `type:dependency` | Dependency updates |
| `type:hotfix` | Critical post-release fix |

### Release Impact

Exactly one release label must be assigned.

| Label | Meaning |
|---|---|
| `release:major` | Breaking change |
| `release:minor` | New feature, backward-compatible |
| `release:patch` | Bug fix or internal improvement |
| `release:none` | No release impact |

---

## 6. Versioning

All repositories follow **Semantic Versioning** (`MAJOR.MINOR.PATCH`). The `version` field under the `library:` key inside each library YAML is the authoritative version record for model libraries.

### PyPSA-to-GEMS-Converter Versioning

| Component | Bump rule | Version file |
|---|---|---|
| Converter (`pyproject.toml`) | Major: Antares major bump / Minor: bug fix, new feature, PyPSA update / Patch: dependency update or library-only change | `pyproject.toml` |
| PyPSA Models Library | Major: new model / Minor: bug fix or improvement / Patch: rename or refactor | `version` under `library:` in `resources/pypsa_models/pypsa_models.yml` |
| PyPSA | Pinned version | `pyproject.toml` |
| Antares-Simulator | Pinned version used by CI | `dependencies.json` → `antares_version` |

### AntaresLegacyModels-to-GEMS-Converter Versioning

| Component | Bump rule | Version file |
|---|---|---|
| Converter (`pyproject.toml`) | Major: Antares major bump / Minor: bug fix, new feature, antares-craft or GemsPy update / Patch: dependency update or library-only change | `pyproject.toml` |
| Antares Legacy Models Library | Major: new model / Minor: bug fix or improvement / Patch: rename or refactor | `version` under `library:` in `src/antares_gems_converter/libs/antares_historic/antares_legacy_models.yml` |
| Antares-Simulator | Pinned version used by CI | `dependencies.json` → `antares_simulator_version` |
| antares-craft | Pinned version | `pyproject.toml` |
| GemsPy | Pinned version | `pyproject.toml` |

### GEMS Versioning

| Component | Bump rule | Version field |
|---|---|---|
| GEMS Language / Documentation | Versioned together with the documentation. Major: breaking syntax change / Minor: new construct or keyword / Patch: clarification or doc fix | Release notes at `doc/0_Home/4_release_notes.md` |
| Model libraries (`libraries/*.yml`) | Major: new model / Minor: bug fix or improvement / Patch: rename or refactor | `version` under `library:` in each `libraries/<library_name>.yml` |
| Antares-Simulator | Pinned version used by CI and E2E tests | `dependencies.json` → `antares_simulator_version` |

### GemsPy Versioning

| Component | Bump rule | Version file |
|---|---|---|
| GemsPy (`pyproject.toml`) | Major: breaking GEMS Language change or backward-incompatible API change / Minor: new feature or GP-01 impact / Patch: bug fix or internal improvement | `pyproject.toml` |

---

## 7. CI/CD Automation

### Per-Repository Pipelines

| Check | GEMS | PyPSA Converter | AntaresLegacy Converter | GemsPy |
|---|---|---|---|---|
| CI trigger | PRs only | Every push + PRs | Every push + PRs | Every push + PRs |
| Python version | 3.11 | 3.11 | 3.12 | 3.11 |
| Package manager | `uv` | `uv` | `uv` | `uv` |
| Formatter | `ruff format` | `ruff format` | `black` | `black` |
| Linter | `ruff check` | `ruff check` | — | — |
| Import sorter | `ruff check` (isort rules) | `ruff check` (isort rules) | — | `isort` |
| Type checker | `mypy` | `mypy` | `mypy` | `mypy` |
| YAML linting | `yamllint` | — | — | — |
| Unit tests | `pytest tests/unit_tests/` | `pytest tests/unit_tests/` | `pytest` (with coverage) | `pytest` (with coverage) |
| E2E tests | `pytest tests/e2e_tests/` | `pytest tests/e2e/` | `pytest tests/antares_historic/` | `pytest tests/e2e/` |

PRs cannot be merged if any required CI check fails.

GemsPy, PyPSA Converter, and AntaresLegacy Converter additionally have a `publish.yml` workflow that triggers automatically when a GitHub release is published — it builds the package and pushes it to PyPI. No manual action is needed after tagging.

### Automated Dependency Monitoring

Each repository monitors its upstream dependencies on a schedule and opens an issue automatically when a new version is detected.

| Workflow | Repo | Schedule | Monitors |
|---|---|---|---|
| `check-antares-update` | GEMS, PyPSA Converter, AntaresLegacy Converter | Weekly (Monday 06:00 UTC) | Antares-Simulator GitHub releases |
| `check-pypsa-update` | PyPSA Converter | Weekly (Monday 06:00 UTC) | PyPSA on PyPI |
| `check-antares-craft-update` | AntaresLegacy Converter | Weekly (Monday 06:00 UTC) | antares-craft on PyPI |
| `check-gemspy-update` | AntaresLegacy Converter | Weekly (Monday 06:00 UTC) | GemsPy on PyPI |

Each monitoring workflow:

1. Compares the latest published version against the pinned version in the repo
2. Opens an issue with a triage checklist if a new version is detected
3. Runs the full test suite against the new version
4. Posts the test result as a comment on the issue

Duplicate issues for the same version are suppressed automatically.

### Library SHA256 Checksums

Each repository automatically maintains SHA256 checksum files alongside its library YAMLs. The checksum file is placed next to the library file and named `<library>.yml.sha256`.

| Workflow | Repo | Trigger | Scope |
|---|---|---|---|
| `update-library-checksums` | GEMS | Push to `release/**` or `hotfix/**` touching `libraries/*.yml` | `libraries/` (excludes `pypsa_models.yml` and `antares_legacy_models.yml`) |
| `update-library-checksums` | PyPSA Converter | Push to `release/**` or `hotfix/**` touching `resources/pypsa_models/*.yml` | `resources/pypsa_models/` |
| `update-library-checksums` | AntaresLegacy Converter | Push to `release/**` or `hotfix/**` touching `src/antares_gems_converter/libs/**/*.yml` | `src/antares_gems_converter/libs/` |

**How it works:**

- Runs on every push to a `release/**` or `hotfix/**` branch that touches a library YAML.
- If no `.sha256` file exists → generated and committed back to the branch automatically.
- If the hash matches the stored one → no action.
- If the hash differs → `.sha256` file updated and committed back to the branch automatically.

> ⚠️ **WARNING: THE CHECKSUM WORKFLOW FIRES WHENEVER YOU PUSH TO A `release/**` OR `hotfix/**` BRANCH AND THE PUSH CONTAINS LIBRARY YAML CHANGES — WHETHER YOU EDITED THE LIBRARY DIRECTLY ON THAT BRANCH OR THE LIBRARY WAS ALREADY MODIFIED IN THE COMMITS CARRIED OVER FROM `main` WHEN THE BRANCH WAS CREATED. IN BOTH CASES THE WORKFLOW WILL AUTOMATICALLY COMMIT AN UPDATED CHECKSUM BACK TO YOUR BRANCH. YOU MUST RUN `git pull` BEFORE MAKING ANY FURTHER LOCAL CHANGES OR PUSHES, OTHERWISE YOUR NEXT PUSH WILL BE REJECTED DUE TO DIVERGED HISTORY.**

The `pypsa_models.yml` and `antares_legacy_models.yml` libraries in GEMS repository are excluded from `update-library-checksums` workflow because their checksums are managed by the respective converter repositories.

---

### Cross-Repository Notifications

When a model library is updated in a converter, an issue is automatically created in the **GEMS** repository to prompt synchronisation of the shared library YAML.

| Workflow | From | To | Trigger |
|---|---|---|---|
| `notify-gems-pypsa-models-update` | PyPSA Converter | GEMS | Push to `main` that modifies `resources/pypsa_models/pypsa_models.yml` |
| `notify-gems-antares-legacy-models-update` | AntaresLegacy Converter | GEMS | Push to `main` that modifies `src/antares_gems_converter/libs/antares_historic/antares_legacy_models.yml` |

**How the workflow runs (step by step):**

1. Triggered on push to `main` when the library YAML file changes.
2. Reads the current `version` under `library:` from the converter's library YAML.
3. Fetches the `version` under `library:` currently in the GEMS repository via the GitHub API (`GEMS_REPO_PAT`).
4. Compares the two versions.
5. If equal → GEMS is already up to date; workflow exits with no action.
6. If different → opens an issue in the GEMS repository prompting synchronisation.

This means the notification reflects the true synchronisation state between the converter and GEMS — it fires whenever the converter's library is ahead of GEMS, regardless of git history. Duplicate issues for the same version are suppressed.

Both workflows require the `GEMS_REPO_PAT` secret (a Personal Access Token with `repo` scope on the GEMS repository).

### GemsPy Release Notification Chain

When a new GemsPy release is published, the `notify-gemspy-release.yml` workflow in GemsPy fires automatically and opens triage issues in three downstream repositories:

| Target repository | Purpose |
|---|---|
| GEMS | Update the `gemspy` pin in `pyproject.toml` (use process LT-02 or DOC-02 as applicable) |
| AntaresLegacy Converter | Run A2G-04 process — test and update the GemsPy pin |
| GEMS-ViewsBuilder | Update the GemsPy dependency (external repository, not part of this ecosystem) |

Each issue includes a per-repo triage checklist. Duplicate issues for the same GemsPy version are suppressed automatically.

The workflow requires: `GEMS_REPO_PAT`, `ANTARES_LEGACY_CONVERTER_PAT`, and `GEMS_VIEWS_BUILDER_PAT` secrets.

> **Note:** GEMS has no automated monitoring workflow for GemsPy — the triage issue opened by GemsPy's `notify-gemspy-release.yml` is the sole trigger. The `gemspy` pin in `GEMS/pyproject.toml` must be updated manually once the issue is opened.

### Library Synchronisation Procedure

When a cross-repo notification issue is opened in GEMS (via `notify-gems-pypsa-models-update` or `notify-gems-antares-legacy-models-update`), follow these steps to copy the updated library into GEMS safely:

1. In the converter repository, locate the three authoritative files: the library `.yml`, its `.yml.sha256` (produced by the `update-library-checksums` workflow on the converter's release branch), and the library `CHANGELOG-<library>.md`.
2. Copy all three files byte-for-byte into `GEMS/libraries/` — do **not** regenerate the hash locally with `sha256sum`. The stored hash must match the converter's exact file byte-for-byte including line endings. The converter is the source of truth for these libraries; no further edits are needed in GEMS.
3. Verify: `sha256sum GEMS/libraries/<library>.yml` must match the content of `GEMS/libraries/<library>.yml.sha256`.
4. Commit the three files together. Do not commit one without the others.
5. Close the notification issue once the GEMS PR is merged.

> **Checksum file naming:** All SHA256 files must follow the `<library>.yml.sha256` convention — the `.yml` extension is part of the checksum filename, making it unambiguous which file was hashed.

---

## 8. Release Process

The release flow is the same for all repositories:

**GEMS:**

```text
main  ──── squash PRs (feature, bugfix, chore…) ────► ready to release
                                      │
                          create release/vX.Y.Z from main
                                      │
                          bump versions + update changelogs
                          (checksum auto-commits if library changed)
                                      │
                          open PR: release/vX.Y.Z → main
                          (squash & merge)
                                      │
                             squash-merge into main
                                      │
                                      ▼
                          manually create tag vX.Y.Z + GitHub release
                          via GitHub UI
```

**Converter repositories:**

```text
main  ──── squash PRs (feature, bugfix, chore…) ────► ready to release
                                      │
                          create release/vX.Y.Z from main
                                      │
                          bump versions + update library changelog (if library changed)
                          (checksum auto-commits if library changed)
                                      │
                          open PR: release/vX.Y.Z → main
                          (squash & merge)
                                      │
                             squash-merge into main
                                      │
                                      ▼
                          manually create tag vX.Y.Z + GitHub release
                          via GitHub UI
```

**GemsPy:**

```text
main  ──── squash PRs (feature, bugfix, chore…) ────► ready to release
                                      │
                          create release/vX.Y.Z from main
                                      │
                                bump version
                                      │
                          open PR: release/vX.Y.Z → main
                          (squash & merge)
                                      │
                             squash-merge into main
                                      │
                                      ▼
                          manually create tag vX.Y.Z + GitHub release
                          via GitHub UI
                                      │
                                      ▼
                          publish to PyPI triggered automatically
```

---

### 8.1 PyPSA-to-GEMS-Converter Release

The example below releases converter version `1.2.0` with a library bump to `1.1.0`.

#### PyPSA Converter — Files to update

| File | What to change |
|---|---|
| `pyproject.toml` | Bump `version` to `1.2.0` |
| `COMPATIBILITY.md` | Update PyPSA and Antares-Simulator version mappings if changed |
| `resources/pypsa_models/pypsa_models.yml` | Bump `version` under `library:` to `1.1.0` (only if library changed) |
| `resources/pypsa_models/CHANGELOG-pypsa_models_library.md` | Add library release entry (only if library changed) |

#### PyPSA Converter — Steps

1. Make sure `main` is up to date

   ```bash
   git checkout main
   git pull origin main
   ```

2. Create the release branch and bump versions

   ```bash
   git checkout -b release/v1.2.0
   ```

   Update `pyproject.toml`, `resources/pypsa_models/pypsa_models.yml`, and `CHANGELOG-pypsa_models_library.md` (if library changed), then push:

   ```bash
   git push origin release/v1.2.0
   ```

3. Open a PR from `release/v1.2.0` targeting `main`
   - Title: `[PR] Release v1.2.0`
   - Labels: `release:minor` / `release:major` / `release:patch`
   - Merge strategy: **Squash & Merge**

4. Go to GitHub → Releases → Draft a new release → create tag `v1.2.0` on `main` → paste the changelog entry → publish.

5. Cross-repo notification (automatic) — if `version` under `library:` in `resources/pypsa_models/pypsa_models.yml` was bumped, the `notify-gems-pypsa-models-update` workflow fires automatically on the `main` merge. It compares the converter's version with the GEMS repository's version and opens an issue in GEMS if they differ. No manual action needed.

---

### 8.2 AntaresLegacyModels-to-GEMS-Converter Release

Same flow as the PyPSA converter. The example below releases converter version `1.2.0` with a library bump to `1.1.0`.

#### AntaresLegacy Converter — Files to update

| File | What to change |
|---|---|
| `pyproject.toml` | Bump `version` to `1.2.0` |
| `COMPATIBILITY.md` | Update Antares-Simulator, antares-craft, and GemsPy version mappings if changed |
| `src/antares_gems_converter/libs/antares_historic/antares_legacy_models.yml` | Bump `version` under `library:` to `1.1.0` (only if library changed) |
| `src/antares_gems_converter/libs/antares_historic/CHANGELOG-antares_legacy_models_library.md` | Add library release entry (only if library changed) |

#### AntaresLegacy Converter — Steps

Same flow as the PyPSA converter (steps 1–5). Replace the file paths with:

- `pyproject.toml`
- `src/antares_gems_converter/libs/antares_historic/antares_legacy_models.yml` (if library changed)
- `src/antares_gems_converter/libs/antares_historic/CHANGELOG-antares_legacy_models_library.md` (if library changed)

Cross-repo notification (automatic) — if `version` under `library:` in `src/antares_gems_converter/libs/antares_historic/antares_legacy_models.yml` was bumped, the `notify-gems-antares-legacy-models-update` workflow fires automatically on the `main` merge. It compares the converter's version with the GEMS repository's version and opens an issue in GEMS if they differ.

---

### 8.3 GEMS Release

The example below releases GEMS version `1.2.0` after syncing an updated PyPSA models library.

#### GEMS — Files to update

| File | What to change |
|---|---|
| `libraries/<library_name>.yml` | Apply library changes and bump `version` under `library:` |
| `libraries/<library_name>.yml.sha256` | Updated automatically by `update-library-checksums` workflow (GEMS-owned libraries only — `pypsa_models.yml` and `antares_legacy_models.yml` must be updated manually) |
| `libraries/CHANGELOG-<library_name>.md` | Add library changelog entry |
| `doc/0_Home/4_release_notes.md` | Add release notes entry if GEMS Language spec changed |
| `COMPATIBILITY.md` | Update documentation version and/or Antares version mapping if changed |

#### GEMS — Steps

1. Make sure `main` is up to date

   ```bash
   git checkout main
   git pull origin main
   ```

2. Create the release branch and bump versions

   ```bash
   git checkout -b release/v1.2.0
   ```

   Update `dependencies.json`, library YAML files, and changelog files, then push:

   ```bash
   git push origin release/v1.2.0
   ```

3. Open a PR from `release/v1.2.0` targeting `main`
   - Title: `[PR] Release v1.2.0`
   - Labels: `release:minor` / `release:major` / `release:patch`
   - Merge strategy: **Squash & Merge**

4. Go to GitHub → Releases → Draft a new release → create tag `v1.2.0` on `main` → paste the changelog entry → publish.

5. Close the notification issue that triggered this release (e.g. `[PYPSA MODELS] New library version: v1.1.0`).

---

### 8.4 GemsPy Release

#### GemsPy — Files to update

| File | What to change |
|---|---|
| `pyproject.toml` | Bump `version` |
| `docs/CHANGELOG.md` | Add release entry |

#### GemsPy — Steps

1. Make sure `main` is up to date

   ```bash
   git checkout main
   git pull origin main
   ```

2. Create the release branch and bump the version

   ```bash
   git checkout -b release/v1.2.0
   ```

   Update `pyproject.toml`, then push:

   ```bash
   git push origin release/v1.2.0
   ```

3. Open a PR from `release/v1.2.0` targeting `main`
   - Title: `[PR] Release v1.2.0`
   - Labels: `release:minor` / `release:major` / `release:patch`
   - Merge strategy: **Squash & Merge**

4. Go to GitHub → Releases → Draft a new release → create tag `v1.2.0` on `main` → fill in release notes → publish.

5. PyPI publish (automatic) — the `publish.yml` workflow triggers on the GitHub release published event and pushes the package to PyPI automatically. No manual action needed.

6. Cross-repo notifications (automatic) — the `notify-gemspy-release.yml` workflow fires on the published release and opens triage issues in GEMS, AntaresLegacy Converter, and GEMS-ViewsBuilder. Confirm the three issues were opened successfully.

---

## 9. Tagging Rules

### Release tags (all repositories)

- Tags are created manually via the GitHub UI when drafting a new release, targeting `main` HEAD after the release PR is merged
- Format: `vX.Y.Z` (e.g. `v1.2.0`, `v0.3.4`)
- Every release PR merged to `main` must result in a tag and a published GitHub release

---

## 10. Hotfix Rules

For critical issues discovered after a release:

1. Branch from `main`: `hotfix/vX.Y.Z`
2. Apply the fix, bump the version in the relevant files, and commit
3. Push the hotfix branch: `git push origin hotfix/vX.Y.Z`
4. Open a PR from `hotfix/vX.Y.Z` targeting `main`
5. Merge via **Squash & Merge**
6. Go to GitHub → Releases → Draft a new release → create tag `vX.Y.Z` on `main` → paste the changelog entry → publish.

---

## 11. Required GitHub Secrets

| Secret | Required by | Purpose |
|---|---|---|
| `GEMS_REPO_PAT` | PyPSA Converter, AntaresLegacy Converter | Create issues in the GEMS repository from cross-repo notification workflows |
| `ANTARES_LEGACY_CONVERTER_PAT` | GemsPy | Create triage issues in AntaresLegacy Converter from `notify-gemspy-release.yml` |
| `GEMS_VIEWS_BUILDER_PAT` | GemsPy | Create triage issues in GEMS-ViewsBuilder from `notify-gemspy-release.yml` |
| `PYPI_TOKEN` | GemsPy, PyPSA Converter, AntaresLegacy Converter | Publish package to PyPI via `publish.yml` |

> ⚠️ **Personal Access Tokens expire and must be renewed periodically.** All PAT-based secrets (`GEMS_REPO_PAT`, `ANTARES_LEGACY_CONVERTER_PAT`, `GEMS_VIEWS_BUILDER_PAT`) should be reviewed and rotated before their expiry date. Next scheduled review: **October 2026**.
