# 16AF-P Acceptance PENDING

## Verdict

```txt
16AF-P = PENDING_LOCAL_RUN
generation_connected = false
```

## Acceptance Criteria

```txt
AC-16AF-P-1 cargo check passes for burn_webgpu_backend and model_core.
AC-16AF-P-2 af16p_ffn_perf_probe runs all layers [0..13].
AC-16AF-P-3 total=14, passed=14, failed=0, parity_pass=true.
AC-16AF-P-4 generation_connected=false.
AC-16AF-P-5 readback_mode=output_only for every layer.
AC-16AF-P-6 readback_buffers=1 for every layer.
AC-16AF-P-7 readback_elements=2048 for current hidden=2048 spec.
AC-16AF-P-8 shader_pipeline_cached=true.
AC-16AF-P-9 max_abs_delta and mean_abs_delta remain under threshold.
AC-16AF-P-10 forbidden path scan remains clean.
```

## Failure Criteria

```txt
FAIL-16AF-P-1 parity regression.
FAIL-16AF-P-2 WGPU validation panic.
FAIL-16AF-P-3 readback_mode falls back to full_intermediates in P probe.
FAIL-16AF-P-4 generation path is connected.
FAIL-16AF-P-5 Tensor.matmul / fused_matmul_autotune / LocalTuner / RawWgpuBufferLease / into_contiguous_aligned reappears in 16AF-P path.
```
