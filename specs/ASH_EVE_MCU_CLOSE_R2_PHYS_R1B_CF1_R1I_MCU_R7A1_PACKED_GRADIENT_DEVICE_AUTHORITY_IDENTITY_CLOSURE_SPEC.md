# ASH-EVE-MCU-CLOSE-R2-PHYS-R1B-CF1-R1I

## MCU R7A1 PACKED-GRADIENT PRODUCER / READER DEVICE-AUTHORITY IDENTITY CLOSURE

### Revision

```text
Patch ID:
ASH-EVE-MCU-CLOSE-R2-PHYS-R1B-CF1-R1I

Class:
PHYSICAL IDENTITY ATTRIBUTION
QUEUE-DOMAIN FAIL-CLOSED CLOSURE
PACKED-GRADIENT PRODUCER / READER LINEAGE WITNESS

Direct parent:
ASH-EVE-MCU-CLOSE-R2-PHYS-R1B-CF1-R1H
```

R1I preserves the R1H Disabled parameter-path closure and starts at the new physical first failure:

```text
E_MCU_R7A1_READER_DEVICE_DRIFT
```

The purpose of R1I is not to make mismatched identities equal. It materializes the producer / resident reader / physical runtime / arena lineage, and moves an invalid same-QueueAuthorityId / different-DeviceAuthorityId mapping to the queue-domain admission boundary.

---

## 1. Parent physical evidence

R1H crossed the former first failure:

```text
E_DK_R2A_PHYS_GENERATION_DRIFT
```

The same physical campaign reached:

```text
PASS_ASH_BASETRAIN_BP_DK_POST_CANDIDATE_TARGET_OPTIMIZER_GENERATION_BINDING_CLOSURE_R1
```

and then stopped at:

```text
PHYS_R1_PRODUCTION_ERROR:
RamAdamTransactionalCandidateExecutionFailed:
E_MCU_R7A1_READER_DEVICE_DRIFT
```

Therefore:

```text
R1H former blocker crossing = SUPPORTED / PHYSICAL
R1B A/B/C promotion         = HOLD
R1I first-failure authority = MCU R7A1 packed-gradient identity
```

---

## 2. R1H / R1G preservation

The R1I parent production file before this revision has SHA-256:

```text
aa794ac09a6a8043e1f3e98605e6bcbfd2d735e1ec9a75455daebaf162473c66
```

R1I adds only the resident subgroup clone / binding witness at the session-to-resident construction seam. Existing R1H calls remain mode-gated:

```text
record_legacy_local_parameter
record_legacy_bridge_parameter
record_inline_parameter_plan
record_legacy_post_parameter
```

R1G Disabled commit / abort finalize no-op gates remain present.

The low-level BP-DK R2A runtime remains byte-preserved:

```text
crates/base_train/src/bp_delta_k_r2a_phys_runtime.rs
SHA-256:
2b56af36c95a2654dc50d7eb4c0ade743bd78714f31d5946097d7f589e2d2c3a
```

No DK policy change is made.

---

## 3. Queue-domain authority defect boundary

Changed file:

```text
crates/burn_webgpu_backend/src/buffer_submission_lease.rs
```

Before R1I:

```text
SubmissionLeaseRuntime.queue_domains
    key = QueueAuthorityId

existing QueueAuthorityId
    -> existing QueueDomainState returned
    -> incoming DeviceAuthorityId not compared
```

R1I changes `queue_domain_locked()` to a fallible authority gate.

Required behavior:

```text
Vacant queue ID
    -> create QueueDomainState from incoming device / queue binding

Occupied queue ID
    -> existing.device_id == incoming.device_authority_id REQUIRED
    -> existing.queue_id  == incoming.queue_authority_id REQUIRED
```

New fail-closed errors:

```text
E_DEVICE_SOFT_SUBGROUP_QUEUE_DOMAIN_DEVICE_DRIFT
E_DEVICE_SOFT_SUBGROUP_QUEUE_DOMAIN_QUEUE_DRIFT
```

The Device drift error carries:

```text
queue_authority_id
existing_device_authority_id
incoming_device_authority_id
```

No new QueueAuthorityId is generated to hide a mismatch.

All four production callers now propagate the fallible queue-domain result:

```text
queue_authority_ids
register_owned_physical_allocation
record_pending_queue_write_site
submit_with_leases
```

---

## 4. Queue-domain controls

R1I adds two local controls in `buffer_submission_lease.rs`.

Negative:

```text
Q7 / D101
then
Q7 / D202

=> E_DEVICE_SOFT_SUBGROUP_QUEUE_DOMAIN_DEVICE_DRIFT
```

Positive:

```text
Q11 / D303
then
Q11 / D303

=> same QueueDomainState authority preserved
```

These tests are source-materialized but were not executed in the bake environment because Cargo is unavailable.

---

## 5. Same-subgroup clone identity

Changed file:

```text
crates/burn_webgpu_backend/src/device_soft_subgroup_r1a.rs
```

R1I adds the process-local diagnostic predicate:

```text
shares_inner_identity_with()
```

implemented by:

```text
Rc::ptr_eq
```

This pointer relation is diagnostic only. It does not replace the authoritative IDs:

```text
DeviceAuthorityId
QueueAuthorityId
PhysicalWgpuRuntimeBindingR1
PhysicalAllocationId
McuArenaDomainIdR7A
```

The production session-to-resident construction now requires:

```text
McuSessionRuntimeR7 subgroup
and
MuonResidentStateGraph subgroup

share the same Rc inner authority
```

and exact:

```text
McuDeviceSoftSubgroupBindingR1A
```

parity.

New errors:

```text
E_MCU_R1I_RESIDENT_SUBGROUP_CLONE_IDENTITY_DRIFT
E_MCU_R1I_RESIDENT_SUBGROUP_BINDING_DRIFT
```

No replacement subgroup constructor is introduced.

---

## 6. R1I packed-gradient witness

Changed file:

```text
crates/burn_webgpu_backend/src/himuon_packed_gradient_r7a1.rs
```

Materialized types:

```text
PackedGradientDeviceAuthorityClassificationR1I
PackedGradientDeviceAuthorityWitnessR1I
```

Classification vocabulary:

```text
Exact
ReaderSubgroupAuthorityDrift
QueueDomainDeviceAlias
PackedBindingLineageDrift
PhysicalRuntimeBindingDrift
PhysicalRuntimeGenerationDrift
ArenaDomainLineageDrift
ResidentSubgroupGenerationDrift
ProducerSubgroupCloneIdentityDrift
Unclassified
```

Witness fields bind the following identity classes without modifying the R7A1 seam digest:

```text
physical runtime existing_id
physical runtime generation
physical runtime device authority
physical runtime queue authority

subgroup device authority
subgroup queue authority
subgroup generation

resolved device / queue authority where available

packed allocation device authority
packed queue authority
packed allocation ordinal

arena domain device authority
arena domain queue authority
arena domain digest
arena page ordinal
arena incarnation

packed binding identity digest
same-subgroup-clone diagnostic boolean
classification
```

The existing `PackedGradientReadBindingR7A1` schema and `identity_digest` algorithm are not rewritten.

---

## 7. Producer lineage witness

The packed-gradient producer now observes, in one witness:

```text
PhysicalWgpuRuntimeBindingR1
McuDeviceSoftSubgroupBindingR1A
McuArenaDomainIdR7A
ArenaLease
PackedGradientReadBindingR7A1
producer SubmissionEpoch
```

Exact producer identity requires:

```text
runtime device / queue
== subgroup device / queue
== arena domain device / queue
== arena allocation device / queue
== packed binding device / queue
== producer submission epoch device / queue
```

and:

```text
arena lease subgroup clone == producer subgroup inner authority
arena page ordinal exact
arena incarnation exact
arena domain digest exact
```

Possible producer failures include:

```text
E_MCU_R1I_PRODUCER_SUBGROUP_CLONE_IDENTITY_DRIFT
E_MCU_R1I_PRODUCER_RUNTIME_SUBGROUP_DEVICE_QUEUE_DRIFT
E_MCU_R1I_PRODUCER_SUBGROUP_ARENA_DEVICE_QUEUE_DRIFT
E_MCU_R1I_PRODUCER_BINDING_LINEAGE_DRIFT
```

No producer ID is rewritten.

---

## 8. Resident reader witness

Canonical local Muon packed-gradient reads now pass through:

```text
packed_gradient_read_spec_r7a1_or_external_with_subgroup_r1i(...)
```

The helper records the resident subgroup and its physical runtime binding before queue-domain resolution.

The pre-resolution witness compares:

```text
physical runtime authority
resident subgroup authority
packed binding authority
```

If the resident subgroup already disagrees with the packed binding, the existing R7A1 reader error remains authoritative:

```text
E_MCU_R7A1_READER_DEVICE_DRIFT
E_MCU_R7A1_READER_QUEUE_DRIFT
```

If the resident subgroup and packed binding agree but the global queue-domain table already maps the same QueueAuthorityId to another DeviceAuthorityId, the new earlier error is:

```text
E_DEVICE_SOFT_SUBGROUP_QUEUE_DOMAIN_DEVICE_DRIFT
```

This distinguishes reader-subgroup drift from queue-domain aliasing.

Canonical reader adoption is wired in all three current local Muon execution surfaces:

```text
base_train_tensorcube_local_muon.rs
base_train_tensorcube_local_muon_pending_p5_r1.rs
base_train_tensorcube_local_muon_active_device_pending_r1.rs
```

---

## 9. No authority rewrite

R1I does not:

```text
rewrite reader DeviceAuthorityId from packed binding
rewrite packed allocation DeviceAuthorityId from reader
allocate a new QueueAuthorityId on conflict
downgrade OwnedExisting to ExternalBorrowed on conflict
copy the packed gradient to a replacement device as fallback
relax arena incarnation checks
relax exact consumer lease retirement
relax cross-device lease adoption
```

Existing guard preserved:

```text
FAIL_A01_CROSS_DEVICE_LEASE_ADOPTION
```

Existing R7A1 arena / allocation / reader guards remain present.

---

## 10. Actual source delta

Relative to R1H:

```text
ADD 0
MOD 7
DEL 0
```

Changed files and R1I SHA-256:

```text
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
  d5ad5f8b20f3427f10d72c22d2c895fae6512cda4a26eae42d27f6a41f83e6d7

crates/burn_webgpu_backend/src/base_train_tensorcube_local_muon.rs
  58169d7f3ba1347b1e3fd55f8ccbd2bbbf361440067778d1f3b7eaad91837d0e

crates/burn_webgpu_backend/src/base_train_tensorcube_local_muon_active_device_pending_r1.rs
  d8147b381f47a64abe4e90575277f0dda09e84e61a272d15fe29c738ade320e1

crates/burn_webgpu_backend/src/base_train_tensorcube_local_muon_pending_p5_r1.rs
  119f715b196549cd6bc1b9d8a3698acd03026e11f8826c14823f3599fa98b87b

crates/burn_webgpu_backend/src/buffer_submission_lease.rs
  7e3cc0617d2bc076f3239eab6779b541e0aee2fcf92351391e43b5140b85cf4d

crates/burn_webgpu_backend/src/device_soft_subgroup_r1a.rs
  57480e26090a05f831ffbe5df8871cf059dc596e11867a80b866e593e9ae11a2

crates/burn_webgpu_backend/src/himuon_packed_gradient_r7a1.rs
  4d438f9aae3ad1976447ba7b1b8c06f9c38d0f1c185057f69ed4639a157f7ccf
```

Source-delta digest:

```text
078a15b2ea072ae80cb5b99676e7e9f00505269b576489249acb3f4cbc39b00c
```

Key baked locations:

```text
buffer_submission_lease.rs
  queue-domain device parity error        line 397
  negative queue-domain control           line 994

 device_soft_subgroup_r1a.rs
  Rc inner identity predicate             line 193

himuon_packed_gradient_r7a1.rs
  producer witness                        line 277
  reader witness                          line 370
  reader pre-resolution phase             line 394
  canonical reader helper                 line 442

base_train_tensorcube_local_muon.rs
  producer witness adoption               line 778
  canonical reader helper adoption        line 2728

base_train production callsite
  resident clone identity guard           line 3527
  resident clone witness                  line 3536
```

---

## 11. Archive seal

Full code-only archive:

```text
ASH_PASS3_EVE_MCU_CLOSE_R2_PHYS_R1B_CF1_R1I_MCU_R7A1_PACKED_GRADIENT_DEVICE_AUTHORITY_IDENTITY_CLOSURE_CODE_ONLY.zip
SHA-256:
6a0d9b6eb040f425099e84c5ff1322918342d4b6e83be2058ad0b5deb5ce1589
Files: 8423
CRC: PASS
```

Overlay code-only archive:

```text
ASH_EVE_MCU_CLOSE_R2_PHYS_R1B_CF1_R1I_MCU_R7A1_PACKED_GRADIENT_DEVICE_AUTHORITY_IDENTITY_CLOSURE_OVERLAY_CODE_ONLY.zip
SHA-256:
3a9654fce164c5918865ab9de7debb67a7098f747e525e561d9173156de1dd81
Files: 7
CRC: PASS
```

Per request, neither ZIP contains:

```text
specs/
artifacts/
generated manifest JSON
this specification
```

Existing Rust source or test files whose names contain `manifest` remain part of the code inventory; they are source code, not generated manifest artifacts.

---

## 12. Static bake acceptance

Static validator result:

```text
PASS R1H local gate preserved
PASS R1H bridge gate preserved
PASS R1H inline gate preserved
PASS R1H post gate preserved
PASS R1G commit gate preserved
PASS R1G abort gate preserved
PASS queue domain fallible
PASS queue domain device parity guard
PASS queue domain queue parity guard
PASS all production queue_domain callers propagate
PASS queue alias negative test materialized
PASS queue exact positive test materialized
PASS same Rc identity witness
PASS resident clone identity guard
PASS resident binding guard
PASS producer witness
PASS reader witness
PASS physical runtime witness fields
PASS arena witness fields
PASS producer witness wired
PASS canonical reader witness wired
PASS cross-device guard preserved
PASS reader existing guard preserved
PASS no authority rewrite pattern introduced
PASS no specs tree
PASS no artifacts tree
PASS BP-DK low-level preserved
```

Archive CRC checks pass for Full and Overlay.

---

## 13. Evidence boundary

The bake environment does not provide:

```text
cargo
rustc
rustfmt
```

Therefore:

```text
SOURCE       CONFIRMED
STATIC       CONFIRMED
ARCHIVE      CONFIRMED
COMPILE      NOT VERIFIED
RUNTIME      NOT VERIFIED
PHYSICAL     NOT VERIFIED
PERFORMANCE  NOT MEASURED
```

The newly added Rust tests are materialized but not executed here.

No release compile, Native CF1, queue-domain runtime, packed-gradient physical closure, A/B/C, or performance PASS is claimed by this bake.

---

## 14. Re-materialization contract

```text
dataset regeneration      NOT REQUIRED
R1A regeneration          NOT REQUIRED
R1A cursor regeneration   NOT REQUIRED
base_train rebuild         REQUIRED
burn_webgpu_backend build  REQUIRED
Native CF1 reseal          REQUIRED
fresh R1B campaign root    REQUIRED
A/B/C reentry              REQUIRED
```

---

## 15. Next physical classification

R1I intentionally supports distinct next failures.

### A. Queue-domain alias

```text
E_DEVICE_SOFT_SUBGROUP_QUEUE_DOMAIN_DEVICE_DRIFT
```

with:

```text
same QueueAuthorityId
existing DeviceAuthorityId != incoming DeviceAuthorityId
```

means:

```text
QUEUE_DOMAIN_DEVICE_ALIAS
```

is physically supported.

### B. Resident subgroup drift

A reader witness with:

```text
class=ReaderSubgroupAuthorityDrift
```

followed by the existing reader device / queue drift means the resident consumer arrived with a different subgroup authority before queue-domain resolution.

### C. Producer lineage drift

A producer witness failure means the divergence happened before the packed gradient was published to the reader.

### D. Exact identity and progression

If producer and reader witnesses are Exact, the queue-domain guard accepts the binding, and execution crosses the old:

```text
E_MCU_R7A1_READER_DEVICE_DRIFT
```

boundary, R1I has physically crossed its target blocker.

A later first failure belongs to a new attribution boundary.

---

## Final law

> A packed-gradient allocation belongs to one DeviceAuthorityId / QueueAuthorityId lineage. Producer, arena, physical runtime, resident reader and submission lease runtime must agree on that lineage.

> A QueueAuthorityId already registered to DeviceAuthorityId D1 cannot be silently reused by an incoming binding that claims DeviceAuthorityId D2.

> R1I does not repair identity mismatch by rewriting IDs. It moves the mismatch to its earliest observable authority boundary and preserves the mismatch as evidence.

> R1H remains preserved. R1I begins at the new physical first failure only.
