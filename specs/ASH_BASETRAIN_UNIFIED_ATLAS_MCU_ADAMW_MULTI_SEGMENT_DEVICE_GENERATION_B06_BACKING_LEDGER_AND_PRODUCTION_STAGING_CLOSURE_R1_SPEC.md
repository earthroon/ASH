# ASH-BASETRAIN-UNIFIED-ATLAS-MCU-ADAMW-MULTI-SEGMENT-DEVICE-GENERATION-B06-BACKING-LEDGER-AND-PRODUCTION-STAGING-CLOSURE-R1

## Multi-Parameter AdamW GPU Candidate Ledger / Exact Physical Backing Set / SubmissionEpoch Union / B06 Device-Generation Ticket / Real Stage Surface / Production Pending-Scheduler Blocker Truth

## 0. Revision identity

Revision:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-ADAMW-MULTI-SEGMENT-DEVICE-GENERATION-B06-BACKING-LEDGER-AND-PRODUCTION-STAGING-CLOSURE-R1`

Parent:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-FULL-MODEL-DEVICE-SEGMENTED-SUCCESSOR-CONSUMER-ADAMW-ACTIVE-DEVICE-CANDIDATE-AND-BOUNDED-DURABLE-PACK-PROJECTION-CLOSURE-R1`

Reserved full physical PASS:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_ADAMW_MULTI_SEGMENT_DEVICE_GENERATION_B06_BACKING_LEDGER_AND_PRODUCTION_STAGING_CLOSURE_R1`

Static source-truth PASS:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_ADAMW_MULTI_SEGMENT_B06_LEDGER_PRODUCTION_STAGING_R1_STATIC`

## 1. Purpose

The parent materially provides an AdamW ActiveDevice backend, direct device source leases, GPU-resident candidate weight/m/v, a real SubmissionEpoch, `AdamWDeviceSegmentedGenerationR1`, `FullTrainableDeviceGenerationR1`, and a single-ticket B06 device-stage surface.

The remaining B06 metadata mismatch was exact: one `AdamWDeviceCandidateBacking` represents one physical weight/m/v allocation triplet, but a real AdamW target generation contains multiple parameter segments and therefore multiple physical triplets and multiple real SubmissionEpochs.

This revision removes that false single-backing collapse and gives B06 a canonical multi-segment generation ticket.

Source inspection also confirms that the outer optimizer still does not own a real asynchronous AdamW pending-generation scheduler. Therefore this bake does not falsely mark production staging complete.

## 2. Current exact source truth

After this bake:

```text
AdamW ActiveDevice backend                         true
AdamW segmented generation                        true
AdamW multi-segment B06 backing ledger            true
B06 AdamW generation-stage coordinator API         true
ProductionMuonRuntime generation-stage wrapper     true
Outer production Active AdamW pending scheduler    false
Real production generation-stage callsite          false
Durable device-to-pack projection                  false
Outer full-model device successor consumer         false
Parent full production cutover                     false
Parent P5 physical PASS                            not claimed
```

## 3. Leaf backing remains physical-segment metadata

Existing:

`AdamWDeviceCandidateBacking`

continues to describe one physical segment only:

- weight allocation;
- m allocation;
- v allocation;
- exact SubmissionEpoch set.

It is not widened into a fabricated aggregate allocation.

## 4. Canonical segment key

New:

`AdamWDeviceCandidateSegmentKeyR1`

binds:

- canonical parameter index;
- element start;
- element count.

The key derives total ordering and is used as the canonical generation-ledger key.

## 5. Segment ticket

New:

`AdamWDeviceCandidateSegmentTicketR1`

binds:

- segment key;
- source generation;
- target generation;
- exact physical backing triplet;
- compact-status D2H bytes;
- segment digest.

A segment ticket requires target = source + 1, nonzero cardinality, nonempty exact SubmissionEpoch evidence, and a nonempty segment digest.

## 6. Generation ledger

New:

`AdamWDeviceCandidateGenerationLedgerR1`

contains:

- exact source/target `TrainableGenerationId`;
- expected parameter count;
- expected element count;
- `BTreeMap<AdamWDeviceCandidateSegmentKeyR1, AdamWDeviceCandidateSegmentTicketR1>`;
- canonical exact SubmissionEpoch union;
- coverage digest;
- ledger digest.

## 7. Deterministic ordering

Canonical ordering is the BTreeMap order of:

```text
canonical_parameter_index
→ element_start
→ element_count
```

It never derives from GPU completion order, insertion order, callback order, or SubmissionEpoch ordinal.

## 8. Coverage and overlap checks

Ledger validation requires:

- nonzero expected coverage;
- all segment generations identical;
- no overlapping ranges under one canonical parameter;
- exact expected parameter count;
- exact expected element count;
- no duplicate SubmissionEpoch in the current R1 one-submit-per-segment geometry;
- recomputed epoch union equal to the sealed exact union.

Failure identifiers include:

- `E_MCU_ADAMW_B06_R1_SEGMENT_OVERLAP`;
- `E_MCU_ADAMW_B06_R1_GENERATION_MISMATCH`;
- `E_MCU_ADAMW_B06_R1_ELEMENT_COVERAGE_MISMATCH`;
- `E_MCU_ADAMW_B06_R1_DUPLICATE_SUBMISSION_EPOCH`;
- `E_MCU_ADAMW_B06_R1_SUBMISSION_EPOCH_UNION_DRIFT`.

## 9. Generation ticket

New:

`AdamWDeviceCandidateGenerationTicketR1`

binds:

- source/target generation;
- ownership digest;
- canonical layout digest;
- row-map digest;
- expected/written AdamW elements;
- zero full candidate D2H counters;
- compact status bytes;
- exact generation ledger;
- full-trainable coverage digest;
- device-sealed bit;
- ticket digest.

## 10. No host candidate authority in device ticket

Generation-ticket validation requires:

```text
candidate_weight_d2h_bytes = 0
candidate_m_d2h_bytes = 0
candidate_v_d2h_bytes = 0
host_candidate_vec_materialization_count = 0
compact_status_passed = true
```

## 11. B06 storage widening

`HybridOptimizerCommitCoordinator` now owns a separate:

`pending_adamw_device_generation: Option<AdamWDeviceCandidateGenerationTicketR1>`.

This is distinct from legacy/single-segment:

`pending_adamw: Option<AdamWDeviceCandidateTicket>`.

The two authorities may not be staged simultaneously.

## 12. B06 generation-stage API

New coordinator API:

`stage_adamw_device_candidate_generation_r1(...)`.

It requires:

- `ActiveVerified` mode;
- admitted next-step device consumer;
- no existing host/single AdamW ticket;
- no duplicate device-generation ticket;
- exact current source generation;
- exact successor target generation;
- exact ownership digest;
- exact canonical layout digest;
- full AdamW expected/written coverage;
- valid multi-segment ledger.

After validation it seals the device-generation ticket.

## 13. Active B06 prepare path

`prepare_full_commit()` now uses the multi-segment device-generation ticket when one is staged in `ActiveVerified` mode.

The prior single-segment device ticket remains a compatibility fallback for existing source/tests until the real production pending scheduler is adopted.

Mirror mode continues to use the host candidate ticket.

## 14. B06 cleanup

Commit, abort and clear paths now clear both:

- legacy/single AdamW pending ticket;
- multi-segment AdamW device-generation ticket.

No stale generation ticket survives commit or abort.

## 15. Base-train generation builder

`AdamWDeviceSegmentedGenerationR1::build_generation_ticket_r1(...)` converts the physically owned segmented generation into the canonical B06 generation ticket.

For every real segment it binds:

- canonical segment key;
- physical weight/m/v allocation IDs;
- real SubmissionEpoch;
- compact status evidence;
- segment digest.

It then constructs:

- exact epoch union;
- coverage digest;
- ledger digest;
- generation ticket digest.

## 16. No aggregate-backing fabrication

The prior `aggregate_backing()` single-triplet compatibility method remains fail-closed for multi-segment generations with:

`E_MCU_FULL_MODEL_R1_ADAMW_MULTI_SEGMENT_B06_BACKING_LEDGER_REQUIRED`.

The new generation-ticket builder is the correct multi-segment path.

## 17. Production runtime stage surface

`ProductionMuonRuntime` now exposes:

`stage_b06_adamw_device_candidate_generation_r1(...)`.

It requires ActiveVerified and delegates to the B06 generation-stage API.

## 18. Structural child capabilities

New child module:

`unified_atlas_mcu_adamw_multi_segment_b06_ledger_r1.rs`.

Source capabilities:

```text
ADAMW_MULTI_SEGMENT_B06_BACKING_LEDGER_MATERIALIZED_R1 = true
ADAMW_B06_DEVICE_GENERATION_STAGE_SURFACE_MATERIALIZED_R1 = true
ADAMW_ACTIVE_DEVICE_GENERATION_PRODUCTION_CALLSITE_MATERIALIZED_R1 = false
```

The aggregate child production-staging closure is the conjunction of the real prerequisites and remains false.

## 19. Exact production blocker discovered

The canonical outer optimizer functions:

- `optimizer_candidate_packed`;
- `optimizer_candidate_ram_resident`

still perform AdamW as an immediate synchronous host-output operation.

They currently do not retain a collection of `PendingAdamWActiveDeviceCandidateR1` objects across parameter segments and later finalize them into `AdamWDeviceSegmentedGenerationR1`.

Therefore a real production generation ticket does not yet exist at the outer callsite.

## 20. No fake host→GPU ticket bridge

This bake does not solve the missing production scheduler by:

```text
host AdamW candidate Vec
→ upload back to GPU
→ fabricate device generation ticket
```

That would preserve the host candidate as execution SSOT and violate the ActiveDevice contract.

## 21. Production staging remains fail-closed

The outer scheduler still contains:

`stage_b06_adamw_host_candidate(...)`

and contains no real call to:

`stage_b06_adamw_device_candidate_generation_r1(...)`.

Therefore the source-truth production-callsite capability remains false.

## 22. Durable projection remains separate

The existing full-model module still has:

`DEVICE_TO_DURABLE_PACK_PROJECTION_MATERIALIZED_R1 = false`.

This child does not attempt to retire the outer host candidate pack writer.

## 23. Outer/full cutover remains false

Because real production AdamW ActiveDevice staging and durable projection remain open:

```text
outer full-model device successor consumer = false
parent production pending queue cutover = false
```

No parent P5 activation is claimed.

## 24. Structural receipt

`AdamWMultiSegmentB06LedgerStructuralReceiptR1` reports each materialized sub-capability independently.

Current verdict:

`MULTI_SEGMENT_LEDGER_MATERIALIZED_ADAMW_PENDING_SCHEDULER_REQUIRED`.

No full PASS token is emitted.

## 25. Static validator

New validator:

`tools/validate_ash_basetrain_unified_atlas_mcu_adamw_multi_segment_device_generation_b06_backing_ledger_production_staging_r1_static.py`.

It verifies:

- exact child revision;
- segment key/ticket types;
- multi-segment BTreeMap ledger;
- overlap and duplicate-epoch rejection;
- exact SubmissionEpoch union;
- B06 device-generation ticket;
- B06 generation-stage API;
- pending generation owner;
- Active prepare support;
- base-train generation-ticket builder;
- runtime generation-stage wrapper;
- ledger/stage-surface capabilities true;
- production-callsite capability false;
- outer host stage still present;
- no outer generation-stage call yet;
- durable projection still false.

## 26. Regression state

Static PASS remains observed for:

- this child;
- full-model/AdamW parent;
- Local Muon R2 cutover child;
- BP-DeltaK device reduction/exact digest;
- Device Segmented Source Direct Submit;
- BP-DeltaK segmented successor;
- pending queue core;
- ActiveDevice pending handoff;
- prior cutover child;
- generic pending submit/later collect;
- P5;
- P4;
- P3;
- P2;
- P1;
- P0;
- R6;
- R7;
- MCU control plane.

## 27. Compile boundary

A real release compile is mandatory because this child changes B06 type/borrow state and cross-crate public ABI.

The assistant bake environment has no `cargo`, `rustc` or `rustfmt`; therefore release compile is not claimed.

## 28. Full physical PASS remains withheld

This source bake does not claim:

- real multi-segment AdamW GPU campaign;
- production Active AdamW pending scheduler;
- actual production generation-stage call;
- AdamW numerical parity;
- AdamW produced-generation G+1→G+2 reuse;
- durable pack projection;
- outer full-model consumer activation;
- parent P5 PASS.

## 29. Exact next child A

The next missing physical execution authority is:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-ADAMW-ACTIVE-DEVICE-PENDING-GENERATION-PRODUCTION-SCHEDULER-AND-MULTI-SEGMENT-COLLECT-CLOSURE-R1`.

It must replace the synchronous host-output AdamW segment loop with real pending ActiveDevice segment ownership and seal the generation ledger through the actual production path.

Only then may:

`ADAMW_ACTIVE_DEVICE_GENERATION_PRODUCTION_CALLSITE_MATERIALIZED_R1 = true`.

## 30. Exact next child B

After real AdamW production staging, the remaining outer boundary is:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-FULL-TRAINABLE-DEVICE-GENERATION-BOUNDED-DURABLE-PACK-PROJECTION-AND-OUTER-HOST-SCATTER-RETIREMENT-CLOSURE-R1`.

That child must stream the committed device candidate into the existing canonical R6 pack/manifest contract without constructing a full host candidate.

## 31. Packaging policy

Source ZIP excludes:

- this specification and all Markdown;
- `specs/`;
- patch notes;
- generated ledgers/receipts/evidence;
- runtime packs/manifests;
- `active_training_state.json`;
- logs/review outputs;
- Python bytecode caches.

Rust/WGSL/Python implementation source remains included.

## 32. GitHub publication policy

GitHub publication is specification-only unless implementation publication is explicitly requested.

## 33. Center sentence

**B06는 이제 AdamW 여러 parameter를 하나의 가짜 allocation으로 접지 않는다. 각 GPU segment의 weight/m/v physical allocation과 real SubmissionEpoch를 그대로 ledger에 넣고, 그 canonical 집합 전체를 하나의 target generation ticket으로 받는다. 다만 production optimizer는 아직 그 GPU segment들을 pending으로 만들고 모으는 scheduler가 없다. 그래서 ledger는 true, B06 generation-stage surface도 true지만, real production callsite는 false다. host candidate를 다시 GPU에 올려서 이 빈칸을 속이지 않는다. 다음 child는 바로 실제 AdamW pending-generation scheduler를 만들어 이 ledger를 production에서 채우는 단계다.**