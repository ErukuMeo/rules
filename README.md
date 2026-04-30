# Rules

这是一个用于维护多端代理分流规则的仓库。目标是只维护一份源规则，然后通过脚本生成多个客户端生态可直接引用的规则集，并配合 Sub-Store 完成节点订阅合并、节点清洗和多端配置输出。

## 设计目标

- 规则只维护一次，避免 Android、iOS、Windows、Linux、macOS 各写一套。
- 规则源放在 GitHub，便于审查、回滚、自动生成和 Raw URL 引用。
- Sub-Store 专注处理节点订阅、筛选、重命名、排序和客户端订阅输出。
- 生成结果覆盖 Mihomo / Clash.Meta、Surge、Loon、Quantumult X 和 sing-box。
- 所有生成产物都可以通过 GitHub Raw URL 被 Sub-Store 或客户端模板引用。

## 目录结构

```text
source/rules.json              源规则，唯一需要手工维护的规则数据
scripts/generate_rules.py      规则生成器和校验器
dist/mihomo/                   Mihomo / Clash.Meta rule-providers 和 rules
dist/surge/                    Surge 规则列表
dist/loon/                     Loon 规则列表
dist/quantumultx/              Quantumult X 规则列表
dist/sing-box/rule-set/        sing-box source rule-set JSON
dist/sub-store/rule-urls.json  供 Sub-Store 或模板引用的 URL 索引
templates/                     可合并到客户端配置里的示例片段
tests/                         生成器测试
docs/                          Sub-Store 接入说明和实施计划
```

## 使用方式

1. 编辑 `source/rules.json`。
2. 确认仓库信息正确：

```json
{
  "owner": "ErukuMeo",
  "name": "rules",
  "branch": "main"
}
```

3. 生成规则产物：

```bash
python scripts/generate_rules.py
```

4. 检查生成产物是否与源规则同步：

```bash
python scripts/generate_rules.py --check
```

5. 运行测试：

```bash
python -m unittest discover -s tests -v
```

6. 提交 `source/`、`scripts/`、`dist/`、`templates/`、`docs/` 和测试文件。

## 源规则格式

每个分类包含一个策略组名称和一组规则：

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

当前支持的规则类型：

- `domain`
- `domain_suffix`
- `domain_keyword`
- `ip_cidr`
- `geoip`
- `geosite`

## 策略组约定

建议在 Sub-Store 和各客户端模板中保持这些策略组名称一致：

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

规则负责决定请求进入哪个策略组；Sub-Store 负责把节点组织到这些策略组背后。

## Sub-Store 接入方式

推荐职责划分：

```text
GitHub 仓库：
  维护源规则
  生成多端规则集
  发布 Raw URL

Sub-Store：
  合并机场/节点订阅
  清洗节点名称
  按地区、协议、倍率、可用性过滤节点
  生成客户端订阅或完整配置
  引用本仓库生成的规则 URL
```

生成后的 URL 索引在：

```text
dist/sub-store/rule-urls.json
```

例如 Mihomo 规则入口：

```text
https://raw.githubusercontent.com/ErukuMeo/rules/main/dist/mihomo/rule-providers.yaml
https://raw.githubusercontent.com/ErukuMeo/rules/main/dist/mihomo/rules.yaml
```

## 各客户端产物

### Mihomo / Clash.Meta

```text
dist/mihomo/rule-providers.yaml
dist/mihomo/rules.yaml
dist/mihomo/rules/<category>.yaml
```

可以将 `rule-providers.yaml` 和 `rules.yaml` 合并到 Sub-Store 生成的 Mihomo 配置中，也可以参考：

```text
templates/mihomo/profile-fragment.yaml
```

### Surge / Loon / Quantumult X

```text
dist/surge/<category>.list
dist/loon/<category>.list
dist/quantumultx/<category>.list
```

每条规则会携带策略组名称，例如：

```text
DOMAIN-SUFFIX,openai.com,AI
```

### sing-box

```text
dist/sing-box/rule-set/<category>.json
```

这些文件是 source rule-set JSON。可以参考：

```text
templates/sing-box/route-fragment.json
```

如果后续需要 `.srs` 二进制规则集，可以在 GitHub Actions 中增加 sing-box 下载和编译步骤。

## GitHub Actions

工作流文件：

```text
.github/workflows/generate-rules.yml
```

它会执行：

```bash
python scripts/generate_rules.py --check
```

如果 `source/rules.json` 修改后没有同步更新 `dist/`，CI 会失败，避免发布过期规则。

## 安全注意事项

不要提交以下内容：

- 机场订阅 URL
- Sub-Store Sync Token
- GitHub Token
- 私有 Gist 地址
- 任何包含认证信息的节点链接

这些内容应该保存在 Sub-Store、客户端本地配置或 GitHub Actions Secrets 中。
