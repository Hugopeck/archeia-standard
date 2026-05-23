# Contracts

This folder contains the source JSON Schemas for the Archeia Standard.

These schemas are copied into a conforming project at `.archeia/.system/contracts/`.
The installed copies are what validators read when they check Archeia artifacts.

## Files

- `living-doc.schema.json`: base contract for living artifacts.
- `accumulating-record.schema.json`: base contract for accumulating records.
- `transient-artifact.schema.json`: base contract for transient artifacts.
- `product.schema.json`: product delivery surface contract.
- `c4.schema.json`: machine-readable architecture evidence contract.

See [`../docs/standard/rules.md`](../docs/standard/rules.md) for validation behavior.
