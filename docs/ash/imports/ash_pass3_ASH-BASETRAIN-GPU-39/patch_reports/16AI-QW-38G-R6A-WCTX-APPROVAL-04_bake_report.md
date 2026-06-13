# WCTX-APPROVAL-04 Bake Report

## Contract

`Runtime Apply Gate Draft / No Silent Apply Seal`

## Baked files

```txt
crates/ash_core/src/word_context_approval_04_runtime_apply_gate_draft.rs
crates/ash_core/src/bin/ash_word_context_approval_04_runtime_apply_gate_draft.rs
crates/ash_core/src/lib.rs
acceptance_reports/16AI-QW-38G-R6A-WCTX-APPROVAL-04.md
patch_reports/16AI-QW-38G-R6A-WCTX-APPROVAL-04_bake_report.md
WCTX_APPROVAL_04_STATIC_CHECKS.txt
WCTX_APPROVAL_04_BAKE_MANIFEST.json
```

## Boundary

Opened:

```txt
runtime_apply_gate_draft_created = true
explicit_runtime_apply_required = true
runtime_state_snapshot_bound = true
```

Closed:

```txt
runtime_apply_executed = false
runtime_apply_receipt_created = false
silent_apply_executed = false
implicit_apply_executed = false
default_apply_executed = false
runtime_token_append_executed = false
runtime_sequence_mutated = false
runtime_output_created = false
production_output_emitted = false
```

## Build status

`BAKED_STATIC_NO_CARGO`

`cargo` and `rustc` were not available in the baking container, so this bake includes static file checks only.
