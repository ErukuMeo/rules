# Rule Content Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand the practical rule categories beyond the initial baseline so Sub-Store generated profiles cover common Google, developer, gaming, and download workflows.

**Architecture:** Keep `source/rules.json` as the only hand-maintained rule source. Add new policy mappings and categories using the existing metadata fields (`priority`, `enabled`, `source`, `notes`), then regenerate `dist/`. Add a source coverage test so the expected category IDs are enforced by CI.

**Tech Stack:** Python 3.12 standard library, JSON source rules, generated YAML/JSON/text artifacts, `unittest`, GitHub Actions.

---

### Task 1: Plan and Progress Tracking

**Files:**
- Create: `docs/superpowers/plans/2026-04-30-rule-content-expansion.md`

- [x] **Step 1: Write this implementation plan**

Document the next rule content expansion tasks and expected verification steps.

- [x] **Step 2: Commit and push the plan**

Run:

```bash
git add docs/superpowers/plans/2026-04-30-rule-content-expansion.md
git commit -m "docs: add rule content expansion plan"
git push https://github.com/ErukuMeo/rules.git main
```

### Task 2: Add New Rule Categories

**Files:**
- Modify: `source/rules.json`
- Modify: `tests/test_generate_rules.py`
- Modify: `dist/**`
- Modify: `docs/superpowers/plans/2026-04-30-rule-content-expansion.md`

- [ ] **Step 1: Write failing source coverage test**

Add a test asserting the real source contains these category IDs:

```text
ai, streaming, apple, microsoft, google, developer, games, download, cn, proxy, direct, reject
```

Expected initial result: test fails before source categories are added.

- [ ] **Step 2: Add policies and categories**

Add policy mappings and category entries:

```text
google -> GOOGLE
developer -> DEVELOPER
games -> GAMES
download -> DOWNLOAD
```

Use priorities between `microsoft` and `cn` for new categories so specific service categories run before broad `cn/proxy/direct/reject` fallbacks.

- [ ] **Step 3: Regenerate and verify**

Run:

```bash
python scripts/generate_rules.py
python scripts/generate_rules.py --check
python -m unittest discover -s tests -v
python -m py_compile scripts/generate_rules.py
```

Expected: generated files are current, tests pass, and script compiles.

- [ ] **Step 4: Commit and push**

Run:

```bash
git add source/rules.json tests/test_generate_rules.py dist docs/superpowers/plans/2026-04-30-rule-content-expansion.md
git commit -m "feat: expand baseline rule categories"
git push https://github.com/ErukuMeo/rules.git main
```

### Task 3: Documentation and Final Verification

**Files:**
- Modify: `README.md`
- Modify: `docs/sub-store.md`
- Modify: `docs/superpowers/plans/2026-04-30-rule-content-expansion.md`

- [ ] **Step 1: Document new policy groups**

Add `GOOGLE`, `DEVELOPER`, `GAMES`, and `DOWNLOAD` to policy group examples and explain when to use them.

- [ ] **Step 2: Run final verification**

Run:

```bash
python scripts/generate_rules.py
python scripts/generate_rules.py --check
python -m unittest discover -s tests -v
python -m py_compile scripts/generate_rules.py
git -c safe.directory=E:/Work/Projects/rules status --short
```

Expected: generated files are current, tests pass, script compiles, and only documentation/plan files are staged for the docs commit.

- [ ] **Step 3: Commit and push**

Run:

```bash
git add README.md docs/sub-store.md docs/superpowers/plans/2026-04-30-rule-content-expansion.md
git commit -m "docs: document expanded rule categories"
git push https://github.com/ErukuMeo/rules.git main
```

- [ ] **Step 4: Report status**

List pushed commits, verification commands, and the recommended next phase.
