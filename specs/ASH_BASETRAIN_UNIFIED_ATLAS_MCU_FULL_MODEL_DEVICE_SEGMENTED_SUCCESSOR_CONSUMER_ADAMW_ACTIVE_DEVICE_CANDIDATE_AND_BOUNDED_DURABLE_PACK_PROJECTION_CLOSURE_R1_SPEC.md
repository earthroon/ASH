# ASH-BASETRAIN-UNIFIED-ATLAS-MCU-FULL-MODEL-DEVICE-SEGMENTED-SUCCESSOR-CONSUMER-ADAMW-ACTIVE-DEVICE-CANDIDATE-AND-BOUNDED-DURABLE-PACK-PROJECTION-CLOSURE-R1

## AdamW ActiveDevice Backend / Direct Device Source Lease / GPU Candidate Weight-M-V / Real SubmissionEpoch / B06 Device Staging Surface / AdamW Segmented Generation / Full-Trainable Generation Owner / Durable Projection ABI / Outer Production Adoption Fail-Closed

---

# 0. Revision identity

Revision:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-FULL-MODEL-DEVICE-SEGMENTED-SUCCESSOR-CONSUMER-ADAMW-ACTIVE-DEVICE-CANDIDATE-AND-BOUNDED-DURABLE-PACK-PROJECTION-CLOSURE-R1`

Reserved full PASS token:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_FULL_MODEL_DEVICE_SEGMENTED_SUCCESSOR_CONSUMER_ADAMW_ACTIVE_DEVICE_CANDIDATE_AND_BOUNDED_DURABLE_PACK_PROJECTION_CLOSURE_R1`

Static source-truth PASS:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_FULL_MODEL_DEVICE_SEGMENTED_SUCCESSOR_R1_STATIC`

Parent:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-LOCAL-MUON-PRODUCTION-PENDING-WAVE-QUEUE-CUTOVER-AND-ACTIVE-ASYNC-PHYSICAL-QUALIFICATION-CLOSURE-R2`

---

# 1. Purpose

The parent R2 materially implements the Local Muon parameter-level ActiveAsync scheduler, but the outer production scheduler still uses host full-model candidate authority.

Source inspection identified two independent full-model gaps:

1. AdamW has a B06 device-ticket ABI, but the production optimizer path still produces full host candidate weight/m/v and calls the host-mirror B06 staging path.
2. The outer scheduler immediately serializes host candidate arrays into the canonical R6 pack/manifest contract, so deleting host candidate scatter without replacing that durable materialization boundary would leave P3/commit inputs empty.

This revision materializes the AdamW ActiveDevice backend and full-device generation ownership surface, while deliberately keeping outer production adoption and durable projection fail-closed until the real production callsites are replaced.

---

# 2. Current exact source truth

After this bake:

```text
AdamW ActiveDevice backend                         true
AdamW direct device source lease                  true
AdamW GPU candidate weight/m/v                    true
AdamW full candidate D2H in Active backend        zero by contract
AdamW ordinary exact wait in Active backend       zero by structure
B06 AdamW device staging runtime surface           true
AdamW production callsite uses device staging      false
AdamW segmented-generation owner                   true
FullTrainableDeviceGenerationR1 owner              true
Durable projection plan ABI                        true
Durable projection canonical callsite              false
Outer full-model device successor consumer         false
Parent production full cutover                     false
Parent P5 physical PASS                            not claimed
```

---

# 3. Backend module

New backend module:

`crates/burn_webgpu_backend/src/adamw_active_device_candidate_r1.rs`

Backend source capability:

`ADAMW_ACTIVE_DEVICE_CANDIDATE_BACKEND_MATERIALIZED_R1 = true`.

---

# 4. Numerical path preservation

The ActiveDevice AdamW backend reuses the existing R6 AdamW shader:

`base_train_r6_adamw_candidate.wgsl`.

This revision changes memory provenance, candidate ownership and completion behavior. It does not invent a second AdamW formula.

---

# 5. AdamW device source owner

`AdamWDeviceSourceSegmentR1` owns exact GPU source backing for:

- weight;
- Adam first moment m;
- Adam second moment v.

It binds:

- source generation;
- canonical parameter index;
- logical element range;
- physical allocation IDs;
- source digest;
- real WGPU buffers;
- active reader count.

---

# 6. Explicit seed boundary

`AdamWDeviceSourceSegmentR1::seed_from_host(...)` is an explicit bootstrap authority.

Host-to-device traffic during initial seed does not count as next-generation direct-source proof.

The seed is not silently described as a produced-generation reuse.

---

# 7. Direct source lease

`AdamWDeviceSourceLeaseR1` is read-only source authority.

It binds the exact source generation and physical weight/m/v backing before submit.

The source lease has no host candidate vector.

---

# 8. Reader lifetime

Issuing an AdamW source lease increments the source segment reader count.

After real Queue submission the lease binds to the exact `SubmissionEpoch`.

Reader release occurs only after exact physical completion of that submission.

---

# 9. Pre-submit failure

A source lease dropped before real submission may cancel its reader reservation.

---

# 10. Post-submit failure

A source lease dropped after a real SubmissionEpoch has been attached does not silently declare completion.

It remains conservatively pinned and emits a diagnostic.

---

# 11. AdamW ActiveDevice producer

`AdamWActiveDeviceCandidateProducerR1` creates the existing AdamW compute pipeline and binds:

- gradient device lease or zero-gradient dummy;
- device source weight;
- device source m;
- device source v;
- GPU candidate weight output;
- GPU candidate m output;
- GPU candidate v output;
- compact status.

---

# 12. Candidate physical allocations

Candidate weight/m/v each receive distinct A01 physical allocation identities.

The candidate buffers remain live after physical completion under `AdamWActiveDeviceCandidateSegmentR1`.

---

# 13. No full candidate readback

The Active backend does not allocate or map full candidate readback buffers for weight/m/v.

Required evidence:

```text
candidate_weight_d2h_bytes = 0
candidate_m_d2h_bytes = 0
candidate_v_d2h_bytes = 0
host_candidate_vec_materialization_count = 0
```

---

# 14. Compact status only

The Active backend reads four status bytes.

`compact_status_d2h_bytes = 4` in the current R1 implementation.

---

# 15. No ordinary exact wait

The Active backend uses:

- `a01_submit_with_leases`;
- nonblocking A01 poll/refresh;
- `submission_completed_nonblocking`;
- asynchronous map callback.

The module contains no `wait_for_submission_exact` call.

---

# 16. Pending owner

`PendingAdamWActiveDeviceCandidateR1` owns:

- real tracked submission;
- exact source reader lease;
- GPU candidate weight/m/v buffers;
- physical candidate allocation IDs;
- compact status readback;
- asynchronous map state.

---

# 17. Completion

`try_collect(...)` returns `None` until both:

- the real SubmissionEpoch is complete;
- compact status mapping is ready.

---

# 18. Candidate segment

Successful collection yields:

`AdamWActiveDeviceCandidateSegmentR1`.

It preserves:

- source generation;
- target generation;
- parameter identity;
- element range;
- real SubmissionEpoch;
- physical weight/m/v allocations;
- GPU candidate buffers;
- zero-D2H transfer evidence.

---

# 19. B06 backing

`AdamWActiveDeviceCandidateSegmentR1::backing()` produces the existing B06 metadata type:

`AdamWDeviceCandidateBacking`.

The metadata backing refers to actual retained physical candidate buffers. It is not itself the buffer owner.

---

# 20. Next-generation AdamW source

`AdamWActiveDeviceCandidateSegmentR1::issue_next_source_lease(...)` permits the produced target-generation GPU candidate to become the source of a later AdamW execution without source weight/m/v host reconstruction.

Physical G+1→G+2 reuse is not claimed by this source bake.

---

# 21. Base-train full-model module

New module:

`crates/base_train/src/unified_atlas_mcu_full_model_device_segmented_successor_r1.rs`.

---

# 22. Capability decomposition

The module exposes separate source-truth capabilities rather than one blanket flag.

```text
ADAMW_ACTIVE_DEVICE_CANDIDATE_BACKEND_SOURCE_MATERIALIZED_R1 = true
ADAMW_ACTIVE_DEVICE_CANDIDATE_PRODUCTION_STAGING_MATERIALIZED_R1 = false
ADAMW_DEVICE_SEGMENTED_GENERATION_MATERIALIZED_R1 = true
FULL_TRAINABLE_DEVICE_GENERATION_MATERIALIZED_R1 = true
DEVICE_TO_DURABLE_PACK_PROJECTION_MATERIALIZED_R1 = false
```

---

# 23. Outer consumer capability

`OUTER_FULL_MODEL_DEVICE_SEGMENTED_SUCCESSOR_CONSUMER_MATERIALIZED_R1`

is the conjunction of the production staging, AdamW generation, full-trainable generation and durable projection capabilities.

Its current value is false.

---

# 24. Parent cutover source truth

The parent R2 constant:

`TENSORCUBE_LOCAL_MUON_OUTER_FULL_MODEL_DEVICE_SEGMENTED_SUCCESSOR_CONSUMER_MATERIALIZED_R2`

now derives from the new full-model module instead of a literal `false`.

The parent full cutover remains fail-closed because the derived outer capability is false.

---

# 25. AdamW segmented generation

`AdamWDeviceSegmentedGenerationR1` owns produced AdamW candidate segments for one exact source→target generation transition.

It tracks:

- expected parameter count;
- expected element count;
- published segments;
- published elements;
- active source readers.

---

# 26. Current R1 AdamW publication geometry

The current generation owner accepts whole-parameter AdamW segments only.

`element_start` must be zero.

Multi-fragment AdamW parameter assembly is not yet materialized in this bake.

---

# 27. Exact new blocker: multi-segment B06 AdamW backing

The existing B06 `AdamWDeviceCandidateBacking` represents one physical allocation triplet:

- one weight allocation;
- one m allocation;
- one v allocation;
- SubmissionEpoch set.

It cannot truthfully represent a multi-parameter AdamW generation with multiple physical allocation triplets.

`AdamWDeviceSegmentedGenerationR1::aggregate_backing()` therefore rejects multi-segment collapse with:

`E_MCU_FULL_MODEL_R1_ADAMW_MULTI_SEGMENT_B06_BACKING_LEDGER_REQUIRED`.

No fabricated aggregate allocation is created.

---

# 28. B06 runtime staging surface

`ProductionMuonRuntime` now exposes:

`stage_b06_adamw_device_candidate_r1(...)`.

It requires B06 `ActiveVerified` and delegates to the existing:

`HybridOptimizerCommitCoordinator::stage_adamw_device_candidate(...)`.

---

# 29. Production staging remains false

The inspected outer production scheduler still contains no call to:

`stage_b06_adamw_device_candidate_r1(...)`.

It still calls:

`stage_b06_adamw_host_candidate(...)`.

Therefore:

`ADAMW_ACTIVE_DEVICE_CANDIDATE_PRODUCTION_STAGING_MATERIALIZED_R1 = false`.

---

# 30. Full-trainable generation owner

`FullTrainableDeviceGenerationR1` can own:

- one concrete Muon device generation;
- one concrete AdamW device generation;
- canonical `FullTrainableCoverageReceipt`;
- one exact full-generation digest.

---

# 31. Full coverage requirements

Construction requires:

```text
coverage.complete = true
overlap_elements = 0
unclassified_elements = 0
duplicate_write_elements = 0
missing_elements = 0
```

Muon and AdamW target generations must equal the same full-model generation.

---

# 32. No generation split

A full-trainable generation cannot claim:

```text
Muon target = G+1
AdamW target = G
```

under one canonical full-generation identity.

---

# 33. Durable projection plan ABI

`FullTrainableDeviceDurableProjectionPlanR1` binds:

- generation;
- bounded transfer-window bytes;
- expected weight bytes;
- expected Adam m bytes;
- expected Adam v bytes;
- canonical layout digest;
- plan digest.

---

# 34. Durable projection is still not materialized

The current outer pack writer still consumes host candidate state.

There is no real production callsite yet that streams device Muon/AdamW backing into:

- `weights.r6pack`;
- `adam_m.r6pack`;
- `adam_v.r6pack`;
- `PackedRuntimeStateManifestV1`.

Therefore:

`DEVICE_TO_DURABLE_PACK_PROJECTION_MATERIALIZED_R1 = false`.

---

# 35. Existing durable SSOT remains valid

This revision does not replace:

- `ParameterStage`;
- `PackedRuntimeStateManifestV1`;
- current pack SHA-256 fields;
- current P3 transaction authority.

The next durable-projection child must reproduce them exactly from device-generation state.

---

# 36. Runtime vs durable authority

Target design remains:

```text
FullTrainableDeviceGenerationR1
= live execution authority

R6 packs + PackedRuntimeStateManifestV1
= bounded durable projection
```

The durable projection must never be read back and re-uploaded merely to continue the same Active generation.

---

# 37. Bounded projection requirement

The future projector must use an existing bounded transfer window and may not allocate full-model host weight/m/v vectors.

---

# 38. Durable D2H classification

Any D2H required solely to produce canonical disk/RAM packs must be separately recorded as durable-projection traffic.

It must not be hidden inside zero candidate-D2H telemetry.

---

# 39. Candidate D2H remains zero

Active runtime candidate authority requires:

```text
Muon full candidate D2H = 0
AdamW candidate weight D2H = 0
AdamW candidate m D2H = 0
AdamW candidate v D2H = 0
```

---

# 40. No Active→Mirror fallback

A missing outer device consumer may not be solved by downloading the full model and continuing through host candidate scatter.

The parent outer gate remains fail-closed.

---

# 41. Pre-existing B06 ledger correction

This bake also fixes a duplicated nested loop line in the prior B06 Muon successor-ledger digest implementation.

The fix restores one exact iteration over `pending_muon_device_successors` and does not change the ledger semantics.

---

# 42. Static validator

New validator:

`tools/validate_ash_basetrain_unified_atlas_mcu_full_model_device_segmented_successor_adamw_active_candidate_r1_static.py`.

It verifies at minimum:

- AdamW Active backend module export;
- backend capability true;
- real pending AdamW candidate type;
- real SubmissionEpoch;
- nonblocking completion;
- no exact wait symbol in Active backend;
- direct device source binding;
- zero weight/m/v candidate D2H evidence;
- AdamW segmented generation type;
- full-trainable generation type;
- durable projection plan ABI;
- B06 device staging runtime method;
- AdamW production staging false;
- durable projection false;
- outer consumer derived rather than hardcoded;
- legacy outer host candidate path still present;
- no production device-stage call yet.

---

# 43. Parent validator maintenance

Earlier validators that expected the literal source text:

`...OUTER_FULL_MODEL...: bool = false`

are updated to validate the new derived source-truth expression.

They still require the actual child blockers to remain false.

This is validator alignment, not gate weakening.

---

# 44. Static regression state

The following static chain passes in this bake:

- full-model/AdamW child;
- Local Muon R2 parameter ActiveAsync scheduler;
- BP-DeltaK device reduction/exact digest;
- Device Segmented Source Direct Submit;
- BP-DeltaK segmented successor;
- pending queue core/BP-DeltaK gate;
- ActiveDevice pending handoff;
- prior production cutover validator;
- generic pending submit/later collect;
- P5 SubmissionEpoch ActiveAsync;
- P4 exact Atlas lease;
- P3 Active Transactional Commit/Restart;
- P2 production Wave shadow;
- P1 immutable qualification bundle;
- P0 physical evidence truth;
- R6 global queue;
- R7 mixed-precision ABI;
- MCU control plane.

---

# 45. Compile boundary

A real Rust release compile is mandatory before physical qualification.

This child adds public WGPU ownership types and modifies cross-crate ABI.

The bake environment does not contain `cargo`, `rustc` or `rustfmt`, so compile PASS is not claimed.

---

# 46. Source QA

Modified Rust source passes the bake's lightweight delimiter scan.

Modified Python validators pass `py_compile`.

These checks do not replace the Rust compiler.

---

# 47. Full physical PASS is withheld

This source bake does not claim:

- AdamW GPU execution on target hardware;
- AdamW candidate numerical parity;
- AdamW G+1→G+2 direct-source reuse;
- multi-parameter AdamW device generation B06 staging;
- bounded device-to-pack projection;
- exact projected pack digest parity;
- outer full-model device consumer activation;
- Local Muon bound=2 production overlap;
- parent P5 PASS.

---

# 48. Exact next blocker A

Materialize an AdamW multi-segment physical backing ledger compatible with B06.

The next B06 AdamW authority must represent all exact parameter/fragment physical allocation triplets and SubmissionEpochs instead of forcing them into one triplet.

Recommended scope:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-ADAMW-MULTI-SEGMENT-DEVICE-GENERATION-B06-BACKING-LEDGER-AND-PRODUCTION-STAGING-CLOSURE-R1`.

---

# 49. Exact next blocker B

Materialize the actual bounded device-to-durable projection callsite that replaces outer full-model host candidate scatter while preserving the existing canonical pack/manifest contract.

Recommended scope:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-FULL-TRAINABLE-DEVICE-GENERATION-BOUNDED-DURABLE-PACK-PROJECTION-AND-OUTER-HOST-SCATTER-RETIREMENT-CLOSURE-R1`.

---

# 50. Activation order

Recommended sequence:

```text
AdamW multi-segment backing ledger
→ real production stage_adamw_device_candidate callsite
→ full-trainable generation exact coverage
→ bounded durable projection
→ outer Active branch skips host scatter
→ outer consumer capability true
→ parent full production cutover true
→ bound=2 physical A/B campaign
→ parent P5 PASS
```

---

# 51. Full PASS semantics reserved for this revision family

Full closure will mean AdamW remains GPU-resident through candidate creation, Muon and AdamW form one exact full-trainable device generation, the outer scheduler uses that generation instead of a full host candidate, and canonical durable packs are produced only through bounded projection from device state.

The current bake intentionally stops before claiming those outer callsites are complete.

---

# 52. Packaging policy

Implementation ZIP excludes:

- this specification and all Markdown;
- `specs/`;
- patch notes;
- generated receipts/evidence/manifests;
- runtime pack outputs;
- `active_training_state.json`;
- `current.json`;
- `publication_seal.json`;
- logs and review outputs;
- Python bytecode caches.

Rust/WGSL/Python implementation source remains included.

---

# 53. GitHub publication policy

GitHub publication for this revision is specification-only unless implementation publication is separately requested.

---

# 54. Center sentence

> **AdamW에도 이제 진짜 GPU candidate 몸체가 생겼습니다. source weight/m/v를 device lease로 읽고, candidate weight/m/v를 GPU에 남긴 채 real SubmissionEpoch로 끝내며, B06 device ticket으로 넘길 수 있는 길도 열렸습니다. 다만 full-model production은 아직 그 길을 타지 않습니다. AdamW 여러 parameter의 물리 backing을 하나의 B06 권위로 모으는 ledger와, device generation을 기존 R6 pack/manifest로 bounded projection하는 outer callsite가 아직 없습니다. 그래서 이번 bake는 AdamW backend를 true로 만들되 outer consumer는 false로 남깁니다. 이 두 마지막 host 권위를 걷어낸 뒤에야 안쪽에서 이미 만들어둔 A/B ActiveAsync scheduler를 실제 full production에서 열 수 있습니다.**