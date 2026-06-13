# SFT-GPU-8H-B Bake Report

## Status
Baked.

## Commit
SFT-GPU-8H-B — GPU buffer bridge seal

## Files changed / added
- `crates/lora_train/src/lm_head_vocab_atlas_gpu_bridge.rs`
- `crates/lora_train/src/lm_head_vocab_atlas.rs`
- `crates/lora_train/src/lib.rs`
- `tools/validate_sft_gpu_8h_b_static.py`
- `acceptance_reports/SFT-GPU-8H-B_gpu_buffer_bridge_seal.md`

## Runtime behavior
When `projection=gpu_parallel_vocab_atlas` and `gpu_parallel.required=true`, the train path now:

1. validates the 8H-A GPU-parallel config,
2. compacts response-only active SFT rows,
3. creates GPU-resident bridge tensors for hidden/labels/loss mask/LoRA A/B/CE state/grad state/tile metadata,
4. writes `vocab_atlas_gpu_bridge_report.json` and `.md`,
5. stops explicitly with the 8H-C handoff message.

## Guarded memory policy
- Full `lm_head.weight [vocab, hidden]` GPU buffer remains forbidden.
- Full logits `[active_tokens, vocab]` buffer remains forbidden.
- Logits readback remains forbidden.
- Readback policy is sealed to `loss_and_report_only`.

## Validation
`python tools/validate_sft_gpu_8h_b_static.py`

Expected result:
`[PASS_STATIC] SFT-GPU-8H-B GPU buffer bridge seal (22 checks)`

## Next
SFT-GPU-8H-C — pass1 GPU tile group projection + partial logsumexp kernel.
