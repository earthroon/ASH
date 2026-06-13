# 16AI-QW-38G-R6A-R12 — Root Cause Split Plan / Final Boundary vs LM Head Seal

## Status
PENDING_RUNTIME / PASS_ROOT_CAUSE_SPLIT_PLAN / FAIL_ROOT_CAUSE_SPLIT_SOURCE_INVALID

## SSOT
- source: `workspace/qw38g_r6a_r10_r2_trace_backed_aggregation_summary.json`
- required candidate: `final_norm_or_projection_boundary`
- required confidence: `strong`
- root cause confirmed: `false`

## Axis Summary
| axis | expected confidence | next probe |
|---|---|---|
| hidden direction | medium_unknown | R12A |
| lm_head row | weak_to_medium / unknown_optional_audit_missing | R12B |
| final norm amplification | medium_candidate | R12C |
| ban mask displacement | strong | R12D |
| reserved token structural | medium | R12E |

## Blocked Actions
- weight mutation
- tokenizer mutation
- ban mask mutation
- output guard bypass
- lm_head row zeroing

## Acceptance
- `root_cause_confirmed = false`
- `root_cause_candidate_count >= 5`
- plan JSON, receipt JSON, and report MD written
- mutation env flags rejected
- recommended next patch: `16AI-QW-38G-R6A-R12B_LM_HEAD_ROW_CONTRIBUTION_MARGIN_AUDIT`
