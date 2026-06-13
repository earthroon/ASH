# 16AI-QW-BUILD-02 — ModelCore Probe Bin Cluster Parse Closure / Vocab Lattice JSON Macro Seal

## Status
STATIC_VALIDATION_PASS

## Scope
- Base: 16AI-QW-BUILD-01 baked SSOT
- Purpose: close remaining model_core probe-bin compile blockers after LEGACY-01 and BUILD-01.

## Changed files
- `crates/model_core/src/bin/af16ai6b_cheonjiin_structural_probe.rs`
- `crates/model_core/src/bin/af16ai6c_surface_candidate_probe.rs`
- `crates/model_core/src/bin/af16ai6d_vocab_lattice_probe.rs`

## Fixes
1. Applied the same mean-boundary-confidence scalar split to 16AI-6C and 16AI-6D that BUILD-01 applied to 16AI-6B.
2. Added a crate-local recursion limit to the 16AI-6B/6C/6D probe bins so their large `serde_json::json!` report payloads do not fail during all-target builds.

## Guard
- No runtime inference path mutation.
- No `native_wgpu` hidden capture mutation.
- No tokenizer, safetensors, lm_head, final_norm, or ban-mask mutation.
- No legacy runtime repair or sherpa graph change.
