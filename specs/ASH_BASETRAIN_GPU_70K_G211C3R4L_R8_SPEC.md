# G211C3R4L-R8
## Candidate Cache Runtime Shadow Attach / Disabled-By-Default Policy Wiring Seal

## Scope

G211C3R4L-R8 consumes the G211C3R4L-R7 candidate cache adoption gate and wires the selected cache apply candidate as a disabled-by-default runtime shadow policy. R8 does not adopt the cache policy as production runtime behavior, does not open the runtime splice, does not commit shadow output, and does not declare a performance winner.

R8 selects `PipelineBuffersBindGroupCachedShadow` as the default shadow mode. `FullCandidateResourceCachedShadow` may be recorded as an optional shadow mode only when explicit enable, freshness guards, output ownership guards, and off-switch receipts remain sealed.

## Parent seal

```text
parent_patch_id = G211C3R4L-R7
parent_verdict = PASS_G211C3R4L_R7_CANDIDATE_CACHE_ADOPTION_GATE_SEALED
parent_default_apply_candidate = PipelineBuffersBindGroupCachedApplyCandidate
parent_optional_apply_candidate = FullCandidateResourceCachedApplyCandidate
cache_policy_runtime_adopted = false
performance_winner_declared = false
```

## Shadow attach principle

```text
Primary path:
existing runtime path -> committed output

Shadow path:
candidate cache path -> shadow receipt only -> no output commit
```

Required:

```text
committed_output_owner = ExistingRuntimePrimaryPath
shadow_output_owner = CandidateCacheShadowPath
shadow_output_committed = false
committed_output_owner_unchanged = true
```

Forbidden:

```text
shadow output replaces primary output
shadow output mutates decode result
shadow output mutates logits
shadow output mutates tensor registry
shadow output mutates SFT pass1 state
shadow path silently becomes default path
```

## Policy state machine

Allowed states:

```text
Disabled
ShadowObserveOnly
ShadowBlocked
```

Default:

```text
default_shadow_policy_state = Disabled
shadow_policy_enabled = false
```

Allowed transitions:

```text
Disabled -> ShadowObserveOnly
ShadowObserveOnly -> Disabled
ShadowObserveOnly -> ShadowBlocked
ShadowBlocked -> Disabled
```

Forbidden transitions:

```text
Disabled -> RuntimeAdopted
ShadowObserveOnly -> RuntimeAdopted
ShadowBlocked -> RuntimeAdopted
```

R8 does not define `RuntimeAdopted` as a valid state.

## Shadow policy config defaults

```text
shadow_policy_enabled = false
selected_shadow_candidate_mode = PipelineBuffersBindGroupCachedShadow
allow_optional_full_cache_shadow = false
commit_shadow_output = false
mutate_runtime_output = false
mutate_decode_output = false
mutate_backend_policy = false
```

R8 PASS requires:

```text
default_shadow_policy_disabled = true
shadow_policy_runtime_adopted = false
shadow_policy_explicit_enable_required = true
```

## Candidate modes

Default shadow mode:

```text
PipelineBuffersBindGroupCachedShadow
```

Optional shadow mode:

```text
FullCandidateResourceCachedShadow
```

The default shadow mode reuses pipeline, bind group layout, A/B/C/control buffers, and bind group. Timestamp and readback resources remain fresh.

Optional full-cache shadow is allowed only if:

```text
allow_optional_full_cache_shadow = true
optional_full_cache_parent_r7_receipt_present = true
timestamp_freshness_guard_passed = true
readback_freshness_guard_passed = true
rollback_receipt_present = true
```

Optional full-cache shadow is not allowed as default.

## Runtime wiring contract

Required:

```text
runtime_shadow_wiring_present = true
runtime_shadow_wiring_default_disabled = true
runtime_shadow_wiring_requires_explicit_enable = true
runtime_shadow_wiring_no_output_commit = true
runtime_shadow_wiring_no_decode_mutation = true
runtime_shadow_wiring_no_backend_policy_mutation = true
```

Allowed:

```text
build shadow policy object
build shadow receipt
run shadow candidate in audit binary
record shadow candidate timing and correctness
compare shadow output against primary output
```

Forbidden:

```text
replacing committed runtime tensor
replacing logits
replacing decode output
changing generation path
changing SFT pass1 path
changing Burn baseline
writing shadow output into production output slot
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

R8 replays R7 guards in shadow mode.

Required:

```text
output_stale_read_guard_passed = true
control_words_freshness_guard_passed = true
timestamp_freshness_guard_passed = true
bind_group_identity_guard_passed = true
rollback_guard_passed = true
shadow_no_commit_guard_passed = true
shadow_policy_default_off_guard_passed = true
shadow_output_ownership_guard_passed = true
runtime_mutation_guard_passed = true
```

## Correctness contract

R8 compares shadow candidate output against:

```text
CPU reference
Burn baseline
R7 selected apply candidate output
ColdCreateEveryIteration output
Existing runtime primary output
```

Required:

```text
shadow_cpu_mismatch_count = 0
shadow_burn_mismatch_count = 0
shadow_parent_r7_mismatch_count = 0
shadow_cold_mismatch_count = 0
shadow_primary_output_mismatch_count = 0
shadow_nan_count = 0
shadow_inf_count = 0
```

## Timestamp continuity

R8 preserves R5/R6/R7 timestamp marker coverage in shadow mode.

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

## Fixture contract

```text
k_panel_count = 1 -> M=16 N=16 K=8
k_panel_count = 2 -> M=16 N=16 K=16
k_panel_count = 4 -> M=16 N=16 K=32
k_panel_count = 8 -> M=16 N=16 K=64
same_input_ssot_used = true
```

Input SSOT:

```text
logical_a/logical_b generated once
Burn tensors derived from same logical input
Cold candidate derived from same logical input
R7 apply candidate derived from same logical input
R8 shadow candidate derived from same logical input
Primary runtime comparison derived from same logical input
```

## Measurement policy

```text
warmup_iterations >= 5
measure_iterations >= 30
outlier_policy = trim_min_max_one_each_if_samples_ge_10
raw_samples_retained = true
summary_stats_computed = true
```

R8 measures:

```text
PrimaryRuntimeBoundary
ColdCreateEveryIteration
PipelineBuffersBindGroupCachedShadow
FullCandidateResourceCachedShadow optional
ShadowAttachOverhead
RollbackOffSwitchReplay
```

Required phase groups:

```text
host_shadow_attach_overhead_us
host_shadow_policy_eval_us
host_shadow_candidate_total_us
gpu_shadow_candidate_encoder_total_us
gpu_shadow_candidate_dispatch_body_us
primary_runtime_boundary_us
```

## Off-switch contract

Off-switch target:

```text
shadow_policy_enabled = false
selected_shadow_candidate_mode = PipelineBuffersBindGroupCachedShadow
commit_shadow_output = false
```

Required:

```text
off_switch_available = true
off_switch_restores_disabled_state = true
off_switch_does_not_change_primary_output = true
off_switch_does_not_mutate_backend_policy = true
off_switch_does_not_mutate_decode_path = true
off_switch_does_not_mutate_sft_pass1_path = true
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
shadow_policy_runtime_adopted = false
shadow_output_committed = false
```

## Local artifacts

Generated locally only:

```text
workspace/runtime/tensorcube/g211c3r4l_r8_shadow_policy_config_latest.json
workspace/runtime/tensorcube/g211c3r4l_r8_runtime_shadow_wiring_latest.json
workspace/runtime/tensorcube/g211c3r4l_r8_shadow_guard_replay_latest.json
workspace/runtime/tensorcube/g211c3r4l_r8_shadow_off_switch_receipt_latest.json
workspace/runtime/tensorcube/g211c3r4l_r8_runtime_shadow_attach_receipt_latest.json
artifacts/g211c3r4l_r8_candidate_cache_runtime_shadow_attach_local_manifest.json
```

These files are not committed.

## Audit commands

Default:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin g211c3r4l_r8_candidate_cache_runtime_shadow_attach_audit
```

Conservative shadow mode:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin g211c3r4l_r8_candidate_cache_runtime_shadow_attach_audit -- --require-native-adapter --k-panels 1,2,4,8 --warmup 5 --measure 30 --shadow-mode pipeline-buffers-bindgroup
```

Optional full-cache shadow:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin g211c3r4l_r8_candidate_cache_runtime_shadow_attach_audit -- --require-native-adapter --k-panels 1,2,4,8 --warmup 5 --measure 30 --shadow-mode pipeline-buffers-bindgroup --optional-full-cache-shadow
```

Explicit shadow observe:

```bash
cargo run -p orchestrator_local --features orchestrator_tcu_audit_bins --bin g211c3r4l_r8_candidate_cache_runtime_shadow_attach_audit -- --require-native-adapter --k-panels 1,2,4,8 --warmup 5 --measure 30 --shadow-mode pipeline-buffers-bindgroup --enable-shadow-observe
```

## PASS verdict

```text
PASS_G211C3R4L_R8_CANDIDATE_CACHE_RUNTIME_SHADOW_ATTACH_SEALED
```

PASS means the cache policy is wired as disabled-by-default shadow attach only. PASS does not mean runtime cache policy has been adopted.

## Failure conditions

```text
FAIL: parent_patch_id != G211C3R4L-R7
FAIL: parent R7 verdict is not PASS
FAIL: selected_default_shadow_mode missing
FAIL: selected_default_shadow_mode is not PipelineBuffersBindGroupCachedShadow
FAIL: default_shadow_policy_disabled = false
FAIL: shadow_policy_runtime_adopted = true
FAIL: shadow_policy_explicit_enable_required = false
FAIL: runtime_shadow_wiring_present = false
FAIL: runtime_shadow_wiring_default_disabled = false
FAIL: shadow_output_committed = true
FAIL: committed_output_owner_unchanged = false
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
FAIL: shadow parent R7 mismatch > 0
FAIL: shadow cold mismatch > 0
FAIL: shadow primary output mismatch > 0
FAIL: timestamp markers missing
FAIL: timestamp marker coverage < 1.0
FAIL: performance_winner_declared = true
FAIL: runtime_inference_replacement_allowed = true
FAIL: backend_policy_connection_allowed = true
FAIL: hardware_tensorcore_claimed = true
FAIL: candidate uses fifth storage binding
```
