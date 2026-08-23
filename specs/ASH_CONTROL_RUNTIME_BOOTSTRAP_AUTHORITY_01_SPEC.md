# ASH-CONTROL-RUNTIME-BOOTSTRAP-AUTHORITY-01

## Status

```text
Patch ID: ASH-CONTROL-RUNTIME-BOOTSTRAP-AUTHORITY-01
Role: Rust-native control-plane bootstrap authority
Production authority: false
CF1 authority migration: not included
Training math change: none
Optimizer change: none
Checkpoint change: none
Inference change: none
```

## 1. Authority declaration

```text
Rust-Native Control Runtime Bootstrap /
Independent Control-Plane Crate /
No BaseTrain Dependency /
No Inference Runtime Dependency /
No Burn Dependency /
No WGPU Dependency /

Existing Ash-Core Cargo Evidence Primitive Reuse /
No Competing Cargo Receipt SSOT /

Cargo Metadata Workspace Resolution /
No Repository-Root Equals Workspace-Root Assumption /
Deterministic Path Authority /

Typed Process Execution /
Exit-Status Failure Authority /
Stdout / Stderr Evidence Only /
No Human-Text PASS Authority /

Bootstrap Validation Graph /
Explicit Node Dependency /
Deterministic Node Ordering /
Fail-Closed Execution /

Control Runtime Binary Identity /
Bootstrap Receipt Publication /
Atomic Receipt Commit /
No Partial Receipt Authority /

No CF1 Validator Migration Yet /
No CF1 Receipt Replacement Yet /
No 104-Gate Adoption Yet /
No BaseTrain Build Authority Yet /

No Python Runtime Dependency /
No PowerShell Runtime Dependency /
No PythonExe /
No Shell Semantic Authority /

No Training Math Change /
No Optimizer Change /
No Checkpoint Change /
No Inference Runtime Change /
No Production Route Mutation
```

## 2. Current authority preservation

The existing CF1 PowerShell compile chain remains authoritative for this revision.
The existing Python CF1 validators remain active.
The existing CF1 compile receipt remains active.

CONTROL-01 creates a new independent Rust control-plane executable but does not claim CF1 production authority.

Required bootstrap receipt state:

```text
productionAuthorityClaimed = false
```

## 3. New crate

```text
crates/ash_control_runtime/
```

Initial module surface:

```text
main.rs
lib.rs
bootstrap.rs
workspace.rs
process.rs
validation.rs
receipt.rs
atomic_publish.rs
identity.rs
error.rs
```

The crate must not directly depend on:

```text
base_train
runtime
orchestrator_local
burn
burn-wgpu
wgpu
model_core
lora_train
train_data
```

Utility dependencies and `ash_core` are allowed.

## 4. Control-plane SSOT

```text
ash_core
= shared control contract primitives

ash_control_runtime
= control operation execution authority

base_train
= training execution authority

runtime
= inference execution authority

orchestrator_local
= workflow / audit consumer
```

Contract definition and process execution authority are separate concerns.
`ash_core` may define shared evidence types; actual bootstrap process execution belongs to `ash_control_runtime`.

## 5. Existing ash_core primitive reuse

The repository already contains:

```text
CargoCommandExecutionReceipt
CargoWorkspaceDiscoverySnapshot
CargoCompileDiagnosticEntry
CargoCompileDiagnosticIndex
CargoWorkspaceBuildSmokeReceipt
CargoBuildSmokePolicy
```

CONTROL-01 reuses and, where necessary, backward-compatibly extends the generic command/workspace primitives.
It must not create a competing Cargo command receipt SSOT.

CLOSURE-02-specific smoke policy remains a domain-specific policy and is not promoted wholesale to the new control runtime.

## 6. Workspace authority

Repository root and Cargo workspace root are different concepts.

Forbidden assumption:

```text
workspace_root = repo_root
```

Resolution chain:

```text
repo root
  -> crates/ash_control_runtime/Cargo.toml
  -> cargo metadata --manifest-path ...
  -> workspace_root
  -> target_directory
  -> Cargo.lock
```

A root-level `Cargo.toml` is not required.

## 7. Typed process execution

Commands are represented as structured data:

```rust
ControlCommandSpec {
    id,
    kind,
    program,
    args,
    working_directory,
    timeout_ms,
}
```

No shell command concatenation is authoritative.

Forbidden:

```text
cmd /C cargo ...
powershell -Command cargo ...
```

Cargo is spawned directly.

## 8. Process success authority

Only the process exit status determines process success.

```text
exit code 0     -> process PASS
non-zero        -> process FAIL
timeout         -> process TIMEOUT
```

Stdout and stderr are diagnostic evidence only.

Forbidden:

```text
stdout contains PASS -> success
stderr contains Finished -> success
stderr contains warning -> failure
```

Mandatory negative semantics:

```text
exit 1 + stdout "PASS" -> FAIL
exit 0 + error-looking stderr text -> process PASS
```

## 9. Bootstrap validation graph

Exact bootstrap graph:

```text
B001 ManifestExists
B002 DependencyBoundary
B003 CargoAvailable
B004 MetadataResolution
B005 CargoLockResolution
B006 ControlCargoFmt
B007 ControlCargoCheck
B008 ControlUnitTests
B009 BinaryIdentity
B010 ReceiptPublication
```

This graph is unrelated to the existing CF1 104 structural gates.

Node membership is a typed registry.
Dynamic discovery of validator scripts is forbidden.

## 10. Deterministic graph ordering

Execution ordering is derived from:

```text
explicit dependency edges
+
canonical node ID ordering
```

File-system enumeration order, source registration side effects, and script filename ordering are not authority.

## 11. Fail-closed dependency behavior

If a prerequisite fails, dependent nodes become:

```text
BlockedByDependency
```

They may not be silently marked passed or generically skipped.

Disposition SSOT:

```text
Passed
Failed
BlockedByDependency
```

## 12. Dependency boundary validation

The control crate Cargo manifest is parsed structurally as TOML.
String grep is forbidden as dependency authority.

Target-specific dependency tables are included in the scan.

If any forbidden target/data-plane dependency is present, B002 fails.

## 13. Bootstrap Cargo operations

CONTROL-01 performs only control-runtime self-validation:

```text
cargo --version
cargo metadata
cargo fmt --check
cargo check
cargo test
```

It does not authoritatively build `base_train`.
It does not launch `base_train`.
It does not launch inference runtime.
It does not initialize GPU state.

## 14. Self-build boundary

Bootstrap is invoked only after the control binary exists.

```text
cargo build --manifest-path crates/ash_control_runtime/Cargo.toml
    -> ash_control_runtime bootstrap ...
```

The bootstrap process does not recursively rebuild and replace its own executable.

## 15. Binary identity

The bootstrap process records:

```text
std::env::current_exe()
SHA256(current_exe)
```

This is the identity of the control runtime executing the bootstrap.
It is not yet the authoritative CF1 `base_train` release identity.

## 16. Shared command receipts

Each Cargo operation emits the existing shared:

```text
CargoCommandExecutionReceipt
```

Required invariant for a successful command:

```text
commandExecuted = true
exitCode = 0
status = Passed
```

A non-zero exit may never be represented as `Passed`.

## 17. Logs

Stdout and stderr may be persisted as diagnostics and SHA256-bound in the command receipt.
Their contents are not success authority.

Generated logs and receipts are runtime artifacts and are not baked into the source ZIP.

## 18. Atomic receipt publication

Authoritative bootstrap receipt publication follows:

```text
same-directory temporary file
 -> write
 -> flush
 -> fsync
 -> readback validation
 -> atomic replace/rename
 -> final receipt
```

On Unix, same-filesystem rename is used.
On Windows, replacement uses an OS atomic replace primitive with write-through semantics.

If publication fails before final replacement:

```text
new authoritative receipt = absent
previous last-good receipt = preserved
```

## 19. Failure artifact separation

A failed bootstrap may publish a diagnostic failure report.
That report is not an authoritative PASS receipt.

```text
bootstrap_failure_report.json
!=
ash_control_runtime_bootstrap_receipt.json
```

## 20. Bootstrap receipt

Canonical receipt:

```rust
AshControlRuntimeBootstrapReceipt {
    schema,
    patch_id,
    control_runtime_version,
    repo_root,
    control_manifest_path,
    workspace_discovery_hash,
    validation_graph_hash,
    validation_node_count,
    validation_pass_count,
    validation_failure_count,
    validation_blocked_count,
    validation_nodes,
    command_receipt_hashes,
    control_binary_path,
    control_binary_sha256,
    python_runtime_dependency,
    powershell_runtime_dependency,
    production_authority_claimed,
    all_mandatory_gates_passed,
    receipt_hash,
}
```

## 21. Receipt self-digest

Receipt hashing uses canonical struct serialization with `receipt_hash` cleared before SHA256 calculation.
The persisted receipt must validate its own digest.

Mandatory values:

```text
pythonRuntimeDependency = false
powershellRuntimeDependency = false
productionAuthorityClaimed = false
allMandatoryGatesPassed = true
validationFailureCount = 0
validationBlockedCount = 0
```

## 22. Python retirement boundary

CONTROL-01 requires no Python process to execute the new bootstrap path.

Forbidden runtime invocation:

```text
python
python3
py.exe
*.py
```

Existing Python files elsewhere in the repository do not fail CONTROL-01 because CF1 migration is explicitly deferred.

## 23. PowerShell retirement boundary

CONTROL-01 requires no PowerShell process to execute the new bootstrap path.

Forbidden runtime invocation:

```text
powershell
pwsh
*.ps1
```

Existing CF1 PowerShell remains untouched and authoritative until the later CF1 promotion revision.

## 24. No native command translation layer

The Rust process layer consumes native `std::process::ExitStatus` directly.
No PowerShell `NativeCommandError`, `$LASTEXITCODE` semantic translation, or stderr-object interpretation layer is allowed.

## 25. No source mutation

The control runtime validates and reports.
It does not repair source code.

Forbidden:

```text
fmt failed -> run cargo fmt and modify source
dependency violation -> rewrite Cargo.toml
```

Allowed:

```text
cargo fmt --check
```

## 26. Runtime lifetime

CONTROL-01 is a one-shot process:

```text
start
 -> inspect
 -> validate
 -> publish receipt
 -> exit
```

No daemon, scheduler, IPC service, WebSocket server, or GPU worker is introduced.

## 27. Exit contract

```text
0        = all mandatory bootstrap gates closed
non-zero = bootstrap authority not closed
```

Failure attribution remains typed and is not reduced to a generic PASS/FAIL log search.

## 28. Required test matrix

Minimum tests:

```text
workspace_metadata_resolves_from_manifest
repo_root_is_not_assumed_to_be_workspace_root
base_train_dependency_is_rejected
runtime_dependency_is_rejected
cargo_nonzero_exit_is_failure
stderr_text_does_not_override_exit_zero
validation_dependency_failure_blocks_child
validation_order_is_deterministic
bootstrap_receipt_hash_is_deterministic
partial_receipt_is_not_promoted
existing_receipt_survives_failed_publication
current_exe_sha256_is_nonempty
python_process_is_never_invoked
powershell_process_is_never_invoked
```

## 29. Mandatory static gates

```text
PASS_CONTROL01_NEW_CRATE_EXISTS
PASS_CONTROL01_ASH_CORE_CONTROL_PRIMITIVE_REUSE
PASS_CONTROL01_NO_BASE_TRAIN_DEPENDENCY
PASS_CONTROL01_NO_RUNTIME_DEPENDENCY
PASS_CONTROL01_NO_ORCHESTRATOR_DEPENDENCY
PASS_CONTROL01_NO_BURN_DEPENDENCY
PASS_CONTROL01_NO_WGPU_DEPENDENCY
PASS_CONTROL01_TYPED_COMMAND_EXECUTION
PASS_CONTROL01_EXIT_STATUS_AUTHORITY
PASS_CONTROL01_STDERR_EVIDENCE_ONLY
PASS_CONTROL01_METADATA_WORKSPACE_RESOLUTION
PASS_CONTROL01_NO_ROOT_WORKSPACE_ASSUMPTION
PASS_CONTROL01_TYPED_BOOTSTRAP_GRAPH
PASS_CONTROL01_DETERMINISTIC_GRAPH_ORDER
PASS_CONTROL01_FAIL_CLOSED_DEPENDENCIES
PASS_CONTROL01_CURRENT_EXE_IDENTITY
PASS_CONTROL01_ATOMIC_RECEIPT_PUBLICATION
PASS_CONTROL01_NO_PARTIAL_RECEIPT
PASS_CONTROL01_NO_PYTHON_RUNTIME
PASS_CONTROL01_NO_POWERSHELL_RUNTIME
PASS_CONTROL01_NO_CF1_AUTHORITY_MUTATION
PASS_CONTROL01_NO_TRAINING_MUTATION
PASS_CONTROL01_NO_INFERENCE_MUTATION
```

## 30. ZIP bake policy

Generated runtime manifests, receipts, logs, and artifact directories are not source-bake material.

Required bake policy:

```text
runtime_artifacts_baked_into_zip = false
generated_manifests_baked_into_zip = false
sha256_sidecars_baked_into_zip = false
```

`Cargo.toml` is source code required to build the crate and is not classified as a generated runtime manifest.

This specification is committed to the ASH repository as specification authority; runtime-generated evidence is not committed as source authority by CONTROL-01.

## 31. Explicit non-goals

CONTROL-01 does not include:

```text
CF1 receipt contract extraction
81 Python validator migration
104 CF1 structural gate migration
base_train release build authority
source tree release manifest authority
CF1 shadow parity
CF1 physical promotion
legacy Python deletion
legacy PowerShell deletion
optimizer changes
training changes
checkpoint changes
inference changes
```

## 32. Completion truth

CONTROL-01 is closed only when ASH possesses an independent Rust control-plane executable that can:

```text
resolve its Cargo workspace through cargo metadata,
validate its own dependency boundary,
execute typed Cargo processes,
use exit status as the sole process outcome authority,
replay a deterministic bootstrap validation graph,
identify its own executable by SHA256,
and publish an atomic self-validating bootstrap receipt,
without Python, PowerShell, base_train, inference runtime, Burn, or WGPU authority.
```

It must still truthfully report:

```text
CF1ValidatorMigration = false
CF1CompileAuthorityAdoption = false
CF1ReceiptReplacement = false
CF1StructuralGateAdoption = false
ProductionAuthorityClaimed = false
```

## 33. Next revision

```text
ASH-CONTROL-RUNTIME-CF1-CONTRACT-EXTRACTION-01A
```

01A moves the shared CF1 receipt/contract semantics out of `base_train` implementation ownership and establishes a producer/consumer-neutral contract SSOT before any validator or compile authority migration occurs.
