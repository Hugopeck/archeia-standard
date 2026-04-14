# The Archeia Standard

**An open substrate for structured, in-repo knowledge that AI agents and humans share.**

Version: [`0.2.1`](VERSION) · License: MIT

Archeia is a standard and a kernel for agentic development: a minimal, in-repo substrate for structured project knowledge that AI agents read, write, and coordinate through — without a server, a schema registry, or a message broker between them.

This repository contains the formal specification. The reference implementation — **Archeia Solo**, a distribution for solo builders shipping bootstrapped AI-first software — lives at [github.com/Hugopeck/archeia](https://github.com/Hugopeck/archeia).

Archeia defines the durable source-of-truth layer for agent systems. If a distribution later needs vector search, graph traversal, or dynamic context management, those retrieval layers can sit on top of the Archeia tree without changing the canonical store underneath.

## Start here

- **[`MANIFESTO.md`](MANIFESTO.md)** — the one-page pitch. Read this first.
- **[`PRINCIPLES.md`](PRINCIPLES.md)** — the seven fundamental truths the standard rests on.
- **[`KERNEL.md`](KERNEL.md)** — the formal substrate: primitives, invariants, operations, inherent skills, extension mechanism.
- **[`SCHEMA.md`](SCHEMA.md)** — the canonical software application of the kernel. Five domains, ownership, cross-domain contracts.
- **[`TEMPORAL_MODEL.md`](TEMPORAL_MODEL.md)** — the three lifecycle shapes: living, accumulating, transient.
- **[`ONTOLOGY.md`](ONTOLOGY.md)** — canonical vocabulary grounded in cognitive science, multi-agent systems research, and recent (2023–2026) AI literature.

## Contracts

Enforceable JSON Schemas for cross-domain interchange live under [`contracts/`](contracts/):

- [`living-doc.schema.json`](contracts/living-doc.schema.json) — base schema for semantic-memory documents
- [`accumulating-record.schema.json`](contracts/accumulating-record.schema.json) — base schema for episodic-memory records
- [`transient-artifact.schema.json`](contracts/transient-artifact.schema.json) — base schema for lifecycle artifacts
- [`draft.schema.json`](contracts/draft.schema.json) — business → product contract
- [`product.schema.json`](contracts/product.schema.json) — product → execution contract
- [`c4.schema.json`](contracts/c4.schema.json) — codebase → product contract (C4 model data)

## Distributions

A **distribution** is an opinionated bundle that extends the kernel for a specific audience. See [`distributions/README.md`](distributions/README.md) for the "how to write a distribution" guide and the current roster.

The reference distribution is **Archeia Solo**, at [github.com/Hugopeck/archeia](https://github.com/Hugopeck/archeia). It targets solo builders running AI-agent-maximalist bootstrapped software businesses, ships 16 skills and a growing agent roster, and implements all six kernel operations.

Future distributions expected: Archeia Research (research labs), Archeia Studio (game studios), Archeia Enterprise (compliance-heavy environments), Archeia OSS (open-source projects with monetization intent).

## Supporting material

- [`docs/faq.md`](docs/faq.md) — comparisons against wikis, vector DBs, RAG, knowledge graphs, docs-as-code tools, ADR repos, and current agent frameworks. Structural, implementation, and political questions.
- [`docs/memory-vs-knowledge.md`](docs/memory-vs-knowledge.md) — the honest audit of what Archeia solves and what it doesn't, measured against the four canonical memory competencies from MemoryAgentBench (Hu, Wang & McAuley, 2025). Required reading before claiming Archeia "solves memory."

## Versioning

The standard uses semantic versioning. `VERSION` at the repo root contains the current kernel version. Tools that consume `.archeia/` trees should read this version and either process the repo (if they support it) or refuse with a clear error.

- **Major** — breaking changes to primitives, invariants, operations, or inherent skills
- **Minor** — additive changes: new optional fields, new operations, new validation checks that don't break existing conforming repos
- **Patch** — clarifications, documentation fixes, attribution corrections

The current version is **0.2.1**. The kernel will reach **1.0.0** when the first external distribution (not Archeia Solo) ships and the kernel has survived that contact with a new audience.

## Contributing

This repository is the open spec. Corrections, clarifications, and additions are welcome via PR. Changes that affect terminology, operations, or shapes require a version bump per the rules in [`KERNEL.md`](KERNEL.md) §13. Changes that introduce new canonical citations require verification against primary sources (see [`ONTOLOGY.md`](ONTOLOGY.md) §12 for the standard's position on verified vs unverified claims).

## Origin

This repository was extracted from [github.com/Hugopeck/archeia](https://github.com/Hugopeck/archeia) on 2026-04-13, commit `e037dc8`, to separate the open standard from its reference distribution. Prior history of the standard files lives in the archeia repository under `git log --follow standard/<file>`. The `archeia-standard` repo starts with a fresh initial commit citing the origin; the `archeia` repo continues as Archeia Solo, the reference distribution.

## License

The Archeia Standard is released under the MIT License. See `LICENSE` for details.
