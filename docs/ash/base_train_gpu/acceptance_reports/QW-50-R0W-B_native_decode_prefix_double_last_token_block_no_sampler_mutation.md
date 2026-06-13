# QW-50-R0W-B
## Native Decode Prefix Double Last Token Block / No Sampler Mutation Seal

## 1. SSOT
- base_patch: QW-50-R0W-A
- related_runtime_chain: QW-52C-R13-S6
- mutation_scope: native decode prefix build only
- sampler_mutation: false
- logit_mutation: false
- token_ban_added: false
- rerank_execution: false
- retry_execution: false

## 2. Prior Evidence
- prior trace reported double_last_token_tail duplication on every inspected step.
- prior output guard rejected the raw output with repetition_loop.
- repeated attractor token: 417 / ▁보니까.

## 3. Repair Rule
```rust
if generated.last().copied() == Some(last_token) {
    // QW-50-R0W-B: do not push last_token again.
} else {
    generated_prefix.push(last_token);
}
```

## 4. Implemented Files
- crates/model_core/src/decode_state.rs
- crates/model_core/src/decode_prefix_inspector.rs

## 5. Static Verification
- unconditional `generated_prefix.push(state.last_token)` remaining: 0
- helper call count: 3
- record trace call count: 3
- `last_token_push.pushed` trace field added with serde default: true

## 6. Expected Replay Evidence
- duplication_detected_after: false
- duplication_count_after: 0
- prefix_tail_double_last_token_after: false
- prefix_len_delta_after: 0 when generated tail already equals last_token

## 7. No Mutation Proof
- sampler_mutation: false
- logit_mutation: false
- token_ban_added: false
- hard_ban_added: false
- blacklist_mutation: false
- rerank_execution: false
- retry_execution: false
- model_weight_mutation: false
- lora_scale_mutation: false

## 8. Cargo Verification
- status: PATCH_APPLIED_CARGO_UNVERIFIED_IN_BAKE_ENV
- reason: cargo/rustc unavailable in bake environment

## 9. Required Local Verification
```powershell
cargo check --workspace --all-targets
$env:RUST_BACKTRACE = "1"
$env:WGPU_BACKEND = "vulkan"
cargo run --release --manifest-path ".\crates\runtime\Cargo.toml" --example infer_only -- --runtime-profile ".\specs\runtime_profile.toml" --task subtitle_polish --text "I didn't mean to hurt you. I just wanted to protect you." --max-new-tokens 160 --seed 42 --json
```

## 10. Remaining Issues
- checkpoint/runtime model spec hash mismatch remains separate.
- checkpoint/runtime tokenizer hash mismatch remains separate.
- LoRA attach state remains unchanged.
- output quality after prefix repair requires replay evidence.
