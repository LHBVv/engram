# Evaluation(评测方案与结果)

> 本文档是简历数字的出处与证据链。方案先行(立项时定),结果随每轮评测更新。

## 为什么评测是本项目的一等公民

"做了一个记忆服务"是 demo;"冲突消解准确率 X%,hybrid 检索比纯向量 recall@5 提升 Y 个百分点"
才是简历硬货。评测体系本身(benchmark 构建、LLM-as-judge)也是学习目标与面试考点。

## 三条评测线

### 1. Extraction 质量
- **评测集**:自建标注集,≥100 段对话(覆盖:含明确事实 / 纯闲聊 / 混合 / 假设性讨论)
- **指标**:precision(抽出来的是不是该记的)、recall(该记的漏没漏)、噪音率(闲聊误抽率)
- **构建方式**:人工写 + LLM 辅助扩充后人工校对;ground truth 存 `evals/ground_truth/`(冻结,禁止 AI 修改)

### 2. Conflict Resolution 准确率
- **评测集**:合成冲突场景 ≥100 case,四类操作各有覆盖(UPDATE 类重点造:数值更新/状态翻转/部分更新)
- **指标**:操作类型判定 accuracy(整体 + 分类型混淆矩阵)、误删率(错误 UPDATE/DELETE 的比例,重点盯)
- **优势**:冲突是合成注入的,ground truth 天然存在,评测最干净

### 3. 端到端检索质量
- **评测集**:多会话用户历史 + QA 对(参考 LongMemEval 任务设计:单跳/多跳/时间推理/知识更新)
- **指标**:recall@k、MRR;对比组:naive 纯向量检索、全量历史塞 context(同时记录 token 成本)
- **目标产出**:质量-成本二维对比表

## 评测工程

- 入口:`uv run python evals/run.py --suite <extraction|resolution|retrieval>`
- 每轮结果追加到下方结果区,标注代码版本(git sha)与 prompt 版本
- LLM-as-judge 使用处需做抽样人工校验,报告 judge 与人工的一致率

## 结果记录区

| 日期 | git sha | suite | 关键指标 | 备注 |
|---|---|---|---|---|
| (待 Phase 3) | | | | |
