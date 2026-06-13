# SFT-GPU-8H-G timing profiler / adapter export / no-readback discipline

## Status
PASS_STATIC / PENDING_RUNTIME

## Sealed
- timing profiler summary
- readback discipline report
- adapter_manifest.json
- adapter_model.safetensors
- GPU parallel train step seal report

## Guards
- full logits readback forbidden
- tile logits readback forbidden
- full weight readback forbidden
- artifact_family=module_lora
- target_key=lm_head
- update_applied=true
- A/B delta norm positive

## Next
SFT-GPU-8H-H runtime delta verify
