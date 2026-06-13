# 16AI-QW-38G-R6A-SAMPLER-01 Acceptance

## Static checks

- GPU top-p active-set renormalization: PASS_STATIC
- Full-vocab denominator removed from post-filter top-p math: PASS_STATIC
- final_mask empty token-0 fallback removed: PASS_STATIC
- legacy shader active-set semantics aligned: PASS_STATIC
- recovery mode ABI-compatible encoding: PASS_STATIC
- CPU/GPU parity fixtures generated: PASS_STATIC

## Execution checks

- cargo check: NOT_RUN
- cargo test: NOT_RUN
- rustfmt: NOT_RUN
- WebGPU shader runtime compile: NOT_RUN

## Notes

The patch intentionally avoids adding new GPU buffers. Recovery mode uses the existing `_pad0` field in `SelectionOut`.

## Static check artifact

- `workspace/sampler01_static_checks.json`: PASS
