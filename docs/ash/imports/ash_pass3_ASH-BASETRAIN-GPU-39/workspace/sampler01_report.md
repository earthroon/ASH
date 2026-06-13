# 16AI-QW-38G-R6A-SAMPLER-01 Report

## 확정

- `gpu_sampling_topp_scan.wgsl` no longer uses the full-vocabulary `stats[0].sum_exp` as the top-p denominator after top-k/min-p filtering.
- Active probabilities are now computed from the post top-k/min-p active set: `active_sum_exp`.
- `gpu_sampling_select.wgsl` no longer falls through to `best_idx = 0u` when `final_mask` is empty. It prefers final candidates, then active-probability candidates, then finite global candidates.
- `gpu_sampling_select_legacy.wgsl` was aligned to the same active-set renormalization semantics instead of retaining the old full-denominator path.
- Recovery mode is encoded into `SelectionOut._pad0` without changing the GPU buffer ABI.

## 추정

This should reduce word-salad risk caused by mismatched CPU/GPU candidate sets and silent token-0 fallback, but runtime parity must still be checked with cargo/WGSL validation in an environment that has the Rust toolchain.

## 판단불가

- `cargo check` / `cargo test` / `rustfmt` were not run in this container.
- Actual WebGPU shader compilation and dispatch parity were not run.
- The runtime value of recovery mode is logged but not yet promoted into a high-level receipt object.
