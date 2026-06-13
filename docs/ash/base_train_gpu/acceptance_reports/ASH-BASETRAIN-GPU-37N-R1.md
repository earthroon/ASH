# ASH-BASETRAIN-GPU-37N-R1 Acceptance Report

## Patch

`ASH-BASETRAIN-GPU-37N-R1`

Payload Receipt Digest Alias Buildfix / Local Payload Digest Variable Rebind Seal

## Source Patch

`ASH-BASETRAIN-GPU-37N`

## Fixed Build Error

```txt
error[E0425]: cannot find value `payload_receipt_digest_hex` in this scope
```

## Root Cause

The local digest variable created by the receipt loader was named:

```rust
payload_digest_hex
```

but the `Output` initializer in `block_output()` used shorthand syntax for a non-existent local variable:

```rust
payload_receipt_digest_hex,
```

## Fix

The `Output` field now explicitly receives the existing local variable:

```rust
payload_receipt_digest_hex: payload_digest_hex,
```

## Guard Preservation

- Multi-word diagnostic dispatch path remains unchanged.
- `dispatch_workgroups`, `copy_buffer_to_buffer`, `map_async`, and `queue.write_buffer` remain allowed for 37N.
- Forward/backward/optimizer/mutation remain sealed.
- Live 37M and 37F PASS receipts are not included in the baked ZIP.
- No `*.sha256` files are included.

## Static Verdict

`STATIC_CHECK_PASS`

## Runtime Verdict

Cargo was not available in the bake container, so local cargo build/run is left to the operator environment.
