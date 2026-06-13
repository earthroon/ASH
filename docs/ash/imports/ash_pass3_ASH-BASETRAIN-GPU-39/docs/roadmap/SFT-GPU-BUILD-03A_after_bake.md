# After SFT-GPU-BUILD-03A

## Immediate verification
Run:

```powershell
cargo test -p lora_train lm_head_vocab_atlas -- --nocapture
cargo test -p lora_train lm_head_runtime_delta_verify -- --nocapture
```

## Expected next layer
If compile proceeds, the next possible blocker should be either:

1. lora_train runtime assertion failure in vocab atlas / runtime delta verify tests, or
2. another narrow fixture schema drift exposed after the syntax layer is cleared.

## Next patch candidate
`SFT-GPU-BUILD-04 — LoRA Train Test Runtime Assertion Closure / Native GPU Fixture Evidence Seal`

Use BUILD-04 only if cargo test reaches runtime assertions or fixture evidence mismatches. Do not proceed to OBS-08 until lora_train test closure is clean enough for the GPU-SFT line.
