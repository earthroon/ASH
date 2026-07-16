# ASH-TCU-DECODE-04 SPEC

## LIVE_SHADOW_COMPLETION_READBACK_PARITY_GATE

```text
patch_id=ASH-TCU-DECODE-04_LIVE_SHADOW_COMPLETION_READBACK_PARITY_GATE
parent_patch=ASH-TCU-DECODE-03_LIVE_SAME_DEVICE_SHADOW_DISPATCH_SPLICE
parent_package=ash_pass3_ASH-TCU-DECODE-03_live_same_device_shadow_dispatch_splice_code_baked_no_spec_no_docs_no_runtime_artifacts_no_sha.zip
parent_package_sha256=f55a0d0280d81d81c9f8a772003757e63e2b42bebb9bf3772715685b16eec29a
parent_execution_id=decode03-2c74c1021fe8054abe6b
parent_status=PASS_ASH_TCU_DECODE_03_LIVE_SAME_DEVICE_SHADOW_DISPATCH_SPLICE
parent_route_digest=1b9009ff7216b57f6bcabeb0eb39d9c8d5e99019601f40de052166ff8f138327
selected_generation_step=0
selected_tile_id=0
selected_tile_span=[0,1024)
mutation_class=bounded_live_shadow_completion_readback_and_parity_observation
output_authority=burn
production_authority=false
runtime_output_changed=false
```

## 1. Status

```text
PASS=PASS_ASH_TCU_DECODE_04_LIVE_SHADOW_COMPLETION_READBACK_PARITY_GATE
HOLD=HOLD_ASH_TCU_DECODE_04_LIVE_SHADOW_COMPLETION_READBACK_PARITY_GATE
FAIL=FAIL_ASH_TCU_DECODE_04_LIVE_SHADOW_COMPLETION_READBACK_PARITY_GATE
```

Expected PASS verdict:

```text
live_same_device_m1_n1024_k2048_shadow_output_completed_read_back_once_and_matched_the_live_burn_first_full_tile_reference_within_bounded_f32_tolerance_while_burn_remained_the_only_output_authority
```

## 2. Purpose

DECODE-03 proved that the canonical TensorCube route can borrow the actual live ASH generation buffers and submit one command buffer on the existing Burn WGPU Device and Queue. It intentionally left the scratch output unobserved.

DECODE-04 adds the smallest bounded observation surface to the same invocation:

1. execute generation step 0, vocab tile 0 only;
2. encode the M1-N1024-K2048 TensorCube dispatch;
3. copy exactly 1024 f32 scratch values into one staging buffer;
4. wait for completion with the existing Device;
5. map and read exactly 4096 bytes once;
6. reuse the existing Burn tile-0 `tile_row` materialization as reference;
7. compare all 1024 values under a fixed hybrid tolerance;
8. reject cardinality drift, NaN, infinity and degenerate zero-to-zero evidence;
9. persist digests, aggregate metrics and at most 32 difference rows;
10. preserve Burn as the only output authority for PASS, HOLD and FAIL.

This patch does not authorize TensorCube output merge, sampler use, route promotion, all-tile dispatch, repeated generation-step dispatch, ragged-tail execution or Burn replacement.

## 3. Parent truth

```text
execution_id=decode03-2c74c1021fe8054abe6b
route_digest=1b9009ff7216b57f6bcabeb0eb39d9c8d5e99019601f40de052166ff8f138327
raw_buffer_lease_count=2
tensorcube_dispatch_count=1
queue_submit_count=1
readback_count=0
burn_output_authority=true
runtime_output_changed=false
```

Canonical route:

```text
M=1
N=1024
K=2048
lhs_runtime_dtype=f32
rhs_runtime_dtype=f32
accumulation_dtype=f32
workgroup=[16,16,1]
dispatch=[64,1,1]
selected_tile_id=0
```

DECODE-04 consumes this route digest and the DECODE-03 arithmetic shader contract without changing numerical route semantics.

## 4. Activation contract

```text
mode=live_generation_single_full_tile_completion_readback_parity
readback_authorized=true
parity_authorized=true
output_commit_authorized=false
burn_output_authority=true
production_authority=false
```

Model API:

```rust
pub fn configure_tensorcube_decode04_live_shadow_parity(
    &mut self,
    config: Decode04ParityConfig,
) -> anyhow::Result<serde_json::Value>;
```

The activation receipt binds:

```text
parent_route_digest
selected_generation_step=0
selected_tile_id=0
readback_element_count=1024
readback_bytes=4096
absolute_tolerance=0.001
relative_tolerance=0.001
hard_absolute_ceiling=0.01
non_degenerate_reference_required=true
output_commit_authorized=false
```

DECODE-03 and DECODE-04 modes are mutually exclusive within one model instance.

## 5. Execution scope

```text
activation_required=true
generation_step_ordinal=0
selected_tile_id=0
selected_tile_token_start=0
selected_tile_token_len=1024
selected_tile_class=canonical_default_full_tile
max_tensorcube_dispatches_per_generation=1
max_tensorcube_readbacks_per_generation=1
max_parity_comparisons_per_generation=1
```

Forbidden:

```text
tiles 1..46 dispatch
N=131 ragged-tail dispatch
generation step 1+ dispatch
retry after candidate failure
candidate rerun to improve parity
multiple prompts in one audit execution
```

## 6. Buffer and ordering contract

Scratch buffer:

```text
size=4096
usage=STORAGE|COPY_SRC
```

Staging buffer:

```text
size=4096
usage=MAP_READ|COPY_DST
```

One command encoder records this exact order:

```text
begin compute pass
bind canonical live lhs and rhs buffers
bind scratch output
bind ABI parameter buffer
dispatch_workgroups(64,1,1)
end compute pass
copy_buffer_to_buffer(scratch,0,staging,0,4096)
finish command buffer
queue.submit exactly once
```

The compute dispatch and copy must not be split into separate TensorCube queue submissions.

## 7. Completion and readback contract

```text
completion_timeout_ms=30000
map_mode=Read
map_offset=0
map_size=4096
map_count=1
unmap_count=1
readback_count=1
readback_f32_count=1024
```

The same WGPU Device used by Burn is polled to a bounded deadline. No additional Device or Queue may be created. A stale or incorrectly sized mapped range is rejected.

The candidate vector remains private to the DECODE-04 readback capsule and comparator. It is not exposed as a production tensor API.

## 8. Burn reference contract

The existing Burn vocab-atlas loop already performs:

```rust
let tile_row = tile_logits
    .into_data()
    .to_vec::<f32>()
    .expect("failed to materialize native vocab atlas tile logits");
```

For tile 0 only, this existing `tile_row` is passed to the DECODE-04 comparator. No duplicate Burn matmul or additional Burn reference readback is permitted.

```text
burn_reference_capture_count=1
additional_burn_readback_count=0
```

## 9. Finite and non-degenerate gate

Both candidate and Burn reference require exactly 1024 finite f32 values.

```text
nan_count=0
inf_count=0
```

A ceremonial zero-to-zero comparison is not PASS. The Burn reference is non-degenerate only when:

```text
burn_nonzero_count>=16
burn_l2_norm>1.0e-6
burn_value_span>1.0e-6
```

A degenerate reference produces:

```text
HOLD_ASH_TCU_DECODE_04_LIVE_SHADOW_COMPLETION_READBACK_PARITY_GATE
reason=decode04_live_burn_reference_degenerate
```

## 10. Numerical tolerance

Fixed SSOT values:

```text
absolute_tolerance=0.001
relative_tolerance=0.001
hard_absolute_ceiling=0.01
```

Per element:

```text
abs_diff=abs(burn-candidate)
scale=max(abs(burn),abs(candidate),1.0)
rel_diff=abs_diff/scale
pass=(abs_diff<=0.001 OR rel_diff<=0.001) AND abs_diff<=0.01
```

Overall PASS requires:

```text
mismatch_count=0
nan_count=0
inf_count=0
reference_degenerate=false
local_argmax_contract_valid=true
```

Exact bit equality is diagnostic only and is not required because valid f32 reduction order may differ.

## 11. Argmax contract

Record:

```text
burn_local_argmax
candidate_local_argmax
burn_argmax_tie_count
local_argmax_equal_or_tied_set_valid
```

When Burn has an exact f32-bit top tie, the candidate argmax may be any member of the Burn tied set. Otherwise local argmax equality is required.

## 12. Bounded difference evidence

Record aggregate metrics:

```text
passed_count
mismatch_count
exact_bit_match_count
max_abs_diff
max_rel_diff
mean_abs_diff
rmse
```

Persist at most 32 rows sorted by:

1. descending absolute difference;
2. descending relative difference;
3. ascending local index.

Each row may contain:

```text
local_index
global_token_id
burn_value
candidate_value
abs_diff
rel_diff
within_tolerance
```

The full 1024-value vectors, lhs vector, rhs weights and checkpoint payloads are forbidden from the default artifact bundle.

## 13. Runtime counters

Successful activated generation:

```text
raw_buffer_lease_count=2
host_upload_count=0
scratch_output_allocation_count=1
staging_buffer_allocation_count=1
command_encoder_creation_count=1
tensorcube_dispatch_count=1
scratch_copy_count=1
queue_submit_count=1
completion_wait_count=1
map_count=1
unmap_count=1
readback_count=1
readback_bytes=4096
readback_f32_count=1024
burn_reference_capture_count=1
additional_burn_readback_count=0
parity_comparison_count=1
shadow_output_merge_count=0
shadow_output_topk_for_generation_count=0
shadow_output_sampler_use_count=0
shadow_output_commit_count=0
downstream_output_commit_count=0
route_registry_write_count=0
runtime_output_change_count=0
```

## 14. Session lifecycle

`TensorCubeGenerationShadowSession` owns exactly-once state:

```text
decode04_dispatch_submitted
decode04_copy_encoded
decode04_readback_completed
decode04_reference_captured
decode04_parity_completed
decode04_parity_passed
```

Required transition:

```text
Eligible
-> DispatchSubmitted
-> CopyEncoded
-> ReadbackCompleted
-> ReferenceCaptured
-> ParityCompleted
-> Finalized
```

Second dispatch, second readback, parity before reference and incomplete activated finalization fail closed.

## 15. Output authority firewall

The candidate may flow only to:

```text
DECODE-04 comparator
candidate digest builder
aggregate metric builder
bounded top-32 difference evidence
```

The candidate must never flow to:

```text
merged_logits
top_k_tile_candidates
sampler
token selection
fallback output
output cache
production commit
```

Burn `tile_row` continues into `merged_logits` exactly as before. Burn remains the returned logits and token authority under PASS, HOLD and FAIL.

## 16. Error classification

HOLD when authority is intact but promotion proof is incomplete:

```text
GPU unavailable
checkpoint unavailable
completion timeout
map unavailable
finite candidate outside tolerance
Burn reference degenerate
bounded completion not proven
```

FAIL for contract corruption or unsafe behavior:

```text
parent artifact hash mismatch
route digest mismatch
wrong shape
wrong readback bytes or cardinality
NaN or infinity
host-upload fallback
fixture substitution
extra Device or Queue
duplicate dispatch/readback/parity
candidate production flow
authority change
protected state mutation
```

HOLD and FAIL must preserve:

```text
burn_output_authority=true
production_authority=false
shadow_output_commit_count=0
runtime_output_changed=false
```

## 17. Required source changes

```text
crates/burn_webgpu_backend/src/tensorcube_decode_04_live_parity.rs
crates/burn_webgpu_backend/src/lib.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d0r1_shadow_observation.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d0r1_shadow_observer_owner.rs
crates/model_core/src/native_wgpu.rs
crates/model_core/tests/ash_tcu_decode_04_live_shadow_completion_readback_parity_gate.rs
crates/orchestrator_local/src/ash_tcu_decode_04_live_shadow_completion_readback_parity_gate_report.rs
crates/orchestrator_local/src/bin/ash_tcu_decode_04_live_shadow_completion_readback_parity_gate.rs
crates/orchestrator_local/src/lib.rs
crates/orchestrator_local/Cargo.toml
```

## 18. Static fail-closed audit

The Rust audit verifies:

```text
scratch STORAGE|COPY_SRC
staging MAP_READ|COPY_DST
copy_buffer_to_buffer call count=1
copy bytes=4096
map and unmap present
candidate cardinality=1024
finite gate present
non-degenerate gate present
fixed tolerance constants present
Burn tile_row used as reference
candidate merge/top-k/sampler flow absent
output commit authorization=false
```

String-only placeholder receipts without a live dispatch and readback are rejected.

## 19. Tests

Backend tests cover:

```text
exact match PASS
bounded difference PASS
tolerance mismatch HOLD
hard ceiling HOLD
NaN/Inf FAIL
cardinality FAIL
degenerate zero reference HOLD
argmax tie handling
digest stability
largest-difference deterministic ordering and max-32 bound
```

Model/session tests cover:

```text
exactly-once dispatch/copy/readback/reference/parity counters
parity-before-readback rejection
second readback rejection
second parity rejection
DECODE-03/04 mutual exclusion
Burn output continuity through the unchanged tile_row merge path
```

## 20. Protected state

Before and after the smoke, hash or compare:

```text
model spec
checkpoint path set and bytes
route digest
route registry epoch
LoRA attachment set
sampling configuration
Burn output-authority flag
```

Allowed mutations are limited to DECODE-04 counters, receipts and Rust-owned artifacts.

## 21. Rust-owned artifacts

Immutable root:

```text
artifacts/tensorcube/decode_04/<execution_id>/
```

Required files:

```text
ash_tensorcube_decode_04_parent_chain.json
ash_tensorcube_decode_04_activation_receipt.json
ash_tensorcube_decode_04_completion_readback_receipt.json
ash_tensorcube_decode_04_burn_reference_capture_receipt.json
ash_tensorcube_decode_04_parity_comparison.json
ash_tensorcube_decode_04_largest_differences.json
ash_tensorcube_decode_04_authority_firewall.json
ash_tensorcube_decode_04_protected_state_guard.json
ash_tensorcube_decode_04_source_digest_manifest.json
ash_tensorcube_decode_04_report.json
ash_tensorcube_decode_04_final_seal.json
ash_tensorcube_decode_04_verdict.txt
ash_tensorcube_decode_04_local_manifest.json
```

Latest mirrors live under:

```text
workspace/runtime/tensorcube/ash_tensorcube_decode_04_*_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_verdict_latest.txt
workspace/runtime/tensorcube/ash_tensorcube_decode_04_local_manifest_latest.json
```

The local manifest is written last. Every immutable artifact row includes relative path, SHA-256, byte size, schema and artifact role.

## 22. Parent-chain validation

The audit reads the DECODE-03 local manifest, follows its immutable `final_seal` row, verifies the artifact SHA-256 and requires:

```text
parent_status=PASS_ASH_TCU_DECODE_03_LIVE_SAME_DEVICE_SHADOW_DISPATCH_SPLICE
parent_execution_id=decode03-2c74c1021fe8054abe6b
parent_route_digest=1b9009ff7216b57f6bcabeb0eb39d9c8d5e99019601f40de052166ff8f138327
parent_burn_output_authority=true
parent_runtime_output_changed=false
```

Console text alone is not parent evidence.

## 23. Execution interface

```text
ash_tcu_decode_04_live_shadow_completion_readback_parity_gate
```

CLI:

```text
--repo-root <PATH>
--model-spec <PATH>
--checkpoint <PATH> [repeatable]
--parent-manifest <PATH>
--smoke-token-id <U32>
--completion-timeout-ms 30000
--activate-live-shadow-readback-parity
--run-live-generation-smoke
--require-single-dispatch-per-generation
--require-single-readback-per-generation
--require-strict-live-fusion-raw-access
--require-same-device-and-queue
--require-no-host-upload
--require-readback-bytes 4096
--require-readback-f32-count 1024
--require-absolute-tolerance 0.001
--require-relative-tolerance 0.001
--require-hard-absolute-ceiling 0.01
--require-non-degenerate-reference
--require-no-output-commit
--require-burn-output-authority
--require-no-runtime-output-change
--write-runtime-artifacts
--write-local-manifest
```

FAIL exits 1. HOLD writes artifacts and exits 2. PASS exits 0.

## 24. PASS output

```text
PASS_ASH_TCU_DECODE_04_LIVE_SHADOW_COMPLETION_READBACK_PARITY_GATE
verdict=live_same_device_m1_n1024_k2048_shadow_output_completed_read_back_once_and_matched_the_live_burn_first_full_tile_reference_within_bounded_f32_tolerance_while_burn_remained_the_only_output_authority
execution_id=decode04-<digest-prefix>
parent_execution_id=decode03-2c74c1021fe8054abe6b
route_digest=1b9009ff7216b57f6bcabeb0eb39d9c8d5e99019601f40de052166ff8f138327
raw_buffer_lease_count=2
tensorcube_dispatch_count=1
scratch_copy_count=1
queue_submit_count=1
readback_count=1
readback_bytes=4096
readback_f32_count=1024
parity_comparison_count=1
mismatch_count=0
max_abs_diff=<MEASURED>
max_rel_diff=<MEASURED>
burn_nonzero_count=<MEASURED>
burn_l2_norm=<MEASURED>
burn_value_span=<MEASURED>
local_argmax_equal=<true_or_tied_set_valid>
shadow_output_commit_count=0
burn_output_authority=true
runtime_output_changed=false
local_manifest=<ASH_ROOT>\workspace\runtime\tensorcube\ash_tensorcube_decode_04_local_manifest_latest.json
```

## 25. Next state

A DECODE-04 PASS authorizes only:

```text
ASH-TCU-DECODE-05_LIVE_SHADOW_REPEATABILITY_AND_SCOPE_EXPANSION_GATE
```

It does not authorize production output promotion, TensorCube logits merge, sampler consumption, all 47 full tiles, ragged-tail execution, Burn removal, latency claims or hardware Tensor Core claims.

## 26. Final invariant

```text
The same live TensorCube command proven by DECODE-03 completes.
Exactly 1024 f32 candidate values are read back once.
The existing live Burn tile-0 output is the only reference.
Degenerate zero-to-zero evidence cannot masquerade as parity.
Numerical mismatch cannot influence generation.
Burn remains the only authority for every returned logit and token.
The only new truth is a bounded, hash-sealed numerical observation of one live full-tile invocation.
```
