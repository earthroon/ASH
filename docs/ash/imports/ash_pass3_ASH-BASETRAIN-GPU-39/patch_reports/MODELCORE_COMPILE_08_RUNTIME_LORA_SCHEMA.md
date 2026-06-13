# MODELCORE-COMPILE-08 — Runtime LoRA Schema Drift Reconciliation

## Purpose

Reconcile `runtime_lora.rs` schema drift without silent defaults.

This commit repairs missing reason summary methods, stale native step-start reads, grad handle binding request fields, adapter fingerprint preview defaults, and explicit metric bindings.

## Changed Files

- `crates/model_core/src/runtime_lora.rs`
- `patch_reports/MODELCORE_COMPILE_08_RUNTIME_LORA_SCHEMA.md`
- `patches/MODELCORE_COMPILE_08.diff`

## Changes

- Added a targeted `RuntimeLoraReasonSummary` trait and macro-backed implementations for runtime LoRA reason enums that already expose `as_str()`.
- Added grad handle binding telemetry fields to `ModuleLocalNativeSourcePlusDeltaCommitBridgeRequest`.
- Updated request defaults and `from_dry_run_and_guard()` with explicit `not_bound` status and `grad_pair_not_attached_yet` reason.
- Filled `ModuleLocalNativeAdapterSyncReadbackPreview` fingerprint defaults explicitly.
- Added `ModuleLocalNativeTrainStepOutput::native_step_started()` as a query bridge instead of resurrecting the stale stored field.
- Replaced stale `output.native_step_started` reads with `output.native_step_started()`.
- Derived `adapter_commit_delta_payload` from the candidate delta readback payload instead of using an unbound shorthand.
- Filled missing `ModuleLocalNativeDedicatedNstepStepResult` optional phase-result fields explicitly in the step projection constructor.
- Bound `checkpoint_parity_latency_ms` explicitly from the measured checkpoint latency variable.
- Fixed `memory_high_water_delta_ratio` projection to use the computed `memory_delta_ratio`.

## Non-Goals

- No generation telemetry Result alias/type inference repair.
- No NativeWgpuModel execution_path repair.
- No reference checkpoint forward full repair.
- No ownership/borrow repair for traces/severity.
- No config changes.
- No runtime fallback/no-op insertion.

## Prohibited Shortcuts Avoided

- Did not add a stale stored `native_step_started` field to `ModuleLocalNativeTrainStepOutput`.
- Did not remove grad handle telemetry writes.
- Did not use silent zero for checkpoint parity latency.
- Did not use silent zero for memory high-water delta ratio.
- Did not expose unrelated runtime_lora internals.

## Validation

Run locally:

```powershell
cargo check -p model_core 2>&1 | Tee-Object ".\target\MODELCORE_COMPILE_08_check.log"
```

Expected cleared patterns:

```text
summary_string
native_step_started
grad_a_handle_id
grad_b_handle_id
grad_a_byte_len
grad_b_byte_len
grad_handle_binding_status
grad_handle_binding_reason
adapter_a_fingerprint_before
adapter_a_fingerprint_after
adapter_b_fingerprint_before
adapter_b_fingerprint_after
adapter_commit_delta_payload
checkpoint_parity_latency_ms
memory_high_water_delta_ratio
ModuleLocalNativeDedicatedNstepStepResult
```

Allowed remaining patterns:

```text
generation_telemetry.rs Result<T> E0107
generation_telemetry.rs HashMap E0282
ReferenceModel forward_hidden_ids_full
ReferenceModel forward_logits_ids_full
NativeWgpuModel execution_path
traces borrow E0505
severity moved E0382
```
