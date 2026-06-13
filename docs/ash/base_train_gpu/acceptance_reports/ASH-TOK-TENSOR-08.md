# ASH-TOK-TENSOR-08 Acceptance Report

## Title

Grouped Safetensors Header Shape Probe / No Full Tensor Decode No Row Parity Claim Seal

## Verdict

```txt
PASS_ASH_TOK_TENSOR_08_GROUPED_SAFETENSORS_HEADER_SHAPE_PROBE_NO_FULL_TENSOR_DECODE_NO_ROW_PARITY_CLAIM
```

## Acceptance

- Header-only parser contract baked: PASS
- Safetensors source asset packaged: false
- Full-file read route allowed: false
- Payload decode allowed: false
- tensor_to_f32_vec execution: false
- Row parity probe executed: false
- Embedding/lm_head key confirmation: deferred until local header probe
- lm_head axis orientation confirmation: deferred until grouped probe
- Model forward / optimizer / weight commit: false

## Boundary

The safetensors artifact remains an external reference. This bake does not include or open the real safetensors file in the packaged ZIP. Actual local header probing is performed by running the baked binary with `ASH_TOK_TENSOR_08_SAFETENSORS_PATH` on the machine that has the artifact.
