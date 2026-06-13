# QW-54D Roadmap

## Goal
Move the Cheonjiin/CJI/Cairo chain from measurement into the QW-53E-RTA inline demotion signal path.

## Patch chain
1. QW-53E-RTA-R1: real sampler hook binding
2. QW-54A: candidate piece to Cheonjiin facade
3. QW-54B: facade to CJI XYZ tensor pack
4. QW-54C: tensor pack to WGPU Cairo stress
5. QW-54D: structural risk fusion into QW-53E-RTA

## Runtime command
```bash
ASH_DECODE_PROFILE=subtitle_safe_sampled_v1 \
ASH_DECODE_SEED=42 \
ASH_QW53E_RTA_MODE=explicit_lab_apply \
ASH_QW53E_RTA_EXPLICIT_ENABLE=1 \
ASH_QW53E_RTA_R1_BINDING_TRACE=1 \
ASH_QW54A_ENABLE=1 \
ASH_QW54B_ENABLE=1 \
ASH_QW54C_ENABLE=1 \
ASH_QW54D_ENABLE=1 \
ASH_QW54D_TRACE=1 \
cargo run -p runtime --example infer_only -- \
  --prompt-file workspace/probes/qw54d_structural_risk_fusion_probe.txt \
  --max-new-tokens 96
```

## Validation
```bash
cargo test -p runtime qw54d
cargo test -p model_core qw54d
cargo test -p burn_webgpu_backend qw54d
cargo run -p model_core --bin qw54d_structural_risk_fusion_audit_validate -- .
```
