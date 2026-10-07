# Market Brief Prompt

生成完整市场研究 prompt 的 skill。选择并适配原始模板后，把整段 prompt
交给执行端可用的最高能力研究模型，以该模型支持的最高 reasoning effort
完成整份报告。研究、核验、分析、展望、撰写与自审共享同一上下文。

本项目的交付物是 prompt。模型与 effort 在执行端设置；prompt 文本不能替
宿主切换配置。本仓库不包含模型客户端、任务分级调度或报告运行框架。

入口：[skills/market-brief-prompt/SKILL.md](skills/market-brief-prompt/SKILL.md)。
安装时复制整个 `skills/market-brief-prompt/` 目录，包括模板资源。

例如：

```text
$market-brief-prompt 生成 A股盘前研究 prompt。
$market-brief-prompt 生成美股周度复盘 prompt，重点关注财报和利率。
$market-brief-prompt 生成2026年9月的Crypto月度复盘prompt，只使用月末前公开的信息。
```

支持A股、美股的盘前/盘后/周度/月度，以及Crypto的日报/周度/月度，共11种。
报告默认语言沿用原始模板，全部为中文；明确要求其他语言时统一调整。
未给日期或截止时，保留由执行模型在运行时核验的规则。

`initial-prompts/` 保留最初11份prompt原文；skill内的 `assets/prompts/` 是相同
模板的可移植副本，维护时同步两处。生成时完整保留研究方法、时间边界、市场
专属内容、章节、反证和后市展望，只按明确要求适配。

[功能设计](design-docs/market-brief-skill-design.md)与
[技术设计](design-docs/market-brief-skill-architecture.md)描述当前prompt生成架构。
原有任务分级、研究helper、运行记录契约及其测试已撤回；之前的实验结果仍在
忽略的 `temp/` 中，供历史对照，不作为当前功能。
