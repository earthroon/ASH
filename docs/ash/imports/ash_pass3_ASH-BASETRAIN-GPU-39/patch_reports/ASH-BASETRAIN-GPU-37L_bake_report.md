# ASH-BASETRAIN-GPU-37L Bake Report

## Patch

`ASH-BASETRAIN-GPU-37L` adds the first actual dispatch smoke path after 37K upload.

## SSOT

- Primary: 37K bound resource upload candidate receipt.
- Payload: 37F verified payload/readback smoke receipt.

## Runtime boundary

37L replays bounded payload read and queue upload, then executes a diagnostic compute dispatch. It copies 16 bytes from `diagnostic_out` into a readback buffer and checks `word0 == u32::from_le_bytes(payload[0..4])`.

## Container limitation

`cargo/rustc` is unavailable in this container, so local build/run is operator-side. Static guards and artifact generation were completed.
