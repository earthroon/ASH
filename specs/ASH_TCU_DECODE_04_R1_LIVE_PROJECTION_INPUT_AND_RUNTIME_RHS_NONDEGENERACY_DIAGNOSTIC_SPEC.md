# ASH-TCU-DECODE-04-R1 SPEC

## LIVE_PROJECTION_INPUT_AND_RUNTIME_RHS_NONDEGENERACY_DIAGNOSTIC

```text
patch_id=ASH-TCU-DECODE-04-R1_LIVE_PROJECTION_INPUT_AND_RUNTIME_RHS_NONDEGENERACY_DIAGNOSTIC
parent_patch=ASH-TCU-DECODE-04_LIVE_SHADOW_COMPLETION_READBACK_PARITY_GATE
parent_package=ash_pass3_ASH-TCU-DECODE-04_live_shadow_completion_readback_parity_gate_code_baked_no_spec_no_docs_no_runtime_artifacts_no_sha.zip
parent_package_sha256=2985ad1513a62c53f1b44b380680f8d24265861c66e95a1260fadc933d80bed0
parent_execution_id=decode04-9536340a5ad0c628f829
parent_status=HOLD_ASH_TCU_DECODE_04_LIVE_SHADOW_COMPLETION_READBACK_PARITY_GATE
parent_verdict=decode04_live_burn_reference_degenerate
parent_route_digest=1b9009ff7216b57f6bcabeb0eb39d9c8d5e99019601f40de052166ff8f138327
selected_generation_step=0
selected_tile_id=0
selected_tile_span=[0,1024)
mutation_class=bounded_live_projection_input_and_runtime_rhs_truth_diagnostic
output_authority=burn
production_authority=false
runtime_output_changed=false
```

## 1. Status contract

```text
PASS=PASS_ASH_TCU_DECODE_04_R1_LIVE_PROJECTION_INPUT_AND_RUNTIME_RHS_NONDEGENERACY_DIAGNOSTIC
HOLD=HOLD_ASH_TCU_DECODE_04_R1_LIVE_PROJECTION_INPUT_AND_RUNTIME_RHS_NONDEGENERACY_DIAGNOSTIC
FAIL=FAIL_ASH_TCU_DECODE_04_R1_LIVE_PROJECTION_INPUT_AND_RUNTIME_RHS_NONDEGENERACY_DIAGNOSTIC
```

R1 PASS means that the diagnostic completed, evidence was internally coherent, Burn remained the sole output authority, and one root-cause class was sealed. It does not mean that DECODE-04 numerical parity passed.

A PASS diagnostic may identify a defect domain.

## 2. Parent truth

The parent execution established:

```text
execution_id=decode04-9536340a5ad0c628f829
route_digest=1b9009ff7216b57f6bcabeb0eb39d9c8d5e99019601f40de052166ff8f138327
status=HOLD_ASH_TCU_DECODE_04_LIVE_SHADOW_COMPLETION_READBACK_PARITY_GATE
verdict=decode04_live_burn_reference_degenerate
raw_buffer_lease_count=2
tensorcube_dispatch_count=1
scratch_copy_count=1
queue_submit_count=1
readback_count=1
readback_bytes=4096
readback_f32_count=1024
candidate_non_finite_count=0
burn_reference_capture_count=1
burn_nonzero_count=0
burn_l2_norm=0
burn_value_span=0
candidate_digest=ad7facb2586fc6e966c004d7d1d16b024f5805ff7cb47c7a85dabd8b48892ca7
burn_reference_digest=ad7facb2586fc6e966c004d7d1d16b024f5805ff7cb47c7a85dabd8b48892ca7
shadow_output_commit_count=0
burn_output_authority=true
runtime_output_changed=false
```

The R1 audit must verify the parent local manifest and the consumed immutable final seal, Burn reference receipt, and candidate readback receipt by SHA-256.

## 3. Purpose

Independent inspection proved that checkpoint embedding row 1 and checkpoint LM-head rows `[0,1024)` are non-degenerate, while the live Burn tile-0 output and live TensorCube candidate are the same all-zero vector.

R1 must reproduce the relevant facts inside Rust and assign the zero origin to one ownership boundary:

1. the exact live projection input `last_hidden`;
2. the exact runtime vocab-atlas tile-0 weight tensor;
3. the exact raw lease shape, offset, and binding range used by TensorCube;
4. the shared projection arithmetic or layout contract after both inputs are proven non-degenerate.

R1 must not weaken the DECODE-04 non-degeneracy gate, change tolerances, change smoke token, rotate to another tile, or promote TensorCube output.

## 4. Live object identity

The same objects must be used by the parent projection and the diagnostic:

```text
lhs = exact last_hidden Tensor object used by Burn and TensorCube
rhs = exact NativeVocabAtlas.tiles[0].weight Tensor object used by Burn and TensorCube
```

The model path remains:

```text
smoke token 1
-> native embedding row gather
-> transformer forward
-> final normalized hidden
-> last_hidden [1,2048]
-> vocab-atlas tile-0 projection
```

The existing Burn projection remains:

```rust
let tile_logits = last_hidden
    .clone()
    .matmul(tile.weight.clone().swap_dims(0, 1))
    .reshape([tile.token_len]);
```

## 5. Authorized diagnostic observations

Exactly one activated generation may add:

```text
projection_input_materialization_count=1
projection_input_element_count=2048
projection_input_bytes=8192

runtime_rhs_materialization_count=1
runtime_rhs_element_count=2097152
runtime_rhs_bytes=8388608

source_rhs_host_observation_count=1
selected_source_tile_id=0
raw_binding_metadata_capture_count=1
root_cause_classification_count=1
```

The source evidence must be computed only for tile 0, directly over the existing `lm_head_cpu` slice before `TensorData::new`. It must not clone the full source tile merely to compute evidence.

The full projection input and full runtime RHS are ephemeral. They must not be serialized. At most 32 bounded runtime witness rows may be persisted.

## 6. Canonical f32 digest

Source and runtime RHS use the same digest contract:

```text
algorithm=SHA-256
encoding=little-endian IEEE-754 f32 bits
order=row-major [1024,2048]
negative_zero=bit pattern preserved
NaN_or_Infinity=FAIL
```

Exact source/runtime equality requires:

```text
source_element_count=2097152
runtime_element_count=2097152
source_bytes=8388608
runtime_bytes=8388608
source_digest == runtime_digest
```

Sampling may not be used to claim full equality.

## 7. Raw binding contract

The binding receipt must be built from the same two live leases used by the DECODE-04 dispatch.

Canonical LHS:

```text
shape=[1,2048]
len_elements=2048
bytes_per_element=4
expected_bytes=8192
binding_size=8192
buffer_offset_mod_4=0
```

Canonical RHS:

```text
shape=[1024,2048]
len_elements=2097152
bytes_per_element=4
expected_bytes=8388608
binding_size=8388608
buffer_offset_mod_4=0
```

Required shared-runtime evidence:

```text
same_runtime_device=true
same_runtime_queue=true
raw_buffer_lease_count=2
host_upload_count=0
fixture_registry_hit_count=0
live_fusion_resolve_count=2
vendor_access_path=fusion_client.resolve_tensor_float_gpu_only
```

Metadata from a second lease or a fixture may not substitute for the exact leases consumed by the live dispatch.

## 8. Non-degeneracy thresholds

The unchanged thresholds are:

```text
nonzero_count>=16
l2_norm>1.0e-6
value_span>1.0e-6
```

They apply independently to:

```text
projection input
source RHS
runtime RHS
Burn tile-0 output
TensorCube candidate
```

DECODE-04 numerical thresholds remain unchanged:

```text
absolute_tolerance=0.001
relative_tolerance=0.001
hard_absolute_ceiling=0.01
require_non_degenerate_reference=true
```

## 9. Root-cause classes and precedence

The classifier must return exactly one class when evidence is complete.

```text
RawBindingContractInvalid
ProjectionInputDegenerate
RuntimeRhsDegenerateAfterNondegenerateSource
RuntimeRhsSourceDigestDrift
SharedProjectionArithmeticOrLayoutSuspect
ReferenceRecoveredAndParityReEvaluable
AmbiguousEvidence
```

Precedence is fixed:

```text
1. invalid live binding contract
   -> RawBindingContractInvalid

2. valid binding and degenerate last_hidden
   -> ProjectionInputDegenerate

3. non-degenerate projection input and source RHS, degenerate runtime RHS
   -> RuntimeRhsDegenerateAfterNondegenerateSource

4. non-degenerate runtime RHS with source/runtime digest mismatch
   -> RuntimeRhsSourceDigestDrift

5. non-degenerate projection input, exact non-degenerate source/runtime RHS,
   valid bindings, Burn and candidate both degenerate with equal digest
   -> SharedProjectionArithmeticOrLayoutSuspect

6. non-degenerate projection input, exact non-degenerate source/runtime RHS,
   valid bindings, Burn reference non-degenerate
   -> ReferenceRecoveredAndParityReEvaluable

7. otherwise
   -> AmbiguousEvidence
```

`AmbiguousEvidence` produces HOLD and may not pass.

## 10. Output authority firewall

Diagnostic data may flow only to:

```text
R1 statistics
R1 digests
bounded witness rows
root-cause classifier
Rust artifacts
```

It must never flow to:

```text
merged_logits
top_k_tile_candidates
sampler
token selection
fallback output
production cache
output commit
```

The existing Burn `tile_row` remains the only value appended to `merged_logits`.

Required counters:

```text
additional_generation_count=0
additional_tensorcube_dispatch_count=0
additional_tensorcube_candidate_readback_count=0
additional_burn_projection_count=0
full_raw_vector_artifact_count=0
shadow_output_commit_count=0
downstream_output_commit_count=0
burn_output_authority=true
production_authority=false
runtime_output_changed=false
```

## 11. Lifecycle ownership

The generation-scoped session records the following exactly once and in order, after the parent DECODE-04 parity observation:

```text
decode04_r1_binding_metadata_captured
decode04_r1_projection_input_materialized
decode04_r1_runtime_rhs_materialized
decode04_r1_output_correlation_built
decode04_r1_root_cause_classified
```

Partial R1 lifecycle state is a contract failure.

## 12. Required source surfaces

```text
crates/burn_webgpu_backend/src/tensorcube_decode_04_r1_projection_input_rhs_diagnostic.rs
crates/burn_webgpu_backend/src/tensorcube_decode_04_live_parity.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d0r1_shadow_observer_owner.rs
crates/burn_webgpu_backend/src/lib.rs
crates/model_core/src/native_wgpu.rs
crates/model_core/tests/ash_tcu_decode_04_r1_live_projection_input_and_runtime_rhs_nondegeneracy_diagnostic.rs
crates/orchestrator_local/src/ash_tcu_decode_04_r1_live_projection_input_and_runtime_rhs_nondegeneracy_diagnostic_report.rs
crates/orchestrator_local/src/bin/ash_tcu_decode_04_r1_live_projection_input_and_runtime_rhs_nondegeneracy_diagnostic.rs
crates/orchestrator_local/src/lib.rs
crates/orchestrator_local/Cargo.toml
```

## 13. Required tests

Backend tests must cover:

```text
canonical_f32_digest_preserves_negative_zero_bits
projection_input_degeneracy_threshold_truth_table
runtime_rhs_exact_digest_match
bounded_rhs_runtime_witness_rows_max_32
raw_binding_exact_range_validation_truth
classification_binding_invalid_precedes_value_classes
classification_projection_input_degenerate
classification_runtime_rhs_degenerate
classification_runtime_rhs_source_drift
classification_shared_projection_arithmetic_suspect
classification_reference_recovered
ambiguous_evidence_cannot_pass
```

Model-core tests must prove:

```text
source evidence precedes tensor upload and belongs only to tile 0
the same live last_hidden and tile.weight objects are observed
projection input and runtime RHS are materialized once
R1 adds no dispatch and no Burn projection
candidate and diagnostic values never enter generation output
full vectors are forbidden from artifacts
```

## 14. Rust artifact contract

Immutable root:

```text
artifacts/tensorcube/decode_04_r1/<execution_id>/
```

Latest mirrors:

```text
workspace/runtime/tensorcube/
```

Required immutable artifacts:

```text
ash_tensorcube_decode_04_r1_parent_chain.json
ash_tensorcube_decode_04_r1_activation_receipt.json
ash_tensorcube_decode_04_r1_source_rhs_receipt.json
ash_tensorcube_decode_04_r1_projection_input_receipt.json
ash_tensorcube_decode_04_r1_runtime_rhs_receipt.json
ash_tensorcube_decode_04_r1_raw_binding_receipt.json
ash_tensorcube_decode_04_r1_output_correlation_receipt.json
ash_tensorcube_decode_04_r1_root_cause_classification.json
ash_tensorcube_decode_04_r1_authority_firewall.json
ash_tensorcube_decode_04_r1_protected_state_guard.json
ash_tensorcube_decode_04_r1_source_digest_manifest.json
ash_tensorcube_decode_04_r1_report.json
ash_tensorcube_decode_04_r1_final_seal.json
ash_tensorcube_decode_04_r1_verdict.json
ash_tensorcube_decode_04_r1_local_manifest.json
```

Each manifest row contains:

```text
name
schema
artifact_role
relative_path
immutable_path
latest_path
size_bytes
sha256
```

The local manifest must be written last.

## 15. Canonical binary and CLI

Binary:

```text
ash_tcu_decode_04_r1_live_projection_input_and_runtime_rhs_nondegeneracy_diagnostic
```

CLI:

```text
--repo-root <PATH>
--model-spec <PATH>
--checkpoint <PATH> [repeatable]
--parent-manifest <PATH>
--smoke-token-id 1
--completion-timeout-ms 30000
--activate-live-input-rhs-diagnostic
--run-live-generation-smoke
--require-parent-decode04-degenerate-hold
--require-projection-input-elements 2048
--require-projection-input-bytes 8192
--require-runtime-rhs-elements 2097152
--require-runtime-rhs-bytes 8388608
--require-full-runtime-rhs-digest
--require-exact-source-runtime-rhs-digest
--require-exact-live-binding-ranges
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
0=PASS diagnostic sealed with one root-cause class
2=HOLD diagnostic incomplete or ambiguous
1=FAIL contract corruption or authority violation
```

## 16. Expected console contract

```text
PASS_ASH_TCU_DECODE_04_R1_LIVE_PROJECTION_INPUT_AND_RUNTIME_RHS_NONDEGENERACY_DIAGNOSTIC
verdict=<SEALED_DIAGNOSTIC_VERDICT>
root_cause_class=<SEALED_CLASS>
execution_id=decode04r1-<digest-prefix>
parent_execution_id=decode04-9536340a5ad0c628f829
route_digest=1b9009ff7216b57f6bcabeb0eb39d9c8d5e99019601f40de052166ff8f138327
projection_input_nonzero_count=<MEASURED>
projection_input_l2_norm=<MEASURED>
projection_input_value_span=<MEASURED>
source_rhs_nonzero_count=<MEASURED>
runtime_rhs_nonzero_count=<MEASURED>
source_runtime_rhs_exact_match=<MEASURED>
raw_binding_contract_valid=<MEASURED>
lhs_binding_size=<MEASURED>
rhs_binding_size=<MEASURED>
burn_output_degenerate=<MEASURED>
candidate_output_degenerate=<MEASURED>
burn_candidate_digest_equal=<MEASURED>
burn_output_authority=true
runtime_output_changed=false
local_manifest=<ASH_ROOT>/workspace/runtime/tensorcube/ash_tensorcube_decode_04_r1_local_manifest_latest.json
```

## 17. Next-state routing

```text
ProjectionInputDegenerate
-> ASH-TCU-DECODE-04-R2_FINAL_PROJECTION_INPUT_ORIGIN_DIAGNOSTIC

RuntimeRhsDegenerateAfterNondegenerateSource
-> ASH-TCU-DECODE-04-R2_VOCAB_ATLAS_MATERIALIZATION_TRUTH_REPAIR

RuntimeRhsSourceDigestDrift
-> ASH-TCU-DECODE-04-R2_VOCAB_ATLAS_SOURCE_RUNTIME_DIGEST_REPAIR

RawBindingContractInvalid
-> ASH-TCU-DECODE-04-R2_LIVE_RAW_BINDING_RANGE_TRUTH_REPAIR

SharedProjectionArithmeticOrLayoutSuspect
-> ASH-TCU-DECODE-04-R2_SHARED_PROJECTION_LAYOUT_AND_ARITHMETIC_DIFFERENTIAL_GATE

ReferenceRecoveredAndParityReEvaluable
-> rerun ASH-TCU-DECODE-04 under unchanged thresholds
```

R1 does not authorize DECODE-05. Only a subsequent DECODE-04 numerical PASS may authorize DECODE-05.

## 18. Package boundary

The baked ZIP contains code only.

Forbidden packaged paths:

```text
specs/
docs/
artifacts/
workspace/runtime/
target/
*.sha
*.sha256
```

No precomputed R1 receipt, verdict, manifest, PASS marker, hidden vector, or RHS vector may be baked into the package.

## 19. Final invariant

```text
The parent zero-to-zero HOLD is not weakened.
The exact live projection input is measured once.
The exact runtime vocab-atlas tile-0 RHS is measured once in full.
The runtime RHS is compared bit-for-bit with the source f32 tile.
The exact TensorCube binding ranges come from the live dispatch leases.
One root-cause domain is sealed when evidence is complete.
No full hidden or weight vector is persisted.
No diagnostic value can influence logits, sampling, or token output.
Burn remains the sole production authority.
R1 creates diagnostic truth, not promotion authority.
```
