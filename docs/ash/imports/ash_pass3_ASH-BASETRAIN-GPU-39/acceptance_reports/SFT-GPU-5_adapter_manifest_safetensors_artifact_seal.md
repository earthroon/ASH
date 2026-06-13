# SFT-GPU-5 Acceptance

## Status

PENDING until run on a Rust/WGPU host.

## Scope

adapter manifest / safetensors artifact seal

## Checked Files

- `crates/lora_train/src/gpu_lm_head_lora_smoke.rs`
- `crates/lora_train/src/sft_lm_head_artifact.rs`
- `crates/lora_train/src/training.rs`
- `crates/lora_train/src/lib.rs`
- `docs/A_SFT_GPU_DIRECT_LINE.md`

## Required Contract

- `artifact_family = module_lora`
- `target_key = lm_head`
- `target_modules = ["lm_head"]`
- tensor key `lm_head.lora_A`
- tensor key `lm_head.lora_B`
- A shape = `[rank, hidden_size]`
- B shape = `[vocab_size, rank]`
- dtype = `F32`
- adapter format = `safetensors`
- manifest path exists
- adapter path exists
- saved artifact reloads successfully

## Gates

- [ ] output directory `artifacts/lm_head_lora/` is created
- [ ] `adapter_manifest.json` exists
- [ ] `adapter_model.safetensors` exists
- [ ] `artifact_report.json` exists
- [ ] manifest `schema_version = 1`
- [ ] manifest `artifact_family = module_lora`
- [ ] manifest `target_key = lm_head`
- [ ] manifest `adapter_path` points to an existing file
- [ ] safetensors contains `lm_head.lora_A`
- [ ] safetensors contains `lm_head.lora_B`
- [ ] `lm_head.lora_A` shape matches `[rank, hidden_size]`
- [ ] `lm_head.lora_B` shape matches `[vocab_size, rank]`
- [ ] `lm_head.lora_B` norm > 0
- [ ] reload validation passes
- [ ] no `shared_hidden_token_adapter` tensor keys exist
- [ ] no `layers.0.lm_head` tensor keys exist

## Non-goals

- runtime load / logits delta is not verified here
- generation quality is not evaluated here
- adapter merge is not implemented here
