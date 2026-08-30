# ASH-BASETRAIN-UNIFIED-ATLAS-MCU-LOCAL-MUON-DEVICE-SEGMENTED-SOURCE-DIRECT-SUBMIT-AND-NEXT-GENERATION-REUSE-CLOSURE-R1

## Concrete Muon Device Segmented Source Authority / Read-Only Source Lease / Direct GPU Weight-Momentum Binding / Zero Source H2D / Exact Queue-Device Identity / Source Reader Lifetime / Real SubmissionEpoch Completion / G+1 Reuse Evidence / No Host Mirror Fallback

---

# 0. Revision identity

Revision:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-LOCAL-MUON-DEVICE-SEGMENTED-SOURCE-DIRECT-SUBMIT-AND-NEXT-GENERATION-REUSE-CLOSURE-R1`

Parent:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-BP-DK-DEVICE-RESIDENT-POST-UPDATE-EVIDENCE-AND-DEVICE-SEGMENTED-SUCCESSOR-APPLICATION-CLOSURE-R1`

PASS token reserved for physical closure:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_LOCAL_MUON_DEVICE_SEGMENTED_SOURCE_DIRECT_SUBMIT_AND_NEXT_GENERATION_REUSE_CLOSURE_R1`

Static PASS:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_LOCAL_MUON_DEVICE_SEGMENTED_SOURCE_DIRECT_SUBMIT_R1_STATIC`

---

# 1. Purpose

The parent revision materializes a concrete `MuonDeviceSegmentedGenerationR1` whose parameter segments own real candidate-weight and Muon-momentum GPU backing produced by a prior ActiveDevice Local Muon execution.

Before this revision the next Local Muon ActiveDevice submit still required host `&[f32]` source weight and source momentum and staged both through H2D upload arenas.

This revision adds a distinct direct-source path in which a complete `MuonDeviceSegmentedGenerationR1` issues a read-only physical source lease and the Local Muon bind group consumes that lease's GPU weight/momentum buffers directly.

The new path does not materialize source host vectors and does not stage source weight or source momentum through H2D.

---

# 2. Center transition

Before:

```text
MuonDeviceSegmentedGenerationR1(G+1)
    exists on device

next Local Muon
    host weight &[f32]
    host momentum &[f32]
        -> H2D
        -> GPU submit
```

After:

```text
MuonDeviceSegmentedGenerationR1(G+1)
        -> MuonDeviceSegmentedSourceLeaseR1
        -> direct weight/momentum device bindings
        -> real Queue submit
        -> real SubmissionEpoch
        -> exact physical completion
        -> source reader release
        -> candidate generation G+2
```

---

# 3. Core invariant

For the direct-source path:

`source authority = exact published MuonDeviceSegmentedGenerationR1 segment`.

It is not:

- a stale host model mirror;
- a reconstructed host Vec;
- a device-to-host-to-device bridge;
- an implicit "latest generation" lookup after Wave admission.

---

# 4. Source-truth capability

Backend source truth:

`TENSORCUBE_LOCAL_MUON_DEVICE_SEGMENTED_SOURCE_DIRECT_SUBMIT_MATERIALIZED_R1 = true`.

The parent compatibility alias:

`TENSORCUBE_LOCAL_MUON_DEVICE_SEGMENTED_SOURCE_SUBMIT_MATERIALIZED_R1`

now derives from that backend source capability.

No ENV, CLI, qualification fixture or receipt field may force the capability.

---

# 5. Aggregate BP-DeltaK gate remains fail-closed

The parent aggregate remains the conjunction of:

1. segmented backing handoff;
2. device BP-DeltaK reduction/exact digest;
3. device segmented source direct submit.

Current source state in this bake:

```text
segmented backing handoff           true
device segmented source submit      true
device reduction / exact digest     false
aggregate BP-DK device consumer     false
production queue cutover            false
```

This revision does not unlock production ActiveAsync by itself.

---

# 6. Scope

R1 direct source is materialized for:

- Local Muon;
- B04A Atlas-wave resident execution;
- B05 ActiveDeviceCandidate;
- homogeneous/default Local Muon expert;
- homogeneous R8 expert override;
- exact one-physical-batch source segment;
- source weight and source Muon momentum.

R1 does not materialize R8A asynchronous multi-view source submission.

---

# 7. Existing host path preserved

The existing host-source ActiveDevice APIs remain present and continue to stage host source weight/momentum through A03 upload arenas.

They are not counted as device-source qualification evidence.

The direct-source APIs are separate and have no source `&[f32]` arguments.

---

# 8. Direct source APIs

Materialized backend APIs:

`submit_resident_active_device_candidate_from_segmented_source_p4_p5_pending_r1`

and:

`submit_resident_active_device_candidate_from_segmented_source_with_expert_r8_p4_p5_pending_r1`.

Both accept `MuonDeviceSegmentedSourceLeaseR1` instead of host source weight/momentum slices.

---

# 9. Direct source lease

`MuonDeviceSegmentedSourceLeaseR1` binds:

- source generation;
- canonical parameter index;
- exact element count;
- generation digest;
- segment backing digest;
- weight physical allocation ID;
- momentum physical allocation ID;
- weight GPU buffer;
- momentum GPU buffer;
- shared active-reader authority;
- exact submitted SubmissionEpoch after Queue submission.

---

# 10. Generation completeness prerequisite

`MuonDeviceSegmentedGenerationR1::issue_source_lease_r1()` first obtains and validates the generation publication receipt.

A source lease cannot be issued unless:

```text
published_parameter_count == expected_parameter_count
published_element_count == expected_element_count
missing_parameter_count == 0
missing_element_count == 0
complete == true
```

Failure:

`E_MCU_DEVICE_SEGMENTED_SOURCE_R1_GENERATION_INCOMPLETE`.

---

# 11. Exact parameter binding

A direct submit binds one exact canonical parameter index before physical submission.

The source lease's parameter index must equal the requested direct-source parameter index.

Failure:

`E_MCU_DEVICE_SEGMENTED_SOURCE_R1_PARAMETER_MISMATCH`.

---

# 12. Exact generation binding

The source lease generation must equal `resident_request.source_generation`.

Failure:

`E_MCU_DEVICE_SEGMENTED_SOURCE_R1_GENERATION_MISMATCH`.

Candidate generation remains exactly source generation + 1 under the existing Local Muon resident request contract.

---

# 13. Exact R1 range contract

The current R1 source backing ABI represents one exact physical source segment and does not yet provide sub-buffer element-offset source leases.

Therefore the direct-source Wave requires:

`source_lease.element_count == current physical Local Muon batch element_count`.

Failure:

`E_MCU_DEVICE_SEGMENTED_SOURCE_R1_RANGE_MISMATCH`.

Later subsegment/window widening requires an explicit ABI revision rather than pointer arithmetic hidden inside R1.

---

# 14. Device authority validation

Weight and momentum physical allocation IDs must belong to the same A01 device authority.

Before encoding the direct-source submit, the current Queue's A01 device authority is resolved with `queue_authority_ids(queue)` and must equal the source allocation device authority.

Failure:

`E_MCU_DEVICE_SEGMENTED_SOURCE_R1_DEVICE_MISMATCH`.

---

# 15. Direct binding

The current R1 implementation directly binds:

- source segmented weight buffer to Local Muon binding 3;
- source segmented momentum buffer to Local Muon binding 4.

No source D2D staging is required by the current materialized path.

Current direct-source access evidence therefore records:

```text
source_weight_h2d_bytes = 0
source_momentum_h2d_bytes = 0
source_weight_d2d_bytes = 0
source_momentum_d2d_bytes = 0
host_source_materialization_count = 0
direct_device_source_bound = true
```

---

# 16. No host source fallback

The direct-source path MUST NOT call A03 source upload for weight or momentum.

The path may still stage small control data such as kernel params/status through the existing control upload authority.

That does not change source weight/momentum authority.

---

# 17. A01 submission classification

For host source mode, source weight/momentum remain owned upload leases.

For device-segmented source mode, A01 submission metadata records the source buffers as external read dependencies:

`local_muon.weight.device_segmented_r1`

and:

`local_muon.momentum.device_segmented_r1`.

The source generation's physical lifetime remains controlled by its dedicated reader lease, not by pretending A01 owns the generation backing.

---

# 18. Real SubmissionEpoch

The direct-source execution still uses the existing real `a01_submit_with_leases` Queue authority.

The exact returned SubmissionEpoch is attached to the source reader lease after submission.

No private completion sequence is introduced.

---

# 19. Source reader authority

Every `MuonDeviceSegmentBackingR1` owns a shared active-source-reader count.

Issuing a source lease increments that count.

The generation backing may not be reclaimed while any active reader remains.

---

# 20. Pre-submit cancellation

A source lease dropped before being bound to a real SubmissionEpoch releases its reader reservation.

This permits validation failure before physical submission without leaking generation reader state.

---

# 21. Post-submit early drop is fail-closed

After a source lease is bound to a real SubmissionEpoch, dropping it before exact physical completion does not declare a successful release.

The source reader remains conservatively pinned and a diagnostic is emitted.

This prefers a safe leak/failure state over reclaiming backing that the GPU may still read.

---

# 22. Exact physical reader release

The pending ActiveDevice collector already resolves exact nonblocking physical completion.

Only after the exact direct-source Wave has completed does it call source-lease release with the same SubmissionEpoch.

A different epoch is rejected with:

`E_MCU_DEVICE_SEGMENTED_SOURCE_R1_COMPLETION_EPOCH_MISMATCH`.

---

# 23. Generation reclaim preflight

`MuonDeviceSegmentedGenerationR1::release_all()` first requires aggregate active source reader count = 0 before reclaiming any segment.

This prevents partial generation destruction in which early segments are reclaimed and a later segment fails due to an active reader.

---

# 24. Backing-level reclaim gate

Each `MuonDeviceSegmentBackingR1::release()` independently verifies its active source reader count is zero before returning its weight/momentum arena leases.

This is a second fail-closed boundary beneath generation-level preflight.

---

# 25. Direct source access evidence

`MuonDeviceSegmentedSourceAccessEvidenceR1` records exact source provenance and transfer facts:

- source generation;
- canonical parameter index;
- exact element count;
- generation digest;
- segment digest;
- weight allocation ID;
- momentum allocation ID;
- weight H2D bytes;
- momentum H2D bytes;
- weight D2D bytes;
- momentum D2D bytes;
- host source materialization count;
- direct binding boolean;
- evidence digest.

---

# 26. Evidence zero requirements

`validate_direct_source()` requires:

```text
source_weight_h2d_bytes = 0
source_momentum_h2d_bytes = 0
host_source_materialization_count = 0
direct_device_source_bound = true
```

Weight and momentum allocation device identities must also match.

---

# 27. Pending and successor evidence preservation

The direct-source access evidence is stored in `PendingLocalMuonActiveDeviceCandidateR1` and later copied into `LocalMuonActiveDeviceSuccessorR1`.

The B06 successor ticket also preserves the optional direct-source access evidence.

Therefore the final candidate can prove which segmented source generation physically produced it.

---

# 28. No source authority mixing

One direct-source Wave binds both weight and momentum from the same source lease and generation segment.

The R1 direct API does not support device weight with host momentum or the inverse.

---

# 29. Source generation is read-only

The direct source lease exposes only read access to the source generation backing.

Candidate writes continue to use distinct candidate weight/momentum/update arenas for generation G+1.

The source generation G is never overwritten in place by this child.

---

# 30. Concurrent readers

Independent Waves may issue multiple read-only source leases from the same complete generation when higher-level R6 mutable-range and production admission rules allow it.

The shared reader count keeps the generation alive until all exact physical source reads complete.

---

# 31. Numerical path preservation

No Local Muon arithmetic, R7 expert arithmetic, R8 routing policy, norm reduction policy or candidate-output algorithm is changed.

Only source memory provenance changes from host-upload backing to existing device-generation backing.

---

# 32. No new epsilon

Physical qualification must use the already-qualified Local Muon numerical parity contract.

No tolerance is loosened merely because the source remained on device.

---

# 33. Physical qualification oracle

A physical campaign compares the direct segmented-source execution against the existing qualified source path for identical semantic source content and execution descriptors.

The comparison must preserve existing candidate weight, candidate momentum, orthogonal update and status gates.

---

# 34. Next-generation reuse requirement

Structural source capability alone does not prove reusable device generations.

Full revision PASS requires at least one direct-source access evidence item produced from a `MuonDeviceSegmentedGenerationR1` that itself was built from the preceding ActiveDevice candidate handoff.

The intended physical chain is:

```text
G
 -> ActiveDevice candidate
 -> MuonDeviceSegmentedGenerationR1(G+1)
 -> issue source lease from G+1
 -> direct source Local Muon submit
 -> candidate G+2
```

---

# 35. No seed-only PASS

An initial host-seeded generation may be used to bootstrap a future campaign, but it does not by itself prove next-generation reuse.

The qualifying direct-source access must come from the concrete successor-generation owner materialized by the parent child.

---

# 36. Closure receipt

`LocalMuonDeviceSegmentedSourceDirectSubmitClosureReceiptR1` records:

- direct-source source-truth capability;
- observed direct-source Wave count;
- produced-generation reuse count;
- source weight/momentum H2D bytes;
- source weight/momentum D2D bytes;
- host source materialization count;
- generation identity mismatch count;
- failed-generation source rejection count;
- final active source lease count;
- next-generation source reuse observation;
- verdict/pass token/digest.

---

# 37. Receipt evidence derivation

The physical constructor derives `produced_generation_reuse_count` from the number of validated real direct-source access evidence records.

It does not accept an externally supplied reuse count.

This avoids a free integer becoming qualification authority.

---

# 38. Structural receipt

`structural_observed()` emits:

`STRUCTURAL_OBSERVED_PHYSICAL_REUSE_PENDING`

and no PASS token.

The current assistant bake is in this state.

---

# 39. Physical PASS predicate

Full PASS requires at minimum:

```text
direct_source_capability = true
observed_direct_source_wave_count > 0
produced_generation_reuse_count > 0
source_weight_h2d_bytes = 0
source_momentum_h2d_bytes = 0
host_source_materialization_count = 0
final_active_source_lease_count = 0
next_generation_source_reuse_observed = true
```

plus the existing Local Muon numerical/status qualification.

---

# 40. No physical PASS claimed by source bake

The source bake does not contain RTX execution evidence and does not claim:

- G+1 -> G+2 physical reuse;
- physical numerical parity;
- physical zero-H2D telemetry from a real campaign;
- full revision PASS token.

---

# 41. Static validator

Validator:

`tools/validate_ash_basetrain_unified_atlas_mcu_local_muon_device_segmented_source_direct_submit_r1_static.py`.

It proves at minimum:

- direct-source backend capability true;
- source lease and access evidence types exist;
- active reader authority exists;
- exact generation publication gate exists;
- both direct source submit APIs exist;
- direct source API signatures contain no host source weight/momentum slices;
- source buffers enter A01 as external read dependencies;
- exact real SubmissionEpoch is bound to source lease;
- source lease releases only after exact physical completion;
- parent segmented generation can issue source leases;
- production queue cutover remains false;
- aggregate BP-DeltaK device consumer is not hardcoded true.

---

# 42. Parent static validator update

The parent BP-DeltaK segmented-successor validator is updated from the obsolete expectation:

`device segmented source submit = false`

into a source-derived check that it resolves to the new backend direct-source capability.

The parent's device reduction/digest capability remains false, so aggregate closure remains fail-closed.

---

# 43. Public ABI correction

The backend Local Muon module explicitly exports:

- `MuonDeviceSegmentBackingR1`;
- `BpDkDeviceUpdateEvidenceBackingR1`;
- `LocalMuonDeviceSegmentedHandoffR1`;
- `MuonDeviceSegmentedSourceLeaseR1`;
- `MuonDeviceSegmentedSourceAccessEvidenceR1`.

This also corrects the prior source state where segmented backing types were consumed by base_train but were not listed in the Local Muon module's explicit public re-export list.

---

# 44. Current bake state

Materialized in source:

```text
segmented generation physical backing           true
direct read-only source lease                    true
generation completeness gate                     true
active source reader lifetime                    true
direct source Local Muon API                     true
homogeneous R8 direct source API                 true
source weight H2D in direct API                  absent
source momentum H2D in direct API                absent
real SubmissionEpoch source binding              true
exact completion reader release                  true
source access evidence                           true
B06 successor source provenance                  true
```

Still not materialized/qualified:

```text
BP-DK GPU RMS/cosine reduction                   false
BP-DK exact device SHA256 producer               false
aggregate BP-DK device consumer                  false
production pending queue actual cutover           false
physical G+1 -> G+2 campaign                     not observed
parent P5 ActiveAsync PASS                       not claimed
```

---

# 45. Regression requirements

The following static chain must remain PASS:

- this direct-source child;
- BP-DeltaK segmented successor parent;
- production pending queue core / BP-DeltaK gate R2;
- ActiveDevice pending handoff;
- production pending queue cutover child;
- generic pending submit/later collect;
- P5 SubmissionEpoch dependency ActiveAsync;
- P4 exact Atlas lease generation;
- P3 transactional commit/restart;
- P2 real production shadow;
- P1 immutable qualification bundle;
- P0 evidence truth;
- R6 global job queue;
- R7 mixed-precision expert ABI;
- MCU control-plane.

---

# 46. Compile boundary

A release Rust compile remains mandatory.

This child changes ownership and public ABI around `ArenaLease`, WGPU buffers, SubmissionEpoch and atomically counted source-reader lifetime.

The current assistant environment contains no `cargo`, `rustc` or `rustfmt`; therefore this bake claims source/static validation only.

---

# 47. Physical campaign

Minimum campaign after release compile:

1. build a complete real `MuonDeviceSegmentedGenerationR1(G+1)` from ActiveDevice successor backing;
2. validate its generation publication receipt;
3. issue an exact source lease for a real parameter;
4. submit through the direct-source Local Muon API;
5. prove no host source weight or momentum Vec is materialized;
6. prove source weight H2D = 0;
7. prove source momentum H2D = 0;
8. observe a real SubmissionEpoch;
9. keep the source reader active until exact physical completion;
10. collect the ActiveDevice successor normally;
11. close source reader count back to zero;
12. compare resulting candidate against the qualified source oracle;
13. materialize candidate generation G+2;
14. seal physical receipt only after all gates pass.

---

# 48. Negative fixtures

Qualification should exercise at minimum:

- incomplete generation source rejection;
- wrong canonical parameter source rejection;
- element-count/range mismatch rejection;
- device authority mismatch rejection where safely constructible;
- generation backing release while active reader exists;
- completion epoch mismatch rejection.

None of these fixtures may release or corrupt a current live source generation.

---

# 49. Production queue separation

This child does not wire the direct source API into the production scheduler.

The already materialized `ProductionMuonPendingWaveQueueCoreR2` remains the future queue owner.

`TENSORCUBE_LOCAL_MUON_PRODUCTION_PENDING_QUEUE_CUTOVER_MATERIALIZED_P5_R1` remains false until that real callsite cutover occurs.

---

# 50. BP-DeltaK sibling gate

After this child, the remaining aggregate BP-DeltaK blocker is:

`TENSORCUBE_LOCAL_MUON_BP_DK_DEVICE_POST_UPDATE_REDUCTION_AND_DIGEST_MATERIALIZED_R1 = false`.

The next exact child is therefore:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-BP-DK-DEVICE-POST-UPDATE-REDUCTION-EXACT-DIGEST-AND-COMPACT-EVIDENCE-MATERIALIZATION-R1`.

---

# 51. After BP-DeltaK sibling closure

When the sibling reduction/digest child becomes physically materialized, the aggregate device-resident BP-DeltaK consumer becomes source-truth eligible.

Only then should the production pending queue be wired into the actual streaming scheduler and qualified at bound=2.

---

# 52. Parent P5 remains canonical ActiveAsync authority

This child cannot set:

`active_async_enabled = true`

or:

`per_wave_exact_wait_retired = true`.

Those remain evidence-derived fields of the canonical parent P5 physical campaign.

---

# 53. AdamW and full-model caveat

This child proves only Muon source generation continuity.

It does not prove AdamW Active device candidate staging or full-trainable segmented-generation continuity.

No full-model `DeviceSegmentedGenerationV1` closure may be inferred solely from this child.

---

# 54. P3 caveat

This child does not change durable P3 checkpoint/restart semantics.

A later exact device-generation-to-durable-state materialization bridge is still required before restart authority can depend on device-only current state.

---

# 55. Packaging policy

Implementation source ZIP excludes:

- this specification and all `specs/` content;
- Markdown patch notes;
- `BAKE_MANIFEST*`;
- generated direct-source receipts/evidence;
- generated P0-P5 qualification evidence;
- runtime qualification JSON/JSONL;
- `current.json` and `publication_seal.json`;
- P3 runtime transaction artifacts;
- logs and review outputs;
- Python bytecode caches.

Rust/Python implementation source remains included.

---

# 56. GitHub publication policy

GitHub publication for this revision is spec-only unless implementation publication is separately requested.

---

# 57. Full PASS semantics

Full physical revision PASS means a Muon generation physically produced by the previous ActiveDevice step became the exact source authority of a later real Local Muon submission, source weight and Muon momentum were bound directly from the published GPU generation without host materialization or H2D, the source generation remained immutable and pinned through exact SubmissionEpoch completion, the reader lifetime drained to zero after physical completion, the resulting candidate remained numerically compatible with the qualified Local Muon oracle, and the resulting execution produced the next candidate generation without a source CPU round-trip.

---

# 58. PASS does not mean

This revision does not by itself prove:

- BP-DeltaK GPU reduction/digest closure;
- production bounded pending queue cutover;
- production peak in-flight > 1;
- parent P5 physical ActiveAsync PASS;
- AdamW device successor closure;
- full-model segmented generation closure;
- P3 durable device-generation restart closure;
- R8A multi-view async;
- R8B pressure-aware routing.

---

# 59. Center sentence

**The previous child gave G+1 a real GPU body. This child gives that body a real future: the next Local Muon submit reads G+1 weight and momentum directly through an exact read-only generation lease, produces a real SubmissionEpoch, and holds the old generation until that physical read is complete. No source Vec is rebuilt on CPU and no source weight or momentum is uploaded again. Structural direct submit is now real; the G+1 to G+2 physical campaign still has to earn the PASS.**