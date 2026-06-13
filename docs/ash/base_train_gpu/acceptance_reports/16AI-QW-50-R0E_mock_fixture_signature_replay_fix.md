# QW-50-R0E — mock fixture signature replay fix

## Scope

- Target crate: `ash_core`
- Target file: `crates/ash_core/src/word_context_mock_wctx_e2e_chain_index.rs`

## Fix

- Updated `build_enko_mock_decode_candidate_fixture_receipt` call site from the obsolete one-argument `&case` form to the current three-argument signature.
- Passed `&case.staging_receipt`, `case.mock_candidate_target_korean.as_str()`, and `case.mock_reason.as_str()` explicitly from each mock fixture case.
- Removed invalid `commit.replay_result.runtime_apply_executed` access.
- Used `commit.risk.runtime_apply_executed` for mutation invariant aggregation while preserving non-mutating mock replay semantics.

## Guard

- No runtime apply execution was introduced.
- No production apply was introduced.
- No runtime pointer mutation was introduced.
- No adapter registry mutation was introduced.
- No unrelated files were patched.

## Static Pattern Check

```json
{
  "patch_id": "QW-50-R0E",
  "target_file": "crates/ash_core/src/word_context_mock_wctx_e2e_chain_index.rs",
  "one_arg_builder_call_remaining": false,
  "three_arg_builder_call_present": true,
  "commit_replay_result_runtime_apply_executed_remaining": false,
  "commit_risk_runtime_apply_executed_present": true,
  "runtime_apply_gate_open_as_executed_pattern_remaining": false,
  "file_sha256": "88ca3a1de58314708437c0ca7bd22b2e252269b007c90c4ab6d25dd59916a66a",
  "status": "PASS_STATIC_PATTERN_CHECK"
}
```

## Verification

```txt
cargo check -p ash_core --lib
```

## Status

PENDING_LOCAL_CARGO_CHECK
