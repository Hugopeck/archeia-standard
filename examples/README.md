# Examples

This folder contains the canonical Archeia example tree and validation fixtures. It is the primary way to see what a valid Standard v0 installation looks like and to test the validator against known-good and known-bad cases.

## Layout

```text
examples/
├── .archeia/          # Complete valid Instance (~154 canonical directories)
└── invalid/           # Six negative test fixtures (see invalid/README.md)
```

Each fixture is a **project root** — a directory containing its own `.archeia/` tree. The validator expects a project root, not the `.archeia/` folder directly.

## Canonical `.archeia/` Tree

The `examples/.archeia/` directory is the complete canonical Archeia tree. It includes:

- every canonical folder from the model (~154 directories)
- installed `.archeia/.system/spec.yaml` manifest
- installed schemas under `.archeia/.system/contracts/`
- README instructions in every canonical folder
- sample valid artifacts for the main artifact shapes and contract surfaces

Validate it with:

```sh
scripts/archeia_validate examples
```

This should pass with zero errors.

### What the example demonstrates

- **Four domains** — `strategy/`, `operations/`, `product/`, `growth/`
- **Three shapes** — living docs, accumulating records, transient artifacts with lifecycle
- **Two contract surfaces** — product delivery frontmatter and C4 architecture evidence
- **System metadata** — `VERSION`, `spec.yaml`, and installed contract schemas

See [`../docs/standard/ontology.md`](../docs/standard/ontology.md) for what each path means (`ontology.md`).

## Invalid Fixtures

`invalid/` contains focused failure cases for the validator. Each fixture is a mini project root with its own `.archeia/` tree, broken in exactly one way.

| Fixture | What's broken | Expected error |
|---|---|---|
| [`artifact-outside-domain`](invalid/artifact-outside-domain/) | `.archeia/research/` directory and artifact outside declared domains | `T002`, `A010` |
| [`bad-transient-status`](invalid/bad-transient-status/) | Transient artifact with status `impossible` | `L001` |
| [`domains-yaml-without-spec`](invalid/domains-yaml-without-spec/) | Legacy `domains.yaml` present, `spec.yaml` missing | `S001` (fatal), `S002` (warning) |
| [`missing-c4-evidence`](invalid/missing-c4-evidence/) | C4 element with empty evidence array | `C003` |
| [`missing-folder-readme`](invalid/missing-folder-readme/) | Canonical directory missing its `README.md` | `T011` |
| [`missing-terminal-timestamp`](invalid/missing-terminal-timestamp/) | Terminal transient artifact without terminal timestamp | `L002` |

Run any fixture:

```sh
scripts/archeia_validate examples/invalid/<fixture-name>
```

See [`invalid/README.md`](invalid/README.md) for details on each fixture and how to add new ones.

## Standard vs Instance READMEs

This repo contains two kinds of README:

- **Standard READMEs** — like this file and those in `contracts/`, `docs/`, `scripts/`. They explain the Standard source repo.
- **Instance READMEs** — the ~154 README instruction files inside `examples/.archeia/`. They explain what belongs at each canonical path in an installed tree.

## Further Reading

- Validation rules: [`../docs/standard/rules.md`](../docs/standard/rules.md)
- Build contract: [`../docs/standard/spec.md`](../docs/standard/spec.md)
- Validator and error codes: [`../scripts/README.md`](../scripts/README.md)
- Source schemas: [`../contracts/README.md`](../contracts/README.md)
