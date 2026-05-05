---
title: Harness Engineering — Synthesis of Seven Foundational Sources
source: synthesis
date: 2026-05-01
tags: [harness-engineering, agent-scaffolding, context-engineering, autonomous-coding, multi-agent, orchestration]
---

# Harness Engineering — Synthesis of Seven Foundational Sources

A consolidated read of six primary sources on agent harness design, published between October 2025 and April 2026 by Cursor, Anthropic, OpenAI, and Stanford/SambaNova. The first half summarizes each source on its own terms; the second half extracts shared principles that recur across multiple sources; the appendix is a unifying glossary that reconciles overlapping vocabulary.

## Sources covered

1. **Cursor — *Continually Improving Our Agent Harness*** (2026-04-30)
2. **Anthropic — *Scaling Managed Agents: Decoupling the Brain from the Hands*** (2026-04-08)
3. **Anthropic — *Building a C Compiler with a Team of Parallel Claudes*** (2026-02-05)
4. **OpenAI — *Harness Engineering: Leveraging Codex in an Agent-First World*** (early 2026)
5. **Anthropic — *Effective Harnesses for Long-Running Agents*** (2025-11-26)
6. **Zhang et al. — *Agentic Context Engineering* (ACE), arXiv:2510.04618** (2025-10)

---

## 1. Source-by-source summaries

### 1.1 Cursor — Continually Improving Our Agent Harness

**Thesis.** The harness — not the underlying model — is now the dominant lever for agent quality, and it must be developed like a continuously shipping product, with vision, A/B tests on real usage, and per-model customization underneath model-agnostic abstractions.

**Definition of *harness*.** The infrastructure surrounding LLM interactions: system prompts and tool descriptions, static and dynamic context window management, tool provisioning and error handling, and model-specific customizations. It is the *orchestration layer*, not the agent itself.

**Key techniques.**
- **Dynamic context discovery** — the agent pulls past conversations, terminal sessions, and tools "while it works" rather than pre-loading static context.
- **Keep rate** — measure what fraction of generated code remains in the user's codebase after fixed intervals.
- **Error taxonomy** — distinguish unknown errors (real bugs) from expected errors (`InvalidArguments`, `UnexpectedEnvironment`, `ProviderError`); fire anomaly alerts when the expected-error baseline is exceeded per-tool, per-model.
- **Per-model tool format** — OpenAI models get patch-based file edits; Claude gets string replacement; each model is provisioned with the tool format it had during training.
- **Mid-chat model switching is costly** — staying on one model per conversation avoids cache-miss penalties.
- **One model exhibited "context anxiety"** — refusing work as the window filled — and was patched at the prompt layer.

### 1.2 Anthropic — Scaling Managed Agents (decoupling the brain from the hands)

**Thesis.** Harnesses encode assumptions about what the model cannot do on its own, and those assumptions go stale as models improve — so build the *meta-harness* around stable interfaces that let the harness, the execution environment, and the event log evolve independently.

**Three decoupled components.**
- **Session** — an append-only log of all events, living *outside* the model's context window. Accessed via `getEvents()` so the harness can transform slices before passing them in, instead of making irreversible compaction decisions.
- **Harness** — the loop that calls the model and routes tool calls. Encodes assumptions about model limitations.
- **Sandbox** — the execution environment. Called via `execute(name, input) → string`, so containers are "cattle, not pets" and "the harness doesn't know whether the sandbox is a container, a phone, or a Pokémon emulator."

**Concrete payoffs.**
- Time-to-first-token improved ~60% at p50 and >90% at p95 because container provisioning became lazy.
- Failed harnesses can resume any session via `wake(sessionId)`.
- Credentials never reach the sandbox where model-generated code runs — auth is bundled with resources at init or proxied through external vaults.
- Workarounds for Sonnet 4.5's "context anxiety" did not become architectural dead weight when Opus 4.5 eliminated the underlying behavior.

### 1.3 Anthropic — Building a C Compiler with Parallel Claudes

**Thesis.** Multiple model instances can autonomously co-author non-trivial systems software (a 100k-line Rust C compiler that builds Linux 6.9, QEMU, FFmpeg, SQLite, PostgreSQL, Redis, and Doom) — but only when the harness gives them an almost-perfect verifier and the right partitioning strategy.

**Key lessons.**
- **The verifier dominates everything.** "Claude will work autonomously to solve whatever problem I give it. So it's important that the task verifier is nearly perfect." Bad tests cause optimization for the wrong objective.
- **Output formatting is for grep, not humans.** Errors and progress are designed for automated parsing.
- **Naive parallelism converges.** On monolithic tasks, agents produce identical solutions and merge-conflict; the fix was using GCC as an *oracle* to partition work file-by-file.
- **File-based locks** prevent duplicate work across containers that mount a shared git repo.
- **Specialization beats homogeneity** — different agents owned dedup, performance, docs, and architecture.
- **Sustained autonomy** comes from a bash loop that respawns sessions without human intervention.
- **Deterministic 1–10% test sampling** maintains regression detection without polluting context.

**Scale.** ~$20,000 in API costs, ~2 billion input tokens, ~2,000 sessions. New features began breaking old ones — Opus 4.6 had reached the limit of what the harness could absorb.

### 1.4 OpenAI — Harness Engineering (Codex in an Agent-First World)

**Thesis.** When agents do most of the implementation, the engineering team's job becomes designing the *environment* the agents operate in. In a five-month internal trial, OpenAI engineers shipped a beta product of roughly a million lines of code "without any manually written source code," interacting with the system almost entirely through prompts.

**Core principles (recurring across coverage of the post).**
- **Context management** — organize and expose the right information rather than dumping ad-hoc instructions.
- **Boring technology** — composable, API-stable, training-set-represented stacks are easier for agents to model.
- **Mechanical enforcement** — custom linters and structural tests encode rules (structured logging, naming, file size, platform reliability) and inject remediation instructions back into the agent's context on failure.
- **Architecture as enabler** — strict dependency layering (Types → Config → Repo → Service → Runtime → UI) and modular boundaries are what let agents move fast without architectural drift.
- **Intent-based development** — engineers express *what* through declarative prompts; agents handle *how*.
- **Structured documentation as source of truth** — design specs, execution plans, and architectural maps are machine-readable, cross-linked, and CI-validated.
- **Autonomous feedback loops** — agents open PRs, evaluate changes, and iterate until acceptance criteria are met.
- **Observability-driven development** — agents use logs, metrics, and spans to reproduce bugs in isolated environments and validate fixes.

OpenAI frames the result this way (paraphrased across coverage): "Our most difficult challenges now center on designing environments, feedback loops, and control systems."

### 1.5 Anthropic — Effective Harnesses for Long-Running Agents

**Thesis.** Agents work in discrete sessions with no memory of previous work — "engineers working in shifts, where each new engineer arrives with no memory." Even Opus 4.5 cannot one-shot a production application from a high-level spec; structural support is required.

**The two-agent pattern.** Separate the **initialization phase** from the **coding phase**, each with its own prompt and entry protocol.

**Environment scaffolding for a claude.ai-style clone.**
- A **feature list file** of 200+ structured JSON entries with `passes: true/false`.
- A **progress file** documenting what each session accomplished.
- **Git history** for reverting failed attempts.
- An `init.sh` script that automates server startup.
- **Puppeteer MCP** for browser automation tests, with explicit end-to-end verification before any feature is marked complete.

**Session-start protocol.** Read progress file → check git log → run dev server → verify basic functionality → pick next unfinished feature.

**Failure modes the harness must defend against.** Premature victory declarations, undocumented bugs, incomplete testing, environment confusion.

### 1.6 ACE — Agentic Context Engineering (Zhang et al., arXiv:2510.04618)

**Thesis.** Adapt language models to tasks by evolving their *input context* — not their weights — through a structured, modular loop. Two failure modes drive the design:
- **Brevity bias** — iteratively summarized contexts drop domain-specific insights.
- **Context collapse** — repeated rewriting erodes detail over time.

**The loop.** Three integrated processes:
1. **Generation** — produce candidate context elements.
2. **Reflection** — evaluate and refine them.
3. **Curation** — organize, select, and structure them into evolving "playbooks" that "accumulate, refine, and organize strategies."

**Operates on two surfaces.** Offline contexts (system prompts) and online contexts (agent memory).

**Results.** +10.6% on agent benchmarks, +8.6% on finance tasks, matching production-level systems on the AppWorld leaderboard — and notably *without labeled supervision*, leveraging natural execution feedback. The framework "scales with long-context models" while reducing adaptation latency and rollout cost.

---

## 2. Shared principles

The six sources use different vocabulary and ship different products, but the same load-bearing ideas recur. Each principle below is supported by multiple sources.

### P1. The harness is software, and it ships continuously
Cursor (continually improving), Anthropic (managed agents — stable interfaces precisely so the harness inside can keep changing), OpenAI (the engineering team's primary job is environment design). The harness is not a fixture of the agent; it is the artifact most under active development. Treat it like any product: vision, instrumentation, A/B tests, error budgets.

### P2. Decouple the model from the environment
Anthropic Managed Agents makes this its central architectural claim — *brain*, *hands*, *session* are independently replaceable. OpenAI enforces an analogous separation through dependency layering (Types → Config → Repo → Service → Runtime → UI). Cursor's harness exposes model-agnostic abstractions with per-model adapters underneath. The decoupling protects against model churn and lets components fail (and be replaced) on their own.

### P3. Persistent state lives outside the context window
Managed Agents puts the session in an append-only log accessed via `getEvents()`. Anthropic's long-running harness uses progress files, feature-list JSON, and git history. ACE turns context into evolving playbooks that survive across runs. The model's window is treated as ephemeral working memory; durable state belongs in files, logs, and databases the harness owns.

### P4. Verification must approach perfection
The C-compiler post is blunt: "the task verifier [must be] nearly perfect," because the agent will optimize for whatever signal it receives. The long-running harness mandates end-to-end verification (Puppeteer) before any feature is marked complete. ACE turns natural execution feedback into a self-improvement signal — explicitly noting that this works "without labeled supervision" only because the feedback channel is reliable. The harness's job is not just to run the agent — it is to define *truth* for the agent.

### P5. Mechanical guardrails beat polite instructions
OpenAI's mechanical enforcement (custom linters, structural tests, file-size limits, structured-logging rules) injects remediation instructions back into the agent's context on failure. Anthropic's C-compiler harness uses file-based locks, deterministic test sampling, and grep-friendly error formatting; the long-running harness uses `init.sh`, structured feature-list JSON, and Puppeteer checks as gates. Whenever a rule can be expressed as code that fails loudly, prefer that to a sentence in a system prompt.

### P6. Context is curated, not stuffed
ACE names the failure modes — brevity bias and context collapse. OpenAI calls it "organizing and exposing the right information so the agent can reason over it, rather than overwhelming it with ad-hoc instructions." Cursor's continually-improving harness implements *dynamic context discovery* — pulling past conversations, terminal sessions, and tools "while it works" rather than pre-loading them. More tokens is not more signal.

### P7. Plan before doing
Anthropic's two-agent (init/coding) split and OpenAI's intent-based development with declarative prompts both separate the *what* and *how* into distinct phases with distinct prompts. The C-compiler experiment extends this to roles — agents specialized for dedup, performance, docs, and architecture each plan within their lane. Planning is not premature optimization; it is the cheapest place to catch the wrong problem.

### P8. Long sessions degrade — design for shifts, not marathons
Anthropic's "engineers in shifts" framing, ACE's protection against context collapse, Managed Agents' session-resume primitives, and Cursor's documented "context anxiety" failure mode all assume the *session is short and resumable*, not long and stateful. Build for the shift change.

### P9. Per-model fit is a real cost
Cursor provisions each model with the tool format it was trained on (OpenAI patches vs. Claude string replacement) and customizes prompts per-model. Mid-chat model switching incurs cache penalties; "context anxiety" was a model-specific bug requiring model-specific mitigation. The harness abstracts the *interface*, not the *idiosyncrasies*.

### P10. Production telemetry is the real benchmark
Cursor measures keep rate, classifies error types, and alerts on anomalies. OpenAI uses observability-driven development with logs/metrics/spans flowing back into agent reasoning. Anthropic's C-compiler harness emits grep-friendly errors. Benchmarks set ceilings; production telemetry tells you which way to push them.

### P11. Parallelism requires partitioning and an oracle
The C-compiler post is the canonical example: naive parallelism converged on identical solutions, and only a partitioning strategy (GCC as oracle, file-based locks, role specialization) made multi-agent work tractable. OpenAI's autonomous feedback loops (agents opening and evaluating PRs) imply a similar discipline. Multi-agent without partitioning is multi-conflict.

### P12. Boring, stable technology is agent-friendly
OpenAI explicitly names this: composability, API stability, and strong training-set representation make a stack legible to agents. The C-compiler success leans on Rust + git + bash — well-understood, well-represented technology. Novel frameworks add a tax the agent pays in mistakes.

---

## 3. Tensions worth watching

The sources do not fully agree, and the disagreements are informative.

- **How much to bake into the harness vs. the model.** Anthropic's Managed Agents argues *less* — keep the harness thin enough to discard, because today's workaround is tomorrow's dead weight. Anthropic's own long-running harness argues *more* — without explicit feature lists, progress files, and init scripts, even Opus 4.5 fails. The tension is real; the resolution is probably "thin where the model is improving, thick where the workflow is stable."
- **Up-front planning vs. dynamic discovery.** Anthropic's two-agent split and OpenAI's intent-based development front-load planning into a distinct phase; Cursor's continually-improving harness emphasizes pulling context dynamically as the agent works. Both are right at different scopes — plan the *task*, discover the *details*.
- **Specialization vs. generality.** The C-compiler experiment found that specialized agents (dedup, perf, docs, arch) outperformed generic ones; OpenAI's Codex setup leans on a more uniform agent population disciplined by the environment. The cost of specialization is harness complexity; the cost of generality is convergence and conflict.

---

## 4. Glossary — unifying the vocabulary

The same words mean different things across these sources. The definitions below are the ones used in this document; where a source uses a term differently, it is noted.

| Term | Definition (as used here) | Notes on cross-source variation |
|---|---|---|
| **Agent** | A model + the harness around it that gives it tools, memory, control flow, and an environment. | OpenAI's *Codex* refers both to the product and to individual agent instances within it. |
| **Harness** | Everything around the model that converts a single forward pass into useful work: the loop, the tools, the prompts, the context manager, the error taxonomy, the model-specific adapters. The orchestration layer. | OpenAI's framing: "Agent = Model + Harness." Anthropic's *Managed Agents* uses "harness" narrowly for the loop that calls the model and routes tool calls — sandbox and session are separate components alongside it. Cursor uses "harness" more broadly to include tool descriptions and prompts. |
| **Scaffold / Scaffolding** | The structural files and conventions of the project the agent works in: feature lists, progress files, READMEs, dependency layering, init scripts. | Anthropic's *Long-Running* post calls this "environment scaffolding." OpenAI calls similar artifacts "structured documentation architecture." Often used interchangeably with parts of "harness," but scaffolding lives in the *project*; the harness lives around the *model*. |
| **Sandbox** | The execution environment in which the model's generated code runs — typically a container, but in principle anything with an `execute(name, input) → string` interface. | Anthropic's *Managed Agents* makes this a first-class component, deliberately interchangeable. The C-compiler experiment uses Docker containers mounting a shared git repo. |
| **Session** | An append-only log of all events (model calls, tool calls, results) for a single piece of work. Lives outside the model's context window. | Anthropic's *Managed Agents* concept. The closest analogue in the long-running harness is the progress file plus git history. ACE's "online context" overlaps. |
| **Context window** | The token budget the model sees on a single forward pass. | All sources treat the window as ephemeral working memory and push durable state out of it. |
| **Context** | Everything passed to the model: system prompt, tool descriptions, conversation history, retrieved documents, scratchpad. | ACE distinguishes *offline context* (system prompts) from *online context* (agent memory). |
| **Context engineering** | The discipline of curating what enters the context window — what to include, exclude, compress, retrieve, or evolve over time. | Simon Willison's term, adopted by Anthropic and Stanford. ACE is the operational version. |
| **Brevity bias** | The tendency of iteratively summarized contexts to lose domain-specific detail. | ACE term. |
| **Context collapse** | Degradation of context detail through repeated rewriting cycles. | ACE term. |
| **Playbook** | A structured, evolving context artifact that accumulates, refines, and organizes strategies. | ACE term. Closest equivalents: Cursor's `.cursor/rules/` and `SKILL.md`, Anthropic's progress files. |
| **Rules** | Static, persistent instructions in version-controlled files (e.g., `.cursor/rules/`, `CLAUDE.md`, `AGENTS.md`). | Cursor term. Always-loaded. |
| **Skills** | Dynamic, context-aware capabilities defined in `SKILL.md` files and loaded only when relevant. | Cursor term. Distinct from "rules" because conditional. |
| **MCP (Model Context Protocol)** | The standard protocol for exposing external tools to a model. | Used across Anthropic, Cursor, and OpenAI tooling. |
| **Tool** | A callable function the model can invoke during its loop, with a typed input and a string-typed result. | Tool *format* (patches vs. string replacement) is per-model — see Cursor's harness post. |
| **Verifier** | The function that decides whether a unit of work is correct. Tests, type checkers, linters, oracles, end-to-end browser checks. | The C-compiler post calls this the "task verifier." Anthropic's long-running harness calls similar checks "end-to-end verification." Both insist it must be nearly perfect because agents optimize for it. |
| **Oracle** | A reference implementation used to validate the agent's output. | C-compiler post: GCC as oracle for partial compiler outputs. |
| **Plan Mode** | A distinct phase where the agent researches, asks clarifying questions, and proposes an implementation strategy before writing code. | Cursor term. Anthropic's two-agent (init/coding) split is the same idea expressed differently. |
| **Two-agent pattern** | Separate initialization and coding phases, each with its own prompt and entry protocol. | Anthropic's *Long-Running* post. |
| **Sub-agent / Managed agent / Cloud agent** | An agent invoked by another agent or by an external scheduler, typically with its own context and lifetime. | Anthropic's *Managed Agents* are infrastructure-level. Cursor's "cloud agents" are user-launched background runs. Sub-agents in Claude Code are in-process delegations. |
| **Keep rate** | Fraction of agent-generated code that remains in the user's codebase after a fixed interval. A production-quality signal. | Cursor metric. |
| **Error taxonomy** | A classification of failures (`InvalidArguments`, `UnexpectedEnvironment`, `ProviderError`, …) used to drive anomaly detection. | Cursor practice. |
| **Mechanical enforcement** | Using linters, structural tests, and CI checks to encode rules — instead of (or in addition to) prompt-level guidance — and feeding their error messages back into the agent's context. | OpenAI term. The principle appears across all three vendors under different names. |
| **Boring technology** | Composable, API-stable, well-represented-in-training-data stacks that agents model accurately. | OpenAI term. |
| **Cattle, not pets** | Treating execution environments as anonymous and replaceable rather than hand-recovered. | Anthropic *Managed Agents* phrasing. |
| **Decoupling (brain / hands / session)** | The architectural separation of the model's reasoning loop, the execution environment, and the event log into independently replaceable components. | Anthropic *Managed Agents* term. |
| **Dependency layering** | A strict, mechanically enforced ordering of architectural layers (e.g., Types → Config → Repo → Service → Runtime → UI) that keeps agents from violating modular boundaries. | OpenAI practice. |
| **Context anxiety** | A failure mode in which a model refuses or degrades work as its context window approaches full. | Cursor-named, Anthropic-confirmed. Sonnet 4.5 exhibited it; Opus 4.5 did not. A useful reminder that today's harness fix is tomorrow's dead weight. |

---

## 5. Where this lands for Archeia

Three observations from this synthesis bear directly on the spec:

- **P3 (state outside the window)** validates the existing `.archeia/` directory as durable, machine-readable state — but the field is converging on session-as-event-log designs (Managed Agents) that Archeia does not yet model.
- **P5 (mechanical guardrails)** suggests Archeia's standards should be enforceable by linters and CI checks where possible, not just documented in `STANDARDS.md`. OpenAI's "inject remediation into agent context on lint failure" is a concrete pattern worth copying.
- **The harness/scaffolding split** in the glossary is a vocabulary choice Archeia should make explicitly. Most sources blur the two; Archeia *is* scaffolding (project-level), and it sits *inside* a harness (Claude Code, Conductor, etc.). Naming that boundary cleanly will help every downstream decision.
