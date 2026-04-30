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

    def test_load_source_rejects_invalid_category_id(self):
        payload = minimal_source()
        payload["categories"][0]["id"] = "AI Rules"
        directory, path = write_source(payload)

        with directory, self.assertRaisesRegex(SourceError, "invalid category id"):
            load_source(path)

    def test_load_source_requires_final_policy(self):
        payload = minimal_source()
        del payload["policies"]["final"]
        directory, path = write_source(payload)

        with directory, self.assertRaisesRegex(SourceError, "policies.final"):
            load_source(path)

    def test_load_source_rejects_invalid_category_metadata(self):
        payload = minimal_source()
        payload["categories"][0]["enabled"] = "yes"
        directory, path = write_source(payload)

        with directory, self.assertRaisesRegex(SourceError, "enabled"):
            load_source(path)

        payload = minimal_source()
        payload["categories"][0]["priority"] = "1"
        directory, path = write_source(payload)

        with directory, self.assertRaisesRegex(SourceError, "priority"):
            load_source(path)

        payload = minimal_source()
        payload["categories"][0]["source"] = ["manual"]
        directory, path = write_source(payload)

        with directory, self.assertRaisesRegex(SourceError, "source"):
            load_source(path)

        payload = minimal_source()
        payload["categories"][0]["notes"] = {"text": "manual"}
        directory, path = write_source(payload)

        with directory, self.assertRaisesRegex(SourceError, "notes"):
            load_source(path)

    def test_build_outputs_omits_placeholder_note_for_real_repository(self):
        directory, path = write_source(minimal_source())
        with directory:
            source = load_source(path)
            outputs = build_outputs(source)

        sub_store_path = next(path for path in outputs if path.name == "rule-urls.json")
        payload = json.loads(outputs[sub_store_path])
        self.assertNotIn("note", payload)

    def test_build_outputs_omits_disabled_categories_and_sorts_by_priority(self):
        payload = minimal_source()
        payload["policies"]["streaming"] = "STREAMING"
        payload["policies"]["direct"] = "DIRECT"
        payload["categories"] = [
            {
                "id": "streaming",
                "description": "Streaming",
                "policy": "STREAMING",
                "priority": 20,
                "rules": [{"type": "domain_suffix", "value": "netflix.com"}],
            },
            {
                "id": "direct",
                "description": "Direct",
                "policy": "DIRECT",
                "priority": 10,
                "enabled": False,
                "rules": [{"type": "domain", "value": "localhost"}],
            },
            {
                "id": "ai",
                "description": "AI",
                "policy": "AI",
                "priority": 5,
                "source": "manual",
                "notes": "AI services",
                "rules": [{"type": "domain_suffix", "value": "openai.com"}],
            },
        ]
        directory, path = write_source(payload)

        with directory:
            source = load_source(path)
            outputs = build_outputs(source)

        self.assertEqual([category.id for category in source.categories], ["ai", "streaming"])
        rendered = {str(path).replace("\\", "/"): content for path, content in outputs.items()}
        self.assertFalse(any("/direct." in path or "/direct/" in path for path in rendered))

        rules_yaml = next(content for path, content in rendered.items() if path.endswith("dist/mihomo/rules.yaml"))
        self.assertLess(rules_yaml.index("RULE-SET,ai,AI"), rules_yaml.index("RULE-SET,streaming,STREAMING"))

    def test_build_outputs_generates_repository_aware_template_fragments(self):
        directory, path = write_source(minimal_source())
        with directory:
            source = load_source(path)
            outputs = build_outputs(source)

        rendered = {str(path).replace("\\", "/"): content for path, content in outputs.items()}

        mihomo = next(
            content
            for path, content in rendered.items()
            if path.endswith("dist/templates/mihomo/profile-fragment.yaml")
        )
        self.assertIn("url: https://raw.githubusercontent.com/example/rules/main/dist/mihomo/rules/ai.yaml", mihomo)
        self.assertIn("- RULE-SET,ai,AI", mihomo)

        sing_box = next(
            content
            for path, content in rendered.items()
            if path.endswith("dist/templates/sing-box/route-fragment.json")
        )
        sing_box_payload = json.loads(sing_box)
        self.assertEqual(sing_box_payload["final"], "FINAL")
        self.assertEqual(sing_box_payload["rules"][0], {"rule_set": "ai", "outbound": "AI"})

        markdown = next(
            content
            for path, content in rendered.items()
            if path.endswith("dist/templates/sub-store/rule-urls.md")
        )
        self.assertIn("| ai |", markdown)
        self.assertIn("https://raw.githubusercontent.com/example/rules/main/dist/sing-box/rule-set/ai.json", markdown)


if __name__ == "__main__":
    unittest.main()
