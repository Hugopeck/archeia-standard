# The Archeia Standard

**Archeia is a standard for durable project knowledge inside a software repo.**

It gives humans and AI agents one shared place to read, write, validate, and hand off software operating context. Instead of scattering project truth across chat logs, tickets, wikis, docs, and memory tools, Archeia puts the working knowledge of a software project in a predictable `.archeia/` tree.

The goal is simple: agents should not have to guess where the roadmap lives, which decision is current, what architecture evidence exists, or where active work is tracked. Humans should be able to inspect and review the same files.

## The Core Idea

Archeia treats the repo as the collaboration surface.

```text
.archeia/
├── .system/
├── strategy/
├── operations/
├── product/
└── growth/
```

The four public folders are the knowledge domains:

- `strategy/` — direction, values, landscape, roadmap, and strategic decisions.
- `operations/` — execution, process, people, finance, compliance, and support.
- `product/` — product strategy, design, technical context, and delivery.
- `growth/` — adoption, go-to-market, sales, success, and rollout.

The hidden `.system/` folder contains the installed standard metadata that tools use:

```text
.archeia/.system/
├── VERSION
├── spec.yaml
└── contracts/
```

## Ontology + Rules

The standard has two layers:

- **Ontology** explains what the folders, artifact shapes, ownership model, and contract surfaces mean.
- **Rules** explain what validators, tools, and distributions must enforce.

This split matters. The ontology gives humans and agents a shared map. The rules make that map checkable.

## Why This Exists

AI agents are strongest when they can work from stable context. They struggle when every session has to reconstruct the project from scratch.

Archeia gives agents and humans:

- predictable paths for important project knowledge
- clear ownership for writes
- lifecycle rules for different kinds of artifacts
- schemas for cross-domain contracts
- git-backed history and review
- a structure that works without a hosted service

It is not a memory database, a wiki, a ticket system, or an agent framework. Those tools can integrate with it. Archeia is the repo-local knowledge contract underneath them.

## Start Here

If you are reading the standard for the first time:

1. Read [`docs/standard/overview.md`](docs/standard/overview.md) for the motivation.
2. Read [`docs/standard/ontology.md`](docs/standard/ontology.md) for the model.
3. Read [`docs/standard/rules.md`](docs/standard/rules.md) for packaging and validation.
4. Explore [`examples/.archeia/`](examples/.archeia/) to see the complete installed tree.

For terminology and citations, see [`docs/research/terminology.md`](docs/research/terminology.md).

## Repository Layout

```text
.
├── contracts/                 # Source JSON Schemas
├── docs/                      # Standard docs, guides, distributions, and research
├── examples/                  # Valid and invalid installed trees
├── scripts/                   # Deterministic validation tools
├── VERSION
└── README.md
```

The source schemas live in `contracts/`. A conforming project installs copies under `.archeia/.system/contracts/`.

## Validate The Canonical Example

Run:

```sh
scripts/archeia_validate examples
```

The canonical `examples/.archeia/` tree should pass with zero errors.

Invalid fixtures live under:

```text
examples/invalid/
```

Each invalid fixture is designed to fail with a specific validation error.

## What `spec.yaml` Declares

The installed `.archeia/.system/spec.yaml` file is the machine-readable companion to the ontology. It declares:

- standard version
- distribution metadata
- domains and owners
- canonical tree paths
- artifact shapes
- contract surfaces
- lifecycle status mappings
- retention windows
- schema bindings

Validators read this file before checking an Archeia tree.

## Status

Archeia is pre-1.0. The core model is stabilizing, but breaking changes may still happen while the standard is sharpened through examples, validators, and distribution work.

Current version: [`VERSION`](VERSION)

## Contributing

Good contributions make the standard clearer, more enforceable, or easier to adopt.

Useful changes include:

- clearer wording in the standard docs
- tighter schemas
- better validation fixtures
- additional validator checks
- distribution examples
- research notes that affect the ontology or rules

When changing the standard, update the docs, examples, and validator together where possible. A rule is strongest when it is explained, demonstrated, and checked.
