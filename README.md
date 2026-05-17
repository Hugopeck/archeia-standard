# The Archeia Standard

**An open software business OS: a structured, in-repo substrate for software operators, teams, and agents to share durable operating knowledge.**

Version: [`0.5.0`](VERSION) · License: MIT

Archeia is a standard and a kernel for a **software business OS**: a minimal but rich in-repo substrate for structured software operating knowledge that humans and AI agents read, write, and coordinate through.

## Start here

- **[`MANIFESTO.md`](MANIFESTO.md)** — the one-page pitch.
- **[`PRINCIPLES.md`](PRINCIPLES.md)** — the seven fundamental truths.
- **[`KERNEL.md`](KERNEL.md)** — the thick software kernel: domains, meanings, rich tree, invariants, operations, and extension mechanism.
- **[`SCHEMA.md`](SCHEMA.md)** — a short companion explainer for the kernel's software tree and migration.
- **[`TEMPORAL_MODEL.md`](TEMPORAL_MODEL.md)** — the three lifecycle shapes.
- **[`ONTOLOGY.md`](ONTOLOGY.md)** — canonical vocabulary and academic grounding.

## Conformance and positioning

- **[`POSITIONING.md`](POSITIONING.md)** — what Archeia adds beyond the SOTA harness corpus.
- **[`CONFORMANCE.md`](CONFORMANCE.md)** — the implementation checklist / definition of done.
- **[`REFERENCE-ALGORITHMS.md`](REFERENCE-ALGORITHMS.md)** — language-agnostic pseudocode for the six deterministic kernel operations.
- **[`TEST-MATRIX.md`](TEST-MATRIX.md)** — the per-schema and per-operation tests every conformant repo passes.

## Contracts

Enforceable JSON Schemas for cross-domain interchange live under [`contracts/`](contracts/):

- [`living-doc.schema.json`](contracts/living-doc.schema.json) — base schema for living documents
- [`accumulating-record.schema.json`](contracts/accumulating-record.schema.json) — base schema for accumulating records
- [`transient-artifact.schema.json`](contracts/transient-artifact.schema.json) — base schema for transient artifacts
- [`product.schema.json`](contracts/product.schema.json) — product execution surface → operations contract
- [`c4.schema.json`](contracts/c4.schema.json) — `product/technical/architecture/c4/` contract

## Canonical software kernel

The software kernel uses four canonical domains:

- `strategy/` — vision, values, landscape, roadmap, decisions
- `operations/` — execution, optimization, people, finance, compliance
- `product/` — product strategy, design, technical, and product execution
- `growth/` — acquisition, retention, monetization

Within `product/`, the canonical validated subareas are:

- `product/strategy/`
- `product/design/`
- `product/technical/`
- `product/execution/`

The machine-readable architecture contract surface lives at `product/technical/architecture/c4/`.

## Migration

The `0.4.0` revision was the breaking canonical-layout migration:

- `business/` is replaced by `strategy/` plus parts of `operations/`
- top-level `execution/` moves to `operations/execution/`
- top-level `codebase/` moves under `product/technical/architecture/` and `product/technical/devs/`
- the old executable product surface is replaced by:
  - `product/strategy/roadmap/`
  - `product/technical/specs/`
  - `product/execution/prds/`

See [`SCHEMA.md`](SCHEMA.md) for the explicit mapping summary and [`MIGRATION-0.4.0.md`](MIGRATION-0.4.0.md) for the historical migration note.

## Distributions

A **distribution** is an opinionated bundle that extends the kernel for a specific software operating context. Distributions strengthen usage, policy, and workflow over the shared kernel tree. See [`distributions/README.md`](distributions/README.md) for the guide and current roster.

The reference distribution is **Archeia Solo**, at [github.com/Hugopeck/archeia](https://github.com/Hugopeck/archeia). A companion distribution-flavor also lives in this repo: [`distributions/archeia-enforcement.md`](distributions/archeia-enforcement.md).

## Living standard

The agentic software field is moving fast. Archeia tracks this evolution deliberately: design decisions are checked against current harness-engineering practice, then codified as repository contracts that humans and agents can both rely on.

## Versioning

The standard uses semantic versioning, with the usual pre-1.0 caveat that breaking revisions may still land as `0.x` minor bumps while the standard is stabilizing:

- **Major** — breaking changes to primitives, invariants, operations, or required distribution tooling
- **Minor** — additive changes that do not break existing conforming repos
- **Patch** — clarifications and documentation fixes

The current version is **0.5.0**. This release makes the kernel thick again: the rich software tree, broad semantic definitions, and flex rules now live in `KERNEL.md`, while `SCHEMA.md` is reduced to a companion explainer.

## Contributing

This repository is the open spec. Corrections, clarifications, and additions are welcome via PR.
