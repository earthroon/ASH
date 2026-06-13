# 16AI-QW-38G-R6A-R12B-R1 — Compile Hotfix / Large serde_json Macro Split

## Status
STATIC_PATCHED_COMPILE_NOT_EXECUTED_IN_CONTAINER

## Trigger
Local build failed in `crates/model_core/src/native_wgpu.rs` around the R12B summary writer:

```text
error: recursion limit reached while expanding `$crate::json_internal!`
```

## Cause
The R12B summary receipt was assembled as one large `serde_json::json!({ ... })` object. This can exceed the default Rust macro recursion limit during macro expansion.

## Fix
Replaced the single large summary `json!` macro with explicit `serde_json::Map` construction:

- `source_paths` now uses a small `serde_json::Map`.
- `summary_map` inserts each key one by one.
- final summary is sealed as `serde_json::Value::Object(summary_map)`.

## Guard
No runtime model behavior changed.

- `lm_head` mutation: none
- tokenizer mutation: none
- safetensors mutation: none
- ban mask mutation: none
- output guard bypass: none

## Compile Status
Cargo/rustc are not available in the container, so compile is not re-executed here. This patch specifically removes the failing macro expansion site reported by the user log.
