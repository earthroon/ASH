# 16AI-QW-38G — Reserved Direction Hidden Activation Source Trace / Layerwise Residual Seal

## Status
PENDING_RUNTIME

## SSOT
- Base patch: 16AI-QW-38D hidden projection trace
- Current confirmed state: token_id=13 (`<glossary:on>`) is a raw top1 attractor; lm_head/embedding row norms are not outliers; final hidden state repeatedly projects toward token_id=13.
- Patch scope: trace-only layerwise residual direction audit.

## Runtime Contract
- `ASH_FORCE_NO_LORA=1`
- `ASH_PROMPT_TEMPLATE=ash_dialogue_ko`
- `ASH_LAYERWISE_RESERVED_TRACE=1`
- `ASH_LAYERWISE_RESERVED_TRACE_MAX_STEPS=4` by default
- `ASH_LAYERWISE_RESERVED_TRACE_LAYERS=0,mid,last` by default
- `ASH_LAYERWISE_RESERVED_TRACE_STAGES=embed,post_attn,post_mlp,post_final_norm` by default
- `ASH_LAYERWISE_RESERVED_TARGET_ID=13`

## Expected Artifacts
- `workspace/infer_qw38g_layerwise_reserved_direction_stdout.json`
- `workspace/infer_qw38g_layerwise_reserved_direction_stderr.log`
- `workspace/qw38g_layerwise_reserved_direction_trace.jsonl`
- `workspace/qw38g_layerwise_reserved_direction_summary.json`

## Acceptance Criteria
| Check | Status |
|---|---|
| layerwise trace env gate exists | PENDING_RUNTIME |
| trace default off | PENDING_RUNTIME |
| no LoRA forced | PENDING_RUNTIME |
| target token id logged | PENDING_RUNTIME |
| stage/layer logged | PENDING_RUNTIME |
| dot/cosine/vector norm logged | PENDING_RUNTIME |
| JSONL written | PENDING_RUNTIME |
| summary written | PENDING_RUNTIME |
| no weight/tokenizer/safetensors/banlist mutation | PASS_STATIC |

## Decision Matrix
- `embed_direction_high=true` → next: `16AI-QW-38J — Prompt Token Embedding Influence Audit / Control Token Contamination Seal`
- `attention_direction_spike_detected=true` → next: RoPE/KV/mask trace line (`16AI-QW-35C/35D`)
- `mlp_direction_spike_detected=true` → next: `16AI-QW-38K — MLP Reserved Direction Activation Audit / FFN Gate Seal`
- `final_norm_direction_spike_detected=true` → next: `16AI-QW-38H — Final Norm Stability Audit / RMSNorm Scale Seal`
- `trace unavailable` → next: `16AI-QW-38G-R0 — Layer Residual Hook Exposure / Native Forward Trace Surface Seal`
