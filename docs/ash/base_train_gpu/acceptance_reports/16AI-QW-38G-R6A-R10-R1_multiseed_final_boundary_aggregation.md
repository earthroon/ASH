# 16AI-QW-38G-R6A-R10-R1 — Multi-Seed Final Boundary Aggregation / Repro Confidence Lift Seal

## Status
PENDING_RUNTIME

## SSOT
- Base: `ash_pass3_16AI-QW-38G-R6A-R11-R1_projection_margin_reachability_baked.zip`
- Target candidate: `final_norm_or_projection_boundary`
- Target token: `13 / <glossary:on>`
- Default seeds: `42,43,44`
- Aggregation mode: `aggregate_receipts`
- Runner-assisted mode: supported by `-Mode fanout`

## Implemented Scope
- Adds a Rust-side aggregation gate via `ASH_MULTI_SEED_FINAL_BOUNDARY_AGGREGATION=1`.
- Reads seed-specific R10 final boundary confirm receipts/summaries.
- Reads seed-specific R11 projection margin receipts/summaries.
- Writes seed evidence JSONL, aggregation summary JSON, and aggregation receipt JSON.
- Keeps production apply and full vector readback hard-rejected.
- Does not pretend a single process observed multiple seeds.

## Seed Evidence Contract
| seed | R10 receipt | R11 receipt | status |
|---:|---|---|---|
| 42 | `workspace/qw38g_r6a_r10_seed_42_final_boundary_confirm_receipt.json` | `workspace/qw38g_r6a_r11_seed_42_projection_margin_receipt.json` | pending runtime |
| 43 | `workspace/qw38g_r6a_r10_seed_43_final_boundary_confirm_receipt.json` | `workspace/qw38g_r6a_r11_seed_43_projection_margin_receipt.json` | pending runtime |
| 44 | `workspace/qw38g_r6a_r10_seed_44_final_boundary_confirm_receipt.json` | `workspace/qw38g_r6a_r11_seed_44_projection_margin_receipt.json` | pending runtime |

## Acceptance Criteria
- `PASS_MULTI_SEED_FINAL_BOUNDARY_AGGREGATION` when at least 3 valid seed evidence rows satisfy reproducibility thresholds.
- `PARTIAL_MULTI_SEED_AGGREGATION` when only a partial seed set is valid.
- `FAIL_MULTI_SEED_AGGREGATION` when no valid seed evidence exists.
- Confidence lift must be written as `confidence_after_aggregation`.
- `repro_confidence_lifted` must be explicit.
- `full_vector_readback_used` must remain false.
- all normal path guards and rollback receipts must be summarized.

## Runtime
```powershell
.\scripts\run_16AI_QW_38G_R6A_R10_R1_multiseed_aggregation.ps1 -Build -Mode fanout -Seeds "42,43,44"
```

Aggregate existing seed receipts only:
```powershell
.\scripts\run_16AI_QW_38G_R6A_R10_R1_multiseed_aggregation.ps1 -Mode aggregate -Seeds "42,43,44"
```

## Outputs
- `workspace/qw38g_r6a_r10_r1_multiseed_aggregation_trace.jsonl`
- `workspace/qw38g_r6a_r10_r1_multiseed_aggregation_summary.json`
- `workspace/qw38g_r6a_r10_r1_multiseed_aggregation_receipt.json`
