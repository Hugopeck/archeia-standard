# Blueprint Bundles (Deferred)

Earlier versions of Archeia used **distribution** for a reusable opinionated bundle on top of the shared ontology: owners, lifecycles, skills, agents, and emphasis rules that could be applied to many projects.

That model made sense when Archeia was a public standard with multiple external adopters shipping their own bundles (for example, Archeia Solo).

## Current model

Archeia Factory now has two forms:

- **Blueprint** — the reusable source architecture in this repo.
- **Instance** — the `.archeia/` operating layer installed into a specific project repo.

`init` creates an Instance from the Blueprint. The Instance manifest (`spec.yaml`) describes that installation directly: domains, owners, lifecycles, tree, schemas, and contracts.

There is no separate distribution layer in the current model.

## Legacy manifest field

Installed manifests may still carry a `distribution` block recording which Blueprint bundle was used to create the Instance. This is lineage metadata, not a live concept in the Factory docs. The field name will be updated in a future schema pass.

## If reusable Blueprint bundles return

If the Factory later needs multiple reusable init recipes (for example, solo vs company-ops), those bundles would live on the Blueprint side. The installed result would still be called an Instance.

Until then, see:

- [`../standard/ontology.md`](../standard/ontology.md) — operational model
- [`../standard/rules.md`](../standard/rules.md) — manifest and validation
- [`../guides/faq.md`](faq.md) — common questions
