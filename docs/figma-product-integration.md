# Figma and the Product Domain

| | |
|---|---|
| **Status** | Research report |
| **Date** | 2026-05-11 |
| **Scope** | How Archeia should integrate Figma into `.archeia/product/` given current Codex, Claude Code, and Figma MCP capabilities. |

## Executive Summary

Figma should be treated as a **live external product/design workspace**, not as a passive artifact that Archeia merely links to. As of May 2026, Figma's MCP server gives coding agents structured access to design context, variables, screenshots, FigJam content, Code Connect mappings, design-system search, write-to-canvas, and code-to-canvas workflows. Figma explicitly supports both Claude Code and Codex as MCP clients.

This changes the right Archeia model:

- `.archeia/product/` should remain the durable, versioned product truth that agents can diff, cite, validate, and plan from.
- Figma should be a first-class external source and sink for product/design work.
- `product/design/*.md` should become a **design contract** that cites Figma nodes, extracted MCP context, Code Connect mappings, and visual QA evidence.
- Archeia should not mirror whole Figma files into git; it should consolidate selected frames, flows, variables, and decisions into small, durable product artifacts.

The product-domain implication is bidirectional:

```text
Figma frame / FigJam / Make / variables
  → Figma MCP or REST extraction
  → product/design/*.md, product/features/*.md, product/requirements/*.md
  → execution/tasks/*.md
  → implementation + visual QA
  → optional code-to-canvas / write-to-canvas update back into Figma
```

## Current Tool Reality

### Figma MCP Is The Primary Agent Interface

Figma now provides a Figma MCP server. The remote server is hosted by Figma at `https://mcp.figma.com/mcp`; the desktop server runs locally through the Figma desktop app. Figma recommends the remote server for most users because it provides the broadest feature set and does not require the desktop app. The desktop server remains useful for selection-based workflows where a designer selects a frame or layer in Figma Desktop and asks an agent to act on it.

The Figma MCP server exposes design context to agentic development tools. Official docs describe workflows for copying a Figma file, frame, or layer URL into an MCP client, or selecting an object in the desktop app, then asking the agent to implement or analyze the design.

### Codex And Claude Code Both Support Figma MCP

Figma's MCP comparison page lists both **Claude Code** and **Codex by OpenAI** as supporting remote and desktop Figma MCP servers. The official OpenAI research surfaced a first-party Figma/Codex workflow: bring Figma Design, Figma Make, and FigJam context into Codex, generate editable Figma designs from code, and implement Figma designs back into code through the Figma MCP server.

OpenAI's current Codex documentation also shows that Codex can connect to MCP servers from the CLI or IDE extension. Separately, OpenAI's Responses API supports remote MCP servers as tools, with explicit approval flows before data is shared with a remote MCP server.

Claude Code supports MCP servers over HTTP/SSE/local process transports, provides `/mcp` management, OAuth authentication for remote servers, MCP prompts as slash commands, and output-size handling for large MCP tool results. Anthropic's docs explicitly use design integration as an example MCP use case.

### Figma MCP Is Structured Context, Not Magic Codegen

Figma's own developer docs are clear that the MCP server is not a one-click "design to perfect code" system. It extracts structured design input and a code starting point; the AI assistant is responsible for adapting that context to the codebase, reusing components, and producing final code.

This matters for Archeia: the right contract is not "Figma is canonical, agent copies it." The right contract is "Figma provides rich design context; Archeia records the product/design contract and execution trace."

### Code Connect Is Load-Bearing

Code Connect maps Figma components to real production components. When MCP processes a frame containing connected components, it can include implementation details such as import statements, component snippets, prop mappings, source paths, and custom instructions.

Without Code Connect, the agent infers from visual/layout metadata. With Code Connect, the agent can use the actual component library. For serious teams, Archeia should treat Code Connect coverage as part of product/design readiness.

### Write-To-Canvas And Code-To-Canvas Make The Loop Bidirectional

Figma's remote MCP server supports `use_figma` for writing native Figma content to the canvas: frames, components, variables, and auto layout. It also supports code-to-canvas workflows such as `generate_figma_design`, which can capture live UI from a browser into editable Figma frames.

This means product/design is no longer a one-way "designer hands off to engineer" path. A coding agent can:

- Read a Figma frame.
- Implement it in the repo.
- Validate the implementation visually.
- Capture the live UI back into Figma for review.
- Potentially update Figma canvas structure directly.

Archeia needs to record the durable decisions and evidence across that loop.

## Recommended Archeia Model

### 1. Keep Figma External, Make References First-Class

Do not store Figma file JSON dumps under `.archeia/product/`. Whole-file mirrors are noisy, large, hard to review, and likely to drift.

Instead, product artifacts should include explicit source references:

```yaml
external_sources:
  - type: figma
    file_url: https://www.figma.com/design/...
    node_id: "123:456"
    mode: remote-mcp
    last_read: 2026-05-11T10:00:00Z
    evidence:
      - get_design_context
      - get_variable_defs
      - get_screenshot
      - get_code_connect_map
```

The canonical product truth remains in `.archeia/product/`, but the artifact can point to live Figma sources and name how those sources were read.

### 2. Treat `product/design/*.md` As Design Contracts

`product/design/*.md` should not be a prose copy of a Figma file. It should be the durable contract between product/design and execution.

Recommended sections:

- **Figma Source** — file URL, node IDs, frame names, version or timestamp, MCP mode.
- **Design Intent** — what the design is trying to accomplish.
- **User Flow** — states, transitions, error cases, empty states.
- **Component Mapping** — production components and Code Connect mappings.
- **Variables And Tokens** — Figma variables/tokens relevant to implementation.
- **Copy And Content Rules** — product copy that engineering must preserve.
- **Responsive Behavior** — breakpoints, resizing, auto-layout assumptions.
- **Accessibility Requirements** — focus order, labels, contrast, keyboard behavior.
- **Implementation Notes** — constraints for execution/codebase.
- **Visual QA Evidence** — screenshots, Playwright diffs, Figma reference nodes.

Example:

```markdown
---
title: Onboarding Flow Design Contract
owner: product-skills
status: current
last_reviewed: 2026-05-11T10:00:00Z
related_feature: FEAT-onboarding
external_sources:
  - type: figma
    file_url: https://www.figma.com/design/abc123/Product
    node_id: "42:900"
    mode: remote-mcp
    last_read: 2026-05-11T10:00:00Z
code_connect:
  coverage: partial
  components:
    - Button
    - TextField
    - OnboardingCard
---

# Figma Source

# Design Intent

# User Flow

# Component Mapping

# Variables And Tokens

# Acceptance Notes

# Visual QA Evidence
```

### 3. Link Feature Specs To Design Contracts

`product/features/*.md` should cite design contracts, not raw Figma links alone:

```yaml
feature_id: FEAT-onboarding
design:
  - product/design/onboarding-flow.md
figma_sources:
  - https://www.figma.com/design/abc123/Product?node-id=42-900
```

Execution tasks should reference the feature and design contract:

```yaml
implements: FEAT-onboarding
design_contract: product/design/onboarding-flow.md
figma_node: "42:900"
```

This gives agents a stable local contract while preserving direct access to Figma context when MCP is available.

### 4. Use Two Integration Paths

Archeia should support both interactive and durable ingestion.

| Path | Tooling | Best For | Writes To |
|---|---|---|---|
| Interactive MCP | Figma remote MCP, desktop MCP, Claude Code, Codex | Design-to-code, visual iteration, selected-frame analysis, code-to-canvas | `product/design/*.md`, `execution/tasks/*.md`, code, optionally Figma |
| Durable API Sync | Figma REST API, Variables API, Dev Resources API, webhooks | Token sync, design index, traceability, audit, stale-link checks | `product/design/*.md`, generated reports, external-source metadata |

Interactive MCP is for agent work. Durable API sync is for validation, indexing, and consistency checks.

### 5. Make Code Connect Readiness A Gate

For UI-heavy features, Archeia should record whether the relevant Figma frames have Code Connect coverage:

```yaml
code_connect:
  coverage: full | partial | none | unknown
  checked_at: 2026-05-11T10:00:00Z
  missing_components:
    - PricingTable
    - PlanCard
```

Recommended rule:

> If a feature depends on Figma design and `code_connect.coverage` is `none` or `unknown`, execution may still proceed, but the task must be flagged as higher-risk and require visual QA.

## Proposed Product Domain Additions

The current product-domain overhaul should be extended with explicit external-source support.

### `product/design/*.md`

Clarify that design docs may be derived from Figma and should carry Figma source references, MCP extraction metadata, Code Connect coverage, and visual QA evidence.

### `product/features/*.md`

Require feature specs to link to design contracts when UI behavior is material.

### `product/requirements/*.md`

Allow requirements/PRDs to cite FigJam boards or Figma Make prototypes as source evidence.

### `product/feedback/*.md`

Allow feedback records to cite Figma comments, FigJam workshops, prototype tests, and usability-session frames.

### Optional New Artifact: `product/sources/*.md`

This is optional. If external-source tracking becomes heavy, add:

```text
product/sources/figma.md
```

as a living index of canonical Figma files, teams, libraries, design-system sources, and MCP setup requirements. For now, this can probably stay inside `product/product.md` or `product/design/*.md` frontmatter.

## Recommended Skill Workflows

### `archeia:sync-figma-design`

Reads a Figma URL through MCP or REST, then updates the matching `product/design/*.md`.

Inputs:

- Figma file/frame/layer URL.
- Related feature ID.
- Optional mode: `remote-mcp`, `desktop-mcp`, or `rest`.

Outputs:

- Updated design contract.
- Extracted variables/tokens.
- Code Connect coverage summary.
- Figma screenshot reference.
- Evidence comments for missing context.

### `archeia:review-figma-for-feature`

Reads a feature spec and linked Figma design, then checks whether the feature is executable.

Checks:

- Feature has acceptance criteria.
- Design contract exists.
- Figma node is reachable.
- Code Connect coverage is known.
- Required states are represented.
- Responsive behavior is specified.
- Accessibility notes exist or are marked insufficient.

### `archeia:figma-to-task`

Reads a feature spec plus design contract, then creates or updates execution tasks.

Rules:

- Tasks cite `feature_id`.
- Tasks cite `design_contract`.
- Tasks include Figma node IDs only as supporting evidence.
- Tasks include visual QA requirements when Figma is source evidence.

### `archeia:code-to-figma-review`

Uses code-to-canvas or screenshots after implementation to create review evidence.

Outputs:

- Figma review frame or link.
- Playwright screenshot/diff evidence.
- Update to `product/design/*.md` visual QA section.
- Optional product decision if implementation diverges from design.

## Risks And Constraints

### Prompt Injection And Untrusted Design Content

Figma content can contain text. Agents reading Figma through MCP should treat design text, comments, and annotations as untrusted input unless they are in an approved product/design source. This is especially important when Figma files include imported community components, pasted screenshots, or external comments.

### Token And Output Size

Large Figma frames can produce too much context. Figma recommends structuring files well and avoiding overly large selections. Archeia skills should prefer specific frame/layer URLs over whole-file ingestion.

### Design System Drift

Without Code Connect and variables, agents may generate UI that looks close but does not use the real component system. Archeia should track Code Connect coverage and token usage as readiness signals.

### External Availability

Figma is SaaS. `.archeia/product/` still needs enough durable local context for agents to understand product intent when Figma is unavailable. Do not make raw Figma access the only source of product truth.

### Permission Boundaries

Write-to-canvas requires stronger permissions than read workflows. Archeia should separate read-only design ingestion from write-back workflows and require explicit user approval for write-to-canvas operations.

## Recommendation

The Figma-specific finding generalizes to any external product source:

> External product tools MAY be live working surfaces for their native medium, but `.archeia/product/` remains the durable product contract. Product artifacts SHOULD cite external sources using `external_sources`, including extraction method, last-read time, source version when available, and source status. Tool-specific context should be consolidated into agent-readable local artifacts before execution depends on it.

For Figma specifically:

> Figma MAY be the live working surface for product/design, but `.archeia/product/` remains the durable product contract. Product artifacts SHOULD cite Figma sources using `external_sources`, and `product/design/*.md` SHOULD consolidate selected Figma context into agent-readable design contracts. Figma MCP is the preferred interactive bridge; Figma REST/API sync is the preferred durable indexing and validation bridge.

Concretely:

- Add `external_sources` frontmatter convention for product artifacts.
- Clarify `product/design/*.md` as a design contract that may be derived from Figma MCP.
- Require feature specs to link to design contracts for UI-bearing features.
- Track Code Connect coverage where Figma is used for implementation.
- Treat Figma MCP output as evidence and context, not final product truth.
- Use visual QA evidence when execution implements Figma-derived UI.

## Sources

- Figma Help Center, "Guide to the Figma MCP server" — https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server
- Figma Help Center, "Compare Figma's remote and desktop MCP servers" — https://help.figma.com/hc/en-us/articles/35281385065751-Figma-MCP-collection-Compare-Figma-s-remote-and-desktop-MCP-servers
- Figma Developer Docs, "Figma MCP Server" — https://developers.figma.com/docs/figma-mcp-server/
- Figma Developer Docs, "What the MCP sends vs. what the agent does" — https://developers.figma.com/docs/figma-mcp-server/mcp-vs-agent/
- Figma Developer Docs, "Code Connect integration" — https://developers.figma.com/docs/figma-mcp-server/code-connect-integration/
- Figma Developer Docs, "Write to canvas" — https://developers.figma.com/docs/figma-mcp-server/write-to-canvas/
- Figma Developer Docs, "Code to canvas" — https://developers.figma.com/docs/figma-mcp-server/code-to-canvas/
- Figma Developer Docs, "Create skills for the Figma MCP server" — https://developers.figma.com/docs/figma-mcp-server/create-skills/
- Anthropic Docs, "Connect Claude Code to tools via MCP" — https://docs.anthropic.com/en/docs/claude-code/mcp
- OpenAI, "OpenAI Codex and Figma launch seamless code-to-design experience" — https://openai.com/index/figma-partnership/
- Figma Help Center, "Codex and Figma: Set up the MCP server" — https://help.figma.com/hc/en-us/articles/39888629089175-Codex-and-Figma-Set-up-the-MCP-server
- OpenAI Developers, "Docs MCP" — https://platform.openai.com/docs/docs-mcp
- OpenAI Developers, "Connectors and MCP servers" — https://platform.openai.com/docs/guides/tools-remote-mcp
- OpenAI Developers, "Codex cloud" — https://platform.openai.com/docs/codex
