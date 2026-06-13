# ASH-BASETRAIN-GPU-11-SSOT-R1 Bake Report

## 확정

- Base source: `ash_pass3_ASH-BASETRAIN-GPU-11_minimal_multi_buffer_forward_dispatch_smoke_lut_baked.zip`
- R1 source: `ash_pass3_ASH-BASETRAIN-GPU-11-R1_storage_buffer_limit_uniform_token_fix_baked.zip`
- Runtime PASS receipt: `ASH_BASETRAIN_GPU_11_SSOT_R1_OPERATOR_PASS_RECEIPT.json`
- Verdict: `PASS_ASH_BASETRAIN_GPU_11_MINIMAL_MULTI_BUFFER_FORWARD_DISPATCH_SMOKE_EMBED_QPROJ_LMHEAD_READINESS_TO_FIXED_TOKEN_DISPATCH_STATE_NO_BACKWARD_NO_OPTIMIZER`
- Token input binding: `uniform`
- Storage buffer count after R1: `4`
- Logits scope: `[1, 1, 1024]` chunk-window smoke

## 닫은 경로

- semantic full forward: false
- loss: false
- backward: false
- optimizer: false
- safetensors mutation: false

## 다음 패치

`ASH-BASETRAIN-GPU-12` — Multi-Buffer Forward Output Audit / Fixed Token Chunk-Window Logits Smoke Readback And Boundary Verification No Backward No Optimizer Seal
