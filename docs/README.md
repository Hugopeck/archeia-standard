# Archeia Docs

The docs are organized by role.

## Document authority

| Doc | Authoritative for |
|---|---|
| [`standard/overview.md`](standard/overview.md) | Why Archeia exists |
| [`standard/ontology.md`](standard/ontology.md) | What concepts mean — **edit here to change the model** |
| [`standard/rules.md`](standard/rules.md) | What tools enforce — **edit here to change enforcement** |
| [`standard/spec.md`](standard/spec.md) | Build contract — **mirrors ontology + rules; do not invent here** |
| [`research/theoretical-basis.md`](research/theoretical-basis.md) | Research grounding and citations — **not operational canon** |

**Rule:** Change the model in ontology. Change enforcement in rules. Mirror both in spec. Never invent only in spec.

## Read The Architecture

- [`standard/overview.md`](standard/overview.md): why Archeia exists.
- [`standard/spec.md`](standard/spec.md): build contract — start here to implement tools.
- [`standard/ontology.md`](standard/ontology.md): the operational model — domains, shapes, ownership, and contracts.
- [`standard/rules.md`](standard/rules.md): validation, operations, and tests.

## Use The Guides

- [`guides/faq.md`](guides/faq.md): common questions.
- [`guides/figma-product-integration.md`](guides/figma-product-integration.md): Figma and product-design integration.
- [`guides/memory-vs-knowledge.md`](guides/memory-vs-knowledge.md): what Archeia solves and what it does not.
- [`guides/distributions.md`](guides/distributions.md): note on deferred Blueprint bundles (legacy "distribution" concept).
- [`guides/enforcement.md`](guides/enforcement.md): validation and CI guardrail examples.

## Inspect The Research Basis

Research docs ground decisions intellectually. They do not override ontology, rules, or spec. When theory and dogfood conflict, dogfood wins — then update the operational docs.

- [`research/theoretical-basis.md`](research/theoretical-basis.md): theoretical framework, citations, and word choices (large; read for *why*, not as a build checklist).
- [`research/bibliography.md`](research/bibliography.md): source index.
- [`research/harness-engineering-synthesis.md`](research/harness-engineering-synthesis.md): harness-engineering synthesis notes.
