# Archeia Ontology

The ontology defines what Archeia means. It names the core concepts, the canonical folders, the lifecycle shapes, and the ownership model.

Rules and validators are described in [`rules.md`](rules.md). Terminology and citations live in [`../research/terminology.md`](../research/terminology.md).

## Scope

Archeia defines a software-project knowledge layer under `.archeia/`. It does not define a non-software operating model, a hosted service, a UI, or one universal approval workflow.

## Primitives

- **Root**: a project root containing `.archeia/`.
- **Domain**: one top-level folder under `.archeia/`.
- **Artifact**: a file inside a domain.
- **Shape**: the lifecycle category of an artifact: living, accumulating, or transient.
- **Owner**: the writer family allowed to write a top-level domain.
- **Schema**: the frontmatter or structured-data contract an artifact must satisfy.
- **Contract surface**: a declared read relationship between domains.
- **Writer**: anything that produces artifacts.
- **Reader**: anything that consumes artifacts.

## Domains

Every conforming software project uses four top-level domains:

- `strategy/`: direction, values, landscape, roadmap, and strategy-owned execution.
- `operations/`: support, improvement, execution, people, finance, compliance, and process.
- `product/`: product strategy, design, technical evidence, and delivery context.
- `growth/`: adoption, go-to-market, sales, success, support, and rollout.

Each artifact belongs to exactly one top-level domain.

## Canonical Tree

The full canonical tree is shown in `examples/`. A project may use the tree sparsely, but canonical names and meanings do not change.

The top-level shape is:

```text
.archeia/
├── strategy/
├── operations/
├── product/
└── growth/
```

Important subtrees include:

- `operations/optimization/processes/`: repeatable operating methods, SOPs, runbooks, and process knowledge.
- `product/technical/specs/`: executable software specs.
- `product/technical/architecture/c4/`: machine-readable architecture evidence.
- `product/execution/prds/`: integrated buildable product missions.
- `growth/execution/experiments/`: growth experiment state and learnings.

Across canonical domains and subdomains, three local knowledge surfaces may appear directly:

- `decisions/`: accumulating records of choices and tradeoffs.
- `conventions/`: living documents for local defaults and ways of working.
- `learnings/`: accumulating records of lessons and discoveries.

These surfaces should not be hidden under wrappers such as `meta/` or `memory/`.

## Lifecycle Shapes

### Living

A living artifact is edited in place. It represents the current truth for one concept. Git holds its history.

Examples: vision docs, process docs, product specs, architecture views, dashboards, conventions.

### Accumulating

An accumulating artifact is an append-only record. New records are added; old records stay on disk. Status fields can mark records as active, superseded, archived, or retired.

Examples: decisions, learnings, retros, research snapshots, technical studies, win-loss records.

### Transient

A transient artifact moves through statuses and is pruned after a retention window once it reaches a terminal status. Git preserves the old file after pruning.

Examples: tasks, plans, projects, programs, and running experiments.

## Ownership

Each top-level domain has one owner family. Writers may read across domains, but writes go through the owning domain.

Ownership keeps parallel agent work simple. Delegation is allowed, but the owning domain remains responsible for the write.

## Contract Surfaces

Archeia defines two canonical cross-domain contract surfaces:

- Product delivery: `product/strategy/roadmap/*.md`, `product/technical/specs/*.md`, and `product/execution/prds/*.md`.
- Technical evidence: `product/technical/architecture/c4/*.json`.

These surfaces are validated by schemas in `contracts/` when installed into `.archeia/.system/contracts/`.

## Flex Rules

- Canonical names stay fixed.
- Canonical meanings stay fixed.
- Sparse use is normal.
- Omission is allowed when a subtree is irrelevant.
- Broader interpretation is allowed inside the defined meaning.
- Arbitrary repurposing is not conforming.
- Distributions may add stricter rules or extra subtrees, but should not redefine canonical paths.

## Evidence Policy

Descriptive artifacts should cite their sources. This is a policy until the standard defines a concrete citation grammar that validators can check without guessing.
