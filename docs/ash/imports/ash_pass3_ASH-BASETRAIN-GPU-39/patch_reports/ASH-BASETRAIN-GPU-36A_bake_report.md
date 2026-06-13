# ASH-BASETRAIN-GPU-36A Bake Report

- Added bounded window read smoke runner.
- Uses lookup-table / combinator style control flow; no standalone Rust `if`/`match` tokens in 36A source.
- Static baked receipt blocks with `BLOCKED_36_RECEIPT_NOT_FOUND` because no local 36 PASS receipt is provided in the bake container.
- Previous patch runtime receipts are intentionally excluded from their original artifact paths to avoid overwriting local PASS receipts.
- Cargo/rustc unavailable in bake container; local build/run required.
