# SAME DEVICE RAW LOGITS BRIDGE PRIORITY6 PATCH

## Goal
Implement roadmap stage 3 on top of priority5:
- keep eager `cpu_row` elimination from hot sampled path
- keep GPU-native exact `top_k`
- add **GPU-native exact `top_p`** filtering in the backend selection shader

## Scope
- `crates/burn_webgpu_backend/src/shaders/gpu_sampling_select.wgsl`
- docs only; no Rust-side bind layout changes

## What changed
The select shader now:
1. computes temperature-scaled logits entirely on-GPU
2. computes global `max_scaled` and `sum_exp` for normalization
3. preserves the existing exact `top_k` membership rule
4. adds exact nucleus (`top_p`) membership by comparing a token's probability with the cumulative mass of all higher-probability tokens (plus deterministic tie-break by lower index)
5. emits a real logprob for the selected token from the full normalized distribution instead of echoing score as placeholder

## Current tradeoff
This is still a **single-invocation scalar WGSL path**.
That means:
- exact and deterministic for small/medium vocab
- not performance-optimal
- intended as truth path / correctness patch before later multi-pass optimization

## Not included yet
- multi-workgroup prefix-sum implementation for `top_p`
- separate `gpu_sampling_topp_scan.wgsl` runtime wiring
- zero-readback finalization
- compile verification in this environment
