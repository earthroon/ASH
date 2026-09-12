# ASH-EVE-MCU-CLOSE-R2-PHYS-R1B-CF1-R1J

## MCU R7A1 PACKED-GRADIENT PRODUCTION READER SUBGROUP AUTHORITY CLOSURE

### Revision

```text
Patch ID:
ASH-EVE-MCU-CLOSE-R2-PHYS-R1B-CF1-R1J

Class:
PRODUCTION DEVICE / QUEUE AUTHORITY CLOSURE
NON-GRAPH MUON EXECUTION AUTHORITY INJECTION
QUALIFICATION-ONLY DEFAULT SUBGROUP ISOLATION

Direct parent:
ASH-EVE-MCU-CLOSE-R2-PHYS-R1B-CF1-R1I
```

R1J preserves the R1I producer/reader identity witness and closes the source mechanism physically attributed by R1I:

```text
producer lineage = Exact
initial resident clone = Exact
later reader = ReaderSubgroupAuthorityDrift
producer device/queue = D1/Q1
reader device/queue = D2/Q2
```

The implementation target is the implicit production rule:

```text
resident_graph = None
    -> McuDeviceSoftSubgroupHandleR1A::new_default()
```

R1J separates graph residency from device/queue authority residency.

---

## 1. Authority law

Production law:

```text
Resident graph present
    -> reader subgroup = resident graph subgroup

Resident graph absent
    -> reader subgroup = existing MCU session subgroup

Qualification / isolated harness explicitly requests default
    -> new_default() permitted
```

Forbidden production law:

```text
resident_graph = None
    -> implicit fresh subgroup authority
```

Compact invariant:

```text
Graph state is optional.
Device / queue authority is not.
```

---

## 2. Implementation shape

R1J materializes:

```text
MuonExecutionCallerClassR1J
MuonExecutionSubgroupSourceKindR1J
```

Caller classes:

```text
ResidentPrimary
ProductionNonGraph
Control
Counterfactual
Replay
Qualification
```

Subgroup source classes:

```text
ResidentGraph
SessionInjected
QualificationDefault
```

Production non-graph execution uses explicit session-injected APIs:

```text
execute_with_norm_path_session_r1j(...)
execute_resident_with_norm_path_session_r1j(...)
```

Qualification-compatible legacy wrappers remain available, but production callsites no longer use their implicit default path.

---

## 3. Local Muon authority selection

Changed file:

```text
crates/burn_webgpu_backend/src/base_train_tensorcube_local_muon.rs
```

Internal authority dispatch is now:

```text
resident graph + no injected subgroup
    -> ResidentGraph

no resident graph + injected session subgroup
    -> SessionInjected

no resident graph + no injected subgroup + Qualification caller
    -> QualificationDefault

no resident graph + no injected subgroup + non-Qualification caller
    -> E_MCU_R1J_PRODUCTION_SUBGROUP_AUTHORITY_MISSING

resident graph + injected subgroup
    -> E_MCU_R1J_SUBGROUP_SOURCE_SPLIT
```

SessionInjected additionally requires:

```text
same Rc inner authority = true
exact subgroup binding  = true
```

Errors:

```text
E_MCU_R1J_SESSION_INJECTED_SUBGROUP_CLONE_IDENTITY_DRIFT
E_MCU_R1J_SESSION_INJECTED_SUBGROUP_BINDING_DRIFT
```

`new_default()` remains only in the explicit QualificationDefault branch.

---

## 4. Fused-pair Muon authority selection

Changed file:

```text
crates/burn_webgpu_backend/src/tensorcube_fused_pair_muon.rs
```

The fused-pair non-graph consumer had the same implicit default-subgroup source mechanism and is closed under the same R1J law.

R1J adds:

```text
execute_with_norm_path_session_r1j(...)
```

and uses the same explicit authority dispatch:

```text
ResidentGraph
SessionInjected
QualificationDefault
```

The fused reader is also moved onto the existing R1I reader witness helper:

```text
packed_gradient_read_spec_r7a1_or_external_with_subgroup_r1i(...)
```

No packed binding rewrite is introduced.

---

## 5. Production callsite migration

Changed file:

```text
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
```

All four production non-graph callsites that previously reached implicit default authority now inject:

```text
self.mcu.parent_r7.device_soft_subgroup_r1a()
```

Exact caller classifications:

```text
same-source local counterfactual primary
    -> Counterfactual

same-source local counterfactual replay
    -> Replay

all-local control
    -> Control

planned local non-graph
    -> ProductionNonGraph

fused-pair non-graph
    -> ProductionNonGraph
```

Production source now contains:

```text
.execute_with_norm_path(                 = 0
.execute_resident_with_norm_path(        = 0
```

for this production callsite module.

Remaining direct legacy wrapper usage under `base_train` is limited to the dedicated qualification binary:

```text
ash_bp_dk_active_fusion_physical_qualification_08a.rs
```

---

## 6. R1J reader authority witness

Both local and fused executors emit:

```text
[ASH-MCU-R7A1-R1J][reader-authority]
```

Fields include:

```text
label
caller_class
subgroup_source
subgroup_device
subgroup_queue
subgroup_generation
session_device
session_queue
packed_device
packed_queue
resident_graph_present
same_session_inner
```

Expected formerly-drifting non-graph reader:

```text
subgroup_source=SessionInjected
same_session_inner=Some(true)
subgroup_device == session_device == packed_device
subgroup_queue  == session_queue  == packed_queue
```

R1I downstream witness is preserved and should subsequently report:

```text
class=Exact
```

---

## 7. R1I preservation

R1J does not modify:

```text
crates/burn_webgpu_backend/src/buffer_submission_lease.rs
crates/burn_webgpu_backend/src/himuon_packed_gradient_r7a1.rs
```

Therefore the following R1I contracts are byte-preserved from the parent archive:

```text
same QueueAuthorityId / different DeviceAuthorityId fail-closed guard
E_DEVICE_SOFT_SUBGROUP_QUEUE_DOMAIN_DEVICE_DRIFT
R1I producer identity witness
R1I reader-pre-resolution witness
E_MCU_R7A1_READER_DEVICE_DRIFT
E_MCU_R7A1_READER_QUEUE_DRIFT
cross-device lease guard
arena / allocation lineage guards
```

R1J expects correct authority injection to avoid those errors; it does not weaken them.

---

## 8. R1H / BP-DK preservation

R1J preserves the R1H Disabled contract:

```text
DK generation open            = 0
legacy local phys record      = 0
legacy bridge phys record     = 0
inline-plan phys record       = 0
legacy post phys record       = 0
prepared-plan freeze          = 0
commit resolve                = 0
abort resolve                 = 0
```

No DK policy or threshold changes are made.

---

## 9. No authority rewrite

R1J does not:

```text
rewrite reader DeviceAuthorityId
rewrite reader QueueAuthorityId
rewrite packed allocation identity
rewrite packed binding identity
allocate a fresh queue ID after conflict
reclassify OwnedExisting as ExternalBorrowed
copy the packed gradient to a new device as fallback
force resident graph activation
force B04/B05 routing
relax queue-domain parity guard
relax cross-device lease adoption
```

The correct existing subgroup authority is injected before reader construction.

---

## 10. Optimizer / numerical preservation

R1J changes no:

```text
Muon arithmetic
AdamW arithmetic
HiMuon momentum
candidate weight math
counterfactual math
replay math
fusion math
154 Muon / 47 AdamW / 0 mixed route
RAM36 policy
successor weight reservation
checkpoint format
model geometry
micro-batch geometry
```

This revision is physical-authority plumbing only.

---

## 11. Actual source delta

Relative to R1I:

```text
ADD 0
MOD 3
DEL 0
```

Changed sources:

```text
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
R1I SHA-256:
d5ad5f8b20f3427f10d72c22d2c895fae6512cda4a26eae42d27f6a41f83e6d7
R1J SHA-256:
894f2961bfb85520dc0859f9e015c4e568a82b74b52527cc7a345a71b521b9e6

crates/burn_webgpu_backend/src/base_train_tensorcube_local_muon.rs
R1I SHA-256:
58169d7f3ba1347b1e3fd55f8ccbd2bbbf361440067778d1f3b7eaad91837d0e
R1J SHA-256:
c4050d90c0b4174409c2e26cffe7f1e7bdef9172a7b5db4b94f7cbf60936d8e8

crates/burn_webgpu_backend/src/tensorcube_fused_pair_muon.rs
R1I SHA-256:
6938fa1b076ebc1e9a714659a688c2dbf38a8ad59f638f410d1ed0deaaacba16
R1J SHA-256:
064ff4fc784fad88ae3b043dea672184c23304fb9f5ec5aadacac0e1b9d8c437
```

Source-delta digest:

```text
4052f59cc184574815cf063217ecfbdfde47c53049c1e15a740e865e80022785
```

Key locations after bake:

```text
base_train_tensorcube_local_muon.rs
  caller class enum                         line 1014
  session-injected local API                line 1651
  session-injected resident/control API     line 1746
  production-missing authority guard        line 2152
  R1J reader-authority witness              line 2164

tensorcube_fused_pair_muon.rs
  session-injected fused API                line 350
  production-missing authority guard        line 474
  R1J reader-authority witness              line 482

production callsite
  counterfactual / replay injection          line 9846
  all-local control injection               line 11675
  planned-local non-graph injection         line 11834
  fused-pair non-graph injection            line 12005
```

---

## 12. Archive seal

Full code-only archive:

```text
ASH_PASS3_EVE_MCU_CLOSE_R2_PHYS_R1B_CF1_R1J_MCU_R7A1_PRODUCTION_READER_SUBGROUP_AUTHORITY_CLOSURE_CODE_ONLY.zip
SHA-256:
bacaa30d8115942f903b6621d2bba388806499327450c907af2e5b866637759b
Files: 8423
CRC: PASS
```

Overlay code-only archive:

```text
ASH_EVE_MCU_CLOSE_R2_PHYS_R1B_CF1_R1J_MCU_R7A1_PRODUCTION_READER_SUBGROUP_AUTHORITY_CLOSURE_OVERLAY_CODE_ONLY.zip
SHA-256:
8d415a2005d7ccf39cda99886a670d11b788fcbfe17bf3f02f967b43c7699cf3
Files: 3
CRC: PASS
```

Per artifact policy, neither ZIP contains:

```text
specs/
artifacts/
generated manifest JSON
this specification
```

---

## 13. Static bake acceptance

```text
R1I parent inventory exact                     PASS
actual changed file count = 3                  PASS
ADD / DEL = 0                                  PASS
production old non-graph wrapper calls = 0     PASS
counterfactual session injection               PASS_STATIC
replay session injection                       PASS_STATIC
control session injection                      PASS_STATIC
planned-local session injection                PASS_STATIC
fused-pair session injection                   PASS_STATIC
ResidentGraph branch preserved                 PASS_STATIC
QualificationDefault explicit branch retained  PASS_STATIC
production missing authority fail-closed       PASS_STATIC
R1I queue-domain file unchanged                PASS_STATIC
R1I packed-gradient witness file unchanged     PASS_STATIC
Full ZIP CRC                                   PASS
Overlay ZIP CRC                                PASS
```

---

## 14. Evidence boundary

The bake environment does not provide Cargo / rustc / rustfmt.

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

No release compile, Native CF1, physical reader closure, A/B/C promotion or performance PASS is claimed by this bake.

---

## 15. Re-materialization contract

```text
dataset regeneration      NOT REQUIRED
R1A regeneration          NOT REQUIRED
R1A cursor regeneration   NOT REQUIRED
burn_webgpu_backend build  REQUIRED
base_train rebuild         REQUIRED
Native CF1 reseal          REQUIRED
fresh R1B campaign root    REQUIRED
A/B/C reentry              REQUIRED
```

---

## 16. Physical acceptance

At the execution that previously produced:

```text
class=ReaderSubgroupAuthorityDrift
subgroup_device=2
subgroup_queue=2
packed_device=1
packed_queue=1
```

R1J expects:

```text
[ASH-MCU-R7A1-R1J][reader-authority]
caller_class=Replay | Counterfactual | Control | ProductionNonGraph
subgroup_source=SessionInjected
same_session_inner=Some(true)
subgroup_device == session_device == packed_device
subgroup_queue  == session_queue  == packed_queue
```

followed by:

```text
[ASH-MCU-R7A1-R1I][reader-pre-resolution]
class=Exact
```

and no:

```text
E_MCU_R7A1_READER_DEVICE_DRIFT
E_MCU_R7A1_READER_QUEUE_DRIFT
```

at that former boundary.

A later first failure is a new attribution boundary and is not automatically folded into R1J.

---

## Completion law

R1J may issue:

```text
PASS_EVE_MCU_CLOSE_R2_PHYS_R1B_CF1_R1J
```

only when the real production campaign demonstrates:

```text
resident readers preserve resident/session authority
non-graph readers use SessionInjected
production implicit default subgroup genesis count = 0
R1I producer witness remains Exact
R1I reader witness is Exact on formerly drifting paths
R1I queue-domain guard remains intact
execution crosses the prior E_MCU_R7A1_READER_DEVICE_DRIFT boundary
```

Until then:

```text
HOLD_EVE_MCU_CLOSE_R2_PHYS_R1B_CF1_R1J_PHYSICAL_PENDING
```

---

## Final law

> Graph state is optional. Device/queue authority is not.

> Production `resident_graph=None` means no graph state, not no execution authority. The MCU session subgroup remains authoritative.

> Resident executions inherit the resident graph subgroup. Non-graph production executions inherit the MCU session subgroup. Fresh default subgroup genesis is explicit qualification behavior only.

> R1J fixes the authority source before reader construction. It does not rewrite a mismatched reader afterward and does not weaken any R1I guard.
