# ASH-TCU-DECODE-01 SPEC

## GENERATION_SHADOW_SESSION_LIFECYCLE_SEAL

```text
patch_id=ASH-TCU-DECODE-01_GENERATION_SHADOW_SESSION_LIFECYCLE_SEAL
parent_package=ASH_R5R4R1R2 (2)(3).zip
parent_sha256=fbb5eba433f936558ec9d3ea557ff186d8e0eb91959f52c7fcbe3979c4fe77de
source_authority=supplied_parent_zip_rust_surfaces
local_cargo_workspace_assumed_present=true
mutation_class=runtime_lifecycle_repair_shadow_only
output_authority=burn
production_authority=false
runtime_output_changed=false
```

## 1. Purpose

The parent already creates a generation-scoped TensorCube shadow session and passes it across prefill and cached decode projection observation. The defect is terminal ownership: live generation paths can drop a started session without calling backend `finalize()`, and the one-shot vocab-atlas forward also drops its local session.

DECODE-01 introduces one non-clone model-core lifecycle owner that owns start state, active backend session, exactly-once finalization, and the terminal receipt. It closes every reachable normal, early, cancellation, sink-error, prefill-error, decode-error, and one-shot termination path without changing Burn logits or generation behavior.

## 2. Required authority boundary

```text
burn_output_authority=true
production_authority=false
raw_buffer_lease_count=0
tensorcube_dispatch_count=0
tensorcube_output_count=0
parity_comparison_count=0
downstream_output_commit_count=0
route_mutation_count=0
runtime_output_changed=false
```

This patch must not enable TensorCube dispatch, real-shape routes, parity, logits promotion, BaseTrain mutation, tokenizer mutation, sampler mutation, KV semantic mutation, model-weight mutation, or route-epoch mutation.

## 3. Lifecycle SSOT

Replace the loose `DecodeState` ownership:

```rust
Option<ModelTensorCubeGenerationShadowSession>
```

with one non-clone owner:

```rust
pub struct ModelTensorCubeGenerationShadowLifecycle {
    session: Option<ModelTensorCubeGenerationShadowSession>,
    start_status: ModelTensorCubeShadowStartStatus,
    start_error: Option<String>,
    final_receipt: Option<ModelTensorCubeGenerationShadowLifecycleReceipt>,
    finalize_attempt_count: u8,
    backend_finalize_call_count: u8,
}
```

Required rules:

- `session` remains private.
- Projection callsites receive only `Option<&mut Session>` through `session_mut()`.
- Only `finalize_once()` may take and consume the backend session.
- The owner must not implement `Clone`.
- `DecodeState` must not derive `Clone` while owning the lifecycle.
- Repeated `finalize_once()` returns the stored receipt and never calls backend finalize twice.
- `Drop` may emit a diagnostic only. It must not fabricate PASS or perform authoritative finalization.

## 4. State and receipt contracts

Start status:

```rust
Started | Blocked | NotRequested
```

Termination reason:

```rust
OneShotForwardComplete
Eos
MaxNewTokens
StopSequence
RepetitionGuard
Cancelled
PrefillError
DecodeError
SamplingError
SinkError
GenerationError
AlreadyFinishedCall
Unknown
```

Finalize status:

```rust
Finalized | FinalizeFailed | NotStarted | AlreadyFinalized
```

Receipt schema:

```text
ash_model_tensorcube_generation_shadow_lifecycle_v1
```

The receipt binds start status, exact termination reason, finalize status, backend pre-finalize state, backend observation receipt, start/finalize errors, attempt count, backend finalize count, Burn authority, and runtime-output-change truth.

A blocked observer start must remain diagnostic and must not fail Burn generation. A backend finalize failure must be recorded but must not replace successful Burn output or erase the original generation error.

## 5. Required termination coverage

Every generation entry point that starts or receives a lifecycle must terminalize it exactly once before ownership leaves the public operation.

Required normal and early reasons:

- first-token EOS;
- cached EOS;
- max-new-token exhaustion;
- stop-sequence hit;
- repetition guard;
- already-finished decode call;
- one-shot vocab-atlas forward completion.

Required error reasons:

- prefill error;
- decode error;
- sampling or generation error;
- streaming cancellation;
- streaming sink failure.

Cancellation and sink errors must finalize first and then propagate the original error unchanged. Repetition guard must retain `RepetitionGuard` as lifecycle reason even when the output token is rewritten to EOS by existing behavior.

## 6. DecodeState and telemetry wiring

`DecodeState` owns `ModelTensorCubeGenerationShadowLifecycle` and exposes only narrow helpers for mutable projection observation and terminalization.

Prefill constructs the lifecycle before native prefill, finalizes a local owner on prefill failure, and transfers ownership into `DecodeState` only on success.

Decode projection continues to use the same lifecycle session through the existing Burn-owned vocab-atlas projection.

Telemetry-bearing generation APIs must publish the terminal lifecycle receipt. APIs that do not return telemetry still must finalize the lifecycle before return.

## 7. One-shot forward repair

`NativeWgpuModel::forward_logits_for_generation()` must:

1. begin one local lifecycle;
2. pass its session to the existing observed Burn vocab-atlas projection;
3. finalize with `OneShotForwardComplete` before returning logits;
4. keep Burn logits authoritative even when start or finalize is diagnostic-failed.

## 8. Required source changes

Modify:

```text
crates/model_core/src/tensorcube_generation_shadow_session.rs
crates/model_core/src/decode_state.rs
crates/model_core/src/generation_sampling.rs
crates/model_core/src/generation_telemetry.rs
crates/model_core/src/native_wgpu.rs
crates/model_core/src/lib.rs
crates/orchestrator_local/src/lib.rs
crates/orchestrator_local/Cargo.toml
```

Add:

```text
crates/model_core/tests/ash_tcu_decode_01_generation_shadow_session_lifecycle.rs
crates/orchestrator_local/src/ash_tcu_decode_01_generation_shadow_session_lifecycle_seal_report.rs
crates/orchestrator_local/src/bin/ash_tcu_decode_01_generation_shadow_session_lifecycle_seal.rs
```

No backend execution module or WGSL file is added.

## 9. Rust-owned artifact generation

The bake ZIP contains source only. It must contain no pre-generated DECODE-01 receipt, report, final seal, verdict, local manifest, immutable bundle, latest mirror, or SHA sidecar.

The sole runtime evidence owner is:

```text
ash_tcu_decode_01_generation_shadow_session_lifecycle_seal
```

Immutable root:

```text
artifacts/tensorcube/decode_01/<execution_id>/
```

Latest mirror root:

```text
workspace/runtime/tensorcube/
```

The Rust executable generates at least:

```text
lifecycle_contract
static_coverage
protected_behavior_guard
source_digest_manifest
report
final_seal
verdict
local_manifest
```

`local_manifest` is written last from the actual artifact bytes produced by the same Rust process and binds immutable path, latest path, and SHA-256 digest for every artifact.

Required truth:

```text
runtime_generated=true
rust_artifact_owner=ash_tcu_decode_01_generation_shadow_session_lifecycle_seal
spec_baked_into_zip=false
docs_baked_into_zip=false
packaged_runtime_artifact_count=0
sha256_sidecars_baked=false
```

Python, shell, bake tooling, and copied console text must not synthesize PASS evidence.

## 10. Static fail-closed gate

The Rust audit must inspect the actual source tree and fail when any of the following is nonzero:

```text
unclassified_lifecycle_start_callsite_count
unclassified_termination_return_count
bare_error_propagation_after_session_start_count
loose_decode_state_shadow_session_option_count
backend_finalize_callsite_outside_lifecycle_owner_count
unguarded_stream_sink_call_count
```

The audit covers lifecycle starts, prefill constructors, decode steps, cached loops, streaming loops, repetition early returns, cancellation checks, sink writes, and one-shot vocab-atlas forward.

## 11. Required tests

- started lifecycle finalizes backend exactly once;
- repeated finalization returns the stored receipt;
- blocked and not-requested starts produce terminal non-started receipts;
- finalize failure preserves exact backend error and zero output claim;
- successful receipt preserves all execution counters at zero;
- first-token EOS, decode EOS, max tokens, stop sequence, repetition guard, cancellation, sink error, prefill error, and decode error are terminalized;
- one-shot forward contains explicit finalization;
- deterministic protected behavior retains token IDs, finish reason, stop hit, Burn authority, and runtime output.

## 12. PASS

```text
PASS_ASH_TCU_DECODE_01_GENERATION_SHADOW_SESSION_LIFECYCLE_SEAL
selected_outcome=generation_shadow_session_lifecycle_sealed
session_owner=model_core_non_clone_lifecycle_ssot
normal_termination_coverage=complete
error_termination_coverage=complete
cancel_termination_coverage=complete
one_shot_forward_coverage=complete
backend_finalize_exactly_once=true
burn_output_authority=true
production_authority=false
runtime_output_changed=false
tensorcube_dispatch_count=0
```

PASS additionally requires the Rust executable to generate immutable artifacts and latest mirrors at runtime, write the local manifest last, and prove the bake ZIP contains zero generated evidence.

## 13. HOLD and FAIL

HOLD when a lifecycle start or termination path cannot yet be proven without changing output safety, telemetry publication remains incomplete, or unrelated local changes block compilation.

FAIL on double backend finalize, lifecycle leak, fabricated finalized receipt, original error loss, session cloning into multiple owners, any TensorCube execution/output mutation, route mutation, token/output behavior change, or authoritative finalization from `Drop`.

## 14. Next state

Only the following next state is authorized after DECODE-01 PASS:

```text
ASH-TCU-DECODE-02_VOCAB_ATLAS_REAL_SHAPE_ROUTE_IDENTITY
```

DECODE-01 does not authorize same-device lease, TensorCube dispatch, parity comparison, or logits promotion.