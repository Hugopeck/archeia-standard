# Archeia FAQ

## What is Archeia?

Archeia is my private system for giving software projects a shared knowledge layer with clear meanings, owners, lifecycle shapes, schemas, and validation rules. The Standard lives in this repo. Each project gets an Instance: the `.archeia/` layer installed by `init`.

## Where should I start?

Read [`../standard/overview.md`](../standard/overview.md) for the reason Archeia exists, [`../standard/spec.md`](../standard/spec.md) for the build contract, [`../standard/ontology.md`](../standard/ontology.md) for the model, and [`../standard/rules.md`](../standard/rules.md) for validation and operations.

## Is this a wiki replacement?

Only for project-scoped knowledge that agents need to read. Team-wide or private company knowledge can still live in a wiki. Archeia is for repo-local operating context.

## Is this a ticket system replacement?

It can replace lightweight task tracking inside a repo. It is not meant to replace customer-facing issue trackers or large multi-team planning systems.

## Why files instead of a memory database?

Files are easy for humans and agents to inspect. Paths are stable. Git gives history. A vector database or graph can be layered on top later, but the source of truth stays in the repo.

## What are the four domains?

- `strategy/`: direction and choices about where the project is going.
- `operations/`: support, process, execution, people, finance, and compliance.
- `product/`: product strategy, design, technical context, and delivery.
- `growth/`: adoption, rollout, marketing, sales, and success.

## What are the three artifact shapes?

- **Living** artifacts are edited in place.
- **Accumulating** artifacts are append-only records.
- **Transient** artifacts move through statuses and are pruned after retention.

## What replaced `domains.yaml`?

Installed repos now use `.archeia/.system/spec.yaml`. It declares domains, owners, the canonical tree, schemas, contracts, lifecycles, retention, and instance identity.

## Can an Instance extend the canonical tree?

Yes. An Instance may add stricter local rules, workflow defaults, or extra subtrees. It should not rename or redefine canonical model paths.
