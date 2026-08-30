# ASH-BASETRAIN-UNIFIED-ATLAS-MCU-SUBMISSION-EPOCH-DEPENDENCY-TRACKING-AND-ACTIVE-ASYNC-COMPLETION-CLOSURE-R1

## Exact SubmissionEpoch Dependency Ledger / P4 Lease Binding / Mirror-Verified Semantic Retirement / ActiveAsync Admission Boundary / No Fake Async / Submit-Collect Split Requirement

## 0. Revision identity

Revision:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-SUBMISSION-EPOCH-DEPENDENCY-TRACKING-AND-ACTIVE-ASYNC-COMPLETION-CLOSURE-R1`

Parent:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-EXACT-ATLAS-SLOT-LEASE-GENERATION-THREADING-AND-STALE-RESIDENCY-CLOSURE-R1`

PASS:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_SUBMISSION_EPOCH_DEPENDENCY_TRACKING_AND_ACTIVE_ASYNC_COMPLETION_CLOSURE_R1`

Static PASS:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_ACTIVE_ASYNC_COMPLETION_R1_STATIC`

## 1. Purpose

P4 establishes exact Local Muon Atlas residency identity as runtime Atlas identity + slot + lease generation and binds real Queue SubmissionEpoch values to that lease.

P5 introduces the semantic dependency authority needed before the existing exact per-Wave wait can be retired. Each real submission is indexed by its exact SubmissionEpoch and is bound to one exact P4 lease snapshot, one real production Wave identity, and an explicit typed consumer set.

The required semantic chain is:

`Queue submit -> real SubmissionEpoch -> P5 dependency ledger -> physical completion -> semantic consumer closure -> P4 lease retirement -> slot reuse`.

Physical completion is not semantic retirement, and semantic retirement is not inferred from callback order, Queue poll order, slot number, or timing.

## 2. Source-derived correction

The current Local Muon backend still performs a monolithic sequence inside one call:

`encode -> submit -> map request -> exact wait -> host/map collection -> resource reclaim -> return output`.

Therefore the current source cannot truthfully produce more than one independently submitted Local Muon Wave in flight through that API. Moving the existing exact wait to another thread would not qualify as ActiveAsync because it would preserve one blocking wait per Wave and merely hide it.

This bake therefore materializes the exact P5 dependency ledger and MirrorVerified production adoption now, but keeps physical ActiveAsync fail-closed behind the compiled source-truth capability:

`TENSORCUBE_LOCAL_MUON_ASYNC_SUBMIT_COLLECT_SPLIT_MATERIALIZED_P5_R1 = false`.

Attempting P5 ActiveAsync while this capability remains false fails with:

`E_MCU_P5_BACKEND_SUBMIT_COLLECT_SPLIT_REQUIRED`.

No P5 PASS token, `active_async_enabled=true`, or `per_wave_exact_wait_retired=true` may be emitted while the capability is false.

## 3. Existing async runtime reuse

P5 does not create a second Queue, Device, completion engine, or retirement worker universe.

It reuses the existing C08 `AsyncRetirementRuntimeMode::{Off, MirrorVerified, ActiveAsync}` authority. The P5 runtime is a semantic dependency layer around the real SubmissionEpoch and P4 lease identities produced by the existing backend.

P5 mode and C08 mode must agree:

- P5 MirrorVerified requires C08 MirrorVerified.
- P5 ActiveAsync requires C08 ActiveAsync.

## 4. Runtime mode

Environment:

`ASH_UNIFIED_ATLAS_MCU_SUBMISSION_EPOCH_DEPENDENCY_ACTIVE_ASYNC_R1=OFF|MIRROR_VERIFIED|ACTIVE_ASYNC`.

Qualification flag:

`ASH_UNIFIED_ATLAS_MCU_SUBMISSION_EPOCH_DEPENDENCY_ACTIVE_ASYNC_R1_QUALIFICATION=0|1`.

Bound:

`ASH_UNIFIED_ATLAS_MCU_SUBMISSION_EPOCH_DEPENDENCY_ACTIVE_ASYNC_R1_MAX_IN_FLIGHT_WAVES=<n>`.

Default maximum in-flight bound is 2.

## 5. CLI

Mirror adoption:

`--admit-unified-atlas-mcu-submission-epoch-dependency-mirror-r1`.

Physical ActiveAsync qualification request:

`--qualify-unified-atlas-mcu-active-async-completion-r1`.

Optional bound:

`--mcu-active-async-max-in-flight-waves <n>`.

P5 CLI requires P4 exact-lease admission in the same runtime invocation. Mirror CLI sets C08 to `MIRROR_VERIFIED`. ActiveAsync qualification sets C08 to `ACTIVE_ASYNC` and P5 qualification fixtures to enabled, but current source then fails closed at the submit-collect capability check until the backend split exists.

## 6. Core identity

`SubmissionEpochKeyR1` binds:

- device authority ID;
- Queue authority ID;
- real submission ordinal;
- semantic key digest.

The ordinal originates from the existing `a01_submit_with_leases` authority. P5 does not maintain a private submission counter.

## 7. Wave dependency entry

`McuWaveDependencyEntryR1` binds:

- Wave identity digest;
- parameter/resident tensor identity digest;
- R6 queue generation;
- exact R8 assignment identity, or the exact parent R6 execution manifest when R8 is not enabled;
- P4 lease-manifest digest;
- exact P4 lease identity;
- every real SubmissionEpoch belonging to the physical Wave;
- exact completed-submission set;
- typed semantic consumer set;
- completion state;
- entry digest.

## 8. Completion state

States:

`Submitted -> PhysicalComplete -> SemanticComplete -> Retired`.

`Failed` is a terminal failure-side state.

Direct `Submitted -> Retired` is forbidden.

## 9. Typed semantic consumers

Current consumer ABI includes:

- `CanonicalCandidate`;
- `P2ShadowComparison`;
- `R6CompletionEvidence`;
- `R8aExecutionEvidence`;
- `P3Transaction` for later exact use where transaction state physically retains residency.

Consumers are represented by typed `McuWaveConsumerTokenR1` identities. Token identity includes Wave, consumer kind, and consumer generation.

## 10. No historical receipt lifetime

Persisted receipts and digest strings are not live GPU consumers. Only actual runtime dependencies acquire consumer tokens.

## 11. MirrorVerified production adoption

In the current source, the Local Muon backend has already performed the exact wait before returning the output. P5 MirrorVerified therefore registers the exact real SubmissionEpoch vector and verifies:

`output.poll_wait_count == real SubmissionEpoch count`.

The ledger marks those exact submissions `PhysicalComplete` only after this parity check.

If the cardinality differs:

`E_MCU_P5_MIRROR_RETIREMENT_DIVERGENCE`.

MirrorVerified does not retire the P4 lease immediately. The exact Wave remains semantically live until all registered P2/R6/R8A/candidate consumers have completed.

## 12. Current production callsite ordering

For a P4-covered Local Muon Wave:

1. P4 acquires exact lease identity.
2. R6/R8/R8A preserve the exact residency identity.
3. Backend executes and returns real SubmissionEpoch values.
4. P4 binds those SubmissionEpochs and observes the current exact-wait completion.
5. P5 registers the same exact submission/lease snapshot.
6. P2 comparison, R6 completion, R8A execution evidence, and canonical candidate materialization complete.
7. P5 releases all exact typed consumers at the conservative current last-consumer boundary.
8. P5 requires `SemanticComplete`.
9. Existing P4 `retire_after_last_consumer` retires the exact generation.
10. P5 marks its Wave entry `Retired`.

Thus P5 does not steal reclamation authority from P4.

## 13. R8 identity binding

P5 records the exact R8 assignment manifest digest when R8 is active. If R8 is absent it records the exact parent R6 execution manifest identity rather than inventing a router identity.

P5 does not mutate R8 policy or route decisions.

## 14. In-flight bound

The P5 ledger enforces `max_in_flight_waves` before admitting a new dependency entry. Exceeding the bound fails with:

`E_MCU_P5_IN_FLIGHT_LIMIT_EXCEEDED`.

Under MirrorVerified current production behavior this bound normally observes one semantically live Wave at a time because the backend still waits internally.

Physical P5 PASS later requires peak in-flight > 1 under a true split backend.

## 15. Exact async completion API

The P5 ledger implements `observe_async_completion(real SubmissionEpoch)` for the future split backend.

It rejects:

- unregistered completion: `E_MCU_P5_UNKNOWN_COMPLETION_EPOCH`;
- duplicate completion: `E_MCU_P5_DUPLICATE_COMPLETION`.

Completion only updates the Wave selected by the exact SubmissionEpoch key. Completion order is never a semantic index.

## 16. Semantic completion

A Wave becomes `SemanticComplete` only when:

- every exact submission belonging to the Wave is physically complete; and
- the typed consumer set is empty.

Physical completion with live consumers remains non-retirable.

Consumer release errors include:

- `E_MCU_P5_DEPENDENCY_DOUBLE_RELEASE`;
- `E_MCU_P5_DEPENDENCY_UNKNOWN_CONSUMER`.

## 17. P4 retirement

P5 never frees an Atlas slot directly and never increments lease generation.

After P5 reaches `SemanticComplete`, the production callsite invokes the existing P4 exact-generation retirement function. Only after P4 retirement succeeds does P5 mark the dependency entry `Retired`.

Premature P5 retirement fails with:

`E_MCU_P5_PREMATURE_SEMANTIC_RETIREMENT`.

## 18. Drain

Before final P5 receipt publication, all dependency entries must be retired or terminally failed according to exact recovery semantics.

Current `assert_drained()` requires zero non-retired P5 Waves.

Failure:

`E_MCU_P5_RUNTIME_DRAIN_REQUIRED`.

A later physical ActiveAsync backend split must also drain the existing C08 tracked completion resources and P4 active leases before Device/Queue teardown.

## 19. ActiveAsync source gate

The Local Muon backend exports:

`TENSORCUBE_LOCAL_MUON_ASYNC_SUBMIT_COLLECT_SPLIT_MATERIALIZED_P5_R1`.

Current value in this bake:

`false`.

This is an explicit source-truth statement, not a feature flag the caller can override.

P5 ActiveAsync construction requires this compiled capability to be true. Until then:

`E_MCU_P5_BACKEND_SUBMIT_COLLECT_SPLIT_REQUIRED`.

## 20. Why the capability is false

The current backend still calls:

`a01_wait_for_submission_exact(device, &a01_tracked)`

inside `TensorCubeLocalMuonBatchExecutor::execute_internal` before returning candidate output.

Because the caller cannot receive a pending real submission handle before that wait, it cannot submit Wave B while Wave A remains genuinely in-flight through this production API.

P5 refuses to label this topology ActiveAsync.

## 21. Required backend materialization to flip the capability

Within this same revision, physical ActiveAsync closure requires a later code materialization that splits Local Muon execution into at least:

`prepare/encode/submit -> PendingLocalMuonWaveR1`

and

`poll/complete/collect(PendingLocalMuonWaveR1) -> TensorCubeLocalMuonBatchCandidateOutput`.

The pending handle must retain every A01/A02/A03 resource and map/completion identity required for safe later collection. It must return the real SubmissionEpoch to the P5 ledger immediately after submit, before blocking collection.

No per-Wave exact wait may remain in the ordinary ActiveAsync hot path.

## 22. No fake async

The following does not qualify:

`submit -> spawn thread -> exact wait inside thread -> callback`.

That topology still owns one blocking exact wait per Wave and only relocates it.

The static validator intentionally keeps the compiled capability false while the monolithic exact-wait path remains the only Local Muon production API.

## 23. Physical ActiveAsync requirements

After submit/collect materialization exists, P5 physical PASS requires at minimum:

- P4 physical closure already valid;
- real P1/P2/R8/R8A production authority as applicable;
- more than one real Local Muon Wave submitted;
- peak exact in-flight Wave count > 1;
- real async completion count equals real submitted SubmissionEpoch count;
- exact wait calls in ordinary ActiveAsync Wave path = 0;
- every Wave reaches SemanticComplete;
- every Wave retires through exact P4 lease retirement;
- duplicate completion rejection observed in qualification;
- no orphan submission;
- no premature retirement;
- final in-flight count = 0;
- final active P4 lease count = 0.

At least one same-slot P4 reuse must remain safe while ActiveAsync scheduling is enabled.

## 24. Out-of-order completion

Full P5 physical qualification must prove completion handling independent of FIFO assumptions. If hardware naturally returns submissions in order, the qualification harness may delay delivery/processing of one real completion observation while processing another already-completed real SubmissionEpoch first.

SubmissionEpoch identities themselves may not be fabricated.

## 25. Receipt

`McuActiveAsyncCompletionClosureReceiptR1` records:

- P5 mode;
- qualification-fixture state;
- compiled backend split capability;
- MirrorVerified Wave count;
- Mirror retirement divergence count;
- ActiveAsync Wave count;
- peak in-flight count;
- real SubmissionEpoch count;
- async completion count;
- semantic retirement count;
- ActiveAsync exact-wait count;
- duplicate/unknown completion reject counts;
- orphan submission count;
- premature retirement count;
- final in-flight count;
- `per_wave_exact_wait_retired`;
- `active_async_enabled`;
- final PASS predicate and digest.

## 26. Evidence-derived Active fields

`per_wave_exact_wait_retired` and `active_async_enabled` derive only from the complete physical ActiveAsync predicate.

They are never literal true declarations.

In this code bake the compiled backend capability is false, so both fields remain false and the receipt verdict can be `OBSERVED` in Mirror mode but not `PASS` for ActiveAsync.

## 27. Static validation

Validator:

`tools/validate_ash_basetrain_unified_atlas_mcu_submission_epoch_dependency_active_async_r1_static.py`.

It verifies:

- P5 module/export;
- real SubmissionEpoch key identity;
- typed consumer tokens;
- explicit completion-state machine;
- exact P4 lease snapshot binding;
- MirrorVerified exact-wait parity;
- unknown/duplicate completion rejection;
- consumer double-release rejection;
- semantic completion before P4 retirement;
- in-flight bound;
- drain;
- source-truth backend capability;
- no literal Active PASS fields;
- production callsite adoption;
- P5 CLI surface.

The static gate also asserts that current backend capability remains false while the monolithic exact wait is still present.

## 28. Current bake status

This bake closes:

- exact P5 dependency ABI;
- production MirrorVerified adoption;
- P4 lease + real SubmissionEpoch ledger binding;
- typed semantic-consumer lifecycle;
- conservative last-consumer retirement integration;
- duplicate/unknown completion error paths;
- bounded ledger admission;
- drain and closure receipt;
- fail-closed ActiveAsync source boundary.

This bake does **not** yet physically close:

- true submit-before-collect Local Muon API;
- peak in-flight > 1 production execution;
- zero exact-wait ActiveAsync hot path;
- out-of-order real Local Muon completion campaign;
- `active_async_enabled=true`;
- `per_wave_exact_wait_retired=true`.

Those remain mandatory before the revision PASS token can be produced.

## 29. Packaging policy

Implementation source ZIP excludes:

- this specification and `specs/`;
- Markdown patch notes;
- `BAKE_MANIFEST*`;
- generated P0-P5 receipts/evidence;
- `current.json` and `publication_seal.json` runtime artifacts;
- P3 transaction runtime artifacts;
- P4/P5 qualification artifacts;
- telemetry/log/review outputs.

Source implementing P5 schemas, validators and runtime behavior remains included.

## 30. GitHub publication policy

GitHub publication for this bake is spec-only. Implementation source remains in the downloadable bake unless separately requested for repository publication.

## 31. PASS semantics

The full revision PASS token may be emitted only after the source capability is truthfully flipped by a real submit/collect split and a physical campaign proves multiple exact Local Muon Waves simultaneously in flight, real SubmissionEpoch-keyed completion, zero ordinary per-Wave exact waits, exact semantic dependency closure, P4 generation-safe retirement, duplicate/stale completion isolation, and zero final in-flight/active-lease state.

MirrorVerified observation alone is not P5 physical PASS.

## 32. Next implementation gate inside P5

The immediate next code gate is:

`LOCAL-MUON-PENDING-SUBMISSION-HANDLE-AND-LATER-COLLECT-MATERIALIZATION`.

Only after that code exists should `TENSORCUBE_LOCAL_MUON_ASYNC_SUBMIT_COLLECT_SPLIT_MATERIALIZED_P5_R1` change from false to true.

## Center sentence

**P4 made every memory residency generation exact. This P5 bake gives every real submission an exact semantic ledger entry and proves the current synchronous retirement path against it. It deliberately does not call a hidden wait async. ActiveAsync begins only when Local Muon can return after submit and collect later. Until then, the ledger is real and the ActiveAsync PASS is not.**