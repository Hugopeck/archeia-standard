# Blueprint Bundles (Deferred)

Earlier versions of Archeia used **distribution** for a reusable opinionated bundle on top of the shared ontology: owners, lifecycles, skills, agents, and emphasis rules that could be applied to many projects.

That model made sense when Archeia was a public standard with multiple external adopters shipping their own bundles (for example, Archeia Solo).

## Current model

Archeia Factory now has two forms:

- **Blueprint** — the reusable source architecture in this repo.
- **Instance** — the `.archeia/` operating layer installed into a specific project repo.

`init` creates an Instance from the Blueprint. The Instance manifest (`spec.yaml`) describes that installation directly: domains, owners, lifecycles, tree, schemas, and contracts.

There is no separate distribution layer in the current model.

## Instance identity in the manifest

Installed manifests record lineage in `instance_identity`:

```json
"instance_identity": {
  "name": "full-canonical-tree",
  "version": "0.1.0"
}
```

Legacy fields `standard_version` and `distribution` are removed. Validators reject them.

## If reusable Blueprint bundles return

If the Factory later needs multiple reusable init recipes (for example, solo vs company-ops), those bundles would live on the Blueprint side. The installed result would still be called an Instance.

Until then, see:

- [`../standard/ontology.md`](../standard/ontology.md) — operational model
- [`../standard/rules.md`](../standard/rules.md) — manifest and validation
- [`../guides/faq.md`](faq.md) — common questions
