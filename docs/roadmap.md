# Roadmap — 20 天冲刺版

> 冲刺窗口:**2026-07-14 → 2026-08-02**(D1–D20)。
> 时间假设:前两周为假期全职投入(每天 6–8h),D15 之后与 semester 2 开学重叠,
> 故硬核开发全部前置,D15+ 只做交付与收尾。
> 每日站会替代品:当天结束更新 devlog + 勾选本文件的 checkbox。

## 冲刺总览

| 阶段 | 天数 | 主题 | 验收 |
|---|---|---|---|
| Sprint 1 | D1–D3 | 环境 + 最小读写闭环 | curl 存入→检索→命中,三机环境一致 |
| Sprint 2 | D4–D9 | 核心 pipeline(⭐重头)| 小王剧本端到端跑通 |
| Sprint 3 | D10–D14 | 检索升级 + 评测数字 | evaluation.md 有可写简历的数字 |
| Sprint 4 | D15–D18 | demo + 部署 + 门面 | live demo 可访问,README 成品 |
| Buffer | D19–D20 | 缓冲 + 面试手册蒸馏 | interview-qa 完整一轮 |

## 20 天 Scope 裁剪清单(相对原四月计划)

- ❌ 独立 Dashboard 应用 → 降级为 demo 内嵌的"记忆查看页"(表格 + 变更历史)
- ❌ 中文 FTS 分词(zhparser 坑深)→ 检索先做 向量 + 时间衰减 两路;FTS 列为 backlog
- ❌ 完整 CI/CD 流水线 → GitHub Actions 只跑测试;部署用一键脚本(deploy.sh)
- ✂️ 评测集规模:extraction 50 段 / conflict 50 case / retrieval 30 QA(诚实标注规模)
- ✂️ prompt 版本管理:降级为 prompt 文件进 git + evaluation.md 记录版本号
- ❌ rerank / 遗忘机制 / graph memory → backlog(gap period)

## 学习模式分级(20 天版,覆盖 AGENTS.md 默认约定)

- **导师模式(保持)**:conflict resolution、hybrid retrieval —— 面试拷打率最高的两块
- **半自主**:fact extraction —— prompt 由我设计与迭代,pipeline 代码可 AI 生成
- **全自主生成**:API 层、存储层、demo、部署脚本、测试脚手架

---

## Sprint 1:环境 + 最小闭环(D1–D3)

- [X] D1:GitHub 仓库建立;Win/Mac clone;docker compose 起 PG+Redis;uv 初始化;DeepSeek key 验证
- [ ] D2:建表(memories/audit_log)+ 迁移;embedding 选型速决(**ADR-002,限时 1 小时做决定**,建议直接用 API 型 embedding 避免本地模型部署开销)
- [ ] D3:FastAPI 骨架 + API key 鉴权;`POST /memories`(同步直存版)+ `GET /search`(纯向量);pytest 骨架 + Actions 跑测试
- **验收**:三条 curl 完成存→查→命中

## Sprint 2:核心 pipeline(D4–D9)⭐

- [ ] D4:Redis Streams 队列 + worker 骨架,写路径切异步(按 user_id 保序)
- [ ] D5–D6:Fact Extraction:prompt 设计(可记类别/排除项/confidence)、结构化输出、闲聊过滤;用 10 段自测对话快速迭代
- [ ] D7–D8:Conflict Resolution(导师模式):相似记忆召回 → ADD/UPDATE/DELETE/NOOP 判定 → 保守降级 → audit_log 落盘(**ADR-003:判定策略与阈值机制**)
- [ ] D9:端到端联调 + 补测试
- **验收**:小王健身教练剧本(膝伤→新会话规避→伤愈 UPDATE)跑通,audit_log 可见演变
- **风险预案**:若 D8 结束 resolution 准确率明显不行,D9 只修最大问题,剩余进 Sprint 3 用评测驱动修

## Sprint 3:检索升级 + 评测(D10–D14)⭐ 简历数字产出

- [ ] D10:混合检索(导师模式):向量 + 时间衰减,RRF 融合(**ADR-004:融合与衰减设计**)
- [ ] D11–D12:评测集构建:extraction 50 段 / conflict 50 case / retrieval 30 QA;ground_truth 冻结
- [ ] D13:评测 runner + 首轮全量跑分,记录 baseline
- [ ] D14:一轮评测驱动迭代(修最痛的一处),记录提升数字 → evaluation.md
- **验收**:evaluation.md 有 ≥2 个可写简历的数字(如 conflict accuracy、hybrid vs 纯向量的 recall 提升)

## Sprint 4:交付(D15–D18)⚠️ 与开学重叠,任务刻意轻量

- [ ] D15–D16:Demo 聊天应用(薄壳,含记忆查看页)
- [ ] D17:腾讯云部署(docker compose + deploy.sh + HTTPS/Caddy),live demo 上线
- [ ] D18:README 重写(架构图 + GIF + live 链接 + 数字);简历项目描述定稿
- **验收**:手机点开 live demo 能玩;README 30 秒讲清价值

## Buffer(D19–D20)

- [ ] interview-qa.md 完整蒸馏(把 ADR-002/003/004 + devlog 的坑全部转成 Q&A)
- [ ] 机动:处理 Sprint 1–4 的溢出项
- **若进度提前**:从 backlog 拉 FTS 或第二轮评测迭代

---

## 每日纪律(20 天版)

1. 当天最后 10 分钟:更新 devlog(2 分钟)+ 勾 roadmap checkbox
2. 遇到 >2 小时卡死的坑:记 devlog 后**绕行或降级**,不死磕(20 天没有死磕预算)
3. ADR 限时:每个决策文档 ≤30 分钟,写要点不写论文
4. 每个 Sprint 结束问一次:"落后了吗?" → 落后就从裁剪清单再砍,**永远保 Sprint 3 的评测数字**(它是简历硬通货,demo 好不好看是次要的)

## Backlog(gap period / 12 月后)

FTS + 中文分词、rerank、遗忘机制、graph memory、压测报告、完整 CI/CD、与 AIOps 项目集成

## 变更记录

| 日期 | 变更 |
|---|---|
| 2026-07-13 | v0.1 四月计划初版 |
| 2026-07-13 | v0.2 改为 20 天冲刺版,scope 裁剪见上 |
