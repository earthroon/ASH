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

When canonical committed segmented source exists:

```text
COMMITTED_SEGMENTED
```

remains the existing BP-DK source authority.

CF3 does not redirect later generations through the FreshGenesis live-source path.

---

## 5. FreshGenesis source authority

For the admitted generation-zero campaign before `committed_device_source.muon` is installed:

```text
source generation = 0
target generation = 1
```

source Weight/Momentum are observed from the exact live Atlas source projection already used by candidate execution.

No fake `MuonDeviceSegmentedGenerationR1` is constructed.

---

## 6. No candidate authority regression

CF4-CF2 remains authoritative for candidate evidence:

```text
candidate Weight      → parameter assembly
candidate Momentum    → parameter assembly
orthogonal Update     → parameter assembly
```

CF3 does not restore:

```text
partition_view_by_key_cf4(...)
```

for Atlas candidate backings.

Candidate ResidentGraph lookup remains prohibited.

---

## 7. Source/candidate authority split

FreshGenesis physical observation now has two legitimate backing lifetimes:

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

Required:

```text
BP-DK source GPU copy bytes = 0
BP-DK source D2H bytes      = 0
BP-DK source H2D bytes      = 0
```

Important scope:

The existing Atlas candidate path may already upload RAM-canonical source data into its transient source projection. CF3 adds no additional source H2D and no additional source full-buffer copy for BP-DK.

---

## 9. Live source read boundary

For each Atlas physical batch:

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

Source reads therefore occur before the original A02 source lease reclaim.

---

## 10. Source read lease authority

CF3 uses the existing A01 submission lease authority over the exact live physical allocations:

```text
source Weight allocation
source Momentum allocation
candidate Weight allocation
candidate Momentum allocation
Update allocation
```

The BP-DK source read submission obtains a real `SubmissionEpoch` and exact-waits it before returning to the wave reclaim path.

This is the physical source-read pin.

---

## 11. Source physical identity

Each source observation records:

```text
canonical parameter index
source generation
source Weight PhysicalAllocationId
source Momentum PhysicalAllocationId
canonical tile coverage
wave provenance
real SubmissionEpoch
```

Physical allocation identity is attribution, not a lifetime extension.

---

## 12. Source generation parity

Required:

```text
target_generation = source_generation + 1
```

with checked arithmetic.

No saturating generation repair is accepted.

---

## 13. Source geometry

Each live observation batch requires:

```text
element_count > 0
element_count % 256 = 0
```

Canonical local/fused tile ordinals are derived from already-authoritative parameter element offsets.

No semantic tail padding.

---

## 14. Local wave mapping

For local Muon batches:

```text
local physical tile 0..K
    → canonical tile ordinal from gradient_tile_base_element_offset / 256
```

There are no pair observations in a local-only batch.

---

## 15. Fused wave mapping

For fused pairs:

```text
local tile 2i     → canonical lhs tile
local tile 2i + 1 → canonical rhs tile
local pair i      → canonical pair_ordinal
```

Pair topology comes from the existing fusion plan descriptors.

No second pair planner is introduced.

---

## 16. Compact source observation

The existing BP-DK reduction/pair WGSL is reused.

A FreshGenesis batch emits only:

```text
tile RMS observations
pair cosine/status observations
```

The batch path does NOT dispatch target SHA-256.

This avoids duplicate whole-target hashing per wave.

---

## 17. Exact target/update digest

After CF4-CF2 seals the full candidate assembly, CF3 performs one exact target-only digest submission using the existing SHA-256 pipeline over:

```text
assembled candidate Weight
assembled candidate Momentum
assembled orthogonal Update
```

This produces the existing canonical three digests.

---

## 18. No per-wave digest-of-digests

Forbidden:

```text
per-wave candidate SHA
→ hash of hashes
```

The exact target/update SHA is computed over the full canonical assembled f32 sequence using the existing digest ABI.

---

## 19. Persistent pipeline reuse

CF3 MUST NOT rebuild BP-DK pipelines per parameter.

`BpDkDevicePostUpdateRuntimeR1` now owns the producer through shared `Arc` authority and exposes a process-local producer handle for CF3.

Thus FreshGenesis source observation reuses the same persistent:

```text
reduction pipeline
pair pipeline
SHA-256 pipeline
```

already owned by BP-DK runtime.

---

## 20. Compact evidence collector

`BpDkFreshGenesisObservationCollectorCf3` is parameter-local metadata/evidence state.

It owns:

```text
shared producer handle
tile observation map
pair observation map
source identity attribution digest
compact D2H byte count
source observation SubmissionEpoch list
```

It does not own a duplicate full source tensor.

---

## 21. Exact tile/pair coverage

Before semantic receipt construction:

```text
observed_tile_count == expected_tile_count
observed_pair_count == expected_pair_count
```

Duplicate canonical tile or pair ordinals fail closed.

---

## 22. Source attribution digest

FreshGenesis source attribution digest binds:

```text
patch/source policy
canonical parameter
source generation
target generation
source physical allocation identities
canonical tile ordinals
batch provenance
```

It is an attribution identity, not a replacement for source tensor content SHA.

---

## 23. Existing semantic receipt SSOT

Final semantic authority remains:

```text
AshBpDkPostUpdateParameterReceipt
```

CF3 reconstructs it through the existing:

```text
AshBpDkPostUpdateStreamingBuilder::finalize_from_device_evidence_r1
```

No CF3-specific semantic receipt universe.

---

## 24. Compact finalization adapter

`BpDkDevicePostUpdateRuntimeR1` gains a compact-evidence finalization entry point for already-collected CF3 evidence.

It preserves the existing checks for:

```text
reduction policy
digest policy
full_candidate_d2h_bytes = 0
host_candidate_materialization_count = 0
semantic plan digest parity
```

---

## 25. CF4-CF2 assembly preservation

CF3 does not change the CF4-CF2 candidate assembly contract:

```text
candidate W/M/update copied pre-reclaim
copy SubmissionEpoch exact completion
coverage exact
gap_count = 0
overlap_count = 0
reclaim only after completed copy
```

---

## 26. C08 / P5 preservation

Current CANARY remains:

```text
B04 ActiveVerified
B05 ActiveDeviceCandidate
B06 ActiveVerified
C07 ActiveCompact
C08 MirrorVerified
```

CF3 does not claim:

```text
C08 ActiveAsync
P5 production queue cutover
exact-wait retirement
```

Exact waits are accepted physical safety boundaries in this non-promoting CANARY.

---

## 27. No optimizer math change

CF3 changes only evidence transport/lifetime authority.

No change to:

```text
Adam math
Muon math
orthogonalization
BP-DK semantic math
fusion planner policy
router policy
optimizer commit order
```

---

## 28. Source authority witnesses

FreshGenesis expected:

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

Later generation expected:

```text
selected_authority=COMMITTED_SEGMENTED
```

---

## 29. Source read witnesses

Before each live source reduction:

```text
[ASH-BP-DK-CF9-CF4-CF3][source-read-lease]
lease_state=ACQUIRED
```

After exact physical completion:

```text
lease_state=RELEASED_AFTER_EXACT_COMPLETION
submission_epoch=<real epoch>
```

---

## 30. Source buffer witness

Expected:

```text
[ASH-BP-DK-CF9-CF4-CF3][source-buffer]
authority=B04_ATLAS_WAVE_FRESH_GENESIS
weight_physical_allocation_ordinal=<real>
momentum_physical_allocation_ordinal=<real>
bpdk_source_d2h_bytes=0
bpdk_source_h2d_bytes=0
bpdk_source_gpu_copy_bytes=0
```

---

## 31. Source/target parity witness

Before final compact receipt:

```text
[ASH-BP-DK-CF9-CF4-CF3][source-target-parity]
generation_relation_exact=true
element_geometry_exact=true
device_exact=true
queue_exact=true
admitted=true
```

---

## 32. Parent failure retirement

For admitted FreshGenesis Atlas-wave source, CF3 must retire:

```text
E_CF9_CF4_SOURCE_GENERATION_MISSING
```

The token may remain valid only in the explicit `COMMITTED_SEGMENTED` branch when that branch's required source is actually absent.

---

## 33. Earlier failures remain retired

CF3 must not regress:

```text
BpDkPostUpdateCandidateCardinality
E_CF9_CF4_RESIDENT_PARTITION_VIEW_MISSING
E_DEVICE_SOFT_SUBGROUP_ARENA_PAGE_MISSING
```

---

## 34. Forbidden fixes

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

## 35. Static acceptance

Required:

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
canonical tile remap                                     present
canonical fused pair remap                               present
exact tile/pair coverage                                 present
CF4-CF2 candidate assembly                               preserved
existing semantic finalizer                              reused
```

---

## 36. Static validation record

Parent and CF3 observed identical historical validator results:

```text
R7A parent     79 / 83 PASS
R7A CF3        79 / 83 PASS

R7A1 parent    77 / 82 PASS
R7A1 CF3       77 / 82 PASS
```

The remaining failures are pre-existing source-pattern drift in those historical validators. No new CF3 validator regression was observed.

This static record is not compile or WGPU physical proof.

---

## 37. Compile acceptance

Required native authority:

```text
base_train --release --locked
```

Compile PASS must come from the user's native CF1 run.

The bake environment does not claim compilation.

---

## 38. Single-build CF1 law

Operational sequence:

```text
apply overlay
→ verify source hashes
→ touch modified source timestamps
→ native-cf1-release-compile-authority
   (base_train release build exactly once)
→ CF1 binary SHA == base_train.exe SHA
→ 2-step CANARY
```

Do not run a redundant standalone `cargo build base_train` before CF1.

---

## 39. Physical acceptance

One real CANARY must reach:

```text
CF4-CF2 assembly-seal admitted=true
↓
CF3 source-authority selected_authority=B04_ATLAS_WAVE_FRESH_GENESIS
↓
CF3 source-read-lease ACQUIRED
↓
CF3 source-buffer physical IDs
↓
CF3 source-read-lease RELEASED_AFTER_EXACT_COMPLETION
↓
CF3 source-target-parity admitted=true
↓
CF4 device-post-collect
↓
CF4 canonical post-receipt
```

with:

```text
full_candidate_d2h_bytes=0
host_candidate_materialization_count=0
bpdk_source_d2h_bytes=0
bpdk_source_h2d_bytes=0
bpdk_source_gpu_copy_bytes=0
```

---

## 40. PASS token

Reserved:

```text
PASS_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF9_CF4_CF3
```

Meaning:

> The BP-DK source authority is explicitly classified. Canonical committed segmented source remains authoritative when present. During FreshGenesis Atlas-wave streaming before segmented source installation, BP-DK reads the exact live source Weight/Momentum projection in place before reclaim, pins the read through a real SubmissionEpoch, retains only compact source-dependent observations, combines them with exact SHA-256 from the CF4-CF2 sealed target assembly, and reconstructs the existing canonical semantic receipt without source D2H, additional source H2D, source GPU duplication, fake segmented generation, or candidate ResidentGraph reconstruction.

---

## 41. Non-claims

CF3 does not claim:

```text
C08 ActiveAsync
P5 queue cutover
all exact waits retired
full BP-DK numerical qualification complete
full R1B campaign complete
A/B/C promotion complete
resource geometry final for all future generations
```

---

## 42. Code bake record

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

## 43. Artifacts

Full code-only:

```text
ASH_PASS3_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF9_CF4_CF3_BP_DK_SOURCE_AUTHORITY_FRESH_GENESIS_B04_LIVE_SOURCE_READ_CLOSURE_CODE_ONLY.zip
SHA-256: af8ddce448fa02c7b26e94394a208eb3d74e9cf067e2099cbb00f3f04833ab22
Files: 8424
CRC: PASS
specs/: 0
artifacts/: 0
```

Overlay code-only:

```text
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
