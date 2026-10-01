# ASH-C08-ACTIVE-PHYSICAL-ADMISSION-CF1-CLOSE-R1

## ACTIVE PHYSICAL ADMISSION PRODUCTION CLOSURE

```text
+ CF1 / CF1A PHYSICAL PASS PRESERVATION
+ LOCAL FALSE → PHYSICAL PASS → ADOPTED TRUE TRANSITION WITNESS
+ ONE-SHOT PHYSICAL ADOPTION AUTHORITY
+ QUALIFICATION RECEIPT HASH RESEAL WITNESS
+ SOURCE / PHYSICAL / ADOPTED RECEIPT LINEAGE CLOSURE
+ MCU R7 PRODUCTION DEVICE / QUEUE AUTHORITY PRESERVATION
+ SAME DEVICE / SAME QUEUE POST-ADOPTION CONTINUITY
+ CALLBACK / MAP / DEFERRED-RETIREMENT TERMINAL CLOSURE
+ OBSERVED-ZERO HOT-PATH EXACT-WAIT PRESERVATION
+ QUALIFICATION-ONLY EXACT-WAIT PRESERVATION
+ ASSERT-ACTIVE-READY POST-ADOPTION ORDERING
+ NO PRE-ADOPTION ACTIVE-READY SUCCESS
+ MULTI-STEP ADOPTED-AUTHORITY REUSE
+ NO POST-ADOPTION REQUALIFICATION
+ NO POST-ADOPTION READOPTION
+ A/B/C LEG-LOCAL PHYSICAL AUTHORITY
+ NO CROSS-LEG RECEIPT REUSE
+ NO CROSS-LEG IN-MEMORY AUTHORITY REUSE
+ NO CROSS-BINARY RECEIPT REUSE
+ D09 ADOPTED ACTIVE-PHYSICAL HANDOFF WITNESS
+ R4D-R2-CLOSE-R1 HANDOFF PRESERVATION
+ FAIL-CLOSED NEGATIVE QUALIFICATION
+ PHYSICAL / SEMANTIC / LINEAGE CLOSURE RECEIPT
+ FINAL C08 FREEZE SEAL
+ NO C08 POLICY RELAXATION
+ NO CF1 EVIDENCE RELAXATION
+ NO CF1A IDENTITY RELAXATION
+ NO D09 POLICY CHANGE
+ NO R4D SEMANTIC CHANGE
```

## 0. Patch identity

- Patch ID: `ASH-C08-ACTIVE-PHYSICAL-ADMISSION-CF1-CLOSE-R1`
- Parent: `ASH-C08-ACTIVE-PHYSICAL-ADMISSION-CF1A`
- Parent physical authorities:
  - `PASS_ASH_C08_ACTIVE_PHYSICAL_ADMISSION_CF1`
  - `PASS_ASH_C08_ACTIVE_PHYSICAL_ADMISSION_CF1A`
- Schema: `ASH_C08_ACTIVE_PHYSICAL_ADMISSION_CF1_CLOSE_R1_V1`
- Leg receipt: `c08_active_physical_admission_cf1_close_r1_receipt.json`
- ABC receipt: `c08_active_physical_admission_cf1_close_r1_abc_receipt.json`
- Leg PASS token: `PASS_ASH_C08_ACTIVE_PHYSICAL_ADMISSION_CF1_CLOSE_R1`
- ABC PASS token: `PASS_ASH_C08_ACTIVE_PHYSICAL_ADMISSION_CF1_CLOSE_R1_ABC`

CF1-CLOSE-R1 adds no new C08 admission policy. It closes the live production authority chain established by CF1 and CF1A.

## 1. Required authority transition

Every production leg SHALL establish this monotonic transition:

```text
UNQUALIFIED
→ LOCAL_QUALIFIED_FALSE
→ CF1_PHYSICAL_PASS
→ CF1A_IDENTITY_PASS
→ ADOPTED_ACTIVE
→ ACTIVE_READY
→ POST_ADOPTION_REUSE
→ D09_HANDOFF
→ CLOSED
```

Forbidden shortcuts include:

```text
UNQUALIFIED → ADOPTED_ACTIVE
LOCAL_QUALIFIED_FALSE → ACTIVE_READY
ACTIVE_READY → SECOND_ADOPTION
POST_ADOPTION_REUSE → REQUALIFICATION
```

## 2. Local false preservation

Immediately before adoption the local C08 qualification SHALL be present, valid, hash-sealed, and still carry:

```text
active_physical_admission = false
```

An already-active local receipt before the explicit physical adoption edge is a hard failure.

No literal `active_physical_admission: true` promotion is allowed.

## 3. CF1 / CF1A preservation

The current leg SHALL carry a valid CF1 physical receipt with:

```text
physical_admission_pass = true
PASS_ASH_C08_ACTIVE_PHYSICAL_ADMISSION_CF1
```

and a valid CF1A identity binding with:

```text
identity_authority_source = MCU_R7_PRODUCTION_PHYSICAL
cf1a_identity_rebind_pass = true
PASS_ASH_C08_ACTIVE_PHYSICAL_ADMISSION_CF1A
same_device_identity = true
same_queue_identity = true
```

CF1-CLOSE-R1 SHALL NOT weaken any callback, map, retirement, device/queue, exact-wait, or upstream predicates.

## 4. Source / physical lineage binding

The physical receipt SHALL bind exactly to the pre-adoption local receipt:

```text
physical.source_qualification_receipt_hash
==
pre_adoption_local.receipt_hash
```

A source qualification hash mismatch fails closed.

## 5. One-shot adoption

Within each A/B/C leg:

```text
qualification_call_count = 1
physical_receipt_materialization_count = 1
physical_adoption_call_count = 1
```

The runtime SHALL reject a second adoption and SHALL preserve:

```text
post_adoption_readoption_count = 0
```

The first qualification/adoption is the only physical promotion edge for that leg.

## 6. Event ordering

The runtime SHALL maintain a monotonic closure event sequence.

Required order:

```text
qualification_sequence
< physical_receipt_sequence
< adoption_sequence
< active_ready_sequence
<= first_post_adoption_use_sequence
< d09_observation_sequence
```

No successful `assert_active_ready()` may occur before adoption.

## 7. Hash reseal

The pre-adoption and adopted qualification hashes SHALL both be recorded.

Required:

```text
pre_adoption_receipt_hash != post_adoption_receipt_hash
```

The adopted receipt SHALL validate under the canonical C08 qualification hash after:

```text
hot_path_wait_count = physical.hot_path_exact_wait_count
active_physical_admission = physical.physical_admission_pass
```

The active value provenance SHALL be:

```text
CF1_PHYSICAL_RECEIPT_PHYSICAL_ADMISSION_PASS
```

and not a literal, runtime mode bit, environment flag, or static contract.

## 8. Active-ready ordering

`assert_active_ready()` SHALL succeed only after physical adoption and hash reseal.

Required runtime evidence:

```text
pre_adoption_active_ready_success_count = 0
active_ready_assert_count > 0
active_ready_sequence > adoption_sequence
```

## 9. Multi-step adopted-authority reuse

After the first adoption, subsequent optimizer steps SHALL reuse the adopted qualification without re-running the physical qualification fixture.

Required:

```text
post_adoption_reuse_observation_count > 0
post_adoption_requalification_count = 0
post_adoption_readoption_count = 0
```

This applies across multi-invocation legs as long as the same leg-local production runtime is parked/restored rather than reconstructed.

## 10. Production device / queue continuity

CF1A establishes MCU R7 production identity during qualification. CLOSE-R1 SHALL verify the adopted production path continues under the same authority:

```text
first_post_adoption_device_id == production_device_id
first_post_adoption_queue_id  == production_queue_id
```

Device or queue drift after adoption fails closed.

## 11. Terminal fixture closure

At leg closure the original CF1 physical fixtures SHALL be terminal:

```text
callback terminal closed
map terminal closed / unmapped
deferred retirement terminal closed
deferred retirement final length = 0
fixture resource leak count = 0
```

CF1-CLOSE-R1 does not introduce an alternate cleanup path.

## 12. Exact-wait closure

The qualification-only parity wait remains physically exercised:

```text
qualification_only_exact_wait_count > 0
```

Candidate-like CF1 qualification windows remain:

```text
hot_path_exact_wait_observation_window_count >= 2
hot_path_exact_wait_count = 0
```

The adopted production interval SHALL also be measured and satisfy:

```text
post_adoption_hot_path_exact_wait_observed = true
post_adoption_hot_path_exact_wait_count = 0
```

The post-adoption counter observation SHALL use a telemetry counter snapshot that does not trigger a full lease census or key materialization.

## 13. Binary identity

Each leg receipt binds:

```text
runtime_binary_sha256
native_cf1_release_binary_sha256
```

and requires exact equality. A receipt from another release binary is not an ACTIVE authority.

## 14. D09 handoff

D09 policy is unchanged. CLOSE-R1 only observes the semantic input after adoption.

Required:

```text
d09_c08_mode = ActiveAsync
d09_c08_active_physical_admission = true
d09_observation_sequence > adoption_sequence
```

CLOSE-R1 does not decide D09 promotion or modify benchmark thresholds, lane selection, measured-phase rules, or sample requirements.

## 15. R4D preservation

C08 closure may enrich audit lineage but SHALL NOT alter R4D semantic predicates.

The existing R4D-R2 / CF2 / CF3 / CLOSE-R1 modules and policies remain byte/semantic-preserved relative to the CF1A parent.

## 16. Leg receipt

`C08ActivePhysicalAdmissionCf1CloseR1Receipt` SHALL include at minimum:

- campaign leg and campaign identity;
- current/native-CF1 binary hashes and equality;
- MCU R7 production device/queue identity;
- pre-adoption local hash and false state;
- CF1 physical receipt hash and CF1/CF1A PASS states;
- source qualification hash match;
- qualification/materialization/adoption/ready counters;
- event sequence ordinals;
- post-adoption receipt hash and reseal result;
- active-value provenance;
- reuse/requalification/readoption counters;
- post-adoption device/queue continuity;
- callback/map/deferred-retirement terminal closure;
- qualification and post-adoption exact-wait witnesses;
- D09 handoff fields;
- physical, semantic, and lineage closure classifications;
- PASS token and receipt hash.

## 17. Leg PASS predicates

Physical closure requires at minimum:

```text
binary identity match
CF1 physical pass
CF1A identity pass
post-adoption device/queue continuity
callback/map/retirement terminal closure
fixture_resource_leak_count = 0
qualification-only exact wait observed
candidate hot-path exact wait = 0
post-adoption exact wait observed = 0
```

Semantic closure requires at minimum:

```text
pre-adoption active = false
source qualification hash match
qualification/materialization/adoption each exactly once
no pre-adoption active-ready success
correct sequence ordering
post-adoption active = true
reuse observed
no requalification
no readoption
D09 active handoff observed
```

Lineage closure requires at minimum:

```text
pre hash != post hash
active source = CF1_PHYSICAL_RECEIPT_PHYSICAL_ADMISSION_PASS
current binary = native CF1 release binary
```

A leg PASS exists only when physical, semantic, and lineage closure all pass.

## 18. A/B/C leg-local authority

Each Full Production ABC leg SHALL start from its own non-active C08 runtime authority and independently execute qualification and adoption.

Forbidden:

```text
leg A physical receipt → leg B adoption
leg B physical receipt → leg C adoption
leg A adopted runtime authority → leg B/C
```

Disk JSON receipts remain audit artifacts only and SHALL NOT be deserialized into live ACTIVE authority.

## 19. ABC aggregate receipt

After successful A/B/C execution, the physical campaign SHALL read and validate each leg-local CLOSE receipt and create:

```text
c08_active_physical_admission_cf1_close_r1_abc_receipt.json
```

The aggregate SHALL require:

```text
all three leg receipts valid
all three binary bindings valid
all three CF1 PASS
all three CF1A PASS
adoption exactly once per leg
hash reseal pass per leg
active-ready after adoption per leg
post-adoption reuse per leg
no requalification per leg
no readoption per leg
no cross-leg physical receipt reuse
no cross-leg active authority reuse
D09 handoff observed per leg
```

Only then may it emit:

```text
PASS_ASH_C08_ACTIVE_PHYSICAL_ADMISSION_CF1_CLOSE_R1_ABC
```

## 20. Fail-closed attribution

At minimum the implementation SHALL retain or materialize dedicated failures for:

```text
FAIL_C08_CF1_CLOSE_R1_LOCAL_RECEIPT_MISSING
FAIL_C08_CF1_CLOSE_R1_LOCAL_ALREADY_ACTIVE
FAIL_C08_CF1_CLOSE_R1_CF1_PHYSICAL_PASS_MISSING
FAIL_C08_CF1_CLOSE_R1_CF1A_IDENTITY_PASS_MISSING
FAIL_C08_CF1_CLOSE_R1_SOURCE_QUALIFICATION_HASH_DRIFT
FAIL_C08_CF1_CLOSE_R1_MULTIPLE_ADOPTION
FAIL_C08_CF1_CLOSE_R1_ADOPTION_ORDER_VIOLATION
FAIL_C08_CF1_CLOSE_R1_PRE_ADOPTION_ACTIVE_READY
FAIL_C08_CF1_CLOSE_R1_HASH_NOT_RESEALED
FAIL_C08_CF1_CLOSE_R1_POST_ADOPTION_RECEIPT_INVALID
FAIL_C08_CF1_CLOSE_R1_POST_ADOPTION_REQUALIFICATION
FAIL_C08_CF1_CLOSE_R1_POST_ADOPTION_READOPTION
FAIL_C08_CF1_CLOSE_R1_POST_ADOPTION_DEVICE_DRIFT
FAIL_C08_CF1_CLOSE_R1_POST_ADOPTION_QUEUE_DRIFT
FAIL_C08_CF1_CLOSE_R1_POST_ADOPTION_EXACT_WAIT_NONZERO
FAIL_C08_CF1_CLOSE_R1_FIXTURE_RESOURCE_LEAK
FAIL_C08_CF1_CLOSE_R1_CROSS_LEG_PHYSICAL_RECEIPT
FAIL_C08_CF1_CLOSE_R1_CROSS_LEG_ACTIVE_AUTHORITY
FAIL_C08_CF1_CLOSE_R1_BINARY_IDENTITY_MISMATCH
FAIL_C08_CF1_CLOSE_R1_STALE_BINARY_RECEIPT
FAIL_C08_CF1_CLOSE_R1_D09_HANDOFF_UNOBSERVED
```

## 21. Static gates

`tools/validate_ash_c08_active_physical_admission_cf1_close_r1_static.py` SHALL verify:

- CF1 and CF1A authority tokens remain present;
- local false and evidence-derived promotion remain intact;
- one-shot adoption and sequencing state exist;
- pre/post receipt hashes and hash-reseal path exist;
- adopted production reuse is observed without physical requalification;
- post-adoption exact-wait observation uses a counter-only, no-census snapshot;
- production device/queue continuity is enforced;
- leg receipt and ABC aggregate are materialized;
- D09 handoff is observation-only;
- D09, R4D, Cargo manifests, and WGSL remain parent-preserved.

## 22. Final freeze condition

Once Full Production ABC emits the ABC PASS token, C08 physical qualification, production identity, adoption, hash reseal, post-adoption reuse, and D09 handoff are considered CLOSED and C08 becomes a frozen dependency unless new physical evidence demonstrates regression.

The next development authority returns to R4D-R2 closure, beginning with real source-alias physical observation.

## Final invariant

```text
LOCAL FALSE
+ CF1 PHYSICAL PASS
+ CF1A PRODUCTION AUTHORITY PASS
+ ONE-SHOT ADOPTION
+ HASH RESEAL
+ ACTIVE-READY ORDER
+ MULTI-STEP REUSE
+ OBSERVED ZERO POST-ADOPTION EXACT WAIT
+ A/B/C LEG ISOLATION
+ D09 HANDOFF
=
C08 ACTIVE PHYSICAL ADMISSION CLOSED
```
