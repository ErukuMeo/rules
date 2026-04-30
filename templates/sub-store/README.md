# Sub-Store Template Notes

Use Sub-Store to assemble nodes and policies, then merge the rule fragments from this repository into the exported client profile.

Recommended flow:

1. Create or import node subscriptions in Sub-Store.
2. Normalize node names and regions.
3. Create policy groups named `AI`, `STREAMING`, `APPLE`, `MICROSOFT`, `PROXY`, `DIRECT`, `REJECT`, and `FINAL`.
4. For Mihomo / Clash.Meta clients, merge `templates/mihomo/profile-fragment.yaml` or use the generated files in `dist/mihomo/`.
5. For sing-box clients, merge `templates/sing-box/route-fragment.json` into the `route` object of the Sub-Store generated sing-box config.

Keep secrets in Sub-Store. Do not commit provider URLs, tokens, private Gist URLs, or airport API links.
