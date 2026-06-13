# MODELCORE-COMPILE-10 — Result Alias / Type Inference Seal

## Purpose

Seal ambiguous result aliases and type inference failures without changing runtime behavior.

This commit keeps the generation and GPU sampling logic intact, and only adds explicit type boundaries where Rust inference was previously forced to guess.

## Changed Files

- `crates/model_core/src/generation_telemetry.rs`
- `crates/model_core/src/generation_sampling.rs`
- `patches/MODELCORE_COMPILE_10.diff`
- `patch_reports/MODELCORE_COMPILE_10_TYPE_INFERENCE.md`

## Changes

### generation_telemetry.rs

- Added explicit aggregation map type for `GpuRawBridgeTelemetrySummary::by_label_group`:
  - `BTreeMap<String, GpuRawBridgeLabelSummary>`
- Added explicit bucket type for raw bridge label aggregation:
  - `&mut GpuRawBridgeLabelSummary`
- Added explicit aggregation map type for `TensorCubeRuntimeSpliceTelemetrySummary::by_label_group`:
  - `BTreeMap<String, TensorCubeRuntimeSpliceLabelSummary>`
- Added explicit bucket type for tensorcube runtime splice aggregation:
  - `&mut TensorCubeRuntimeSpliceLabelSummary`

### generation_sampling.rs

- Added explicit `GpuSamplingRuntime` references at GPU sampling dispatch sites.
- Added explicit `GpuPenaltyPass` references at GPU penalty dispatch sites.
- Added explicit `GpuRawBridgeStepTelemetry` bindings where raw bridge telemetry is cloned into `NextTokenChoice`.
- Added explicit closure parameter type for GPU penalty CPU-logit adjustment.

## Non-Goals

- No runtime LoRA schema repair.
- No ReferenceModel execution path repair.
- No ownership / borrow repair.
- No sampling policy change.
- No GPU sampling fallback order change.
- No no-op or fallback insertion.
- No config changes.

## Prohibited Shortcuts Avoided

- Did not use `as _`.
- Did not use `unwrap` or `expect`.
- Did not use `Default::default()` to satisfy inference.
- Did not change GPU sampling dispatch order.
- Did not change telemetry counter semantics.

## Validation

Run:

```powershell
cargo check -p model_core 2>&1 | Tee-Object ".\target\MODELCORE_COMPILE_10_check.log"
```

Targeted check:

```powershell
Select-String -Path ".\target\MODELCORE_COMPILE_10_check.log" -Pattern "E0107|E0282|Result<|or_default|dispatch_top_n_raw_lease|dispatch_sample_raw_lease|dispatch_sample_cpu_logits|dispatch_argmax_raw_lease|dispatch_adjust_cpu_logits|raw_bridge.clone"
```

Expected cleared patterns:

```text
E0107
E0282
type annotations needed for `&mut _`
cannot infer type
```

Allowed remaining patterns:

```text
traces borrow E0505
severity moved E0382
```
