# ASH-BASETRAIN-GPU-21-R1 Bake Report

## Patch

ASH-BASETRAIN-GPU-21-R1 — Failure Route LUT Rebind / Composite Mask 52 To Raw Payload Export Route No Loss No Optimizer Seal

## Source SSOT

- Source patch: ASH-BASETRAIN-GPU-21
- Source verdict: FAIL_ASH_BASETRAIN_GPU_21_COMPOSITE_BLOCKER_MASK_52
- Source violation mask: 52
- Source failure root: raw logits payload missing; local window logits source invalid

## Scope

This patch does not convert the original ASH-BASETRAIN-GPU-21 loss smoke failure into a pass. It only rebinds the failure route for mask 52 from the incorrect PASS successor route to the raw payload export route.

## Corrected Route

- Old route: ASH-BASETRAIN-GPU-22_LOSS_SCALAR_AUDIT_NO_BACKWARD
- Corrected route: ASH-BASETRAIN-GPU-21-0_RAW_LOGITS_PAYLOAD_EXPORT
- Route LUT index: 3
- Primary blocker bit: 2
- Active bits: [2, 4, 5]

## Closed Boundaries

- raw_payload_export_executed = false
- loss_computed = false
- loss_scalar_created = false
- backward_executed = false
- optimizer_step_executed = false
- safetensors_mutation_present = false

## Expected Verdict

PASS_ASH_BASETRAIN_GPU_21_R1_FAILURE_ROUTE_LUT_REBIND_COMPOSITE_MASK_52_TO_RAW_PAYLOAD_EXPORT_ROUTE_NO_LOSS_NO_OPTIMIZER
