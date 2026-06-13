# 16AI-QW-38G-R6A-DECODE-03C Report

## Patch

Dynamic Sampler Shadow Policy Seal

## Input SSOT

- Input patch: `16AI-QW-38G-R6A-DECODE-03B`
- SSOT: `model_core::decode03b_pci`
- Runtime mode: observe-only / shadow-only

## Implemented files

- `crates/model_core/src/decode03c_shadow_policy.rs`
- `crates/model_core/src/lib.rs`
- `crates/model_core/src/sampler_parity.rs`
- `workspace/decode03c_shadow_policy_schema.json`
- `workspace/decode03c_shadow_steps.jsonl`
- `workspace/decode03c_summary.json`
- `workspace/decode03c_static_checks.json`
- `workspace/decode03c_probe_prompts.jsonl`
- `workspace/decode03c.patch`
- `acceptance_reports/16AI-QW-38G-R6A-DECODE-03C_acceptance.md`

## Behavior contract

`DECODE-03C` does not mutate sampler behavior. It computes the sampler values that *would* have been applied by a dynamic sampler and writes them to receipt only.

Hard contract:

- `behavior_change=false`
- `shadow_only=true`
- `ready_for_default_enable=false`

## Shadow policy buckets

- `ConfidentPath`: relaxes guard pressure and lowers `min_p`.
- `StablePath`: keeps the safe static profile shape.
- `UncertainPath`: tightens `temperature`, `min_p`, `top_p`, and guard strength.
- `UnstablePath`: marks panic guard and rollback candidate.
- `CollapsingPath`: marks panic guard, rollback, safe stop, and EOS bias candidates.

## Risk adjustments

- `numeric_risk` forces panic + safe stop + EOS bias.
- `fallback_risk` forces panic + rollback + safe stop.
- `entropy_conflict` relaxes guard if no fatal risk is present.
- `margin_collapse` tightens temperature and `min_p`.
- `selected_rank_risk` tightens temperature, `top_p`, and `min_p`.
- `overcompression_risk` relaxes `min_p` and `top_p` unless fatal risk has already taken priority.

## Not run in this environment

- `cargo check`
- `cargo test`
- WGSL compile
- Runtime smoke
- Fixed prompt replay

## Runtime invocation

```bash
ASH_SAMPLER_PARITY=probe \
ASH_SAMPLER05_PARITY=receipt \
ASH_DECODE03A_ENTROPY=receipt \
ASH_DECODE03B_PCI=receipt \
ASH_DECODE03C_SHADOW=receipt \
ASH_DECODE03C_REQUIRE_DECODE03B=true \
ASH_DECODE03C_SHADOW_ONLY=true \
ASH_DECODE03C_BEHAVIOR_CHANGE=false \
ASH_DECODE03C_RECEIPT=workspace/decode03c_shadow_steps.jsonl \
ASH_DECODE03C_SUMMARY=workspace/decode03c_summary.json
```

## Next patch

`16AI-QW-38G-R6A-DECODE-03D — Dynamic Temperature / Min-p Controlled Enable Seal`

Only proceed if `decode03c_summary.json` has `ready_for_decode03d_controlled_enable=true` after real runtime receipt generation.
