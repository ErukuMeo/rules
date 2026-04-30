# Rules

This repository maintains one source rule dataset and generates rule artifacts for multiple proxy client ecosystems. It is designed to pair with Sub-Store: GitHub owns the reusable rules, while Sub-Store owns node subscription aggregation, filtering, renaming, and client-specific subscription output.

## Structure

```text
source/rules.json              Source of truth
scripts/generate_rules.py      Generator and validator
dist/mihomo/                   Mihomo / Clash.Meta rule providers
dist/surge/                    Surge rule lists
dist/loon/                     Loon rule lists
dist/quantumultx/              Quantumult X rule lists
dist/sing-box/rule-set/        sing-box source rule-set JSON
dist/sub-store/rule-urls.json  URL index for Sub-Store templates/scripts
```

## Local Workflow

1. Edit `source/rules.json`.
2. Set `repository.owner`, `repository.name`, and `repository.branch` to your GitHub repository.
3. Generate artifacts:

```bash
python scripts/generate_rules.py
```

4. Verify generated artifacts are current:

```bash
python scripts/generate_rules.py --check
```

5. Commit both `source/` and `dist/`.

## Rule Model

Each category has one policy name and a list of rules:

```json
{
  "id": "ai",
  "description": "AI services and model providers",
  "policy": "AI",
  "rules": [
    { "type": "domain_suffix", "value": "openai.com" },
    { "type": "domain_suffix", "value": "chatgpt.com" }
  ]
}
```

Supported rule types:

- `domain`
- `domain_suffix`
- `domain_keyword`
- `ip_cidr`
- `geoip`
- `geosite`

## GitHub Actions

`.github/workflows/generate-rules.yml` runs:

```bash
python scripts/generate_rules.py --check
```

The workflow fails when `source/rules.json` and `dist/` are out of sync. This keeps Raw GitHub URLs stable for Sub-Store and clients.

## Publishing URLs

After replacing the placeholder repository fields in `source/rules.json`, generated URLs follow this pattern:

```text
https://raw.githubusercontent.com/<owner>/<repo>/<branch>/dist/<platform>/<file>
```

The generated `dist/sub-store/rule-urls.json` contains the full URL index.
