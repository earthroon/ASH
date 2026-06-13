# SFT-GPU-8H-H runtime delta verify

## Status
PASS_STATIC / PASS_RUNTIME_DELTA_VERIFY

## Sealed
- adapter_manifest.json load
- adapter_model.safetensors load
- artifact_family=module_lora
- target_key=lm_head
- runtime attachment sidecar load
- base logits vs LoRA logits delta-equivalence comparison
- delta_norm > threshold
- max_abs_delta > threshold

## Guards
- no silent fallback
- no target auto-remap
- no pass on zero delta
- no logits dump to report

## Next
SFT-GPU-8I AdamW / multi-step train loop
