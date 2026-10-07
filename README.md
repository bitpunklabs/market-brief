# Market Brief Prompt

生成完整市场研究 prompt 的 skill。选择并适配原始模板后，直接输出完整研究
prompt，供模型完成研究、核验、分析、展望、撰写与自审。

研究聚焦基本面及其市场定价反应。后市展望围绕前文核心问题，给出具体的大盘、
板块或主题判断与观察方向；前提和反证自然融入讨论，避免固定情景与时段清单。
技术分析不在研究范围内。

生成结果不附带模型选择、effort或执行配置交接说明。本仓库不包含模型客户端、
任务分级调度或报告运行框架。

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

`initial-prompts/` 维护从最初11份prompt演进的源模板，原版本保存在Git历史；
skill内的 `assets/prompts/` 是相同模板的可移植副本，维护时同步两处。
生成时完整保留研究方法、时间边界、市场
专属内容、章节、反证和后市展望，只按明确要求适配。

[功能设计](design-docs/market-brief-skill-design.md)与
[技术设计](design-docs/market-brief-skill-architecture.md)描述当前prompt生成架构。
原有任务分级、研究helper、运行记录契约及其测试已撤回；之前的实验结果仍在
忽略的 `temp/` 中，供历史对照，不作为当前功能。
