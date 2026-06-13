# 16AI-QW-43 — Minimal Pair Eval Matrix / Word Salad Regression Seal

## Seal

QW-43 creates a minimal-pair evaluation matrix and compares the current adapter baseline against the QW-42 delta candidate in shadow-only mode.

## Scope

Added:

- `crates/lora_train/src/qwave_eval_metric.rs`
- `crates/lora_train/src/minimal_pair_eval_matrix.rs`
- `crates/lora_train/src/delta_candidate_eval.rs`
- `crates/lora_train/src/word_salad_regression_eval.rs`
- `artifacts/minimal_pair_eval/qw43_minimal_pair_eval_matrix.json`
- `artifacts/minimal_pair_eval/qw43_baseline_eval_report.json`
- `artifacts/minimal_pair_eval/qw43_delta_candidate_eval_report.json`
- `artifacts/minimal_pair_eval/qw43_word_salad_regression_report.json`
- `artifacts/minimal_pair_eval/qw43_minimal_pair_eval_matrix_receipt.json`
- `artifacts/minimal_pair_eval/qw43_baseline_eval_receipt.json`
- `artifacts/minimal_pair_eval/qw43_delta_candidate_eval_receipt.json`
- `artifacts/minimal_pair_eval/qw43_word_salad_regression_eval_receipt.json`

Modified:

- `crates/lora_train/src/lib.rs`
- `meta.json`

## Source receipts

QW-43 references the QW-35 through QW-42 receipt chain, including:

- QW-38 word-salad negative corpus receipt
- QW-42 adapter delta artifact receipt
- QW-42 rollback pointer receipt

## Evaluation mode

Native forward evaluation was not executed in this container because `cargo` / `rustc` is unavailable.

Therefore this patch is explicitly sealed as:

- `eval_executed_native = false`
- `eval_static_shadow_only = true`
- `decision = PendingNativeEval`

No `PASS_RUNTIME` claim is made.

## Static shadow regression summary

Static fixture values were generated for the minimal-pair matrix:

- sample_count: 3
- improved_count: 3
- regressed_count: 0
- neutral_count: 0
- mean_word_salad_score_delta: -0.075
- mean_qwave_smoothness_delta: -0.02125
- mean_semantic_preservation_delta: 0.01725
- mean_route_instability_delta: -0.051
- max_regression_score: 0.0
- decision: PendingNativeEval

## Mutation guard

The QW-43 evaluation stage does not apply the delta to production.

- production_apply_executed: false
- runtime_pointer_mutated: false
- adapter_pointer_mutated: false
- base_model_mutated: false
- optimizer_step_executed: false
- backward_executed: false

## Acceptance status

`PASS_STATIC_SHADOW_PENDING_NATIVE_EVAL`

The minimal-pair matrix, baseline report, delta-candidate report, and word-salad regression receipts were generated. Native runtime validation remains pending.
