# 16AI-QW-38G-R6A-R12A-R5 — Layer21 Attention Head Attribution / Head-Position Margin Source Seal

## Status
STATIC_BAKED

## Purpose
R5 consumes the R4 adjudication that layer 21 attention is the dominant margin-jump component and opens the layer 21 attention block into head-level and source-position attribution.

## Implemented Changes
- Added the R5 env-gated head attribution path in `crates/model_core/src/native_wgpu.rs`.
- Added decode/prefill call sites in `crates/model_core/src/decode_state.rs` immediately after grouped-query attention context is produced and before `o_proj` collapse.
- Added `scripts/run_16AI_QW_38G_R6A_R12A_R5_layer21_attention_head_attribution.ps1`.
- Added static validation artifacts under `workspace/`.

## Capture Scope
- target layer: 21
- target token: 13
- masked token: 373
- head output contribution: captured as per-head `o_proj` contribution vector
- source-position contribution: top-N attention source positions per head
- scoreboards: head scoreboard, position scoreboard, head-position matrix, top head candidate, source position candidates

## Guard
- tokenizer modified: false
- safetensors modified: false
- lm_head modified: false
- final_norm modified: false
- ban_mask modified: false
- mutation performed: false

## Notes
This patch does not confirm root cause. It identifies the strongest layer 21 attention head/source-position candidate and recommends an R6 follow-up based on single-head versus distributed-head evidence.
