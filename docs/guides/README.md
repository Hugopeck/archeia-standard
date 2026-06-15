# Guides — Practical How-Tos

This folder contains supplementary documentation for working with Archeia. Guides answer practical questions, audit honest scope, and show integration patterns.

**Guides do not override operational canon.** When a guide and a standard doc disagree, the standard doc wins:

- Model → [`../standard/ontology.md`](../standard/ontology.md)
- Enforcement → [`../standard/rules.md`](../standard/rules.md)
- Build contract → [`../standard/spec.md`](../standard/spec.md)

## Guide Index

| Guide | Audience | When to read |
|---|---|---|
| [`faq.md`](faq.md) | Anyone new to Archeia | First — common questions in plain language |
| [`memory-vs-knowledge.md`](memory-vs-knowledge.md) | Anyone evaluating scope | Before committing — honest audit of what Archeia solves and defers |
| [`enforcement.md`](enforcement.md) | Projects running validation in CI | When wiring `archeia_validate` into hooks or pipelines (draft) |
| [`figma-product-integration.md`](figma-product-integration.md) | Product/design workflows | When connecting Figma artifacts to the product domain |
| [`distributions.md`](distributions.md) | Standard maintainers | When encountering the legacy "distribution" concept — now deferred |

## Suggested Reading Order

1. **Start with FAQ** — [`faq.md`](faq.md) covers what Archeia is, where to start, and how it relates to wikis, tickets, and memory databases.
2. **Audit scope honestly** — [`memory-vs-knowledge.md`](memory-vs-knowledge.md) evaluates Archeia against four memory competencies. Read this before assuming Archeia replaces harness memory or vector databases.
3. **Read standard canon** — [`../standard/overview.md`](../standard/overview.md) and [`../standard/spec.md`](../standard/spec.md) for the authoritative model.
4. **Integrate as needed** — enforcement, Figma, or other guides when your workflow requires them.

## Relationship to Other Docs

```text
standard/     authoritative — model, rules, spec
guides/       supplementary — how-tos, audits, integrations  ← you are here
research/     theoretical — citations, field signals, OODA Observe leg
```

Guides may reference research (especially [`memory-vs-knowledge.md`](memory-vs-knowledge.md)) but research docs do not override guides or standard docs.

## Contributing a New Guide

New guides should:

- State their audience and scope in the opening paragraphs
- Not invent model changes — propose those in `ontology.md`, not in a guide
- Link back to the relevant standard doc for authoritative definitions
- Live as a single `.md` file in this folder (no subdirectories unless the topic genuinely needs one)
