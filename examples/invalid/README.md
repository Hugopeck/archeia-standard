# Invalid Fixtures

This folder is the negative test matrix for `scripts/archeia_validate`. Each subdirectory is a mini project root containing a `.archeia/` tree that is intentionally broken in exactly one way.

## Purpose

Valid fixtures prove the canonical tree passes. Invalid fixtures prove the validator catches specific failures with the right error codes. Together they form a regression suite for Blueprint v0 enforcement.

Run all fixtures from the repo root:

```sh
for f in examples/invalid/*/; do
  echo "=== $f ==="
  scripts/archeia_validate "$f" || true
  echo
done
```

Only `examples/.archeia/` (via `scripts/archeia_validate examples`) should pass with zero errors.

## Fixture Matrix

| Fixture | Violation | Error code(s) | Severity |
|---|---|---|---|
| [`artifact-outside-domain`](artifact-outside-domain/) | `.archeia/research/` directory and `note.md` artifact exist outside the four declared domains | `T002`, `A010` | error |
| [`bad-transient-status`](bad-transient-status/) | Transient task uses status `impossible`, not in the declared lifecycle | `L001` | error |
| [`domains-yaml-without-spec`](domains-yaml-without-spec/) | Legacy `domains.yaml` present; `spec.yaml` missing | `S001`, `S002` | fatal + warning |
| [`missing-c4-evidence`](missing-c4-evidence/) | C4 element has an empty `evidence` array | `C003` | error |
| [`missing-folder-readme`](missing-folder-readme/) | Canonical directory `product/technical/specs/` missing `README.md` | `T011` | error |
| [`missing-terminal-timestamp`](missing-terminal-timestamp/) | Transient task in terminal status without a terminal timestamp field | `L002` | error |

## Convention

Each fixture follows the same structure:

```text
<fixture-name>/
└── .archeia/
    ├── .system/
    │   ├── spec.yaml       # usually present (except domains-yaml-without-spec)
    │   └── contracts/      # installed schemas
    ├── strategy/
    ├── operations/
    ├── product/
    └── growth/
```

- The fixture name describes the violation, not the error code.
- Fixtures should be minimal — break one rule, keep everything else valid.
- Each fixture is self-contained; do not share `.archeia/` trees between fixtures.

## Adding a New Fixture

1. Copy the structure from an existing fixture or from `examples/.archeia/`.
2. Introduce exactly one violation.
3. Run `scripts/archeia_validate examples/invalid/<name>` and confirm the expected error code.
4. Add a row to the matrix in this README and in [`../README.md`](../README.md).
5. If the violation represents a new rule, update [`../../docs/standard/rules.md`](../../docs/standard/rules.md) and the validator in [`../../scripts/archeia_validate`](../../scripts/archeia_validate) first.

## Further Reading

- Full error code reference: [`../../scripts/README.md`](../../scripts/README.md)
- Validation rules: [`../../docs/standard/rules.md`](../../docs/standard/rules.md)
- Valid reference tree: [`../.archeia/`](../.archeia/)
