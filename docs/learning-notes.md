# Learning Notes(学习笔记)

> 与 devlog 的分工:devlog 记"做了什么",这里记"学会了什么"。
> 每学一个新概念,用费曼式的 2-3 段话写下自己的理解——写不出来说明还没懂。
> 每月蒸馏进 interview-qa.md。

## 索引(按 Phase 组织)

### Phase 0-1:基础设施
- [x] Docker Compose 多服务编排与网络
- [ ] pgvector:向量在关系库中的存储与 HNSW 索引原理
- [ ] FastAPI 异步模型:async/await、依赖注入、生命周期
- [x] uv:锁文件与跨平台依赖一致性

### Phase 2:核心 pipeline
- [ ] LLM 结构化输出:JSON mode / function calling 的机制与失败模式
- [ ] 消息队列语义:至少一次投递、幂等消费、按 key 分区保序
- [ ] Prompt 工程化:版本管理、回归测试

### Phase 3:检索与评测
- [ ] 混合检索:RRF 融合原理、为什么多路召回优于单路
- [ ] 时间衰减函数的设计
- [ ] 评测方法论:LLM-as-judge 的偏差与校准、recall@k / MRR 的含义
- [ ] LongMemEval 的任务设计思想

### Phase 4:交付
- [ ] CI/CD:GitHub Actions → 云服务器的部署流水线
- [ ] 生产部署基础:进程守护、HTTPS、日志与可观测性

---

## 笔记正文

(按学习顺序追加,每条格式:`### [日期] 概念名` + 自己的话解释 + 一个"如果面试官问我会怎么答"的要点)

### 2026-07-20 Docker Compose 多服务编排

Docker image 是创建容器的只读模板,container 是 image 的运行实例。`docker compose up -d` 会按同一份配置创建 PostgreSQL 和 Redis 容器、项目内部网络及持久化 volume。宿主机通过 `5432:5432`、`6379:6379` 访问容器;容器之间则通过 Compose service name 通信。volume 独立于容器生命周期,所以普通的 `docker compose down` 后数据仍可保留。

`running` 只代表容器进程存在,不代表服务已经可以接收请求。PostgreSQL healthcheck 使用 `pg_isready` 检查数据库是否真正就绪。本项目用 PostgreSQL + pgvector 持久化记忆和向量,Redis 后续作为异步 ingestion 的消息队列。

**如果面试官问**:Compose 的价值不只是少敲几条启动命令,而是把多服务的镜像、端口、网络、健康检查和持久化配置版本化,使不同开发机能够复现同一套基础设施。

### 2026-07-20 uv 与可复现依赖

`pyproject.toml` 声明项目需要哪些依赖及允许的版本范围,`uv.lock` 记录解析后的精确版本,`.venv` 是依赖实际安装的位置。`uv sync` 让本地环境与项目声明保持一致,`uv run <command>` 则保证命令在项目虚拟环境中运行,避免误用系统 Python。

**如果面试官问**:只提交依赖范围不能保证不同机器安装到相同版本;lock 文件把完整依赖图固定下来,配合 `uv sync --locked` 可在开发机和 CI 中复现一致环境。lock 文件应由 uv 生成,不应手工维护。

### 2026-07-20 外部 API 最小链路验证

DeepSeek 检查脚本从 `.env` 读取 API key,在 HTTP `Authorization: Bearer <key>` header 中完成认证,并向 `/chat/completions` 发送包含 model 和 messages 的 JSON。HTTP 200 与可解析的模型回复共同证明配置读取、网络连接、认证、请求格式和响应解析这条最小链路可用。`.env` 被 Git 忽略,避免密钥进入版本库。

**如果面试官问**:初始化阶段先做最小 API smoke test,可以在业务 pipeline 之前隔离验证外部依赖,以后出现故障时更容易判断是供应商/API 配置问题还是业务代码问题。
