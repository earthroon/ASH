# QW-50-R0H — edge registry missed evidence calls / center cue clone fix

## Scope

- Target crate: `ash_core`
- Target file: `crates/ash_core/src/word_context_edge_registry.rs`

## Fix

- Replaced remaining `evidence(...)` helper calls in edge registry push sites with `build_evidence(...)`.
- Fixed `first.center_cue_id` partial move by cloning the field before later borrowing `first`.

## Static Pattern Check

```json
{
  "patch_id": "QW-50-R0H",
  "target_file": "crates/ash_core/src/word_context_edge_registry.rs",
  "evidence_push_evidence_remaining": false,
  "evidence_list_push_evidence_remaining": false,
  "ev_push_evidence_remaining": false,
  "build_evidence_call_count": 30,
  "fn_build_evidence_exists": true,
  "center_cue_id_clone_present": true,
  "center_cue_id_direct_move_remaining": false,
  "brace_balance": 0,
  "paren_balance": 0,
  "bracket_balance": 0,
  "status": "STATIC_PATTERN_CHECK_PASS"
}
```

## Guard

- No evidence ordering change intended.
- No edge relation policy change intended.
- No confidence band mutation intended.
- No receipt hash mutation intended.
- No runtime pointer mutation.
- No adapter registry mutation.
- No production apply.

## Verification

```txt
cargo check -p ash_core --lib
```

## Status

PENDING_LOCAL_CARGO_CHECK
