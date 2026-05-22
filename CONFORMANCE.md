# Archeia Conformance Checklist

This document is the **Definition of Done** for any tool, distribution, or harness that claims to support the Archeia Standard.

## 1. Kernel conformance

A kernel-conforming implementation MUST:

- recognize all nine primitives from [`KERNEL.md`](KERNEL.md)
- uphold all seven invariants
- implement the three lifecycle shapes
- provide the six deterministic kernel operations
- provide the `archivist` agent role
- read domains, ownership, shapes, and contracts from `standard/domains.yaml`
- validate artifacts against base schemas and any applicable contract schemas
- enforce the four canonical top-level software domains
- preserve canonical kernel names and meanings
- permit omission and sparse use where the kernel allows it

## 2. Validation

A conforming `validate` implementation MUST check:

- `.archeia/` exists at the project root
- `standard/domains.yaml` exists and declares at least one domain
- `standard/VERSION` exists and is valid semver
- every artifact under `.archeia/` belongs to a declared domain
- every artifact conforms to its base shape schema
- every artifact conforms to any applicable artifact-type schema
- every cross-domain read is backed by a contract schema
- every transient artifact has a valid status
- every terminal transient artifact has a terminal timestamp
- ownership is respected as an advisory check
- every canonical `.archeia/` folder has a `README.md` scaffold

## 3. Kernel software-tree conformance

A repo claiming kernel conformance MUST additionally satisfy the thick software-kernel contract from [`KERNEL.md`](KERNEL.md):

- exactly the four canonical top-level domains exist under `.archeia/`: `strategy/`, `operations/`, `product/`, `growth/`
- no top-level rename or replacement of those canonical domains occurs
- canonical meanings are respected; arbitrary semantic repurposing is not
- omission and sparse use are allowed where the kernel says they are allowed
- direct `decisions/`, `conventions/`, and `learnings/` subfolders are permitted under canonical domains and subdomains when needed
- wrapper folders do not satisfy the canonical direct-surface convention for `decisions/`, `conventions/`, and `learnings/`
- `optimization/processes/` is canonically owned by `operations/`
- every canonical `.archeia/` folder contains a `README.md` scaffold
- `operations/` contains the canonical kernel subareas `execution/`, `optimization/`, `people/`, `finance/`, and `compliance/`
- `operations/optimization/` contains the canonical kernel subareas `monitoring/`, `processes/`, and `initiatives/`
- `operations/people/` contains `hiring/`, `performance/`, `workplace/`, and `compensation/`
- `operations/finance/` contains `operational/`, `strategic/`, and `compliance/`
- `operations/compliance/` contains `regulatory/`, `data-security/`, `risk/`, and `ethics/`
- `product/` contains the canonical kernel subareas `strategy/`, `design/`, `technical/`, `execution/`
- `growth/` contains the canonical kernel subareas `strategy/`, `marketing/`, `sales/`, `success/`, `execution/`
- `product/technical/architecture/c4/` is the canonical machine-readable architecture surface and contains only living artifacts
- both cross-domain contracts are enforced:
  - product delivery surface → `product/execution/` and `operations/execution/`
  - `product/technical/architecture/c4/` → product feasibility review / operations scoping
- product artifacts that depend on external product sources cite those sources with extraction and freshness metadata
- `docs/` is not required for software conformance and is not inspected by the canonical validator

## 4. Distribution conformance

A repo is distribution-conforming if it is kernel-conforming and also satisfies the stricter usage, workflow, approval, retention, and emphasis rules of its chosen distribution.

## 5. Harness compatibility

A conforming harness MUST:

- flush writes to `.archeia/` to disk before compaction may discard them from in-context state
- retain enough context across compaction for the next turn to know which `.archeia/` paths to re-read
- either complete an in-flight `.archeia/` write or abort it cleanly

## 6. Versioning

A conforming distribution MUST:

- pin a kernel version range in `standard/domains.yaml`
- declare its own distribution version separately from the kernel version
- refuse to process a repo whose pinned kernel version is unsupported

## References

- [`KERNEL.md`](KERNEL.md)
- [`SCHEMA.md`](SCHEMA.md)
- [`REFERENCE-ALGORITHMS.md`](REFERENCE-ALGORITHMS.md)
- [`TEST-MATRIX.md`](TEST-MATRIX.md)
