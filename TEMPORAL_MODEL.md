# The Lifecycle Model

> **Claim:** project knowledge comes in three lifecycle shapes — **living**, **accumulating**, and **transient** — and each one needs different handling. Most of `.archeia/` is living artifacts backed by git. A minority is accumulating records that stay on disk forever. A smaller minority is transient artifacts that flow through states and get pruned. The standard's job is to recognize which shape each artifact is and apply the minimum machinery required.

This document replaces the earlier past/present/future framing. That framing was elegant but wrong: it tried to universalize a lifecycle that most artifacts don't actually have, and it ended up duplicating what git already does perfectly for living documents. The three-shapes model is what falls out when you walk through the real artifacts honestly.

---

## 1. Three shapes of project knowledge

Every artifact in every Archeia domain belongs to exactly one of three shapes. The shape determines everything: whether it has a temporal state, whether it gets pruned, whether it supports supersession, how its history is stored, and which kernel rules apply to it.

| Shape | One-line definition | History lives in |
|---|---|---|
| **Living** | One file per concept, edited in place, always current | Git |
| **Accumulating** | Append-only records that never leave disk | The disk itself (all records stay) |
| **Transient** | Flows through states during its lifetime, then pruned | Disk during retention, git after |

Most of `.archeia/` is shape 1 (living). A smaller but essential subset is shape 2 (accumulating). A minority is shape 3 (transient), and it is concentrated in `operations/execution/` plus running growth experiments.

The rest of this document specifies each shape in detail and maps kernel behavior onto them.

---

## 2. Shape 1: Living documents

### Definition

A living document is a single file that represents one concept. It is edited in place as the concept evolves. The file always contains the current truth about what it describes. History lives in git — `git log <path>` shows every version, `git show <commit>:<path>` retrieves any past state.

### Examples by domain

- **`strategy/`** — `vision/*.md`, `values/*.md`, `roadmap/*.md`, and local `conventions/*.md`
- **`operations/`** — `guides/*.md`, `optimization/*.md`, `people/*.md`, `finance/*.md`, `compliance/*.md`, and local `conventions/*.md`
- **`product/`** — `product/strategy/roadmap/*.md`, `product/technical/specs/*.md`, `product/execution/prds/*.md`, `product/technical/architecture/{c4,analysis,views}/*`, and local `conventions/*.md`
- **`growth/`** — `metrics/*.md`, `channels/current/*.md`, and any ongoing dashboard-style summaries

### Rules

1. **One file per concept.** There is one `product.md`, one `roadmap.md`, one `vision.md`, and one canonical file per feature. Never `product-v1.md`, `product-v2.md`, `product-current.md`. The concept has a canonical path and that path is stable forever.
2. **Edit in place.** Updates are commits to the same file. No renames, no suffix games, no supersession chains.
3. **No `temporal_state` field.** Living documents are implicitly "always present." Frontmatter can have whatever a distribution needs (`title`, `updated_at`, `owner`), but temporal state is not a meaningful question for them.
4. **No supersession.** There is nothing to supersede — there's only the current version and git history.
5. **No pruning.** Living documents are never deleted under normal operation. They're core project knowledge.

### Typical frontmatter

```yaml
---
title: Product Spec
owner: product
updated_at: 2026-04-12T15:30:00Z
---
```

That's the whole frontmatter. No `status`, no `temporal_state`, no supersession links. The file is the file. Git holds history.

### Why this is right

Nobody versions the current roadmap or a feature spec as separate files. You edit the file. You commit. You edit again. That's how humans already work on docs, and trying to impose past/present/future state on top of that is fighting the tool (git) that already solved the problem.

The living-document shape captures the majority of `.archeia/` because most project knowledge is this: the current state of a thing, evolved over time, with history preserved by the version control system you're already using.

---

## 3. Shape 2: Accumulating records

### Definition

An accumulating record is an append-only artifact. Each record has its own file and its own identity. Writing a new record does not replace the old one — both coexist on disk, with a `status` field indicating which is active. Records are *never deleted*. The entire history of decisions and authored events is directly readable in the filesystem.

### Examples by domain

- **`*/decisions/`** — domain-local decisions. The canonical example. Each decision is its own file, written once, referenced forever. Supersession writes a new decision that links to the old one; both stay.
- **`*/learnings/`** — domain-local learnings. Each learning record captures a lesson worth preserving without rewriting current truth.
- **`operations/execution/retros/`** — retrospectives. Each retro is a record of a past event. They never get deleted because later work references them.
- **`strategy/landscape/{competition,industry,market}/`** — dated external landscape snapshots. Each snapshot is its own record. Old snapshots inform later product, growth, and strategy decisions and stay on disk.
- **`growth/experiments/learnings/`** — concluded experiment learnings. Each learning record stays forever. The raw running state of the experiment is different — that's shape 3 under `growth/experiments/running/`.
- **`growth/channels/history/`** — retired channel records with performance history.

### Rules

1. **Each record has its own file and its own identity.** A new ADR is a new file (`decisions/20260412-1530-auth-rewrite.md`). Never edit an existing ADR to change its content (other than the single permitted mutation in rule 4).
2. **Append-only.** The set of records can grow; it cannot shrink. Records are never deleted.
3. **`status` field tracks relevance.** Common values: `active`, `superseded`, `archived`, `retired`. Semantics depend on the domain.
4. **Supersession is a write, not an edit.** To supersede record A with record B: write B with frontmatter `supersedes: <path-to-A>`, then do the *single permitted mutation* on A — update its frontmatter `status` from `active` to `superseded` and add `superseded_by: <path-to-B>`. No other edits to A are permitted. Both files stay on disk.
5. **No `temporal_state` field.** Time is not the axis here. The entire history of records is visible at once in the directory; readers filter by `status`, not by time.
6. **No pruning.** Ever. Accumulating records are the project's memory.

### Typical frontmatter

```yaml
---
title: Use PostgreSQL row-level security for multi-tenant isolation
created: 2026-04-12T15:30:00Z
author: architect
status: active
supersedes: null
superseded_by: null
---
```

And after supersession:

```yaml
---
title: Use PostgreSQL row-level security for multi-tenant isolation
created: 2026-04-12T15:30:00Z
author: architect
status: superseded
superseded_by: decisions/20260801-0900-schema-per-tenant.md
---
```

### Why this is right

The entire point of an ADR is that it stays forever. You don't prune a superseded decision — you write a new one that explains why the old one was wrong, and both live together so future readers can understand the reasoning. Retros are the same: you write a retro once, and later work references it to avoid repeating mistakes.

These artifacts are *authored history*. The act of writing them is the point. Treating them as transient is a category error.

Accumulating records look like a special case, but they're load-bearing: the entire design of an agentic workspace depends on having a way to capture decisions and events that other agents can read later without digging through git log archaeology.

---

## 4. Shape 3: Transient artifacts

### Definition

A transient artifact has a real lifecycle. It is created as a proposal, becomes active, reaches completion, and then — after a bounded retention window — gets pruned from the filesystem. Git preserves the long tail.

This is the only shape where temporal state (`future` / `present` / `past`) is a meaningful concept, and even here it's derived from a status field rather than stored separately.

### Examples by domain

- **`operations/execution/tasks/`** — the canonical transient. A task is created as `todo`, becomes `active` when work starts, becomes `done` when work completes, and gets pruned from the filesystem after a retention window (default 14 days in Archeia Solo). Git preserves every state forever.
- **`operations/execution/plans/`** — sprint plans. Active during a sprint, then superseded by the next sprint's plan and pruned after a retention window (default 30 days).
- **Distribution-defined proposals** — temporary sketches or proposals may exist as transient artifacts in whichever domain owns them. The canonical software layout does not reserve a `drafts/` directory.
- **`growth/experiments/running/`** — an experiment's running state is transient. Once it concludes, the running artifact is completed and pruned after its retention window. Durable outcomes, when worth keeping, are written as separate accumulating records under `growth/experiments/learnings/`.

### Rules

1. **Has a `status` field.** Status values are distribution-defined per artifact type. Typical for tasks: `todo`, `active`, `done`, `cancelled`. Typical for proposals: `proposed`, `review`, `accepted`, `rejected`.
2. **Temporal state is derived from status.** There is no `temporal_state` field in the frontmatter. The distribution defines a mapping from each status value to a temporal category (future / present / past). Readers who care about temporal state look up the mapping, don't read a field.
3. **Has a retention window.** The distribution defines how long a transient artifact stays on disk after reaching a terminal status. Archeia Solo defaults: tasks 14 days and plans 30 days.
4. **Has a terminal timestamp.** When an artifact reaches a terminal status (`done`, `cancelled`, `accepted`, `rejected`), a timestamp is recorded in frontmatter (e.g., `completed_at: 2026-04-12T16:45:00Z`). The retention window starts ticking from this timestamp.
5. **Pruned when the window expires.** A maintenance operation (e.g., `archeia:prune`) walks transient artifacts, checks retention windows, and deletes expired ones. Git preserves the file forever.
6. **Supersession is rare.** Transient artifacts usually don't supersede — they complete and get pruned. If supersession is genuinely needed, promote the artifact to shape 2 (accumulating) first.

### Typical frontmatter

```yaml
---
id: 2.3
title: Rewrite auth middleware
created: 2026-04-12T10:00:00Z
started: 2026-04-12T14:30:00Z
completed: 2026-04-13T16:45:00Z
status: done
scope:
  - server/auth/**
acceptance_criteria:
  - JWT refresh token flow works end-to-end
  - All existing auth tests pass
---
```

No `temporal_state`. The `status: done` plus the `completed` timestamp is enough — temporal state is `past`, retention window starts at 2026-04-13T16:45:00Z, and the file is eligible for pruning after that date + the distribution's retention setting.

### Why this is right

Tasks are the one thing that genuinely has a lifecycle worth tracking. They're born proposed, they do work, they finish. Keeping done tasks on disk forever is noise — after a sprint or two, they're just context clutter. But deleting them immediately loses the "what did we just ship?" signal that's useful in the next session.

Retention windows solve this: keep recent history on disk (glob-accessible, zero-latency) for the period when it's still operationally relevant, then delete and let git hold the archive. This is the correct lifecycle model because it matches how humans actually treat task state — recent matters, ancient doesn't, and git is the ancient archive.

---

## 5. The status → temporal mapping

Transient artifacts don't store temporal state; they store status, and temporal state is derived by the distribution's mapping table. Here's Archeia Solo's default mapping:

| Artifact type | Status | Temporal |
|---|---|---|
| Task | `todo`, `backlog` | `future` |
| Task | `active`, `in_progress`, `review` | `present` |
| Task | `done`, `cancelled` | `past` |
| Plan | `proposed` | `future` |
| Plan | `current` | `present` |
| Plan | `superseded` | `past` |
| Proposal | distribution-defined active statuses | `future` |
| Proposal | distribution-defined terminal statuses | `past` |
| Running experiment | `proposed` | `future` |
| Running experiment | `running` | `present` |
| Running experiment | `concluded` | `past` |

A distribution is free to change the status vocabulary or the mapping. The standard requires only that the mapping exists and is documented in the distribution's spec.

---

## 6. Kernel Behavior Mapped To Shapes

| Behavior | Shape 1 (living) | Shape 2 (accumulating) | Shape 3 (transient) |
|---|---|---|---|
| **`write`** | Create or edit in place; git preserves history. | Create new records; only schema-declared metadata mutations are allowed on existing records. | Create or update lifecycle artifacts according to the distribution's status vocabulary. |
| **`transition`** | N/A | N/A | Apply a declared status transition. Present transitions record start timestamps when required; past transitions record terminal timestamps and start retention. |
| **`prune`** | Never | Never | Delete an artifact whose retention window has expired. Git preserves. |
| **`history`** | `git log <path>` — walk commit history. | Walk on-disk records and frontmatter relationships such as `supersedes:` / `superseded_by:`. | Walk recent past-state artifacts on disk, then fall back to git log. |

The operations are **owner-performed**, per Truth #4 in [PRINCIPLES.md](PRINCIPLES.md#4-ownership-plus-delegation-is-the-concurrency-model). Subagents may compute which transitions to make, but the owner always commits the frontmatter change, the git commit, or the file deletion.

---

## 7. The five domains × three shapes

| Domain | Living | Accumulating | Transient |
|---|---|---|---|
| **`strategy/`** | `vision/*.md`, `values/*.md`, `roadmap/*.md`, `conventions/*.md` | `landscape/{competition,industry,market}/*.md`, `decisions/*.md`, `learnings/*.md` | distribution-defined purpose-named paths only |
| **`operations/`** | `guides/*.md`, `optimization/*.md`, `people/*.md`, `finance/*.md`, `compliance/*.md`, `conventions/*.md` | `execution/retros/*.md`, `decisions/*.md`, `learnings/*.md` | `execution/tasks/*.md`, `execution/plans/*.md`, `execution/projects/*.md` |
| **`product/`** | `strategy/roadmap/*.md`, `technical/specs/*.md`, `execution/prds/*.md`, `technical/architecture/{c4,analysis,views}/*`, `technical/devs/*.md`, `*/conventions/*.md` | `design/feedback/*.md`, `*/decisions/*.md`, `*/learnings/*.md`, `execution/logs/*.md`, `execution/archive/*.md` | `execution/plans/*.md` |
| **`growth/`** | `metrics/*.md`, `channels/current/*.md`, `conventions/*.md` | `channels/history/*.md`, `experiments/learnings/*.md`, `decisions/*.md`, `learnings/*.md` | `experiments/running/*.md` |

A few observations that fall out:

- **`product/technical/` is primarily living repo-intelligence artifacts.** Machine-readable architecture evidence, analysis, views, and dev-facing technical surfaces are regenerated or edited in place, with history in git.
- **`product/` has a light transient presence.** Most product surfaces evolve in place or accumulate as records, while `product/execution/plans/` is the main canonical transient path inside the domain.
- **`operations/execution/` is the main transient concentration.** Tasks, plans, projects — these are the things that flow.
- **`growth/` has all three shapes without shape-switching paths.** Current metrics and active channels are living, retired channel records and experiment learnings are accumulating, and running experiments are transient.

---

## 8. Product technical surfaces are primarily living documents

> **Named principle (updated).** The canonical product-technical intelligence surfaces are primarily living repo-intelligence artifacts. Machine-readable architecture evidence and adjacent generated views are edited or regenerated in place, and every version is preserved by git.

The earlier framing said "codebase is a witness, not a planner" and pointed out that codebase has no `future` state. The current kernel keeps the same idea but expresses it through `product/technical/architecture/` and adjacent technical surfaces. These paths are predominantly shape 1. They don't plan, and they don't own operational task flow. They are the current observed technical state of the code, expressed as durable living artifacts.

This is the purest form of the "codebase is downstream" principle. Product-technical intelligence reads source files, produces living repo intelligence, and commits it. Git provides all the history anyone needs. The dominant pattern is continuous regeneration or maintenance of the current technical truth.

---

## 9. Retention windows

Retention windows are a distribution concern, not a kernel concern. The standard requires only that transient artifacts have a retention window defined *somewhere* in the distribution's spec; the kernel does not pick the values.

**Archeia Solo defaults:**

| Artifact type | Retention after terminal status | Rationale |
|---|---|---|
| Task | 14 days | Covers "what did we just ship?" context for the next sprint |
| Plan | 30 days | A sprint's worth of history, since plans are sprint-scale |
| Discarded draft | 0 days | If it's rejected, it's rejected — git holds it |
| Concluded running experiment (no learning worth keeping) | 7 days | Short grace period in case someone wants to read the raw state |
| Concluded running experiment (with learning) | Promoted to accumulating record; original pruned after 7 days | The learning outlives the experiment |

Other distributions will pick different values. A research-lab distribution might keep experiments for 90 days. A compliance-driven distribution might keep tasks for 7 years (to satisfy audit requirements) — in which case tasks are effectively accumulating, not transient, and the distribution should model them as shape 2 instead.

**Who runs the pruner:** an inherent kernel skill (e.g., `archeia:prune`) walks transient artifacts, reads terminal timestamps, compares against retention windows from the distribution config, and deletes expired files. Each file deletion is its own git commit so the history is a clean audit trail.

---

## 10. Worked examples

### A task (shape 3)

```markdown
# Created:
---
id: 2.3
title: Rewrite auth middleware
created: 2026-04-12T10:00:00Z
status: todo
scope: [server/auth/**]
---

# Work starts (archeia:work runs `transition`):
---
id: 2.3
title: Rewrite auth middleware
created: 2026-04-12T10:00:00Z
started: 2026-04-12T14:30:00Z
status: active
scope: [server/auth/**]
---

# Work completes (archeia:work runs `transition`):
---
id: 2.3
title: Rewrite auth middleware
created: 2026-04-12T10:00:00Z
started: 2026-04-12T14:30:00Z
completed: 2026-04-13T16:45:00Z
status: done
scope: [server/auth/**]
pr: https://github.com/Hugopeck/archeia/pull/42
---

# 14 days later (archeia:prune deletes the file):
# git rm operations/execution/tasks/2.3-rewrite-auth.md
# git preserves the full history forever.
```

### A product feature spec (shape 1)

```markdown
# 2026-01-15: First version
---
title: Team Invites
feature_id: FEAT-team-invites
status: planned
updated_at: 2026-01-15T09:00:00Z
---

# Team Invites
...user problem, acceptance criteria, dependencies, evidence...

# 2026-04-12: Spec has grown
---
title: Team Invites
feature_id: FEAT-team-invites
status: active
updated_at: 2026-04-12T17:00:00Z
---

# Team Invites
...acceptance criteria refined, dependencies updated, evidence linked...
```

Same file. Same path. Edited in place. `git log .archeia/product/technical/specs/team-invites.md` shows every version. No superseded files cluttering the directory. The feature spec is a living document and the living document shape gets out of git's way.

### An ADR (shape 2)

```markdown
# 2026-01-15: Decision written
# File: product/technical/decisions/20260115-0900-row-level-security.md
---
title: Use PostgreSQL row-level security for multi-tenant isolation
created: 2026-01-15T09:00:00Z
author: architect
status: active
supersedes: null
superseded_by: null
---

## Context
...

## Decision
Adopt Postgres RLS for tenant isolation.

## Consequences
...

## Alternatives considered
...

# 2026-08-01: Decision is revisited and superseded
# New file: product/technical/decisions/20260801-0900-schema-per-tenant.md
---
title: Use schema-per-tenant for multi-tenant isolation
created: 2026-08-01T09:00:00Z
author: architect
status: active
supersedes: decisions/20260115-0900-row-level-security.md
superseded_by: null
---

## Context
The RLS approach from decision 20260115 hit scale limits at N tenants.
Schema-per-tenant gives us isolation + independent migration schedules.

## Decision
Migrate to schema-per-tenant.

## Consequences
...

# And the OLD file gets its one permitted frontmatter mutation:
# File: product/technical/decisions/20260115-0900-row-level-security.md
---
title: Use PostgreSQL row-level security for multi-tenant isolation
created: 2026-01-15T09:00:00Z
author: architect
status: superseded
supersedes: null
superseded_by: decisions/20260801-0900-schema-per-tenant.md
---
# Body is unchanged.
```

Both files stay on disk forever. Future readers can follow the `supersedes` / `superseded_by` links in either direction to understand the full history of the isolation decision.

### A generated scan report view (shape 1)

```markdown
# product/technical/architecture/analysis/repository.md always has one generated analysis.
# Regeneration edits the view in place; git holds history if committed.

# 2026-04-01 run:
---
title: Scan Report
generated: 2026-04-01T12:00:00Z
skill: archeia:scan-repo
---

# Scan Report
...LOC, deps, test coverage, README gaps...

# 2026-04-12 run (same file, new content):
---
title: Scan Report
generated: 2026-04-12T18:00:00Z
skill: archeia:scan-repo
---

# Scan Report
...LOC, deps, test coverage, README gaps... (updated numbers)
```

No `repository-2026-04-01.md` sitting next to the current one. No archive directory. Just one generated analysis, regenerated in place, with history in git. If someone wants to compare today's scan to last month's scan, they run `git show HEAD~30:.archeia/product/technical/architecture/analysis/repository.md`.

### A proposal that becomes durable product or strategy truth

```markdown
# A distribution-defined proposal artifact (shape 3):
---
id: onboarding-rewrite
title: Rewrite onboarding to reduce first-week churn
created: 2026-04-12T10:30:00Z
author: hugopeck
status: draft
---

# Onboarding rewrite proposal
...

# After review and decision to incorporate it into strategy/vision/vision.md:
# 1. archeia:create-vision (or similar) edits strategy/vision/vision.md
#    in place to incorporate the proposal's content — shape 1 edit.
# 2. The proposal's status becomes a terminal accepted status, retention window starts.
# 3. After the distribution-defined retention window, the proposal file is pruned.
# 4. git preserves the proposal forever.
```

The living document (`vision.md`) grows. The proposal eventually disappears from disk. Git holds the proposal's history in case anyone wants to see it.

---

## 11. Summary

The three-shapes model replaces the past/present/future framing from earlier drafts. It is more truthful, because it describes how Archeia artifacts actually work instead of imposing a uniform lifecycle on things that don't have one. It is more useful, because it keeps `.archeia/` scannable by pruning transient artifacts and storing living-doc history in git where it belongs. It is more opinionated, because it forces each artifact to declare its shape, which prevents drift into "everything accumulates forever."

The kernel recognizes three shapes and ships mechanical operations (`init`, `validate`, `write`, `transition`, `prune`, `history`) that enforce those shapes. Everything else — status vocabularies, retention windows, shape assignments for each artifact type, and latent authoring skills — is a distribution concern.

What falls out is a standard that gets out of git's way for the 80% of artifacts that are living documents, gives ADRs and retros the permanent home they need, and handles operational state (tasks, plans, running experiments, proposals) with bounded retention that matches how humans already think about those artifacts.

This is the temporal model. What's novel is not the categories themselves — accountants had ledgers, software had live docs, every to-do list is transient — but the recognition that an agentic workspace needs all three, each with different rules, and that trying to collapse them into a single model breaks at least two of them.
