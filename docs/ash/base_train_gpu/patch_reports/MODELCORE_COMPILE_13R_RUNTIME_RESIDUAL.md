# MODELCORE-COMPILE-13R — Runtime Crate Compile Residual Seal

## Purpose

Repair runtime crate compile residuals blocking the `lora_train` compile seal.

The observed log shows `model_core` reaching warning-only status, while `runtime` fails with compile errors before the LoRA dump entrypoint can run.

## Changed Files

- `crates/runtime/src/infer/output_text.rs`
- `crates/runtime/src/infer.rs`
- `crates/runtime/src/infer/request_resolution.rs`
- `crates/runtime/src/engine/generation_sink.rs`
- `crates/runtime/src/engine/generation_runner.rs`
- `crates/runtime/src/lora.rs`
- `crates/model_core/src/lib.rs`

## Changes

- Fixed broken newline character literals in output text handling.
- Restored the `StandardInferRequest` DTO in the active runtime inference surface.
- Re-exported `load_runtime_lora_attachments` from `model_core` root.
- Replaced direct `EngineGenerationSink.summary` field access with a crate-internal accessor.
- Added explicit closure parameter types in request resolution.
- Restored prompt assembly and repeat-ratio helper scope in `infer.rs`.
- Added explicit `Vec<RuntimeLoraAttachment>` bindings for runtime LoRA loading.

## Non-Goals

- No runtime LoRA schema changes.
- No NativeWgpuModel changes.
- No LoRA dump runtime execution.
- No config changes.
- No tokenizer/model/jsonl path changes.
- No warning hygiene sweep.

## Validation

Run locally:

```powershell
cargo check -p runtime 2>&1 | Tee-Object ".\target\MODELCORE_COMPILE_13R_runtime_check.log"
cargo check -p lora_train 2>&1 | Tee-Object ".\target\MODELCORE_COMPILE_13R_lora_train_check.log"
```

Expected cleared patterns:

```text
character constant must be escaped
load_runtime_lora_attachments
StandardInferRequest
field `summary` of struct `EngineGenerationSink` is private
type annotations needed
build_prompt
infer_recent_repeat_ratio
infer_opening_repeat_ratio
infer_dominant_token_ratio
loaded.is_empty
```

Allowed remaining patterns:

```text
warnings only
```

## Bake Environment Status

```text
STATUS: UNVERIFIED_IN_BAKE_ENVIRONMENT
reason: cargo/rustc is not available in the bake container
```
