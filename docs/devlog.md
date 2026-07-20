# Devlog(开发日志,append-only)

> 每次开发 session 结束追加一条,格式:日期 | 做了什么 | 卡点 | 下一步。
> 目的:进度自我管理 + 面试素材("你遇到过最难的问题"的答案都在这里)。

---

## 2026-07-13
- **做了什么**:正式立项。确定选题(记忆服务)、完成文档体系设计、生成项目骨架与全部文档初稿(blueprint / roadmap / ADR-001 等)。明确"学习为核心"的定位与 AI 辅助开发的协作规范(核心模块导师模式)。
- **卡点**:无。
- **下一步**:建 GitHub 仓库,三台机器打通;写 docker-compose.yml 并在 Win/Mac 验证;申请/配置 DeepSeek API key。

## 2026-07-20
- **做了什么**:完成 D1 环境初始化。使用 Docker Compose 启动 PostgreSQL 16 + pgvector 与 Redis 7,确认 PostgreSQL healthcheck 为 healthy、pgvector 0.8.5 已启用、Redis 返回 PONG;使用 uv 同步 Python 依赖;通过最小 HTTP 请求验证 DeepSeek API key 可用。项目本地基础设施与外部 LLM 调用链路均已打通。
- **卡点**:最初 Docker Desktop daemon 未启动,导致 CLI 无法连接 Docker socket;启动 Docker Desktop 后解决。`uv sync` 发现 lock 文件中的旧项目名 `memory-service` 与 `pyproject.toml` 的 `engram` 不一致,已自动同步 lock 内容。
- **下一步**:进入 D2。限时完成 ADR-002 embedding 选型,确定向量维度;随后引入 SQLAlchemy/Alembic,创建 memories 与 audit_log 的首个数据库迁移。
