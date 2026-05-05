# Archeia Reference Algorithms

Language-agnostic pseudocode for the kernel operations. This document is normative for *behavior* — a conforming implementation MUST produce the same observable result — and informative for *implementation* — implementers MAY choose any code, language, or framework that achieves it.

The key words **MUST**, **SHOULD**, and **MAY** are interpreted per [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

---

## 1. CRUD substrate

The five deterministic kernel operations (`advance`, `complete`, `prune`, `supersede`, `evolve`) are CRUD with shape-specific preconditions. The named operations are the teachable surface; CRUD is the implementation reality. `consolidate` is the only operation that is not CRUD — it is the kernel's only latent operation.

The CRUD substrate operates on artifacts identified by path. Every operation has a precondition (which MUST hold or the operation aborts) and a postcondition (which MUST hold after the operation completes).

```
type Artifact = {
  path: string                # e.g., ".archeia/execution/tasks/2026-05-01-foo.md"
  domain: string              # e.g., "execution"
  shape: "living" | "accumulating" | "transient"
  frontmatter: map[string -> any]
  body: string
}

primitive Create(path, frontmatter, body) -> Artifact
primitive Read(path) -> Artifact | NotFound
primitive Update(path, frontmatter_patch, body_patch?) -> Artifact
primitive Delete(path) -> void           # must be a git commit
primitive ReadHistory(path, mode) -> list[Snapshot]   # mode ∈ {git_log, supersession_chain, on_disk_then_git}
```

Every operation below resolves to one or more of these primitives.

---

## 2. `advance` — promote a transient artifact from future to present

**Precondition.** The artifact's shape MUST be `transient`. Its current `status` MUST map to `future` per the distribution's `standard/domains.yaml`. The target status MUST map to `present`.

**Postcondition.** The artifact's status is the target status. Its frontmatter has a `started` timestamp (or distribution-defined equivalent).

```
function advance(path, target_status):
  artifact = Read(path)

  assert artifact.shape == "transient"
  current_status = artifact.frontmatter["status"]
  mapping = distribution.status_temporal_mapping(artifact.domain, artifact.type)
  assert mapping[current_status] == "future"
  assert mapping[target_status] == "present"

  patch = {
    "status": target_status,
    "started": now(),
  }
  Update(path, frontmatter_patch=patch)
```

`advance` is **deterministic**. It MUST NOT invoke a model.

---

## 3. `complete` — promote a transient artifact from present to past

**Precondition.** The artifact's shape MUST be `transient`. Its current `status` MUST map to `present`. The target status MUST map to `past`.

**Postcondition.** The artifact's status is the target status. Its frontmatter has the distribution's terminal-timestamp field set to the current time. The retention clock starts now.

```
function complete(path, target_status):
  artifact = Read(path)

  assert artifact.shape == "transient"
  current_status = artifact.frontmatter["status"]
  mapping = distribution.status_temporal_mapping(artifact.domain, artifact.type)
  assert mapping[current_status] == "present"
  assert mapping[target_status] == "past"

  terminal_field = distribution.terminal_timestamp_field(artifact.domain, artifact.type)
  patch = {
    "status": target_status,
    terminal_field: now(),
  }
  Update(path, frontmatter_patch=patch)
```

`complete` is **deterministic**.

---

## 4. `prune` — delete expired transient artifacts

**Precondition (per artifact).** The artifact's shape MUST be `transient`. Its current `status` MUST map to `past`. The duration since its terminal timestamp MUST exceed the distribution's retention window for that artifact type.

**Postcondition.** The artifact is deleted from disk. The deletion is a git commit; the file remains in history.

```
function prune(scope = "all transient"):
  for artifact in walk(scope):
    if artifact.shape != "transient":
      continue

    mapping = distribution.status_temporal_mapping(artifact.domain, artifact.type)
    if mapping[artifact.frontmatter["status"]] != "past":
      continue

    terminal_field = distribution.terminal_timestamp_field(artifact.domain, artifact.type)
    terminal_time = artifact.frontmatter[terminal_field]
    retention_days = distribution.retention_window(artifact.domain, artifact.type)

    if now() - terminal_time < retention_days * 86400:
      continue

    Delete(artifact.path)        # implementation MUST commit the deletion to git
```

`prune` is **deterministic**. The implementation MAY batch deletions into a single commit, but the commit message SHOULD enumerate every pruned path.

---

## 5. `supersede` — replace one accumulating record with a newer one

**Precondition.** Both records MUST have shape `accumulating`. The old record's `status` MUST be `active`. The new record MUST validate against the same schema as the old.

**Postcondition.** A new record exists with `supersedes: <old_path>` in its frontmatter. The old record's frontmatter has `status: superseded` and `superseded_by: <new_path>`. Both records remain on disk.

```
function supersede(old_path, new_path, new_frontmatter, new_body):
  old = Read(old_path)
  assert old.shape == "accumulating"
  assert old.frontmatter["status"] == "active"

  new_frontmatter["supersedes"] = old_path
  Create(new_path, new_frontmatter, new_body)

  patch = {
    "status": "superseded",
    "superseded_by": new_path,
  }
  Update(old_path, frontmatter_patch=patch)
```

`supersede` is **deterministic**. The Create-then-Update sequence MUST be atomic per the distribution's transaction model: if Update fails, the implementation MUST either roll back the Create or surface the inconsistency for repair. Half-supersession is not a conforming state.

---

## 6. `evolve` — read history of a named concept

**Precondition.** The path MUST resolve to an existing artifact (or to a known-deleted path with git history).

**Postcondition.** The implementation returns a structured history per the artifact's shape.

```
function evolve(path):
  artifact = Read(path) | LastKnown(path)
  shape = artifact.shape

  if shape == "living":
    return ReadHistory(path, mode = "git_log")

  if shape == "accumulating":
    chain = []
    cursor = path
    while cursor != null:
      record = Read(cursor)
      chain.append(record)
      cursor = record.frontmatter.get("supersedes", null)
    return chain                        # ordered newest-first; reverse for chronological

  if shape == "transient":
    on_disk = list_recent_past_state(artifact.domain, artifact.type)
    git_history = ReadHistory(path, mode = "git_log")
    return merge(on_disk, git_history)
```

The return shape (timeline, list, diff view) is distribution-defined. The contract is: "show me how this thing changed over time," using the right mechanism for the artifact's shape. `evolve` is **deterministic**.

---

## 7. `consolidate` — the one latent operation

**Precondition.** Inputs are a set of source artifacts (paths, git refs, or external data sources) and a target artifact path. The target's shape MUST be `living` or `accumulating` (transient artifacts MUST NOT be consolidation targets).

**Postcondition.** The target artifact exists or has been updated. Every substantive claim in the target cites at least one source from the inputs. Claims that cannot be evidenced are flagged in-line with `<!-- INSUFFICIENT EVIDENCE: [description] -->`. If the target is a living document, its `last_verified` frontmatter is now.

```
function consolidate(sources, target_path):
  target = Read(target_path) | new()
  assert target.shape in {"living", "accumulating"}

  source_contents = [Read(s) for s in sources]

  # Latent step: the model synthesizes the target from the sources.
  # This is the only kernel operation that invokes a model.
  draft = model_synthesize(
    sources = source_contents,
    target = target,
    rules = {
      "every_claim_must_cite_a_source": true,
      "flag_unevidenced_claims_inline": true,
      "preserve_idempotence_up_to_paraphrase": true,
    }
  )

  if target.shape == "living":
    draft.frontmatter["last_verified"] = now()

  if target_exists(target_path):
    Update(target_path, frontmatter_patch=draft.frontmatter, body_patch=draft.body)
  else:
    Create(target_path, draft.frontmatter, draft.body)
```

`consolidate` is **latent**. It is the ONLY kernel operation that MUST invoke a model. Distributions SHOULD implement consolidate as multiple specialized skills (e.g., `archeia:write-tech-docs`, `archeia:scan-git`, `archeia:clarify-idea`, `archeia:review-draft`) rather than a single generic skill, because narrow consolidation scopes produce better output and cost less.

The operation is semantically idempotent: two runs of the same consolidation over the same inputs MUST produce semantically equivalent outputs. Exact prose MAY differ (the operation is latent), but the set of claims and citations MUST be the same up to paraphrase.

---

## 8. `archeia:init` — scaffold an `.archeia/` tree

**Precondition.** The implementation operates on an existing project root. A pre-existing `.archeia/` is permitted.

**Postcondition.** The five canonical domain directories exist (for software distributions); `standard/domains.yaml` exists; `standard/VERSION` exists; the kernel base schemas plus the distribution's contract schemas exist under `standard/contracts/`. Running on an already-initialized root is a no-op plus a validation pass.

```
function init(root, distribution):
  ensure_directory(root + "/.archeia/")

  for domain in distribution.domains:
    ensure_directory(root + "/.archeia/" + domain.id + "/")

  if not exists(root + "/.archeia/standard/domains.yaml"):
    write(root + "/.archeia/standard/domains.yaml", distribution.domains_yaml)

  if not exists(root + "/.archeia/standard/VERSION"):
    write(root + "/.archeia/standard/VERSION", distribution.kernel_version_pin)

  for schema_path, schema_content in distribution.required_schemas:
    if not exists(root + "/.archeia/standard/contracts/" + schema_path):
      write(root + "/.archeia/standard/contracts/" + schema_path, schema_content)

  return validate(root)
```

`init` is **deterministic** and **idempotent**.

---

## 9. `archeia:validate` — check kernel and distribution conformance

**Precondition.** An `.archeia/` directory exists.

**Postcondition.** A structured report of conformance issues, each with a file-path citation.

```
function validate(root):
  issues = []

  if not exists(root + "/.archeia/"):
    issues.append({severity: "fatal", file: root, msg: "no .archeia/ at project root"})
    return issues

  domains_yaml = parse(root + "/.archeia/standard/domains.yaml")
  if domains_yaml == null or len(domains_yaml.domains) < 1:
    issues.append({severity: "fatal", file: "standard/domains.yaml", msg: "missing or empty"})

  version = read(root + "/.archeia/standard/VERSION")
  if not is_valid_semver(version):
    issues.append({severity: "fatal", file: "standard/VERSION", msg: "not a valid semver"})

  for artifact in walk(root + "/.archeia/"):
    if not in_declared_domain(artifact, domains_yaml):
      issues.append({severity: "error", file: artifact.path, msg: "outside any declared domain"})

    if artifact.shape == null:
      issues.append({severity: "error", file: artifact.path, msg: "no shape declared"})
      continue

    if not validates_against_base_schema(artifact, artifact.shape):
      issues.append({severity: "error", file: artifact.path, msg: "fails base schema for " + artifact.shape})

    artifact_schema = lookup_artifact_schema(artifact, domains_yaml)
    if artifact_schema and not validates_against(artifact, artifact_schema):
      issues.append({severity: "error", file: artifact.path, msg: "fails " + artifact_schema.name})

  for contract in domains_yaml.contracts:
    for source in walk_matching(contract.from):
      if not validates_against(source, contract.schema):
        issues.append({severity: "error", file: source.path, msg: "fails contract " + contract.name})

  for artifact in walk_transient(root + "/.archeia/"):
    if artifact.frontmatter["status"] not in distribution.status_vocabulary(artifact.type):
      issues.append({severity: "error", file: artifact.path, msg: "invalid status"})

    if maps_to_past(artifact) and not has_terminal_timestamp(artifact):
      issues.append({severity: "error", file: artifact.path, msg: "past status without terminal timestamp"})

  for artifact in walk(root + "/.archeia/"):
    last_writer = git_blame_writer(artifact)
    declared_owner = lookup_owner(artifact.domain, domains_yaml)
    if not is_authorized(last_writer, declared_owner):
      issues.append({severity: "advisory", file: artifact.path, msg: "writer not in declared owner family"})

  return issues
```

`validate` is **deterministic**. Severity levels:

- `fatal` — the repo is not even kernel-shaped; processing MUST stop.
- `error` — a normative MUST is violated; the implementation MUST report it.
- `advisory` — a normative SHOULD is violated, or git blame is ambiguous; the implementation SHOULD report it.

---

## 10. Atomicity, ordering, and concurrency

**Atomicity.** Implementations SHOULD wrap each operation in a transaction whose unit is one git commit. The Create-then-Update inside `supersede` MUST be transactional.

**Ordering.** Operations on the same artifact MUST be serialized. Operations on different artifacts MAY proceed concurrently.

**Concurrency.** Per [Truth #4 of `PRINCIPLES.md`](PRINCIPLES.md), the kernel does not require a multi-writer concurrency model; ownership rules guarantee one writer per domain. Implementations MAY assume single-writer-per-domain and skip locking, OR MAY implement file-level locking for defense in depth.

---

## 11. References

- [`KERNEL.md`](KERNEL.md) §5 — the operation contracts these algorithms implement
- [`CONFORMANCE.md`](CONFORMANCE.md) — the audit checklist
- [`TEST-MATRIX.md`](TEST-MATRIX.md) — the test plan that exercises these algorithms
- [`TEMPORAL_MODEL.md`](TEMPORAL_MODEL.md) — the three lifecycle shapes the operations dispatch on
