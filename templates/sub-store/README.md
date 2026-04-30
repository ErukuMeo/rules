# Sub-Store 模板说明

`templates/` 目录中的文件是静态参考，便于手工查看结构。日常接入时优先使用 `dist/templates/`，因为它们由 `source/rules.json` 自动生成，会跟随仓库地址、分类顺序和策略组变化。

## 推荐流程

1. 在 Sub-Store 中创建或导入节点订阅。
2. 清洗节点名称，并按地区、倍率、协议或可用性过滤。
3. 创建策略组：`AI`、`STREAMING`、`APPLE`、`MICROSOFT`、`PROXY`、`DIRECT`、`REJECT`、`FINAL`。
4. Mihomo / Clash.Meta 客户端引用或合并：

```text
dist/templates/mihomo/profile-fragment.yaml
```

5. sing-box 客户端将下面片段合并到配置的 `route` 对象：

```text
dist/templates/sing-box/route-fragment.json
```

6. 需要 URL 总表时查看：

```text
dist/templates/sub-store/rule-urls.md
dist/sub-store/rule-urls.json
```

不要提交机场订阅、Token、私有 Gist 地址或任何包含认证信息的节点链接。
