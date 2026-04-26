# GEMS Ecosystem — Developer Guidelines

This document defines the **standard development, branching, versioning, CI/CD, and release workflow** across all official GEMS ecosystem repositories.

---

## Repositories in Scope

| Repository | Purpose |
|---|---|
| [GEMS](https://github.com/AntaresSimulatorTeam/GEMS) | Language specification, model libraries, documentation |
| [AntaresLegacyModels-to-GEMS-Converter](https://github.com/AntaresSimulatorTeam/AntaresLegacyModels-to-GEMS-Converter) | Converts Antares legacy studies to GEMS format |
| [PyPSA-to-GEMS-Converter](https://github.com/AntaresSimulatorTeam/PyPSA-to-GEMS-Converter) | Converts PyPSA networks to GEMS studies |

---

## 1. Starting a Change

Every change **must start from a tracked GitHub Issue** in the relevant repository.

The issue must describe:

- purpose of the change
- compatibility impact
- applicable process ID (see Section 3)

PRs without an associated issue are only allowed for trivial documentation fixes or emergency hotfixes.

---

## 2. Branch Management

### Core Branches

| Branch | Role |
|---|---|
| `main` | Production state. Every commit is a tagged release. |
| `develop` | Integration branch for the next release. Updated via PRs only. |

Direct commits to `main` or `develop` are **not allowed**.

### Working Branch Types

| Type | Purpose |
|---|---|
| `feature/...` | New functionality |
| `bugfix/...` | Bug fixes |
| `refactor/...` | Internal restructuring |
| `perf/...` | Performance improvements |
| `docs/...` | Documentation changes |
| `chore/...` | Maintenance, dependency updates |
| `release/vX.Y.Z` | Release preparation |
| `hotfix/vX.Y.Z` | Urgent post-release corrections |

### Naming Convention

```text
<branch-type>/<short-description>

feature/add-sts-model
bugfix/fix-thermal-parameter-mapping
chore/update-antares-craft-dependency
```

All branches are created from `develop`, except hotfixes which branch from `main`.

---

## 3. Process IDs and Issue Templates

Each repository defines named governance processes. When opening an issue, select the applicable process template.

### GEMS

| Process | Trigger | Template |
|---|---|---|
| **DOC-01** | New Antares-Simulator release affecting the GEMS Language definition | `doc-01.yml` |
| **DOC-02** | Internal documentation improvement | `doc-02.yml` |
| **LT-01** | New Antares-Simulator release affecting model libraries or taxonomies | `lt-01.yml` |
| **LT-02** | Internal library or taxonomy bug fix or improvement | `lt-02.yml` |
| **LT-03** | New model library or taxonomy | `lt-03.yml` |

Incoming cross-repo notifications from the converters are handled under **LT-02**.

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

Each template includes a step-by-step process checklist, versioning steps, and validation requirements.

---

## 4. Pull Request Rules

### Workflow

1. Create a branch from `develop`
2. Implement the change
3. Open a PR targeting `develop`, linked to the issue
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
- [ ] Changelog entry added if library changed
- [ ] COMPATIBILITY.md updated if supported versions changed
```

### Merge Strategy

| Target | Strategy | Who |
|---|---|---|
| `develop` | Squash & Merge | All feature/bugfix/chore/versioning PRs |
| `main` | Merge commit | From `develop` (release) or `hotfix/` |

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

All repositories follow **Semantic Versioning** (`MAJOR.MINOR.PATCH`).

### PyPSA-to-GEMS-Converter

| Component | Bump rule | Version file |
|---|---|---|
| Converter (`pyproject.toml`) | Major: Antares major bump / Minor: bug fix, new feature, PyPSA update / Patch: dependency update or library-only change | `pyproject.toml` |
| PyPSA Models Library | Major: new model / Minor: bug fix or improvement / Patch: rename or refactor | `dependencies.json` → `pypsa_models_library_version` |
| PyPSA | Pinned version | `requirements.txt` |
| Antares-Simulator | Pinned version used by CI | `dependencies.json` → `antares_version` |

> **Note:** The PyPSA converter uses the key `antares_version` while the AntaresLegacy converter uses `antares_simulator_version`. These are intentionally different keys in each repo's `dependencies.json`.

### AntaresLegacyModels-to-GEMS-Converter

| Component | Bump rule | Version file |
|---|---|---|
| Converter (`pyproject.toml`) | Major: Antares major bump / Minor: bug fix, new feature, antares-craft or GemsPy update / Patch: dependency update or library-only change | `pyproject.toml` |
| Antares Legacy Models Library | Major: new model / Minor: bug fix or improvement / Patch: rename or refactor | `dependencies.json` → `antares_legacy_models_library_version` |
| Antares-Simulator | Pinned version used by CI | `dependencies.json` → `antares_simulator_version` |
| antares-craft | Pinned version | `requirements.txt` |
| GemsPy | Pinned version | `requirements.txt` |

### GEMS

| Component | Bump rule | Key in `dependencies.json` |
|---|---|---|
| GEMS Language | Major: breaking syntax change / Minor: new construct or keyword / Patch: clarification or doc fix | `gems_language_version` |
| basic\_models\_library | Major: new model / Minor: bug fix or improvement / Patch: rename or refactor | `basic_models_library_version` |
| antares\_legacy\_models | Major: new model / Minor: bug fix or improvement / Patch: rename or refactor | `antares_legacy_models_version` |
| pypsa\_models | Major: new model / Minor: bug fix or improvement / Patch: rename or refactor | `pypsa_models_version` |
| andromede\_models | Major: new model / Minor: bug fix or improvement / Patch: rename or refactor | `andromede_models_version` |
| Antares-Simulator | Pinned version used by CI and E2E tests | `antares_simulator_version` |

---

## 7. Changelogs

Every repository and every independently versioned model library maintains a dedicated changelog.

### Repository Changelogs

| Repository | Changelog location |
|---|---|
| PyPSA-to-GEMS-Converter | `CHANGELOG.md` at repo root |
| AntaresLegacyModels-to-GEMS-Converter | `CHANGELOG.md` at repo root |
| GEMS | `CHANGELOG-gems-language.md` at repo root (GEMS Language changes only) |

### Library Changelogs

| Library | Changelog location |
|---|---|
| PyPSA Models Library | `resources/pypsa_models/CHANGELOG-pypsa_models_library.md` |
| Antares Legacy Models Library | `src/antares_gems_converter/libs/antares_historic/CHANGELOG-antares_legacy_models_library.md` |
| GEMS libraries | `libraries/CHANGELOG-<library_name>.md` |

A changelog entry **must be added before tagging a release**. Recommended sections: `Added`, `Changed`, `Fixed`, `Removed`, `Deprecated`.

---

## 8. CI/CD Automation

### Per-Repository Pipelines

| Check | GEMS | PyPSA Converter | AntaresLegacy Converter |
|---|---|---|---|
| Linting | `ruff` | `ruff` | `black` |
| Type checking | `mypy` | `mypy` | `mypy` |
| YAML linting | `yamllint` | — | — |
| Unit tests | `pytest tests/unit_tests/` | `pytest tests/unit_tests/` | `pytest` (with coverage) |
| E2E tests | `pytest tests/e2e_tests/` | `pytest tests/e2e/` | `pytest tests/antares_historic/` |

PRs cannot be merged if any required CI check fails.

### Automated Dependency Monitoring

Each repository monitors its upstream dependencies on a schedule and opens an issue automatically when a new version is detected.

| Workflow | Repo | Schedule | Monitors |
|---|---|---|---|
| `check-antares-update` | All three | Daily 06:00 UTC | Antares-Simulator GitHub releases |
| `check-pypsa-update` | PyPSA Converter | Monday 06:00 UTC | PyPSA on PyPI |
| `check-antares-craft-update` | AntaresLegacy Converter | Monday 06:00 UTC | antares-craft on PyPI |
| `check-gemspy-update` | AntaresLegacy Converter | Monday 06:00 UTC | GemsPy on PyPI |

Each monitoring workflow:

1. Compares the latest published version against the pinned version in the repo
2. Opens an issue with a triage checklist if a new version is detected
3. Runs the full test suite against the new version
4. Posts the test result as a comment on the issue

Duplicate issues for the same version are suppressed automatically.

### Cross-Repository Notifications

When a model library is updated in a converter, an issue is automatically created in the **GEMS** repository to prompt synchronisation of the shared library YAML.

| Workflow | From | To | Trigger |
|---|---|---|---|
| `notify-gems-pypsa-models-update` | PyPSA Converter | GEMS | Push to `main` where `pypsa_models_library_version` in `dependencies.json` changed vs last `pypsa_models-v*` library tag |
| `notify-gems-antares-legacy-models-update` | AntaresLegacy Converter | GEMS | Push to `main` where `antares_legacy_models_library_version` in `dependencies.json` changed vs last `antares_legacy_models-v*` library tag |

Each library has its own dedicated tag namespace (`pypsa_models-v*`, `antares_legacy_models-v*`), separate from the converter release tags (`vX.Y.Z`).

**How the workflow runs (step by step):**

1. Triggered on push to `main` when `dependencies.json` changes.
2. Reads the current library version from `dependencies.json` at HEAD.
3. Finds the most recent library tag (e.g. the latest `pypsa_models-v*` tag). On the very first run, no tag exists yet — the previous version is treated as empty.
4. Compares current vs previous version.
5. If unchanged → workflow exits with no action.
6. If changed → pushes a new library tag (e.g. `pypsa_models-v1.1.0`) onto the HEAD commit of `main`, then opens an issue in the GEMS repository.

This means a converter release without a library change never triggers a notification. Duplicate issues for the same version are suppressed.

Both workflows require the `GEMS_REPO_PAT` secret (a Personal Access Token with `repo` scope on the GEMS repository).

---

## 9. Release Process

The release flow is the same for all repositories:

```text
develop  ──── squash PRs ────► last PR bumps versions
                                      │
                             squash-merge to develop
                                      │
                                      ▼
                          open PR: develop → main
                          (merge commit — do not squash)
                                      │
                             merge commit into main
                                      │
                                      ▼
                          create release/vX.Y.Z from main HEAD
                          tag vX.Y.Z on release branch
                          push tag + branch atomically
                                      │
                                      ▼
                          publish GitHub release
```

---

### 9.1 PyPSA-to-GEMS-Converter Release

The example below releases converter version `1.2.0` with a library bump to `1.1.0`.

#### PyPSA Converter — Files to update

| File | What to change |
|---|---|
| `pyproject.toml` | Bump `version` to `1.2.0` |
| `dependencies.json` | Bump `pypsa_models_library_version` to `1.1.0` (only if library changed) |
| `CHANGELOG.md` | Add converter release entry |
| `resources/pypsa_models/CHANGELOG-pypsa_models_library.md` | Add library release entry (only if library changed) |

#### PyPSA Converter — Steps

1. Make sure `develop` is up to date

   ```bash
   git checkout develop
   git pull origin develop
   ```

2. Open a version bump PR to `develop`
   - Update `pyproject.toml`, `dependencies.json`, `CHANGELOG.md`, and `resources/pypsa_models/CHANGELOG-pypsa_models_library.md`
   - PR title: `[PR] Release v1.2.0 — version bump`
   - Squash & merge to `develop`

3. Open a PR from `develop` targeting `main`
   - Title: `[PR] Release v1.2.0`
   - Labels: `release:minor` / `release:major` / `release:patch`
   - Merge strategy: **merge commit** — do not squash (see Section 10)

4. After the PR is merged to `main` — create the release branch, tag it, and push

   ```bash
   git checkout main
   git pull origin main
   git checkout -b release/v1.2.0
   git tag v1.2.0
   git push --atomic origin release/v1.2.0 v1.2.0
   ```

   > The `release/vX.Y.Z` branch is a permanent snapshot of `main` at the time of release, kept for audit and security purposes. The tag is placed on this branch — no further commits are made to it.

5. Go to GitHub → Releases → Draft a new release → select tag `v1.2.0` → paste the changelog entry → publish.

6. Cross-repo notification (automatic) — if `pypsa_models_library_version` was bumped, the `notify-gems-pypsa-models-update` workflow fires automatically on the `main` merge. It pushes `pypsa_models-v1.1.0` and opens an issue in GEMS. No manual action needed.

---

### 9.2 AntaresLegacyModels-to-GEMS-Converter Release

Same flow as the PyPSA converter. The example below releases converter version `1.2.0` with a library bump to `1.1.0`.

#### AntaresLegacy Converter — Files to update

| File | What to change |
|---|---|
| `pyproject.toml` | Bump `version` to `1.2.0` |
| `dependencies.json` | Bump `antares_legacy_models_library_version` to `1.1.0` (only if library changed) |
| `CHANGELOG.md` | Add converter release entry |
| `src/antares_gems_converter/libs/antares_historic/CHANGELOG-antares_legacy_models_library.md` | Add library release entry (only if library changed) |

#### AntaresLegacy Converter — Steps

1. Make sure `develop` is up to date (same as PyPSA converter step 1).

2. Open a version bump PR to `develop`
   - Update `pyproject.toml`, `dependencies.json`, `CHANGELOG.md`, and `src/antares_gems_converter/libs/antares_historic/CHANGELOG-antares_legacy_models_library.md`
   - PR title: `[PR] Release v1.2.0 — version bump`
   - Squash & merge to `develop`

3. Open PR `develop` → `main`, merge commit, publish GitHub release (same as PyPSA converter steps 3–5).

4. Cross-repo notification (automatic) — if `antares_legacy_models_library_version` was bumped, the `notify-gems-antares-legacy-models-update` workflow fires automatically on the `main` merge. It pushes `antares_legacy_models-v1.1.0` and opens an issue in GEMS.

---

### 9.3 GEMS Release

A GEMS release is typically triggered by:

- An incoming notification issue from a converter (library updated — process **LT-02**)
- A new Antares-Simulator release affecting libraries (process **LT-01**)
- A new internal library or taxonomy (process **LT-03**)

The example below releases GEMS version `1.2.0` after syncing an updated PyPSA models library.

#### GEMS — Files to update

| File | What to change |
|---|---|
| `dependencies.json` | Bump the relevant version key(s) (e.g. `pypsa_models_version`, `gems_language_version`) |
| `libraries/<library_name>.yml` | Apply library changes |
| `libraries/CHANGELOG-<library_name>.md` | Add library changelog entry |
| `CHANGELOG-gems-language.md` | Add entry if GEMS Language spec changed |
| `COMPATIBILITY.md` | Update if `antares_simulator_version` changed |

#### GEMS — Steps

1. Make sure `develop` is up to date

   ```bash
   git checkout develop
   git pull origin develop
   ```

2. Open a version bump PR to `develop`
   - Update `dependencies.json`, library YAML files, and changelog files
   - PR title: `[PR] Release v1.2.0 — version bump`
   - Squash & merge to `develop`

3. Open a PR from `develop` targeting `main`
   - Title: `[PR] Release v1.2.0`
   - Labels: `release:minor` / `release:major` / `release:patch`
   - Merge strategy: **merge commit** — do not squash (see Section 10)

4. After the PR is merged to `main` — create the release branch, tag it, and push

   ```bash
   git checkout main
   git pull origin main
   git checkout -b release/v1.2.0
   git tag v1.2.0
   git push --atomic origin release/v1.2.0 v1.2.0
   ```

   > The `release/vX.Y.Z` branch is a permanent snapshot of `main` at the time of release, kept for audit and security purposes. The tag is placed on this branch — no further commits are made to it.

5. Go to GitHub → Releases → Draft a new release → select tag `v1.2.0` → paste the changelog entry → publish.

6. Close the notification issue that triggered this release (e.g. `[PYPSA MODELS] New library version: v1.1.0`).

---

## 10. Tagging Rules

### Release tags (all repositories)

- After the PR from `develop` is merged to `main`, a `release/vX.Y.Z` branch is created from `main` HEAD and the tag `vX.Y.Z` is placed on that branch
- Format: `vX.Y.Z` (e.g. `v1.2.0`, `v0.3.4`)
- Every release PR merged to `main` must result in a tag on the corresponding `release/vX.Y.Z` branch
- The `develop` → `main` PR **must** use a **merge commit** — squash is not allowed

#### Why merge commit and not squash

The merge strategy determines whether the full history of individual squash commits from `develop` is preserved on `main`.

With a **merge commit**, git creates a new merge commit on `main` with two parents: the previous `main` HEAD and the HEAD of `develop`. All squash commits from `develop` remain reachable from `main`:

```text
develop:  ... ── A ── B ── C (version bump)
                              \
main:     ... ── X ──────────── M
                                 \
                        release/v1.2.0 ◄── tag v1.2.0
```

With a **squash merge**, all commits from `develop` are flattened into one commit on `main`. The individual per-feature squash commits are no longer reachable:

```text
develop:  ... ── A ── B ── C (version bump)

main:     ... ── X ── S  (S flattens A+B+C — history lost)
```

This is why squash merge is not allowed for release PRs.

#### Release branch as snapshot

After the merge to `main`, a `release/vX.Y.Z` branch is created from `main` HEAD. The tag `vX.Y.Z` is then placed on the current HEAD (the same commit as `main` HEAD — git tags point to commits, not branches) and pushed atomically with the branch. By convention the release tag lives alongside its `release/vX.Y.Z` branch; `main` carries only library tags. This branch is a permanent read-only snapshot of `main` at the time of release, retained for audit and security purposes. No further commits are made to it.

### Library version tags

- Format: `<library_name>-vX.Y.Z` (e.g. `pypsa_models-v1.1.0`, `antares_legacy_models-v1.2.0`)
- Created automatically by the cross-repo notification workflow on the HEAD commit of `main` when a library version change is detected
- Independent of the converter release tag — a library tag is only created when `pypsa_models_library_version` or `antares_legacy_models_library_version` in `dependencies.json` actually changes

---

## 11. Hotfix Rules

For critical issues discovered after a release:

1. Branch from `main`: `hotfix/vX.Y.Z`
2. Apply the fix and commit
3. Push the hotfix branch: `git push origin hotfix/vX.Y.Z`
4. Open a PR from `hotfix/vX.Y.Z` targeting `main` (two approvals recommended)
5. Merge via **merge commit** — do not squash (same reason as release PRs, see Section 10)
6. After the PR is merged to `main` — create the release branch, tag it, and push

   ```bash
   git checkout main
   git pull origin main
   git checkout -b release/vX.Y.Z
   git tag vX.Y.Z
   git push --atomic origin release/vX.Y.Z vX.Y.Z
   ```

7. Publish the GitHub release for the new tag
8. **Mandatory**: open a PR from `main` targeting `develop` and merge it — direct pushes to `develop` are not allowed

---

## 12. Required GitHub Secrets

| Secret | Required by | Purpose |
|---|---|---|
| `GEMS_REPO_PAT` | PyPSA Converter, AntaresLegacy Converter | Create issues in the GEMS repository from cross-repo notification workflows |
