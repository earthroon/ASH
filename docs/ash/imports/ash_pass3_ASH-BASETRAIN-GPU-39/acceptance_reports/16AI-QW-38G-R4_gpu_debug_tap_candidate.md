# 16AI-QW-38G-R4 — GPU Debug Tap Candidate / Bounded Intermediate Activation Readback Seal

## Status
PENDING_RUNTIME / PASS_STATIC

## SSOT
- Base: 16AI-QW-38G-R3 stage map baked state
- Observed boundary from R3: `actual_traceable_boundary = final_hidden_projection`
- Rust-side layerwise residual boundary: unavailable from current hook
- Goal: bounded debug tap candidate with fail-closed receipt

## Implemented Surface
- `ASH_GPU_DEBUG_TAP=1`
- `ASH_GPU_DEBUG_TAP_MAX_STEPS=1`
- `ASH_GPU_DEBUG_TAP_LAYERS=mid,last`
- `ASH_GPU_DEBUG_TAP_STAGES=post_mlp,post_block`
- `ASH_GPU_DEBUG_TAP_TARGET_IDS=13`
- `ASH_GPU_DEBUG_TAP_SCALAR_ONLY=1`
- `ASH_GPU_DEBUG_TAP_OUT=workspace/qw38g_r4_gpu_debug_tap_trace.jsonl`
- `ASH_GPU_DEBUG_TAP_SUMMARY=workspace/qw38g_r4_gpu_debug_tap_summary.json`
- `ASH_GPU_DEBUG_TAP_RECEIPT=workspace/qw38g_r4_gpu_debug_tap_receipt.json`

## Runtime Expected Outcomes

| Case | Meaning | Next |
|---|---|---|
| `FAIL_TAP_UNAVAILABLE` | requested `post_mlp/post_block` is not reachable from current Rust boundary | R6 shader debug buffer design |
| `PASS_GPU_DEBUG_TAP_FINAL_ONLY` | only final hidden/projection boundary is reachable if `post_final_norm` is requested | 38H final norm stability audit |
| `FAIL_FULL_VECTOR_REJECTED` | full vector request rejected by guard | keep scalar-only |

## Acceptance Criteria
- gpu_debug_tap_env_gate_exists = true
- gpu_debug_tap_default_off = true
- projection_scalar_only_default = true
- full_vector_readback_rejected = true
- max_steps_default <= 1
- tap_plan_logged = true
- tap_attempt/tap_unavailable_logged = true
- debug_tap_summary_written = true
- debug_tap_receipt_written = true
- no_weight_mutation = true
- no_tokenizer_mutation = true
- no_safetensors_mutation = true
- no_banlist_mutation = true

## Notes
R4 deliberately does not fake success for `post_mlp/post_block`. If current Rust-side boundary cannot access intermediate activations, the patch writes a fail-closed receipt rather than silently passing.
