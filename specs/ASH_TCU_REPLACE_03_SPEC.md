# ASH-TCU-REPLACE-03

## Canonical Policy Snapshot Consumer Rebind / Runtime Decision Reader Migration / Legacy Boolean Input Authority Retirement / Snapshot-Native Guard Evaluation / Ephemeral Permit and Denial Receipt / Runtime Policy Composition-Root Ownership / Compatibility Projection Control-Flow Isolation / Same-State Decision Parity / No Default Route Change / No Production Replacement Seal

---

## 0. Patch Metadata

- **Patch ID**: `ASH-TCU-REPLACE-03`
- **Parent**: `ASH-TCU-REPLACE-02-R1`
- **Parent runtime schema**: `ash.tcu.replace.02.r1.parent_binding_repair.runtime_artifact.v1`
- **Parent semantic inventory digest**: `1b545cec1a2a6302984a9c69183f830d539cf45335ebdb7b5546a8ae721a4636`
- **Parent execution artifact digest**: `7155313ceb7ae85867dd47f2bcedd7486609d2a6a330c32a65aa8958d7a78057`
- **Parent policy module SHA-256**: `69c8f77cd42f676412371a005026335e5e6fe05929c43367530fd52fd19f4187`
- **Parent compatibility projection SHA-256**: `8d84603ba977982d97dea2ce57e4f700cc6575f27f2e76fd2b5020fb5d50e76d`
- **Parent spec commit**: `c6530c7be60f611e6cf0f7978607ce1876441302`
- **Parent readiness**: `repository_ready_for_replace_03=true`
- **Decision schema**: `ash.tcu.replace.03.snapshot_native_decision.v1`
- **Runtime context schema**: `ash.tcu.replace.03.runtime_policy_context.v1`
- **Audit artifact schema**: `ash.tcu.replace.03.consumer_rebind_audit.runtime_artifact.v1`
- **Primary runtime artifact**: `workspace/runtime/tensorcube/ash_tcu_replace_03_consumer_rebind_runtime_artifact.json`
- **Local manifest**: `artifacts/ASH_TCU_REPLACE_03_LOCAL_MANIFEST.json`

### Patch class

`runtime decision-read ownership migration`

### Explicit prohibitions

```text
policy mode semantic change       forbidden
legacy projection semantic change forbidden
runtime route mutation            forbidden
default route change              forbidden
production replacement            forbidden
GPU command submission change     forbidden
performance claim                  forbidden
```

---

## 1. Problem Statement

REPLACE-02 established `TensorCubeReplacementPolicySnapshot` as the canonical state owner, but existing Q-wave consumer surfaces still obtained the immediate branch value through a compatibility boolean:

```text
policy snapshot
→ LegacyReplacementBooleanView
→ tensorcube_matmul_replacement_enabled: bool
→ runtime guard or contract-leak branch
```

REPLACE-03 replaces that path with:

```text
single immutable runtime snapshot
→ TensorCubeReplacementDecisionReader
→ typed capability request
→ TensorCubeReplacementGuardVerdict
→ Allowed(permit) | Denied(reason)
→ runtime control flow
```

Compatibility booleans remain available only for serialized reports, telemetry, diagnostics, receipts and parity tests.

---

## 2. State Ownership

### 2.1 Canonical policy state owner

`crates/burn_webgpu_backend/src/tensorcube_replacement_policy.rs`

### 2.2 Decision interpretation owner

`crates/burn_webgpu_backend/src/tensorcube_replacement_decision.rs`

### 2.3 Runtime snapshot composition root

`crates/burn_webgpu_backend/src/tensorcube_replacement_runtime_context.rs`

The runtime context owns one immutable `TensorCubeReplacementPolicySnapshot` in one `OnceLock` composition root. Consumers can borrow the snapshot or create a reader, but cannot replace or mutate the snapshot.

### 2.4 Compatibility projection owner

`crates/burn_webgpu_backend/src/tensorcube_replacement_legacy_projection.rs`

The projection remains read-only and reporting-only. Its source digest must remain identical to the parent digest.

---

## 3. Parent Binding

The audit must read the REPLACE-02-R1 parent artifact through exact JSON pointers:

| Field | JSON pointer | Expected |
|---|---|---|
| patch ID | `/patch_id` | `ASH-TCU-REPLACE-02-R1` |
| schema | `/schema` | `ash.tcu.replace.02.r1.parent_binding_repair.runtime_artifact.v1` |
| semantic digest | `/semantic_inventory_digest` | `1b545cec...a4636` |
| execution digest | `/execution_artifact_digest` | `7155313c...8057` |
| REPLACE-03 readiness | `/verdict/repository_ready_for_replace_03` | `true` |
| parent policy SHA | `/policy_semantic_preservation/policy_module_sha256` | `69c8f77c...4187` |
| parent projection SHA | `/policy_semantic_preservation/projection_module_sha256` | `8d84603b...e76d` |
| parent spec commit | `/github_spec_commit` | `c6530c7b...1302` |

Recursive key-name lookup, alias fallback, ancestor fallback and value-coincidence selection are forbidden.

---

## 4. Capability Vocabulary

```rust
pub enum TensorCubeReplacementCapability {
    ObserveShadowEvidence,
    MeasureShadowRoute,
    PrepareCandidateMetadata,
    PrepareApplyTransaction,
    SelectReplacementRoute,
    OwnReplacementOutput,
    ChangeDefaultRoute,
    ExecuteProductionReplacement,
}
```

Enum declaration order does not imply permission ordering. Every mode-capability pair must be represented explicitly in the capability matrix.

### REPLACE-03 runtime permit allowlist

Only these two permits may be emitted:

```text
ShadowOnly × ObserveShadowEvidence
ShadowOnly × MeasureShadowRoute
```

The following permit counters must remain zero:

```text
candidate_prepare_permit_count
apply_prepare_permit_count
route_select_permit_count
output_ownership_permit_count
default_route_change_permit_count
production_replacement_permit_count
```

---

## 5. Decision Request

```rust
pub struct TensorCubeReplacementDecisionRequest {
    capability: TensorCubeReplacementCapability,
    scope: TensorCubeReplacementDecisionScope,
    candidate_identity: Option<String>,
    route_identity: Option<String>,
    request_source: TensorCubeReplacementDecisionSource,
}
```

Runtime requests must carry `RuntimeConsumer { consumer_id }`. Audit and test request sources are non-runtime evidence sources.

Scope types:

```text
RepositoryDefault
ShadowRun { run_identity }
Candidate { candidate_identity }
InternalCanary { canary_identity }
UserVisibleCanary { canary_identity }
Production
```

`Production` scope is denied by REPLACE-03.

---

## 6. Snapshot-Native Decision Reader

```rust
pub struct TensorCubeReplacementDecisionReader<'a> {
    snapshot: &'a TensorCubeReplacementPolicySnapshot,
}
```

The reader borrows one canonical snapshot and owns no replacement mode copy, legacy boolean matrix, mutable cache or route state.

```rust
pub fn evaluate(
    &self,
    request: TensorCubeReplacementDecisionRequest,
) -> TensorCubeReplacementGuardVerdict<'a>;
```

Boolean runtime APIs such as `is_allowed() -> bool` or `replacement_enabled() -> bool` are forbidden.

---

## 7. Typed Guard Verdict

```rust
pub enum TensorCubeReplacementGuardVerdict<'a> {
    Allowed(TensorCubeReplacementPermit<'a>),
    Denied(TensorCubeReplacementDenial),
}
```

Permit requirements:

- constructor private to the decision module
- fields private
- lifetime bound to the snapshot
- serialized receipt cannot be reloaded as authority
- capability, scope, snapshot digest, request digest and decision digest recorded

Denial reasons:

```text
ModeDisallowsCapability
ScopeMismatch
CandidateIdentityMissing
CandidateIdentityMismatch
RouteIdentityMissing
RouteIdentityMismatch
RuntimeConstructionForbidden
ProductionCapabilityForbiddenByPatch
```

A generic unclassified denial is forbidden.

---

## 8. Capability Matrix

The matrix is exhaustive over seven modes and eight capabilities, producing 56 entries.

- `Disabled`: deny all capabilities.
- `ShadowOnly`: allow only shadow observation and shadow measurement.
- `CandidatePrepared`: type-level observation, measurement and candidate preparation may be represented; runtime construction remains forbidden.
- `ApplyAuthorized` and later modes: type-level preparation may be represented, but route selection, output ownership, default-route mutation and production execution remain denied by REPLACE-03.

---

## 9. Identity and Scope Validation

Validation order:

```text
1. evaluate mode-capability matrix
2. reject Production scope
3. validate scope identity
4. validate candidate identity when required
5. validate route identity when required
6. emit typed permit or denial
```

Shadow observation requires an exact `ShadowRun.run_identity` match. Shadow measurement additionally requires exact route identity equality. No missing-identity fallback is allowed.

---

## 10. Runtime Composition Root

```rust
pub struct TensorCubeReplacementRuntimeContext {
    snapshot: TensorCubeReplacementPolicySnapshot,
}
```

```rust
static REPOSITORY_DEFAULT_REPLACEMENT_CONTEXT:
    OnceLock<TensorCubeReplacementRuntimeContext>;
```

Required:

```text
runtime_policy_composition_root_count=1
runtime_policy_snapshot_instance_count=1
runtime_policy_distinct_snapshot_digest_count=1
runtime_policy_consumer_unbound_count=0
```

No setter, swap, environment override or CLI replacement override is permitted.

---

## 11. Consumer Migration Scope

The following eleven surfaces must migrate runtime replacement control flow:

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

Each surface must borrow the shared runtime context, submit a typed `SelectReplacementRoute` request, directly match `Allowed` or `Denied`, retain legacy bool only in compatibility report fields, contain no old projection constructor call and contain no legacy bool in a runtime control-flow sink.

Required:

```text
runtime_decision_consumer_count=11
runtime_decision_consumer_migrated_count=11
runtime_decision_consumer_unmigrated_count=0
snapshot_native_guard_use_count>0
typed_guard_verdict_match_count>0
```

---

## 12. Legacy Boolean Authority Retirement

The public compatibility field may remain in historical config and report schemas for ABI and serialization continuity. It must not be used as an if condition, match scrutinee, while condition, logical control-flow term, runtime decision argument or snapshot reconstruction input.

Required:

```text
legacy_runtime_boolean_parameter_count=0
legacy_runtime_boolean_authority_field_count=0
legacy_runtime_boolean_branch_count=0
legacy_runtime_boolean_forwarding_count=0
runtime_legacy_bool_to_snapshot_conversion_count=0
```

---

## 13. Compatibility Projection Isolation

All previous `repository_default_legacy_boolean_view()` constructor calls in migrated surfaces must be retired.

Reporting fields may use:

```text
repository_default_replacement_context()
→ shared snapshot
→ legacy_boolean_view()
→ serialized compatibility field
```

Required:

```text
old_projection_constructor_use_count=0
compatibility_projection_runtime_control_flow_use_count=0
projection module SHA-256=8d84603ba977982d97dea2ce57e4f700cc6575f27f2e76fd2b5020fb5d50e76d
```

---

## 14. Same-State Decision Parity

The audit must compare legacy and snapshot-native decisions for at least:

```text
Disabled × SelectReplacementRoute
Disabled × ExecuteProductionReplacement
ShadowOnly × SelectReplacementRoute
ShadowOnly × OwnReplacementOutput
```

Required:

```text
decision_parity_case_count>0
decision_parity_match_count=decision_parity_case_count
decision_parity_mismatch_count=0
```

Shadow observe and measure allow cases are separately proven in the guard inventory and unit tests.

---

## 15. Decision Digests

Each decision digest includes decision schema, snapshot semantic digest, mode, policy scope, capability, request scope, identities, decision source, request digest, allowed/denied and denial reason.

Timestamps, absolute paths, process IDs, addresses and log ordering are excluded. Same snapshot and same request must produce the same digest.

---

## 16. Policy Semantic Preservation

The parent policy file is permitted one structural extension only:

```rust
pub fn candidate_identity(&self) -> Option<&str>;
pub fn route_identity(&self) -> Option<&str>;
```

These are read-only getters. They do not change construction, mode admission, legacy import, projection or snapshot digest semantics.

The projection module must remain byte-identical to the parent source hash.

Required:

```text
policy_getter_only_change=true
projection_semantics_unchanged=true
snapshot digest construction unchanged
legacy matrix import unchanged
```

---

## 17. Runtime Safety Gates

Required counters:

```text
runtime_route_mutation_count=0
registry_mutation_count=0
route_epoch_increment_count=0
default_route_change_count=0
production_replacement_execution_count=0
promotion_token_consumption_count=0
gpu_adapter_request_count=0
gpu_device_request_count=0
gpu_command_submission_count=0
shader_change_count=0
model_output_change_count=0
training_output_change_count=0
performance_claim_count=0
```

Executed output parity is not fabricated. Static-only verification must report:

```text
executed_output_parity=false
executed_output_parity_status=not_executed_static_no_change_evidence_only
```

---

## 18. Required Runtime Outputs

```text
workspace/runtime/tensorcube/
  ash_tcu_replace_03_consumer_rebind_runtime_artifact.json
  ash_tcu_replace_03_parent_binding_receipt.json
  ash_tcu_replace_03_runtime_snapshot_composition_root_receipt.json
  ash_tcu_replace_03_consumer_inventory.json
  ash_tcu_replace_03_consumer_migration_summary.json
  ash_tcu_replace_03_capability_registry.json
  ash_tcu_replace_03_capability_matrix.json
  ash_tcu_replace_03_guard_evaluation_inventory.json
  ash_tcu_replace_03_guard_decision_digest_inventory.json
  ash_tcu_replace_03_legacy_boolean_input_audit.json
  ash_tcu_replace_03_compatibility_projection_isolation_audit.json
  ash_tcu_replace_03_decision_parity_receipt.json
  ash_tcu_replace_03_no_runtime_behavior_change_guard.json
  ash_tcu_replace_03_no_default_route_change_guard.json
  ash_tcu_replace_03_no_production_replacement_guard.json
  ash_tcu_replace_03_no_gpu_behavior_change_guard.json
  ash_tcu_replace_03_no_performance_claim_guard.json
  ash_tcu_replace_03_static_checks.json
  ash_tcu_replace_03_verdict.json

artifacts/
  ASH_TCU_REPLACE_03_LOCAL_MANIFEST.json
```

Generated evidence must not be included in the code-only baked ZIP.

---

## 19. Blocking Predicates

```text
TCU_REPLACE_03_PARENT_BINDING_PASS
TCU_REPLACE_03_RUNTIME_POLICY_COMPOSITION_ROOT_SINGLE
TCU_REPLACE_03_RUNTIME_POLICY_SNAPSHOT_INSTANCE_SINGLE
TCU_REPLACE_03_RUNTIME_DECISION_READER_MIGRATION_COMPLETE
TCU_REPLACE_03_SNAPSHOT_NATIVE_GUARD_USE_COUNT_NONZERO
TCU_REPLACE_03_LEGACY_RUNTIME_BOOLEAN_BRANCH_COUNT_ZERO
TCU_REPLACE_03_LEGACY_RUNTIME_BOOLEAN_FORWARDING_COUNT_ZERO
TCU_REPLACE_03_COMPATIBILITY_PROJECTION_RUNTIME_CONTROL_FLOW_COUNT_ZERO
TCU_REPLACE_03_DECISION_PARITY_MISMATCH_COUNT_ZERO
TCU_REPLACE_03_GUARD_EVALUATION_INVENTORY_PASS
TCU_REPLACE_03_NO_ROUTE_SELECT_PERMIT
TCU_REPLACE_03_NO_OUTPUT_OWNERSHIP_PERMIT
TCU_REPLACE_03_NO_DEFAULT_ROUTE_CHANGE_PERMIT
TCU_REPLACE_03_NO_PRODUCTION_REPLACEMENT_PERMIT
TCU_REPLACE_03_NO_RUNTIME_BEHAVIOR_CHANGE
TCU_REPLACE_03_NO_DEFAULT_ROUTE_CHANGE
TCU_REPLACE_03_NO_PRODUCTION_REPLACEMENT
TCU_REPLACE_03_NO_GPU_BEHAVIOR_CHANGE
TCU_REPLACE_03_NO_PERFORMANCE_CLAIM
TCU_REPLACE_03_POLICY_AND_PROJECTION_SEMANTICS_PRESERVED
```

Any failed predicate produces HOLD and a non-zero exit code.

---

## 20. Required Tests

```text
repository default context is singleton
repository default snapshot is Disabled
Disabled denies all eight capabilities
ShadowOnly allows matching ObserveShadowEvidence
ShadowOnly allows matching MeasureShadowRoute
route identity mismatch denies
Disabled and ShadowOnly deny SelectReplacementRoute
Production scope denies
same snapshot and request produce same decision digest
parent paths are exact
capability matrix has 56 entries
decision parity mismatch count is zero
```

---

## 21. Readiness for REPLACE-04

`repository_ready_for_replace_04` may be true only when parent binding passes, the single composition root is proven, all eleven consumers are migrated, legacy control-flow counts are zero, projection control-flow count is zero, guard inventory passes, parity mismatch is zero, dangerous permit counts are zero and all safety guards pass.

Recommended next patch:

```text
ASH-TCU-REPLACE-04
Canonical Replacement Transition Transaction /
Mode Transition Graph /
Authorization and Rollback Anchor Binding /
Candidate-to-Apply Prepared Transaction /
Dry-Run Transition Receipt /
No Active Route Mutation /
No Production Replacement Seal
```

---

## 22. PASS and HOLD Markers

### PASS

```text
PASS_ASH_TCU_REPLACE_03_CANONICAL_POLICY_SNAPSHOT_CONSUMERS_REBOUND_RUNTIME_DECISION_READERS_MIGRATED_LEGACY_BOOLEAN_INPUT_AUTHORITY_RETIRED_SNAPSHOT_NATIVE_GUARD_EVALUATION_ESTABLISHED_EPHEMERAL_PERMITS_BOUND_TO_SNAPSHOT_COMPATIBILITY_PROJECTION_ISOLATED_FROM_RUNTIME_CONTROL_FLOW_SAME_STATE_DECISION_PARITY_PROVEN_NO_DEFAULT_ROUTE_CHANGE_NO_PRODUCTION_REPLACEMENT
```

### HOLD

```text
HOLD_ASH_TCU_REPLACE_03_RUNTIME_DECISION_READER_OR_COMPATIBILITY_AUTHORITY_MIGRATION_INCOMPLETE
```

---

## 23. Final Seal

REPLACE-03 passes only when one immutable runtime composition root owns the policy snapshot, all eleven migrated consumers use typed snapshot-native guards, compatibility booleans remain reporting-only, dangerous permits remain zero, parent decision parity is preserved and no route, default, registry, epoch, GPU, model, training or production state changes.
