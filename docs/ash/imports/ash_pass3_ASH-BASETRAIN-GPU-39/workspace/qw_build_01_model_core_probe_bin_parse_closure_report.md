# 16AI-QW-BUILD-01 — ModelCore Probe Bin Parse Closure / Cheonjiin Structural Probe Comparison Seal

## Status
STATIC_PASS_MODEL_CORE_PROBE_BIN_PARSE_CLOSURE

## SSOT
- source_zip: ash_pass3_16AI-QW-LEGACY-01_runtime_unz_legacy_default_build_quarantine_baked (2).zip
- source_log: pasted build log after LEGACY-01
- failed_target: model_core bin `af16ai6b_cheonjiin_structural_probe`
- failed_path: `crates/model_core/src/bin/af16ai6b_cheonjiin_structural_probe.rs`
- failure_type: Rust parser ambiguity around `as f32 < 0.35`
- mutation_scope: syntax/parse closure only

## Change
The low-boundary confidence expression was split into an explicit `mean_boundary_confidence` scalar and a simple boolean comparison:

```rust
let mean_boundary_confidence = if boundaries.is_empty() {
    1.0
} else {
    boundaries.iter().map(|b| b.confidence).sum::<f32>() / boundaries.len() as f32
};
let low_boundary_confidence = !boundaries.is_empty() && mean_boundary_confidence < 0.35;
```

## Guard
- runtime_unz_legacy quarantine remains unchanged.
- sherpa feature/vendor support remains unchanged.
- R12A-R1 hidden capture hooks remain unchanged.
- No model weights, tokenizer, safetensors, lm_head, final_norm, or ban mask were modified.

## Expected Next
Run:

```powershell
.\scriptsun_16AI_QW_BUILD_01_model_core_probe_bin_parse_closure.ps1 -Build
```

Then retry the R12A-R1 runner if default build passes.
