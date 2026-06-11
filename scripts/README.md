# Scripts

This folder contains small deterministic tools for working with the Archeia Blueprint and installed `.archeia/` trees.

These tools use **stdlib Python only** — no pip dependencies. They are designed to run in any project environment without setup.

## `archeia_validate`

`archeia_validate` checks an installed Archeia tree against the rules in [`docs/standard/rules.md`](../docs/standard/rules.md). It is a **contract check**, not a content-quality gate — it verifies structure, schemas, and lifecycle rules, not whether the prose is good.

### Usage

```sh
scripts/archeia_validate <project-root>
```

The argument is a **project root** — a directory containing `.archeia/`, not the `.archeia/` folder itself.

```sh
# Validate the canonical example (should pass)
scripts/archeia_validate examples

# Validate a real project
scripts/archeia_validate /path/to/your/project

# Validate a negative fixture (should fail)
scripts/archeia_validate examples/invalid/missing-c4-evidence
```

### Requirements

- Python 3 (stdlib only)
- `.archeia/.system/spec.yaml` present and parseable
- `.archeia/.system/contracts/` with all five schema files

### What it checks

- `.archeia/` directory exists
- `spec.yaml` manifest exists, parses, and has required fields
- Installed schemas exist and parse as JSON
- Four top-level domains exist: `strategy/`, `operations/`, `product/`, `growth/`
- No directories or artifacts outside declared domains
- Every canonical directory has a `README.md` scaffold
- Product contract artifacts satisfy required frontmatter
- C4 artifacts have elements with non-empty evidence pointing to real files
- Transient artifacts use valid lifecycle statuses
- Terminal transient artifacts have terminal timestamp fields

### Output format

Each issue prints as:

```text
<SEVERITY> <CODE> <path>: <message>
```

Severities: `FATAL`, `ERROR`, `WARNING`.

Exit code: `0` if no fatal or error issues; `1` otherwise.

### Error codes

| Code | Severity | Check |
|---|---|---|
| `A001` | fatal | Missing `.archeia/` directory |
| `A010` | error | Artifact outside a declared domain |
| `S001` | fatal | Missing `.archeia/.system/spec.yaml` |
| `S002` | warning | Deprecated `domains.yaml` present |
| `S003` | error | `spec.yaml` cannot parse as JSON |
| `S004` | error | Legacy manifest fields (`standard_version`, `distribution`) |
| `S005` | error | Missing `archeia_version` |
| `S006` | error | Missing `instance_identity.name` |
| `S010` | error | Missing installed schema file |
| `S011` | error | Installed schema cannot parse |
| `T001` | error | Missing canonical top-level domain |
| `T002` | error | Directory outside declared top-level domains |
| `T010` | error | Missing canonical directory |
| `T011` | error | Missing canonical directory README |
| `P001` | error | Product contract missing required frontmatter field |
| `P002` | error | Product contract owner is not `product-skills` |
| `C001` | error | C4 file cannot parse as JSON |
| `C002` | error | C4 file has no elements |
| `C003` | error | C4 element missing non-empty evidence |
| `C004` | error | C4 evidence path does not exist |
| `L001` | error | Invalid transient lifecycle status |
| `L002` | error | Terminal transient missing terminal timestamp |

See [`examples/invalid/README.md`](../examples/invalid/README.md) for fixtures that exercise each code.

## Planned Tools

The standard defines five more operations not yet implemented as scripts:

| Operation | Purpose |
|---|---|
| `archeia_init` | Install an Instance into a target repo |
| `archeia_write` | Create or update artifacts with precondition checks |
| `archeia_transition` | Move transient artifacts through declared statuses |
| `archeia_prune` | Remove expired transient artifacts |
| `archeia_history` | Show history by artifact shape |

See [`docs/standard/rules.md`](../docs/standard/rules.md) for operation rules.

## Further Reading

- Build contract: [`docs/standard/spec.md`](../docs/standard/spec.md)
- CI integration examples: [`docs/guides/enforcement.md`](../docs/guides/enforcement.md)
- Valid and invalid fixtures: [`examples/README.md`](../examples/README.md)
