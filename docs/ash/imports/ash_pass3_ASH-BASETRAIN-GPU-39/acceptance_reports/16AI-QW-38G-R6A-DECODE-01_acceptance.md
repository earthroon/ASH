# 16AI-QW-38G-R6A-DECODE-01 Acceptance

## Static acceptance
- [x] CPU oracle sampler module exists.
- [x] `SamplingApplyMode::CpuOracleSampler` exists.
- [x] `sample_with_cpu_oracle` exists.
- [x] sampled decode fallback no longer calls `select_next_token(&logits_for_fallback)` directly.
- [x] reference checkpoint streaming path calls CPU oracle when sampled decode is requested.
- [x] DECODE-00 probe schema extended with CPU oracle fields.
- [x] summary, fixture, schema, report generated.

## Execution acceptance
- [ ] `cargo check` — NOT_RUN, cargo unavailable.
- [ ] `cargo test` — NOT_RUN, cargo unavailable.
- [ ] `rustfmt` — NOT_RUN, rustfmt unavailable.

## Seal
Static bake accepted with execution validation pending in Rust toolchain environment.
