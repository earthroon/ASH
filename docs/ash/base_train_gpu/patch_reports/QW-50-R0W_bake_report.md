# QW-50-R0W Bake Report

## Patch
- `QW-50-R0W`
- `Native Decode TopK Token Trace / Repetition Attractor Source Seal`

## Base
- Previous baked base: `ASH-REBASE-00`
- Runtime lineage base: `QW-50-R0V`

## Implemented

### Runtime trace field
`StandardInferResult` now carries:

```rust
pub native_decode_r0w_trace: Option<serde_json::Value>
```

`infer_only --json` now surfaces:

- `nativeDecodeR0wTrace`
- `generatedTokenIds`
- `generatedPieces`
- `generatedPieceTrace`
- `top1Trace`
- `topKCandidatesByStep`
- `repeatAnalysis`
- `outputSplit`
- `mutationPolicy`

### Native decode trace module
Added:

```txt
crates/runtime/src/infer/qw50_r0w_trace.rs
```

The module builds a trace-only JSON packet with:

- generated tail token ids
- raw generated ids
- token piece trace
- top1 trace
- top-k candidate trace
- repeat attractor analysis
- raw/final output split
- mutation policy flags

### CPU fallback top-k trace
Added a trace-only helper in:

```txt
crates/model_core/src/generation_sampling.rs
```

Helper:

```rust
build_r0w_trace_candidate_pool_from_cpu_row()
```

This extracts top-k rows from an already materialized CPU logits row without changing logits, sampler order, token selection, guard policy, LoRA scale, or model weights.

### Output guard split
`run_standard_infer_with_decode` now tracks:

- `rawModelOutputBeforeGuard`
- `finalOutputAfterGuard`
- `outputGuardAccepted`
- `outputGuardRejectReasons`
- `outputGuardFallbackApplied`
- `fallbackResponseMatched`

## Added tools

```txt
tools/run_qw50_r0w_trace_probe.py
tools/inspect_qw50_r0w_trace.py
tools/compare_qw50_r0w_guarded_no_guard.py
tools/validate_qw50_r0w_static.py
```

## Added trace artifacts

```txt
workspace/trace/qw50_r0w_native_decode_trace_schema.json
workspace/trace/qw50_r0w_receipt.json
workspace/trace/qw50_r0w_static_validation_result.json
```

## Mutation policy

All policy mutation flags remain false:

```json
{
  "decode_policy_mutation": false,
  "guard_policy_mutation": false,
  "lora_scale_mutation": false,
  "model_weight_mutation": false,
  "token_ban_added": false,
  "webgpu_policy_mutation": false,
  "qwave_detector_enabled": false,
  "cheonjiin_detector_enabled": false
}
```

## Validation

Static validation passed:

```txt
workspace/trace/qw50_r0w_static_validation_result.json
```

Python tool syntax validation passed via `python3 -m py_compile`.

## Not run

`cargo check` and runtime inference were not run in the sandbox because `cargo`/`rustc` are not installed in this environment.

## Next

Recommended next patches:

- `QW-50-R0W-A` — Generated Prefix / DecodeState Duplication Inspector Seal
- `QW-50-R0X` — Decode Repetition Penalty Candidate / Attractor Temporary Suppression Seal
- `QW-50-R0Y` — Output Guard Reject Reason Exposure / Fallback Threshold Review Seal
- `QW-50-R0Z` — Tokenizer Piece Decode Parity / Byte Fallback Trace Seal
