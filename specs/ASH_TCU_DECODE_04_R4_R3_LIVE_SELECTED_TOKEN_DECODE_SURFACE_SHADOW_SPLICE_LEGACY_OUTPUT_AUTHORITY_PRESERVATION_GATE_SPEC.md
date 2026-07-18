# ASH-TCU-DECODE-04-R4-R3
# Live Selected Token Decode Surface Shadow Splice / Legacy Output Authority Preservation Gate

- Patch ID: `ASH-TCU-DECODE-04-R4-R3_LIVE_SELECTED_TOKEN_DECODE_SURFACE_SHADOW_SPLICE_LEGACY_OUTPUT_AUTHORITY_PRESERVATION_GATE`
- Parent: `ASH-TCU-DECODE-04-R4-R2-R2_LIVE_DECODESTATE_KV_BOUNDARY_SNAPSHOT_PARITY_AND_NO_PRODUCTION_HANDLE_TRUTH_GATE`
- Runtime mode: `live_generation_shadow_splice_compare_only`
- Legacy output authority: `exclusive`
- TensorCube production authority: `false`
- PASS authorizes: `ASH-TCU-DECODE-04-R4-R3-R1_STATEFUL_FRAGMENT_STAGING_AND_SENTENCEPIECE_CONTEXT_OWNERSHIP_GATE`
- Production replacement: `forbidden`

## 1. Purpose

R4-R3 inserts the accepted R4-R2 selected-token decode surface beside the existing generation decoder. For every production-selected token, the legacy decoder remains authoritative while TensorCube records an immutable comparison receipt.

```text
production selected token
  |-- legacy append path       -> user-visible text and stream authority
  `-- TensorCube shadow splice -> comparison receipt only
```

The gate proves exact selected-token binding, four-route splice coverage, legacy output authority, shadow on/off parity, zero TensorCube mutation authority, and classified mismatch evidence.

## 2. Concrete SSOT

The implementation SSOT is:

```text
model_core::append_legacy_fragment_with_r4r3_shadow
model_core::observe_r4r3_live_selected_token_shadow
model_core::R4R3LiveShadowSpliceReceipt
GenerationTelemetry::tensorcube_r4_r3_live_shadow_splice
```

The existing `append_token_piece_to_text` remains the only fragment producer. The helper calls it first, preserves its exact return value and output mutation, then invokes the immutable TensorCube observer.

The live shadow activation seal is:

```text
ASH_TCU_DECODE04_R4_R3_SHADOW=1
```

When the seal is absent, legacy execution remains unchanged and no R4-R3 live receipt is produced.

## 3. Hot-path route matrix

All eight token-materialization call sites must route through the same helper:

| Route | Initial token | Decode-loop token |
|---|---:|---:|
| `sampled_cached` | required | required |
| `sampled_streaming` | required | required |
| `greedy_cached` | required | required |
| `greedy_streaming` | required | required |

Required structural truth:

```text
route_adapter_count=4
canonical_splice_function_count=1
route_adapter_duplicate_classifier_count=0
route_adapter_duplicate_tokenizer_lookup_count=0
bypass_route_count=0
```

Streaming routes may forward only the fragment returned by the legacy append helper. TensorCube fragments may never be pushed into `StreamingTextHoldback` or a production sink.

## 4. Observer capability boundary

The observer may receive only:

- immutable tokenizer manifest
- copied selected token ID
- copied generation epoch and step index
- copied route ID and stream mode
- immutable legacy fragment observation
- copied output lengths

Forbidden capabilities:

```text
&mut DecodeState
&mut KvCache
&mut output sink
&mut stream sink
sampler handle
RNG handle
wgpu::Queue
wgpu::CommandEncoder
finish or stop mutation handle
route-switch handle
production transaction handle
```

Every forbidden capability counter must be zero.

## 5. Canonical TensorCube surface

The observer must call the accepted R4-R2 implementation:

```text
build_r4r2_primary_decode_surface
```

It records:

- exact selected token ID
- raw piece and piece kind
- special-token class and reserved group
- start-context fragment
- continuation-context fragment
- byte-fragment pending state
- text-materialization readiness
- output suppression and structural line-break semantics
- canonical surface digest

R4-R3 may compare start and continuation projections, but may not choose either as production output.

## 6. Comparison classes

Every observed step receives exactly one class:

```text
exact_fragment_match
exact_empty_match
tensor_cube_start_projection_match
tensor_cube_continuation_projection_match
structural_line_break_match
control_suppression_match
byte_fragment_deferred_by_tensor_cube
legacy_replacement_character_observed
context_dependent_difference
special_token_policy_deferred
invalid_utf8_difference
unexpected_mismatch
```

Expected structural differences are evidence, not fallback triggers. `unexpected_mismatch` is FAIL. No mismatch may rewrite the legacy fragment, select another token, or invoke another tokenizer.

## 7. Exact token binding

For every receipt:

```text
production_selected_token_id
== legacy_observed_token_id
== tensorcube_observed_token_id
```

The shadow path must not invoke sampling, read or advance RNG, reorder candidates, apply penalties, or replace an unknown token with UNK.

## 8. Legacy authority and no-mutation contract

Required counters:

```text
tensorcube_token_append_attempt_count=0
tensorcube_kv_mutation_attempt_count=0
tensorcube_text_emit_attempt_count=0
tensorcube_stream_emit_attempt_count=0
tensorcube_finish_stop_attempt_count=0
tensorcube_sampler_use_count=0
tensorcube_rng_use_count=0
tensorcube_route_change_attempt_count=0
```

The shadow observer may not mutate token history, KV state, output bytes, stream chunks, finish reason, stop state, sampler state, RNG state, or runtime route.

## 9. Shadow on/off parity

The audit binary executes the same deterministic selected-token fixture with shadow disabled and enabled. Required parity:

```text
selected_token_sequence_parity=true
legacy_fragment_sequence_parity=true
output_byte_parity=true
stream_chunk_sequence_parity=true
finish_stop_parity=true
kv_owner_parity=true
decode_state_parity=true
rng_parity=true
sampler_parity=true
runtime_route_parity=true
all_production_state_parity=true
```

The audit fixture uses the exact R4-R2-R2 parent lineage, R4-R2-R1 selected token, canonical tokenizer manifest, and the same `model_core` observer used by the live hot path.

## 10. Parent admission

Input:

```text
--repo-root <PATH>
--r4-r2-r2-parent-manifest <PATH>
```

The parent must:

- be exact R4-R2-R2 PASS
- have `all_truth_checks_pass=true`
- authorize R4-R3
- forbid production apply
- prove no production handle
- prove live boundary snapshot parity
- reproduce its stable execution ID
- bind the exact R4-R2-R1 selected token and tokenizer manifest

## 11. Rust-owned artifacts

```text
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_local_manifest_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_parent_admission_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_route_coverage_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_capability_inventory_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_live_step_shadow_receipts_latest.jsonl
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_comparison_summary_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_shadow_on_off_parity_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_legacy_output_authority_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r3_non_mutation_audit_latest.json
```

Writes are atomic. The local manifest is written last. Parent, tokenizer, production output, and stream sinks are protected inputs and may not be overwritten.

## 12. Binary and required seals

Binary:

```text
ash_tcu_decode_04_r4_r3_live_selected_token_decode_surface_shadow_splice_legacy_output_authority_preservation_gate
```

Required seals:

```text
--activate-live-selected-token-shadow-splice
--activate-legacy-output-authority-preservation
--activate-shadow-on-off-parity
--activate-route-coverage-audit
--require-parent-r4-r2-r2-pass
--require-parent-r4-r3-authorization
--require-parent-no-production-handle-proof
--require-parent-live-boundary-snapshot-parity
--require-sampled-cached-route
--require-sampled-streaming-route
--require-greedy-cached-route
--require-greedy-streaming-route
--require-single-canonical-shadow-splice
--require-no-route-local-classifier
--require-legacy-exclusive-output-authority
--require-no-tensorcube-token-append
--require-no-tensorcube-kv-mutation
--require-no-tensorcube-finish-stop-mutation
--require-no-tensorcube-text-emit
--require-no-tensorcube-stream-emit
--require-no-tensorcube-sampler-use
--require-no-tensorcube-rng-use
--require-no-production-route-change
--require-selected-token-id-binding
--require-shadow-on-off-token-sequence-parity
--require-shadow-on-off-output-byte-parity
--require-shadow-on-off-stream-chunk-parity
--require-shadow-on-off-decodestate-parity
--require-shadow-on-off-kv-owner-parity
--require-shadow-on-off-rng-parity
--require-shadow-on-off-sampler-parity
--require-shadow-on-off-finish-stop-parity
--require-per-step-shadow-receipts
--require-comparison-classification
--require-mismatch-no-silent-fallback
--write-runtime-artifacts
--write-local-manifest
```

## 13. Execution identity

```text
decode04r4r3-<first 20 hex of lineage_bundle_digest>
```

The lineage seed includes parent execution and boundary evidence, route coverage, selected-token sequence, TensorCube surface sequence, legacy fragment sequence, comparison summary, shadow on/off parity, legacy authority, non-mutation audit, and runtime route digest. Timestamps, paths, pointer values, process data, and timings are excluded.

## 14. PASS, HOLD, FAIL

PASS marker:

```text
PASS_ASH_TCU_DECODE_04_R4_R3_LIVE_SELECTED_TOKEN_DECODE_SURFACE_SHADOW_SPLICE_LEGACY_OUTPUT_AUTHORITY_PRESERVATION_GATE
```

PASS requires all four routes, exact selected-token binding, one canonical observer, zero forbidden capabilities, zero TensorCube mutation attempts, classified comparisons, zero unexpected mismatch, complete shadow on/off production parity, exclusive legacy output authority, and `all_truth_checks_pass=true`.

PASS grants only:

```text
decode04_r4_r3_r1_authorized=true
decode04_r4_r4_authorized=false
production_apply_authorized=false
legacy_decoder_retirement_authorized=false
token_append_authorized=false
kv_mutation_authorized=false
finish_stop_authorized=false
text_emit_authorized=false
stream_emit_authorized=false
```

HOLD covers unavailable or stale parent, tokenizer, route, deterministic fixture, or classifiable evidence when production state remains unchanged. FAIL covers capability leakage, route bypass, token divergence, observer duplication, legacy-byte mutation, production-state change, unexpected mismatch, or silent fallback. No HOLD or FAIL path may authorize production apply.

## 15. Next gate

PASS authorizes only:

```text
ASH-TCU-DECODE-04-R4-R3-R1
Stateful Fragment Staging / SentencePiece Context Ownership Gate
```

R4-R3-R1 may introduce shadow-owned incremental context and byte-fragment staging. It still may not replace legacy output authority without its own parity and transaction gates.