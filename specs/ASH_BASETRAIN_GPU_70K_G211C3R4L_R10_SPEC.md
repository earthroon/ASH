# G211C3R4L-R10
## Limited Shadow Enable Gate / Manual Opt-In Candidate Cache Runtime Policy Seal

## Scope

G211C3R4L-R10 consumes the G211C3R4L-R9 shadow observe stability ledger and creates a limited manual opt-in gate for candidate cache runtime policy execution. R10 keeps the default policy disabled, forbids automatic promotion, and allows candidate cache runtime policy only inside an explicit audit-scoped opt-in run.

R10 does not adopt the cache policy as default production runtime behavior, does not persist manual opt-in after the audit run, does not open the runtime splice, and does not declare a performance winner.

## Parent seal

```text
parent_patch_id = G211C3R4L-R9
parent_verdict = PASS_G211C3R4L_R9_SHADOW_OBSERVE_STABILITY_LEDGER_SEALED
parent_default_shadow_mode = PipelineBuffersBindGroupCachedShadow
parent_optional_shadow_mode = FullCandidateResourceCachedShadow
shadow_policy_runtime_adopted = false
shadow_output_committed = false
committed_output_owner_unchanged = true
runtime splice remains closed
performance_winner_declared = false
```

## Core principle

```text
Manual opt-in is allowed.
Default adoption is forbidden.
Automatic promotion is forbidden.
```

Default runtime remains:

```text
default_runtime_policy = ExistingRuntimePrimaryPath
manual_opt_in_policy = CandidateCacheLimitedRuntimePolicy
```

Required:

```text
default_policy_disabled = true
manual_opt_in_required = true
automatic_promotion_allowed = false
default_runtime_policy_unchanged = true
```

## Manual opt-in contract

Manual opt-in requires an explicit flag.

```text
--manual-opt-in-cache-policy
```

Without the flag:

```text
manual_opt_in_requested = false
manual_opt_in_enabled = false
candidate_cache_runtime_policy_enabled = false
default_policy_disabled = true
```

With the flag:

```text
manual_opt_in_requested = true
manual_opt_in_enabled = true only if all opt-in gates pass
candidate_cache_runtime_policy_enabled = true only inside audit scope
```

Forbidden:

```text
manual opt-in inferred from R9 PASS
manual opt-in inferred from performance delta
manual opt-in inferred from optional full-cache ledger
manual opt-in enabled by default config
manual opt-in persisted after audit
```

## Candidate runtime policy modes

Default manual opt-in mode:

```text
PipelineBuffersBindGroupCachedManualOptIn
```

Optional manual opt-in mode:

```text
FullCandidateResourceCachedManualOptIn
```

Optional full-cache opt-in is allowed only by explicit flag.

```text
--optional-full-cache-opt-in
```

Optional full-cache opt-in must never become default.

## Candidate storage layout

Candidate shader storage layout remains the QW-55A-0-R3 four-storage-buffer control_words layout.

```text
binding(0): A atlas
binding(1): B atlas
binding(2): C atlas
binding(3): control_words
```

Forbidden:

```text
candidate fifth storage binding
tile_id_table as separate storage binding
parent R3 candidate shader mutation
timestamp resources as shader storage binding
readback resources as shader storage binding
```

## Opt-in gate contract

Required before enable:

```text
parent_r9_ledger_passed = true
selected_manual_opt_in_mode_present = true
manual_opt_in_requested = true
manual_opt_in_gate_passed = true
candidate_cache_runtime_policy_enabled = true
default_policy_disabled_before_opt_in = true
```

Safety gates:

```text
correctness_gate_passed = true
timestamp_gate_passed = true
guard_gate_passed = true
ownership_gate_passed = true
off_switch_gate_passed = true
rollback_gate_passed = true
```

Mutation gates:

```text
decode_path_mutated = false
backend_policy_mutated = false
sft_pass1_path_mutated = false
model_weights_mutated = false
```

Default adoption gates:

```text
default_runtime_policy_adopted = false
automatic_promotion_allowed = false
manual_opt_in_persisted_after_run = false
```

## Output ownership contract

Without manual opt-in:

```text
committed_output_owner = ExistingRuntimePrimaryPath
candidate_policy_output_owner = CandidateCacheManualOptInPath
candidate_policy_output_committed = false
```

With manual opt-in audit scope:

```text
committed_output_owner = ManualOptInCandidateCachePath
manual_opt_in_scope = AuditOnly
default_runtime_policy_unchanged = true
manual_opt_in_output_committed = true
default_runtime_output_replaced = false
default_runtime_policy_adopted = false
manual_opt_in_persisted_after_run = false
```

Forbidden:

```text
manual opt-in output becomes default output after audit
manual opt-in output mutates decode path
manual opt-in output mutates logits path
manual opt-in output mutates backend global policy
manual opt-in output persists into next run without explicit flag
```

## Correctness contract

R10 compares manual opt-in candidate output against:

```text
CPU reference
Burn baseline
ColdCreateEveryIteration output
R9 shadow ledger output
Existing runtime primary output
```

Required:

```text
manual_opt_in_cpu_mismatch_count = 0
manual_opt_in_burn_mismatch_count = 0
manual_opt_in_cold_mismatch_count = 0
manual_opt_in_parent_r9_mismatch_count = 0
manual_opt_in_primary_output_mismatch_count = 0
manual_opt_in_nan_count = 0
manual_opt_in_inf_count = 0
```

Tolerance:

```text
abs_tolerance = 1e-4
rel_tolerance = 1e-4
```

## Guard contract

Required guards:

```text
output_stale_read_guard_passed = true
control_words_freshness_guard_passed = true
timestamp_freshness_guard_passed = true
bind_group_identity_guard_passed = true
manual_opt_in_explicit_flag_guard_passed = true
manual_opt_in_scope_guard_passed = true
manual_opt_in_no_persist_guard_passed = true
default_policy_disabled_guard_passed = true
runtime_mutation_guard_passed = true
rollback_guard_passed = true
```

Optional full-cache additional guards:

```text
readback_freshness_guard_passed = true
timestamp_resource_reuse_guard_passed = true
readback_resource_reuse_guard_passed = true
full_cache_not_default_guard_passed = true
```

## Timestamp continuity

Required:

```text
timestamp_query_created = true
timestamp_query_resolved = true
timestamp_readback_mapped = true
timestamp_period_ns_present = true
timestamp_ticks_resolved = true
timestamp_us_converted = true
missing_timestamp_markers = []
timestamp_marker_coverage_ratio = 1.0
```

## Rollback / off-switch contract

Rollback target:

```text
policy_state = Disabled
candidate_cache_runtime_policy_enabled = false
manual_opt_in_requested = false
manual_opt_in_enabled = false
committed_output_owner = ExistingRuntimePrimaryPath
```

Required:

```text
rollback_available = true
rollback_restores_disabled_state = true
rollback_restores_existing_runtime_primary_owner = true
rollback_does_not_change_primary_output = true
rollback_does_not_mutate_backend_policy = true
rollback_does_not_mutate_decode_path = true
rollback_does_not_mutate_sft_pass1_path = true
rollback_does_not_mutate_model_weights = true
manual_opt_in_persisted_after_run = false
default_runtime_policy_adopted = false
```

## Fixture contract

```text
k_panel_count = 1 -> M=16 N=16 K=8
k_panel_count = 2 -> M=16 N=16 K=16
k_panel_count = 4 -> M=16 N=16 K=32
k_panel_count = 8 -> M=16 N=16 K=64
same_input_ssot_used = true
input_ssot_hash_matches_parent_r9 = true
```

## Measurement policy

```text
warmup_iterations >= 5
measure_iterations >= 30
outlier_policy = trim_min_max_one_each_if_samples_ge_10
raw_samples_retained = true
summary_stats_computed = true
```

R10 records timing only.

```text
speedup_required_for_pass = false
performance_winner_declared = false
```

## Local artifacts

Generated locally only:

```text
workspace/runtime/tensorcube/g211c3r4l_r10_manual_opt_in_policy_latest.json
workspace/runtime/tensorcube/g211c3r4l_r10_manual_opt_in_gate_latest.json
workspace/runtime/tensorcube/g211c3r4l_r10_manual_opt_in_correctness_latest.json
workspace/runtime/tensorcube/g211c3r4l_r10_manual_opt_in_rollback_latest.json
workspace/runtime/tensorcube/g211c3r4l_r10_limited_shadow_enable_gate_receipt_latest.json
artifacts/g211c3r4l_r10_limited_shadow_enable_gate_local_manifest.json
```

These files are not committed.

## Audit commands

Default dry run, should stay disabled:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin g211c3r4l_r10_limited_shadow_enable_gate_audit
```

Manual opt-in conservative mode:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin g211c3r4l_r10_limited_shadow_enable_gate_audit -- --require-native-adapter --k-panels 1,2,4,8 --warmup 5 --measure 30 --manual-opt-in-cache-policy --manual-opt-in-mode pipeline-buffers-bindgroup
```

Manual opt-in with optional full-cache candidate:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin g211c3r4l_r10_limited_shadow_enable_gate_audit -- --require-native-adapter --k-panels 1,2,4,8 --warmup 5 --measure 30 --manual-opt-in-cache-policy --manual-opt-in-mode pipeline-buffers-bindgroup --optional-full-cache-opt-in
```

Blocked mode test, no explicit opt-in:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin g211c3r4l_r10_limited_shadow_enable_gate_audit -- --require-native-adapter --k-panels 1,2,4,8 --warmup 5 --measure 30 --manual-opt-in-mode pipeline-buffers-bindgroup
```

Expected blocked verdict:

```text
PASS_G211C3R4L_R10_MANUAL_OPT_IN_BLOCKED_DISABLED_SEAL
```

Expected enabled verdict:

```text
PASS_G211C3R4L_R10_LIMITED_SHADOW_ENABLE_GATE_SEALED
```

## PASS conditions

Required enabled run:

```text
parent_patch_id = G211C3R4L-R9
parent_verdict = PASS_G211C3R4L_R9_SHADOW_OBSERVE_STABILITY_LEDGER_SEALED
selected_default_manual_opt_in_mode = PipelineBuffersBindGroupCachedManualOptIn
manual_opt_in_requested = true
manual_opt_in_enabled = true
default_policy_disabled = true
default_runtime_policy_adopted = false
automatic_promotion_allowed = false
same_input_ssot_used = true
input_ssot_hash_matches_parent_r9 = true
cpu_reference_used_for_correctness_only = true
cpu_reference_used_as_benchmark_baseline = false
correctness_gate_passed = true
timestamp_gate_passed = true
guard_gate_passed = true
ownership_gate_passed = true
rollback_gate_passed = true
rollback_restores_disabled_state = true
manual_opt_in_persisted_after_run = false
speedup_required_for_pass = false
performance_winner_declared = false
runtime_inference_replacement_allowed = false
backend_policy_connection_allowed = false
hardware_tensorcore_claimed = false
```

## Failure conditions

```text
FAIL: parent_patch_id != G211C3R4L-R9
FAIL: parent R9 verdict is not PASS
FAIL: selected_default_manual_opt_in_mode missing
FAIL: selected_default_manual_opt_in_mode is not PipelineBuffersBindGroupCachedManualOptIn
FAIL: manual_opt_in_requested = false in opt-in run
FAIL: manual_opt_in_enabled = true without explicit flag
FAIL: manual_opt_in_enabled = true while opt-in gate failed
FAIL: default_policy_disabled = false
FAIL: default_runtime_policy_adopted = true
FAIL: automatic_promotion_allowed = true
FAIL: manual opt-in persists after run
FAIL: rollback receipt missing
FAIL: rollback does not restore disabled state
FAIL: rollback does not restore existing runtime primary owner
FAIL: default runtime output replaced
FAIL: decode path mutated
FAIL: backend policy mutated
FAIL: SFT pass1 path mutated
FAIL: model weights mutated
FAIL: runtime inference replacement allowed
FAIL: input SSOT differs from parent R9
FAIL: CPU reference used as benchmark baseline
FAIL: manual opt-in CPU mismatch > 0
FAIL: manual opt-in Burn mismatch > 0
FAIL: manual opt-in cold mismatch > 0
FAIL: manual opt-in parent R9 mismatch > 0
FAIL: manual opt-in primary output mismatch > 0
FAIL: NaN detected
FAIL: Inf detected
FAIL: timestamp markers missing
FAIL: timestamp marker coverage < 1.0
FAIL: output stale readback detected
FAIL: control_words not fresh for fixture
FAIL: timestamp readback contains stale iteration data
FAIL: bind group identity mismatch
FAIL: optional full-cache opt-in enabled without explicit flag
FAIL: full-cache opt-in selected as default
FAIL: performance_winner_declared = true
FAIL: speedup_required_for_pass = true
FAIL: hardware_tensorcore_claimed = true
FAIL: candidate uses fifth storage binding
```
