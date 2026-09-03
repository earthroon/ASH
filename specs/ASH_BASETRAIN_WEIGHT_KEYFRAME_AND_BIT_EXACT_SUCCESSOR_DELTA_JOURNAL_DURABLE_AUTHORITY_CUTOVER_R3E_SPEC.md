# ASH-BASETRAIN-WEIGHT-KEYFRAME-AND-BIT-EXACT-SUCCESSOR-DELTA-JOURNAL-DURABLE-AUTHORITY-CUTOVER-R3E

## 0. Revision

```text
Patch ID:
ASH-BASETRAIN-WEIGHT-KEYFRAME
-AND-BIT-EXACT-SUCCESSOR-DELTA-JOURNAL
-DURABLE-AUTHORITY-CUTOVER-R3E

Short name:
ASH EVE R3E
WEIGHT KEYFRAME + BIT-EXACT SUCCESSOR JOURNAL

Status:
STATIC DURABLE AUTHORITY MATERIALIZATION RELEASE

Rust compile PASS: NOT CLAIMED
GPU physical PASS: NOT CLAIMED
Codec-selection physical campaign PASS: NOT CLAIMED
Crash/replay physical PASS: NOT CLAIMED
N8 PASS: NOT CLAIMED
```

```text
HOLD_ASH_WEIGHT_R3E_PHYSICAL_PENDING
```

## 1. Direct Parent

R3E inherits R3D:

```text
ASH-TRAINABLE-GENERATION-DURABLE-REFERENCE
-ADAM-RECOVERY-HEAD
-AND-ORDINARY-STEP-FULL-MV-PAYLOAD-RETIREMENT-R3D
```

R3D already removes ordinary full Adam M/V durable payload. R3E changes Weight durability only. Runtime Weight remains `ResidentWeightPack`; Eve/HiMuon/AdamW mathematics and R3C/R3C1 generation authority are unchanged.

## 2. Existing Shadow Parent

The source already contains `weight_successor_bit_exact_journal_shadow_r1.rs` with RAW/XOR/XOR+byte-shuffle/XOR+bitplane zstd measurements, bounded blocks, decode verification, byte/bit mismatch counters, source/target digests and keyframe-feasibility evidence.

Historical shadow truth remains immutable:

```text
shadow_authoritative = false
r6_weight_pack_retired = false
descriptor_binding_materialized = false
p3_participant_materialized = false
```

R3E introduces separate production authority rather than flipping shadow flags.

## 3. Central Invariant

Under admitted R3E, an ordinary non-keyframe generation does not create `candidate/weights.r6pack`.

Required ordinary target:

```text
full Weight payload files = 0
full Weight payload write bytes = 0
additional Weight GPU D2H bytes = 0
extra source full-pack read bytes = 0
extra target full-pack read bytes = 0
post-stream full target digest scans = 0
```

Durable Weight is represented by a periodic exact keyframe or an immediate-predecessor exact successor journal.

## 4. Materialized Production Modules

```text
weight_successor_bit_exact_codec_common_r3e.rs
weight_successor_durable_journal_r3e.rs
weight_keyframe_durable_r3e.rs
weight_durable_head_r3e.rs
weight_successor_replay_r3e.rs
trainable_generation_durability_descriptor_r3.rs
trainable_generation_weight_payload_retirement_r3e.rs
```

All are exported by `base_train::lib`.

## 5. Exact Codec Set

Production journal codecs:

```rust
WeightSuccessorCodecR3E {
    XorZstd,
    XorByteShuffleZstd,
    XorBitplaneZstd,
}
```

R3E contains no lossy INT8/INT4/BF16/F16 successor codec. A journal is an exact bit transition.

## 6. No Hard-Coded Winner

No `BEST_CODEC`, `SELECTED_CODEC`, or `DURABLE_CODEC` source constant chooses a winner by assumption.

Admission surface:

```text
--admit-weight-successor-journal-r3e
--weight-keyframe-interval-steps N
--weight-journal-codec-profile CODEC:LEVEL:PROFILE_ID
--weight-journal-codec-selection-receipt PATH
```

R3E defaults OFF and has no default production codec profile.

## 7. Physical Codec Selection Receipt

`WeightJournalCodecSelectionReceiptR3E` binds measured campaign identity, codec/profile, observed generations, actual delta bytes, timing, exact mismatch counters, campaign digest and `physicalQualified`.

Production selection requires:

```text
observed generations > 0
byte mismatch = 0
bit mismatch = 0
exact reconstruction = true
physicalQualified = true
profile identity exact
```

This static bake does not provide such a physical receipt, so physical R3E remains HOLD.

## 8. Bounded Codec Geometry

```text
maximum logical frame = 16 MiB
production scratch bound = 6 * frame bytes
```

Production scratch is registered as `WeightSuccessorJournalDurableScratchR3E` in RAM36 and exact RAM inventory. No full-model transform/compressed/reconstructed temporary is admitted.

## 9. Production Containers

Journal:

```text
magic: ASHWJ3E\0
weight_successor.r3e.bin
weight_successor_manifest.r3e.json
```

Keyframe:

```text
magic: ASHWK3E\0
weight_keyframe.r3e.bin
weight_keyframe_manifest.r3e.json
```

They are version-distinct from shadow `ASHWJR1`.

## 10. Journal Source and Target

Journal source is the current `ResidentWeightPack G`. Target bytes are the existing projected Weight successor `G+1`.

The R3E writer tees the existing source/target projection stream. It does not rerun the optimizer, reopen full source/target Weight packs, or request additional Weight D2H.

Successor journals require exact immediate generation adjacency.

## 11. Frame Exactness

Before a journal frame becomes durable:

```text
source + encoded delta -> decode -> reconstructed target
```

must satisfy:

```text
byte mismatch = 0
bit mismatch = 0
target frame SHA-256 exact
```

Keyframe frames are likewise decoded immediately and compared to exact target bytes.

## 12. Streamed Whole Digests

The journal writer incrementally accumulates whole source and target SHA-256 during the bounded stream. Final source/target digests must match the runtime Weight identities.

No second multi-gigabyte source/target digest traversal is required.

## 13. Persistent Weight Digest Debt Closed

`ResidentWeightPackBuilder` now owns an incremental SHA-256 state. Appended successor bytes update that state, and replay may seal with a verified streamed digest through `finalize_with_verified_digest_r3e`.

The previous static failures:

```text
[30] candidate builder digest
[32] candidate successor no second full digest scan
```

are closed.

Current validator:

```text
validate_ram_weight_pack_persistent_residency_atlas_readahead_r1_static.py
67 / 67 PASS
```

## 14. Keyframe Selection

A keyframe is selected before projection when:

```text
no previous Weight durable head
R3D Adam recovery anchor is due
final writeback
scheduled keyframe cadence
```

Otherwise one immediate-predecessor journal is written.

Keyframe reasons include Bootstrap, ScheduledCadence, AdamRecoveryAnchorCoupling, ExplicitCheckpoint and FinalWriteback.

## 15. Adam Recovery Coupling

Whenever R3D creates `Adam Recovery Anchor D`, R3E forces `Weight Keyframe D`.

Thus the exact recovery generation has a self-contained Weight root and does not depend on a journal chain for normal trainable crash recovery.

## 16. Weight Durability Binding and Head

R3E materializes typed `WeightDurabilityClassR3E::{Keyframe, SuccessorJournal}`, `WeightDurabilityBindingR3E`, and `WeightDurableHeadR3E`.

The binding records source/target generation, source/target Weight digests, layout/registry digests, keyframe generation, replay depth, payload identity, manifest identity and codec profile identity.

Head files:

```text
training_state/weights/r3e/weight_durable_head.r3e.json
training_state/weights/r3e/weight_durable_head.previous.r3e.json
```

The previous head is retained as a crash fallback around head replacement.

## 17. Descriptor R3 and V6 Active State

R3E introduces `TrainableGenerationDurabilityDescriptorR3` and active schema:

```text
ash.basetrain.training_state.v6.r3e
```

Descriptor/active state bind Weight durability, optimizer ref, Muon durability, R3D Adam recovery lineage, Weight head, keyframe generation, replay depth, Weight reconstructability and full-trainable restart eligibility.

Weight reconstructability and full optimizer restartability remain separate facts.

## 18. P3 R3E Transaction

R3E materializes:

```text
prepare_active_transactional_commit_r3e
finalize_active_transactional_commit_r3e
```

The prepare binds Weight durability, Muon durability, `OptimizerGenerationRefR3D`, and Descriptor R3, and explicitly requires ordinary candidate absence of:

```text
weights.r6pack
adam_m.r6pack
adam_v.r6pack
```

The R3E P3 path does not reopen a raw full Weight pack.

## 19. Weight Durable Head Publication

After active-state publication, the prepared Weight head is persisted. Its target generation and target Weight SHA must match the successor used by R3C1 live runtime promotion.

Disk durability does not replace `ResidentWeightPack` as runtime authority.

## 20. Bounded Replay

`WeightSuccessorReplayRuntimeR3E` reconstructs directly into `ResidentWeightPackBuilder`.

A keyframe is decoded in bounded frames. Journals then overwrite exact bounded ranges in the same resident backing. Every predecessor digest must match the preceding target digest.

The final target digest is accumulated during replay and passed to the builder without a second full resident Weight scan.

## 21. R3D Fresh Recovery Integration

R3D continues to choose the complete trainable recovery generation through `adam_recovery_head.r3d.json`.

For V6/R3E retained recovery roots, Weight is restored from the same-generation R3E Weight keyframe directly into resident memory. No retained raw `weights.r6pack` is required.

## 22. Recovery Retention R3E

`retain_recovery_generation_bundle_r3e` requires the selected recovery generation Weight head to be a same-generation keyframe with replay depth zero.

The retained recovery root includes the Weight keyframe tree/head, Adam recovery M/V, Muon momentum, active/control state, optimizer ref, Descriptor R3 and R3E artifact receipt.

Adam recovery M/V are still copied under legacy hydration filenames inside the retained recovery slot because Eve hydration ABI is not changed by R3E.

## 23. Ordinary R3E Receipt

`TrainableGenerationWeightPayloadRetirementReceiptR3E` records source/target generation, durability class, target Weight digest, journal/keyframe bytes, Weight head, Descriptor R3, replay depth, exactness and physical claim.

Current source-level ordinary values include:

```text
full_weight_payload_write_bytes = 0
full_weight_payload_file_count = 0
additional_weight_d2h_bytes = 0
extra_source_pack_read_bytes = 0
extra_target_pack_read_bytes = 0
post_stream_full_digest_scan_count = 0
physical_pass_claimed = false
```

These are intended static telemetry, not physical runtime evidence.

## 24. No Silent Fallback

R3E admission fails closed when codec profile/selection receipt is missing or invalid. Journal verification failure does not silently reactivate full `weights.r6pack` output.

The historical shadow path remains independent and best-effort; production R3E is not.

## 25. Static Validation

New gate:

```text
tools/validate_ash_basetrain_weight_keyframe_bit_exact_successor_delta_journal_r3e_static.py
```

Current result:

```text
52 / 52 PASS
```

Token:

```text
PASS_ASH_BASETRAIN_WEIGHT_KEYFRAME_AND_BIT_EXACT_SUCCESSOR_DELTA_JOURNAL_DURABLE_AUTHORITY_CUTOVER_R3E_STATIC
```

## 26. Expanded Parent Regression

Current campaign includes Eve R1/R2/R3, R3A, R3B, R3C, R3C1, R3D, HiMuon sparse R1/R1A/R1B, MCU AdamW pending, full-model device segmented successor, SubmissionEpoch active async, Weight shadow R1, persistent Weight residency and R3E.

Current result:

```text
17 / 17 PASS
```

## 27. Historical RAM36 Baseline

The separate RAM36 process-budget static validator remains:

```text
60 / 63 PASS
```

with the same pre-existing failures:

```text
main release receipt gate
main exact binary gate
release cf1 parent required
```

They are not new R3E regressions and are not claimed fixed.

## 28. Structural / Compile Boundary

All 15 R3E-changed Rust files pass non-compiler UTF-8 and balanced-delimiter checks. The new Python validator passes `py_compile`.

The bake environment exposes no `cargo`, `rustc`, or `rustfmt`, so no Rust compile PASS is claimed.

## 29. Required Physical Qualification

Physical R3E promotion requires:

```text
real shadow codec campaign
physicalQualified codec-selection receipt
one authoritative keyframe
multiple authoritative journals
ordinary weights.r6pack count = 0
all frame byte/bit mismatch counts = 0
all target Weight digests exact
additional Weight D2H = 0
extra source/target full-pack reads = 0
post-stream full digest scans = 0
bounded replay to exact ResidentWeightPack target
R3D crash recovery with same-generation Adam anchor + Weight keyframe
```

Power-loss/head replacement windows also require crash fixtures.

## 30. Physical PASS Token

Reserved:

```text
PASS_ASH_BASETRAIN_WEIGHT_KEYFRAME_AND_BIT_EXACT_SUCCESSOR_DELTA_JOURNAL_DURABLE_AUTHORITY_CUTOVER_R3E_PHYSICAL
```

Until then:

```text
HOLD_ASH_WEIGHT_R3E_PHYSICAL_PENDING
```

## 31. Storage Metrics

R3E must measure actual journal bytes, keyframe bytes, metadata bytes, keyframe interval, replay depth, compression ratio, rolling Weight durable bytes/step and rolling total durable bytes/step.

The wider `< 1 GiB/step` rolling durable target is not claimed by this static revision.

## 32. Scope Limits

R3E does not yet retire Muon momentum full durable rewrite or Adam recovery anchors. It does not introduce lossy Weight quantization, Device-Hot Eve, or WGPU26 completion callback cutover.

Explicit operator-requested portable full exports remain separate from automatic ordinary training durability.

## 33. Direct Successor

After R3E compile and physical qualification:

```text
ASH-HIMUON-MOMENTUM-DURABLE-CADENCE
-AND-ORDINARY-STEP-FULL-MOMENTUM-REWRITE-RETIREMENT-R3F
```

is the natural next storage reduction.

## 34. Final Invariant

```text
Runtime Weight remains ResidentWeightPack.

A keyframe is one self-contained exact Weight root.
A journal is one exact G -> G+1 edge.

Every frame is decoded and compared before durable admission.
Whole source and target digests are accumulated during the same stream.
No second multi-gigabyte Weight digest scan is needed.

Adam recovery generations force same-generation Weight keyframes,
so exact trainable crash recovery remains self-contained.

Ordinary generations no longer write a full raw Weight world merely to prove they existed.
```

Final sentence:

> **R3E is the durable cut where ASH stops storing a complete multi-gigabyte Weight snapshot for every ordinary optimizer generation. Runtime Weight remains `ResidentWeightPack`; disk durability becomes periodic exact keyframes plus immediate-predecessor bit-exact successor journals, with codec choice gated by physical measurement and every reconstruction path verified against the committed target digest.**
