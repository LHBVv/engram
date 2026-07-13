# Blueprint — Memory Service 项目蓝图

> 本文档是系统设计的**当前正确版本**(活文档)。历史决策与备选方案见 `docs/adr/`。
> 最后更新:2026-07-13(v0.1 立项版)

---

## 1. 项目定位

**一句话**:面向 AI 应用开发者的长期记忆服务(Memory as a Service),让任何基于 LLM API 的应用获得跨会话、可管理、可审计的用户记忆能力。

**形态**:B2B2C 基础设施。开发者(B)通过 REST API 接入,终端用户(C)通过开发者的应用间接受益。

**项目性质**:学习 + 简历项目。优先级排序:核心模块的技术深度 > 可量化的评测结果 > 工程完整度 > 功能广度。

**差异化定位**(相对模型厂商自带记忆):
- 数据主权:记忆存储在接入方可控的位置,而非模型厂商黑盒
- 跨模型可移植:记忆层独立于模型层,切换 LLM 供应商不丢失记忆
- 可控可定制:记什么、记多久、冲突如何消解均可配置
- 可审计:完整的记忆变更历史(audit log)

**对标参考**:Mem0、Zep、Letta(取其核心思想,做简化但完整的实现)。

---

## 2. 核心设计原则

1. **同步读 / 异步写**:检索在对话延迟的关键路径上(目标 P95 < 100ms,不含 embedding 调用);写入(抽取+消解)在对话结束后异步处理,允许秒级延迟。这是全系统最重要的架构不对称。
2. **Fail-open 读路径**:记忆服务不可用时返回空结果,接入方降级为无记忆对话,绝不阻塞主链路。
3. **保守写入**:冲突判定置信度不足时,宁可 ADD(冗余)不可 UPDATE(误删信息)。所有变更可回溯。
4. **记忆是资产**:所有写操作落 audit log,支持导出,用户可查看/删除自己的记忆(GDPR 式能力)。

---

## 3. 系统架构

```
                        ┌─────────────────────────────┐
                        │      接入方 Agent 应用        │
                        └──────┬───────────────┬──────┘
                        (同步读)│               │(异步写)
                               ▼               ▼
                    ┌──────────────────────────────────┐
                    │        API Layer (FastAPI)        │
                    │  /search (sync)   /memories (写入 → 入队即返回)
                    └──────┬───────────────┬───────────┘
                           │               │
                ┌──────────▼─────┐   ┌─────▼──────────┐
                │ Retrieval      │   │ Redis Queue    │
                │ Engine         │   │ (按 user_id    │
                │ (混合检索+融合) │   │  分区保序)     │
                └──────────┬─────┘   └─────┬──────────┘
                           │               ▼
                           │      ┌────────────────────┐
                           │      │ Ingestion Worker    │
                           │      │ 1. Fact Extraction  │──▶ LLM (DeepSeek)
                           │      │ 2. Conflict         │──▶ LLM (DeepSeek)
                           │      │    Resolution       │
                           │      └────────┬───────────┘
                           │               │
                    ┌──────▼───────────────▼──────┐
                    │   PostgreSQL + pgvector      │
                    │  memories / audit_log /      │
                    │  vector index / FTS index    │
                    └──────────────────────────────┘
```

组件职责:

| 组件 | 职责 | 学习目标标记 |
|---|---|---|
| API Layer | 鉴权(API key)、参数校验、限流、读路径编排、写路径入队 | 外围 |
| Retrieval Engine | 混合检索(向量 + 全文 + 时间衰减)、分数融合、top-k | **核心** |
| Ingestion Worker | 消费队列,执行两阶段 pipeline | **核心** |
| Fact Extraction | 从对话中抽取候选事实(结构化输出),过滤不值得记的内容 | **核心** |
| Conflict Resolution | 候选事实 vs 已有记忆,判定 ADD/UPDATE/DELETE/NOOP | **核心** |
| Storage | 事实、向量、审计日志的持久化 | 外围 |
| Demo App | 极简聊天应用,自吃狗粮演示记忆价值 | 外围 |
| Dashboard | 可视化用户记忆库与变更历史 | 外围 |

> "核心"= 学习目标模块,AI 辅助开发时采用导师模式(见 AGENTS.md 协作约定)。

---

## 4. 数据模型(初版)

### memories 表
| 字段 | 类型 | 说明 |
|---|---|---|
| id | uuid | 主键 |
| user_id | text | 终端用户标识(接入方命名空间内) |
| tenant_id | text | 接入方标识(多租户隔离) |
| content | text | 事实文本,如"购房预算 600 万" |
| category | text | 可选分类(preference/fact/event...) |
| embedding | vector(1024) | 事实向量 |
| status | text | active / archived / deleted |
| confidence | float | 抽取置信度 |
| created_at / updated_at | timestamptz | |
| valid_from | timestamptz | 事实生效时间(支持时间推理的基础) |

### audit_log 表
| 字段 | 类型 | 说明 |
|---|---|---|
| id | bigserial | |
| memory_id | uuid | 关联记忆 |
| operation | text | ADD / UPDATE / DELETE / NOOP |
| old_content / new_content | text | 变更前后 |
| reason | text | LLM 给出的判定理由 |
| resolver_confidence | float | 冲突判定置信度 |
| source_message_ref | text | 触发本次变更的对话引用 |
| created_at | timestamptz | |

> 设计意图:audit_log 不仅是合规能力,也是评测冲突消解准确率的原始数据,以及 dashboard 演示"记忆演变"的数据源。

---

## 5. 核心模块设计要点

### 5.1 Fact Extraction(写入侧第一阶段)
- 输入:一段对话消息(user + assistant turns);输出:候选事实列表(JSON 结构化输出)
- 关键难点:**"什么不该记"与"该记什么"同等重要**——纯闲聊返回空列表,避免噪音淹没记忆库
- 策略:prompt 中明确可记忆类别(稳定偏好、个人事实、明确决定)与排除项(临时状态、假设性讨论、模型自己说的话);每条候选带 confidence
- 待决策(→ 未来 ADR):抽取粒度(原子事实 vs 复合陈述)、是否先用小模型/规则做 gating 省成本

### 5.2 Conflict Resolution(写入侧第二阶段)
- 对每条候选事实:向量检索 top-n 相似已有记忆 → LLM 判定操作类型
- 操作语义:
  - **ADD**:全新信息或与已有记忆互补("考虑福田" vs "偏好南山")
  - **UPDATE**:同一事实的新值("预算 600 万" 覆盖 "500 万"),旧记录归档
  - **DELETE**:显式否定("不再考虑南山")→ 标记失效
  - **NOOP**:重复信息,不落库
- 保守策略:resolver_confidence 低于阈值时降级为 ADD;阈值本身通过评测集调优(→ ADR)
- 已知最大质量风险:LLM 误判"不冲突为冲突"导致信息被错误覆盖 → audit log + 归档而非物理删除,保证可恢复

### 5.3 Hybrid Retrieval(读取侧)
- 三路信号:向量相似度(pgvector HNSW)+ 关键词(PostgreSQL FTS)+ 时间衰减(指数衰减因子)
- 融合:加权 RRF(Reciprocal Rank Fusion)起步,权重通过评测集调优
- 待决策(→ ADR):是否引入 rerank 模型;时间衰减对不同 category 是否用不同半衰期

---

## 6. API 设计草案(详见 docs/api.md)

```
POST /v1/memories          # 提交对话消息,异步处理,返回 job_id
GET  /v1/memories/search   # 同步检索,query + user_id → top-k 记忆
GET  /v1/memories          # 列出某用户全部记忆(dashboard 用)
DELETE /v1/memories/{id}   # 删除指定记忆(用户数据权利)
GET  /v1/memories/{id}/history  # 记忆变更历史
```

鉴权:Header `X-API-Key`,key 绑定 tenant_id。

---

## 7. 技术选型总览

| 层 | 选型 | 理由摘要(详见对应 ADR) |
|---|---|---|
| API 框架 | FastAPI (Python 3.12) | 异步原生、OpenAPI 自动生成、生态 |
| 存储 | PostgreSQL 16 + pgvector | 单库同时覆盖结构化+向量+全文,见 ADR-001 |
| 队列/缓存 | Redis (Streams) | 轻量、按 user_id 分区保序 |
| LLM | DeepSeek API | 成本、结构化输出支持、国内可用性 |
| Embedding | 待定(候选:BGE-M3 本地 / 通用 API) | → 未来 ADR |
| 包管理 | uv | 锁版本、跨平台一致 |
| 容器化 | Docker Compose | 三台机器环境一致的基础 |
| 部署 | 腾讯云服务器 + GitHub Actions CI/CD | 常驻 live demo |

---

## 8. 质量与评测(详见 docs/evaluation.md)

三个核心指标方向:
1. **Extraction 质量**:precision/recall(自建标注集)
2. **Conflict Resolution 准确率**:操作类型判定的 accuracy(合成冲突场景集,ground truth 天然存在)
3. **端到端检索质量**:recall@k / MRR,以及对比 baseline(全量塞 context / naive RAG)的效果与成本差异

参考基准:LongMemEval 的任务设计思想。

---

## 9. 明确不做(Scope 边界)

- 不做多模态记忆(仅文本)
- 不做记忆图谱(graph memory)——列为 Phase 5+ 可选扩展
- 不做计费系统、完整多租户管理后台
- 不做 SDK 多语言封装(仅 Python 示例 + REST 文档)
- Demo/Dashboard 保持薄壳,不投入超过总时间 15%
