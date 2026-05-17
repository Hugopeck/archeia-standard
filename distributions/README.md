# Archeia Distributions

A **distribution** is an opinionated bundle that extends [the Archeia Kernel](../KERNEL.md) for a specific software operating context.

Each distribution declares:

1. its target audience
2. which kernel paths are required, emphasized, or left sparse
3. its owner assignments per domain
4. its status vocabularies and temporal mappings for transient artifacts
5. its retention windows
6. its inherent skill roster
7. its agent roster
8. its ethos and workflow

All distributions share the same thick software kernel from [`KERNEL.md`](../KERNEL.md):

- `strategy/`
- `operations/`
- `product/`
- `growth/`

The reference distribution is [Archeia Solo](https://github.com/Hugopeck/archeia).

## Required distribution artifacts

Every distribution must provide:

- `standard/domains.yaml`
- lifecycle specifications for transient artifacts
- JSON Schemas under `standard/contracts/`
- implementations of the six kernel operations plus the `archivist` agent
- any stricter usage rules over the shared kernel tree

## Example

```yaml
distribution: archeia-solo
version: 1.0.0

domains:
  - id: strategy
    owner: strategy-skills
    shapes: [living, accumulating]
    reads: []
  - id: operations
    owner: operations-skills
    shapes: [living, accumulating, transient]
    reads: [strategy, product]
  - id: product
    owner: product-skills
    shapes: [living, accumulating, transient]
    reads: [strategy, operations, growth]
  - id: growth
    owner: growth-skills
    shapes: [living, accumulating, transient]
    reads: [strategy, operations, product]
```

Typical distributions differ by emphasis and policy, not by replacing the kernel tree. A solo distribution may leave many kernel paths sparse. A startup distribution may strengthen `growth/` and `operations/finance/`. An internal-project distribution may interpret `growth/` primarily as adoption and rollout.

## See also

- [`../KERNEL.md`](../KERNEL.md)
- [`../SCHEMA.md`](../SCHEMA.md)
- [`../TEMPORAL_MODEL.md`](../TEMPORAL_MODEL.md)
