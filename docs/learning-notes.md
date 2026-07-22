# Learning Notes(学习笔记)

> 与 devlog 的分工:devlog 记"做了什么",这里记"学会了什么"。
> 每学一个新概念,用费曼式的 2-3 段话写下自己的理解——写不出来说明还没懂。
> 每月蒸馏进 interview-qa.md。

## 索引(按 Phase 组织)

### Phase 0-1:基础设施
- [ ] Docker Compose 多服务编排与网络
- [ ] pgvector:向量在关系库中的存储与 HNSW 索引原理
- [ ] FastAPI 异步模型:async/await、依赖注入、生命周期
- [ ] uv:锁文件与跨平台依赖一致性
- 笔记：PostgreSQL和pgvector保存记忆、向量和audit log，Redis后续作为异步写入队列
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
