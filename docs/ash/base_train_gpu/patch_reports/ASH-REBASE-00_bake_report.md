# ASH-REBASE-00 Bake Report

## Patch
- Patch ID: `ASH-REBASE-00`
- Title: `Legacy Decode / WCTX / LoRA / TCU Receipt Rebind Seal`
- Base patch: `QW-50-R0V`
- Next allowed patch: `QW-50-R0W`

## Scope
This bake adds a rebase registry and receipt layer only.

No runtime inference path, model weights, decode policy, guard policy, LoRA scale, WebGPU policy, QWave detector, or token suppression policy was changed.

## Added outputs
- `workspace/rebase/ash_rebase_00_scan_result.json`
- `workspace/rebase/ash_rebase_00_manifest.json`
- `workspace/rebase/ash_rebase_00_legacy_index.json`
- `workspace/rebase/ash_rebase_00_policy_candidates.json`
- `workspace/rebase/ash_rebase_00_missing_artifacts.json`
- `workspace/rebase/ash_rebase_00_receipt.json`
- `workspace/rebase/ash_rebase_00_validation_result.json`
- `workspace/rebase/ash_rebase_00_rebind_report.md`
- `tools/ash_rebase_00_scan.py`
- `tools/ash_rebase_00_build_index.py`
- `tools/ash_rebase_00_validate.py`

## Rebound families
| Family | Status | Default Apply |
|---|---|---:|
| Decode | candidate_only | false |
| EVAL | calibration_reference | false |
| WCTX-MOCK | audit_reference | false |
| LoRA-RT | runtime_support_reference | false |
| R12 | quarantined_low_confidence | false |
| TCU | health_ledger_reference | false |

## Safety invariants
- `runtime_mutation = false`
- `model_weight_mutation = false`
- `decode_policy_mutation = false`
- `guard_policy_mutation = false`
- `lora_scale_mutation = false`
- `runtime_default_apply = false`
- R12 remains `quarantined_low_confidence`
- Missing legacy artifacts, if any, block default apply but do not block R0W

## Validation
Executed:

```powershell
python -X utf8 .\tools\ash_rebase_00_scan.py
python -X utf8 .\tools\ash_rebase_00_build_index.py
python -X utf8 .\tools\ash_rebase_00_validate.py
```

Result: `PASS`

## Next
Proceed to `QW-50-R0W — Native Decode TopK Token Trace / Repetition Attractor Source Seal`.
