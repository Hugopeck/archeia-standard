# Archeia Test Matrix

The set of automatable tests every conformant Archeia repo MUST pass and every conformant tool MUST be capable of running.

## 1. Structural tests

| ID | Check | How |
|---|---|---|
| S1 | `.archeia/` directory exists at the project root. | filesystem stat |
| S2 | `.archeia/standard/domains.yaml` exists and parses as YAML. | parse |
| S3 | `.archeia/standard/VERSION` exists and is a valid semver string. | regex |
| S4 | `.archeia/standard/contracts/` exists. | filesystem stat |
| S5 | Base schemas exist in `standard/contracts/`. | filesystem stat |
| S6 | Every domain declared in `standard/domains.yaml` has a corresponding directory under `.archeia/`. | walk + compare |
| S7 (software) | Exactly the four canonical top-level domains are present: `strategy/`, `operations/`, `product/`, `growth/`. | walk + assert set equality |
| S8 (software) | Canonical top-level domains are not renamed or replaced. | walk + path check |
| S9 (software) | `product/` contains the canonical kernel subareas `strategy/`, `design/`, `technical/`, and `execution/`, and `growth/` contains `strategy/`, `marketing/`, `sales/`, `success/`, and `execution/`, though omitted nested folders are allowed where unused. | walk + path check |
| S10 (software) | `product/technical/architecture/c4/` contains only living machine-readable architecture artifacts. | walk + glob filter |
| S11 (software) | If a repo claims canonical `decisions/`, `conventions/`, or `learnings/` surfaces, they appear as direct children of their owning canonical domains or subdomains. | walk + path pattern check |
| S12 (software) | If a repo claims a canonical procedural-guides surface, that surface is `operations/optimization/guides/`. | walk + path pattern check |
| S13 (software) | `docs/` is not required for software conformance. | skip / ignore |

## 2. Schema tests

For every artifact `A` under `.archeia/`:

| ID | Check | How |
|---|---|---|
| Sc1 | `A` has parseable frontmatter or structured JSON body as appropriate. | parse |
| Sc2 | `A` has a declared shape. | check |
| Sc3 | `A` validates against its shape's base schema. | JSON Schema validate |
| Sc4 | If `A` has an artifact-type schema, `A` validates against it. | JSON Schema validate |
| Sc5 | If `A` is binary, it has a `<file>.meta.yaml` sidecar. | parse sidecar |

## 3. Contract tests

| ID | Check | How |
|---|---|---|
| C1 | The contract schema file exists under `standard/contracts/`. | filesystem stat |
| C2 | Every artifact matching the contract's `from` glob validates against the contract schema. | JSON Schema validate |
| C3 | The contract's `to` domain has at least one reader skill or agent declared. | distribution metadata |
| C4 | The product execution surface validates against `product.schema.json`: roadmap artifacts under `product/strategy/roadmap/`, specs under `product/technical/specs/`, and PRDs under `product/execution/prds/`. | JSON Schema + body parse |
| C5 | Every `product/technical/architecture/c4/*.json` validates against `c4.schema.json`. | JSON Schema validate |
| C6 | Every C4 element has at least one `evidence` file path that exists in the source tree. | path check |
| C7 | Product artifacts with `external_sources` include `type`, `name`, `extraction_method`, `last_read`, and `source_status`. | frontmatter parse |

## 4. Lifecycle tests

| ID | Check | How |
|---|---|---|
| L1 | Every transient artifact has a valid status. | set membership |
| L2 | The status maps to `future`, `present`, or `past`. | lookup |
| L3 | Past-state transient artifacts have a terminal timestamp. | check |
| L4 | Expired transient artifacts are prune-eligible. | compute |
| L5 | Future-state transient artifacts do not have start timestamps. | check |
| L6 | Present-state transient artifacts do have start timestamps. | check |
| L7 | Accumulating records use valid record statuses. | set membership |
| L8 | Supersession links resolve. | path resolve |
| L9 | Supersession chains do not cycle. | graph traversal |

## 5. Ownership tests

| ID | Check | How |
|---|---|---|
| O1 | The most recent writer of an artifact is in the declared owner family for the top-level domain. | git log |
| O2 | Every commit that modified an artifact came from the owner family or a flagged human override. | git log walk |

## 6. Evidence tests

| ID | Check | How |
|---|---|---|
| E1 | Every substantive claim in a descriptive artifact cites at least one source. | regex + count |
| E2 | Unevidenced claims are flagged. | scan |
| E3 | Cited file paths exist. | path check |
| E4 | Cited commit hashes exist. | git lookup |
| E5 | Prescriptive artifacts cite rationale or prior artifacts. | scan |

## 7. Operation tests

| ID | Operation | Test |
|---|---|---|
| Op1 | `init` | Scaffold the declared `.archeia/` structure and assert idempotence. |
| Op2 | `validate` | Report one fatal, one error, and one advisory issue correctly. |
| Op3 | `write` (living) | Permit valid owner writes and refuse invalid ones. |
| Op4 | `write` (accumulating) | Permit new records and refuse destructive rewrites. |
| Op5 | `transition` | Permit declared transitions and refuse undeclared ones. |
| Op6 | `transition` (terminal) | Set terminal timestamp and start retention clock. |
| Op7 | `prune` | Delete only expired transient artifacts. |
| Op8 | `history` (living) | Return git history for a living document. |
| Op9 | `history` (accumulating) | Return on-disk supersession-linked history. |
| Op10 | `history` (transient) | Return recent on-disk history plus git history after pruning. |

## 8. Negative tests

| ID | Scenario | Expected outcome |
|---|---|---|
| N1 | Cross-domain write (e.g. an operations writer modifies `product/technical/specs/foo.md`). | ownership violation |
| N2 | A new top-level domain not declared in `standard/domains.yaml`. | undeclared domain |
| N3 | A terminal transient artifact without a terminal timestamp. | lifecycle failure |
| N4 | An accumulating record manually deleted. | history-preservation violation |
| N5 | Missing contract schema referenced in `domains.yaml`. | fatal contract failure |
| N6 | `prune` attempts to delete a non-transient artifact. | precondition error |
| N7 | `transition` is invoked against a non-transient artifact. | precondition error |
| N8 | A `write` deletes an accumulating record. | history-preservation error |
| N9 | Top-level `.archeia/codebase/` exists in a canonical software repo. | structural failure |
| N10 | A canonical top-level kernel domain is renamed. | structural failure |
| N11 | `product/technical/architecture/c4/` is missing or contains non-living artifacts. | structural failure |

## References

- [`CONFORMANCE.md`](CONFORMANCE.md)
- [`REFERENCE-ALGORITHMS.md`](REFERENCE-ALGORITHMS.md)
- [`KERNEL.md`](KERNEL.md)
- [`SCHEMA.md`](SCHEMA.md)
- [`contracts/`](contracts/)
