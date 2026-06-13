# QW-52C-R13-S6-R0-R1
## Runtime Workspace Check Unblock / Example Dependency Boundary Seal

## 1. SSOT
- base_patch: QW-52C-R13-S6-R0
- parent_ssot: QW-52C-R13 / PassNoApply / NoPromotion
- runtime_apply_allowed: false
- promotion_eligible: false
- weight_commit_allowed: false
- safe_profile_apply_allowed: false
- policy_promotion_allowed: false

## 2. Prior State
- model_core compile gate: passed after S6-R0 user-side cargo run evidence
- S6 runner: compiled and wrote artifacts in user log
- workspace all-targets: blocked by runtime_unz_legacy example E0432 and runtime infer.rs E0609/E0282

## 3. Repair Decisions
- `crates/runtime_unz/examples/infer_final_layers6.rs` remains present.
- `crates/runtime_unz/Cargo.toml` now gates the legacy example behind `legacy-runtime-example`.
- `crates/runtime/src/infer.rs` no longer reads `req.runtime_profile_path` from `ResolvedStandardInferRequest`; it reads `req.runtime_profile.as_ref().map(|profile| profile.profile_path.display().to_string())`.
- No `runtime_profile_path` alias field was added to `ResolvedStandardInferRequest`.

## 4. Cargo Check
- command: `cargo check --workspace --all-targets`
- bake environment status: `UNVERIFIED_IN_BAKE_ENV_NO_RUSTC`
- local verification required: true

## 5. S6 Runner Preservation
- S6 replay logic changed: false
- S6 validate logic changed: false
- real runtime trace fabricated: false
- fixture promoted to real runtime trace: false

## 6. Forbidden State Check
- runtime_apply_allowed: false
- promotion_eligible: false
- token_selection_mutation_allowed: false
- token_rank_mutation_allowed: false
- logit_mutation_allowed: false
- sampler_mutation_allowed: false

## 7. Next Patch Recommendation
- QW-52C-R13-S6-R1 — Real Runtime TopK Trace Capture / Re-run S6 Seal
