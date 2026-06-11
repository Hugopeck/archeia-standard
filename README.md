# Archeia Factory

**Archeia Factory is my private system for giving software projects a durable, shared knowledge layer that humans and AI agents can both read and write.**

**North star:** I never re-explain project context in a new chat.

Important context scatters fast: chat logs, tickets, wikis, docs, and agent memory. Archeia puts project operating knowledge in one predictable place inside the repo — the `.archeia/` tree — so nobody has to reconstruct the roadmap, the current decision, the architecture evidence, or active work from scratch.

**Current version:** [`0.5.0`](VERSION) (pre-1.0; breaking changes still possible)

## Two Forms

Archeia Factory has two forms:

- **Blueprint** — the reusable architecture maintained in this repo: theory, schemas, procedures, examples, and validation rules.
- **Instance** — the `.archeia/` operating layer installed into a specific project repo.

```text
Archeia Factory
├── Blueprint (this repo)
└── Instance (.archeia/ in a project)   ← init creates this
```

**Factory** is the whole system — Blueprint plus Instance shape, validation, and the procedures that keep installations useful over time. This is not a public adoption program. It is a private operating system for my own projects.

Blueprint **v0** is a rough, complete address space — every canonical path exists so postures and defaults have a settled place, even when the answer is two sentences or "N/A". See [`docs/standard/spec.md`](docs/standard/spec.md#2-blueprint-v0-philosophy).

In prose, prefer `.archeia/`, `spec.yaml`, and domain names over repeating "instance."

## The `.archeia/` Tree

Archeia treats the repo as the collaboration surface.

```text
.archeia/
├── .system/
├── strategy/
├── operations/
├── product/
└── growth/
```

The four domain folders hold project knowledge:

- `strategy/` — direction, values, landscape, roadmap, and strategic decisions.
- `operations/` — execution, process, people, finance, compliance, and support.
- `product/` — product strategy, design, technical context, and delivery.
- `growth/` — adoption, go-to-market, sales, success, and rollout.

The hidden `.system/` folder holds metadata that tools read:

```text
.archeia/.system/
├── VERSION
├── spec.yaml
└── contracts/
```

See [`examples/.archeia/`](examples/.archeia/) for a complete canonical installation.

## Designed For Agents

AI agents work best when boundaries, handoffs, and state are explicit. Archeia borrows the useful spirit of system architecture without heavy notation:

- **Blocks** — bounded elements: domains, artifacts, procedures, agent roles.
- **Boundaries** — what each block owns and does not own.
- **State** — current truth, lifecycle, or health of an artifact.
- **Inputs and outputs** — what a block consumes and produces.
- **Interfaces** — stable handoffs between domains and tools.
- **Constraints** — guardrails for writes, transitions, and pruning.

The goal is enough structure for reliable agent work — not a process map of every internal step.

## Ontology + Rules

Archeia has two documentation layers:

- **Ontology** — what the folders, artifact shapes, ownership model, and contract surfaces mean.
- **Rules** — what validators, tools, and operations must enforce.

The ontology is the shared map. The rules make that map checkable.

## Why This Exists

Agents are strongest when they can work from stable context. They struggle when every session starts from zero.

Archeia gives agents and humans:

- predictable paths for important project knowledge
- clear ownership for parallel writes
- lifecycle rules for different kinds of artifacts
- schemas for cross-domain contracts
- git-backed history and review
- a repo-local structure that works without a hosted service

It is not a memory database, a wiki, a ticket system, or an agent framework. Those tools can integrate with it. Archeia is the repo-local knowledge layer underneath them.

Archeia does not replace `AGENTS.md`, harness rules, Conductor workspaces, or project skills. It composes with them — the stack works together, not as competing alternatives.

## Start Here

If you are reading Archeia for the first time:

1. Read [`docs/standard/overview.md`](docs/standard/overview.md) for the motivation.
2. Read [`docs/standard/spec.md`](docs/standard/spec.md) for the build contract.
3. Read [`docs/standard/ontology.md`](docs/standard/ontology.md) for the model.
4. Read [`docs/standard/rules.md`](docs/standard/rules.md) for validation and operations.
5. Explore [`examples/.archeia/`](examples/.archeia/) to see a complete installation.

For practical questions, see [`docs/guides/faq.md`](docs/guides/faq.md). For theoretical basis and citations, see [`docs/research/theoretical-basis.md`](docs/research/theoretical-basis.md).

## Repository Layout

```text
.
├── contracts/                 # Source JSON Schemas (see contracts/README.md)
├── docs/                      # Architecture docs, guides, and research (see docs/README.md)
├── examples/                  # Valid and invalid installations (see examples/README.md)
├── scripts/                   # Deterministic validation tools (see scripts/README.md)
├── VERSION
└── README.md
```

The source schemas live in `contracts/`. An installed `.archeia/` layer copies them under `.archeia/.system/contracts/`.

## Operations

Archeia defines six deterministic operations on an installed `.archeia/` tree:

| Operation | Purpose | Status |
|---|---|---|
| `init` | Install an Instance into a project repo | Specified, not yet implemented |
| `validate` | Return structured health issues | **Implemented** (`scripts/archeia_validate`) |
| `write` | Create or update artifacts with precondition checks | Specified, not yet implemented |
| `transition` | Move transient artifacts through declared statuses | Specified, not yet implemented |
| `prune` | Remove expired transient artifacts | Specified, not yet implemented |
| `history` | Show history by artifact shape | Specified, not yet implemented |

## Validate The Example

Run from the repo root:

```sh
scripts/archeia_validate examples
```

The `examples/.archeia/` tree should pass with zero errors. The validator expects a **project root** (a directory containing `.archeia/`), not the `.archeia/` folder itself.

To validate a real project:

```sh
scripts/archeia_validate /path/to/your/project
```

Invalid fixtures live under [`examples/invalid/`](examples/invalid/). Each fixture is designed to fail with a specific validation error — see [`examples/invalid/README.md`](examples/invalid/README.md) for the full matrix.

## What `spec.yaml` Declares

The installed `.archeia/.system/spec.yaml` file is the machine-readable manifest. It declares:

- Archeia version
- instance identity (name and version)
- domains and owners
- canonical tree paths (~154 directories in Blueprint v0)
- artifact shapes (living, accumulating, transient)
- contract surfaces (product delivery, C4 evidence)
- lifecycle status mappings
- retention windows
- schema bindings

Validators read this file before checking a `.archeia/` tree. The deprecated `domains.yaml` name is replaced by `spec.yaml`.

## Status

Archeia is pre-1.0. The core model is stabilizing, but breaking changes may still happen while the Factory is sharpened through examples, validators, and real project use.

Current version: [`VERSION`](VERSION)
