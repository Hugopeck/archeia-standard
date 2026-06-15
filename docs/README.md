# Archeia Docs

The docs are organized by role. Each subfolder has its own README with a deeper index.

```text
docs/
├── standard/     # Operational canon — model, rules, spec
├── guides/       # Practical how-tos and honest scope audits
└── research/     # Theoretical basis and field signals (not canon)
```

## Document Authority

| Doc | Authoritative for |
|---|---|
| [`standard/overview.md`](standard/overview.md) | Why Archeia exists |
| [`standard/ontology.md`](standard/ontology.md) | What concepts mean — **edit here to change the model** |
| [`standard/rules.md`](standard/rules.md) | What tools enforce — **edit here to change enforcement** |
| [`standard/spec.md`](standard/spec.md) | Build contract — **mirrors model + rules; do not invent here** |
| [`research/theoretical-basis.md`](research/theoretical-basis.md) | Research grounding and citations — **not operational canon** |

**Rule:** Change the model in `ontology.md`. Change enforcement in rules. Mirror both in spec. Never invent only in spec.

When theory and dogfood conflict, dogfood wins — then update the operational docs.

## Reading Paths

### First time — understand the system

1. [`standard/overview.md`](standard/overview.md) — motivation and principles
2. [`guides/faq.md`](guides/faq.md) — common questions in plain language
3. [`examples/.archeia/`](../examples/.archeia/) — see a complete installation

### Implementing tools — build contract

1. [`standard/spec.md`](standard/spec.md) — consolidated build contract
2. [`standard/ontology.md`](standard/ontology.md) — domains, shapes, ownership, contracts
3. [`standard/rules.md`](standard/rules.md) — validation checks and operations
4. [`../contracts/`](../contracts/) — JSON Schemas
5. [`../scripts/archeia_validate`](../scripts/archeia_validate) — reference validator

### Honest scope audit — what Archeia does and does not solve

1. [`guides/memory-vs-knowledge.md`](guides/memory-vs-knowledge.md) — evaluated against memory competencies
2. [`research/theoretical-basis.md`](research/theoretical-basis.md) — why each concept was chosen

### Staying current — field signals

1. [`research/bibliography.md`](research/bibliography.md) — curated source index
2. [`research/README.md`](research/README.md) — how research feeds the OODA loop

## Standard — Operational Canon

The authoritative model and enforcement docs. See [`standard/README.md`](standard/README.md).

- [`standard/overview.md`](standard/overview.md): why Archeia exists.
- [`standard/spec.md`](standard/spec.md): build contract — start here to implement tools.
- [`standard/ontology.md`](standard/ontology.md): the model — domains, shapes, ownership, and contracts.
- [`standard/rules.md`](standard/rules.md): validation, operations, and tests.

## Guides — Practical How-Tos

Supplementary docs that do not override standard canon. See [`guides/README.md`](guides/README.md).

- [`guides/faq.md`](guides/faq.md): common questions.
- [`guides/memory-vs-knowledge.md`](guides/memory-vs-knowledge.md): what Archeia solves and what it does not.
- [`guides/figma-product-integration.md`](guides/figma-product-integration.md): Figma and product-design integration.
- [`guides/distributions.md`](guides/distributions.md): note on deferred Standard bundles (legacy "distribution" concept).
- [`guides/enforcement.md`](guides/enforcement.md): validation and CI guardrail examples (draft).

## Research — Theoretical Basis

Research docs ground decisions intellectually. They do not override the model, rules, or spec. See [`research/README.md`](research/README.md).

- [`research/theoretical-basis.md`](research/theoretical-basis.md): theoretical framework, citations, and word choices (large; read for *why*, not as a build checklist).
- [`research/bibliography.md`](research/bibliography.md): source index.
- [`research/harness-engineering-synthesis.md`](research/harness-engineering-synthesis.md): harness-engineering synthesis notes.
- [`research/arxiv-ai-engineering-2026.md`](research/arxiv-ai-engineering-2026.md): curated arXiv papers with Archeia-specific relevance.
