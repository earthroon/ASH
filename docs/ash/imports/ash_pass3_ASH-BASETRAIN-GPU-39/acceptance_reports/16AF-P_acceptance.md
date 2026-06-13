# 16AF-P Acceptance Report

## Verdict

```txt
16AF-P = PASS
generation_connected = false
runtime_gate = multi_layer_ffn_parity_only
```

## Criteria

```txt
AC-16AF-P-1 selected layers shape_match=true: true
AC-16AF-P-2 nan_count=0 and inf_count=0: true
AC-16AF-P-3 max_abs_delta <= threshold: true
AC-16AF-P-4 mean_abs_delta <= threshold: true
AC-16AF-P-5 top_index_match=true: true
AC-16AF-P-6 top_k_overlap tracked: true
AC-16AF-P-7 generation_connected=false: true
AC-16AF-P-8 forbidden path list empty: true
AC-16AF-P-9 JSON + Markdown report written: true
```

## Summary

```txt
total = 14
completed = 14
passed = 14
failed = 0
max_abs_delta_global = 0.0000000260770320892334
mean_abs_delta_avg = 0.0000000024972721668348186
elapsed_ms_total = 50325.8817
telemetry_total_gpu_ms = 622.6086999999999
telemetry_weight_upload_ms = 213.10080000000002
telemetry_submit_readback_ms = 393.1204
telemetry_readback_buffers = 14
telemetry_readback_elements = 28672
```
