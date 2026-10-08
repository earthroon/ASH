# AOF-R1-CF1: Native Compile Closure

## Revision
- Parent: AOF-R1-VH5.
- Scope: backend/base_train/model_core/orchestrator native Cargo boundary and exact workspace dependency input.
- Successor: AOF-R1-CF2.
- This document is a **contract and implementation description, not a PASS receipt**.

## Required implementation
1. Repair the existing `burn_webgpu_backend::aof_r1_verification::wait_for_queue` visibility for the true `base_train` consumer. Preserve one canonical completion implementation, including actual `Queue::on_submitted_work_done`, polling, error semantics and device binding.
2. Do not substitute head-execution math-fixture compile for native crate/binary compile.
3. Preflight `crates/asr_sidecar/Cargo.toml` exact `sherpa-rs` path dependency. Missing vendor input is a dedicated HOLD; never create a dummy package, change dependency versions, suppress the workspace member, or claim AOF E0603 from a missing-path Cargo failure.
4. Preserve legacy/fused head numerical contracts, rank and +2/+3/+4/+5 topology, head-only optimizer, prefix-commit, FuturePool, packed retirement, EOS/cancel/emit, and production OFF.
5. The API visibility expansion `pub(crate) -> pub` is an explicit *API scope change*, not a queue completion policy change.

## Exact source touch points
- `crates/burn_webgpu_backend/src/aof_r1_verification.rs`
- `crates/orchestrator_local/src/aof_r1_cf1_native_compile_cli.rs`
- `crates/orchestrator_local/src/bin/ash_aof_r1_cf7_cf8_cf9_gate.rs`
- Do not rewrite `Cargo.toml` / `Cargo.lock` merely to bypass the missing external input.

## Execution authority
```text
cargo metadata --format-version 1 --locked
cargo check -p burn_webgpu_backend --lib --release --locked -j 1
cargo check -p model_core --lib --release --locked -j 1 --features aof-r1-qualification
cargo check -p base_train --lib --release --locked -j 1
cargo check -p base_train --bin ash_aof_r1_frozen_heads_quality --release --locked -j 1
cargo check -p orchestrator_local --bin ash_aof_r1_cf7_cf8_cf9_gate --features orchestrator_aof_r1_audit_bins --release --locked -j 1
```
The actual manifest target names and required features are authoritative.

## Receipt and gate
- CLI: `--cf1-compile --out NEW_FILE`.
- Receipt: `aof_r1_cf1_native_compile_closure_receipt.json`, schema `ash.aof_r1.cf1.native_compile_closure.v1`.
- Record selected source digest, before/after digest, Cargo.lock digest within the digest scope, exact dependency input state, six stage commands and exit codes, stderr digests/tails and SHA, runtime=NOT_RUN, physical=NOT_RUN.
- Missing vendor input: `HOLD`; compile errors: `HOLD` with original diagnostics; fail closed on changed source identity.
- **Only six actual Cargo stages PASS + exact input closure + unchanged digest may emit `PASS_AOF_R1_CF1_NATIVE_COMPILE_CLOSURE`.**
- SOURCE/STATIC checks do not promote to COMPILE; do not run or claim GPU evidence here.

## Negative gates
```text
completion-api-inaccessible -> FAIL
duplicated queue completion authority -> FAIL
exact path input missing -> HOLD
crate/binary compile failure -> HOLD
parent numerical or commit semantics drift -> FAIL
unrun cargo stages -> NOT_RUN, never PASS
```

## Exit condition
Native target compilation succeeds against the exact workspace graph, with numerical and physical behavior unchanged. No production or performance promotion.
