# ASH-BASETRAIN-UNIFIED-ATLAS-MCU-LOCAL-MUON-PRODUCTION-PENDING-WAVE-QUEUE-CUTOVER-AND-ACTIVE-ASYNC-PHYSICAL-QUALIFICATION-CLOSURE-R2

## Local-Muon Parameter-Level ActiveAsync Scheduler Materialization / Bound-2 Queue Ownership / Multi-Wave B06 Successor Ledger / Parameter-Sized D2D Assembly / Exact Subrange Device Source / Device BP-DeltaK Evidence / Outer Full-Model Host-Scatter Boundary Truth / Full Production Cutover Fail-Closed

---

# 0. Revision identity

Revision:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-LOCAL-MUON-PRODUCTION-PENDING-WAVE-QUEUE-CUTOVER-AND-ACTIVE-ASYNC-PHYSICAL-QUALIFICATION-CLOSURE-R2`

Parent:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-BP-DK-DEVICE-POST-UPDATE-REDUCTION-EXACT-DIGEST-AND-COMPACT-EVIDENCE-MATERIALIZATION-R1`

Reserved full physical PASS token:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_LOCAL_MUON_PRODUCTION_PENDING_WAVE_QUEUE_CUTOVER_AND_ACTIVE_ASYNC_PHYSICAL_QUALIFICATION_CLOSURE_R2`

Static source-truth PASS:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_LOCAL_MUON_PRODUCTION_PENDING_WAVE_QUEUE_CUTOVER_R2_STATIC`

---

# 1. Purpose

The source entering R2 already materializes the physical building blocks required for Local Muon device-only asynchronous execution:

- R6 exact multi-epoch queue authority;
- P4 exact Atlas slot/lease generation;
- P5 real SubmissionEpoch dependency tracking;
- Local Muon submit-before-wait pending execution;
- ActiveDeviceCandidate GPU-resident successor handoff;
- bounded runtime-owned production pending queue core;
- concrete Muon segmented-generation backing;
- direct next-generation device-source submission;
- BP-DeltaK device reduction, exact replay-f32 SHA-256 and compact evidence.

R2 attempts the first real Production Muon scheduler cutover.

Source inspection during that cutover revealed that Local Muon parameter-level asynchronous execution and full-model production adoption are two different boundaries. R2 therefore materializes the parameter-level ActiveAsync scheduler and seals the remaining outer full-model blocker instead of falsely marking the entire production scheduler as cut over.

---

# 2. Source-derived correction: full production cutover is not yet true

The outer scheduler:

`crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs`

still reconstructs a host full-model candidate.

For Muon-owned elements it chooses among:

- `candidate_weight_streamed_to_successor` and `ResidentWeightPackBuilder::read_f32_at(...)`;
- `candidate_weight_in_place` host packed state;
- `candidate_weight_packed` host candidate vectors.

It then merges AdamW residual updates into the same host candidate and serializes weight/optimizer packs.

An ActiveDevice Local Muon result intentionally contains no full host candidate vector.

Therefore either of the following would be incorrect:

1. download the device candidate to satisfy the outer host scatter, violating the zero-full-D2H ActiveDevice contract;
2. pass stale host state as if it were the new Muon candidate.

R2 rejects both.

---

# 3. Current source-truth capability decomposition

R2 defines:

`TENSORCUBE_LOCAL_MUON_PRODUCTION_PARAMETER_ACTIVE_ASYNC_SCHEDULER_MATERIALIZED_R2 = true`

and:

`TENSORCUBE_LOCAL_MUON_OUTER_FULL_MODEL_DEVICE_SEGMENTED_SUCCESSOR_CONSUMER_MATERIALIZED_R2 = false`.

The existing full cutover capability is now derived as:

```text
TENSORCUBE_LOCAL_MUON_PRODUCTION_PENDING_QUEUE_CUTOVER_MATERIALIZED_P5_R1
=
parameter ActiveAsync scheduler
AND
outer full-model device-segmented successor consumer
```

Therefore its current value is false.

This is deliberate source truth, not a missing constant flip.

---

# 4. Exact active-path outer blocker

Before entering the Local Muon ActiveAsync parameter scheduler, the real production callsite requires:

`TENSORCUBE_LOCAL_MUON_OUTER_FULL_MODEL_DEVICE_SEGMENTED_SUCCESSOR_CONSUMER_MATERIALIZED_R2`.

Current fail-closed error:

`E_MCU_P5_FULL_MODEL_DEVICE_SEGMENTED_SUCCESSOR_CONSUMER_REQUIRED_R2`.

The failure occurs before Local Muon GPU submission, preventing an ActiveDevice transaction from falling through into the outer host-candidate authority.

---

# 5. Structural achievement of this R2

Although full production cutover remains false, R2 materially implements the Local Muon parameter-level scheduler that the outer consumer will eventually call.

Implementation:

`execute_fusion_execution_plan_candidate_active_async_r2(...)`.

It is not a qualification-only executor.

It is placed in the Production Muon callsite runtime and uses the existing production authorities.

---

# 6. Initial ActiveAsync bound

The scheduler requires:

`max_in_flight_waves >= 2`.

The intended first physical campaign remains bound=2.

R2 does not require bound=3 to prove actual asynchronous overlap.

---

# 7. Local-domain scope

The currently materialized pending ActiveDevice backend is a Local Muon physical-batch backend.

Therefore R2 parameter ActiveAsync admits only plans whose domains are all:

`AshBpDkMuonExecutionDomainKind::Local`.

Fused domains fail before submit with:

`E_MCU_P5_ACTIVE_ASYNC_FUSED_DOMAIN_NOT_MATERIALIZED_R2`.

No synchronous fused-pair host result is mixed into one ActiveAsync parameter transaction.

---

# 8. R8/R8A scope

R8A heterogeneous multi-view ActiveAsync remains unmaterialized and is rejected with:

`E_MCU_P5_ACTIVE_ASYNC_R8A_MULTI_VIEW_NOT_MATERIALIZED_R2`.

The current deterministic R8 router is also rejected by this parameter scheduler with:

`E_MCU_PRODUCTION_CUTOVER_R2_R8_ROUTER_ASYNC_NOT_MATERIALIZED`.

This R2 therefore does not overclaim R8/R8A asynchronous routing.

---

# 9. P2/replay/counterfactual scope

The current P2 production shadow lifetime is not qualified for this multi-Wave asynchronous scheduler.

R2 therefore requires P2 shadow disabled for the ActiveAsync path:

`E_MCU_PRODUCTION_CUTOVER_R2_P2_ASYNC_SHADOW_NOT_QUALIFIED`.

Active fusion replay and BP-DeltaK counterfactual execution are likewise required off for this R2 path:

- `E_MCU_PRODUCTION_CUTOVER_R2_ACTIVE_REPLAY_NOT_QUALIFIED`;
- `E_MCU_PRODUCTION_CUTOVER_R2_COUNTERFACTUAL_NOT_QUALIFIED`.

These prior correctness authorities are not deleted; their async lifetime integration remains separate work.

---

# 10. Production queue SSOT

R2 uses the existing:

`ProductionMuonPendingWaveQueueCoreR2`.

No second async queue authority is introduced.

The queue continues to bind distinct identities rather than collapsing them:

- backend pending-Wave identity;
- P5 semantic-Wave identity;
- real SubmissionEpoch;
- P4 exact lease digest;
- R6 queue generation/epoch identity.

---

# 11. Queue admission loop

The Local Muon parameter scheduler follows the real bounded shape:

```text
while work remains OR queue nonempty:

    while work remains AND queue.can_submit():
        prepare exact Wave
        acquire P4
        seal R6 epoch
        issue device-source range lease
        submit pending Local Muon Wave
        receive real SubmissionEpoch
        bind P4 submissions
        register P5 consumers
        enqueue real pending owner

    nonblocking progress/collect
    nonblocking D2D fragment-copy progress
```

There is no ordinary per-Wave exact blocking wait in this helper.

---

# 12. Real A/B overlap capability at parameter level

The deterministic R2 Wave partition intentionally creates more than one Local Wave when the parameter has enough canonical tiles and the configured bound is at least 2.

The first intended physical witness is still:

```text
submit A
A pending
submit B before A collect
A+B represented concurrently
```

The source structure is now capable of this inside the Local Muon parameter scheduler.

The assistant environment did not execute the GPU campaign, so the witness is not claimed as observed.

---

# 13. Exact R6 multi-epoch use

Every Wave receives its own R6 epoch seal.

Multiple R6 epochs may remain live simultaneously.

Completion uses the exact per-Wave seal, not a global newest/current descriptor vector.

---

# 14. Exact P4 lease use

Every Wave acquires its own exact P4 Local Muon lease.

The backend pending Wave receives a `TensorCubeLocalMuonAtlasLeaseContextR1` built from the exact P4 identity.

The P4 lease is bound to the real Local Muon SubmissionEpoch set after Queue submit.

---

# 15. Exact P5 registration

After physical submission, the real SubmissionEpoch set is registered in P5.

The Wave's typed semantic consumers include:

- `CanonicalCandidate`;
- `R6CompletionEvidence`;
- `B05DeviceCandidate`;
- `B06DeviceSuccessor`;
- `BpDkDevicePostUpdateEvidence`;
- `MuonSegmentedSuccessorApplication`.

No anonymous raw consumer decrement is used in the new scheduler.

---

# 16. Completion routing

The production queue retains the exact reverse relationship between real SubmissionEpoch and production Wave.

A completed pending object is collected through the existing nonblocking ActiveDevice collector.

If it is not ready, the same owned pending object is restored to the queue.

No physical object reconstruction occurs.

---

# 17. Physical completion is not semantic completion

When the Local Muon SubmissionEpoch completes, R2:

1. records exact P5 physical completion;
2. records exact P4 physical completion;
3. completes the exact R6 epoch;
4. obtains the GPU-resident ActiveDevice successor.

It does not retire the P4 lease at this point.

---

# 18. B06 multi-Wave successor blocker and fix

The prior B06 implementation contained only:

`Option<LocalMuonDeviceSuccessorTicketR1>`.

That structure could not accept two successor tickets from one multi-Wave parameter.

R2 replaces it with:

`BTreeMap<String, LocalMuonDeviceSuccessorTicketR1>`

keyed by pending-Wave identity digest.

Duplicate insertion for the same Wave rejects with:

`FAIL_B06_PARTIAL_OPTIMIZER_COMMIT:duplicate-muon-successor-wave`.

---

# 19. B06 successor ledger identity

The ledger digest is versioned under:

`ASH.B06.MUON.DEVICE.SUCCESSOR.LEDGER.R2`.

Active commit preparation validates all staged successor tickets and aggregates their exact SubmissionEpoch set.

The aggregate must match the B05 Muon device-candidate SubmissionEpoch authority.

---

# 20. Source-derived segmented-generation blocker

The parent segmented generation initially stored one whole backing per canonical parameter.

That was insufficient for production Atlas-wave execution because one parameter may complete through multiple pending Waves.

Publishing A and B as two whole entries under one parameter key would be invalid.

R2 therefore introduces parameter-sized device assembly.

---

# 21. Parameter-sized device assembly

New physical owner:

`MuonDeviceParameterAssemblyR2`.

It allocates parameter-sized GPU arenas for:

- candidate weight;
- candidate Muon momentum;
- orthogonal update.

It tracks exact element-range reservation and completion.

---

# 22. D2D fragment publication

A completed ActiveDevice successor is not copied to host.

Instead:

`submit_successor_fragment_r2(...)`

issues device-to-device copies into the exact parameter assembly offsets.

It copies:

- candidate weight;
- candidate momentum;
- orthogonal update.

Each copy has its own real A01 SubmissionEpoch.

---

# 23. D2D copy lifetime

The source successor arenas remain owned until the fragment-copy SubmissionEpoch physically completes.

Only after that copy completes are the old successor candidate arenas reclaimed.

Therefore P4/Atlas reuse cannot race a D2D read from the old candidate backing.

---

# 24. P4/P5 retirement after stable handoff

For a Wave, the order is:

```text
Local Muon physical complete
→ B06 successor ticket staged
→ fragment D2D copy submitted
→ fragment D2D copy physically complete
→ release exact P5 consumer tokens
→ P5 SemanticComplete
→ retire exact P4 lease
→ mark P5 lease retired
→ retire production queue entry
```

P4 retirement is therefore later than both Local Muon completion and stable device handoff.

---

# 25. Parameter assembly coverage

The assembly requires:

- no overlapping reserved ranges;
- no duplicate completed ranges;
- zero active fragment writers;
- exact contiguous coverage from element 0 to parameter element count.

`coverage_complete()` must be true before finalization.

---

# 26. Stable target-generation publication

Once exact parameter coverage is complete, the assembly is consumed into:

- one whole `MuonDeviceSegmentBackingR1`;
- one whole `BpDkDeviceUpdateEvidenceBackingR1`.

These are published through the existing segmented-generation/evidence-arena authority.

The stable parameter backing is no longer tied to one ephemeral P4 lease.

---

# 27. Exact subrange device-source support

R2 extends `MuonDeviceSegmentBackingR1` with exact range leases:

`issue_source_range_lease_r2(generation_digest, element_start, element_count)`.

`MuonDeviceSegmentedSourceLeaseR1` now carries `element_start`.

The direct Local Muon bind group uses `wgpu::BufferBinding` offset/size rather than assuming the whole parameter backing equals one Wave.

---

# 28. Next-generation Wave source

This permits one contiguous parameter backing in generation G to serve multiple independent Local Muon Waves as exact read-only subranges.

No source weight or momentum H2D is introduced by the range lease.

---

# 29. Target-generation BP-DeltaK observation while generation is building

R2 adds a building-segment read lease for the target generation.

After one canonical parameter has been fully assembled/published, BP-DeltaK may read that parameter even if other parameters of target generation G+1 are not yet complete.

This does not make the whole generation canonical or committed.

---

# 30. BP-DeltaK device evidence

After parameter assembly publication, R2 invokes the already-materialized `BpDkDevicePostUpdateRuntimeR1`.

It reads:

- source parameter backing;
- target parameter backing;
- orthogonal-update evidence backing.

It returns the existing canonical `AshBpDkPostUpdateParameterReceipt` semantics through compact device evidence.

No host candidate `push_tile()` data path is used inside the ActiveAsync parameter helper.

---

# 31. Device source-generation installation

R2 adds explicit:

`install_muon_device_source_generation_r2(...)`.

The caller must provide a complete generation whose target generation equals the current B06 committed model generation.

This is an explicit seed/import authority.

R2 does not silently claim that arbitrary existing host/model memory is already a valid device segmented generation.

---

# 32. Target generation creation

`ensure_muon_device_target_generation_r2(source_generation)` lazily creates the exact G+1 Muon target generation and BP-DeltaK update-evidence arena.

Expected parameter/element counts come from the existing registry's Muon candidate projection.

---

# 33. Device-generation rotation hook

R2 adds:

`rotate_muon_device_generation_after_active_commit_r2(...)`.

It requires:

- target generation complete;
- target generation equals committed model generation;
- BP-DeltaK update evidence arena drained;
- old source generation has zero active readers.

Only then does target become the next source generation.

Because full production cutover is currently false, this hook is not yet activated as a normal production path.

---

# 34. R2B transient reclamation correction

The previous R2B reclamation logic blanket-rejected ActiveAsync.

R2 now permits parameter/step transient reclamation under ActiveAsync only when exact runtime state is drained:

- production pending queue count = 0;
- P5 in-flight Wave count = 0;
- P4 active lease count = 0.

No cleanup is allowed merely because a local callback returned.

---

# 35. P4 active-lease telemetry

P4 exposes an exact active lease count getter for these drain gates.

This is telemetry/admission state, not a replacement for exact per-lease identity.

---

# 36. Parameter scheduler output authority

The new ActiveAsync helper returns no full host candidate vectors.

Its output classifies:

- `device_candidate_mode = ActiveDeviceCandidate`;
- candidate weight readback = 0;
- candidate momentum readback = 0;
- update readback = 0;
- host candidate materialization count = 0;
- exact wait wall = 0;
- source weight/momentum upload bytes = 0 for device-source execution.

This is exactly why the outer full-model host scatter cannot consume it yet.

---

# 37. No silent outer fallback

The production callsite checks the outer consumer capability before entering the new ActiveAsync parameter helper.

Current source therefore cannot accidentally:

- run the new device-only helper;
- receive empty host candidate vectors;
- continue into old full-model host scatter.

The failure is earlier and explicit.

---

# 38. Outer full-model boundary remains canonical blocker

The exact remaining source boundary is the outer full-model candidate/serialization scheduler.

It currently combines:

- Muon candidate results;
- AdamW candidate updates;
- full candidate weight serialization;
- optimizer state serialization;
- parameter-stage publication.

A full production ActiveAsync cutover requires a device-segmented/full-model successor consumer at that level.

---

# 39. AdamW implication

Because the outer scheduler combines Muon and AdamW ownership into one full candidate authority, the next boundary cannot be solved by Local Muon alone.

The next revision must inspect/materialize the AdamW ActiveDevice candidate path and full-trainable generation ownership as part of retiring the host candidate scatter.

Muon-only segmented generation closure does not imply full-model segmented generation closure.

---

# 40. Full production cutover remains fail-closed

The current exact source state is:

```text
Local Muon parameter ActiveAsync scheduler        true
B06 multi-Wave successor ledger                   true
parameter-sized D2D assembly                      true
subrange device source                            true
device BP-DeltaK parameter evidence                true
outer full-model device successor consumer         false
full production pending queue cutover               false
parent P5 physical PASS                            not claimed
```

---

# 41. Reserved R2 physical PASS meaning

The R2 full PASS token remains reserved for the originally intended physical production closure.

It is not emitted by this source bake.

Full PASS still requires an actual production path capable of reaching the bound=2 scheduler through the outer full-model consumer and then physically demonstrating overlap.

---

# 42. Required future A/B physical witness

After the outer full-model boundary is closed, the same R2 scheduler must demonstrate:

```text
A real Local Muon Wave submitted
A remains pending
B real Local Muon Wave submitted before A collect
peak pending > 1
```

No synthetic sleep/qualification-only queue may substitute for this witness.

---

# 43. Required future physical counters

Full R2/P5 physical closure still requires:

- submitted Wave count > 1;
- peak in-flight Wave count > 1;
- submit-while-prior-pending count > 0;
- exact async completion count matching tracked submissions;
- semantic retirement count matching successfully submitted Waves;
- P4 retirement count matching successfully closed Waves;
- ordinary ActiveAsync exact-wait count = 0;
- orphan submissions = 0;
- premature retirements = 0;
- final production queue = 0;
- final P5 in-flight = 0;
- final P4 active leases = 0;
- final R6 active epochs = 0.

---

# 44. Required future negative fixtures

Physical qualification must still exercise:

- duplicate completion rejection;
- stale P4 slot-generation rejection;
- unknown SubmissionEpoch rejection;
- double typed-consumer release rejection;
- bound-2 third-Wave backpressure.

No negative fixture may mutate the current live generation.

---

# 45. Parent P5 remains canonical

Even once full cutover becomes true, this R2 child does not directly set:

`active_async_enabled = true`

or:

`per_wave_exact_wait_retired = true`.

Those remain evidence-derived outputs of the canonical parent P5 receipt.

---

# 46. R2 static validator

New validator:

`tools/validate_ash_basetrain_unified_atlas_mcu_local_muon_production_pending_wave_queue_cutover_active_async_r2_static.py`.

It verifies at minimum:

- R2 revision constants;
- parameter-level scheduler capability true;
- outer full-model device successor consumer false;
- full cutover is the conjunction of those two capabilities;
- actual parameter ActiveAsync scheduler helper exists;
- bounded queue admission via existing queue core;
- direct segmented source submission;
- exact P4/R6/P5 registration;
- nonblocking pending collection;
- no exact blocking wait in the helper;
- B06 per-Wave successor ledger;
- parameter-sized D2D assembly;
- exact assembly coverage;
- exact source subrange bindings;
- device BP-DeltaK runtime use;
- P2/fused/R8/R8A/replay/counterfactual fail-closed scope;
- exact outer full-model blocker;
- existing outer host candidate scatter still present;
- source-generation install/rotation bridges;
- full production cutover still fail-closed.

---

# 47. Prior validator source-truth update

Several earlier static validators previously required the literal source string:

`TENSORCUBE_LOCAL_MUON_PRODUCTION_PENDING_QUEUE_CUTOVER_MATERIALIZED_P5_R1: bool = false`.

R2 replaces that literal with a derived capability expression.

Those validators are updated to verify the actual source-truth equation and the explicit outer blocker instead of a stale textual literal.

This is validator maintenance, not a weakening of the gate.

---

# 48. Static regression chain

The current source bake statically passes:

- R2 parameter-scheduler/full-model-boundary validator;
- BP-DeltaK device reduction/exact digest child;
- Device Segmented Source Direct Submit child;
- BP-DeltaK segmented successor child;
- pending queue core / BP-DeltaK R2 gate;
- ActiveDevice pending handoff;
- prior production-cutover child validator;
- generic pending submit/later collect;
- parent P5 SubmissionEpoch dependency validator;
- P4 exact Atlas lease validator;
- P3 transactional commit/restart validator;
- P2 real production Wave shadow validator;
- P1 immutable bundle validator;
- P0 physical evidence-truth validator;
- R6 validator;
- R7 validator;
- MCU control-plane validator.

---

# 49. R8/R8A validator packaging behavior

R8/R8A source validators continue to stop at their existing `specs/*.md` presence check in source-only ZIP worktrees because specifications are deliberately excluded from implementation packages.

Current observed stop points:

- `R8_STATIC_MISSING:specs/ASH_BASETRAIN_UNIFIED_ATLAS_MCU_DETERMINISTIC_PRECISION_EXPERT_ROUTER_AND_PATH_INTEGRAL_POLICY_COMPILER_R8_SPEC.md`;
- `R8A_STATIC_MISSING:specs/ASH_BASETRAIN_UNIFIED_ATLAS_MCU_GPU_RESIDENT_EXPERT_BUCKET_VIEW_AND_HETEROGENEOUS_DISPATCH_R8A_SPEC.md`.

No new R8/R8A source failure is claimed.

---

# 50. Compile boundary

A real Rust release compile is mandatory before this source can be physically exercised.

R2 changes ownership/type paths across:

- Production Muon scheduler;
- B06 successor staging;
- WGPU parameter assembly;
- source range bindings;
- segmented generation lifetime;
- P4/P5 retirement;
- BP-DeltaK target-generation access.

Static token validation and delimiter scans cannot replace the Rust compiler or borrow checker.

---

# 51. Current assistant environment limitation

The bake environment contains no:

- `cargo`;
- `rustc`;
- `rustfmt`;
- `naga`;
- WGSL analyzer.

Therefore this bake does not claim:

- release compile PASS;
- WGPU shader validation;
- real A/B GPU overlap;
- bound=2 physical qualification;
- parent P5 PASS.

---

# 52. Source syntax QA

A lightweight delimiter scanner passes the modified Rust source surfaces.

All relevant Python static validators compile with `py_compile`.

These are source QA only.

---

# 53. Exact next gate

The next source boundary should be explicitly named around the newly discovered outer authority rather than creating another Local Muon pending child.

Recommended next revision:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-FULL-MODEL-DEVICE-SEGMENTED-SUCCESSOR-CONSUMER-AND-HOST-CANDIDATE-SCATTER-RETIREMENT-CLOSURE-R1`

Its scope must include the real relationship between:

- Muon device-segmented successor;
- AdamW ActiveDevice candidate/staging;
- full-trainable next-generation ownership;
- outer full-model parameter serialization/commit authority.

---

# 54. Next-gate minimum requirements

The outer consumer child must ensure that the full-model scheduler can consume a Muon device-only successor without:

- full Muon candidate D2H;
- stale host Muon values;
- fake empty candidate vectors;
- silently reconstructing a second canonical full-model state.

It must also determine whether AdamW already has a real production ActiveDevice staging path or requires its own materialization.

---

# 55. Full cutover activation after next gate

Only when the outer full-model consumer is physically connected may:

`TENSORCUBE_LOCAL_MUON_OUTER_FULL_MODEL_DEVICE_SEGMENTED_SUCCESSOR_CONSUMER_MATERIALIZED_R2`

become true.

Then the derived full cutover capability can become true without changing the parameter-scheduler capability.

---

# 56. Physical campaign after outer boundary closure

Once the full cutover source gate resolves true:

1. run release compile;
2. seed/install an exact current Muon device generation;
3. configure P5 ActiveAsync bound=2;
4. keep P2 shadow/replay/counterfactual/R8A outside the unqualified async campaign;
5. submit real Wave A;
6. submit real Wave B while A remains pending;
7. observe exact completions, allowing B-before-A;
8. complete D2D assembly handoff;
9. produce device BP-DeltaK evidence;
10. close typed P5 consumers;
11. retire exact P4 leases;
12. drain queue/P5/P4/R6;
13. run negative identity fixtures;
14. seal R2 child physical receipt;
15. feed the same observations into parent P5;
16. only parent P5 may activate ActiveAsync final state.

---

# 57. AdamW/full-model caveat

This R2 source bake proves no AdamW ActiveDevice physical closure.

The existence of `stage_adamw_device_candidate(...)` or a device backing type alone is not sufficient.

The next source review must identify the real production callsite and ownership/lifetime path before making a full-trainable-generation claim.

---

# 58. P3 caveat

Even after full runtime ActiveAsync closure, device-resident current-generation state is not automatically durable restart authority.

An exact P3 device-generation-to-durable-pack/materialization bridge remains a later boundary.

---

# 59. R8A caveat

Local-domain ActiveAsync does not imply heterogeneous R8A multi-view lifetime closure.

R8A requires its own exact simultaneous view-generation authority before it can enter the production async scheduler.

---

# 60. Packaging policy

Implementation source ZIP excludes:

- this specification and all Markdown;
- `specs/`;
- patch notes;
- `BAKE_MANIFEST*`;
- generated R2/P5/P4 qualification receipts;
- runtime JSON/JSONL;
- `current.json`;
- `publication_seal.json`;
- P3 runtime transaction artifacts;
- logs/review outputs;
- Python bytecode caches.

Rust/WGSL/Python implementation source remains included.

---

# 61. GitHub publication policy

GitHub publication for this revision is specification-only unless implementation publication is separately requested.

---

# 62. Current bake claim

This bake may claim:

```text
Local Muon parameter ActiveAsync scheduler       MATERIALIZED
bound-2 capable queue state machine              MATERIALIZED
B06 multi-Wave successor ledger                 MATERIALIZED
parameter-sized D2D successor assembly           MATERIALIZED
exact subrange device-source leases              MATERIALIZED
device BP-DeltaK parameter evidence integration  MATERIALIZED
exact P4/P5 retirement ordering                  MATERIALIZED
outer full-model host-scatter blocker            EXPLICIT / FAIL-CLOSED
full production cutover                          FALSE
R2 physical overlap PASS                         NOT OBSERVED
parent P5 PASS                                   NOT CLAIMED
```

---

# 63. Full R2 PASS remains reserved

Full R2 PASS means the actual outer production scheduler has adopted device-segmented successor authority, the Local Muon bound=2 parameter scheduler is physically reachable through that production path, A and B are demonstrably in flight together, all exact identity/lifetime gates close, and parent P5 receives real evidence rather than source constants.

This source bake does not claim that state.

---

# 64. Center sentence

> **R2에서 줄은 실제로 섰습니다. Local Muon parameter 안에서는 A와 B를 동시에 들 수 있고, B06도 Wave별 ticket을 모으며, 완료된 fragment는 CPU가 아니라 parameter-sized GPU assembly로 D2D 이동하고, BP-DeltaK도 device evidence로 끝낼 수 있습니다. 그런데 그 바깥 full-model scheduler가 아직 “Muon 후보 숫자를 host 배열에 넣어 달라”고 합니다. 거기서 다시 D2H를 하면 지금까지 닫은 ActiveDevice SSOT를 깨게 됩니다. 그래서 이번 bake는 queue를 억지로 true로 만들지 않습니다. 안쪽 async scheduler는 true, 바깥 full-model device consumer는 false, 따라서 full cutover는 false입니다. 다음 revision은 바로 그 마지막 host candidate 권위를 걷어내야 합니다.**
