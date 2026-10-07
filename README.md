# Market Brief

可移植市场研究 skill：宿主 agent 完成检索、核验、分析与报告交付；一个
Python 标准库 helper 处理时间窗口、收益复算和研究记录检查。无模型客户端、
数据库或常驻服务。

当前是第一批本地实现。CN/US/Crypto 的 11 个原始任务已登记，研究规则按
资产、市场、频率加载；尚未安装到宿主，也未完成真实联网报告或模型配置应用验收。
原始 prompt 保留在 `initial-prompts/`，设计与架构在 `design-docs/`。

## 开发与使用

Python 3.11+，需要系统 IANA 时区数据；helper 无第三方依赖。

```sh
python3 -m unittest discover -s tests -v
python3 skills/market-brief/scripts/brief.py resolve tests/fixtures/crypto-daily/request.json
python3 skills/market-brief/scripts/brief.py check tests/fixtures/crypto-daily/run.json --brief tests/fixtures/crypto-daily/brief.md
```

fixture 是带明确标记的合成输入，用于测试契约，不是市场研究结果。
helper 的参数、JSON 字段和状态说明见
[记录契约](skills/market-brief/references/records.md)。退出码：0 成功、1 无效或检查失败、2 待确认。

独立 skill 根目录为 [skills/market-brief](skills/market-brief/SKILL.md)；安装时复制
整个目录到目标宿主的 skill 发现路径，不能只复制入口。运行记录保存在用户工作区，
安装目录不写入数据。本仓库的 `runs/` 和 `temp/` 默认不提交。

## 实现与验收边界

已实现：11 个稳定 task ID 与唯一档位表；逐步加载研究规则；给定时钟和日历的
时间解析；复利收益与流量日均；来源版本/引用关系/数字/正文和输入哈希检查；
请求与继承/实际执行结果分开记录。

待完成：首个真实联网报告与原始材料留存；每个任务的冻结研究案例和原 prompt
质量比较；Codex/Claude Code 宿主能力应用与回退实测；首个新增股票市场案例。
helper 尚不解析 wtd/mtd、自定义区间和未来完整期的提前版。静态检查通过不代表
经济判断正确、实际模型切换成功或真实交付完成。
