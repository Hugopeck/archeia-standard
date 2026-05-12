# The Archeia Kernel

| | |
|---|---|
| **Status** | Draft, pre-1.0 |
| **Version** | See [`VERSION`](VERSION) |
| **Conformance** | See [`CONFORMANCE.md`](CONFORMANCE.md) |
| **Reference algorithms** | See [`REFERENCE-ALGORITHMS.md`](REFERENCE-ALGORITHMS.md) |
| **Test matrix** | See [`TEST-MATRIX.md`](TEST-MATRIX.md) |
| **Positioning vs. SOTA** | See [`POSITIONING.md`](POSITIONING.md) |
| **Normative language** | The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, **MAY**, and **REQUIRED** in this document are to be interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119). |
| **License** | MIT |

> **Claim:** the Archeia Kernel is the minimal substrate any conforming distribution extends. It defines the primitives, the invariants, the kernel operations, the required tooling every distribution must provide, and the extension mechanism for adding new domains. It is deliberately small — small enough to read in one sitting, small enough to implement in a day, small enough to be non-negotiable.

The kernel is what you're citing when you say "this tool supports the Archeia Standard." The distributions are what you're citing when you say "this repo uses Archeia Solo." The two are different layers, and this document specifies the lower one: the canonical, human-readable source-of-truth layer.

---

## 1. Scope

The kernel defines:

- **Primitives** — the concepts every Archeia implementation must understand
- **Invariants** — the rules every conforming implementation must uphold
- **The three lifecycle shapes** — living, accumulating, transient
- **The six kernel operations** — `init`, `validate`, `write`, `transition`, `prune`, `history`
- **Required tooling** — the operations every conforming distribution must provide (by its own name or equivalent script/library function)
- **Inherent agents** — the agent roles every conforming distribution must provide
- **The extension mechanism** — how a distribution declares its domains, status vocabularies, retention windows, and ownership assignments
- **Validation** — how a tool checks that a repo conforms to the kernel

The kernel does **not** define:

- Which domains exist beyond a minimal `standard/` self-description (domain list is a distribution concern)
- Which format artifacts take beyond "text-native by default, binary-with-sidecar allowed"
- Which tool produces artifacts (agents, skills, scripts, humans — all permitted)
- Which VCS provides history (git is the reference implementation; any versioned storage works)
- Which approval workflow governs state transitions (policy, not spec)
- Which audience reads the artifacts (humans, agents, both — all permitted)
- **Where prose documentation lives.** `.archeia/` is for operational state, contract artifacts, and AI-maintained generated intelligence. In the canonical software application, `.archeia/codebase/` is the AI-maintained repo-intelligence surface, including machine-readable models and generated analyses. Human-owned publication docs — architecture narratives, contributor guides, public docs — belong in the project's conventional `docs/` tree. The kernel does not specify writes to `docs/`; any publication bridge from `.archeia/` to `docs/` is project or distribution policy outside the canonical contract surface. See [`POSITIONING.md`](POSITIONING.md) §4.4 for the rationale.

The [canonical software-project application of the kernel](SCHEMA.md) commits to five specific domains (`business/`, `product/`, `codebase/`, `growth/`, `execution/`) for software projects, but that commitment lives in `SCHEMA.md`, not here. The kernel itself is domain-agnostic above the minimum.

---

## 2. Primitives

Every Archeia implementation must understand these eight concepts:

### 2.1 Root

A **root** is a project root containing an `.archeia/` directory. A root is usually a git repository, but the kernel only requires "persistent storage with history" — any VCS (git, jj, hg, pijul) or even a versioned blob store qualifies. Git is the reference implementation.

### 2.2 Domain

A **domain** is a named subdirectory under `.archeia/` representing one knowledge area. Every artifact belongs to exactly one domain. The kernel does not fix the domain list — distributions declare their domains in a `standard/domains.yaml` file at the root. The [canonical software application](SCHEMA.md) commits to exactly five (`business/`, `product/`, `codebase/`, `growth/`, `execution/`).

### 2.3 Artifact

An **artifact** is a file inside a domain. Text-native by default: markdown, JSON, YAML, HTML. Binary artifacts are allowed only when paired with a `<file>.meta.yaml` sidecar carrying provenance, owner, schema version, and source.

Every artifact belongs to exactly one lifecycle shape (see §4).

### 2.4 Shape

A **shape** is one of three lifecycle categories every artifact belongs to:

- **Living** — edited in place, history in git, always current
- **Accumulating** — append-only record, status field tracks relevance, never pruned
- **Transient** — flows through status values with bounded retention, pruned when expired

The full specification of the three shapes is in `[TEMPORAL_MODEL.md](TEMPORAL_MODEL.md)`.

### 2.5 Owner

Every domain has exactly one **owner** — a writer family (a specific skill or an agent role) authorized to write to that domain. Owners are declared in the distribution's `standard/domains.yaml`.

One owner per domain. Many readers. Per Truth #4 in `[PRINCIPLES.md](PRINCIPLES.md)`, parallelism comes from subagent delegation, not concurrent writes.

### 2.6 Schema

A **schema** is the frontmatter and structural contract a domain's artifacts must satisfy. Schemas live as JSON Schema files under `standard/contracts/` and are enforced at write time by conforming writers and at validate time by the kernel `validate` operation.

The kernel ships base schemas for the three shapes (`living-doc.schema.json`, `accumulating-record.schema.json`, `transient-artifact.schema.json`) which specific artifact schemas extend.

### 2.7 Contract

A **contract** is a declared read relationship between two domains. For example: "Domain B reads artifact X from domain A, which guarantees frontmatter fields Y, Z and body sections P, Q." Contracts live as JSON Schema files under `standard/contracts/`.

The two contracts the [canonical software application](SCHEMA.md) enforces:

- `product/{product.md,roadmap.md,features/*.md}` → `execution/{projects/*.md,tasks/*.md}` (via `product.schema.json`)
- `codebase/model/c4/*.json` → `product/decisions/*.md` (via `c4.schema.json`)

### 2.8 Writer / Reader

A **writer** is anything that produces artifacts — agents, skills, scripts, humans. A **reader** is anything that consumes artifacts. The kernel is writer-agnostic and reader-agnostic. As long as writes conform to the schema and follow the ownership rules, the kernel doesn't care what produced them.

---

## 3. Invariants

Every conforming implementation MUST uphold these seven invariants. Violation of any one means the implementation is non-conforming.

1. **Knowledge MUST live in the root.** Artifacts MUST be stored in `.archeia/` under the project root. They MUST NOT be stored in a wiki, behind a URL, or behind auth as the canonical copy. Downstream tooling MAY index `.archeia/` for retrieval, but the root tree is the source of truth.
2. **Every artifact MUST belong to exactly one owning domain.** No shared ownership, no multi-domain artifacts, no cross-domain writes.
3. **Every artifact MUST have exactly one lifecycle shape** — living, accumulating, or transient. The artifact's shape determines which rules apply to it; an artifact MUST NOT switch shapes during its lifetime.
4. **Reads MUST be free; writes MUST be owner-only.** Any agent, skill, or human MAY read any artifact under `.archeia/`. Only the declared domain owner MAY write. Cross-domain coordination MUST happen through reads of contract-conforming artifacts, not through cross-domain writes.
5. **Every factual claim MUST cite a source.** Descriptive artifacts (codebase analyses, architecture models derived from code, git history analyses) MUST cite the file paths or commits their claims come from. Prescriptive artifacts (vision, strategy, decisions) MUST cite their rationale and the prior artifacts they build on. Claims that cannot be evidenced MUST be flagged in-line with `<!-- INSUFFICIENT EVIDENCE: [description] -->` rather than fabricated.
6. **Cross-domain dependencies MUST be declared contracts, not inferred.** If domain B reads from domain A, there MUST be a JSON Schema under `standard/contracts/` describing the exact frontmatter and structure B relies on. Implementations MUST NOT infer cross-domain dependencies that are not declared.
7. **History MUST be preserved.** Living documents MUST preserve history in git. Accumulating records MUST preserve history on disk forever. Transient artifacts MUST preserve history in git after pruning. No history MAY be destroyed.

---

## 4. The three lifecycle shapes

See `[TEMPORAL_MODEL.md](TEMPORAL_MODEL.md)` for the full specification. This section defines only what the kernel requires.

A conforming implementation MUST:

- **Recognize all three shapes.** Every artifact type in every domain MUST be assigned exactly one shape.
- **Apply the shape's rules.** Living documents MUST be edited in place. Accumulating records MUST be append-only and MUST permit only the single frontmatter mutation rule defined for supersession. Transient artifacts MUST flow through status values and MUST be pruned after retention.
- **Store history according to the shape.** Living artifacts: history MUST be in git. Accumulating: history MUST be on-disk forever. Transient: history MUST be on-disk during retention and in git after pruning.
- **Map status to temporal state for transient artifacts.** The distribution defines the mapping; the kernel REQUIRES one to exist.

---

## 5. The six kernel operations

Every conforming distribution MUST provide these six operations as deterministic scripts, library functions, or equivalent tooling. Kernel operations are mechanical repo operations: they inspect or mutate `.archeia/` while enforcing ownership, shape, schema, lifecycle, retention, and contract rules. They are not agent workflows and MUST NOT require model judgment.

Latent work belongs in skills layered above the kernel. A skill such as `review-product`, `clarify-idea`, or `write-codebase-model` may use a model to decide what should change, but the final filesystem mutation still goes through the deterministic kernel rules.

### 5.1 `init` — deterministic

**Applies to:** project roots.

**Effect:** create the declared `.archeia/` structure for the distribution, including domain directories, standard metadata, contract schemas, and scaffolded directory `README.md` files where the distribution declares them. Running `init` on an already initialized root MUST be idempotent and MUST NOT overwrite user-authored artifacts.

### 5.2 `validate` — deterministic

**Applies to:** project roots.

**Effect:** walk `.archeia/` and report conformance issues: missing required structure, undeclared domains, invalid shapes, schema failures, contract failures, invalid transient statuses, missing terminal timestamps, expired transient artifacts, and advisory ownership issues.

### 5.3 `write` — deterministic

**Applies to:** all artifact shapes.

**Effect:** create, update, or delete an artifact only if the requested mutation satisfies the owning domain, permitted shape, artifact schema, cross-domain contract, and shape-specific history rules. `write` is the gate every writer must pass through before changing `.archeia/`.

Shape-specific constraints:

- **Living:** MAY be edited in place; git is the history mechanism.
- **Accumulating:** MAY create new records; MUST NOT delete records; existing records MAY receive only schema-declared metadata mutations such as supersession links.
- **Transient:** MAY create or update active lifecycle artifacts according to the distribution's status vocabulary; deletion outside `prune` MUST be refused unless the distribution explicitly allows it.

### 5.4 `transition` — deterministic

**Applies to:** transient artifacts only.

**Effect:** change a transient artifact's `status` according to the distribution's declared lifecycle map. The implementation MUST refuse transitions not declared by the distribution. When a transition enters a present-mapped state, it records the distribution's start timestamp field if required. When a transition enters a past-mapped state, it records the distribution's terminal timestamp field and starts the retention clock.

### 5.5 `prune` — deterministic

**Applies to:** transient artifacts only.

**Effect:** the implementation MUST delete an artifact from disk whose retention window (distribution-defined, per artifact type) has elapsed since its terminal timestamp. The deletion MUST be a git commit so the file is preserved in history. The implementation MUST NOT delete artifacts whose retention window has not elapsed.

**Example:** a task with `status: done`, `completed: 2026-03-29T16:45:00Z` and a 14-day retention window is pruned on or after 2026-04-12.

### 5.6 `history` — deterministic

**Applies to:** all shapes, with different semantics per shape.

**Effect:** the implementation MUST return the history of a named concept, dispatching by shape:

- **Living:** `git log <path>` — walk commit history.
- **Accumulating:** walk on-disk records and any `supersedes:` / `superseded_by:` chain.
- **Transient:** walk recent past-state artifacts on disk (during retention) and fall back to `git log` for older history.

The operation's return type is distribution-defined (a structured list, a timeline, a diff view) but the contract MUST be consistent: "show me how this thing changed over time."

### 5.7 Latent skill pattern: consolidation

Consolidation is not a kernel operation. It is a common latent skill pattern: read source artifacts and produce or update a target artifact that integrates their content with cited evidence. Examples include `review-product`, `clarify-idea`, `write-codebase-model`, and `scan-git`.

A consolidation skill SHOULD cite sources for substantive claims, flag insufficient evidence instead of fabricating, keep scope narrow, and send final mutations through `write`, `transition`, or both. The kernel validates the resulting artifacts; it does not decide what they should say.

---

## 6. Required Tooling

Every conforming distribution MUST provide the six kernel operations under its own namespace or expose equivalent scripts/library functions. A distribution named `archeia-solo` provides `archeia:init`, `archeia:validate`, etc. A future `archeia-research` distribution would provide the same operations under the same names.

| Operation | Latent / Deterministic | What it does |
| --- | --- | --- |
| **`archeia:init`** | Deterministic | Scaffold `.archeia/` for a new project. Creates the domain directories per the distribution's `standard/domains.yaml`, writes a default `standard/SCHEMA.md` pointer, creates a `standard/VERSION` file, and copies in the contract schemas. Idempotent — running on an existing root is a no-op plus a validation pass. |
| **`archeia:validate`** | Deterministic | Walk `.archeia/`, check every artifact against its domain's shape and schema, verify cross-domain contracts, check that all transient artifacts have valid status values per the distribution's status vocabulary, verify ownership is respected. Report conformance issues with file-path citations. |
| **`archeia:write`** | Deterministic | Create, update, or delete artifacts while enforcing owner, shape, schema, contract, and history rules. |
| **`archeia:transition`** | Deterministic | Apply a distribution-declared status transition to a transient artifact and record required timestamps. |
| **`archeia:prune`** | Deterministic | Walk all transient artifacts, identify expired ones (past-state status with terminal timestamp + retention window elapsed), and delete them. Each deletion is a git commit. Distributions may wrap this as a scheduled maintenance skill. |
| **`archeia:history`** | Deterministic | Return artifact history using git, on-disk records, and frontmatter relationships appropriate to the artifact's shape. |

Latent authoring skills are distribution concerns. They may be required by a distribution, but they are not kernel operations.

---

## 7. Inherent agents

Every conforming distribution MUST provide this one agent role, with a system prompt that handles the temporal-state transitions for the distribution's artifacts:

### `archivist`

**Role:** manages past-state transitions, supersession decisions, and retention policy.

**Reads:** the full `.archeia/` tree.

**Writes:** invokes `archeia:write`, `archeia:transition`, and `archeia:prune` for temporal and retention changes.

**Invoked when:** the user asks "how did we get here," "mark this finished," "record that this decision was superseded," "prune finished tasks," or when a maintenance schedule fires.

The archivist is the one agent role that exists because of the kernel's temporal semantics, not because of any distribution's specific workflow. Every distribution needs one.

A distribution MAY provide additional agent roles (`librarian`, `conductor`, and others) but only `archivist` is required by the kernel.

---

## 8. The extension mechanism: declaring a distribution

A distribution extends the kernel by providing four things:

### 8.1 A `standard/domains.yaml` file

Declares which domains exist, who owns each, what shapes are permitted in each, and what contracts the distribution enforces.

```yaml
distribution: archeia-solo
version: 1.0.0

domains:
  - id: business
    owner: business-skills
    shapes: [living, accumulating, transient]
    reads: []
  - id: product
    owner: product-skills
    shapes: [living, accumulating]
    reads: [business, codebase]
  - id: codebase
    owner: codebase-skills
    shapes: [living]
    reads: [product]
  - id: growth
    owner: growth-skills
    shapes: [living, accumulating, transient]
    reads: [business, product]
  - id: execution
    owner: execution-skills
    shapes: [accumulating, transient]
    reads: [product, codebase]

contracts:
  - from: product
    to: execution
    schema: standard/contracts/product.schema.json
  - from: codebase
    to: product
    schema: standard/contracts/c4.schema.json
```

### 8.2 Status vocabularies and temporal mappings for transient artifacts

For every transient artifact type, declare:

- Status vocabulary (e.g., `todo, active, done, cancelled`)
- Status → temporal mapping (`todo → future`, `active → present`, `done → past`)
- Retention window (e.g., 14 days after terminal status)
- Terminal timestamp field name (e.g., `completed`)

Declared alongside the domain entries in `standard/domains.yaml` or in a separate `standard/lifecycles.yaml` — the kernel doesn't care which file, only that the information exists and is machine-readable.

### 8.3 JSON Schemas under `standard/contracts/`

Enforceable schemas for every artifact type the distribution uses. At minimum:

- The kernel's three base schemas (`living-doc.schema.json`, `accumulating-record.schema.json`, `transient-artifact.schema.json`)
- The distribution's cross-domain contract schemas (e.g., `product.schema.json`, `c4.schema.json`)
- Any per-artifact-type schema the distribution wants to enforce (e.g., `task.schema.json`, `adr.schema.json`)

### 8.4 Implementations of the six kernel operations and the archivist agent

The distribution ships `archeia:init`, `archeia:validate`, `archeia:write`, `archeia:transition`, `archeia:prune`, `archeia:history`, and an `archivist` agent. These can be implemented as skill files, scripts, CI checks, or library functions — the kernel only cares that they exist and honor the operation contracts.

---

## 9. Where the harness fits

Archeia is the contract for the **knowledge layer**: where artifacts live, who owns them, how they evolve. Below the knowledge layer is the **execution layer**, where skills run inside a **harness** — a runtime that loads skill files, invokes the model, manages context, enforces safety, and reads/writes the filesystem. Claude Code, Cursor, OpenCode, custom CLI loops, and bespoke agent frameworks are all harnesses.

**Archeia is harness-agnostic.** Any harness that produces and consumes conforming `.archeia/` trees is interoperable with Archeia, regardless of its language, framework, or model provider.

The term "harness" is industry coinage that has crossed into academic literature. Recent papers that use it formally include Meta-Harness (Lee et al., arXiv:2603.28052, 2026), Natural-Language Agent Harnesses (arXiv:2603.25723, 2026), AutoHarness (arXiv:2603.03329, 2026), and OpenDev's 81-page technical report (arXiv:2603.05344, 2026). The field has settled on "harness" as the term for this layer, and Archeia adopts it. See [`ONTOLOGY.md`](ONTOLOGY.md) §7 for the full citation survey.

### The one hard requirement Archeia places on harnesses

The harness owns **compaction** — the moment when the context window fills up and the model summarizes its working state to continue. Compaction is memory triage; whatever doesn't survive is lost. This is a harness concern, not Archeia's concern. But the harness must respect one invariant:

> **Writes to `.archeia/` MUST be flushed to disk before compaction may discard them from in-context state.**

If a harness compacts away a pending write to `.archeia/product/features/team-invites.md`, that's a harness bug, not an Archeia problem. The filesystem is the durable store; the harness's working memory is ephemeral by design. Compaction policy and persistence guarantees are separate concerns, and the kernel draws this line explicitly so that harness authors know where their responsibility ends and Archeia's begins.

### What must survive compaction

- **References to `.archeia/` paths the next turn will re-read from disk.** The harness must retain enough context for the next turn to know which files to re-open.
- **Any in-flight write that has not yet been committed to disk.** Either the write happens and the commit is visible to future turns, or the write never happened. No half-states.

### What can be lost at compaction

- Ephemeral reasoning traces, intermediate scratch
- Tool-call logs that are already persisted elsewhere (e.g., in the harness's own session log)
- Anything that has already been persisted into a durable artifact in the last turn

This division of labor is consistent with Sarah Wooders' framing in "Why memory isn't a plugin (it's the harness)" (X, April 4, 2026): *"Asking to plug memory into an agent harness is like asking to plug driving into a car. Managing context, and therefore memory, is a core capability and responsibility of the agent harness."* The harness manages what lives in the context window at any moment; Archeia provides the durable substrate the context window reads from and writes to. Neither layer replaces the other. This framing is also the core argument of Harrison Chase's "Your harness, your memory" (LangChain Blog, April 11, 2026), which makes the case that closed harnesses yield memory ownership to third parties and that open harnesses are the necessary response — an argument Archeia's open-standard approach aligns with directly.

### Why this matters

Without this boundary, the two layers fight each other. If a harness tries to manage persistent memory by keeping everything in context (bloat), or if Archeia tries to specify what the context window looks like (scope creep), both fail. Drawing the boundary here — Archeia owns durable, harness owns ephemeral, compaction must not drop pending durable writes — lets both layers do their jobs without stepping on each other.

---

## 10. Skill format (parameterized procedures)

Skills are procedural-memory artifacts that live **outside** `.archeia/` (typically in `skills/`, not a kernel concern where). A skill is a Markdown document with YAML frontmatter that teaches the model how to execute a specific workflow. The kernel specifies the minimum frontmatter shape.

### Required frontmatter fields

```yaml
---
name: <skill-name>
description: <trigger sentence for automatic invocation via description-matching>
---
```

Only `name` and `description` are strictly required. `name` must be unique within the distribution's namespace. `description` is the trigger text used by harnesses that support automatic skill selection (Claude Code, Cursor, etc.) — agents match user intent against skill descriptions to decide which skill to invoke.

### Recommended frontmatter fields

```yaml
---
name: review-product
description: ...
version: 0.1.0
parameters:
  - name: product_path
    type: file
    required: true
    description: Path to the product artifact under .archeia/product/
  - name: codebase_context
    type: directory
    required: false
    default: .archeia/codebase/model/c4/
reads:
  - .archeia/business/
  - .archeia/codebase/model/c4/
writes:
  - .archeia/product/product.md
  - .archeia/product/roadmap.md
  - .archeia/product/features/
  - .archeia/product/decisions/
pattern: consolidation
---
```

The `parameters` field is a refinement adopted from Garry Tan's "Thin Harness, Fat Skills" essay (X, [April 10, 2026](https://x.com/garrytan/status/2042925773300908103)) and supported by recent literature on atomic skills (Ma et al., arXiv:2604.05013, 2026). The core insight is that **skills are method calls with typed parameters, not undifferentiated prompts**. The same `/investigate` skill with different parameters produces radically different behaviors. Making this explicit lets harnesses validate inputs at invocation time and lets skill authors reason about reuse. Tan's own reference implementation is [gstack](https://github.com/garrytan/gstack) — 23 Claude Code skills organized as a virtual engineering organization.

The `reads` and `writes` fields declare the skill's `.archeia/` footprint. The optional `pattern` field names a non-kernel authoring pattern such as `consolidation`; kernel operations remain the deterministic tools that perform final filesystem mutations. These fields are not required for backward compatibility, but distributions that ship new skills are strongly encouraged to populate them, and kernel version 1.0 may make them mandatory.

### Skill invocation is harness business

How a skill gets invoked — automatic description-matching, explicit slash command, programmatic API call, scheduled cron — is the harness's concern. The kernel only specifies the file format and semantics.

---

## 11. Validation: what makes a repo conforming

A repo is **kernel-conforming** if `archeia:validate` passes with no errors against it. A conforming validator MUST check:

1. `.archeia/` MUST exist at the project root.
2. `standard/domains.yaml` MUST exist and MUST declare at least one domain.
3. `standard/VERSION` MUST exist and MUST be a valid semver string.
4. Every artifact under `.archeia/` MUST belong to a declared domain.
5. Every artifact MUST have a declared shape and MUST conform to that shape's base schema.
6. Every artifact MUST conform to any applicable artifact-type schema.
7. Every cross-domain read MUST be backed by a contract schema and the referenced artifacts MUST satisfy it.
8. Every transient artifact MUST have a valid status per the domain's status vocabulary.
9. Every transient artifact in a terminal status MUST have a terminal timestamp.
10. The validator SHOULD inspect git history for writes to each domain and SHOULD confirm they come from the declared owner. This check is advisory — git blame does not always identify writer families.

The validator SHOULD report failures with file-path citations so that a conforming repair tool can act on them. See [`CONFORMANCE.md`](CONFORMANCE.md) for the audit checklist and [`TEST-MATRIX.md`](TEST-MATRIX.md) for the concrete tests.

A repo is **distribution-conforming** if it is kernel-conforming AND it satisfies the additional rules of its declared distribution (specific domain layout, specific skill roster, specific retention windows, etc.). The [canonical software distribution](SCHEMA.md) and [Archeia Solo](https://github.com/Hugopeck/archeia/blob/main/DISTRIBUTION.md) both add such rules.

---

## 12. What the kernel explicitly does not do

The kernel is small by design. It does not:

- **Define a universal domain list.** Five domains is a software-project commitment; other fields pick their own.
- **Mandate a specific agent framework.** Claude Code, Cursor, custom loops — all fine as long as they produce conforming artifacts.
- **Provide a UI.** Humans use their editor; agents use their tools. No web dashboard, no SPA, no electron app. If a distribution wants to add a UI, it's a distribution concern.
- **Replace git.** Git is the history layer. The kernel assumes history exists; it does not provide history.
- **Define approval workflows.** "Who can accept a proposal?" is a policy question, not a kernel question. Distributions layer approval on top via status transitions tied to git PR reviews, human confirmation, or automated checks.
- **Provide search, full-text indexing, or embeddings.** The kernel is not a knowledge graph or a vector store. If you want search, glob and grep are the default; layer anything fancier on top yourself.

The kernel stays small so it can be implemented in a weekend, so it can be cited by tools from different vendors without intellectual-property friction, and so it can survive ten years of changing agent frameworks without needing a major version bump.

---

## 13. Versioning

The kernel uses semantic versioning. `standard/VERSION` at the repo root contains the kernel version the repo pins. A conforming tool reads this version and either processes the repo (if it supports that version) or refuses with a clear error.

- **Major version bump** — breaking changes to primitives, invariants, operations, or required distribution tooling.
- **Minor version bump** — additive changes: new optional fields, new optional operations, new validation checks that don't break existing conforming repos.
- **Patch version bump** — clarifications, documentation fixes, or non-normative additions.

The current kernel version is **0.2.1**. The 0.1 → 0.2 bump reflected the addition of Truth #7 (latent vs deterministic) to PRINCIPLES.md, the addition of the harness boundary section (§9), and the parameterized-skill format refinement (§10). The 0.2.0 → 0.2.1 patch bump corrects attribution errors across the ontology and audit docs: the "Thin Harness, Fat Skills" essay is by **Garry Tan** (not Steve Yegge, who was only quoted in it); the verified Sarah Wooders quote from "Why memory isn't a plugin (it's the harness)" is now cited correctly; Harrison Chase's "Your harness, your memory" (LangChain Blog) is now cited directly; and Michael Chomsky's analysis essay (which introduced the four-memory-competencies audit framework via MemoryAgentBench) is now cited separately from Harrison Chase's essay. The kernel will reach **1.0.0** when the first external distribution (not Archeia Solo) is shipped and the kernel has survived that contact with a new audience.

---

## 14. Summary

The Archeia Kernel is eight primitives, seven invariants, three lifecycle shapes, six deterministic operations, one inherent agent role, a harness boundary spec, a skill format spec, and one extension mechanism. Every conforming distribution extends it by declaring domains, contracts, and retention windows; every tool interoperable with Archeia implements the kernel operations against the distribution's schemas.

Everything else in the Archeia Standard — the specific domains, the specific skills, the specific ethos, the specific workflow — lives above the kernel in a distribution. The kernel's job is to be the smallest thing that makes all of that possible, so that many distributions can coexist without fighting each other, and so that tools from different vendors can compose on the same `.archeia/` tree without adapter code.

If you're implementing a tool that claims to support the Archeia Standard, this document is what you cite. If you're extending Archeia for a new audience or domain, this document is what you extend. Everything else is layered on top.
