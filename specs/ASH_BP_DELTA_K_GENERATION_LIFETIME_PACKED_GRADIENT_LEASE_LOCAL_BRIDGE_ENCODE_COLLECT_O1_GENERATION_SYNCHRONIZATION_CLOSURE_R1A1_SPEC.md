# ASH-BP-DELTA-K-GENERATION-LIFETIME-PACKED-GRADIENT-LEASE-LOCAL-BRIDGE-ENCODE-COLLECT-SPLIT-O1-GENERATION-SYNCHRONIZATION-CLOSURE-R1A1

## 0. Revision

```text
Patch ID:
ASH-BP-DELTA-K
-GENERATION-LIFETIME-PACKED-GRADIENT-LEASE
-LOCAL-BRIDGE-ENCODE-COLLECT-SPLIT
-O1-GENERATION-SYNCHRONIZATION-CLOSURE
-R1A1

Short name:
DK-PERF-R1A1
```

Status at this source bake:

```text
R1 parent compile                                      = REPORTED PASS
R1A source materialization                             = PRESENT
R1A1 generation synchronization coordinator            = MATERIALIZED / ACTIVE
R1A1 bounded packed-gradient generation authority      = MATERIALIZED / ACTIVE
R1A1 Local generation slice ledger                     = MATERIALIZED / ACTIVE
R1A1 Bridge generation slice ledger                    = MATERIALIZED / ACTIVE
R1A1 physical receipt authority                        = MATERIALIZED
R1A1 all-gradient generation-wide physical residency   = EXPLICITLY REJECTED
R1A1 Local backend encode/collect physical split       = HOLD
R1A1 Bridge backend encode/collect physical split      = HOLD
R1A1 post parameter exact-wait retirement              = HOLD
R1A1 O(1) physical generation synchronization          = HOLD
R1A1 Disabled true outer zero-cost bypass              = HOLD
R1A1 post-bake Rust compile                            = NOT CLAIMED BY BAKE ENVIRONMENT
```

Static source token:

```text
PASS_ASH_BP_DELTA_K_GENERATION_LIFETIME_PACKED_GRADIENT_LEASE_LOCAL_BRIDGE_ENCODE_COLLECT_O1_GENERATION_SYNC_R1A1_STATIC
```

Physical HOLD:

```text
HOLD_ASH_BP_DELTA_K_GENERATION_LIFETIME_PACKED_GRADIENT_LEASE_LOCAL_BRIDGE_ENCODE_COLLECT_O1_GENERATION_SYNC_R1A1_PENDING
```

Reserved physical PASS:

```text
PASS_ASH_BP_DELTA_K_GENERATION_LIFETIME_PACKED_GRADIENT_LEASE_LOCAL_BRIDGE_ENCODE_COLLECT_O1_GENERATION_SYNC_R1A1
```

## 1. Direct parent

Direct parent source artifact:

```text
ASH_PASS3_DK_PERF_R1A_GENERATION_EPOCH_STATIC_SOURCE_BAKE_CODE_ONLY.zip
SHA-256 = 98b2d2fc93c0ca05876245153735118c9948cdfe2b4ce2b8724b3d86978b2933
entries = 8,423
```

R1A already materialized generation-scoped pre/post evidence authority, batched evidence capacity authority, post Delta-K busy-spin/yield retirement, resident weight direct-source adoption, persistent post runtime, hotpath full-payload SHA retirement mode, and Local EMA generation transaction.

R1A1 is the physical synchronization/lifetime successor.

## 2. Mathematical non-goal

R1A1 SHALL NOT change Delta-K = I * M^2, local I/M, bridge flattened 256D gradient cosine, bridge information/material/Delta-K, fusion/fission thresholds, confirmation generations, cooldown, greedy pair ordering, Muon 16x16/16x32/32x16 geometry, Newton-Schulz, same-source counterfactual mathematics, or objective-probe mathematics.

R1A1 is a resource/synchronization revision only.

## 3. Source-level constraint discovered during bake

The initial R1A1 design could be misread as retaining every parameter-sized packed-gradient buffer until generation end. That interpretation is prohibited. For a ~1.1B-class model, simultaneously retaining every packed-gradient duplicate can require several additional GB of VRAM and conflict with the RTX 3080-class bounded-memory target.

Therefore generation-lifetime authority does not mean unbounded generation-wide physical residency. The generation owns lease identity, ordering, consumer-set semantics, and retirement policy. Physical packed-gradient allocations are held in bounded windows constrained by the existing MCU R7A arena budget.

## 4. No duplicate-gradient law

R1A1 SHALL NOT obtain batching by creating a second generation-wide copy of all gradients, nor by separately repacking Local, Bridge, and Muon copies. The intended final structure remains one canonical packed producer per physical window entry with Local, Bridge, and Muon consumers using the existing R7A1 exact multi-consumer submission leases.

## 5. Generation packed-gradient bounded-window authority

Added:

```text
crates/base_train/src/generation_lifetime_packed_gradient_lease_r1a1.rs
```

`GenerationPackedGradientLeaseSetR1A1` owns the active optimizer generation, bounded live packed-gradient window, canonical parameter identity set, R7A1 packed-gradient runtimes while live, physical arena domain, producer/consumer retirement receipts, live-byte accounting, peak-byte accounting, and generation commit/abort lineage.

State is `Idle -> Collecting -> WindowOpen -> Finalizing -> Collecting ... -> Idle`. `Poisoned` is reserved for lifecycle failure.

## 6. First physical window is intentionally size one

The initial static cutover constructs the coordinator with `max_live_packed_gradient_bytes = 0`. In this authority zero means one live packed-gradient entry is permitted and no second entry may be admitted before current-window reclaim.

This preserves the parent's packed-gradient VRAM peak while moving producer/reclaim authority under the generation coordinator. It does not claim performance batching yet.

## 7. Active R7A1 reclaim cutover

For Delta-K ObserveOnly/Active modes with R7A1 arena-backed packed gradients, parameter-end reclaim now routes through:

```text
ProductionBpDkRuntimeR8
    -> BpDeltaKGenerationSynchronizationCoordinatorR1A1
    -> GenerationPackedGradientLeaseSetR1A1
    -> adopt_runtime(...)
    -> reclaim_window()
```

rather than directly invoking `McuPackedGradientRuntimeR7A1::seal_and_reclaim` from the parameter owner.

Disabled mode retains legacy direct reclaim until the final Disabled outer bypass is cut over. This establishes one generation-scoped reclaim authority without increasing the live physical window.

## 8. Existing R7A1 authority remains canonical

R1A1 reuses `McuPackedGradientRuntimeR7A1`, `PackedGradientProducerOutputR7A1`, `PackedGradientReadBindingR7A1`, `PackedGradientConsumerSubmissionReceiptR7A1`, exact tracked submission lease identity, R7A arena incarnation identity, and `verify_and_reclaim_packed_gradient_multi_consumer_r7a1`. No second lease system is introduced.

## 9. Generation identity and duplicate producer protection

The bounded generation authority rejects generation drift, canonical parameter duplicate producer adoption, parameter identity mismatch, window budget overflow, empty runtime identity, and zero logical packed-gradient byte size.

`seen_parameters` remains generation-scoped across physical window reclaim, so one parameter cannot silently create a second R1A1 packed-gradient producer in the same generation.

## 10. Generation synchronization coordinator

Added:

```text
crates/base_train/src/bp_delta_k_generation_sync_coordinator_r1a1.rs
```

`BpDeltaKGenerationSynchronizationCoordinatorR1A1` uses the SAME typed `BpDeltaKRuntimeModeR1` instance already owned by `BpDeltaKPersistentDeviceRuntimeR1`. The environment is not reparsed to create a second runtime-mode authority.

## 11. Coordinator state model

The typed state surface contains Idle, PackingGradients, EncodingLocal, LocalSubmitted, LocalCollected, EncodingBridge, BridgeSubmitted, BridgeCollected, Planned, MuonExecuting, EncodingPost, PostSubmitted, PostCollected, PendingGenerationCommit, Committed, Aborted, and Poisoned.

The current static integration opens the coordinator at the optimizer-generation boundary for observing modes and resolves it at generation commit/abort. The later encode/collect physical cutover will advance the intermediate states.

## 12. Generation commit/abort binding

`ProductionMuonRuntime` now resolves the R1A1 coordinator from the actual optimizer generation transaction. Commit resolves R1A1 Commit before existing Local pending commit; abort resolves R1A1 Abort before existing Local/Bridge/planner abort. R1A1 generation identity therefore cannot silently outlive the optimizer generation transaction.

## 13. Local encode/collect ledger authority

Added:

```text
crates/base_train/src/bp_delta_k_local_encode_collect_r1a1.rs
```

`BpDeltaKLocalEncodeCollectLedgerR1A1` and `BpDeltaKLocalEncodedSliceR1A1` record optimizer generation, canonical parameter index, tile begin/count, and evidence byte offset/length. The production callsite records slices in generation order using the existing 48-byte Local compact receipt ABI per tile.

## 14. Bridge encode/collect ledger authority

Added:

```text
crates/base_train/src/bp_delta_k_bridge_encode_collect_r1a1.rs
```

Bridge slices record optimizer generation, canonical parameter index, pair begin/count, and evidence byte offset/length using the existing 32-byte compact receipt ABI per pair. Bridge collection begins only after the Local ledger establishes the prerequisite phase.

## 15. Evidence ordering authority

Local/Bridge directories are ordered by canonical parameter index. Existing tile/pair ordering remains canonical. GPU completion order SHALL NOT become semantic ordering.

## 16. Current encode/collect physical truth

The new ledgers are active metadata/offset authorities, but backend physical observers are still monolithic. `bp_delta_k_local_observer.rs` still contains `wait_for_submission_exact(...)`, and `bp_delta_k_bridge_pair_observer.rs` still contains `wait_for_submission_exact(...)`.

Therefore Local and Bridge physical encode/collect split remain HOLD, and no O(1) synchronization claim is made by this static bake.

## 17. Post evidence truth

R1A already retired the Delta-K-specific busy-spin/yield loop. The current post path still uses `collect_parameter_after_exact_wait_r1a(...)`, which resolves one tracked submission per parameter.

Thus post busy-spin retirement is source-level PASS, while post per-parameter exact-wait retirement and generation-batch collection remain HOLD.

## 18. Next physical cutover must be source-direct or bounded-window

True O(1) generation synchronization cannot be honestly obtained by retaining every packed-gradient duplicate simultaneously on a 10 GB-class GPU.

Preferred design A is canonical-gradient direct observation: Local and Bridge read canonical device gradient segments directly, while Muon packs only when actual Muon execution requires packed layout. Fallback design B is a bounded multi-parameter packed window: pack K gradients, Local batch K, Bridge batch K, Muon K, then retire the window.

The final R1A1 physical promotion should prefer design A when the canonical gradient ABI can support exact segmented observation without changing mathematics.

## 19. O(1) definition retained

Final R1A1 still requires Local parameter waits = 0, Bridge parameter waits = 0, Post parameter waits = 0, and bounded generation-level visibility barriers independent of parameter count. The static bake does not reinterpret O(1) to hide remaining waits.

## 20. Disabled zero-cost target retained

Final Disabled mode requires zero incremental Delta-K runtime construction, Local/Bridge/Post dispatch, submit, wait, map, H2D/D2H, graph construction, planner calls, and hotpath full-payload SHA. The outer observation call graph is not yet physically bypassed, so Disabled zero-cost remains HOLD.

## 21. Gradient transport law

Final physical qualification requires `gradient_host_materialization_count = 0`, `gradient_full_h2d_bytes = 0`, and `gradient_duplicate_device_copy_bytes = 0` for the canonical device-resident source. The initial bounded-window authority introduces no new full-gradient copy.

## 22. Weight transport law

Inherited from R1: canonical Delta-K full weight H2D = 0. The resident weight source is untouched.

## 23. Hotpath digest law

Inherited from R1: normal hotpath full-payload SHA count = 0. R1A1 does not regress digest authority separation.

## 24. Pipeline lifetime law

Inherited from R1: steady-state Delta-K shader, BGL, pipeline-layout, and compute-pipeline build counts are zero. The R1A1 files introduce no GPU pipeline owner.

## 25. Physical receipt authority

Added:

```text
crates/base_train/src/bp_delta_k_perf_r1a1_physical_receipt.rs
```

The receipt covers runtime mode, optimizer generation, parameter/tile/pair counts, packed-gradient producer/consumer counts, lease reuse/stale acceptance, gradient H2D/host materialization/duplicate copy, Local/Bridge/Post submits, parameter waits, generation waits, map counts, poll-yield count, steady-state pipeline build count, hotpath full-payload SHA count, semantic parity, topology parity, generation transaction continuity, and physical claim/pass token.

`DK_PERF_R1A1_PHYSICAL_QUALIFIED_AT_BAKE = false`.

## 26. Physical PASS requirements

Final physical PASS requires semantic parity, topology decision parity, generation transaction continuity, zero consumer-lease reuse/stale acceptance, zero gradient host materialization/H2D/duplicate copy on the canonical path, zero Local/Bridge/Post parameter waits, zero poll-yield, Local/Bridge/Post generation waits <= 1, zero steady-state pipeline builds, and zero hotpath full-payload SHA.

The initial static bake does not satisfy the wait-count requirements yet.

## 27. Semantic parity remains mandatory

R1A1 may not change Local I/M/Delta-K, Bridge cosine/I/M/Delta-K, candidate graph/order, selected pair set, Right/Down orientation, fusion/fission decision, confirmation streak, or cooldown state. A faster result with different topology is a failed R1A1 implementation.

## 28. Generation abort law

Abort must leave Local temporal history, Bridge temporal history, and planner history at the previous committed generation. R1A1 synchronization metadata and any live packed-gradient window must retire without becoming successor-generation authority.

## 29. Static source delta

Relative to the direct R1A parent:

```text
ADD 5
MOD 2
DEL 0
```

Added:

```text
crates/base_train/src/generation_lifetime_packed_gradient_lease_r1a1.rs
crates/base_train/src/bp_delta_k_local_encode_collect_r1a1.rs
crates/base_train/src/bp_delta_k_bridge_encode_collect_r1a1.rs
crates/base_train/src/bp_delta_k_generation_sync_coordinator_r1a1.rs
crates/base_train/src/bp_delta_k_perf_r1a1_physical_receipt.rs
```

Modified:

```text
crates/base_train/src/lib.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
```

No Burn/CubeCL/WGPU generation file, TensorCube shader, Delta-K shader, fusion threshold, or Muon mathematics file was modified.

## 30. Code artifacts

Full code-only artifact:

```text
ASH_PASS3_DK_PERF_R1A1_GENERATION_PACKED_GRADIENT_STATIC_SOURCE_BAKE_CODE_ONLY.zip
SHA-256 = d16747b8d47ecb9e29ee02359f1ef93df4e892afd52bbeca5697b9f88513712b
entries = 8,428
```

Overlay artifact:

```text
ASH_PASS3_DK_PERF_R1A1_GENERATION_PACKED_GRADIENT_STATIC_SOURCE_BAKE_OVERLAY.zip
SHA-256 = 7f869a00dfba3802ff193907f96a4309f7202ade8856dacb85ee84d76bfcec93
entries = 7
```

Applying the overlay to the direct R1A parent reproduces the full 8,428-file tree byte-for-byte. No target/cache/bytecode entries are included.

## 31. Compile truth

The artifact construction environment has no Cargo/Rustc, so post-bake compile PASS is not claimed.

First local gates:

```powershell
cargo check --locked -p burn_webgpu_backend --all-targets
cargo check --locked -p base_train --all-targets
```

Compiler results override static source assumptions.

## 32. Static bake claim

This bake may claim: generation coordinator materialized and production-bound; typed generation commit/abort binding; bounded packed-gradient generation authority; R7A1 reclaim routed through generation authority for observing modes; window=1 VRAM-neutral cutover; Local/Bridge generation evidence slice directories materialized and production-recorded; physical receipt authority; no gradient duplication; and R1/R1A math/transport laws preserved.

It SHALL NOT claim: Local/Bridge backend encode/collect split complete, post generation batch complete, O(1) synchronization complete, Disabled zero-cost complete, physical semantic parity PASS, or physical performance PASS.

## 33. Next physical slice

After compile PASS, preferred next slice is:

```text
DK-PERF-R1A1-R2
Canonical Gradient Segmented Direct Observation
+ Local Generation Batch
+ Bridge Generation Batch
+ Parameter-Wait Retirement
```

if exact direct segmented observer binding is practical. The fallback is a bounded packed-gradient multi-parameter window with explicit VRAM and synchronization receipts. Neither may create a full-generation duplicate gradient store.

## 34. Final law

> Generation lifetime means one generation owns the packed-gradient lease protocol; it does not grant permission to pin every packed-gradient duplicate in VRAM simultaneously.

> Packed-gradient physical residency is bounded by the MCU arena budget.

> Existing R7A1 remains the single physical producer/consumer authority.

> Local and Bridge evidence are assigned generation-scoped compact offsets before backend submission ownership is migrated.

> The first R1A1 cut moves ownership without increasing VRAM peak.

> O(1) synchronization remains HOLD until Local, Bridge, and Post no longer own parameter-local waits.

> No performance claim may hide those waits, and no batching implementation may pay for synchronization reduction with a second full-gradient authority.
