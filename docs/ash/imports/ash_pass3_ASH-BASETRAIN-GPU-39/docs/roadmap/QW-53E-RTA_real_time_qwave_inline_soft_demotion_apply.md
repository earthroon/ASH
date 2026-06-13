# QW-53E-RTA Roadmap

1. Wire WGPU top-k candidate source into the inline QW-53E-RTA hook.
2. Build live QWave context from WGPU/QWave evidence, not CPU oracle rows.
3. Calculate repeat/QWave risk in Rust-owned runtime policy.
4. Apply finite soft demotion to candidates only in explicit lab mode.
5. Preserve candidate set and pass adjusted candidates to sampler.
6. Write original-vs-adjusted traces and receipts.
7. Validate no hard ban, no token mask, no vocab removal, no CPU candidate apply.

Next likely patch: QW-53F — Aggressive Lab Decode A/B Trace / Loop Escape Quality Regression Seal.
