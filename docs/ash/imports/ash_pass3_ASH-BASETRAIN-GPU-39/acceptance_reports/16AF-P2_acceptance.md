# 16AF-P2 Acceptance Report

## Verdict

```txt
16AF-P2 = PASS
generation_connected = false
runtime_gate = ffn_weight_preupload_perf_only
```

## Criteria

```txt
AC-16AF-P2-1 generation_connected=false: true
AC-16AF-P2-2 all requested layers completed: true
AC-16AF-P2-3 preupload cache generated: true
AC-16AF-P2-4 cached weight dispatch used: true
AC-16AF-P2-5 layer weight_upload_ms near-zero: true
AC-16AF-P2-6 all layers parity pass: true
AC-16AF-P2-7 max_abs_delta <= threshold: true
AC-16AF-P2-8 nan_count=0 and inf_count=0: true
AC-16AF-P2-9 top_k_overlap tracked: true
AC-16AF-P2-10 forbidden path list empty: true
AC-16AF-P2-11 JSON + Markdown report written: true
```

## Summary

```txt
total = 14
completed = 14
passed = 14
failed = 0
max_abs_delta_global = 0.0000000260770320892334
mean_abs_delta_avg = 0.0000000024972721668348186
telemetry_weight_upload_ms = 0
weight_upload_reduction_ratio = 1
```
