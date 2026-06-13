# QW-50-R0R — Runtime Legacy Inference Surface / Attachment Smoke Compile Fix

## Scope

- `crates/runtime/tests/ash_composite_attachment_smoke.rs`
- `crates/runtime_unz/src/infer.rs`
- `crates/runtime/examples/lora_attach_smoke.rs`

## Fix

- Repaired the `vec![RuntimeAshAttachedLoraWeight { ... }]` delimiter in the runtime composite attachment smoke test.
- Removed stale `model_core::{DecodeTokenGroups, GuidedDecodeConfig}` imports from `runtime_unz` and introduced local legacy decode config/group structs for that crate surface.
- Aligned tokenizer vocab access with `manifest.trainer.vocab_size`.
- Added `loop_index: None` to `AshDecisionInput` construction.
- Replaced missing `ReferenceModel::guided_generate(...)` with existing `ReferenceModel::greedy_generate(...)` using the resolved legacy decode config fields.
- Fixed partial move in `runtime/examples/lora_attach_smoke.rs` by taking the scenario candidate before reusing the scenario.

## Guard

- No model_core public API compatibility aliases were added.
- No production apply was introduced.
- No runtime pointer or adapter registry mutation was introduced.
- Legacy guided decode state remains local to `runtime_unz`.

## Verification

```txt
cargo check --workspace --all-targets
```

## Status

PENDING_LOCAL_CARGO_CHECK
