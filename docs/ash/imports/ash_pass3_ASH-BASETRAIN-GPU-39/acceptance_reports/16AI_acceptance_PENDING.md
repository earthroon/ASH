# 16AI Acceptance PENDING

## Required local checks

```powershell
$ckpt = ".\tokenizer_v5\artifacts\full_model_vocab_v5_resized.safetensors"

cargo run --manifest-path crates/model_core/Cargo.toml --bin af16ai_quality_matrix -- `
  --spec "specs/model_spec_300m_dialogue_continue_gqa8_headwise_atlas.toml" `
  --checkpoint $ckpt `
  --tokenizer-manifest ".\artifacts\tokenizer_manifest_v5_final.json" `
  --prompt-text "브라질 장수풍뎅이의 장점은 무엇인가요?" `
  --mode tokenizer `
  --wrappers "plain,dialogue-ko,instruction-ko,chatml-lite" `
  --max-new-tokens 1 `
  --vocab-limit 56253
```

## Optional generation compare smoke

```powershell
cargo run --manifest-path crates/model_core/Cargo.toml --bin af16ai_quality_matrix -- `
  --spec "specs/model_spec_300m_dialogue_continue_gqa8_headwise_atlas.toml" `
  --checkpoint $ckpt `
  --tokenizer-manifest ".\artifacts\tokenizer_manifest_v5_final.json" `
  --prompt-text "브라질 장수풍뎅이의 장점은 무엇인가요?" `
  --mode generation `
  --wrappers "dialogue-ko" `
  --sampling-presets "greedy" `
  --enable-candidate true `
  --parity-passed true `
  --max-new-tokens 1 `
  --vocab-limit 56253
```

## PASS criteria

- Tokenizer mode completes and writes JSON/MD reports.
- Wrapper token_count / token_per_char / decoded_text are logged.
- generation_connected_default=false remains preserved.
- Generation mode, if run, keeps CPU/native token ids matching or explicitly reports first mismatch.
