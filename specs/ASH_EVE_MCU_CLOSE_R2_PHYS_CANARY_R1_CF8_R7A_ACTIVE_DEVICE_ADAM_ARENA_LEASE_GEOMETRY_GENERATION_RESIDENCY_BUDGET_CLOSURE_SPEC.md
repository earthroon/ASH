# ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF8

## R7A ACTIVE-DEVICE ADAM
## ARENA LEASE-GEOMETRY / GENERATION-RESIDENCY BUDGET CLOSURE

```text
+ R7A ACTIVE-LEASE ACQUIRE-SITE ATTRIBUTION
+ SOURCE W/M/V THREE-LEASE GEOMETRY
+ CANDIDATE W/M/V THREE-LEASE GEOMETRY
+ PARAMS / STATUS / READBACK TRANSIENT THREE-LEASE GEOMETRY
+ SINGLE-SEGMENT MINIMUM NINE-LEASE ADMISSION
+ MAX-PENDING-SEGMENT BUDGET COUPLING
+ COLLECTED CANDIDATE GENERATION-RESIDENCY ACCOUNTING
+ ACTUAL ADAM SEGMENT-GEOMETRY DERIVED LEASE FLOOR
+ CANARY / FULL-R1B SAME GEOMETRY LAW
+ RETAINED-BYTE / PAGE BUDGET PRESERVATION
+ NO EARLY CANDIDATE RECLAIM
+ NO LEASE-BOUND BYPASS
+ NO MAGIC 8 / 9 CONSTANT PROMOTION
```

## 0. Revision

```text
Patch ID:
ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF8

Class:
PHYSICAL RESOURCE-BUDGET GEOMETRY CLOSURE
R7A ACTIVE-DEVICE ADAM LEASE AUTHORITY

Direct parent:
ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF7
```

Parent physical first failure:

```text
RamAdamTransactionalCandidateExecutionFailed:
E_MCU_R7A_ARENA_ACTIVE_LEASE_BOUND
```

CF7 already reaches:

```text
selected_candidate_branch=RamResidentActiveDeviceProjection
```

CF8 therefore changes only the R7A active-lease budget authority and attribution surface.

## 1. Structural conflict

One active Adam segment owns:

```text
source Weight / M / V          = 3
candidate Weight / M / V       = 3
params / status / readback     = 3
                                  --
single pending segment peak    = 9
```

The parent campaign's fixed `max_in_flight_leases=8` is below the first segment's minimum simultaneous lease geometry.

Nine is a derived single-segment witness, not the final generation budget.

## 2. Exact segment authority

CF8 derives the planned Adam segment ledger from the same execution authorities used by production submission:

```text
canonical source-record bridge
R6_STREAM_CHUNK_ELEMENTS
ProductionMuonRuntime::route_span(...)
finalized gradient segment boundaries
explicit AdamW ranges
```

Each segment binds:

```text
canonical_parameter_index
element_start
element_count
```

The ledger is canonically sorted before hashing.

## 3. Geometry digest

Digest domain:

```text
ASH.MCU.R7A.CF8.ADAM.SEGMENT.GEOMETRY
```

For every exact segment:

```text
canonical_parameter_index LE
element_start LE
element_count LE
```

The pending-generation scheduler independently hashes the actually submitted `AdamRangeR1` set with the same domain and field encoding.

Required after generation collection:

```text
planned segment count   == submitted segment count
planned element count   == published element count
planned geometry digest == submitted geometry digest
```

## 4. Derived lease floor

Let:

```text
N = exact planned Adam segment count
P = ADAMW_ACTIVE_DEVICE_PENDING_GENERATION_DEFAULT_MAX_IN_FLIGHT_R1
E = min(P, N)
```

Candidate W/M/V survive collection as generation-resident state, therefore:

```text
candidate_residency = 3 * N
pending_extra       = (3 source + 3 transient) * E
```

Authoritative lease floor:

```text
ADAM_LEASE_FLOOR = 3*N + 6*min(P,N)
```

For `N=1`, this derives `9` as the structural cross-check.

All admission arithmetic uses checked add/mul and checked `u32` conversion.

## 5. Bootstrap and reseal

The historical unexplained campaign literal `8` is retired.

Before exact generation geometry exists, the campaign config carries only the structural bootstrap expression:

```text
3 + 3 + 3
```

This is not the final lease authority.

Before the first R7A Adam arena acquisition, CF8 reseals `max_in_flight_leases` to the exact derived generation floor and recomputes the R7A policy/domain digest.

A changed reseal is legal only while the prior domain reports:

```text
acquire_count       = 0
active_lease_count  = 0
retained_bytes      = 0
```

Otherwise fail:

```text
E_CF8_R7A_ARENA_RESEAL_AFTER_ACQUIRE
```

No mid-generation expansion is permitted.

## 6. Acquire-site attribution

Every R7A domain acquire emits, before the lease-bound `ensure!`:

```text
[ASH-MCU-R7A-CF8][lease-acquire]
```

Fields:

```text
site
semantic role
binding class
active_before
sealed_max
logical_size
reserved_size
device_authority_id
queue_authority_id
domain_digest
admitted
```

Required ordering:

```text
observe -> witness -> enforce -> acquire
```

## 7. Geometry witness

Before the first Adam source allocation:

```text
[ASH-MCU-R7A-CF8][adam-lease-geometry]
```

records:

```text
planned_segment_count
planned_adam_element_count
configured_max_pending_segments
effective_max_pending_segments
source_per_pending
candidate_per_live
transient_per_pending
single_segment_peak
candidate_residency_ceiling
pending_extra_ceiling
derived_adam_lease_floor
sealed_max_in_flight_leases
geometry_digest
admitted
```

Required:

```text
sealed_max_in_flight_leases >= derived_adam_lease_floor
```

Otherwise:

```text
E_CF8_R7A_ADAM_LEASE_BUDGET_UNDERPROVISIONED
```

## 8. Actual submission drift guards

After pending-generation completion:

```text
submitted_segment_count == planned_segment_count
final_published_element_count == planned_adam_element_count
submitted_segment_geometry_digest == planned_segment_geometry_digest
scheduler max_in_flight_segments == geometry pending bound
```

Errors:

```text
E_CF8_R7A_ADAM_SEGMENT_GEOMETRY_COUNT_DRIFT
E_CF8_R7A_ADAM_SEGMENT_GEOMETRY_ELEMENT_DRIFT
E_CF8_R7A_ADAM_SEGMENT_GEOMETRY_DIGEST_DRIFT
E_CF8_R7A_ADAM_PENDING_BOUND_DRIFT
```

## 9. Lifetime preservation

CF8 does not change the existing candidate reclaim law:

```text
candidate segment dead
AND active readers == 0
AND A01 tracked lifetime permits release
```

No candidate W/M/V buffer is reclaimed early to satisfy arena pressure.

No source/transient lifetime is shortened outside existing exact completion paths.

## 10. Independent resource axes

CF8 changes only the logical active-lease ceiling authority.

These remain unchanged and fail-closed independently:

```text
mcu_r7a_arena_budget_bytes
mcu_r7a_arena_max_pages
max buffer size
storage/uniform binding limits
A01 lifetime checks
```

A later retained-byte/page failure is a new physical boundary, not a reason to widen CF8 preemptively.

## 11. Forbidden repairs

```text
lease bound -> direct device buffer create
lease bound -> disable R7A arena
lease bound -> reduce pending scheduler bound
lease bound -> early candidate reclaim
lease bound -> mutate bound during acquire
magic large lease constant
```

## 12. CANARY / Full R1B law

CANARY and Full R1B differ only in optimizer-step horizon:

```text
CANARY 2
FULL   8
```

For the same model/route/gradient segmentation/pending bound they use the same per-generation R7A lease geometry law.

Step horizon is not multiplied into simultaneous residency.

## 13. Parent preservation

Preserve:

```text
CF5 two-step/eight-step separation
CF6 FreshGenesis 0/0/0 exactness
CF7 R3B attribution CANARY profile
B04 ActiveVerified
B05 ActiveDeviceCandidate
B06 ActiveVerified
C07 ActiveCompact
C08 MirrorVerified
promotion_claim=false
R1K RamResidentActiveDeviceProjection
R1J reader subgroup authority
R1I queue/device parity guards
```

No C08 ActiveAsync claim or synthetic physical admission is introduced.

## 14. Static acceptance

Required:

```text
fixed campaign literal 8 retired
bootstrap expressed from 3+3+3 role geometry
exact Adam segment prepass exists
lease formula = 3N + 6*min(P,N)
pending bound reused from scheduler authority
one-time pre-acquire arena reseal exists
used arena domain cannot be resealed
R7A policy/domain digest includes final lease bound
acquire witness precedes active-lease ensure
actual submitted geometry digest exists
count/element/digest/pending-bound drift guards exist
retained-byte budget unchanged
page budget unchanged
candidate reclaim law unchanged
no direct-create fallback
```

## 15. Compile / CF1 boundary

Required operator compile:

```powershell
cargo build `
  -p base_train `
  --bin base_train `
  --release `
  --locked `
  -j 1
```

Bake environment has no Rust toolchain, so:

```text
SOURCE  SEALED
STATIC  REVIEWED
COMPILE NOT CLAIMED
PHYSICAL NOT CLAIMED
```

CF8 changes release source, therefore Native CF1 must be resealed after compile. CF7 CF1 must not be reused.

## 16. Physical expected sequence

```text
[ASH-MCU-EVE-R1K][preflight] ... parity_admitted=true
[ASH-D10-CF7][r3b-attribution-canary] ... admitted=true
[ASH-EVE-MCU-CANARY-CF6] ... exact
[ASH-D10-CF7][runtime-profile] ... admitted=true
[ASH-MCU-EVE-R1K][candidate-branch] ... RamResidentActiveDeviceProjection
[ASH-MCU-R7A-CF8][adam-lease-geometry] ... admitted=true
[ASH-MCU-R7A-CF8][lease-acquire] ...
```

The old `E_MCU_R7A_ARENA_ACTIVE_LEASE_BOUND` must not recur while `active_before < sealed_max`.

## 17. Artifact seal

CF8 Full code-only:

```text
ASH_PASS3_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF8_R7A_ACTIVE_DEVICE_ADAM_ARENA_LEASE_GEOMETRY_GENERATION_RESIDENCY_BUDGET_CLOSURE_CODE_ONLY.zip
SHA256 574513edb9ede67cf32f100ae02dba3c7e7bb3e0854b18b5dcbfb8a2b1ce88b5
FILES 8424
CRC PASS
```

CF8 Overlay code-only:

```text
ASH_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF8_R7A_ACTIVE_DEVICE_ADAM_ARENA_LEASE_GEOMETRY_GENERATION_RESIDENCY_BUDGET_CLOSURE_OVERLAY_CODE_ONLY.zip
SHA256 1f634d8fa6b5af85491c52c54a64e6ca30a298ea9deaae00011ee0492ad41912
FILES 7
CRC PASS
```

Archive policy:

```text
specs/ 0
artifacts/ 0
generated runtime manifest/receipt additions 0
```

Delta:

```text
ADD 0
MOD 7
DEL 0
```

Modified files:

```text
crates/base_train/src/eve_mcu_close_r2_physical_campaign_r1b.rs
crates/base_train/src/mcu_device_resource_runtime_r7a.rs
crates/base_train/src/mcu_session_runtime_r7.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
crates/base_train/src/unified_atlas_mcu_adamw_active_device_pending_generation_scheduler_r1.rs
crates/burn_webgpu_backend/src/usage_segregated_buffer_arena.rs
```

Source SHA256:

```text
e39ea0b3ea1fdee8d71fb7d8931cf69377121f127210347900ae0cf5a984798c  eve_mcu_close_r2_physical_campaign_r1b.rs
a2b5d9b3be2628a0eb8728504da4f941c0a6b2fa9a9ec4d3f88021df1fc2bb3b  mcu_device_resource_runtime_r7a.rs
35982f856050efa58fab1695cee26a8ecb04c1565400a2a5f1ddba92a77cccc1  mcu_session_runtime_r7.rs
90eb438a6b3dadee64817a84a0c160cdf1d186f12fb3a7742ad2bc21456aa509  production_multistep_loop_accumulation8_scheduler.rs
5a48c6028ca97c418b93838c2be4a746d78a5e871ab7113b4f48f655b59c6ef9  tensorcube_local_muon_production_callsite_adoption.rs
33a6a5cf464a8898a0147e05c221d9868591909e018b0c325d29b533a7334820  unified_atlas_mcu_adamw_active_device_pending_generation_scheduler_r1.rs
fdff51099f8b10902efc55dd8a9b2ebe0393f20b5217706fd42dce50002fa527  usage_segregated_buffer_arena.rs
```

## 18. Final law

> R7A active leases are a simultaneous residency contract, not a tuning integer.

> Nine is the one-segment structural witness. The generation seal is derived from the exact segment topology.

> Candidate W/M/V remain generation-resident until existing exact lifetime authority permits reclaim.

> The lease ceiling is resealed once before first acquire and is bound into the R7A policy/domain digest.

> Actual submission count, element coverage and geometry digest must reproduce the ledger used to derive the seal.

> Retained bytes and page count remain independent fail-closed authorities.

> No early reclaim, no lease-bound bypass, no direct-create escape, no magic 8/9 promotion.
