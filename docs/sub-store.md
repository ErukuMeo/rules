# Sub-Store 接入说明

本仓库负责维护和发布规则，Sub-Store 负责组装节点订阅和输出多端配置。两者不要混在一起：规则可以公开放在 GitHub，节点订阅和 Token 应该留在 Sub-Store 或本地。

## 职责划分

GitHub 仓库：

- 维护源规则：`source/rules.json`
- 生成规则产物：`dist/`
- 发布 Raw GitHub URL
- 通过 CI 校验 `source/` 和 `dist/` 是否同步

Sub-Store：

- 导入一个或多个机场/节点订阅
- 按地区、协议、倍率、名称或脚本过滤节点
- 统一节点命名和排序
- 建立客户端需要的策略组
- 输出 Android、iOS、Windows、Linux、macOS 可用的订阅或完整配置
- 引用本仓库生成的规则或模板片段

## 初次配置

1. 编辑 `source/rules.json`。
2. 确认仓库字段为：

```json
{
  "owner": "ErukuMeo",
  "name": "rules",
  "branch": "main"
}
```

3. 本地生成规则：

```bash
python scripts/generate_rules.py
```

4. 推送到 GitHub。
5. 在 Sub-Store 模板或脚本中引用：

```text
dist/sub-store/rule-urls.json
dist/templates/sub-store/rule-urls.md
```

## 策略组命名

保持 Sub-Store、生成规则和客户端模板中的策略组名称一致：

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

规则只负责把请求分到这些策略组；每个策略组背后的节点由 Sub-Store 管理。

## 推荐使用流程

1. 在 Sub-Store 中导入节点订阅。
2. 用 Sub-Store 的重命名和脚本能力清洗节点名。
3. 根据地区或用途创建策略组，例如 `PROXY`、`AI`、`STREAMING`。
4. 生成客户端基础配置。
5. 根据客户端类型合并本仓库的生成模板：

```text
Mihomo:  dist/templates/mihomo/profile-fragment.yaml
sing-box: dist/templates/sing-box/route-fragment.json
```

6. 客户端订阅 Sub-Store 输出的最终配置。
7. 后续只修改 `source/rules.json`，重新生成并推送后，客户端更新订阅即可获得新规则。

## Mihomo / Clash.Meta

可直接引用：

```text
dist/templates/mihomo/profile-fragment.yaml
```

这个片段包含：

- `rule-providers`
- `rules`
- 每个分类对应的远程 rule provider URL

如果你想拆开使用，也可以引用：

```text
dist/mihomo/rule-providers.yaml
dist/mihomo/rules.yaml
dist/mihomo/rules/<category>.yaml
```

## Surge / Loon / Quantumult X

使用分类规则列表：

```text
dist/surge/<category>.list
dist/loon/<category>.list
dist/quantumultx/<category>.list
```

每条规则已包含策略组，例如：

```text
DOMAIN-SUFFIX,openai.com,AI
```

## sing-box

可直接引用：

```text
dist/templates/sing-box/route-fragment.json
```

这个片段包含：

- remote `rule_set`
- `rules`
- `final`

分类规则集位于：

```text
dist/sing-box/rule-set/<category>.json
```

这些文件当前是 source rule-set JSON。如果客户端要求 `.srs`，后续需要增加 sing-box 编译步骤。

## 安全注意事项

不要提交以下内容：

- 机场订阅 URL
- Sub-Store Sync Token
- GitHub Token
- 私有 Gist 地址
- 包含认证信息的节点链接

这些敏感信息应保存在 Sub-Store、客户端本地配置或 GitHub Actions Secrets 中。
