# 16AI-QW-38D — Hidden State to Reserved Row Projection Audit / Final Norm Direction Seal

## Status
PENDING_RUNTIME

## SSOT
- Base patch: 16AI-QW-38A reserved-token raw logit attractor audit
- Confirmed prior state: base-only raw top1 is token_id=13 `<glossary:on>` for 20/21 observed decode steps.
- Confirmed prior row norm audit: token_id=13 lm_head/embedding rows are not outliers.

## Scope
This patch adds a trace-only hidden projection audit. It does not modify weights, tokenizer, safetensors, banlist, prompt defaults, LoRA, KV cache, RoPE, or attention masks.

## Added Runtime Evidence
- `ASH_HIDDEN_PROJECTION_TRACE=1`
- `ASH_HIDDEN_PROJECTION_TRACE_MAX_STEPS`
- `ASH_HIDDEN_PROJECTION_TOP_N`
- `ASH_HIDDEN_PROJECTION_TRACE_JSONL`
- stderr lines prefixed with `[16AI-QW-38D][hidden_proj]`
- JSONL: `workspace/qw38d_hidden_projection_trace.jsonl`
- Summary: `workspace/qw38d_hidden_projection_summary.json`

## Acceptance Criteria
- `hidden_projection_trace_jsonl_written = true`
- `hidden_projection_summary_written = true`
- `projection_to_token_13_logged = true`
- `projection_to_masked_top1_logged = true`
- `token_13_minus_masked_top1_margin_logged = true`
- `hidden_direction_collapse_suspect = true/false` explicitly reported
- `no_weight_mutation = true`
- `no_tokenizer_mutation = true`
- `no_safetensors_mutation = true`
- `no_banlist_mutation = true`

## Runtime Command
```powershell
.\scripts\run_16AI_QW_38D_hidden_projection.ps1
```

## Decision Matrix
- If token_13 projection dominates with normal hidden norm: next patch is `16AI-QW-38G — Reserved Direction Hidden Activation Source Trace / Layerwise Residual Seal`.
- If final hidden norm spikes/collapses: next patch is `16AI-QW-38H — Final Norm Stability Audit / RMSNorm Scale Seal`.
- If dot/logit mismatch appears: next patch is `16AI-QW-38E — Vocab Atlas Tile Argmax Parity / Raw TopK Merge Seal`.
