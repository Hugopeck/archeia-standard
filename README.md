# Archeia Factory

**Archeia Factory is my private system for giving software projects a durable, shared knowledge layer that humans and AI agents can both read and write.**

Important context scatters fast: chat logs, tickets, wikis, docs, and agent memory. Archeia puts project operating knowledge in one predictable place inside the repo — the `.archeia/` tree — so nobody has to reconstruct the roadmap, the current decision, the architecture evidence, or active work from scratch.

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

## Start Here

If you are reading Archeia for the first time:

1. Read [`docs/standard/overview.md`](docs/standard/overview.md) for the motivation.
2. Read [`docs/standard/spec.md`](docs/standard/spec.md) for the build contract.
3. Read [`docs/standard/ontology.md`](docs/standard/ontology.md) for the model.
4. Read [`docs/standard/rules.md`](docs/standard/rules.md) for validation and operations.
5. Explore [`examples/.archeia/`](examples/.archeia/) to see a complete installation.

For theoretical basis and citations, see [`docs/research/theoretical-basis.md`](docs/research/theoretical-basis.md).

## Repository Layout

```text
.
├── contracts/                 # Source JSON Schemas
├── docs/                      # Architecture docs, guides, and research
├── examples/                  # Valid and invalid installations
├── scripts/                   # Deterministic validation tools
├── VERSION
└── README.md
```

The source schemas live in `contracts/`. An installed `.archeia/` layer copies them under `.archeia/.system/contracts/`.

## Validate The Example

Run:

```sh
scripts/archeia_validate examples
```

The `examples/.archeia/` tree should pass with zero errors.

Invalid fixtures live under:

```text
examples/invalid/
```

Each invalid fixture is designed to fail with a specific validation error.

## What `spec.yaml` Declares

The installed `.archeia/.system/spec.yaml` file is the machine-readable manifest. It declares:

- Archeia version
- instance identity (name and version)
- domains and owners
- canonical tree paths
- artifact shapes
- contract surfaces
- lifecycle status mappings
- retention windows
- schema bindings

Validators read this file before checking a `.archeia/` tree.

## Status

Archeia is pre-1.0. The core model is stabilizing, but breaking changes may still happen while the Factory is sharpened through examples, validators, and real project use.

Current version: [`VERSION`](VERSION)
