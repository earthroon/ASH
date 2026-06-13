# 16AI-QW-38G-R6 — Shader Debug Buffer Design / Explicit Intermediate Export Candidate Seal

## Status
PENDING_RUNTIME / PASS_SHADER_DEBUG_BUFFER / FAIL_SHADER_DEBUG_TAP_UNAVAILABLE

## SSOT
- Base: 16AI-QW-38G-R4 GPU debug tap candidate
- Current reachable boundary: `final_hidden_projection`
- Rust-side `post_mlp` / `post_block` tap: unavailable as of R4
- Patch intent: introduce a fail-closed shader debug buffer candidate surface without full activation readback

## Contract
- Default off: `ASH_SHADER_DEBUG_BUFFER=1` required.
- Scalar-only default: `ASH_SHADER_DEBUG_BUFFER_SCALAR_ONLY=1`.
- Full vector readback is rejected.
- Byte budget enforced by `ASH_SHADER_DEBUG_BUFFER_MAX_BYTES`.
- Generates receipt and summary even when the insertion point is unavailable.
- Does not mutate weights, tokenizer, safetensors, banlist, prompt defaults, or output guard.

## Runtime Artifacts
- `workspace/qw38g_r6_shader_debug_buffer_trace.jsonl`
- `workspace/qw38g_r6_shader_debug_buffer_summary.json`
- `workspace/qw38g_r6_shader_debug_buffer_receipt.json`
- `workspace/infer_qw38g_r6_shader_debug_buffer_live.log`

## Acceptance
| metric | required |
|---|---|
| shader_debug_buffer_env_gate_exists | true |
| shader_debug_buffer_default_off | true |
| scalar_only_default | true |
| full_vector_readback_rejected | true |
| byte_budget_guard_exists | true |
| debug_buffer_plan_logged | true |
| debug_buffer_receipt_written | true |
| debug_buffer_summary_written | true |
| trace_written | true/false explicitly |
| tap_reached | true/false explicitly |
| no_weight_mutation | true |
| no_tokenizer_mutation | true |
| no_safetensors_mutation | true |
| no_banlist_mutation | true |

## Decision Matrix
- `tap_reached=true`: proceed to `16AI-QW-38G-R7 — Shader Scalar Tap Source Compare`.
- `GPU_DEBUG_BUFFER_INSERTION_POINT_UNAVAILABLE`: proceed to `16AI-QW-38G-R6A — Shader Dispatch Hook Exposure`.
- `FAIL_DEBUG_BUFFER_BUDGET_EXCEEDED`: reduce max steps/layers/stages/targets.
