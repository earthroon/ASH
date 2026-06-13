# 16AF-M Multi-Layer FFN Parity Matrix Bake Report

## Status

```txt
16AF-M = BAKED
generation_connected = false
runtime_gate = multi_layer_ffn_parity_only
runtime_validation = PENDING_LOCAL_RUN
```

## SSOT

```txt
Base: 16AF-R1a export cleanup bake
Prior runtime proof: 16AF-R layer=0 PASS
Goal: selected layers [0,1,last] Native Atlas FFN parity matrix
```

## Changed Files

```txt
crates/model_core/src/native_atlas_ffn_probe.rs
crates/model_core/src/bin/af16m_multi_layer_parity.rs
scripts/run_16AF_M_multi_layer_parity.ps1
scripts/run_16AF_M_multi_layer_parity.sh
```

## Implementation

```txt
- Added run_native_atlas_ffn_16af_parity_probe_with_top_k(...)
- Preserved old run_native_atlas_ffn_16af_parity_probe(...) as top_k=8 wrapper
- Added af16m_multi_layer_parity runner
- Default selected layer set: [0, 1, last]
- Supported flags: --layers, --all-layers, --threshold, --top-k, --fail-fast, --out-json, --out-md, --out-acceptance
- Writes infer_debug/16AF-M_multi_layer_parity.json
- Writes infer_debug/16AF-M_multi_layer_parity.md
- Writes acceptance_reports/16AF-M_acceptance.md
```

## Runtime Contract

```txt
PASS requires:
shape_match=true for all requested layers
nan_count=0
inf_count=0
max_abs_delta <= threshold
mean_abs_delta <= threshold
top_index_match=true
generation_connected=false
forbidden_paths_used=[]
```

## Static Forbidden Path Scan

```txt
No forbidden path references found in new 16AF-M runner/probe changes.
```

## Toolchain Note

```txt
cargo/rustc unavailable in this container.
Local cargo check/runtime execution remains pending.
```
