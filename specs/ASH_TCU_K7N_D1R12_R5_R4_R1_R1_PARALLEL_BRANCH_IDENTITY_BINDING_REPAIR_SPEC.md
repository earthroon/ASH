# ASH-TCU-K7N-D1R12-R5-R4-R1-R1

## Parallel Branch Identity Binding Repair

### Patch ID

`ASH-TCU-K7N-D1R12-R5-R4-R1-R1_PARALLEL_BRANCH_IDENTITY_BINDING_REPAIR`

### Purpose

Repair the branch-compatibility constitution used by R5-R4-R1 without replaying measurements or mutating branch evidence, route classification, registry state, policy, weights, or runtime output.

The direct parent execution `d1r12-r5-r4-r1-0fa8776fe8b41b5ef209` established valid S05 and S13 evidence with zero persistent authority and zero persistent effective weight, but selected `branch_compatibility_invalid`.

Source inspection identifies the invalid shared-identity comparison: R5-R4-R1 required the S05 and S13 route entries to have the same `decision_digest`. A decision digest belongs to a branch-local route decision, so distinct S05 and S13 routes may and normally do have different decision digests. It must not be included in shared model-generation identity.

### Direct parent

- Patch: `ASH-TCU-K7N-D1R12-R5-R4-R1_PARALLEL_GATE_EVIDENCE_RECONCILIATION_RERUN`
- Execution: `d1r12-r5-r4-r1-0fa8776fe8b41b5ef209`
- Outcome: `branch_compatibility_invalid`

### Evidence parents

S05:

- Execution: `d1r12-r5-r3a-r3-0ba517ce6b0c8a27c181`
- Outcome: `zero_reproduced_red_branch_sealed`
- Route: `ash.tensorcube.k7n.d1r9.shadow.s05_m1_n1_k4.568e107d07767a58`
- Shape: `S05_M1_N1_K4`
- Persistent authority: false
- Persistent effective weight: 0

S13:

- Execution: `d1r12-r5-r3b-e6d3724554de93dc66a0`
- Outcome: `cold_start_only_transient`
- Route: `ash.tensorcube.k7n.d1r9.shadow.s13_m1_n16_k5.307d7e28a0a4753c`
- Shape: `S13_M1_N16_K5`
- Persistent authority: false
- Persistent effective weight: 0

### Canonical parallel-gate scope

`parallel_gate_scope:ash.tensorcube.k7n.d1r9.shadow.s05_m1_n1_k4.568e107d07767a58|ash.tensorcube.k7n.d1r9.shadow.s13_m1_n16_k5.307d7e28a0a4753c`

Canonical member order is `s05`, then `s13`. Each route remains physically distinct and owns exactly one branch role.

### Identity ownership

Branch-local physical identity:

- route ID
- shape ID
- signature digest
- decision digest
- bucket identity
- branch role

Shared runtime-generation identity:

- parent D1R8 generation
- whitelist generation
- runtime authority
- shader digest
- ABI digest
- pipeline-layout digest
- route schema and route mode
- output authority
- sampler contract
- KV contract
- aggregation-policy generation
- registry generation
- route epoch binding

Evidence authority remains owned by R5-R3A-R3 and R5-R3B.

### Required repair

Forbidden shared comparison:

`S05 decision_digest == S13 decision_digest`

Required ownership:

`decision_digest_ownership=branch_local_route_decision`

Required receipt:

`decision_digest_excluded_from_shared_model_identity=true`

Required route comparison mode:

`distinct_members_same_parallel_scope`

Required shape comparison mode:

`branch_specific_shape`

### Compatibility vector

The patch must reconstruct the failed parent vector and produce explicit rows for:

- scope identity
- scope membership
- model identity
- output authority
- sampler contract
- KV contract
- aggregation-policy generation
- registry generation
- route epoch

No unconditional compatibility fallback is allowed. PASS requires zero remaining failed dimensions and zero remaining indeterminate dimensions.

### Normal compatibility

- Shared model identity: `exact_shared_runtime_generation`
- Output authority: exact Burn authority
- Sampler contract: exact parent-sealed contract
- KV contract: exact parent-sealed contract
- Aggregation policy: exact immutable generation
- Registry generation: `exact_current_generation`
- Route epoch: `exact_same_epoch`

### Evidence preservation

The patch must preserve:

- S05 persistent authority=false
- S05 persistent effective weight=0
- S13 persistent authority=false
- S13 persistent effective weight=0
- S13 cold-start observation as non-authoritative diagnostic history
- Combined persistent authority count=0
- Combined persistent effective weight=0

### No replay

- replay execution count=0
- GPU dispatch count=0
- new measurement pair count=0
- child process count=0

### Outcomes

PASS outcomes, exit 0:

- `shared_identity_binding_repaired`
- `scope_membership_binding_repaired`
- `historical_epoch_binding_repaired`
- `multiple_identity_bindings_repaired`

Non-PASS outcomes:

- `parent_compatibility_evidence_insufficient`, exit 5
- `shared_model_identity_incompatible`, exit 6
- `sampler_or_kv_contract_incompatible`, exit 6
- `policy_generation_incompatible`, exit 6
- `registry_or_epoch_binding_incompatible`, exit 6
- `parent_evidence_mismatch`, exit 8
- `protected_state_violation`, exit 70

Expected repair class from source inspection:

`route_specific_decision_digest_removed_from_shared_model_identity`

### Normal next state

`ASH-TCU-K7N-D1R12-R5-R4-R1-R2_PARALLEL_GATE_EVIDENCE_RECONCILIATION_RERUN_WITH_REPAIRED_IDENTITY_BINDING`

R5-R4-R1-R2 must bind the repaired identity receipt and rerun reconciliation only. It must not replay performance measurements.

### Mutation authority

This patch does not evaluate or execute hold retirement. Required local value:

`route_hold_retirement_mutation_eligible=not_evaluated_identity_repair_only`

Required mutation counters are all zero. Output authority remains Burn and runtime output remains unchanged.

### Implementation files

New:

- `crates/model_core/src/vocab_atlas_shadow_parallel_branch_identity_binding_repair_contract.rs`
- `crates/orchestrator_local/src/ash_tcu_k7n_d1r12_r5_r4_r1_r1_parallel_branch_identity_binding_repair_report.rs`
- `crates/orchestrator_local/src/bin/ash_tcu_k7n_d1r12_r5_r4_r1_r1_parallel_branch_identity_binding_repair.rs`

Modified registrations:

- `crates/model_core/src/lib.rs`
- `crates/orchestrator_local/Cargo.toml`

No backend module is added.

### Required artifacts

The patch writes manifest-owned artifacts for parent reconciliation, prior compatibility reconstruction, identity constitution, scope identity and membership, branch-role binding, model/runtime/policy/registry/epoch compatibility, dimension vector, repair classification, repaired identity binding, rerun input, determinism audit, protected-state guard, report, verdict, final seal, and local manifest.

### Protected state

Hash before and after:

- R5-R4-R1 immutable artifacts
- R5-R3A-R3 immutable artifacts
- R5-R3B immutable artifacts
- historical R5-R4 immutable artifacts
- R2 aggregation policy
- active route registry
- route epoch
- Burn backend source

PASS requires all protected state unchanged.

### PASS meaning

PASS means the two distinct routes are valid members of one parallel-gate scope, branch-local decision digests no longer contaminate shared model identity, shared runtime-generation identity is compatible, branch semantics remain unchanged, and an R5-R4-R1 rerun input has been produced.

PASS does not remove the conditional hold, mutate the registry, merge routes, advance the epoch, replay performance measurements, promote TensorCube output, or establish production readiness.
