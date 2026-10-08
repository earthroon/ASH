# AOF-R1-CF4
## PREFIX COMMIT TRANSFER ATTRIBUTION

**Patch ID:** `AOF-R1-CF4`  
**Parent:** `AOF-R1-CF3`  
**Successor:** `AOF-R1-CF5 BLOCK PREFIX COMMIT / KV CAPACITY AUTHORITY`  
**Class:** native commit cost attribution only; not a KV storage rewrite or a speedup/promotion claim.

## Scope

```text
+ CF1 / CF2 / VH6 / CF3 semantic preservation
+ canonical stage_kv allocation requests + f32 logical byte count
+ old KV prefix copy / accepted suffix append exact extent split
+ actual queue.submit & actual prefix compute-dispatch count
+ existing read_observation MAP_READ/copy submission attribution
+ existing on_submitted_work_done callback observation + poll count
+ CPU wall around allocation / Queue submission / callback wait / validation / publication
+ per-commit physical-attempt outcome and compact session/depth/length aggregation
+ failed commit attempts preserved in GenerationTelemetry / ArkGenerationFailure
+ same model/tokenizer/owner real native commit-stability campaign reuse
+ new CF4 physical receipt, HOLD when measured negative coverage missing
+ no fabricated GPU timestamp, device/PCIe bus bytes, VRAM reserved bytes or speedup
+ no new queue submission, map_async, D2H, H2D, callback or exact-wait
+ no canonical KV, token, EOS, cancel, emit or FuturePool change
```

## Exact implementation ownership

**New files:**
- `crates/burn_webgpu_backend/src/aof_r1_commit_trace.rs`: thread-local per-attempt trace, overflow witness, phase machine, real submission/callback/poll/readback accounting.
- `crates/model_core/src/aof_r1_cf4_transfer_attribution.rs`: per-attempt outcome/bytes/duration and checked fail-closed aggregation, `UNKNOWN` physical fields and unit tests.
- `crates/orchestrator_local/src/aof_r1_cf4_attribution_cli.rs`: `--cf4-attribution` wraps the *existing* full physical commit-stability runner, consumes freshly produced case files, generates aggregate receipt; no synthetic model/GPU path.
- `tools/validate_ash_aof_r1_cf4_prefix_commit_transfer_static.py`: exact callsite/source, hash, invariant and trained checkpoint digest gates.

**Modified files:**
- `crates/burn_webgpu_backend/src/{aof_r1_verification.rs,lib.rs}`
- `crates/model_core/src/{aof_r1_prefix_commit.rs,decode_state.rs,generation_sampling.rs,generation_telemetry.rs,lib.rs}`
- `crates/orchestrator_local/src/{aof_r1_commit_stability_cli.rs,bin/ash_aof_r1_cf7_cf8_cf9_gate.rs}`

## Real trace boundaries and formula

The existing `stage_prefix_append` WGSL copies two packed f32 matrices (key/value) over the old logical prefix `[0,past)`, and writes one new accepted suffix token at `past`. For one layer:

```text
old-prefix logical bytes = 2 * kv_heads * head_width * past * 4
suffix-append logical bytes = 2 * kv_heads * head_width * 4
next K/V staging logical bytes = 2 * kv_heads * head_width * (past + 1) * 4
```

These are **logical element extents**, not physical GPU bandwidth, DMA, or committed VRAM bytes. Count both K/V within the same actual compute dispatch, not two imagined submissions. Preserve f32 and exact WGSL ranges.

Within the current backend `dispatch`, one real `queue.submit` is followed by the original `wait_for_queue`. Existing `read_observation` has a *second, separate* real queue submission and its own `map_async` polling. Count both when they happen inside the scoped commit, separately tagging readback logical bytes and map polls. The outer `complete_publication` adds a completion callback without a new explicit queue submission. Callback observations are measured after actual bound-queue completion.

The commit scope is thread-local, RAII-cleaned and starts before verified-token selection; it never registers a new GPU callback or issues its own GPU operation. A missing trace after publication marks counter evidence incomplete, **not** a new fallible canonical commit. Counter overflow or inconsistent extents fails attribution.

## Publication / failure preservation

```text
existing selection
  -> stage_kv tensor request and WGSL full-prefix dispatch
  -> existing Queue completion + error-scope validation
  -> existing currentness, structure, admission, cancel checks
  -> state.kv = next
  -> canonical token / receipt publication
```

The single canonical `state.kv = next` point and all original guards remain authoritative. Every invoked attempt, including early stale/cancel/partial-layer failures, appends one bounded per-commit observation. Generation error carries an identical observation vector so the error path is not lost. Do not classify a failed pre-submit attempt as a physical transfer.

**Outcomes:** `Published`, `RejectedBeforeStaging`, `FailedDuringStaging`, `FailedDuringCompletion`, `RejectedBeforePublication`, `IncompletePublication`. No new canonical result enum is introduced.

## Native qualifier / output

CLI target is the existing `ash_aof_r1_cf7_cf8_cf9_gate` under its manifest-declared audit feature.

```powershell
cargo run -p orchestrator_local --bin ash_aof_r1_cf7_cf8_cf9_gate --release --locked --features orchestrator_aof_r1_audit_bins -- `
  --cf4-attribution .\COMMIT_STABILITY_INPUT.json --out .\CF4_NEW_OUTPUT_DIR
```

The provided input must satisfy the **original** `CommitStabilityInput` (two real trained ranks, D1/D2/D4, actual EOS/Stop/Max token cases, real model/tokenizer/checkpoint inputs). The wrapper invokes the existing physical runner once, reads its newly emitted `case_*.json` and aggregates actual candidate-leg `aof_r1_cf4_observations`. It does not re-read GPU buffers or execute an invented smoke model.

Receipt: `aof_r1_cf4_prefix_commit_transfer_attribution_receipt.json`.

Contains per-case outcomes; exact session, round, prefix index, depth, lengths; allocation requests/logical bytes; prefix/suffix logical elements/bytes; actual Queue submission/callback/poll/readback counts; host wall segments; coverage classification; and `gpu_copy_execution_ns = null`, `physical_bus_transfer_bytes = null`, `actual_allocator_reserved_bytes = null`, `performance_promotion = false`, `production_admission = false`, `promoted = false`.

The wrapper requires at least one successfully published actual prefix dispatch and at least one observed rejected attempt to issue a physical-attribution PASS; otherwise it writes an explicit `HOLD_INCOMPLETE_COVERAGE` receipt and returns an error. The wrapper itself does not assert complete quality/promotion/throughput qualification. If a required negative is not exported by the current campaign, retain HOLD rather than fabricating the missing arm.

## Acceptance hierarchy

**SOURCE:** canonical logic exists and the new trace is connected to real sites.  
**STATIC:** callsite/bytes/unchanged WGSL/training digest/negative gates pass.  
**COMPILE:** `cargo metadata`, backend/model_core release check, orchestrator native audit binary compile.  
**RUNTIME:** Rust trace tests and semantic commit matrix.  
**PHYSICAL:** actual NativeWGPU campaign including at least one successful and one rejected commit; valid live Queue submission/completion; OFF/ON token, text, stop and canonical KV parity.  
**PERFORMANCE:** measured separately in a later controlled A/B. `UNKNOWN` until then.

Do not promote from any lower evidence layer to a higher one.

## Actual source bake / evidence as of 2026-10-08

- Parent CF3 code-only ZIP SHA-256: `52eb9126da1b35787cdd7ed8e1435d1c749a0bc7dea4a48855a53fd5b693fa01`.
- Full CF4 ZIP SHA-256: `0b0904f845755d96b96f7a7da4605d1ae6da82bbf88ae93ef311b46c9434a231` (**8,719 files**, CRC PASS).
- CF4 overlay SHA-256: `95d739695abb83cc129faa2cc94a1c56eed4b42df646185ff2b326bf1287609f` (**4 ADD, 9 MOD, 0 DEL**, CRC PASS).
- CF4 source/static: **65/65 PASS**.
- Parent CF3 static: **51/51 PASS**.
- Legacy CF1/CF2/VH6 static: **51/52**, with exactly `PARENT_PRESERVED:crates/model_core/src/aof_r1_prefix_commit.rs` failing because CF4 intentionally instruments that file. The old hash is *not* rewritten or a parent 52/52 claimed. This is an explicit narrow byte-preservation supersession, guarded by the CF4 semantic/ordering source gates.
- Training checkpoint source digest, 19 hashed files: `e20f93b19bcb8a93a96809a28d2faf5c72c68896da060002d36a43e2286b8283`, byte-preserved.
- Negative source mutations individually rejected: fabricated GPU duration, omitted queue-submit observation, damaged prefix copy formula, drifted WGSL prefix range. Originals restored and final static rerun PASS.
- Rust Cargo/rustc tools **not installed** in the build container. Exact external sherpa-rs workspace path **not provided** in the code-only ZIP. **COMPILE/RUNTIME/PHYSICAL: NOT_RUN; PERFORMANCE: NOT_MEASURED; no CF4 physical PASS.**

## Required next execution (Windows, exact workspace)

```powershell
cargo metadata --format-version 1 --locked
cargo check -p burn_webgpu_backend --lib --release --locked -j 1
cargo check -p model_core --lib --release --locked -j 1
cargo check -p base_train --lib --release --locked -j 1
cargo check -p orchestrator_local --bin ash_aof_r1_cf7_cf8_cf9_gate --features orchestrator_aof_r1_audit_bins --release --locked -j 1
cargo test -p burn_webgpu_backend --lib cf4_scope --release --locked -j 1
cargo test -p model_core --lib cf4_ --release --locked -j 1
python tools/validate_ash_aof_r1_cf4_prefix_commit_transfer_static.py
```

Then execute the existing real `commit_stability` campaign through `--cf4-attribution`, inspect all case receipts, and compare against same-source OFF control. Unsupported accepted-length 8 combinations are `NOT_APPLICABLE`, not manufactured results. Physical GPU kernel duration and VRAM occupancy require independent instrumentation; host waiting does not prove either.

## Completion law

```text
CANONICAL COMMIT SOURCE UNCHANGED IN BEHAVIOR
+ LOGICAL PREFIX/SUFFIX BYTES GROUNDED IN REAL WGSL CALLS
+ EXISTING QUEUE / CALLBACK / MAP OPERATIONS ACCOUNTED HONESTLY
+ SUCCESSES AND FAILURES RECORDED
+ NO NEW GPU ROUNDTRIP
+ SOURCE / STATIC / COMPILE / RUNTIME / PHYSICAL PASS
= PASS_AOF_R1_CF4_PREFIX_COMMIT_TRANSFER_ATTRIBUTION
```

The source bake alone does **not** satisfy this completion law. CF5 remains blocked until the physical cost classification is supported.