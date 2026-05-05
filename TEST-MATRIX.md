# Archeia Test Matrix

The set of automatable tests every conformant Archeia repo MUST pass and every conformant tool MUST be capable of running. Each row in this document is a mechanical check that can be expressed as a JSON Schema validation, a glob query, a git-history query, or a small validator function.

This is the test plan for [`CONFORMANCE.md`](CONFORMANCE.md) — the conformance checklist tells you *what* to satisfy; this document tells you *how to verify* it.

---

## 1. Test categories

| Category | What it checks | Failure severity |
|---|---|---|
| **Structural** | Required directories and files exist; nothing is in the wrong place. | fatal |
| **Schema** | Every artifact validates against its base schema and any artifact-specific schema. | error |
| **Contract** | Every cross-domain dependency satisfies its declared JSON Schema contract. | error |
| **Lifecycle** | Transient artifacts have valid status, terminal timestamps where expected, and respect retention windows. | error |
| **Ownership** | Writes to each domain came from the declared owner. | advisory |
| **Evidence** | Descriptive artifacts cite source files; unevidenced claims are flagged. | advisory |
| **Operation** | The six kernel operations behave per [`REFERENCE-ALGORITHMS.md`](REFERENCE-ALGORITHMS.md) — pre/postconditions hold. | error |

---

## 2. Structural tests

| ID | Check | How |
|---|---|---|
| S1 | `.archeia/` directory exists at the project root. | filesystem stat |
| S2 | `.archeia/standard/domains.yaml` exists and parses as YAML. | parse |
| S3 | `.archeia/standard/VERSION` exists and is a valid semver string. | regex `^\d+\.\d+\.\d+(-[0-9A-Za-z-]+)?$` |
| S4 | `.archeia/standard/contracts/` exists. | filesystem stat |
| S5 | The kernel base schemas exist in `standard/contracts/`: `living-doc.schema.json`, `accumulating-record.schema.json`, `transient-artifact.schema.json`. | filesystem stat |
| S6 | Every domain declared in `standard/domains.yaml` has a corresponding directory under `.archeia/`. | walk + compare |
| S7 (software) | Exactly the five canonical domains are present: `business/`, `product/`, `codebase/`, `growth/`, `execution/`. No others. | walk + assert set equality |
| S8 (software) | `.archeia/codebase/` contains only the C4 JSON contract artifacts listed in [`SCHEMA.md`](SCHEMA.md) §2.3. | walk + glob filter |
| S9 (software) | If `docs/architecture.md` exists, it is owned by the codebase domain (per [`SCHEMA.md`](SCHEMA.md) §5). Absence is not a failure. | filesystem stat + ownership check |

---

## 3. Schema tests

For every artifact `A` under `.archeia/`:

| ID | Check | How |
|---|---|---|
| Sc1 | `A` has YAML frontmatter parseable as a map. | parse |
| Sc2 | `A`'s shape is declared (in frontmatter or inferable from path). | check |
| Sc3 | `A` validates against its shape's base schema (`living-doc`, `accumulating-record`, or `transient-artifact`). | JSON Schema validate |
| Sc4 | If `A` has an artifact-type schema (e.g., `task.schema.json`, `adr.schema.json`), `A` validates against it. | JSON Schema validate |
| Sc5 | If `A` is binary, it has a `<file>.meta.yaml` sidecar with `provenance`, `owner`, `schema_version`, `source`. | parse sidecar |

---

## 4. Contract tests (cross-domain reads)

For every contract declared in `standard/domains.yaml`:

| ID | Check | How |
|---|---|---|
| C1 | The contract schema file exists under `standard/contracts/`. | filesystem stat |
| C2 | Every artifact matching the contract's `from` glob validates against the contract schema. | JSON Schema validate per file |
| C3 | The contract's `to` domain has at least one reader skill or agent declared. | distribution metadata |

For the **canonical software application** specifically:

| ID | Check | How |
|---|---|---|
| C4 | `business/drafts/*.md` validate against `draft.schema.json`. | JSON Schema validate |
| C5 | `product/product.md` validates against `product.schema.json` (must contain Features, Constraints, Priorities sections; status: locked; locked_at timestamp). | JSON Schema + body parse |
| C6 | Every `codebase/architecture/*.json` validates against `c4.schema.json`. | JSON Schema validate |
| C7 | Every C4 element has at least one `evidence` file path that exists in the source tree. | path check |

---

## 5. Lifecycle tests

For every transient artifact `T`:

| ID | Check | How |
|---|---|---|
| L1 | `T.frontmatter.status` is in the distribution's status vocabulary for that artifact type. | set membership |
| L2 | The status maps to one of `future`, `present`, or `past` per the distribution's mapping. | lookup |
| L3 | If `T` is in a `past`-mapped status, `T.frontmatter` has the distribution's terminal timestamp field set. | check |
| L4 | If `T` has a terminal timestamp, the distribution's retention window has not been exceeded — OR `prune` would delete it on the next run. | compute |
| L5 | If `T` is in a `future`-mapped status, no `started` timestamp is present. | check |
| L6 | If `T` is in a `present`-mapped status, `started` is set and ≤ now(). | check |

For every accumulating record `R`:

| ID | Check | How |
|---|---|---|
| L7 | `R.frontmatter.status` is one of `active`, `superseded`, `archived`. | set membership |
| L8 | If `R.status == superseded`, `R.frontmatter.superseded_by` references an existing record at the named path. | path resolve |
| L9 | If `R.frontmatter.supersedes` is set, the referenced record exists and has `status: superseded`. | path resolve + check |
| L10 | The supersession chain has no cycles. | graph traversal |

For every living document `L`:

| ID | Check | How |
|---|---|---|
| L11 | `L` is regenerable per its declared regeneration contract (informational; not always automatable). | metadata check |
| L12 | If `L.frontmatter.last_verified` is present, it is a valid ISO 8601 timestamp ≤ now(). | parse |

---

## 6. Ownership tests (advisory)

For every artifact `A`:

| ID | Check | How |
|---|---|---|
| O1 | The most recent writer per `git log --follow A` is in the declared owner family for `A.domain`. | git blame + owner-family lookup |
| O2 | Every commit that modified `A` came from a writer in the declared owner family OR is flagged as a human override (`--allow-empty-message` or a `--co-author` for the owner skill). | git log walk |

These are **advisory** because git blame does not reliably identify writer families. Distributions MAY tighten them to `error` if their workflow records writer identity precisely.

---

## 7. Evidence tests (advisory)

For every descriptive artifact `D` (codebase domain artifacts plus any artifact with `kind: descriptive` in frontmatter):

| ID | Check | How |
|---|---|---|
| E1 | Every substantive claim in `D` cites at least one source (file path, commit hash, URL, or named external dataset). | regex + count |
| E2 | Unevidenced claims are flagged with `<!-- INSUFFICIENT EVIDENCE: ... -->` markers. | scan |
| E3 | Cited file paths exist in the source tree. | path check |
| E4 | Cited commit hashes exist in `git log`. | git lookup |

For every prescriptive artifact `P` (drafts, ADRs, vision documents):

| ID | Check | How |
|---|---|---|
| E5 | `P` cites its rationale (a problem statement, a referenced source, or a prior artifact). | scan |

Evidence checks are advisory because correctness requires reading the artifact, not just parsing it. Distributions SHOULD enforce them in CI for the artifacts where evidence discipline is load-bearing (codebase, ADRs, drafts).

---

## 8. Operation tests

For each kernel operation, run the reference algorithm from [`REFERENCE-ALGORITHMS.md`](REFERENCE-ALGORITHMS.md) against a fixture and assert pre/postconditions:

| ID | Operation | Test |
|---|---|---|
| Op1 | `advance` | Start with a transient artifact at `status: todo` (future). Run `advance` to `status: active`. Assert: status changed; `started` is set to a recent timestamp. Re-running on a non-future status fails the precondition. |
| Op2 | `complete` | Start with `status: active` (present). Run `complete` to `status: done`. Assert: status changed; `completed` is set; retention clock has begun. |
| Op3 | `prune` | Create a fixture with one transient artifact whose terminal timestamp is older than retention and one whose terminal timestamp is younger. Run `prune`. Assert: only the older one is deleted; deletion is a git commit; the younger one is untouched. |
| Op4 | `supersede` | Start with an accumulating record at `status: active`. Run `supersede` to a new path. Assert: new record exists with `supersedes:` set; old record is `status: superseded` with `superseded_by:` set; both files are on disk. |
| Op5 | `evolve` (living) | Modify a living document twice. Run `evolve`. Assert: returns the git log for the path. |
| Op6 | `evolve` (accumulating) | Build a chain of three superseded records. Run `evolve` on the newest. Assert: returns all three in order. |
| Op7 | `evolve` (transient) | Create a transient artifact, complete it, prune it. Run `evolve`. Assert: returns the on-disk past-state (if still in retention) plus the post-pruning git history. |
| Op8 | `consolidate` | Provide three source files. Run `consolidate` to a new living document. Assert: every claim cites at least one source; `last_verified` is set; running again with the same inputs produces a semantically equivalent output. |
| Op9 | `consolidate` (idempotence) | Run `consolidate` twice on identical inputs. Assert: claim set and citation set are equal; prose may differ. |
| Op10 | `init` | Run `init` on an empty repo. Assert: `.archeia/`, `standard/domains.yaml`, `standard/VERSION`, `standard/contracts/` all exist. Re-run. Assert: idempotent (no errors, no overwrites). |
| Op11 | `validate` | Run `validate` on a repo with three injected violations (one fatal, one error, one advisory). Assert: report contains all three at correct severity. |

---

## 9. Negative tests

Conformance also requires that *non-conforming* repos fail validation. Implementations MUST surface, not silently accept, the following situations:

| ID | Scenario | Expected outcome |
|---|---|---|
| N1 | Cross-domain write (a business writer modifies `product/product.md`). | `validate` reports an ownership violation. |
| N2 | A new domain directory not declared in `standard/domains.yaml`. | `validate` reports an undeclared domain. |
| N3 | A transient artifact in a `past`-mapped status without a terminal timestamp. | `validate` reports L3 failure. |
| N4 | An accumulating record manually deleted. | `validate` reports a missing supersession target if any record references it; OR a history-preservation violation if no supersession exists. |
| N5 | A contract file referenced in `domains.yaml` that doesn't exist in `standard/contracts/`. | `validate` reports C1 failure as fatal. |
| N6 | A `prune` invocation that would delete a non-transient artifact. | The implementation refuses with a precondition error. |
| N7 | A `supersede` invocation against a non-accumulating artifact. | The implementation refuses with a precondition error. |
| N8 | A `consolidate` invocation with a transient target. | The implementation refuses with a target-shape error. |
| N9 | Frontmatter mutation on an accumulating record other than the supersede mutation. | `validate` reports a history-preservation violation. |
| N10 | Binary artifact without a sidecar. | `validate` reports Sc5 failure. |

---

## 10. Test fixtures

A reference implementation SHOULD ship a `fixtures/` directory containing minimal example repos for each test row:

- `fixtures/conforming-software/` — passes every test.
- `fixtures/missing-archeia/` — fails S1.
- `fixtures/extra-domain/` — fails N2.
- `fixtures/cross-domain-write/` — fails N1.
- `fixtures/past-without-timestamp/` — fails L3.
- `fixtures/broken-supersession/` — fails L8 or N4.
- `fixtures/binary-without-sidecar/` — fails Sc5.

Every implementation that publishes conformance results SHOULD report which fixtures it processes correctly.

---

## 11. Continuous integration

A conformant repo SHOULD wire the following into CI:

- **On every push:** S1–S9, Sc1–Sc5, C1–C7, L1–L12.
- **On a schedule (daily or weekly):** Op3 (prune), O1–O2 (ownership), E1–E5 (evidence).
- **On every PR that modifies `standard/`:** the full suite, plus a regression test against the `fixtures/conforming-software/` fixture.

Error messages SHOULD be formatted to be re-fed into an agent's context per OpenAI's mechanical-enforcement principle (see [`distributions/archeia-enforcement.md`](distributions/archeia-enforcement.md) and [`POSITIONING.md`](POSITIONING.md) §4.2). A failing check is a remediation prompt, not just a red X.

---

## 12. References

- [`CONFORMANCE.md`](CONFORMANCE.md) — the conformance checklist this matrix tests
- [`REFERENCE-ALGORITHMS.md`](REFERENCE-ALGORITHMS.md) — the algorithms whose pre/postconditions Op1–Op11 verify
- [`KERNEL.md`](KERNEL.md) — the normative kernel
- [`SCHEMA.md`](SCHEMA.md) — the canonical software application
- [`contracts/`](contracts/) — the JSON Schemas referenced by Sc and C tests
- [`distributions/archeia-enforcement.md`](distributions/archeia-enforcement.md) — the mechanical-enforcement distribution flavor
