# 16AI-QW-38G-R6A-R12A — Final Hidden Direction Delta Probe / Target Attractor Vector Alignment Seal

## Patch Type
Probe / audit patch. No model, tokenizer, ban-mask, lm_head, final_norm, or safetensors mutation is performed.

## SSOT
- Previous closed patch: `16AI-QW-38G-R6A-R12B — LM Head Row Contribution Margin Audit / Target Row vs Neighbor Rows Seal`
- Previous status expected: `PASS_LM_HEAD_ROW_CONTRIBUTION_AUDIT`
- Previous adjudication expected: `LM_HEAD_ROW_ALIGNMENT_OR_HIDDEN_DIRECTION_INTERACTION`
- Fixed target row: `13 / <glossary:on>`
- Fixed masked row: `373 / 이`
- Root cause remains unconfirmed.

## Implementation
This patch adds a read-only hidden-vector capture path around final norm:

1. `pre_final_norm` last hidden row is captured before final norm.
2. `post_final_norm` last hidden row is captured immediately after final norm.
3. `projection_input_hidden` is captured at the vocab-atlas projection boundary.
4. Each stage is compared against target row `13`, masked row `373`, neighbor rows, and Korean sample rows.
5. Trace, summary, receipt, and report artifacts are written under `workspace/`.

## Added Runtime Gate
Default off. Must be explicitly enabled:

```powershell
$env:ASH_QW38G_R6A_R12A_FINAL_HIDDEN_DIRECTION_DELTA = "1"
```

Capture flags:

```powershell
$env:ASH_QW38G_R6A_R12A_CAPTURE_PRE_FINAL = "1"
$env:ASH_QW38G_R6A_R12A_CAPTURE_POST_FINAL = "1"
$env:ASH_QW38G_R6A_R12A_CAPTURE_PROJECTION_INPUT = "1"
```

## Added Runner

```powershell
.\scripts\run_16AI_QW_38G_R6A_R12A_final_hidden_direction_delta_probe.ps1 -Build
```

## Expected Outputs

- `workspace/qw38g_r6a_r12a_final_hidden_direction_delta_trace.jsonl`
- `workspace/qw38g_r6a_r12a_final_hidden_direction_delta_summary.json`
- `workspace/qw38g_r6a_r12a_final_hidden_direction_delta_receipt.json`
- `workspace/qw38g_r6a_r12a_final_hidden_direction_delta_report.md`
- `workspace/infer_qw38g_r6a_r12a_final_hidden_direction_delta_live.log`

## Adjudication Branches

- `FINAL_NORM_AMPLIFICATION_PRIMARY_CANDIDATE`
- `PRE_FINAL_HIDDEN_DIRECTION_PRIMARY_CANDIDATE`
- `PROJECTION_BOUNDARY_INTERACTION_CANDIDATE`
- `TARGET_MASKED_ALIGNMENT_TOO_CLOSE_INCONCLUSIVE`
- `HIDDEN_NORM_SPIKE_CANDIDATE`
- `INSUFFICIENT_FINAL_HIDDEN_DIRECTION_EVIDENCE`
- `FINAL_HIDDEN_DIRECTION_DELTA_OBSERVED_UNCONFIRMED`

## Guard

- `root_cause_confirmed = false`
- `mutation_performed = false`
- `safetensors_modified = false`
- `tokenizer_modified = false`
- `lm_head_modified = false`
- `final_norm_modified = false`
- `ban_mask_modified = false`

## Container Note
Cargo/rustc are not installed in the bake container, so compile execution is not performed here. The patch is statically baked and must be compiled on the local Ash workstation with the included runner.
