# 16AI-QW-38G-R6A-WCTX-09 Bake Report

## Domain SSOT

Ash is an EN-to-KO translation subtitle-machine domain component.

## What changed

Added a manual approval receipt layer after WCTX-08 controlled ContextPlan injection candidate generation.

WCTX-09 adds:

- `EnKoApprovalDecisionKind`
- `EnKoManualApprovalDecision`
- `EnKoApprovalReviewChecklist`
- `EnKoApprovalDecisionReceipt`
- `EnKoManualApplyGate`
- `EnKoContextPlanApprovalReceipt`
- `EnKoContextPlanApprovalMatrix`

## Core API

```rust
pub fn build_enko_context_plan_approval_receipt(
    candidate_receipt: &EnKoContextPlanInjectionCandidateReceipt,
    decision: EnKoManualApprovalDecision,
    checklist: EnKoApprovalReviewChecklist,
) -> EnKoContextPlanApprovalReceipt

pub fn build_pending_enko_context_plan_approval_receipt(
    candidate_receipt: &EnKoContextPlanInjectionCandidateReceipt,
) -> EnKoContextPlanApprovalReceipt

pub fn run_enko_context_plan_approval_matrix(
    candidate_receipts: &[EnKoContextPlanInjectionCandidateReceipt],
) -> EnKoContextPlanApprovalMatrix
```

## Default behavior

The default runner generates only `Pending` manual approval receipts.

- `can_proceed_to_dry_run=false`
- `can_apply_to_runtime=false`
- `gate_open_for_dry_run=false`
- `gate_open_for_runtime_apply=false`
- `runtime_default_apply=false`

## Approval rule

`ApprovedForDryRun` is valid only when:

- `operator_id` exists
- `explicit_manual_decision=true`
- approval reason is non-empty
- review checklist is complete
- source WCTX-08 receipt still has `runtime_default_apply=false`

Even then:

- `gate_open_for_dry_run=true`
- `gate_open_for_runtime_apply=false`
- `runtime_default_apply=false`

## Validation limitation

No Rust compiler was available in the bake environment. Static JSON receipts and source code were materialized; local validation should run:

```bash
cargo run -p ash_core --bin ash_word_context_context_plan_approval
```
