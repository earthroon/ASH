# ASH-BASETRAIN-UNIFIED-ATLAS-MCU-LOCAL-MUON-PRODUCTION-PENDING-WAVE-QUEUE-CUTOVER-AND-ACTIVE-ASYNC-PHYSICAL-QUALIFICATION-CLOSURE-R1

## Production Pending-Wave Queue / Exact R6 Multi-Epoch Authority / B05-B06-C07-C08 Mode-Matrix Preservation / Active-Device Pending Handoff Gate / Bounded Multi-Wave In-Flight Qualification / Parent-P5 PASS Closure

---

# 0. Revision identity

Revision:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-LOCAL-MUON-PRODUCTION-PENDING-WAVE-QUEUE-CUTOVER-AND-ACTIVE-ASYNC-PHYSICAL-QUALIFICATION-CLOSURE-R1`

Parent implementation revision:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-LOCAL-MUON-PENDING-SUBMISSION-HANDLE-AND-LATER-COLLECT-MATERIALIZATION-CLOSURE-R1`

Parent semantic closure to finish:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-SUBMISSION-EPOCH-DEPENDENCY-TRACKING-AND-ACTIVE-ASYNC-COMPLETION-CLOSURE-R1`

Child PASS token:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_LOCAL_MUON_PRODUCTION_PENDING_WAVE_QUEUE_CUTOVER_AND_ACTIVE_ASYNC_PHYSICAL_QUALIFICATION_CLOSURE_R1`

Parent P5 PASS token:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_SUBMISSION_EPOCH_DEPENDENCY_TRACKING_AND_ACTIVE_ASYNC_COMPLETION_CLOSURE_R1`

Static PASS token:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_LOCAL_MUON_PRODUCTION_PENDING_WAVE_QUEUE_CUTOVER_ACTIVE_ASYNC_R1_STATIC`

---

# 1. Purpose

The previous child proved that the Local Muon backend can physically return a `PendingTensorCubeLocalMuonWaveR1` after real Queue submission and before an exact blocking wait.

The intended next state is a production loop that owns more than one such pending Wave and completes them through the exact P5/P4 authority chain:

```text
submit A
A remains pending
submit B
A+B simultaneously tracked
observe real SubmissionEpoch completion
collect exact Wave
close P5 semantic dependencies
retire exact P4 lease
reuse capacity
```

This revision owns the production-cutover requirements and the prerequisite state repairs discovered while attempting that cutover.

---

# 2. Source-derived correction: R6 was single-current-epoch

The parent R6 queue previously stored one current descriptor vector and one current queue generation.

That topology is valid for synchronous WITHIN_WAVE execution but not for real multi-Wave overlap.

Example failure without repair:

```text
seal A -> queue generation 10
submit A
seal B -> queue generation 11
complete A -> stale-generation rejection
```

Therefore production ActiveAsync cannot be materialized by only adding a `VecDeque<PendingWave>` around the existing callsite.

R6 itself first requires exact simultaneous epoch ownership.

---

# 3. R6 exact multi-epoch ledger

R6 is extended with an exact active-epoch ledger:

```rust
struct McuTensorCubeJobEpochStateR6 {
    seal: McuTensorCubeJobEpochSealR6,
    descriptors: Vec<McuTensorCubeJobDescriptorR6>,
}
```

and:

```rust
active_epochs: BTreeMap<(u64, u64), McuTensorCubeJobEpochStateR6>
```

The key is:

```text
(queue_generation_id, queue_epoch_id)
```

Each sealed Wave owns its own immutable/exact R6 descriptor set until that exact epoch completes.

---

# 4. R6 ownership rule

R6 generation creation remains owned by R6.

The new ledger does not create a second queue-generation counter.

It changes storage from:

```text
one current descriptor authority
```

to:

```text
multiple exact active epoch authorities
```

while preserving one monotonic R6 generation/epoch sequence.

---

# 5. R6 exact lookup

The following operations resolve the exact active epoch identified by the supplied seal:

- Atlas lease validation;
- execution descriptor materialization;
- R8 descriptor snapshot;
- homogeneous R8 expert application;
- R8A expert application;
- R8A execution descriptor materialization;
- epoch completion.

They do not implicitly use the most recently sealed Wave.

---

# 6. R6 completion

`complete_epoch()` removes only:

```text
(seal.queue_generation_id, seal.queue_epoch_id)
```

from the active ledger.

Completion of A after B has already been sealed is legal if A's exact seal, descriptor manifest and completion evidence still match.

---

# 7. R6 closure

Final R6 closure additionally requires:

```text
active_epochs.is_empty()
```

A receipt cannot claim complete queue closure while an exact in-flight R6 epoch remains live.

---

# 8. Source-derived correction: R8A remains single-current-view

The current R8A authority owns one current bucket view lifecycle.

Its state machine is not yet a multi-view asynchronous ledger.

Therefore the first Local Muon production ActiveAsync scope MUST NOT silently overlap multiple heterogeneous R8A views.

This revision does not claim R8A multi-view ActiveAsync closure.

---

# 9. Initial asynchronous routing scope

The first production queue closure is restricted to the exact Local Muon scope that does not require simultaneous R8A current-view ownership.

Heterogeneous R8A asynchronous overlap remains a later explicit child.

Required declaration in this revision's receipt:

```text
homogeneous_local_muon_scope_only = true
r8a_async_multi_view_materialized = false
```

---

# 10. Source-derived correction: P2 ShadowObserved lifetime

The current P2 real-Wave shadow comparison is built around the canonical result and exact pre-state under the existing synchronous lifetime.

This revision MUST NOT assume P2 ShadowObserved can safely extend across multiple asynchronous pending Waves without an exact snapshot/consumer-lifetime materialization.

A later ActiveAsync production cutover must either:

1. explicitly bind P2 to independently owned snapshots/leases; or
2. prohibit P2 ShadowObserved during the first physical ActiveAsync qualification campaign.

No silent lifetime inference is allowed.

---

# 11. Critical source-derived correction: C08 Active mode matrix

Current C08 `AsyncRetirementRuntimeMode::ActiveAsync` requires:

```text
B06 ActiveVerified
+
C07 ActiveCompact
+
segmented device successor admitted
```

The callsite enforces the matching upstream chain:

```text
B06 ActiveVerified
-> B05 ActiveDeviceCandidate
```

This is existing source authority and is not weakened by P5.

---

# 12. Current pending backend physical domain

The already materialized Local Muon pending submit/collect backend currently requires:

```text
device_candidate_mode.device_candidate_enabled()
+
device_candidate_mode.bulk_readback_required()
```

and fails otherwise with:

`E_MCU_PENDING_R1_MIRROR_VERIFIED_READBACK_REQUIRED`.

`bulk_readback_required()` is true for the current MirrorVerified path and false for `ActiveDeviceCandidate`.

Therefore the existing pending backend split is real, but its currently materialized physical domain is the MirrorVerified bulk-readback domain.

---

# 13. Why parent P5 ActiveAsync is still blocked

The current parent requirements form this chain:

```text
P5 ActiveAsync
-> C08 ActiveAsync
-> B06 ActiveVerified + C07 ActiveCompact
-> B05 ActiveDeviceCandidate
```

but the currently materialized Atlas-wave pending backend path requires:

```text
B05 MirrorVerified-compatible bulk readback
```

Both cannot be true for the same production Wave under the current source.

Therefore production ActiveAsync PASS MUST remain fail-closed.

---

# 14. No mode-matrix bypass

This revision MUST NOT obtain an apparent async PASS by any of the following:

- weakening C08 Active upstream admission to Mirror parents without a separate qualified contract;
- pretending B05 MirrorVerified is B05 ActiveDeviceCandidate;
- reporting host candidate vectors in B05 ActiveDeviceCandidate mode;
- moving an exact wait to another thread;
- ignoring B06/C07 active requirements;
- using the generic pending capability boolean as proof of ActiveDeviceCandidate pending handoff.

---

# 15. Distinct source-truth capabilities

The generic child capability remains:

`TENSORCUBE_LOCAL_MUON_ASYNC_SUBMIT_COLLECT_SPLIT_MATERIALIZED_P5_R1 = true`

because a real submit-before-wait pending API exists.

This revision introduces the stricter production Active-device capability:

`TENSORCUBE_LOCAL_MUON_PRODUCTION_ACTIVE_DEVICE_PENDING_HANDOFF_MATERIALIZED_P5_R1`

Current source value for this bake:

`false`.

These booleans answer different questions and MUST NOT be collapsed.

---

# 16. Active-device pending handoff meaning

The stricter capability may become true only when the Atlas-wave pending path supports the actual B05 ActiveDeviceCandidate/B06/C07 Active successor contract without violating active-mode no-bulk-readback invariants.

At minimum the implementation must prove one of the following exact physical handoffs:

1. a pending device-candidate object whose candidate weight/momentum/update remain GPU-resident until B06 consumes them; or
2. an equivalent existing device-resident successor authority already accepted by B06/C07.

Host candidate materialization is not an acceptable substitute in ActiveDeviceCandidate mode.

---

# 17. Current fail-closed admission

`ProductionMuonPendingQueueCutoverRuntimeR1::new()` rejects P5 ActiveAsync while the active-device pending handoff capability is false.

Required error:

`E_MCU_P5_ACTIVE_DEVICE_CANDIDATE_ATLAS_WAVE_PENDING_HANDOFF_REQUIRED`.

The failure occurs before a production Wave can be mislabeled as ActiveAsync-cutover evidence.

---

# 18. Production queue receipt authority

`ProductionMuonPendingQueueCutoverReceiptR1` records at minimum:

- generic pending backend capability;
- P4 exact lease authority presence;
- P5 ActiveAsync mode;
- ActiveDeviceCandidate pending handoff materialization state;
- homogeneous Local Muon scope declaration;
- R8A multi-view materialization state;
- configured maximum in-flight Waves;
- submitted Wave count;
- peak pending Wave count;
- submit-while-prior-pending count;
- collected Wave count;
- semantic-consumed Wave count;
- P4-retired Wave count;
- active-path exact-wait count;
- duplicate/stale completion reject counts;
- orphan submission count;
- final pending count;
- parent P5 PASS observation;
- verdict/PASS token/digest.

---

# 19. Child PASS predicate

Full child PASS requires all of:

```text
P5 mode = ActiveAsync
active-device pending handoff materialized = true
generic pending backend capability = true
P4 exact lease prerequisite closed = true
submitted_wave_count > 1
peak_pending_wave_count > 1
submit_while_prior_pending_count > 0
collected_wave_count = submitted_wave_count
semantic_consumed_wave_count = submitted_wave_count
p4_retired_wave_count = submitted_wave_count
active_path_exact_wait_count = 0
duplicate_completion_reject_count > 0
stale_completion_reject_count > 0
orphan_submission_count = 0
final_pending_count = 0
parent P5 PASS = true
```

Current bake cannot satisfy this predicate because the active-device pending handoff source capability is false.

---

# 20. Parent P5 remains canonical ActiveAsync truth

This child MUST NOT create a parallel ActiveAsync PASS authority.

Even after production queue cutover is implemented, the canonical ActiveAsync closure remains the parent P5 receipt.

Only the parent receipt may derive:

```text
active_async_enabled = true
per_wave_exact_wait_retired = true
```

from its complete physical predicate.

---

# 21. Intended future production queue topology

Once the ActiveDeviceCandidate pending handoff exists, production cutover uses a bounded runtime-local pending queue:

```text
ProductionMuonRuntime
  owns pending Wave queue

PendingTensorCubeLocalMuonWaveR1
  owns physical pending resources

P5 ledger
  owns SubmissionEpoch/semantic dependency truth

P4 runtime
  owns exact Atlas lease lifetime

B05/B06/C07
  own device-candidate/device-commit/evidence authority
```

No process-global pending queue is introduced.

---

# 22. Intended production submission ordering

For Wave A:

```text
acquire exact P4 lease
-> seal exact R6 epoch
-> route exact R8 authority
-> submit ActiveDeviceCandidate pending work
-> receive real SubmissionEpoch
-> bind exact P4 submission
-> register exact P5 dependency entry
-> insert production pending entry
-> allow later independent Wave admission
```

Registration must be complete before Wave B is admitted.

---

# 23. Intended bounded overlap

First physical qualification target:

`max_in_flight_waves = 2`.

The required real witness is:

```text
A has a real SubmissionEpoch and remains unretired
B receives a real SubmissionEpoch
peak exact in-flight Wave count >= 2
```

Thread count or timestamps alone are insufficient.

---

# 24. Intended completion identity

Completion is resolved by exact real SubmissionEpoch.

No completion-order indexing is allowed.

A completion for B may advance only B.

A stale completion from an old P4 lease generation may not modify a newer same-slot generation.

---

# 25. Intended semantic retirement

Physical completion alone is insufficient.

Required chain:

```text
physical completion
-> device candidate/evidence consumer completion
-> all exact P5 consumers released
-> P5 SemanticComplete
-> P4 exact lease retirement
-> pending queue capacity released
```

The production queue does not free Atlas slots directly.

---

# 26. Intended P3 boundary

P3 PREPARE cannot consume a parameter/optimizer target until every mandatory Wave needed by that target has reached the exact state required by B05/B06/P5 and no pending result is semantically incomplete.

Async GPU execution may overlap.

Optimizer transaction semantics may not reorder.

---

# 27. No hidden exact wait

When full cutover is eventually admitted, the ordinary ActiveAsync Wave path must record:

`active_path_exact_wait_count = 0`.

A shutdown/fatal global drain may block and is classified separately.

A blocking wait performed once for every normal Wave is not a drain merely because it uses a different function name.

---

# 28. Backpressure

Future bounded queue admission must prefer explicit backpressure over:

- host spill;
- silent synchronous fallback;
- exceeding the P4 ring capacity;
- disabling memory guards;
- overwriting an active R6/P4/P5 identity.

---

# 29. R8A future child requirement

After homogeneous Local Muon ActiveAsync is closed, heterogeneous overlap requires an R8A multi-view ledger whose identity is at least sufficient to preserve multiple simultaneously live bucket-view generations.

Until that child exists:

`r8a_async_multi_view_materialized = false`.

No R8A ActiveAsync PASS is implied by this revision.

---

# 30. P2 future child requirement

If P2 ShadowObserved must coexist with real multi-Wave ActiveAsync, it requires an explicit async shadow lifetime/snapshot contract.

Until that contract is materialized, physical P5 qualification should not count a Wave whose P2 shadow lifetime is ambiguous.

---

# 31. Static validator

Validator:

`tools/validate_ash_basetrain_unified_atlas_mcu_local_muon_production_pending_wave_queue_cutover_active_async_r1_static.py`.

It verifies at minimum:

- child module/export;
- production cutover receipt/runtime schema;
- explicit ActiveDeviceCandidate pending-handoff source capability;
- capability currently false;
- exact fail-closed error;
- R6 exact active-epoch ledger;
- exact R6 epoch removal at completion;
- no single-current R6 descriptor SSOT remains;
- existing pending backend still has MirrorVerified bulk-readback gate;
- pending module still contains no exact blocking wait;
- current C08 Active upstream admission remains intact;
- current B06 Active -> B05 ActiveDeviceCandidate mode matrix remains intact;
- parent P5 physical PASS remains evidence-derived;
- no unadmitted production ActiveAsync helper is wired around the blocker.

Static PASS proves the blocker is represented correctly. It does not prove physical ActiveAsync.

---

# 32. R6 validator update

The existing R6 static validator is updated to validate the exact active-epoch ledger instead of requiring the obsolete single preallocated descriptor vector implementation.

This is a validator adaptation to the new R6 SSOT, not a relaxation of R6 invariants.

---

# 33. R8A validator update

The existing R8A static validator's R6 integration token is updated from the obsolete global `self.descriptors` form to exact epoch descriptor-manifest materialization.

Its final specification-presence gate remains unchanged.

---

# 34. Required Rust tests before ActiveDevice capability flip

At minimum:

```text
R6:
A_seal_then_B_seal_then_A_complete_is_valid
B_complete_does_not_remove_A_epoch
unknown_epoch_complete_rejected
same_epoch_duplicate_active_insert_rejected
final_receipt_requires_zero_active_epochs

mode matrix:
P5_active_rejected_without_active_device_pending_handoff
mirror_pending_capability_does_not_imply_active_device_handoff
B06_active_requires_B05_active_device_candidate

future handoff:
active_device_pending_submit_returns_before_completion
active_device_pending_path_has_zero_bulk_candidate_d2h
active_device_pending_backing_survives_until_B06_consumer
```

---

# 35. Required physical campaign after missing handoff is materialized

Only after `TENSORCUBE_LOCAL_MUON_PRODUCTION_ACTIVE_DEVICE_PENDING_HANDOFF_MATERIALIZED_P5_R1=true` is source-truth may the full campaign run:

1. release compile;
2. valid P1 current immutable bundle;
3. P4 physical lease PASS;
4. valid B05 ActiveDeviceCandidate authority;
5. B06 ActiveVerified;
6. C07 ActiveCompact;
7. C08 ActiveAsync admitted;
8. P5 ActiveAsync qualification mode;
9. homogeneous Local Muon scope;
10. bounded pending queue = 2;
11. submit real Wave A;
12. register exact A R6/P4/P5 identities;
13. submit real Wave B before A retirement;
14. prove peak in-flight > 1;
15. observe real exact completion identities;
16. close exact device-candidate/evidence semantic consumers;
17. retire exact P4 generations;
18. reuse a slot with generation +1;
19. replay stale old-generation completion;
20. replay duplicate completion;
21. require no new-generation mutation;
22. drain production/P5/P4 state to zero;
23. seal parent P5 PASS;
24. seal child PASS.

---

# 36. Current bake state

This bake materializes:

```text
R6 exact multi-epoch storage              MATERIALIZED
R6 exact per-seal descriptor lookup       MATERIALIZED
R6 out-of-order exact epoch completion    STRUCTURALLY MATERIALIZED
R6 final active-epoch drain gate          MATERIALIZED
production cutover receipt/runtime        MATERIALIZED
ActiveDevice pending-handoff source gate  MATERIALIZED
mode-matrix fail-closed error              MATERIALIZED
child static validator                    PASS
parent P5/P4/P3/P2/P1/P0 static chain     PASS where applicable
```

This bake does not claim:

```text
ActiveDeviceCandidate Atlas-wave pending handoff   MATERIALIZED
production peak in-flight > 1                      PHYSICALLY OBSERVED
parent P5 ActiveAsync PASS                         OBSERVED
per_wave_exact_wait_retired = true                 VALID
active_async_enabled = true                        VALID
```

---

# 37. Why this bake does not flip the stricter capability

The current pending backend still materially requires the MirrorVerified bulk-readback contract.

Flipping the ActiveDevice pending capability now would cause the source to claim a physical path that the B05 ActiveDeviceCandidate no-bulk-readback contract explicitly forbids.

Therefore `false` is the only source-truth value in this bake.

---

# 38. Next exact implementation gate

The next gate is no longer "add a queue".

It is:

`LOCAL-MUON-ATLAS-WAVE-ACTIVE-DEVICE-CANDIDATE-PENDING-HANDOFF-AND-DEVICE-SUCCESSOR-COLLECT-CLOSURE-R1`.

That child must preserve B05 ActiveDeviceCandidate semantics while allowing the exact pending resource lifetime needed by C08/P5 ActiveAsync.

Only after that child is physically real should the production pending queue be enabled.

---

# 39. After full P5 closure

Only after the parent P5 physically emits:

```text
active_async_enabled = true
per_wave_exact_wait_retired = true
```

should the roadmap advance to:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-PHYSICAL-PRESSURE-FEATURE-PRODUCERS-AND-ROUTER-COST-ACTIVATION-R8B`.

That ordering prevents R8 from consuming pressure signals whose ActiveAsync ownership is not yet physically exact.

---

# 40. Packaging policy

Implementation source ZIP excludes:

- this specification and all `specs/` content;
- Markdown patch notes;
- `BAKE_MANIFEST*`;
- generated P0-P5 receipts/evidence;
- generated production pending queue receipts;
- generated qualification/runtime JSON or JSONL;
- `current.json`;
- `publication_seal.json`;
- P3 transaction runtime artifacts;
- validation logs;
- review artifacts.

Rust/Python implementation source remains included.

---

# 41. GitHub publication policy

GitHub publication for this revision is spec-only unless implementation publication is separately requested.

---

# 42. PASS semantics

Full revision PASS means the actual B05 ActiveDeviceCandidate/B06/C07/C08 production chain can submit and own multiple exact Local Muon Waves simultaneously through a bounded Production Muon pending queue, every Wave has a distinct exact R6 epoch, P4 lease generation and P5 SubmissionEpoch dependency identity, no ordinary Wave uses a per-Wave exact wait, all device-resident candidate/evidence consumers close before P4 retirement, stale or duplicate completion cannot affect another residency generation, the queue drains to zero, and the canonical parent P5 receipt physically derives ActiveAsync enabled and per-Wave exact-wait retired.

The current source bake does not claim that PASS.

---

# 43. Final authority declaration

Before this bake:

```text
The pending backend existed, but R6 still had a single-current-epoch shape and the production-cutover mode matrix had not been explicitly reconciled.
```

After this bake:

```text
R6 can hold exact identities for more than one live Wave.
The production cutover has its own typed receipt/runtime authority.
The source also explicitly states why production ActiveAsync is not yet admissible:
C08 requires the active B05/B06/C07 chain, while the current Atlas-wave pending backend is still MirrorVerified bulk-readback scoped.

That incompatibility is now a gate, not a hidden assumption.
No source path can turn the generic pending capability into an ActiveDeviceCandidate production PASS by accident.
```

---

# 44. Center sentence

> **Pending handle 하나 만든다고 production async가 되는 건 아니었다. R6도 A와 B를 동시에 기억할 수 있어야 하고, 더 중요한 건 C08 Active가 요구하는 B05/B06/C07의 실제 모드와 pending backend의 물리 계약이 같아야 한다. 이번 베이크는 R6의 기억을 여러 epoch로 넓히고, 그 모드 차이를 전용 게이트로 봉인한다. 다음에는 Mirror readback pending을 ActiveDeviceCandidate의 device-resident pending handoff로 바꾼다. 그 뒤에야 A가 살아 있는 동안 B를 던지는 production queue를 진짜로 켤 수 있다.**