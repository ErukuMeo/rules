import json
import tempfile
import unittest
from pathlib import Path

from scripts.generate_rules import SourceError, build_outputs, load_source


def write_source(payload):
    directory = tempfile.TemporaryDirectory()
    path = Path(directory.name) / "rules.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return directory, path


def minimal_source():
    return {
        "version": 1,
        "repository": {
            "owner": "example",
            "name": "rules",
            "branch": "main",
        },
        "policies": {
            "ai": "AI",
            "final": "FINAL",
        },
        "categories": [
            {
                "id": "ai",
                "description": "AI",
                "policy": "AI",
                "rules": [
                    {"type": "domain_suffix", "value": "openai.com"},
                ],
            }
        ],
    }


class GenerateRulesTests(unittest.TestCase):
    def test_load_source_accepts_minimal_valid_source(self):
        directory, path = write_source(minimal_source())
        with directory:
            source = load_source(path)

        self.assertEqual(source.repository["owner"], "example")
        self.assertEqual(source.categories[0].id, "ai")

    def test_load_source_rejects_duplicate_rule_in_category(self):
        payload = minimal_source()
        payload["categories"][0]["rules"].append({"type": "domain_suffix", "value": "OPENAI.com"})
        directory, path = write_source(payload)

        with directory, self.assertRaisesRegex(SourceError, "duplicate rule"):
            load_source(path)

    def test_load_source_rejects_undefined_policy(self):
        payload = minimal_source()
        payload["categories"][0]["policy"] = "MISSING"
        directory, path = write_source(payload)

        with directory, self.assertRaisesRegex(SourceError, "undefined policy"):
            load_source(path)

    def test_build_outputs_omits_placeholder_note_for_real_repository(self):
        directory, path = write_source(minimal_source())
        with directory:
            source = load_source(path)
            outputs = build_outputs(source)

        sub_store_path = next(path for path in outputs if path.name == "rule-urls.json")
        payload = json.loads(outputs[sub_store_path])
        self.assertNotIn("note", payload)


if __name__ == "__main__":
    unittest.main()
