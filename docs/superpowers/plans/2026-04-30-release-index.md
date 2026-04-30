# Release Index Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate a deterministic release index for all published rule artifacts so Sub-Store users can inspect available clients, categories, Raw URLs, file sizes, and checksums from one place.

**Architecture:** Keep `source/rules.json` as the only hand-maintained rule source. Extend `scripts/generate_rules.py` so `build_outputs()` first creates all existing artifacts, then derives a `dist/manifest.json` and `dist/manifest.md` from those in-memory outputs. The manifest must be deterministic and covered by tests so CI catches stale or malformed release metadata.

**Tech Stack:** Python 3.12 standard library, JSON source rules, generated Markdown/JSON artifacts, `unittest`, GitHub Actions.

---

### Task 1: Plan and Progress Tracking

**Files:**
- Create: `docs/superpowers/plans/2026-04-30-release-index.md`

- [x] **Step 1: Write this implementation plan**

Document the release index tasks, verification commands, and expected commits.

- [x] **Step 2: Commit and push the plan**

Run:

```bash
git add docs/superpowers/plans/2026-04-30-release-index.md
git commit -m "docs: add release index plan"
git push https://github.com/ErukuMeo/rules.git main
```

### Task 2: Generate Release Manifest

**Files:**
- Modify: `tests/test_generate_rules.py`
- Modify: `scripts/generate_rules.py`
- Modify: `dist/**`
- Modify: `docs/superpowers/plans/2026-04-30-release-index.md`

- [x] **Step 1: Write failing manifest test**

Add a test that loads a minimal source, builds outputs, and asserts:

```python
manifest = json.loads(outputs[manifest_path])
self.assertEqual(manifest["repository"]["owner"], "example")
self.assertEqual(manifest["version"], 1)
self.assertEqual(manifest["categories"], ["ai"])
self.assertIn("generatedAt", manifest)
self.assertEqual(manifest["generatedAt"], "1970-01-01T00:00:00Z")
self.assertIn("dist/mihomo/rules/ai.yaml", manifest["artifacts"])
self.assertEqual(
    manifest["artifacts"]["dist/mihomo/rules/ai.yaml"]["url"],
    "https://raw.githubusercontent.com/example/rules/main/dist/mihomo/rules/ai.yaml",
)
self.assertGreater(manifest["artifacts"]["dist/mihomo/rules/ai.yaml"]["size"], 0)
self.assertRegex(manifest["artifacts"]["dist/mihomo/rules/ai.yaml"]["sha256"], r"^[0-9a-f]{64}$")
```

Expected initial result: the test fails because `dist/manifest.json` is not generated.

- [x] **Step 2: Implement manifest generation**

Add helper functions in `scripts/generate_rules.py`:

```python
def raw_url(source: Source, relative_path: str) -> str:
    repo = source.repository
    return f"https://raw.githubusercontent.com/{repo['owner']}/{repo['name']}/{repo['branch']}/{relative_path}"
```

```python
def build_manifest(source: Source, outputs: dict[Path, str]) -> dict[str, Any]:
    artifacts = {}
    for path, content in sorted(outputs.items(), key=lambda item: item[0].as_posix()):
        relative_path = path.relative_to(ROOT).as_posix()
        artifacts[relative_path] = {
            "url": raw_url(source, relative_path),
            "size": len(content.encode("utf-8")),
            "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
        }
    return {
        "version": source.version,
        "repository": source.repository,
        "generatedAt": "1970-01-01T00:00:00Z",
        "categories": [category.id for category in source.categories],
        "artifacts": artifacts,
    }
```

Then append these generated files after the existing category outputs:

```python
manifest = build_manifest(source, outputs)
outputs[DIST_DIR / "manifest.json"] = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
outputs[DIST_DIR / "manifest.md"] = render_manifest_markdown(source, manifest)
```

The fixed timestamp is intentional: output must be deterministic for `--check`.

- [x] **Step 3: Run generation and tests**

Run:

```bash
python scripts/generate_rules.py
python scripts/generate_rules.py --check
python -m unittest discover -s tests -v
python -m py_compile scripts/generate_rules.py
```

Expected: generated files are current, tests pass, and script compiles.

- [x] **Step 4: Commit and push**

Run:

```bash
git add scripts/generate_rules.py tests/test_generate_rules.py dist docs/superpowers/plans/2026-04-30-release-index.md
git commit -m "feat: generate release manifest"
git push https://github.com/ErukuMeo/rules.git main
```

### Task 3: Documentation and Final Verification

**Files:**
- Modify: `README.md`
- Modify: `docs/sub-store.md`
- Modify: `docs/superpowers/plans/2026-04-30-release-index.md`

- [x] **Step 1: Document manifest files**

Document these generated files:

```text
dist/manifest.json
dist/manifest.md
```

Explain that `manifest.json` is machine-readable and `manifest.md` is for quick browser inspection.

- [x] **Step 2: Run final verification**

Run:

```bash
python scripts/generate_rules.py --check
python -m unittest discover -s tests -v
python -m py_compile scripts/generate_rules.py
git -c safe.directory=E:/Work/Projects/rules status --short
```

Expected: generated files are current, tests pass, script compiles, and only documentation/plan files are staged for the docs commit.

- [x] **Step 3: Commit and push**

Run:

```bash
git add README.md docs/sub-store.md docs/superpowers/plans/2026-04-30-release-index.md
git commit -m "docs: document release manifest"
git push https://github.com/ErukuMeo/rules.git main
```

- [x] **Step 4: Report status**

List pushed commits, verification commands, and the recommended next phase.
