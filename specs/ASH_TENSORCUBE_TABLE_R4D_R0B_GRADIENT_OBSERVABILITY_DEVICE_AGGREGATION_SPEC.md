# TENSORCUBE-TABLE-R4D-R0B

## GRADIENT OBSERVABILITY DEVICE AGGREGATION

```text
TENSORCUBE-TABLE-R4D-R0B

GRADIENT OBSERVABILITY DEVICE AGGREGATION

+ R0A PIPELINE RESIDENCY PRESERVATION
+ DEVICE-RESIDENT PER-OBSERVATION SLOT LEDGER
+ R27 EXACT DEVICE RESULT RETENTION
+ R2D EXACT SUM-SQUARE RESULT RETENTION
+ STEP-BARRIER COMPACT READBACK
+ NONFINITE / NONZERO / MAX-ABS / SUM-SQUARE PRESERVATION
+ FIRST-FAILURE SLOT / LABEL IDENTITY
+ STEP-BARRIER-OBSERVABLE CLASSIFICATION
+ PER-GRADIENT HOST READBACK ELIMINATION
+ PER-GRADIENT POLL-WAIT ELIMINATION
+ GENERATION / OPTIMIZER-STEP BINDING
+ COVERAGE / DUPLICATE FAIL-CLOSED SEAL
+ OBSERVE PARENT-PARITY QUALIFICATION
+ NO RAW GRADIENT D2H
+ NO NEW GRADIENT-MATH WGSL
+ NO THRESHOLD RELAXATION
```

## 1. Purpose

R0B removes the CPU synchronization point attached to each migrated R27/R2D gradient observation while preserving the exact parent reduction math and R0A persistent pipelines.

Parent:

```text
TENSORCUBE-TABLE-R4D-R0A
HOT-PATH PIPELINE RESIDENCY
```

Parent hot path:

```text
gradient -> R27/R2D device reduction -> tiny map/readback -> Poll(Wait) -> host receipt
```

R0B ACTIVE:

```text
gradient 0 -> exact device result slot -\
gradient 1 -> exact device result slot --+-> retained device slots
gradient N -> exact device result slot -/
                                      |
                                      v
                            optimizer-step barrier
                                      |
                                      v
                         one compact copy/map/wait
                                      |
                                      v
                           host receipt materialization
```

The evidence transport changes. The numerical evidence does not.

## 2. Implementation Resolution

R0B intentionally does **not** add new gradient-aggregation WGSL. Existing exact outputs remain authoritative:

```text
R27 result       20 bytes
R2D sum-square   4 bytes optional
slot ceiling     24 bytes
```

Constants:

```text
R4D_R0B_MAX_OBSERVATIONS_PER_STEP = 16,384
R4D_R0B_COMPACT_SLOT_BYTES        = 24
maximum compact barrier bytes     = 393,216
```

The target optimization is per-gradient host synchronization cardinality, not compact evidence byte count.

## 3. Runtime Mode

```text
ASH_TENSORCUBE_TABLE_R4D_R0B_MODE
```

Accepted:

```text
OFF / DISABLED / 0
OBSERVE / OBSERVE_ONLY
ACTIVE / ACTIVE_VERIFIED / 1
```

Default is `OFF`.

- `OFF`: parent immediate observations remain authoritative.
- `OBSERVE`: new device slots and parent immediate observations both execute; barrier parity must be exact. Not a performance fixture.
- `ACTIVE`: migrated R27/R2D observations use retained device slots only; receipts are materialized after the step barrier.

R0B requires R0A. Enabling R0B without R0A fails closed with `R4D_R0B_REQUIRES_R4D_R0A_PIPELINE_RESIDENCY`.

## 4. Backend Pending APIs

R27 adds:

```text
R27R1PendingGradientObservation
enqueue_r27r1_gradient_surface_with_pipeline_runtime(...)
```

R2D adds:

```text
R2DPendingGradientSumSquares
enqueue_r2d_gradient_sum_squares_with_pipeline_runtime(...)
```

The enqueue paths preserve parent R27/R2D dispatch/reduction math and return device buffers without `map_async`, `get_mapped_range`, or `device.poll`.

Legacy immediate wrappers remain for OFF/OBSERVE compatibility and isolated tests.

## 5. Observation Classification

R0B represents:

```text
ImmediateSafetyCritical
StepBarrierObservable
```

All observations migrated by this bake are explicitly `StepBarrierObservable`.

Other safety/status readbacks are not silently migrated. Forward finite guards, R14/R15/G204D status, AdamW status, durability readbacks remain out of scope.

## 6. Step / Coverage Authority

Each active R0B step binds:

```text
source_generation
target_generation = source_generation + 1
source_optimizer_step
target_optimizer_step = source_optimizer_step + 1
```

Capacity is fail-closed at 16,384 slots. Duplicate slot identity is fail-closed.

Terminal coverage requires:

```text
expected_gradient_count == observed_gradient_count
expected_element_count  == observed_element_count
duplicate_gradient_count = 0
coverage_gap_count        = 0
```

The expected/observed gradient count is the canonical migrated **observation-slot** set for the R6 wave-resident path. R0B does not claim a separate model-wide gradient manifest.

## 7. ACTIVE Deferred Receipt Materialization

ACTIVE does not fabricate final gradient stats before readback. Backward carries structural element coverage plus R0B slot IDs. After the single barrier, exact device results restore and reseal:

```text
nonzero element count
max_abs
sum_sq
L2 norm
logical gradient receipt digest
layer parameter-gradient role count
input-adjoint nonzero/max_abs/nonfinite
layer receipt digest
```

Final backward summaries are computed only after materialization.

## 8. Canonical Wave Ordering

```text
begin R0B step
forward/backward observations queued
R6 accumulator end-wave
R6 accumulator finalize
final accumulated gradients queued into same ledger
ONE r4d_r0b_seal_step(...)
materialize lane receipts
materialize accumulated-gradient receipt
compute final backward receipt digests/summaries
```

One barrier covers migrated per-gradient observations and final accumulated-gradient observations.

## 9. Single Barrier Readback

At seal, one buffer of `slot_count * 24` bytes is allocated. One encoder copies R27 20-byte results and optional R2D 4-byte results into that buffer, followed by one canonical source-level sequence:

```text
queue.submit
map_async
PollType::Wait
get_mapped_range
```

R0B does **not** claim to remove existing R27/R2D GPU dispatches or submissions. It removes migrated host readback/wait transactions.

## 10. Exact Result / First Failure

R27 preserves:

```text
positive_count
negative_count
zero_count
nonfinite_count
max_abs
```

and requires:

```text
positive + negative + zero + nonfinite == element_count
```

R2D sum-square must remain finite.

The first parsed nonfinite result is retained as bounded identity:

```text
slot:<slot>:label:<canonical observation label>
```

No raw-gradient D2H is needed for failure attribution.

## 11. OBSERVE Parity / ACTIVE Gates

OBSERVE compares retained device-slot results against the parent immediate R27/R2D results and fails with `FAIL_R4D_R0B_OBSERVE_PARITY` on drift.

ACTIVE requires:

```text
device_ledger_update_count > 0
coverage exact
per_gradient_readback_count = 0
per_gradient_blocking_wait_count = 0
step_barrier_readback_count == step_seal_count == step_begin_count
raw_gradient_d2h_bytes = 0
nonfinite_count = 0
```

No finite/nonzero/norm/clipping/optimizer threshold is relaxed.

## 12. Raw Gradient / Math Preservation

Forbidden:

```text
full gradient tensor D2H
host Vec<f32> gradient materialization
new gradient arithmetic WGSL
new tolerance relaxation
```

WGSL source graph remains byte-identical to R0A parent.

## 13. Parent Bug Repair

One R6A-R2 output-backward callsite in `atlas_runtime_real_loss_backward.rs` used obsolete `device, queue` arguments. R0B repairs it to the canonical route-context invocation. This is a compile-shape repair only; gradient math is unchanged.

## 14. Terminal Receipt

```text
tensorcube_table_r4d_r0b_gradient_observability_device_aggregation_receipt.json
[ASH-TENSORCUBE-TABLE-R4D-R0B][gradient-observability-device-aggregation]
PASS_TENSORCUBE_TABLE_R4D_R0B_GRADIENT_OBSERVABILITY_DEVICE_AGGREGATION
HOLD_TENSORCUBE_TABLE_R4D_R0B_PHYSICAL_PERFORMANCE_UNVERIFIED
```

Receipt includes step/coverage counts, nonfinite/nonzero/max_abs/sum_sq, per-gradient readback/wait counts, step-barrier readback counts/bytes, raw gradient D2H, OBSERVE parity failures, first-failure identity, and migrated observation class.

## 15. Explicit Non-Goals

R0B does not change:

```text
forward finite-guard readbacks
R14/R15/G204D non-gradient readbacks
AdamW per-segment status readback
weight H2D residency
resident SHA/finite validation scans
durable projection host copies
filesystem durability barriers
```

## 16. Actual Code Delta

```text
MOD 8
ADD 2
DEL 0
```

Modified:

```text
crates/base_train/src/atlas_runtime_real_loss_backward.rs
crates/base_train/src/lib.rs
crates/base_train/src/packed_runtime_native_bootstrap_accumulation_wave_residency.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/tensorcube_table_r4d_r0a_hot_path_pipeline_residency.rs
crates/burn_webgpu_backend/src/base_train_r27r1_gradient_observability.rs
crates/burn_webgpu_backend/src/base_train_r2d_gradient_stream.rs
tools/validate_ash_tensorcube_table_r4d_r0a_hot_path_pipeline_residency_static.py
```

Added:

```text
crates/base_train/src/tensorcube_table_r4d_r0b_gradient_observability_device_aggregation.rs
tools/validate_ash_tensorcube_table_r4d_r0b_gradient_observability_device_aggregation_static.py
```

## 17. Build Graph Preservation

```text
Cargo.toml byte-identical
Cargo.lock byte-identical
WGSL parent files = 320
WGSL changed = 0
```

## 18. Static Acceptance

```text
PASS_TENSORCUBE_TABLE_R4D_R0B_GRADIENT_OBSERVABILITY_DEVICE_AGGREGATION_STATIC checks=178
PASS_TENSORCUBE_TABLE_R4D_R0A_HOT_PATH_PIPELINE_RESIDENCY_STATIC checks=104
PASS_TENSORCUBE_TABLE_R4C_CF6_DIRECT_BOUNDED_WEIGHT_UPLOAD_STATIC checks=135
PASS_TENSORCUBE_TABLE_R4C_CF5_HOST_COPY_COLLAPSE_STATIC checks=127
PASS_TENSORCUBE_TABLE_R4C_CF4_HOST_DEVICE_IO_ROUNDTRIP_ATTRIBUTION_STATIC checks=67
PASS_TENSORCUBE_TABLE_R4C_CF3_SLOT_LIFECYCLE_STATIC checks=77
PASS_TENSORCUBE_TABLE_R4B_CF3_FULL_ROUTE_HOST_LEDGER_COMPACTION_STATIC checks=127
PASS_TENSORCUBE_TABLE_R1_CF1_IMMUTABLE_BYTE_ACCOUNTING_STATIC
PASS_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF1_STATIC checks=63
PASS_EVE_MCU_R3H_CF11_PAGED_COW_CANDIDATE_WEIGHT_SUCCESSOR_STATIC checks=64
```

## 19. Evidence State

Bake environment has no Rust toolchain.

```text
SOURCE       BAKED
STATIC       PASS
COMPILE      UNVERIFIED IN BAKE ENVIRONMENT
RUNTIME      UNVERIFIED AFTER R0B
PHYSICAL     UNVERIFIED AFTER R0B
PERFORMANCE  UNVERIFIED
```

No compile or speedup claim is made from static evidence.

## 20. Artifact Seals

```text
Overlay code-only ZIP
SHA-256 be27d9f6fa407a75bfa568a9835e34d2ca7fedd0eb50c1e4b6fd6beb0e82e7cc
files=10
CRC=PASS

Full code-only ZIP
SHA-256 499070eb5da24f8dd3f40a167c7116d28611561377246843c38bfe710762b8c7
files=8520
CRC=PASS
```

## 21. Local Compile Acceptance

```powershell
cargo check -p burn_webgpu_backend --lib --release --locked -j 1
cargo check -p base_train --lib --release --locked -j 1
cargo build -p base_train --bin base_train --release --locked -j 1
```

Compile PASS must not be inferred before these execute successfully.

## 22. Runtime Qualification Order

First:

```text
ASH_TENSORCUBE_TABLE_R4D_R0A_MODE=ACTIVE
ASH_TENSORCUBE_TABLE_R4D_R0B_MODE=OBSERVE
```

Require parent/device parity, exact coverage, and exact generation/step identity.

Then:

```text
ASH_TENSORCUBE_TABLE_R4D_R0A_MODE=ACTIVE
ASH_TENSORCUBE_TABLE_R4D_R0B_MODE=ACTIVE
```

ACTIVE must demonstrate migrated per-gradient readback/wait counts zero, one bounded readback per opened step, raw gradient D2H zero, exact coverage, and no B06/CF11 regression.

## 23. Performance Claim Boundary

Same-source A/B is:

```text
R0A parent
vs
R0A + R0B ACTIVE
```

Measure map/poll counts, compact readback transactions/bytes, CPU process time, backward wall time, optimizer-step wall time, and generation wall time.

R0B claims no exact speedup before physical A/B.

## 24. Successor

After compile + OBSERVE parity + ACTIVE physical closure:

```text
TENSORCUBE-TABLE-R4C-CF7
PARTIAL VRAM HOT-WEIGHT FORWARD / BACKWARD REUSE
```

## 25. Final Law

> **R0B does not weaken gradient observability. It changes when exact device evidence crosses the host boundary.**

> **The existing R27 and R2D reductions remain the numerical authority. Their compact device results remain resident across the step and are read once at the semantic barrier.**

> **Per-gradient map/poll synchronization is removed for the migrated R6 wave-resident production path; raw gradients never become host payload.**
