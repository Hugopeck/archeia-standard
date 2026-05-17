# Migration to 0.4.0

The `0.4.0` revision replaces the prior canonical 5-domain software layout with a 4-domain layout:

- `strategy/`
- `operations/`
- `product/`
- `growth/`

Key path moves:

- `business/vision/` → `strategy/vision/`
- `business/culture/` values material → `strategy/values/`
- `business/landscape/` → `strategy/landscape/`
- `business/strategy/` directional roadmap material → `strategy/roadmap/`
- `business/people/` → `operations/people/`
- `business/finance/` → `operations/finance/`
- `business/legal/` and compliance material → `operations/compliance/`
- top-level `execution/` → `operations/execution/`
- old `product/roadmap.md` → `product/strategy/roadmap/`
- old `product/requirements/*.md` and `product/features/*.md` → `product/technical/specs/`
- old top-level `codebase/model/c4/*.json` → `product/technical/architecture/c4/*.json`

The old canonical layout is non-conforming under `0.4.0`.

This note remains historical. As of `0.5.0`, the rich software tree and flex rules are now defined in `KERNEL.md`, and `SCHEMA.md` is only a companion explainer.
