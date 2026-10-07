# Market Brief Prompt

生成式市场研究 prompt skill。模型从共享研究能力、市场机制和频率职责设计
完整任务，供同一个接收模型完成研究、分析、展望、写作与自审。

入口：[SKILL.md](skills/market-brief-prompt/SKILL.md)。复制整个
`skills/market-brief-prompt/` 目录即可安装。

```text
$market-brief-prompt 生成A股盘前研究prompt。
$market-brief-prompt 生成美股周度prompt，重点分析财报和利率。
$market-brief-prompt 生成2026年9月Crypto月度prompt，仅使用月末前公开信息。
$market-brief-prompt 优化这份旧prompt，保留研究深度并简化重复指令。
```

CN、US支持盘前/盘后/周度/月度；Crypto支持日报/周度/月度。prompt 和报告默认 CN 使用中文，其他市场使用英文；显式语言要求覆盖默认。
其他市场先用官方资料建立制度画像，再复用共享能力与相应频率。

`references/` 是生成规则主体；`assets/prompts/` 的11份手写prompt作为对照组，
`initial-prompts/` 保留相同仓库副本。生成独立起草，比较时再检验实质职责得失。

后市展望围绕研究中的核心未决问题形成具体判断、机制和观察方向。输出采用正向
任务要求，时间与行情在执行时核验。模型与effort在执行环境配置。

[功能设计](design-docs/market-brief-skill-design.md)与
[技术设计](design-docs/market-brief-skill-architecture.md)说明模块、生成、维护与演进。
生成样例、比较和迭代保存在忽略的 `temp/`。本地prompt覆盖检查与实际研究报告质量
分开验收。项目保持一个skill与Markdown资源，无需模型客户端或调度服务。
