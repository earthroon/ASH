# SFT-FFN-INFRA-GPU-SAFETY-01 Acceptance

## Status

PASS_STATIC / PENDING_WGPU_RUNTIME_TEST

## Scope

WGPU map_async readback deadlock guard and generation telemetry profiling gate.

## SSOT

- Readback policy digest
- Readback receipt digest
- Telemetry policy digest
- Telemetry gate digest
- GPU safety seal

## Confirmed Static Gates

- `gpu_penalty.rs` readback now uses explicit `device.poll(PollType::Poll)` inside a bounded callback progress loop.
- `gpu_penalty.rs` no longer uses `rx.recv()` as an unbounded wait in `map_readback_bytes`.
- `gpu_penalty.rs` has a timeout guard for map readback.
- `gpu_sampling.rs` readback now uses explicit `device.poll(PollType::Poll)` inside a bounded callback progress loop.
- `gpu_sampling.rs` no longer uses `rx.recv()` as an unbounded wait in its readback helper.
- `gpu_sampling.rs` has a timeout guard for map readback.
- `burn_webgpu_backend` exposes a `profiling` feature gate.
- `topk_us`, `select_us`, and related pass timings are recorded through a profiling-gated helper.
- In non-profiling builds, GPU sampling perf counters are not enabled by default.
- `generation_telemetry.rs` keeps us-level metrics only when backend perf telemetry is enabled.
- Runtime attach remains closed.
- Promotion apply remains closed.
- Current pointer update remains closed.

## Opened

- map_async readback deadlock guard
- explicit device.poll boundary
- readback timeout guard
- map_async error receipt
- telemetry profiling gate
- token telemetry sampling boundary
- GPU safety receipt

## Closed

- unbounded rx.recv blocking wait in targeted readback helpers
- per-token telemetry always-on default
- GPU timestamp sync in production default path
- production runtime attach
- promotion apply
- current pointer update

## Runtime Acceptance Pending

Requires WGPU runtime test or certified external device.poll loop evidence.
