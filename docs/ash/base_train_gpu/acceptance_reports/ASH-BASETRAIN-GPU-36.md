# ASH-BASETRAIN-GPU-36 Acceptance Report

## Selected Group Weight Slice Load Preflight / Manifest Candidate To Byte Range Read Plan No Tensor Full Load No GPU Upload Seal

### Static bake verdict

`BLOCKED_R3B_RECEIPT_NOT_FOUND`

This is a valid sealed static result for the bake environment because no explicit `--r3b-receipt` path was provided during static bake.

### Local PASS command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_36_selected_group_weight_slice_load_preflight -- --r3b-receipt .rtifacts\ASH_BASETRAIN_GPU_35_R3B_ATLAS_GROUP_TENSOR_KEY_JOIN_ADAPTER.json
```

### Required PASS status

```txt
PASS_ASH_BASETRAIN_GPU_36_SELECTED_GROUP_WEIGHT_SLICE_LOAD_PREFLIGHT_MANIFEST_CANDIDATE_TO_BYTE_RANGE_READ_PLAN_NO_TENSOR_FULL_LOAD_NO_GPU_UPLOAD
```

### Scope

- Reads the R3B PASS receipt.
- Validates `selected_group_manifest_candidate_count == 1`.
- Validates dtype, shape, element count, expected byte size, file absolute offset range, source digest flag, and runtime default apply guard.
- Materializes only a read plan envelope.

### Explicitly closed

- selected group weight bytes read
- full tensor load
- safetensors header read
- file open
- mmap materialization
- GPU device request
- GPU buffer creation
- GPU upload
- forward
- backward
- optimizer
- delta materialization
- checkpoint write
- safetensors mutation
- runtime 1.1B training claim

### Next patch on PASS

`ASH-BASETRAIN-GPU-36A` — Bounded Weight Slice Read Smoke / Read Plan To Limited Byte Window Probe No Tensor Full Load No GPU Upload Seal
