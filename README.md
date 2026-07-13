# Engram

> Long-term memory as a service for LLM applications — selective fact extraction,
> conflict resolution, and hybrid retrieval, exposed as a simple REST API.

*An **engram** is the physical trace a memory leaves in the brain — this service is that trace for your AI application.*

**Status: 🚧 Phase 0 (project setup) — see [roadmap](docs/roadmap.md)**

## Why

LLM APIs are stateless. Every AI application team ends up hand-rolling the same thing:
deciding *what* to remember about each user, resolving contradictions when facts change,
and retrieving the right memories fast enough for the conversation loop.
This project packages that into a standalone service — the memory layer stays
**model-agnostic, self-hosted, and auditable** (your users' memory is your asset,
not your LLM vendor's).

## Core design

- **Sync read / async write**: retrieval sits on the conversation's latency-critical
  path (target P95 < 100ms); extraction + conflict resolution run async after the turn ends.
- **Two-stage ingestion**: fact extraction (what's worth remembering) →
  conflict resolution (ADD / UPDATE / DELETE / NOOP against existing memories,
  with conservative fallback and full audit history).
- **Hybrid retrieval**: vector similarity + full-text + time decay, fused with RRF.

Architecture details: [docs/blueprint.md](docs/blueprint.md)

## Stack

FastAPI · PostgreSQL + pgvector · Redis Streams · DeepSeek API · Docker Compose · uv

## Quickstart

```bash
docker compose up -d
uv sync
uv run uvicorn src.api.main:app --reload
# interactive API docs at http://localhost:8000/docs
```

(Full integration guide: [docs/api.md](docs/api.md))

## Project docs

| Doc | Purpose |
|---|---|
| [blueprint](docs/blueprint.md) | Architecture & design (living doc) |
| [ADRs](docs/adr/) | Decision records with trade-offs |
| [roadmap](docs/roadmap.md) | Phased plan & milestones |
| [evaluation](docs/evaluation.md) | Benchmarks & measured results |

---

*A learning-focused portfolio project. Evaluation numbers and live demo will land here as phases complete.*
