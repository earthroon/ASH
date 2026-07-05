# G211C3R4L-R9
## Shadow Observe Stability Ledger / Repeated Disabled-By-Default Runtime Shadow Evidence Seal

## Scope

G211C3R4L-R9 consumes the G211C3R4L-R8 runtime shadow attach receipt and records repeated shadow observe evidence into a stability ledger. R9 repeats disabled-by-default shadow observation across multiple cycles and fixtures while preserving output ownership and the closed runtime splice.

R9 does not adopt the cache policy as production runtime behavior, does not commit shadow output, does not open the runtime splice, and does not declare a performance winner.

## Parent seal

```text
parent_patch_id = G211C3R4L-R8
parent_verdict = PASS_G211C3R4L_R8_CANDIDATE_CACHE_RUNTIME_SHADOW_ATTACH_SEALED
parent_default_shadow_mode = PipelineBuffersBindGroupCachedShadow
parent_optional_shadow_mode = FullCandidateResourceCachedShadow
default_shadow_policy_disabled = true
shadow_policy_runtime_adopted = false
shadow_output_committed = false
committed_output_owner_unchanged = true
performance_winner_declared = false
```

## Core principle

```text
Repeated shadow observation must never become runtime adoption.
```

Required ownership invariant:

```text
committed_output_owner = ExistingRuntimePrimaryPath
shadow_output_owner = CandidateCacheShadowPath
shadow_output_committed = false
committed_output_owner_unchanged = true
```

## Ledger run model

Default:

```text
ledger_cycle_count = 3
required_fixture_k_panels = [1, 2, 4, 8]
required_shadow_mode = PipelineBuffersBindGroupCachedShadow
optional_shadow_mode = FullCandidateResourceCachedShadow
```

Minimum PASS requirement:

```text
ledger_cycle_count >= 3
each_cycle_contains_all_required_fixtures = true
each_fixture_contains_shadow_receipt = true
each_cycle_contains_off_switch_replay = true
```

Each cycle records:

```text
cycle_id
run_id
adapter_fingerprint
policy_config_hash
input_ssot_hash
shadow_receipt_hash
off_switch_receipt_hash
ledger_entry_hash
```

## Policy state contract

Allowed states:

```text
Disabled
ShadowObserveOnly
ShadowBlocked
```

Forbidden state:

```text
RuntimeAdopted
```

Before each cycle:

```text
shadow_policy_enabled = false
default_shadow_policy_disabled = true
```

During each cycle:

```text
shadow_policy_enabled = true only when --enable-shadow-observe is explicitly supplied
```

After each cycle:

```text
off_switch_restores_disabled_state = true
shadow_policy_enabled_after_off_switch = false
```

Top-level PASS requires:

```text
default_shadow_policy_disabled = true
shadow_policy_runtime_adopted = false
shadow_policy_explicit_enable_required = true
```

## Shadow mode contract

Required default mode:

```text
PipelineBuffersBindGroupCachedShadow
```

Required behavior:

```text
pipeline_reused = true
bind_group_layout_reused = true
buffers_reused = true
bind_group_reused = true
timestamp_resources_reused = false
readback_resources_reused = false
```

Optional mode:

```text
FullCandidateResourceCachedShadow
```

Optional full-cache shadow is allowed only by explicit flag:

```text
--optional-full-cache-shadow
```

Optional mode must not become default.

```text
optional_full_cache_shadow_default = false
```

## Stability checks

### Output ownership stability

Across all cycles:

```text
shadow_output_committed = false
committed_output_owner_unchanged = true
runtime_inference_path_mutated = false
decode_path_mutated = false
backend_policy_mutated = false
sft_pass1_path_mutated = false
```

### Correctness stability

Across all cycles and fixtures:

```text
shadow_cpu_mismatch_count = 0
shadow_burn_mismatch_count = 0
shadow_parent_r8_mismatch_count = 0
shadow_cold_mismatch_count = 0
shadow_primary_output_mismatch_count = 0
shadow_nan_count = 0
shadow_inf_count = 0
```

### Timestamp stability

Across all cycles and fixtures:

```text
timestamp_marker_coverage_ratio = 1.0
missing_timestamp_markers = []
```

### Guard stability

Across all cycles and fixtures:

```text
output_stale_read_guard_passed = true
control_words_freshness_guard_passed = true
timestamp_freshness_guard_passed = true
bind_group_identity_guard_passed = true
shadow_no_commit_guard_passed = true
shadow_policy_default_off_guard_passed = true
shadow_output_ownership_guard_passed = true
runtime_mutation_guard_passed = true
```

### Off-switch stability

After every cycle:

```text
off_switch_available = true
off_switch_restores_disabled_state = true
off_switch_does_not_change_primary_output = true
off_switch_does_not_mutate_backend_policy = true
off_switch_does_not_mutate_decode_path = true
off_switch_does_not_mutate_sft_pass1_path = true
```

## Timing drift policy

R9 records timing drift but does not treat normal variance as failure.

Allowed observations:

```text
host_candidate_total_median_us_by_cycle
gpu_candidate_encoder_total_median_us_by_cycle
gpu_candidate_dispatch_body_median_us_by_cycle
host_p90_us_by_cycle
gpu_p90_us_by_cycle
host_timing_drift_ratio
gpu_timing_drift_ratio
```

R9 must not declare a performance winner.

```text
performance_winner_declared = false
speedup_required_for_pass = false
```

Timing drift becomes failure only when the measurement itself is invalid.

```text
FAIL: host timing samples missing
FAIL: gpu timestamp samples missing
FAIL: timestamp marker coverage < 1.0
FAIL: NaN timing stats
FAIL: negative timing stats
```

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

## Fixture contract

```text
k_panel_count = 1 -> M=16 N=16 K=8
k_panel_count = 2 -> M=16 N=16 K=16
k_panel_count = 4 -> M=16 N=16 K=32
k_panel_count = 8 -> M=16 N=16 K=64
same_input_ssot_used = true
input_ssot_hash_stable_across_cycles = true
```

Input SSOT:

```text
logical_a/logical_b generated once per fixture
Burn tensors derived from same logical input
Cold candidate derived from same logical input
R8 shadow candidate derived from same logical input
Primary runtime comparison derived from same logical input
```

## Measurement policy

```text
ledger_cycle_count = 3
warmup_iterations >= 5
measure_iterations >= 30
outlier_policy = trim_min_max_one_each_if_samples_ge_10
raw_samples_retained = true
summary_stats_computed = true
```

Required phase groups:

```text
host_shadow_attach_overhead_us
host_shadow_policy_eval_us
host_shadow_candidate_total_us
gpu_shadow_candidate_encoder_total_us
gpu_shadow_candidate_dispatch_body_us
primary_runtime_boundary_us
off_switch_replay_us
```

## Local artifacts

Generated locally only:

```text
workspace/runtime/tensorcube/g211c3r4l_r9_shadow_ledger_entries_latest.json
workspace/runtime/tensorcube/g211c3r4l_r9_shadow_cycle_summaries_latest.json
workspace/runtime/tensorcube/g211c3r4l_r9_shadow_stability_ledger_latest.json
workspace/runtime/tensorcube/g211c3r4l_r9_shadow_observe_stability_ledger_receipt_latest.json
artifacts/g211c3r4l_r9_shadow_observe_stability_ledger_local_manifest.json
```

These files are not committed.

## Audit commands

Default:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin g211c3r4l_r9_shadow_observe_stability_ledger_audit
```

Default 3-cycle shadow ledger:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin g211c3r4l_r9_shadow_observe_stability_ledger_audit -- --require-native-adapter --k-panels 1,2,4,8 --warmup 5 --measure 30 --ledger-cycles 3 --shadow-mode pipeline-buffers-bindgroup --enable-shadow-observe
```

Longer 5-cycle ledger:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin g211c3r4l_r9_shadow_observe_stability_ledger_audit -- --require-native-adapter --k-panels 1,2,4,8 --warmup 5 --measure 30 --ledger-cycles 5 --shadow-mode pipeline-buffers-bindgroup --enable-shadow-observe
```

Optional full-cache shadow ledger:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin g211c3r4l_r9_shadow_observe_stability_ledger_audit -- --require-native-adapter --k-panels 1,2,4,8 --warmup 5 --measure 30 --ledger-cycles 3 --shadow-mode pipeline-buffers-bindgroup --enable-shadow-observe --optional-full-cache-shadow
```

## PASS verdict

```text
PASS_G211C3R4L_R9_SHADOW_OBSERVE_STABILITY_LEDGER_SEALED
```

PASS means repeated disabled-by-default shadow observe evidence has been ledgered. PASS does not mean runtime cache policy has been adopted.

## PASS conditions

Required:

```text
parent_patch_id = G211C3R4L-R8
parent_verdict = PASS_G211C3R4L_R8_CANDIDATE_CACHE_RUNTIME_SHADOW_ATTACH_SEALED
selected_default_shadow_mode = PipelineBuffersBindGroupCachedShadow
default_shadow_policy_disabled = true
shadow_policy_runtime_adopted = false
shadow_policy_explicit_enable_required = true
runtime_shadow_wiring_present = true
runtime_shadow_wiring_default_disabled = true
shadow_output_committed = false
committed_output_owner_unchanged = true
ledger_cycle_count >= 3
tested_k_panel_counts includes [1,2,4,8]
same_input_ssot_used = true
input_ssot_hash_stable_across_cycles = true
cpu_reference_used_for_correctness_only = true
cpu_reference_used_as_benchmark_baseline = false
output_hash_stability_passed = true
correctness_stability_passed = true
timestamp_stability_passed = true
guard_stability_passed = true
off_switch_stability_passed = true
ownership_stability_passed = true
timing_samples_recorded = true
speedup_required_for_pass = false
performance_winner_declared = false
runtime_inference_replacement_allowed = false
backend_policy_connection_allowed = false
hardware_tensorcore_claimed = false
```

## Failure conditions

```text
FAIL: parent_patch_id != G211C3R4L-R8
FAIL: parent R8 verdict is not PASS
FAIL: selected_default_shadow_mode missing
FAIL: selected_default_shadow_mode is not PipelineBuffersBindGroupCachedShadow
FAIL: default_shadow_policy_disabled = false
FAIL: shadow_policy_runtime_adopted = true
FAIL: shadow_policy_explicit_enable_required = false
FAIL: runtime_shadow_wiring_present = false
FAIL: runtime_shadow_wiring_default_disabled = false
FAIL: shadow_output_committed = true
FAIL: committed_output_owner_unchanged = false
FAIL: ledger_cycle_count < 3
FAIL: required fixture missing from any cycle
FAIL: ledger entry missing receipt hash
FAIL: input_ssot_hash changed across cycles for same fixture
FAIL: shadow output replaces primary output
FAIL: decode path mutated
FAIL: backend policy mutated
FAIL: SFT pass1 path mutated
FAIL: runtime inference path mutated
FAIL: output stale readback detected
FAIL: control_words not fresh for fixture
FAIL: timestamp readback contains stale iteration data
FAIL: bind group identity mismatch
FAIL: off switch receipt missing
FAIL: off switch fails to restore disabled state
FAIL: shadow CPU mismatch > 0
FAIL: shadow Burn mismatch > 0
FAIL: shadow parent R8 mismatch > 0
FAIL: shadow cold mismatch > 0
FAIL: shadow primary output mismatch > 0
FAIL: timestamp markers missing
FAIL: timestamp marker coverage < 1.0
FAIL: timing samples missing
FAIL: timing stat NaN
FAIL: negative timing stat
FAIL: performance_winner_declared = true
FAIL: runtime_inference_replacement_allowed = true
FAIL: backend_policy_connection_allowed = true
FAIL: hardware_tensorcore_claimed = true
FAIL: candidate uses fifth storage binding
```
