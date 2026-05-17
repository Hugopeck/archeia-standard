# Archeia Software Tree

This document is a **companion explainer** for [`KERNEL.md`](KERNEL.md). It is not a second normative layer.

If you want the normative software contract, read [`KERNEL.md`](KERNEL.md). This file exists to give a shorter, more readable view of the canonical software tree and its migration from the previous 5-domain layout.

## The canonical software domains

Archeia's software kernel uses four top-level domains:

- `strategy/`
- `operations/`
- `product/`
- `growth/`

Within those domains, the kernel also defines the rich canonical subtree, including:

- `strategy/{vision,values,landscape,roadmap,decisions}`
- `operations/{execution,optimization,people,finance,compliance}`
- `product/{strategy,design,technical,execution}`
- `growth/{metrics,channels,experiments}`

The key idea is:

- names stay canonical
- meanings stay canonical
- omission and sparse use are allowed
- broader interpretation is allowed within each path's defined meaning
- arbitrary renaming and unrelated repurposing are not kernel-conforming

## Migration from the previous 5-domain layout

- `business/vision/` → `strategy/vision/`
- `business/culture/` values material → `strategy/values/`
- `business/landscape/` → `strategy/landscape/`
- `business/strategy/` directional roadmap material → `strategy/roadmap/`
- business decision records → `strategy/decisions/`
- `business/people/` → `operations/people/`
- `business/finance/` → `operations/finance/`
- `business/legal/` and compliance material → `operations/compliance/`
- top-level `execution/` → `operations/execution/`
- old `product/roadmap.md` → `product/strategy/roadmap/`
- old `product/requirements/*.md` and `product/features/*.md` → `product/technical/specs/`
- old top-level `codebase/` intelligence → `product/technical/architecture/` and `product/technical/devs/`

## When to read this file

Read this file when you want:

- the short version of the software tree
- the migration mapping
- a simpler companion to the full kernel contract

Read [`KERNEL.md`](KERNEL.md) when you want:

- conformance requirements
- lifecycle expectations
- contract surfaces
- flex rules
- distribution extension rules
