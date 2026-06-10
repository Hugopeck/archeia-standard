# Archeia Build Spec

This document is the build contract for Archeia Factory. It consolidates what implementers need from the operational model ([`ontology.md`](ontology.md)) and enforcement rules ([`rules.md`](rules.md)) into one place.

Use this document when building tools — especially `init` and `validate`. For motivation, see [`overview.md`](overview.md). For theoretical grounding, see [`../research/theoretical-basis.md`](../research/theoretical-basis.md).

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

## 2. What Lives Where

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

## 3. Domains

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

## 4. Lifecycle Shapes

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

## 5. Ownership

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

## 6. Contract Surfaces

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

## 7. Flex Rules

- Canonical names stay fixed.
- Canonical meanings stay fixed.
- Sparse use is normal.
- Omission is allowed when a subtree is irrelevant.
- Broader interpretation is allowed inside the defined meaning.
- Arbitrary repurposing of canonical paths is invalid.
- An Instance may add stricter local rules or extra subtrees, but should not redefine canonical paths.

---

## 8. Instance Manifest (`spec.yaml`)

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

## 9. Operations

Archeia defines six deterministic operations. Tools may implement them in any language if observable behavior matches.

| Operation | Purpose |
|---|---|
| `init` | Install an Instance into a project repo. |
| `validate` | Return structured health issues. |
| `write` | Create or update artifacts when ownership, shape, schema, and contract rules pass. |
| `transition` | Move transient artifacts through declared statuses. |
| `prune` | Remove expired transient artifacts after their retention window. |
| `history` | Show history using the right mechanism for the artifact shape. |

Failed preconditions should stop an operation before partial writes.

### `init` — build requirements

This section is the contract for implementing `init`. No `init` tool ships yet; `scripts/archeia_validate` defines the acceptance bar.

**Input:** a project root directory (target repo).

**Output:** an Instance that passes `scripts/archeia_validate <project-root>` with zero errors.

**`init` must:**

1. Create `.archeia/` and the four top-level domain directories.
2. Create `.archeia/.system/` with `VERSION`, `spec.yaml`, and `contracts/`.
3. Copy all five schema files from Blueprint `contracts/` into `.archeia/.system/contracts/`.
4. Write `spec.yaml` declaring domains, owners, canonical tree, shapes, contracts, lifecycles, retention, and schema bindings.
5. Scaffold every path listed in `canonical_tree` with a `README.md` (except `.archeia/.system/contracts/`).
6. Not write artifacts outside declared top-level domains.

**Reference template:** `examples/.archeia/` (valid full-canonical-tree Instance).

**Suggested invocation (not yet implemented):**

```sh
scripts/archeia_init <project-root>
```

### `validate` — implemented

```sh
scripts/archeia_validate <project-root>
```

Exits `0` when no fatal or error issues exist. Prints structured issues to stdout.

See [section 10](#10-validation-checks) for the full check list.

---

## 10. Validation Checks

What `scripts/archeia_validate` checks today:

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

## 11. Harness Boundary

The harness is the execution environment that loads skills, invokes models, manages context, and writes files. Archeia is the project knowledge contract at the layer below.

A harness must flush `.archeia/` writes to disk before it discards in-context state. Losing a pending `.archeia/` write during compaction is a harness bug.

Archeia does not specify the harness. It specifies what the harness produces and consumes.

---

## 12. What Archeia Is Not

- A hosted service, ticket system, wiki, vector database, or agent framework.
- A public adoption or conformance program.
- A complete workflow map of every internal step.

Those tools can sit around an Instance. Archeia is the repo-local knowledge contract they can read from and write to.

---

## 13. Open Questions

Items not yet specified. Resolve before or during implementation.

### `init`

- [ ] CLI flags: `--dry-run`, `--force` on existing `.archeia/`, sparse tree vs full canonical tree?
- [ ] Should `init` copy example artifact templates or only scaffold empty `README.md` files?
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

---

## 14. Related Documents

| Document | Role |
|---|---|
| [`overview.md`](overview.md) | Why Archeia exists |
| [`ontology.md`](ontology.md) | Operational model and block model |
| [`rules.md`](rules.md) | Rules, operations, and test scenarios |
| [`../research/theoretical-basis.md`](../research/theoretical-basis.md) | Research grounding and citations |
| [`../../examples/.archeia/`](../../examples/.archeia/) | Valid reference Instance |
| [`../../scripts/archeia_validate`](../../scripts/archeia_validate) | Current validator implementation |
