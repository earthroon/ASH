# ASH-TCU-K7N-D1R12-R5-R6

## CONDITIONAL_HOLD_RETIREMENT_MUTATION_PLAN

## 1. Identity

```text
patch_id=ASH-TCU-K7N-D1R12-R5-R6_CONDITIONAL_HOLD_RETIREMENT_MUTATION_PLAN
PASS=PASS_ASH_TCU_K7N_D1R12_R5_R6_CONDITIONAL_HOLD_RETIREMENT_MUTATION_PLAN_TRANSACTION_AND_ROLLBACK_CONTRACT_SEALED
HOLD=HOLD_ASH_TCU_K7N_D1R12_R5_R6_CONDITIONAL_HOLD_RETIREMENT_MUTATION_PLAN_SUCCESSOR_OR_TRANSACTION_NOT_RESOLVED
FAIL=FAIL_ASH_TCU_K7N_D1R12_R5_R6_CONDITIONAL_HOLD_RETIREMENT_MUTATION_PLAN_PARENT_OR_REGISTRY_CONTRACT_INVALID
```

GitHub path:

```text
specs/ASH_TCU_K7N_D1R12_R5_R6_CONDITIONAL_HOLD_RETIREMENT_MUTATION_PLAN_SPEC.md
```

## 2. Purpose and mutation boundary

R5-R6 consumes the successful R5-R4-R1-R2 reconciliation and produces the deterministic, fail-closed input for the later hold-retirement apply transaction.

R5-R6 is plan-only. It must not change classification, registry bytes, route epoch, branch evidence, policy, or runtime output.

## 3. Direct parent

```text
parent_patch=ASH-TCU-K7N-D1R12-R5-R4-R1-R2_PARALLEL_GATE_EVIDENCE_RECONCILIATION_RERUN_WITH_REPAIRED_IDENTITY_BINDING
parent_execution_id=d1r12-r5-r4-r1-r2-4f938091f0b138fa9f02
parent_outcome=parallel_gate_no_persistent_hold_support_reconciled
```

Required parent facts:

```text
repaired_branch_compatibility_status=compatible_after_identity_and_runtime_repair
combined_persistent_authority_count=0
combined_persistent_effective_weight=0
current_hold_evidence_status=superseded_historical_evidence_only
parallel_gate_route_authority_support=no_current_persistent_hold_support
route_hold_retirement_evidence_eligible=true
route_hold_retirement_plan_eligible=true
output_authority=burn
runtime_output_changed=false
```

Manifest-bound inputs:

```text
hold_retirement_plan_input
reconciliation_receipt
final_seal
local_manifest
```

Console reconstruction is forbidden when a manifest-bound artifact exists.

## 4. State ownership correction

`conditional_hold` belongs to the D1R12 health-classification layer, not the D1R9 shadow registry.

```text
D1R12 health owner:
  invalid
  confirmed_hold
  conditional_hold
  observation_hold
  amber
  healthy

D1R9 registry owner:
  route membership
  exact-signature shadow mode
  enabled state
  runtime authority
  registry content digest
  route epoch
```

The successor is therefore a composite state:

```text
successor_classification_resolution_status=resolved_composite_registry_state
successor_classification=healthy
successor_observation_mode=exact_signature_non_authoritative_shadow
successor_output_authority=burn
successor_production_authority=false
successor_persistent_authority=false
successor_persistent_effective_weight=0
```

## 5. Scope

```text
parallel_gate_scope_id=parallel_gate_scope:ash.tensorcube.k7n.d1r9.shadow.s05_m1_n1_k4.568e107d07767a58|ash.tensorcube.k7n.d1r9.shadow.s13_m1_n16_k5.307d7e28a0a4753c
s05_route=ash.tensorcube.k7n.d1r9.shadow.s05_m1_n1_k4.568e107d07767a58
s13_route=ash.tensorcube.k7n.d1r9.shadow.s13_m1_n16_k5.307d7e28a0a4753c
```

Both entries must be present, enabled, Active, bound to the current registry epoch, use `exact_signature_non_authoritative_shadow`, retain Burn output authority, and prohibit shadow and production output commit.

## 6. Successor transition proof

The D1R12 R2 health-precedence function is the transition-policy owner.

```text
invalid=false
confirmed=false
conditional=false
observation=false
amber=false
derived_health=healthy
transition_source=conditional_hold
transition_target=healthy
transition_edge_valid=true
```

No independent fallback string is allowed.

## 7. Active-registry stale guard

The parent plan input binds:

```text
active_registry_generation=<D1R9 current_registry_digest>
active_route_epoch=<D1R9 epoch>
```

R5-R6 must re-read the active registry and require exact equality. A mismatch selects:

```text
active_registry_state_changed_since_reconciliation
```

No silent rebase is allowed.

## 8. Epoch and digest rebind

D1R9 validates every entry with:

```text
entry.applied_route_epoch == registry.epoch
```

Therefore the later apply transaction must perform:

```text
registry.epoch -> registry.epoch + 1
all entry.applied_route_epoch -> new registry epoch
registry.current_registry_digest -> resealed digest
```

Required plan output:

```text
route_epoch_change_required=true
planned_route_epoch_increment=1
registry_generation_change_required=true
registry_epoch_rebind_required=true
planned_entry_epoch_rebind_count=<active registry entry count; expected 17>
```

R5-R6 must simulate, reseal, and validate the post-state in memory without writing it.

## 9. Planned transaction ownership

R5-R6 owns the successor resolution, read/write sets, CAS contract, epoch transition, registry digest transition, rollback plan, failure-injection plan, apply eligibility, and R5-R6-A1 input.

R5-R6 does not own actual writes, actual epoch advancement, rollback execution, production authority, or runtime output.

## 10. Read and write sets

Read set:

```text
R1-R2 plan input, receipt, final seal, manifest
D1R9 active registry
D1R12 R2 aggregation policy
D1R12 route-health precedence contract
D1R9 route-epoch contract
S05 and S13 registry entries
```

Allowed apply write set:

```text
classification ledger: conditional_hold -> healthy
D1R9 registry epoch: old -> old + 1
all registry entry epochs: old -> new
D1R9 current registry digest: old -> resealed new digest
transition history
mutation receipt
```

Forbidden changes:

```text
route IDs
scope membership
entry mode or enabled state
entry health
persistent authority or effective weight
measurements and historical diagnostics
model, sampler, KV, tokenizer assets
output or production authority
```

## 11. Compare-and-swap and atomicity

```text
expected_classification=conditional_hold
expected_registry_digest=<captured digest>
expected_route_epoch=<captured epoch>
expected_scope_id=<exact scope>
new_classification=healthy
new_registry_digest=<validated simulated digest>
new_route_epoch=expected_route_epoch+1
```

Any mismatch produces zero commits.

The classification transition, registry epoch increment, all-entry epoch rebind, digest reseal, transition history, and mutation receipt must commit atomically. Partial publication is forbidden.

## 12. Preconditions and postconditions

Preconditions:

```text
parent evidence exact
parent plan eligible
current classification conditional_hold
current hold support absent
combined persistent authority zero
combined effective weight zero
active registry snapshot exact
scope members exact
successor composite resolved
transition derives healthy
post-state registry validates
rollback contract resolves
output authority burn
production authority false
```

Postconditions for apply:

```text
classification=healthy
conditional_hold=false
shadow observation preserved=true
diagnostic history preserved=true
persistent authority=false
persistent effective weight=0
registry epoch=previous+1
all entries bound to the new epoch
scope membership unchanged=true
route IDs unchanged=true
production authority=false
output authority=burn
```

## 13. Rollback

D1R9 route epochs are monotonic. Required rollback policy:

```text
rollback_epoch_policy=monotonic_compensation
rollback_epoch=post_mutation_epoch+1
```

Rollback restores `conditional_hold` while rebinding all registry entries to the monotonic compensation epoch. It requires the exact mutation receipt, exact post-state, and no later mutation or generation.

## 14. Failure injection

```text
before_route_lock
after_route_lock
after_precondition_validation
before_classification_write
after_classification_staging
before_epoch_rebind_staging
after_epoch_rebind_staging
before_transaction_commit
after_transaction_commit
before_receipt_publication
```

```text
pre-commit failure -> zero persistent writes
post-commit failure -> recoverable from mutation receipt
```

## 15. No-apply constitution

```text
route_mutation_count=0
route_classification_change_count=0
registry_mutation_count=0
route_epoch_change_count=0
rollback_execution_count=0
replay_execution_count=0
gpu_dispatch_count=0
new_measurement_pair_count=0
output_authority=burn
runtime_output_changed=false
```

## 16. Outcomes and next states

```text
conditional_hold_retirement_mutation_plan_sealed
active_registry_state_changed_since_reconciliation
successor_classification_unresolved
registry_transition_not_permitted
route_epoch_contract_unresolved
rollback_contract_unresolved
mutation_preconditions_not_satisfied
parent_evidence_mismatch
protected_state_violation
```

Normal next state:

```text
ASH-TCU-K7N-D1R12-R5-R6-A1_CONDITIONAL_HOLD_RETIREMENT_TRANSACTION_APPLY
```

Repair next states:

```text
active registry changed -> R5-R4-R1-R2-R1 active-registry rebase audit
successor unresolved -> R5-R6-R1 successor registry contract repair
transition invalid -> R5-R6-R2 transition graph repair plan
epoch unresolved -> R5-R6-R3 route epoch ownership audit
rollback unresolved -> R5-R6-R4 rollback contract repair
```

## 17. Implementation surface

```text
crates/model_core/src/vocab_atlas_shadow_conditional_hold_retirement_mutation_plan_contract.rs
crates/orchestrator_local/src/ash_tcu_k7n_d1r12_r5_r6_conditional_hold_retirement_mutation_plan_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7n_d1r12_r5_r6_conditional_hold_retirement_mutation_plan.rs
crates/model_core/src/lib.rs
crates/orchestrator_local/Cargo.toml
```

No backend module is added.

Required model export:

```rust
#[path = "vocab_atlas_shadow_conditional_hold_retirement_mutation_plan_contract.rs"]
pub mod vocab_atlas_shadow_conditional_hold_retirement_mutation_plan_contract;
pub use vocab_atlas_shadow_conditional_hold_retirement_mutation_plan_contract::*;
```

Required seals:

```text
ASH_TCU_K7N_D1R12_R5_R6_MODEL_EXPORT_SURFACE_SEAL
ASH_TCU_K7N_D1R12_R5_R6_MODEL_CRATE_ROOT_EXPORT_FINGERPRINT_SEAL
ASH_TCU_K7N_D1R12_R5_R6_MODEL_CRATE_ROOT_EXPORT_REPAIR_SEAL
ASH_TCU_K7N_D1R12_R5_R6_ORCHESTRATOR_REPORT_SURFACE_SEAL
```

## 18. Artifacts

Immutable root:

```text
artifacts/tensorcube/k7n_d1r12_r5_r6/<execution_id>/
```

Required latest artifacts:

```text
parent_binding
active_route_registry_snapshot
route_transition_graph
successor_classification_resolution
mutation_read_set
mutation_write_set
mutation_preconditions
mutation_postconditions
compare_and_swap_contract
route_epoch_transition
registry_generation_transition
mutation_plan
rollback_snapshot
rollback_plan
failure_injection_plan
apply_eligibility
hold_retirement_apply_input
determinism_audit
protected_state_guard
report
verdict
final_seal
local_manifest
```

## 19. Determinism and protected state

The semantic plan bundle is recomputed twice. Digests must match. Timestamp, PID, temporary path, filesystem enumeration order, and unordered-map iteration are excluded from semantic identity.

Before and after hashes must prove unchanged:

```text
R1-R2 immutable artifact tree
active D1R9 registry
R2 aggregation policy
Burn backend source tree
```

## 20. Expected PASS

```text
PASS_ASH_TCU_K7N_D1R12_R5_R6_CONDITIONAL_HOLD_RETIREMENT_MUTATION_PLAN_TRANSACTION_AND_ROLLBACK_CONTRACT_SEALED
current_route_classification=conditional_hold
successor_semantics=shadow_observation_without_route_hold
successor_classification_resolution_status=resolved_composite_registry_state
successor_classification=healthy
successor_observation_mode=exact_signature_non_authoritative_shadow
transition_edge_valid=true
combined_persistent_authority_count=0
combined_persistent_effective_weight=0
registry_generation_change_required=true
route_epoch_change_required=true
planned_route_epoch_increment=1
planned_entry_epoch_rebind_count=17
compare_and_swap_contract_complete=true
mutation_transaction_atomic=true
rollback_snapshot_complete=true
rollback_epoch_policy=monotonic_compensation
rollback_contract_complete=true
route_hold_retirement_mutation_eligible=true
route_mutation_count=0
route_classification_change_count=0
registry_mutation_count=0
route_epoch_change_count=0
selected_outcome=conditional_hold_retirement_mutation_plan_sealed
next_state=ASH-TCU-K7N-D1R12-R5-R6-A1_CONDITIONAL_HOLD_RETIREMENT_TRANSACTION_APPLY
output_authority=burn
runtime_output_changed=false
execution_id=<generated>
local_manifest=<path>
```

## 21. Exit codes

```text
plan sealed=0
active registry changed=5
mutation preconditions failed=5
successor unresolved=6
transition not permitted=6
route epoch unresolved=7
rollback unresolved=7
parent evidence mismatch=8
protected state violation=70
```

PASS means the plan, CAS boundary, epoch rebind, rollback, and apply input are sealed. It does not mean the hold, registry, or epoch has already changed.
