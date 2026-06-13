# ASH-BASETRAIN-GPU-37K-R1 Acceptance Report

## Title

GPU Readback Payload Receipt Digest Alias Buildfix / Local Digest Variable Rebind No Dispatch Seal

## Source Patch

ASH-BASETRAIN-GPU-37K

## Problem

The 37K source generated local digest variables named:

```txt
bind_group_digest_hex
payload_digest_hex
```

but the blocked output constructor attempted to initialize `Output` using shorthand names that did not exist in the local scope:

```txt
bind_group_receipt_digest_hex
payload_receipt_digest_hex
```

This caused Rust E0425 compile errors.

## Fix

The `Output` initializer now explicitly maps the local digest aliases to the `Output` fields:

```rust
bind_group_receipt_digest_hex: bind_group_digest_hex,
payload_receipt_digest_hex: payload_digest_hex,
```

## Guard Preservation

This patch does not change the 37K runtime policy.

Allowed remains:

```txt
bounded File::open / SeekFrom::Start / read_exact
payload assembly
queue.write_buffer
GPU device/shader/pipeline/buffer/bind group recreation
```

Forbidden remains:

```txt
read_to_end
mmap runtime materialization
F32 decode
copy_buffer_to_buffer
map_async
readback
dispatch_workgroups
forward/backward/optimizer/mutation
```

## Static Verdict

```txt
STATIC_CHECK_PASS
```
