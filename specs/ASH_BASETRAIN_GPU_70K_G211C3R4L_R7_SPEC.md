# G211C3R4L-R7
## Candidate Cache Adoption Gate / Pipeline-Buffer-BindGroup Reuse Apply Candidate Seal

## Scope

G211C3R4L-R7 consumes the G211C3R4L-R6 candidate resource reuse probe and creates a cache apply-candidate gate receipt. It does not adopt a production runtime policy, does not open the runtime splice, and does not declare a performance winner.

R7 selects `PipelineBuffersBindGroupCachedApplyCandidate` as the conservative default apply candidate. `FullCandidateResourceCachedApplyCandidate` may be recorded as an optional apply candidate only when extra freshness guards and rollback receipt checks remain sealed.

## Parent seal

```text
parent_patch_id = G211C3R4L-R6
parent_verdict = PASS_G211C3R4L_R6_CANDIDATE_RESOURCE_REUSE_PROBE_SEALED
baseline_target_kind = BurnWebGpuMatmul
candidate_target_kind = Logical16FromTile8SoftGroupKPanel
performance_winner_declared = false
runtime policy adopted = false
```

## Adoption modes

Default apply candidate:

```text
PipelineBuffersBindGroupCachedApplyCandidate
```

Optional apply candidate:

```text
FullCandidateResourceCachedApplyCandidate
```

The default candidate reuses pipeline, bind group layout, A/B/C/control buffers, and bind group. Timestamp and readback resources remain fresh unless explicitly guarded by optional full-cache mode.

## Adoption gate contract

Required:

```text
parent_r6_probe_passed = true
selected_adoption_mode_present = true
selected_mode_cache_events_present = true
selected_mode_guard_replay_passed = true
selected_mode_correctness_replay_passed = true
selected_mode_timestamp_continuity_passed = true
rollback_receipt_created = true
runtime_splice_remains_closed = true
cache_policy_apply_candidate_created = true
cache_policy_runtime_adopted = false
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

## Guard replay contract

R7 replays guards for the selected apply candidate.

```text
output_stale_read_guard_enabled = true
c_buffer_write_observed = true
readback_after_current_submit = true
output_readback_hash_changed_when_input_changes = true
control_words_fresh_for_fixture = true
tile_id_table_fresh_for_fixture = true
k_panel_count_fresh_for_fixture = true
control_words_hash_matches_current_fixture = true
timestamp_query_indices_not_reused_without_resolve = true
timestamp_readback_contains_current_iteration = true
missing_timestamp_markers = []
timestamp_marker_coverage_ratio = 1.0
bind_group_cache_hit_allowed_only_with_stable_buffer_identity = true
bind_group_identity_hash_recorded = true
bind_group_identity_hash_matches_cached_buffers = true
```

## Rollback contract

Rollback target:

```text
rollback_target_mode = ColdCreateEveryIteration
```

Rollback must restore:

```text
pipeline_reused = false
bind_group_layout_reused = false
bind_group_reused = false
buffers_reused = false
timestamp_resources_reused = false
readback_resources_reused = false
```

Rollback must not mutate:

```text
runtime_inference_path
backend_policy
decode_path
SFT pass1 path
```

## Correctness preservation

Every fixture and adoption mode must preserve:

```text
Burn vs CPU reference
Candidate vs CPU reference
Candidate vs Burn
Selected adoption mode vs ColdCreateEveryIteration
Selected adoption mode vs parent R6 selected-mode output
```

Required:

```text
burn_cpu_mismatch_count = 0
candidate_cpu_mismatch_count = 0
candidate_burn_mismatch_count = 0
candidate_cold_mismatch_count = 0
candidate_parent_mode_mismatch_count = 0
burn_nan_count = 0
candidate_nan_count = 0
burn_inf_count = 0
candidate_inf_count = 0
```

## Fixture contract

```text
k_panel_count = 1 -> M=16 N=16 K=8
k_panel_count = 2 -> M=16 N=16 K=16
k_panel_count = 4 -> M=16 N=16 K=32
k_panel_count = 8 -> M=16 N=16 K=64
same_input_ssot_used = true
```

## Measurement policy

```text
warmup_iterations >= 5
measure_iterations >= 30
outlier_policy = trim_min_max_one_each_if_samples_ge_10
raw_samples_retained = true
summary_stats_computed = true
```

R7 measures:

```text
ColdCreateEveryIteration
PipelineBuffersBindGroupCachedApplyCandidate
FullCandidateResourceCachedApplyCandidate optional
RollbackColdCreateReplay
```

## Runtime mutation seal

```text
runtime_inference_replacement_allowed = false
sft_pass1_replacement_allowed = false
backend_policy_connection_allowed = false
subgroup_fast_path_enabled = false
cooperative_matrix_claimed = false
hardware_tensorcore_claimed = false
speedup_required_for_pass = false
performance_winner_declared = false
cache_policy_runtime_adopted = false
```

## Local artifacts

Generated locally only:

```text
workspace/runtime/tensorcube/g211c3r4l_r7_cache_adoption_fixture_latest.json
workspace/runtime/tensorcube/g211c3r4l_r7_cache_guard_replay_latest.json
workspace/runtime/tensorcube/g211c3r4l_r7_cache_rollback_receipt_latest.json
workspace/runtime/tensorcube/g211c3r4l_r7_cache_adoption_gate_receipt_latest.json
artifacts/g211c3r4l_r7_candidate_cache_adoption_gate_local_manifest.json
```

These files are not committed.

## Audit commands

Default:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin g211c3r4l_r7_candidate_cache_adoption_gate_audit
```

Strict conservative default:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin g211c3r4l_r7_candidate_cache_adoption_gate_audit -- --require-native-adapter --k-panels 1,2,4,8 --warmup 5 --measure 30 --adoption-mode pipeline-buffers-bindgroup
```

With optional full-cache candidate:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin g211c3r4l_r7_candidate_cache_adoption_gate_audit -- --require-native-adapter --k-panels 1,2,4,8 --warmup 5 --measure 30 --adoption-mode pipeline-buffers-bindgroup --optional-full-cache
```

## PASS verdict

```text
PASS_G211C3R4L_R7_CANDIDATE_CACHE_ADOPTION_GATE_SEALED
```

PASS means the cache policy is sealed as an apply candidate only. PASS does not mean runtime cache policy has been adopted.

## Failure conditions

```text
FAIL: parent_patch_id != G211C3R4L-R6
FAIL: parent R6 verdict is not PASS
FAIL: selected_default_apply_candidate_mode missing
FAIL: selected_default_apply_candidate_mode is not PipelineBuffersBindGroupCachedApplyCandidate
FAIL: cache_policy_apply_candidate_created = false
FAIL: cache_policy_runtime_adopted = true
FAIL: selected R6 mode receipt missing
FAIL: selected mode guard replay failed
FAIL: selected mode correctness replay failed
FAIL: selected mode timestamp continuity failed
FAIL: stale output readback detected
FAIL: control_words not fresh for fixture
FAIL: timestamp readback contains stale iteration data
FAIL: bind group identity mismatch
FAIL: bind group cache hit with unstable buffer identity
FAIL: rollback receipt missing
FAIL: rollback target does not restore cold create mode
FAIL: rollback output mismatch
FAIL: rollback mutates runtime inference path
FAIL: rollback mutates backend policy
FAIL: rollback mutates decode path
FAIL: rollback mutates SFT pass1 path
FAIL: burn correctness mismatch > 0
FAIL: candidate correctness mismatch > 0
FAIL: candidate vs Burn mismatch > 0
FAIL: candidate vs cold mismatch > 0
FAIL: candidate vs parent selected mode mismatch > 0
FAIL: performance_winner_declared = true
FAIL: runtime_inference_replacement_allowed = true
FAIL: backend_policy_connection_allowed = true
FAIL: hardware_tensorcore_claimed = true
FAIL: candidate uses fifth storage binding
```
