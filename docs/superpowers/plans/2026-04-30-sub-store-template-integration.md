# Sub-Store Template Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the current rule outputs into easier-to-consume Sub-Store/client template artifacts while keeping source rules as the single source of truth.

**Architecture:** `source/rules.json` remains the input. `scripts/generate_rules.py` will generate both rule artifacts under `dist/` and reusable client template fragments under `dist/templates/`; static examples in `templates/` stay as documentation-oriented references. Tests in `tests/test_generate_rules.py` will verify the generated templates include the expected repository URLs, rule ordering, and policy names.

**Tech Stack:** Python 3.12 standard library, JSON source rules, generated YAML/JSON/text fragments, `unittest`, GitHub Actions.

---

### Task 1: Plan and Progress Tracking

**Files:**
- Create: `docs/superpowers/plans/2026-04-30-sub-store-template-integration.md`

- [x] **Step 1: Write this implementation plan**

Document the next concrete tasks and keep checkbox status updated as work proceeds.

- [x] **Step 2: Commit and push the plan**

Run:

```bash
git add docs/superpowers/plans/2026-04-30-sub-store-template-integration.md
git commit -m "docs: add sub-store template integration plan"
git push https://github.com/ErukuMeo/rules.git main
```

Expected: GitHub `main` contains this plan before implementation changes start.

### Task 2: Generated Client Template Outputs

**Files:**
- Modify: `scripts/generate_rules.py`
- Modify: `tests/test_generate_rules.py`
- Generate: `dist/templates/mihomo/profile-fragment.yaml`
- Generate: `dist/templates/sing-box/route-fragment.json`
- Generate: `dist/templates/sub-store/rule-urls.md`

- [ ] **Step 1: Write failing tests for generated templates**

Add tests that assert `build_outputs()` includes:

```text
dist/templates/mihomo/profile-fragment.yaml
dist/templates/sing-box/route-fragment.json
dist/templates/sub-store/rule-urls.md
```

Expected initial result: tests fail because the generator does not emit these paths yet.

- [ ] **Step 2: Implement generated templates**

Add renderer functions that use `source.repository`, `source.categories`, and `source.policies` rather than hard-coded repository URLs.

- [ ] **Step 3: Regenerate and verify**

Run:

```bash
python scripts/generate_rules.py
python scripts/generate_rules.py --check
python -m unittest discover -s tests -v
python -m py_compile scripts/generate_rules.py
```

Expected: generated files are current and all tests pass.

- [ ] **Step 4: Commit and push generated template outputs**

Run:

```bash
git add scripts/generate_rules.py tests/test_generate_rules.py dist/templates dist/sub-store/rule-urls.json docs/superpowers/plans/2026-04-30-sub-store-template-integration.md
git commit -m "feat: generate sub-store client templates"
git push https://github.com/ErukuMeo/rules.git main
```

### Task 3: Documentation Update

**Files:**
- Modify: `README.md`
- Modify: `docs/sub-store.md`
- Modify: `templates/sub-store/README.md`
- Modify: `docs/superpowers/plans/2026-04-30-sub-store-template-integration.md`

- [ ] **Step 1: Document generated template locations**

Explain that `dist/templates/` contains generated, repository-aware fragments and `templates/` contains editable static references.

- [ ] **Step 2: Add Sub-Store usage sequence**

Document the expected flow: import nodes in Sub-Store, create policy names, merge generated fragment, update client subscription.

- [ ] **Step 3: Verify docs and generated outputs**

Run:

```bash
python scripts/generate_rules.py --check
python -m unittest discover -s tests -v
```

Expected: docs changes do not affect generated output, and tests pass.

- [ ] **Step 4: Commit and push documentation update**

Run:

```bash
git add README.md docs/sub-store.md templates/sub-store/README.md docs/superpowers/plans/2026-04-30-sub-store-template-integration.md
git commit -m "docs: document generated sub-store templates"
git push https://github.com/ErukuMeo/rules.git main
```

### Task 4: Final Verification

**Files:**
- No new files expected.

- [ ] **Step 1: Run full verification**

Run:

```bash
python scripts/generate_rules.py
python scripts/generate_rules.py --check
python -m unittest discover -s tests -v
python -m py_compile scripts/generate_rules.py
git -c safe.directory=E:/Work/Projects/rules status --short
```

Expected: generation is current, tests pass, script compiles, and working tree is clean.

- [ ] **Step 2: Report commit hashes and status**

List the commits pushed during this continuation and any remaining recommended next work.
