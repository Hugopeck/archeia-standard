---
status: draft
target-audience: any project running Archeia validation in CI
blueprint-pin: ">=0.5.0, <1.0.0"
---

# Archeia Enforcement — the mechanical-guardrails companion

`archeia-enforcement` is a companion guardrail pack: linters, CI checks, validators, and hooks that turn the Blueprint's validation rules into mechanical checks.

## Example failure formats

### Schema

```text
[archeia:schema] FAIL .archeia/product/technical/specs/onboarding.md
  → does not satisfy contracts/product.schema.json
  → missing required field: status
  Remediation: add a valid `status` to the frontmatter, then re-run.
```

### Lifecycle

```text
[archeia:lifecycle] FAIL .archeia/operations/execution/tasks/abc-123.md
  → status `done` maps to `past`, but no terminal timestamp present
  Remediation: run `archeia:transition` again or add the required terminal timestamp.
```

### Contract

```text
[archeia:contract] FAIL product -> operations
  → .archeia/product/technical/specs/onboarding.md does not satisfy product.schema.json
  → blocking: operations writers cannot generate execution work from this spec until it conforms
  Remediation: fix the spec frontmatter and required sections before generating execution work.
```

### Evidence

```text
[archeia:evidence] FAIL .archeia/product/technical/architecture/c4/system.json
  → element `auth-service` cites an evidence path that does not exist in tree
  Remediation: regenerate the C4 artifact or update the evidence path to match the current source layout.
```

### Prune

```text
[archeia:prune] BLOCKED .archeia/operations/execution/tasks/old-task.md
  → artifact is eligible to prune but the working tree is dirty
  Remediation: commit or stash the working tree, then re-run prune.
```

## Scope

This companion:

- does **not** define domains or contracts
- does **not** implement standard operations
- does wrap validation and CI behavior around the Blueprint contract

## References

- [`../standard/rules.md`](../standard/rules.md)
- [`../standard/ontology.md`](../standard/ontology.md)
