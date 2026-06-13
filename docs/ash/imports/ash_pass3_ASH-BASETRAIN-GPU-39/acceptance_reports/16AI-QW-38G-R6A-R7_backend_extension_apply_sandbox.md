# 16AI-QW-38G-R6A-R7 — Backend Extension Apply Sandbox / Debug Variant Smoke Seal

## Status
PENDING_RUNTIME

## SSOT
- Base: `ash_pass3_16AI-QW-38G-R6A-R6_apply_candidate_baked.zip`
- Patch: `16AI-QW-38G-R6A-R7`
- Runtime gate: `ASH_BACKEND_EXTENSION_SANDBOX=1`
- Sandbox mode: `debug_variant_smoke`
- Production apply: forbidden in R7
- Readback: forbidden in R7, deferred to R8

## Implemented boundaries
- Apply candidate source validation from R6 receipt/candidate JSON
- Debug shader variant sandbox smoke candidate
- Debug pipeline cache key sandbox smoke with `sandbox_id`
- Debug bind group layout smoke using selected group/slot from R6 candidate
- Debug buffer binding smoke, scalar-only, no readback
- Normal path guard
- Rollback receipt generation

## Mutation guard
| mutation | expected |
|---|---:|
| production apply | false |
| shader write | false |
| pipeline mutation | false |
| bind group mutation | false |
| generation output mutation | false |
| readback | false |
| full vector readback | false |

## Runtime outputs
- `workspace/qw38g_r6a_r7_sandbox_smoke.json`
- `workspace/qw38g_r6a_r7_sandbox_smoke_receipt.json`
- `workspace/qw38g_r6a_r7_sandbox_rollback_receipt.json`
- `workspace/infer_qw38g_r6a_r7_sandbox_smoke_live.log`

## Acceptance criteria
- `sandbox_default_off = true`
- `production_apply_rejected = true`
- `readback_rejected = true`
- `apply_candidate_loaded = true`
- `apply_candidate_valid = true`
- `debug_shader_variant_smoke_passed = true`
- `debug_pipeline_cache_smoke_passed = true`
- `debug_bind_group_layout_smoke_passed = true`
- `debug_buffer_binding_smoke_passed = true`
- `normal_path_guard_passed = true`
- `rollback_receipt_written = true`

## Next patch
`16AI-QW-38G-R6A-R8 — Debug Buffer Bind Sandbox Readback Smoke / Scalar Tap Seal`
