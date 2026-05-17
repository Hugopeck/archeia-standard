# Archeia Reference Algorithms

Language-agnostic pseudocode for the kernel operations. This document is normative for *behavior* and informative for *implementation*: a conforming implementation MUST produce the same observable result, but MAY use any language, storage wrapper, or agent framework.

The key words **MUST**, **SHOULD**, and **MAY** are interpreted per [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

---

## 1. Kernel Operations

Kernel operations are deterministic repo operations over `.archeia/`. They do not decide what strategy, operations, product, or growth content should say. They only scaffold, validate, write, transition, prune, and read history while enforcing the distribution's declared rules.

```
type Artifact = {
  path: string
  domain: string
  shape: "living" | "accumulating" | "transient"
  frontmatter: map[string -> any]
  body: string
}
```

Every operation has a precondition and a postcondition. If the precondition fails, the operation MUST refuse rather than partially mutate the tree.

---

## 2. `init` — scaffold an `.archeia/` tree

**Precondition.** The implementation operates on an existing project root. A pre-existing `.archeia/` is permitted.

**Postcondition.** The distribution's declared domain directories, standard metadata, required schemas, and scaffolded directory READMEs exist. Running on an already initialized root is a no-op plus validation.

```
function init(root, distribution):
  ensure_directory(root + "/.archeia/")

  for domain in distribution.domains:
    ensure_directory(root + "/.archeia/" + domain.id + "/")

  ensure_file_if_absent(root + "/.archeia/standard/domains.yaml", distribution.domains_yaml)
  ensure_file_if_absent(root + "/.archeia/standard/VERSION", distribution.kernel_version_pin)

  for schema_path, schema_content in distribution.required_schemas:
    ensure_file_if_absent(root + "/.archeia/standard/contracts/" + schema_path, schema_content)

  for readme_path, readme_content in distribution.scaffold_readmes:
    ensure_file_if_absent(root + "/.archeia/" + readme_path, readme_content)

  return validate(root)
```

`init` is deterministic and idempotent.

---

## 3. `validate` — check conformance

**Precondition.** An `.archeia/` directory exists.

**Postcondition.** The implementation returns a structured report of conformance issues, each with a file-path citation and severity.

```
function validate(root):
  issues = []

  if not exists(root + "/.archeia/"):
    return [{severity: "fatal", file: root, msg: "no .archeia/ at project root"}]

  domains_yaml = parse(root + "/.archeia/standard/domains.yaml")
  if domains_yaml == null or len(domains_yaml.domains) < 1:
    issues.append({severity: "fatal", file: "standard/domains.yaml", msg: "missing or empty"})

  version = read(root + "/.archeia/standard/VERSION")
  if not is_valid_semver(version):
    issues.append({severity: "fatal", file: "standard/VERSION", msg: "not a valid semver"})

  for artifact in walk_artifacts(root + "/.archeia/"):
    if not in_declared_domain(artifact, domains_yaml):
      issues.append({severity: "error", file: artifact.path, msg: "outside any declared domain"})
      continue

    if not shape_is_permitted(artifact, domains_yaml):
      issues.append({severity: "error", file: artifact.path, msg: "shape not permitted in domain"})

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

  for artifact in walk_artifacts(root + "/.archeia/"):
    last_writer = git_blame_writer(artifact)
    declared_owner = lookup_owner(artifact.domain, domains_yaml)
    if not is_authorized(last_writer, declared_owner):
      issues.append({severity: "advisory", file: artifact.path, msg: "writer not in declared owner family"})

  return issues
```

`validate` is deterministic.

---

## 4. `write` — create, update, or delete safely

**Precondition.** The requested mutation targets a declared domain and is performed by that domain's owner or an authorized delegate.

**Postcondition.** The artifact tree is changed only if owner, shape, schema, contract, and history-preservation rules pass.

```
function write(mutation):
  assert target_domain_is_declared(mutation.path)
  assert writer_is_authorized(mutation.writer, domain_owner(mutation.path))

  proposed = apply_mutation_in_memory(mutation)
  assert proposed.shape in permitted_shapes(proposed.domain)
  assert validates_against_base_schema(proposed, proposed.shape)

  artifact_schema = lookup_artifact_schema(proposed)
  if artifact_schema:
    assert validates_against(proposed, artifact_schema)

  if proposed.shape == "living":
    allow_create_or_update(proposed)

  if proposed.shape == "accumulating":
    if mutation.kind == "delete":
      reject("accumulating records are never deleted")
    if mutation.kind == "update_existing":
      assert only_schema_declared_metadata_mutations(mutation)
    allow_create_or_metadata_update(proposed)

  if proposed.shape == "transient":
    if mutation.kind == "delete":
      reject("transient deletion goes through prune unless distribution allows direct delete")
    assert status_is_valid(proposed)
    allow_create_or_update(proposed)

  commit(mutation)
```

`write` is deterministic. Latent skills decide *what* to write; `write` decides whether the mutation is allowed.

---

## 5. `transition` — change transient status

**Precondition.** The artifact is transient. The current status and target status are connected by a distribution-declared transition.

**Postcondition.** The artifact has the target status and any required timestamp fields.

```
function transition(path, target_status):
  artifact = Read(path)
  assert artifact.shape == "transient"

  current_status = artifact.frontmatter["status"]
  lifecycle = distribution.lifecycle(artifact.domain, artifact.type)
  assert lifecycle.allows(current_status, target_status)

  patch = {"status": target_status}

  if lifecycle.maps_to_present(target_status) and lifecycle.start_field:
    patch[lifecycle.start_field] = now()

  if lifecycle.maps_to_past(target_status):
    patch[lifecycle.terminal_timestamp_field] = now()

  write(Update(path, frontmatter_patch=patch))
```

`transition` is deterministic. Distribution vocabularies decide whether statuses are called `active`, `running`, `accepted`, `rejected`, `done`, or something else.

---

## 6. `prune` — delete expired transient artifacts

**Precondition (per artifact).** The artifact is transient, maps to past, has a terminal timestamp, and its retention window has elapsed.

**Postcondition.** Eligible artifacts are deleted from disk through a git commit; their history remains in git.

```
function prune(scope = "all transient"):
  for artifact in walk(scope):
    if artifact.shape != "transient":
      continue

    if not maps_to_past(artifact):
      continue

    terminal_time = artifact.frontmatter[terminal_timestamp_field(artifact)]
    retention_days = distribution.retention_window(artifact.domain, artifact.type)

    if now() - terminal_time < retention_days * 86400:
      continue

    Delete(artifact.path)
    commit("prune " + artifact.path)
```

`prune` is deterministic. Implementations MAY batch deletions into one commit if the commit message enumerates every pruned path.

---

## 7. `history` — show artifact history

**Precondition.** The path resolves to an existing artifact or to a known-deleted path with git history.

**Postcondition.** The implementation returns a structured history appropriate to the artifact's shape.

```
function history(path):
  artifact = Read(path) | LastKnown(path)

  if artifact.shape == "living":
    return ReadHistory(path, mode = "git_log")

  if artifact.shape == "accumulating":
    return related_records(
      path,
      relationships = ["supersedes", "superseded_by", "related_to"]
    )

  if artifact.shape == "transient":
    return merge(
      recent_on_disk_records(artifact.domain, artifact.type),
      ReadHistory(path, mode = "git_log")
    )
```

`history` is deterministic. The return shape (timeline, list, diff view) is distribution-defined.

---

## 8. Atomicity, Ordering, and Concurrency

**Atomicity.** Implementations SHOULD make each mutating operation one git commit. Multi-file mutations performed through `write` SHOULD be transactional: either all intended files are changed or none are.

**Ordering.** Operations on the same artifact MUST be serialized. Operations on different artifacts MAY proceed concurrently when ownership rules allow it.

**Concurrency.** Per [Truth #4 of `PRINCIPLES.md`](PRINCIPLES.md), the kernel does not require a multi-writer concurrency model; ownership rules guarantee one writer per domain. Implementations MAY assume single-writer-per-domain and skip locking, OR MAY implement file-level locking for defense in depth.

---

## 9. References

- [`KERNEL.md`](KERNEL.md) §5 — the operation contracts these algorithms implement
- [`CONFORMANCE.md`](CONFORMANCE.md) — the audit checklist
- [`TEST-MATRIX.md`](TEST-MATRIX.md) — the test plan that exercises these algorithms
- [`TEMPORAL_MODEL.md`](TEMPORAL_MODEL.md) — the three lifecycle shapes the operations dispatch on
