# ASH-REBASE-00 Rebind Report

## Base
- Current base: QW-50-R0V
- Next patch: QW-50-R0W

## Purpose
Legacy Decode / EVAL / WCTX-MOCK / LoRA-RT / R12 / TCU chains were rebound as references, candidates, or quarantined records only.
No runtime inference path, model weights, decode policy, guard policy, or LoRA scale was changed.

## Mutation Policy
- Model weights: no write
- Runtime mutation: false
- Decode policy: no change
- Guard policy: no change
- LoRA scale: no change
- Runtime default apply: false

## Rebound Families
| Family | Source | Found | Hits | Status | Default Apply | Rebind Policy |
|---|---|---:|---:|---|---:|---|
| decode | QW-38G-R6A-DECODE | True | 60 | candidate_only | false | receipt_index_only |
| eval | QW-38G-R6A-EVAL | True | 8 | calibration_reference | false | fixture_reference_only |
| wctx_mock | QW-38G-R6A-WCTX-MOCK | True | 28 | audit_reference | false | archive_and_fixture_reference_only |
| lora_rt | QW-38G-R6A-LORA-RT | True | 44 | runtime_support_reference | false | attach_ledger_reference_only |
| r12 | QW-38G-R6A-R12 | True | 59 | quarantined_low_confidence | false | quarantine_candidate_only |
| tcu | TCU | True | 111 | health_ledger_reference | false | operator_review_candidate |

## Blocked Actions
- enable_legacy_decode_guard_by_default
- apply_r12_head_direction
- change_lora_scale
- change_guard_threshold
- ban_attractor_tokens
- enable_webgpu_inference_policy
- enable_qwave_cheonjiin_detector

## Next
Proceed to QW-50-R0W.
Do not enable legacy policies before generated token/top-k trace exists.
