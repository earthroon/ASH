# ASH-TCU-REPLACE-04-R2

## Active Composition-Root Eligible Edge Audit /
## Disabled-to-Shadow Dry-Run Preparation Contract /
## Repository Snapshot-Bound Transition Request /
## Active-Domain Authorization and Rollback Evidence /
## Active-vs-Fixture Transaction Isolation /
## Prepared-Store-Only Readiness /
## No Runtime Snapshot Mutation /
## No Active Route Mutation /
## No Production Replacement Seal

---

## 0. Patch Identity

```text
Patch ID
ASH-TCU-REPLACE-04-R2

Parent
ASH-TCU-REPLACE-04-R1

Parent schema
ash.tcu.replace.04.r1.snapshot_binding_repair.runtime_artifact.v1

Parent semantic digest
4828d4ec6d0eae7d74db2815a154715acbef58216d48144d8b768461751932a5

Parent execution digest
0b977a0dbbf2b97510522f0b8a8ab62e187c7277394aa9d09cab640317aadd09

Parent spec commit
9e8b60a9820a7989b86f2ed002b953f4f717d02f
```

Active composition-root authority:

```text
composition_root_id=repository_default_replacement_context
authority_domain=active_composition_root
snapshot_mode=disabled
snapshot_digest=f6cc60a0d7c726183ac8e257443d25db3e42480271dc88fb0a237706b2d3f692
```

Parent readiness:

```text
fixture_transition_mechanics_ready=true
active_composition_root_transition_binding_ready=false
repository_ready_for_replace_05=false
```

Runtime schema:

```text
ash.tcu.replace.04.r2.active_edge_audit.runtime_artifact.v1
```

Primary artifact:

```text
workspace/runtime/tensorcube/ash_tcu_replace_04_r2_active_edge_audit_runtime_artifact.json
```

Primary implementation:

```text
crates/burn_webgpu_backend/src/tensorcube_replacement_active_edge_policy.rs
crates/burn_webgpu_backend/src/tensorcube_replacement_transition.rs
crates/orchestrator_local/src/bin/ash_tcu_replace_04_r2_active_edge_audit.rs
```

---

# 1. Purpose

REPLACE-04-R1 separated the real repository composition-root snapshot from the ShadowOnly audit fixture. The active root is still `Disabled`, while the existing candidate and apply transactions are fixture-domain evidence. R2 establishes the first active-domain dry-run proposal:

```text
ActiveCompositionRoot × Disabled -> ShadowOnly
```

The proposed target is ShadowOnly, but the effective runtime state remains Disabled.

R2 must not replace the runtime snapshot, mutate any route, grant output ownership, execute replacement, submit GPU work, or make a performance claim.

---

# 2. Exact Parent Binding

The parent artifact must be read only through exact JSON pointers:

```text
/patch_id
/schema
/semantic_inventory_digest
/execution_artifact_digest
/github_spec_commit
/active_composition_root_snapshot_binding/binding/snapshot_semantic_digest
/active_composition_root_snapshot_binding/binding/snapshot_mode
/active_composition_root_snapshot_binding/binding/authority_domain
/active_composition_root_snapshot_binding/active_composition_root_binding_count
/readiness_reblock/fixture_transition_mechanics_ready
/readiness_reblock/active_composition_root_transition_binding_ready
/readiness_reblock/repository_ready_for_replace_05
/fixture_promotion_leakage_audit/fixture_evidence_used_as_active_authority_count
/static_checks/executable_transition_edge_count
```

Required values:

```text
patch_id=ASH-TCU-REPLACE-04-R1
schema=ash.tcu.replace.04.r1.snapshot_binding_repair.runtime_artifact.v1
semantic_inventory_digest=4828d4ec6d0eae7d74db2815a154715acbef58216d48144d8b768461751932a5
execution_artifact_digest=0b977a0dbbf2b97510522f0b8a8ab62e187c7277394aa9d09cab640317aadd09
github_spec_commit=9e8b60a9820a7989b86f2ed002b953f4f717d02f
active_root_digest=f6cc60a0d7c726183ac8e257443d25db3e42480271dc88fb0a237706b2d3f692
active_root_mode=disabled
active_authority_domain=active_composition_root
active_binding_count=1
fixture_transition_mechanics_ready=true
active_composition_root_transition_binding_ready=false
repository_ready_for_replace_05=false
fixture_evidence_used_as_active_authority_count=0
executable_transition_edge_count=0
```

Any mismatch is blocking.

---

# 3. Base Graph Preservation

The base topology remains exactly 11 edges: six forward and five rollback edges. R2 must not add, remove, duplicate, or reinterpret a graph edge.

The existing base edge:

```text
Disabled -> ShadowOnly
```

remains non-executable.

R2 eligibility is separate from topology. The active eligibility registry has exactly one entry:

```text
authority_domain=ActiveCompositionRoot
source_mode=Disabled
target_mode=ShadowOnly
allowed_patch_id=ASH-TCU-REPLACE-04-R2
```

Required:

```text
base_transition_edge_count=11
base_transition_graph_change_count=0
r2_active_dry_run_eligible_edge_count=1
executable_transition_edge_count=0
```

Ordinal comparison and broad target matching are forbidden.

---

# 4. Active Transition Request

The canonical request owns:

```text
authority_domain
composition_root_id
runtime_snapshot_digest
runtime_snapshot_mode
logical_source_mode
proposed_target_mode
intent
candidate_identity
route_identity
request_source
semantic_digest
```

Required request values:

```text
authority_domain=ActiveCompositionRoot
composition_root_id=repository_default_replacement_context
runtime_snapshot_digest=f6cc60a0...
runtime_snapshot_mode=Disabled
logical_source_mode=Disabled
proposed_target_mode=ShadowOnly
intent=PrepareCandidate
```

The request must have no prior transaction. Fixture-domain requests, wrong roots, wrong modes, skip edges, and fixture snapshot substitution fail closed.

---

# 5. Active Authorization Evidence

Add authorization kind:

```text
ShadowEntryPreparation
```

Add scope:

```rust
ActiveShadowEntry {
    composition_root_id: String,
    candidate_identity: String,
    route_identity: String,
}
```

Required binding:

```text
authority_domain=ActiveCompositionRoot
source_snapshot_digest=f6cc60a0...
source_mode=Disabled
authorized_target_mode=ShadowOnly
candidate_identity=request.candidate_identity
route_identity=request.route_identity
```

Required flags:

```text
dry_run_only=true
route_selection_authorized=false
output_ownership_authorized=false
default_route_change_authorized=false
production_replacement_authorized=false
```

The evidence and underlying anchor must be digest-revalidated before transaction construction.

---

# 6. Active Rollback Evidence

Required rollback binding:

```text
authority_domain=ActiveCompositionRoot
source_snapshot_digest=f6cc60a0...
source_mode=Disabled
rollback_target_mode=Disabled
candidate_identity=request.candidate_identity
route_identity=request.route_identity
```

Active-route identity, default-route identity, route-registry digest, and route epoch each require an explicit evidence status:

```text
materialized_and_validated
static_no_mutation_evidence
not_materialized
```

R2 may use `not_materialized` because the transaction is store-only and non-executable. Missing values must remain absent; fabricated route names, epochs, and digests are forbidden.

---

# 7. Active Prepared Transaction

Use the R1 canonical transaction fields:

```text
authority_domain
runtime_snapshot_digest
runtime_snapshot_mode
logical_source_mode
proposed_target_mode
effective_runtime_mode
prior_transaction_digest
logical_source_state_digest
```

Required transaction truth:

```text
authority_domain=ActiveCompositionRoot
runtime_snapshot_digest=f6cc60a0...
runtime_snapshot_mode=Disabled
logical_source_mode=Disabled
proposed_target_mode=ShadowOnly
effective_runtime_mode=Disabled
prior_transaction_digest=None
disposition=PreparedDryRunOnly
```

Required eligibility flags:

```text
dry_run_prepared=true
store_eligible=true
apply_eligible=false
route_selection_eligible=false
output_ownership_eligible=false
default_route_change_eligible=false
production_replacement_eligible=false
```

`store_eligible` means only that a future patch may persist and replay-check the prepared transaction. It is not execution authority.

---

# 8. Active Dry-Run Receipt

The receipt must prove:

```text
authority domain exact
composition-root identity exact
runtime snapshot digest exact
runtime snapshot mode exact
base graph edge valid
R2 eligibility valid
authorization valid
rollback valid
identity binding valid
runtime snapshot digest unchanged
runtime snapshot mode remains Disabled
effective runtime mode remains Disabled
store_eligible=true
apply_eligible=false
```

The receipt disposition must be `PreparedDryRunOnly`.

---

# 9. Fixture Isolation

The existing fixture transactions remain:

```text
ShadowOnly -> CandidatePrepared
CandidatePrepared -> ApplyAuthorized
```

They are not active authority. Required zero counts:

```text
fixture_snapshot_used_by_active_transaction_count=0
fixture_anchor_used_by_active_transaction_count=0
fixture_prior_transaction_used_by_active_transaction_count=0
fixture_receipt_used_for_active_readiness_count=0
```

---

# 10. Negative Fixtures

The audit must reject at least:

```text
AuditFixture × Disabled -> ShadowOnly
ActiveCompositionRoot × Disabled -> CandidatePrepared
wrong logical source mode
wrong rollback target
prior transaction injection
fixture snapshot substitution
```

Every rejection must be represented in a typed error or explicit negative-fixture receipt.

---

# 11. Digest Determinism

Semantic digests include all authority, snapshot, mode, identity, edge, authorization, rollback, and eligibility inputs.

Exclude:

```text
absolute parent path
physical parent filename
output directory
timestamp
process ID
thread ID
memory address
host name
Cargo target path
JSON formatting
```

The same parent bytes at different physical paths must produce identical final artifact bytes.

---

# 12. Readiness Scope

When R2 passes:

```text
active_composition_root_transition_binding_ready=true
prepared_transition_store_readiness=true
active_transition_apply_readiness=false
active_route_ownership_readiness=false
repository_ready_for_replace_05=true
```

Required scope:

```text
prepared_transition_store_and_single_use_consumption_contract_only
```

The following must remain false:

```text
apply execution readiness
route ownership readiness
ShadowOnly activation readiness
production replacement readiness
```

---

# 13. Safety Metrics

Required zero values:

```text
runtime_snapshot_mutation_count
runtime_context_replacement_count
active_route_mutation_count
default_route_mutation_count
registry_mutation_count
route_epoch_increment_count
route_select_permit_count
output_ownership_permit_count
default_route_change_permit_count
production_replacement_permit_count
production_replacement_execution_count
gpu_command_submission_count
performance_claim_count
```

---

# 14. Required Predicates

```text
TCU_REPLACE_04_R2_PARENT_BINDING_PASS
TCU_REPLACE_04_R2_BASE_GRAPH_TOPOLOGY_UNCHANGED
TCU_REPLACE_04_R2_ACTIVE_EDGE_ALLOWLIST_EXACT
TCU_REPLACE_04_R2_EXECUTABLE_EDGE_COUNT_ZERO
TCU_REPLACE_04_R2_ACTIVE_BINDING_PASS
TCU_REPLACE_04_R2_ACTIVE_REQUEST_PASS
TCU_REPLACE_04_R2_ACTIVE_AUTHORIZATION_PASS
TCU_REPLACE_04_R2_ACTIVE_ROLLBACK_PASS
TCU_REPLACE_04_R2_ACTIVE_TRANSACTION_PREPARED
TCU_REPLACE_04_R2_ACTIVE_DRY_RUN_PASS
TCU_REPLACE_04_R2_FIXTURE_ISOLATION_PASS
TCU_REPLACE_04_R2_NEGATIVE_FIXTURES_PASS
TCU_REPLACE_04_R2_PREPARED_STORE_READINESS_TRUE
TCU_REPLACE_04_R2_APPLY_READINESS_FALSE
TCU_REPLACE_04_R2_ROUTE_OWNERSHIP_READINESS_FALSE
TCU_REPLACE_04_R2_REPLACE_05_STORE_ONLY_READINESS_TRUE
TCU_REPLACE_04_R2_NO_RUNTIME_SNAPSHOT_MUTATION
TCU_REPLACE_04_R2_NO_ACTIVE_ROUTE_MUTATION
TCU_REPLACE_04_R2_NO_PRODUCTION_REPLACEMENT
TCU_REPLACE_04_R2_STATIC_CHECKS_PASS
```

---

# 15. Required Runtime Outputs

```text
workspace/runtime/tensorcube/
  ash_tcu_replace_04_r2_active_edge_audit_runtime_artifact.json
  ash_tcu_replace_04_r2_parent_binding_receipt.json
  ash_tcu_replace_04_r2_active_composition_root_binding_receipt.json
  ash_tcu_replace_04_r2_base_graph_preservation_receipt.json
  ash_tcu_replace_04_r2_active_edge_eligibility_registry.json
  ash_tcu_replace_04_r2_active_transition_request_receipt.json
  ash_tcu_replace_04_r2_active_authorization_anchor_receipt.json
  ash_tcu_replace_04_r2_active_rollback_anchor_receipt.json
  ash_tcu_replace_04_r2_active_prepared_transaction_receipt.json
  ash_tcu_replace_04_r2_active_dry_run_receipt.json
  ash_tcu_replace_04_r2_fixture_isolation_audit.json
  ash_tcu_replace_04_r2_negative_fixture_receipt.json
  ash_tcu_replace_04_r2_readiness_scope_receipt.json
  ash_tcu_replace_04_r2_runtime_snapshot_preservation_receipt.json
  ash_tcu_replace_04_r2_no_active_route_mutation_guard.json
  ash_tcu_replace_04_r2_no_production_replacement_guard.json
  ash_tcu_replace_04_r2_no_gpu_behavior_change_guard.json
  ash_tcu_replace_04_r2_output_parity_status.json
  ash_tcu_replace_04_r2_no_performance_claim_guard.json
  ash_tcu_replace_04_r2_static_checks.json
  ash_tcu_replace_04_r2_verdict.json

artifacts/
  ASH_TCU_REPLACE_04_R2_LOCAL_MANIFEST.json
```

---

# 16. Output-Parity Honesty

R2 does not execute decode or training output parity.

```text
executed_output_parity=false
executed_output_parity_status=not_executed_static_no_change_evidence_only
```

Static no-mutation evidence must not be represented as executed output equality.

---

# 17. PASS and HOLD

PASS:

```text
PASS_ASH_TCU_REPLACE_04_R2_ACTIVE_COMPOSITION_ROOT_ELIGIBLE_EDGE_AUDITED_DISABLED_TO_SHADOW_DRY_RUN_PREPARATION_CONTRACT_ESTABLISHED_REPOSITORY_SNAPSHOT_BOUND_TRANSITION_REQUEST_PROVEN_ACTIVE_DOMAIN_AUTHORIZATION_AND_ROLLBACK_EVIDENCE_BOUND_ACTIVE_AND_FIXTURE_TRANSACTION_AUTHORITY_ISOLATED_PREPARED_TRANSITION_STORE_ONLY_READINESS_OPENED_NO_RUNTIME_SNAPSHOT_MUTATION_NO_ACTIVE_ROUTE_MUTATION_NO_PRODUCTION_REPLACEMENT
```

HOLD:

```text
HOLD_ASH_TCU_REPLACE_04_R2_ACTIVE_EDGE_SNAPSHOT_AUTHORIZATION_ROLLBACK_OR_READINESS_SCOPE_INCOMPLETE
```

Recommended next patch:

```text
ASH-TCU-REPLACE-05

Prepared Transition Store /
Single-Use Transaction Consumption Contract /
Authorization Freshness and Replay Gate /
Rollback Precondition Revalidation /
Active-Domain Dry-Run Transaction Persistence /
No Apply Execution /
No Route Ownership /
No Default Route Mutation /
No Production Replacement Seal
```

---

# Final Seal

R2 passes only when the repository can truthfully state:

```text
The active composition-root snapshot is the sole authority for
the Disabled-to-ShadowOnly dry-run transaction.

The active snapshot remains Disabled with digest f6cc60a0...

The 11-edge base graph is unchanged.

Exactly one active R2 eligibility exists.

One active-domain transaction is prepared.

The transaction is store eligible and apply ineligible.

The transaction has no prior transaction.

Authorization grants preparation only.

Rollback targets Disabled.

Missing route evidence is explicit and not fabricated.

No fixture evidence enters active readiness.

No runtime snapshot, route, registry, epoch, output authority,
production state, GPU behavior, or performance claim changes.

REPLACE-05 readiness opens only for prepared transaction storage
and single-use consumption semantics.
```
