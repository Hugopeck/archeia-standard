# Archeia Model

The model defines what Archeia means. It names the core concepts, the `.archeia/` folders, the lifecycle shapes, and the ownership model. **This is the authoritative source for model changes** — edit here first, then mirror in [`rules.md`](rules.md) and [`spec.md`](spec.md).

Rules and validators are described in [`rules.md`](rules.md). The build contract is in [`spec.md`](spec.md). Theoretical basis and citations live in [`../research/theoretical-basis.md`](../research/theoretical-basis.md) (research only, not operational canon).

## Scope

**Archeia** is a software factory. The **Standard** is the reusable source package maintained in this repository. An **Instance** is the `.archeia/` operating layer that `init` installs into a project repo.

> **Note:** This document is the **Model** in outward docs. The internal path remains `ontology.md`.

This model defines what an Instance means: folders, shapes, ownership, and contracts. It does not define a non-software operating model, a hosted service, a UI, one universal approval workflow, or a public adoption process.

## Primitives

- **Instance**: the installed `.archeia/` layer in a project repo.
- **Project root**: a software repo that hosts an Instance.
- **Domain**: one top-level folder under `.archeia/`.
- **Artifact**: a file inside a domain.
- **Shape**: the lifecycle category of an artifact: living, accumulating, or transient.
- **Owner**: the writer family allowed to write a top-level domain.
- **Schema**: the frontmatter or structured-data contract an artifact must satisfy.
- **Contract surface**: a declared read relationship between domains.
- **Writer**: anything that produces artifacts.
- **Reader**: anything that consumes artifacts.

## Domains

Every Instance uses four top-level domains:

- `strategy/`: direction, values, landscape, roadmap, and strategy-owned execution.
- `operations/`: support, improvement, execution, people, finance, compliance, and process.
- `product/`: product strategy, design, technical evidence, and delivery context.
- `growth/`: adoption, go-to-market, sales, success, support, and rollout.

Each artifact belongs to exactly one top-level domain.

### Why business-shaped names for every project

The four domains use business vocabulary on purpose. From a general view, **every endeavor is a kind of business** — not only startups or companies.

Even a small weekend personal project has:

- **Strategy** — a vision, goals, and tradeoffs about what to build.
- **Growth** — a story you sell to yourself, your partner, a friend at the bar; adoption and audience even when informal.
- **Operations / compliance** — boundaries: house rules, family agreements, platform policies, ethics postures, what you refuse to ship.
- **Finance / cost** — effort, opportunity cost, and sunk cost even when the cash outlay is zero.

The names may feel heavy for a tiny repo. The decomposition is meant to be universal, not corporate cosplay. Sparse or "N/A" answers are valid; the paths still give agents settled coordinates.

## Canonical Tree

The full folder tree is shown in `examples/`. A project may use the tree sparsely, but canonical names and meanings do not change.

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

Ownership is the concurrency model for parallel human and agent work. Delegation is allowed, but the owning domain remains responsible for the write.

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
- Arbitrary repurposing of canonical paths is invalid.
- An Instance may add stricter local rules or extra subtrees, but should not redefine canonical paths.

## Evidence Policy

Descriptive artifacts should cite their sources. This is a policy until Archeia defines a concrete citation grammar that validators can check without guessing.

## Block Model

Archeia treats domains, artifacts, procedures, and agent roles as lightweight system blocks. This is how agents read the model — not a requirement to model every workflow step.

A block should be clear about:

- **Boundary**: what it owns and what it does not own.
- **State**: the properties that describe its current condition.
- **Inputs**: the files, events, or context it consumes.
- **Outputs**: the artifacts, summaries, decisions, or signals it produces.
- **Interfaces**: the stable handoffs other blocks can rely on.
- **Constraints**: the rules that keep writes and transitions safe.
- **Agent roles**: the writers or readers expected to operate it.

Define the outside of the block with care. Let humans and agents handle the inside with judgment.
