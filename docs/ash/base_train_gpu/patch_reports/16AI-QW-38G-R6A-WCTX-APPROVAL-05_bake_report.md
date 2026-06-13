# WCTX-APPROVAL-05 Bake Report

## Contract

`Explicit Runtime Apply Receipt Bind / No Silent Append No Sequence Mutation Seal`

## Baked files

```txt
crates/ash_core/src/word_context_approval_05_explicit_runtime_apply_receipt_bind.rs
crates/ash_core/src/bin/ash_word_context_approval_05_explicit_runtime_apply_receipt_bind.rs
crates/ash_core/src/lib.rs
acceptance_reports/16AI-QW-38G-R6A-WCTX-APPROVAL-05.md
patch_reports/16AI-QW-38G-R6A-WCTX-APPROVAL-05_bake_report.md
WCTX_APPROVAL_05_STATIC_CHECKS.txt
WCTX_APPROVAL_05_BAKE_MANIFEST.json
```

## Boundary

Opened:

```txt
explicit_runtime_apply_action_present = true
runtime_apply_receipt_bind_executed = true
runtime_apply_receipt_created = true
target_runtime_snapshot_present = true
```

Closed:

```txt
silent_append_executed = false
implicit_append_executed = false
default_append_executed = false
runtime_token_append_executed = false
runtime_sequence_mutated = false
sequence_mutation_receipt_created = false
runtime_output_created = false
production_output_emitted = false
```

## Build status

`BAKED_STATIC_NO_CARGO`

`cargo` and `rustc` were not available in the baking container, so this bake includes static file checks only.
