# ASH-BURN-CUBECL-WGPU26-VENDOR-FORK-R2-PARENT-ARCHIVE-AND-SOURCE-TREE-PROVENANCE-FREEZE-P0

## 0. Revision

```text
Patch ID:
ASH-BURN-CUBECL-WGPU26
-VENDOR-FORK-R2-PARENT-ARCHIVE
-AND-SOURCE-TREE-PROVENANCE-FREEZE-P0

Short name:
ASH WGPU26 R2 P0
CURRENT R2 PARENT FREEZE

Status:
CODE BAKE STATIC PASS

Rust compile PASS:            NOT CLAIMED
Cargo metadata PASS:          NOT CLAIMED
Type-equality compile PASS:   NOT CLAIMED
GPU physical PASS:            NOT CLAIMED
Runtime numerical PASS:       NOT CLAIMED
```

Static token:

```text
PASS_ASH_BURN_CUBECL_WGPU26_VENDOR_FORK_R2_PARENT_ARCHIVE_AND_SOURCE_TREE_PROVENANCE_FREEZE_P0_STATIC
```

Inherited compile hold:

```text
HOLD_ASH_BURN_CUBECL_WGPU26_R2_COMPILE_PENDING
```

Direct semantic parent:

```text
ASH-BURN-CUBECL-WGPU26
-VENDOR-FORK-CANONICAL-STORAGE
-AND-RESOURCE-ABI-R2
```

## 1. Purpose

P0 freezes the supplied full-source-activated R2 parent before compile qualification begins.

The freeze binds:

```text
exact transport archive bytes
exact extracted parent source-tree bytes
exact Cargo authority surface
exact CubeCL vendor provenance
exact R1 / R1A / R2 validator baselines
exact two-file P0 tooling delta
```

P0 is not a runtime revision and does not change Rust, WGSL, Cargo dependency authority, CubeCL storage semantics, Burn semantics, Device/Queue ownership, or GPU execution.

## 2. Code-only artifact law

The P0 code archive is intentionally code-only.

The code archive contains only:

```text
R2 parent files: 8,398
P0 tool additions: 2
--------------------------------
Total ZIP entries: 8,400
```

Added files:

```text
tools/freeze_ash_burn_cubecl_wgpu26_vendor_fork_r2_parent_p0.py
tools/validate_ash_burn_cubecl_wgpu26_vendor_fork_r2_parent_freeze_p0_static.py
```

The following are explicitly excluded from the code ZIP:

```text
P0 Markdown specification
parent tree manifest
validator baseline artifact
next-allowed-patch matrix artifact
parent-freeze receipt artifact
```

P0 evidence is generated into an external `--evidence-dir` and is never embedded into the code-only archive.

This is a deliberate successor rule to the earlier six-file materialization sketch. The code bake owns two tooling files only; all evidence files are external artifacts.

## 3. Parent archive identity

Canonical logical artifact name:

```text
ASH_PASS3_BURN_CUBECL_WGPU26_VENDOR_FORK_R2_FULL_SOURCE_CODE_ONLY.zip
```

Observed transport duplicate suffixes such as `(1)` are non-authoritative.

Frozen parent archive identity:

```text
SHA-256:
5370923f1bd249016c72b4113596ff7ec1e2115a9649f58cefc4894aa899fb4b

archive bytes:
21,394,025

ZIP entry count:
8,398

regular file entry count:
8,398

directory entry count:
0

uncompressed regular-file bytes:
102,019,518
```

Archive path-safety baseline:

```text
duplicate paths:         0
case-fold collisions:    0
symbolic links:          0
path traversal entries:  0
absolute path entries:   0
```

## 4. Parent source-tree identity

Tree digest domain:

```text
ASH_R2_PARENT_TREE_V1\0
```

For each regular file sorted by exact UTF-8 relative POSIX path bytes:

```text
u32_le(path_byte_length)
path_utf8_bytes
u64_le(file_byte_length)
sha256(file_bytes).raw_32_bytes
```

No source normalization is permitted.

Excluded from semantic tree identity:

```text
mtime
ctime
compression method
ZIP entry order
absolute extraction path
owner/group
host filesystem permissions
```

Included exactly as bytes:

```text
line endings
BOMs
trailing whitespace
binary files
Cargo files
Rust/WGSL/source assets
```

Frozen parent tree:

```text
file count:
8,398

total file bytes:
102,019,518

source-tree digest:
795fadb558dfdf9c6f72fc14f05367513bca7f90b6fda3bc98e244233c6a9d43
```

The digest was reproduced independently from the source ZIP and the extracted parent tree.

## 5. Critical subtree identity

The subtree digest domain is:

```text
ASH_R2_SUBTREE_V1\0
```

Frozen subtrees:

```text
crates/ash_wgpu26_api
files = 2
bytes = 2,948
digest = 523182760314b4cd0c8bbdc8065d59d3b95532a5590fe30992410e98d8b8d750

crates/ash_wgpu26_storage_interop
files = 4
bytes = 19,690
digest = c7ef14334ff85c50128e1a5789a554ea819a01daa3d9b5caf39aaf7e78d931dc

vendor_fork_scaffold/cubecl-wgpu-ash
files = 37
bytes = 295,825
digest = b9659bb03909f74d129ed455072740fb33911cc2dee07fbc64f24248ed7a7caf

vendor_fork_scaffold/cubecl-wgpu-ash-overlay
files = 2
bytes = 12,013
digest = d242d4eb2d596a0ce28ba4d5f3ffec786008b8f83348c12aac37b3541874f0ac

vendor_fork_scaffold/upstream_real_insert
files = 5
bytes = 18,925
digest = cbd481b3607d944ef9c49c94f7da375895e8b14e12ebcd96760c6222987614f4
```

## 6. Cargo authority freeze

Critical root digests:

```text
Cargo.toml
23f9651a598bc9fc99ce243f7f18b3fffe4840eb3095d1ce9732c6e0e27b34ad

Cargo.lock
00b5436550c645a93687554999b60e014cc255d7bb1d794e7c7d426d006e55f6
```

Required root patch:

```toml
[patch.crates-io]
cubecl-wgpu = { path = "vendor_fork_scaffold/cubecl-wgpu-ash" }
```

No second root patch is admitted by P0.

Frozen WGPU authority:

```text
direct ASH upstream wgpu owner count = 1
owner = crates/ash_wgpu26_api/Cargo.toml
upstream package = wgpu
exact version = 26.0.1
resolved wgpu package count = 1
```

Frozen CubeCL WGPU authority:

```text
cubecl-wgpu version = 0.9.0
resolved cubecl-wgpu package count = 1
path instances = 1
registry instances = 0
```

P0 does not execute `cargo metadata` and does not infer metadata PASS from TOML/lock parsing.

## 7. CubeCL fork provenance freeze

Required package provenance:

```text
package = cubecl-wgpu
version = 0.9.0
registry checksum = 29787364632fc7ec6a11cf3d95187f82f6fcce17d6bb4f0fb0dde580b837631d
upstream VCS SHA = 2679028d1c62b9f432e77a0acb952c06481dd7a9
path_in_vcs = crates/cubecl-wgpu
```

The exact published `.cargo_vcs_info.json` shape is sealed as present in the parent. P0 does not require a fabricated `dirty` field.

Staged canonical storage and overlay storage must remain byte-identical:

```text
vendor_fork_scaffold/cubecl-wgpu-ash/src/compute/storage.rs
vendor_fork_scaffold/cubecl-wgpu-ash-overlay/storage.rs

SHA-256:
6a7ca3b2a41c2699f217cb26fae1db0517a0f6c4969f623c1fac89543fc17a70
```

## 8. R2 activation state freeze

Required inherited values:

```text
full_source_present = true
patch_active = true
static_foundation_pass = true
compile_pass_claimed = false
physical_pass_claimed = false
activation_state = ActiveUncompiled
compiler_delta_count = 0
shader_delta_count = 0
```

P0 must preserve:

```text
HOLD_ASH_BURN_CUBECL_WGPU26_R2_COMPILE_PENDING
```

Changing `ActiveUncompiled` to `CompileQualified` is outside P0.

## 9. Vendor deployment-mode observation

P0 records but does not redesign the current deployment modes:

```text
vendor_fork_scaffold/cubecl-wgpu-ash
    PathForkActive

vendor_fork_scaffold/cubecl-wgpu-ash-overlay
    StagingOverlay

vendor_fork_scaffold/burn-wgpu-local
    SidecarExtension

vendor_fork_scaffold/burn-fusion-local
    SidecarExtension

vendor_fork_scaffold/upstream_real_insert
    InactiveEvidenceOnly

vendor_fork_scaffold/activation.local.toml
    DevelopmentActivationConfiguration
```

`upstream_real_insert` is intentionally not repaired or activated by P0.

Physical parent truth:

```text
vendor_fork_scaffold/upstream_real_insert/manifest.json
    absent
```

Historical inventory claims that described the manifest as present remain historical evidence only and are not silently rewritten.

## 10. P0 freeze generator

Tool:

```text
tools/freeze_ash_burn_cubecl_wgpu26_vendor_fork_r2_parent_p0.py
```

Code-bake SHA-256:

```text
fad878e0258963aa87ec55dbca2dacb5cc8ed58e4a6703b5f8a780a8936e2598
```

Required interface:

```text
--parent-archive <exact R2 parent ZIP>
--parent-root <untouched extracted R2 parent>
--workspace <P0 child code workspace>
--evidence-dir <external directory>
[--verify-only]
```

The generator validates the archive, extracted parent, critical surfaces, Cargo authority, vendor modes, R2 activation state, CubeCL provenance, existing static validators, and exact child mutation budget.

No `--force` path exists.

Existing evidence may be accepted only when byte-identical to deterministic regeneration.

## 11. P0 static validator

Tool:

```text
tools/validate_ash_burn_cubecl_wgpu26_vendor_fork_r2_parent_freeze_p0_static.py
```

Code-bake SHA-256:

```text
821a24fa30e4e92e84cf3c1ef17a2c191249f1fc02c15161e5ba987cdd872755
```

The validator regenerates expected external evidence from the exact parent and code workspace, then requires byte equality with the supplied external evidence directory.

It additionally rejects:

```text
embedded P0 evidence files
embedded P0 Markdown spec
undeclared third code addition
parent source mutation
compile claim escalation
physical claim escalation
upstream_real_insert activation
```

Successful terminal state:

```text
PASS_ASH_BURN_CUBECL_WGPU26_VENDOR_FORK_R2_PARENT_ARCHIVE_AND_SOURCE_TREE_PROVENANCE_FREEZE_P0_STATIC
HOLD_ASH_BURN_CUBECL_WGPU26_R2_COMPILE_PENDING
CODE_ONLY_ADDITIONS=2
EMBEDDED_EVIDENCE=0
EMBEDDED_P0_SPEC=0
```

## 12. Static validator baseline seal

P0 re-executes the inherited validators with `PYTHONDONTWRITEBYTECODE=1` so validation does not mutate the source tree.

Frozen baselines:

```text
R1
84 / 84 PASS
script SHA-256 = 0a46b5e3ef13e6f1f562023e5fa99e968fecb3a18bc82329ffc13d1d94aeb849
stdout SHA-256 = b4d7953385ba5e568d6ca51b6a4a876127293c761c8f8d3d127ce73128f3fd86

R1A
108 / 108 PASS
script SHA-256 = 84f63b4c54a01fd046718f158e5e2d9f57d5c0c0de328a325810eb4ebb531418
stdout SHA-256 = 774582395b2091996c0adeddb7837edc40ab841bcf3239bd115fa9151e061c31

R2
117 / 117 PASS
script SHA-256 = c8989f532f8b1992e33deb9b93167886172e1f43e4e75d52c0d79c982af3c772
stdout SHA-256 = 6129d0360d97db6f5fcf909ed6999d548dccf9cde457147220edbb4a2f4ed358
```

A validator source digest drift or normalized stdout digest drift is a parent drift even if a changed validator still prints PASS.

## 13. External evidence artifacts

The bake generated the following deterministic files outside the code ZIP:

```text
ASH_BURN_CUBECL_WGPU26_R2_PARENT_TREE_MANIFEST.jsonl
SHA-256 = 21bc63b1e0d0b18598bc949c0ce0b489d1b281f3823529be505782f363945252

ASH_BURN_CUBECL_WGPU26_R2_PARENT_VALIDATOR_BASELINE.json
SHA-256 = 4233e5208bf143ef8a9f4652409c2781c9fda24232c9dc21f664d29f2fa42110

ASH_BURN_CUBECL_WGPU26_R2_NEXT_ALLOWED_PATCH_MATRIX.json
SHA-256 = 3a0e585e969e319d848133a0fc37e3381b654c90f24cedecbf3d3cbb99cfb2e8

ASH_BURN_CUBECL_WGPU26_R2_PARENT_FREEZE.json
SHA-256 = fc580c26b72b522aa2914ff99416568826808d648815966ba0c7ae0e88cbb9b1
```

Two independent clean evidence-generation runs produced byte-identical output for all four files.

## 14. Code-bake artifact identity

Code-only archive:

```text
ASH_PASS3_BURN_CUBECL_WGPU26_VENDOR_FORK_R2_PARENT_FREEZE_P0_CODE_ONLY.zip
```

Identity:

```text
SHA-256:
9de7b67b1b0afd418108607653ea7196bfb13527c08ff95bb8b9521886daabab

archive bytes:
21,405,539

entry count:
8,400

unique entry count:
8,400

Markdown entry count:
0

specs/ entry count:
0

embedded P0 evidence files:
0
```

The code-only ZIP was independently rebuilt twice with identical bytes and identical SHA-256.

The final ZIP was then extracted and the P0 validator re-run against the external evidence. It passed.

## 15. Exact mutation budget

Parent mutation:

```text
modified parent files = 0
deleted parent files = 0
renamed parent files = 0
undeclared additions = 0
```

P0 additions:

```text
2
```

Only the two P0 tooling files are allowed.

No generated manifest, receipt, matrix, Markdown specification, Python bytecode cache, Cargo output, or temporary file belongs to the code archive.

## 16. Fail-closed boundary

Representative stable errors include:

```text
E_P0_PARENT_ARCHIVE_MISSING
E_P0_PARENT_ARCHIVE_SHA256_MISMATCH
E_P0_PARENT_ARCHIVE_SIZE_MISMATCH
E_P0_ZIP_DUPLICATE_PATH
E_P0_ZIP_CASE_COLLISION
E_P0_ZIP_SYMBOLIC_LINK
E_P0_ZIP_PATH_TRAVERSAL
E_P0_ZIP_ABSOLUTE_PATH
E_P0_ARCHIVE_ROOT_PATH_SET_MISMATCH
E_P0_ARCHIVE_ROOT_FILE_SIZE_MISMATCH
E_P0_ARCHIVE_ROOT_FILE_DIGEST_MISMATCH
E_P0_PARENT_TREE_DIGEST_MISMATCH
E_P0_PARENT_FILE_MISSING
E_P0_PARENT_FILE_MUTATED
E_P0_UNDECLARED_CHILD_ADDITION
E_P0_CRITICAL_SURFACE_DIGEST_MISMATCH
E_P0_CARGO_AUTHORITY_DRIFT
E_P0_CUBECL_FORK_PROVENANCE_DRIFT
E_P0_STORAGE_OVERLAY_DRIFT
E_P0_VENDOR_MODE_DRIFT
E_P0_UPSTREAM_REAL_INSERT_BECAME_ACTIVE
E_P0_VALIDATOR_SCRIPT_DRIFT
E_P0_VALIDATOR_RESULT_DRIFT
E_P0_VALIDATOR_OUTPUT_DRIFT
E_P0_COMPILE_CLAIM_ESCALATED
E_P0_PHYSICAL_CLAIM_ESCALATED
E_P0_COMPILE_HOLD_MISSING
E_P0_OUTPUT_ALREADY_EXISTS_WITH_DIFFERENT_CONTENT
E_P0_RECEIPT_SEMANTIC_DIGEST_MISMATCH
```

No mismatch is converted into a warning and no alternate parent is selected automatically.

## 17. Forbidden P0 operations

P0 does not perform:

```text
cargo update
cargo generate-lockfile
cargo metadata promotion
cargo check
cargo test
cargo fmt
rustfmt
CubeCL restaging
Burn dependency pinning changes
Burn path-fork activation
upstream_real_insert repair or execution
runtime route cutover
Device/Queue creation
GPU dispatch
buffer materialization
host upload/readback
```

## 18. Acceptance result

The code bake satisfies:

```text
exact parent archive hash reproduced
exact parent tree digest reproduced
archive/root record maps byte-equal
all critical subtree digests reproduced
Cargo authority frozen
one WGPU 26.0.1 resolved package retained
one path cubecl-wgpu 0.9.0 retained
R2 remains ActiveUncompiled
R1 remains 84 / 84
R1A remains 108 / 108
R2 remains 117 / 117
compile HOLD retained
parent mutation count = 0
code-only additions = 2
embedded evidence = 0
embedded P0 specification = 0
external evidence deterministic across two clean runs
final ZIP extraction revalidated successfully
```

Therefore P0 static admission is:

```text
PASS_ASH_BURN_CUBECL_WGPU26_VENDOR_FORK_R2_PARENT_ARCHIVE_AND_SOURCE_TREE_PROVENANCE_FREEZE_P0_STATIC
```

and compile state remains:

```text
HOLD_ASH_BURN_CUBECL_WGPU26_R2_COMPILE_PENDING
```

## 19. Direct successor

The immediate permitted operation is:

```text
ASH-BURN-CUBECL-WGPU26
-VENDOR-FORK-CANONICAL-STORAGE
-AND-RESOURCE-ABI-R2
-FULL-COMPILE-CLOSURE
```

Only after compile closure may the architectural successor proceed:

```text
ASH-BURN-WGPU26
-EXISTING-DEVICE-HANDLE
-AND-RAW-RESOURCE-TYPE-EQUALITY-SEAL-R2A
```

## 20. Explicit non-claims

P0 does not claim:

```text
cargo metadata success
Rust compilation success
type-equality witness compiler acceptance
burn-raw-access-local feature compilation
CubeCL shader compilation
WGSL compilation
existing Device/Queue physical identity
same-device raw-resource execution
read-only alias physical zero-copy
writable alias exact D2D materialization
queue-completion lifecycle correctness
numerical parity
performance improvement
Burn exact dependency requirement pinning
final vendor deployment-mode SSOT
Burn/Fusion source fork
GPU physical qualification
```

## 21. Final law

> The R2 parent is frozen by archive bytes and canonical source-tree bytes, not by filename, timestamp, branch name, or local extraction path.

> P0 adds exactly two fail-closed tooling files to the code artifact and keeps manifests, receipts, matrices, and the specification outside that artifact.

> `cubecl-wgpu-ash` remains the one active CubeCL path fork, Burn local crates remain sidecar extensions, and `upstream_real_insert` remains inactive evidence.

> Compile qualification begins only from this exact `ActiveUncompiled` parent and must preserve the P0 freeze evidence until a new revision explicitly supersedes it.
