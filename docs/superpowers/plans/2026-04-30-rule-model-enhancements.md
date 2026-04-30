# Rule Model Enhancements Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Strengthen the source rule model so categories can be ordered, disabled, documented, and validated before generating multi-client artifacts.

**Architecture:** `source/rules.json` remains version 1, with backward-compatible optional category fields: `priority`, `enabled`, `source`, and `notes`. `scripts/generate_rules.py` will normalize categories, reject malformed metadata, require the `final` policy, enforce safe category IDs, and generate outputs only for enabled categories sorted by priority and declaration order. Unit tests will cover the new behavior before implementation changes.

**Tech Stack:** Python 3.12 standard library, JSON source rules, generated YAML/JSON/text artifacts, `unittest`, GitHub Actions.

---

### Task 1: Plan and Progress Tracking

**Files:**
- Create: `docs/superpowers/plans/2026-04-30-rule-model-enhancements.md`

- [x] **Step 1: Write this implementation plan**

Document the model changes and expected execution checkpoints.

- [x] **Step 2: Commit and push the plan**

Run:

```bash
git add docs/superpowers/plans/2026-04-30-rule-model-enhancements.md
git commit -m "docs: add rule model enhancement plan"
git push https://github.com/ErukuMeo/rules.git main
```

Expected: GitHub `main` contains this plan before implementation changes start.

### Task 2: Schema Validation Enhancements

**Files:**
- Modify: `scripts/generate_rules.py`
- Modify: `tests/test_generate_rules.py`
- Modify: `docs/superpowers/plans/2026-04-30-rule-model-enhancements.md`

- [x] **Step 1: Write failing tests**

Add tests for:

```text
category id must match lowercase letters, numbers, and hyphen
policies must include final
enabled=false categories are omitted from generated outputs
priority sorts enabled categories before generation
source and notes must be strings when present
```

Expected initial result: at least one new test fails because the current generator does not implement these rules.

- [x] **Step 2: Implement schema changes**

Update dataclasses and `load_source()` to parse and validate `priority`, `enabled`, `source`, and `notes`. Keep missing optional fields backward-compatible.

- [x] **Step 3: Verify**

Run:

```bash
python -m unittest discover -s tests -v
python scripts/generate_rules.py --check
python -m py_compile scripts/generate_rules.py
```

Expected: tests pass, generated files remain current, and the script compiles.

- [x] **Step 4: Commit and push**

Run:

```bash
git add scripts/generate_rules.py tests/test_generate_rules.py docs/superpowers/plans/2026-04-30-rule-model-enhancements.md
git commit -m "feat: strengthen rule source validation"
git push https://github.com/ErukuMeo/rules.git main
```

### Task 3: Source Metadata and Generated Output Refresh

**Files:**
- Modify: `source/rules.json`
- Modify: `dist/**`
- Modify: `docs/superpowers/plans/2026-04-30-rule-model-enhancements.md`

- [x] **Step 1: Add category metadata to source rules**

Add `priority`, `enabled`, and concise `source` values to each existing category.

- [x] **Step 2: Regenerate outputs**

Run:

```bash
python scripts/generate_rules.py
python scripts/generate_rules.py --check
python -m unittest discover -s tests -v
```

Expected: generated files reflect priority ordering and remain synchronized.

- [x] **Step 3: Commit and push**

Run:

```bash
git add source/rules.json dist docs/superpowers/plans/2026-04-30-rule-model-enhancements.md
git commit -m "chore: annotate source rule categories"
git push https://github.com/ErukuMeo/rules.git main
```

### Task 4: Documentation and Final Verification

**Files:**
- Modify: `README.md`
- Modify: `docs/sub-store.md`
- Modify: `docs/superpowers/plans/2026-04-30-rule-model-enhancements.md`

- [ ] **Step 1: Document the enhanced category fields**

Explain `priority`, `enabled`, `source`, and `notes`, including how disabled categories affect generated outputs.

- [ ] **Step 2: Run final verification**

Run:

```bash
python scripts/generate_rules.py
python scripts/generate_rules.py --check
python -m unittest discover -s tests -v
python -m py_compile scripts/generate_rules.py
git -c safe.directory=E:/Work/Projects/rules status --short
```

Expected: generation is current, tests pass, script compiles, and only documentation/plan files are staged for the final docs commit.

- [ ] **Step 3: Commit and push**

Run:

```bash
git add README.md docs/sub-store.md docs/superpowers/plans/2026-04-30-rule-model-enhancements.md
git commit -m "docs: document rule model metadata"
git push https://github.com/ErukuMeo/rules.git main
```

- [ ] **Step 4: Report status**

List pushed commits, verification commands, and any recommended next phase.
