# 16AI-QW-38G-R6A-SALAD-01B — Runtime AshGate Scope Repair / Decode Profile Event Seal

## Summary

SALAD-01A compiled through `ash_core` and then failed in `runtime` because `generation_runner.rs` referenced `gate.audit.decode_profile` and `gate.audit.word_salad_guard` after `gate` was no longer in scope.

## Fix

The patch now captures `decode_profile` and `word_salad_guard` immediately after `derive_gate(...)`, returns both values through the outer tuple, and uses those closure-owned values when emitting `GenerateEvent::AshGate`.

## SSOT

SALAD-01 remains a decode stability / runtime policy patch. It does not modify model weights, tokenizer, safetensors, lm_head, final_norm, or ban masks.

## Local validation command

```powershell
cargo build
```

## Adjudication

PASS_STATIC_SCOPE_HOTFIX_PENDING_LOCAL_CARGO_BUILD
