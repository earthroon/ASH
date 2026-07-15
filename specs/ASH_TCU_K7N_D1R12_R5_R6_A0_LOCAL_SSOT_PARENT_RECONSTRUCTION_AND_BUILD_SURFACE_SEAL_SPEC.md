# ASH-TCU-K7N-D1R12-R5-R6-A0

## LOCAL_SSOT_PARENT_RECONSTRUCTION_AND_BUILD_SURFACE_SEAL

## 1. Identity

```text
patch_id=ASH-TCU-K7N-D1R12-R5-R6-A0_LOCAL_SSOT_PARENT_RECONSTRUCTION_AND_BUILD_SURFACE_SEAL
PASS=PASS_ASH_TCU_K7N_D1R12_R5_R6_A0_LOCAL_SSOT_PARENT_RECONSTRUCTION_AND_BUILD_SURFACE_SEAL_CANONICAL_LOCAL_PARENT_BOUND
HOLD=HOLD_ASH_TCU_K7N_D1R12_R5_R6_A0_LOCAL_SSOT_PARENT_RECONSTRUCTION_AND_BUILD_SURFACE_SEAL_PARENT_OR_EXECUTION_SURFACE_NOT_YET_BOUND
FAIL=FAIL_ASH_TCU_K7N_D1R12_R5_R6_A0_LOCAL_SSOT_PARENT_RECONSTRUCTION_AND_BUILD_SURFACE_SEAL_IDENTITY_BUILD_OR_PROTECTED_STATE_INVALID
```

Direct parent:

```text
parent_patch=ASH-TCU-K7N-D1R12-R5-R6_CONDITIONAL_HOLD_RETIREMENT_MUTATION_PLAN
parent_execution_id=d1r12-r5-r6-a3476f3a9c95d01771fe
parent_outcome=conditional_hold_retirement_mutation_plan_sealed
```

Normal next state:

```text
ASH-TCU-K7N-D1R12-R5-R6-A1_CONDITIONAL_HOLD_RETIREMENT_TRANSACTION_APPLY
```

A0 is a non-mutating pre-apply evidence gate. It must not perform any A1 mutation.

## 2. Purpose

A0 seals the exact current local worktree, Git delta, Cargo build surface, R5-R6 parent evidence and portable source identity from which A1 may be implemented.

A0 prevents stale ZIP parenting, partial overlay parenting, missing crate-root exports, unregistered audit binaries, console-only PASS reconstruction, unexecuted cargo claims and silent parent drift.

## 3. Source authority

The user's current local PASS worktree is the highest source authority.

```text
source_class=current_local_pass_worktree
source_precedence_rank=0
```

The user has confirmed that the actual local project root contains:

```text
Cargo.toml
Cargo.lock
```

A transferred archive that omits either file does not prove that the local worktree omits it. Archives are reference or transport artifacts unless explicitly selected and sealed as the parent.

Source precedence:

```text
P0=current local PASS worktree
P1=explicitly selected full local PASS archive
P2=manifest-bound base plus overlay reconstruction
PX=reference-only archive, unbound overlay, historical snapshot or unknown parent
```

A dirty local worktree is allowed, but its staged, unstaged and untracked source delta must be sealed. A0 must not run reset, clean, checkout, restore, stash, rebase, formatting or line-ending normalization.

## 4. Required local inputs

```text
workspace_root=<actual user local ASH root>
r5_r6_artifact_root=<exact R5-R6 execution artifact root>
output_root=<optional A0 artifact root>
```

Required root files:

```text
Cargo.toml
Cargo.lock
```

Required crate surfaces:

```text
crates/model_core/Cargo.toml
crates/model_core/src/lib.rs
crates/orchestrator_local/Cargo.toml
crates/orchestrator_local/src/lib.rs
crates/runtime/Cargo.toml
crates/tokenizer_core/Cargo.toml
crates/burn_webgpu_backend/Cargo.toml
crates/artifact_store/Cargo.toml
```

Presence alone is insufficient. Cargo metadata, workspace membership, path dependencies, required feature, binary target and crate-root exports must resolve.

## 5. R5-R6 parent binding

A0 consumes manifest-bound R5-R6 artifacts. Console output and copied summaries are not substitutes.

Required parent facts:

```text
selected_outcome=conditional_hold_retirement_mutation_plan_sealed
current_route_classification=conditional_hold
successor_classification_resolution_status=resolved_composite_registry_state
successor_classification=healthy
successor_observation_mode=exact_signature_non_authoritative_shadow
successor_output_authority=burn
successor_production_authority=false
combined_persistent_authority_count=0
combined_persistent_effective_weight=0
route_epoch_change_required=true
planned_route_epoch_increment=1
planned_entry_epoch_rebind_count=17
compare_and_swap_contract_complete=true
mutation_transaction_atomic=true
rollback_epoch_policy=monotonic_compensation
rollback_contract_complete=true
route_hold_retirement_mutation_eligible=true
runtime_output_changed=false
```

Required parent artifacts include the local manifest, final seal, hold-retirement apply input, CAS contract, mutation plan, rollback plan, registry transition, protected-state guard, report and verdict. Every artifact path and digest must match the parent manifest.

## 6. Semantic source identity

A0 computes a deterministic semantic source-tree manifest including root Cargo files, Rust sources, WGSL, build-relevant JSON/TOML, build.rs and specs. It excludes `.git`, `target`, A0 output, caches and temporary files.

Each record contains:

```text
normalized_relative_path
raw_byte_length
sha256
```

Rules:

```text
path separator normalized to /
records sorted by normalized UTF-8 path bytes
raw bytes hashed without line-ending normalization
mtime, PID, absolute path and filesystem enumeration order excluded
unsealed symlinks forbidden
```

The semantic tree is recomputed twice and both digests must match.

## 7. Git identity

When `.git` is available, A0 records:

```text
HEAD commit
branch or detached state
status porcelain v2
staged binary diff
unstaged binary diff
untracked source manifest
submodule state
```

Required truth fields:

```text
git_worktree_clean=<actual>
git_local_delta_bound=true
git_combined_local_delta_digest=<actual>
```

A0 must never fabricate a clean worktree.

## 8. R5-R6 implementation surface

Required files:

```text
crates/model_core/src/vocab_atlas_shadow_conditional_hold_retirement_mutation_plan_contract.rs
crates/orchestrator_local/src/ash_tcu_k7n_d1r12_r5_r6_conditional_hold_retirement_mutation_plan_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7n_d1r12_r5_r6_conditional_hold_retirement_mutation_plan.rs
crates/model_core/src/lib.rs
crates/orchestrator_local/Cargo.toml
```

Required binary:

```text
ash_tcu_k7n_d1r12_r5_r6_conditional_hold_retirement_mutation_plan
```

Required feature:

```text
orchestrator_tcu_audit_bins
```

Static string presence is evidence only. Rust compilation is the authority for symbol resolution.

## 9. Rust execution truth

A0 Rust must execute and record receipts for:

```text
rustc -Vv
cargo -V
cargo metadata --locked --format-version 1
cargo check --locked -p model_core
cargo check --locked --manifest-path crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_tcu_k7n_d1r12_r5_r6_conditional_hold_retirement_mutation_plan
cargo check --locked --manifest-path crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_tcu_k7n_d1r12_r5_r6_a0_local_ssot_parent_reconstruction_and_build_surface_seal
```

Each receipt records command, execution truth, exit code and stdout/stderr digests. A command that was not executed cannot be reported as PASS. Old logs may only be reused when their source-tree and Cargo.lock digests exactly match.

## 10. Parent-source binding

Preferred mode:

```text
parent_source_binding_mode=direct_execution_source_digest
```

Fallback mode when R5-R6 lacks a complete source digest:

```text
parent_source_binding_mode=deterministic_r5_r6_replay_equivalence
```

Replay must reuse the canonical R5-R6 contract/report builder and compare selected outcome, successor state, authority state, planned epoch increment, planned entry rebind count, CAS digest, mutation plan digest, rollback digest, apply-input digest and final semantic seal. A second independent R5-R6 decision implementation is forbidden.

## 11. Rust-generated artifacts only

The baked source archive must not contain pre-generated A0 execution artifacts or a fabricated A0 local manifest.

The A0 Rust binary owns generation of:

```text
source_selection
semantic_source_tree_manifest
git_identity
workspace_inventory
r5_r6_implementation_surface
rust_toolchain_receipts
protected_state_guard
a1_parent_descriptor
report
verdict
final_seal
local_manifest
```

The local manifest is generated last from the actual artifact bytes produced by the same Rust execution.

Required immutable root:

```text
artifacts/tensorcube/k7n_d1r12_r5_r6_a0/<execution_id>/
```

No Python, shell script or bake process may pre-claim A0 PASS, synthesize the execution manifest or fabricate runtime receipts.

## 12. Protected-state guard

A0 may read but must not mutate:

```text
health classification
conditional_hold status
active registry bytes
registry epoch
entry applied_route_epoch values
registry digest
route IDs and scope membership
route modes
output and production authority
model assets
tokenizer assets
sampler state
KV state
runtime output state
```

Required post-A0 counters:

```text
health_classification_mutation_count=0
conditional_hold_mutation_count=0
registry_mutation_count=0
route_epoch_change_count=0
registry_entry_epoch_rebind_count=0
route_membership_change_count=0
route_mode_change_count=0
output_authority_change_count=0
production_authority_change_count=0
model_asset_mutation_count=0
tokenizer_asset_mutation_count=0
sampler_state_mutation_count=0
kv_state_mutation_count=0
gpu_dispatch_count=0
runtime_output_change_count=0
```

Any protected-state mutation selects FAIL with exit code 70.

## 13. A1 parent descriptor

A0 generates:

```text
schema=ash_tensorcube_k7n_d1r12_r5_r6_a0_a1_parent_descriptor_v1
source_class
semantic_source_tree_digest
root_cargo_toml_digest
cargo_lock_digest
git_head
git_worktree_clean
git_combined_local_delta_digest
r5_r6_parent_execution_id
r5_r6_local_manifest_digest
r5_r6_final_seal_digest
r5_r6_apply_input_digest
parent_source_binding_mode
workspace_complete
r5_r6_implementation_surface_complete
rust_build_surface_complete
a1_parent_eligible
output_authority=burn
production_authority=false
runtime_output_changed=false
```

A1 must bind the A0 parent digest plus its complete declared source delta. Silent rebasing onto another parent is forbidden.

## 14. Implementation surface

Model contract:

```text
crates/model_core/src/vocab_atlas_shadow_local_ssot_parent_reconstruction_and_build_surface_seal_contract.rs
```

Orchestrator report:

```text
crates/orchestrator_local/src/ash_tcu_k7n_d1r12_r5_r6_a0_local_ssot_parent_reconstruction_and_build_surface_seal_report.rs
```

Executable:

```text
crates/orchestrator_local/src/bin/ash_tcu_k7n_d1r12_r5_r6_a0_local_ssot_parent_reconstruction_and_build_surface_seal.rs
```

Registration:

```text
crates/model_core/src/lib.rs
crates/orchestrator_local/src/lib.rs
crates/orchestrator_local/Cargo.toml
```

No backend or runtime module is added. Existing canonical hash, report, manifest and atomic publication owners must be reused where available.

## 15. Outcomes

PASS:

```text
selected_outcome=canonical_local_parent_and_build_surface_sealed
next_state=ASH-TCU-K7N-D1R12-R5-R6-A1_CONDITIONAL_HOLD_RETIREMENT_TRANSACTION_APPLY
exit_code=0
```

HOLD examples:

```text
workspace_root_not_resolved
local_workspace_required_file_missing
r5_r6_execution_artifact_root_not_resolved
r5_r6_manifest_bound_artifact_missing
rust_toolchain_unavailable
parent_source_binding_not_yet_resolved
```

FAIL examples:

```text
semantic_source_tree_nondeterministic
git_local_delta_binding_invalid
workspace_manifest_invalid
cargo_lock_rejected
model_core_compile_failed
r5_r6_binary_compile_failed
a0_binary_compile_failed
r5_r6_artifact_digest_mismatch
r5_r6_parent_semantic_mismatch
protected_state_violation
undeclared_parent_overlay_detected
```

## 16. Expected PASS

```text
PASS_ASH_TCU_K7N_D1R12_R5_R6_A0_LOCAL_SSOT_PARENT_RECONSTRUCTION_AND_BUILD_SURFACE_SEAL_CANONICAL_LOCAL_PARENT_BOUND
source_class=current_local_pass_worktree
source_precedence_rank=0
local_root_cargo_toml_present=true
local_root_cargo_lock_present=true
semantic_tree_digest_match=true
git_local_delta_bound=true
cargo_lock_accepted=true
cargo_metadata_exit_code=0
model_core_cargo_check_executed=true
model_core_cargo_check_exit_code=0
r5_r6_binary_cargo_check_executed=true
r5_r6_binary_cargo_check_exit_code=0
a0_binary_cargo_check_executed=true
a0_binary_cargo_check_exit_code=0
r5_r6_implementation_surface_complete=true
r5_r6_parent_execution_id=d1r12-r5-r6-a3476f3a9c95d01771fe
parent_source_binding_resolved=true
a1_parent_descriptor_complete=true
a1_parent_eligible=true
protected_state_mutation_count=0
output_authority=burn
production_authority=false
runtime_output_changed=false
selected_outcome=canonical_local_parent_and_build_surface_sealed
next_state=ASH-TCU-K7N-D1R12-R5-R6-A1_CONDITIONAL_HOLD_RETIREMENT_TRANSACTION_APPLY
execution_id=<generated by Rust>
local_manifest=<generated by Rust>
```

## 17. PASS meaning

A0 PASS means the exact current local worktree, Git delta, Cargo build surface and R5-R6 evidence are sealed as the canonical A1 parent. It does not mean that conditional_hold was removed, the registry epoch advanced, entries were rebound, A1 committed, rollback was validated or production authority was granted.

A0 may seal readiness for A1. A0 may never perform A1.
