# ASH-BASETRAIN-GPU-37K-R1 Bake Report

## Patch

ASH-BASETRAIN-GPU-37K-R1

## Scope

Buildfix only. No semantic expansion.

## Applied Change

Fixed two Rust E0425 local variable alias errors inside `block_output_with_runtime()`.

```rust
bind_group_receipt_digest_hex: bind_group_digest_hex,
payload_receipt_digest_hex: payload_digest_hex,
```

## Static Checks

See:

```txt
artifacts/ASH_BASETRAIN_GPU_37K_R1_STATIC_CHECKS.txt
artifacts/ASH_BASETRAIN_GPU_37K_R1_STATIC_CHECKS.json
```

## Runtime Status

Cargo build/run could not be executed in this container because `cargo/rustc` are unavailable here.

## Receipt Inclusion Policy

Live upstream receipts are not included:

```txt
artifacts/ASH_BASETRAIN_GPU_37J_SELECTED_GROUP_ROW_BLOCK_BIND_GROUP_CANDIDATE.json
artifacts/ASH_BASETRAIN_GPU_37F_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_READBACK_SMOKE.json
```

No `*.sha256` files are included.
