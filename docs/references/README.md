# References — the Observe-Orient leg of Archeia's OODA loop

This folder is the part of the repository that looks outward. Every other directory in this repo acts inward — defining the spec, enforcing contracts, documenting decisions already made. This one watches what is happening in the world and feeds that signal back into the standard before it calcifies.

The **[bibliography](bibliography.md)** is the primary artifact: a curated, date-sorted table of articles, papers, repos, and guides from the leading AI labs, AI-native companies, academic research groups, and open-source communities working on the same problems Archeia is solving.

---

## The OODA loop, applied to a living standard

The OODA loop — **Observe, Orient, Decide, Act** — is a model for how any adaptive system maintains relevance in a fast-moving environment. For Archeia, each phase maps to a concrete activity:

**Observe** — scan what the field is publishing. Anthropic posts a new engineering article on harness design. OpenAI open-sources Symphony. A Princeton team publishes SWE-bench results that shift what "autonomous coding" means. A Cursor engineering post describes a cloud-agent infrastructure pattern no one had articulated before. These are signals. This folder collects them.

**Orient** — read those signals against Archeia's current design. Does the new harness pattern assume something that `KERNEL.md` has already ruled out? Does a paper's finding about context window management invalidate a choice in the `.archeia/` directory layout? Does an open-source repo solve a problem Archeia was planning to solve differently? This is the interpretive step — understanding what the signal means *for this project specifically*, not just in the abstract.

**Decide** — translate the orientation into a spec decision. If the observation is trivial, nothing changes. If it reveals a genuine gap or a better approach, it becomes a candidate for the next spec revision, an ADR in `.archeia/product/decisions/`, or a prompt to revisit a principle in `PRINCIPLES.md`. The bibliography entry is the evidence trail for that decision.

**Act** — update the spec, the kernel, the schema, or a distribution. The loop closes. The standard advances because of what was observed, not despite it.

Without this folder actively maintained, the loop breaks at **Observe**. The spec makes decisions in a vacuum, accumulates assumptions the field has already falsified, and diverges from what agents and harnesses actually need. The references folder is the instrument that keeps the standard honest over time.

---

## What we observe

Archeia sits at the intersection of four threads where the field is moving fastest:

**Context engineering** — how agents perceive, compress, and route the information they need at any given moment. Archeia's `.archeia/` directory structure, its canonical file layout, and the distinction between living documents and decision records are all context engineering choices. The bibliography tracks what leading practitioners have found works at scale — and when their findings contradict Archeia's current assumptions, that is a revision signal.

**Harness engineering** — the scaffolding that wraps a model: tool loops, permission models, hook systems, sandboxing, and orchestration runtimes. Archeia is itself a layer inside a harness (Claude Code, Conductor, or any custom runner). Every harness engineering article from OpenAI, Anthropic, or Cursor is a window into what the surrounding infrastructure can and cannot be relied upon to provide — which directly shapes what Archeia must define vs. what it can defer.

**Agent development** — architectures, multi-agent coordination, planning loops, self-correction, and evaluation frameworks. Archeia's ownership model, delegation conventions, and execution domain exist to make multi-agent collaboration tractable. The field's evaluation results (SWE-bench, AgencyBench, Agentless) show concretely what agents can and cannot do today, which calibrates how ambitious or conservative Archeia's coordination model should be.

**Semi-autonomous repositories** — codebases designed to be read and modified by agents alongside humans. This is Archeia's core premise. References here — from SWE-agent's agent-computer interface research to Cursor's cloud-agent infrastructure — validate or challenge specific choices in the spec. When a leading lab demonstrates a better way to structure a repo for agentic access, Archeia should absorb it.

---

## Sources tracked

| Category | Organizations / Authors |
|---|---|
| Leading AI labs | Anthropic, OpenAI, Google DeepMind |
| AI-native companies | Cursor, Conductor |
| Academic research | Princeton NLP, Stanford, UIUC, Microsoft Research, Scale AI |
| Open-source projects | LangGraph, CrewAI, OpenHands, Letta, SWE-agent, AutoGen |
| Practitioners | Lilian Weng, Simon Willison |

---

## How to use this folder

**When designing a new spec area** — start here before writing anything. Check whether a leading lab has already published patterns that should inform or constrain the approach. Designing without observing is the fastest path to building something the field has already tried and abandoned.

**When challenging an existing decision** — look for papers or posts that contradict or complicate a choice already in the spec. Those are the ones that deserve a serious read and, if warranted, an ADR explaining why Archeia departs from the field's direction.

**When evaluating implementation options** — repos in the bibliography are reference implementations. Studying them before building is faster than rediscovering their lessons.

**When the bibliography feels stale** — update it. If three months have passed and no new entries have been added, the Observe step has gone dark and the loop is broken.

---

## Files in this folder

| File | Purpose |
|---|---|
| [`bibliography.md`](bibliography.md) | Primary index — all sources in a single date-sorted table covering articles, papers, repos, and guides |
| [`arxiv-ai-engineering-2026.md`](arxiv-ai-engineering-2026.md) | Curated arXiv papers from 2026, annotated with Archeia-specific relevance statements, split into Narrative support and Technical direction |
| [`prompts/research-arxiv-2026.md`](prompts/research-arxiv-2026.md) | Reusable research prompt for instructing an agent to find and format new arXiv papers into this folder's format |

---

## Format for new entries

New reference files follow one of two conventions:

- **`<slug>.md`** — an annotated summary of a single source, with key takeaways and a pointer to the original.
- **`<topic>/`** — a subdirectory grouping multiple related references under a shared theme.

Include frontmatter:

```markdown
---
title: <title of the source>
source: <URL or citation>
date: <publication or retrieval date>
tags: [context-engineering, harness-engineering, agent-scaffolding, ...]
---
```

Add a row to `bibliography.md` for every new entry. Prefer depth over breadth — a short, well-annotated summary beats a raw link, and a well-placed revision signal beats an impressively long list of articles no one has read.
