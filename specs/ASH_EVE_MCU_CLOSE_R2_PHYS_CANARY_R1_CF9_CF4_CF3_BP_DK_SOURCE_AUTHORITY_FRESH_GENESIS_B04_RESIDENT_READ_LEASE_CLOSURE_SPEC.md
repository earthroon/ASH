# ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF9-CF4-CF3

## BP-DK SOURCE AUTHORITY
## FRESH-GENESIS B04 RESIDENT READ-LEASE CLOSURE

```text
+ EXPLICIT SOURCE AUTHORITY CLASSIFICATION
+ COMMITTED-SEGMENTED SOURCE WHEN PRESENT
+ B04 FRESH-GENESIS SOURCE AUTHORITY
+ LIVE ATLAS-WAVE SOURCE READ LEASE
+ SOURCE GENERATION EXACT PARITY
+ SOURCE PHYSICAL ALLOCATION IDENTITY
+ SOURCE READ PIN THROUGH BP-DK SUBMISSION EPOCH
+ NO RESIDENT LOOKUP FOR ATLAS CANDIDATE BACKINGS
+ NO SOURCE D2H
+ NO BP-DK SOURCE H2D
+ NO BP-DK SOURCE GPU COPY
+ NO FAKE SEGMENTED GENERATION
+ NO DUPLICATE SOURCE BUFFER AUTHORITY
+ EXACT SOURCE AUTHORITY WITNESS
```

---

## 0. Revision identity

```text
Patch ID:
ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF9-CF4-CF3

Class:
BP-DK SOURCE AUTHORITY / FRESH-GENESIS LIVE SOURCE READ CLOSURE

Direct parent:
ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF9-CF4-CF2-CF1

Parent code-only archive:
ASH_PASS3_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF9_CF4_CF2_CF1_ANYHOW_CONTEXT_IMPORT_COMPILEFIX_CODE_ONLY.zip

Parent SHA-256:
19b35901f77cd1f038eb68127b0cd276b0c0e2f6ad89ba23672ef0706f0c5ece
```

---

## 1. Parent physical boundary

CF9-CF4-CF2 physically established the candidate-side lifetime closure:

```text
Atlas candidate Weight live pre-reclaim handoff       PASS
Atlas candidate Momentum live pre-reclaim handoff     PASS
Atlas orthogonal Update live pre-reclaim handoff      PASS
parameter-local GPU assembly                          PASS
assembly SubmissionEpoch exact completion             PASS
original wave backing reclaim after copy completion   PASS
multi-wave coverage                                   exact
gap_count                                              0
overlap_count                                          0
assembly-seal                                           admitted=true
candidate ResidentGraph reconstruction                 false
```

The new first failure was:

```text
E_CF9_CF4_SOURCE_GENERATION_MISSING
```

Therefore CF4-CF2 remains crossed. CF3 changes only the BP-DK source authority path.

---

## 2. Source-truth correction

The initial CF3 design phrase “B04 resident source” suggested that FreshGenesis under the current Atlas-wave streaming route owned one persistent B04 parameter-wide source `Buffer` in `MuonResidentStateGraph`.

Exact parent source disproves that premise.

In Atlas-wave streaming mode the resident graph explicitly treats RAM as canonical and every GPU wave as a transient projection. Source Weight and Muon Momentum are uploaded into live per-wave A02/A03 arena buffers and reclaimed after the physical wave completes.

Therefore CF3 MUST NOT fabricate a persistent ResidentGraph source view.

The requested semantic intent is preserved using the actual physical authority:

```text
B04 / FreshGenesis / Atlas-wave
    source Weight transient projection LIVE
    source Momentum transient projection LIVE
        ↓
BP-DK source-dependent reduction reads them IN PLACE
before their original reclaim boundary
        ↓
only compact tile/pair observations survive
```

This physical class is named:

```text
B04_ATLAS_WAVE_FRESH_GENESIS
```

The historical patch title is preserved, but “resident read lease” means the admitted B04 live device-source authority, not a fake persistent ResidentGraph buffer.

---

## 3. Explicit source authority classification

CF3 materializes an explicit source authority enum:

```rust
BpDkSourceAuthorityCf3 {
    CommittedSegmented,
    B04AtlasWaveFreshGenesis,
}
```

Selection law:

```text
committed_device_source.muon = Some(...)
    → COMMITTED_SEGMENTED

committed_device_source.muon = None
AND source_generation = 0
AND target_generation = 1
AND B04 ActiveVerified
AND Atlas-wave streaming active
    → B04_ATLAS_WAVE_FRESH_GENESIS

otherwise
    → FAIL CLOSED
```

`Option::None` is not policy. It is only an input to explicit classification.

---

## 4. Committed segmented preservation

When canonical committed segmented source exists, `COMMITTED_SEGMENTED` remains the existing BP-DK source authority. CF3 does not redirect later generations through the FreshGenesis live-source path.

---

## 5. FreshGenesis source authority

For the admitted generation-zero campaign before `committed_device_source.muon` is installed, source generation is 0 and target generation is 1. Source Weight/Momentum are observed from the exact live Atlas source projection already used by candidate execution. No fake `MuonDeviceSegmentedGenerationR1` is constructed.

---

## 6. No candidate authority regression

CF4-CF2 remains authoritative for candidate Weight, candidate Momentum and orthogonal Update through the parameter assembly. CF3 does not restore `partition_view_by_key_cf4(...)` for Atlas candidate backings. Candidate ResidentGraph lookup remains prohibited.

---

## 7. Source/candidate authority split

FreshGenesis physical observation has two legitimate backing lifetimes:

```text
SOURCE W/M
    live Atlas-wave projection
    read before reclaim
    compact reduction evidence retained

TARGET W/M + UPDATE
    CF4-CF2 parameter assembly
    retained until exact digest/evidence completion
```

This is one semantic BP-DK observation, not two competing policies.

---

## 8. No source GPU duplication

CF3 does not allocate a second full source Weight/Momentum buffer for BP-DK.

```text
BP-DK source GPU copy bytes = 0
BP-DK source D2H bytes      = 0
BP-DK source H2D bytes      = 0
```

The existing Atlas candidate path may already upload RAM-canonical source data into its transient source projection. CF3 adds no additional source H2D and no additional source full-buffer copy for BP-DK.

---

## 9. Live source read boundary

```text
candidate execution exact completion
↓
source W/M still LIVE
candidate W/M/update still LIVE
↓
CF3 BP-DK source-dependent reduction submission
↓
real SubmissionEpoch
↓
exact completion
↓
compact tile/pair readback only
↓
CF4-CF2 candidate assembly submission/completion
↓
original wave backings reclaim
```

Source reads occur before the original A02 source lease reclaim.

---

## 10. Source read lease authority

CF3 uses the existing A01 submission lease authority over the exact live physical source/candidate/update allocations. The BP-DK source read submission obtains a real `SubmissionEpoch` and exact-waits it before returning to the wave reclaim path. This is the physical source-read pin.

---

## 11. Source physical identity

Each source observation records canonical parameter index, source generation, source Weight/Momentum `PhysicalAllocationId`, canonical tile coverage, wave provenance and real `SubmissionEpoch`. Physical allocation identity is attribution, not a lifetime extension.

---

## 12. Source generation parity

`target_generation = source_generation + 1` is required with checked arithmetic. No saturating generation repair is accepted.

---

## 13. Source geometry

Each live observation batch requires `element_count > 0` and `element_count % 256 = 0`. Canonical local/fused tile ordinals are derived from authoritative parameter element offsets. No semantic tail padding.

---

## 14. Local and fused mapping

Local physical tiles map to canonical tile ordinals from `gradient_tile_base_element_offset / 256`. Fused local tiles map to canonical lhs/rhs tiles and the existing canonical pair ordinal. Pair topology comes from the existing fusion plan descriptors. No second pair planner is introduced.

---

## 15. Compact source observation

The existing BP-DK reduction/pair WGSL is reused. A FreshGenesis batch emits only tile RMS observations and pair cosine/status observations. The batch path does not dispatch target SHA-256.

---

## 16. Exact target/update digest

After CF4-CF2 seals the full candidate assembly, CF3 performs one exact target-only digest submission using the existing SHA-256 pipeline over assembled candidate Weight, candidate Momentum and orthogonal Update. No per-wave digest-of-digests is accepted.

---

## 17. Persistent pipeline reuse

CF3 does not rebuild BP-DK pipelines per parameter. `BpDkDevicePostUpdateRuntimeR1` owns the producer through shared `Arc` authority and exposes a process-local producer handle. FreshGenesis observation therefore reuses the persistent reduction, pair and SHA-256 pipelines already owned by BP-DK runtime.

---

## 18. Compact evidence collector

`BpDkFreshGenesisObservationCollectorCf3` owns a shared producer handle, tile/pair compact observations, source attribution digest, compact D2H byte count and source observation SubmissionEpoch list. It does not own a duplicate full source tensor.

---

## 19. Exact coverage

Before semantic receipt construction, observed tile and pair counts must equal the semantic plan counts. Duplicate canonical tile or pair ordinals fail closed.

---

## 20. Semantic SSOT

Final semantic authority remains `AshBpDkPostUpdateParameterReceipt`, reconstructed through the existing `AshBpDkPostUpdateStreamingBuilder::finalize_from_device_evidence_r1`. No CF3-specific semantic receipt universe is introduced.

---

## 21. CF4-CF2 preservation

Candidate W/M/update pre-reclaim copy, real copy SubmissionEpoch, exact coverage, zero gap/overlap and reclaim-after-copy-completion remain unchanged.

---

## 22. C08 / P5 preservation

The current CANARY remains B04 ActiveVerified, B05 ActiveDeviceCandidate, B06 ActiveVerified, C07 ActiveCompact, C08 MirrorVerified. CF3 does not claim C08 ActiveAsync, P5 production cutover or exact-wait retirement.

---

## 23. No optimizer math change

CF3 changes evidence transport/lifetime authority only. Adam math, Muon math, orthogonalization, BP-DK semantic math, fusion planner policy, router policy and optimizer commit order are unchanged.

---

## 24. Required witnesses

FreshGenesis source authority:

```text
[ASH-BP-DK-CF9-CF4-CF3][source-authority]
selected_authority=B04_ATLAS_WAVE_FRESH_GENESIS
committed_segmented_present=false
source_generation=0
target_generation=1
source_read_mode=LIVE_PRE_RECLAIM
bpdk_source_d2h_bytes=0
bpdk_source_h2d_bytes=0
bpdk_source_gpu_copy_bytes=0
```

Source read lease:

```text
[ASH-BP-DK-CF9-CF4-CF3][source-read-lease]
lease_state=ACQUIRED
...
lease_state=RELEASED_AFTER_EXACT_COMPLETION
submission_epoch=<real epoch>
```

Source buffer:

```text
[ASH-BP-DK-CF9-CF4-CF3][source-buffer]
authority=B04_ATLAS_WAVE_FRESH_GENESIS
weight_physical_allocation_ordinal=<real>
momentum_physical_allocation_ordinal=<real>
bpdk_source_d2h_bytes=0
bpdk_source_h2d_bytes=0
bpdk_source_gpu_copy_bytes=0
```

Source/target parity:

```text
[ASH-BP-DK-CF9-CF4-CF3][source-target-parity]
generation_relation_exact=true
element_geometry_exact=true
device_exact=true
queue_exact=true
admitted=true
```

---

## 25. Failure retirement

For admitted FreshGenesis Atlas-wave source, CF3 must retire `E_CF9_CF4_SOURCE_GENERATION_MISSING`. Earlier `BpDkPostUpdateCandidateCardinality`, `E_CF9_CF4_RESIDENT_PARTITION_VIEW_MISSING`, and `E_DEVICE_SOFT_SUBGROUP_ARENA_PAGE_MISSING` must remain retired.

---

## 26. Forbidden fixes

```text
fake MuonDeviceSegmentedGenerationR1 for FreshGenesis
persistent fake ResidentGraph source insertion
Atlas candidate ResidentGraph lookup
key suffix stripping
source full D2H
BP-DK-specific source H2D
BP-DK-specific full source GPU copy
zero-filled source reconstruction
per-wave digest-of-digests
per-parameter pipeline rebuild
C08 ActiveAsync promotion
P5 cutover promotion
```

---

## 27. Static acceptance

```text
explicit source authority classification                 present
CommittedSegmented branch                                preserved
FreshGenesis Atlas live-source branch                    present
candidate ResidentGraph lookup                           zero at CF4 callsite
source full D2H                                           zero
BP-DK-specific source H2D                                 zero
BP-DK-specific source GPU copy                            zero
fake segmented source generation                         zero
shared persistent BP-DK producer                         present
source live reduction before source arena reclaim        present
exact source observation SubmissionEpoch wait            present
canonical tile/fused-pair remap                          present
exact tile/pair coverage                                 present
CF4-CF2 candidate assembly                               preserved
existing semantic finalizer                              reused
```

---

## 28. Static validation record

```text
R7A parent     79 / 83 PASS
R7A CF3        79 / 83 PASS
R7A1 parent    77 / 82 PASS
R7A1 CF3       77 / 82 PASS
```

Remaining failures are pre-existing source-pattern drift in historical validators. No new CF3 validator regression was observed. Static validation is not compile/WGPU proof.

---

## 29. Compile / single-build CF1 acceptance

Use the existing single-build workflow:

```text
apply overlay
→ verify source hashes
→ touch modified source timestamps
→ native-cf1-release-compile-authority
   (base_train release build exactly once)
→ CF1 binary SHA == base_train.exe SHA
→ 2-step CANARY
```

The bake environment does not claim native compilation.

---

## 30. Physical acceptance

One real CANARY must reach:

```text
CF4-CF2 assembly-seal admitted=true
→ CF3 source-authority B04_ATLAS_WAVE_FRESH_GENESIS
→ source-read-lease ACQUIRED
→ source-buffer physical IDs
→ source-read-lease RELEASED_AFTER_EXACT_COMPLETION
→ source-target-parity admitted=true
→ CF4 device-post-collect
→ canonical post-receipt
```

with full candidate D2H and host candidate materialization zero, and BP-DK-specific source D2H/H2D/GPU copy zero.

---

## 31. PASS token

```text
PASS_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF9_CF4_CF3
```

---

## 32. Non-claims

CF3 does not claim C08 ActiveAsync, P5 queue cutover, all exact waits retired, full BP-DK numerical qualification, full R1B campaign, A/B/C promotion, or final resource geometry for all future generations.

---

## 33. Code bake record

```text
Direct parent files: 8424
ADD: 0
MOD: 5
DEL: 0
Output full files: 8424
```

Modified source:

```text
6801f1466e85ffcfc2f3619ee98e49a539caeae66941ef21eadeb7eed91e786c
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs

71462d52291dec398942274eea1516868048c7d8782238f06a5f453f4730c54e
crates/base_train/src/unified_atlas_mcu_bp_dk_device_post_update_reduction_exact_digest_compact_evidence_r1.rs

d5525391498cfeb7dd07f7bb9e06132f97065a99dfe645ee5e339af340e4e8e9
crates/burn_webgpu_backend/src/base_train_tensorcube_local_muon.rs

1e745a6919f6e0e741b58e505e5b75d5f314c09f8b2a6bc4c2bd754900855c79
crates/burn_webgpu_backend/src/bp_dk_device_post_update_r1.rs

e70c571510bf72ccf3614f3a5432ecc1fcf3a51078988cbb6e20bd4617cdc2da
crates/burn_webgpu_backend/src/tensorcube_fused_pair_muon.rs
```

---

## 34. Artifacts

```text
Full code-only:
ASH_PASS3_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF9_CF4_CF3_BP_DK_SOURCE_AUTHORITY_FRESH_GENESIS_B04_LIVE_SOURCE_READ_CLOSURE_CODE_ONLY.zip
SHA-256: af8ddce448fa02c7b26e94394a208eb3d74e9cf067e2099cbb00f3f04833ab22
Files: 8424
CRC: PASS
specs/: 0
artifacts/: 0

Overlay code-only:
ASH_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF9_CF4_CF3_BP_DK_SOURCE_AUTHORITY_FRESH_GENESIS_B04_LIVE_SOURCE_READ_CLOSURE_OVERLAY_CODE_ONLY.zip
SHA-256: 0e8797ed929def96fc3c03ed7c653bf27c79a5ff6df1e4ce3777ce8e7b2de511
Files: 5
CRC: PASS
specs/: 0
artifacts/: 0
```

---

# Final law

> **CF3 follows the physical source that actually exists.**
>
> `committed_device_source.muon` is authoritative when installed. During FreshGenesis Atlas-wave streaming before that installation, there is no fake persistent B04 source Buffer to recover. The real source authority is the live per-wave source projection already consumed by candidate execution.
>
> BP-DK reads that source in place before reclaim, under real A01 SubmissionEpoch ownership, and retains only compact source-dependent observations. Candidate/update state remains the CF4-CF2 sealed parameter assembly and exact target/update SHA authority.
>
> No fake segmented generation, no candidate ResidentGraph lookup, no full source D2H, no additional BP-DK source H2D, no BP-DK full-source copy, no duplicate source buffer authority, and no per-parameter pipeline rebuild are accepted.
