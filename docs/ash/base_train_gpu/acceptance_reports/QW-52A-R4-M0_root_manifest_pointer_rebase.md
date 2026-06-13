# QW-52A-R4-M0 — Root Manifest / Latest SSOT Pointer Rebase Seal

## Status

`PASS_STATIC_MANIFEST_REBASE`

## Base

`QW-52A-R4 — Cheonjiin Adapter Gated Fusion Candidate / No Default Apply Seal`

## Purpose

This patch rebases the stale root manifest pointer to the latest baked SSOT:

- latest baked patch: `QW-52A-R4`
- next recommended patch: `QW-52B — Decode Detector Registry / Word Salad Risk Seal`
- runtime default apply: `false`
- gate default: `0.0`
- operator approval required: `true`

This is a metadata-only seal. It does not add detectors and does not change runtime behavior.

## Confirmed Manifest Rebase

- `meta.json.patch_id = QW-52A-R4-M0`
- `meta.json.base_patch = QW-52A-R4`
- `meta.json.latest_baked_patch = QW-52A-R4`
- `meta.json.current_next_recommended_patch = QW-52B`
- `meta.json.runtime_default_apply = false`

## R4 Contract Preserved

- formula: `h_candidate = h + alpha * gate * latent_delta`
- `alpha_candidate = 0.01`
- `gate_default = 0.0`
- `gate_runtime_value = 0.0`
- `runtime_default_apply = false`
- `controlled_enable_required = true`
- `operator_approval_required = true`

## Mutation Policy

No runtime behavior changed.

- hidden state mutation: `false`
- residual stream mutation: `false`
- lm_head input mutation: `false`
- logit mutation: `false`
- sampler mutation: `false`
- token selection mutation: `false`
- LoRA scale mutation: `false`
- WebGPU shader added: `false`

## Added Files

- `crates/model_core/src/bin/qw52a_r4_m0_manifest_rebase_validate.rs`
- `workspace/trace/qw52a_r4_m0_ssot_pointer_rebase_receipt.json`
- `workspace/trace/qw52a_r4_m0_manifest_pointer_diff.json`
- `acceptance_reports/QW-52A-R4-M0_root_manifest_pointer_rebase.md`

## Validation State

- Static manifest rebase receipt generated.
- Cargo check was not executed in this bake environment because `cargo` is unavailable.
- Runtime probe was not executed in this bake environment.

## Next

`QW-52B — Decode Detector Registry / Word Salad Risk Seal`

QW-52B must remain trace-only at entry:

- no logit mutation
- no sampler mutation
- no token rank mutation
- no token ban
- no hidden state fusion
- no gate enable
- no runtime default apply
