# ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF9-CF4

## BP-DK ACTIVE-DEVICE POST-UPDATE
## C08-MIRROR COMPACT-EVIDENCE / HOST-VEC RETIREMENT CLOSURE

```text
+ B05 ACTIVE-DEVICE-CANDIDATE HOST-VEC EMPTY PRESERVATION
+ B05 BULK-READBACK-FALSE AUTHORITY PRESERVATION
+ C08 MIRROR NON-P5 DEVICE POST-UPDATE PATH
+ POST-UPDATE PATH SELECTION BY CANDIDATE AUTHORITY
+ DEVICE COMPACT-EVIDENCE PRODUCER REUSE
+ PARAMETER-LOCAL GPU CANDIDATE ASSEMBLY
+ EXISTING B04 RESIDENT PARTITION SOURCE REUSE
+ CANONICAL 256-ELEMENT TILE REDUCTION PRESERVATION
+ EXACT CANDIDATE SHA-256 DIGEST PRESERVATION
+ EXISTING AshBpDkPostUpdateParameterReceipt RECONSTRUCTION
+ PARAMETER-LOCAL EXACT-WAIT COLLECTION
+ FULL CANDIDATE D2H = 0
+ HOST CANDIDATE MATERIALIZATION = 0
+ ACTIVE-ASYNC DEVICE POST PATH PRESERVATION
+ MIRROR / OFF HOST POST PATH PRESERVATION
+ NO C08 ACTIVE-ASYNC CLAIM
+ NO P5 CUTOVER CLAIM
+ NO ZERO-FILLED HOST CANDIDATE FABRICATION
```

---

## 0. Revision identity

```text
Patch ID:
ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF9-CF4

Class:
BP-DK POST-UPDATE AUTHORITY SELECTION / DEVICE COMPACT EVIDENCE CLOSURE

Direct parent:
ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF9-CF3
```

Parent code-only archive:

```text
SHA-256:
ffe69c9b7907773cdb05041141b47fed4d5b23e76b30ea150c48c0135364a429
```

---

## 1. Physical blocker entering CF4

CF9-CF3 physically crossed:

```text
Legacy A02 subgroup owner-scope isolation
R7A packed reader object resolution
packed-reader-object same_buffer_arc=true
```

The next first failure was:

```text
BpDkPostUpdateCandidateCardinality
```

The physical run therefore reached BP-DK post-update after the prior arena/resource closures.

---

## 2. Root cause

For:

```text
B05 = ActiveDeviceCandidate
```

the production candidate path intentionally reports:

```text
candidate_weight = []
candidate_momentum = []
orthogonal_update = []

candidate_weight_d2h_bytes = 0
candidate_momentum_d2h_bytes = 0
update_d2h_bytes = 0
host_candidate_vec_materialization_count = 0
```

This is the existing B05 authority contract.

The old post-update fallback nevertheless called the host full-vector builder whenever P5 ActiveAsync was not selected. The host builder requires full `tile_count × 256` candidate vectors and therefore rejected the correct empty host vectors with:

```text
BpDkPostUpdateCandidateCardinality
```

---

## 3. Core law

BP-DK post-update observation authority follows **candidate data authority**, not queue scheduling mode.

```text
B05 ActiveDeviceCandidate
    -> DeviceCompactCandidate

B05 MirrorVerified / Off
    -> existing host authority
```

C08/P5 state does not redefine where candidate data lives.

---

## 4. CF7 non-promoting profile support

The existing CANARY profile remains:

```text
B04 ActiveVerified
B05 ActiveDeviceCandidate
B06 ActiveVerified
C07 ActiveCompact
C08 MirrorVerified
promotion_claim=false
```

CF4 allows device compact BP-DK observation in this profile without claiming C08 ActiveAsync or P5 production queue cutover.

---

## 5. Existing BP-DK device authority preserved

CF4 reuses the existing:

```text
BpDkDevicePostUpdateRuntimeR1
TensorCubeBpDkDevicePostUpdateProducerR1
AshBpDkPostUpdateStreamingBuilder::finalize_from_device_evidence_r1
```

No new WGSL reduction or SHA implementation is introduced.

Existing canonical contracts remain:

```text
256-element tile reduction
pair cosine evidence
zero-norm / nonfinite status
candidate Weight SHA-256
candidate Momentum SHA-256
orthogonal Update SHA-256
full_candidate_d2h_bytes = 0
host_candidate_materialization_count = 0
```

---

## 6. Parameter-local GPU assembly

The ordinary B05 path produces device candidate data in exact resident partitions rather than one contiguous host vector.

CF4 materializes a temporary **GPU-only parameter-local contiguous assembly** for:

```text
candidate Weight
candidate Momentum
orthogonal Update
```

using copies from existing B04 resident candidate partitions.

No candidate element crosses to host.

---

## 7. Resident partition view authority

`MuonResidentStateGraph` adds a read-only exact partition-view lookup by existing partition digest.

The returned view contains the already-authoritative:

```text
candidate Weight Arc<Buffer>
candidate Momentum Arc<Buffer>
update Scratch Arc<Buffer>

physical allocation identities
partition identity
source / candidate generation
```

No second candidate producer is introduced.

---

## 8. Exact canonical copy map

CF4 reuses `b05_candidate_write_segments(...)` as the semantic-to-physical tile mapping authority.

For each segment:

```text
source partition offset
    = partition_element_start

destination parameter-local offset
    = canonical_muon_element_start - momentum_base_element_offset
```

The copied extent remains the exact segment `element_count`.

This preserves local/fused tile canonical ordering without host reconstruction.

---

## 9. Allocation parity guards

Before each GPU copy, the resident partition view must match the B05 write segment for:

```text
candidate_weight_allocation
candidate_momentum_allocation
update_scratch_allocation
```

Mismatch fails closed.

---

## 10. A01 lifetime tracking

GPU assembly copies are submitted under existing A01 lease authority.

Source candidate/update ranges are read-only logical submission leases.

Target assembly Weight/Momentum/Update are write leases.

The path uses an exact wait because CF7 C08 is MirrorVerified and CF4 makes no async-retirement claim.

---

## 11. Assembly handoff

After exact copy completion, the existing `MuonDeviceParameterAssemblyR2` produces the existing:

```text
LocalMuonDeviceSegmentedHandoffR1
```

which is published through:

```text
publish_local_muon_segmented_handoff_r1
```

into the existing target segmented generation and BP-DK update-evidence arena.

No fake generation or alternate receipt universe is introduced.

---

## 12. Source generation authority

The BP-DK producer consumes the existing committed segmented Muon source generation.

CF4 does not rebuild the source from host vectors.

---

## 13. Device compact submission

After parameter-local target handoff publication, CF4 calls the existing device post-update runtime:

```text
submit_parameter
collect_parameter_after_exact_wait_r1a
```

The existing semantic builder is passed through unchanged.

---

## 14. Host-vector preservation

Under `ActiveDeviceCandidate`, CF4 explicitly requires:

```text
candidate_weight.is_empty()
candidate_momentum.is_empty()
orthogonal_update.is_empty()

host_candidate_vec_materialization_count == 0
candidate Weight/Momentum/Update D2H == 0
```

A non-empty host candidate is treated as authority drift.

---

## 15. Host builder fail-closed guard

If B05 remains `ActiveDeviceCandidate` and execution somehow reaches the legacy full host post-update builder, fail with:

```text
E_CF9_CF4_BP_DK_HOST_POST_BUILDER_REACHED_UNDER_ACTIVE_DEVICE
```

Do not reinterpret empty vectors as a zero-valued candidate.

---

## 16. No zero-fill repair

Forbidden:

```text
vec![0.0; expected_elements]
```

for Weight, Momentum or Update merely to satisfy host cardinality.

---

## 17. No full candidate D2H

Forbidden:

```text
ActiveDeviceCandidate -> full candidate readback -> host builder
```

CF4 device compact evidence must maintain:

```text
full_candidate_d2h_bytes = 0
host_candidate_materialization_count = 0
```

---

## 18. Existing semantic SSOT

The final post-update semantic authority remains:

```text
AshBpDkPostUpdateParameterReceipt
```

The device path reconstructs the same receipt using existing compact-evidence finalization.

---

## 19. C08/P5 non-claims

CF4 does not claim:

```text
C08 ActiveAsync
P5 production pending queue cutover
per-wave exact-wait retirement
multi-wave async completion
```

The CF4 exact wait is parameter-local evidence collection only.

---

## 20. Existing ActiveAsync preservation

When P5 ActiveAsync is actually selected, the existing ActiveAsync device post path remains canonical.

CF4 synchronous device evidence is selected only when:

```text
B05 ActiveDeviceCandidate
AND
active_async_parameter_r2 == false
```

No double device evidence submission.

---

## 21. Mirror / Off preservation

For B05 `MirrorVerified` or `Off`, the existing host post-update authority remains unchanged.

CF4 does not globally replace host post-update behavior.

---

## 22. Physical witnesses

CF4 emits:

```text
[ASH-BP-DK-CF9-CF4][post-authority]
```

with:

```text
B05 mode
P5 active state
expected elements
host candidate lengths
device candidate backing count
selected authority
assembly submission epoch
```

and:

```text
[ASH-BP-DK-CF9-CF4][device-post-collect]
```

with:

```text
full_candidate_d2h_bytes
host_candidate_materialization_count
tile observation count
pair observation count
digest presence
```

and:

```text
[ASH-BP-DK-CF9-CF4][post-receipt]
```

with the canonical semantic receipt identity.

---

## 23. Expected current physical witness

For the current CF7 CANARY:

```text
b05_mode=ActiveDeviceCandidate
p5_active=false
candidate_weight_host_len=0
candidate_momentum_host_len=0
orthogonal_update_host_len=0
selected_authority=DeviceCompactCandidate
```

Then compact collection must show:

```text
full_candidate_d2h_bytes=0
host_candidate_materialization_count=0
```

---

## 24. Previous blocker retirement

The ordinary CF7 ActiveDeviceCandidate path must no longer terminate on:

```text
BpDkPostUpdateCandidateCardinality
```

If the error persists, CF4 authority selection was not reached.

---

## 25. Parent preservation

CF4 does not modify:

```text
CF9-CF3 A02 subgroup ownership isolation
CF9-CF2 R7A domain-owned Buffer authority
CF9-CF1 R7A domain ordering
CF9 byte/page geometry
CF8 lease geometry
CF7 D10/C08 profile
```

---

## 26. Static acceptance

Required:

```text
ActiveDeviceCandidate selects DeviceCompactCandidate
C08 Mirror does not force host post builder
host candidate vectors remain empty
full candidate D2H remains zero
existing BP-DK producer reused
existing BP-DK shaders reused
existing semantic receipt reused
parameter-local assembly remains GPU-only
resident partition allocation parity guarded
host builder fail-closed under ActiveDeviceCandidate
Mirror/Off host path preserved
ActiveAsync path preserved
```

---

## 27. Build / physical workflow

Use the single-build CF1 flow:

```text
overlay apply
source SHA verification
CF1 release compile authority
    -> base_train release build exactly once
CF1 == EXE hash verification
2-step CANARY
```

Do not run a separate full `cargo build base_train` immediately before CF1.

---

## 28. Physical PASS boundary

CF4 is physically supported when one CANARY proves:

```text
B05 ActiveDeviceCandidate
C08 MirrorVerified
host candidate vectors empty
DeviceCompactCandidate selected
GPU assembly succeeds
compact BP-DK evidence collected
full candidate D2H = 0
host candidate materialization = 0
canonical post-update receipt reconstructed
BpDkPostUpdateCandidateCardinality retired
```

---

## 29. PASS token

```text
PASS_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF9_CF4
```

---

## 30. Non-claims

CF4 does not claim:

```text
C08 ActiveAsync complete
P5 complete
full 2-step CANARY complete
R3B complete
Full R1B complete
A/B/C promotion complete
```

---

# Appendix A. Actual source bake record

```text
Parent files: 8424
ADD: 0
MOD: 3
DEL: 0
Output files: 8424
```

Modified:

```text
c998335547bcf0a782a39d8d405f656ce12c4485c7bb6068229cf7a486ea17b9
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs

0886a4aae7dbce2ccfcaf3e4e16ef7debde20ccccba21aae457f2abcb3aae340
crates/burn_webgpu_backend/src/base_train_tensorcube_local_muon_active_device_pending_r1.rs

87e6c13cf01babc4958ba9078cfacb3edc881a80b7e7b242e320810661dcf6ce
crates/burn_webgpu_backend/src/muon_resident_state_graph.rs
```

Full code-only archive:

```text
ASH_PASS3_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF9_CF4_BP_DK_ACTIVE_DEVICE_POST_UPDATE_C08_MIRROR_COMPACT_EVIDENCE_HOST_VEC_RETIREMENT_CLOSURE_CODE_ONLY.zip
SHA-256: 355a8dc407b0ba47ac4b9e3dbbd0f9e6a5505bb3b9db14abe3eb4ca9f86464b2
Files: 8424
CRC: PASS
specs/: 0
artifacts/: 0
```

Overlay code-only archive:

```text
ASH_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF9_CF4_BP_DK_ACTIVE_DEVICE_POST_UPDATE_C08_MIRROR_COMPACT_EVIDENCE_HOST_VEC_RETIREMENT_CLOSURE_OVERLAY_CODE_ONLY.zip
SHA-256: c5d930eea4e366cb1171bae8761779e8fdc519b6e16d752e79d2d8fa7ca8b293
Files: 3
CRC: PASS
```

Rust compile / GPU physical PASS are not claimed by the bake environment.

---

# Final law

> BP-DK post-update evidence follows candidate data authority, not queue scheduling mode.
>
> Under B05 ActiveDeviceCandidate, empty host candidate vectors are the correct authority state.
>
> CF9-CF4 assembles the existing device candidate partitions on GPU, reuses the existing compact BP-DK reduction/SHA implementation, and reconstructs the existing semantic receipt without full candidate D2H.
>
> C08 Mirror remains Mirror. P5 remains unclaimed. No fake host vector is created.
