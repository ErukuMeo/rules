# Multi-Client Rules Repository Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a GitHub-ready rules repository that maintains one source rule dataset and generates multi-client rule artifacts for Sub-Store driven subscriptions.

**Architecture:** Source rules live in `source/rules.json` using a small, versioned schema. `scripts/generate_rules.py` validates the source and emits deterministic artifacts under `dist/` for Mihomo, Surge/Loon/Quantumult X style clients, sing-box JSON rule sets, and Sub-Store URL references. GitHub Actions runs validation and generation on every push.

**Tech Stack:** Python 3.11+ standard library, JSON source data, GitHub Actions, generated text/YAML/JSON rule artifacts.

---

### Task 1: Repository Structure and Source Rules

**Files:**
- Create: `source/rules.json`
- Create: `.gitignore`

- [ ] **Step 1: Create the initial source rule dataset**

Create `source/rules.json` with a `version`, named policy groups, and rule entries grouped by category. Include representative rules for `ai`, `streaming`, `apple`, `microsoft`, `cn`, `proxy`, `direct`, and `reject`.

- [ ] **Step 2: Add ignore rules for generated and local files**

Create `.gitignore` that ignores Python cache directories and local environment files while keeping generated `dist/` artifacts trackable.

### Task 2: Generator

**Files:**
- Create: `scripts/generate_rules.py`

- [ ] **Step 1: Implement source loading and validation**

Add validation that rejects missing categories, duplicate rule items inside one category, unsupported rule types, and malformed payloads.

- [ ] **Step 2: Implement Mihomo output**

Generate `dist/mihomo/rule-providers.yaml` plus one `dist/mihomo/rules/<category>.yaml` provider payload per category.

- [ ] **Step 3: Implement Surge/Loon/Quantumult X output**

Generate one `dist/surge/<category>.list`, `dist/loon/<category>.list`, and `dist/quantumultx/<category>.list` per category using policy names from the source data.

- [ ] **Step 4: Implement sing-box output**

Generate one `dist/sing-box/rule-set/<category>.json` per category using sing-box source rule-set JSON syntax.

- [ ] **Step 5: Implement Sub-Store reference output**

Generate `dist/sub-store/rule-urls.json` containing raw GitHub URL templates that can be copied into Sub-Store templates or scripts after the repository slug is configured.

### Task 3: CI and Documentation

**Files:**
- Create: `.github/workflows/generate-rules.yml`
- Create: `README.md`
- Create: `docs/sub-store.md`

- [ ] **Step 1: Add GitHub Actions workflow**

Run `python scripts/generate_rules.py --check` to verify generated output is current, then upload `dist/` as an artifact.

- [ ] **Step 2: Document local workflow**

Explain editing `source/rules.json`, running the generator, and using generated URLs in Sub-Store.

- [ ] **Step 3: Document Sub-Store integration**

Describe the intended ownership split: GitHub manages rules and generated files, Sub-Store manages node aggregation, filtering, renaming, and client-specific subscriptions.

### Task 4: Verification

**Files:**
- Generated: `dist/**`

- [ ] **Step 1: Run generation**

Run: `python scripts/generate_rules.py`

Expected: command exits 0 and writes `dist/`.

- [ ] **Step 2: Run check mode**

Run: `python scripts/generate_rules.py --check`

Expected: command exits 0 and reports that generated files are current.

- [ ] **Step 3: Inspect generated file list**

Run: `rg --files`

Expected: source files, docs, workflow, script, and generated `dist/` files are present.
