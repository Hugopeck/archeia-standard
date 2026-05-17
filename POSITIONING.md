# Positioning — what Archeia adds beyond the SOTA harness corpus

The Archeia Standard does not compete with harness engineering. It depends on it. This document pins where Archeia stops being downstream of that corpus and starts contributing its own answer as a **software business OS**.

## 1. Shared ground

Archeia agrees with the modern harness corpus on several core points:

- durable state lives outside the context window
- verification must be mechanical
- mechanical guardrails beat prose
- long sessions degrade, so systems must support shifts rather than marathons

## 2. Archeia's differential

### 2.1 A grammar for durable state

Archeia gives durable artifacts a closed taxonomy: **living**, **accumulating**, and **transient**. That is stricter than the harness corpus, which usually says only that state should persist outside the model context.

### 2.2 A repository-level information architecture

Archeia answers the repository-level question the harness corpus leaves open: where does each artifact go in a software business or software project operating system?

The kernel uses four domains:

- `strategy/`
- `operations/`
- `product/`
- `growth/`

Inside `product/`, the canonical subareas are `strategy/`, `design/`, `technical/`, and `execution/`. Cross-domain reads are declared contract surfaces. Writes are owner-only. The kernel is intentionally thick: path-level distinctions are part of the value, not accidental detail.

### 2.3 A vocabulary grounded in cognitive science

Archeia's ontology grounds artifact shapes in long-running cognitive-science categories rather than ad-hoc vendor terminology.

### 2.4 A split between operational state and documentation

Archeia keeps operational state and AI-maintained repo intelligence in `.archeia/`, while `docs/` remains the human-facing publication surface.

In the current kernel:

- operational state lives in `strategy/`, `operations/`, `product/`, and `growth/`
- machine-readable architecture intelligence lives in `product/technical/architecture/c4/`
- human-facing documentation stays in `docs/`

### 2.5 An in-repo substrate that runs on git

Archeia's coordination substrate is a directory layout plus file conventions backed by git. No service is required.

## 3. Summary table

| Question | Archeia's answer |
|---|---|
| What shape does durable state take? | Three lifecycle shapes with explicit edit/history/retention rules. |
| What is the repo-wide information architecture? | A thick kernel: four canonical domains plus a rich canonical subtree with bounded flexibility. |
| What is the canonical machine-readable architecture surface? | `product/technical/architecture/c4/`. |
| Should `docs/` be the substrate? | No. `.archeia/` is the coordination substrate; `docs/` is publication. |
| Do you need a hosted service? | No. The substrate runs on files plus git. |
