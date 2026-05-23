# Archeia Rules

Rules describe what tools and conforming repos must enforce. The ontology explains the meaning of the system. This document explains validation, packaging, operations, and test expectations.

## Source And Installed Layout

This repository is the source standard. It keeps prose, schemas, scripts, and fixtures in normal source paths:

```text
contracts/
docs/
examples/
scripts/
VERSION
```

A conforming project installs the standard under `.archeia/.system/`:

```text
.archeia/.system/
├── VERSION
├── spec.yaml
└── contracts/
```

`spec.yaml` is the installed machine-readable standard spec. It replaces the old `domains.yaml` name because it declares more than domains.

Validators may warn when they see `domains.yaml`, but new examples and tools should use `spec.yaml`.

## What `spec.yaml` Declares

`spec.yaml` declares:

- standard version
- distribution name and version
- ontology document reference
- domains and owners
- canonical tree directories
- artifact shapes
- contract surfaces
- lifecycle status mappings
- retention windows
- schema bindings

The example spec is installed in `examples/.archeia/.system/spec.yaml`.

## Conformance Checks

A validator should check:

- `.archeia/` exists.
- `.archeia/.system/spec.yaml` exists and parses.
- installed schemas exist and parse as JSON.
- the four top-level domains exist: `strategy/`, `operations/`, `product/`, and `growth/`.
- artifacts belong to a declared top-level domain.
- canonical directories in the full tree fixture have `README.md` scaffolds.
- product contract artifacts satisfy the product schema.
- C4 artifacts have at least one element, and every element has non-empty evidence.
- transient artifacts use a valid status.
- terminal transient artifacts have a terminal timestamp.

Ownership checks are advisory unless the validator has reliable writer identity from git history.

## Operations

Conforming distributions provide six deterministic operations:

- `init`: install `.archeia/.system/` and scaffold the tree.
- `validate`: return structured conformance issues.
- `write`: create or update artifacts only when ownership, shape, schema, and contract rules pass.
- `transition`: move transient artifacts through declared statuses.
- `prune`: remove expired transient artifacts after their retention window.
- `history`: show history using the right mechanism for the artifact shape.

Tools may implement these operations in any language if the observable behavior is the same.

## Operation Rules

- Failed preconditions should stop the operation before partial writes.
- Living artifacts are edited in place.
- Accumulating records are not deleted; only declared metadata updates are allowed.
- Transient deletion goes through pruning unless a distribution explicitly allows direct deletion.
- Operations on the same artifact should be serialized.
- Multi-file writes should be transactional where possible.

## Test Scenarios

The standard fixtures cover these scenarios:

- full canonical tree passes validation.
- missing C4 evidence fails validation.
- missing folder README fails validation.
- old `domains.yaml` without `spec.yaml` fails validation.
- invalid transient status fails validation.
- terminal transient without terminal timestamp fails validation.
- artifact outside a declared domain fails validation.

## Harness Boundary

The harness is the runtime that loads skills, invokes models, manages context, and writes files. Archeia is the knowledge layer contract.

A harness must flush `.archeia/` writes to disk before it discards in-context state. Losing a pending `.archeia/` write during compaction is a harness bug.
