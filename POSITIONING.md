# Positioning — what Archeia adds beyond the SOTA harness corpus

The Archeia Standard does not compete with the harness-engineering work being published by Anthropic, OpenAI, Cursor, and the academic groups working on agentic context engineering. It depends on it. This document pins exactly where Archeia stops being downstream of that corpus and starts contributing something the corpus does not provide.

The reference for "the SOTA harness corpus" is `docs/references/harness-engineering-synthesis.md`, which consolidates six primary sources from October 2025 through April 2026 and extracts twelve shared principles (P1–P12). Read that document first; this one is the diff.

---

## 1. Where Archeia sits in the stack

The synthesis doc names two layers above the model:

- The **harness** — the loop, the tools, the sandbox, the per-model adapters, the context manager. Owned today by Claude Code, Cursor, OpenAI Codex, OpenHands, and bespoke runners.
- The **scaffolding** — the structural files and conventions inside the project the agent works on. Owned today by ad-hoc `CLAUDE.md` / `AGENTS.md` files, `WORKFLOW.md` (Symphony), `SPEC.md` (Symphony), feature-list JSON files (Anthropic's long-running harness), and progress files.

**Archeia is scaffolding, not a harness.** It defines the contract of what lives in `.archeia/`, who owns each part, how artifacts evolve, and how cross-domain dependencies are declared. It runs inside any conformant harness — Claude Code, Cursor, Codex, a bash loop — without modifying the harness itself.

This is the same line `KERNEL.md` §9 already draws ("Archeia is harness-agnostic") and that the Sarah Wooders quote there reinforces. POSITIONING.md exists to make explicit *what scaffolding contribution Archeia adds on top of the SOTA harness corpus*, since most of that corpus blurs the harness/scaffolding boundary.

---

## 2. Where Archeia agrees with SOTA — and absorbs without re-deriving

The kernel was already designed in line with the synthesis doc's twelve principles, even where the principles came from work published after the kernel was drafted. The agreements:

| Principle from synthesis | How Archeia already satisfies it |
|---|---|
| **P3** — Persistent state lives outside the context window | Every artifact in `.archeia/` is durable on disk; the harness's context window reads from and writes to the tree, but the tree is the source of truth. |
| **P4** — Verification must approach perfection | Six JSON Schemas under `contracts/` plus the `archeia:validate` operation. Conformance is checkable, not vibes. (This is the load-bearing contribution `TEST-MATRIX.md` formalizes.) |
| **P5** — Mechanical guardrails beat polite instructions | The schemas + `archeia:validate` + the `archeia-enforcement` distribution flavor turn Archeia rules into CI checks, not prose. |
| **P6** — Context is curated, not stuffed | The five-domain layout *is* the curation policy. An agent doing product work reads `product/`; it does not need to sift through the whole tree. |
| **P7** — Plan before doing | The `business → product → execution` contract chain forces planning to precede execution, mechanically. |
| **P8** — Long sessions degrade — design for shifts, not marathons | Living documents survive sessions; accumulating records survive forever; transient artifacts have explicit retention windows. The shift change is the model. |

These principles are not Archeia's contribution. They are the shared ground.

---

## 3. Where Archeia does not contribute — and explicitly defers

The harness corpus owns several questions Archeia does not. Naming them explicitly prevents scope creep:

- **P1** (the harness ships continuously) — that is the harness vendor's problem, not Archeia's. Archeia versions on the calendar of substrate change, not weekly model behavior.
- **P2** (decouple the model from the environment) — Anthropic's *Managed Agents* brain/hands/session split is a runtime architecture; Archeia neither implements nor mandates it. Archeia just specifies what `.archeia/` looks like; the harness can be a service or a CLI.
- **P9** (per-model fit) — tool format adaptation is a harness concern. Archeia's contracts are in JSON Schema, model-agnostic.
- **P10** (production telemetry) — keep rate, error taxonomies, anomaly alerts are harness instrumentation. Archeia does not specify metrics.
- **P11** (parallelism partitioning + oracles) — Archeia's coordination model is single-writer per domain plus subagent delegation (PRINCIPLES Truth #4). It does not specify how a harness partitions multi-agent coding work; that's a harness pattern.
- **P12** (boring technology) — a stack-selection heuristic, not a substrate spec.

If you are looking for guidance on these six topics, read the synthesis doc and the primary sources it cites. Do not look for them in `KERNEL.md`.

---

## 4. Where Archeia contributes — four claims the SOTA corpus does not make

These four are the differential. Each one is a load-bearing piece of the kernel that has no counterpart in the harness-engineering corpus, and each one answers a question the corpus leaves open.

### 4.1 A grammar for durable state — three lifecycle shapes

The corpus uniformly says: persistent state lives outside the context window. None of the primary sources says *what shape that state takes*.

- Anthropic's *Managed Agents* uses an append-only event log (one shape).
- Anthropic's *Long-Running Harness* uses feature-list JSON + progress file + git history (three artifacts, no taxonomy).
- ACE uses an evolving "playbook" (one shape, structurally undefined).
- Symphony uses a `WORKFLOW.md` plus state in the tracker (split, but not theorized).

Archeia ships a closed taxonomy: every artifact is **living**, **accumulating**, or **transient** (`KERNEL.md` §2.4, `TEMPORAL_MODEL.md`). Each shape has different rules for editing, history, retention, and pruning. The kernel's five operations (`advance`, `complete`, `prune`, `supersede`, `evolve`) are defined per-shape, not generically.

This is a *grammar*. It tells you, for any new artifact, which rules apply. The corpus stops at "store state durably." Archeia tells you which durable state behaves like a wiki page, which behaves like a captain's log, and which behaves like a sticky note that should be thrown away after two weeks.

### 4.2 A repository-level information architecture — five domains

The corpus solves coordination at the *task* layer (Symphony's WORKFLOW.md, Anthropic's two-agent init/coding split) or the *event* layer (Managed Agents' session log). It does not solve it at the *repository* layer.

Archeia's `SCHEMA.md` commits to five canonical domains for software projects: `business/`, `product/`, `codebase/`, `growth/`, `execution/`. Cross-domain reads are declared contracts (JSON Schemas under `contracts/`). Writes are owner-only.

The contribution is not "have folders." Every project has folders. The contribution is the *specific information architecture* — a defensible answer to "where does this artifact go?" that spans the whole company a solo builder is running. Symphony tells you how to coordinate one tracker with one coding agent; Archeia tells you where the customer interview, the ADR, the architecture diagram, the growth experiment, and the open task each go, and how they read from each other.

A solo builder running an AI-agent-maximalist business cannot answer this question by composing harness primitives. They need an architecture. Archeia provides one.

### 4.3 A vocabulary grounded in cognitive science — the ontology

The corpus uses memory-adjacent vocabulary inconsistently. "Context," "memory," "rules," "skills," "playbook," "session," "scaffolding" — each vendor uses these terms differently, and the synthesis doc's Glossary §4 catalogues the variation.

Archeia's `ONTOLOGY.md` grounds the vocabulary in cognitive science. The three lifecycle shapes map onto Tulving's canonical memory taxonomy:

- **Living documents** = semantic memory
- **Accumulating records** = episodic memory
- **Transient artifacts in past state** = prospective memory that has expired

The bridge from Tulving to LLM agents was established by Sumers et al.'s *Cognitive Architectures for Language Agents* (CoALA, arXiv:2309.02427, 2023) at the in-context layer. Archeia extends the same bridge to the in-repo persistent layer (`PRINCIPLES.md` Truth #5).

This is not academic theater. It is the source of the closed taxonomy in §4.1 — three shapes is not arbitrary, it is what Tulving's three memory systems demand once you stop conflating them. It is also why the kernel's `consolidate` operation has an explicit academic name (Müller & Pilzecker 1900; Squire & Alvarez 1995) rather than the misapplied "diarize" the project briefly used and corrected.

The corpus does not provide a vocabulary anchored this way. Archeia does, and that anchoring is what keeps the spec internally consistent as it grows.

### 4.4 A deliberate split between operational state and documentation

OpenAI's harness-engineering post argues for **structured documentation architecture** — design specs, execution plans, architectural maps, all cross-linked, all CI-validated, all in one tree (`docs/`) the agent reads and writes. Documentation IS the substrate. There is no separate hidden tree.

Archeia rejects this for its target audience. The substrate is for *agent coordination state*; documentation is one of the artifact types it carries, but it is not the substrate. Concretely:

- **Operational state** — drafts, vision, ADRs, growth experiments, tasks, retros — lives in `.archeia/`. It has owner rules, lifecycle shapes, retention windows, and contract schemas. It is not meant for human publication.
- **Prose documentation** — architecture explanations, contributor guides, READMEs — lives in `docs/`. It has no Archeia-imposed lifecycle. It is what every existing project already has, and Archeia adoption does not require reorganizing it.
- **Contract artifacts that bridge the two** — for example the C4 JSON files that `product/decisions/` reads from `codebase/` — live in `.archeia/codebase/`. The prose architecture doc that humans read lives in `docs/architecture.md`.

This is a deliberate departure from the OpenAI position. The trade-off is real:

| OpenAI "everything in `docs/`" | Archeia "split substrate from documentation" |
|---|---|
| One tree to maintain | Two trees, but each with a clear purpose |
| Native fit with documentation tooling (MkDocs, Docusaurus) | Documentation tooling untouched; `.archeia/` invisible to it |
| Greenfield-friendly | Brownfield-friendly — adoption does not reorganize existing `docs/` |
| Agents and humans share one surface | Agents have a predictable contract surface; humans have a conventional one |

The OpenAI position works in their context — homogeneous greenfield projects, an engineering organization that can rebuild documentation conventions on demand. Archeia's audience is solo builders and small teams adopting into projects that already have a `docs/`. Telling them "your `docs/` is now Archeia-shaped" is a much heavier lift than "drop an empty `.archeia/` at the root."

This is also what lets Archeia accommodate documentation tooling without owning it. A solo builder can publish `docs/` as a doc site via MkDocs and never expose `.archeia/` to readers. The collaboration substrate stays operational; the publication surface stays human-curated.

### 4.5 An in-repo substrate that runs on git — no service required

The corpus's most elegant coordination architecture (Anthropic's *Managed Agents*) requires a hosted service: an event log accessed via `getEvents()`, sandboxes provisioned via `execute()`, sessions resumable via `wake(sessionId)`. The architecture is correct, and for an organization with infrastructure to run it, ideal.

Archeia targets the case where there is no infrastructure to run it. Solo builders, two-person teams, research labs without a platform group, OSS projects without a host — none of them are going to stand up a managed agent service.

The Archeia substrate is a directory layout plus a set of file conventions. The history layer is git. The audit log is `git log`. The collaboration surface is the editor every contributor already has open. There is no server, no schema registry, no message broker, no auth layer, no operational cost (`PRINCIPLES.md` Truth #3).

The contribution is not "git is good." That is well-known. The contribution is the demonstration that the substrate the corpus designs as a hosted service can be specified entirely in the file system, with the same coordination guarantees, *if* you commit to the constraints in §4.1–4.3 (a closed lifecycle taxonomy, a fixed information architecture, an ownership model that rules out concurrent writes). Archeia is the proof that the constraints are enough.

---

## 5. Summary in one table

| Question the SOTA corpus leaves open | Archeia's answer |
|---|---|
| Durable state should live outside the context — but what shape does it take? | Three lifecycle shapes (living / accumulating / transient), each with explicit rules for edit, history, and retention. |
| Coordination needs an information architecture spanning a whole repo — what is it? | Five domains (business / product / codebase / growth / execution), one owner per domain, cross-domain reads via declared contracts. |
| The vendor vocabularies for "memory," "context," "rules," "skills" disagree — what's the canon? | A taxonomy grounded in Tulving (1972) and CoALA (Sumers et al. 2023), specified in `ONTOLOGY.md`. |
| OpenAI says everything goes in `docs/` — should Archeia agree? | No. Operational state lives in `.archeia/`; prose documentation stays in `docs/`. Splitting the two reduces adoption friction and preserves lifecycle clarity. |
| The most elegant coordination architecture needs a hosted service — what if there isn't one? | A file-system-and-git substrate that meets the same goals without infrastructure, contingent on the constraints above. |

---

## 6. Citation discipline

Every spec change to `KERNEL.md`, `SCHEMA.md`, or the contract schemas should cite either:

- A primary source from the SOTA corpus (via `docs/references/bibliography.md`) that motivates the change, or
- A reasoned departure from the corpus, with the synthesis doc as the index of where the corpus stands.

This is the Observe → Orient → Decide → Act loop described in `docs/references/README.md`. POSITIONING.md is the artifact that names the *Decide* step's standing answer to "what are we contributing." It updates whenever the synthesis doc updates and the answer to that question shifts.

Last calibrated against the synthesis doc dated 2026-05-01.
