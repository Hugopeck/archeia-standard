# Scripts

This folder contains small deterministic tools for working with the Blueprint and installed `.archeia/` trees.

## `archeia_validate`

`archeia_validate` checks an installed Archeia tree. It expects:

- `.archeia/.system/spec.yaml`
- `.archeia/.system/contracts/`
- the four canonical top-level domains
- required canonical folder READMEs
- valid product and C4 contract artifacts
- valid transient lifecycle status and terminal timestamps

Run it from the repo root:

```sh
scripts/archeia_validate examples
```

The script intentionally avoids non-standard Python dependencies.
