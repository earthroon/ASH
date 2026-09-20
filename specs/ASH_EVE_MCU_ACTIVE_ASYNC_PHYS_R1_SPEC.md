# EVE-MCU-ACTIVE-ASYNC-PHYS-R1

## C08 / P5 ACTIVE-ASYNC PHYSICAL CAMPAIGN AUTHORITY

```text
+ DISTINCT ACTIVE-ASYNC CANARY PROFILE
+ C08 ACTIVE-ASYNC ADMISSION
+ P5 ACTIVE-ASYNC ADMISSION
+ B04 ACTIVE VERIFIED PRESERVATION
+ B05 ACTIVE DEVICE CANDIDATE PRESERVATION
+ B06 ACTIVE VERIFIED PRESERVATION
+ C07 ACTIVE COMPACT PRESERVATION
+ TENSORCUBE-CONSUME-R2 ACTIVE VERIFIED REACHABILITY
+ REAL MUON DEVICE SUCCESSOR TICKET
+ NO PROFILE SPOOF
+ NO MIRRORVERIFIED CLAIM REUSE
+ R3H / CF11 / RAM36 PRESERVATION
+ BPDK CHECKPOINT R1 PRESERVATION
```

## 0. Parent

Direct parent:

```text
ASH_PASS3_BPDK_CHECKPOINT_R1_TENSORCUBE_R2_COMPILEFIX1_CODE_ONLY.zip
SHA-256 42dc9393dddf7e14bab9071fa8a89fe19aac6ecbc3d8a35077065ccf9c701adf
```

## 1. New campaign identity

A new CLI is added:

```text
--eve-mcu-active-async-phys-canary-r1
```

The existing:

```text
--eve-mcu-close-r2-phys-canary-r1
```

remains unchanged and continues to represent the MirrorVerified C08 canary.

The new campaign uses a distinct D10 unpublished authority class:

```text
RuntimePublicationAuthorityClass::ActiveAsyncPhysicalCanary
UnpublishedRuntimeProfileClass::ActiveAsyncPhysicalCanary
```

Its D10 runtime digest is:

```text
D10_ACTIVE_ASYNC_PHYSICAL_CANARY_R1
```

No R3bPhysicalAttributionCanary receipt is reused as ActiveAsync evidence.

## 2. Exact runtime profile

The new campaign seals or verifies the exact environment profile:

```text
B04 ASH_MUON_RESIDENT_STATE_MODE=ACTIVE_VERIFIED
B05 ASH_HIMUON_DEVICE_CANDIDATE_MODE=ACTIVE_DEVICE_CANDIDATE
B06 ASH_HYBRID_DEVICE_COMMIT_MODE=ACTIVE_VERIFIED
C07 ASH_GPU_EVIDENCE_MODE=ACTIVE_COMPACT
C08 ASH_C08_ASYNC_SUBMISSION_RETIREMENT_MODE=ACTIVE_ASYNC
P4  ASH_UNIFIED_ATLAS_MCU_EXACT_ATLAS_SLOT_LEASE_GENERATION_R1=ACTIVE_EXACT_LEASE
P5  ASH_UNIFIED_ATLAS_MCU_SUBMISSION_EPOCH_DEPENDENCY_ACTIVE_ASYNC_R1=ACTIVE_ASYNC
P5 qualification=1
P5 max_in_flight_waves>=2
TensorCube Consume R2=ACTIVE_VERIFIED
BP-DK Checkpoint R1=ACTIVE_VERIFIED
```

Missing settings are filled by the campaign CLI. Pre-existing conflicting values fail closed with:

```text
E_ACTIVE_ASYNC_PHYS_R1_PROFILE_ENV_CONFLICT
```

A stale D09 benchmark lane is forbidden:

```text
E_ACTIVE_ASYNC_PHYS_R1_D09_LANE_FORBIDDEN
```

## 3. D10 classification

The active runtime profile already shares the exact B04/B05/B06/C07/C08 mode tuple used by the D09 physical candidate. R1 does not spoof the D09 lane.

Classification now distinguishes:

```text
active tuple + canary_mode=true + no D09 lane
    -> ActiveAsyncPhysicalCanary

active tuple + D09 C08 candidate lane
    -> D09PhysicalCandidate

MirrorVerified C08 tuple + canary_mode=true
    -> R3bPhysicalAttributionCanary
```

The three authority classes remain distinct.

## 4. Runtime reachability seal

When the D10 admission class is ActiveAsyncPhysicalCanary, ProductionMuonRuntime requires:

```text
B04 active verified
B05 active device candidate
B06 active verified
C07 active compact
C08 active async
P4 exact atlas lease active
P5 dependency mode active async
P5 max_in_flight_waves >= 2
production pending-wave queue cutover active
TensorCube Consume R2 ActiveVerified
BP-DK Checkpoint R1 ActiveVerified
```

Failure of any condition aborts before claiming ActiveAsync physical admission.

Successful construction emits:

```text
[ASH-EVE-MCU-ACTIVE-ASYNC-PHYS-R1][runtime-seal]
```

## 5. CLI campaign seal

The new CLI emits:

```text
[ASH-EVE-MCU-ACTIVE-ASYNC-PHYS-R1][cli-seal]
```

before entering the existing two-step physical canary runner.

The underlying two-step source/genesis/config machinery is reused. This avoids forking model, dataset, RAM36, CF11, R8A, BP-DK, or scheduler semantics merely to change the C08/P5 physical profile.

## 6. Terminal receipt

The wrapper emits:

```text
[ASH-EVE-MCU-ACTIVE-ASYNC-PHYS-R1][terminal]
```

with either the completed target or the actual first failure. It does not convert a failing B06/R3C1 condition into a pass.

## 7. B06 preservation

The existing gates remain unchanged:

```text
FAIL_B06_CANDIDATE_NOT_COMPLETE:muon-device-successor-missing
FAIL_B06_CANDIDATE_NOT_COMPLETE:muon-successor-submission-drift
```

The campaign is intended to make TensorCube Consume R2 physically reachable so that a real Muon device-successor ticket can populate the existing B06 ledger.

No synthetic ticket and no gate relaxation are introduced in this revision.

## 8. Parent physical closure preservation

No source code in CF11, RAM36, R8A, packed-MV, TensorCube R1/R2 execution, or BP-DK checkpoint capture is changed by this bake.

The next physical run must preserve previously observed laws:

```text
source retired before successor reservation
workspace dead before successor reservation
full_candidate_heap_allocation_count=0
successor d2h_bytes=0
full_temporary_copy_count=0
BP-DK checkpoint same_encoder_parameters=154
BP-DK checkpoint per_parameter_submits=0
BP-DK checkpoint per_parameter_maps=0
BP-DK checkpoint blocking_waits=0
```

## 9. Changed files

```text
MOD crates/base_train/src/bin/base_train.rs
MOD crates/base_train/src/d10_production_ssot_publication.rs
MOD crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
ADD tools/validate_ash_eve_mcu_active_async_phys_r1_static.py
```

Delta:

```text
MOD 3
ADD 1
DEL 0
```

## 10. Source SHA-256

```text
1d31a14649b61d8961071ccbc26ce568ed402cb1a919d58ba87ab638be1ca9c7  crates/base_train/src/bin/base_train.rs
a07067f4fd75d37e5760e7d2b47555f31bcda255b87962852153e5ee532ac1a7  crates/base_train/src/d10_production_ssot_publication.rs
24e600054d10c404edc161c7406458b9ccdbc27a6745d0cb667c7e9fb731d84b  crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
b71139f723441e1db8258219c96cb63df9ab3bf3c11dfcac0878ae049af9db06  tools/validate_ash_eve_mcu_active_async_phys_r1_static.py
```

## 11. Static qualification

```text
PASS_EVE_MCU_ACTIVE_ASYNC_PHYS_R1_STATIC checks=37
PASS_TENSORCUBE_CONSUME_R2_GPU_PARALLEL_PLANE_STATIC checks=61
PASS_BP_DK_CHECKPOINT_R1_GPU_HOT_CAPTURE_STATIC checks=46
PASS_TENSORCUBE_CONSUME_R1_RELATION_AUTHORITY_STATIC checks=56
PASS_EVE_MCU_R3H_CF11_R1_CF1_CF1_CF1_CF1_CF1_CF1_RAM36_CURRENT_SOURCE_PROMOTION_STATIC checks=32
PASS_EVE_MCU_R3H_CF11_R1_BOUNDED_COW_WORKSPACE_STATIC checks=22
PASS_EVE_MCU_R3H_CF11_R1_CF1_CF1_CF1_CF1_CF1_BPDK_GENERATION_BINDING_STATIC checks=27
PASS_EVE_MCU_R3H_CF11_R1_CF1_CF1_CF1_R8A_PREDURABILITY_SEAL_STATIC checks=30
PASS_EVE_MCU_R3H_CF11_R1_CF1_CF1_MUON_PACKED_ADDRESS_STATIC checks=26
PASS_EVE_MCU_R3H_CF11_R1_CF1_PACKED_MV_DIGEST_STATIC checks=27
PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_ACTIVE_ASYNC_COMPLETION_R1_STATIC
PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_LOCAL_MUON_PRODUCTION_PENDING_WAVE_QUEUE_CUTOVER_ACTIVE_ASYNC_R1_STATIC
```

Inherited parent validator drift remains unchanged and is not promoted as a new failure:

```text
D10 mirror validator: code-only tree excludes its historical spec file
P5-R2 validator: expects a legacy BpDkDevicePostUpdateRuntimeR1::new(device) source literal already absent in parent
```

Rust toolchain is unavailable in the bake environment. COMPILE/RUNTIME/PHYSICAL/PERFORMANCE are not claimed.

## 12. Artifacts

Overlay:

```text
ASH_EVE_MCU_ACTIVE_ASYNC_PHYS_R1_OVERLAY_CODE_ONLY.zip
SHA-256 45dfb7c238524a90bd4a9d301e2d3963bbbec8d4138ceb2de0e04d6c79901ca7
FILES 4
CRC PASS
```

Full:

```text
ASH_PASS3_EVE_MCU_ACTIVE_ASYNC_PHYS_R1_CODE_ONLY.zip
SHA-256 c44bd88fcce1667cda2da04c8faf1e26adb3c2ca1ba1def1ba62799debbe8543
FILES 8447
CRC PASS
```

Both exclude specs/, artifacts/, manifests/, Markdown, __pycache__, and *.pyc.

## 13. Physical acceptance

Run the new CLI only after a fresh release build and Native CF1 seal.

Startup must show:

```text
[ASH-EVE-MCU-ACTIVE-ASYNC-PHYS-R1][cli-seal]
[ASH-D10-ACTIVE-ASYNC-PHYS-R1][admission]
[ASH-EVE-MCU-ACTIVE-ASYNC-PHYS-R1][runtime-seal]
```

Then TensorCube R2 must physically emit:

```text
[ASH-TENSORCUBE-CONSUME-R2][gpu-plane]
```

with zero bulk D2H and zero CPU tile W/M consume counts.

The previous:

```text
FAIL_B06_CANDIDATE_NOT_COMPLETE:muon-device-successor-missing
```

may disappear only if a real successor ticket reaches B06.

BP-DK checkpoint R1 must remain physically admitted with same-encoder capture and zero per-parameter submit/map/wait.

## 14. Final law

> ActiveAsync is a distinct physical campaign authority, not a MirrorVerified canary with different environment labels.

> The new campaign requires the exact active B04/B05/B06/C07/C08 tuple, P4 exact lease, P5 ActiveAsync, TensorCube Consume R2 ActiveVerified, and BP-DK Checkpoint R1 ActiveVerified.

> The old MirrorVerified canary and D09 physical candidate remain distinct authority classes.

> A real B06 successor must arise from the physically reached ActiveAsync/TensorCube R2 path. No B06 gate is weakened or bypassed.
