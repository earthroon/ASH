# 16AI-QW-38A — Reserved Token Raw Logit Attractor Audit / Base LM Head Distribution Seal

## Status

PENDING_RUNTIME

## SSOT

- Previous evidence: `16AI-QW-35E` base-only replay confirmed `force_no_lora=true`, `selected_lora_ids=[]`, `loaded_loras=0`, `attached_loras=0`.
- Previous evidence: `token_id=13 (<glossary:on>)` appeared as raw `native-vocab-atlas tile_argmax` 20 out of 21 observed steps, about 95.2%.
- Previous evidence: final generated surface used normal Korean tokens such as `▁있다던데`, `▁풋살화`, and `▁양보하고`, so banning normal displaced tokens is not the target.

## Patch Scope

This patch adds trace-only instrumentation. It does not mutate:

- checkpoint / safetensors
- tokenizer manifest
- banlist
- LoRA artifacts
- prompt template defaults
- generation policy defaults

## Runtime Flags

```powershell
$env:ASH_PROMPT_TEMPLATE="ash_dialogue_ko"
$env:ASH_FORCE_NO_LORA="1"
$env:ASH_RAW_TOPK_TRACE="1"
$env:ASH_RAW_TOPK_TRACE_TOP_N="16"
$env:ASH_RAW_TOPK_TRACE_MAX_STEPS="32"
$env:ASH_LM_HEAD_ROW_AUDIT="1"
```

## Expected Runtime Artifacts

| artifact | purpose |
|---|---|
| `workspace/infer_qw38a_reserved_attractor_base_only_stderr.log` | runtime stderr and `[16AI-QW-38A][raw_topk]` lines |
| `workspace/infer_qw38a_reserved_attractor_base_only_stdout.json` | infer output JSON |
| `workspace/qw38a_raw_topk_trace.jsonl` | per-step raw top-k trace |
| `workspace/qw38a_reserved_attractor_summary.json` | summarized reserved-token attractor metrics |
| `workspace/qw38a_lm_head_row_norm_report.json` | target row norm audit for lm_head/embed rows |

## Acceptance Criteria

- `raw_top1_token_id_logged = true`
- `raw_top1_piece_logged = true`
- `raw_top1_logit_logged = true`
- `raw_top1_is_banned_logged = true`
- `raw_top1_ban_reason_logged = true`
- `raw_topk_token_ids_logged = true`
- `raw_topk_pieces_logged = true`
- `raw_topk_banned_flags_logged = true`
- `masked_top1_logged = true`
- `token_13_raw_top1_count_logged = true`
- `reserved_raw_top1_rate_logged = true`
- `ban_mask_displacement_rate_logged = true`
- `lm_head_row_norm_report_written = true/false explicitly`
- `no_weight_mutation = true`
- `no_tokenizer_mutation = true`
- `no_safetensors_mutation = true`
- `no_banlist_mutation = true`

## Runtime Command

```powershell
.\scripts\run_16AI_QW_38A_reserved_attractor.ps1
```

## Decision Matrix

| case | condition | next patch |
|---|---|---|
| token 13 row norm outlier | token 13 lm_head row norm is abnormally high | `16AI-QW-38B` row clamp candidate / review only |
| reserved group high | reserved/control tokens dominate raw top-k | `16AI-QW-38C` reserved group distribution audit |
| row norm normal but 13 top1 | hidden state projects into token 13 direction | `16AI-QW-38D` hidden-to-reserved projection audit |
| raw top-k disagrees with tile_argmax | atlas merge/logging issue | `16AI-QW-38E` vocab atlas tile argmax parity |
| masked top1 mismatch | selection path differs after ban mask | `16AI-QW-38F` ban-masked selection source audit |
