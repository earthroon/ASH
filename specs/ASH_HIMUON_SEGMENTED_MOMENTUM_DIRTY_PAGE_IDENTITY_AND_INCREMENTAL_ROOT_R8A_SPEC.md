# ASH-HIMUON-SEGMENTED-MOMENTUM-DIRTY-PAGE-IDENTITY-AND-INCREMENTAL-ROOT-R8A

## 0. Revision

```text
Patch ID:
ASH-HIMUON
-SEGMENTED-MOMENTUM
-DIRTY-PAGE-IDENTITY
-AND-INCREMENTAL-ROOT-R8A

Short name:
ASH HIMUON R8A
SEGMENTED MOMENTUM + DIRTY-PAGE IDENTITY + INCREMENTAL ROOT

Status:
STATIC MATERIALIZATION RELEASE

Rust compile PASS:                NOT CLAIMED
GPU physical PASS:                NOT CLAIMED
segmented hydration PASS:         NOT CLAIMED
incremental identity PASS:        NOT CLAIMED
R3F flat-hash compatibility PASS: NOT CLAIMED
RAM36 physical PASS:              NOT CLAIMED
```

Static token:

```text
PASS_ASH_HIMUON_SEGMENTED_MOMENTUM_DIRTY_PAGE_IDENTITY_AND_INCREMENTAL_ROOT_R8A_STATIC
```

Physical state:

```text
HOLD_ASH_HIMUON_R8A_PHYSICAL_PENDING
```

## 1. Direct Parent

Direct parent:

```text
ASH-HIMUON-SESSION-RUNTIME-OWNERSHIP-SPLIT-AND-MOMENTUM-EXECUTION-DURABILITY-SEPARATION-R8
```

R8 already makes canonical HiMuon momentum private behind execution/durability APIs. R8A replaces that private backing and current-generation identity mechanism without reopening the full ProductionMuon execution graph.

R8A preserves MCU R7/R7A/R7B, packed-gradient R7A1, R4/R4A, R3C/R3C1 and historical R3F recovery-anchor semantics.

## 2. Historical R3F Identity Remains Distinct

Historical R3F `momentum_state_sha256` is the exact SHA-256 of the complete canonical F32 little-endian byte stream.

R8A never labels its incremental root as that digest.

```text
R8A OrderedPageTreeSha256V1
= current live/ordinary momentum state identity

R3F flat F32 SHA-256
= full recovery-anchor / compatibility payload identity
```

The algorithms are explicit and version-distinct.

## 3. Segmented Canonical Backing

Materialized:

```text
HiMuonMomentumRuntimeR8A
HiMuonSegmentedMomentumStoreR8A
HiMuonMomentumPageR8A
```

Canonical production geometry:

```text
page bytes    = 65,536
page elements = 16,384 F32
```

The R8A production runtime contains no canonical full `Vec<f32>` alongside the segmented body.

`HiMuonSessionRuntimeR8` now owns `HiMuonMomentumAuthorityR8A::{ContiguousR8, SegmentedR8A}` so historical R8 remains a compatibility lineage while active R8A uses the segmented successor.

## 4. Direct Segmented Hydration

Production resume uses:

```text
HiMuonMomentumRuntimeR8A::hydrate_segmented_r8a
```

The historical momentum payload is read a page at a time through a bounded 64-KiB byte buffer, decoded directly into F32 pages and finite-checked.

The same required source traversal computes and verifies the historical R3F flat SHA. No complete temporary momentum Vec is created before page adoption.

Fresh zero momentum is also built page-by-page.

## 5. Runtime Access

Canonical production reads/writes remain behind the R8 momentum authority and delegate to segmented-safe operations:

```text
copy_range_into_r8a
copy_range_owned_r8a
copy_tile_256_r8a
commit_candidate_range_r8a
commit_candidate_tile_r8a
```

Cross-page operations are internal to the momentum runtime. ProductionMuon/BPDK code does not own page geometry or mutable page slices.

## 6. Dirty-page Tracking

Materialized:

```text
HiMuonDirtyPageTrackerR8A
```

It uses one dirty-page ordinal vector plus per-page dirty epochs. Repeated writes to the same page within one identity epoch produce one dirty entry.

Successful candidate mutation advances a checked state revision and makes the previously sealed identity stale.

## 7. Ordered Page Tree

Only one production algorithm is admitted:

```text
OrderedPageTreeSha256V1
```

Domain-separated hashes are used for leaf, node, padding and final state-root construction.

A leaf hashes exact logical F32 little-endian bytes plus its logical element count. Tail allocation slack is excluded. Leaves are ordered by canonical page ordinal and padded to the next power of two with a fixed padding digest.

The final R8A state root binds page geometry, element/page count, ordered content root, registry digest, optimizer-routing digest and momentum profile digest.

## 8. Incremental Seal

Materialized:

```text
seal_incremental_identity_r8a
```

For a dirty state it rehashes dirty page payloads only, deduplicates and updates affected tree ancestors, promotes the new roots, updates the sealed revision and only then clears the dirty set.

On seal failure the phase returns to Dirty and the dirty set remains present. A stale root cannot be published.

When no page is dirty the existing sealed root is reused with zero momentum-payload reads.

Per-seal telemetry records dirty-page count, page rehash count, tree-node rehash count and incremental momentum RAM-read bytes.

## 9. Full Anchor Stream Verification

R8 durability continues to write an R3F-compatible exact F32 recovery anchor.

For segmented R8A momentum, that single full stream simultaneously:

```text
writes canonical F32 bytes
updates historical flat SHA-256
computes R8A page leaf hashes
```

After the stream, the leaf set is rebuilt through metadata-only tree hashing and compared with the live sealed R8A content/state roots.

No second full momentum payload traversal is required for this anchor verification.

## 10. R3F Compatibility Preserved

Historical:

```text
digest_resident_muon_momentum_r3f
MuonMomentumStateIdentityR3F
MuonGenerationRefR3F
R3F recovery payload/manifest
```

remain unchanged.

R8A ordinary production does not call the R3F full flat digest for current-generation identity. At an exact anchor generation the flat SHA is obtained from the required full anchor stream.

## 11. MuonGenerationRefR8A

Materialized:

```text
MuonGenerationRefR8A
schema: ash.basetrain.muon_generation_ref.r8a
file:   muon_generation_ref.r8a.json
```

It binds generation, registry/routing/profile identity, `MuonMomentumStateIdentityR8A`, device-generation identity, full TrainableGeneration identity and the historical R3F recovery binding.

It does not contain an R3F `momentum_state_sha256` field containing the R8A root.

## 12. Descriptor R5 and Active State

Materialized:

```text
TrainableGenerationDurabilityDescriptorR5
schema: ash.basetrain.trainable_generation_durability_descriptor.r5
file:   trainable_generation_durability_descriptor.r5.json
```

R5 preserves Weight R3E, Adam R3D, cursor, scheduler and recovery bindings while replacing the current Muon reference with `MuonGenerationRefR8A`.

Historical Descriptor R4 remains immutable and continues to bind R3F.

Active training-state successor:

```text
ash.basetrain.training_state.v8.r8a
```

Resume reopens Descriptor R5 and validates generation, parameter set, cursor, scheduler and Weight identity. Persistent Weight replay recognizes v8.r8a as the R3E-family resident Weight source.

## 13. Ordinary Production Path

Under admitted R8A:

```text
R3F control-only momentum persistence remains active
ordinary full momentum candidate payload count = 0
ordinary full momentum payload write bytes = 0
current momentum identity = incremental R8A root
ordinary current-state R3F flat SHA scan count = 0
additional momentum D2H bytes = 0
```

`TrainableGenerationMuonPayloadRetirementReceiptR8A` records root/page geometry, dirty and tree-rehash metrics, anchor metrics and explicit physical HOLD.

## 14. Anchor Compatibility

At an exact recovery-anchor generation, R8A also materializes historical R3F-compatible Muon ref / Descriptor R4 evidence needed by the retained recovery-root parent.

The authoritative live active state remains R8A / Descriptor R5.

Retained recovery slots copy both compatibility files and R8A/R5 files so a fresh R8A resume can reopen the successor active state while preserving exact historical recovery payload compatibility.

## 15. R8A P3 Transaction

Materialized:

```text
prepare_active_transactional_commit_r8a
finalize_active_transactional_commit_r8a
```

Prepare requires the R8A Muon ref, Descriptor R5, its file binding and R8A ordinary receipt; it rejects ordinary full Muon payload and parent-retired raw Weight/Adam payloads.

Finalize requires the active `v8.r8a` state and exact R8A Muon/descriptor digests.

The production scheduler selects R8A P3 finalize when R8A is active and retains historical R3F finalize as compatibility behavior.

## 16. Downgrade Protection

A source generation already carrying Descriptor R5 cannot silently commit to an older durability schema.

Historical descriptor lineages may advance to R5 without being misclassified as a downgrade.

## 17. R4A Admission

New default-OFF fields:

```text
admit_himuon_segmented_momentum_r8a
admit_himuon_dirty_page_identity_r8a
admit_himuon_incremental_root_r8a
admit_himuon_generation_ref_r8a
```

Dependency chain:

```text
segmented momentum -> HiMuon R8 ownership/separation
dirty identity     -> segmented momentum
incremental root   -> dirty identity
R8A generation ref -> incremental root + R3F recovery parent
```

All participate in the sealed R4A runtime-config identity, so one live session cannot switch backing representation or identity algorithm mid-run.

## 18. RAM36 Boundary

R8A production requires:

```text
canonical segmented momentum body count = 1
complete compatibility momentum Vec count = 0
full-body clone count = 0
```

Added RAM is page-object metadata, dirty tracking, hash-tree metadata and a bounded hydration byte buffer.

## 19. Static Validation

Validator:

```text
tools/validate_ash_himuon_segmented_momentum_dirty_page_identity_incremental_root_r8a_static.py
```

Current result:

```text
115 / 115 PASS
PASS_ASH_HIMUON_SEGMENTED_MOMENTUM_DIRTY_PAGE_IDENTITY_AND_INCREMENTAL_ROOT_R8A_STATIC
```

New R8A production modules contain no Rust `if` keyword; new R8A state/validation branching is match-based.

## 20. Parent Regression

Current bake retains:

```text
HiMuon R8                           90 / 90 PASS
packed-gradient R7A1               82 / 82 PASS
MCU child ownership R7B            78 / 78 PASS
MCU device resource R7A            73 / 73 PASS
Trainable Session R4A              65 / 65 PASS
Trainable Session R4               64 / 64 PASS
Eve R3G                            35 / 35 PASS
R3C                                18 / 18 PASS
R3C1                               30 / 30 PASS
R3D                                41 / 41 PASS
R3E                                52 / 52 PASS
R3F                                66 / 66 PASS
Unified Atlas MCU R6               PASS
Mixed-precision MCU R7             PASS
SubmissionEpoch active async       PASS
Resident Weight                    67 / 67 PASS
```

Historical unchanged baselines remain:

```text
RAM exact inventory                66 / 67
N8 RAM resume-cut                 117 / 118
```

## 21. Compile Boundary

The bake environment exposes no `cargo`, `rustc` or `rustfmt` executable.

Therefore Rust compile PASS and GPU physical PASS are not claimed.

The R8A validator passes `py_compile`; changed Rust sources pass UTF-8, NUL and balanced-delimiter structural checks.

## 22. Physical Qualification

Physical promotion requires real direct segmented hydration, no complete temporary momentum Vec, zero/single/multiple/fully-dirty cases, incremental-root equality against an independent full tree rebuild, exact R3F anchor SHA, exact streamed-tree verification, fresh recovery parity, ordinary flat-SHA scan count zero, ordinary full momentum payload count zero, no additional momentum D2H, RAM36 compliance, R3C1 atomicity and HiMuon numerical parity.

Until then:

```text
HOLD_ASH_HIMUON_R8A_PHYSICAL_PENDING
```

## 23. Explicit Non-claims

R8A does not claim lossy/compressed momentum, ordinary-generation exact crash reconstruction, device-hot canonical momentum, multi-device momentum or tensor-parallel HiMuon.

## 24. Direct Successor

A later durability successor may introduce:

```text
ASH-HIMUON
-MOMENTUM-PAGE-SUCCESSOR-JOURNAL
-AND-EXACT-DIRTY-PAGE-REPLAY-R8B
```

That revision would persist exact changed-page successors between full anchors. R8A deliberately separates runtime identity optimization from that storage problem.

## 25. Final Law

> Canonical HiMuon momentum is one semantic state composed of independently hashable fixed pages.

> Ordinary identity work reads the pages that changed and recomputes only the affected hash-tree structure; it does not automatically traverse the full momentum payload.

> The R8A ordered-page root identifies live state. The historical R3F flat SHA identifies the full canonical byte stream. Both are exact and never mislabeled as the same algorithm.
