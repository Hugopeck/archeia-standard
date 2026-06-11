# AGENTS.md

This file provides guidance for agents when working with code in this repository.

## What This Repo Is

This is the **Archeia Factory Blueprint** — a specification repo (not a runnable application). It defines a structured `.archeia/` knowledge layer that gets installed into project repos. The repo contains the standard definition, JSON schemas, a Python validator, example fixtures, and documentation. There is no build step, no package manager, and no compiled output.

Current version: `0.5.0` (pre-1.0, breaking changes possible).

## Validation (the only runnable tool)

```sh
# Validate the canonical example (should pass with zero errors)
scripts/archeia_validate examples

# Validate a specific invalid fixture (should fail with expected error code)
scripts/archeia_validate examples/invalid/missing-c4-evidence

# Run all invalid fixtures
for f in examples/invalid/*/; do echo "=== $f ==="; scripts/archeia_validate "$f" || true; echo; done
```

The validator is stdlib Python 3 — no pip install needed. It takes a **project root** (directory containing `.archeia/`), not the `.archeia/` folder itself.

## Document Authority Chain

There are three interconnected standard docs. Changes must flow in a specific order:

1. **Model changes** (concepts, domains, shapes, ownership) → edit `docs/standard/ontology.md` first, then mirror to `rules.md` and `spec.md`.
2. **Enforcement changes** (validation, operations) → edit `docs/standard/rules.md` first, then mirror to `spec.md`.
3. **`spec.md`** is a consolidated build contract — it mirrors the other two. Never invent new rules only in `spec.md`.

## Schema Change Protocol

When modifying a JSON schema in `contracts/`:

1. Update the source schema in `contracts/`.
2. Mirror the change in `examples/.archeia/.system/contracts/`.
3. Update affected invalid fixtures under `examples/invalid/`.
4. Mirror enforcement changes in `docs/standard/rules.md` and `docs/standard/spec.md`.

The five source schemas are: `living-doc`, `accumulating-record`, `transient-artifact`, `product`, and `c4`.

## Adding a Validation Rule

1. Add the check to `scripts/archeia_validate` (Python, stdlib only).
2. Create a minimal invalid fixture under `examples/invalid/<violation-name>/` that breaks exactly one rule.
3. Add rows to the fixture matrix in `examples/invalid/README.md` and `examples/README.md`.
4. Update `docs/standard/rules.md` and `docs/standard/spec.md` with the new error code.
5. Verify: the example tree still passes, and the new fixture fails with the expected code.

## Key Concepts

- **`spec.yaml`** is the machine-readable Instance manifest. Despite the `.yaml` extension, the format is **JSON**. It lives at `.archeia/.system/spec.yaml`.
- **Four domains** — `strategy/`, `operations/`, `product/`, `growth/` — are fixed. No directories outside these (plus `.system/`) are allowed under `.archeia/`.
- **Three artifact shapes** — living (edited in place), accumulating (append-only), transient (status flow + retention/pruning).
- **Product delivery contracts** require frontmatter: `title`, `owner` (must be `product-skills`), `status`, `last_reviewed`.
- **C4 evidence** requires every element to have a non-empty `evidence` array pointing to files that actually exist.
- **Transient artifacts** must use statuses declared in `spec.yaml`'s `lifecycles.transient_statuses`. Terminal statuses require a terminal timestamp field.

## Repo Layout

- `contracts/` — source JSON schemas (copied into Instances at `.archeia/.system/contracts/`)
- `docs/standard/` — the authoritative specification: `ontology.md`, `rules.md`, `spec.md`, `overview.md`
- `docs/guides/` — practical guides (FAQ, distributions, enforcement, etc.)
- `docs/research/` — theoretical basis and bibliography (non-canonical, not operational authority)
- `examples/.archeia/` — the canonical valid Instance fixture
- `examples/invalid/` — negative test fixtures, one violation per fixture
- `scripts/archeia_validate` — the only implemented tool (Python 3, stdlib only)
