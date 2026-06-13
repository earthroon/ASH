# ASH-BASETRAIN-GPU-36F Bake Report

## Result

Baked from 36E ZIP with a new receipt-only materialization preflight runner.

## Added implementation

- crates/base_train/src/ash_basetrain_gpu_36f_cpu_tensor_view_candidate_materialization_preflight.rs
- crates/base_train/src/bin/ash_basetrain_gpu_36f_cpu_tensor_view_candidate_materialization_preflight.rs

## Static receipt

- artifacts/ASH_BASETRAIN_GPU_36F_CPU_TENSOR_VIEW_CANDIDATE_MATERIALIZATION_PREFLIGHT.json
- static status: BLOCKED_36E_RECEIPT_NOT_FOUND

## Important boundary

The 36E live input receipt path was removed from the baked ZIP:

```txt
artifacts/ASH_BASETRAIN_GPU_36E_BOUNDED_WEIGHT_SLICE_ROW_CONTINUITY_PROMOTION_GATE.json
```

This prevents stale/static 36E output from overwriting the operator's local PASS receipt.

## Static checks

```txt
source_sha256=b01ab833cb6195bfd01d574031763bfefddfed3d414a52f2cf27633adcb3838c
bin_sha256=c1693851063132a17760378a8239d3a955df74a5d89280450f2c1fe5b0ee41f3
static_receipt_sha256=22abce4af7666eff9181e8405a8398ff3c15447f328013a50abc05ab1c374404
hex_crate_reference_present=false
source_safetensors_file_open_call_present=false
seek_call_present=false
read_to_end_call_present=false
mmap_runtime_call_present=true
wgpu_runtime_call_present=false
match_keyword_present=true
if_keyword_count=0
```

## Build note

The bake container does not provide cargo/rustc, so local cargo build/run must be performed by the operator.
