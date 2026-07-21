# ASH-TCU-REPLACE-02

## TensorCube Replacement Mode SSOT / Immutable Policy Snapshot / Legacy Boolean Derivation Seal

### Strict Legacy Matrix Import / Single Construction Authority / Read-Only Compatibility Projection / Same-State Projection Parity / Direct Boolean Writer Retirement / Parent R2 Semantic Digest Binding / No Runtime Behavior Change / No Replacement Enablement

---

## 0. Patch metadata

- Patch ID: `ASH-TCU-REPLACE-02`
- Parent: `ASH-TCU-REPLACE-01-R2`
- Parent runtime schema: `ash.tcu.replace.01.r2.ownership_audit.runtime_artifact.v1`
- Parent semantic inventory digest: `7cd333f938c4908e52e3ddf9fcd8e41d7c518bd6dbdd5a5be72fe1e0fca52f9d`
- Parent route replacement allowlist digest: `6ec309aa7fb71f1ce0c96747ed50b9528c531eb8a9183499cb5532a8199c6375`
- Parent readiness requirement: `repository_ready_for_replace_02=true`
- Policy schema: `ash.tcu.replace.02.policy_snapshot.v1`
- Audit schema: `ash.tcu.replace.02.policy_snapshot_audit.runtime_artifact.v1`
- Local manifest: `artifacts/ASH_TCU_REPLACE_02_LOCAL_MANIFEST.json`

Implementation owners:

```text
crates/burn_webgpu_backend/src/tensorcube_replacement_policy.rs
crates/burn_webgpu_backend/src/tensorcube_replacement_legacy_projection.rs
crates/orchestrator_local/src/bin/ash_tcu_replace_02_policy_snapshot_audit.rs
```

Runtime behavior change, replacement activation, registry mutation, default route change, GPU command submission, production promotion and performance claims are forbidden.

---

## 1. Purpose

REPLACE-01-R2 proved that replacement-related state can be isolated into a canonical route-replacement graph and that the repository is ready to establish a single policy owner.

REPLACE-02 establishes:

```text
TensorCubeReplacementPolicySnapshot
```

as the sole replacement policy SSOT for the migrated compatibility boundary.

Existing boolean-shaped consumer APIs may remain temporarily, but their safe default values must be read from a read-only snapshot projection. They may no longer originate from independent literal defaults on the migrated surfaces.

This patch changes ownership, not execution behavior.

---

## 2. Parent binding

The policy snapshot constructor and the audit binary must bind all of the following exactly:

```text
patch_id = ASH-TCU-REPLACE-01-R2
runtime_schema = ash.tcu.replace.01.r2.ownership_audit.runtime_artifact.v1
semantic_inventory_digest = 7cd333f938c4908e52e3ddf9fcd8e41d7c518bd6dbdd5a5be72fe1e0fca52f9d
route_symbol_allowlist_digest = 6ec309aa7fb71f1ce0c96747ed50b9528c531eb8a9183499cb5532a8199c6375
repository_ready_for_replace_02 = true
```

Any mismatch is blocking. No fallback to R1 or an older R2 execution is permitted.

Required failure IDs:

```text
FAIL_TCU_REPLACE_02_PARENT_PATCH_ID_MISMATCH
FAIL_TCU_REPLACE_02_PARENT_SCHEMA_MISMATCH
FAIL_TCU_REPLACE_02_PARENT_SEMANTIC_DIGEST_MISMATCH
FAIL_TCU_REPLACE_02_PARENT_ALLOWLIST_DIGEST_MISMATCH
FAIL_TCU_REPLACE_02_PARENT_NOT_READY
FAIL_TCU_REPLACE_02_PARENT_ARTIFACT_MISSING
```

---

## 3. Canonical replacement mode

The owner module must define the exhaustive enum:

```rust
pub enum TensorCubeReplacementMode {
    Disabled,
    ShadowOnly,
    CandidatePrepared,
    ApplyAuthorized,
    InternalCanary,
    UserVisibleCanary,
    ProductionReplacement,
}
```

Enum declaration order must not imply authority or transition legality. Projection must use exhaustive `match` semantics.

REPLACE-02 runtime construction is limited to:

```text
Disabled
ShadowOnly
```

The remaining variants are declared and projectable for schema completeness, but this patch must not construct them in runtime execution.

Required zero counters:

```text
runtime_constructed_apply_authorized_count=0
runtime_constructed_internal_canary_count=0
runtime_constructed_user_visible_canary_count=0
runtime_constructed_production_replacement_count=0
```

---

## 4. Immutable policy snapshot

The policy owner is:

```rust
pub struct TensorCubeReplacementPolicySnapshot
```

All fields must remain private. No setter, `DerefMut`, interior-mutability cell, mutable global current-mode variable or public struct literal construction is allowed.

A new state requires a new snapshot.

The snapshot must bind:

```text
policy schema
parent semantic digest
parent route allowlist digest
replacement mode
policy source
policy scope
candidate identity
route identity
operator authorization digest
rollback anchor digest
construction input digest
snapshot semantic digest
```

Only `tensorcube_replacement_policy.rs` may construct the snapshot.

Required constructors:

```rust
explicit_disabled_default(...)
import_legacy_matrix_strict(...)
import_shadow_evidence(...)
```

No external module may construct `TensorCubeReplacementPolicySnapshot { ... }`.

---

## 5. Policy source and scope

Supported source classes:

```text
legacy_matrix_import
explicit_disabled_default
shadow_evidence_import
test_fixture
```

REPLACE-02 must not add CLI enablement, environment enablement, registry mutation or production approval sources.

Supported scope classes:

```text
repository_default
shadow_run
candidate
internal_canary
user_visible_canary
production
```

Only repository default, shadow and non-active candidate scopes are admissible for this patch.

---

## 6. Legacy boolean matrix

The compatibility import boundary uses a versioned matrix:

```text
ash.tcu.replace.02.legacy_boolean_matrix.v1
```

Canonical fields:

```text
replacement_enabled
replacement_admitted
replacement_selected
replacement_prepared
replacement_apply_authorized
internal_canary_active
user_visible_canary_active
production_replacement_allowed
production_replacement_executed
global_default_route_changed
replacement_output_owned
no_production_replacement
```

Each field owns a fixed bit in `LegacyReplacementMatrixKey(u16)`.

The matrix is import input only. It must not be retained as a mutable second authority.

Required flow:

```text
legacy matrix
→ strict validation
→ immutable policy snapshot
→ read-only compatibility projection
→ existing consumer
```

---

## 7. Strict matrix import

The importer must recognize only explicitly registered matrices.

Initial known matrices:

```text
disabled
shadow_only
```

Unknown matrices fail closed. They must not silently become Disabled.

Contradictory matrices fail closed, including:

```text
production_replacement_executed=true
AND global_default_route_changed=false

no_production_replacement=true
AND production_replacement_allowed=true

internal_canary_active=true
AND user_visible_canary_active=true

production_replacement_executed=true
AND replacement_apply_authorized=false
```

Required counters:

```text
unknown_legacy_matrix_count=0
ambiguous_legacy_matrix_count=0
legacy_matrix_fallback_count=0
```

Required failure IDs:

```text
FAIL_TCU_REPLACE_02_UNKNOWN_LEGACY_BOOLEAN_MATRIX
FAIL_TCU_REPLACE_02_AMBIGUOUS_LEGACY_BOOLEAN_MATRIX
FAIL_TCU_REPLACE_02_LEGACY_MATRIX_FALLBACK_DETECTED
FAIL_TCU_REPLACE_02_LEGACY_MATRIX_SCHEMA_DRIFT
```

---

## 8. Read-only compatibility projection

The projection owner is:

```text
crates/burn_webgpu_backend/src/tensorcube_replacement_legacy_projection.rs
```

It defines:

```rust
pub struct LegacyReplacementBooleanView
```

and one exhaustive mode projection.

The view is immutable and may be created only by the projection owner through the snapshot API.

External struct literals are forbidden:

```text
policy_snapshot_external_struct_literal_count=0
legacy_boolean_view_external_struct_literal_count=0
```

Disabled projection must guarantee:

```text
replacement_enabled=false
replacement_admitted=false
replacement_selected=false
replacement_prepared=false
replacement_apply_authorized=false
internal_canary_active=false
user_visible_canary_active=false
production_replacement_allowed=false
production_replacement_executed=false
global_default_route_changed=false
replacement_output_owned=false
no_production_replacement=true
```

Production projection may exist for schema completeness, but REPLACE-02 may not construct the corresponding mode.

---

## 9. Same-state projection parity

For each registered matrix:

```text
matrix before import
=
view projected from the imported snapshot
```

The audit must prove round-trip parity for the disabled and shadow-only fixtures.

Required:

```text
legacy_projection_mismatch_count=0
missing_projection_surface_count=0
```

A mismatch is blocking and may not be downgraded to a warning.

---

## 10. Migrated consumer surface

REPLACE-02 migrates the fail-closed replacement default on the following Q-wave compatibility surfaces:

```text
qwave_atlas_backend_router.rs
qwave_atlas_parity.rs
qwave_atlas_telemetry.rs
qwave_atlas_timing_probe.rs
qwave_backend_switch_dryrun.rs
qwave_backend_apply_candidate.rs
qwave_backend_apply_sandbox.rs
qwave_backend_rollback_ledger.rs
qwave_backend_recovery_candidate.rs
qwave_backend_apply_preflight.rs
qwave_backend_shadow_commit.rs
```

The public compatibility field may remain, but literal `false` writers on these migrated defaults must be replaced by:

```text
repository default snapshot
→ legacy boolean view
→ tensorcube_matmul_replacement_enabled
```

Required:

```text
migrated_surface_count=11
missing_migrated_surface_count=0
literal_default_writer_count=0
snapshot_projection_use_count>0
```

This patch does not yet require every historical audit receipt or every consumer to read the enum directly. Direct enum consumer migration belongs to REPLACE-03.

---

## 11. Direct writer retirement boundary

The audit must classify the migrated writer boundary and prove:

```text
forbidden_independent_legacy_boolean_writer_count=0
dual_authority_count=0
snapshot_bypass_count=0
```

Allowed writes are limited to:

```text
legacy import matrix construction
legacy projection construction inside the owner
explicit test fixtures
serialization-only structures
```

No migrated runtime default may retain an independent literal replacement authority.

---

## 12. Snapshot digest

Snapshot semantic digest inputs:

```text
policy schema
parent R2 semantic digest
parent route allowlist digest
mode
policy source
policy scope
candidate identity
route identity
operator authorization digest
rollback anchor digest
construction input digest
```

Excluded:

```text
absolute path
timestamp
process ID
memory address
output directory
Cargo profile
host name
JSON whitespace
```

Required:

```text
same parent binding + same construction inputs
=
same snapshot semantic digest
```

Repeat-run mismatch is blocking.

---

## 13. Runtime outputs

The audit emits:

```text
workspace/runtime/tensorcube/
  ash_tcu_replace_02_policy_snapshot_runtime_artifact.json
  ash_tcu_replace_02_parent_r2_binding_receipt.json
  ash_tcu_replace_02_mode_registry.json
  ash_tcu_replace_02_legacy_boolean_matrix_registry.json
  ash_tcu_replace_02_snapshot_construction_inventory.json
  ash_tcu_replace_02_snapshot_digest_inventory.json
  ash_tcu_replace_02_snapshot_determinism_receipt.json
  ash_tcu_replace_02_legacy_projection_inventory.json
  ash_tcu_replace_02_projection_parity_receipt.json
  ash_tcu_replace_02_direct_boolean_writer_audit.json
  ash_tcu_replace_02_struct_literal_gate.json
  ash_tcu_replace_02_no_dual_authority_guard.json
  ash_tcu_replace_02_no_runtime_behavior_change_guard.json
  ash_tcu_replace_02_no_replacement_enablement_guard.json
  ash_tcu_replace_02_no_production_promotion_guard.json
  ash_tcu_replace_02_no_performance_claim_guard.json
  ash_tcu_replace_02_static_checks.json
  ash_tcu_replace_02_verdict.json

artifacts/
  ASH_TCU_REPLACE_02_LOCAL_MANIFEST.json
```

Runtime artifacts and the local manifest are execution outputs and must not be included in the code-only bake ZIP.

---

## 14. Required predicates

Parent binding:

```text
TCU_REPLACE_02_PARENT_R2_PATCH_ID_MATCH
TCU_REPLACE_02_PARENT_R2_SCHEMA_MATCH
TCU_REPLACE_02_PARENT_R2_SEMANTIC_DIGEST_MATCH
TCU_REPLACE_02_PARENT_R2_ALLOWLIST_DIGEST_MATCH
TCU_REPLACE_02_PARENT_R2_READINESS_TRUE
```

SSOT and immutability:

```text
TCU_REPLACE_02_POLICY_SNAPSHOT_SINGLE_OWNER
TCU_REPLACE_02_POLICY_SNAPSHOT_IMMUTABLE
TCU_REPLACE_02_MODE_PROJECTION_EXHAUSTIVE
TCU_REPLACE_02_NO_EXTERNAL_SNAPSHOT_STRUCT_LITERAL
TCU_REPLACE_02_NO_EXTERNAL_LEGACY_VIEW_STRUCT_LITERAL
TCU_REPLACE_02_NO_GLOBAL_MUTABLE_REPLACEMENT_MODE
```

Import and projection:

```text
TCU_REPLACE_02_UNKNOWN_LEGACY_MATRIX_FAILS_CLOSED
TCU_REPLACE_02_AMBIGUOUS_LEGACY_MATRIX_FAILS_CLOSED
TCU_REPLACE_02_SAME_STATE_SAME_SCOPE_PARITY
TCU_REPLACE_02_SNAPSHOT_DIGEST_DETERMINISTIC
```

Writer retirement:

```text
TCU_REPLACE_02_DIRECT_LITERAL_WRITERS_RETIRED_ON_MIGRATED_SURFACES
TCU_REPLACE_02_FORBIDDEN_INDEPENDENT_BOOLEAN_WRITER_COUNT_ZERO
TCU_REPLACE_02_NO_DUAL_BOOLEAN_AUTHORITY
TCU_REPLACE_02_NO_SNAPSHOT_BYPASS
```

Safety:

```text
TCU_REPLACE_02_NO_RUNTIME_BEHAVIOR_CHANGE
TCU_REPLACE_02_NO_REPLACEMENT_ENABLEMENT
TCU_REPLACE_02_NO_PRODUCTION_PROMOTION
TCU_REPLACE_02_NO_PERFORMANCE_CLAIM
```

---

## 15. Required tests

Policy and parent binding:

```text
exact_parent_binding_passes
wrong_parent_digest_fails
same_inputs_produce_same_digest
compiled_default_never_enables_replacement
```

Legacy import:

```text
disabled_import_roundtrips
shadow_import_roundtrips
unknown_matrix_fails_closed
ambiguous_matrix_fails_closed
```

Projection:

```text
disabled_projection_is_fail_closed
every_mode_has_an_explicit_projection
```

Repository audit:

```text
policy owner count = 1
projection owner count = 1
external snapshot literal count = 0
external view literal count = 0
migrated literal false writer count = 0
migrated projection use count > 0
missing migrated surface count = 0
```

---

## 16. Safety guards

Required zero state:

```text
runtime_route_mutation_count=0
registry_mutation_count=0
route_epoch_increment_count=0
default_route_change_count=0
replacement_enablement_count=0
production_replacement_execution_count=0
promotion_token_consumption_count=0
gpu_command_submission_count=0
model_output_change_count=0
training_output_change_count=0
performance_claim_count=0
```

The new policy, projection and audit modules must not import WGPU execution APIs.

---

## 17. Readiness for REPLACE-03

The audit introduces:

```text
repository_ready_for_replace_03
```

Default is false.

It becomes true only when:

```text
parent R2 binding exact
policy owner count = 1
snapshot immutable
projection exhaustive
known matrices strict
unknown and ambiguous matrices rejected
projection parity exact
external snapshot/view literals = 0
migrated literal writers = 0
forbidden independent writers = 0
dual authority = 0
snapshot bypass = 0
snapshot digest deterministic
runtime behavior unchanged
replacement not enabled
production not promoted
performance claim absent
```

Recommended next patch on PASS:

```text
ASH-TCU-REPLACE-03
Canonical Policy Snapshot Consumer Rebind /
Runtime Decision Reader Migration /
Legacy Boolean Input Authority Retirement /
Snapshot-Native Guard Evaluation /
No Default Route Change /
No Production Replacement Seal
```

---

## 18. Cargo run

```powershell
cargo run `
  --manifest-path .\crates\orchestrator_local\Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_replace_02_policy_snapshot_audit `
  -- `
  --repo-root . `
  --out-dir workspace/runtime/tensorcube `
  --parent-r2-artifact workspace/runtime/tensorcube/ash_tcu_replace_01_r2_ownership_audit_runtime_artifact.json `
  --require-no-runtime-behavior-change true `
  --require-no-replacement-enablement true `
  --require-no-production-promotion true
```

---

## 19. PASS verdict

```text
PASS_ASH_TCU_REPLACE_02_
TENSORCUBE_REPLACEMENT_MODE_SSOT_ESTABLISHED_
IMMUTABLE_POLICY_SNAPSHOT_ESTABLISHED_
PARENT_R2_SEMANTIC_DIGEST_BOUND_
LEGACY_BOOLEAN_MATRIX_IMPORTED_STRICTLY_
LEGACY_BOOLEANS_DERIVED_FROM_SINGLE_SNAPSHOT_
SAME_STATE_SAME_SCOPE_PROJECTION_PARITY_PROVEN_
DIRECT_BOOLEAN_WRITERS_RETIRED_
NO_DUAL_AUTHORITY_
NO_RUNTIME_BEHAVIOR_CHANGE_
NO_REPLACEMENT_ENABLEMENT
```

## 20. HOLD verdict

```text
HOLD_ASH_TCU_REPLACE_02_
REPLACEMENT_POLICY_SSOT_OR_COMPATIBILITY_PARITY_INCOMPLETE
```

---

## 21. Final seal

REPLACE-02 passes only when the repository can truthfully state:

```text
TensorCube replacement policy has one immutable owner.

The owner is bound to the exact REPLACE-01-R2 semantic and
route allowlist digests.

Unknown or contradictory legacy matrices fail closed.

The compatibility booleans are read-only projections from
the policy snapshot.

The migrated Q-wave replacement defaults no longer own
independent literal false values.

No external module constructs the snapshot or compatibility view.

No runtime route, registry, epoch or default route changed.

No replacement mode was enabled.

No production replacement was executed.

No GPU command was submitted.

No model or training output changed.

No performance claim was made.
```
