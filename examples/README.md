# Examples

This folder contains the canonical Archeia example tree and validation fixtures.

## Canonical `.archeia/` Tree

The root `examples/.archeia/` directory is the complete canonical Archeia tree. It includes:

- every canonical folder from the ontology
- installed `.archeia/.system/spec.yaml`
- installed schemas
- README scaffolds in canonical folders
- sample valid artifacts for the main artifact shapes and contracts

Validate it with:

```sh
scripts/archeia_validate examples
```

## Invalid Fixtures

`invalid/` contains focused failure cases for the validator. Each fixture is a root containing its own `.archeia/` tree and should fail with a specific error.

See [`../docs/standard/rules.md`](../docs/standard/rules.md) for the validation rules these examples exercise.
