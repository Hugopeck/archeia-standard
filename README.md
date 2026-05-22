# The Archeia Standard

**Archeia is an Agentic Operating System for software businesses: an open, structured, in-repo substrate for software operators, teams, and agents to share durable operating knowledge.**

Version: [`0.5.0`](VERSION) · License: MIT

Archeia is an **Agentic Operating System** (**AOS**) for software businesses. More specifically, Archeia is the **in-repo knowledge-layer AOS** for software businesses: a minimal but rich in-repo substrate for structured software operating knowledge that humans and AI agents read, write, and coordinate through.

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
- [`product.schema.json`](contracts/product.schema.json) — product delivery surface contract
- [`c4.schema.json`](contracts/c4.schema.json) — `product/technical/architecture/c4/` contract

## Canonical software kernel

The software kernel uses four canonical domains:

- `strategy/` — vision, values, landscape, roadmap, strategy execution, decisions, conventions, learnings
- `operations/` — execution, optimization, people, finance, compliance, decisions, conventions, learnings; the support and improvement domain
- `product/` — product strategy, design, technical, and product execution
- `growth/` — growth strategy, marketing, sales, success, and growth execution

Within `strategy/`, the canonical subareas are:

- `strategy/vision/`
- `strategy/values/`
- `strategy/landscape/`
- `strategy/roadmap/`
- `strategy/execution/`

Within `operations/`, the canonical subareas are:

- `operations/execution/`
- `operations/optimization/`
- `operations/people/`
- `operations/finance/`
- `operations/compliance/`

Within `product/`, the canonical validated subareas are:

- `product/strategy/`
- `product/design/`
- `product/technical/`
- `product/execution/`

Within `growth/`, the canonical subareas are:

- `growth/strategy/`
- `growth/marketing/`
- `growth/sales/`
- `growth/success/`
- `growth/execution/`

The machine-readable architecture contract surface lives at `product/technical/architecture/c4/`.

`execution/` is the kernel's universal project-management surface. Its meaning is the same in every domain: the place where active work is organized, tracked, reviewed, and carried forward. Plans, programs, tasks, logs, retros, dashboards, and other execution-state artifacts belong under the owning domain's local `execution/` subtree rather than being centralized elsewhere.

The reason `execution/` is universal is that every top-level domain can move from durable knowledge into active work:

- `strategy/execution/` manages the execution of strategic initiatives and directional work
- `operations/execution/` manages the execution of operational support and internal improvement work
- `product/execution/` manages the execution of product delivery work
- `growth/execution/` manages the execution of go-to-market, adoption, and revenue work

In all four cases, the semantic is identical: `execution/` is the domain-local project-management layer for work in motion.

Across domains and subdomains, the kernel permits direct local `decisions/`, `conventions/`, and `learnings/` surfaces where needed. Procedural operating knowledge lives canonically under `operations/optimization/processes/`, with stronger process patterns often graduating into skills. Monitoring, bottleneck analysis, improvement initiatives, and process redesign live under `operations/optimization/`, while `people/`, `finance/`, and `compliance/` expand into explicit support-domain subtrees:

- `operations/people/{hiring,performance,workplace,compensation}/`
- `operations/finance/{operational,strategic,compliance}/`
- `operations/compliance/{regulatory,data-security,risk,ethics}/`

Every canonical `.archeia/` folder is also required to carry a scaffolded `README.md` describing its meaning and boundaries.

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
