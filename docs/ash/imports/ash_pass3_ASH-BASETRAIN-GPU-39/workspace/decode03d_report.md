# 16AI-QW-38G-R6A-DECODE-03D Bake Report

## Patch
Dynamic Temperature / Min-p Controlled Enable Seal

## Baked status
STATIC_BAKE_DEFINED_NOT_RUN

## Implemented files
- `crates/model_core/src/decode03d_controlled_enable.rs`
- `crates/model_core/src/lib.rs`
- `crates/model_core/src/sampler_parity.rs`
- `workspace/decode03d_controlled_enable_schema.json`
- `workspace/decode03d_applied_steps.jsonl`
- `workspace/decode03d_summary.json`
- `workspace/decode03d_static_checks.json`
- `workspace/decode03d_probe_prompts.jsonl`

## Contract
- Default mode is `Off`.
- Behavior changes require `ASH_DECODE03D_CONTROLLED_ENABLE=true`, `ASH_DECODE03D_MODE=controlled` or `strict_controlled`, and `ASH_DECODE03D_BEHAVIOR_CHANGE_ALLOWED=true`.
- DECODE-03C shadow policy is consumed as the input SSOT.
- Temperature / top-p / min-p / top-k / guard strength are converted into a step-local applied config receipt.
- Rollback / safe stop / EOS bias candidates are recorded but never executed in DECODE-03D.
- Unsupported Min-p backends keep `applied_min_p = current_min_p` and record a warning.

## Runtime command sketch

```bash
ASH_SAMPLER_PARITY=probe \
ASH_SAMPLER05_PARITY=receipt \
ASH_DECODE03A_ENTROPY=receipt \
ASH_DECODE03B_PCI=receipt \
ASH_DECODE03C_SHADOW=receipt \
ASH_DECODE03D_CONTROLLED_ENABLE=true \
ASH_DECODE03D_MODE=controlled \
ASH_DECODE03D_BEHAVIOR_CHANGE_ALLOWED=true \
ASH_DECODE03D_REQUIRE_DECODE03C=true \
ASH_DECODE03D_RECEIPT=workspace/decode03d_applied_steps.jsonl \
ASH_DECODE03D_SUMMARY=workspace/decode03d_summary.json
```

## Not run
`cargo` is unavailable in this container, so cargo check, unit tests, shader compile, and runtime smoke are not run here.
