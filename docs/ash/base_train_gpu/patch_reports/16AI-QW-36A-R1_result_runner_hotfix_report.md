# 16AI-QW-36A-R1 — Result Runner Hotfix / infer_only Example Command Seal

## Status
PASS_STATIC / LOCAL_RUNTIME_REQUIRED

## Why this hotfix exists

The original QW-36A bake changed `crates/runtime/src/infer.rs` correctly, but the suggested runtime commands used a non-existent package/bin surface for this repository shape:

- wrong: `cargo run -p ash_runtime --bin infer -- --input-text ...`
- actual runnable surface in this tree: `cargo run --manifest-path .\crates\runtime\Cargo.toml --example infer_only -- --text ...`

Therefore `cargo check` could pass while no inference result was produced from the suggested command path.

## Added

- `scripts/run_16AI_QW_36A_prompt_template_probe.ps1`
- `scripts/inspect_16AI_QW_36A_logs.ps1`

## Correct execution

```powershell
.\scripts\run_16AI_QW_36A_prompt_template_probe.ps1 `
  -Text "1+1은?" `
  -Task "freeform" `
  -MaxNewTokens 32 `
  -Seed 42 `
  -ModelSpec ".\specs\model_spec_v5_48259.toml" `
  -Tokenizer ".\artifacts\tokenizer_manifest_v5_final.json" `
  -Checkpoint ".\tokenizer_v5\artifacts\full_model_vocab_v5_resized.safetensors"
```

If the checkpoint path is managed by local runtime profile or not present in the zip copy, pass `-NoCheckpoint` explicitly and rely on the resolved runtime profile/checkpoint configuration:

```powershell
.\scripts\run_16AI_QW_36A_prompt_template_probe.ps1 -NoCheckpoint
```

## Expected logs

- `workspace/infer_qw36a_control_1plus1.log`
- `workspace/infer_qw36a_ash_dialogue_1plus1.log`
- `workspace/infer_qw36a_hybrid_1plus1.log`

## Guard

- No safetensors mutation.
- No tokenizer mutation.
- No banlist mutation.
- No default template change.
- Only runner/report surface added.
