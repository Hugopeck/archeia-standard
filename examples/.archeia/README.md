# `.archeia`

This is the root of an installed Archeia Instance — the repo-local knowledge layer where project operating context lives.

## Purpose

`.archeia/` is the single predictable place for project knowledge that humans and AI agents both read and write. When an agent starts cold, it should find current work, product intent, operating constraints, and architecture evidence here — or an explicit "N/A" at the right path.

**North star:** never re-explain project context in a new chat.

## Structure

```text
.archeia/
├── .system/          # Metadata: VERSION, spec.yaml, contracts/
├── strategy/         # Direction, values, landscape, roadmap
├── operations/       # Execution, process, people, finance, compliance
├── product/          # Product strategy, design, technical, delivery
└── growth/           # Adoption, GTM, sales, success, rollout
```

Each subdirectory has its own `README.md` scaffold explaining what belongs at that path.

## What Belongs Here

- Artifacts that match each path's canonical meaning and owning domain
- Living documents edited in place (conventions, vision, specs)
- Accumulating records appended over time (decisions, learnings, retros)
- Transient work-state artifacts with lifecycle status (tasks, plans, experiments)
- Contract-surface artifacts validated by schemas (product delivery, C4 evidence)

## What Does Not Belong Here

- Unrelated project knowledge with no canonical path
- Hidden wrapper folders or ad hoc directory structures
- Content owned by another top-level domain
- Application source code, build artifacts, or secrets

## This Example

This tree is the **canonical Blueprint v0 fixture** in the Archeia Factory repo. It demonstrates every canonical path with README scaffolds and sample valid artifacts.

Validate it:

```sh
scripts/archeia_validate examples
```

For the model behind each path, see [`docs/standard/ontology.md`](../../docs/standard/ontology.md).
