# ASH-BASETRAIN-UNIFIED-ATLAS-MCU-LOCAL-MUON-PENDING-SUBMISSION-HANDLE-AND-LATER-COLLECT-MATERIALIZATION-CLOSURE-R1

## Real Submit-Before-Wait / Owned Pending Physical Wave / Exact SubmissionEpoch Early Return / Deferred Map-Readback Collection / P4 Lease Pin / P5 Dependency Handoff / No Hidden Exact Wait / Parent-P5 Physical-Promotion Boundary

## 0. Revision identity

Revision:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-LOCAL-MUON-PENDING-SUBMISSION-HANDLE-AND-LATER-COLLECT-MATERIALIZATION-CLOSURE-R1`

Parent:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-SUBMISSION-EPOCH-DEPENDENCY-TRACKING-AND-ACTIVE-ASYNC-COMPLETION-CLOSURE-R1`

PASS:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_LOCAL_MUON_PENDING_SUBMISSION_HANDLE_AND_LATER_COLLECT_MATERIALIZATION_CLOSURE_R1`

Static PASS:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_LOCAL_MUON_PENDING_SUBMISSION_HANDLE_AND_LATER_COLLECT_R1_STATIC`

## 1. Purpose

The parent P5 already owns an exact SubmissionEpoch-keyed dependency ledger and P4 exact Atlas lease identity, but its source-truth backend capability was previously false because the Local Muon executor performed:

`encode -> submit -> map request -> exact wait -> collect -> reclaim -> return`.

That topology physically prevents a caller from receiving a live real submission before completion.

This child revision materializes the missing backend split:

`submit -> PendingTensorCubeLocalMuonWaveR1 -> return`

followed later by:

`nonblocking completion observation -> map readiness -> collect -> resource reclaim`.

The split is structural backend authority. It does not by itself grant the parent P5 physical PASS.

## 2. Center invariant

`Submission authority != Completion authority != Collection authority != Semantic retirement authority`.

Submission remains owned by the existing A01 Queue submission path.

Completion remains real SubmissionEpoch completion.

Collection is owned by the new pending Local Muon collector.

Semantic retirement remains P5 dependency closure followed by P4 exact-generation retirement.

## 3. Source-truth capability

The backend source constant:

`TENSORCUBE_LOCAL_MUON_ASYNC_SUBMIT_COLLECT_SPLIT_MATERIALIZED_P5_R1`

changes from `false` to `true` only because this bake contains a real submit-before-wait API and a separate later collect API.

This constant is not configurable through environment or CLI.

The parent P5 still derives `active_async_enabled` and `per_wave_exact_wait_retired` only from real physical campaign evidence.

## 4. Scope

This child owns:

- an owned pending Local Muon physical Wave handle;
- early return of the exact real SubmissionEpoch;
- exact P4 Atlas lease context preservation;
- ownership transfer of the GPU/readback resources required after submit;
- deferred map/readback collection;
- nonblocking physical-completion observation;
- exactly-once collection/reclamation;
- P4 asynchronous completion API needed by future parent-P5 cutover;
- a source static gate proving the pending submission path contains no exact wait.

## 5. Non-goals

This child does not claim:

- parent P5 ActiveAsync physical PASS;
- peak production in-flight Wave count > 1;
- production streaming-loop queue cutover already physically qualified;
- P2 zero-copy shadow comparison;
- fused-pair async execution;
- arbitrary multi-batch R8A widening;
- performance improvement;
- hardware Tensor Core E3.

## 6. Pending handle

`PendingTensorCubeLocalMuonWaveR1` contains:

- semantic pending Wave identity;
- exact real SubmissionEpoch vector;
- optional exact P4 Atlas lease context;
- explicit completion state;
- private execution metadata;
- private owned resource bundle.

A pending Wave is not identified by pointer address, callback order, thread ID, or Atlas slot alone.

## 7. Pending Wave identity

`PendingLocalMuonWaveIdentityR1` binds:

- Wave ID;
- parameter identity digest;
- R6 queue generation;
- execution descriptor manifest digest;
- optional R8 assignment digest;
- optional P4 lease digest;
- identity digest.

## 8. Supported physical domain in R1

The first pending implementation is deliberately bounded to the P4 Local Muon Atlas-wave one-physical-batch path.

Required:

- B05 device-candidate mode enabled;
- MirrorVerified-compatible bulk readback currently available;
- B04A Atlas-wave streaming active;
- one physical batch within the current device/Atlas capacity;
- Local Muon domain;
- existing R7/R8/R8A execution contracts unchanged.

The revision does not silently widen multi-batch or fused domains.

## 9. Submit APIs

The backend materializes three exact child APIs for the current production execution variants:

- `submit_resident_device_candidate_with_norm_path_p4_p5_pending_r1`;
- `submit_resident_device_candidate_with_norm_path_and_expert_r8_p4_p5_pending_r1`;
- `submit_resident_device_candidate_with_expert_buckets_r8a_p4_p5_pending_r1`.

They converge on one pending internal submission path.

## 10. Exact early-return ordering

Mandatory ordering:

1. validate live descriptors/input/expert/lease authority;
2. prepare the B04A Atlas-wave partition;
3. encode the exact existing Local Muon physical work;
4. allocate exact A01/A02/A03 resource leases;
5. submit through `a01_submit_with_leases`;
6. obtain the real SubmissionEpoch;
7. issue map requests and capture map tickets;
8. move all required ownership into the pending handle;
9. return the pending handle.

No `a01_wait_for_submission_exact` occurs in the pending source path.

## 11. No fake async

The following is forbidden as child completion:

`submit -> spawn worker -> exact wait in worker -> pretend pending`.

The current child pending module contains no exact-wait symbol.

The legacy synchronous executor may continue to contain exact waits as a compatibility path.

## 12. Real SubmissionEpoch

The pending handle receives the actual SubmissionEpoch produced by the existing A01 Queue submission authority.

No child-private ordinal replaces it.

Current one-physical-batch Local Muon execution returns one exact epoch; the ABI preserves a vector so future physically qualified multiple-submit paths do not need a new identity model.

## 13. P4 lease preservation

When P4 is active, the exact backend lease context is stored in the pending handle:

- runtime Atlas ID;
- Atlas identity digest;
- slot index;
- lease generation;
- lease digest.

Returning the pending handle does not retire that lease.

The slot may not be reused while this residency remains semantically live.

## 14. Resource ownership transfer

The pending resource bundle owns or guards the exact resources whose lifetime previously ended inside the monolithic executor stack, including the applicable:

- tracked A01 submission;
- gradient buffer guard;
- A02 output/readback arena leases;
- A03 upload and compact-readback leases;
- source/momentum/candidate/update/status buffer Arcs;
- R8A index/directory resources;
- asynchronous map tickets.

Resources are moved into pending ownership rather than recreated later from a global lookup.

## 15. No stack-borrow lifetime extension

The pending object contains no borrowed references whose owner disappears when submit returns.

No unsafe lifetime widening is introduced to make stack state survive.

## 16. Map identity

Map requests are issued before submit returns, but collection does not block for them.

The pending object keeps independent map-ticket identity for:

- candidate weight;
- candidate momentum;
- orthogonal update;
- tile status.

Collection readiness requires all required map tickets to be ready and the exact submission physically complete.

## 17. Nonblocking collection

`try_collect_pending_p5_r1()` performs a nonblocking device poll/refresh and exact A01 completion lookup.

If physical completion is not yet known, it returns `Ok(None)`.

If maps are not yet ready, it returns `Ok(None)`.

It does not invoke an exact blocking wait.

## 18. Completion states

`PendingLocalMuonCompletionStateR1` states are:

- `Submitted`;
- `PhysicalCompletionObserved`;
- `CollectionReady`;
- `Collected`;
- `Failed`.

A pending Wave may not be successfully collected twice.

## 19. Collection

Once ready, collection:

- reads candidate weight;
- reads candidate momentum;
- reads orthogonal update;
- reads tile status;
- validates existing nonfinite/completion/subgroup status contracts;
- marks readback resources unmapped;
- releases A01 submission leases;
- reclaims exact A02/A03 resources;
- records the B04A physical batch;
- marks the exact Atlas-wave partition physically complete;
- reconstructs the existing `TensorCubeLocalMuonBatchCandidateOutput` ABI.

## 20. Output compatibility

The child does not invent a parallel candidate-output semantic ABI.

Collected output remains `TensorCubeLocalMuonBatchCandidateOutput` and retains:

- candidate vectors;
- status;
- existing R4/R5/R7/R8A telemetry;
- exact real SubmissionEpoch evidence;
- P4 lease context;
- device-candidate backing identity.

## 21. Active-path exact wait telemetry

A collected pending output reports:

`poll_wait_count = 0`

and:

`exact_wait_wall_ns = 0`

because no per-Wave exact wait is performed in the child submit/collect path.

For R8A, `r8a_exact_submission_wait_observed=false` is expected under this path; asynchronous physical completion becomes the parent P5 authority instead.

## 22. P4 asynchronous completion extension

P4 gains exact per-SubmissionEpoch asynchronous completion observation.

Each active Atlas lease tracks:

- bound submission epochs;
- completed submission epochs.

An exact epoch can advance only the matching exact lease generation.

When all bound epochs complete, the P4 lease transitions to `CompletionObserved`.

Duplicate or stale completion remains fail-closed.

## 23. No slot-only completion

P4 asynchronous completion still requires the exact lease identity plus exact SubmissionEpoch.

A callback referring only to a slot number is never sufficient.

## 24. Parent P5 handoff

The parent P5 runtime already accepts `register_wave_after_submit(..., exact_wait_count=0, ...)` in `ActiveAsync` mode and has `observe_async_completion(real SubmissionEpoch)`.

The child provides the missing physical object that can now be registered before collection.

The next parent-P5 production cutover must perform:

`submit pending -> bind P4 submissions -> register P5 ledger -> admit later independent Wave -> observe completions -> collect -> release semantic consumers -> P4 retire`.

## 25. Parent P5 still owns ActiveAsync PASS

This child source capability does not automatically make:

`active_async_enabled=true`

or:

`per_wave_exact_wait_retired=true`.

The parent P5 receipt still requires all of its evidence-driven gates, including:

- ActiveAsync qualification mode;
- more than one real active Wave;
- peak in-flight > 1;
- async completion count equals real SubmissionEpoch count;
- semantic retirement count equals ActiveAsync Wave count;
- active-path exact-wait count = 0;
- duplicate-completion rejection evidence;
- zero orphan submissions;
- zero premature retirement;
- final in-flight count = 0.

## 26. Current production cutover boundary

This bake materializes the backend pending submission/collection ABI and capability. The existing production streaming loop is not silently rewritten to claim a physically qualified multi-Wave pipeline without a release compile/GPU campaign.

If the current ordinary production path continues using the legacy synchronous executor while P5 ActiveAsync is requested, the parent P5 exact-wait gate prevents a false PASS.

The next physical materialization/campaign must explicitly cut the streaming loop over to a bounded pending-Wave queue.

## 27. No orphan submission

Once a pending submit succeeds, some caller/runtime authority must retain the pending handle until terminal collection/failure/drain handling.

Dropping a nonterminal handle emits a hard diagnostic and is not interpreted as successful retirement.

## 28. Exactly-once resource collection

The resource bundle is stored behind single owned pending state and is taken on collection.

A second collection attempt fails with:

`E_MCU_PENDING_R1_DOUBLE_COLLECT`.

## 29. Failure after submit

If a real Queue submission exists, later logical failure may not claim that the GPU work never existed.

Map failure, collection failure, or registration failure must enter fail-closed drain/recovery handling in the parent P5 integration.

## 30. No cancellation-based reuse

Logical cancellation is not physical completion and does not retire the exact P4 lease.

## 31. Drain requirement

Before Device/Queue/runtime teardown, future parent integration must ensure:

- no nonterminal pending Local Muon handles;
- P5 in-flight count = 0;
- P4 active lease count = 0.

A global shutdown drain may block. That does not restore an ordinary per-Wave exact wait in the ActiveAsync hot path.

## 32. Structural static validator

Validator:

`tools/validate_ash_basetrain_unified_atlas_mcu_local_muon_pending_submission_handle_later_collect_r1_static.py`.

It proves at minimum:

- source capability is true;
- pending handle and identity exist;
- exact `TrackedSubmission` is owned;
- exact map tickets are owned;
- three pending submit APIs exist;
- real A01 submit occurs before pending return;
- SubmissionEpoch is returned by the pending handle;
- nonblocking collect exists;
- `submission_completed_nonblocking` is used;
- map readiness is checked;
- A01/A02/A03 release/reclaim occurs later;
- B04A physical completion occurs at collection;
- P4 asynchronous completion state exists;
- no exact-wait symbol exists in the pending module.

## 33. Parent static validator update

The parent P5 static validator now distinguishes:

- legacy synchronous backend path, where exact wait may still exist;
- the child pending submit path, where exact wait is forbidden.

It continues to reject literal P5 Active PASS fields.

## 34. Regression preservation

The child does not alter:

- R4 SoftMatrix arithmetic;
- R5 deterministic norm arithmetic;
- R6 job numerical semantics;
- R7 expert arithmetic;
- R8 router policy;
- R8A bucket mapping;
- P1/P2/P3 durable authority.

## 35. Required compile gate

A real release compile is mandatory before physical qualification because this bake introduces a new ownership-heavy Rust path involving A01/A02/A03 and WGPU resource types.

Static validation is not a compile substitute.

## 36. Required child physical campaign

After release compile, minimum child campaign is:

1. enable valid P4/P5 parents;
2. create a real P4-covered Local Muon Wave;
3. call a pending submit API;
4. obtain the real SubmissionEpoch before collection;
5. prove the pending handle survives submit stack return;
6. nonblocking poll until completion/map readiness;
7. collect exactly once;
8. prove candidate/status parity against the retained synchronous parent path;
9. prove active-path exact wait count is zero;
10. drain all pending resources.

## 37. Full parent-P5 campaign after child closure

Then perform the parent physical campaign:

1. submit real Wave A;
2. register A in P5 before collection;
3. submit independent real Wave B while A remains pending;
4. prove peak in-flight > 1;
5. process real completion epochs by identity;
6. collect ready Waves without completion-order semantic corruption;
7. release exact semantic consumers;
8. retire exact P4 lease generations;
9. exercise duplicate/stale completion fixtures;
10. drain pending/P5/P4 state to zero;
11. emit the parent P5 PASS token only if every evidence predicate passes.

## 38. Packaging policy

Implementation source ZIP excludes:

- this specification;
- all `specs/` content;
- Markdown patch notes;
- `BAKE_MANIFEST*`;
- generated P0-P5 receipts/evidence;
- generated pending-submission receipts/evidence;
- generated `current.json` and `publication_seal.json`;
- P3 transaction runtime artifacts;
- runtime qualification/telemetry/log/review artifacts.

Implementation Rust/Python source remains included.

## 39. GitHub publication policy

GitHub publication for this revision is spec-only unless implementation publication is separately requested.

## 40. PASS semantics

The child PASS means the Local Muon backend has a real source path where the physical Queue submission completes before the Rust API call completes, not after it. The call returns an owned pending Wave containing the actual SubmissionEpoch, exact P4 lease context, map identities, and exact resources required for later collection. The pending path contains no exact blocking wait. Completion can be observed nonblocking and collection can occur later without reconstructing resource identity from global state. Resource reclamation remains exactly-once and the existing candidate-output ABI is preserved.

The child PASS alone does not mean the parent P5 has physically demonstrated multiple production Waves simultaneously in flight.

## 41. Current bake state declaration

Source materialized in this bake:

- backend pending submit/collect split: `MATERIALIZED`;
- source capability: `true`;
- exact-wait symbol in pending module: `absent`;
- P4 async completion API: `MATERIALIZED`;
- child static validator: `PASS`;
- parent P5 static validator: `PASS`;
- release compile: `NOT OBSERVED IN THIS ENVIRONMENT`;
- child GPU campaign: `NOT OBSERVED IN THIS ENVIRONMENT`;
- parent P5 peak-in-flight > 1 campaign: `NOT YET CLAIMED`.

## 42. Next exact gate

Next is not a new router revision yet.

The next exact gate is:

`P5 LOCAL-MUON PRODUCTION PENDING-WAVE QUEUE CUTOVER + ACTIVE-ASYNC PHYSICAL QUALIFICATION`.

Only after that parent P5 PASS is real should R8B physical-pressure feature producers be activated.

## Center sentence

**P5 built the ledger. This child finally lets the GPU job leave the function alive. `submit()` returns the real epoch and the resources that still belong to it; `collect()` happens later. The capability is now structurally real, but ActiveAsync still earns its PASS only when production actually keeps more than one of those pending Waves alive at once.**