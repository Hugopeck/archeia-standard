# Contracts

This folder contains the source JSON Schemas for the Archeia Standard.

These schemas define the machine-readable contracts for Archeia artifacts. They are copied into an installed `.archeia/` tree at `.archeia/.system/contracts/`. The installed copies are what validators read when they check Archeia artifacts.

## Files

| Schema | Shape / role | Validator checks |
|---|---|---|
| [`living-doc.schema.json`](living-doc.schema.json) | Base contract for living artifacts (edited in place; git holds history) | Referenced by product schema; frontmatter validation |
| [`accumulating-record.schema.json`](accumulating-record.schema.json) | Base contract for accumulating records (append-only; never pruned) | Schema presence and parse |
| [`transient-artifact.schema.json`](transient-artifact.schema.json) | Base contract for transient artifacts (status flow + retention) | Lifecycle status (`L001`, `L002`) |
| [`product.schema.json`](product.schema.json) | Product delivery surface contract | Product frontmatter (`P001`, `P002`) |
| [`c4.schema.json`](c4.schema.json) | Machine-readable architecture evidence | C4 element and evidence (`C001`–`C004`) |

## Schema Inheritance

Three base shapes cover most artifacts. Two contract surfaces extend the living shape for cross-domain validation:

```text
living-doc.schema.json
├── accumulating-record.schema.json   (separate base; append-only)
├── transient-artifact.schema.json  (separate base; lifecycle)
└── product.schema.json             (extends living-doc via allOf)

c4.schema.json                      (standalone JSON contract)
```

**Living** artifacts correspond to semantic memory — one file per concept, edited in place. **Accumulating** artifacts correspond to episodic memory — decisions, learnings, retros that grow over time. **Transient** artifacts correspond to working/task state — plans, tasks, experiments with status flows and retention windows.

## Contract Surfaces

Two paths are validated as cross-domain contracts (not just shape checks):

### Product delivery (`product.schema.json`)

Applies to markdown artifacts at:

- `product/strategy/roadmap/*.md`
- `product/technical/specs/*.md`
- `product/execution/prds/*.md`

Required frontmatter: `title`, `owner` (must be `product-skills`), `status`, `last_reviewed`.

### Technical evidence (`c4.schema.json`)

Applies to JSON files at:

- `product/technical/architecture/c4/*.json`

Every C4 element must include a non-empty `evidence` array pointing to real files in the repo.

## Installed Reference

The canonical installed copy lives at [`examples/.archeia/.system/contracts/`](../examples/.archeia/.system/contracts/). This is what `scripts/archeia_validate` reads when validating the example tree.

## Versioning

Schema changes follow Standard versioning in [`VERSION`](../VERSION). Pre-1.0, breaking schema changes are still possible. When changing a schema:

1. Update the source file here.
2. Mirror the change in `examples/.archeia/.system/contracts/`.
3. Update any affected fixtures under `examples/invalid/`.
4. Mirror enforcement changes in [`docs/standard/rules.md`](../docs/standard/rules.md) and [`docs/standard/spec.md`](../docs/standard/spec.md).

## Further Reading

- Validation behavior and error codes: [`docs/standard/rules.md`](../docs/standard/rules.md)
- Build contract for implementers: [`docs/standard/spec.md`](../docs/standard/spec.md)
- Model (what shapes and contracts mean): [`docs/standard/ontology.md`](../docs/standard/ontology.md)
