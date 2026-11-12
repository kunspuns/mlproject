r"""
qbecat_bundle.py - recreates the qbecat repository from this single file.

HOW TO USE (office machine):
  1. In VS Code: File > New File, paste ALL of this file, save as  C:\dev\qbecat_bundle.py
  2. In the terminal:   cd C:\dev   then   python qbecat_bundle.py
  3. It writes every file into  C:\dev\qbecat\  and checks each one against its
     fingerprint (SHA-256). "ALL N FILES OK" means the paste was perfect.

Everything below the marker line is the repository's files, as comments:
  # @@FILE <path> <sha256>   starts a file; the following "# " lines are its contents.
Plain, readable text only: you can scroll down and read every line before running.
"""
import hashlib, sys
from pathlib import Path

def norm(text):
    return "\n".join(l.rstrip() for l in text.replace("\r\n", "\n").split("\n")).rstrip("\n") + "\n"

def unpack(target="qbecat"):
    lines = Path(__file__).read_text(encoding="utf-8").splitlines()
    start = lines.index("# @@BUNDLE-START") + 1
    files, current = {}, None
    for line in lines[start:]:
        if line.startswith("# @@FILE "):
            _, _, path, digest = line.split(" ", 3)
            current = (path, digest.strip()); files[current] = []
        elif line.startswith("# @@END"):
            break
        elif current is not None:
            files[current].append(line[2:] if line.startswith("# ") else "")
    target = Path(target)
    if target.exists() and any(target.iterdir()):
        sys.exit(f"'{target}' already exists and is not empty; rename or delete it first.")
    bad = []
    for (path, digest), body in files.items():
        text = norm("\n".join(body))
        dest = target / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8", newline="\n")
        if hashlib.sha256(text.encode("utf-8")).hexdigest() != digest:
            bad.append(path)
    if bad:
        print(f"{len(bad)} FILE(S) DAMAGED IN THE PASTE, re-copy the bundle:")
        for p in bad: print("   ", p)
        sys.exit(1)
    print(f"ALL {len(files)} FILES OK -> {target.resolve()}")

if __name__ == "__main__":
    unpack(sys.argv[1] if len(sys.argv) > 1 else "qbecat")

# @@BUNDLE-START
# @@FILE .azuredevops/pull_request_template.md b3f8555d9a37b28f7d24e2dc75850df2d491a10c9bc15a851effc50fc60ac9c7
# ## What does this change?
#
#
# ## Why?
#
#
# ## Checklist
# - [ ] Tests added or updated (synthetic data only)
# - [ ] `python -m pytest` passes locally
# - [ ] `CHANGELOG.md` updated
# - [ ] Docs updated if behaviour changed
# - [ ] No real data, server/database/table names or credentials in the diff
# @@FILE .gitignore 16c51f288fd151d7d27c3e8e4f8ff26cc5d410de3fa05ccd91cb9d3d35822955
# settings.yaml
# *.log
# out/
# *_debug.xlsx
# __pycache__/
# *.egg-info/
# .venv/
# .pytest_cache/
# dist/
# build/
# test-results.xml
# *.whl
# *.xlsx
# !examples/**/*.xlsx
# data/
# .DS_Store
# @@FILE CHANGELOG.md 26da7f29b5179636dfa9e63a80f8eaecb34397e8dc1c58c0abb4b6222afa2c6a
# # Changelog
#
# ## Unreleased
# - Repository foundations: src/ layout, Azure DevOps pipeline (build wheel → install → test → artifact; publish on v* tags), docs/ with setup, workflow, CI/CD, architecture, methodology and decision records, PR template
# - Version is set only in pyproject.toml
#
# ## 0.1.0 — first team release
# - trace.Pipeline: step-by-step runs with trace, follow, rerun, dump, checks
# - io: aliased engines, SQL templates (YEQT occurrences, n_years, group ELT, account ELTs, reference marginals), validated loaders, show_sql
# - simulation: shared Beta severity, occurrence and year losses from YEQT quantiles, synthetic data
# - ep: OEP/AEP/TVaR/AAL tables (rank convention), closed-form OEP cross-check
# - financial: layers, quota share, aggregate cover, exposed limit as 8 traced steps
# - marginal: port of mi_v3 (last-in exact/smoothed, kernel co-VaR, co-TVaR, standalone) without globals; vectorised last-in
# - cleansing: rule registry, flag-don't-fix, gated autofix, per-table export blocking, sentinels at export, audit trail, division YAML with extends
# - 41 tests incl. exact match to the mi_v3 notebook and brute-force last-in
# @@FILE README.md f4530bf7d448394db5bb76765825181db424c26696b20743b6083fdfddf101a4
# # qbecat
#
# The cat modelling team's shared Python library: simulation from YEQT, EP
# curves, exposed limit, marginal impact and divisional exposure cleansing.
# It is built so that when a number looks wrong you can find the step that made
# it wrong.
#
# ```python
# import qbecat as qc
# from qbecat.simulation import occurrence_losses, year_losses
#
# ylt = year_losses(occurrence_losses(elt, occurrences))
# qc.ep.ep_table(ylt, n_years, [10, 100, 200, 250])
# ```
#
# ## Quick links
# - **New here?** [Getting started](docs/getting-started.md) · [Git setup](docs/git-setup.md) · [Git workflow](docs/git-workflow.md)
# - **How it works:** [Architecture](docs/architecture.md) · [Debugging](docs/debugging.md) · [Conventions](docs/conventions.md)
# - **Methods:** [Marginal impact](docs/methodology/marginal-impact.md) · [Exposed limit](docs/methodology/exposed-limit.md)
# - **Releases:** [CI/CD](docs/ci-cd.md) · [CHANGELOG](CHANGELOG.md)
# - **All docs:** [docs/index.md](docs/index.md)
#
# ## Layout
# ```
# src/qbecat/     the library           tests/      pytest, synthetic data only
# docs/           documentation          examples/   runnable scripts
# config/         settings template      azure-pipelines.yml   CI/CD
# ```
#
# ## Install
# ```bat
# python -m venv .venv
# .venv\Scripts\activate
# python -m pip install -e ".[sql,dev]"
# python -m pytest
# ```
#
# ## Contributing
# Branch → change code **and** tests → pull request into `main`. The pipeline
# must pass before merge. No real data or system names in the repo. See
# [Git workflow](docs/git-workflow.md).
# @@FILE azure-pipelines.yml fb6dd2cbb8dc12e7ba42adcd55f5e32fe7d24137e78274a1a91aafe28f939949
# # Azure DevOps pipeline for qbecat.
# #
# # What it does
# #   Every pull request into main, and every push to main:
# #     build the wheel -> install that wheel -> run all tests against it -> keep the wheel as a download
# #   Every version tag (v0.2.0, v1.0.0, ...):
# #     all of the above, then publish the wheel to the team's Azure Artifacts feed
# #     (only once the feed exists and the 'feedName' variable below is filled in)
# #
# # Tests use synthetic data only, so the build machine never needs database access.
# # How to read results: Pipelines -> qbecat -> a run -> "Tests" tab and "1 published" artifact.
# # Full explanation: docs/ci-cd.md
#
# trigger:
#   branches:
#     include: [main]
#   tags:
#     include: ['v*']
#
# pr:
#   branches:
#     include: [main]
#
# variables:
#   pythonVersion: '3.11'      # keep in line with the version on the team's machines
#   feedRef: ''                # 'ProjectName/FeedName' (project-scoped feed) or 'FeedName' (org-scoped)
#   feedName: ''               # just 'FeedName'. Leave both empty until the feed exists = never publish
#
# stages:
# - stage: Build
#   displayName: Build and test
#   jobs:
#   - job: build_test
#     displayName: Build wheel, install it, run tests
#     pool:
#       vmImage: windows-latest   # same OS as the team. If the org uses its own agents, replace with:  name: <agent pool name>
#     steps:
#     - task: UsePythonVersion@0
#       inputs:
#         versionSpec: $(pythonVersion)
#       displayName: Use Python $(pythonVersion)
#
#     - script: |
#         python -m pip install --upgrade pip
#         python -m pip install build pytest
#       displayName: Install build tools
#
#     - script: python -m build
#       displayName: Build wheel and source package
#
#     # Install the BUILT wheel (not the source folder), so the tests prove the
#     # package that colleagues will install is complete (SQL files, YAML configs included).
#     # --no-index: take qbecat ONLY from dist/, never from the internet (a public
#     # package with the same name must never be picked up by mistake).
#     - script: |
#         python -m pip install numpy scipy pandas pyyaml openpyxl sqlalchemy
#         python -m pip install --no-index --find-links dist qbecat
#       displayName: Install the built wheel
#
#     - script: python -m pytest --junitxml=test-results.xml
#       displayName: Run tests
#
#     - task: PublishTestResults@2
#       condition: succeededOrFailed()
#       inputs:
#         testResultsFiles: test-results.xml
#         testRunTitle: qbecat tests
#       displayName: Publish test results
#
#     - task: PublishPipelineArtifact@1
#       inputs:
#         targetPath: dist
#         artifact: qbecat-dist
#       displayName: Keep the wheel as a pipeline artifact
#
# - stage: Publish
#   displayName: Publish to feed
#   dependsOn: Build
#   condition: and(succeeded(), startsWith(variables['Build.SourceBranch'], 'refs/tags/v'), ne(variables['feedName'], ''))
#   jobs:
#   - job: publish
#     pool:
#       vmImage: windows-latest
#     steps:
#     - download: current
#       artifact: qbecat-dist
#     - task: UsePythonVersion@0
#       inputs:
#         versionSpec: $(pythonVersion)
#     - script: python -m pip install twine
#       displayName: Install twine
#     - task: TwineAuthenticate@1
#       inputs:
#         artifactFeed: $(feedRef)
#       displayName: Authenticate to the feed
#     - script: python -m twine upload -r "$(feedName)" --config-file $(PYPIRC_PATH) $(Pipeline.Workspace)/qbecat-dist/*
#       displayName: Upload to the feed
# @@FILE config/settings.example.yaml 8e53bf74062b04bcc8c3a06acd7de1b934497c9bc1a4f81b058dd44685a25d62
# # Copy to settings.yaml (next to your notebook) or point QBECAT_CONFIG at it.
# # Real server, database and table names go ONLY in your local copy.
# # Never commit the filled-in file.
#
# odbc_driver: "ODBC Driver 17 for SQL Server"
#
# engines:                      # code refers to these aliases only
#   RMS:         {server: "<RMS_SERVER>",         database: "<RMS_DATABASE>"}          # account ELTs (RDM)
#   QBE_MAIN:    {server: "<QBE_MAIN_SERVER>",    database: "<QBE_MAIN_DATABASE>"}     # group ELT, reference marginals
#   QBE_SANDBOX: {server: "<QBE_SANDBOX_SERVER>", database: "<QBE_SANDBOX_DATABASE>"}  # YEQT, vendor event map
#   # LOCAL:     {url: "sqlite:///scratch.db"}    # any SQLAlchemy URL also works
#
# tables:                       # {key} placeholders in qbecat/io/queries/*.sql
#   yeqt:                "<YEQT_TABLE>"             # e.g. schema.table
#   yeqt_info:           "<YEQT_INFO_TABLE>"
#   sim_table_info:      "<SIM_TABLE_INFO_TABLE>"
#   vendor_events_map:   "<VENDOR_EVENTS_MAP_TABLE>"
#   group_elt:           "<GROUP_ELT_TABLE>"
#   rdm_account:         "<RDM_ACCOUNT_TABLE>"
#   rdm_account_std:     "<RDM_ACCOUNT_STD_TABLE>"
#   reference_marginals: "<REFERENCE_MARGINALS_TABLE>"
#
# # Analysis identifiers for a run live in the notebook or a small run config,
# # not here (they change every quarter).
# @@FILE docs/.order 345abe88ade3b29a2c71c16aba3c0321d7012abac69849c2e5941f7775f13e63
# index
# getting-started
# git-setup
# git-workflow
# ci-cd
# architecture
# debugging
# conventions
# extending
# methodology
# decisions
# @@FILE docs/architecture.md 204d1023622e344e745680bed50779b53fff2a2b340328e8d95273f0dc6f223a
# # Architecture
#
# ## Three layers; data only flows downward
#
# ```
# ┌──────────────────────────────────────────────────────────────┐
# │ 1. FOUNDATIONS   config · log · trace · schema · utils       │  used by everything
# ├──────────────────────────────────────────────────────────────┤
# │ 2. DATA IN/OUT   io/  (engines, queries/*.sql, loaders)      │  the only layer that
# │                                                              │  touches databases/files
# ├──────────────────────────────────────────────────────────────┤
# │ 3. CALCULATIONS  simulation → financial → ep → marginal      │  pure maths:
# │                  cleansing (separate branch)                 │  DataFrame in, DataFrame out
# └──────────────────────────────────────────────────────────────┘
# ```
#
# **The key rule:** calculation modules never open a connection. They receive
# validated DataFrames from `io`, so every one of them is testable on synthetic
# data on any machine, including the build machine.
#
# ## Repository layout
#
# ```
# qbecat/                         ← repo root
# ├── README.md                   front page
# ├── CHANGELOG.md                what changed in each version
# ├── pyproject.toml              package definition; the ONLY place the version is set
# ├── azure-pipelines.yml         CI/CD: build → test → package → publish
# ├── .azuredevops/               pull request template
# ├── config/
# │   └── settings.example.yaml   template for engine aliases + table names (real file is git-ignored)
# ├── docs/                       this documentation (publishable as the project wiki)
# │   ├── methodology/            definitions of the methods, with formulas
# │   └── decisions/              short records of design decisions
# ├── src/qbecat/                 THE LIBRARY
# │   ├── config.py · log.py · trace.py · schema.py · utils.py      foundations
# │   ├── io/                     engines, queries/*.sql, loaders, files
# │   ├── simulation/             severity (Beta), occurrence + year losses, synthetic data
# │   ├── financial/              terms, layers, exposed limit
# │   ├── ep/                     OEP/AEP/TVaR/AAL, closed-form OEP
# │   ├── marginal/               tail, window, measures, run
# │   └── cleansing/              rules, stages, run, divisions/*.yaml
# ├── tests/                      pytest, synthetic data only
# └── examples/                   runnable scripts (# %% cells)
# ```
#
# Code sits under `src/` on purpose: tests then run against the *installed*
# package, exactly what colleagues get, rather than the folder they happen to
# be in ([decision 0001](decisions/0001-src-layout.md)).
#
# ## Layer 1: foundations
#
# | File | Job |
# |---|---|
# | `config.py` | Reads `settings.yaml`: engine aliases and table names. Supports `extends:` for layered YAML. |
# | `schema.py` | Canonical columns; `validate()` reports every problem with row numbers. |
# | `trace.py` | `Pipeline`: the debugging core (below). |
# | `log.py` | `configure_logging()`. The library never prints. |
# | `utils.py` | RP ↔ probability, FX conversion, chunking. Deliberately small. |
#
# ## Layer 2: `io/`
#
# ```
# settings.yaml ──► engines.py ──► sql.py ──► queries/*.sql ──► loaders.py ──► canonical, validated DataFrame
# ```
#
# One query per `.sql` file (`{table}` from settings, `:param` bound by the
# driver). One loader per source: run query → rename to canonical columns →
# validate. A bad extract fails at load time with row numbers.
# `show_sql()` gives paste-ready SQL for SSMS.
#
# ## Layer 3: calculations
#
# ```
#           ELT                 occurrences (YEQT)
#            │                         │
#  simulation/severity.py              │   ELT moments → Beta parameters (ONE definition)
#            └──────────┬──────────────┘
#                       ▼
#  simulation/losses.py   occurrence losses → year losses (OEP max, AEP sum)
#         ┌─────────────┼──────────────────┐
#         ▼             ▼                  ▼
#    financial/       ep/              marginal/
#    layers, QS,      OEP/AEP,         tail → window → allocation,
#    exposed limit    TVaR, AAL        last-in, standalone
# ```
#
# `cleansing/` is a separate branch: ingest → map → normalise → evaluate → apply → export.
#
# ## The core: `Pipeline`
#
# Every multi-step calculation is a list of small named functions:
#
# ```python
# Pipeline("exposed_limit", [
#     step(check_exposure),
#     step(location_tiv),
#     step(after_deductible),
#     step(after_location_limit, check=_never_above_tiv),
#     step(policy_gross),
#     step(policy_exposed),
#     step(allocate_to_locations, check=_allocation_adds_up),
#     step(summarise, group_by=["country"]),
# ], watch=["tiv", "exposed_limit"])
# ```
#
# - By default each step receives the previous step's output.
# - A step can also ask for any named input by parameter name, either from
#   `run(...)` keywords or from an earlier step's name.
# - `use={"param": "name"}` renames an input when needed.
#
# Every run records its trace, each step's outputs and inputs, and the results
# of any checks. See [Debugging](debugging.md). Every top-level function returns
# `(result, pipe)`.
# @@FILE docs/ci-cd.md f0ee61b898fd4b9affcbd50659530739ff89dbbe330f931d922beb762393020c
# # CI/CD: how the library is tested and packaged automatically
#
# **CI (continuous integration)**: every proposed change is built and tested
# automatically before it can join `main`.
# **CD (continuous delivery)**: every release is packaged and published
# automatically, so colleagues install a version instead of copying folders.
#
# The definition is one file at the repo root, `azure-pipelines.yml`.
#
# ## What runs when
#
# | Event | What happens |
# |---|---|
# | Pull request into `main` | Build the wheel → install it → run all tests. The PR shows pass/fail; with the branch policy on, a failing PR cannot merge. |
# | Push / merge to `main` | Same, and the wheel is kept as a downloadable **pipeline artifact**. |
# | Version tag `v*` (e.g. `v0.2.0`) | Same, then the wheel is **published to the team feed** (once the feed is configured). |
#
# The tests install the **built wheel**, not the source folder. That catches the
# classic packaging mistake, a file missing from the package (an SQL query or
# a division YAML), before a colleague finds it.
#
# Tests use synthetic data only, so the build machine never needs a database
# connection or access to real data.
#
# ## Making a release
#
# 1. Update `version` in `pyproject.toml`. It is the only place the version
#    lives; `qbecat.__version__` reads it.
#    - `0.1.0 → 0.1.1` for fixes, `0.2.0` for new features, `1.0.0` once the
#      team relies on it in production.
# 2. Add a section to `CHANGELOG.md`.
# 3. Merge via pull request.
# 4. Tag the merged commit and push the tag:
#    ```bat
#    git switch main
#    git pull
#    git tag v0.2.0
#    git push origin v0.2.0
#    ```
#    The pipeline runs and publishes `qbecat 0.2.0`.
#
# ## Installing a released version
#
# **Until a feed exists:** open a pipeline run → *1 published* → download
# `qbecat-0.x.y-py3-none-any.whl`, then
# ```bat
# python -m pip install qbecat-0.x.y-py3-none-any.whl
# ```
#
# **Once the feed exists:**
# ```bat
# python -m pip install artifacts-keyring
# python -m pip install qbecat --index-url https://pkgs.dev.azure.com/<org>/<project>/_packaging/<feed>/pypi/simple/
# ```
# `artifacts-keyring` signs you in with your work account (browser pop-up the first time).
#
# ## Setting up the feed (once, by someone with rights)
#
# 1. **Artifacts → Create Feed** → name e.g. `qbecat-feed`, scope *Project*.
# 2. Feed settings → Permissions → add **<project> Build Service (<org>)** as *Feed Publisher (Contributor)*.
# 3. In `azure-pipelines.yml` set `feedRef: '<project>/qbecat-feed'` and `feedName: 'qbecat-feed'`.
#
# Leave **upstream sources** (public PyPI through the feed) off unless needed. If
# they are turned on, keep the feed as the first index, so a public package that
# happens to share the name `qbecat` can never be installed by mistake.
#
# ## Reading a failed run
#
# Pipelines → qbecat → the red run → click the failed step. The log ends with
# the pytest output: the failing test, the assertion, and the values involved.
# Reproduce it locally with `python -m pytest tests/test_<file>.py -k <test name>`.
# @@FILE docs/conventions.md de6d764a4b9e44bd7f8d402251e3a5777b8aab5b27e7e75b6acaa7b2e4111688
# # Conventions
#
# These hold across the whole library. Changing one is a [decision](decisions/), not a code tweak.
#
# ## Canonical columns
# Loaders map source names once; everything downstream uses these:
#
# | Table | Columns |
# |---|---|
# | ELT | `event_id, mean_loss, sd_i, sd_c, exposure` [+ `rate`, `account_id`] |
# | occurrences | `year, sim_event_id, instance_id, event_id, quantile` |
# | occurrence losses | `year, sim_event_id, instance_id, loss` [+ `account_id`] |
# | exposure | `location_id, policy_id` + `tiv` or `building, contents, bi` + terms |
#
# `event_id` is the ELT's (vendor) event key. Several ELT events can map to one
# simulated occurrence `(year, sim_event_id, instance_id)`; their losses are summed.
#
# ## Years and return periods
# - **`n_years` is always passed explicitly.** Year tables list only years with
#   events; EP functions fill in the zero years. More year rows than
#   `n_years` raises an error.
# - **Loss at return period T** is read at rank `round(n_years / T)`, worst
#   year = rank 1. TVaR at T = average of the worst `round(n_years / T)` years.
#
# ## Severity
# Damage ratio ~ Beta, moment-matched to
# $\mu = \text{mean\_loss}/\text{exposure}$ and $\sigma = (\text{sd\_i} + \text{sd\_c})/\text{exposure}$,
# defined once in `simulation/severity.py`:
# - `repaired`: variance at or above the Beta bound $\mu(1-\mu)$, capped just under it, mean preserved
# - `degenerate`: zero SD, zero mean or mean ≥ exposure; a point mass at the mean (capped at exposure)
#
# ## Simulation
# - **Common random numbers:** every table read against the same occurrences
#   uses the same quantile per occurrence.
# - **Joins:** same-server joins in SQL (`io/queries`), cross-server joins in
#   Python (`simulation/losses.py`). Use `chunk_years=` if memory is tight.
#
# ## Cleansing
# - Rules only flag. A fix is applied only if the rule declares `autofix=True`
#   **and** the division's `autofix_allowlist` lists it.
# - An open CRITICAL finding blocks that table's export only.
# - Sentinels are filled in on the export copy only.
# - Every broker row keeps its Excel row number in `_row`.
#
# ## Code
# - Functions take inputs as arguments and return new objects; they never
#   modify their inputs.
# - The library logs and never prints.
# - No real server, database or table names, and no real data, in the repository.
# @@FILE docs/debugging.md 1acc85a56eff86ff723a8c65f7fc6fafc9840d4ed449698b88f63c1eb12c5888
# # Debugging
#
# Exposed limit, marginal impact and cleansing are each a `Pipeline`. Every
# run function returns `(result, pipe)`. Keep `pipe`; it holds the full record of the run.
#
# | You want to… | Do this |
# |---|---|
# | see what the calculation consists of | `pipe.describe()` |
# | see where a total changed | `pipe.trace`: rows in/out, seconds, new columns, control totals per step |
# | see what one step produced | `pipe.outputs["after_deductible"]` |
# | follow one policy / account / broker row through every step | `pipe.follow(policy_id=17, changes_only=True)` |
# | see one policy's full exposed-limit calculation | `financial.explain_policy(pipe, 17)` |
# | run only part of it | `pipe.run(data, stop_after="policy_gross")` |
# | fix a step and retry just that step | edit the function, then `pipe.rerun("policy_exposed")` |
# | hand someone the whole run | `pipe.dump("debug.xlsx")`: trace plus one sheet per step |
# | check a query in SSMS | `io.show_sql("account_elts", analysis_id=112, persp_code="RL")` |
# | see every query and step as it runs | `qc.configure_logging()` (add `logfile=` to keep it) |
#
# ## When something goes wrong
#
# - **A step raises.** The error names the step and summarises its inputs.
#   Earlier outputs stay in `pipe.outputs`; the failing step's inputs are in
#   `pipe.inputs["<step>"]`.
# - **A check fails.** The run stops at the first step whose output breaks a
#   rule (e.g. exposed value ≤ TIV), not three steps later.
# - **A bad extract.** Loaders validate on arrival:
#   `mean_loss > exposure: 3 rows (e.g. index 14, 88, 301)`.
# - **A missing input.** The error lists which inputs exist and how to wire one in.
#
# ## Compared with a stored procedure
#
# | Stored procedure | qbecat |
# |---|---|
# | One 600-line block | Small functions with one-line docstrings |
# | Intermediate results vanish unless temp tables are added by hand | Every intermediate is kept |
# | "Why is policy X wrong?" means re-running pieces by hand | `explain_policy(pipe, X)` |
# | The definition is changed inside the block | Swap one step |
# | No tests | A hand-calculated test per edge case |
# @@FILE docs/decisions/.order a71cb6797cfa4eaa9cce28f4aa5c03987f0c0607555c9f35740f03db55a8170d
# 0000-template
# 0001-src-layout
# 0002-pipelines-of-small-steps
# 0003-no-real-data-in-repo
# @@FILE docs/decisions/0000-template.md 1725fca991e79797582aa8608107efaa5d1fed70bf812bacb00ab20803849998
# # NNNN: Title
#
# - **Date:**
# - **Status:** proposed / accepted / replaced by NNNN
#
# ## Context
# What problem or choice came up.
#
# ## Decision
# What we decided.
#
# ## Consequences
# What becomes easier, what becomes harder, what we must remember.
# @@FILE docs/decisions/0001-src-layout.md e2b8fe15fbc1acd06392479b13120c5c75591e144f3cdecb48b2999dec1ba239
# # 0001: Library code lives under `src/`
#
# - **Date:** 2026-11
# - **Status:** accepted
#
# ## Context
# With the package folder at the repo root, tests import whatever folder they
# run in. They can pass even when the installed package is missing files.
#
# ## Decision
# Code lives in `src/qbecat/`. CI builds the wheel, installs it, and runs the
# tests against the installed copy.
#
# ## Consequences
# Install with `python -m pip install -e .` before running tests locally.
# Packaging mistakes (a missing `.sql` or `.yaml`) fail in CI, not on a colleague's machine.
# @@FILE docs/decisions/0002-pipelines-of-small-steps.md c5a46f40d84b3e9727671e9a4f68e4be548bd0e4cb0876888ed20f35770742ca
# # 0002: Multi-step calculations are pipelines of small named steps
#
# - **Date:** 2026-11
# - **Status:** accepted
#
# ## Context
# Large stored procedures (e.g. exposed limit) were hard to debug: intermediate
# results weren't visible, and isolating a wrong number meant re-running pieces by hand.
#
# ## Decision
# Multi-step calculations are `qbecat.trace.Pipeline`s of small functions,
# each taking inputs and returning a new table. Every run records the outputs,
# inputs, timings and control totals of every step.
#
# ## Consequences
# Any intermediate value can be inspected (`follow`, `explain_policy`, `dump`).
# Changing a definition means changing one step. Steps must never modify their inputs.
# @@FILE docs/decisions/0003-no-real-data-in-repo.md dfff7939c5b9954816039c510e5151942e760c0dedf5b1b837e75410ef85255f
# # 0003: No real data or real system names in the repository
#
# - **Date:** 2026-11
# - **Status:** accepted
#
# ## Context
# The repository is shared and its history is permanent. Exposure data, ELTs
# and system names must not leak into it, and CI build machines have no
# database access.
#
# ## Decision
# - Server, database and table names live only in a local `settings.yaml`
#   (git-ignored); code uses aliases.
# - Tests and examples use synthetic data (`qbecat.simulation.synthetic_*`).
# - Real-data runs happen in notebooks outside the repo, or in git-ignored folders.
#
# ## Consequences
# CI can run every test anywhere. Validating against real numbers is done
# separately and recorded as a result, not as data in the repo.
# @@FILE docs/extending.md e3dd62214426a3cdaf1c6db2aa402953d99f2d403302b07725484cddae3da9d1
# # Extending the library
#
# | To add… | Do this |
# |---|---|
# | a query | Add `my_query.sql` to `src/qbecat/io/queries/` (`{table_key}` for tables, `:param` for values), add the table to settings, call `run_query("my_query", "QBE_MAIN", param=...)` |
# | a loader | A short function in `io/loaders.py`: `run_query` → `to_canonical` → `validate` |
# | a cleansing rule | One function with `@rule("name", table=..., column=..., severity=...)` returning a mask, or `(mask, proposed)` for a fixable rule |
# | a division | `src/qbecat/cleansing/divisions/XYZ.yaml` starting `extends: base.yaml`, overriding only what differs |
# | a change to exposed limit | Edit one step in `financial/exposed_limit.py`, or build your own step list |
# | a new pipeline | `Pipeline("name", [step(f1), step(f2, use={"elt": "group_elt"}), ...])` |
#
# ## Rules for step functions
# 1. Take inputs as arguments; return a new object; never modify an input.
# 2. One job each, named after what it produces.
# 3. A one-line docstring (`pipe.describe()` shows it).
#
# ## Every change comes with
# - a test in `tests/` (synthetic data; a hand-calculated case is best)
# - a line in `CHANGELOG.md`
# - a docs update if behaviour changed
# @@FILE docs/getting-started.md e404635e9be5614187cf202dff9cf8a575c5d1717568c78ff5c2e9e66392ed7a
# # Getting started
#
# ## Install (work machine)
#
# Everything goes through `python -m`, which works under AppLocker.
#
# ```bat
# cd C:\dev\qbecat
# python -m venv .venv
# .venv\Scripts\activate
# python -m pip install -e ".[sql,dev]"
# python -m pytest
# ```
#
# `-e` (editable) means your code changes take effect without reinstalling. To
# use a released version instead of the source, see [CI/CD](ci-cd.md#installing-a-released-version).
#
# ## Settings
#
# Copy `config/settings.example.yaml` to `settings.yaml` next to your notebook
# (or set `QBECAT_CONFIG` to its path) and fill in servers, databases and
# table names. Code only ever uses the aliases `RMS`, `QBE_MAIN` and
# `QBE_SANDBOX`. `settings.yaml` is git-ignored; never commit it.
#
# ## First EP curve
#
# ```python
# import qbecat as qc
# from qbecat import io
# from qbecat.simulation import occurrence_losses, year_losses
#
# qc.configure_logging()                       # see each query / step with rows and seconds
#
# occ = io.load_occurrences(yeqt_id=..., vendor_version_id=..., hazard_zone_id=...)
# n_years = io.load_n_years(yeqt_id=...)
# elt = io.load_group_elt(port_grouping_id=..., hazard_grouping_id=...)
#
# ylt = year_losses(occurrence_losses(elt, occ))
# qc.ep.ep_table(ylt, n_years, [10, 100, 200, 250])          # OEP, AEP, TVaRs; AAL in .attrs
# ```
#
# | Task | Call | Example |
# |---|---|---|
# | EP curve | `ep.ep_table(ylt, n_years, rps)` | `examples/01_ep_curves.py` |
# | Exposed limit | `financial.exposed_limit(exposure, group_by)` | `examples/02_exposed_limit_debugging.py` |
# | Marginal impact | `marginal.run_marginal_impact(group_elt, account_elts, occ, n_years)` | `examples/03_…`, `05_marginal_impact_production.py` |
# | Cleansing | `cleansing.run_cleansing("broker.xlsx", "EO", out_dir="out")` | `examples/04_cleansing.py` |
#
# The examples run on synthetic data on any machine. In VS Code the `# %%`
# markers make them run as notebook cells.
# @@FILE docs/git-setup.md 95579d1bf7444f162b9dd3c207502eddfd6f6d4062baf5cc1c11d5660daab296
# # One-time setup: VS Code + Git + Azure DevOps
#
# Goal: on a work machine, clone the `qbecat` repo, prove we can **pull** and
# **push**, and get the pipeline running. Allow about an hour; most of it is
# waiting for access if something is missing.
#
# ## What you need (check these first)
#
# | Need | How to check | If missing |
# |---|---|---|
# | **Basic** access level in Azure DevOps (not *Stakeholder*) | You can see **Repos** in the left menu of the project | Ask an org admin to change your access level to Basic |
# | **Contribute** permission on the repo | Step 4 below tests it | Project admin: Project settings → Repositories → qbecat → Security → your user/group → *Contribute* = Allow |
# | **Git for Windows** installed | In VS Code: `Ctrl+`` ` (terminal) → `git --version` prints a version | Request *Git for Windows* through the company software portal / IT. Don't use portable copies that sidestep AppLocker |
#
# VS Code's Git support is **built in**: the Source Control panel (`Ctrl+Shift+G`).
# It needs Git for Windows underneath but **no extension**. The old "Azure Repos"
# extension is not needed.
#
# ## Step 1: tell Git who you are (once per machine)
#
# ```bat
# git config --global user.name  "Your Name"
# git config --global user.email "your.work@email"
# git config --global http.sslBackend schannel
# ```
#
# The last line makes Git trust the same certificates as Windows. It is the
# standard fix for `SSL certificate problem: unable to get local issuer
# certificate` behind a corporate proxy, and it is harmless if you don't need it.
#
# ## Step 2: clone the repo
#
# 1. In Azure DevOps: **Repos → Files → Clone** (top right) → copy the HTTPS URL,
#    which looks like `https://dev.azure.com/<org>/<project>/_git/qbecat`.
#    (The **Clone in VS Code** button there also works.)
# 2. In VS Code: `Ctrl+Shift+P` → **Git: Clone** → paste the URL → choose a folder.
#    - Use a plain local folder such as `C:\dev\`. **Not** a OneDrive-synced folder:
#      OneDrive and Git fight over the same files.
# 3. A browser window asks you to sign in with your **work account**. That is Git
#    Credential Manager, which ships with Git for Windows. Sign in once and it
#    remembers you.
#    - No pop-up, or sign-in fails? Use a Personal Access Token instead: Azure
#      DevOps → user icon (top right) → **Personal access tokens** → New → scope
#      **Code: Read & write**, expiry 30–90 days. Use the token as the password
#      when Git asks. Treat it like a password and never paste it into code.
#
# If the clone succeeds, **pull works**: you have read access.
#
# ## Step 3: install the library from your clone
#
# ```bat
# cd C:\dev\qbecat
# python -m venv .venv
# .venv\Scripts\activate
# python -m pip install -e ".[sql,dev]"
# python -m pytest
# ```
#
# All tests should pass. In VS Code select the interpreter `.venv\Scripts\python.exe`
# (`Ctrl+Shift+P` → *Python: Select Interpreter*).
#
# ## Step 4: the permission test (pull → edit README → push)
#
# Do it on a **branch**. `main` should eventually only change through reviewed
# pull requests (see *Branch policy* below).
#
# VS Code way:
# 1. Bottom-left corner, click the branch name `main` → **Create new branch** → `test/readme-<yourname>`
# 2. Edit `README.md` (add a line, e.g. "Setup tested by <name> on <date>"), save.
# 3. Source Control panel → the file appears under *Changes* → `+` to stage →
#    type a message ("Test push from <name>") → **Commit**.
# 4. Click **Publish Branch**. This is the push.
# 5. In Azure DevOps: **Repos → Pull requests → New pull request** from your
#    branch into `main` → Create. If you have rights, complete (merge) it.
#
# Same thing from the terminal:
# ```bat
# git switch -c test/readme-yourname
# :: edit README.md
# git add README.md
# git commit -m "Test push from yourname"
# git push -u origin test/readme-yourname
# ```
#
# Record the results:
#
# | Check | Result |
# |---|---|
# | Clone / pull | ☐ works |
# | Push a branch | ☐ works ☐ rejected (message: …) |
# | Open a pull request | ☐ works |
# | Complete (merge) the pull request | ☐ works ☐ needs a reviewer/admin |
# | Direct push to `main` | ☐ allowed ☐ blocked by policy (good, once policies are on) |
#
# ## Step 5: create the pipeline
#
# 1. **Pipelines → New pipeline → Azure Repos Git → qbecat → Existing Azure Pipelines YAML file**
#    → path `/azure-pipelines.yml` → **Run**.
# 2. Watch the run: a green **Build and test** stage, a **Tests** tab with the
#    results, and **1 published** artifact (the wheel).
#
# If it doesn't run:
# - *"No hosted parallelism has been purchased or granted"*: the organisation
#   has no Microsoft-hosted build minutes. Either an admin requests or buys
#   them, or we use the organisation's own build agents. Ask which agent
#   pools exist (Project settings → Agent pools) and replace
#   `vmImage: windows-latest` with `name: <pool name>` in `azure-pipelines.yml`.
# - *No permission to create a pipeline*: a project admin can create it, or
#   grant *Create build pipeline* to the team.
#
# ## Step 6: branch policy on `main` (a project admin does this once)
#
# **Repos → Branches → `main` → … → Branch policies**:
# - *Require a minimum number of reviewers*: 1 (allow requestors to approve
#   their own changes while the team is small, if preferred)
# - *Build validation*: add the qbecat pipeline, set to **Required**
#
# After this, nothing reaches `main` without passing all tests. That is the
# foundation the rest of the work relies on.
#
# ## Troubleshooting
#
# | Message | Meaning | Fix |
# |---|---|---|
# | `'git' is not recognized…` | Git for Windows not installed or not on PATH | Install it; restart VS Code |
# | `TF401019: The Git repository … does not exist or you do not have permissions` | Wrong URL or no read access | Re-copy the URL from Repos → Clone; ask for access |
# | `TF401027: You need the Git 'GenericContribute' permission…` | You can read but not push | Ask for *Contribute* on the repo |
# | `TF402455: Pushes to this branch are not permitted; you must use a pull request` | Branch policy on `main`; working as intended | Push a branch and open a PR |
# | `Authentication failed` / `401` | Stale or expired credentials | Windows *Credential Manager* → Windows Credentials → remove entries for `git:https://dev.azure.com…` → retry; or create a new PAT |
# | `SSL certificate problem: unable to get local issuer certificate` | Corporate proxy | `git config --global http.sslBackend schannel` |
# | Repos menu missing in Azure DevOps | Stakeholder access level | Ask for Basic access |
# @@FILE docs/git-workflow.md b5a3651c3d420591fde73c78d40f28c2d16cd4dad037f9a1b5e5d173c2006c94
# # Working with Git: the team workflow
#
# Plain-language version for people new to Git. Setup is in [git-setup.md](git-setup.md).
#
# ## The six words you need
#
# | Word | Meaning |
# |---|---|
# | **repository (repo)** | The project folder plus its full history. The master copy lives in Azure DevOps; everyone has a local copy. |
# | **commit** | A saved snapshot of your changes with a message. Local until you push. |
# | **branch** | A separate line of work. `main` is the trusted version; you work on your own branch. |
# | **push / pull** | Push sends your commits to Azure DevOps; pull brings everyone else's down. |
# | **pull request (PR)** | A request to merge your branch into `main`. The pipeline runs the tests and a colleague reviews. |
# | **merge** | Your branch's changes become part of `main`. |
#
# ## The everyday loop
#
# ```
# pull main → new branch → change code + tests → commit → push → pull request → tests pass + review → merge
# ```
#
# | Step | VS Code | Terminal |
# |---|---|---|
# | Get the latest | Branch `main` (bottom-left) → Source Control `…` → **Pull** | `git switch main` then `git pull` |
# | Start work | Bottom-left → **Create new branch** → `feature/short-name` | `git switch -c feature/short-name` |
# | Save a step | Source Control → stage `+` → message → **Commit** | `git add <files>` then `git commit -m "message"` |
# | Share it | **Publish Branch** / **Sync** | `git push -u origin feature/short-name` |
# | Ask to merge | Azure DevOps → Repos → Pull requests → New | — |
# | After merge | Switch to `main`, **Pull**, delete the old branch | `git switch main`, `git pull`, `git branch -d feature/short-name` |
#
# ## House rules
#
# 1. **Never commit real data or real names.** No exposure files, ELT extracts,
#    `settings.yaml`, server names or passwords. `.gitignore` blocks the usual
#    suspects; the rule still applies to anything it doesn't catch. Tests and
#    examples use synthetic data only.
# 2. **One change per branch, small PRs.** "Add exposure loader" is a good PR;
#    "various fixes" is not.
# 3. **Code and its tests travel together.** A PR that changes a calculation
#    changes or adds a test.
# 4. **Commit messages say what and why**, in the present tense:
#    `Cap Beta variance at bound instead of raising`.
# 5. **Docs change in the same PR** when behaviour changes (`docs/`, `CHANGELOG.md`).
# 6. **Don't rewrite shared history.** No `git push --force` on `main` or on
#    anyone else's branch.
#
# ## Branch names
#
# | Prefix | For |
# |---|---|
# | `feature/` | new functionality (`feature/exposure-loader`) |
# | `fix/` | bug fixes (`fix/rank-off-by-one`) |
# | `docs/` | documentation only |
# | `test/` | experiments, including the setup test |
#
# ## When two people changed the same lines (a conflict)
#
# Git marks the file in VS Code with **Merge Changes**. Open it, choose
# *Accept Current*, *Accept Incoming* or *Accept Both* for each block, save,
# stage, commit. If unsure, stop and ask. Nothing is lost until you commit.
#
# ## Undo cheatsheet
#
# | Situation | Command |
# |---|---|
# | Discard edits to a file (not committed) | VS Code: right-click file → *Discard Changes* |
# | Unstage a file | `git restore --staged <file>` |
# | Fix the last commit message (not pushed yet) | `git commit --amend -m "new message"` |
# | Undo a commit that is already pushed | `git revert <commit id>` (makes a new commit that reverses it) |
# @@FILE docs/index.md ecf77c5ef0d279df50ae6e5d1047417a543876295388453c0f5c3ded18a124f9
# # qbecat documentation
#
# The cat modelling team's shared Python library: simulation from YEQT, EP
# curves, exposed limit, marginal impact and divisional exposure cleansing.
#
# ## Start here
# | Page | For |
# |---|---|
# | [Getting started](getting-started.md) | Install, settings, first EP curve |
# | [Git setup](git-setup.md) | One-time: VS Code + Git + Azure DevOps on a work machine |
# | [Git workflow](git-workflow.md) | Day-to-day: branches, pull requests, house rules |
# | [CI/CD](ci-cd.md) | What the pipeline does; how to release and install a version |
#
# ## How the library works
# | Page | For |
# |---|---|
# | [Architecture](architecture.md) | The layers, the folders, how data flows |
# | [Debugging](debugging.md) | Finding the step where a number goes wrong |
# | [Conventions](conventions.md) | Column names, return periods, severity, n_years |
# | [Extending](extending.md) | Adding a query, loader, rule, division or step |
#
# ## Methodology
# | Page | |
# |---|---|
# | [Marginal impact](methodology/marginal-impact.md) | Last-in, kernel co-VaR, co-TVaR, standalone |
# | [Exposed limit](methodology/exposed-limit.md) | The step-by-step definition |
#
# ## Decisions
# Short records of why things are the way they are: [decisions/](decisions/).
# Add one whenever the team makes a choice someone will later ask about.
# @@FILE docs/methodology/.order 15389652a9278a1ffd4435487a08923bdc28eca28bc2fced6dc7dfe7c7b46f08
# marginal-impact
# exposed-limit
# @@FILE docs/methodology/exposed-limit.md 4cb376b081a73e9ff751121229658616b302f437b4d726ba25a1372572a5715b
# # Exposed limit
#
# Code: `src/qbecat/financial/exposed_limit.py`. One function per step, each
# adding one column, so every intermediate value is visible
# (`explain_policy(pipe, policy_id)`).
#
# > **Status: to be confirmed against the current stored procedure.** This is
# > a standard definition. Run both on one portfolio and compare by policy
# > before relying on it.
#
# | Step | Column added | Definition |
# |---|---|---|
# | 1 | `tiv` | building + contents + bi (or the given TIV) |
# | 2 | `after_deductible` | $\max(\text{tiv} - \text{deductible} - \text{deductible\_pct}\cdot\text{tiv},\ 0)$ |
# | 3 | `after_location_limit` | $\min(\text{after\_deductible},\ \text{location\_limit})$; blank limit = unlimited |
# | 4 | `policy_gross` | sum of `after_location_limit` over the policy's locations |
# | 5 | `policy_exposed` | $\text{share}\cdot\min(\max(\text{policy\_gross} - \text{attachment}, 0),\ \text{policy\_limit})$ |
# | 6 | `exposed_limit` | `policy_exposed` split back to locations in proportion to `after_location_limit` |
# | 7 | summary | totals by the chosen grouping (country, peril zone, …) |
#
# Checks built into the steps:
# - exposed value never exceeds TIV (step 3)
# - per policy, the allocated amounts sum to `policy_exposed` (step 6)
#
# ## Open questions
# - Deductible types used in the source (amount, % of TIV, % of loss, franchise?)
# - Policy-level deductibles or sub-limits by coverage?
# - Is the allocation back to location (step 6) what the reports need, or are they at policy level?
# @@FILE docs/methodology/marginal-impact.md cd9dcd5b1068501c45b1d026d312e4282ae489cdded8e00d946db270ac443bd6
# # Marginal impact
#
# How much of the group's 1-in-T OEP each account is responsible for.
# Code: `src/qbecat/marginal/`. Default T = 200.
#
# ## Inputs
# - account ELTs (RMS), loaded with a load factor on mean and SDs (not exposure)
# - group portfolio ELT (QBE main)
# - YEQT occurrences with loss quantiles (QBE sandbox) and `n_years`
#
# Group and accounts read **the same quantile** for each occurrence, so they
# see identical simulated years.
#
# ## Notation
# - $G_o$: group loss of occurrence $o$; $L_{a,o}$: account $a$'s loss.
# - Year OEP = largest occurrence loss in the year; years are ranked worst first.
#   $\text{OEP}_{(r)}$ is the OEP at rank $r$, and $d(r)$ is that year's *defining occurrence*.
# - Target rank $k = \text{round}(n\_years / T)$; group 1-in-T $= \text{OEP}_{(k)}$.
#
# ## Contribution
# Account losses are scaled so that, per occurrence, they never exceed the group:
#
# $$c_{a,o} = L_{a,o}\cdot\min\!\left(1, \frac{G_o}{\sum_b L_{b,o}}\right)$$
#
# Whatever the accounts don't cover is **other business**.
#
# ## The measures
#
# | Measure | Definition |
# |---|---|
# | **Last-in** | $\text{OEP}_{(k)} - \text{OEP}^{(-a)}_{(k)}$, where $\text{OEP}^{(-a)}$ re-ranks the years after replacing $G_o$ with $G_o - c_{a,o}$ |
# | **Last-in smoothed** | $\sum_r w_r\big(\text{OEP}_{(r)} - \text{OEP}^{(-a)}_{(r)}\big)$ with bell weights around $k$ |
# | **Kernel co-VaR** | $\sum_r w_r\, c_{a,d(r)}$ |
# | **Co-TVaR** | $\frac{1}{k}\sum_{r\le k} c_{a,d(r)}$ |
# | **Standalone** | the account's own OEP at rank $k$, ignoring everything else |
#
# Bell weights: $w_r \propto \exp\!\big(-\tfrac12((r-k)/s)^2\big)$ with spread
# $s = f\cdot k$, $f \in \{0.10, 0.20\}$, set to zero beyond $3s$, normalised to 1.
#
# Co-TVaR and kernel co-VaR add up exactly: accounts + other business = group figure.
#
# ## The window and exactness
# Contributions are computed only for the worst $K = \text{round}(k(1 + 3\max f))$
# years. Removing an account can only lower year OEPs, so the last-in answer is
# **exact** if the deepest rank read is still at or above $\text{OEP}_{(K+1)}$:
# no year from outside the window could have climbed in. Otherwise $K$ doubles
# for those accounts only.
#
# ## Verification (tests/test_marginal.py)
# - Reproduces the original `mi_v3` notebook exactly on synthetic data.
# - Last-in agrees with a brute-force recomputation over all years.
# - Allocations add up to the group exactly.
# - Standalone agrees with the EP engine.
# @@FILE examples/01_ep_curves.py fcc1bcc37357a9a68155b317dc1713e630334a6f919edb3c4751a3860a29e518
# # %% [markdown]
# # # EP curves from an ELT and a YEQT
# # Synthetic data here; with real data swap in the loaders (see 05_marginal_impact_production.py).
#
# # %%
# import qbecat as qc
# from qbecat.simulation import synthetic_elt, synthetic_occurrences, occurrence_losses, year_losses
#
# N_YEARS = 100_000
# elt = synthetic_elt(300, seed=0)                       # event_id, rate, mean_loss, sd_i, sd_c, exposure
# occ = synthetic_occurrences(elt, N_YEARS, seed=1)      # year, sim_event_id, instance_id, event_id, quantile
#
# # %% ELT -> occurrence losses -> year losses -> EP table
# occ_losses = occurrence_losses(elt, occ)
# ylt = year_losses(occ_losses)
# table = qc.ep.ep_table(ylt, N_YEARS, [10, 50, 100, 200, 250, 500])
# print(f"AAL {table.attrs['aal']:,.0f}")
# print(table)
#
# # %% Cross-check against the closed form (same Beta parameters, so differences are sampling noise)
# table["oep_analytic"] = qc.ep.analytic_loss_at_rp(elt, table["return_period"])
# table["rel_diff"] = table["oep"] / table["oep_analytic"] - 1
# print(table[["return_period", "oep", "oep_analytic", "rel_diff"]])
# @@FILE examples/02_exposed_limit_debugging.py fad78c9047e2ce754f332e0f9c3187f9bfa4eb3d5a0fa160e0c9b8fddd409bc9
# # %% [markdown]
# # # Exposed limit, and how to debug it
# # The calculation is 8 small steps instead of one stored procedure.
#
# # %%
# import qbecat as qc
# from qbecat.financial import exposed_limit, explain_policy
# from qbecat.simulation import synthetic_exposure
#
# exposure = synthetic_exposure(50, seed=3)
# summary, pipe = exposed_limit(exposure, group_by=["country", "peril_zone"])
# print(summary)
#
# # %% 1. What does the calculation consist of?
# print(pipe.describe())
#
# # %% 2. Control totals after every step: where does the total move?
# print(pipe.trace)
#
# # %% 3. One policy, inputs next to results, one row per location
# print(explain_policy(pipe, policy_id=3))
#
# # %% 4. One location through every step (only the steps where it changed)
# print(pipe.follow(location_id=14, changes_only=True))
#
# # %% 5. Stop part-way, or re-run a single step with a different input
# pipe.run(exposure, stop_after="policy_gross")
# print(pipe.outputs["policy_gross"].head())
# pipe.run(exposure)
# print(pipe.rerun("summarise", group_by=["country"]))
#
# # %% 6. Everything to Excel, one sheet per step
# pipe.dump("exposed_limit_debug.xlsx")
# @@FILE examples/03_marginal_impact.py 769c8f09ecea54a9124d8c54fee66abb0315a3527e7706539656225305e98221
# # %% [markdown]
# # # Marginal impact (synthetic data)
#
# # %%
# import qbecat as qc
# from qbecat.marginal import MarginalSettings, run_marginal_impact
# from qbecat.simulation import synthetic_accounts, synthetic_elt, synthetic_occurrences
#
# qc.configure_logging()          # shows each step, its time and size as it runs
# N_YEARS = 100_000
# group_elt = synthetic_elt(300, seed=0)
# account_elts = synthetic_accounts(group_elt, 40, seed=2)
# occurrences = synthetic_occurrences(group_elt, N_YEARS, seed=1)
#
# # %%
# summary, pipe = run_marginal_impact(group_elt, account_elts, occurrences, N_YEARS,
#                                     settings=MarginalSettings(return_period=200))
# print(pipe.trace[["step", "seconds", "rows_out"]])
# print(f"group 1-in-200 OEP: {pipe.outputs['tail'].rp_loss:,.0f}")
# print(pipe.outputs["allocations"].totals)          # accounts + other business = group
# print(summary.head(10))
#
# # %% Investigate one account
# acc = summary["account_id"].iloc[0]
# print(pipe.follow(account_id=acc).groupby("step").size())    # where it appears
# contrib = pipe.outputs["window"].contributions
# print(contrib[contrib["account_id"] == acc].sort_values("contribution", ascending=False).head())
# @@FILE examples/04_cleansing.py c914939775d64ec3e47c3ef5f714e2aa70d947568e930f15705921eb72150631
# # %% [markdown]
# # # Cleansing a broker file for a division
#
# # %%
# import qbecat as qc
# from qbecat.cleansing import load_division, rules_frame, run_cleansing
# from qbecat.simulation import synthetic_broker_file
#
# print(rules_frame())                         # every rule, its severity and whether it can autofix
# config = load_division("EO")                 # base.yaml + EO overrides
#
# # a real run: run_cleansing("path/to/broker.xlsx", "EO", out_dir="out")
# state, pipe = run_cleansing(synthetic_broker_file(), config, out_dir="out", stem="demo")
#
# # %%
# print(state.blocked)                          # tables not exported and why
# print(state.open_findings().groupby(["rule", "severity"]).size())
# print(state.mapping["locations"]["columns"])  # which broker header became which field
#
# # %% One broker row (Excel row number) through every stage, with its findings
# row = int(state.open_findings()["_row"].dropna().iloc[0])
# print(pipe.follow(_row=row, changes_only=True))
# @@FILE examples/05_marginal_impact_production.py 1108d88b523bfc8792d343932c36f4966e3f22c6c3e399fa90a6f3a634f65c15
# # %% [markdown]
# # # Marginal impact on real data
# # The mi_v3 notebook as a short script on top of the library.
# # Needs settings.yaml with the three engine aliases and table names filled in
# # (see config/settings.example.yaml). Fill in the run identifiers below.
#
# # %%
# import qbecat as qc
# from qbecat import io
# from qbecat.marginal import MarginalSettings, compare_to_reference, run_marginal_impact
#
# qc.configure_logging(logfile="marginal_impact.log")
# qc.load_settings("settings.yaml")
#
# RUN = dict(
#     analysis_id=None,            # RDM analysis id (account ELTs)
#     persp_code="RL",
#     load_factor=None,            # applied to mean and SDs, not exposure
#     port_grouping_id=None,       # group portfolio
#     hazard_grouping_id=None,
#     yeqt_id=None,
#     vendor_version_id=None,
#     hazard_zone_id=None,
# )
# assert None not in RUN.values(), "fill in RUN first"
#
# # %% Load (each loader validates and fails with row numbers if the extract is bad)
# n_years      = io.load_n_years(RUN["yeqt_id"])
# occurrences  = io.load_occurrences(RUN["yeqt_id"], RUN["vendor_version_id"], RUN["hazard_zone_id"])
# group_elt    = io.load_group_elt(RUN["port_grouping_id"], RUN["hazard_grouping_id"])
# account_elts = io.load_account_elts(RUN["analysis_id"], RUN["persp_code"], RUN["load_factor"])
# reference    = io.load_reference_marginals(RUN["analysis_id"])
#
# # A query looks wrong? Get the exact text to paste into SSMS:
# # print(io.show_sql("account_elts", analysis_id=RUN["analysis_id"], persp_code=RUN["persp_code"]))
#
# # %% Run
# summary, pipe = run_marginal_impact(group_elt, account_elts, occurrences, n_years,
#                                     reference=reference, settings=MarginalSettings(return_period=200))
# print(pipe.trace[["step", "seconds", "rows_out"]])
# print(pipe.outputs["allocations"].totals)
# print(compare_to_reference(summary))
#
# # %% Save
# summary.to_excel("MarginalImpact.xlsx", index=False)
# @@FILE pyproject.toml e89d54cff8fb649275bb396414fdbc590a0169140b1c13f7a311032c66613572
# [build-system]
# requires = ["setuptools>=68"]
# build-backend = "setuptools.build_meta"
#
# [project]
# name = "qbecat"
# version = "0.1.0"          # the ONLY place the version is set; bump it for every release
# description = "Cat modelling team library: simulation from YEQT, EP curves, exposed limit, marginal impact, exposure cleansing"
# readme = "README.md"
# requires-python = ">=3.10"
# dependencies = [
#     "numpy>=1.24",
#     "scipy>=1.10",
#     "pandas>=2.0",
#     "pyyaml>=6.0",
#     "openpyxl>=3.1",
# ]
#
# [project.optional-dependencies]
# sql = ["sqlalchemy>=2.0", "pyodbc>=5.0"]
# parquet = ["pyarrow>=14"]
# dev = ["pytest>=7", "build>=1.0"]
# full = ["sqlalchemy>=2.0", "pyodbc>=5.0", "pyarrow>=14", "pytest>=7", "matplotlib>=3.7"]
#
# [tool.setuptools.packages.find]
# where = ["src"]
# include = ["qbecat*"]
#
# [tool.setuptools.package-data]
# qbecat = ["io/queries/*.sql", "cleansing/divisions/*.yaml"]
#
# [tool.pytest.ini_options]
# testpaths = ["tests"]
# @@FILE src/qbecat/__init__.py b1f9100e9ccebdfe325df18f0c57af8aa97837eb24adea70f9656c56f3c594f5
# """
# qbecat - the cat modelling team's shared Python library.
#
# Modules (dependencies only point downwards in this list):
#     config, log, trace, schema, utils   foundations
#     io                                  databases and files (the only place with connections)
#     simulation                          ELT + YEQT -> occurrence losses -> year losses
#     financial                           deductibles, limits, layers, exposed limit
#     ep                                  OEP / AEP / TVaR / AAL, closed-form OEP
#     marginal                            account marginal impact on the group
#     cleansing                           divisional exposure cleansing
#
# Typical use:
#     import qbecat as qc
#     qc.configure_logging()
#     occ = qc.io.load_occurrences(yeqt_id=..., vendor_version_id=..., hazard_zone_id=...)
# """
#
# from importlib.metadata import PackageNotFoundError, version as _version
#
# try:
#     __version__ = _version("qbecat")      # set in pyproject.toml only
# except PackageNotFoundError:             # running from a source folder without installing
#     __version__ = "0.0.0+local"
#
# from . import cleansing, ep, financial, io, marginal, schema, simulation, utils
# from .config import load_settings, setting, use_settings
# from .log import configure_logging
# from .trace import Pipeline, StepCheckError, StepError, step
#
# __all__ = ["cleansing", "ep", "financial", "io", "marginal", "schema", "simulation", "utils",
#            "load_settings", "setting", "use_settings", "configure_logging", "Pipeline",
#            "StepCheckError", "StepError", "step", "__version__"]
# @@FILE src/qbecat/cleansing/__init__.py 78feed9bd2f7b62bbcbd9674174e6aa12e39475e2de1e4f51042ddf2bd418054
# """
# Divisional exposure cleansing: flag-don't-fix rules, gated autofix,
# per-table export blocking, full audit trail. Division differences live in
# config/divisions/*.yaml, not in code.
# """
#
# from .rules import RULES, Rule, rule, rules_frame
# from .run import cleansing_pipeline, load_division, run_cleansing
# from .stages import (CleansingState, apply_fixes, evaluate, export, ingest, map_columns, normalise,
#                      write_outputs)
#
# __all__ = ["RULES", "Rule", "rule", "rules_frame", "cleansing_pipeline", "load_division",
#            "run_cleansing", "CleansingState", "apply_fixes", "evaluate", "export", "ingest",
#            "map_columns", "normalise", "write_outputs"]
# @@FILE src/qbecat/cleansing/divisions/EO.yaml 1b0f427029760b73985ae88ef593080d4d9f10ae7d81f0ab16ac72e381956436
# extends: base.yaml
# division: EO
#
# thresholds:
#   tiv_max: 1.5e+9            # TODO confirm with EO guidelines
#   latitude_range: [-48, -9]  # AU/NZ bounding box (TODO confirm cut-off text)
#   longitude_range: [112, 179]
#
# severity_overrides:
#   year_built_range: WARNING
# @@FILE src/qbecat/cleansing/divisions/INT.yaml 016d70d6334c48d93172ebb165a5cfd5a548168d5a313a229fcb89e31b8b9fa6
# extends: base.yaml
# division: INT
#
# # TODO: divisional guidelines for INT are not built yet. Until they are,
# # this division uses the base rules and thresholds unchanged.
# @@FILE src/qbecat/cleansing/divisions/MARINE.yaml b6491570a0335aae479612bf7fb7b7f7aa319893c073be60f5c1f5b670ae2ad3
# extends: base.yaml
# division: MARINE
#
# # TODO: divisional guidelines for MARINE are not built yet. Until they are,
# # this division uses the base rules and thresholds unchanged.
# @@FILE src/qbecat/cleansing/divisions/NA.yaml f11e8b20e0d4bf62a23ebe1c7fbdabbd95f0b9bb23109212704c73298755cfd1
# extends: base.yaml
# division: NA
#
# # TODO: divisional guidelines for NA are not built yet. Until they are,
# # this division uses the base rules and thresholds unchanged.
# @@FILE src/qbecat/cleansing/divisions/base.yaml 4c5ad250a0157c482661275f9727cf9e3563d1bf9d6f1494510664479f7a563e
# # Shared cleansing settings. Each division file starts with `extends: base.yaml`
# # and overrides only what differs. Values marked TODO are placeholders that
# # need confirming against the division guidelines.
#
# tables:
#   locations:
#     sheet_names: [Locations, Location, SOV, Schedule, "Schedule of Values", Sheet1]
#     # canonical column: [broker header spellings]. Matching ignores case, spaces and punctuation.
#     columns:
#       location_id:  [loc no, loc number, location number, location id, loc id, locnum, site id]
#       address:      [street address, address, address line 1, street]
#       city:         [city, suburb, town]
#       postcode:     [postcode, post code, zip, postal code]
#       country:      [country, country code, cntry]
#       latitude:     [lat, latitude]
#       longitude:    [long, lon, lng, longitude]
#       tiv:          [total insured value, tiv, sum insured, total sum insured, tsi]
#       year_built:   [year built, yearbuilt, year of construction, built]
#       construction: [construction, construction type, constr, construction class]
#       stories:      [no. of storeys, no of storeys, storeys, stories, number of stories, floors]
#     required: [location_id, country, tiv]
#     numeric:  [latitude, longitude, tiv, year_built, stories]
#
# thresholds:
#   tiv_max: 2.0e+9            # TODO confirm per division
#   latitude_range: [-90, 90]
#   longitude_range: [-180, 180]
#   year_built_min: 1800
#   year_built_max: 2026
#   stories_max: 150
#
# reference:
#   countries: [AU, NZ]
#   country_aliases: {AUS: AU, AUSTRALIA: AU, NZL: NZ, "NEW ZEALAND": NZ}
#   construction_codes: [Masonry, Timber, Steel, Concrete, "Reinforced Concrete", Unknown]
#
# rules: all                  # or a list of rule names
# rules_disabled: []
# severity_overrides: {}      # rule name -> INFO | WARNING | ERROR | CRITICAL
#
# # Gate 2 of autofix: a proposed fix is applied only if the rule declares
# # autofix=True AND is listed here.
# autofix_allowlist: [country_code, construction_code]
#
# # Filled in on the export copy only (never seen by validation).
# sentinels:
#   year_built: 0
#   stories: 0
#   construction: Unknown
#
# export:
#   locations:
#     sheet: Locations
#     # canonical column -> RMS template header  (TODO: align with the current RMS template)
#     columns:
#       location_id:  LOCNUM
#       address:      STREETNAME
#       city:         CITY
#       postcode:     POSTALCODE
#       country:      CNTRYCODE
#       latitude:     LATITUDE
#       longitude:    LONGITUDE
#       tiv:          TIV
#       year_built:   YEARBUILT
#       construction: CONSTRUCTION
#       stories:      NUMSTORIES
# @@FILE src/qbecat/cleansing/rules.py b7f49ddd2e34f1d8093fcf1b3045f015d426c4e85800e41720d988eddb062c0c
# """
# Cleansing rules: small functions that FLAG problems and never change data.
#
# A rule receives a copy of one table and the division config, and returns
# either
#     mask                      True where a row has the problem, or
#     (mask, proposed_values)   for rules that can suggest a fix
# It has no way to write to the data. A proposed fix is applied later by the
# apply stage only if BOTH gates are open:
#     1. the rule is declared autofix=True here, and
#     2. the rule is listed in the division's autofix_allowlist.
#
# Adding a rule = writing one function with @rule(...). Test it on a tiny
# DataFrame: rules are plain functions, so no pipeline is needed to debug one.
# """
#
# from __future__ import annotations
#
# from dataclasses import dataclass
# from typing import Callable
#
# import numpy as np
# import pandas as pd
#
# SEVERITIES = ["INFO", "WARNING", "ERROR", "CRITICAL"]   # CRITICAL blocks that table's export
#
#
# @dataclass(frozen=True)
# class Rule:
#     name: str
#     func: Callable
#     table: str
#     column: str
#     severity: str
#     autofix: bool
#     description: str
#
#
# RULES: dict[str, Rule] = {}
#
#
# def rule(name: str, *, table: str, column: str, severity: str = "ERROR",
#          autofix: bool = False, description: str = ""):
#     """Register a rule. column = the column findings refer to (must exist for the rule to run)."""
#     if severity not in SEVERITIES:
#         raise ValueError(f"severity must be one of {SEVERITIES}")
#
#     def register(func):
#         if name in RULES:
#             raise ValueError(f"rule '{name}' registered twice")
#         RULES[name] = Rule(name, func, table, column, severity, autofix,
#                            description or (func.__doc__ or "").strip().split("\n")[0])
#         return func
#     return register
#
#
# def rules_frame() -> pd.DataFrame:
#     """All registered rules (a readable catalogue for reviewers)."""
#     return pd.DataFrame([{k: v for k, v in r.__dict__.items() if k != "func"} for r in RULES.values()])
#
#
# def _threshold(cfg, key):
#     try:
#         return cfg["thresholds"][key]
#     except KeyError:
#         raise KeyError(f"threshold '{key}' missing from division config 'thresholds:'") from None
#
#
# def _norm(s: pd.Series) -> pd.Series:
#     return s.astype("string").str.strip().str.upper()
#
#
# # ======================================================================
# # built-in rules (generic; division-specific ones go in their own module)
# # ======================================================================
# @rule("duplicate_location_id", table="locations", column="location_id", severity="CRITICAL")
# def duplicate_location_id(df, cfg):
#     """Location id appears more than once (RMS import would reject the file)."""
#     return df["location_id"].duplicated(keep=False) & df["location_id"].notna()
#
#
# @rule("missing_location_id", table="locations", column="location_id", severity="CRITICAL")
# def missing_location_id(df, cfg):
#     """Location id is blank."""
#     return df["location_id"].isna()
#
#
# @rule("tiv_missing", table="locations", column="tiv", severity="CRITICAL")
# def tiv_missing(df, cfg):
#     """TIV missing, zero or negative."""
#     return df["tiv"].isna() | (df["tiv"] <= 0)
#
#
# @rule("tiv_outlier", table="locations", column="tiv", severity="WARNING")
# def tiv_outlier(df, cfg):
#     """TIV above the division's maximum single-location value."""
#     return df["tiv"] > _threshold(cfg, "tiv_max")
#
#
# @rule("latitude_range", table="locations", column="latitude", severity="ERROR")
# def latitude_range(df, cfg):
#     """Latitude outside the allowed range."""
#     lo, hi = _threshold(cfg, "latitude_range")
#     return df["latitude"].notna() & ~df["latitude"].between(lo, hi)
#
#
# @rule("longitude_range", table="locations", column="longitude", severity="ERROR")
# def longitude_range(df, cfg):
#     """Longitude outside the allowed range."""
#     lo, hi = _threshold(cfg, "longitude_range")
#     return df["longitude"].notna() & ~df["longitude"].between(lo, hi)
#
#
# @rule("lat_long_zero", table="locations", column="latitude", severity="WARNING")
# def lat_long_zero(df, cfg):
#     """Latitude and longitude both zero (usually a failed geocode)."""
#     if "longitude" not in df:
#         return pd.Series(False, index=df.index)
#     return (df["latitude"] == 0) & (df["longitude"] == 0)
#
#
# @rule("year_built_range", table="locations", column="year_built", severity="WARNING")
# def year_built_range(df, cfg):
#     """Year built outside the plausible range."""
#     return df["year_built"].notna() & ~df["year_built"].between(
#         _threshold(cfg, "year_built_min"), _threshold(cfg, "year_built_max"))
#
#
# @rule("stories_range", table="locations", column="stories", severity="WARNING")
# def stories_range(df, cfg):
#     """Number of storeys not between 1 and the maximum."""
#     return df["stories"].notna() & ~df["stories"].between(1, _threshold(cfg, "stories_max"))
#
#
# @rule("country_code", table="locations", column="country", severity="ERROR", autofix=True)
# def country_code(df, cfg):
#     """Country not a valid code; proposes the code when a known alias matches."""
#     allowed = set(cfg["reference"]["countries"])
#     aliases = {k.upper(): v for k, v in cfg["reference"].get("country_aliases", {}).items()}
#     cleaned = _norm(df["country"])
#     proposed = cleaned.map(lambda v: v if v in allowed else aliases.get(v, pd.NA) if pd.notna(v) else pd.NA)
#     bad = ~df["country"].isin(allowed)
#     return bad, proposed
#
#
# @rule("construction_code", table="locations", column="construction", severity="ERROR", autofix=True)
# def construction_code(df, cfg):
#     """Construction not in the division's code list; proposes the code when only case/spacing differ."""
#     codes = list(cfg["reference"]["construction_codes"])
#     by_upper = {c.upper(): c for c in codes}
#     proposed = _norm(df["construction"]).map(lambda v: by_upper.get(v, pd.NA) if pd.notna(v) else pd.NA)
#     bad = df["construction"].notna() & ~df["construction"].isin(codes)
#     return bad, proposed
# @@FILE src/qbecat/cleansing/run.py 5afd51524ec180dbbc5056b0b6447428f7a06c594013433e10e8b69b2286f4ea
# """
# Run the cleansing for one broker file and one division.
#
#     state, pipe = run_cleansing("broker.xlsx", "EO", out_dir="out")
#     state.open_findings()          # what still needs a person
#     state.blocked                  # tables not exported, and why
#     pipe.follow(_row=57)           # one broker row through every stage, with its findings
# """
#
# from __future__ import annotations
#
# from pathlib import Path
#
# from ..config import read_yaml
# from ..trace import Pipeline, step
# from . import stages
#
# DIVISIONS_DIR = Path(__file__).resolve().parent / "divisions"
#
#
# def load_division(division: str, directory=None) -> dict:
#     """Division config (EO, NA, INT, MARINE, ...) merged over base.yaml via 'extends'."""
#     path = Path(directory or DIVISIONS_DIR) / f"{division.upper()}.yaml"
#     if not path.exists():
#         available = sorted(p.stem for p in Path(directory or DIVISIONS_DIR).glob("*.yaml"))
#         raise FileNotFoundError(f"no division config {path.name}; available: {available}")
#     cfg = read_yaml(path)
#     cfg.setdefault("division", division.upper())
#     return cfg
#
#
# def cleansing_pipeline() -> Pipeline:
#     return Pipeline("cleansing", [
#         step(stages.ingest),
#         step(stages.map_columns, use={"state": "ingest"}),
#         step(stages.normalise, use={"state": "map_columns"}),
#         step(stages.evaluate, use={"state": "normalise"}),
#         step(stages.apply_fixes, use={"state": "evaluate"}),
#         step(stages.export, use={"state": "apply_fixes"}),
#     ])
#
#
# def run_cleansing(source, division: str | dict, out_dir=None, stem: str | None = None,
#                   divisions_dir=None):
#     """
#     source: broker file path or {sheet name: DataFrame}.
#     division: name of a division config, or an already-loaded config dict.
#     Writes the four output files when out_dir is given. Returns (state, pipeline).
#     """
#     config = division if isinstance(division, dict) else load_division(division, divisions_dir)
#     pipe = cleansing_pipeline()
#     state = pipe.run(source=source, config=config)
#     if out_dir is not None:
#         stem = stem or (Path(source).stem if isinstance(source, (str, Path)) else "broker")
#         stages.write_outputs(state, out_dir, stem)
#     return state, pipe
# @@FILE src/qbecat/cleansing/stages.py d13c8e00feed5727c453bccd58ca0fba9198e4d6721c3baedd3aed433525bc43
# """
# Cleansing stages. Each stage is one function: (state, config) -> new state.
#
#     ingest -> map_columns -> normalise -> evaluate -> apply_fixes -> export
#
# Every working table keeps a `_row` column = the row number in the broker's
# Excel file, and every finding carries the same `_row`, so
# pipeline.follow(_row=57) shows one broker row and its findings through
# every stage.
# """
#
# from __future__ import annotations
#
# import json
# import logging
# import re
# import traceback
# from dataclasses import dataclass, field, replace
# from datetime import datetime, timezone
# from pathlib import Path
#
# import numpy as np
# import pandas as pd
#
# from ..io.files import read_sheets
# from .rules import RULES, SEVERITIES
#
# log = logging.getLogger(__name__)
#
# FINDING_COLUMNS = ["finding_id", "stage", "rule", "table", "_row", "column", "value",
#                    "proposed", "severity", "message", "autofix", "status"]
#
#
# @dataclass
# class CleansingState:
#     source: str = ""
#     raw: dict = field(default_factory=dict)        # sheet name -> frame, as received
#     tables: dict = field(default_factory=dict)     # canonical table -> working frame
#     findings: pd.DataFrame = field(default_factory=lambda: pd.DataFrame(columns=FINDING_COLUMNS))
#     mapping: dict = field(default_factory=dict)
#     audit: list = field(default_factory=list)
#     exports: dict = field(default_factory=dict)    # template sheet -> frame ready for RMS
#     blocked: dict = field(default_factory=dict)    # table -> reason
#
#     def open_findings(self) -> pd.DataFrame:
#         return self.findings[self.findings["status"] == "open"]
#
#
# def _now():
#     return datetime.now(timezone.utc).isoformat(timespec="seconds")
#
#
# def _event(stage, action, **details):
#     return {"time": _now(), "stage": stage, "action": action, **details}
#
#
# def _key(text) -> str:
#     """Header/sheet normaliser: 'No. of Storeys ' -> 'noofstoreys'."""
#     return re.sub(r"[^a-z0-9]", "", str(text).lower())
#
#
# def _findings(rows: list[dict], start: int) -> pd.DataFrame:
#     df = pd.DataFrame(rows, columns=FINDING_COLUMNS)
#     df["finding_id"] = np.arange(start, start + len(df))
#     return df
#
#
# def _add(state: CleansingState, rows: list[dict]) -> pd.DataFrame:
#     if not rows:
#         return state.findings
#     new = _findings(rows, len(state.findings) + 1)
#     return new if state.findings.empty else pd.concat([state.findings, new], ignore_index=True)
#
#
# # ------------------------------------------------------------------ stages
# def ingest(source, config: dict) -> CleansingState:
#     """Read every sheet of the broker file (path or {sheet: DataFrame})."""
#     raw = read_sheets(source) if isinstance(source, (str, Path)) else {k: v.copy() for k, v in source.items()}
#     for df in raw.values():
#         df.columns = [str(c).strip() for c in df.columns]
#     name = str(source) if isinstance(source, (str, Path)) else "<in-memory>"
#     audit = [_event("ingest", "read", source=name, division=config.get("division"),
#                     sheets={k: len(v) for k, v in raw.items()})]
#     return CleansingState(source=name, raw=raw, audit=audit)
#
#
# def map_columns(state: CleansingState, config: dict) -> CleansingState:
#     """Match sheets and broker headers to canonical tables/columns using the config synonyms."""
#     tables, mapping, rows, audit = {}, {}, [], list(state.audit)
#     for table, spec in config["tables"].items():
#         wanted = {_key(s) for s in spec.get("sheet_names", [table])}
#         sheet = next((s for s in state.raw if _key(s) in wanted), None)
#         if sheet is None and len(state.raw) == 1 and len(config["tables"]) == 1:
#             sheet = next(iter(state.raw))
#         if sheet is None:
#             rows.append(dict(stage="map", rule="sheet_not_found", table=table, severity="CRITICAL",
#                              message=f"no sheet matching {spec.get('sheet_names')}; sheets: {list(state.raw)}",
#                              autofix=False, status="open"))
#             continue
#         raw = state.raw[sheet]
#         headers = {_key(h): h for h in raw.columns}
#         rename = {}
#         for canonical, synonyms in spec["columns"].items():
#             hit = next((headers[_key(s)] for s in [canonical, *synonyms] if _key(s) in headers), None)
#             if hit is not None and hit not in rename:
#                 rename[hit] = canonical
#         missing = [c for c in spec.get("required", []) if c not in rename.values()]
#         for col in missing:
#             rows.append(dict(stage="map", rule="required_column_missing", table=table, column=col,
#                              severity="CRITICAL", message=f"no broker column maps to '{col}'",
#                              autofix=False, status="open"))
#         unmapped = [h for h in raw.columns if h not in rename]
#         for h in unmapped:
#             rows.append(dict(stage="map", rule="unmapped_column", table=table, column=h,
#                              severity="INFO", message="broker column not used", autofix=False,
#                              status="open"))
#         df = raw[list(rename)].rename(columns=rename)
#         df.insert(0, "_row", raw.index.to_numpy() + 2)            # Excel row (header is row 1)
#         tables[table] = df.reset_index(drop=True)
#         mapping[table] = {"sheet": sheet, "columns": {v: k for k, v in rename.items()},
#                           "missing_required": missing, "unmapped": unmapped}
#         audit.append(_event("map", "mapped", table=table, sheet=sheet, rows=len(df),
#                             mapped=len(rename), missing_required=missing))
#     return replace(state, tables=tables, mapping=mapping, audit=audit, findings=_add(state, rows))
#
#
# def normalise(state: CleansingState, config: dict) -> CleansingState:
#     """Parse numeric columns (thousand separators allowed). Unparseable values are flagged, keeping the raw text."""
#     tables, rows, audit = {}, [], list(state.audit)
#     for table, df in state.tables.items():
#         df = df.copy()
#         for col in config["tables"][table].get("numeric", []):
#             if col not in df:
#                 continue
#             raw = df[col]
#             text = raw.astype("string").str.replace(",", "", regex=False).str.strip()
#             parsed = pd.to_numeric(text, errors="coerce")
#             bad = raw.notna() & (text != "") & parsed.isna()
#             for i in np.flatnonzero(bad.to_numpy()):
#                 rows.append(dict(stage="normalise", rule="not_numeric", table=table,
#                                  _row=int(df["_row"].iat[i]), column=col, value=str(raw.iat[i]),
#                                  severity="ERROR", message=f"'{raw.iat[i]}' is not a number",
#                                  autofix=False, status="open"))
#             df[col] = parsed.astype(float)
#             audit.append(_event("normalise", "parsed_numeric", table=table, column=col,
#                                 unparseable=int(bad.sum())))
#         tables[table] = df
#     return replace(state, tables=tables, audit=audit, findings=_add(state, rows))
#
#
# def enabled_rules(config: dict) -> list:
#     chosen = config.get("rules", "all")
#     names = list(RULES) if chosen == "all" else list(chosen)
#     unknown = [n for n in names if n not in RULES]
#     if unknown:
#         raise KeyError(f"config lists unknown rules {unknown}; registered: {sorted(RULES)}")
#     return [RULES[n] for n in names if n not in set(config.get("rules_disabled", []))]
#
#
# def evaluate(state: CleansingState, config: dict) -> CleansingState:
#     """Run every enabled rule. Rules see a copy and only report; a crashing rule becomes a CRITICAL finding."""
#     rows, audit = [], list(state.audit)
#     overrides = config.get("severity_overrides", {})
#     for r in enabled_rules(config):
#         df = state.tables.get(r.table)
#         if df is None:
#             continue
#         if r.column not in df:
#             audit.append(_event("evaluate", "skipped", rule=r.name, reason=f"no column '{r.column}'"))
#             continue
#         severity = overrides.get(r.name, r.severity)
#         try:
#             out = r.func(df.copy(deep=True), config)
#             mask, proposed = out if isinstance(out, tuple) else (out, None)
#             mask = pd.Series(mask, index=df.index).fillna(False).astype(bool)
#         except Exception as exc:
#             rows.append(dict(stage="evaluate", rule=r.name, table=r.table, column=r.column,
#                              severity="CRITICAL", autofix=False, status="open",
#                              message=f"rule crashed: {type(exc).__name__}: {exc}"))
#             audit.append(_event("evaluate", "rule_crashed", rule=r.name,
#                                 error=traceback.format_exc(limit=3)))
#             continue
#         for i in np.flatnonzero(mask.to_numpy()):
#             p = None if proposed is None else proposed.iat[i]
#             rows.append(dict(stage="evaluate", rule=r.name, table=r.table,
#                              _row=int(df["_row"].iat[i]), column=r.column,
#                              value=None if pd.isna(df[r.column].iat[i]) else df[r.column].iat[i],
#                              proposed=None if p is None or pd.isna(p) else p,
#                              severity=severity, message=r.description,
#                              autofix=r.autofix, status="open"))
#         audit.append(_event("evaluate", "ran", rule=r.name, flagged=int(mask.sum()), severity=severity))
#     return replace(state, audit=audit, findings=_add(state, rows))
#
#
# def apply_fixes(state: CleansingState, config: dict) -> CleansingState:
#     """
#     Apply proposed values ONLY where the rule declared autofix AND the division
#     allowlists it. Every change is logged with old and new value.
#     """
#     allow = set(config.get("autofix_allowlist", []))
#     f = state.findings.copy()
#     gate = (f["autofix"] == True) & f["rule"].isin(allow) & f["proposed"].notna() & (f["status"] == "open")  # noqa: E712
#     tables = {k: v.copy() for k, v in state.tables.items()}
#     audit = list(state.audit)
#     for idx in f.index[gate]:
#         x = f.loc[idx]
#         df = tables[x["table"]]
#         pos = df.index[df["_row"] == x["_row"]]
#         old = df.loc[pos, x["column"]].iloc[0]
#         df.loc[pos, x["column"]] = x["proposed"]
#         f.loc[idx, "status"] = "fixed"
#         audit.append(_event("apply", "autofix", rule=x["rule"], table=x["table"], _row=int(x["_row"]),
#                             column=x["column"], old=None if pd.isna(old) else str(old),
#                             new=str(x["proposed"])))
#     not_allowed = (f["autofix"] == True) & ~f["rule"].isin(allow) & (f["status"] == "open")  # noqa: E712
#     audit.append(_event("apply", "summary", fixed=int(gate.sum()),
#                         fixable_but_not_allowlisted=int(not_allowed.sum())))
#     return replace(state, tables=tables, findings=f, audit=audit)
#
#
# def export(state: CleansingState, config: dict) -> CleansingState:
#     """
#     Build the RMS template tables. A table with any open CRITICAL finding is
#     blocked (other tables still export). Sentinels for missing values are
#     applied here, on the export copy only, so validation never saw them.
#     """
#     exports, blocked, audit = {}, {}, list(state.audit)
#     open_f = state.open_findings()
#     for table, df in state.tables.items():
#         critical = open_f[(open_f["table"] == table) & (open_f["severity"] == "CRITICAL")]
#         if len(critical):
#             blocked[table] = f"{len(critical)} open CRITICAL findings ({', '.join(sorted(set(critical['rule'])))})"
#             audit.append(_event("export", "blocked", table=table, reason=blocked[table]))
#             continue
#         spec = config.get("export", {}).get(table, {})
#         out = df.copy()
#         for col, value in config.get("sentinels", {}).items():
#             if col in out:
#                 n = int(out[col].isna().sum())
#                 out[col] = out[col].fillna(value)
#                 if n:
#                     audit.append(_event("export", "sentinel", table=table, column=col, value=value, rows=n))
#         columns = spec.get("columns", {c: c for c in out.columns if c != "_row"})
#         present = {c: h for c, h in columns.items() if c in out}
#         sheet = spec.get("sheet", table)
#         exports[sheet] = out[list(present)].rename(columns=present)
#         audit.append(_event("export", "exported", table=table, sheet=sheet, rows=len(out)))
#     for table in config["tables"]:
#         if table not in state.tables:
#             blocked.setdefault(table, "table not found in broker file")
#     return replace(state, exports=exports, blocked=blocked, audit=audit)
#
#
# # ------------------------------------------------------------------ outputs
# def write_outputs(state: CleansingState, out_dir, stem: str) -> dict:
#     """_exceptions.xlsx, _audit.jsonl, _mapping.json and _rms.xlsx (if anything exported)."""
#     out_dir = Path(out_dir)
#     out_dir.mkdir(parents=True, exist_ok=True)
#     f = state.findings
#     severity_rank = {s: i for i, s in enumerate(SEVERITIES)}
#     summary = (f.groupby(["table", "rule", "severity", "status"], dropna=False).size()
#                .rename("count").reset_index()
#                .sort_values(["severity", "count"], key=lambda s: s.map(severity_rank) if s.name == "severity" else s,
#                             ascending=False))
#     status = pd.DataFrame([{"table": t, "exported": t not in state.blocked,
#                             "reason": state.blocked.get(t, "")} for t in
#                            sorted(set(state.tables) | set(state.blocked))])
#     paths = {"exceptions": out_dir / f"{stem}_exceptions.xlsx",
#              "audit": out_dir / f"{stem}_audit.jsonl",
#              "mapping": out_dir / f"{stem}_mapping.json"}
#     with pd.ExcelWriter(paths["exceptions"]) as xl:
#         status.to_excel(xl, sheet_name="export_status", index=False)
#         summary.to_excel(xl, sheet_name="summary", index=False)
#         f[f["status"] == "open"].to_excel(xl, sheet_name="open", index=False)
#         f[f["status"] == "fixed"].to_excel(xl, sheet_name="fixed", index=False)
#     with open(paths["audit"], "w", encoding="utf-8") as fh:
#         for e in state.audit:
#             fh.write(json.dumps(e, default=str) + "\n")
#     paths["mapping"].write_text(json.dumps(state.mapping, indent=2, default=str), encoding="utf-8")
#     if state.exports:
#         paths["rms"] = out_dir / f"{stem}_rms.xlsx"
#         with pd.ExcelWriter(paths["rms"]) as xl:
#             for sheet, df in state.exports.items():
#                 df.to_excel(xl, sheet_name=sheet[:31], index=False)
#     log.info("cleansing outputs written to %s", out_dir)
#     return paths
# @@FILE src/qbecat/config.py 224b2040fa983a407aa4c61780ba7b433e99337bf4ec97bb58282859118e3efd
# """
# Settings from a YAML file: database engine aliases and table names.
#
# Real server, database and table names live ONLY in your local settings file,
# never in code. Code refers to engines by alias ("RMS", "QBE_MAIN",
# "QBE_SANDBOX") and to tables by key ("group_elt", "yeqt", ...).
#
# Where the settings file is found (first hit wins):
#   1. the path passed to load_settings(path)
#   2. the QBECAT_CONFIG environment variable
#   3. ./settings.yaml in the working directory
# Start from config/settings.example.yaml.
# """
#
# from __future__ import annotations
#
# import copy
# import os
# from pathlib import Path
#
# import yaml
#
# ENV_VAR = "QBECAT_CONFIG"
# _cache: dict | None = None
#
#
# class ConfigError(RuntimeError):
#     pass
#
#
# def deep_merge(base: dict, override: dict) -> dict:
#     """Recursively merge override into a copy of base (override wins)."""
#     out = copy.deepcopy(base)
#     for k, v in (override or {}).items():
#         if isinstance(v, dict) and isinstance(out.get(k), dict):
#             out[k] = deep_merge(out[k], v)
#         else:
#             out[k] = copy.deepcopy(v)
#     return out
#
#
# def read_yaml(path) -> dict:
#     """Read a YAML file; supports 'extends: other.yaml' (relative to this file)."""
#     path = Path(path)
#     if not path.exists():
#         raise ConfigError(f"config file not found: {path}")
#     data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
#     parent = data.pop("extends", None)
#     if parent:
#         data = deep_merge(read_yaml(path.parent / parent), data)
#     return data
#
#
# def load_settings(path=None, *, reload: bool = False) -> dict:
#     """Load (and cache) the settings dict."""
#     global _cache
#     if _cache is not None and path is None and not reload:
#         return _cache
#     candidates = [path, os.environ.get(ENV_VAR), "settings.yaml"]
#     for c in candidates:
#         if c and Path(c).exists():
#             _cache = read_yaml(c)
#             _cache["_source"] = str(Path(c).resolve())
#             return _cache
#     raise ConfigError(
#         "no settings file found. Copy config/settings.example.yaml to settings.yaml "
#         f"(or set {ENV_VAR}=<path>) and fill in the placeholders.")
#
#
# def use_settings(settings: dict):
#     """Use an in-memory settings dict (tests, notebooks)."""
#     global _cache
#     _cache = settings
#
#
# def setting(key: str, settings: dict | None = None, default=KeyError):
#     """Dotted lookup, e.g. setting('tables.group_elt')."""
#     node = settings if settings is not None else load_settings()
#     for part in key.split("."):
#         if not isinstance(node, dict) or part not in node:
#             if default is KeyError:
#                 raise ConfigError(f"setting '{key}' is missing from {node.get('_source', 'settings') if isinstance(node, dict) else 'settings'}")
#             return default
#         node = node[part]
#     return node
# @@FILE src/qbecat/ep/__init__.py 5f9f219fcbf495494a4b9d8717b76ff9e32345aaacefb50df041ceef67213b88
# """EP curve engine: OEP / AEP / TVaR / AAL from year losses, plus closed-form OEP."""
#
# from .analytic import analytic_aal, analytic_loss_at_rp, analytic_oep
# from .curves import aal, ep_by, ep_table, exceedance_curve, loss_at_rp, sorted_year_values, tvar
#
# __all__ = ["analytic_aal", "analytic_loss_at_rp", "analytic_oep", "aal", "ep_by", "ep_table",
#            "exceedance_curve", "loss_at_rp", "sorted_year_values", "tvar"]
# @@FILE src/qbecat/ep/analytic.py e30da23954c16af543f3f96c0f04051d529f5f70595af764f127e40fadbf7b0f
# """
# Closed-form OEP from an ELT with rates (no simulation).
#
# Occurrences with loss above x form a thinned Poisson process with rate
# rho(x) = sum_i rate_i * P(L_i > x), so OEP(x) = 1 - exp(-rho(x)).
# Uses the same Beta parameters as the simulated path (simulation.severity),
# so analytic vs simulated differences are sampling noise only: a useful
# check on any new YEQT or ELT extract.
# """
#
# from __future__ import annotations
#
# import numpy as np
# import pandas as pd
# from scipy.optimize import brentq
# from scipy.stats import beta as beta_dist
#
# from ..simulation.severity import add_beta_parameters
#
#
# def _prepared(elt):
#     if "rate" not in elt.columns:
#         raise ValueError("analytic EP needs a 'rate' column (annual event rate)")
#     return elt if "alpha" in elt.columns else add_beta_parameters(elt)
#
#
# def analytic_oep(elt: pd.DataFrame, losses) -> np.ndarray:
#     """P(largest occurrence in a year > x) for each x in losses."""
#     e = _prepared(elt)
#     x = np.atleast_1d(np.asarray(losses, dtype=float))
#     rate = e["rate"].to_numpy(float)
#     expo = e["exposure"].to_numpy(float)
#     point = np.minimum(e["mean_loss"].to_numpy(float), expo)
#     live = ~e["degenerate"].to_numpy(bool)
#     a, b = e["alpha"].to_numpy(float), e["beta"].to_numpy(float)
#     out = np.empty(len(x))
#     for j, xj in enumerate(x):
#         sf = np.where(point > xj, 1.0, 0.0)
#         sf[live] = beta_dist.sf(xj / expo[live], a[live], b[live])
#         out[j] = 1 - np.exp(-np.sum(rate * sf))
#     return out
#
#
# def analytic_loss_at_rp(elt: pd.DataFrame, return_periods) -> np.ndarray:
#     """Loss x with OEP(x) = 1/RP (NaN if the RP is below the model's shortest RP)."""
#     e = _prepared(elt)
#     hi = float(e["exposure"].max())
#     out = []
#     for rp in np.atleast_1d(return_periods):
#         target = 1 / rp
#         if analytic_oep(e, [0.0])[0] < target:
#             out.append(np.nan)
#             continue
#         out.append(brentq(lambda x: analytic_oep(e, [x])[0] - target, 0.0, hi, xtol=1e-6 * hi))
#     return np.array(out)
#
#
# def analytic_aal(elt: pd.DataFrame) -> float:
#     """sum(rate x mean_loss)."""
#     return float((elt["rate"] * elt["mean_loss"]).sum())
# @@FILE src/qbecat/ep/curves.py c8c7e5e94dca7637d1efa0024dbf8103ea4ddadfb26082df68fd9b48a0ecbe34
# """
# Empirical EP curves from year losses.
#
# Conventions (shared by the whole library, including marginal impact):
#   * Year losses are given only for years with events; n_years is ALWAYS
#     passed explicitly and missing years count as zero loss. (Forgetting the
#     zero years is the most common silent EP bug.)
#   * Loss at return period T is read at rank k = round(n_years / T), rank 1
#     being the worst year (method="rank"). method="interpolate" interpolates
#     linearly between neighbouring ranks instead; at integer k it equals "rank".
#   * TVaR at T is the average of the worst k years.
# """
#
# from __future__ import annotations
#
# import numpy as np
# import pandas as pd
#
#
# def sorted_year_values(year_values, n_years: int) -> np.ndarray:
#     """All n_years annual values, worst first (event-free years filled with 0)."""
#     v = np.asarray(year_values, dtype=float)
#     if len(v) > n_years:
#         raise ValueError(f"{len(v):,} year values but n_years = {n_years:,}: "
#                          "duplicated years, or the wrong n_years?")
#     if np.any(~np.isfinite(v)) or np.any(v < 0):
#         raise ValueError("year values must be finite and non-negative")
#     full = np.zeros(n_years)
#     full[:len(v)] = v
#     return -np.sort(-full)
#
#
# def _ranks(n_years, return_periods):
#     rp = np.atleast_1d(np.asarray(return_periods, dtype=float))
#     if np.any(rp <= 0):
#         raise ValueError("return periods must be positive")
#     return n_years / rp
#
#
# def loss_at_rp(year_values, n_years: int, return_periods, method: str = "rank") -> np.ndarray:
#     """Loss at each return period (NaN where the RP is beyond the simulation)."""
#     v = sorted_year_values(year_values, n_years)
#     k = _ranks(n_years, return_periods)
#     if method == "rank":
#         idx = np.rint(k).astype(int)
#         out = np.where(idx >= 1, v[np.clip(idx, 1, n_years) - 1], np.nan)
#     elif method == "interpolate":
#         out = np.interp(k, np.arange(1, n_years + 1), v)
#         out = np.where(k >= 1, out, np.nan)
#     else:
#         raise ValueError("method must be 'rank' or 'interpolate'")
#     return out
#
#
# def tvar(year_values, n_years: int, return_periods) -> np.ndarray:
#     """Average of the worst round(n_years / RP) years."""
#     v = sorted_year_values(year_values, n_years)
#     csum = np.cumsum(v)
#     idx = np.rint(_ranks(n_years, return_periods)).astype(int)
#     return np.where(idx >= 1, csum[np.clip(idx, 1, n_years) - 1] / np.maximum(idx, 1), np.nan)
#
#
# def aal(year_values, n_years: int) -> float:
#     """Average annual loss over all simulated years."""
#     return float(np.sum(year_values) / n_years)
#
#
# def ep_table(ylt: pd.DataFrame, n_years: int, return_periods, method: str = "rank") -> pd.DataFrame:
#     """
#     OEP, AEP and their TVaRs at each return period, from year_losses() output
#     (columns oep, aep). AAL is in table.attrs["aal"].
#     """
#     rp = np.atleast_1d(np.asarray(return_periods, dtype=float))
#     out = pd.DataFrame({
#         "return_period": rp,
#         "prob": 1 / rp,
#         "oep": loss_at_rp(ylt["oep"], n_years, rp, method),
#         "aep": loss_at_rp(ylt["aep"], n_years, rp, method),
#         "tvar_oep": tvar(ylt["oep"], n_years, rp),
#         "tvar_aep": tvar(ylt["aep"], n_years, rp),
#     })
#     out.attrs["aal"] = aal(ylt["aep"], n_years)
#     out.attrs["n_years"] = n_years
#     return out
#
#
# def ep_by(ylt: pd.DataFrame, n_years: int, return_periods, by: str = "account_id",
#           basis: str = "oep", method: str = "rank") -> pd.DataFrame:
#     """One row per group (e.g. account), one column per return period, plus AAL."""
#     rows = {}
#     for key, g in ylt.groupby(by):
#         rows[key] = {**{f"rp_{rp:g}": x for rp, x in
#                         zip(np.atleast_1d(return_periods), loss_at_rp(g[basis], n_years, return_periods, method))},
#                      "aal": aal(g["aep"], n_years)}
#     return pd.DataFrame.from_dict(rows, orient="index").rename_axis(by).reset_index()
#
#
# def exceedance_curve(year_values, n_years: int) -> pd.DataFrame:
#     """Full empirical curve for plotting: rank, loss, exceedance_prob, return_period."""
#     v = sorted_year_values(year_values, n_years)
#     rank = np.arange(1, n_years + 1)
#     return pd.DataFrame({"rank": rank, "loss": v, "exceedance_prob": rank / n_years,
#                          "return_period": n_years / rank})
# @@FILE src/qbecat/financial/__init__.py 55f0423bf9ab6d2b5b5f27353fb85b72dda34c70580a9ea892eeef53303eedbf
# """Financial terms (deductibles, limits, layers, treaties) and exposed limit."""
#
# from .exposed_limit import explain_policy, exposed_limit, exposed_limit_pipeline
# from .terms import (aggregate_layer, apply_deductible, apply_limit, layer, occurrence_layer,
#                     quota_share)
#
# __all__ = ["explain_policy", "exposed_limit", "exposed_limit_pipeline", "aggregate_layer", "apply_deductible",
#            "apply_limit", "layer", "occurrence_layer", "quota_share"]
# @@FILE src/qbecat/financial/exposed_limit.py 1f227ce7ed19fc746670a97fbef1a681c5174e36108a7982506cf48d1bae2952
# """
# Exposed limit, as a sequence of small steps instead of one stored procedure.
#
# Each step adds ONE column, so after a run you can see the number at every
# stage for any location or policy:
#
#     summary, pipe = exposed_limit(exposure, group_by=["country", "peril_zone"])
#     pipe.trace                     # control totals of tiv / exposed_limit after every step
#     pipe.follow(policy_id=17)      # that policy's locations through every step
#     pipe.dump("exposed_limit_debug.xlsx")
#
# Default definition (CONFIRM AGAINST THE CURRENT STORED PROCEDURE):
#   1. tiv                  = building + contents + bi        (or the given tiv)
#   2. after_deductible     = max(tiv - deductible - deductible_pct x tiv, 0)
#   3. after_location_limit = min(after_deductible, location_limit)
#   4. policy_gross         = sum of after_location_limit over the policy's locations
#   5. policy_exposed       = share x min(max(policy_gross - attachment, 0), policy_limit)
#   6. exposed_limit        = policy_exposed allocated back to locations pro rata
#                             to after_location_limit (so it can be summed by zone)
#   7. summary              = sums by the grouping columns
# To change the definition, edit or replace one step function, or build your
# own list of steps with qbecat.trace.step: nothing else needs to change.
# """
#
# from __future__ import annotations
#
# import numpy as np
# import pandas as pd
#
# from ..schema import validate
# from ..trace import Pipeline, step
# from .terms import apply_deductible, apply_limit, layer
#
# COVERAGES = ("building", "contents", "bi")
#
#
# def _col(df, name, fill):
#     return df[name].astype(float).fillna(fill) if name in df.columns else pd.Series(fill, index=df.index)
#
#
# def check_exposure(exposure: pd.DataFrame) -> pd.DataFrame:
#     """Validate the exposure table (ids, numeric terms, unique locations)."""
#     return validate(exposure, "exposure", "exposed_limit input")
#
#
# def location_tiv(df: pd.DataFrame, coverages=COVERAGES) -> pd.DataFrame:
#     """tiv = sum of coverage values present (keeps a given tiv column if no coverages)."""
#     present = [c for c in coverages if c in df.columns]
#     if present:
#         return df.assign(tiv=df[present].astype(float).fillna(0).sum(axis=1))
#     if "tiv" not in df.columns:
#         raise ValueError(f"exposure needs 'tiv' or coverage columns {list(coverages)}")
#     return df.assign(tiv=df["tiv"].astype(float))
#
#
# def after_deductible(df: pd.DataFrame) -> pd.DataFrame:
#     """Location deductible (amount and/or % of TIV)."""
#     ded = _col(df, "deductible", 0.0) + _col(df, "deductible_pct", 0.0) * df["tiv"]
#     return df.assign(after_deductible=apply_deductible(df["tiv"], ded))
#
#
# def after_location_limit(df: pd.DataFrame) -> pd.DataFrame:
#     """Location limit (NaN = unlimited)."""
#     return df.assign(after_location_limit=apply_limit(df["after_deductible"],
#                                                       _col(df, "location_limit", np.nan)))
#
#
# def policy_gross(df: pd.DataFrame) -> pd.DataFrame:
#     """Sum of location values to policy level (repeated on each location row)."""
#     return df.assign(policy_gross=df.groupby("policy_id")["after_location_limit"].transform("sum"))
#
#
# def policy_exposed(df: pd.DataFrame) -> pd.DataFrame:
#     """Policy layer: share x min(max(gross - attachment, 0), policy limit)."""
#     return df.assign(policy_exposed=layer(df["policy_gross"], _col(df, "attachment", 0.0),
#                                           _col(df, "policy_limit", np.nan), _col(df, "share", 1.0)))
#
#
# def allocate_to_locations(df: pd.DataFrame) -> pd.DataFrame:
#     """exposed_limit per location, pro rata to after_location_limit."""
#     weight = np.divide(df["after_location_limit"], df["policy_gross"],
#                        out=np.zeros(len(df)), where=df["policy_gross"].to_numpy() > 0)
#     return df.assign(exposed_limit=df["policy_exposed"] * weight)
#
#
# def summarise(df: pd.DataFrame, group_by=("country",)) -> pd.DataFrame:
#     """Totals by grouping columns."""
#     group_by = list(group_by)
#     return (df.groupby(group_by, as_index=False)
#               .agg(n_locations=("location_id", "size"), n_policies=("policy_id", "nunique"),
#                    tiv=("tiv", "sum"), exposed_limit=("exposed_limit", "sum")))
#
#
# # ---------------------------------------------------------------- checks
# def _never_above_tiv(df):
#     bad = df["after_location_limit"] > df["tiv"] + 1e-6
#     return [f"{bad.sum()} locations have exposed value above TIV"] if bad.any() else []
#
#
# def _allocation_adds_up(df):
#     per_policy = df.groupby("policy_id").agg(alloc=("exposed_limit", "sum"), layer=("policy_exposed", "first"))
#     bad = ~np.isclose(per_policy["alloc"], per_policy["layer"], rtol=1e-9, atol=1e-6)
#     # a policy whose gross is zero allocates nothing, by design
#     bad &= per_policy["layer"] > 0
#     return [f"{bad.sum()} policies: allocated exposed limit != policy exposed "
#             f"(e.g. {per_policy.index[bad][:5].tolist()})"] if bad.any() else []
#
#
# def exposed_limit_pipeline(group_by=("country",)) -> Pipeline:
#     return Pipeline("exposed_limit", [
#         step(check_exposure),
#         step(location_tiv),
#         step(after_deductible),
#         step(after_location_limit, check=_never_above_tiv),
#         step(policy_gross),
#         step(policy_exposed),
#         step(allocate_to_locations, check=_allocation_adds_up),
#         step(summarise, group_by=list(group_by)),
#     ], watch=["tiv", "after_deductible", "after_location_limit", "exposed_limit"])
#
#
# CALCULATION_COLUMNS = ["location_id", "policy_id", "tiv", "deductible", "deductible_pct",
#                        "after_deductible", "location_limit", "after_location_limit", "policy_gross",
#                        "attachment", "policy_limit", "share", "policy_exposed", "exposed_limit"]
#
#
# def explain_policy(pipe: Pipeline, policy_id) -> pd.DataFrame:
#     """The full calculation for one policy, one row per location, inputs next to results."""
#     final = pipe.outputs.get("allocate_to_locations")
#     if final is None:
#         raise ValueError("run the pipeline at least as far as 'allocate_to_locations' first")
#     rows = final[final["policy_id"] == policy_id]
#     return rows[[c for c in CALCULATION_COLUMNS if c in rows.columns]].reset_index(drop=True)
#
#
# def exposed_limit(exposure: pd.DataFrame, group_by=("country",)):
#     """Run the exposed limit steps. Returns (summary, pipeline) - keep the pipeline for debugging."""
#     pipe = exposed_limit_pipeline(group_by)
#     summary = pipe.run(exposure)
#     return summary, pipe
# @@FILE src/qbecat/financial/terms.py fb5408406d91069fdb6266da2e41d00cab6f88a45fd87a37ff5eb53df1640ebb
# """
# Financial terms as small vectorised functions. A missing (NaN) limit means
# unlimited; a missing deductible or attachment means zero.
# """
#
# from __future__ import annotations
#
# import numpy as np
# import pandas as pd
#
#
# def _arr(x, fill):
#     a = np.asarray(x, dtype=float)
#     return np.where(np.isnan(a), fill, a)
#
#
# def apply_deductible(value, deductible):
#     """max(value - deductible, 0)."""
#     return np.maximum(np.asarray(value, dtype=float) - _arr(deductible, 0.0), 0.0)
#
#
# def apply_limit(value, limit):
#     """min(value, limit); NaN limit = unlimited."""
#     return np.minimum(np.asarray(value, dtype=float), _arr(limit, np.inf))
#
#
# def layer(value, attachment=0.0, limit=np.nan, share=1.0):
#     """share x min(max(value - attachment, 0), limit): the amount a layer pays."""
#     return _arr(share, 1.0) * apply_limit(apply_deductible(value, attachment), limit)
#
#
# def occurrence_layer(occ_losses: pd.DataFrame, attachment: float, limit: float,
#                      share: float = 1.0, name: str = "layer") -> pd.DataFrame:
#     """Add ceded_<name> and net columns to occurrence losses (per-occurrence terms)."""
#     ceded = layer(occ_losses["loss"], attachment, limit, share)
#     return occ_losses.assign(**{f"ceded_{name}": ceded, "net": occ_losses["loss"].to_numpy() - ceded})
#
#
# def quota_share(occ_losses: pd.DataFrame, cession: float, column: str = "loss",
#                 name: str = "qs") -> pd.DataFrame:
#     """Proportional cession of `column`."""
#     if not 0 <= cession <= 1:
#         raise ValueError("cession must be in [0, 1]")
#     ceded = cession * occ_losses[column].to_numpy(float)
#     return occ_losses.assign(**{f"ceded_{name}": ceded, "net": occ_losses[column].to_numpy() - ceded})
#
#
# def aggregate_layer(year_losses: pd.DataFrame, attachment: float, limit: float,
#                     column: str = "aep", name: str = "agg") -> pd.DataFrame:
#     """Annual aggregate cover (stop-loss style) on year losses."""
#     ceded = layer(year_losses[column], attachment, limit)
#     return year_losses.assign(**{f"ceded_{name}": ceded, f"net_{column}": year_losses[column].to_numpy() - ceded})
# @@FILE src/qbecat/io/__init__.py 71916635e3bd1581109a02b86c6effe8688a84b62c07c75210cc7edb36fe3071
# """Data in and out: the only place that knows about databases and files."""
#
# from .engines import get_engine
# from .files import read_frame, read_sheets, write_frame, write_sheets
# from .loaders import (apply_load_factor, load_account_elts, load_group_elt, load_n_years,
#                       load_occurrences, load_reference_marginals)
# from .sql import list_queries, query_text, run_query, show_sql
#
# __all__ = [
#     "get_engine", "read_frame", "read_sheets", "write_frame", "write_sheets",
#     "apply_load_factor", "load_account_elts", "load_group_elt", "load_n_years",
#     "load_occurrences", "load_reference_marginals",
#     "list_queries", "query_text", "run_query", "show_sql",
# ]
# @@FILE src/qbecat/io/engines.py b40251c46dd1c8758660742fb55cefef6dec5ba0ed85e5af44f5b9640b9862f6
# """
# Database engines by alias. Server and database names come from the settings
# file; code only ever says get_engine("RMS").
#
# settings.yaml:
#     engines:
#       RMS:         {server: "<RMS_SERVER>",         database: "<RMS_DATABASE>"}
#       QBE_MAIN:    {server: "<QBE_MAIN_SERVER>",    database: "<QBE_MAIN_DATABASE>"}
#       QBE_SANDBOX: {server: "<QBE_SANDBOX_SERVER>", database: "<QBE_SANDBOX_DATABASE>"}
#       TEST:        {url: "sqlite:///test.db"}       # a full URL also works
#     odbc_driver: "ODBC Driver 17 for SQL Server"
# """
#
# from __future__ import annotations
#
# import logging
#
# from ..config import ConfigError, load_settings
#
# log = logging.getLogger(__name__)
# _engines: dict = {}
#
#
# def engine_url(alias: str, settings: dict | None = None):
#     settings = settings or load_settings()
#     engines = settings.get("engines", {})
#     if alias not in engines:
#         raise ConfigError(f"engine alias '{alias}' not in settings; known aliases: {sorted(engines)}")
#     spec = engines[alias]
#     if "url" in spec:
#         return spec["url"]
#     server, database = spec.get("server", ""), spec.get("database", "")
#     if not server or server.startswith("<") or not database or database.startswith("<"):
#         raise ConfigError(f"engine '{alias}': fill in server/database in {settings.get('_source', 'settings')}")
#     from sqlalchemy.engine import URL
#     query = {"driver": spec.get("driver", settings.get("odbc_driver", "ODBC Driver 17 for SQL Server"))}
#     if spec.get("trusted_connection", True):
#         query["trusted_connection"] = "yes"
#     return URL.create("mssql+pyodbc", host=server, database=database, query=query)
#
#
# def get_engine(alias: str, settings: dict | None = None):
#     """SQLAlchemy engine for an alias (created once, then reused)."""
#     key = (alias, id(settings))
#     if key not in _engines:
#         from sqlalchemy import create_engine
#         _engines[key] = create_engine(engine_url(alias, settings))
#         log.info("engine '%s' created", alias)   # never log the URL itself
#     return _engines[key]
# @@FILE src/qbecat/io/files.py 937a45bf981bfbc6759b7ac8ec192d8a06992343fea4aea566bcbfe77770b3e1
# """Reading and writing tables from files (Excel, CSV, parquet)."""
#
# from __future__ import annotations
#
# import logging
# from pathlib import Path
#
# import pandas as pd
#
# log = logging.getLogger(__name__)
#
#
# def read_frame(path, sheet=0, **kwargs) -> pd.DataFrame:
#     """Read one table; header whitespace is stripped (a classic Excel trap)."""
#     path = Path(path)
#     suffix = path.suffix.lower()
#     if suffix in (".xlsx", ".xlsm", ".xls"):
#         df = pd.read_excel(path, sheet_name=sheet, **kwargs)
#     elif suffix == ".csv":
#         df = pd.read_csv(path, **kwargs)
#     elif suffix == ".parquet":
#         df = pd.read_parquet(path, **kwargs)
#     else:
#         raise ValueError(f"unsupported file type '{suffix}' for {path}")
#     df.columns = [str(c).strip() for c in df.columns]
#     log.info("read %s: %d rows x %d cols", path.name, *df.shape)
#     return df
#
#
# def read_sheets(path) -> dict[str, pd.DataFrame]:
#     """Every sheet of an Excel file as {sheet name: frame}."""
#     sheets = pd.read_excel(path, sheet_name=None)
#     for df in sheets.values():
#         df.columns = [str(c).strip() for c in df.columns]
#     return sheets
#
#
# def write_frame(df: pd.DataFrame, path) -> Path:
#     path = Path(path)
#     path.parent.mkdir(parents=True, exist_ok=True)
#     suffix = path.suffix.lower()
#     if suffix in (".xlsx", ".xlsm"):
#         df.to_excel(path, index=False)
#     elif suffix == ".csv":
#         df.to_csv(path, index=False)
#     elif suffix == ".parquet":
#         df.to_parquet(path, index=False)
#     else:
#         raise ValueError(f"unsupported file type '{suffix}'")
#     log.info("wrote %s (%d rows)", path, len(df))
#     return path
#
#
# def write_sheets(frames: dict[str, pd.DataFrame], path) -> Path:
#     """Several frames into one Excel file, one sheet each."""
#     path = Path(path)
#     path.parent.mkdir(parents=True, exist_ok=True)
#     with pd.ExcelWriter(path) as xl:
#         for name, df in frames.items():
#             df.to_excel(xl, sheet_name=str(name)[:31], index=False)
#     log.info("wrote %s (%d sheets)", path, len(frames))
#     return path
# @@FILE src/qbecat/io/loaders.py c9fc15716f9adcda15f74bdaa448eacc3d9e67318492240662fae7af8a8fc8cd
# """
# Loaders: query -> canonical columns -> validated DataFrame.
#
# Every loader takes its identifiers as arguments (no global settings inside
# functions) and an engine alias, so the same function serves every analysis.
# Each returns canonical column names (see qbecat.schema) and has already
# been validated, so a bad extract fails here with row numbers, not three
# steps later.
# """
#
# from __future__ import annotations
#
# import logging
#
# import pandas as pd
#
# from ..schema import to_canonical, validate
# from .sql import run_query
#
# log = logging.getLogger(__name__)
#
# _ELT_COLS = {c: c for c in ["event_id", "mean_loss", "sd_i", "sd_c", "exposure"]}
#
#
# def load_n_years(yeqt_id: int, engine="QBE_SANDBOX") -> int:
#     """Number of simulated years (including years with no events)."""
#     return int(run_query("n_years", engine, yeqt_id=yeqt_id).iloc[0, 0])
#
#
# def load_occurrences(yeqt_id: int, vendor_version_id: int, hazard_zone_id: int,
#                      engine="QBE_SANDBOX") -> pd.DataFrame:
#     """Every occurrence of the YEQT with its loss quantile and vendor event id."""
#     df = run_query("occurrences", engine, yeqt_id=yeqt_id,
#                    vendor_version_id=vendor_version_id, hazard_zone_id=hazard_zone_id)
#     df = to_canonical(df, {c: c for c in ["year", "sim_event_id", "instance_id",
#                                           "event_id", "quantile"]}, "occurrences")
#     return validate(df, "occurrences", "load_occurrences")
#
#
# def load_group_elt(port_grouping_id: int, hazard_grouping_id: int,
#                    engine="QBE_MAIN") -> pd.DataFrame:
#     """Group portfolio ELT (one row per event)."""
#     df = run_query("group_elt", engine, port_grouping_id=port_grouping_id,
#                    hazard_grouping_id=hazard_grouping_id)
#     return validate(to_canonical(df, _ELT_COLS, "elt"), "elt", "load_group_elt")
#
#
# def load_account_elts(analysis_id: int, persp_code: str = "RL", load_factor: float = 1.0,
#                       engine="RMS") -> pd.DataFrame:
#     """
#     Account ELTs (one row per account and event). load_factor scales
#     mean_loss, sd_i and sd_c (not exposure), as in the marginal impact method.
#     """
#     df = run_query("account_elts", engine, analysis_id=analysis_id, persp_code=persp_code)
#     df = to_canonical(df, {"account_id": "account_id", **_ELT_COLS}, "elt")
#     df = apply_load_factor(df, load_factor)
#     return validate(df, "elt", "load_account_elts")
#
#
# def load_reference_marginals(analysis_id: int, engine="QBE_MAIN") -> pd.DataFrame:
#     """Reference marginal impacts (account_id, reference)."""
#     df = run_query("reference_marginals", engine, analysis_id=analysis_id)
#     df["account_id"] = pd.to_numeric(df["account_id"], errors="coerce")
#     bad = int(df["account_id"].isna().sum())
#     if bad:
#         log.warning("%d reference rows have a non-numeric account id and are dropped", bad)
#     return df.dropna(subset=["account_id"]).astype({"account_id": "int64"})
#
#
# def apply_load_factor(elt: pd.DataFrame, factor: float) -> pd.DataFrame:
#     """Scale mean and both SDs by a load factor; exposure unchanged."""
#     if factor == 1.0:
#         return elt
#     return elt.assign(mean_loss=elt["mean_loss"] * factor,
#                       sd_i=elt["sd_i"] * factor, sd_c=elt["sd_c"] * factor)
# @@FILE src/qbecat/io/queries/account_elts.sql d467376de7aa1a587f5960e08878eb61153de397c1b444f0e824d9396b82960d
# -- Account-level ELTs for one RDM analysis: one row per (account, event).
# -- Server: RMS (RDM)
# SELECT ra.ID         AS account_id,
#        ra.EVENTID    AS event_id,
#        ra.PERSPVALUE AS mean_loss,
#        ras.STDDEVI   AS sd_i,
#        ras.STDDEVC   AS sd_c,
#        ras.EXPVALUE  AS exposure
# FROM {rdm_account} ra
# JOIN {rdm_account_std} ras
#   ON  ra.ANLSID      = ras.ANLSID
#   AND ra.ID          = ras.ID
#   AND ra.PERSPCODE   = ras.PERSPCODE
#   AND ra.EVENTID     = ras.EVENTID
#   AND ra.PARTITIONID = ras.PARTITIONID
# WHERE ra.ANLSID    = :analysis_id
#   AND ra.PERSPCODE = :persp_code
#   AND ras.EXPVALUE > 0
# @@FILE src/qbecat/io/queries/group_elt.sql b81a34d491b9eefe91ba3f044ea865ef01a56ebde86c6179ccddc60c4fec3478
# -- Group portfolio ELT: one row per vendor event.
# -- Server: QBE main
# SELECT VENDOREVENTID AS event_id,
#        PerspValue    AS mean_loss,
#        StdDevI       AS sd_i,
#        StdDevC       AS sd_c,
#        ExpValue      AS exposure
# FROM {group_elt}
# WHERE PortGroupingID       = :port_grouping_id
#   AND HazardZoneGroupingID = :hazard_grouping_id
#   AND ExpValue > 0
# @@FILE src/qbecat/io/queries/n_years.sql 1a98039620a044ba5684e28a65734c5e5adf53d53b810618af49836155bb9d7e
# -- Number of simulated years in the simulation set of :yeqt_id.
# -- YEQT has no rows for years without events, so count distinct years across
# -- every YEQT that shares the same simulation set (NumSimID).
# -- Server: QBE sandbox (alias in settings: engines.QBE_SANDBOX)
# SELECT COUNT(DISTINCT y.SimID) AS n_years
# FROM {yeqt} y
# JOIN {yeqt_info} yi       ON yi.YEQTID      = y.YEQTID
# JOIN {sim_table_info} sti ON sti.SimTableID = yi.SimTableID
# WHERE sti.NumSimID = (
#     SELECT sti2.NumSimID
#     FROM {yeqt_info} yi2
#     JOIN {sim_table_info} sti2 ON sti2.SimTableID = yi2.SimTableID
#     WHERE yi2.YEQTID = :yeqt_id
# )
# @@FILE src/qbecat/io/queries/occurrences.sql 27658fd9017fd0cdc7337af726eb71b26a4cc37d3a396b0c1caabb7756a92981
# -- Every simulated occurrence in a YEQT, with the vendor event id the ELTs use.
# -- Same-server join (YEQT and the vendor event map are both on the sandbox),
# -- so it runs in SQL. Output columns are already canonical.
# -- Server: QBE sandbox
# SELECT y.SimID        AS [year],
#        y.EventID      AS sim_event_id,
#        y.InstanceID   AS instance_id,
#        v.VENDOREVENTID AS event_id,
#        y.LossQuantile AS quantile
# FROM {yeqt} y
# JOIN {vendor_events_map} v ON v.EVENTID = y.EventID
# WHERE y.YEQTID       = :yeqt_id
#   AND v.VENDORVERID  = :vendor_version_id
#   AND v.HAZARDZONEID = :hazard_zone_id
# @@FILE src/qbecat/io/queries/reference_marginals.sql c3029915406775ee08df4c7d897df4153c64dc8291c9824b92ad9599ebade05b
# -- Reference marginal impacts to compare against: one row per account group.
# -- Accgrpid is stored as text; the loader converts it to a number.
# -- Server: QBE main
# SELECT Accgrpid       AS account_id,
#        MarginalImpact AS reference
# FROM {reference_marginals}
# WHERE RDM_ANLSID = :analysis_id
# @@FILE src/qbecat/io/sql.py 349d77fac155f1d1d3586f68898759c204b02fff0e1ec7747598b9218ce30284
# """
# SQL lives in versioned .sql files under qbecat/io/queries/, not in Python strings.
#
# In a .sql file:
#   {table_key}   a table name, filled from settings 'tables:' (identifiers only)
#   :param        a value, bound safely by the driver (never pasted into the text)
#
# Debugging a query: show_sql("account_elts", analysis_id=112) gives the exact
# text with values inlined, ready to paste into SSMS. (show_sql is for reading
# only; run_query always binds values properly.)
# """
#
# from __future__ import annotations
#
# import logging
# import re
# import time
# from pathlib import Path
#
# import pandas as pd
#
# from ..config import ConfigError, load_settings
#
# log = logging.getLogger(__name__)
#
# QUERY_DIR = Path(__file__).parent / "queries"
# _TABLE = re.compile(r"\{(\w+)\}")
# _SAFE_IDENTIFIER = re.compile(r"^[A-Za-z0-9_.\[\]]+$")
#
#
# def list_queries() -> list[str]:
#     return sorted(p.stem for p in QUERY_DIR.glob("*.sql"))
#
#
# def query_text(name: str, tables: dict | None = None) -> str:
#     """The query with {table} placeholders filled in (values still as :params)."""
#     path = QUERY_DIR / f"{name}.sql"
#     if not path.exists():
#         raise FileNotFoundError(f"no query '{name}'; available: {list_queries()}")
#     if tables is None:
#         tables = load_settings().get("tables", {})
#     text = path.read_text(encoding="utf-8")
#
#     def fill(m):
#         key = m.group(1)
#         if key not in tables:
#             raise ConfigError(f"query '{name}' needs table '{key}': add it under 'tables:' in settings")
#         value = str(tables[key])
#         if value.startswith("<") or not _SAFE_IDENTIFIER.match(value):
#             raise ConfigError(f"table '{key}' = '{value}' is a placeholder or not a plain table name")
#         return value
#
#     return _TABLE.sub(fill, text)
#
#
# def show_sql(name: str, tables: dict | None = None, **params) -> str:
#     """Query text with parameter values inlined, for pasting into SSMS. Display only."""
#     text = query_text(name, tables)
#     for k, v in params.items():
#         literal = f"'{v}'" if isinstance(v, str) else str(v)
#         text = re.sub(rf":{k}\b", literal, text)
#     return text
#
#
# def run_query(name: str, engine, tables: dict | None = None, **params) -> pd.DataFrame:
#     """Run a named query with bound parameters. engine: alias string or SQLAlchemy engine/connection."""
#     from sqlalchemy import text as sql_text
#     if isinstance(engine, str):
#         from .engines import get_engine
#         engine = get_engine(engine)
#     t0 = time.perf_counter()
#     df = pd.read_sql(sql_text(query_text(name, tables)), engine, params=params)
#     log.info("query %-22s %10s rows  %6.1fs", name, f"{len(df):,}", time.perf_counter() - t0)
#     return df
# @@FILE src/qbecat/log.py 2aa0d9aeafc0072b7a66acd9edee87601a342b47e046619ca892612808395c38
# """
# Library logging. The library never prints; it logs to the 'qbecat' logger,
# which is silent until you call configure_logging() in a notebook or script.
# """
#
# from __future__ import annotations
#
# import logging
# import sys
#
# _FORMAT = "%(asctime)s %(levelname)-7s %(name)s: %(message)s"
#
#
# def configure_logging(level: str | int = "INFO", logfile: str | None = None, stream=sys.stdout):
#     """Show library log messages (pipeline steps, queries, row counts). Safe to call twice."""
#     logger = logging.getLogger("qbecat")
#     logger.setLevel(level)
#     for h in list(logger.handlers):
#         if getattr(h, "_qbecat_owned", False):
#             logger.removeHandler(h)
#     handlers = [logging.StreamHandler(stream)]
#     if logfile:
#         handlers.append(logging.FileHandler(logfile, encoding="utf-8"))
#     for h in handlers:
#         h.setFormatter(logging.Formatter(_FORMAT, "%H:%M:%S"))
#         h._qbecat_owned = True
#         logger.addHandler(h)
#     logger.propagate = False
#     return logger
#
#
# logging.getLogger("qbecat").addHandler(logging.NullHandler())
# @@FILE src/qbecat/marginal/__init__.py 683dddf75d63c3280e53382273d289470ad84de1e4692a0e7a5261401cc9441e
# """Marginal impact of accounts on the group portfolio's 1-in-T OEP."""
#
# from .measures import Allocation, allocate, last_in_for_window, last_in_marginals, standalone
# from .run import (MarginalSettings, combine_measures, compare_to_reference, marginal_impact_pipeline,
#                   measure_columns, run_marginal_impact)
# from .tail import GroupTail, Window, group_tail, kernel_weights, tail_window, window_size
#
# __all__ = ["Allocation", "allocate", "last_in_for_window", "last_in_marginals", "standalone",
#            "MarginalSettings", "combine_measures", "compare_to_reference", "marginal_impact_pipeline",
#            "measure_columns", "run_marginal_impact", "GroupTail", "Window", "group_tail",
#            "kernel_weights", "tail_window", "window_size"]
# @@FILE src/qbecat/marginal/measures.py 98ba881c452d9d1885518b94376c970c7fd73687a80332b3b47ff9fb56d6170d
# """
# The four marginal impact measures, each a plain function of the group tail
# and the window of account contributions.
#
#   last-in marginal   group 1-in-T with the account minus without it
#                      (single rank, and smoothed over neighbouring ranks)
#   kernel co-VaR      the account's share of the group 1-in-T (bell-weighted ranks)
#   co-TVaR            the account's share of the tail beyond the 1-in-T
#   standalone         the account's own 1-in-T, ignoring the rest of the group
# """
#
# from __future__ import annotations
#
# import logging
# from dataclasses import dataclass
#
# import numpy as np
# import pandas as pd
#
# from ..schema import OCC_KEY
# from ..simulation.losses import occurrence_losses
# from .tail import (GroupTail, Window, kernel_label, kernel_weights, tail_window, window_size,
#                    year_starts)
#
# log = logging.getLogger(__name__)
#
#
# # ------------------------------------------------------------------ last-in
# def last_in_for_window(window: Window, tail: GroupTail, account_ids,
#                        kernel_spreads=(0.10, 0.20)) -> pd.DataFrame:
#     """
#     Remove each account's contribution from every occurrence it touches in the
#     window, recompute those years' OEP, re-sort, and compare with the base.
#
#     Exact when the deepest rank read is still >= the OEP of the first year
#     outside the window (no outside year could have climbed in).
#     """
#     K, target = window.size, tail.target_rank
#     G = window.occ["group_loss"].to_numpy()
#     starts = year_starts(window.occ)
#     base = tail.years["oep"].to_numpy()[:K]
#     outside_max = float(tail.years["oep"].iloc[K]) if len(tail.years) > K else 0.0
#     deepest = min(K, window_size(target, kernel_spreads))
#     ranks = np.arange(1, K + 1)
#     kernels = {kernel_label("last_in_smoothed", target, f): kernel_weights(ranks, target, f)
#                for f in kernel_spreads}
#     by_account = {a: (g["row"].to_numpy(), g["contribution"].to_numpy())
#                   for a, g in window.contributions.groupby("account_id")}
#
#     rows = []
#     for a in account_ids:
#         if a in by_account:
#             r, c = by_account[a]
#             net = G.copy()
#             np.subtract.at(net, r, c)
#             new = -np.sort(-np.maximum.reduceat(net, starts))
#         else:                                   # touches none of these years
#             new = base
#         row = {"account_id": a,
#                "last_in_marginal": tail.rp_loss - new[target - 1],
#                "last_in_exact": bool(new[deepest - 1] >= outside_max),
#                "last_in_window": K}
#         for name, w in kernels.items():
#             row[name] = float(w @ (base - new))
#         rows.append(row)
#     return pd.DataFrame(rows)
#
#
# def last_in_marginals(tail: GroupTail, window: Window, account_elts: pd.DataFrame,
#                       occurrences: pd.DataFrame, kernel_spreads=(0.10, 0.20)) -> pd.DataFrame:
#     """All accounts; the window doubles only for accounts whose answer is not yet exact."""
#     pending = list(pd.unique(account_elts["account_id"]))
#     finished = []
#     while pending:
#         result = last_in_for_window(window, tail, pending, kernel_spreads)
#         finished.append(result[result["last_in_exact"]])
#         pending = list(result.loc[~result["last_in_exact"], "account_id"])
#         if not pending:
#             break
#         if window.size >= len(tail.years):     # whole ranking used: exact by definition
#             finished.append(result[~result["last_in_exact"]].assign(last_in_exact=True))
#             break
#         log.info("last-in: %d accounts not exact at window %s; doubling", len(pending), f"{window.size:,}")
#         window = tail_window(tail, account_elts[account_elts["account_id"].isin(pending)],
#                              occurrences, kernel_spreads, size=2 * window.size)
#     return pd.concat(finished, ignore_index=True)
#
#
# # ------------------------------------------------------- co-VaR / co-TVaR
# @dataclass
# class Allocation:
#     shares: pd.DataFrame     # account_id + one column per measure
#     totals: pd.DataFrame     # per measure: group, accounts, other_business
#
#
# def rank_weights(tail: GroupTail, kernel_spreads=(0.10, 0.20)) -> dict[str, pd.Series]:
#     """Year weights (indexed by year) for each allocation measure; each sums to 1."""
#     ranks = tail.years.set_index("year")["rank"]
#     target = tail.target_rank
#     weights = {"co_tvar": (ranks <= target).astype(float) / target}
#     for f in kernel_spreads:
#         w = pd.Series(kernel_weights(ranks.to_numpy(), target, f), index=ranks.index)
#         weights[kernel_label("kernel_co_var", target, f)] = w
#     return {name: w[w > 0] for name, w in weights.items()}
#
#
# def allocate(window: Window, tail: GroupTail, kernel_spreads=(0.10, 0.20)) -> Allocation:
#     """
#     Share out each group figure using every account's contribution to each
#     year's defining occurrence. Accounts + other business = group, exactly.
#     """
#     defining = window.contributions.merge(tail.years[OCC_KEY], on=OCC_KEY)
#     oep = tail.years.set_index("year")["oep"]
#     window_years = set(tail.years["year"].iloc[:window.size])
#     shares, totals = [], {}
#     for name, w in rank_weights(tail, kernel_spreads).items():
#         outside = set(w.index) - window_years
#         if outside:
#             raise ValueError(f"{name}: {len(outside)} weighted years lie outside the window; "
#                              "increase the window size")
#         share = (defining["year"].map(w).fillna(0.0) * defining["contribution"]) \
#             .groupby(defining["account_id"]).sum().rename(name)
#         group_value = float((w * oep.reindex(w.index)).sum())
#         shares.append(share)
#         totals[name] = {"group": group_value, "accounts": float(share.sum()),
#                         "other_business": group_value - float(share.sum())}
#     shares = pd.concat(shares, axis=1).rename_axis("account_id").reset_index()
#     return Allocation(shares, pd.DataFrame(totals).T.rename_axis("measure").reset_index())
#
#
# # ---------------------------------------------------------------- standalone
# def _nth_largest(values: np.ndarray, n: int) -> float:
#     if len(values) < n:
#         return 0.0
#     return float(np.partition(values, len(values) - n)[len(values) - n])
#
#
# def standalone(account_elts: pd.DataFrame, occurrences: pd.DataFrame, n_years: int,
#                target_rank: int, batch_size: int = 25) -> pd.DataFrame:
#     """Each account on its own across all years: its 1-in-T OEP and AAL (batched for memory)."""
#     ids = pd.unique(account_elts["account_id"])
#     rows = []
#     for start in range(0, len(ids), batch_size):
#         batch = account_elts[account_elts["account_id"].isin(ids[start:start + batch_size])]
#         losses = occurrence_losses(batch, occurrences, by=["account_id"])
#         year_oep = losses.groupby(["account_id", "year"])["loss"].max()
#         aal = losses.groupby("account_id")["loss"].sum() / n_years
#         for a, oep in year_oep.groupby(level="account_id"):
#             rows.append({"account_id": a, "standalone": _nth_largest(oep.to_numpy(), target_rank),
#                          "standalone_aal": float(aal[a])})
#     return pd.DataFrame(rows, columns=["account_id", "standalone", "standalone_aal"])
# @@FILE src/qbecat/marginal/run.py 1b223b4923fb6fca2b5f573a0a1f25d61f400b7bdb2b24f96c7a48693e676997
# """
# Marginal impact end to end, as a traced pipeline.
#
#     summary, pipe = run_marginal_impact(group_elt, account_elts, occurrences, n_years,
#                                         reference=reference)
#     pipe.trace                               # rows and seconds per step
#     pipe.outputs["tail"].rp_loss             # group 1-in-200
#     pipe.outputs["allocations"].totals       # accounts + other business = group
#     pipe.follow(account_id=1234)             # one account through every step
#     pipe.run(..., stop_after="window")       # stop early while investigating
# """
#
# from __future__ import annotations
#
# from dataclasses import dataclass
#
# import numpy as np
# import pandas as pd
#
# from ..simulation.losses import occurrence_losses
# from ..simulation.severity import add_beta_parameters
# from ..trace import Pipeline, step
# from .measures import allocate, last_in_marginals, standalone
# from .tail import group_tail, tail_window
#
#
# @dataclass
# class MarginalSettings:
#     return_period: float = 200
#     kernel_spreads: tuple = (0.10, 0.20)   # fractions of the target rank (250 and 500 at 500k sims)
#     standalone_batch: int = 25             # accounts simulated together for standalone
#     include_standalone: bool = True        # the slowest step; switch off while iterating
#
#
# def standalone_for_tail(account_severity: pd.DataFrame, occurrences: pd.DataFrame, n_years: int,
#                         tail, batch_size: int = 25) -> pd.DataFrame:
#     """Each account's own 1-in-T OEP and AAL, at the group's target rank."""
#     return standalone(account_severity, occurrences, n_years, tail.target_rank, batch_size)
#
#
# def combine_measures(last_in: pd.DataFrame, allocations, standalone_measures=None,
#                      reference: pd.DataFrame | None = None) -> pd.DataFrame:
#     """One row per account with every measure, and differences to the reference if given."""
#     out = last_in.merge(allocations.shares, on="account_id", how="left")
#     if standalone_measures is not None:
#         out = out.merge(standalone_measures, on="account_id", how="left")
#     measures = measure_columns(out)
#     out[measures] = out[measures].fillna(0.0)
#     if reference is not None:
#         out = out.merge(reference, on="account_id", how="left")
#         ref = out["reference"].replace(0, np.nan)
#         for m in measures:
#             out[f"{m}_diff"] = out[m] - out["reference"]
#             out[f"{m}_diff_pct"] = 100 * out[f"{m}_diff"] / ref
#         out = out.sort_values("reference", ascending=False, na_position="last")
#     else:
#         out = out.sort_values("last_in_marginal", ascending=False)
#     return out.reset_index(drop=True)
#
#
# def measure_columns(summary: pd.DataFrame) -> list[str]:
#     prefixes = ("last_in_marginal", "last_in_smoothed", "kernel_co_var", "co_tvar")
#     cols = [c for c in summary.columns if c.startswith(prefixes) and not c.endswith(("_diff", "_diff_pct"))]
#     if "standalone" in summary.columns:
#         cols.append("standalone")
#     return cols
#
#
# def compare_to_reference(summary: pd.DataFrame) -> pd.DataFrame:
#     """Totals and error statistics of each measure against the reference marginals."""
#     both = summary.dropna(subset=["reference"])
#     positive = both[both["reference"] > 0]
#     rows = {}
#     for m in measure_columns(summary):
#         rows[m] = {
#             "total_ours / total_reference": positive[m].sum() / positive["reference"].sum(),
#             "size_weighted_abs_diff_pct": 100 * (positive[m] - positive["reference"]).abs().sum()
#                                           / positive["reference"].sum(),
#             "median_abs_diff_pct": both[f"{m}_diff_pct"].abs().median(),
#         }
#     out = pd.DataFrame(rows).T
#     out.attrs["accounts_in_both"] = len(both)
#     out.attrs["only_ours"] = int(summary["reference"].isna().sum())
#     return out
#
#
# def marginal_impact_pipeline(settings: MarginalSettings | None = None) -> Pipeline:
#     s = settings or MarginalSettings()
#     steps = [
#         step(add_beta_parameters, "group_severity", use={"elt": "group_elt"}),
#         step(add_beta_parameters, "account_severity", use={"elt": "account_elts"}),
#         step(occurrence_losses, "group_losses", use={"elt": "group_severity"}),
#         step(group_tail, "tail", return_period=s.return_period),
#         step(tail_window, "window", use={"account_elts": "account_severity"},
#              kernel_spreads=s.kernel_spreads),
#         step(allocate, "allocations", kernel_spreads=s.kernel_spreads,
#              check=lambda a: [] if np.allclose(a.totals["group"],
#                                                a.totals["accounts"] + a.totals["other_business"])
#              else ["allocation does not add up to the group"]),
#         step(last_in_marginals, "last_in", use={"account_elts": "account_severity"},
#              kernel_spreads=s.kernel_spreads),
#     ]
#     if s.include_standalone:
#         steps.append(step(standalone_for_tail, "standalone", batch_size=s.standalone_batch))
#         steps.append(step(combine_measures, "summary", use={"standalone_measures": "standalone"}))
#     else:
#         steps.append(step(combine_measures, "summary"))
#     return Pipeline("marginal_impact", steps)
#
#
# def run_marginal_impact(group_elt: pd.DataFrame, account_elts: pd.DataFrame,
#                         occurrences: pd.DataFrame, n_years: int,
#                         reference: pd.DataFrame | None = None,
#                         settings: MarginalSettings | None = None, **run_kwargs):
#     """Run the whole method. Returns (summary, pipeline); keep the pipeline for debugging."""
#     pipe = marginal_impact_pipeline(settings)
#     summary = pipe.run(group_elt=group_elt, account_elts=account_elts, occurrences=occurrences,
#                        n_years=n_years, reference=reference, **run_kwargs)
#     return summary, pipe
# @@FILE src/qbecat/marginal/tail.py e8ecc6ec498459a51afb74960de4a9559ae2539501cfb3c6fc299c8e2bb5fd15
# """
# The group's tail: ranked years and the window of worst years the marginal
# measures look at.
#
# Terms
#   occurrence           one event happening once in one simulated year (year, sim_event_id, instance_id)
#   year OEP             the largest single occurrence loss in the year
#   rank                 years sorted by OEP, worst first; the 1-in-T is the year at rank round(n_years / T)
#   defining occurrence  the occurrence that sets a year's OEP
#   window               the worst K years (ranks 1..K) where account contributions are computed
# """
#
# from __future__ import annotations
#
# import logging
# from dataclasses import dataclass
#
# import numpy as np
# import pandas as pd
#
# from ..schema import OCC_KEY
# from ..simulation.losses import occurrence_losses, ranked_years
# from ..utils import target_rank
#
# log = logging.getLogger(__name__)
#
#
# @dataclass
# class GroupTail:
#     years: pd.DataFrame        # year, sim_event_id, instance_id, oep, rank (worst first)
#     occ_losses: pd.DataFrame   # every group occurrence loss
#     n_years: int
#     return_period: float
#     target_rank: int
#     rp_loss: float             # group OEP at the return period
#
#
# @dataclass
# class Window:
#     size: int                  # K: ranks 1..K are covered
#     occ: pd.DataFrame          # group occurrences in window years, sorted by rank; column group_loss
#     contributions: pd.DataFrame  # account_id, occurrence key, row (into occ), loss, contribution
#
#
# def group_tail(group_losses: pd.DataFrame, n_years: int, return_period: float) -> GroupTail:
#     """Rank the group's years by OEP and read the loss at the return period."""
#     years = ranked_years(group_losses)
#     k = target_rank(n_years, return_period)
#     if k > len(years):
#         raise ValueError(f"only {len(years):,} years have a loss but the 1-in-{return_period:g} "
#                          f"needs rank {k:,}")
#     rp_loss = float(years["oep"].iloc[k - 1])
#     log.info("group 1-in-%g OEP = %s (rank %s of %s years)", return_period,
#              f"{rp_loss:,.0f}", f"{k:,}", f"{n_years:,}")
#     return GroupTail(years, group_losses, n_years, return_period, k, rp_loss)
#
#
# def window_size(target: int, kernel_spreads) -> int:
#     """Deepest rank any measure reads: target + 3 x the widest kernel spread."""
#     return int(round(target * (1 + 3 * max(kernel_spreads))))
#
#
# def tail_window(tail: GroupTail, account_elts: pd.DataFrame, occurrences: pd.DataFrame,
#                 kernel_spreads=(0.10, 0.20), size: int | None = None) -> Window:
#     """
#     Every account's contribution to every group occurrence in the worst `size`
#     years, scaled so that per occurrence they never add up to more than the
#     group's loss:  scale = min(1, group loss / sum of account losses).
#     If accounts add up to less than the group, the gap is "other business".
#     """
#     size = min(size or window_size(tail.target_rank, kernel_spreads), len(tail.years))
#     in_window = tail.years.iloc[:size][["year", "rank"]]
#     occ = (tail.occ_losses.merge(in_window, on="year")
#            .rename(columns={"loss": "group_loss"})
#            .sort_values(["rank", "group_loss"], ascending=[True, False], kind="stable")
#            .reset_index(drop=True))
#
#     acct = occurrence_losses(account_elts, occurrences[occurrences["year"].isin(in_window["year"])],
#                              by=["account_id"])
#     acct = acct.merge(occ[OCC_KEY + ["group_loss"]].reset_index(names="row"), on=OCC_KEY)
#     total = acct.groupby(OCC_KEY)["loss"].transform("sum").to_numpy()
#     g = acct["group_loss"].to_numpy()
#     scale = np.divide(g, total, out=np.zeros(len(acct)), where=total > 0)
#     acct["contribution"] = acct["loss"].to_numpy() * np.minimum(1.0, scale)
#     contributions = acct[["account_id", *OCC_KEY, "row", "loss", "contribution"]]
#
#     # self-check: per-year maxima of the window must reproduce the ranked OEPs
#     starts = year_starts(occ)
#     if not np.allclose(np.maximum.reduceat(occ["group_loss"].to_numpy(), starts),
#                        tail.years["oep"].to_numpy()[:size]):
#         raise AssertionError("window occurrences do not reproduce the group's ranked OEPs")
#     log.info("window: %s years, %s occurrences, %s account contributions",
#              f"{size:,}", f"{len(occ):,}", f"{len(contributions):,}")
#     return Window(size, occ, contributions)
#
#
# def year_starts(occ: pd.DataFrame) -> np.ndarray:
#     """Row where each year's block starts in a rank-sorted occurrence table."""
#     r = occ["rank"].to_numpy()
#     return np.flatnonzero(np.r_[True, r[1:] != r[:-1]])
#
#
# def kernel_weights(ranks: np.ndarray, target: int, fraction: float) -> np.ndarray:
#     """Bell-curve weights over ranks centred on target (zero beyond 3 spreads), summing to 1."""
#     spread = fraction * target
#     w = np.exp(-0.5 * ((ranks - target) / spread) ** 2)
#     w[np.abs(ranks - target) > 3 * spread] = 0.0
#     return w / w.sum()
#
#
# def kernel_label(prefix: str, target: int, fraction: float) -> str:
#     return f"{prefix}_{round(fraction * target)}"
# @@FILE src/qbecat/schema.py 9627445b15347c5b0b8a75f5c6e1c57504dc69f8ae2ea2f1c1f41cea7fcc3f44
# """
# Canonical tables and their validation.
#
# Every loader maps source columns to these names once, at the boundary, so
# everything downstream speaks one language. validate() reports ALL problems
# at once, with the offending row numbers, instead of failing later with a
# cryptic KeyError or a silently wrong number.
#
# Canonical tables
# ----------------
# elt          event_id, mean_loss, sd_i, sd_c, exposure  [+ rate, account_id]
# occurrences  year, sim_event_id, instance_id, event_id, quantile
#              (one row per simulated occurrence; event_id is the ELT's event key,
#               several ELT events can map to one simulated occurrence)
# occ_losses   year, sim_event_id, instance_id, loss  [+ account_id]
# exposure     location_id, policy_id, tiv  [+ coverage values, terms, grouping]
# """
#
# from __future__ import annotations
#
# from dataclasses import dataclass, field
# from typing import Callable
#
# import numpy as np
# import pandas as pd
#
# OCC_KEY = ["year", "sim_event_id", "instance_id"]   # identifies one occurrence
#
#
# class SchemaError(ValueError):
#     pass
#
#
# @dataclass
# class Schema:
#     name: str
#     required: dict                    # column -> "id" | "number"
#     optional: dict = field(default_factory=dict)
#     key: list = field(default_factory=list)          # must be unique (columns that exist)
#     rules: list = field(default_factory=list)        # (description, fn(df) -> bad-row mask)
#
#
# def _number(col):
#     return lambda df: ~np.isfinite(pd.to_numeric(df[col], errors="coerce").to_numpy(float))
#
#
# SCHEMAS: dict[str, Schema] = {
#     "elt": Schema(
#         "elt",
#         required={"event_id": "id", "mean_loss": "number", "sd_i": "number",
#                   "sd_c": "number", "exposure": "number"},
#         optional={"rate": "number", "account_id": "id"},
#         key=["account_id", "event_id"],
#         rules=[
#             ("mean_loss < 0", lambda d: d["mean_loss"] < 0),
#             ("sd_i < 0 or sd_c < 0", lambda d: (d["sd_i"] < 0) | (d["sd_c"] < 0)),
#             ("exposure <= 0", lambda d: d["exposure"] <= 0),
#             ("mean_loss > exposure", lambda d: d["mean_loss"] > d["exposure"] * (1 + 1e-9)),
#             ("rate < 0", lambda d: d["rate"] < 0 if "rate" in d else pd.Series(False, d.index)),
#         ]),
#     "occurrences": Schema(
#         "occurrences",
#         required={"year": "id", "sim_event_id": "id", "instance_id": "id",
#                   "event_id": "id", "quantile": "number"},
#         key=["year", "sim_event_id", "instance_id", "event_id"],
#         rules=[("quantile outside [0, 1]",
#                 lambda d: (d["quantile"] < 0) | (d["quantile"] > 1))]),
#     "occ_losses": Schema(
#         "occ_losses",
#         required={"year": "id", "sim_event_id": "id", "instance_id": "id", "loss": "number"},
#         optional={"account_id": "id"},
#         key=["account_id", "year", "sim_event_id", "instance_id"],
#         rules=[("loss < 0", lambda d: d["loss"] < 0)]),
#     "exposure": Schema(
#         "exposure",
#         required={"location_id": "id", "policy_id": "id"},
#         optional={"tiv": "number", "building": "number", "contents": "number", "bi": "number",
#                   "deductible": "number", "deductible_pct": "number", "location_limit": "number",
#                   "attachment": "number", "policy_limit": "number", "share": "number"},
#         key=["location_id"],
#         rules=[("share outside (0, 1]",
#                 lambda d: ((d["share"] <= 0) | (d["share"] > 1)) if "share" in d
#                 else pd.Series(False, d.index))]),
# }
#
#
# def problems(df: pd.DataFrame, schema: str | Schema, max_rows: int = 5) -> list[str]:
#     """Every problem found, as readable strings (empty list = valid)."""
#     s = SCHEMAS[schema] if isinstance(schema, str) else schema
#     out = []
#     missing = [c for c in s.required if c not in df.columns]
#     if missing:
#         return [f"missing required columns {missing}; columns present: {list(df.columns)}"]
#
#     def rows(mask) -> str:
#         idx = np.flatnonzero(np.asarray(mask, dtype=bool))
#         shown = ", ".join(str(df.index[i]) for i in idx[:max_rows])
#         return f"{len(idx):,} rows (e.g. index {shown})"
#
#     for col, kind in {**s.required, **{c: k for c, k in s.optional.items() if c in df.columns}}.items():
#         if col in s.required and df[col].isna().any():
#             out.append(f"'{col}' has nulls: {rows(df[col].isna())}")
#         if kind == "number":
#             bad = _number(col)(df) & df[col].notna()
#             if bad.any():
#                 out.append(f"'{col}' is not numeric/finite: {rows(bad)}")
#     if out:                       # rules below assume clean types
#         return out
#     key = [c for c in s.key if c in df.columns]
#     if key:
#         dup = df.duplicated(key, keep=False)
#         if dup.any():
#             out.append(f"duplicate key {key} (a repeated row would double-count losses): {rows(dup)}")
#     for desc, fn in s.rules:
#         bad = fn(df)
#         if bool(np.any(bad)):
#             out.append(f"{desc}: {rows(bad)}")
#     return out
#
#
# def validate(df: pd.DataFrame, schema: str | Schema, where: str = "") -> pd.DataFrame:
#     """Raise SchemaError listing every problem; return df unchanged if valid."""
#     found = problems(df, schema)
#     if found:
#         name = schema if isinstance(schema, str) else schema.name
#         raise SchemaError(f"{where or name}: {len(found)} problem(s) in '{name}' table:\n  - "
#                           + "\n  - ".join(found))
#     return df
#
#
# def to_canonical(df: pd.DataFrame, column_map: dict, schema: str | None = None,
#                  numeric: bool = True) -> pd.DataFrame:
#     """
#     Rename source columns to canonical ones using {canonical: source} and keep
#     only mapped columns. Converts 'number' columns with pd.to_numeric (bad
#     values become NaN and are then reported by validate).
#     """
#     lookup = {str(c).strip().lower(): c for c in df.columns}
#     rename, missing = {}, []
#     for canonical, source in column_map.items():
#         hit = lookup.get(str(source).strip().lower())
#         if hit is None:
#             missing.append(source)
#         else:
#             rename[hit] = canonical
#     if missing:
#         raise SchemaError(f"source columns not found: {missing}; columns present: {list(df.columns)}")
#     out = df[list(rename)].rename(columns=rename)
#     if schema and numeric:
#         s = SCHEMAS[schema]
#         for col, kind in {**s.required, **s.optional}.items():
#             if kind == "number" and col in out:
#                 out[col] = pd.to_numeric(out[col], errors="coerce").astype(float)
#     return out
# @@FILE src/qbecat/simulation/__init__.py a6fd0de991bf0576de2ba574b515d3c6679079c6e1d34839504964f07ae81282
# """ELT -> occurrence losses -> year losses, with one shared severity definition."""
#
# from .losses import occurrence_losses, ranked_years, year_losses
# from .severity import add_beta_parameters, loss_at_quantile
# from .synthetic import (synthetic_accounts, synthetic_broker_file, synthetic_elt,
#                         synthetic_exposure, synthetic_occurrences)
#
# __all__ = ["occurrence_losses", "ranked_years", "year_losses", "add_beta_parameters",
#            "loss_at_quantile", "synthetic_accounts", "synthetic_broker_file", "synthetic_elt",
#            "synthetic_exposure", "synthetic_occurrences"]
# @@FILE src/qbecat/simulation/losses.py f027e426736a18fae45a0cda561eddd47b25fecbca59ef82bb5600a6b6c01ade
# """
# ELT + occurrences (YEQT) -> occurrence losses -> year losses.
#
# The join of YEQT to ELT happens here, in Python, because the ELTs and the
# YEQT live on different servers that cannot be linked. Joins within one
# server (YEQT to the vendor event map) are done in SQL (io/queries).
#
# Common random numbers: every table read against the same occurrences uses
# the same quantile for the same occurrence, so the group and its accounts
# see identical simulated years. Comparisons between them contain no
# reseeding noise.
# """
#
# from __future__ import annotations
#
# import logging
#
# import numpy as np
# import pandas as pd
#
# from ..schema import OCC_KEY
# from ..utils import chunks_by
# from .severity import add_beta_parameters, loss_at_quantile
#
# log = logging.getLogger(__name__)
#
#
# def occurrence_losses(elt: pd.DataFrame, occurrences: pd.DataFrame, by=(),
#                       chunk_years: int | None = None) -> pd.DataFrame:
#     """
#     Loss of every occurrence for the events in `elt`.
#
#     by=["account_id"] keeps accounts separate. ELT events that map to the
#     same simulated occurrence are parts of one occurrence and are summed.
#     chunk_years: process this many years at a time to bound memory
#     (results are identical; only peak memory changes).
#     Returns columns [*by, year, sim_event_id, instance_id, loss].
#     """
#     by = list(by)
#     if "alpha" not in elt.columns:
#         elt = add_beta_parameters(elt)
#     cols = by + ["event_id", "mean_loss", "exposure", "alpha", "beta", "degenerate"]
#     elt = elt[cols]
#     if chunk_years:
#         parts = [occurrence_losses(elt, part, by) for part in chunks_by(occurrences, "year", chunk_years)]
#         return pd.concat(parts, ignore_index=True)
#     rows = occurrences[OCC_KEY + ["event_id", "quantile"]].merge(elt, on="event_id", how="inner")
#     rows["loss"] = loss_at_quantile(rows, rows["quantile"].to_numpy())
#     return rows.groupby(by + OCC_KEY, as_index=False, sort=False)["loss"].sum()
#
#
# def year_losses(occ_losses: pd.DataFrame, by=()) -> pd.DataFrame:
#     """
#     One row per year that has at least one occurrence:
#     [*by, year, oep (largest occurrence), aep (sum), n_occurrences].
#     Years with no events are NOT listed; pass n_years to the EP functions.
#     """
#     g = occ_losses.groupby(list(by) + ["year"], sort=False)["loss"]
#     out = pd.DataFrame({"oep": g.max(), "aep": g.sum(), "n_occurrences": g.size()})
#     return out.reset_index()
#
#
# def ranked_years(occ_losses: pd.DataFrame) -> pd.DataFrame:
#     """
#     Each year's defining occurrence (the one that sets its OEP), worst year first:
#     [year, sim_event_id, instance_id, oep, rank].
#     """
#     idx = occ_losses.groupby("year")["loss"].idxmax()
#     years = (occ_losses.loc[idx, OCC_KEY + ["loss"]]
#              .rename(columns={"loss": "oep"})
#              .sort_values("oep", ascending=False, kind="stable")
#              .reset_index(drop=True))
#     years["rank"] = np.arange(1, len(years) + 1)
#     return years
# @@FILE src/qbecat/simulation/severity.py 6ef05b9c3c17e63797cc87c18aa6e57c6f4ba5d74afa35c63a7ccf681df8b0fb
# """
# Per-event severity: the ONE place ELT moments become a loss distribution.
#
# Each event's loss is exposure x damage ratio, damage ratio ~ Beta(alpha, beta)
# moment-matched to
#     mu    = mean_loss / exposure
#     sigma = (sd_i + sd_c) / exposure
# The simulated path (losses at YEQT quantiles) and the analytic path (ep.analytic)
# both call add_beta_parameters, so they can never disagree because of a
# parameterisation difference (calibration by construction).
#
# Rows a Beta cannot represent are handled explicitly and flagged so you can
# inspect them (elt.query("repaired") / elt.query("degenerate")):
#   degenerate  sd = 0, mean = 0 or mean >= exposure -> point mass at the mean
#               (capped at exposure)
#   repaired    variance at or above the Beta maximum mu(1-mu) -> capped just
#               under it; the mean is preserved exactly
# """
#
# from __future__ import annotations
#
# import logging
#
# import numpy as np
# import pandas as pd
# from scipy.special import betaincinv
#
# log = logging.getLogger(__name__)
#
# _VAR_CAP = 1 - 1e-6     # repaired variance = cap * mu(1-mu)
#
#
# def add_beta_parameters(elt: pd.DataFrame, repair: str = "cap") -> pd.DataFrame:
#     """
#     Return elt with columns alpha, beta, degenerate, repaired added.
#     repair: "cap" (default) or "raise" (refuse rows above the Beta variance bound).
#     """
#     if repair not in ("cap", "raise"):
#         raise ValueError("repair must be 'cap' or 'raise'")
#     exposure = elt["exposure"].to_numpy(float)
#     mu = elt["mean_loss"].to_numpy(float) / exposure
#     sigma = (elt["sd_i"].to_numpy(float) + elt["sd_c"].to_numpy(float)) / exposure
#
#     degenerate = (sigma <= 0) | (mu <= 0) | (mu >= 1)
#     var, vmax = sigma ** 2, mu * (1 - mu)
#     repaired = ~degenerate & (var >= vmax)
#     if repaired.any():
#         if repair == "raise":
#             rows = elt.index[repaired][:5].tolist()
#             raise ValueError(f"{repaired.sum():,} ELT rows have sd too large for a Beta "
#                              f"(sigma^2 >= mu(1-mu)), e.g. index {rows}")
#         log.info("severity: %d of %d rows had variance capped at the Beta bound",
#                  repaired.sum(), len(elt))
#     var = np.where(repaired, vmax * _VAR_CAP, var)
#     with np.errstate(divide="ignore", invalid="ignore"):
#         nu = np.where(degenerate, np.nan, vmax / var - 1)
#     return elt.assign(alpha=mu * nu, beta=(1 - mu) * nu,
#                       degenerate=degenerate, repaired=repaired)
#
#
# def loss_at_quantile(rows: pd.DataFrame, quantile) -> np.ndarray:
#     """
#     Loss = exposure x BetaInverse(quantile; alpha, beta). `rows` must already
#     carry alpha/beta/degenerate (from add_beta_parameters). Point-mass rows
#     return their mean (capped at exposure) whatever the quantile.
#     """
#     q = np.asarray(quantile, dtype=float)
#     exposure = rows["exposure"].to_numpy(float)
#     loss = np.minimum(rows["mean_loss"].to_numpy(float), exposure)     # degenerate rows
#     live = ~rows["degenerate"].to_numpy(bool)
#     if live.any():
#         loss = loss.copy()
#         loss[live] = exposure[live] * betaincinv(rows["alpha"].to_numpy(float)[live],
#                                                  rows["beta"].to_numpy(float)[live], q[live])
#     return loss
# @@FILE src/qbecat/simulation/synthetic.py d8b0967ca08ebac277ba1adcb63737206cf82a185d9bf84f0a4c1f47697614c2
# """
# Synthetic data with realistic structure, for tests, examples and moving code
# between machines. Never use real exposure data for that.
# """
#
# from __future__ import annotations
#
# import numpy as np
# import pandas as pd
#
#
# def synthetic_elt(n_events: int = 300, seed: int = 0, total_rate: float = 2.0) -> pd.DataFrame:
#     """Group-style ELT with rates: event_id, rate, mean_loss, sd_i, sd_c, exposure."""
#     rng = np.random.default_rng(seed)
#     rate = rng.lognormal(0, 1.2, n_events)
#     rate *= total_rate / rate.sum()
#     exposure = rng.lognormal(np.log(5e8), 0.6, n_events)
#     damage = rng.beta(0.6, 12, n_events)                       # mean damage ratio, skewed
#     mean = exposure * damage
#     sd = mean * rng.uniform(0.6, 1.6, n_events)
#     sd = np.minimum(sd, 0.95 * exposure * np.sqrt(damage * (1 - damage)))
#     share_c = rng.uniform(0.2, 0.6, n_events)
#     return pd.DataFrame({"event_id": np.arange(1, n_events + 1), "rate": rate,
#                          "mean_loss": mean, "sd_i": sd * (1 - share_c), "sd_c": sd * share_c,
#                          "exposure": exposure})
#
#
# def synthetic_occurrences(elt: pd.DataFrame, n_years: int = 20_000, seed: int = 1) -> pd.DataFrame:
#     """
#     YEQT-style occurrences from an ELT with rates (Poisson frequency):
#     year, sim_event_id, instance_id, event_id, quantile.
#     Here sim_event_id == event_id (one ELT event per simulated event).
#     """
#     rng = np.random.default_rng(seed)
#     rate = elt["rate"].to_numpy(float)
#     counts = rng.poisson(rate.sum(), n_years)
#     years = np.repeat(np.arange(1, n_years + 1), counts)
#     events = rng.choice(elt["event_id"].to_numpy(), size=len(years), p=rate / rate.sum())
#     df = pd.DataFrame({"year": years, "sim_event_id": events})
#     df["instance_id"] = df.groupby(["year", "sim_event_id"]).cumcount() + 1
#     df["event_id"] = df["sim_event_id"]
#     df["quantile"] = rng.uniform(size=len(df))
#     return df
#
#
# def synthetic_accounts(group_elt: pd.DataFrame, n_accounts: int = 40, seed: int = 2,
#                        covered: float = 0.85, hit_rate: float = 0.35) -> pd.DataFrame:
#     """
#     Split a group ELT into account ELTs (account_id, event_id, mean_loss, sd_i,
#     sd_c, exposure). Accounts cover `covered` of each event's loss; the rest
#     is "other business". Each account is hit by roughly `hit_rate` of events.
#     """
#     rng = np.random.default_rng(seed)
#     size = rng.lognormal(0, 1.0, n_accounts)
#     rows = []
#     for _, ev in group_elt.iterrows():
#         hit = rng.uniform(size=n_accounts) < hit_rate
#         if not hit.any():
#             continue
#         w = size * hit * rng.uniform(0.5, 1.5, n_accounts)
#         w = covered * w / w.sum()
#         for a in np.flatnonzero(hit):
#             rows.append((a + 1, int(ev["event_id"]), ev["mean_loss"] * w[a], ev["sd_i"] * w[a],
#                          ev["sd_c"] * w[a], ev["exposure"] * w[a]))
#     return pd.DataFrame(rows, columns=["account_id", "event_id", "mean_loss", "sd_i", "sd_c", "exposure"])
#
#
# def synthetic_exposure(n_policies: int = 50, seed: int = 3) -> pd.DataFrame:
#     """Location-level exposure with location and policy terms."""
#     rng = np.random.default_rng(seed)
#     rows = []
#     loc = 1
#     for pol in range(1, n_policies + 1):
#         n_loc = rng.integers(1, 8)
#         attachment = float(rng.choice([0, 1e6, 5e6]))
#         policy_limit = float(rng.choice([2e7, 5e7, np.nan]))
#         share = float(rng.choice([1.0, 0.5, 0.25]))
#         for _ in range(n_loc):
#             building = rng.lognormal(np.log(4e6), 0.8)
#             rows.append({"location_id": loc, "policy_id": pol,
#                          "country": rng.choice(["AU", "NZ"]),
#                          "peril_zone": rng.choice(["Z1", "Z2", "Z3"]),
#                          "building": building, "contents": 0.3 * building, "bi": 0.15 * building,
#                          "deductible": float(rng.choice([0, 5e4, 2.5e5])),
#                          "location_limit": float(rng.choice([np.nan, 3e6, 1e7])),
#                          "attachment": attachment, "policy_limit": policy_limit, "share": share})
#             loc += 1
#     return pd.DataFrame(rows)
#
#
# def synthetic_broker_file(n_rows: int = 200, seed: int = 4) -> dict[str, pd.DataFrame]:
#     """A messy broker SOV (headers as brokers write them, deliberate errors)."""
#     rng = np.random.default_rng(seed)
#     tiv = rng.lognormal(np.log(3e6), 1.0, n_rows).round(0)
#     df = pd.DataFrame({
#         "Loc No ": np.arange(1, n_rows + 1),
#         "Street Address": [f"{i} Example St" for i in range(n_rows)],
#         "Country": rng.choice(["AU", "Aus ", "australia", "NZ", "NZL"], n_rows),
#         "Lat": rng.uniform(-44, -12, n_rows).round(5),
#         "Long": rng.uniform(113, 178, n_rows).round(5),
#         "Total Insured Value": tiv.astype(object),
#         "Year Built": rng.integers(1900, 2024, n_rows).astype(object),
#         "Construction": rng.choice(["Masonry", "Timber", "Steel", "Concrete"], n_rows),
#         "No. of Storeys": rng.integers(1, 30, n_rows),
#     })
#     bad = rng.choice(n_rows, 12, replace=False)
#     df.loc[bad[0:3], "Total Insured Value"] = np.nan
#     df.loc[bad[3], "Total Insured Value"] = "n/a"
#     df.loc[bad[4:6], "Lat"] = 95.0
#     df.loc[bad[6], "Year Built"] = 2090
#     df.loc[bad[7], "Construction"] = "Straw"
#     df.loc[bad[8], "Loc No "] = df.loc[bad[9], "Loc No "]          # duplicate id
#     return {"Locations": df}
# @@FILE src/qbecat/trace.py 14f3cc47ccb3fec5d57867def068708cf79e26b4f9efc2d9ebfba9e9d25010f0
# """
# Step-by-step pipelines you can inspect.
#
# Why this exists
# ---------------
# A long stored procedure fails (or gives a wrong number) as one block, and
# you debug it by commenting out half of it. Here every calculation is a list
# of small, named steps. After a run you can:
#
#     pipe.trace                 # one row per step: rows in/out, seconds, new columns, control totals
#     pipe.outputs["step"]       # exactly what a step produced
#     pipe.follow(policy_id=42)  # one policy/account/location through every step
#     pipe.run(data, stop_after="step")   # run only up to a step
#     pipe.rerun("step", **overrides)     # re-run ONE step on its stored inputs
#     pipe.dump("debug.xlsx")    # every step's output, one sheet each
#     pipe.describe()            # the steps and what each does (like an SP outline)
#
# Rules for step functions (keep them and debugging stays easy)
# -------------------------------------------------------------
# 1. Take inputs as arguments, return a NEW object. Never modify an input in place.
# 2. One job per step; name it after what it produces.
# 3. Put a one-line docstring on it: `describe()` prints it.
#
# How a step gets its arguments
# -----------------------------
# For each parameter of the step function, in this order:
#   1. a fixed value given when the step was declared:  step(f, cap=0.5)
#   2. a renamed context entry:                         step(f, use={"elt": "group_elt"})
#   3. a context entry with the same name (inputs passed to run(), or the
#      output of an earlier step, stored under the step's name)
#   4. for the FIRST parameter only: the previous step's output
#   5. the parameter's default value
# Anything else is an error that names the missing input and lists what exists.
# """
#
# from __future__ import annotations
#
# import dataclasses
# import inspect
# import logging
# import time
# from dataclasses import dataclass, field
# from pathlib import Path
# from typing import Any, Callable, Iterable
#
# import numpy as np
# import pandas as pd
#
# log = logging.getLogger(__name__)
#
# _MISSING = object()
#
#
# class StepError(RuntimeError):
#     """A step raised. Outputs of all earlier steps are still on the pipeline."""
#
#
# class StepCheckError(StepError):
#     """A step ran but its check found a problem in what it produced."""
#
#
# @dataclass
# class Step:
#     func: Callable
#     name: str
#     use: dict = field(default_factory=dict)
#     kwargs: dict = field(default_factory=dict)
#     check: Callable | None = None
#
#     @property
#     def doc(self) -> str:
#         text = (self.func.__doc__ or "").strip()
#         return text.splitlines()[0] if text else ""
#
#
# def step(func: Callable, name: str | None = None, *, use: dict | None = None,
#          check: Callable | None = None, **kwargs) -> Step:
#     """
#     Declare one pipeline step.
#
#     check: optional function(result) -> list of problem strings (empty = fine).
#            If it returns anything, the run stops at this step with StepCheckError.
#     """
#     return Step(func, name or func.__name__, dict(use or {}), kwargs, check)
#
#
# # ---------------------------------------------------------------------------
# # helpers to look inside whatever a step returned
# # ---------------------------------------------------------------------------
# def _frames(obj, label="") -> Iterable[tuple[str, pd.DataFrame]]:
#     """Yield (label, DataFrame) for a frame, a dict of frames, or a dataclass of frames."""
#     if isinstance(obj, pd.DataFrame):
#         yield label, obj
#     elif isinstance(obj, pd.Series):
#         yield label, obj.to_frame()
#     elif isinstance(obj, dict):
#         for k, v in obj.items():
#             if isinstance(v, (pd.DataFrame, pd.Series)):
#                 yield from _frames(v, f"{label}.{k}" if label else str(k))
#     elif dataclasses.is_dataclass(obj) and not isinstance(obj, type):
#         for f in dataclasses.fields(obj):
#             v = getattr(obj, f.name)
#             if isinstance(v, (pd.DataFrame, pd.Series, dict)):
#                 yield from _frames(v, f"{label}.{f.name}" if label else f.name)
#
#
# def _size(obj) -> int | None:
#     frames = list(_frames(obj))
#     return sum(len(df) for _, df in frames) if frames else None
#
#
# def _brief(obj) -> str:
#     if isinstance(obj, (pd.DataFrame, pd.Series)):
#         return f"{type(obj).__name__}[{len(obj):,} rows]"
#     if isinstance(obj, (int, float, np.number)):
#         return f"{obj:,.6g}"
#     frames = list(_frames(obj))
#     if frames:
#         return f"{type(obj).__name__}(" + ", ".join(f"{k}={len(v):,}" for k, v in frames) + ")"
#     return type(obj).__name__
#
#
# class Pipeline:
#     """An ordered list of named steps with a full record of every run."""
#
#     def __init__(self, name: str, steps: list[Step], watch: Iterable[str] = ()):
#         names = [s.name for s in steps]
#         dupes = {n for n in names if names.count(n) > 1}
#         if dupes:
#             raise ValueError(f"pipeline '{name}': duplicate step names {sorted(dupes)}")
#         self.name = name
#         self.steps = list(steps)
#         self.watch = list(watch)       # columns whose totals are recorded after every step
#         self.outputs: dict[str, Any] = {}
#         self.inputs: dict[str, dict] = {}
#         self.context: dict[str, Any] = {}
#         self.trace = pd.DataFrame()
#
#     # ----------------------------------------------------------------- run
#     def run(self, data=_MISSING, *, stop_after: str | None = None,
#             keep: bool = True, **context):
#         """
#         Run the steps in order. `data` feeds the first step; keyword arguments
#         become named inputs any step can ask for by parameter name.
#         Returns the output of the last step that ran.
#         """
#         if stop_after is not None and stop_after not in self.step_names:
#             raise ValueError(f"stop_after='{stop_after}' is not a step; steps: {self.step_names}")
#         ctx = dict(context)
#         last = data
#         rows = []
#         self.outputs, self.inputs = {}, {}
#         try:
#             for s in self.steps:
#                 args = self._arguments(s, ctx, last)
#                 t0 = time.perf_counter()
#                 try:
#                     result = s.func(**args)
#                 except Exception as exc:
#                     raise StepError(
#                         f"pipeline '{self.name}' failed at step '{s.name}': "
#                         f"{type(exc).__name__}: {exc}\n"
#                         f"  inputs: {', '.join(f'{k}={_brief(v)}' for k, v in args.items())}\n"
#                         f"  outputs of earlier steps are in pipeline.outputs; "
#                         f"its inputs are in pipeline.inputs['{s.name}']"
#                     ) from exc
#                 seconds = time.perf_counter() - t0
#                 if keep:
#                     self.outputs[s.name] = result
#                     self.inputs[s.name] = args
#                 rows.append(self._record(s, args, result, seconds))
#                 log.info("%s | %-28s %8.2fs  %s", self.name, s.name, seconds, _brief(result))
#                 if s.check is not None:
#                     problems = list(s.check(result) or [])
#                     rows[-1]["check"] = "FAIL" if problems else "ok"
#                     if problems:
#                         raise StepCheckError(
#                             f"pipeline '{self.name}', step '{s.name}': check failed:\n  - "
#                             + "\n  - ".join(problems))
#                 ctx[s.name] = result
#                 last = result
#                 if s.name == stop_after:
#                     break
#         finally:
#             self.trace = pd.DataFrame(rows)
#             self.context = ctx
#         return last
#
#     def _arguments(self, s: Step, ctx: dict, last) -> dict:
#         sig = inspect.signature(s.func)
#         args = {}
#         params = [p for p in sig.parameters.values()
#                   if p.kind in (p.POSITIONAL_OR_KEYWORD, p.KEYWORD_ONLY)]
#         for i, p in enumerate(params):
#             if p.name in s.kwargs:
#                 args[p.name] = s.kwargs[p.name]
#             elif p.name in s.use:
#                 key = s.use[p.name]
#                 if key not in ctx:
#                     raise StepError(f"step '{s.name}': use={{'{p.name}': '{key}'}} but "
#                                     f"'{key}' is not available; available: {sorted(ctx)}")
#                 args[p.name] = ctx[key]
#             elif p.name in ctx:
#                 args[p.name] = ctx[p.name]
#             elif i == 0 and last is not _MISSING:
#                 args[p.name] = last
#             elif p.default is not p.empty:
#                 continue
#             else:
#                 raise StepError(
#                     f"step '{s.name}' needs an input called '{p.name}' that nobody provided.\n"
#                     f"  available inputs: {sorted(ctx)}\n"
#                     f"  fix: pass {p.name}=... to run(), or declare step(..., use={{'{p.name}': '<name>'}})")
#         unknown = set(s.kwargs) - {p.name for p in params}
#         if unknown and not any(p.kind == p.VAR_KEYWORD for p in sig.parameters.values()):
#             raise StepError(f"step '{s.name}': {sorted(unknown)} are not parameters of "
#                             f"{s.func.__name__}{sig}")
#         return args
#
#     def _record(self, s: Step, args: dict, result, seconds: float) -> dict:
#         first_in = next(iter(args.values()), None)
#         row = {"step": s.name, "seconds": round(seconds, 3),
#                "rows_in": _size(first_in), "rows_out": _size(result)}
#         if isinstance(result, pd.DataFrame):
#             before = set(first_in.columns) if isinstance(first_in, pd.DataFrame) else set()
#             row["new_columns"] = ", ".join(c for c in result.columns if c not in before)
#             for col in self.watch:
#                 if col in result.columns and pd.api.types.is_numeric_dtype(result[col]):
#                     row[f"total_{col}"] = float(result[col].sum())
#         else:
#             row["new_columns"] = ""
#             row["result"] = _brief(result)
#         return row
#
#     # ------------------------------------------------------------ inspect
#     @property
#     def step_names(self) -> list[str]:
#         return [s.name for s in self.steps]
#
#     def describe(self) -> pd.DataFrame:
#         """The steps in order, with each step's one-line docstring."""
#         return pd.DataFrame({"step": [s.name for s in self.steps],
#                              "function": [f"{s.func.__module__}.{s.func.__name__}" for s in self.steps],
#                              "does": [s.doc for s in self.steps]})
#
#     def follow(self, changes_only: bool = False, **filters) -> pd.DataFrame:
#         """
#         Rows matching filters (e.g. policy_id=42) in every step output that has
#         those columns, stacked with a 'step' column. The quickest way to see
#         where one record's number changes. changes_only=True drops rows that
#         are identical to how the record looked at an earlier step.
#         """
#         if not filters:
#             raise ValueError("give at least one filter, e.g. follow(policy_id=42)")
#         pieces = []
#         for name, out in self.outputs.items():
#             for label, df in _frames(out, name):
#                 if all(c in df.columns for c in filters):
#                     mask = np.ones(len(df), dtype=bool)
#                     for col, val in filters.items():
#                         vals = val if isinstance(val, (list, tuple, set)) else [val]
#                         mask &= df[col].isin(vals).to_numpy()
#                     if mask.any():
#                         pieces.append(df.loc[mask].assign(step=label))
#         if not pieces:
#             return pd.DataFrame(columns=["step", *filters])
#         out = pd.concat(pieces, ignore_index=True)
#         out = out[["step"] + [c for c in out.columns if c != "step"]]
#         if changes_only:
#             part = out["step"].str.split(".", n=1).str[1].fillna("")
#             same = out.drop(columns="step").astype(str).assign(_part=part.to_numpy()).duplicated()
#             out = out.loc[~same.to_numpy()].reset_index(drop=True)
#         return out
#
#     def rerun(self, name: str, **overrides):
#         """Re-run one step on the inputs it received last time (after editing its code, say)."""
#         if name not in self.inputs:
#             raise KeyError(f"no stored inputs for '{name}' (did the run reach it with keep=True?)")
#         s = self.steps[self.step_names.index(name)]
#         return s.func(**{**self.inputs[name], **overrides})
#
#     def dump(self, path, max_rows: int = 100_000) -> Path:
#         """Write the trace and every step's output to one Excel file (sheet per step)."""
#         path = Path(path)
#         path.parent.mkdir(parents=True, exist_ok=True)
#         used = set()
#         with pd.ExcelWriter(path) as xl:
#             self.trace.to_excel(xl, sheet_name="trace", index=False)
#             for name, out in self.outputs.items():
#                 for label, df in _frames(out, name):
#                     sheet = label.replace(".", "_")[:31]
#                     i = 1
#                     while sheet in used:
#                         sheet = f"{label[:28]}_{i}"; i += 1
#                     used.add(sheet)
#                     df.head(max_rows).to_excel(xl, sheet_name=sheet, index=False)
#         log.info("%s: debug dump written to %s", self.name, path)
#         return path
#
#     def __repr__(self):
#         return f"Pipeline('{self.name}', steps={self.step_names})"
# @@FILE src/qbecat/utils.py 742d9738eb828e36198962e80b11a86214ba91be7157484f8757d2ecbb4b1b3a
# """
# Small helpers used by several modules. Keep this file small: a helper that
# belongs to one area (EP, financial terms, ...) goes in that module instead.
# """
#
# from __future__ import annotations
#
# import logging
# from typing import Iterator
#
# import numpy as np
# import pandas as pd
#
# log = logging.getLogger(__name__)
#
#
# # --------------------------------------------------------------- return periods
# def rp_to_prob(return_period, poisson: bool = False):
#     """Annual exceedance probability. Simple: 1/RP. Poisson: 1 - exp(-1/RP)."""
#     rp = np.asarray(return_period, dtype=float)
#     if np.any(rp <= 0):
#         raise ValueError("return periods must be positive")
#     return 1 - np.exp(-1 / rp) if poisson else 1 / rp
#
#
# def prob_to_rp(prob, poisson: bool = False):
#     """Return period from annual exceedance probability (inverse of rp_to_prob)."""
#     p = np.asarray(prob, dtype=float)
#     if np.any((p <= 0) | (p >= 1)):
#         raise ValueError("probabilities must be in (0, 1)")
#     return -1 / np.log(1 - p) if poisson else 1 / p
#
#
# def target_rank(n_years: int, return_period: float) -> int:
#     """Rank (1 = worst year) read for a return period: round(n_years / RP)."""
#     k = int(round(n_years / return_period))
#     if k < 1:
#         raise ValueError(f"return period {return_period} is beyond what {n_years:,} years can resolve")
#     return k
#
#
# # --------------------------------------------------------------- currency
# def convert_currency(df: pd.DataFrame, columns: list[str], fx: pd.DataFrame,
#                      currency_col: str = "currency", to: str = "AUD") -> pd.DataFrame:
#     """
#     Convert money columns to one currency. fx has columns currency, rate where
#     1 unit of `currency` = rate units of `to`. Unknown currencies raise
#     (never silently left unconverted).
#     """
#     rates = fx.set_index("currency")["rate"].to_dict()
#     rates.setdefault(to, 1.0)
#     unknown = sorted(set(df[currency_col].dropna()) - set(rates))
#     if unknown:
#         raise ValueError(f"no FX rate for {unknown}; fx table has {sorted(rates)}")
#     factor = df[currency_col].map(rates)
#     out = df.assign(**{c: df[c] * factor for c in columns})
#     out[currency_col] = to
#     log.info("converted %s to %s using %d rates", columns, to, len(rates))
#     return out
#
#
# # --------------------------------------------------------------- chunking
# def chunks_by(df: pd.DataFrame, column: str, size: int) -> Iterator[pd.DataFrame]:
#     """
#     Yield pieces of df holding at most `size` distinct values of `column`
#     (a value is never split across pieces). Use to process years or events
#     in memory-bounded batches; combine per-year results, never quantiles.
#     """
#     values = df[column].unique()
#     for start in range(0, len(values), size):
#         yield df[df[column].isin(values[start:start + size])]
# @@FILE tests/conftest.py ad97af4d667bf874e4dbcfa6a08253b5a55787b9dc9ac780f286bad5052bef43
# import pytest
#
# from qbecat.simulation import (synthetic_accounts, synthetic_elt, synthetic_exposure,
#                                synthetic_occurrences)
#
# N_YEARS = 40_000
#
#
# @pytest.fixture(scope="session")
# def n_years():
#     return N_YEARS
#
#
# @pytest.fixture(scope="session")
# def group_elt():
#     return synthetic_elt(200, seed=0)
#
#
# @pytest.fixture(scope="session")
# def occurrences(group_elt):
#     return synthetic_occurrences(group_elt, N_YEARS, seed=1)
#
#
# @pytest.fixture(scope="session")
# def account_elts(group_elt):
#     return synthetic_accounts(group_elt, 25, seed=2)
#
#
# @pytest.fixture(scope="session")
# def exposure():
#     return synthetic_exposure(40, seed=3)
# @@FILE tests/mi_v3_reference.py 6c96c3eea8db60aeee430cc769b8135880fc23a36b8a60cac986403ac0169b0c
# """
# The original mi_v3 notebook logic (globals and all), kept only as a test
# oracle: the library's marginal module must reproduce it. Column names are
# mapped from the canonical ones to the notebook's upper-case ones on entry.
# """
#
# import numpy as np
# import pandas as pd
# from scipy.special import betaincinv
#
# OCC = ["SIMID", "EVENTID", "INSTANCEID"]
#
#
# def run(group_elt, account_elts, occurrences, n_sims, return_period=200, spreads=(0.10, 0.20)):
#     up = {"mean_loss": "PERSPVALUE", "sd_i": "STDDEVI", "sd_c": "STDDEVC", "exposure": "EXPVALUE",
#           "event_id": "VENDOREVENTID", "account_id": "ID"}
#     group_elt = group_elt.rename(columns=up)
#     account_elts = account_elts.rename(columns=up)
#     occurrences = occurrences.rename(columns={"year": "SIMID", "sim_event_id": "EVENTID",
#                                               "instance_id": "INSTANCEID", "quantile": "LOSSQUANTILE",
#                                               "event_id": "VENDOREVENTID"})
#
#     def beta_parameters(mean, stdi, stdc, exposure):
#         mu = np.clip(mean / exposure, 1e-9, 1 - 1e-9)
#         var = np.clip(((stdi + stdc) / exposure) ** 2, 1e-12, mu * (1 - mu) * (1 - 1e-6))
#         common = mu * (1 - mu) / var - 1
#         return mu * common, (1 - mu) * common
#
#     def occurrence_losses(elt, occurrences, by=()):
#         rows = occurrences.merge(elt, on="VENDOREVENTID")
#         a, b = beta_parameters(rows["PERSPVALUE"].to_numpy(), rows["STDDEVI"].to_numpy(),
#                                rows["STDDEVC"].to_numpy(), rows["EXPVALUE"].to_numpy())
#         rows["Loss"] = rows["EXPVALUE"].to_numpy() * betaincinv(a, b, rows["LOSSQUANTILE"].to_numpy())
#         return rows.groupby(list(by) + OCC, as_index=False)["Loss"].sum()
#
#     def nth_largest(values, n):
#         values = np.asarray(values, dtype=float)
#         if len(values) < n:
#             return 0.0
#         return float(np.partition(values, len(values) - n)[len(values) - n])
#
#     TARGET_RANK = round(n_sims / return_period)
#     group_losses = occurrence_losses(group_elt, occurrences)
#     largest = group_losses.groupby("SIMID")["Loss"].idxmax()
#     years = (group_losses.loc[largest, OCC + ["Loss"]].rename(columns={"Loss": "OEP"})
#              .sort_values("OEP", ascending=False).reset_index(drop=True))
#     years["Rank"] = np.arange(1, len(years) + 1)
#     GROUP_RP = nth_largest(years["OEP"], TARGET_RANK)
#
#     def account_contributions(K):
#         window_years = years.loc[years["Rank"] <= K, "SIMID"]
#         window_occ = group_losses[group_losses["SIMID"].isin(window_years)].rename(columns={"Loss": "GroupLoss"})
#         acct = occurrence_losses(account_elts, occurrences[occurrences["SIMID"].isin(window_years)], by=["ID"])
#         acct = acct.merge(window_occ, on=OCC)
#         scale = np.minimum(1.0, acct["GroupLoss"] / acct.groupby(OCC)["Loss"].transform("sum"))
#         acct["Contribution"] = acct["Loss"] * scale
#         return acct[["ID"] + OCC + ["Contribution"]], window_occ
#
#     def rank_kernels(K):
#         ranks = np.arange(1, K + 1)
#         kernels = {}
#         for f in spreads:
#             spread = f * TARGET_RANK
#             w = np.exp(-0.5 * ((ranks - TARGET_RANK) / spread) ** 2)
#             w[np.abs(ranks - TARGET_RANK) > 3 * spread] = 0.0
#             kernels[f"last_in_smoothed_{round(spread)}"] = w / w.sum()
#         return kernels
#
#     def last_in_for_window(contributions, window_occ, K, account_ids):
#         K = min(K, len(years))
#         base_oep = years.loc[years["Rank"] <= K].set_index("SIMID")["OEP"]
#         base_sorted = years["OEP"].to_numpy()[:K]
#         outside_max = years["OEP"].iloc[K] if len(years) > K else 0.0
#         deepest = min(K, round(TARGET_RANK * (1 + 3 * max(spreads))))
#         kernels = rank_kernels(K)
#         occ_by_year = window_occ.set_index("SIMID")
#         by_account = dict(tuple(contributions.groupby("ID")))
#         results = []
#         for account_id in account_ids:
#             contrib = by_account.get(account_id)
#             if contrib is None:
#                 new_sorted = base_sorted
#             else:
#                 touched = contrib["SIMID"].unique()
#                 occ = occ_by_year.loc[touched].reset_index().merge(contrib[OCC + ["Contribution"]], on=OCC, how="left")
#                 occ["NetLoss"] = occ["GroupLoss"] - occ["Contribution"].fillna(0.0)
#                 oep = base_oep.copy()
#                 oep.loc[touched] = occ.groupby("SIMID")["NetLoss"].max()
#                 new_sorted = np.sort(oep.to_numpy())[::-1]
#             row = {"account_id": account_id, "last_in_marginal": GROUP_RP - new_sorted[TARGET_RANK - 1],
#                    "last_in_exact": bool(new_sorted[deepest - 1] >= outside_max)}
#             for name, w in kernels.items():
#                 row[name] = float(w @ (base_sorted - new_sorted))
#             results.append(row)
#         return pd.DataFrame(results)
#
#     K = round(TARGET_RANK * (1 + 3 * max(spreads)))
#     contributions, window_occ = account_contributions(K)
#     pending, finished = list(account_elts["ID"].unique()), []
#     while pending:
#         result = last_in_for_window(contributions, window_occ, K, pending)
#         finished.append(result[result["last_in_exact"]])
#         pending = list(result.loc[~result["last_in_exact"], "account_id"])
#         if pending and K >= len(years):
#             finished.append(result[~result["last_in_exact"]].assign(last_in_exact=True))
#             break
#         if pending:
#             K *= 2
#             contributions, window_occ = account_contributions(K)
#     last_in = pd.concat(finished, ignore_index=True)
#
#     # allocation (co-TVaR and kernel co-VaR) at the initial window
#     contributions, _ = account_contributions(round(TARGET_RANK * (1 + 3 * max(spreads))))
#     defining = contributions.merge(years[OCC], on=OCC)
#     ranks = years.set_index("SIMID")["Rank"]
#     weights = {"co_tvar": (ranks <= TARGET_RANK).astype(float)}
#     for f in spreads:
#         spread = f * TARGET_RANK
#         w = np.exp(-0.5 * ((ranks - TARGET_RANK) / spread) ** 2)
#         w[(ranks - TARGET_RANK).abs() > 3 * spread] = 0.0
#         weights[f"kernel_co_var_{round(spread)}"] = w
#     shares = []
#     for name, w in weights.items():
#         w = (w / w.sum())[w > 0]
#         shares.append((defining["SIMID"].map(w).fillna(0.0) * defining["Contribution"])
#                       .groupby(defining["ID"]).sum().rename(name))
#     alloc = pd.concat(shares, axis=1).rename_axis("account_id").reset_index()
#     return last_in.merge(alloc, on="account_id", how="left").fillna(0.0), GROUP_RP
# @@FILE tests/test_cleansing.py d6bac861028295db92e20d129dea7492e4c160ea99f0c269957725f9a76c35dd
# import json
#
# import numpy as np
# import pandas as pd
# import pytest
#
# from qbecat.cleansing import RULES, load_division, rule, run_cleansing
# from qbecat.simulation import synthetic_broker_file
#
#
# def clean_file():
#     df = pd.DataFrame({"Loc No": [1, 2, 3], "Country": ["AU", "Aus ", "NZ"],
#                        "Lat": [-33.9, -37.8, -41.3], "Long": [151.2, 144.9, 174.8],
#                        "Total Insured Value": ["1,000,000", "2000000", "500000"],
#                        "Year Built": [1990, np.nan, 2001], "Construction": ["Masonry", "timber", "Steel"]})
#     return {"Locations": df}
#
#
# @pytest.fixture
# def eo():
#     return load_division("EO")
#
#
# def test_division_extends_base(eo):
#     assert eo["division"] == "EO"
#     assert eo["thresholds"]["tiv_max"] == 1.5e9                  # EO override
#     assert eo["thresholds"]["stories_max"] == 150                # inherited from base
#     assert "location_id" in eo["tables"]["locations"]["columns"]
#
#
# def test_clean_file_exports_with_gated_fixes_and_sentinels(eo, tmp_path):
#     state, pipe = run_cleansing(clean_file(), eo, out_dir=tmp_path, stem="t")
#     assert state.blocked == {}
#     out = state.exports["Locations"]
#     assert out["CNTRYCODE"].tolist() == ["AU", "AU", "NZ"]          # alias fixed (allowlisted)
#     assert out["CONSTRUCTION"].tolist() == ["Masonry", "Timber", "Steel"]
#     assert out["TIV"].tolist() == [1e6, 2e6, 5e5]                   # thousand separators parsed
#     assert out["YEARBUILT"].tolist() == [1990, 0, 2001]             # sentinel at export only
#     # validation never saw the sentinel: no year_built finding for the blank row
#     assert not (state.findings["rule"] == "year_built_range").any()
#     for suffix in ("exceptions.xlsx", "audit.jsonl", "mapping.json", "rms.xlsx"):
#         assert (tmp_path / f"t_{suffix}").exists()
#     events = [json.loads(l) for l in (tmp_path / "t_audit.jsonl").read_text().splitlines()]
#     fixes = [e for e in events if e["action"] == "autofix"]
#     assert {(e["old"], e["new"]) for e in fixes} == {("Aus ", "AU"), ("timber", "Timber")}
#
#
# def test_autofix_needs_both_gates(eo):
#     cfg = {**eo, "autofix_allowlist": []}                          # gate 2 closed
#     state, _ = run_cleansing(clean_file(), cfg)
#     assert state.tables["locations"]["country"].tolist() == ["AU", "Aus ", "NZ"]
#     assert (state.findings.query("rule == 'country_code'")["status"] == "open").all()
#
#
# def test_rules_cannot_change_data(eo):
#     before = clean_file()["Locations"].copy()
#
#     @rule("_test_vandal", table="locations", column="country", severity="INFO")
#     def vandal(df, cfg):
#         df["country"] = "XX"                                       # tries to write
#         return df["country"] == "XX"
#     try:
#         state, pipe = run_cleansing(clean_file(), eo)
#         assert state.tables["locations"]["country"].tolist()[0] == "AU"
#         assert pipe.outputs["evaluate"].tables["locations"]["country"].tolist() == \
#                pipe.outputs["normalise"].tables["locations"]["country"].tolist()
#     finally:
#         RULES.pop("_test_vandal")
#     assert before.equals(clean_file()["Locations"])
#
#
# def test_critical_blocks_only_its_table(eo):
#     cfg = {**eo, "tables": {**eo["tables"], "policies": {
#         "sheet_names": ["Policies"], "columns": {"policy_id": ["policy"]}, "required": ["policy_id"]}},
#         "export": {**eo["export"], "policies": {"sheet": "Policies"}}}
#     src = clean_file()
#     src["Locations"].loc[0, "Total Insured Value"] = None          # CRITICAL on locations
#     src["Policies"] = pd.DataFrame({"Policy": [10, 20]})
#     state, _ = run_cleansing(src, cfg)
#     assert "locations" in state.blocked and "tiv_missing" in state.blocked["locations"]
#     assert "Policies" in state.exports and "Locations" not in state.exports
#
#
# def test_crashing_rule_is_reported_not_swallowed(eo):
#     @rule("_test_crash", table="locations", column="country", severity="INFO")
#     def crash(df, cfg):
#         raise RuntimeError("oops")
#     try:
#         state, _ = run_cleansing(clean_file(), eo)
#     finally:
#         RULES.pop("_test_crash")
#     f = state.findings.query("rule == '_test_crash'")
#     assert f["severity"].tolist() == ["CRITICAL"] and "oops" in f["message"].iloc[0]
#     assert "locations" in state.blocked
#
#
# def test_messy_broker_file_end_to_end(eo):
#     state, pipe = run_cleansing(synthetic_broker_file(), eo)
#     rules = set(state.findings["rule"])
#     assert {"tiv_missing", "not_numeric", "latitude_range", "duplicate_location_id",
#             "year_built_range", "construction_code"} <= rules
#     row = int(state.findings.query("rule == 'not_numeric'")["_row"].iloc[0])
#     trail = pipe.follow(_row=row, changes_only=True)
#     assert "evaluate.findings" in set(trail["step"]) or "normalise.findings" in set(trail["step"])
# @@FILE tests/test_core.py 5f88ad89fce07d80a6590e3a15a5cea403ed7821c36e50676dc690be41516625
# """schema, severity, simulation, EP, utils."""
#
# import numpy as np
# import pandas as pd
# import pytest
#
# from qbecat import ep, utils
# from qbecat.schema import SchemaError, problems, to_canonical, validate
# from qbecat.simulation import add_beta_parameters, occurrence_losses, year_losses
#
#
# # ------------------------------------------------------------------ schema
# def test_schema_reports_every_problem_with_rows(group_elt):
#     bad = group_elt.copy()
#     bad.loc[3, "mean_loss"] = bad.loc[3, "exposure"] * 2
#     bad.loc[7, "sd_i"] = -1
#     found = problems(bad, "elt")
#     assert any("mean_loss > exposure" in p and "index 3" in p for p in found)
#     assert any("sd_i < 0" in p and "index 7" in p for p in found)
#     with pytest.raises(SchemaError):
#         validate(bad, "elt")
#
#
# def test_schema_duplicates_and_missing_columns(group_elt):
#     dup = pd.concat([group_elt, group_elt.head(1)])
#     assert any("duplicate key" in p for p in problems(dup, "elt"))
#     assert "missing required columns" in problems(group_elt.drop(columns="sd_c"), "elt")[0]
#
#
# def test_to_canonical_is_case_and_space_insensitive():
#     raw = pd.DataFrame({" EVENTID": [1], "PerspValue": ["5"], "StdDevI": [1], "StdDevC": [1],
#                         "ExpValue": [10], "junk": [0]})
#     out = to_canonical(raw, {"event_id": "eventid", "mean_loss": "perspvalue", "sd_i": "stddevi",
#                              "sd_c": "stddevc", "exposure": "expvalue"}, "elt")
#     assert list(out.columns) == ["event_id", "mean_loss", "sd_i", "sd_c", "exposure"]
#     assert out["mean_loss"].dtype.kind == "f"
#
#
# # ---------------------------------------------------------------- severity
# def test_beta_moments_and_flags():
#     elt = pd.DataFrame({"event_id": [1, 2, 3, 4], "mean_loss": [10, 10, 0, 50],
#                         "sd_i": [5, 0, 1, 40], "sd_c": [5, 0, 0, 40], "exposure": [100, 100, 100, 100]})
#     s = add_beta_parameters(elt)
#     assert np.isclose(s.alpha[0] / (s.alpha[0] + s.beta[0]), 0.1)            # mean preserved
#     var = s.alpha[0] * s.beta[0] / ((s.alpha[0] + s.beta[0]) ** 2 * (s.alpha[0] + s.beta[0] + 1))
#     assert np.isclose(np.sqrt(var), 0.10)                                     # sd = (5+5)/100
#     assert s.degenerate.tolist() == [False, True, True, False]
#     assert s.repaired.tolist() == [False, False, False, True]                 # 0.8^2 > 0.25
#     with pytest.raises(ValueError, match="too large"):
#         add_beta_parameters(elt, repair="raise")
#
#
# # -------------------------------------------------------------- simulation
# def test_simulated_aal_matches_analytic(group_elt, occurrences, n_years):
#     yl = year_losses(occurrence_losses(group_elt, occurrences))
#     sim = ep.aal(yl["aep"], n_years)
#     # standard error of the AAL estimate from the simulated years themselves
#     se = np.sqrt(np.var(np.r_[yl["aep"], np.zeros(n_years - len(yl))]) / n_years)
#     assert abs(sim - ep.analytic_aal(group_elt)) < 4 * se
#
#
# def test_analytic_oep_matches_simulated(group_elt, occurrences, n_years):
#     yl = year_losses(occurrence_losses(group_elt, occurrences))
#     rps = [10, 50, 100]
#     sim = ep.loss_at_rp(yl["oep"], n_years, rps)
#     ana = ep.analytic_loss_at_rp(group_elt, rps)
#     assert np.allclose(sim, ana, rtol=0.04)
#
#
# def test_chunked_equals_unchunked(group_elt, occurrences):
#     a = occurrence_losses(group_elt, occurrences).sort_values(["year", "sim_event_id", "instance_id"])
#     b = occurrence_losses(group_elt, occurrences, chunk_years=3_000).sort_values(["year", "sim_event_id", "instance_id"])
#     assert np.allclose(a["loss"].to_numpy(), b["loss"].to_numpy())
#
#
# def test_common_random_numbers(group_elt, account_elts, occurrences):
#     """Accounts and group read the same quantile per occurrence: the same events hit both."""
#     g = occurrence_losses(group_elt, occurrences)
#     a = occurrence_losses(account_elts, occurrences, by=["account_id"])
#     key = ["year", "sim_event_id", "instance_id"]
#     assert set(map(tuple, a[key].drop_duplicates().to_numpy())) <= set(map(tuple, g[key].to_numpy()))
#
#
# # ---------------------------------------------------------------------- EP
# def test_rank_convention_and_zero_years():
#     values = [100, 90, 80]                      # 3 years with loss out of 10
#     assert ep.loss_at_rp(values, 10, [10, 5, 2])[0] == 100        # rank 1
#     assert ep.loss_at_rp(values, 10, [5])[0] == 90                # rank 2
#     assert ep.loss_at_rp(values, 10, [2])[0] == 0                 # rank 5 is an empty year
#     assert np.isnan(ep.loss_at_rp(values, 10, [100])[0])          # beyond the simulation
#     assert ep.tvar(values, 10, [5])[0] == 95
#     assert ep.aal(values, 10) == 27
#     assert ep.loss_at_rp(values, 10, [10 / 1.5], method="interpolate")[0] == 95
#     with pytest.raises(ValueError, match="n_years"):
#         ep.loss_at_rp(values, 2, [1])
#
#
# def test_ep_table(group_elt, occurrences, n_years):
#     t = ep.ep_table(year_losses(occurrence_losses(group_elt, occurrences)), n_years, [10, 100])
#     assert (t["aep"] >= t["oep"]).all() and (t["tvar_oep"] >= t["oep"]).all()
#     assert t.attrs["aal"] > 0
#
#
# def test_return_period_helpers():
#     assert np.isclose(utils.prob_to_rp(utils.rp_to_prob(200, poisson=True), poisson=True), 200)
#     assert utils.target_rank(500_000, 200) == 2500
#     with pytest.raises(ValueError):
#         utils.target_rank(100, 1000)
#
#
# def test_currency_refuses_unknown():
#     df = pd.DataFrame({"currency": ["USD", "AUD"], "loss": [1.0, 1.0]})
#     out = utils.convert_currency(df, ["loss"], pd.DataFrame({"currency": ["USD"], "rate": [1.5]}))
#     assert out["loss"].tolist() == [1.5, 1.0]
#     with pytest.raises(ValueError, match="no FX rate"):
#         utils.convert_currency(df.assign(currency=["EUR", "AUD"]), ["loss"],
#                                pd.DataFrame({"currency": ["USD"], "rate": [1.5]}))
# @@FILE tests/test_financial.py 84a3fedcb0d66204a7aae0774ce8a031f9f42cbebd832d10c83f19d71166ee8d
# import numpy as np
# import pandas as pd
# import pytest
#
# from qbecat.financial import (explain_policy, exposed_limit, exposed_limit_pipeline, layer,
#                               occurrence_layer)
# from qbecat.trace import StepCheckError
#
#
# def test_layer_terms():
#     assert layer([5, 15, 40], attachment=10, limit=20, share=0.5).tolist() == [0, 2.5, 10]
#     assert layer([5], attachment=np.nan, limit=np.nan).tolist() == [5]        # NaN = none / unlimited
#
#
# def test_exposed_limit_hand_calculation():
#     # policy 1: two locations, 1m xs 0.5m, 50% share
#     exp = pd.DataFrame({
#         "location_id": [1, 2, 3], "policy_id": [1, 1, 2], "country": ["AU", "AU", "NZ"],
#         "building": [800_000.0, 600_000.0, 100.0], "contents": [200_000.0, 0, 0], "bi": [0.0, 0, 0],
#         "deductible": [100_000.0, 0, 0], "location_limit": [np.nan, 500_000.0, np.nan],
#         "attachment": [500_000.0, 500_000.0, 0], "policy_limit": [1_000_000.0, 1_000_000.0, np.nan],
#         "share": [0.5, 0.5, 1.0]})
#     summary, pipe = exposed_limit(exp, ["country"])
#     calc = explain_policy(pipe, 1)
#     # loc1: 1.0m - 0.1m = 0.9m ; loc2: min(0.6m, 0.5m) = 0.5m ; policy gross 1.4m
#     assert calc["after_location_limit"].tolist() == [900_000, 500_000]
#     # 0.5 x min(1.4m - 0.5m, 1m) = 450k, split 9:5
#     assert np.isclose(calc["policy_exposed"].iloc[0], 450_000)
#     assert np.allclose(calc["exposed_limit"], [450_000 * 9 / 14, 450_000 * 5 / 14])
#     assert np.isclose(summary.set_index("country").loc["AU", "exposed_limit"], 450_000)
#     assert np.isclose(summary.set_index("country").loc["NZ", "exposed_limit"], 100)
#     assert pipe.trace["check"].dropna().eq("ok").all()
#
#
# def test_a_broken_step_fails_at_that_step(exposure):
#     pipe = exposed_limit_pipeline()
#     # simulate a bug: replace the limit step with one that ignores the deductible
#     bad = pipe.steps[3]
#     bad.func = lambda df: df.assign(after_location_limit=df["tiv"] * 1.1)
#     with pytest.raises(StepCheckError, match="above TIV"):
#         pipe.run(exposure)
#     assert "after_deductible" in pipe.outputs      # everything before the bug is inspectable
#
#
# def test_occurrence_layer_identity():
#     occ = pd.DataFrame({"loss": [0.0, 50.0, 500.0]})
#     out = occurrence_layer(occ, attachment=100, limit=200)
#     assert np.allclose(out["ceded_layer"] + out["net"], out["loss"])
# @@FILE tests/test_io.py 8e232ca072ada655e5877b416dd9805ae15f27a5d3e0f58975b20c4a6adc852d
# import pandas as pd
# import pytest
# from sqlalchemy import create_engine
#
# from qbecat.config import ConfigError, deep_merge
# from qbecat.io import load_group_elt, query_text, show_sql
# from qbecat.io.engines import engine_url
# from qbecat.schema import SchemaError
#
# TABLES = {"group_elt": "GROUP_ELT"}
#
#
# @pytest.fixture
# def db(tmp_path, group_elt):
#     eng = create_engine(f"sqlite:///{tmp_path / 't.db'}")
#     raw = group_elt.rename(columns={"event_id": "VENDOREVENTID", "mean_loss": "PerspValue",
#                                     "sd_i": "StdDevI", "sd_c": "StdDevC", "exposure": "ExpValue"})
#     raw = raw.drop(columns="rate").assign(PortGroupingID=354, HazardZoneGroupingID=352)
#     raw.to_sql("GROUP_ELT", eng, index=False)
#     return eng
#
#
# def test_loader_round_trip_through_a_database(db, group_elt, monkeypatch):
#     import qbecat.io.sql as sql
#     monkeypatch.setattr(sql, "load_settings", lambda: {"tables": TABLES})
#     df = load_group_elt(354, 352, engine=db)
#     assert list(df.columns) == ["event_id", "mean_loss", "sd_i", "sd_c", "exposure"]
#     assert len(df) == len(group_elt)
#     assert load_group_elt(999, 352, engine=db).empty
#
#
# def test_bad_extract_fails_at_the_loader(db, monkeypatch):
#     import qbecat.io.sql as sql
#     monkeypatch.setattr(sql, "load_settings", lambda: {"tables": TABLES})
#     with db.begin() as c:
#         c.exec_driver_sql("UPDATE GROUP_ELT SET StdDevI = -1 WHERE VENDOREVENTID = 5")
#     with pytest.raises(SchemaError, match="sd_i < 0"):
#         load_group_elt(354, 352, engine=db)
#
#
# def test_table_placeholders_are_refused():
#     with pytest.raises(ConfigError, match="placeholder"):
#         query_text("group_elt", {"group_elt": "<GROUP_ELT_TABLE>"})
#     with pytest.raises(ConfigError, match="not a plain table name"):
#         query_text("group_elt", {"group_elt": "x; DROP TABLE y"})
#     with pytest.raises(ConfigError, match="needs table"):
#         query_text("group_elt", {})
#
#
# def test_show_sql_inlines_values_for_ssms():
#     text = show_sql("account_elts", {"rdm_account": "dbo.A", "rdm_account_std": "dbo.S"},
#                     analysis_id=112, persp_code="RL")
#     assert "ra.ANLSID    = 112" in text and "= 'RL'" in text and "dbo.A ra" in text
#
#
# def test_engine_aliases_refuse_placeholders():
#     s = {"engines": {"RMS": {"server": "<RMS_SERVER>", "database": "<RMS_DATABASE>"}}}
#     with pytest.raises(ConfigError, match="fill in"):
#         engine_url("RMS", s)
#     with pytest.raises(ConfigError, match="known aliases"):
#         engine_url("NOPE", s)
#
#
# def test_deep_merge():
#     assert deep_merge({"a": {"x": 1, "y": 2}}, {"a": {"y": 3}}) == {"a": {"x": 1, "y": 3}}
# @@FILE tests/test_marginal.py d32366b81e91a3245ab3f61ae7bbdadcd9ed47d56af36a116e459dc5daadaa71
# import numpy as np
# import pandas as pd
# import pytest
#
# from qbecat.ep import loss_at_rp
# from qbecat.marginal import MarginalSettings, compare_to_reference, run_marginal_impact
# from qbecat.schema import OCC_KEY
# from qbecat.simulation import occurrence_losses
#
# import mi_v3_reference
#
#
# @pytest.fixture(scope="module")
# def result(group_elt, account_elts, occurrences, n_years):
#     return run_marginal_impact(group_elt, account_elts, occurrences, n_years)
#
#
# def test_reproduces_original_notebook(result, group_elt, account_elts, occurrences, n_years):
#     summary, pipe = result
#     ref, ref_rp = mi_v3_reference.run(group_elt, account_elts, occurrences, n_years)
#     assert np.isclose(pipe.outputs["tail"].rp_loss, ref_rp)
#     cols = [c for c in ref.columns if c not in ("account_id", "last_in_exact")]
#     merged = summary.merge(ref, on="account_id", suffixes=("", "_ref"))
#     assert len(merged) == len(ref)
#     for c in cols:
#         assert np.allclose(merged[c], merged[f"{c}_ref"], rtol=1e-6, atol=1e-3), c
#
#
# def test_allocation_adds_up_to_group(result):
#     totals = result[1].outputs["allocations"].totals
#     assert np.allclose(totals["group"], totals["accounts"] + totals["other_business"])
#     assert (totals["other_business"] >= -1e-6).all()
#
#
# def test_last_in_matches_brute_force(result, group_elt, account_elts, occurrences, n_years):
#     """Remove one account from EVERY occurrence of EVERY year, re-rank everything."""
#     summary, pipe = result
#     tail = pipe.outputs["tail"]
#     g = occurrence_losses(group_elt, occurrences)
#     a = occurrence_losses(account_elts, occurrences, by=["account_id"]).merge(
#         g.rename(columns={"loss": "group_loss"}), on=OCC_KEY)
#     total = a.groupby(OCC_KEY)["loss"].transform("sum")
#     a["contribution"] = a["loss"] * np.minimum(1, a["group_loss"] / total)
#     for acc in summary["account_id"].head(5):
#         c = a[a["account_id"] == acc][OCC_KEY + ["contribution"]]
#         net = g.merge(c, on=OCC_KEY, how="left")
#         net["loss"] = net["loss"] - net["contribution"].fillna(0)
#         oep = net.groupby("year")["loss"].max()
#         brute = tail.rp_loss - loss_at_rp(oep, n_years, [200])[0]
#         ours = summary.set_index("account_id").loc[acc, "last_in_marginal"]
#         assert np.isclose(ours, brute, rtol=1e-9, atol=1e-6), acc
#
#
# def test_standalone_matches_ep_engine(result, account_elts, occurrences, n_years):
#     summary, _ = result
#     acc = summary["account_id"].iloc[0]
#     ol = occurrence_losses(account_elts[account_elts["account_id"] == acc], occurrences)
#     oep = ol.groupby("year")["loss"].max()
#     assert np.isclose(summary.set_index("account_id").loc[acc, "standalone"],
#                       loss_at_rp(oep, n_years, [200])[0])
#
#
# def test_reference_comparison_and_fast_mode(group_elt, account_elts, occurrences, n_years):
#     ref = pd.DataFrame({"account_id": account_elts["account_id"].unique()})
#     ref["reference"] = 1e6
#     summary, pipe = run_marginal_impact(group_elt, account_elts, occurrences, n_years, reference=ref,
#                                         settings=MarginalSettings(include_standalone=False))
#     assert "standalone" not in pipe.step_names
#     stats = compare_to_reference(summary)
#     assert "last_in_marginal" in stats.index
#     assert {"last_in_marginal_diff", "co_tvar_diff_pct"} <= set(summary.columns)
# @@FILE tests/test_trace.py 54fde0e45497c5fb2e180cf3b401f52960c47428f0e60cbaf784e7322b7dedbc
# import pandas as pd
# import pytest
#
# from qbecat.trace import Pipeline, StepCheckError, StepError, step
#
#
# def add_one(df):
#     """Add one to x."""
#     return df.assign(x=df["x"] + 1)
#
#
# def double(df, factor=2):
#     """Multiply x."""
#     return df.assign(y=df["x"] * factor)
#
#
# def combine(left, right):
#     return left.merge(right, on="k")
#
#
# def boom(df):
#     raise ZeroDivisionError("bad")
#
#
# @pytest.fixture
# def df():
#     return pd.DataFrame({"k": [1, 2, 3], "x": [1.0, 2.0, 3.0]})
#
#
# def test_linear_run_trace_and_outputs(df):
#     p = Pipeline("t", [step(add_one), step(double, factor=10)], watch=["x"])
#     out = p.run(df)
#     assert out["y"].tolist() == [20, 30, 40]
#     assert p.trace["step"].tolist() == ["add_one", "double"]
#     assert p.trace["total_x"].tolist() == [9.0, 9.0]
#     assert p.trace.loc[1, "new_columns"] == "y"
#     assert df["x"].tolist() == [1.0, 2.0, 3.0]            # input untouched
#
#
# def test_named_inputs_and_use(df):
#     other = pd.DataFrame({"k": [1, 2], "z": [9, 8]})
#     p = Pipeline("t", [step(add_one, "left", use={"df": "a"}), step(combine, use={"right": "b"})])
#     out = p.run(a=df, b=other)
#     assert len(out) == 2 and "z" in out
#
#
# def test_missing_input_error_names_it(df):
#     p = Pipeline("t", [step(combine)])
#     with pytest.raises(StepError, match="needs an input called 'right'"):
#         p.run(df)
#
#
# def test_failure_keeps_earlier_outputs(df):
#     p = Pipeline("t", [step(add_one), step(boom), step(double)])
#     with pytest.raises(StepError, match="failed at step 'boom'"):
#         p.run(df)
#     assert "add_one" in p.outputs and "boom" not in p.outputs
#     assert p.trace["step"].tolist() == ["add_one"]
#
#
# def test_check_stops_run(df):
#     p = Pipeline("t", [step(add_one, check=lambda d: ["x too big"] if d["x"].max() > 3 else []),
#                        step(double)])
#     with pytest.raises(StepCheckError, match="x too big"):
#         p.run(df)
#
#
# def test_stop_after_rerun_follow_dump(df, tmp_path):
#     p = Pipeline("t", [step(add_one), step(double)])
#     p.run(df, stop_after="add_one")
#     assert list(p.outputs) == ["add_one"]
#     p.run(df)
#     assert p.rerun("double", factor=100)["y"].tolist() == [200, 300, 400]
#     f = p.follow(k=2)
#     assert f["step"].tolist() == ["add_one", "double"] and f["x"].tolist() == [3.0, 3.0]
#     assert p.dump(tmp_path / "d.xlsx").exists()
#     assert p.describe()["does"].tolist() == ["Add one to x.", "Multiply x."]
#
#
# def test_unknown_fixed_parameter_is_an_error(df):
#     with pytest.raises(StepError, match="not parameters"):
#         Pipeline("t", [step(add_one, facter=3)]).run(df)
# @@END
