# The Archeia Kernel

| | |
|---|---|
| **Status** | Draft, pre-1.0 |
| **Version** | See [`VERSION`](VERSION) |
| **Conformance** | See [`CONFORMANCE.md`](CONFORMANCE.md) |
| **Reference algorithms** | See [`REFERENCE-ALGORITHMS.md`](REFERENCE-ALGORITHMS.md) |
| **Test matrix** | See [`TEST-MATRIX.md`](TEST-MATRIX.md) |
| **Normative language** | The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, **MAY**, and **REQUIRED** in this document are interpreted per RFC 2119. |

Archeia is an **Agentic Operating System** (**AOS**) for software businesses. More specifically, Archeia is the **in-repo knowledge-layer AOS** for software businesses: structured, in-repo operating knowledge that software teams, operators, and agents read, write, and coordinate through. This document is the single normative software contract. It defines the software domains, the artifact shapes, the ownership model, the deterministic kernel operations, the canonical software tree, and the flex rules that let one shared kernel work across many kinds of software projects.

---

## 1. Scope

The kernel defines:

- the core primitives every conforming implementation understands
- the seven invariants every conforming implementation preserves
- the three lifecycle shapes: living, accumulating, transient
- the six deterministic kernel operations
- the required `archivist` agent
- the canonical software domains and their broad meanings
- the rich canonical software subtree
- the canonical cross-domain software surfaces
- the flex rules for omission, sparse use, and bounded broad interpretation
- the extension mechanism distributions use to strengthen policy and workflow

The kernel does **not** define:

- a non-software operating model
- arbitrary path renaming
- arbitrary semantic reassignment of canonical folders
- one mandatory approval workflow
- one mandatory skill roster beyond the kernel mechanics

---

## 2. Primitives

### 2.1 Root

A **root** is a project root containing an `.archeia/` directory.

### 2.2 Domain

A **domain** is a named top-level subdirectory under `.archeia/`. Archeia's kernel is software-only and defines exactly four canonical top-level domains:

- `strategy/`
- `operations/`
- `product/`
- `growth/`

### 2.3 Artifact

An **artifact** is a file inside a domain. Text-native by default: markdown, JSON, YAML, HTML. Binary artifacts are allowed only when paired with a `<file>.meta.yaml` sidecar carrying provenance, owner, schema version, and source.

### 2.4 Shape

A **shape** is one of three lifecycle categories:

- **Living** — edited in place, history in git, always current
- **Accumulating** — append-only record, status tracks relevance, never pruned
- **Transient** — flows through statuses with bounded retention, pruned when expired

### 2.5 Owner

Every top-level domain has exactly one **owner**: a writer family authorized to write to that domain.

### 2.6 Schema

A **schema** is the frontmatter and structural contract an artifact must satisfy. Schemas live as JSON Schema files under `standard/contracts/`.

### 2.7 Contract Surface

A **contract surface** is a declared software read relationship between domains. Contract surfaces are bound to concrete paths and enforced by schemas.

### 2.8 Writer / Reader

A **writer** is anything that produces artifacts. A **reader** is anything that consumes them.

### 2.9 Domain-local knowledge surfaces

A **domain-local knowledge surface** is a conventional subtree used to capture reusable local knowledge inside a domain or subdomain. The kernel defines three universal domain-local knowledge surfaces:

- `decisions/` — accumulating records of choices, tradeoffs, and rulings
- `conventions/` — living documents describing current defaults, preferences, and standard ways of doing things
- `learnings/` — accumulating records of discoveries, mistakes, and lessons worth preserving

The kernel also defines one operations-owned procedural surface:

- `operations/optimization/guides/` — living or accumulating procedural guides for repeatable work that may touch one domain, multiple domains, or the whole Archeia tree

---

## 3. Invariants

Every conforming implementation MUST uphold these invariants:

1. **Knowledge MUST live in `.archeia/` under the project root.**
2. **Every artifact MUST belong to exactly one owning top-level domain.**
3. **Every artifact MUST have exactly one lifecycle shape.**
4. **Reads MUST be free; writes MUST be owner-only.**
5. **Every factual claim in a descriptive artifact MUST cite a source.**
6. **Cross-domain dependencies MUST be declared contract surfaces, not inferred ad hoc.**
7. **History MUST be preserved.**

---

## 4. The Canonical Software Domains

Every kernel-conforming software repo MUST have exactly these four top-level domains under `.archeia/`:

```text
.archeia/
├── strategy/
├── operations/
├── product/
└── growth/
```

### 4.1 `strategy/`

**Canonical meaning.** The upstream direction surface: why this software effort should exist, what values constrain it, what landscape it operates in, and what direction it is pursuing.

**Broader semantic envelope.** `strategy/` covers business vision, founder intent, project direction, stakeholder direction, research-program direction, and major directional sequencing. It is not limited to a formal company strategy deck.

**What belongs here.**

- long-horizon intent
- values and non-negotiables
- external landscape evidence
- strategic roadmap sequencing
- strategic decisions

**What does not belong here.**

- active task tracking
- detailed implementation specs
- channel operations
- technical architecture evidence

### 4.2 `operations/`

**Canonical meaning.** The operating and delivery surface: how software work is coordinated, constrained, measured, and improved.

**Broader semantic envelope.** `operations/` is not only task execution. It includes active delivery coordination under `execution/`, operating-system observation and improvement under `optimization/`, procedural operating knowledge under `optimization/guides/`, and the people, financial, and compliance constraints that shape what execution can actually do. In a solo project, `people/` may simply capture capability and availability constraints. In an internal project, `operations/` can encode stakeholder dependencies and rollout constraints.

**What belongs here.**

- active delivery coordination, execution state, and retros
- blocker handling, operating cadences, and delivery workflows
- operating metrics, bottleneck analysis, and process improvement
- SOPs, playbooks, runbooks, and workflow guides
- staffing/capacity/ownership boundaries
- budgets and financial constraints
- compliance, governance, legal, and procurement constraints
- process, framework, rollout, adoption, and continuous-improvement work

**What does not belong here.**

- market or user discovery
- customer adoption, revenue, and channel programs
- detailed product design artifacts
- executable product specs and PRDs
- technical architecture models and codebase truth

### 4.3 `product/`

**Canonical meaning.** The product-development surface: what is being shaped, designed, specified, validated technically, and prepared for delivery.

**Broader semantic envelope.** `product/` is not only a PM surface. It includes product strategy, design, technical feasibility, and integrated product-delivery surfaces. It is the center of the software kernel because most software work is transformed here from direction into executable truth.

**What belongs here.**

- product strategy
- design contracts and feedback
- technical specs and architecture evidence
- PRDs, product execution logs, roles, and archived product artifacts

**What does not belong here.**

- company-wide finance constraints
- general operational staffing context
- raw growth channel operations

### 4.4 `growth/`

**Canonical meaning.** The go-to-market and adoption domain: how software is positioned, marketed, sold, adopted, supported, retained, expanded, and operationalized in the world.

**Broader semantic envelope.** `growth/` is not only revenue growth. It includes brand, messaging, campaigns, inbound and outbound motions, sales execution, customer success, support, internal rollout, enablement, retention, expansion, and monetization depending on the software context.

**What belongs here.**

- growth strategy and metrics
- marketing systems, brand assets, and campaigns
- sales motions, pipeline intelligence, and enablement
- customer-success, support, adoption, retention, and expansion surfaces
- growth execution programs, dashboards, logs, retros, and experiments

**What does not belong here.**

- canonical product specs
- technical architecture
- active operations execution task state

---

## 5. The Canonical Software Tree

The rich canonical software tree is part of the kernel contract. Omission is allowed where irrelevant; meanings are not.

**Universal naming rule.** Any canonical domain or subdomain MAY contain direct `decisions/`, `conventions/`, and `learnings/` subfolders when needed. These surfaces are first-class and MUST NOT be hidden under wrapper folders such as `meta/` or `memory/`. `optimization/guides/` is not universal; it is canonically owned by `operations/`.

```text
.archeia/
├── strategy/
│   ├── vision/
│   ├── values/
│   ├── landscape/
│   │   ├── competition/
│   │   ├── industry/
│   │   └── market/
│   ├── roadmap/
│   ├── decisions/
│   ├── conventions/
│   └── learnings/
├── operations/
│   ├── execution/
│   │   ├── tasks/
│   │   ├── projects/
│   │   ├── plans/
│   │   ├── retros/
│   │   ├── decisions/
│   │   ├── conventions/
│   │   └── learnings/
│   ├── optimization/
│   │   └── guides/
│   ├── people/
│   ├── finance/
│   ├── compliance/
│   ├── decisions/
│   ├── conventions/
│   └── learnings/
├── product/
│   ├── strategy/
│   │   ├── market/
│   │   ├── users/
│   │   ├── roadmap/
│   │   ├── metrics/
│   │   ├── decisions/
│   │   ├── conventions/
│   │   └── learnings/
│   ├── design/
│   │   ├── flows/
│   │   ├── protos/
│   │   ├── feedback/
│   │   ├── assets/
│   │   ├── decisions/
│   │   ├── conventions/
│   │   └── learnings/
│   ├── technical/
│   │   ├── specs/
│   │   ├── studies/
│   │   ├── architecture/
│   │   │   ├── c4/
│   │   │   ├── analysis/
│   │   │   └── views/
│   │   ├── devs/
│   │   ├── decisions/
│   │   ├── conventions/
│   │   └── learnings/
│   └── execution/
│       ├── prds/
│       ├── plans/
│       ├── retros/
│       ├── logs/
│       ├── roles/
│       ├── archive/
│       ├── decisions/
│       ├── conventions/
│       └── learnings/
└── growth/
    ├── strategy/
    │   ├── roadmap/
    │   ├── segments/
    │   ├── positioning/
    │   ├── metrics/
    │   ├── channel-mix/
    │   ├── pricing/
    │   ├── decisions/
    │   ├── conventions/
    │   └── learnings/
    ├── marketing/
    │   ├── brand/
    │   ├── messaging/
    │   ├── assets/
    │   ├── style/
    │   ├── campaigns/
    │   ├── content/
    │   ├── web/
    │   ├── inbound/
    │   ├── outbound/
    │   ├── community/
    │   ├── events/
    │   ├── decisions/
    │   ├── conventions/
    │   └── learnings/
    ├── sales/
    │   ├── outbound/
    │   ├── pipeline/
    │   ├── accounts/
    │   ├── enablement/
    │   ├── objections/
    │   ├── pricing/
    │   ├── win-loss/
    │   ├── decisions/
    │   ├── conventions/
    │   └── learnings/
    ├── success/
    │   ├── onboarding/
    │   ├── activation/
    │   ├── adoption/
    │   ├── retention/
    │   ├── expansion/
    │   ├── enablement/
    │   ├── support/
    │   ├── decisions/
    │   ├── conventions/
    │   └── learnings/
    └── execution/
        ├── plans/
        ├── programs/
        ├── experiments/
        │   ├── running/
        │   └── learnings/
        ├── logs/
        ├── retros/
        ├── dashboards/
        ├── decisions/
        ├── conventions/
        └── learnings/
```

---

## 6. Canonical Meanings for Major Subtrees

### 6.1 `strategy/vision/`

**Canonical meaning.** Long-horizon purpose, mission, thesis, and what the software effort refuses to pursue.

**Broad interpretation.** Can represent founder intent, product-program intent, internal initiative mission, or lab-software intent.

### 6.2 `strategy/values/`

**Canonical meaning.** Non-negotiables and principles.

**Broad interpretation.** Can capture product principles, trust posture, brand constraints, safety posture, operator constraints, or internal service values.

### 6.3 `strategy/roadmap/`

**Canonical meaning.** Directional sequencing.

**Broad interpretation.** Can represent a company roadmap, project roadmap, internal rollout sequence, or research-software direction sequence.

### 6.4 `operations/people/`

**Canonical meaning.** People and capability constraints that shape execution.

**Broad interpretation.** Can include org maps, ownership boundaries, support capacity, hiring gaps, collaborator maps, or solo-operator capacity limits. This path records capability and capacity as operating constraints on delivery; it does not replace product truth or growth hiring/adoption programs.

### 6.5 `operations/finance/`

**Canonical meaning.** Financial constraints and operating finance context that shape execution.

**Broad interpretation.** Can include budgets, runway constraints, procurement constraints, vendor cost context, approval thresholds, or funding limits that change what execution is possible. This path governs budget reality for delivery; it does not replace `growth/` revenue operations or `strategy/` directional planning.

### 6.6 `operations/compliance/`

**Canonical meaning.** Constraints imposed by legal, privacy, compliance, procurement, or internal governance regimes.

**Broad interpretation.** Can be light in low-risk projects and heavy in regulated or internal-enterprise contexts. This path captures governance and risk constraints on how work is carried out; it does not replace product technical architecture or growth trust/adoption programs.

### 6.7 `operations/optimization/`

**Canonical meaning.** The operating-system improvement surface for execution.

**Broad interpretation.** Can include operating metrics, adherence monitoring, bottleneck detection, workflow diagnostics, process redesign, service-level review, rollout and adoption material, framework-setting, and continuous-improvement loops. `operations/optimization/` turns evidence from execution into better ways of executing and houses the procedural operating knowledge that makes those improvements repeatable.

### 6.8 `product/strategy/market/`

**Canonical meaning.** Product-relevant external or deployment landscape.

**Broad interpretation.** Can include external category positioning, competitor evidence, ecosystem mapping, internal stakeholder environment, or deployment-context intelligence.

### 6.9 `product/design/protos/`

**Canonical meaning.** Durable design or interaction contracts tied to prototypes.

**Broad interpretation.** Can include high-fidelity prototypes, wireframes, flow sketches, interactive references, and linked external design sources.

### 6.10 `product/technical/specs/`

**Canonical meaning.** Executable software specs.

**Broad interpretation.** This is the kernel path for requirements, feature specs, API contracts, technical requirement documents, and any other durable software spec an execution surface will rely on.

### 6.11 `growth/`

**Canonical meaning.** Go-to-market and adoption.

**Broad interpretation.** Can mean revenue growth, brand development, demand generation, sales motion, customer success, support, internal adoption, rollout, enablement, retention, or expansion depending on the software context.

### 6.12 Universal `decisions/`

**Canonical meaning.** The accumulating record of local choices, tradeoffs, and rulings within a domain or subdomain.

**Broad interpretation.** May capture ADR-style technical decisions, strategic decisions, design rulings, operating policy choices, or growth-program decisions as long as the decision remains local to the owning path.

### 6.13 Universal `conventions/`

**Canonical meaning.** The living statement of local defaults, preferences, and standard ways of doing things within a domain or subdomain.

**Broad interpretation.** May capture naming conventions, authoring defaults, expected review patterns, default sequencing, recurring heuristics, and house style. `conventions/` is softer than formal external standards and stronger than individual preference.

### 6.14 Universal `learnings/`

**Canonical meaning.** The accumulating record of lessons, mistakes, discoveries, and reusable insights within a domain or subdomain.

**Broad interpretation.** May capture postmortem lessons, user-research takeaways, execution lessons, architectural lessons, or go-to-market findings, provided they are preserved as local learning rather than rewritten into current canonical truth.

### 6.15 `operations/optimization/guides/`

**Canonical meaning.** The procedural operating surface for repeatable work.

**Broad interpretation.** `operations/optimization/guides/` may contain how-tos, SOPs, playbooks, runbooks, workflow guides, rollout instructions, adoption material, and knowledge-hub content for one domain, multiple domains, or the whole Archeia tree. A guide may explain how to carry out repeatable work involving `strategy/`, `product/`, `growth/`, or cross-domain coordination, but the guide itself remains an `operations/` artifact because it governs execution behavior rather than domain truth. These guides are the procedural output of operational learning, frameworks, and process improvement.

---

## 7. Lifecycle Expectations

The kernel defines default lifecycle expectations for the canonical software tree.

### 7.1 `strategy/`

- `vision/`, `values/`, `roadmap/` → living
- `landscape/*/` → accumulating
- `conventions/` → living
- `decisions/`, `learnings/` → accumulating

### 7.2 `operations/`

- `execution/tasks/`, `execution/projects/`, `execution/plans/` → transient
- `execution/retros/` → accumulating
- `optimization/`, `optimization/guides/`, `people/`, `finance/`, `compliance/` → living by default unless a distribution adds accumulating record types
- `conventions/` → living
- `decisions/`, `learnings/` → accumulating

### 7.3 `product/`

- `product/strategy/roadmap/`, `product/strategy/metrics/` → living
- `product/strategy/market/`, `product/strategy/users/` → accumulating by default
- `product/design/flows/`, `product/design/protos/` → living
- `product/design/feedback/` → accumulating
- `product/design/assets/` → living, binary allowed with sidecars
- `product/technical/specs/` → living
- `product/technical/studies/` → accumulating by default
- `product/technical/architecture/c4/`, `analysis/`, `views/`, `devs/` → living
- `product/execution/prds/`, `roles/` → living
- `product/execution/plans/` → transient
- `product/execution/retros/`, `logs/`, `archive/` → accumulating
- all `conventions/` subtrees → living
- all `decisions/` and `learnings/` subtrees → accumulating

### 7.4 `growth/`

- `strategy/roadmap/`, `strategy/metrics/`, `strategy/segments/`, `strategy/positioning/`, `strategy/channel-mix/`, `strategy/pricing/` → living
- `marketing/brand/`, `messaging/`, `assets/`, `style/`, `campaigns/`, `content/`, `web/`, `inbound/`, `outbound/`, `community/`, `events/` → living
- `sales/outbound/`, `pipeline/`, `accounts/`, `enablement/`, `objections/`, `pricing/` → living
- `success/onboarding/`, `activation/`, `adoption/`, `retention/`, `expansion/`, `enablement/`, `support/` → living
- `execution/dashboards/` → living
- all `conventions/` subtrees → living
- `sales/win-loss/`, `execution/logs/`, `execution/retros/`, all `decisions/` subtrees, all `learnings/` subtrees → accumulating
- `execution/plans/`, `execution/programs/`, `execution/experiments/running/` → transient

See [`TEMPORAL_MODEL.md`](TEMPORAL_MODEL.md) for the shape rules themselves.

---

## 8. Ownership Model

Every file under `.archeia/` MUST have exactly one owning **top-level** domain.

| Domain | Permitted shapes | Reads from |
|---|---|---|
| `strategy/` | living, accumulating | MAY read `growth/` and `operations/` evidence |
| `operations/` | living, accumulating, transient | `strategy/`, `product/` |
| `product/` | living, accumulating, transient | `strategy/`, `operations/`, `growth/` |
| `growth/` | living, accumulating, transient | `strategy/`, `operations/finance/`, `product/` |

`product/strategy/`, `product/design/`, `product/technical/`, and `product/execution/` are not separate ownership domains.

Ownership rules:

1. **Write to your top-level domain only.**
2. **Read across domains freely.**
3. **No implicit writes.**
4. **Schema enforcement at write time.**
5. **Parallelism via delegation, not concurrent access.**

---

## 9. Canonical Software Contract Surfaces

The kernel includes two canonical software contract surfaces.

### 9.1 Product delivery surface → operations execution

**Paths.**

- `product/strategy/roadmap/*.md`
- `product/technical/specs/*.md`
- `product/execution/prds/*.md`

**Purpose.** These artifacts are the durable delivery contract operations execution relies on.

**Who reads it.** `operations/execution/`.

### 9.2 Technical evidence surface

**Paths.**

- `product/technical/architecture/c4/*.json`

**Purpose.** Machine-readable architecture evidence for product feasibility review and operations scoping.

**Who reads it.** `product/` and `operations/`.

These surfaces are enforced through `contracts/product.schema.json` and `contracts/c4.schema.json`.

---

## 10. Flex Rules

The kernel is thick, but flexibility is explicit and bounded.

1. **Canonical names stay fixed.** Renaming canonical folders is not kernel-conforming.
2. **Canonical meanings stay fixed.** A path keeps its kernel meaning.
3. **Omission is allowed.** If a subtree is irrelevant, it MAY remain absent or empty.
4. **Sparse use is normal.** Small or specialized software projects do not need to populate every subtree.
5. **Broader interpretation is allowed within the canonical meaning.** A path may be used broadly if it stays inside the semantic envelope defined by this kernel.
6. **Arbitrary repurposing is not allowed.** A canonical path MAY NOT be reassigned to an unrelated role.
7. **Distributions may strengthen requirements.** A distribution may require heavier use of specific kernel paths.
8. **Distributions may add subtrees.** A distribution may extend the tree, but SHOULD NOT redefine canonical meanings.

---

## 11. The Three Lifecycle Shapes

A conforming implementation MUST:

- recognize all three shapes
- apply each shape's rules
- store history according to shape
- map transient statuses to temporal state

See [`TEMPORAL_MODEL.md`](TEMPORAL_MODEL.md) for the full specification.

---

## 12. The Six Kernel Operations

Every conforming distribution MUST provide these six deterministic operations:

- `init`
- `validate`
- `write`
- `transition`
- `prune`
- `history`

They inspect or mutate `.archeia/` while enforcing ownership, shape, schema, lifecycle, retention, and contract rules.

---

## 13. Required Tooling

Every conforming distribution MUST provide:

- `<distribution>:init`
- `<distribution>:validate`
- `<distribution>:write`
- `<distribution>:transition`
- `<distribution>:prune`
- `<distribution>:history`

---

## 14. Inherent Agent

Every conforming distribution MUST provide:

- `archivist` — manages past-state transitions, supersession decisions, and retention policy

---

## 15. Extension Mechanism

A distribution extends the kernel by providing:

1. `standard/domains.yaml`
2. status vocabularies and temporal mappings for transient artifacts
3. JSON Schemas under `standard/contracts/`
4. implementations of the six kernel operations and the `archivist` agent
5. stricter usage requirements, workflow defaults, governance, and audience-specific emphasis over the kernel tree

Distributions do not replace the kernel tree. They specialize how it is used.

---

## 16. How To Use This Kernel Across Software Project Types

### 16.1 Solo builder

- `operations/people/` may only record personal capacity and support constraints
- `growth/` may mean acquisition, monetization, or simple user uptake
- many kernel paths may remain sparse

### 16.2 Startup SaaS

- `strategy/roadmap/`, `operations/finance/`, and `growth/` are typically heavier
- `product/technical/specs/` and `product/execution/prds/` become central handoff surfaces

### 16.3 Internal project

- `growth/` often means adoption, rollout, enablement, stakeholder pull, and retention of internal users
- `operations/compliance/` may carry heavier internal governance and procurement constraints

### 16.4 Personal software project

- many kernel subtrees may be omitted
- `strategy/` may be brief
- `operations/people/` may be minimal
- the shared map still helps tools and agents know where truth belongs

### 16.5 Research-lab software project

- `product/technical/studies/` and `learnings/` tend to be heavier
- `growth/` may mean adoption, usage, community uptake, or deployment expansion rather than revenue

Across all of these, omission and sparse use are normal. Renaming and unrelated repurposing are not.

---

## 17. Harness Boundary

Archeia is the contract for the **knowledge layer**. The harness is the runtime that loads skills, invokes models, manages context, enforces safety, and reads/writes the filesystem.

The one hard harness requirement is:

> **Writes to `.archeia/` MUST be flushed to disk before compaction may discard them from in-context state.**

If a harness compacts away a pending write to `.archeia/product/technical/specs/team-invites.md`, that is a harness bug, not an Archeia problem.

---

## 18. Skill Format

Skills live outside `.archeia/`. Minimum frontmatter:

```yaml
---
name: <skill-name>
description: <trigger sentence>
---
```

Recommended extended fields:

```yaml
---
name: review-product
description: review the current product surfaces and propose updates
version: 0.1.0
parameters:
  - name: product_path
    type: directory
    required: true
reads:
  - .archeia/strategy/
  - .archeia/product/
writes:
  - .archeia/product/strategy/roadmap/
  - .archeia/product/technical/specs/
  - .archeia/product/execution/prds/
pattern: consolidation
---
```

---

## 19. Validation

A repo is **kernel-conforming** if `archeia:validate` passes with no errors against it. A conforming validator MUST check:

1. `.archeia/` exists at the project root
2. the four canonical top-level domains exist
3. no extra top-level canonical software domains replace or rename the kernel ones
4. every artifact belongs to a declared top-level domain
5. every artifact has a declared shape and conforms to its base schema
6. every artifact conforms to any applicable artifact-type schema
7. the canonical software contract surfaces satisfy their schemas
8. every transient artifact has a valid status
9. every terminal transient artifact has a terminal timestamp
10. kernel omission/sparsity is allowed where paths are irrelevant or empty
11. ownership is respected as an advisory check

---

## 20. What the Kernel Explicitly Does Not Do

The kernel does not:

- define a non-software operating model
- allow arbitrary folder renaming
- allow arbitrary semantic drift of canonical paths
- mandate a specific agent framework
- provide a UI
- replace git
- define one universal approval workflow
- provide search or embeddings

---

## 21. Versioning

The kernel uses semantic versioning, with the usual pre-1.0 caveat that breaking revisions may still land as `0.x` minor bumps while the kernel is stabilizing.

- **Major** — breaking changes to primitives, invariants, operations, or required distribution tooling
- **Minor** — additive changes and pre-1.0 structural revisions
- **Patch** — clarifications and non-normative fixes

The current kernel version is **0.5.0**.

---

## 22. Summary

The Archeia Kernel is the thick software contract for an AOS for software businesses: four canonical domains, a rich canonical tree, strict meanings, bounded flexibility, deterministic operations, and a distribution layer that strengthens usage without replacing the shared map.
