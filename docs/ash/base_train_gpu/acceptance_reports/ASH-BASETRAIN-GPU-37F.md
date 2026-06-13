# ASH-BASETRAIN-GPU-37F Acceptance Report

## Patch

ASH-BASETRAIN-GPU-37F

Selected Group Row-Block GPU Upload Readback Smoke / Actual GPU Buffer To CPU Digest Verification No Dispatch Seal

## SSOT

Input SSOT is a local PASS receipt:

```text
artifacts/ASH_BASETRAIN_GPU_37E_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_SMOKE.json
```

This baked ZIP intentionally does not include that live 37E receipt, to avoid overwriting the operator's local PASS receipt.

## Purpose

37F validates the representative GPU upload path by reading the same three source segments, uploading their contiguous payload to a GPU storage buffer, copying that storage buffer to a MAP_READ readback buffer, mapping the readback range, and comparing CPU source bytes against GPU readback bytes by digest.

## Allowed

- bounded source segment read by `seek + read_exact`
- actual GPU instance / adapter / device / queue request
- actual storage buffer creation
- actual readback buffer creation
- `queue.write_buffer`
- command encoder creation
- `copy_buffer_to_buffer`
- `queue.submit`
- `map_async`
- readback digest verification

## Forbidden

- full selected group read
- F32 decode
- CPU tensor materialization
- compute shader module
- compute pipeline
- bind group
- dispatch
- forward
- backward
- optimizer
- mutation

## Expected PASS

```text
PASS_ASH_BASETRAIN_GPU_37F_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_READBACK_SMOKE_ACTUAL_GPU_BUFFER_TO_CPU_DIGEST_VERIFICATION_NO_DISPATCH
```

## Static bake verdict

```text
BLOCKED_37E_RECEIPT_NOT_FOUND
```

This is expected in the bake container because the live 37E PASS receipt is not included.
