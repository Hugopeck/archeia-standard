---
title: arXiv — AI Engineering (2026 Selection)
date: 2026-05-01
tags: [context-engineering, harness-engineering, agent-scaffolding, multi-agent, autonomous-coding, evaluation]
---

# arXiv — AI Engineering: 2026 Selected Papers

Curated arXiv papers from 2026 that are directly relevant to Archeia's design decisions. Each entry is classified by how it bears on the project: papers under **Narrative support** substantiate design choices when explaining Archeia to users; papers under **Technical direction** inform implementation decisions internally.

---

## Quick reference

| # | Authors | Title (short) | Tag | arXiv |
|---|---|---|---|---|
| 1 | Mohsenimofidi et al. | Context engineering improves agent outcomes | `context-engineering` | [2510.21413](https://arxiv.org/abs/2510.21413) |
| 2 | Gloaguen et al. | Bloated context files hurt agent performance | `context-engineering` `evaluation` | [2602.11988](https://arxiv.org/abs/2602.11988) |
| 3 | Li et al. | Curated skills beat broad self-generated context | `agent-scaffolding` `evaluation` | [2602.12670](https://arxiv.org/abs/2602.12670) |
| 4 | Feng et al. | Long-horizon autonomy is still weak | `autonomous-coding` `evaluation` | [2602.14337](https://arxiv.org/abs/2602.14337) |
| 5 | Vasilopoulos | Codified context is feasible in complex repos | `context-engineering` `semi-autonomous-repos` | [2602.20478](https://arxiv.org/abs/2602.20478) |
| 6 | Chen et al. | Quality ≠ token length | `context-engineering` | [2602.13517](https://arxiv.org/abs/2602.13517) |
| 7 | Charakorn et al. | Context compression for repeated-query workflows | `context-engineering` `harness-engineering` | [2602.15902](https://arxiv.org/abs/2602.15902) |
| 8 | Sivakumaran et al. | Faithful reasoning traces for explanation quality | `agent-scaffolding` | [2602.16154](https://arxiv.org/abs/2602.16154) |
| 9 | Wang et al. | Dynamic multi-agent topology for efficiency | `multi-agent` `orchestration` | [2602.17100](https://arxiv.org/abs/2602.17100) |
| 10 | Guo et al. | Tool description quality is a first-order lever | `agent-scaffolding` `harness-engineering` | [2602.20426](https://arxiv.org/abs/2602.20426) |
| 11 | Yu et al. | Dynamic talent markets beat static agent teams | `multi-agent` `orchestration` | [2604.22446](https://arxiv.org/abs/2604.22446) |
| 12 | Bai et al. | Agentic coding token costs are high-variance | `evaluation` `autonomous-coding` | [2604.22750](https://arxiv.org/abs/2604.22750) |
| 13 | Su et al. | Skill loading is indiscriminate without curation | `agent-scaffolding` `harness-engineering` | [2604.24594](https://arxiv.org/abs/2604.24594) |
| 14 | Xu et al. | Structured hierarchical memory aids long-horizon reasoning | `context-engineering` `memory` | [2604.21748](https://arxiv.org/abs/2604.21748) |
| 15 | Yi et al. | Internalized debate matches explicit debate at 7% of token cost | `multi-agent` `harness-engineering` | [2604.24881](https://arxiv.org/abs/2604.24881) |
| 16 | Nathani et al. | Proactive agents need stateful evaluation environments | `evaluation` `agent-scaffolding` | [2604.00842](https://arxiv.org/abs/2604.00842) |

---

## Narrative support

Papers that substantiate Archeia's core design thesis when communicating with users, contributors, or evaluators.

---

### 1 — Context engineering improves agent outcomes

**Mohsenimofidi et al. (2025)**
*Context Engineering for AI Agents in Open-Source Software*
`context-engineering`
[arXiv:2510.21413](https://arxiv.org/abs/2510.21413)

**Relevance:** Direct empirical support for Archeia's foundational claim — that structured, high-quality repository context materially improves coding-agent performance. Use this when explaining why `.archeia/` exists at all.

---

### 2 — Bloated context files hurt agent performance

**Gloaguen et al. (2026)**
*Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?*
`context-engineering` `evaluation`
[arXiv:2602.11988](https://arxiv.org/abs/2602.11988)

**Relevance:** Context must be current, minimal, and decision-relevant. Unnecessary or stale requirements reduce agent success rates and increase cost. Directly supports Archeia's curation discipline and its `last_verified` hygiene conventions.

---

### 3 — Curated skills beat broad self-generated context

**Li et al. (2026)**
*SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks*
`agent-scaffolding` `evaluation`
[arXiv:2602.12670](https://arxiv.org/abs/2602.12670)

**Relevance:** Reinforces Archeia's high-signal curation stance over documentation sprawl. Curated, well-scoped skills outperform broad self-generated context across task types.

---

### 4 — Long-horizon autonomy is still weak; explicit guidance matters

**Feng et al. (2026)**
*LongCLI-Bench: A Preliminary Benchmark and Study for Long-horizon Agentic Programming in Command-Line Interfaces*
`autonomous-coding` `evaluation`
[arXiv:2602.14337](https://arxiv.org/abs/2602.14337)

**Relevance:** Supports Archeia's design choices around explicit decision traceability, staged guidance, and human approval checkpoints. Agents operating autonomously over long horizons still fail without structured intermediate anchors.

---

### 5 — Codified context infrastructure is feasible in complex repos

**Vasilopoulos (2026)**
*Codified Context: Infrastructure for AI Agents in a Complex Codebase*
`context-engineering` `semi-autonomous-repos`
[arXiv:2602.20478](https://arxiv.org/abs/2602.20478)

**Relevance:** Practical evidence that layered, persistent context can sustain multi-session consistency in a real production codebase. The closest existing case study to what Archeia proposes.

> **Caveat:** Observational single-project case study — treat as existence proof, not benchmark.

---

### 11 — Dynamic talent markets beat static multi-agent teams

**Yu et al. (2026)**
*From Skills to Talent: Organising Heterogeneous Agents as a Real-World Company*
`multi-agent` `orchestration`
[arXiv:2604.22446](https://arxiv.org/abs/2604.22446)

**Relevance:** Archeia currently treats skills as static bundles assigned to agents at configuration time. This paper's finding — that portable "Talents" (bundled skills/tools) recruited dynamically via a market achieve +15.5 points over fixed-topology SOTA on PRDBench — directly challenges that assumption. Informs the next revision of the execution domain's agent roster model.

---

### 12 — Agentic coding token costs are high-variance and poorly predicted

**Bai et al. (2026)**
*How Do AI Agents Spend Your Money? Analyzing and Predicting Token Consumption in Agentic Coding Tasks*
`evaluation` `autonomous-coding`
[arXiv:2604.22750](https://arxiv.org/abs/2604.22750)

**Relevance:** Agents consume ~1000× more tokens than chat or reasoning modes, with 30× run-to-run variance that is uncorrelated with output quality. This is empirical evidence for Archeia's context minimalism: pre-structured, stable context reduces the variance that causes runaway token spend without improving results. The finding also argues against dynamically generated context at agent invocation time.

---

### 13 — Skill loading is indiscriminate without explicit curation

**Su et al. (2026)**
*Skill Retrieval Augmentation for Agentic AI*
`agent-scaffolding` `harness-engineering`
[arXiv:2604.24594](https://arxiv.org/abs/2604.24594)

**Relevance:** SRA-Bench shows agents load skills regardless of relevance or need — the bottleneck has shifted from retrieval to *incorporation* (knowing when and which skill to use). This directly validates Archeia's curation discipline over large skill libraries and informs the description schema in MCP skill definitions: skill scope must be precise enough that an agent can determine relevance without loading it first.

---

## Technical direction

Papers that inform internal implementation choices — how Archeia is built, what patterns it adopts, what future extensions are worth pursuing.

---

### 6 — Quality is not proportional to token length

**Chen et al. (2026)**
*Think Deep, Not Just Long: Measuring LLM Reasoning Effort via Deep-Thinking Tokens*
`context-engineering`
[arXiv:2602.13517](https://arxiv.org/abs/2602.13517)

**Relevance:** Optimize for high-signal context and measurable outcome quality, not token volume. Directly argues against accumulating context indiscriminately — Archeia's conciseness constraints are on the right side of the evidence.

---

### 7 — Context compression for repeated-query workflows

**Charakorn et al. (2026)**
*Doc-to-LoRA: Learning to Instantly Internalize Contexts*
`context-engineering` `harness-engineering`
[arXiv:2602.15902](https://arxiv.org/abs/2602.15902)

**Relevance:** Potential future technique for lowering latency and cost in MCP-based and multi-step workflows where the same context is queried repeatedly across sessions.

---

### 8 — Faithful reasoning traces for explanation quality

**Sivakumaran et al. (2026)**
*Balancing Faithfulness and Performance in Reasoning via Multi-Listener Soft Execution*
`agent-scaffolding`
[arXiv:2602.16154](https://arxiv.org/abs/2602.16154)

**Relevance:** Rationale generation in agent outputs should be verifiable and faithful, not merely fluent. Informs how Archeia should structure decision records and ADRs that agents produce.

---

### 9 — Dynamic multi-agent topology for efficiency and quality

**Wang et al. (2026)**
*AgentConductor: Topology Evolution for Multi-Agent Competition-Level Code Generation*
`multi-agent` `orchestration`
[arXiv:2602.17100](https://arxiv.org/abs/2602.17100)

**Relevance:** Future orchestration reference for Archeia distributions that need to manage quality/cost tradeoffs across dynamically composed agent teams.

---

### 10 — Tool and skill interface quality is a first-order lever

**Guo et al. (2026)**
*Learning to Rewrite Tool Descriptions for Reliable LLM-Agent Tool Use*
`agent-scaffolding` `harness-engineering`
[arXiv:2602.20426](https://arxiv.org/abs/2602.20426)

**Relevance:** Directly informs MCP skill schema design and tool description conventions. Tool description quality is not cosmetic — it is a primary determinant of agent reliability.

---

### 14 — Structured hierarchical memory supports Archeia's temporal model

**Xu et al. (2026)**
*StructMem: Structured Memory for Long-Horizon Behavior in LLMs*
`context-engineering` `memory`
[arXiv:2604.21748](https://arxiv.org/abs/2604.21748)

**Relevance:** Temporal anchoring + periodic consolidation into relational structure improves multi-hop and temporal reasoning while reducing token overhead compared to flat or graph-based memories. This mirrors Archeia's `TEMPORAL_MODEL.md` design — living documents are consolidated over time, episodic records accumulate rather than sprawl — and provides empirical grounding for that choice.

---

### 15 — Internalized debate matches explicit debate at 7% of token cost

**Yi et al. (2026)**
*Latent Agents: A Post-Training Procedure for Internalized Multi-Agent Debate*
`multi-agent` `harness-engineering`
[arXiv:2604.24881](https://arxiv.org/abs/2604.24881)

**Relevance:** Two-stage distillation (debate structure + internalization) achieves equivalent or better outcomes to explicit multi-agent debate while using up to 93% fewer tokens. For Archeia distributions that rely on multi-agent deliberation patterns, this sets a cost benchmark to design toward and suggests internalization as a long-run efficiency path once orchestration patterns mature.

---

### 16 — Proactive agents require stateful, environment-aware evaluation

**Nathani et al. (2026)**
*Proactive Agent Research Environment (PARE)*
`evaluation` `agent-scaffolding`
[arXiv:2604.00842](https://arxiv.org/abs/2604.00842)

**Relevance:** FSM-based app modeling enables realistic testing of goal inference, timing, and multi-app orchestration beyond flat tool APIs. Informs how Archeia's execution domain should structure evaluation artifacts: stateful task descriptions that capture environment transitions, not only input/output pairs.
