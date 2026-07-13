# Memory Service — Agent Context

## 项目一句话
面向 AI 应用开发者的长期记忆服务(B2B2C 基础设施)。学习 + 简历项目,
开发者是墨尔本大学 CS 本科生,目标岗位:AI Agent / LLM 应用工程师。

## 架构速览
FastAPI + PostgreSQL(pgvector) + Redis(Streams 队列)。
核心不对称:**同步读(search, P95<100ms)/ 异步写(extraction → conflict resolution)**。
读路径 fail-open;写入保守(低置信度降级 ADD);全量 audit log。
详见 docs/blueprint.md,分阶段计划见 docs/roadmap.md。

## 常用命令
- 环境:`docker compose up -d` && `uv sync`
- 测试:`uv run pytest`
- 评测:`uv run python evals/run.py --suite <name>`
- 代码检查:`uv run ruff check . && uv run ruff format .`

## 开发约定
- Python 3.12,强制类型标注,ruff 格式化
- 重要设计决策 → 写 `docs/adr/NNN-title.md`(格式见 ADR-001)
- 每个开发 session 结束 → 提醒开发者更新 `docs/devlog.md`
- 学到新概念 → 提醒记入 `docs/learning-notes.md`

## 协作模式(最重要,严格遵守)
本项目以学习为核心目标,开发者需要在面试中对核心模块的每个决定负责:

- **导师模式模块**(`src/core/` 下的 extraction / resolution / retrieval,以及 `evals/` 的评测逻辑):
  不要直接生成完整实现。流程:先给出方案对比与原理讲解 → 开发者确认方向 →
  小步实现并解释每个关键决定 → 主动提出反例和边界情况让开发者思考。
  开发者写的代码以 review + 提问的方式辅导,不要默默重写。
- **直接生成模块**(`src/api/` 的 CRUD、demo/、dashboard/、配置、测试脚手架、CI):
  可以直接高效生成,无需教学。
- **禁止**:修改 `evals/ground_truth/` 下的任何文件(评测集冻结)。
- 判断标准:"这段代码如果面试官逐行问,开发者能否讲清每个决定?"
  不能 → 必须走导师模式。

## 语言
与开发者交流用中文(可中英混合,技术术语保留英文)。
