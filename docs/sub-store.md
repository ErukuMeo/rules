# Sub-Store Integration

Use this repository as the rule source and use Sub-Store as the subscription assembly layer.

## Ownership Split

GitHub repository:

- Maintains source rules in `source/rules.json`.
- Generates reusable rule files under `dist/`.
- Publishes stable Raw GitHub URLs.

Sub-Store:

- Imports one or more airport/node subscriptions.
- Filters nodes by region, protocol, name, or custom scripts.
- Renames and sorts nodes.
- Exports client-specific subscriptions for Android, iOS, Windows, Linux, and macOS.
- References the generated rules or embeds them through client templates.

## First Setup

1. Edit `source/rules.json`.
2. Replace:

```json
{
  "owner": "YOUR_GITHUB_USERNAME",
  "name": "rules",
  "branch": "main"
}
```

3. Run:

```bash
python scripts/generate_rules.py
```

4. Push the repository to GitHub.
5. Open `dist/sub-store/rule-urls.json` and copy the URLs needed by your Sub-Store templates.

## Recommended Policy Groups

Keep policy names consistent across client templates:

```text
DIRECT
REJECT
PROXY
AI
STREAMING
APPLE
MICROSOFT
FINAL
```

Sub-Store can generate the node groups behind these names. The generated rules should only decide which policy a request uses.

## Mihomo / Clash.Meta

Use:

```text
dist/mihomo/rule-providers.yaml
dist/mihomo/rules.yaml
```

These files are intended to be merged into a Mihomo profile. `rule-providers.yaml` defines remote rule providers. `rules.yaml` defines the `RULE-SET` ordering.

## Surge, Loon, Quantumult X

Use the generated category lists:

```text
dist/surge/<category>.list
dist/loon/<category>.list
dist/quantumultx/<category>.list
```

Each line includes the category policy, for example:

```text
DOMAIN-SUFFIX,openai.com,AI
```

## sing-box

Use:

```text
dist/sing-box/rule-set/<category>.json
```

These are source rule-set JSON files. If your client prefers compiled `.srs` files, add a later CI step with the sing-box binary to compile them.

## Security Notes

Do not commit airport subscription URLs, API tokens, Sub-Store sync tokens, or private Gist tokens. Keep those in Sub-Store or GitHub Actions secrets.
