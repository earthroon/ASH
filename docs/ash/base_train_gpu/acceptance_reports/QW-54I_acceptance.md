# QW-54I Acceptance Report

## Status

`PATCH_IMPLEMENTED_PENDING_LOCAL_CARGO_RUNTIME_CHECK`

## Implemented

- Runtime-local recent attractor orbit ledger
- TTL-based expiry
- Canonical sorted/deduped attractor token set signature
- QW-54H escape event ledger capture
- Current QW-54G set overlap check
- Soft cooldown demotion
- Trace/report/receipt output
- CLI/env/profile wiring

## Contract preserved

```txt
hard_ban_used = false
token_masked = false
vocab_removed = false
model_weight_mutation = false
sampler_default_silent_mutation = false
```

## Local validation required

```powershell
cargo check -p model_core --lib
cargo check -p runtime --all-targets
```

## Runtime evidence required

A passing runtime trace should show:

```txt
qw54h_escape_event_observed = true
ledger_entry_created = true
recent_orbit_hit = true on later overlapping steps
cooldown_applied = true or cooldown_reason = NoSafeReplacement
hard_ban_used = false
token_masked = false
vocab_removed = false
invariant_violation = false
```
