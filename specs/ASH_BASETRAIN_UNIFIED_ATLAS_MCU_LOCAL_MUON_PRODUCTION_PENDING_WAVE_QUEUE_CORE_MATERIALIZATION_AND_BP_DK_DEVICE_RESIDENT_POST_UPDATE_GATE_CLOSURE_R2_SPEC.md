# ASH-BASETRAIN-UNIFIED-ATLAS-MCU-LOCAL-MUON-PRODUCTION-PENDING-WAVE-QUEUE-CORE-MATERIALIZATION-AND-BP-DK-DEVICE-RESIDENT-POST-UPDATE-GATE-CLOSURE-R2

## Runtime-Owned ActiveDevice Pending Queue / Exact SubmissionEpoch-to-Wave Index / Pending-to-Successor Ownership Transfer / Bounded In-Flight State / P5-P4 Retirement Preconditions / BP-DeltaK Host-Tile Dependency Attribution / Fail-Closed Production Cutover

---

# 0. Revision identity

Revision:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-LOCAL-MUON-PRODUCTION-PENDING-WAVE-QUEUE-CORE-MATERIALIZATION-AND-BP-DK-DEVICE-RESIDENT-POST-UPDATE-GATE-CLOSURE-R2`

Parent:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-LOCAL-MUON-ATLAS-WAVE-ACTIVE-DEVICE-CANDIDATE-PENDING-HANDOFF-AND-DEVICE-SUCCESSOR-COLLECT-CLOSURE-R1`

Structural PASS token:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_LOCAL_MUON_PRODUCTION_PENDING_WAVE_QUEUE_CORE_MATERIALIZATION_AND_BP_DK_DEVICE_RESIDENT_POST_UPDATE_GATE_CLOSURE_R2`

Static PASS:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_LOCAL_MUON_PRODUCTION_PENDING_WAVE_QUEUE_CORE_BP_DK_GATE_R2_STATIC`

---

# 1. Purpose

The previous child made the B05 ActiveDeviceCandidate Local Muon submission physically capable of returning before completion while keeping candidate weight, Muon momentum and orthogonal update GPU-resident behind `LocalMuonActiveDeviceSuccessorR1`.

The next intended production state is a bounded queue that owns more than one such pending Wave.

While wiring that queue into the real parameter streaming path, a higher-level dependency became authoritative:

`AshBpDkPostUpdateStreamingBuilder::push_tile()` still consumes full host `f32` candidate weight, candidate momentum and orthogonal-update tile vectors.

Therefore the production queue may be materialized as a real owner, but the streaming-loop ActiveAsync cutover cannot be truthfully enabled until BP-DeltaK post-update has a device-resident consumer/evidence path.

This revision materializes the bounded queue core and seals that remaining blocker as explicit source truth.

---

# 2. Center invariant

The runtime now distinguishes four separate identities:

`backend pending Wave identity`

`P5 semantic Wave identity`

`real SubmissionEpoch identity`

`P4 Atlas lease identity`.

None of them may be silently substituted for another.

---

# 3. Queue core source truth

New source capability:

`TENSORCUBE_LOCAL_MUON_PRODUCTION_PENDING_QUEUE_CORE_MATERIALIZED_P5_R2 = true`.

This means a runtime-local bounded owner exists for real `PendingLocalMuonActiveDeviceCandidateR1` objects and their later `LocalMuonActiveDeviceSuccessorR1` objects.

It does not mean the production streaming loop has completed its ActiveAsync semantic cutover.

---

# 4. Full production cutover remains separate

Existing capability remains:

`TENSORCUBE_LOCAL_MUON_PRODUCTION_PENDING_QUEUE_CUTOVER_MATERIALIZED_P5_R1 = false`.

The queue data structure exists, but the parameter streaming transaction still cannot consume device-only candidate results through all required higher-level authorities.

---

# 5. New BP-DeltaK source-truth gate

New capability:

`TENSORCUBE_LOCAL_MUON_BP_DK_DEVICE_RESIDENT_POST_UPDATE_CONSUMER_MATERIALIZED_P5_R1 = false`.

This is the exact blocker for production ActiveAsync cutover after the ActiveDevice pending handoff.

---

# 6. Why the BP-DeltaK gate is false

The current `AshBpDkPostUpdateStreamingBuilder::push_tile()` contract requires:

- source weight `[f32;256]`;
- source momentum `[f32;256]`;
- candidate weight `[f32;256]`;
- candidate momentum `[f32;256]`;
- orthogonal update `[f32;256]`.

It computes full-value-dependent evidence including candidate RMS, deltas, pair cosines and exact candidate digests.

The current streaming callsite also writes successor weight and process-local momentum from those host candidate tiles.

The new ActiveDevice pending path intentionally does not create those host candidate vectors.

---

# 7. No readback rollback

This revision MUST NOT solve the mismatch by reading candidate weight/momentum/update back to the host.

That would violate the already materialized B05 ActiveDeviceCandidate contract:

`candidate_weight_full_d2h_bytes = 0`

`candidate_momentum_full_d2h_bytes = 0`

`update_full_d2h_bytes = 0`

`host_full_candidate_materialization_count = 0`.

---

# 8. Queue owner

`ProductionMuonPendingWaveQueueCoreR2` is runtime-local state owned by `ProductionMuonExecutionRuntime`.

It is not process-global and is not owned by the backend module.

---

# 9. Exact queue key

`ProductionMuonPendingWaveKeyR2` binds:

- parameter identity digest;
- Wave ordinal;
- exact R6 queue generation;
- exact P5 semantic Wave identity digest;
- exact P4 lease digest;
- canonical queue-key digest.

---

# 10. Backend identity is not P5 identity

The backend pending object's `PendingLocalMuonWaveIdentityR1.identity_digest` and the P5 semantic Wave identity are distinct axes.

The queue requires both to exist but does not rewrite one into the other.

This prevents backend physical lifetime identity from becoming semantic transaction identity by coincidence.

---

# 11. SubmissionEpoch index

The queue core maintains:

`(device_id, queue_id, submission_ordinal) -> queue Wave key`.

Every real SubmissionEpoch belonging to an enqueued pending Wave must be unique in this index.

Duplicate registration fails closed.

---

# 12. Queue physical states

`ProductionMuonPendingPhysicalStateR2` contains:

- Submitted;
- Collecting;
- SuccessorReady;
- SuccessorClaimed;
- Retired;
- Failed.

The physical owner is represented separately so ownership moves can be exact.

---

# 13. Physical owner states

The queue physically owns one of:

`Submitted(PendingLocalMuonActiveDeviceCandidateR1)`

or:

`SuccessorReady(LocalMuonActiveDeviceSuccessorR1)`.

A short `EmptyTransition` state exists only while Rust ownership is moved out for collection or downstream device consumption.

---

# 14. Bounded admission

`ProductionMuonPendingWaveQueueCoreR2::new(max_in_flight_waves)` requires a positive bound.

`enqueue_submitted()` rejects admission when the current queue cardinality has reached that bound.

No silent bound overshoot is allowed.

---

# 15. Pending insertion invariants

`enqueue_submitted()` requires:

- at least one real SubmissionEpoch;
- exact P4 lease digest equality between queue key and pending object;
- non-empty backend pending identity;
- no duplicate queue key;
- no duplicate SubmissionEpoch mapping.

---

# 16. Collection ownership transfer

`take_submitted_for_collect()` moves the actual pending object out of the queue and changes queue state to `Collecting`.

If the backend is not yet ready, `restore_submitted_after_not_ready()` moves the same object back into queue ownership.

No object reconstruction from a global table occurs.

---

# 17. Successor publication

When nonblocking collection creates a `LocalMuonActiveDeviceSuccessorR1`, `publish_successor_ready()` moves that successor into the queue.

The successor's P4 lease digest must equal the queue key's P4 lease digest.

---

# 18. Device-consumer handoff

`take_successor_for_device_consumer()` moves the physical GPU successor out of queue ownership and marks the entry `SuccessorClaimed`.

The downstream device consumer then owns that moved value until its exact release path completes.

---

# 19. No duplicate physical owner

At no time may the queue simultaneously own both the submitted pending object and the successor object for the same Wave.

Rust move semantics are the preferred enforcement mechanism.

---

# 20. Queue retirement prerequisites

`retire_entry()` requires external proof that:

- P5 semantic completion is true;
- P4 exact lease retirement is complete;
- the physical successor has already been moved out/consumed.

The queue does not retire P4 itself.

---

# 21. Exact epoch index removal

On successful queue entry retirement, every SubmissionEpoch owned by that entry is removed from the queue's exact reverse index.

Drain requires both the Wave map and SubmissionEpoch index to be empty.

---

# 22. Queue core is wired into ProductionMuonRuntime

`ProductionMuonExecutionRuntime` now owns:

`production_pending_wave_queue_core_r2: ProductionMuonPendingWaveQueueCoreR2`.

The queue is constructed with the exact P5 `max_in_flight_waves` bound.

This makes the queue's state ownership location explicit and reproducible.

---

# 23. Active runtime construction

P5 ActiveAsync runtime construction may now proceed when:

- generic pending submit/collect split exists;
- ActiveDeviceCandidate pending handoff exists;
- bounded queue core exists.

The production execution path itself remains gated before it can fall into the legacy Mirror-only streaming route.

---

# 24. Callsite preflight

At entry to the current Atlas-wave streaming function, if the production cutover runtime is ActiveAsync, it calls:

`require_active_production_cutover_ready()`.

The call happens before the legacy B05/B06 MirrorVerified assertions.

---

# 25. Exact current failure

Because the BP-DeltaK device-resident post-update consumer is not yet materialized, the Active path fails with:

`E_MCU_P5_BP_DK_DEVICE_RESIDENT_POST_UPDATE_CONSUMER_REQUIRED`.

This prevents the runtime from accidentally falling through to Mirror bulk readback.

---

# 26. Legacy Mirror streaming remains unchanged

When P5 production ActiveAsync cutover is not active, the existing MirrorVerified streaming path remains unchanged.

This revision does not silently alter its numerical/evidence behavior.

---

# 27. Cutover receipt extension

`ProductionMuonPendingQueueCutoverReceiptR1` now reports two additional source-truth fields:

- `production_pending_queue_core_materialized`;
- `bp_dk_device_resident_post_update_consumer_materialized`.

The full PASS predicate requires both to be true in addition to the previous ActiveAsync evidence conditions.

---

# 28. Parent P5 remains canonical

This revision does not create a second ActiveAsync PASS authority.

The canonical parent P5 receipt remains the only authority allowed to derive:

`active_async_enabled = true`

and:

`per_wave_exact_wait_retired = true`.

---

# 29. Current bake state

Materialized in this bake:

- runtime-owned bounded ActiveDevice pending queue core;
- exact SubmissionEpoch reverse index;
- exact pending take/restore ownership transition;
- exact pending-to-successor ownership transition;
- exact successor-to-device-consumer ownership transition;
- queue retirement requiring P5 semantic completion and P4 retirement;
- queue drain authority;
- ProductionMuonRuntime queue ownership;
- Active streaming preflight;
- explicit BP-DeltaK device-resident post-update gate;
- cutover receipt source-truth extensions;
- R2 static validator.

Not materialized in this bake:

- device-resident BP-DeltaK post-update consumer;
- device-resident successor-weight/momentum post-update application replacing host tile writes;
- actual production multi-Wave streaming-loop cutover;
- peak in-flight > 1 physical evidence;
- parent P5 PASS.

---

# 30. Why production cutover remains false

The current streaming loop still commits ordered tiles through host `PendingTile` values and calls:

`post_update_builder.push_tile(... candidate_weight, candidate_momentum, orthogonal_update ...)`.

It then writes successor weight/momentum from those same host vectors.

Until those operations have a device-resident equivalent or an explicitly qualified compact/device evidence authority, production ActiveDevice multi-Wave execution cannot proceed without violating B05.

---

# 31. Static validator

Validator:

`tools/validate_ash_basetrain_unified_atlas_mcu_local_muon_production_pending_wave_queue_core_bpdk_gate_r2_static.py`.

It verifies at minimum:

- R2 revision identity;
- bounded queue core type;
- actual pending and successor physical ownership types;
- queue-core source capability true;
- BP-DeltaK device-resident consumer capability false;
- full production cutover capability false;
- exact SubmissionEpoch reverse index;
- take/restore/publish/take/retire/drain transitions;
- queue owned by `ProductionMuonExecutionRuntime`;
- Active streaming preflight exists;
- current post-update builder still requires host candidate `f32` slices;
- current streaming loop still feeds host candidate tiles into that builder;
- ActiveDevice pending path still has zero full-candidate D2H and no exact wait;
- no unqualified Active streaming helper exists.

---

# 32. Regression requirements

The following source/static gates must remain PASS:

- R2 queue-core/BP-DeltaK gate;
- ActiveDevice pending handoff R1;
- production pending-wave cutover R1;
- pending submit/later collect R1;
- parent P5 ActiveAsync;
- P4 exact Atlas lease;
- P3 transactional commit/restart;
- P2 real production shadow;
- P1 immutable bundle;
- P0 evidence truth;
- R6;
- R7;
- MCU control plane.

R8/R8A may continue to stop only at their existing spec-presence checks because source ZIP packaging excludes Markdown specifications.

---

# 33. Compile boundary

A real Rust release compile is still mandatory.

This environment does not contain `cargo`, `rustc` or `rustfmt`, so this bake may claim source/static validation only.

No compile or RTX physical PASS is implied.

---

# 34. Next exact child

The next implementation gate is:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-BP-DK-DEVICE-RESIDENT-POST-UPDATE-EVIDENCE-AND-SUCCESSOR-APPLICATION-CLOSURE-R1`.

That child must replace the host candidate-tile dependency for the ActiveDevice production path without reintroducing full candidate D2H.

---

# 35. Required next-child authority

The device-resident BP-DeltaK child must provide enough exact authority to replace the current host operations for ActiveDevice mode:

- candidate weight post-update evidence;
- candidate momentum post-update evidence;
- orthogonal-update evidence;
- exact candidate digest/effectiveness evidence required by current BP-DeltaK contracts;
- successor weight application;
- successor Muon momentum application;
- canonical Wave/tile ordering identity.

---

# 36. No evidence weakening

The next child may move evidence production to GPU/compact form, but it may not simply delete current BP-DeltaK gates to obtain ActiveAsync.

Any evidence contract replaced must preserve or explicitly re-qualify the semantics currently enforced by `AshBpDkPostUpdateStreamingBuilder`.

---

# 37. After the next child

Once the BP-DeltaK device-resident consumer is physically qualified:

1. flip only its exact source-truth capability;
2. wire the already materialized queue core into the production Wave scheduling loop;
3. flip the full production cutover capability only after the callsite actually uses the queue;
4. run bound=2 physical qualification;
5. require peak in-flight > 1;
6. require ordinary per-Wave exact wait count = 0;
7. require exact P5 semantic closure;
8. require exact P4 retirement;
9. drain queue/P5/P4 to zero;
10. seal parent P5 PASS.

---

# 38. Packaging policy

Implementation source ZIP excludes:

- this specification and all `specs/` content;
- Markdown patch notes;
- `BAKE_MANIFEST*`;
- generated P0-P5 receipts/evidence;
- generated queue receipts;
- generated runtime/qualification JSON or JSONL;
- `current.json`;
- `publication_seal.json`;
- P3 transaction runtime artifacts;
- validation logs;
- review artifacts;
- Python bytecode caches.

Implementation Rust/Python source remains included.

---

# 39. GitHub publication policy

GitHub publication for this revision is spec-only unless implementation publication is separately requested.

---

# 40. PASS semantics

The structural R2 PASS means the production runtime now has one explicit bounded SSOT that can own real ActiveDevice pending Wave objects and later GPU-resident successor objects, index every real SubmissionEpoch back to the exact Wave, move physical ownership exactly once through collection and device-consumer handoff, and retire queue identity only after P5 semantic completion and P4 lease retirement.

It also means the source truthfully blocks production ActiveAsync before the legacy Mirror-only streaming path because the current BP-DeltaK post-update contract still requires full host candidate tiles.

The R2 source/static PASS does not mean the production multi-Wave ActiveAsync physical campaign has passed.

---

# 41. PASS does not mean

This revision does not prove:

- BP-DeltaK device-resident post-update closure;
- production peak in-flight > 1;
- parent P5 ActiveAsync PASS;
- `active_async_enabled=true`;
- `per_wave_exact_wait_retired=true`;
- R8A multi-view async;
- R8B pressure routing;
- maximum throughput.

---

# 42. Center sentence

> **GPU pending과 B06 successor는 이제 실제 bounded queue 안에 들어갈 자리가 생겼다. SubmissionEpoch도 어느 Wave 것인지 정확히 역으로 찾을 수 있다. 그런데 production의 윗층 BP-ΔK는 아직 candidate 숫자 자체를 CPU 타일로 받아야 움직인다. 그 숫자를 다시 읽어오면 ActiveDevice를 깨는 거라서, queue를 억지로 켜지 않는다. 이번 R2는 줄을 세우는 그릇을 실제로 만들고, 다음 막힘을 `BP-ΔK device-resident post-update` 한 점으로 좁힌다.**