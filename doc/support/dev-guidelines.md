# GEMS Ecosystem — Developer Guidelines

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

The branching model differs between repositories because merging to `main` in the GEMS repository triggers a documentation website rebuild.

#### GEMS

| Branch | Role |
|---|---|
| `main` | Published branch. Every merge triggers a ReadTheDocs rebuild. Updated only via PRs from `release/` or `hotfix/`. Direct commits are not allowed. |
| `develop` | Integration branch for ongoing work. All `feature`, `bugfix`, `chore` PRs target `develop`. Not protected — direct commits are allowed to resolve conflicts with `main`. |

#### Converter Repositories and GemsPy

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

In GEMS, all `feature`, `bugfix`, `chore`, `docs`, and `refactor` branches are created from `develop`. `release` and `hotfix` branches are created from `develop` and `main` respectively.

In converter repositories and GemsPy, all branches are created from `main`.

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

**GEMS:**

1. Create a branch from `develop`
2. Implement the change
3. Open a PR targeting `develop`, linked to the issue
4. Apply labels (see Section 5)
5. Pass CI and code review
6. Squash and merge

**Converter repositories and GemsPy:**

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
| `develop` (GEMS only) | Squash & Merge | All `feature`, `bugfix`, `chore`, `docs`, `refactor` PRs |
| `main` | Squash & Merge | `release` and `hotfix` PRs (GEMS); all PRs (converters and GemsPy) |

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

All repositories follow **Semantic Versioning** (`MAJOR.MINOR.PATCH`). The `library.version` field inside each library YAML is the authoritative version record for model libraries.

### PyPSA-to-GEMS-Converter Versioning

| Component | Bump rule | Version file |
|---|---|---|
| Converter (`pyproject.toml`) | Major: Antares major bump / Minor: bug fix, new feature, PyPSA update / Patch: dependency update or library-only change | `pyproject.toml` |
| PyPSA Models Library | Major: new model / Minor: bug fix or improvement / Patch: rename or refactor | `library.version` in `resources/pypsa_models/pypsa_models.yml` |
| PyPSA | Pinned version | `requirements.txt` |
| Antares-Simulator | Pinned version used by CI | `dependencies.json` → `antares_version` |

### AntaresLegacyModels-to-GEMS-Converter Versioning

| Component | Bump rule | Version file |
|---|---|---|
| Converter (`pyproject.toml`) | Major: Antares major bump / Minor: bug fix, new feature, antares-craft or GemsPy update / Patch: dependency update or library-only change | `pyproject.toml` |
| Antares Legacy Models Library | Major: new model / Minor: bug fix or improvement / Patch: rename or refactor | `library.version` in `src/antares_gems_converter/libs/antares_historic/antares_legacy_models.yml` |
| Antares-Simulator | Pinned version used by CI | `dependencies.json` → `antares_simulator_version` |
| antares-craft | Pinned version | `requirements.txt` |
| GemsPy | Pinned version | `requirements.txt` |

### GEMS Versioning

| Component | Bump rule | Version field |
|---|---|---|
| GEMS Language / Documentation | Versioned together with the documentation. Major: breaking syntax change / Minor: new construct or keyword / Patch: clarification or doc fix | Release notes at `doc/0_Home/4_release_notes.md` |
| Model libraries (`libraries/*.yml`) | Major: new model / Minor: bug fix or improvement / Patch: rename or refactor | `library.version` inside each `libraries/<library_name>.yml` |
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
| Linting | `ruff` | `ruff` | `black` | `black` + `isort` |
| Type checking | `mypy` | `mypy` | `mypy` | `mypy` |
| YAML linting | `yamllint` | — | — | — |
| Unit tests | `pytest tests/unit_tests/` | `pytest tests/unit_tests/` | `pytest` (with coverage) | `pytest` (with coverage) |
| E2E tests | `pytest tests/e2e_tests/` | `pytest tests/e2e/` | `pytest tests/antares_historic/` | `pytest tests/e2e/` |

PRs cannot be merged if any required CI check fails.

GemsPy additionally has a `publish.yml` workflow that triggers automatically when a GitHub release is published — it builds the package and pushes it to PyPI. No manual action is needed after tagging.

### Automated Dependency Monitoring

Each repository monitors its upstream dependencies on a schedule and opens an issue automatically when a new version is detected.

| Workflow | Repo | Schedule | Monitors |
|---|---|---|---|
| `check-antares-update` | GEMS, PyPSA Converter, AntaresLegacy Converter | Daily 06:00 UTC | Antares-Simulator GitHub releases |
| `check-pypsa-update` | PyPSA Converter | Monday 06:00 UTC | PyPSA on PyPI |
| `check-antares-craft-update` | AntaresLegacy Converter | Monday 06:00 UTC | antares-craft on PyPI |
| `check-gemspy-update` | AntaresLegacy Converter | Monday 06:00 UTC | GemsPy on PyPI |

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

> ⚠️ **WARNING: THE CHECKSUM WORKFLOW FIRES WHENEVER YOU PUSH TO A `release/**` OR `hotfix/**` BRANCH AND THE PUSH CONTAINS LIBRARY YAML CHANGES — WHETHER YOU EDITED THE LIBRARY DIRECTLY ON THAT BRANCH OR THE LIBRARY WAS ALREADY MODIFIED IN THE COMMITS CARRIED OVER FROM `develop` OR `main` WHEN THE BRANCH WAS CREATED. IN BOTH CASES THE WORKFLOW WILL AUTOMATICALLY COMMIT AN UPDATED CHECKSUM BACK TO YOUR BRANCH. YOU MUST RUN `git pull` BEFORE MAKING ANY FURTHER LOCAL CHANGES OR PUSHES, OTHERWISE YOUR NEXT PUSH WILL BE REJECTED DUE TO DIVERGED HISTORY.**

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
2. Reads the current `library.version` from the converter's library YAML.
3. Fetches the `library.version` currently in the GEMS repository via the GitHub API (`GEMS_REPO_PAT`).
4. Compares the two versions.
5. If equal → GEMS is already up to date; workflow exits with no action.
6. If different → opens an issue in the GEMS repository prompting synchronisation.

This means the notification reflects the true synchronisation state between the converter and GEMS — it fires whenever the converter's library is ahead of GEMS, regardless of git history. Duplicate issues for the same version are suppressed.

Both workflows require the `GEMS_REPO_PAT` secret (a Personal Access Token with `repo` scope on the GEMS repository).

---

## 8. Release Process

The release flow is the same for all repositories:

**GEMS:**

```text
develop  ──── squash PRs (feature, bugfix, chore…) ────► ready to release
                                      │
                          create release/vX.Y.Z from develop
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
                                      │
                                      ▼
                          merge main back into develop
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
| `resources/pypsa_models/pypsa_models.yml` | Bump `library.version` to `1.1.0` (only if library changed) |
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

5. Cross-repo notification (automatic) — if `library.version` in `resources/pypsa_models/pypsa_models.yml` was bumped, the `notify-gems-pypsa-models-update` workflow fires automatically on the `main` merge. It compares the converter's version with the GEMS repository's version and opens an issue in GEMS if they differ. No manual action needed.

---

### 8.2 AntaresLegacyModels-to-GEMS-Converter Release

Same flow as the PyPSA converter. The example below releases converter version `1.2.0` with a library bump to `1.1.0`.

#### AntaresLegacy Converter — Files to update

| File | What to change |
|---|---|
| `pyproject.toml` | Bump `version` to `1.2.0` |
| `src/antares_gems_converter/libs/antares_historic/antares_legacy_models.yml` | Bump `library.version` to `1.1.0` (only if library changed) |
| `src/antares_gems_converter/libs/antares_historic/CHANGELOG-antares_legacy_models_library.md` | Add library release entry (only if library changed) |

#### AntaresLegacy Converter — Steps

Same flow as the PyPSA converter (steps 1–5). Replace the file paths with:

- `pyproject.toml`
- `src/antares_gems_converter/libs/antares_historic/antares_legacy_models.yml` (if library changed)
- `src/antares_gems_converter/libs/antares_historic/CHANGELOG-antares_legacy_models_library.md` (if library changed)

Cross-repo notification (automatic) — if `library.version` in `src/antares_gems_converter/libs/antares_historic/antares_legacy_models.yml` was bumped, the `notify-gems-antares-legacy-models-update` workflow fires automatically on the `main` merge. It compares the converter's version with the GEMS repository's version and opens an issue in GEMS if they differ.

---

### 8.3 GEMS Release

The example below releases GEMS version `1.2.0` after syncing an updated PyPSA models library.

#### GEMS — Files to update

| File | What to change |
|---|---|
| `libraries/<library_name>.yml` | Apply library changes and bump `library.version` |
| `libraries/<library_name>.yml.sha256` | Updated automatically by `update-library-checksums` workflow (GEMS-owned libraries only — `pypsa_models.yml` and `antares_legacy_models.yml` must be updated manually) |
| `libraries/CHANGELOG-<library_name>.md` | Add library changelog entry |
| `doc/0_Home/4_release_notes.md` | Add release notes entry if GEMS Language spec changed |
| `COMPATIBILITY.md` | Update documentation version and/or Antares version mapping if changed |

#### GEMS — Steps

1. Make sure `develop` is up to date

   ```bash
   git checkout develop
   git pull origin develop
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

5. Merge `main` back into `develop` to keep it in sync:

   ```bash
   git checkout develop
   git merge main
   git push origin develop
   ```

6. Close the notification issue that triggered this release (e.g. `[PYPSA MODELS] New library version: v1.1.0`).

---

### 8.4 GemsPy Release

#### GemsPy — Files to update

| File | What to change |
|---|---|
| `pyproject.toml` | Bump `version` |

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
7. **GEMS only** — merge `main` back into `develop`:

   ```bash
   git checkout develop
   git merge main
   git push origin develop
   ```

---

## 11. Required GitHub Secrets

| Secret | Required by | Purpose |
|---|---|---|
| `GEMS_REPO_PAT` | PyPSA Converter, AntaresLegacy Converter | Create issues in the GEMS repository from cross-repo notification workflows |
| `PYPI_TOKEN` | GemsPy | Publish package to PyPI via `publish.yml` |
