---
distribution: archeia-enforcement
status: draft
target-audience: any team running a software-conforming Archeia repo in CI
kernel-pin: ">=0.3.0, <1.0.0"
---

# Archeia Enforcement — the mechanical-guardrails companion

`archeia-enforcement` is not a full distribution in the same sense as Archeia Solo, Archeia Research, or Archeia Studio. It is a **companion distribution-flavor**: a bundle of linters, CI checks, validators, and pre-commit hooks that any other distribution can layer on top of itself to turn the kernel's normative requirements into mechanical guardrails.

It is the operational answer to OpenAI's harness-engineering principle that *"custom linters and structural tests encode rules and inject remediation instructions back into the agent's context on failure"* (see [`docs/references/harness-engineering-synthesis.md`](../docs/references/harness-engineering-synthesis.md) P5). Where the kernel says SHOULD or MUST in prose, this distribution makes the rule fail loudly in CI.

This file is the spec. The implementation lives downstream — distributions adopting it ship the actual linters as scripts, GitHub Actions, pre-commit hooks, or whatever their adopters use.

---

## 1. Why this exists

`KERNEL.md`, `SCHEMA.md`, and `CONFORMANCE.md` define what a conforming repo looks like. `REFERENCE-ALGORITHMS.md` defines how the kernel operations should behave. `TEST-MATRIX.md` defines what a conforming repo must pass. None of them tell an adopter *how to wire those checks into CI such that an agent's mistakes get caught and corrected automatically*.

`archeia-enforcement` answers that. It specifies a set of CI checks every Archeia repo SHOULD run, the format their failure messages SHOULD take so they can be re-fed into an agent's context, and the cadence at which each check SHOULD run.

This is the load-bearing piece for [`POSITIONING.md`](../POSITIONING.md) §4.5 (the in-repo, no-server substrate). Without mechanical enforcement, the kernel's invariants degrade to wishes. With it, the substrate stays honest as a single solo builder ships hundreds of agent runs a week.

---

## 2. The seven enforcement tracks

Every adopter of `archeia-enforcement` SHOULD ship checks across all seven tracks. Each track maps to one or more sections of [`TEST-MATRIX.md`](../TEST-MATRIX.md).

### 2.1 Schema validator

**What:** runs the JSON Schemas in `standard/contracts/` against every artifact in `.archeia/`.

**When:** on every push, on every PR.

**Maps to:** TEST-MATRIX §3 (Schema tests Sc1–Sc5).

**Failure message format:**

```
[archeia:schema] FAIL .archeia/business/drafts/2026-05-01-foo.md
  → does not satisfy contracts/draft.schema.json
  → missing required field: status
  → expected one of: draft, review, advanced, discarded
  Remediation: add `status: draft` to the frontmatter, then re-run.
```

The "Remediation:" line is the load-bearing piece — agents that re-read the CI output use it as a prompt.

### 2.2 Lifecycle checker

**What:** verifies transient artifacts have valid statuses, terminal timestamps where required, and respect retention windows. Identifies artifacts that prune would delete on its next run.

**When:** on every push; on a daily schedule for the prune-eligibility report.

**Maps to:** TEST-MATRIX §5 (Lifecycle tests L1–L12).

**Failure message format:**

```
[archeia:lifecycle] FAIL .archeia/execution/tasks/abc-123.md
  → status `done` maps to `past`, but no terminal timestamp present
  → expected `completed` field per execution domain's terminal_timestamp_field
  Remediation: run `archeia:complete` again, or add `completed: <ISO 8601>` to frontmatter.
```

### 2.3 Cross-domain contract enforcer

**What:** for every contract declared in `standard/domains.yaml`, validates that artifacts matching the `from` glob conform to the contract schema before any reader in the `to` domain consumes them.

**When:** on every push; ideally as a pre-commit hook on the writer's side.

**Maps to:** TEST-MATRIX §4 (Contract tests C1–C7).

**Failure message format:**

```
[archeia:contract] FAIL business → product
  → .archeia/business/drafts/2026-05-01-foo.md does not satisfy draft.schema.json
  → blocking: product writers cannot consume this draft until it conforms
  Remediation: fix the draft frontmatter, OR move this draft out of the review queue (status: discarded).
```

### 2.4 Ownership checker (advisory)

**What:** for every commit that modified a file under `.archeia/`, verifies the writer is in the declared owner family for that domain. Flags anomalies, does not block (advisory).

**When:** on every push, on a weekly digest.

**Maps to:** TEST-MATRIX §6 (Ownership tests O1–O2).

**Failure message format:**

```
[archeia:ownership] WARN .archeia/product/product.md
  → commit abc1234 by `business-skills` modified a file owned by product-skills
  → cross-domain write detected (kernel invariant I4)
  Remediation: revert the offending commit or convert it to a business-domain write that product-skills consumes.
```

### 2.5 Evidence linter

**What:** for every descriptive artifact (codebase domain, ADRs, drafts), checks that substantive claims cite a source and that unevidenced claims are flagged with the `<!-- INSUFFICIENT EVIDENCE: ... -->` marker.

**When:** on every PR that modifies a descriptive artifact; on a weekly schedule for full-tree audit.

**Maps to:** TEST-MATRIX §7 (Evidence tests E1–E5).

**Failure message format:**

```
[archeia:evidence] FAIL .archeia/codebase/architecture/system.json
  → element `auth-service` lists evidence path `src/auth/server.py` which does not exist in tree
  Remediation: regenerate the C4 artifact, OR update the evidence path to match the current source layout.
```

### 2.6 Pruning agent

**What:** runs the `prune` operation on a schedule. Reports which artifacts were deleted and which are pending. Fails loudly if the pruning agent ever needs to skip an artifact (e.g., uncommitted changes block deletion).

**When:** daily.

**Maps to:** TEST-MATRIX §8 Op3.

**Failure message format:**

```
[archeia:prune] BLOCKED .archeia/execution/tasks/old-task.md
  → terminal timestamp 2026-04-01, retention 14 days, eligible to prune
  → cannot delete: uncommitted changes in working tree
  Remediation: commit or stash the working tree, then re-run prune.
```

### 2.7 Operation pre/postcondition checker

**What:** runs the operation tests Op1–Op11 from [`TEST-MATRIX.md`](../TEST-MATRIX.md) §8 against the distribution's actual implementations of the kernel operations. This is a regression test, not a per-push check.

**When:** on every change to any inherent skill; on every release of the distribution.

**Maps to:** TEST-MATRIX §8.

---

## 3. The remediation-message convention

Every check above ends in a `Remediation:` line. This is non-decorative: it is the contract by which a CI failure becomes an agent prompt.

A conforming agent harness that runs these checks SHOULD:

1. Capture the full failure message.
2. Identify the `Remediation:` line.
3. Inject the message into the next agent turn as context.
4. Permit the agent to act on the remediation directly.

The format is loose by design; the only hard rule is that `Remediation:` is on its own line and precedes a single human-readable instruction. Tools MAY parse this line to populate a structured remediation field; tools MAY also pass the whole message verbatim.

This is the OpenAI mechanical-enforcement pattern made explicit. Without the remediation contract, CI failures are just red X's. With it, every failure is a self-correcting loop.

---

## 4. Reference implementations

This distribution is a spec, not code. Suggested implementations:

- **GitHub Actions** workflow files in `.github/workflows/archeia-*.yml`.
- **Pre-commit hooks** via `pre-commit` config in `.pre-commit-config.yaml`.
- **Standalone CLI** that bundles all checks into one binary (e.g., `archeia lint`).
- **Editor integrations** that surface schema violations inline (LSP-style).

Archeia Solo's own enforcement layer is the canonical reference once it ships. Until then, the test fixtures in [`TEST-MATRIX.md`](../TEST-MATRIX.md) §10 are the working contract.

---

## 5. What this distribution does NOT do

- It does **not** implement the kernel operations. It only verifies them.
- It does **not** define new domains, shapes, or contracts. It enforces the ones declared by the parent distribution.
- It does **not** prescribe a CI provider. GitHub Actions, GitLab CI, CircleCI, local pre-commit — all are fine.
- It does **not** replace `archeia:validate`. It wraps it and adds the remediation-message contract plus the schedule conventions.

---

## 6. Adopting `archeia-enforcement`

A distribution adopts this companion by:

1. Declaring it in their `standard/domains.yaml`:
   ```yaml
   companions:
     - archeia-enforcement
   ```
2. Shipping the seven tracks as CI workflows (or equivalent).
3. Configuring failure messages in the format §2 specifies.
4. Documenting in their own README which tracks they implement.

A distribution MAY pick a subset of the seven tracks (e.g., schema + lifecycle + contract only, deferring evidence and ownership). It SHOULD declare the chosen subset explicitly in its README.

---

## 7. References

- [`POSITIONING.md`](../POSITIONING.md) §4.2 — mechanical guardrails as an Archeia agreement with OpenAI's harness-engineering position
- [`docs/references/harness-engineering-synthesis.md`](../docs/references/harness-engineering-synthesis.md) P5 — the principle this distribution operationalizes
- [`CONFORMANCE.md`](../CONFORMANCE.md) — the requirements this distribution checks
- [`TEST-MATRIX.md`](../TEST-MATRIX.md) — the test plan this distribution runs
- [`REFERENCE-ALGORITHMS.md`](../REFERENCE-ALGORITHMS.md) — the operation contracts this distribution verifies
- [`KERNEL.md`](../KERNEL.md) — the normative substrate
