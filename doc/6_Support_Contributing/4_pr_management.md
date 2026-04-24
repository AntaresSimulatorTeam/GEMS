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

```
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

```
[PR] <id>: <short description> <process-id>

[PR] 001: Add STS model support A2G-02
[PR] 002: Adapt converter to new PyPSA API P2G-03
[PR] 003: Update Antares legacy thermal model A2G-01
```

### PR Description

Each PR must include:

```
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
| `develop` | Squash & Merge | All feature/bugfix/chore PRs |
| `main` | Merge commit | Only from `release/` or `hotfix/` |

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

### AntaresLegacyModels-to-GEMS-Converter

| Component | Bump rule | Version file |
|---|---|---|
| Converter (`pyproject.toml`) | Major: Antares major bump / Minor: bug fix, new feature, antares-craft or GemsPy update / Patch: dependency update or library-only change | `pyproject.toml` |
| Antares Legacy Models Library | Major: new model / Minor: bug fix or improvement / Patch: rename or refactor | `dependencies.json` → `antares_legacy_models_library_version` |
| Antares-Simulator | Pinned version used by CI | `dependencies.json` → `antares_simulator_version` |
| antares-craft | Pinned version | `requirements.txt` |
| GemsPy | Pinned version | `requirements.txt` |

### GEMS

| Component | Key in `dependencies.json` |
|---|---|
| GEMS Language | `gems_language_version` |
| basic\_models\_library | `basic_models_library_version` |
| antares\_legacy\_models | `antares_legacy_models_version` |
| pypsa\_models | `pypsa_models_version` |
| andromede\_models | `andromede_models_version` |
| Antares-Simulator | `antares_simulator_version` |

---

## 7. Changelogs

Every repository and every independently versioned model library maintains a dedicated changelog.

### Repository Changelogs

- `CHANGELOG.md` at repo root for converter releases

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
| Unit tests | — | `pytest tests/unit_tests/` | `pytest` (with coverage) |
| E2E tests | `pytest tests/e2e_tests/` | `pytest tests/e2e/` | `pytest tests/antares_historic/` |

PRs cannot be merged if any required CI check fails.

### Automated Dependency Monitoring

Each converter monitors its upstream dependencies on a schedule and opens an issue automatically when a new version is detected.

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
| `notify-gems-pypsa-models-update` | PyPSA Converter | GEMS | Push to `main` where `pypsa_models_library_version` in `dependencies.json` changed vs last git tag |
| `notify-gems-antares-legacy-models-update` | AntaresLegacy Converter | GEMS | Push to `main` where `antares_legacy_models_library_version` in `dependencies.json` changed vs last git tag |

The version comparison is performed against the **last git tag**, not the previous commit, to correctly handle multi-commit pushes. Duplicate issues for the same version are suppressed.

Both workflows require the `GEMS_REPO_PAT` secret (a Personal Access Token with `repo` scope on the GEMS repository).

---

## 9. Release Process

```
develop  ──── squash PRs ────► create release/vX.Y.Z
                                      │
                                      ▼
                          finalise changelog, bump versions
                          tag vX.Y.Z on release branch
                                      │
                                      ▼
                          push branch + tag to remote
                          open PR: release/vX.Y.Z → main
                                      │
                                      ▼
                          merge commit into main
                                      │
                                      ▼
                          publish GitHub release
                                      │
                                      ▼
                          merge release/vX.Y.Z → develop
```

### Step-by-step with git commands

The example below releases version `1.1.0`.

### 1. Make sure `develop` is up to date

```bash
git checkout develop
git pull origin develop
```

### 2. Create the release branch

```bash
git checkout -b release/v1.1.0
```

### 3. Finalise the release on the branch

Update the relevant files:

- `pyproject.toml` — bump the version field to `1.1.0`
- `dependencies.json` — bump `pypsa_models_library_version` or `antares_legacy_models_library_version` if the library changed
- `CHANGELOG-*.md` — add the release entry with today's date

Then commit:

```bash
git add pyproject.toml dependencies.json CHANGELOG-pypsa_models_library.md
git commit -m "release: prepare v1.1.0"
```

### 4. Create the tag on the last commit of the release branch

Only create the tag when all commits on the release branch are final — version bumps, changelog, any last-minute fixes. The tag must point to the last commit.

```bash
git tag v1.1.0
```

> Do not add any commits after tagging. If you need to fix something, make the commit first, then tag.

### 5. Push the branch and the tag together

```bash
git push --atomic origin release/v1.1.0 v1.1.0
```

> `--atomic` ensures both the branch and the tag land on the remote in a single operation — either both succeed or both fail.

### 6. Open the Release PR

Open a PR from `release/v1.1.0` targeting `main` on GitHub.

- Title: `[PR] Release v1.1.0`
- Apply labels: `release:minor` (or `release:major` / `release:patch`)
- Merge strategy: **merge commit** — do not squash (technical requirement, see Section 10)

### 7. After the PR is merged — publish the GitHub release

Go to GitHub → Releases → Draft a new release → select the existing tag `v1.1.0` → paste the changelog entry → publish.

### 8. Sync the release branch back into `develop`

Open a second PR from `release/v1.1.0` targeting `develop` and merge it. This brings any release preparation commits (version bumps, changelog) back into `develop`.

> Direct pushes to `develop` are not allowed — this sync must go through a PR like any other change.

---

## 10. Tagging Rules

- Tags are created on the `release/vX.Y.Z` branch before the PR is merged
- Format: `vX.Y.Z` (e.g. `v1.2.0`, `v0.3.4`)
- Every commit on `main` must correspond to a tag
- The release branch **must** be merged into `main` via a **merge commit** — squash is not allowed. This is a technical requirement for two reasons:
  1. The tag (e.g. `v1.1.0`) is placed on the release branch commit before the PR is merged. A merge commit makes that tagged commit reachable from `main` via `HEAD^2`. With a squash merge, the original release branch commit is discarded and the tag becomes unreachable from `main`, violating the rule above.
  2. The cross-repo notification workflows use `git describe --tags --abbrev=0 HEAD^1` to find the previous release tag. `HEAD^1` is the first parent of the merge commit — the previous tip of `main` — which always has a prior release tag reachable. With a squash merge, subsequent releases would have a squashed (untagged) commit as their `HEAD^1`, causing `git describe` to skip over it and return a stale tag, leading to wrong version comparisons and duplicate notifications.

---

## 11. Hotfix Rules

For critical issues discovered after a release:

1. Branch from `main`: `hotfix/vX.Y.Z`
2. Apply the fix
3. Open PR targeting `main` (two approvals recommended)
4. Merge and tag `vX.Y.(Z+1)`
5. **Mandatory**: merge the hotfix back into `develop`

---

## 12. Required GitHub Secrets

| Secret | Required by | Purpose |
|---|---|---|
| `GEMS_REPO_PAT` | PyPSA Converter, AntaresLegacy Converter | Create issues in the GEMS repository from cross-repo notification workflows |
