# ASH-BASETRAIN-GPU-35-R2C-R1 Acceptance

## Verdict

Compile-only buildfix candidate.

## Expected local result

- `error[E0308] mismatched types` for `EXPECTED_GROUP_ID` should be resolved.
- Unused parentheses warning in `confidence()` should be resolved.

## Non-goals

This R1 patch does not execute weight load, GPU allocation, backward, optimizer, or checkpoint mutation.
