# Archeia Build Spec

This document is the build contract for Archeia Factory. It consolidates what implementers need from the operational model ([`ontology.md`](ontology.md)) and enforcement rules ([`rules.md`](rules.md)) into one place.

Use this document when building tools — especially `init` and `validate`. For motivation, see [`overview.md`](overview.md). For theoretical grounding, see [`../research/theoretical-basis.md`](../research/theoretical-basis.md).

Archeia is at **Blueprint v0**: a rough, complete starting point meant to be tested by real use, not perfected in advance.

---

## 1. Identity

```text
Archeia Factory     the whole system
├── Blueprint       reusable source architecture (this repo)
└── Instance        installed `.archeia/` layer in a project repo
```

| Term | Meaning |
|---|---|
| **Factory** | The complete system: Blueprint, Instance shape, validation, and procedures. |
| **Blueprint** | The reusable source maintained in this repository. |
| **Instance** | The `.archeia/` operating layer that `init` installs into a project repo. |
| **Project root** | A software repo that hosts an Instance. |

```text
Blueprint (this repo)  --init-->  Instance (.archeia/ in a project)
```

In prose, prefer `.archeia/`, `spec.yaml`, and domain names over repeating "instance."

---

## 2. Blueprint v0 Philosophy

Blueprint v0 is intentionally broad. The canonical tree defines a **complete address space** for project operating knowledge — not because every project needs full answers everywhere, but because every project should have a **settled place** for every class of question.

### The core bet

Important postures, defaults, and decisions often live only in someone's head. They sound obvious to the person who holds them. They are not obvious to an agent. Archeia challenges that by making coordinates explicit:

- For any topic — ethics, hiring, compliance, roadmap, architecture — there is exactly one canonical path.
- The file at that path holds an answer, however small: two sentences, "N/A", or "not applicable for this project."
- An agent does not have to guess where truth should live; it only has to read whether it has been written yet.

Sparse content is normal. Missing paths are not.

### What v0 is and is not

| Blueprint v0 is | Blueprint v0 is not |
|---|---|
| A complete question bank distributed across paths | A demand for full company documentation in every repo |
| A rough starting Blueprint to iterate by using | A finished operating system |
| An address space contract agents can rely on | A judgment of content quality |
| A decomposition map for future agent ownership | A replacement for harness skills today |

The roughness of ~170 canonical directories is accepted. Improvement comes from dogfooding, not from shrinking the tree before the first real Instance.

### Question-stub READMEs

Each canonical directory gets a `README.md` that is a **question stub**, not an empty placeholder. `init` scaffolds these from Blueprint templates.

A stub should:

- name the path's purpose in plain language
- include one to three prompts for what to answer here
- allow minimal valid answers ("N/A", "solo — no hiring yet", two sentences)

Example pattern:

```markdown
# Ethics

Answer here (even "N/A" or "not applicable yet"):

- What is our minimum ethics posture for this project?
- What would we refuse to build or ship?
```

### How tools serve v0 (Option A)

```text
Blueprint v0 (question bank + contract)
    ↓ init           primary v0 deliverable — scaffold full tree + stubs
Instance           address space exists
    ↓ humans/agents fill slots (minimally is fine)
    ↓ validate       contract check — Instance still matches Blueprint
    ↓ dogfood log    which paths were used, skipped, or wrong
    ↓ Blueprint v1   refine questions, merge paths, agent-absorb subtrees
```

**`init`** is the main v0 tool. It removes the friction of creating the tree by hand.

**`validate`** is a **contract check**, not a content-quality gate. It verifies that the Instance implements the Blueprint address space (paths, manifest, declared schemas). It does not judge whether answers are good or whether agents benefited.

Product value in v0 is proven by dogfooding, not by validation alone.

### v0 success criterion

> When an agent faces a decision in domain X, it can find the canonical path for X without asking the human — and the file either contains an answer or explicitly says it is not applicable yet.

### Dogfood iteration (manual, pre-tooling)

After using an Instance on a real project, mark paths:

| Mark | Meaning |
|---|---|
| **used** | agent or human read/wrote here; question was valuable |
| **skipped** | never touched; may be fine for this project type |
| **wrong question** | path exists but the framing misfired; Blueprint candidate for change |

This log feeds Blueprint v1. No validator enforces it in v0.

### Future evolution: agent absorption

Over time, mature subtrees may compress into **domain agents** (skills or harness roles). Example: a compliance agent owns `operations/compliance/*` — embedded questions, update rules, and judgments — and the scattered README stubs become agent instructions rather than 170 human-maintained entry points.

v0 does not implement agent absorption. The wide tree is a **decomposition map** for that future handoff.

---

## 3. What Lives Where

### Blueprint (this repository)

```text
contracts/          # source JSON Schemas
docs/               # architecture docs, guides, research
examples/           # valid and invalid Instance fixtures
scripts/            # deterministic tools (validate today; init planned)
VERSION             # Blueprint version
```

### Instance (project repo)

```text
.archeia/
├── .system/
│   ├── VERSION
│   ├── spec.yaml       # machine-readable manifest (JSON content)
│   └── contracts/      # installed schema copies
├── strategy/
├── operations/
├── product/
└── growth/
```

The Blueprint copies source schemas from `contracts/` into `.archeia/.system/contracts/` during `init`.

---

## 4. Domains

Every Instance uses four top-level domains. Each artifact belongs to exactly one.

| Domain | Purpose |
|---|---|
| `strategy/` | Direction, values, landscape, roadmap, and strategy-owned execution. |
| `operations/` | Support, improvement, execution, people, finance, compliance, and process. |
| `product/` | Product strategy, design, technical evidence, and delivery context. |
| `growth/` | Adoption, go-to-market, sales, success, support, and rollout. |

### Important subtrees

- `operations/optimization/processes/` — repeatable operating methods, SOPs, runbooks.
- `product/technical/specs/` — executable software specs.
- `product/technical/architecture/c4/` — machine-readable architecture evidence.
- `product/execution/prds/` — integrated buildable product missions.
- `growth/execution/experiments/` — growth experiment state and learnings.

### Local knowledge surfaces

These may appear directly under any canonical domain or subdomain:

- `decisions/` — accumulating records of choices and tradeoffs.
- `conventions/` — living documents for local defaults and ways of working.
- `learnings/` — accumulating records of lessons and discoveries.

Do not hide these under wrappers such as `meta/` or `memory/`.

### Canonical tree

The full canonical directory list lives in `examples/.archeia/.system/spec.yaml` under `canonical_tree`. A project may use the tree sparsely, but canonical names and meanings do not change.

---

## 5. Lifecycle Shapes

| Shape | Behavior | Examples |
|---|---|---|
| **Living** | Edited in place. Git holds history. | Vision docs, process docs, specs, conventions. |
| **Accumulating** | Append-only records. Old records stay on disk. | Decisions, learnings, retros, studies. |
| **Transient** | Moves through statuses. Pruned after retention once terminal. | Tasks, plans, projects, programs, running experiments. |

### Shape rules

- Living artifacts are edited in place.
- Accumulating records are not deleted; only declared metadata updates are allowed.
- Transient deletion goes through pruning unless the Instance manifest explicitly allows direct deletion.
- Operations on the same artifact should be serialized.
- Multi-file writes should be transactional where possible.

---

## 6. Ownership

Each top-level domain has one owner family. Writers may read across domains, but writes go through the owning domain.

Ownership is the concurrency model for parallel human and agent work. Delegation is allowed, but the owning domain remains responsible for the write.

Default owner families (from the example Instance):

| Domain | Owner |
|---|---|
| `strategy/` | `strategy-skills` |
| `operations/` | `operations-skills` |
| `product/` | `product-skills` |
| `growth/` | `growth-skills` |

Ownership checks are advisory unless a validator has reliable writer identity from git history.

---

## 7. Contract Surfaces

Two canonical cross-domain contract surfaces are validated by installed schemas:

### Product delivery

- Paths: `product/strategy/roadmap/*.md`, `product/technical/specs/*.md`, `product/execution/prds/*.md`
- Schema: `product.schema.json`
- Required frontmatter: `title`, `owner`, `status`, `last_reviewed`
- `owner` must be `product-skills`

### Technical evidence

- Paths: `product/technical/architecture/c4/*.json`
- Schema: `c4.schema.json`
- Every element must have a non-empty `evidence` array
- Each evidence path must exist relative to the Instance or project root

---

## 8. Flex Rules

- Canonical names stay fixed.
- Canonical meanings stay fixed.
- Sparse use is normal.
- Omission is allowed when a subtree is irrelevant.
- Broader interpretation is allowed inside the defined meaning.
- Arbitrary repurposing of canonical paths is invalid.
- An Instance may add stricter local rules or extra subtrees, but should not redefine canonical paths.

---

## 9. Instance Manifest (`spec.yaml`)

The installed manifest is `.archeia/.system/spec.yaml`. Despite the extension, the current format is **JSON**.

Reference: `examples/.archeia/.system/spec.yaml`

### Top-level fields

| Field | Type | Purpose |
|---|---|---|
| `standard_version` | string | Blueprint version this Instance was built from. **Legacy name** — planned rename to `archeia_version`. |
| `distribution` | object | Instance identity. **Legacy name** — planned rename. |
| `distribution.name` | string | Instance configuration name (example: `archeia-standard-full-canonical-tree`). |
| `distribution.version` | string | Instance configuration version. |
| `ontology` | object | Reference to the ontology document. |
| `ontology.document` | string | Path to ontology in Blueprint (example: `docs/standard/ontology.md`). |
| `domains` | string[] | Declared top-level domains. Must include all four. |
| `owners` | object | Maps each domain to its owner family. |
| `canonical_tree` | string[] | Every canonical directory path, relative to project root. |
| `shapes` | string[] | Declared artifact shapes: `living`, `accumulating`, `transient`. |
| `contracts` | object[] | Declared contract surfaces (name, schema, paths). |
| `lifecycles` | object | Transient status mappings and terminal timestamp fields. |
| `retention` | object | Retention windows in days for transient artifact types. |
| `schemas` | object | Maps shape and contract names to installed schema filenames. |

### `lifecycles` (example Instance)

```json
"transient_statuses": {
  "future": ["todo", "backlog", "proposed"],
  "present": ["active", "in_progress", "review", "current", "running"],
  "past": ["done", "cancelled", "superseded", "accepted", "rejected", "concluded"]
}
```

Terminal timestamp fields: `completed_at`, `cancelled_at`, `concluded_at`, `terminal_timestamp`

A transient artifact with a `past`-mapped status must have at least one terminal timestamp field set.

### `retention` (example Instance)

```json
"tasks_days": 14,
"plans_days": 30,
"experiments_days": 30
```

### Installed schemas

These files must exist under `.archeia/.system/contracts/`:

- `living-doc.schema.json`
- `accumulating-record.schema.json`
- `transient-artifact.schema.json`
- `product.schema.json`
- `c4.schema.json`

### Deprecated manifest

Validators may warn on `domains.yaml`. New Instances must use `spec.yaml`.

---

## 10. Operations

Archeia defines six deterministic operations. Tools may implement them in any language if observable behavior matches.

| Operation | Purpose |
|---|---|
| `init` | Install an Instance into a project repo. |
| `validate` | Contract check — return structured Blueprint compliance issues. |
| `write` | Create or update artifacts when ownership, shape, schema, and contract rules pass. |
| `transition` | Move transient artifacts through declared statuses. |
| `prune` | Remove expired transient artifacts after their retention window. |
| `history` | Show history using the right mechanism for the artifact shape. |

Failed preconditions should stop an operation before partial writes.

### `init` — build requirements (v0)

This section is the contract for implementing `init`. No `init` tool ships yet; `scripts/archeia_validate` defines the acceptance bar.

See [section 2](#2-blueprint-v0-philosophy) for why v0 scaffolds the full canonical tree with question-stub READMEs.

**Input:** a project root directory (target repo).

**Output:** an Instance that passes `scripts/archeia_validate <project-root>` with zero errors.

**`init` must:**

1. Create `.archeia/` and the four top-level domain directories.
2. Create `.archeia/.system/` with `VERSION`, `spec.yaml`, and `contracts/`.
3. Copy all five schema files from Blueprint `contracts/` into `.archeia/.system/contracts/`.
4. Write `spec.yaml` from the Blueprint reference template (`examples/.archeia/.system/spec.yaml`), updating instance identity as needed.
5. Scaffold every path listed in `canonical_tree` with a **question-stub** `README.md` (except `.archeia/.system/contracts/`). Each stub names the path purpose and includes one to three prompts. Stubs may be rendered from Blueprint templates keyed by path.
6. Not write artifacts outside declared top-level domains.

**v0 decisions (settled):**

- Full canonical tree — not a sparse or optional subset.
- Question-stub READMEs — not blank files.
- No example artifact templates beyond stubs in v0.

**Reference Instance:** `examples/.archeia/` (passes validate today; README stubs will gain question prompts when templates land).

**Suggested invocation (not yet implemented):**

```sh
scripts/archeia_init <project-root>
```

### `validate` — implemented (contract check)

```sh
scripts/archeia_validate <project-root>
```

Exits `0` when no fatal or error issues exist. Prints structured issues to stdout.

**Job in v0:** verify Blueprint contract compliance — manifest, paths, scaffolds, and declared schema surfaces. Does **not** judge content quality, answer completeness, or agent outcomes.

See [section 11](#11-validation-checks) for the full check list.

---

## 11. Validation Checks

What `scripts/archeia_validate` checks today. These are **contract checks** for Blueprint v0 (see [section 2](#2-blueprint-v0-philosophy)), not content-quality gates:

### Structure

| Code | Severity | Check |
|---|---|---|
| A001 | fatal | `.archeia/` exists |
| S001 | fatal | `.archeia/.system/spec.yaml` exists |
| S002 | warning | `domains.yaml` present without `spec.yaml` (deprecated) |
| S003 | error | `spec.yaml` parses as JSON |
| S010 | error | each installed schema file exists |
| S011 | error | each installed schema parses as JSON |
| T001 | error | four top-level domains exist |
| T002 | error | no directories under `.archeia/` outside declared domains (except `.system`) |
| T010 | error | every `canonical_tree` path exists as a directory |
| T011 | error | every canonical directory has `README.md` (except `contracts/`) |
| A010 | error | no `.md` artifacts outside declared domains |

### Product delivery contracts

| Code | Severity | Check |
|---|---|---|
| P001 | error | required frontmatter: `title`, `owner`, `status`, `last_reviewed` |
| P002 | error | `owner` must be `product-skills` |

### Technical evidence (C4)

| Code | Severity | Check |
|---|---|---|
| C001 | error | C4 JSON parses |
| C002 | error | at least one element |
| C003 | error | every element has non-empty `evidence` |
| C004 | error | every evidence path exists |

### Transient lifecycle

Checked in these directories when present:

- `operations/execution/tasks/`
- `operations/execution/projects/`
- `operations/execution/plans/`
- `product/execution/plans/`
- `growth/execution/plans/`
- `growth/execution/programs/`
- `growth/execution/experiments/running/`

| Code | Severity | Check |
|---|---|---|
| L001 | error | `status` is in manifest `transient_statuses` |
| L002 | error | terminal status has a terminal timestamp field |

### Test fixtures

| Fixture | Expected failure |
|---|---|
| `examples/.archeia/` | passes |
| `examples/invalid/missing-c4-evidence/` | C003 |
| `examples/invalid/missing-folder-readme/` | T011 |
| `examples/invalid/domains-yaml-without-spec/` | S001 |
| `examples/invalid/bad-transient-status/` | L001 |
| `examples/invalid/missing-terminal-timestamp/` | L002 |
| `examples/invalid/artifact-outside-domain/` | A010 |

---

## 12. Harness Boundary

The harness is the execution environment that loads skills, invokes models, manages context, and writes files. Archeia is the project knowledge contract at the layer below.

A harness must flush `.archeia/` writes to disk before it discards in-context state. Losing a pending `.archeia/` write during compaction is a harness bug.

Archeia does not specify the harness. It specifies what the harness produces and consumes.

---

## 13. What Archeia Is Not

- A hosted service, ticket system, wiki, vector database, or agent framework.
- A public adoption or conformance program.
- A complete workflow map of every internal step.

Those tools can sit around an Instance. Archeia is the repo-local knowledge contract they can read from and write to.

---

## 14. Open Questions

Items not yet specified. Resolve before or during implementation.

### `init` (v0 settled / still open)

- [x] v0 scaffolds the **full canonical tree** (not sparse).
- [x] v0 scaffolds **question-stub READMEs** (not blank placeholders).
- [x] v0 does not copy example artifact templates beyond stubs.
- [ ] CLI flags: `--dry-run`, `--force` on existing `.archeia/`?
- [ ] Where do README question templates live in the Blueprint (`templates/readmes/` or keyed map)?
- [ ] How should `init` set `distribution.name` / instance identity — fixed default or configurable?
- [ ] Should `VERSION` in `.archeia/.system/` mirror Blueprint `VERSION` or track Instance config version separately?

### Schema rename (planned)

- [ ] Rename `standard_version` → `archeia_version` in `spec.yaml`
- [ ] Rename `distribution` → instance identity field (name TBD)
- [ ] Rename `spec.yaml` to `spec.json` or keep extension with JSON content?

### Update and sync

- [ ] How does a project Instance update when the Blueprint changes?
- [ ] Diff tool: Blueprint vs installed Instance?
- [ ] Local overrides: can a project patch manifest fields without forking the tree?

### Operations not yet implemented

- [ ] `write`, `transition`, `prune`, `history` — language, CLI shape, error format
- [ ] Retention enforcement: validator checks windows or only `prune` operation?

### Validation gaps

- [ ] Living and accumulating schema validation (only product and C4 contracts are checked today)
- [ ] Ownership enforcement from git history
- [ ] Citation grammar for evidence policy

### Blueprint bundles (deferred)

- [ ] Multiple reusable init recipes on the Blueprint side — see [`../guides/distributions.md`](../guides/distributions.md)

### Agent absorption (post-v0)

- [ ] Manifest metadata for agent-owned subtrees vs directory-owned stubs
- [ ] Validate rules when a subtree is owned by a skill instead of README files

---

## 15. Related Documents

| Document | Role |
|---|---|
| [`overview.md`](overview.md) | Why Archeia exists |
| [`ontology.md`](ontology.md) | Operational model and block model |
| [`rules.md`](rules.md) | Rules, operations, and test scenarios |
| [`../research/theoretical-basis.md`](../research/theoretical-basis.md) | Research grounding and citations |
| [`../../examples/.archeia/`](../../examples/.archeia/) | Valid reference Instance |
| [`../../scripts/archeia_validate`](../../scripts/archeia_validate) | Current validator implementation |
