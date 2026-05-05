# Archeia Conformance Checklist

This document is the **Definition of Done** for any tool, distribution, or harness that claims to support the Archeia Standard. It restates the kernel's normative requirements in checklist form so that an implementer can audit their work line-by-line.

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, **MAY**, and **REQUIRED** are interpreted per [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

There are two levels of conformance:

- **Kernel-conforming** — implements every MUST in [`KERNEL.md`](KERNEL.md). Sufficient for a tool that wants to read or write `.archeia/` trees produced by any distribution.
- **Distribution-conforming** — kernel-conforming plus every MUST in the distribution's own spec (e.g., the canonical software application in [`SCHEMA.md`](SCHEMA.md), or the rules of a specific distribution like `archeia-solo`).

A tool MAY claim partial conformance by listing the specific levels and sections it implements, but MUST NOT claim "Archeia-conforming" without satisfying every kernel MUST.

---

## 1. Primitives

A conforming implementation MUST recognize all eight primitives defined in [`KERNEL.md`](KERNEL.md) §2:

- [ ] **Root** — the implementation operates on a project root containing an `.archeia/` directory.
- [ ] **Domain** — the implementation reads `standard/domains.yaml` to discover which domains exist; it does not hard-code a domain list.
- [ ] **Artifact** — the implementation accepts text-native files by default and accepts binary files only with a `<file>.meta.yaml` sidecar.
- [ ] **Shape** — the implementation recognizes the three lifecycle shapes (living, accumulating, transient) and applies their distinct rules.
- [ ] **Owner** — the implementation reads ownership assignments from `standard/domains.yaml` and enforces write authority accordingly.
- [ ] **Schema** — the implementation validates artifacts against the JSON Schemas in `standard/contracts/` at write time (for writers) or read time (for validators).
- [ ] **Contract** — the implementation enforces declared cross-domain read contracts.
- [ ] **Writer / Reader** — the implementation does not couple to a specific writer or reader; agents, skills, scripts, and humans are all permitted producers and consumers.

---

## 2. Invariants

A conforming implementation MUST uphold all seven invariants from [`KERNEL.md`](KERNEL.md) §3. Violation of any one is non-conformance.

- [ ] **I1.** Knowledge MUST live in `.archeia/` under the project root. The implementation MUST NOT depend on a server, schema registry, or message broker between agents.
- [ ] **I2.** Every artifact MUST belong to exactly one owning domain. No shared ownership, no multi-domain artifacts.
- [ ] **I3.** Every artifact MUST have exactly one lifecycle shape (living, accumulating, or transient).
- [ ] **I4.** Reads MUST be free across domains; writes MUST be owner-only. The implementation MUST NOT permit cross-domain writes.
- [ ] **I5.** Every factual claim in a descriptive artifact MUST cite a source (file path or commit). Every prescriptive artifact MUST cite its rationale and the prior artifacts it builds on. Claims that cannot be evidenced MUST be flagged in-line with `<!-- INSUFFICIENT EVIDENCE: [description] -->`.
- [ ] **I6.** Cross-domain dependencies MUST be declared as JSON Schema contracts under `standard/contracts/`. The implementation MUST NOT infer cross-domain dependencies that are not declared.
- [ ] **I7.** History MUST be preserved per shape: living → git, accumulating → on-disk forever, transient → on-disk during retention then git after pruning. The implementation MUST NOT destroy history.

---

## 3. The three lifecycle shapes

A conforming implementation MUST follow [`TEMPORAL_MODEL.md`](TEMPORAL_MODEL.md) and:

- [ ] Recognize all three shapes and apply each shape's rules.
- [ ] Edit living documents in place; preserve history in git.
- [ ] Append to accumulating records; never delete them; permit only the single frontmatter mutation defined for supersession.
- [ ] Flow transient artifacts through status values mapped to `future` / `present` / `past`; prune them after the distribution's declared retention window.
- [ ] Map each transient status to a temporal state per the distribution's `standard/domains.yaml` (or `standard/lifecycles.yaml`).

---

## 4. The six kernel operations

A conforming distribution MUST provide all six operations, either as named skills or as internal functions. Each operation MUST honor its contract from [`KERNEL.md`](KERNEL.md) §5 and the pseudocode in [`REFERENCE-ALGORITHMS.md`](REFERENCE-ALGORITHMS.md).

| Op | MUST | SHOULD | MAY |
|---|---|---|---|
| `advance` | Promote a transient artifact from a `future`-mapped status to a `present`-mapped status; record a `started` timestamp. | Be exposed as a named skill `archeia:advance`. | Be inlined into specialized skills. |
| `complete` | Promote a transient artifact from a `present`-mapped status to a `past`-mapped status; record a terminal timestamp; start the retention clock. | Be exposed as a named skill `archeia:complete`. | Be inlined into specialized skills. |
| `prune` | Delete transient artifacts whose retention window has elapsed since their terminal timestamp. Each deletion MUST be a git commit. | Be exposed as a named skill `archeia:prune` and runnable on a schedule. | Be wrapped as a maintenance skill (e.g., `archeia:tidy`). |
| `supersede` | Write a new accumulating record with `supersedes: <old-path>`; mutate the old record's `status` from `active` to `superseded` and add `superseded_by: <new-path>`. Both records MUST remain on disk. | Be exposed as a named skill. | Be inlined into other skills (e.g., `review-draft` superseding a prior decision). |
| `evolve` | Return the history of a named concept: `git log` for living, supersession chain for accumulating, on-disk + git for transient. | Be exposed as a named skill. | Return any structured form (timeline, diff, list) the distribution chooses. |
| `consolidate` | Read source artifacts and produce a target artifact that integrates their content with cited evidence. Target MUST be living or accumulating. Every substantive claim MUST cite at least one source. Operation MUST be semantically idempotent. When the target is a living document, `last_verified` MUST be updated. | Be implemented as multiple specialized skills (e.g., `archeia:write-tech-docs`, `archeia:scan-git`) rather than one generic skill. | Track consolidation cost in distribution telemetry. |

---

## 5. Inherent skills

A conforming distribution MUST provide all six inherent skills under its own namespace ([`KERNEL.md`](KERNEL.md) §6). Each SHOULD be invocable by name.

- [ ] `<distribution>:init` — scaffold `.archeia/`. MUST be idempotent.
- [ ] `<distribution>:validate` — walk `.archeia/`, check shape and schema conformance, verify cross-domain contracts, check transient status validity, verify ownership.
- [ ] `<distribution>:advance` — implements the `advance` operation.
- [ ] `<distribution>:complete` — implements the `complete` operation.
- [ ] `<distribution>:prune` — implements the `prune` operation. Each deletion MUST be a git commit.
- [ ] `<distribution>:consolidate` — implements the `consolidate` operation, OR the distribution provides specialized consolidation skills that collectively cover the operation contract.

`supersede` and `evolve` skills are RECOMMENDED but OPTIONAL — they MAY be inlined into other skills.

---

## 6. Inherent agents

A conforming distribution MUST provide one agent role ([`KERNEL.md`](KERNEL.md) §7):

- [ ] `archivist` — manages past-state transitions, supersession decisions, and retention policy. Reads the full `.archeia/` tree; writes frontmatter mutations on accumulating records and invocations of `complete` / `prune` on transient artifacts.

A distribution MAY provide additional agent roles. Only `archivist` is REQUIRED by the kernel.

---

## 7. The extension mechanism

A conforming distribution MUST provide all four extension artifacts ([`KERNEL.md`](KERNEL.md) §8):

- [ ] **`standard/domains.yaml`** declaring domains, owners, permitted shapes, and cross-domain reads.
- [ ] **Status vocabularies and temporal mappings** for every transient artifact type (status values, status → temporal mapping, retention window in days, terminal timestamp field name). MAY live in `standard/domains.yaml` or `standard/lifecycles.yaml`.
- [ ] **JSON Schemas** under `standard/contracts/` covering the kernel's three base shapes plus every distribution-specific contract.
- [ ] **Working implementations** of the six inherent skills and the `archivist` agent.

---

## 8. Validation

A conforming `validate` implementation MUST check all of the following ([`KERNEL.md`](KERNEL.md) §11):

- [ ] `.archeia/` exists at the project root.
- [ ] `standard/domains.yaml` exists and declares at least one domain.
- [ ] `standard/VERSION` exists and is a valid semver string.
- [ ] Every artifact under `.archeia/` belongs to a declared domain.
- [ ] Every artifact has a declared shape and conforms to that shape's base schema.
- [ ] Every artifact conforms to any applicable artifact-type schema.
- [ ] Every cross-domain read is backed by a contract schema, and the referenced artifacts satisfy it.
- [ ] Every transient artifact has a valid status per the domain's status vocabulary.
- [ ] Every transient artifact in a terminal status has a terminal timestamp.
- [ ] Ownership is respected (advisory check via git history).

The validator SHOULD report failures with file-path citations so that a conforming repair tool can act on them.

---

## 9. Software-distribution conformance (canonical software application)

A repo claiming to use the canonical software application from [`SCHEMA.md`](SCHEMA.md) MUST additionally satisfy:

- [ ] Exactly the five canonical domains exist under `.archeia/`: `business/`, `product/`, `codebase/`, `growth/`, `execution/`.
- [ ] No domain directory outside the canonical five exists under `.archeia/`.
- [ ] `.archeia/codebase/` contains only the C4 JSON contract artifacts listed in [`SCHEMA.md`](SCHEMA.md) §2.3 — no prose docs.
- [ ] All three cross-domain contracts are enforced: `business → product` (via `draft.schema.json`), `product → execution` (via `product.schema.json`), `codebase → product/decisions` (via `c4.schema.json`).
- [ ] Codebase-owned colocated files in `docs/` (per [`SCHEMA.md`](SCHEMA.md) §5) follow the same ownership rules; their absence is not a conformance failure.

---

## 10. Harness compatibility

A conforming **harness** ([`KERNEL.md`](KERNEL.md) §9) MUST:

- [ ] Flush writes to `.archeia/` to disk before compaction may discard them from in-context state.
- [ ] Retain enough context across compaction for the next turn to know which `.archeia/` paths to re-read.
- [ ] Either complete an in-flight `.archeia/` write or abort it cleanly. Half-states are non-conformant.

A harness MAY manage anything else about its context window however it wants. The kernel does not constrain compaction policy beyond the durable-write boundary.

---

## 11. Skill format

A conforming skill ([`KERNEL.md`](KERNEL.md) §10) MUST have YAML frontmatter with at minimum:

- [ ] `name` — unique within the distribution's namespace.
- [ ] `description` — the trigger sentence used for automatic skill selection.

A conforming skill SHOULD additionally populate:

- [ ] `version`, `parameters`, `reads`, `writes`, `operation`.

These will become MUST in kernel version 1.0.

---

## 12. Versioning

A conforming distribution MUST:

- [ ] Pin a kernel version range in `standard/domains.yaml` (e.g., `kernel: ">=0.3.0, <1.0.0"`).
- [ ] Declare its own distribution version separately from the kernel version.
- [ ] Refuse to process a repo whose pinned kernel version is unsupported, with a clear error rather than corrupting the tree.

---

## 13. Conformance reporting

A tool that wants to advertise its conformance level SHOULD report:

- The kernel version it implements.
- The distribution(s) it supports.
- Which sections of this checklist it has audited (e.g., "kernel-conforming except §11.skills format extended frontmatter, which is OPTIONAL pre-1.0").

A tool MUST NOT claim "Archeia-conforming" without satisfying every MUST in §1–§8 and §10–§12 of this document at the kernel version it pins.

---

## 14. References

- [`KERNEL.md`](KERNEL.md) — the abstract substrate this checklist audits against
- [`SCHEMA.md`](SCHEMA.md) — the canonical software application
- [`REFERENCE-ALGORITHMS.md`](REFERENCE-ALGORITHMS.md) — pseudocode for the six operations
- [`TEST-MATRIX.md`](TEST-MATRIX.md) — the per-schema test plan a conforming repo passes
- [`POSITIONING.md`](POSITIONING.md) — what Archeia adds beyond the SOTA harness corpus
- [`PRINCIPLES.md`](PRINCIPLES.md) — the seven fundamental truths
- [`TEMPORAL_MODEL.md`](TEMPORAL_MODEL.md) — the three lifecycle shapes
- [`ONTOLOGY.md`](ONTOLOGY.md) — vocabulary and academic citations
