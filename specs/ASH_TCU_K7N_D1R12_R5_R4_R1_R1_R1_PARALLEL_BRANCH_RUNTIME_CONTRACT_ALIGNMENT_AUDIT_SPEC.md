# ASH-TCU-K7N-D1R12-R5-R4-R1-R1-R1

## Parallel Branch Runtime Contract Alignment Audit

### Patch ID

`ASH-TCU-K7N-D1R12-R5-R4-R1-R1-R1_PARALLEL_BRANCH_RUNTIME_CONTRACT_ALIGNMENT_AUDIT`

### Purpose

Audit why `R5-R4-R1-R1` selected `sampler_or_kv_contract_incompatible` without mutating sampler, KV, route registry, route epoch, branch evidence or runtime output.

The audit distinguishes actual runtime-generation incompatibility from:

- legacy protected-state schemas that omitted sampler/KV receipt fields;
- raw digest or serialization drift;
- branch-local invocation state included in shared identity;
- runtime families that were never invoked by either TensorCube measurement branch.

### Required parents

- R5-R4-R1-R1 execution `d1r12-r5-r4-r1-r1-30b3cfbcc502474baf95`, outcome `sampler_or_kv_contract_incompatible`.
- R5-R4-R1 execution `d1r12-r5-r4-r1-0fa8776fe8b41b5ef209`, outcome `branch_compatibility_invalid`.
- S05 execution `d1r12-r5-r3a-r3-0ba517ce6b0c8a27c181`, outcome `zero_reproduced_red_branch_sealed`.
- S13 execution `d1r12-r5-r3b-e6d3724554de93dc66a0`, outcome `cold_start_only_transient`.

### Immutable branch semantics

```text
s05_persistent_authority=false
s05_persistent_effective_weight=0
s13_persistent_authority=false
s13_persistent_effective_weight=0
combined_persistent_authority_count=0
combined_persistent_effective_weight=0
current_route_classification=conditional_hold
output_authority=burn
```

### Root-cause contract

R5-R4-R1 read `sampler_contract_unchanged` and `kv_contract_unchanged` from the S13 protected-state artifact. R5-R3B required the corresponding CLI verification flags but its protected-state schema did not persist those fields. Missing fields must not be silently converted to `true` or treated as an actual runtime mismatch without first auditing whether sampler and autoregressive KV were invoked.

### Runtime-family invocation audit

Statically audit the S05 and S13 branch sources for actual sampler/decode and autoregressive KV execution. CLI flags, `kv_bucket` metadata and receipt labels do not constitute execution.

When neither branch invokes a runtime family:

```text
runtime_family_status=not_applicable_non_decode_tensorcube_measurement_branch
```

The legacy field omission increments `legacy_omitted_receipt_count`, but it increments `missing_required_receipt_count` only when the omitted receipt is authority-relevant to an invoked runtime family.

Expected present branch result:

```text
legacy_omitted_receipt_count=4
missing_required_receipt_count=0
authority_relevant_mismatch_count=0
```

### State ownership

Active sampler SSOT owns implementation generation, candidate selection, top-k/global merge semantics, normalization, min-p/temperature, EOS/STOP, seed/tie-break and selected-token ownership.

Active KV SSOT owns layout, precision, axis order, head/layer dimensions, append/rollback ownership, request isolation, cache epoch, prefix reuse and capacity policy.

Branch artifacts own only invocation scope and branch-local instance state. This patch owns decomposition, non-invocation proof, legacy schema-gap classification, compatibility receipt and R5-R4-R1-R2 rerun eligibility.

### Active source snapshots

Sampler source set:

```text
crates/runtime_unz/src/sampler.rs
crates/model_core/src/sampling_helpers.rs
crates/model_core/src/sampler_parity.rs
crates/model_core/src/sampler05_parity.rs
```

KV source set:

```text
crates/ash_core/src/cache_policy.rs
crates/model_core/src/kv_rollback00_probe.rs
crates/model_core/src/kv_rollback01_forked_replay.rs
```

These snapshots prove that the audit itself does not mutate active contracts. They are not substitutes for a missing receipt when a runtime family was actually invoked.

### Normal compatibility

When sampler is not invoked:

```text
sampler_engine_compatibility=not_applicable_non_invoked
sampler_policy_compatibility=not_applicable_non_invoked
sampler_eos_stop_compatibility=not_applicable_non_invoked
sampler_seed_ownership_compatibility=not_applicable_non_invoked
sampler_contract_compatibility=compatible_by_non_invocation_scope
```

When autoregressive KV is not invoked:

```text
kv_layout_compatibility=not_applicable_non_invoked
kv_shape_compatibility=not_applicable_non_invoked
kv_ownership_compatibility=not_applicable_non_invoked
kv_epoch_compatibility=not_applicable_non_invoked
kv_prefix_reuse_compatibility=not_applicable_non_invoked
kv_contract_compatibility=compatible_by_non_invocation_scope
```

Expected combined result:

```text
combined_runtime_contract_compatibility=compatible_after_branch_local_exclusion
runtime_contract_alignment_class=branch_local_identity_exclusion_alignment
```

### Outcomes

PASS:

- `runtime_contracts_exactly_compatible`
- `runtime_contracts_semantically_equivalent`
- `branch_local_fields_removed_from_shared_identity`

Fail or hold:

- `sampler_engine_generation_mismatch`
- `sampler_policy_semantics_mismatch`
- `sampler_eos_stop_or_seed_ownership_mismatch`
- `kv_layout_or_shape_contract_mismatch`
- `kv_ownership_or_epoch_contract_mismatch`
- `combined_sampler_kv_contract_mismatch`
- `parent_runtime_contract_evidence_insufficient`
- `runtime_contract_canonicalizer_fault`
- `parent_evidence_mismatch`
- `protected_state_violation`

### Next state

For any PASS outcome:

`ASH-TCU-K7N-D1R12-R5-R4-R1-R2_PARALLEL_GATE_EVIDENCE_RECONCILIATION_RERUN_WITH_REPAIRED_IDENTITY_BINDING`

R5-R4-R1-R2 must bind both the R5-R4-R1-R1 repaired identity receipt and this patch's runtime compatibility receipt. It must not repeat performance replay.

### Implementation files

```text
crates/model_core/src/vocab_atlas_shadow_parallel_branch_runtime_contract_alignment_audit_contract.rs
crates/orchestrator_local/src/ash_tcu_k7n_d1r12_r5_r4_r1_r1_r1_parallel_branch_runtime_contract_alignment_audit_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7n_d1r12_r5_r4_r1_r1_r1_parallel_branch_runtime_contract_alignment_audit.rs
crates/model_core/src/lib.rs
crates/orchestrator_local/Cargo.toml
```

No backend module is added.

### Required artifacts

The patch writes parent reconciliation, active sampler/KV source snapshots, S05/S13 contract observations, contract decompositions, branch-local exclusion registry, normalization receipts, sampler/KV compatibility, comparison vector, mismatch classification, alignment recommendation, runtime compatibility receipt, rerun input, determinism audit, protected-state guard, report, verdict, final seal and local manifest under `k7n_d1r12_r5_r4_r1_r1_r1`.

### Protected state

Required counters:

```text
replay_execution_count=0
gpu_dispatch_count=0
new_measurement_pair_count=0
sampler_contract_mutation_count=0
sampler_policy_mutation_count=0
eos_stop_contract_mutation_count=0
kv_contract_mutation_count=0
kv_layout_mutation_count=0
kv_ownership_mutation_count=0
cache_epoch_mutation_count=0
route_classification_change_count=0
registry_mutation_count=0
route_epoch_change_count=0
output_authority=burn
runtime_output_changed=false
```

### Expected normal outcome

```text
PASS_ASH_TCU_K7N_D1R12_R5_R4_R1_R1_R1_PARALLEL_BRANCH_RUNTIME_CONTRACT_ALIGNMENT_AUDIT_SHARED_RUNTIME_SEMANTICS_RECONCILED
OUTCOME_ASH_TCU_K7N_D1R12_R5_R4_R1_R1_R1_BRANCH_LOCAL_FIELDS_REMOVED_FROM_SHARED_IDENTITY
selected_outcome=branch_local_fields_removed_from_shared_identity
r5_r4_r1_r2_reconciliation_rerun_eligible=true
```

### Exit codes

```text
compatible outcomes=0
evidence insufficient=5
sampler or KV mismatch=6
canonicalizer fault=7
parent evidence mismatch=8
protected state violation=70
```

PASS does not remove the conditional hold, mutate the route registry, change sampler/KV implementation, promote TensorCube output or establish production readiness.