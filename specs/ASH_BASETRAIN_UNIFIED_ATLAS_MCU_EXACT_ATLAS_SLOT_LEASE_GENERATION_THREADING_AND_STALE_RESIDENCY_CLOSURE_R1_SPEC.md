# ASH-BASETRAIN-UNIFIED-ATLAS-MCU-EXACT-ATLAS-SLOT-LEASE-GENERATION-THREADING-AND-STALE-RESIDENCY-CLOSURE-R1

## Exact Local-Muon Atlas Lease Identity / R6 Residency Binding / R8-R8A Preservation / Real SubmissionEpoch Binding / Exact-Wait Completion / Same-Slot ABA Rejection / Semantic Retirement / ActiveAsync Prerequisite Closure

## 0. Revision identity

Revision:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-EXACT-ATLAS-SLOT-LEASE-GENERATION-THREADING-AND-STALE-RESIDENCY-CLOSURE-R1`

Parent:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-REAL-PRODUCTION-PARAMETER-WAVE-ACTIVE-TRANSACTIONAL-COMMIT-AND-RESTART-CLOSURE-R1`

PASS:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_EXACT_ATLAS_SLOT_LEASE_GENERATION_THREADING_AND_STALE_RESIDENCY_CLOSURE_R1`

Static PASS:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_EXACT_ATLAS_SLOT_LEASE_GENERATION_R1_STATIC`

## 1. Purpose

P3 closes durable model/optimizer generation state. P4 closes the corresponding GPU residency identity hole for the Local Muon Atlas slice.

Before P4, R6 carries an Atlas slot index but production lease generation is not an exact runtime authority. A slot number alone cannot distinguish two different residency incarnations after the same slot is retired and reused.

P4 establishes:

`Atlas residency identity = runtime Atlas identity + slot index + exact lease generation`.

That identity is issued once by the Local Muon Atlas lease authority and is threaded through R6, R8, R8A, the physical backend, the exact Queue submissions, completion observation and semantic retirement.

## 2. Source-derived physical boundary

The existing MCU control-plane `slot_generation` field is a legacy observation field. It is not adopted as the P4 Local Muon exact lease-generation SSOT.

The current B04A Local Muon path already owns bounded Atlas-wave ring geometry and transient physical candidate allocations. P4 therefore does not claim to create a new dedicated physical page allocator. It adds an exact logical lease-generation ledger over the existing Local Muon B04A Atlas-ring use and binds that ledger to the actual backend candidate backing and actual Queue submissions.

Current qualified geometry remains:

- physical page bytes: 16 MiB;
- Local Muon Atlas ring slots: 3;
- R6 maximum jobs per page: 16,384;
- R6 active scope: WITHIN_WAVE.

## 3. Core SSOT

Exactly one P4 authority issues Local Muon Atlas lease generations:

`McuExactAtlasSlotLeaseGenerationRuntimeR1`.

R6, R8, R8A, the backend, Queue submission and completion code are consumers. They must not create independent lease-generation counters.

## 4. Runtime mode

Environment:

`ASH_UNIFIED_ATLAS_MCU_EXACT_ATLAS_SLOT_LEASE_GENERATION_R1=OFF|ACTIVE|ACTIVE_EXACT_LEASE`

CLI admission:

`--admit-unified-atlas-mcu-exact-atlas-slot-lease-generation-r1`

Qualification mode:

`--qualify-unified-atlas-mcu-exact-atlas-slot-lease-generation-r1`

Qualification mode also enables:

`ASH_UNIFIED_ATLAS_MCU_EXACT_ATLAS_SLOT_LEASE_GENERATION_R1_QUALIFICATION_FIXTURES=1`.

Invalid qualification flag values fail closed with:

`E_MCU_ATLAS_LEASE_R1_QUALIFICATION_ENV_INVALID`.

## 5. Parent admission

P4 Active requires the existing R6 queue to be physically qualified for active execution. P4 does not turn a Shadow-only or unqualified R6 queue into an active residency authority.

Failure:

`E_MCU_ATLAS_LEASE_R1_R6_ACTIVE_QUALIFICATION_REQUIRED`.

## 6. Runtime Atlas identity

Each constructed P4 Local Muon Atlas lease runtime receives a nonzero runtime Atlas identity.

`UnifiedAtlasRuntimeIdentityR1` binds:

- `atlas_id`;
- Atlas geometry digest;
- runtime generation;
- full runtime identity digest.

The runtime identity is derived from process-local runtime nonce material plus geometry. A newly constructed process/runtime is therefore not semantically identical to an old runtime merely because it reuses slot 0 and lease generation 1.

This runtime identity is transient GPU-lifetime authority. It is not a model, checkpoint, P1 bundle or P3 durable-state identity.

## 7. Exact lease identity

`AtlasSlotLeaseIdentityR1` binds:

- exact runtime `atlas_id`;
- exact `atlas_identity_digest`;
- `slot_index`;
- monotonically increasing per-slot `lease_generation`;
- monotonically increasing allocation epoch;
- canonical lease digest.

For one runtime slot:

`new lease generation > previous lease generation`.

A lease generation is issued only when a new slot lease becomes resident. R6/R8/R8A/submission do not increment it.

## 8. Slot allocation and reuse

Current Local Muon selection is deterministic:

`slot = wave_ordinal % atlas_ring_slot_count`.

A slot with an active lease cannot be reused.

Failure:

`E_MCU_ATLAS_LEASE_R1_SLOT_REUSE_BEFORE_RETIREMENT`.

After exact completion and semantic retirement, reusing the same slot issues the next generation.

## 9. Lease state machine

Current P4 R1 runtime states are:

`Resident -> Submitted -> CompletionObserved -> retired/free`.

The runtime stores the last retired lease identity and the exact real submission epochs that belonged to it so qualification can exercise same-slot ABA rejection after reuse.

P4 does not activate callback-only asynchronous completion. Exact waits remain active.

## 10. R6 descriptor extension

The parent numerical/job descriptor ABI remains:

`ASH.UNIFIED.ATLAS.MCU.TENSORCUBE.JOB.DESCRIPTOR.F32.R5.R6`.

P4 adds child residency extension identity:

`ASH.MCU.R6.ATLAS-LEASE-IDENTITY.P4.R1`.

Each lease-qualified R6 descriptor carries:

- `atlas_slot_index`;
- `atlas_slot_lease_generation`;
- exact 32-byte lease digest.

R6 may not attach a guessed generation after descriptor construction. The lease exists first, then R6 seals the descriptor epoch from it.

## 11. R6 exact lease validation

Before physical execution P4 validates its current active lease and R6 independently validates that the epoch seal/descriptors carry the exact same:

- slot;
- lease generation;
- lease digest.

Stale descriptor authority fails with an exact stale-generation error and cannot be silently rebound to the slot's current lease.

## 12. R6 receipt truth

`atlas_slot_lease_generation_available=true` is no longer a fixed declaration.

It derives only from actual exact-generation-bearing R6 descriptors with zero missing-generation descriptors in the observed R6 runtime.

P4 physical PASS is still separately required before P4 may claim complete stale-residency closure.

## 13. Full descriptor manifest vs residency manifest

R6 has two distinct digest purposes after P4:

1. `descriptor_manifest_digest_r6` binds the full current execution descriptor, including mutable expert backend assignment;
2. `descriptor_residency_manifest_digest_r6` binds stable canonical job/residency identity and deliberately excludes `execution_backend_id`.

This separation is mandatory because R8 selects experts after routing. Expert assignment may change the execution backend ID, but it must not change which Atlas residency the canonical job refers to.

## 14. R8 preservation

`McuExpertAssignmentManifestR8` binds:

`r6_residency_manifest_digest`.

That digest includes exact lease identity while remaining stable across the legal R8/R8A expert-ID application step.

R8 does not own lease generation and P4 does not make lease generation a routing cost feature.

## 15. R8A preservation

R8A materialization recomputes the live R6 residency manifest from the post-expert-assignment canonical descriptors and requires exact equality with the R8 assignment's `r6_residency_manifest_digest`.

Failure:

`E_MCU_R8A_R6_RESIDENCY_MANIFEST_DRIFT`.

Thus R8A may change per-job expert backend identity but may not change the canonical Atlas residency identity underneath the assignment.

## 16. No second per-bucket residency SSOT

R8A packed descriptor indices continue to reference canonical R6 descriptors. P4 does not create a copied per-expert numerical payload or a second per-bucket lease table.

The exact R6 residency identity remains the source of truth.

## 17. Backend lease context

The physical Local Muon backend receives an optional typed:

`TensorCubeLocalMuonAtlasLeaseContextR1`.

It binds:

- runtime Atlas ID;
- runtime Atlas identity digest;
- exact slot;
- exact lease generation;
- exact lease digest.

P4-specific resident execution APIs pass this context through homogeneous/default and R8A indexed physical execution.

## 18. Backend backing identity

When P4 lease context is present, the backend must not recompute a semantic slot solely from `batch_index % ring_slots`.

The candidate backing identity embeds the exact supplied P4 Atlas/slot/generation/digest context.

The old batch-index-derived backing name remains only as legacy behavior when P4 context is absent.

## 19. Backend return evidence

`TensorCubeLocalMuonBatchCandidateOutput` returns:

- every real `queue_submission_epoch` generated by the physical backend;
- the exact P4 Atlas lease context consumed by that backend execution.

The production callsite requires the returned lease context to equal the originally acquired P4 lease before submission evidence can be admitted.

Failures:

- `E_MCU_ATLAS_LEASE_R1_BACKEND_CONTEXT_MISSING`;
- `E_MCU_ATLAS_LEASE_R1_BACKEND_CONTEXT_MISMATCH`.

## 20. Real SubmissionEpoch binding

P4 does not create a qualification-only Queue counter.

Every recorded submission identity originates from the existing `a01_submit_with_leases` path and its real `SubmissionEpoch`.

P4 binds one lease to the exact ordered vector of real submission epochs actually returned by the backend.

Submission epochs must remain on one exact Device/Queue identity and increase monotonically within the bound vector.

## 21. Exact wait preservation

The existing backend exact wait remains authoritative in P4 R1.

After physical output returns, P4 requires:

`exact_wait_count == bound SubmissionEpoch count`.

Only then does the lease transition from `Submitted` to `CompletionObserved`.

P4 does not claim `per_wave_exact_wait_retired=true`.

## 22. Semantic retirement

Queue completion alone does not free a lease.

P4 retirement additionally requires:

`remaining_consumer_count == 0`.

Current Local Muon P4 callsite retires only after canonical P2/R6/R8A completion/evidence processing and output accounting have finished for that Wave.

Early retirement is rejected and counted.

## 23. No historical-receipt lifetime

A receipt containing a lease digest does not keep GPU residency alive. Only actual live semantic consumers participate in retirement.

## 24. Same-slot ABA qualification

Qualification mode must observe actual slot reuse.

When a retired lease A is followed by current lease B on the same slot, P4 automatically exercises four negative checks against the production lease handlers:

1. stale A descriptor identity;
2. stale A submission binding;
3. late A completion;
4. stale A reclamation.

The stale A completion/reclamation fixtures use the exact real `SubmissionEpoch` vector captured from A's earlier physical execution.

## 25. ABA safety predicate

For current B:

`slot(A) == slot(B)` is deliberately insufficient.

Required mismatch:

`lease_generation(A) != lease_generation(B)`.

Every stale A operation must reject while B remains the active current lease unchanged.

## 26. Negative fixture failure classes

Required errors include:

- `E_MCU_ATLAS_LEASE_R1_STALE_DESCRIPTOR_GENERATION`;
- `E_MCU_ATLAS_LEASE_R1_STALE_SUBMISSION_GENERATION`;
- `E_MCU_ATLAS_LEASE_R1_STALE_COMPLETION_GENERATION`;
- `E_MCU_ATLAS_LEASE_R1_STALE_RECLAMATION_GENERATION`.

A wrong generic failure does not qualify the negative fixture.

## 27. Qualification fixture authority

Negative ABA fixtures are enabled only by explicit qualification mode.

Normal `--admit...` mode enforces exact lease identity but does not inject stale operations into an ordinary production run.

## 28. Closure receipt

`McuExactAtlasLeaseGenerationClosureReceiptR1` binds at minimum:

- exact runtime Atlas identity digest;
- whether qualification fixtures were explicitly enabled;
- lease allocation count;
- same-slot reuse count;
- exact SubmissionEpoch binding count;
- completion observation count;
- semantic retirement count;
- stale descriptor reject count;
- stale submission reject count;
- stale completion reject count;
- stale reclamation reject count;
- early-reclamation reject count;
- active lease count;
- R6 exact lease-generation availability;
- ActiveAsync lease-identity prerequisite closure;
- final PASS predicate and digest.

## 29. P4 PASS predicate

PASS requires all of the following in one physical qualification campaign:

- explicit qualification fixtures enabled;
- at least one real lease allocation;
- at least one real Queue submission bound to a lease;
- at least one exact completion observation;
- at least one semantic retirement;
- at least one same-slot reuse;
- at least one stale descriptor rejection;
- at least one stale submission rejection;
- at least one stale completion rejection;
- at least one stale reclamation rejection;
- zero active leases at final closure.

`active_async_lease_identity_prerequisite_closed=true` is derived from that predicate. It does not itself activate ActiveAsync.

## 30. R6 declaration after P4

For the P4-covered Local Muon slice, R6 may truthfully report exact lease-generation availability only after actual exact-generation descriptors have been admitted.

Implementing a field or static validator alone is not physical P4 qualification.

## 31. Interaction with P2

P2 real-Wave shadow replay remains a semantic consumer while its comparison needs the live Wave state. P4 must not retire the canonical lease before the comparison dependency has ended, unless P2 owns an explicitly independent copied lease/snapshot.

P4 R1 does not silently invent such a second lease.

## 32. Interaction with P3

P3 durable model-state authority and P4 runtime residency authority remain distinct SSOTs.

Once P3-required candidate state has escaped GPU residency into its authoritative durable participants and no runtime consumer remains, historical P3 metadata does not keep the P4 lease alive.

After restart, old P4 lease identities are not durable model-state dependencies.

## 33. ActiveAsync remains disabled

P4 deliberately preserves:

- current exact Queue waits;
- current one-Wave R8A physical execution assumptions;
- `active_async_enabled=false`;
- `per_wave_exact_wait_retired=false`.

P4 is the identity prerequisite for asynchronous completion, not the asynchronous completion revision itself.

## 34. No authority expansion

P4 does not claim:

- global MCU ownership of Gradient/AdamW/Embedding/LMHead;
- fused-pair closure;
- arbitrary multi-batch R8A;
- R8 physical-pressure cost producers;
- hardware Tensor Core E3;
- training throughput improvement;
- exact historical owner attribution for old large allocations.

## 35. Static validator

Validator:

`tools/validate_ash_basetrain_unified_atlas_mcu_exact_atlas_slot_lease_generation_r1_static.py`.

It verifies at minimum:

- P4 module and export;
- one exact allocator/runtime authority;
- fail-closed qualification flag parsing;
- exact R6 generation/digest fields;
- R6 stable residency manifest;
- R8 residency-manifest binding;
- R8A residency-manifest equality check;
- typed backend lease context;
- all real Queue SubmissionEpoch capture;
- P4 backend API adoption in the production callsite;
- exact context echo verification;
- exact completion and semantic retirement;
- same-slot ABA fixture code;
- P4 CLI admission and qualification modes.

Static PASS does not substitute for the physical GPU campaign.

## 36. Required Rust tests

Minimum unit coverage:

- same-slot reuse increments generation;
- stale descriptor rejects after reuse;
- stale submission rejects after reuse;
- late old-generation completion cannot affect the new generation;
- stale old-generation reclamation cannot free the new generation;
- runtime Atlas identity validates;
- invalid qualification flag fails closed;
- R6 stable residency digest survives expert backend-ID change while full descriptor digest changes.

## 37. Required physical qualification campaign

Minimum physical sequence:

1. run current Native-CF1-sealed release binary;
2. load valid P1 current bundle and qualified R6/R7/R8/R8A parents;
3. enable P4 qualification mode;
4. execute enough real Local Muon Waves to fill and reuse the three-slot ring;
5. observe real lease A submission and exact wait;
6. retire A through the production retirement path;
7. allocate lease B on the same slot with generation A+1;
8. execute automatic stale A descriptor/submission/completion/reclamation negative fixtures;
9. prove B remains current;
10. execute B normally;
11. complete and retire all leases;
12. require P4 closure receipt PASS.

## 38. Physical proof boundary

A campaign that never reuses a slot cannot close P4 physical qualification.

A synthetic descriptor with a manually incremented generation does not prove allocator generation authority.

A synthetic completion counter does not prove Queue binding. Submission evidence must originate from the real backend submission path.

## 39. Packaging policy

Implementation source ZIP excludes:

- this specification;
- all `specs/` content;
- Markdown patch notes;
- `BAKE_MANIFEST*`;
- generated P0/P1/P2/P3/P4 receipts and evidence;
- generated qualification bundle manifests;
- generated `current.json` and `publication_seal.json`;
- generated P3 transaction prepare/commit/restart files;
- generated P4 closure/evidence/telemetry files;
- validation logs and review artifacts.

Rust/Python implementation and validation source remain included.

## 40. GitHub publication policy

GitHub publication for this revision is spec-only unless implementation publication is separately requested.

## 41. PASS semantics

P4 PASS means the Local Muon Atlas runtime issued exact generation-bearing lease identities for real reusable Atlas-ring residency, R6 descriptors carried that identity, R8 preserved stable residency identity across expert routing, R8A verified that the post-routing descriptors still represented the exact same residency, the physical backend consumed and echoed the same lease context, every real Queue submission was bound through its actual `SubmissionEpoch`, exact wait completion was matched to the same lease, semantic retirement occurred only after the last consumer, same-slot reuse created a new generation, and stale descriptor/submission/completion/reclamation operations from the retired generation could not affect the new current lease.

P4 PASS does not mean ActiveAsync is enabled or exact waits are retired.

## 42. Next revision

Next:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-SUBMISSION-EPOCH-DEPENDENCY-TRACKING-AND-ACTIVE-ASYNC-COMPLETION-CLOSURE-R1`.

That revision may replace the present synchronous sequence:

`submit -> exact wait -> completion -> semantic retirement -> reuse`

with lease-bound asynchronous dependency tracking only after P4 proves that an old completion can never alias a new residency generation.

## Center sentence

**P3 sealed model-state generations. P4 seals GPU-residency generations. The same physical slot may be reused, but its lease identity may not be reused. R6, R8, R8A, Queue submission, completion and reclamation must all carry the exact generation so yesterday's completion can never free today's memory.**