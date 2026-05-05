# Research Prompt: arXiv AI Engineering Papers (2026)

Use this prompt to instruct an agent to find, evaluate, and format new arXiv papers for addition to `docs/references/arxiv-ai-engineering-2026.md`. Run it whenever the bibliography feels stale or before a significant spec revision.

---

## Prompt

```
You are a research agent building a curated bibliography of arXiv papers for the Archeia Standard — an open spec for structured, in-repo knowledge that AI agents and humans share. Your task is to find 2026 papers on AI engineering that are relevant to Archeia's four core concerns and format them following the template below.

---

## SCOPE

Papers must meet ALL of the following criteria:

1. **Published in 2026** — the submission date (not revision date) must be 2026-xx-xx. Do not include papers submitted in 2024 or 2025, even if revised in 2026.
2. **AI engineering** — focused on how AI systems are built, structured, evaluated, and operated in practice. Not purely theoretical ML, not pure NLP linguistics, not benchmark leaderboard papers with no engineering takeaway.
3. **Directly relevant** to at least one of Archeia's four concerns (see below).

If a paper is borderline, err on the side of exclusion. A short list of high-relevance papers is more useful than a long list of marginal ones.

---

## ARCHEIA'S FOUR CONCERNS

Use these as your relevance filter. A paper is relevant if it bears directly on one of these:

**Context engineering** — how agents perceive, compress, select, and route context. Includes: context file design (AGENTS.md, CLAUDE.md, repo-level steering files), context window management, context quality vs. quantity, prompt compression, retrieval-augmented context, context staleness and hygiene.

**Harness engineering** — the scaffolding around a model: tool loops, permission models, hook systems, sandboxing, orchestration runtimes, MCP (Model Context Protocol), agent-computer interfaces, execution environments.

**Agent scaffolding** — how individual agents are structured: planning loops, self-correction, tool/skill design and description quality, memory access patterns, reasoning trace faithfulness, tool use reliability.

**Multi-agent orchestration** — how multiple agents coordinate: topology design, delegation, ownership and conflict resolution, coordination protocols, multi-agent evaluation, dynamic team composition.

Cross-cutting themes that are always relevant: autonomous coding benchmarks with engineering implications, long-horizon agent performance, context/reasoning quality vs. cost tradeoffs.

---

## SEARCH STRATEGY

Search the following sources:

1. **arXiv cs.AI, cs.SE, cs.CL, cs.MA** — use the arXiv search API or Semantic Scholar for papers submitted between 2026-01-01 and today with relevant keywords.
2. **Semantic Scholar** — keyword search: "context engineering", "harness engineering", "agent scaffolding", "multi-agent orchestration", "autonomous coding", "LLM tool use", "agentic coding", "repository context", "agent evaluation 2026".
3. **Papers with Code** — recent papers tagged with "code generation", "software agents", "LLM agents".

For each candidate paper, check:
- Submission date is genuinely 2026 (check the arXiv abstract page, not just the title)
- Abstract describes a practical engineering contribution, not only a theoretical result
- Findings have a clear implication for how AI systems are built or structured

---

## CLASSIFICATION

Classify each paper as one of:

**Narrative support** — substantiates a design choice Archeia has already made. Use when: the paper provides evidence that a pattern Archeia uses (curation, explicit context, staged guidance, etc.) works better than alternatives. These papers are useful for explaining Archeia to external audiences.

**Technical direction** — informs how Archeia or a distribution should be built. Use when: the paper describes a technique, architecture, or finding that Archeia has not yet incorporated but should consider. These papers feed future spec revisions.

If a paper is strong for both, classify it as Narrative support and note the technical implication in the Relevance field.

---

## OUTPUT FORMAT

Produce a markdown file following this exact structure. Do not deviate from the format.

---

```markdown
---
title: arXiv — AI Engineering (2026 Selection, <MONTH> batch)
date: <YYYY-MM-DD>
tags: [context-engineering, harness-engineering, agent-scaffolding, multi-agent, autonomous-coding, evaluation]
---

# arXiv — AI Engineering: 2026 Selected Papers (<MONTH> batch)

<One sentence describing the batch — what themes dominate this selection and why.>

---

## Quick reference

| # | Authors | Title (short) | Tags | arXiv |
|---|---|---|---|---|
| 1 | <Last name et al.> | <6–8 word title summary> | `<tag>` `<tag>` | [<ID>](https://arxiv.org/abs/<ID>) |
...

---

## Narrative support

<Papers that substantiate Archeia's existing design choices.>

---

### <N> — <Punchy 5–8 word claim the paper supports>

**<Authors> (<year>)**
*<Full paper title>*
`<tag>` `<tag>`
[arXiv:<ID>](https://arxiv.org/abs/<ID>)

**Relevance:** <2–3 sentences. Explain specifically what the paper found and how it maps to a concrete Archeia design decision. Name the decision (e.g., "Archeia's `last_verified` hygiene convention", "the `.archeia/` curation discipline"). Avoid vague claims like "supports our approach".>

> **Caveat:** <Include only if there is a genuine limitation — single-project study, self-reported results, narrow task domain, etc. Omit this line if no significant caveat.>

---

## Technical direction

<Papers that inform future implementation decisions.>

---

### <N> — <Punchy 5–8 word claim>

**<Authors> (<year>)**
*<Full paper title>*
`<tag>` `<tag>`
[arXiv:<ID>](https://arxiv.org/abs/<ID>)

**Relevance:** <2–3 sentences. What did the paper find or demonstrate? What specific Archeia component, schema field, skill design, or future extension does this inform? Be concrete.>
```

---

## QUALITY BAR

Each Relevance field must:
- Name a specific Archeia concept, file, schema field, or design decision
- State what the paper found (not just what it is about)
- Explain the implication in one or two sentences

Reject any entry where the Relevance field could apply to any AI project generically. If you cannot write a specific Relevance statement, the paper is not relevant enough to include.

Aim for 8–15 papers per batch. Fewer strong entries beat more weak ones.
```
