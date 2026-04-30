#!/usr/bin/env python3
"""Generate multi-client rule artifacts from source/rules.json."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILE = ROOT / "source" / "rules.json"
DIST_DIR = ROOT / "dist"

SUPPORTED_TYPES = {
    "domain",
    "domain_suffix",
    "domain_keyword",
    "ip_cidr",
    "geoip",
    "geosite",
}

CLASSICAL_TYPE_MAP = {
    "domain": "DOMAIN",
    "domain_suffix": "DOMAIN-SUFFIX",
    "domain_keyword": "DOMAIN-KEYWORD",
    "ip_cidr": "IP-CIDR",
    "geoip": "GEOIP",
    "geosite": "GEOSITE",
}

SING_BOX_FIELD_MAP = {
    "domain": "domain",
    "domain_suffix": "domain_suffix",
    "domain_keyword": "domain_keyword",
    "ip_cidr": "ip_cidr",
    "geoip": "geoip",
    "geosite": "geosite",
}


@dataclass(frozen=True)
class Rule:
    type: str
    value: str


@dataclass(frozen=True)
class Category:
    id: str
    description: str
    policy: str
    rules: tuple[Rule, ...]


@dataclass(frozen=True)
class Source:
    version: int
    repository: dict[str, str]
    policies: dict[str, str]
    categories: tuple[Category, ...]


class SourceError(ValueError):
    pass


def load_source(path: Path) -> Source:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SourceError(f"Source file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SourceError(f"Invalid JSON in {path}: {exc}") from exc

    if raw.get("version") != 1:
        raise SourceError("source/rules.json must use version 1")

    repository = raw.get("repository")
    if not isinstance(repository, dict):
        raise SourceError("repository must be an object")
    for key in ("owner", "name", "branch"):
        value = repository.get(key)
        if not isinstance(value, str) or not value:
            raise SourceError(f"repository.{key} must be a non-empty string")

    policies = raw.get("policies")
    if not isinstance(policies, dict) or not policies:
        raise SourceError("policies must be a non-empty object")

    categories_raw = raw.get("categories")
    if not isinstance(categories_raw, list) or not categories_raw:
        raise SourceError("categories must be a non-empty array")

    categories: list[Category] = []
    category_ids: set[str] = set()
    for category_raw in categories_raw:
        if not isinstance(category_raw, dict):
            raise SourceError("each category must be an object")

        category_id = require_string(category_raw, "id")
        if category_id in category_ids:
            raise SourceError(f"duplicate category id: {category_id}")
        category_ids.add(category_id)

        description = require_string(category_raw, "description")
        policy = require_string(category_raw, "policy")
        if policy not in set(policies.values()):
            raise SourceError(f"category {category_id} uses undefined policy: {policy}")

        rules_raw = category_raw.get("rules")
        if not isinstance(rules_raw, list) or not rules_raw:
            raise SourceError(f"category {category_id} must have non-empty rules")

        rules: list[Rule] = []
        seen_rules: set[tuple[str, str]] = set()
        for rule_raw in rules_raw:
            if not isinstance(rule_raw, dict):
                raise SourceError(f"category {category_id} contains a non-object rule")
            rule_type = require_string(rule_raw, "type")
            value = require_string(rule_raw, "value")
            if rule_type not in SUPPORTED_TYPES:
                raise SourceError(f"category {category_id} has unsupported type: {rule_type}")
            key = (rule_type, value.lower())
            if key in seen_rules:
                raise SourceError(f"category {category_id} has duplicate rule: {rule_type}:{value}")
            seen_rules.add(key)
            rules.append(Rule(rule_type, value))

        categories.append(Category(category_id, description, policy, tuple(rules)))

    return Source(
        version=raw["version"],
        repository={key: str(repository[key]) for key in ("owner", "name", "branch")},
        policies={str(key): str(value) for key, value in policies.items()},
        categories=tuple(categories),
    )


def require_string(obj: dict[str, Any], key: str) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip():
        raise SourceError(f"{key} must be a non-empty string")
    return value.strip()


def classical_rule(rule: Rule, policy: str | None = None) -> str:
    base = f"{CLASSICAL_TYPE_MAP[rule.type]},{rule.value}"
    if policy:
        return f"{base},{policy}"
    return base


def yaml_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def render_mihomo_provider(category: Category) -> str:
    lines = [
        f"# {category.description}",
        "payload:",
    ]
    lines.extend(f"  - {yaml_quote(classical_rule(rule))}" for rule in category.rules)
    return "\n".join(lines) + "\n"


def render_mihomo_rule_providers(source: Source) -> str:
    repo = source.repository
    base_url = f"https://raw.githubusercontent.com/{repo['owner']}/{repo['name']}/{repo['branch']}/dist/mihomo/rules"
    lines = ["rule-providers:"]
    for category in source.categories:
        lines.extend(
            [
                f"  {category.id}:",
                "    type: http",
                "    behavior: classical",
                "    format: yaml",
                f"    url: {base_url}/{category.id}.yaml",
                f"    path: ./ruleset/{category.id}.yaml",
                "    interval: 86400",
            ]
        )
    return "\n".join(lines) + "\n"


def render_mihomo_rules(source: Source) -> str:
    lines = ["rules:"]
    for category in source.categories:
        lines.append(f"  - RULE-SET,{category.id},{category.policy}")
    lines.append(f"  - MATCH,{source.policies['final']}")
    return "\n".join(lines) + "\n"


def render_classical_list(category: Category) -> str:
    lines = [f"# {category.description}"]
    lines.extend(classical_rule(rule, category.policy) for rule in category.rules)
    return "\n".join(lines) + "\n"


def render_sing_box_rule_set(category: Category) -> str:
    grouped: dict[str, list[str]] = {}
    for rule in category.rules:
        grouped.setdefault(SING_BOX_FIELD_MAP[rule.type], []).append(rule.value)

    sing_box_rule = {key: values for key, values in sorted(grouped.items())}
    payload = {
        "version": 3,
        "rules": [sing_box_rule],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def render_sub_store_urls(source: Source) -> str:
    repo = source.repository
    base_url = f"https://raw.githubusercontent.com/{repo['owner']}/{repo['name']}/{repo['branch']}/dist"
    payload = {
        "repository": repo,
        "mihomo": {
            "ruleProviders": f"{base_url}/mihomo/rule-providers.yaml",
            "rules": f"{base_url}/mihomo/rules.yaml",
        },
        "surge": {category.id: f"{base_url}/surge/{category.id}.list" for category in source.categories},
        "loon": {category.id: f"{base_url}/loon/{category.id}.list" for category in source.categories},
        "quantumultx": {
            category.id: f"{base_url}/quantumultx/{category.id}.list" for category in source.categories
        },
        "sing-box": {
            category.id: f"{base_url}/sing-box/rule-set/{category.id}.json" for category in source.categories
        },
    }
    if repo["owner"] == "YOUR_GITHUB_USERNAME":
        payload["note"] = "Replace repository.owner/name/branch in source/rules.json before publishing."
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def build_outputs(source: Source) -> dict[Path, str]:
    outputs: dict[Path, str] = {
        DIST_DIR / "mihomo" / "rule-providers.yaml": render_mihomo_rule_providers(source),
        DIST_DIR / "mihomo" / "rules.yaml": render_mihomo_rules(source),
        DIST_DIR / "sub-store" / "rule-urls.json": render_sub_store_urls(source),
    }

    for category in source.categories:
        outputs[DIST_DIR / "mihomo" / "rules" / f"{category.id}.yaml"] = render_mihomo_provider(category)
        outputs[DIST_DIR / "surge" / f"{category.id}.list"] = render_classical_list(category)
        outputs[DIST_DIR / "loon" / f"{category.id}.list"] = render_classical_list(category)
        outputs[DIST_DIR / "quantumultx" / f"{category.id}.list"] = render_classical_list(category)
        outputs[DIST_DIR / "sing-box" / "rule-set" / f"{category.id}.json"] = render_sing_box_rule_set(category)

    return outputs


def write_outputs(outputs: dict[Path, str]) -> None:
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    for path, content in sorted(outputs.items()):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")


def check_outputs(outputs: dict[Path, str]) -> int:
    mismatches: list[str] = []
    for path, expected in sorted(outputs.items()):
        if not path.exists():
            mismatches.append(f"missing: {path.relative_to(ROOT)}")
            continue
        actual = path.read_text(encoding="utf-8")
        if actual != expected:
            mismatches.append(f"outdated: {path.relative_to(ROOT)}")

    existing = {path for path in DIST_DIR.rglob("*") if path.is_file()} if DIST_DIR.exists() else set()
    expected_paths = set(outputs)
    for extra in sorted(existing - expected_paths):
        mismatches.append(f"extra: {extra.relative_to(ROOT)}")

    if mismatches:
        print("Generated files are not current:", file=sys.stderr)
        for mismatch in mismatches:
            print(f"  - {mismatch}", file=sys.stderr)
        print("Run: python scripts/generate_rules.py", file=sys.stderr)
        return 1

    print("Generated files are current.")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate multi-client rule artifacts.")
    parser.add_argument("--check", action="store_true", help="verify dist output without writing files")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        source = load_source(SOURCE_FILE)
        outputs = build_outputs(source)
        if args.check:
            return check_outputs(outputs)
        write_outputs(outputs)
    except SourceError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(f"Generated {len(outputs)} files in {DIST_DIR.relative_to(ROOT)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
