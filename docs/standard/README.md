# Standard — Operational Canon

This folder holds the authoritative documentation for Archeia's operational model. If you are building tools, validating installations, or changing how Archeia works, start here.

These four documents are the source of truth for what Archeia means and what it enforces. Everything else in the repo — schemas, validators, examples, guides — derives from them.

## The Four Documents

| Document | Read for | Edit when |
|---|---|---|
| [`overview.md`](overview.md) | Motivation, principles, and what Archeia is not | The "why" or positioning changes |
| [`ontology.md`](ontology.md) | Model — domains, shapes, ownership, contracts, canonical tree | Model changes — **edit here first** |
| [`rules.md`](rules.md) | Validation checks, operations, and enforcement | Tool behavior or checks change — **edit here first** |
| [`spec.md`](spec.md) | Consolidated build contract for implementers | Mirroring model + rules changes |

## Authority Hierarchy

```text
ontology.md (Model)  ──defines──>  what the system means
rules.md     ──defines──>  what tools must enforce
spec.md      ──mirrors──>  both, for implementers
overview.md  ──explains──>  why any of it exists
```

**Rule:** Change the model in `ontology.md`. Change enforcement in rules. Mirror both in spec. Never invent only in spec.

Research docs in [`../research/`](../research/) inform these documents but do not override them. Guides in [`../guides/`](../guides/) supplement them but do not override them.

## Reading Order by Task

### Understand the system

1. [`overview.md`](overview.md) — the problem, the claim, the principles
2. [`ontology.md`](ontology.md) — domains, artifact shapes, ownership model
3. Explore [`../../examples/.archeia/`](../../examples/.archeia/) — see the model installed

### Build or extend a tool

1. [`spec.md`](spec.md) — build contract (consolidated from model + rules)
2. [`rules.md`](rules.md) — validation checks and six operations
3. [`../../contracts/`](../../contracts/) — JSON Schemas
4. [`../../scripts/archeia_validate`](../../scripts/archeia_validate) — reference implementation

### Change the model

1. Edit [`ontology.md`](ontology.md) with the conceptual change
2. Edit [`rules.md`](rules.md) with the enforcement change
3. Mirror both in [`spec.md`](spec.md)
4. Update [`../../contracts/`](../../contracts/) if schemas change
5. Update [`../../examples/`](../../examples/) fixtures to match

## Key Concepts (Quick Reference)

**Two forms:** Standard (this repo) and Instance (`.archeia/` in a project repo).

**Four domains:** `strategy/`, `operations/`, `product/`, `growth/` — each with a single owner family.

**Three shapes:**
- **Living** — edited in place; git holds history
- **Accumulating** — append-only records; never pruned
- **Transient** — work-state artifacts with status flows and retention windows

**Two contract surfaces:**
- Product delivery (`product.schema.json`) — roadmap, specs, PRDs
- C4 evidence (`c4.schema.json`) — architecture elements with file evidence

**Standard v0 philosophy:** a complete address space (~154 canonical directories). Every class of project question has exactly one settled path. Content can be sparse ("N/A", two sentences); missing paths are not allowed.

## What Is Not Here

- Practical how-tos → [`../guides/`](../guides/)
- Theoretical citations and field signals → [`../research/`](../research/)
- JSON Schemas → [`../../contracts/`](../../contracts/)
- Runnable fixtures → [`../../examples/`](../../examples/)

## Status

Archeia is at Standard v0 ([`../../VERSION`](../../VERSION)). The `init` operation is specified but not yet implemented. `validate` is implemented in [`../../scripts/archeia_validate`](../../scripts/archeia_validate).
