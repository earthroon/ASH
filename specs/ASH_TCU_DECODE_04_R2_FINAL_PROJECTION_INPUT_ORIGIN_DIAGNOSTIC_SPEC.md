# ASH-TCU-DECODE-04-R2 SPEC

## FINAL_PROJECTION_INPUT_ORIGIN_DIAGNOSTIC

```text
patch_id=ASH-TCU-DECODE-04-R2_FINAL_PROJECTION_INPUT_ORIGIN_DIAGNOSTIC
parent_patch=ASH-TCU-DECODE-04-R1_LIVE_PROJECTION_INPUT_AND_RUNTIME_RHS_NONDEGENERACY_DIAGNOSTIC
parent_code_hotfix=ASH-TCU-DECODE-04-R1-R1_CRATE_ROOT_NATIVE_API_COMPILE_CLOSURE
parent_package=ash_pass3_ASH-TCU-DECODE-04-R1-R1_crate_root_native_api_compile_closure_code_baked_no_spec_no_docs_no_runtime_artifacts_no_sha.zip
parent_package_sha256=5c5dd6e0e78c5e12f6001f73ac945ed50a47d5f7f9f00d40e711bab79c8688e3
parent_execution_id=decode04r1-a3a4c02bc06a420be761
parent_status=PASS_ASH_TCU_DECODE_04_R1_LIVE_PROJECTION_INPUT_AND_RUNTIME_RHS_NONDEGENERACY_DIAGNOSTIC
parent_verdict=decode04_r1_projection_input_degenerate
parent_root_cause_class=projection_input_degenerate
parent_decode04_execution_id=decode04-9536340a5ad0c628f829
parent_route_digest=1b9009ff7216b57f6bcabeb0eb39d9c8d5e99019601f40de052166ff8f138327
model_layer_count=22
hidden_size=2048
selected_generation_step=0
smoke_token_id=1
mutation_class=bounded_live_hidden_state_origin_diagnostic
output_authority=burn
production_authority=false
runtime_output_changed=false
```

## 1. Status

```text
PASS=PASS_ASH_TCU_DECODE_04_R2_FINAL_PROJECTION_INPUT_ORIGIN_DIAGNOSTIC
HOLD=HOLD_ASH_TCU_DECODE_04_R2_FINAL_PROJECTION_INPUT_ORIGIN_DIAGNOSTIC
FAIL=FAIL_ASH_TCU_DECODE_04_R2_FINAL_PROJECTION_INPUT_ORIGIN_DIAGNOSTIC
```

R2 PASS means that one earliest origin class was sealed. It does not mean the model defect was repaired, DECODE-04 parity passed, or TensorCube gained production authority.

## 2. Purpose

R1 proved that the checkpoint embedding row and source/runtime vocab RHS are nonzero, the runtime RHS is bit-exact with the source tile, and the live raw binding contract is valid, while the live projection input is exactly zero. R2 localizes the first zero or first identity-bridge corruption between embedding output and vocab projection input.

The diagnostic observes one selected-token hidden row during one generation smoke pass. It does not rerun generation, replace tensors, alter KV state, or commit diagnostic values downstream.

## 3. Parent truth

```text
projection_input_element_count=2048
projection_input_nonzero_count=0
projection_input_l2_norm=0
projection_input_value_span=0
source_rhs_nonzero_count=2097151
runtime_rhs_nonzero_count=2097151
source_runtime_rhs_exact_match=true
raw_binding_contract_valid=true
lhs_binding_size=8192
rhs_binding_size=8388608
burn_output_degenerate=true
candidate_output_degenerate=true
burn_candidate_digest_equal=true
burn_output_authority=true
runtime_output_changed=false
```

The parent manifest and immutable final seal, projection-input receipt, runtime-RHS receipt, raw-binding receipt, and authority-firewall receipt must be SHA-256 verified before model execution.

## 4. Activation

```rust
pub fn configure_tensorcube_decode04_r2_final_projection_input_origin_diagnostic(
    &mut self,
    config: Decode04R2DiagnosticConfig,
) -> anyhow::Result<serde_json::Value>;

pub fn run_tensorcube_decode04_r2_live_generation_smoke(
    &self,
    token_id: u32,
) -> anyhow::Result<Decode04R2DiagnosticReceipt>;
```

Canonical configuration:

```text
parent_execution_id=decode04r1-a3a4c02bc06a420be761
parent_decode04_execution_id=decode04-9536340a5ad0c628f829
route_digest=1b9009ff7216b57f6bcabeb0eb39d9c8d5e99019601f40de052166ff8f138327
smoke_token_id=1
generation_step_ordinal=0
layer_count=22
hidden_size=2048
stage_checkpoint_count=70
identity_bridge_count=24
diagnostic_timeout_ms=120000
require_parent_projection_degeneracy_reproduction=true
require_exact_identity_bridge_digests=true
forbid_second_generation_pass=true
forbid_raw_payload_persistence=true
```

DECODE-03, DECODE-04, DECODE-04-R1, and DECODE-04-R2 modes are mutually exclusive in one model instance.

## 5. Stage plan

Exactly 70 ordered checkpoints are observed:

```text
00 embedding_output
01 layer_00_input
02 layer_00_post_attention_residual
03 layer_00_output
...
64 layer_21_input
65 layer_21_post_attention_residual
66 layer_21_output
67 final_norm_input
68 final_norm_output
69 projection_input
```

Count:

```text
embedding checkpoints=1
layer checkpoints=22*3=66
final norm checkpoints=2
projection checkpoints=1
total=70
```

Each checkpoint observes exactly one selected row:

```text
element_count=2048
byte_count=8192
selected_batch_index=0
selected_token_index=0
```

## 6. Per-stage evidence

Each stage records only bounded statistics and hashes:

```text
ordinal
stage_id
stage_kind
layer_index
source_shape
element_count
byte_count
finite_count
nonzero_count
positive_zero_count
negative_zero_count
min_value
max_value
value_span
l1_norm
l2_norm
max_abs_value
f32_bit_digest_sha256
non_degenerate
bounded_witnesses<=16
```

Digest contract:

```text
algorithm=SHA-256
value_encoding=little-endian IEEE-754 f32 bits
iteration_order=selected row logical order 0..2047
negative_zero=bit pattern preserved
NaN_or_Infinity=FAIL
```

No full 2048-value vector may be persisted.

## 7. Nondegeneracy

A stage is nondegenerate only when:

```text
finite_count=2048
nonzero_count>=16
l2_norm>1.0e-6
value_span>1.0e-6
```

A finite all-zero row is degenerate. NaN or infinity is contract corruption and produces FAIL.

## 8. Identity bridges

Exactly 24 no-op state-transfer bridges require exact f32-bit digest equality:

```text
embedding_output -> layer_00_input
layer_00_output -> layer_01_input
...
layer_20_output -> layer_21_input
layer_21_output -> final_norm_input
final_norm_output -> projection_input
```

Each bridge records:

```text
from_stage_id
to_stage_id
from_digest
to_digest
digest_equal
from_non_degenerate
to_non_degenerate
bridge_contract_valid
```

No numerical tolerance is permitted on identity bridges.

## 9. Earliest-origin ownership

Classification is ordered and fail-closed. Later zeros cannot overwrite an earlier origin.

```text
1. RuntimeEmbeddingOutputDegenerate
2. EmbeddingToLayer0IngressBridgeDrift
3. for layer 0..21:
   a. AttentionResidualDegenerateAtLayer<N>
   b. FfnResidualDegenerateAtLayer<N>
   c. LayerBoundaryBridgeDriftAfterLayer<N> for N<21
4. FinalNormInputBridgeDrift
5. FinalNormOutputDegenerate
6. ProjectionInputExtractionDegenerate
7. ParentProjectionDegeneracyNotReproduced
8. AmbiguousOrigin
```

Ownership conditions:

```text
RuntimeEmbeddingOutputDegenerate:
  embedding_output is degenerate

EmbeddingToLayer0IngressBridgeDrift:
  embedding_output nondegenerate
  layer_00_input digest differs

AttentionResidualDegenerateAtLayer<N>:
  layer_N_input nondegenerate
  layer_N_post_attention_residual degenerate

FfnResidualDegenerateAtLayer<N>:
  layer_N_post_attention_residual nondegenerate
  layer_N_output degenerate

LayerBoundaryBridgeDriftAfterLayer<N>:
  layer_N_output digest differs from layer_N+1_input

FinalNormInputBridgeDrift:
  layer_21_output digest differs from final_norm_input

FinalNormOutputDegenerate:
  final_norm_input nondegenerate
  final_norm_output degenerate

ProjectionInputExtractionDegenerate:
  final_norm_output nondegenerate
  projection_input degenerate or digest differs
```

`ParentProjectionDegeneracyNotReproduced` and `AmbiguousOrigin` produce HOLD, not silent recovery.

## 10. Single-pass and authority firewall

```text
prompt_count=1
generation_pass_count=1
generation_step_ordinal=0
stage_materialization_count=70
stage_total_readback_elements=143360
stage_total_readback_bytes=573440
identity_bridge_validation_count=24
origin_classification_count=1
additional_tensorcube_dispatch_count=0
additional_vocab_projection_count=0
full_vector_artifact_count=0
diagnostic_hidden_replacement_count=0
diagnostic_kv_cache_write_count=0
diagnostic_logits_use_count=0
diagnostic_sampler_use_count=0
shadow_output_commit_count=0
downstream_output_commit_count=0
burn_output_authority=true
production_authority=false
runtime_output_changed=false
```

Diagnostic values may flow only to statistics, digest generation, bridge comparison, root-cause classification, and bounded artifacts. They must never replace hidden state, enter logits, alter KV cache, feed top-k or sampling, or select a token.

## 11. Required source changes

```text
crates/burn_webgpu_backend/src/tensorcube_decode_04_r2_final_projection_input_origin_diagnostic.rs
crates/burn_webgpu_backend/src/lib.rs
crates/model_core/src/native_wgpu.rs
crates/model_core/tests/ash_tcu_decode_04_r2_final_projection_input_origin_diagnostic.rs
crates/orchestrator_local/src/ash_tcu_decode_04_r2_final_projection_input_origin_diagnostic_report.rs
crates/orchestrator_local/src/bin/ash_tcu_decode_04_r2_final_projection_input_origin_diagnostic.rs
crates/orchestrator_local/src/lib.rs
crates/orchestrator_local/Cargo.toml
```

When R2 is disabled, the normal forward path remains unchanged.

## 12. Required tests

Backend tests seal stage ordering, bridge ordering, digest determinism, zero accounting, bounded witnesses, every canonical root-cause class, HOLD classes, and earliest-origin precedence.

Model tests seal R2 fields and methods, live-forward stage insertion, actual projection-input observation, mode mutual exclusion, Cargo binary registration, and the output-authority firewall.

## 13. Artifacts

Immutable root:

```text
artifacts/tensorcube/decode_04_r2/<execution_id>/
```

Latest mirrors:

```text
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r2_*_latest.json
```

Required artifacts:

```text
parent_chain
activation_receipt
stage_plan
hidden_stage_trace
identity_bridge_receipt
parent_reproduction_receipt
first_origin_receipt
root_cause_classification
authority_firewall
protected_state_guard
source_digest_manifest
report
final_seal
verdict
local_manifest
```

The local manifest is written last. Full embedding, hidden, norm, projection-input, model-weight, KV-cache, logits, or TensorCube candidate vectors are forbidden.

## 14. Error classification

HOLD:

```text
GPU or checkpoint unavailable
stage materialization unavailable
parent projection degeneration not reproduced
ambiguous origin
bounded diagnostic timeout
```

FAIL:

```text
parent manifest or artifact hash mismatch
wrong parent execution/status/verdict/class/route
stage count/order/cardinality drift
identity bridge count drift
NaN or infinity
second generation pass
fixture substitution
full vector persistence
hidden or KV mutation
logits, sampler, or output use
authority change
protected source/model spec/checkpoint mutation
manifest not written last
```

HOLD and FAIL preserve Burn authority and zero diagnostic output commits.

## 15. CLI

```text
--repo-root <PATH>
--model-spec <PATH>
--checkpoint <PATH> [repeatable]
--parent-manifest <PATH>
--smoke-token-id 1
--diagnostic-timeout-ms 120000
--activate-final-projection-input-origin-diagnostic
--run-live-generation-smoke
--require-parent-r1-projection-input-degenerate-pass
--require-layer-count 22
--require-hidden-size 2048
--require-stage-checkpoint-count 70
--require-stage-elements 2048
--require-stage-bytes 8192
--require-identity-bridge-count 24
--require-parent-projection-degeneracy-reproduction
--require-first-origin-classification
--require-exact-identity-bridge-digests
--require-no-second-generation-pass
--require-no-host-upload
--require-no-fixture-substitution
--require-no-full-vector-artifacts
--require-no-output-commit
--require-burn-output-authority
--require-no-runtime-output-change
--write-runtime-artifacts
--write-local-manifest
```

Exit codes:

```text
0=PASS earliest root-cause class sealed
2=HOLD diagnosis not reproduced or ambiguous
1=FAIL contract corruption or authority violation
```

## 16. Expected console

```text
PASS_ASH_TCU_DECODE_04_R2_FINAL_PROJECTION_INPUT_ORIGIN_DIAGNOSTIC
verdict=<SEALED_VERDICT>
root_cause_class=<SEALED_CLASS>
execution_id=decode04r2-<digest-prefix>
parent_execution_id=decode04r1-a3a4c02bc06a420be761
parent_decode04_execution_id=decode04-9536340a5ad0c628f829
route_digest=1b9009ff7216b57f6bcabeb0eb39d9c8d5e99019601f40de052166ff8f138327
stage_checkpoint_count=70
identity_bridge_count=24
first_degenerate_stage_id=<MEASURED>
previous_stage_id=<MEASURED>
layer_index=<MEASURED_OR_NONE>
parent_projection_degeneracy_reproduced=true
full_vector_artifact_count=0
shadow_output_commit_count=0
burn_output_authority=true
runtime_output_changed=false
local_manifest=<ASH_ROOT>/workspace/runtime/tensorcube/ash_tensorcube_decode_04_r2_local_manifest_latest.json
```

## 17. Next state

```text
RuntimeEmbeddingOutputDegenerate
-> ASH-TCU-DECODE-04-R3_RUNTIME_EMBEDDING_OUTPUT_ORIGIN_DIAGNOSTIC

EmbeddingToLayer0IngressBridgeDrift
-> ASH-TCU-DECODE-04-R3_EMBEDDING_LAYER0_STATE_TRANSFER_REPAIR

AttentionResidualDegenerateAtLayer<N>
-> ASH-TCU-DECODE-04-R3_LAYER_<N>_ATTENTION_RESIDUAL_DIFFERENTIAL_DIAGNOSTIC

FfnResidualDegenerateAtLayer<N>
-> ASH-TCU-DECODE-04-R3_LAYER_<N>_FFN_RESIDUAL_DIFFERENTIAL_DIAGNOSTIC

LayerBoundaryBridgeDriftAfterLayer<N>
-> ASH-TCU-DECODE-04-R3_LAYER_<N>_<N+1>_STATE_TRANSFER_REPAIR

FinalNormInputBridgeDrift
-> ASH-TCU-DECODE-04-R3_FINAL_NORM_INPUT_STATE_TRANSFER_REPAIR

FinalNormOutputDegenerate
-> ASH-TCU-DECODE-04-R3_FINAL_NORM_ARITHMETIC_DIFFERENTIAL_DIAGNOSTIC

ProjectionInputExtractionDegenerate
-> ASH-TCU-DECODE-04-R3_PROJECTION_INPUT_SLICE_RESHAPE_OWNERSHIP_REPAIR
```

After any repair, rerun R2 and then rerun DECODE-04 with unchanged parity tolerances. R2 never directly authorizes DECODE-05.

## 18. Package boundary

The baked ZIP contains code only. Forbidden paths:

```text
specs/
docs/
artifacts/
workspace/runtime/
target/
*.sha
*.sha256
```

No R2 receipt, manifest, verdict, PASS marker, hidden vector, or runtime artifact may be baked into the package.

## 19. Final invariant

```text
The R1 projection-input degeneration is the only authorized parent class.
The live selected-token hidden row is observed at exactly 70 ordered checkpoints.
Every observation is finite, bounded, and hash-sealed.
Every no-op state bridge is checked by exact f32-bit digest continuity.
The earliest degeneration or bridge corruption boundary owns the diagnosis.
Later zero vectors cannot overwrite an earlier origin.
No full hidden vector is persisted.
No diagnostic value can modify hidden states, logits, sampling, or token output.
Burn remains the sole production authority.
R2 creates origin truth, not repair or promotion authority.
```