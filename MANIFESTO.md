# Archeia

**Archeia is an Agentic Operating System for software businesses: a standard and kernel for structured, in-repo operating knowledge that software teams, operators, and AI agents read, write, and coordinate through.**

## The problem

AI coding agents fail less from lack of intelligence than from lack of reliable context and a durable collaboration surface. Project truth is scattered across tools the agent cannot see; task state, architecture, product direction, and decisions are reconstructed from guesses every session.

Archeia fixes that by putting the software project's operating mind inside the repo.

## What you get

A single directory, `.archeia/`, at the root of your software project. Four canonical domains inside it:

- `**strategy/**` — vision, values, landscape, roadmap, decisions
- `**operations/**` — execution, optimization, people, finance, compliance
- `**product/**` — product strategy, design, technical, and product execution
- `**growth/**` — acquisition, retention, monetization

Inside `product/`, the canonical subareas are:

- `product/strategy/`
- `product/design/`
- `product/technical/`
- `product/execution/`

Every artifact has a temporal model. Every top-level domain has exactly one writer family. The filesystem is the canonical store. Ownership is the concurrency model. Git is the audit log. The kernel is thick because software work repeatedly needs the same distinctions: strategy, operations, product, growth; decisions, conventions, and learnings; delivery surfaces versus technical evidence; guides versus skills.

## What it replaces

- Notion and Confluence are replaced by `.archeia/product/`, `.archeia/strategy/`, and `.archeia/operations/` for the parts agents need to read.
- Jira and Linear are replaced by `.archeia/operations/execution/` for active delivery state.
- ADR repos are replaced by domain-local `decisions/` surfaces, especially under `product/technical/decisions/`.
- scattered team norms are replaced by domain-local `conventions/` surfaces.
- ad hoc internal how-tos are replaced by `operations/guides/`, with the best guides later formalized as skills.
- Architecture-analysis tools are replaced by `.archeia/product/technical/architecture/c4/` plus adjacent generated architecture intelligence.
- Closed or tool-specific memory silos are replaced by the whole tree as the durable source of truth.

## Start here

- **Read the kernel:** [`KERNEL.md`](KERNEL.md) — the thick software contract
- **Read the software-tree companion:** [`SCHEMA.md`](SCHEMA.md)
- **Read the principles:** [`PRINCIPLES.md`](PRINCIPLES.md)
- **Read the temporal model:** [`TEMPORAL_MODEL.md`](TEMPORAL_MODEL.md)
- **Read the ontology:** [`ONTOLOGY.md`](ONTOLOGY.md)

Archeia is a way to give AI agents a shared source of truth and a way of working together. The rest is skills, agents, and the discipline to write everything down where the agents can find it.
