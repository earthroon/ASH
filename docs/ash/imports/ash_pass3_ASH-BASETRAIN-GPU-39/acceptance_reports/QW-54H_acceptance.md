# QW-54H Acceptance

Status: PATCH_IMPLEMENTED_PENDING_LOCAL_CARGO_RUNTIME_CHECK

## PASS criteria

- `cargo check -p model_core --lib`
- `cargo check -p runtime --all-targets`
- `infer_only --enable-qw54f --enable-qw54g --enable-qw54h --json` accepts flags.
- QW-54H trace records `greedy_status = PROVISIONAL_ONLY` when QW-54G detected set contains selected token.
- QW-54H receipt keeps `hard_ban_used_count = 0`, `token_masked_count = 0`, `vocab_removed_count = 0`.

## FAIL criteria

- closed attractor detected and selected token is member, but selected_after == selected_before without invariant violation trace.
- QW-54H uses hard ban, token mask, vocab removal, or model mutation.
