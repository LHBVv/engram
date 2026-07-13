# API 文档

> 原则:API reference 由 FastAPI 自动生成(服务启动后访问 `/docs`),本文件只写
> **概念说明 + Quickstart**,不手工维护接口细节。

## 核心概念

- **Memory(记忆)**:一条关于终端用户的原子事实,如"购房预算 600 万"。有生命周期:active → archived/deleted。
- **记忆的生命周期**:对话消息提交 → 事实抽取 → 冲突消解(ADD/UPDATE/DELETE/NOOP)→ 落库;每次变更进 audit log。
- **租户与用户**:`tenant_id`(接入方,由 API key 绑定)+ `user_id`(接入方自己的用户标识),两级隔离。
- **读写语义**:`search` 同步(设计目标 P95 < 100ms);`memories` 写入异步(提交即返回 job_id,秒级完成处理)。读路径 fail-open。

## Quickstart(三步接入)

```bash
# 1. 对话结束后,提交消息(异步)
curl -X POST https://<host>/v1/memories \
  -H "X-API-Key: $KEY" -H "Content-Type: application/json" \
  -d '{"user_id": "user_123", "messages": [
        {"role": "user", "content": "我膝盖有旧伤,别给我安排深蹲"},
        {"role": "assistant", "content": "好的,已了解"}]}'

# 2. 下次对话前,检索相关记忆(同步)
curl "https://<host>/v1/memories/search?user_id=user_123&query=腿部训练计划&top_k=5" \
  -H "X-API-Key: $KEY"

# 3. 把返回的记忆注入你的 prompt
```

## 端点总览

| 方法 | 路径 | 语义 | 同步性 |
|---|---|---|---|
| POST | /v1/memories | 提交对话消息,触发抽取 pipeline | 异步(返回 job_id)|
| GET | /v1/memories/search | 混合检索 top-k 相关记忆 | 同步 |
| GET | /v1/memories | 列出用户全部记忆(分页) | 同步 |
| DELETE | /v1/memories/{id} | 删除记忆(用户数据权利) | 同步 |
| GET | /v1/memories/{id}/history | 记忆变更历史 | 同步 |

(字段级细节以 `/docs` 的 OpenAPI 为准)
