# ASH-TCU-DECODE-04-R4-R1

## TOPK_SURFACE_SAMPLER_SHADOW_ADAPTER_AND_TOKEN_SELECTION_NON_COMMIT_GATE

```text
patch_id=ASH-TCU-DECODE-04-R4-R1_TOPK_SURFACE_SAMPLER_SHADOW_ADAPTER_AND_TOKEN_SELECTION_NON_COMMIT_GATE
parent_status=PASS_ASH_TCU_DECODE_04_R4_FUSED_FINAL_RMSNORM_GROUPED_LM_HEAD_TOPK_GATE
route_digest=1b9009ff7216b57f6bcabeb0eb39d9c8d5e99019601f40de052166ff8f138327
production_authority=false
```

## Runtime boundary

R4-R1 is artifact-only. It must not reopen the model checkpoint or dispatch GPU work.

```text
r4_parent_runtime_reexecution_count=0
checkpoint_open_count=0
checkpoint_range_read_count=0
gpu_dispatch_count=0
```

Required immutable parent artifacts:

```text
ash_tensorcube_decode_04_r4_local_manifest_latest.json
ash_tensorcube_decode_04_r4_topk_receipt_latest.json
ash_tensorcube_decode_04_r4_parity_receipt_latest.json
ash_tensorcube_decode_04_r4_allocation_receipt_latest.json
```

Missing or inconsistent parent artifacts produce HOLD. Silent R4 reexecution is forbidden.

## Candidate surface SSOT

The only selection input is `gpu_forward_topk` from the R4 top-k receipt.

```text
selection_surface_source=gpu_forward_topk
entry_count=64
unique_token_count=64
vocab_size=48259
non_finite_logit_count=0
surface_order_violation_count=0
surface_rank_violation_count=0
selection_surface_fallback_count=0
```

`gpu_reverse_topk` and `cpu_streaming_topk` remain parity evidence only.

Canonical order:

```text
primary=logit descending
secondary=token_id ascending
```

## Explicit policy SSOT

```text
policy_id=decode04_r4_r1_shadow_policy_v1
selection_universe=topk64
temperature=0.80
top_p=0.95
min_p=0.05
repetition_penalty=1.05
repetition_window=64
frequency_penalty=0.0
presence_penalty=0.0
candidate_limit=64
special_token_policy=observe_only
```

All policy values are explicit CLI inputs. Silent defaults and unsupported non-neutral fields are forbidden.

Canonical operation order:

```text
repetition penalty
-> frequency penalty
-> presence penalty
-> temperature
-> stable softmax
-> min-p
-> top-p
-> renormalization
-> deterministic CDF
-> explicit draw selection
```

## Explicit history and draw SSOT

```text
history_source=explicit_fixture
history_token_ids=[19747,1,19747]
synthetic_fixture=true
production_history_read_count=0
```

Token `19747` must exist in the parent top-k surface. The fixture is not rewritten when absent.

```text
draw_algorithm=explicit_u64_fraction_v1
draw_u64=[0,4611686018427387904,9223372036854775808,13835058055282163712,18446744073709551615]
canonical_draw_index=2
production_rng_read_count=0
production_rng_clone_count=0
production_rng_advance_count=0
```

Draw conversion must remain in `0.0 <= u < 1.0`, including `u64::MAX`.

## Deterministic fixtures

```text
F0 parent surface integrity with neutral policy
F1 greedy selection
F2 canonical stochastic selection
F3 reverse-input stability
F4 equal-logit token-id tie-break
```

The adapter and independent oracle may share immutable input structures only. Candidate transforms, filtering, CDF construction and categorical selection helpers must not be shared.

Required parity:

```text
fixture_count=5
draw_comparison_count=5
retained_id_mismatch_count=0
selected_id_mismatch_count=0
selected_rank_mismatch_count=0
probability_mismatch_count=0
cdf_mismatch_count=0
forward_reverse_adapter_selection_match=true
greedy_fixture_pass=true
tie_break_fixture_pass=true
```

## Non-commit firewall

The selected token is receipt-local draft data only.

```text
commit_authorized=false
selected_token_runtime_write_count=0
token_append_attempt_count=0
token_append_commit_count=0
kv_append_attempt_count=0
kv_append_commit_count=0
text_decode_attempt_count=0
stream_emit_attempt_count=0
production_rng_state_changed=false
runtime_route_changed=false
runtime_output_changed=false
all_state_unchanged=true
```

The adapter receives no mutable DecodeState, GenerationCursor, KV handle or production RNG handle.

## Memory and performance

```text
max_candidate_count=64
max_fixture_candidate_count=64
full_vocab_candidate_allocation_count=0
full_vocab_probability_allocation_count=0
full_vocab_cdf_allocation_count=0
peak_shadow_sampler_heap_bytes<=4194304
```

```text
parent_artifact_load_ms<=250
surface_validation_ms<=10
all_fixture_sampler_ms<=20
oracle_parity_ms<=20
artifact_write_ms<=250
total_runtime_ms<=1000
soft_total_runtime_target_ms=250
```

A single run remains provisional performance evidence.

## Runtime artifacts

```text
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r1_local_manifest_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r1_parent_surface_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r1_policy_snapshot_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r1_history_snapshot_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r1_draw_transcript_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r1_sampler_trace_latest.jsonl
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r1_selection_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r1_oracle_parity_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r1_non_commit_audit_latest.json
```

## Status

```text
PASS=PASS_ASH_TCU_DECODE_04_R4_R1_TOPK_SURFACE_SAMPLER_SHADOW_ADAPTER_AND_TOKEN_SELECTION_NON_COMMIT_GATE
HOLD=HOLD_ASH_TCU_DECODE_04_R4_R1_TOPK_SURFACE_SAMPLER_SHADOW_ADAPTER_AND_TOKEN_SELECTION_NON_COMMIT_GATE
FAIL=FAIL_ASH_TCU_DECODE_04_R4_R1_TOPK_SURFACE_SAMPLER_SHADOW_ADAPTER_AND_TOKEN_SELECTION_NON_COMMIT_GATE
PASS_VERDICT=decode04_r4_r1_topk_surface_shadow_sampler_selection_parity_non_commit_pass
```

PASS authorizes only `ASH-TCU-DECODE-04-R4-R2` selected-token decode-surface and special-token classification non-emit work. It does not authorize sampler adoption, token append, KV mutation, text emission, production route switching or DECODE-05 promotion.
