# ASH-BASETRAIN-GPU-70K-G90

## Delta Packet Adoption Dry-Run Execution / Adoption Candidate To Runtime Route Plan Seal

Seal: **No Weight Commit / No Checkpoint Mutation**

---

## 1. Patch Identity

```text
PatchId: ASH-BASETRAIN-GPU-70K-G90
SourcePatchId: ASH-BASETRAIN-GPU-70K-G89
PreviousPassTarget: PASS_ASH_BASETRAIN_GPU_70K_G89_DELTA_PACKET_STACK_ADOPTION_CANDIDATE_REVIEW_GATE
RuntimePassTarget: PASS_ASH_BASETRAIN_GPU_70K_G90_DELTA_PACKET_ADOPTION_DRY_RUN_EXECUTION
NextPatch: ASH-BASETRAIN-GPU-70K-G91
```

G90 transforms the G89 adoption candidate envelope into deterministic dry-run runtime route, adoption, and rollback scope plans. G90 does not actually adopt the delta packet, mutate the ledger, mutate runtime routes, mutate weights, commit weights, or mutate checkpoints.

---

## 2. SSOT Boundary

### State owner

```text
crates/base_train
artifacts/ASH_BASETRAIN_GPU_70K_G90_RUNTIME_ROUTE_PLAN.json
artifacts/ASH_BASETRAIN_GPU_70K_G90_ADOPTION_DRY_RUN_PLAN.json
artifacts/ASH_BASETRAIN_GPU_70K_G90_ROLLBACK_SCOPE_PLAN.json
```

### Input SSOT

```text
ASH_BASETRAIN_GPU_70K_G89_DELTA_PACKET_STACK_ADOPTION_CANDIDATE_REVIEW_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G89_DELTA_PACKET_ADOPTION_CANDIDATE_ENVELOPE.json
```

Recommended lineage inputs:

```text
ASH_BASETRAIN_GPU_70K_G88_DELTA_PACKET_STACK_APPEND_READBACK_AND_REPLAY_INTEGRITY_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G87_DELTA_PACKET_STACK_APPEND_EXECUTION_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G86_DELTA_PACKET_STACK_APPEND_DRY_RUN_RECEIPT.json
ASH_BASETRAIN_GPU_70K_DELTA_PACKET_STACK_LEDGER.json
```

### Output SSOT

```text
ASH_BASETRAIN_GPU_70K_G90_DELTA_PACKET_ADOPTION_DRY_RUN_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G90_RUNTIME_ROUTE_PLAN.json
ASH_BASETRAIN_GPU_70K_G90_ADOPTION_DRY_RUN_PLAN.json
ASH_BASETRAIN_GPU_70K_G90_ROLLBACK_SCOPE_PLAN.json
ASH_BASETRAIN_GPU_70K_G90_RUNTIME_ROUTE_PLAN_SCHEMA_AUDIT.json
ASH_BASETRAIN_GPU_70K_G90_ADOPTION_DRY_RUN_LINEAGE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G90_ADOPTION_BOUNDARY_AUDIT.json
ASH_BASETRAIN_GPU_70K_G90_NO_ACTUAL_ADOPTION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G90_NO_LEDGER_MUTATION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G90_NO_WEIGHT_MUTATION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G90_NO_CHECKPOINT_MUTATION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G90_NO_RUNTIME_ROUTE_MUTATION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G90_FORBIDDEN_CLAIM_AUDIT.json
```

### Reproducibility rule

```text
same G89 candidate digest + same selected group + same route policy = same route/adoption/rollback plan digests
```

---

## 3. Implementation Files

```text
crates/base_train/src/ash_basetrain_gpu_70k_g90_delta_packet_adoption_dry_run_execution.rs
crates/base_train/src/bin/ash_basetrain_gpu_70k_g90_delta_packet_adoption_dry_run_execution.rs
```

`crates/base_train/src/lib.rs` must export the G90 module, and `crates/base_train/Cargo.toml` must define the matching G90 bin target.

---

## 4. CLI Contract

Required:

```text
--g89-adoption-candidate-review-receipt <path>
--g89-adoption-candidate-envelope <path>
--selected-group-id <string>
--out-dir <path>
```

Recommended lineage:

```text
--g88-readback-replay-receipt <path>
--g87-append-execution-receipt <path>
--g86-dry-run-receipt <path>
--delta-packet-stack-ledger <path>
```

Optional:

```text
--g89-candidate-schema-audit <path>
--g89-candidate-lineage-audit <path>
--g89-candidate-boundary-audit <path>
--g89-no-actual-adoption-audit <path>
--g89-no-weight-mutation-audit <path>
--g89-no-checkpoint-mutation-audit <path>
--g89-no-runtime-route-mutation-audit <path>
--g89-forbidden-claim-audit <path>
--expected-predecessor-status <string>
--route-policy <string>
--route-label <string>
```

Default selected group:

```text
vocab_row_group__lm_head_weight
```

Default route policy:

```text
review_only_non_default_route_plan
```

---

## 5. Validation Gates

G90 must validate:

```text
g89.status == PASS_ASH_BASETRAIN_GPU_70K_G89_DELTA_PACKET_STACK_ADOPTION_CANDIDATE_REVIEW_GATE
g89.boundary_failures == 0
g89.candidate_envelope_created == true
g89.candidate_digest_stable == true
g89.ledger_entry_verified == true
g89.actual_delta_packet_adopted == false
g89.actual_weight_mutated == false
g89.actual_checkpoint_mutated == false
g89.runtime_default_route_mutated == false
g89.ledger_mutated_by_g89 == false
candidate.candidate_kind == delta_packet_stack_adoption_candidate
candidate.candidate_state == review_gate_only
candidate.candidate_digest == g89.candidate_digest
candidate digest recomputes stably
selected_group_id == vocab_row_group__lm_head_weight
route_policy == review_only_non_default_route_plan
```

If lineage inputs are provided, G90 also verifies G88/G87/G86 statuses and ledger digest chain. If not provided, G90 may run with `lineage_audit_strength == candidate_only`.

---

## 6. Allowed Writes

G90 may write only route plan, adoption dry-run plan, rollback scope plan, receipt, and audit artifacts.

Forbidden:

```text
actual delta packet adoption
ledger append/rewrite/delete
runtime route mutation
runtime default route mutation
runtime adapter route mutation
weight mutation
weight commit
checkpoint mutation
optimizer execution
training success claim
```

---

## 7. Route Plan Contract

Required route plan facts:

```text
plan_kind == delta_packet_adoption_runtime_route_plan
plan_state == dry_run_only
route_policy == review_only_non_default_route_plan
target_route_kind == non_default_candidate_route
target_route_mutation_allowed == false
default_route_mutation_allowed == false
runtime_route_mutated == false
runtime_default_route_mutated == false
actual_delta_packet_adopted == false
actual_weight_mutated == false
actual_weight_committed == false
actual_checkpoint_mutated == false
ledger_mutated_by_g90 == false
route_plan_digest is present
route_plan_digest_algorithm == fnv64_canonical_json_v1
route_plan_digest_stable == true
```

---

## 8. Receipt Contract

Required PASS status:

```text
PASS_ASH_BASETRAIN_GPU_70K_G90_DELTA_PACKET_ADOPTION_DRY_RUN_EXECUTION
```

Required PASS facts:

```text
g89_predecessor_status_verified == true
g89_candidate_envelope_verified == true
candidate_digest_verified == true
route_plan_created == true
route_plan_digest_stable == true
adoption_dry_run_plan_created == true
adoption_dry_run_plan_digest_stable == true
rollback_scope_plan_created == true
rollback_scope_plan_digest_stable == true
actual_delta_packet_adopted == false
actual_weight_mutated == false
actual_weight_committed == false
actual_checkpoint_mutated == false
runtime_route_mutated == false
runtime_default_route_mutated == false
ledger_mutated_by_g90 == false
boundary_failures == 0
```

---

## 9. Static Check Policy

Static checks must verify that the G90 source, bin, lib export, Cargo bin entry, route plan artifact path, adoption dry-run plan artifact path, rollback scope plan artifact path, digest stability checks, no-actual-adoption guard, no-ledger guard, no-weight guard, no-checkpoint guard, no-runtime-route guard, and forbidden callsite guards are present. The bake must exclude PowerShell scripts and sha256 sidecars.

If cargo/rustc is unavailable in the bake environment, validation must record `cargo_runtime_checked_in_bake_environment = false` and the reason.

---

## 10. Recommended Cargo Run

```powershell
$g89r = ".\\artifacts\\ASH_BASETRAIN_GPU_70K_G89_DELTA_PACKET_STACK_ADOPTION_CANDIDATE_REVIEW_RECEIPT.json"
$g89e = ".\\artifacts\\ASH_BASETRAIN_GPU_70K_G89_DELTA_PACKET_ADOPTION_CANDIDATE_ENVELOPE.json"
$g88r = ".\\artifacts\\ASH_BASETRAIN_GPU_70K_G88_DELTA_PACKET_STACK_APPEND_READBACK_AND_REPLAY_INTEGRITY_RECEIPT.json"
$g87r = ".\\artifacts\\ASH_BASETRAIN_GPU_70K_G87_DELTA_PACKET_STACK_APPEND_EXECUTION_RECEIPT.json"
$g86r = ".\\artifacts\\ASH_BASETRAIN_GPU_70K_G86_DELTA_PACKET_STACK_APPEND_DRY_RUN_RECEIPT.json"
$ledger = ".\\artifacts\\ASH_BASETRAIN_GPU_70K_DELTA_PACKET_STACK_LEDGER.json"

cargo run -p base_train --bin ash_basetrain_gpu_70k_g90_delta_packet_adoption_dry_run_execution -- `
  --g89-adoption-candidate-review-receipt $g89r `
  --g89-adoption-candidate-envelope $g89e `
  --g88-readback-replay-receipt $g88r `
  --g87-append-execution-receipt $g87r `
  --g86-dry-run-receipt $g86r `
  --delta-packet-stack-ledger $ledger `
  --selected-group-id vocab_row_group__lm_head_weight `
  --out-dir .\\artifacts
```

---

## 11. Next Patch

```text
ASH-BASETRAIN-GPU-70K-G91
Delta Packet Adoption Operator Approval Queue /
Dry-Run Runtime Route Plan To Explicit Adoption Approval Seal
No Weight Commit No Checkpoint Mutation
```
