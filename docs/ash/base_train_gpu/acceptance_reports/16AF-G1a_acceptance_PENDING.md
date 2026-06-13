# 16AF-G1a Acceptance PENDING

## Required local command

```powershell
$ckpt = ".\tokenizer_v5\artifacts\full_model_vocab_v5_resized.safetensors"

cargo run --manifest-path crates/model_core/Cargo.toml --bin af16g_generation_candidate_gate -- `
  --spec "specs/model_spec_300m_dialogue_continue_gqa8_headwise_atlas.toml" `
  --checkpoint $ckpt `
  --enable-candidate false `
  --parity-passed true `
  --max-new-tokens 0 `
  --vocab-limit 256
```

## Expected seal

```txt
[16AF-G][summary] candidate_wire_present=true generation_connected_default=false candidate_runtime_enabled=false fallback_cpu_reference=true pass=true
[16AF-G][seal] PASS native FFN generation candidate gate wired default_false
```
