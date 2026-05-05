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
├── product/         # What we've committed to build
├── codebase/        # What the code is, right now
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

**Purpose.** The locked, implementation-ready definition of what we're building. Everything in `product/` has been reviewed against codebase reality and design feasibility. Engineers treat this as the source of truth for what to build.

**Permitted shapes:** living, accumulating.

| Path | Shape | What it is |
|---|---|---|
| `product/product.md` | Living | The locked product spec. Features, constraints, priorities. Evolved in place — when the spec grows or changes, edit the file and commit. See [`product.schema.json`](contracts/product.schema.json) for the required sections. |
| `product/design/*.md` | Living | UI specs, interaction patterns, component inventories. Each design document is living and edited in place. |
| `product/decisions/*.md` | Accumulating | ADRs. Each decision is its own file, written once, referenced forever. Supersession writes a new ADR; both old and new stay on disk. |

**Note:** product has **no transient artifacts.** Drafts that would become part of product.md live in `business/drafts/` until they advance. Once advanced, they're merged into `product/product.md` (a living document) or captured as new entries in `product/decisions/` (accumulating records). Nothing in `product/` flows through a transient lifecycle.

**Owner:** declared by the distribution.

**Reads from:** `business/drafts/` (as input to review), `codebase/architecture/` (for feasibility validation during review).

**Read by:** `codebase/` (for framing), `execution/` (to generate tasks from the locked spec), `growth/` (for feature context when planning channels).

### 2.3 `codebase/`

**Purpose.** The structured, machine-readable representation of what the code is right now — specifically, the C4 model artifacts that other domains consume as a contract. Every element cites a source file path. No human decisions live here; only observations derived from source, config, and git history.

**Permitted shapes:** living **only**.

| Path | Shape | What it is |
|---|---|---|
| `codebase/architecture/system.json` | Living | C4 System Context as structured JSON. |
| `codebase/architecture/containers.json` | Living | C4 Container data. |
| `codebase/architecture/components.json` | Living | C4 Component data. |
| `codebase/architecture/dataflow.json` | Living | Primary data flows (when present). |
| `codebase/architecture/entities.json` | Living | ORM/schema entities (when present). |
| `codebase/architecture/statemachine.json` | Living | State machines (when present). |

> **The codebase domain inside `.archeia/` is the contract surface only.** The C4 JSON files are read by `product/decisions/` (via [`c4.schema.json`](contracts/c4.schema.json)) when validating feasibility. They are not for human reading — they are the machine-readable evidence other domains rely on.
>
> **Prose documentation about the codebase lives in `docs/`, not in `.archeia/`.** This is a deliberate departure from the OpenAI "everything in `docs/`" position, taken from the opposite end: prose architecture docs, developer guides, coding standards, scan and git reports, and rendered diagrams all live in the project's conventional `docs/` tree. They are owned by the codebase domain (see §5), but they are not part of the contract surface. See [`POSITIONING.md`](POSITIONING.md) §4.4 for the full rationale.
>
> **Codebase artifacts inside `.archeia/` are purely shape 1 — living documents only.** The codebase domain has no accumulating records and no transient artifacts. Every C4 JSON is regenerated from source evidence, edited in place as the code evolves, and preserved in git.

**Owner:** declared by the distribution (typically `codebase-skills`). The same owner writes the colocated prose docs in `docs/` (see §5).

**Reads from:** the codebase itself (source files, config, git history) and optionally `product/product.md` to contextualize architecture against intent.

**Read by:** `product/` (for feasibility validation during draft review), `execution/` (for technical context when scoping work), every other domain as ground-truth reference.

**Regeneration contract.** Every file in `codebase/architecture/` and every codebase-owned file in `docs/` is regenerable — delete any of them and run the codebase skills again and they will be rebuilt from source evidence. Every regeneration is a commit to the same file path; git holds every prior version.

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

**Reads from:** `business/strategy/strategy.md` (for positioning and pricing context), `product/product.md` (for feature context).

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

**Reads from:** `product/product.md` (to generate tasks from specs), `codebase/` (for technical context when scoping work).

**Read by:** all domains may read execution state for status awareness.

---

## 3. Ownership model

Every file under `.archeia/` MUST have exactly one owning domain. The owning domain's writers — skills, agents, scripts, or humans following the domain's schema — MUST be the only ones authorized to create, modify, or delete files in that domain's directories.

| Domain | Permitted shapes | Reads from |
|---|---|---|
| `business/` | living, accumulating, transient | (upstream origin) |
| `product/` | living, accumulating | `business/drafts/`, `codebase/architecture/` |
| `codebase/` | living only | source code, git history, `product/product.md` |
| `growth/` | living, accumulating, transient | `business/strategy/`, `product/product.md` |
| `execution/` | accumulating, transient | `product/product.md`, `codebase/` |

**The ownership rules** (restated from [`KERNEL.md`](KERNEL.md#3-invariants) for convenience):

1. **Write to your domain only.** A business writer MUST NOT write to `product/`. A codebase writer MUST NOT write to `execution/`.
2. **Read across domains freely.** Any writer MAY read any file in `.archeia/` for context. The ownership rule governs writes, not reads.
3. **No implicit writes.** A writer that reads `business/drafts/` to produce `product/product.md` is doing a cross-domain read followed by a same-domain write. The read is from `business/`; the write is to `product/`. This is correct behavior — no rule is violated.
4. **Schema enforcement at write time.** Each domain defines the schema its artifacts MUST satisfy. Writers MUST validate before writing; readers MAY re-validate on read. See [`contracts/`](contracts/) for the enforceable JSON Schemas.
5. **Parallelism via delegation, not concurrent access.** When a domain owner needs to parallelize work, it MUST delegate to subagents (per [Truth #4](PRINCIPLES.md#4-ownership-plus-delegation-is-the-concurrency-model)). Subagents compute; the owner commits.

---

## 4. The three cross-domain contracts

Software-project Archeia MUST enforce three cross-domain contracts. Each is a JSON Schema under [`contracts/`](contracts/) that validates the frontmatter and (where applicable) the body structure of an artifact one domain reads from another.

### 4.1 `business/drafts/*.md` → `product/` review

**Contract:** [`contracts/draft.schema.json`](contracts/draft.schema.json)

**What it guarantees:** every business draft MUST have a `title`, a `status` in the draft lifecycle vocabulary (`draft | review | advanced | discarded`), a `created` timestamp, and an `author`. When the status is `advanced`, an `advanced_into` field MUST name the living document the draft was merged into. When `discarded`, a `discarded_at` timestamp MUST be set.

**Who reads it:** product writers read drafts with `status: review` and produce updates to `product/product.md` or new `product/decisions/*.md` entries. After the draft has been reviewed and acted on, the draft's status MUST transition to `advanced` or `discarded`, entering its retention window.

### 4.2 `product/product.md` → `execution/` task generation

**Contract:** [`contracts/product.schema.json`](contracts/product.schema.json)

**What it guarantees:** `product.md` MUST be a living document with `status: locked`, a `locked_at` timestamp, and a body containing three required sections:

- **Features** — each feature MUST have a name, description, and list of acceptance criteria. Every feature MUST have a stable identifier that tasks can reference.
- **Constraints** — technical and business constraints that scope the work.
- **Priorities** — ordered list or MoSCoW classification.

**Who reads it:** execution writers parse these sections to generate `execution/projects/` and `execution/tasks/` entries. Each task MUST reference the feature identifier it implements.

### 4.3 `codebase/architecture/*.json` → `product/` feasibility review

**Contract:** [`contracts/c4.schema.json`](contracts/c4.schema.json)

**What it guarantees:** each C4 JSON file (`system.json`, `containers.json`, `components.json`, `dataflow.json`, `entities.json`, `statemachine.json`) MUST carry structured model data with `level`, `generated_at`, `skill`, and an `elements` array. Each element MUST have an `id`, `name`, `description`, and an `evidence` array citing file paths in the source tree. Elements MAY have `relationships` linking to other elements.

**Who reads it:** product writers read these files during draft review to validate that proposed features are feasible given the current architecture. The `evidence` array is load-bearing: the reviewer MUST be able to open the cited source files and verify each architectural claim. Citations to nonexistent paths MUST fail validation.

---

## 5. Colocated files outside `.archeia/`

Some files live outside the `.archeia/` tree but are still owned by the codebase domain. They follow the same ownership rules (one owner, free reads).

| File | Location | Owner | Purpose |
|---|---|---|---|
| `AGENTS.md` | Repo root | codebase | Cross-platform agent instructions ([agents.md standard](https://www.agents.md/)) |
| `CLAUDE.md` | Repo root | codebase | Claude Code-specific instructions |
| `README.md` | Per directory | codebase | Directory-level context, key concepts, learnings |
| `agents.md` | Per directory | codebase | Local agent rules where they differ from root |
| `docs/architecture.md` | Repo `docs/` | codebase | Prose architecture document following C4 Model structure. Rendered from the C4 JSONs in `.archeia/codebase/architecture/`. |
| `docs/standards.md` | Repo `docs/` | codebase | Coding conventions extracted from the codebase. |
| `docs/guide.md` | Repo `docs/` | codebase | Developer setup, commands, testing, deployment. |
| `docs/scan-report.md` | Repo `docs/` | codebase | Quantitative scan: LOC, dependencies, test coverage, README gaps. Regenerated in place. |
| `docs/git-report.md` | Repo `docs/` | codebase | Contributors, bus factor, churn, velocity. Regenerated in place. |
| `docs/diagrams/*.mmd` | Repo `docs/` | codebase | Mermaid diagrams rendered from the C4 JSONs. |

These are living documents. Their history lives in git. They are regenerated by codebase writers on each run and edited in place as the code evolves.

**Why `docs/`, not `.archeia/`.** Prose documentation belongs in the conventional location every project already uses. Putting `architecture.md` in `.archeia/codebase/` competes with the project's pre-existing `docs/architecture.md` and creates two-tree drift. Archeia owns the *contract artifacts* (the C4 JSONs that other domains consume) and *colocates* the prose that humans read in the location humans expect. See [`POSITIONING.md`](POSITIONING.md) §4.4. Distributions MAY publish `docs/` as a documentation site; the C4 JSONs in `.archeia/` are not meant to be published.

---

## 6. Minimum frontmatter required

Every artifact under `.archeia/` MUST have frontmatter sufficient for its shape's base schema:

- **Living documents** MUST have at minimum `title` and `owner`. See [`contracts/living-doc.schema.json`](contracts/living-doc.schema.json).
- **Accumulating records** MUST have at minimum `title`, `created`, `status`. See [`contracts/accumulating-record.schema.json`](contracts/accumulating-record.schema.json).
- **Transient artifacts** MUST have at minimum `id`, `title`, `created`, `status`. See [`contracts/transient-artifact.schema.json`](contracts/transient-artifact.schema.json).

Specific artifact types (drafts, product spec, tasks, ADRs, C4 JSONs) extend these base schemas with their own required fields. See the individual schemas in [`contracts/`](contracts/).

---

## 7. Validation

A repo is **software-conforming** if [`archeia:validate`](KERNEL.md#6-inherent-skills) passes against it and the repo uses exactly the five canonical domains specified above. A conforming validator MUST check:

1. `.archeia/business/`, `.archeia/product/`, `.archeia/codebase/`, `.archeia/growth/`, `.archeia/execution/` MUST all exist (even if empty).
2. No domain directory outside the canonical five MAY exist under `.archeia/`.
3. Every artifact MUST conform to its shape's base schema and any applicable specific schema.
4. All three cross-domain contracts MUST be enforced on the artifacts they apply to.
5. `.archeia/codebase/` MUST contain only living documents (no accumulating, no transient) — and within it, only the C4 JSON contract artifacts listed in §2.3.
6. Codebase-owned colocated files in `docs/` (per §5) SHOULD also be living documents, but their absence MUST NOT be a conformance failure — `docs/` is not strictly required for kernel conformance, only for full software-distribution publication.
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
