# QW-50-R0D — human review decision kind/metadata depth fix

## Scope

- Target crate: `ash_core`
- Target file:
  - `crates/ash_core/src/word_context_decode_review_approval.rs`

## Fix

- Removed invalid nested enum field access patterns such as `approval.decision.decision.decision`.
- Kept `EnKoDecodeCandidateHumanReviewDecisionKind` as a kind enum only.
- Read `explicit_manual_decision`, `operator_id`, and `reason` from the full `EnKoDecodeCandidateHumanReviewDecision` struct.
- Preserved target update candidate approval semantics without enabling runtime or production apply.
- Added local clone protection for owned receipt keys and decision kind in the case result builder to avoid same-file partial move follow-up errors.

## Guard

- No runtime apply execution.
- No production apply.
- No adapter registry mutation.
- No target update side effect.
- No manual approval bypass.

## Static Pattern Check

- `decision.decision.decision` remaining: `false`
- `decision.decision.operator_id` remaining: `false`
- `decision.decision.reason` remaining: `false`
- `decision.decision.explicit_manual_decision` remaining: `false`
- `approval.decision.operator_id` present: `true`
- `approval.decision.reason` present: `true`
- `approval.decision.explicit_manual_decision` present: `true`

## Verification

```txt
cargo check -p ash_core --lib
```

## Status

PENDING_LOCAL_CARGO_CHECK
