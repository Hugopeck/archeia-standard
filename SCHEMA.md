# Archeia Standard — Canonical Software Application

| | |
|---|---|
| **Status** | Draft, pre-1.0 |
| **Version** | See [`VERSION`](VERSION) |
| **Conformance** | See [`CONFORMANCE.md`](CONFORMANCE.md) §9 (software-distribution conformance) |
| **Normative language** | The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, **MAY**, and **REQUIRED** in this document are interpreted per [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119). |

> **This document is the Repository Contract for software projects using Archeia.** It is the standard application of [the Archeia Kernel](KERNEL.md) to software — five domains, their ownership, their lifecycle shapes, and the three cross-domain contracts every software project MUST enforce. It is distribution-agnostic: it does not commit to any specific skill roster, agent roster, or ethos. Those belong in [distributions](distributions/).
>
> The "Repository Contract" framing is deliberate. The five-domain layout, the lifecycle assignments, and the three cross-domain contracts together specify what a tool can rely on finding in *any* Archeia software repo. A tool that processes `.archeia/` trees from multiple projects MUST treat this document as its target.
>
> If you are implementing Archeia for a software project, this is what you cite for the directory layout and domain semantics. If you are writing a tool that consumes `.archeia/` trees across many projects, this is the target your tool MUST expect.

---

## 1. Scope

This document defines:

- The five canonical domains for software projects and their purposes
- The lifecycle shape of every artifact type in each domain (living, accumulating, or transient — per [the lifecycle model](TEMPORAL_MODEL.md))
- The ownership model (one writer per domain, free reads across domains)
- The three enforceable cross-domain contracts
- Colocated files outside `.archeia/` that are still owned by Archeia domains

It does **not** define:

- Which specific skills or agents produce each artifact (see [distributions](distributions/))
- Which retention windows apply to transient artifacts (see [distributions](distributions/))
- Which approval workflows govern status transitions (policy, not spec)
- Whether to use markdown, JSON, or HTML for specific artifacts (the shape's base schema allows any text-native format; distributions may constrain further)

For the abstract substrate this document builds on, see [`KERNEL.md`](KERNEL.md). For the five fundamental truths, see [`PRINCIPLES.md`](PRINCIPLES.md). For the lifecycle model, see [`TEMPORAL_MODEL.md`](TEMPORAL_MODEL.md). For a complete, opinionated software implementation, see [`distributions/solo-builder.md`](https://github.com/Hugopeck/archeia/blob/main/DISTRIBUTION.md).

---

## 2. The five canonical domains (the Repository Contract)

Every software project that uses Archeia MUST have exactly five domains under `.archeia/`. They are not optional and not extensible: this is the canonical software answer. A project that needs different domains MUST declare a different distribution and extend the kernel directly rather than modify this document.

```
.archeia/
├── business/        # Why we're building, for whom, how we earn
├── product/         # Product truth: what users need, what we're building, and why
├── codebase/        # AI-maintained repo intelligence: what the code is, right now
├── growth/          # How we acquire, retain, monetize
└── execution/       # What we're doing right now
```

Each domain has one owner (a writer family declared by the distribution), permitted lifecycle shapes, and a declared set of cross-domain read relationships. The rest of this section specifies each domain in detail.

### 2.1 `business/`

**Purpose.** Captures the holistic business vision — why this product exists, who it's for, how it makes money, and what the competitive landscape looks like. Business is the upstream origin of every other domain's intent.

**Permitted shapes:** living, accumulating, transient.

| Path | Shape | What it is |
|---|---|---|
| `business/vision/vision.md` | Living | The current vision document, evolved over time. Captures premise, target user, value proposition, scope, and differentiation. Edited in place; history in git. |
| `business/strategy/strategy.md` | Living | Current business model, positioning, pricing, and go-to-market stance. Evolved in place. |
| `business/landscape/*.md` | Accumulating | Dated market research snapshots. Each snapshot is its own record, kept forever — later strategy decisions reference them. |
| `business/drafts/*.md` | Transient | Draft proposals that either advance into a living document or are discarded. Retention window: short (distribution-defined). |

**Owner:** declared by the distribution (typically `business-skills` or `product-skills` depending on how the distribution partitions this work).

**Reads from:** nothing. Business is the upstream origin.

**Read by:** `product/` (for vision context when reviewing drafts), `growth/` (for strategy context when planning channels).

### 2.2 `product/`

**Purpose.** The product truth domain: what user problems matter, what experience we are committing to, what features exist or are planned, and what evidence or decisions justify that product direction. `product/` turns business intent into product commitments that execution can plan against.

Product work often happens in external product surfaces: design tools, prototype tools, research repositories, feedback systems, analytics dashboards, support systems, and planning tools. Those tools MAY be authoritative working surfaces for their native medium, but they are not the Archeia contract surface. `.archeia/product/` stores the durable product contract, the source references it depends on, the extraction/freshness metadata, and the decision trail.

**Permitted shapes:** living, accumulating.

| Path | Shape | What it is |
|---|---|---|
| `product/product.md` | Living | Canonical product index and current-state summary. Names the product, active scope, primary users, product constraints, priority model, and indexes the roadmap and feature specs. See [`product.schema.json`](contracts/product.schema.json) for the required sections. |
| `product/roadmap.md` | Living | Current sequencing of product bets, milestones, releases, and now/next/later priorities. Evolved in place; history in git. |
| `product/features/*.md` | Living | Canonical feature specs. Each feature has a stable feature ID, user value, acceptance criteria, status, dependencies, and links to requirements, design contracts, feedback, decisions, external sources, and codebase evidence. |
| `product/requirements/*.md` | Living | PRDs and requirement specs while they are current. A requirement may cite external research, prototype, feedback, analytics, support, or planning sources; it may be refined in place until represented by one or more feature specs or superseded by a decision. |
| `product/design/*.md` | Living | Product/design contracts for experiences, flows, states, interaction rules, visual references, content rules, and implementation-relevant design evidence. May be derived from external design or prototype tools, but MUST consolidate the executable product/design contract locally. |
| `product/feedback/*.md` | Accumulating | User interviews, support themes, sales notes, research digests, analytics findings, prototype-test results, and other product evidence. Each record is preserved so future product decisions can cite the original signal. |
| `product/decisions/*.md` | Accumulating | Product decisions and ADRs. Each decision is its own file, written once, referenced forever. Supersession writes a new decision; both old and new stay on disk. |

**Note:** product has **no transient artifacts.** Rough opportunities and strategic proposals live in `business/drafts/` until they become product work. Once accepted into product, they are consolidated into `product/product.md`, `product/roadmap.md`, `product/requirements/*.md`, `product/features/*.md`, or `product/decisions/*.md`. Product artifacts evolve in place or accumulate as records; they do not flow through a pruneable transient lifecycle.

**Owner:** declared by the distribution.

**Reads from:** `business/drafts/` and `business/strategy/` (for intent and positioning), `codebase/model/c4/` (for feasibility validation), and `growth/metrics/` or `growth/experiments/` when product direction depends on funnel or retention evidence.

**Read by:** `codebase/` (for framing), `execution/` (to generate projects and tasks from roadmap and feature specs), `growth/` (for feature context when planning channels).

**External source convention.** Product artifacts MAY cite external product sources in frontmatter. Writers SHOULD use this convention whenever a product artifact depends on a source outside the repo:

```yaml
external_sources:
  - type: design_tool | prototype | research_repo | feedback_system | analytics | support | planning | other
    name: "Tool or source name"
    url: "https://..."
    object_id: "optional external object identifier"
    extraction_method: mcp | api | export | manual | other
    source_version: "optional version, timestamp, revision, or snapshot id"
    last_read: 2026-05-11T10:00:00Z
    source_status: current | stale | unreachable | insufficient
```

External sources are evidence and working surfaces, not substitutes for Archeia artifacts. A product artifact that depends on an external source SHOULD consolidate the implementation-relevant product truth locally and use `source_status` plus `last_read` as a staleness signal.

### 2.3 `codebase/`

**Purpose.** The AI-maintained, evidence-cited representation of what the code is right now: machine-readable models, generated analyses, inferred conventions, developer guidance, and renderable views derived from source, config, and git history. No human product decisions live here; only observations and interpretations grounded in codebase evidence.

**Permitted shapes:** living **only**.

| Path | Shape | What it is |
|---|---|---|
| `codebase/model/c4/system.json` | Living | C4 System Context as structured JSON. |
| `codebase/model/c4/containers.json` | Living | C4 Container data. |
| `codebase/model/c4/components.json` | Living | C4 Component data. |
| `codebase/model/c4/dataflow.json` | Living | Primary data flows (when present). |
| `codebase/model/c4/entities.json` | Living | ORM/schema entities (when present). |
| `codebase/model/c4/statemachine.json` | Living | State machines (when present). |
| `codebase/analysis/repository.md` | Living | Generated repository scan: structure, modules, size, languages, dependencies, test surface, and notable gaps. |
| `codebase/analysis/history.md` | Living | Generated git-history analysis: churn, contributors, hotspots, bus-factor risks, velocity, and notable inflection points. |
| `codebase/analysis/dependencies.md` | Living | Generated dependency analysis: package graph, dependency risk, version posture, and integration boundaries. |
| `codebase/analysis/testing.md` | Living | Generated test analysis: commands, coverage posture, test architecture, flaky areas, and missing test seams. |
| `codebase/analysis/risks.md` | Living | Generated maintainability, security, operational, and architecture-risk synthesis. |
| `codebase/conventions/coding.md` | Living | Inferred codebase conventions: style, patterns, layering, naming, testing norms, and local rules observed in the repo. |
| `codebase/guide/developer.md` | Living | Generated developer/codebase guide: setup, commands, package map, common workflows, and implementation orientation. |
| `codebase/views/architecture/*.mmd` | Living | Generated renderable architecture views, typically Mermaid, derived from `codebase/model/c4/`. |

> **`codebase/model/c4/` is the machine-readable contract surface.** Other domains MUST rely on `codebase/model/c4/*.json` unless a distribution explicitly declares another cross-domain contract. These files are read by `product/decisions/` (via [`c4.schema.json`](contracts/c4.schema.json)) when validating feasibility. They are not documentation pages — they are structured evidence other domains rely on.
>
> **The rest of `.archeia/codebase/` is generated codebase intelligence.** `analysis/`, `conventions/`, `guide/`, and `views/` are owned by codebase writers, regenerated from source evidence, and safe for agents to update. They are not the project's human-owned documentation surface.
>
> **Codebase artifacts inside `.archeia/` are purely shape 1 — living artifacts only.** The codebase domain has no accumulating records and no transient artifacts. Every artifact is regenerated from source evidence, edited in place as the code evolves, and preserved in git.

**Owner:** declared by the distribution (typically `codebase-skills`). Codebase writers own `.archeia/codebase/` by default. Canonical Archeia does not grant codebase writers ownership of `docs/`.

**Reads from:** the codebase itself (source files, config, git history) and optionally `product/product.md`, `product/roadmap.md`, and `product/features/*.md` to contextualize architecture against intent.

**Read by:** `product/` (for feasibility validation during draft review), `execution/` (for technical context when scoping work), every other domain as ground-truth reference.

**Regeneration contract.** Every file in `.archeia/codebase/` is regenerable — delete any of them and run the codebase skills again and they will be rebuilt from source evidence.

### 2.4 `growth/`

**Purpose.** How we acquire, retain, and monetize users. Growth is its own discipline — it reads from both business (strategy, pricing) and product (features, specs) but is subordinate to neither.

**Permitted shapes:** living, accumulating, transient.

| Path | Shape | What it is |
|---|---|---|
| `growth/metrics/current.md` | Living | Current KPIs, funnel definitions, benchmarks, cohort analyses. Updated in place. |
| `growth/channels/*.md` (retired) | Accumulating | Retired channels with their performance history. Kept forever so later channels can learn from them. |
| `growth/experiments/*.md` (concluded with learnings) | Accumulating | Concluded experiments whose learnings outlive the raw running state. |
| `growth/channels/*.md` (active) | Transient | Running acquisition channels. When retired, either promoted to an accumulating record with outcomes or pruned. |
| `growth/experiments/*.md` (running) | Transient | Running experiments. When concluded, either promoted to an accumulating record or pruned. |

**Owner:** declared by the distribution.

**Reads from:** `business/strategy/strategy.md` (for positioning and pricing context), `product/product.md`, `product/roadmap.md`, and `product/features/*.md` (for product and feature context).

**Read by:** `business/` (to inform strategy iteration).

### 2.5 `execution/`

**Purpose.** What we're doing right now. Active projects, tasks, plans, and retrospectives. The operational state of the work — the place where product intent becomes shipped code.

**Permitted shapes:** accumulating, transient. (No living documents — execution is all action, no summary living doc.)

| Path | Shape | What it is |
|---|---|---|
| `execution/tasks/*.md` | Transient | Individual work units. Flow through `todo → active → done/cancelled`. Pruned after a retention window (distribution-defined). |
| `execution/projects/*.md` | Transient | Active projects. Flow through `proposed → active → completed`. Pruned after a retention window. |
| `execution/plans/*.md` | Transient | Sprint plans, roadmaps. Flow through `proposed → current → superseded`. Pruned after a retention window. |
| `execution/retros/*.md` | Accumulating | Retrospectives. Each retro is authored once, referenced forever, never pruned. |

**Owner:** declared by the distribution (typically `execution-skills`).

**Reads from:** `product/product.md`, `product/roadmap.md`, and `product/features/*.md` (to generate projects and tasks from product commitments), `codebase/` (for technical context when scoping work).

**Read by:** all domains may read execution state for status awareness.

---

## 3. Ownership model

Every file under `.archeia/` MUST have exactly one owning domain. The owning domain's writers — skills, agents, scripts, or humans following the domain's schema — MUST be the only ones authorized to create, modify, or delete files in that domain's directories.

| Domain | Permitted shapes | Reads from |
|---|---|---|
| `business/` | living, accumulating, transient | (upstream origin) |
| `product/` | living, accumulating | `business/drafts/`, `business/strategy/`, `codebase/model/c4/`, `growth/` |
| `codebase/` | living only | source code, git history, `product/product.md`, `product/roadmap.md`, `product/features/*.md` |
| `growth/` | living, accumulating, transient | `business/strategy/`, `product/product.md`, `product/roadmap.md`, `product/features/*.md` |
| `execution/` | accumulating, transient | `product/product.md`, `product/roadmap.md`, `product/features/*.md`, `codebase/` |

**The ownership rules** (restated from [`KERNEL.md`](KERNEL.md#3-invariants) for convenience):

1. **Write to your domain only.** A business writer MUST NOT write to `product/`. A codebase writer MUST NOT write to `execution/`.
2. **Read across domains freely.** Any writer MAY read any file in `.archeia/` for context. The ownership rule governs writes, not reads.
3. **No implicit writes.** A writer that reads `business/drafts/` to produce `product/features/onboarding.md` is doing a cross-domain read followed by a same-domain write. The read is from `business/`; the write is to `product/`. This is correct behavior — no rule is violated.
4. **Schema enforcement at write time.** Each domain defines the schema its artifacts MUST satisfy. Writers MUST validate before writing; readers MAY re-validate on read. See [`contracts/`](contracts/) for the enforceable JSON Schemas.
5. **Parallelism via delegation, not concurrent access.** When a domain owner needs to parallelize work, it MUST delegate to subagents (per [Truth #4](PRINCIPLES.md#4-ownership-plus-delegation-is-the-concurrency-model)). Subagents compute; the owner commits.

---

## 4. The three cross-domain contracts

Software-project Archeia MUST enforce three cross-domain contracts. Each is a JSON Schema under [`contracts/`](contracts/) that validates the frontmatter and (where applicable) the body structure of an artifact one domain reads from another.

### 4.1 `business/drafts/*.md` → `product/` review

**Contract:** [`contracts/draft.schema.json`](contracts/draft.schema.json)

**What it guarantees:** every business draft MUST have a `title`, a `status` in the draft lifecycle vocabulary (`draft | review | advanced | discarded`), a `created` timestamp, and an `author`. When the status is `advanced`, an `advanced_into` field MUST name the living document the draft was merged into. When `discarded`, a `discarded_at` timestamp MUST be set.

**Who reads it:** product writers read drafts with `status: review` and produce updates to product living documents (`product/product.md`, `product/roadmap.md`, `product/requirements/*.md`, `product/features/*.md`) or new `product/decisions/*.md` entries. After the draft has been reviewed and acted on, the draft's status MUST transition to `advanced` or `discarded`, entering its retention window.

### 4.2 `product/{product.md,roadmap.md,features/*.md}` → `execution/` task generation

**Contract:** [`contracts/product.schema.json`](contracts/product.schema.json)

**What it guarantees:** the product execution surface MUST contain:

- `product/product.md` as the current product index and summary, with required sections for **Product Summary**, **Active Scope**, **Feature Index**, **Constraints**, and **Priority Model**.
- `product/roadmap.md` as the current sequencing surface, with required sections for **Now**, **Next**, and **Later**.
- `product/features/*.md` as feature-level specs. Each feature MUST have a stable feature ID, status, user problem, acceptance criteria, and enough links to requirements, design contracts, feedback, decisions, external sources, or codebase evidence for execution to scope work safely.

**Who reads it:** execution writers parse the roadmap to generate `execution/projects/` and parse feature specs to generate `execution/tasks/`. Each task MUST reference the feature ID it implements. `product/product.md` remains the entry point and index, not the only executable product artifact.

### 4.3 `codebase/model/c4/*.json` → `product/` feasibility review

**Contract:** [`contracts/c4.schema.json`](contracts/c4.schema.json)

**What it guarantees:** each C4 JSON file (`system.json`, `containers.json`, `components.json`, `dataflow.json`, `entities.json`, `statemachine.json`) under `codebase/model/c4/` MUST carry structured model data with `level`, `generated_at`, `skill`, and an `elements` array. Each element MUST have an `id`, `name`, `description`, and an `evidence` array citing file paths in the source tree. Elements MAY have `relationships` linking to other elements.

**Who reads it:** product writers read these files during draft review to validate that proposed features are feasible given the current architecture. The `evidence` array is load-bearing: the reviewer MUST be able to open the cited source files and verify each architectural claim. Citations to nonexistent paths MUST fail validation.

---

## 5. Colocated files outside `.archeia/`

Some files live outside the `.archeia/` tree but may still carry repo-local agent instructions or human-facing documentation. They are not part of the canonical `.archeia/` contract surface.

The distinction is about audience and maintenance, not file extension:

- `.archeia/codebase/` is the canonical AI-maintained repo-intelligence surface.
- `docs/` is the conventional human-facing documentation and publication surface.
- Canonical Archeia does not specify writes to `docs/`.

| File | Location | Owner | Purpose |
|---|---|---|---|
| `AGENTS.md` | Repo root | codebase | Cross-platform agent instructions ([agents.md standard](https://www.agents.md/)) |
| `CLAUDE.md` | Repo root | codebase | Claude Code-specific instructions |
| `README.md` | Per directory | codebase | Directory-level context, key concepts, learnings |
| `agents.md` | Per directory | codebase | Local agent rules where they differ from root |

These are outside the default `.archeia/` contract surface. Their history lives in git. Human-maintained docs SHOULD NOT be overwritten by codebase skills.

**Why not write `docs/` by default.** Existing `docs/` trees are usually human-owned publication surfaces. Agents writing generated analyses there by default is invasive and risks two-tree drift. Archeia keeps generated codebase intelligence in `.archeia/codebase/`. See [`POSITIONING.md`](POSITIONING.md) §4.4.

---

## 6. Minimum frontmatter required

Every artifact under `.archeia/` MUST have frontmatter sufficient for its shape's base schema:

- **Living documents** MUST have at minimum `title` and `owner`. See [`contracts/living-doc.schema.json`](contracts/living-doc.schema.json).
- **Accumulating records** MUST have at minimum `title`, `created`, `status`. See [`contracts/accumulating-record.schema.json`](contracts/accumulating-record.schema.json).
- **Transient artifacts** MUST have at minimum `id`, `title`, `created`, `status`. See [`contracts/transient-artifact.schema.json`](contracts/transient-artifact.schema.json).

Specific artifact types (drafts, product execution surface, tasks, ADRs, C4 JSONs) extend these base schemas with their own required fields. See the individual schemas in [`contracts/`](contracts/).

---

## 7. Validation

A repo is **software-conforming** if [`archeia:validate`](KERNEL.md#6-inherent-skills) passes against it and the repo uses exactly the five canonical domains specified above. A conforming validator MUST check:

1. `.archeia/business/`, `.archeia/product/`, `.archeia/codebase/`, `.archeia/growth/`, `.archeia/execution/` MUST all exist (even if empty).
2. No domain directory outside the canonical five MAY exist under `.archeia/`.
3. Every artifact MUST conform to its shape's base schema and any applicable specific schema.
4. All three cross-domain contracts MUST be enforced on the artifacts they apply to.
5. `.archeia/codebase/` MUST contain only living artifacts (no accumulating, no transient). The `codebase/model/c4/` subtree is the canonical machine-readable contract surface; `analysis/`, `conventions/`, `guide/`, and `views/` are generated codebase intelligence.
6. `docs/` is not part of the canonical `.archeia/` contract surface and MUST NOT be required for software conformance.
7. Ownership SHOULD be respected — writes to each domain (and to its colocated files) SHOULD come from the declared owner per the distribution's `standard/domains.yaml`. This check is advisory — git blame does not always identify writer families.

Repos that diverge from the five canonical domains are not software-conforming and should either adopt the canonical layout or declare a different distribution entirely (e.g., a research distribution with its own domain list).

---

## 8. What this document does not include

Deliberately, this document does **not** specify:

- **A fixed skill roster.** Which skills produce which artifacts is a distribution concern. See [`distributions/solo-builder.md`](https://github.com/Hugopeck/archeia/blob/main/DISTRIBUTION.md) for the reference Archeia Solo distribution's 16 skills.
- **A fixed agent roster.** Which agents exist is a distribution concern. See [`distributions/solo-builder.md`](https://github.com/Hugopeck/archeia/blob/main/DISTRIBUTION.md) and the [`agents/`](https://github.com/Hugopeck/archeia/tree/main/agents/) folder.
- **Retention windows.** How long transient artifacts stay on disk before pruning is a distribution concern. Archeia Solo's defaults are in [`distributions/solo-builder.md`](https://github.com/Hugopeck/archeia/blob/main/DISTRIBUTION.md).
- **An ethos.** Philosophical commitments (ship fast, user sovereignty, boil the lake, etc.) are distribution concerns.
- **Approval workflows.** Who can advance a draft to locked, who can supersede a decision, who authorizes a prune — all of this is policy, layered on top by distributions or by the adopting organization.

The five canonical domains, their shapes, their ownership, and their three contracts are the distribution-agnostic software skeleton. Everything else is layered on top.

---

## 9. References

- **[`KERNEL.md`](KERNEL.md)** — the abstract substrate this document builds on
- **[`PRINCIPLES.md`](PRINCIPLES.md)** — the six fundamental truths
- **[`TEMPORAL_MODEL.md`](TEMPORAL_MODEL.md)** — the three lifecycle shapes
- **[`contracts/`](contracts/)** — the JSON Schemas enforced by the canonical software layout
- **[`distributions/solo-builder.md`](https://github.com/Hugopeck/archeia/blob/main/DISTRIBUTION.md)** — the reference Archeia Solo distribution
- **[`distributions/README.md`](distributions/README.md)** — how to write a distribution

## License

MIT.
