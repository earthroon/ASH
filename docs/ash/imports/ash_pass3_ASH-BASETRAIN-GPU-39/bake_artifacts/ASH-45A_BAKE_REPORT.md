# ASH-45A Bake Report

## Commit
ASH-45A — Adapter-Scoped Calibration Evidence Isolation

## Result
PASS_ASH_45A_ADAPTER_SCOPED_CALIBRATION_EVIDENCE_ISOLATION

## What Changed
ASH-45A adds an attribution layer between raw ASH-45 evidence sources and scoring adjustment generation. Rollback, perf, and manual-review signals now carry attribution scope before they can affect adapter/event-tag scoring.

## New Contracts
- `AshCalibrationAttributionClass`
- `AshCalibrationAttributionDecision`
- `AshCalibrationAttributionTrace`
- `attribute_rollback_signal_to_adapter()`
- `attribute_perf_signal_to_adapter()`
- `attribute_manual_review_signal_to_adapter()`
- `attribution_decision_for_trace()`
- `is_attribution_eligible_for_adjustment_class()`

## Guarded Cases
- Direct adapter rollback remains eligible for threshold / avoidance calibration.
- Unrelated adapter rollback is demoted to `GlobalUnattributed` warning-only evidence.
- Global perf pressure without artifact/current-pointer match no longer becomes adapter-scoped `PerfRegression`.
- Evidence with `GlobalUnattributed` attribution cannot become strong-confidence.
- Adjustment generation filters global/unknown unattributed evidence before applying multiplier or threshold changes.

## Non-mutations Preserved
- Runtime router config: unchanged.
- ASH-38 routing policy: unchanged.
- ASH-34 temporal overlay: unchanged.
- Current pointer: unchanged.
- Adapter registry: unchanged.
- LoRA attach/detach: not executed.
- Hot reload: not executed.
- Python validator: not added.

## Local Execution Note
This bake environment does not provide `cargo`/`rustc`, so Rust-native tests were sealed but not executed here. Static checks verified the ASH-45A files, attribution fields, audit booleans, and no Python validator addition.
