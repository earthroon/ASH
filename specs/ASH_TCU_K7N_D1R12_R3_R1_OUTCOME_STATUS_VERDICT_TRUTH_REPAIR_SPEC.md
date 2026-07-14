# ASH-TCU-K7N-D1R12-R3-R1 SPEC

## Outcome / Status / Verdict Truth Repair

## 1. Patch Identity

- Patch ID: `ASH-TCU-K7N-D1R12-R3-R1_OUTCOME_STATUS_VERDICT_TRUTH_REPAIR`
- Normal PASS marker: `PASS_ASH_TCU_K7N_D1R12_R3_R1_OUTCOME_STATUS_VERDICT_TRUTH_REPAIR_REGRESSION_TRUTH_RESTORED_PARENT_IMMUTABLE`
- Hard failure marker: `FAIL_ASH_TCU_K7N_D1R12_R3_R1_OUTCOME_STATUS_VERDICT_TRUTH_REPAIR_TRUTH_MAPPING_OR_PARENT_PROTECTED_STATE_VIOLATION`
- GitHub path: `specs/ASH_TCU_K7N_D1R12_R3_R1_OUTCOME_STATUS_VERDICT_TRUTH_REPAIR_SPEC.md`

Patch class:

```text
outcome truth projection repair
+ status marker ownership repair
+ verdict derivation SSOT
+ CLI exit-disposition repair
+ cross-artifact truth parity gate
+ historical parent mismatch receipt
+ future D1R12-R3 emission repair
+ no replay rerun
+ no parent artifact rewrite
+ no registry mutation
+ no production promotion
```

## 2. Direct Parent

Required parent:

```text
ASH-TCU-K7N-D1R12-R3_REPAIRED_CANARY_HEALTH_REPLAY
execution_id=d1r12-r3-6458db8a777cd4f936c5
selected_outcome=repaired_policy_regression
```

Required parent evidence:

```text
active_route_count=17
replay_attempt_count=49152
replay_failure_count=0
parity_sample_count=544
parity_failing_sample_count=0
restart_count=2
replay_bucket_count=1401
healthy_route_count=11
amber_route_count=1
conditional_hold_route_count=0
confirmed_hold_route_count=0
observation_hold_route_count=5
invalid_route_count=0
false_hold_count=0
classification_drift_count=6
deterministic_recompute=true
route_epoch_before=1
route_epoch_after=1
output_authority=burn
tensorcube_authoritative_output_count=0
shadow_output_commit_count=0
production_output_commit_count=0
runtime_output_changed=false
```

## 3. Confirmed Parent Truth Conflict

The parent emitted the normal PASS marker and normal PASS verdict while also sealing:

```text
selected_outcome=repaired_policy_regression
healthy_route_count=11
observation_hold_route_count=5
classification_drift_count=6
```

The selected outcome and evidence counters are authoritative. The parent normal PASS marker and normal PASS verdict are invalid projections of that evidence.

## 4. Purpose

D1R12-R3-R1 repairs the projection boundary from one selected outcome into:

```text
terminal status marker
outcome marker
verdict
report status
final-seal status
local-manifest status
console output
process exit code
next-state contract
```

The patch must prove:

```text
one selected outcome maps to exactly one terminal status
one selected outcome maps to exactly one verdict
one selected outcome maps to exactly one exit disposition
all truth-bearing artifacts consume one immutable truth envelope
normal PASS is impossible for a non-normal outcome
historical parent artifacts remain immutable
future D1R12-R3 executions use the repaired projection
```

## 5. State Ownership

D1R12-R3 owns replay evidence, route and bucket health, parity, restart evidence, determinism evidence, protected-state evidence and the selected outcome.

D1R12-R3-R1 owns:

```text
parent truth-conflict audit
canonical outcome-to-status mapping
canonical outcome-to-verdict mapping
canonical outcome-to-exit mapping
canonical truth envelope
historical correction receipt
future source projection repair
cross-artifact truth parity audit
R3-R1 report, verdict, final seal and manifest
```

D1R12-R3-R1 does not own route classification, bucket classification, replay scheduling, aggregation thresholds, registry state, route epoch, Burn output, TensorCube output, sampler ownership, KV ownership or parent artifacts.

## 6. Explicit Non-Goals

This patch does not authorize:

- replay rerun;
- replay attempt expansion;
- observation-hold or amber reclassification;
- aggregation threshold or precedence changes;
- sample-floor relaxation;
- route membership or route epoch mutation;
- whitelist expansion or holdlist promotion;
- TensorCube authoritative output;
- shadow or production output commit;
- sampler substitution;
- KV mutation;
- D1R13 promotion;
- parent artifact rewrite, deletion or replacement.

## 7. Two-Axis Truth Model

Execution integrity and health outcome are separate axes.

```rust
pub enum D1R12R3OutcomeClass {
    NormalPass,
    BoundedHold,
    PolicyRegressionFailure,
    RuntimeFailure,
    ParentEvidenceFailure,
}
```

A replay may complete deterministically while selecting a regression. Therefore:

```text
execution_completed=true
!=
normal_health_pass=true
```

## 8. Canonical Truth Envelope

```rust
pub struct D1R12R3TruthEnvelope {
    pub selected_outcome: String,
    pub outcome_class: D1R12R3OutcomeClass,
    pub execution_completed: bool,
    pub normal_pass: bool,
    pub promotion_blocked: bool,
    pub terminal_status_marker: String,
    pub outcome_marker: String,
    pub verdict: String,
    pub process_exit_code: u8,
    pub next_patch: String,
    pub summary_digest: String,
    pub outcome_evidence_digest: String,
    pub truth_projection_digest: String,
    pub receipt_digest: String,
}
```

Required derivation:

```text
selected outcome
-> validate evidence compatibility
-> derive one truth envelope
-> report / verdict / final seal / console / exit code / manifest
```

Independent status or verdict construction outside the truth owner is forbidden.

## 9. Canonical Outcome Mapping

### Repaired Health Reproduced

```text
class=normal_pass
status=PASS_ASH_TCU_K7N_D1R12_R3_REPAIRED_CANARY_HEALTH_REPLAY_SEVENTEEN_ROUTES_HEALTHY_FALSE_HOLD_ZERO_REGISTRY_UNCHANGED
exit_code=0
next=ASH-TCU-K7N-D1R12-R4_REPAIRED_CANARY_SUSTAINED_SOAK
```

Required evidence:

```text
healthy=17
amber=0
conditional_hold=0
confirmed_hold=0
observation_hold=0
invalid=0
false_hold=0
classification_drift=0
replay_failure=0
parity_failure=0
deterministic_recompute=true
```

### Bounded Amber Drift

```text
class=bounded_hold
status=HOLD_ASH_TCU_K7N_D1R12_R3_REPAIRED_CANARY_HEALTH_REPLAY_BOUNDED_AMBER_DRIFT_REQUIRES_ROUTE_SCOPE_REVIEW
exit_code=2
next=ASH-TCU-K7N-D1R12-R4_AMBER_ROUTE_SCOPE_REVIEW
```

### Repaired Policy Regression

```text
class=policy_regression_failure
status=FAIL_ASH_TCU_K7N_D1R12_R3_REPAIRED_CANARY_HEALTH_REPLAY_REPAIRED_POLICY_REGRESSION_NO_PROMOTION
exit_code=3
next=ASH-TCU-K7N-D1R12-R4_AGGREGATION_POLICY_REGRESSION_REPAIR
```

Required when any regression evidence exists, including observation hold, confirmed or conditional hold, invalid route, false hold, non-bounded classification drift, or failure to reproduce the repaired seventeen-route state.

### Runtime Replay Instability

```text
class=runtime_failure
status=FAIL_ASH_TCU_K7N_D1R12_R3_REPAIRED_CANARY_HEALTH_REPLAY_RUNTIME_REPLAY_INSTABILITY_NO_HEALTH_CLAIM
exit_code=4
next=ASH-TCU-K7N-D1R12-R4_REPLAY_RUNTIME_STABILITY_REPAIR
```

### Parent Evidence Inconsistent

```text
class=parent_evidence_failure
status=FAIL_ASH_TCU_K7N_D1R12_R3_REPAIRED_CANARY_HEALTH_REPLAY_PARENT_EVIDENCE_INCONSISTENT_NO_RUNTIME_CLAIM
exit_code=5
next=ASH-TCU-K7N-D1R12-R4_PARENT_EVIDENCE_RECONSTRUCTION
```

### Truth Projection Failure

```text
status=FAIL_ASH_TCU_K7N_D1R12_R3_REPAIRED_CANARY_HEALTH_REPLAY_OUTCOME_STATUS_VERDICT_TRUTH_MAPPING_VIOLATION
exit_code=70
```

Unknown, empty, duplicated or evidence-incompatible outcomes fail closed. No fallback may map to normal PASS.

## 10. Verdict Mapping

Each outcome owns one exact verdict. The normal PASS verdict may be emitted only for `repaired_health_reproduced`.

The repaired-policy-regression verdict is:

```text
the_d1r12_r3_repaired_canary_health_replay_completed_but_failed_to_reproduce_the_d1r12_r2_repaired_seventeen_route_health_state_because_route_classification_drift_observation_hold_or_repaired_policy_regression_remained_while_burn_output_authority_and_protected_runtime_registry_model_sampler_and_kv_state_were_preserved
```

## 11. Console Contract

The R3 binary emits in order:

```text
zero or more segment diagnostic markers
exactly one terminal status
exactly one outcome marker
exactly one verdict
canonical summary fields
execution ID
local manifest path
```

Segment PASS markers prove only segment execution. The terminal marker must be emitted after outcome selection and truth-envelope derivation.

## 12. Exit Semantics

The R3 replay binary must write safe diagnostic artifacts before returning non-zero outcome exit codes. Exit code `0` is forbidden unless all normal PASS conditions are satisfied.

The R3-R1 audit binary may return `0` when it correctly detects and repairs the historical projection defect. This does not convert the parent regression into a health PASS.

## 13. Historical Parent Preservation

Immutable parent root:

```text
artifacts/tensorcube/k7n_d1r12_r3/d1r12-r3-6458db8a777cd4f936c5/
```

Hash before and after:

```text
replay_summary
report
verdict
final_seal
local_manifest
route_health
health_drift
determinism_audit
protected_state_guard
```

Required:

```text
parent_artifact_rewrite_count=0
parent_artifact_delete_count=0
parent_artifact_digest_change_count=0
```

R3-R1 writes a correction receipt. It does not rewrite history.

## 14. Cross-Artifact Truth Parity

The following must agree across report, truth envelope, verdict, final seal, console projection and local manifest:

```text
selected_outcome
outcome_marker
outcome_class
normal_pass
terminal_status
verdict
process_exit_code
next_patch
truth_projection_digest
```

Any conflict is a hard failure.

## 15. Source Ownership

Canonical truth ownership:

```text
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r12_r3_truth_projection.rs
```

The source audit must prove:

```text
derive_d1r12_r3_truth_envelope call present
unconditional normal PASS print absent
static normal verdict call absent
truth terminal status used by console and artifacts
truth exit code used by process termination
```

## 16. Protected State

Hash or preserve:

- active route registry and route epoch;
- aggregation policy;
- whitelist and holdlist;
- K7N shader and ABI;
- pipeline layout;
- Burn source;
- model weights;
- sampler and KV contracts;
- all parent R3 artifacts.

Allowed changes are limited to R3 truth-projection source, R3-R1 audit source, module/bin registration, tests and R3-R1 runtime artifacts produced locally.

## 17. Required Implementation Files

Backend:

```text
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r12_r3_truth_projection.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r12_r3_r1_truth_repair.rs
```

Modified backend:

```text
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r12_r3_replay_summary.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r12_r3_contract_audit.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r12_r3_verdict.rs
crates/burn_webgpu_backend/src/lib.rs
```

Model core:

```text
crates/model_core/src/vocab_atlas_shadow_repaired_canary_truth_projection_contract.rs
crates/model_core/src/lib.rs
```

Orchestrator:

```text
crates/orchestrator_local/src/ash_tcu_k7n_d1r12_r3_r1_outcome_status_verdict_truth_repair_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7n_d1r12_r3_r1_outcome_status_verdict_truth_repair.rs
```

Modified orchestrator:

```text
crates/orchestrator_local/src/ash_tcu_k7n_d1r12_r3_repaired_canary_health_replay_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7n_d1r12_r3_repaired_canary_health_replay.rs
crates/orchestrator_local/Cargo.toml
```

## 18. Required Runtime Artifacts

Immutable root:

```text
artifacts/tensorcube/k7n_d1r12_r3_r1/<execution_id>/
```

Latest mirrors:

```text
workspace/runtime/tensorcube/ash_tensorcube_k7n_d1r12_r3_r1_parent_truth_snapshot_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7n_d1r12_r3_r1_parent_conflict_audit_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7n_d1r12_r3_r1_outcome_status_map_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7n_d1r12_r3_r1_outcome_verdict_map_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7n_d1r12_r3_r1_exit_disposition_map_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7n_d1r12_r3_r1_canonical_truth_envelope_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7n_d1r12_r3_r1_historical_truth_repair_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7n_d1r12_r3_r1_console_projection_audit_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7n_d1r12_r3_r1_cross_artifact_truth_audit_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7n_d1r12_r3_r1_source_ownership_audit_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7n_d1r12_r3_r1_protected_state_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7n_d1r12_r3_r1_report_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7n_d1r12_r3_r1_verdict_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7n_d1r12_r3_r1_final_seal_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7n_d1r12_r3_r1_local_manifest_latest.json
```

These artifacts and the manifest must be generated by the local Rust audit binary. They must not be pre-baked into the code archive or committed to GitHub.

## 19. Required Tests

1. parent execution and all evidence counters exact;
2. parent PASS status conflict reproduced;
3. parent normal verdict conflict reproduced;
4. normal PASS contract violation reproduced;
5. each of five outcomes maps to one unique status;
6. each outcome maps to one unique verdict;
7. exit codes are `0,2,3,4,5`, truth failure `70`;
8. regression cannot return `0`;
9. unknown or evidence-incompatible outcome fails closed;
10. segment markers cannot become terminal status;
11. report, verdict, final seal and truth envelope agree;
12. unconditional normal PASS emission absent;
13. static normal verdict emission absent;
14. parent artifacts remain byte-identical;
15. registry, epoch, policy, shader, ABI, pipeline, Burn, model, sampler and KV state unchanged;
16. output authority remains Burn.

## 20. Required Audit Command

```powershell
cargo run --manifest-path .\crates\orchestrator_local\Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k7n_d1r12_r3_r1_outcome_status_verdict_truth_repair -- `
  --repo-root "D:\1111113232\DUST\1\ash_pass3" `
  --require-parent-r3-execution "d1r12-r3-6458db8a777cd4f936c5" `
  --require-parent-selected-outcome "repaired_policy_regression" `
  --require-parent-active-route-count "17" `
  --require-parent-replay-attempt-count "49152" `
  --require-parent-replay-failure-count "0" `
  --require-parent-parity-sample-count "544" `
  --require-parent-parity-failure-count "0" `
  --require-parent-restart-count "2" `
  --require-parent-replay-bucket-count "1401" `
  --require-parent-healthy-route-count "11" `
  --require-parent-amber-route-count "1" `
  --require-parent-conditional-hold-count "0" `
  --require-parent-confirmed-hold-count "0" `
  --require-parent-observation-hold-count "5" `
  --require-parent-invalid-route-count "0" `
  --require-parent-false-hold-count "0" `
  --require-parent-classification-drift-count "6" `
  --require-parent-deterministic-recompute `
  --require-parent-route-epoch-before "1" `
  --require-parent-route-epoch-after "1" `
  --require-parent-output-authority "burn" `
  --require-parent-tensorcube-authoritative-output-count "0" `
  --require-parent-shadow-output-commit-count "0" `
  --require-parent-production-output-commit-count "0" `
  --require-parent-runtime-output-unchanged `
  --load-parent-r3-replay-summary `
  --load-parent-r3-report `
  --load-parent-r3-verdict `
  --load-parent-r3-final-seal `
  --load-parent-r3-local-manifest `
  --load-parent-r3-route-health `
  --load-parent-r3-health-drift `
  --load-parent-r3-determinism-audit `
  --load-parent-r3-protected-state-guard `
  --audit-parent-status-outcome-conflict `
  --audit-parent-verdict-outcome-conflict `
  --audit-parent-normal-pass-contract `
  --derive-canonical-truth-envelope `
  --require-derived-outcome-class "policy_regression_failure" `
  --require-derived-terminal-status "FAIL_ASH_TCU_K7N_D1R12_R3_REPAIRED_CANARY_HEALTH_REPLAY_REPAIRED_POLICY_REGRESSION_NO_PROMOTION" `
  --require-derived-exit-code "3" `
  --require-derived-next-patch "ASH-TCU-K7N-D1R12-R4_AGGREGATION_POLICY_REGRESSION_REPAIR" `
  --audit-all-five-outcome-mappings `
  --audit-terminal-status-uniqueness `
  --audit-verdict-uniqueness `
  --audit-exit-disposition-uniqueness `
  --audit-next-state-uniqueness `
  --audit-cross-artifact-truth-parity `
  --audit-console-projection-contract `
  --audit-source-truth-owner `
  --require-no-unconditional-normal-pass-emission `
  --require-no-static-normal-verdict-emission `
  --require-parent-artifacts-unchanged `
  --require-route-registry-unchanged `
  --require-route-epoch-unchanged `
  --require-aggregation-policy-unchanged `
  --verify-k7n-shader-unchanged `
  --verify-k7n-abi-unchanged `
  --verify-pipeline-layout-unchanged `
  --verify-burn-source-unchanged `
  --verify-model-weights-unchanged `
  --verify-sampler-contract-unchanged `
  --verify-kv-contract-unchanged `
  --write-parent-truth-snapshot `
  --write-parent-conflict-audit `
  --write-outcome-status-map `
  --write-outcome-verdict-map `
  --write-exit-disposition-map `
  --write-canonical-truth-envelope `
  --write-historical-truth-repair-receipt `
  --write-console-projection-audit `
  --write-cross-artifact-truth-audit `
  --write-source-ownership-audit `
  --write-protected-state-guard `
  --write-report `
  --write-verdict `
  --write-final-seal `
  --no-replay-rerun `
  --no-parent-artifact-rewrite `
  --no-route-health-reclassification `
  --no-active-route-mutation `
  --no-canary-promotion `
  --no-production-output-promotion `
  --no-production-claim
```

## 21. Expected R3-R1 Result

```text
parent_status_outcome_conflict_detected=true
parent_verdict_outcome_conflict_detected=true
parent_normal_pass_contract_violated=true
derived_outcome_class=policy_regression_failure
derived_normal_pass=false
derived_promotion_blocked=true
derived_exit_code=3
derived_next_patch=ASH-TCU-K7N-D1R12-R4_AGGREGATION_POLICY_REGRESSION_REPAIR
parent_artifacts_unchanged=true
future_r3_projection_repaired=true
output_authority=burn
runtime_output_changed=false
```

## 22. PASS Meaning

R3-R1 PASS means the historical projection conflict was reproduced, the authoritative regression outcome was preserved, future R3 output surfaces now derive from one truth envelope, and parent/protected state remained immutable.

It does not mean that the five observation holds, one amber route or six classification drifts were repaired.

## 23. Normal PASS Verdict

```text
the_d1r12_r3_r1_truth_repair_reproduced_the_historical_parent_status_outcome_and_verdict_conflict_preserved_the_authoritative_repaired_policy_regression_outcome_derived_one_canonical_failure_status_verdict_exit_disposition_and_next_state_repaired_future_d1r12_r3_truth_projection_and_left_all_parent_replay_registry_policy_shader_abi_pipeline_model_sampler_kv_and_burn_output_authority_state_unchanged
```

## 24. Next-State Contract

On R3-R1 PASS, authorize drafting only:

```text
ASH-TCU-K7N-D1R12-R4_AGGREGATION_POLICY_REGRESSION_REPAIR
```

Carry forward defect:

```text
replay_bucket_coverage_floor_underallocation
```

No D1R13 or TensorCube production-output promotion is authorized.
