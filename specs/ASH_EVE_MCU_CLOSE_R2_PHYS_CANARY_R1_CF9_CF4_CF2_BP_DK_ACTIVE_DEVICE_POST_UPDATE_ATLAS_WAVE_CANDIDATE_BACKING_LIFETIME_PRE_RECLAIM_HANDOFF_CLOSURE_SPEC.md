# ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF9-CF4-CF2

## BP-DK ACTIVE-DEVICE POST-UPDATE
## ATLAS-WAVE CANDIDATE BACKING LIFETIME + PRE-RECLAIM HANDOFF CLOSURE

```text
+ ATLAS-WAVE BACKING KEY / RESIDENT-PARTITION KEY SEPARATION
+ NO RESIDENT-GRAPH VIEW LOOKUP FOR ATLAS-WAVE BACKINGS
+ CANDIDATE W/M/UPDATE PRE-RECLAIM DEVICE HANDOFF
+ PARAMETER-LOCAL ASSEMBLY DURING LIVE WAVE BACKING LIFETIME
+ EXACT CANDIDATE / UPDATE RANGE COPY
+ ASSEMBLY SUBMISSION EPOCH OWNERSHIP
+ DURABLE COMMITTED SOURCE AUTHORITY REUSE
+ RECLAIM ONLY AFTER ASSEMBLY COPY COMPLETION
+ MULTI-WAVE PARAMETER ASSEMBLY COVERAGE LEDGER
+ EXACT NON-OVERLAP / NO-GAP RANGE ADMISSION
+ EXISTING CF4 DEVICE COMPACT BP-DK PRODUCER REUSE
+ FULL CANDIDATE D2H = 0
+ HOST CANDIDATE MATERIALIZATION = 0
+ C08 MIRROR PRESERVATION
+ NO P5 CUTOVER CLAIM
+ NO KEY SUFFIX STRIPPING
+ NO STALE PHYSICAL ALLOCATION LOOKUP
+ NO DUPLICATE SOURCE PHYSICAL AUTHORITY
```

## 0. Revision

```text
Patch ID: ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF9-CF4-CF2
Class: PHYSICAL BACKING LIFETIME / PRE-RECLAIM DEVICE HANDOFF CLOSURE
Direct code parent: ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF9-CF4-CF1
Semantic parent: ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF9-CF4
```

Parent code-only archive:

```text
ASH_PASS3_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF9_CF4_CF1_MUON_DEVICE_CANDIDATE_WRITE_SEGMENT_IMPORT_COMPILEFIX_CODE_ONLY.zip
SHA-256: 681e127ba1fbbb77af45d5f5f3fd6875386cd0df67283c1374cd06a193a12005
```

CF4-CF1 was compile-only and introduced no semantic change.

## 1. Entering physical blocker

The CANARY had already crossed CF9-CF2 R7A object ownership, CF9-CF3 A02 subgroup reuse scope, and packed-gradient producer/reader same-buffer parity. CF4 then retired the old host-vector cardinality blocker and reached:

```text
E_CF9_CF4_RESIDENT_PARTITION_VIEW_MISSING:<partition>:slot:<N>:wave:<M>
```

Classification:

```text
POST-CANDIDATE BACKING LIFETIME / IDENTITY-DOMAIN MISBINDING
```

## 2. Root cause

Atlas-wave candidate keys and ResidentGraph partition keys are separate authorities. They must not be reconciled by suffix removal or string rewriting.

More importantly, Atlas-wave candidate Weight, candidate Momentum and orthogonal Update are backed by transient A02 arena leases. Recording a `PhysicalAllocationId` does not extend Buffer lifetime. The prior CF4 outer flow was invalid:

```text
record transient allocation metadata
→ reclaim live wave backing
→ later lookup through ResidentGraph
→ assemble BP-DK target
```

## 3. Closure law

For transient Atlas-wave candidate surfaces:

```text
GPU→GPU HANDOFF COMPLETION
must precede
ORIGINAL WAVE BACKING RECLAIM
```

CF4-CF2 moves the handoff into local/fused physical executors while exact candidate/update Buffer objects are still live.

## 4. Existing authority reuse

No new memory framework or WGSL is introduced. CF4-CF2 reuses:

```text
MuonDeviceParameterAssemblyR2
```

which already owns parameter-local Weight/Momentum/Update assembly, exact range reservation/completion, real SubmissionEpoch history, and final segmented target/update-evidence handoff.

New typed live range:

```text
MuonDeviceLiveCopyRangeCf4Cf2 {
    source_element_start,
    parameter_element_start,
    element_count,
}
```

## 5. Source SSOT refinement

The current CF7 path already has a durable canonical source:

```text
self.mcu.committed_device_source.muon
```

The existing BP-DK device runtime obtains the exact source read lease from this segmented committed source. CF4-CF2 therefore does **not** create a redundant full source assembly.

Concrete authority split:

```text
source W/M       = COMMITTED_DEVICE_SEGMENTED SSOT
candidate W/M    = pre-reclaim parameter assembly
orthogonal Update= pre-reclaim parameter assembly
```

Witnesses report:

```text
source_authority=COMMITTED_DEVICE_SEGMENTED
source_copy_required=false
```

This avoids duplicate source physical authority while preserving the source lease through BP-DK physical completion.

## 6. Local-wave handoff

After the local candidate submission reaches exact completion, but before candidate arenas are reclaimed:

```text
candidate Weight
candidate Momentum
orthogonal Update
```

are copied GPU→GPU into canonical parameter offsets in `MuonDeviceParameterAssemblyR2`.

Destination authority is existing descriptor geometry:

```text
gradient_tile_base_element_offset
```

No Atlas key parsing occurs.

## 7. Fused-wave handoff

Each fused pair contributes two canonical 256-element ranges:

```text
lhs → lhs_gradient_base_element_offset
rhs → rhs_gradient_base_element_offset
```

Transient pair-local source layout is copied into canonical parameter order. No host concatenation is used.

## 8. Exact range and coverage contract

Every range must satisfy:

```text
element_count > 0
checked source/destination arithmetic
destination end <= parameter element count
source byte end <= live candidate/update reserved bytes
```

The existing assembly ledger remains SSOT:

```text
reserved_ranges
completed_ranges
```

Final admission requires exact continuity:

```text
0 .. expected_element_count
gap_count = 0
overlap_count = 0
```

No last-write-wins, no duplicate start, no wave-count heuristic.

## 9. Real copy SubmissionEpoch

Each live handoff encodes real `copy_buffer_to_buffer` commands for candidate Weight, candidate Momentum and Update, then submits through existing A01 authority:

```text
a01_submit_with_leases
→ real SubmissionEpoch
→ a01_wait_for_submission_exact
→ a01_release_submission_leases
→ mark range complete
```

Only after that boundary does existing candidate/update A02 reclaim execute.

## 10. Reclaim ordering

Required concrete order:

```text
candidate compute exact completion
→ original candidate submission leases released
→ CF4-CF2 live candidate/update copy submitted
→ assembly copy exact completion
→ CF4-CF2 copy leases released
→ range completion committed
→ existing candidate/update A02 reclaim
```

No reclaimed allocation is reopened later.

## 11. ResidentGraph separation

The CF4 active-device outer callsite no longer calls `partition_view_by_key_cf4()` for Atlas-wave candidate backings. `device_candidate_backings` may remain telemetry/provenance, but it is not a lifetime-resurrection mechanism.

Forbidden:

```text
slot/wave suffix stripping
fake ResidentGraph alias insertion
stale PhysicalAllocationId reopening
search-all-subgroups fallback
```

## 12. Parameter seal and downstream BP-DK

After exact assembly coverage, CF4-CF2 finalizes the existing assembly into:

```text
MuonDeviceSegmentBackingR1
BpDkDeviceUpdateEvidenceBackingR1
```

and reuses the existing CF4 BP-DK device path for reduction, pair cosine, canonical SHA-256, compact readback and `AshBpDkPostUpdateParameterReceipt` reconstruction.

No CF4-CF2 shader is added.

## 13. Required host/D2H invariants

```text
candidate_weight host Vec = empty
candidate_momentum host Vec = empty
orthogonal_update host Vec = empty
full_candidate_d2h_bytes = 0
host_candidate_materialization_count = 0
```

No zero-filled host fallback is accepted.

## 14. C08 / P5 boundary

The pre-reclaim copy uses an exact wait as a physical lifetime safety boundary under the CF7 CANARY. It does not claim:

```text
C08 ActiveAsync
P5 production pending-wave cutover
all per-parameter synchronization retired
```

C08 remains `MirrorVerified`.

## 15. Required witnesses

```text
[ASH-BP-DK-CF9-CF4-CF2][assembly-begin]
[ASH-BP-DK-CF9-CF4-CF2][wave-handoff]
[ASH-BP-DK-CF9-CF4-CF2][assembly-submit]
[ASH-BP-DK-CF9-CF4-CF2][assembly-complete]
[ASH-BP-DK-CF9-CF4-CF2][pre-reclaim]
[ASH-BP-DK-CF9-CF4-CF2][assembly-seal]
```

Required handoff fields:

```text
resident_graph_lookup=false
source_authority=COMMITTED_DEVICE_SEGMENTED
source_copy_required=false
candidate_weight_live=true
candidate_momentum_live=true
update_live=true
```

Required pre-reclaim fields:

```text
assembly_epoch_completed=true
range_committed=true
action=RECLAIM_WAVE_BACKINGS
```

Required seal:

```text
covered_elements=expected_elements
gap_count=0
overlap_count=0
candidate_complete=true
update_complete=true
admitted=true
```

## 16. Expected existing CF4 witnesses after seal

```text
[ASH-BP-DK-CF9-CF4][post-authority]
selected_authority=DeviceCompactCandidate

[ASH-BP-DK-CF9-CF4][device-post-collect]
full_candidate_d2h_bytes=0
host_candidate_materialization_count=0
```

## 17. Forbidden fixes

```text
NO key suffix stripping
NO fake ResidentGraph aliases
NO stale allocation resurrection
NO zero-filled candidate buffer
NO full candidate D2H
NO host candidate reconstruction
NO duplicate source assembly
NO forced C08 ActiveAsync
NO P5 enablement solely to avoid lifetime closure
NO speculative resource-budget increase
```

## 18. Static acceptance

Required source properties:

```text
CF4 outer Atlas ResidentGraph lookup = 0
local pre-reclaim live-copy path = materialized
fused pre-reclaim live-copy path = materialized
parameter assembly created before candidate execution
real A01 copy SubmissionEpoch = used
exact wait before existing backing reclaim = yes
exact coverage ledger = reused
source authority = committed segmented source
candidate/update assembly = device resident
new WGSL = 0
full host candidate materialization = 0
```

## 19. Static validation performed

Modified Rust delimiter/syntax-structure scan:

```text
PASS 4 / 4
```

Parent vs child relevant validators:

```text
R7A  parent 79/83  child 79/83
R7A1 parent 77/82  child 77/82
```

The failures are the same pre-existing source-pattern drift. No new validator failure was introduced by CF4-CF2.

The active-device-pending historical validator also fails on both parent and child because it already forbids the pre-existing `a01_wait_for_submission_exact` symbol. The parameter-lifetime validator requires a spec excluded from code-only archives, so it cannot run on either code-only tree.

## 20. Qualification state

The bake environment has no Cargo/Rustc.

```text
SOURCE MATERIALIZATION = CONFIRMED
STATIC DELTA CHECK      = CONFIRMED
RUST COMPILE            = NOT RUN
PHYSICAL CANARY         = HOLD
```

Compile/native authority is established only by the user's CF1 single-build run.

## 21. Single-build CF1 law

```text
apply overlay
→ verify modified source SHA
→ touch modified Rust mtimes
→ native CF1 release compile authority
   (base_train release build exactly once)
→ CF1 binary SHA == current base_train.exe SHA
→ no further source/build modification
→ 2-step CANARY
```

Do not run a separate full `cargo build base_train` immediately before CF1.

## 22. Physical acceptance

A real CANARY must show:

```text
assembly-begin
→ wave-handoff
→ assembly-submit
→ assembly-complete
→ pre-reclaim
→ assembly-seal
→ post-authority DeviceCompactCandidate
→ device-post-collect
```

and must not fail first with:

```text
BpDkPostUpdateCandidateCardinality
E_CF9_CF4_RESIDENT_PARTITION_VIEW_MISSING
```

Any later fail-closed error becomes the next physical boundary.

Reserved physical token:

```text
PASS_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF9_CF4_CF2
```

The static bake does not emit this token.

## 23. Bake record

```text
Direct parent files: 8424
ADD: 0
MOD: 4
DEL: 0
```

Modified source SHA-256:

```text
524e5783f251f5292b571ba5b710eba4f5c8164cb2a977b20ab727b6f7525882  crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
b835231b7aa2a8a52c30754b5ad0d043d769b5c4e9a9ad2e5558656908e1e075  crates/burn_webgpu_backend/src/base_train_tensorcube_local_muon.rs
690e65389cd1ad3a6928733b6504be0ab2256997fd66aa469cc4f4000e839f98  crates/burn_webgpu_backend/src/base_train_tensorcube_local_muon_active_device_pending_r1.rs
428d5bc4dec9b27183f996a9f56a7373f04c5d3659d30c1b0e4b18778ae77c87  crates/burn_webgpu_backend/src/tensorcube_fused_pair_muon.rs
```

Full code-only bake:

```text
ASH_PASS3_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF9_CF4_CF2_BP_DK_ACTIVE_DEVICE_POST_UPDATE_ATLAS_WAVE_CANDIDATE_BACKING_LIFETIME_PRE_RECLAIM_HANDOFF_CLOSURE_CODE_ONLY.zip
SHA-256: d1d2d1571d7ef4d0a01c0887aaf3c8412da69411516d5319916e5cb34c751e2f
Files: 8424
CRC: PASS
specs/: 0
artifacts/: 0
```

Overlay code-only bake:

```text
ASH_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF9_CF4_CF2_BP_DK_ACTIVE_DEVICE_POST_UPDATE_ATLAS_WAVE_CANDIDATE_BACKING_LIFETIME_PRE_RECLAIM_HANDOFF_CLOSURE_OVERLAY_CODE_ONLY.zip
SHA-256: 90932e46aac28057f773152fae5667686d019c4bb5e43f7bd90da866b869b186
Files: 4
CRC: PASS
```

## 24. Final law

> Atlas-wave candidate identity and ResidentGraph partition identity remain separate authorities. No string rewrite may merge them.
>
> PhysicalAllocationId does not extend lifetime. Transient candidate Weight, candidate Momentum and Update are copied into parameter assembly while their original Buffer objects are live.
>
> The copy owns a real SubmissionEpoch, and original wave resources are reclaimed only after exact copy completion.
>
> Source Weight/Momentum are not redundantly copied because the committed segmented source is already the canonical durable source and the existing BP-DK runtime owns its exact read lease.
>
> Multi-wave assembly admits only exact non-overlapping gap-free canonical parameter coverage.
>
> No host candidate materialization, no full candidate D2H, no stale allocation resurrection, no ResidentGraph alias, and no C08/P5 promotion claim.
