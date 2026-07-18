# ASH-TCU-DECODE-04-R4-R2-R2
# Live DecodeState / KV Boundary Snapshot Parity and No-Production-Handle Truth Gate

- Patch ID: `ASH-TCU-DECODE-04-R4-R2-R2_LIVE_DECODESTATE_KV_BOUNDARY_SNAPSHOT_PARITY_AND_NO_PRODUCTION_HANDLE_TRUTH_GATE`
- Parent: `ASH-TCU-DECODE-04-R4-R2-R1_PARENT_ARTIFACT_LINEAGE_SURFACE_DIGEST_TOKENIZER_IDENTITY_TRUTH_REPAIR_GATE`
- Runtime mode: `live_boundary_observe_only`
- Production authority: `false`
- PASS authorizes: `ASH-TCU-DECODE-04-R4-R3_LIVE_SELECTED_TOKEN_DECODE_SURFACE_SHADOW_SPLICE`
- Production apply: `forbidden`

## Purpose

R4-R2-R1 proves parent artifact, selected-token, surface-digest, and tokenizer identity. R4-R2-R2 proves that an observe-only TensorCube pass receives no production mutation capability and leaves the concrete `model_core::DecodeState`, embedded `KvCache`, route, sampler/RNG state, and output counters unchanged.

Both claims are mandatory and independent:

```text
no_production_handle_proven=true
live_boundary_snapshot_parity_proven=true
```

## Parent admission

Input:

```text
--repo-root <PATH>
--r4-r2-r1-parent-manifest <PATH>
```

The parent must be exact PASS, have `all_truth_checks_pass=true`, authorize R4-R2-R2, forbid R4-R3, and satisfy:

```text
execution_id = "decode04r4r2r1-" + lineage_bundle_digest[0..20]
```

## Quiescent boundary

The concrete owner contains production `DecodeState` and embedded `KvCache`. Observation is allowed only when token, KV, emit, finish, sampler, RNG, and cancel transaction counts are all zero. The orchestrator owns boundary acquisition and release. The observer receives only copied receipts and immutable snapshots.

Forbidden observer capabilities include mutable DecodeState/KV owners, output sinks, stream sinks, sampler, RNG, GPU queue/encoder, route switch, cancel transition, and production transaction handles. Every forbidden capability count must equal zero.

## Snapshot contract

DecodeState evidence includes generation epoch, token count and digest, last token, text/pending-byte digests, finish/stop state, repetition digest, mutation epoch, and append/change counters.

KV evidence includes generation and mutation epochs, layer count, logical and committed lengths, layer cursor digest, slot/allocation digests, append/truncate/reset counters, payload write serial, and pending transaction count.

Runtime evidence includes route epoch/digest, sampler and RNG digests, output/stream write counters, flush count, finish/cancel events, and production output digest.

Pre and post snapshots must carry the same boundary identity and be typed-equal. Required invariants:

```text
pending_kv_transaction_count=0
logical_sequence_len=committed_sequence_len
kv_generation_epoch=decode_state_generation_epoch
all mutation/write/event deltas=0
runtime_output_changed=false
all_state_unchanged=true
```

This gate proves KV owner metadata and write-serial parity, not full GPU payload byte readback.

## Rust-owned artifacts

The Rust binary alone writes:

```text
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r2_r2_local_manifest_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r2_r2_parent_admission_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r2_r2_boundary_guard_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r2_r2_capability_inventory_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r2_r2_pre_boundary_snapshot_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r2_r2_post_boundary_snapshot_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r2_r2_boundary_parity_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_r2_r2_non_mutation_audit_latest.json
```

Artifacts are atomic and the local manifest is written last. Generated evidence is not baked into source archives.

## Binary and required seals

Binary:

```text
ash_tcu_decode_04_r4_r2_r2_live_decodestate_kv_boundary_snapshot_parity_and_no_production_handle_truth_gate
```

Required seals:

```text
--activate-live-boundary-observe-only
--activate-decoder-state-snapshot-parity
--activate-kv-owner-snapshot-parity
--activate-no-production-handle-proof
--require-parent-r4-r2-r1-pass
--require-parent-r4-r2-r2-authorization
--require-quiescent-boundary
--require-authoritative-decodestate-snapshot
--require-authoritative-kv-owner-snapshot
--require-authoritative-runtime-route-snapshot
--require-capability-inventory
--require-no-decodestate-mut-handle
--require-no-kv-mut-handle
--require-no-output-sink-mut-handle
--require-no-stream-sink-mut-handle
--require-no-sampler-handle
--require-no-rng-handle
--require-no-gpu-queue-handle
--require-no-command-encoder-handle
--require-no-route-switch-handle
--require-no-production-transaction-handle
--require-decodestate-pre-post-parity
--require-kv-pre-post-parity
--require-runtime-route-pre-post-parity
--require-output-sink-pre-post-parity
--require-stream-sink-pre-post-parity
--require-sampler-state-pre-post-parity
--require-rng-state-pre-post-parity
--require-no-token-append
--require-no-kv-append
--require-no-kv-truncate
--require-no-kv-reset
--require-no-finish-reason-change
--require-no-stop-state-change
--require-no-text-emit
--require-no-stream-emit
--require-no-runtime-output-change
--require-no-production-route-change
--write-runtime-artifacts
--write-local-manifest
```

## Execution identity

Execution ID is `decode04r4r2r2-` plus the first 20 hex characters of a stable digest over parent execution/lineage, boundary identity, pre/post snapshot digests, capability inventory, parity audit, non-mutation audit, and route digest. Timestamps, paths, pointer values, and environment data are excluded.

## PASS, HOLD, FAIL

PASS marker:

```text
PASS_ASH_TCU_DECODE_04_R4_R2_R2_LIVE_DECODESTATE_KV_BOUNDARY_SNAPSHOT_PARITY_AND_NO_PRODUCTION_HANDLE_TRUTH_GATE
```

PASS grants only `decode04_r4_r3_authorized=true`. Token append, KV mutation, finish mutation, text/stream emission, and production apply remain false.

HOLD covers unavailable or stale evidence and non-quiescent boundaries. FAIL covers capability leakage or observed mutation. No HOLD or FAIL path may silently fall back to PASS or production apply.