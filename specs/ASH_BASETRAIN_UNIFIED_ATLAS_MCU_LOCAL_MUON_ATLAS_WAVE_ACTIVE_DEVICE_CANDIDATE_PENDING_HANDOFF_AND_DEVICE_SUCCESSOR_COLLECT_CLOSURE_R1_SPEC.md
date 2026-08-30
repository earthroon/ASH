# ASH-BASETRAIN-UNIFIED-ATLAS-MCU-LOCAL-MUON-ATLAS-WAVE-ACTIVE-DEVICE-CANDIDATE-PENDING-HANDOFF-AND-DEVICE-SUCCESSOR-COLLECT-CLOSURE-R1

## B05 ActiveDeviceCandidate GPU-Resident Pending Authority / Zero Full-Candidate D2H / Exact B06 Successor Ticket / Runtime-Owned Physical Backing / C07 Compact Evidence Preservation / P4 Lease Pin / P5 Semantic Consumer Extension / Production Queue Cutover Separation

---

# 0. Revision identity

Revision:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-LOCAL-MUON-ATLAS-WAVE-ACTIVE-DEVICE-CANDIDATE-PENDING-HANDOFF-AND-DEVICE-SUCCESSOR-COLLECT-CLOSURE-R1`

Parent:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-LOCAL-MUON-PRODUCTION-PENDING-WAVE-QUEUE-CUTOVER-AND-ACTIVE-ASYNC-PHYSICAL-QUALIFICATION-CLOSURE-R1`

PASS token:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_LOCAL_MUON_ATLAS_WAVE_ACTIVE_DEVICE_CANDIDATE_PENDING_HANDOFF_AND_DEVICE_SUCCESSOR_COLLECT_CLOSURE_R1`

Static PASS:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_LOCAL_MUON_ACTIVE_DEVICE_PENDING_HANDOFF_R1_STATIC`

---

# 1. Purpose

The previous child materialized a real submit-before-wait Local Muon pending handle, but that path remained MirrorVerified bulk-readback scoped.

The production ActiveAsync mode matrix requires:

`C08 ActiveAsync -> B06 ActiveVerified + C07 ActiveCompact -> B05 ActiveDeviceCandidate`.

Therefore a generic pending handle is not enough. The Local Muon candidate must remain GPU-resident after the real Queue submission completes and must survive until the existing active device successor authority has consumed it.

This revision materializes that exact missing lifetime surface.

---

# 2. Source-derived correction: the numerical ActiveDeviceCandidate path already existed

The parent synchronous Local Muon executor already distinguishes MirrorVerified from ActiveDeviceCandidate.

For ActiveDeviceCandidate it already requires:

- candidate weight full D2H = 0;
- candidate momentum full D2H = 0;
- update full D2H = 0;
- host candidate Vec materialization count = 0.

Therefore this revision MUST NOT invent a second numerical implementation or a new epsilon/parity contract.

The work is a lifetime/ownership split around the already existing active no-bulk-readback semantics.

---

# 3. Source-derived correction: B06 is metadata commit authority, not a WGPU resource owner

`HybridOptimizerCommitCoordinator` is an optimizer-generation/commit metadata authority. It is not the correct owner for live WGPU buffer objects.

Therefore this revision does not place candidate `wgpu::Buffer` objects inside B06.

Physical backing ownership remains in a runtime-owned successor object:

`LocalMuonActiveDeviceSuccessorR1`.

B06 receives a sealed `LocalMuonDeviceSuccessorTicketR1` binding the exact same:

- source/candidate generation;
- pending Wave identity;
- P4 lease digest;
- physical allocation identities;
- real SubmissionEpoch set;
- zero-full-D2H transfer evidence.

The runtime-owned successor keeps the actual candidate buffers alive while the device consumer uses them.

This preserves one physical owner and one commit-metadata authority rather than duplicating either.

---

# 4. Center invariant

`ActiveDeviceCandidate pending authority = exact real SubmissionEpoch + exact P4 lease + live GPU candidate backing + exact B06 successor ticket`.

It is never:

`GPU candidate -> full host Vec -> re-upload -> pretend device successor`.

---

# 5. Scope

R1 is restricted to:

- Local Muon;
- B04A Atlas-wave resident execution;
- one physical batch per pending Wave;
- homogeneous/default or homogeneous R8 expert execution;
- B05 ActiveDeviceCandidate;
- B06 ActiveVerified metadata/commit authority;
- C07 ActiveCompact evidence contract;
- P4 exact Atlas lease identity;
- P5 exact SubmissionEpoch dependency identity.

R8A asynchronous multi-view remains out of scope.

---

# 6. R8A exclusion

The active pending backend exposes no R8A bucket pending API in this revision.

`r8a_async_multi_view_materialized = false` remains authoritative.

Heterogeneous R8A overlap requires its own multi-view lifetime child.

---

# 7. Source-truth capabilities

The existing generic capability remains:

`TENSORCUBE_LOCAL_MUON_ASYNC_SUBMIT_COLLECT_SPLIT_MATERIALIZED_P5_R1 = true`.

This revision changes the stricter capability to:

`TENSORCUBE_LOCAL_MUON_PRODUCTION_ACTIVE_DEVICE_PENDING_HANDOFF_MATERIALIZED_P5_R1 = true`.

A separate production streaming-loop capability remains:

`TENSORCUBE_LOCAL_MUON_PRODUCTION_PENDING_QUEUE_CUTOVER_MATERIALIZED_P5_R1 = false`.

These capabilities answer three distinct questions:

1. Can a Local Muon physical submission return before exact wait? Yes.
2. Can an ActiveDeviceCandidate remain GPU-resident and produce an exact successor? Yes, structurally after this revision.
3. Does the production streaming loop already keep multiple such Waves in flight? No, not yet.

They MUST NOT be collapsed.

---

# 8. No runtime override

The source-truth capabilities cannot be forced by environment, CLI, receipt content or qualification data.

---

# 9. Dedicated ActiveDevice pending module

Implementation module:

`crates/burn_webgpu_backend/src/base_train_tensorcube_local_muon_active_device_pending_r1.rs`.

The Active path is separated from the Mirror pending module so that full candidate readback is absent structurally rather than disabled by a fragile runtime branch.

---

# 10. Candidate-mode admission

Both Active pending submit APIs take the exact current `MuonDeviceCandidateRuntimeMode` and require:

`MuonDeviceCandidateRuntimeMode::ActiveDeviceCandidate`.

Failure:

`E_MCU_ACTIVE_DEVICE_PENDING_R1_B05_ACTIVE_DEVICE_CANDIDATE_REQUIRED`.

The exact candidate mode is decided before physical Queue submission and cannot be reinterpreted later.

---

# 11. Public submit APIs

Current child APIs:

- `submit_resident_active_device_candidate_p4_p5_pending_r1`;
- `submit_resident_active_device_candidate_with_expert_r8_p4_p5_pending_r1`.

Both converge on one active pending submission implementation.

No R8A pending API is materialized.

---

# 12. Submit-before-wait ordering

Required order:

1. validate ActiveDeviceCandidate mode;
2. validate P4 exact lease;
3. validate B04A Atlas-wave one-batch geometry;
4. prepare exact existing Local Muon dispatch;
5. allocate GPU candidate weight/momentum/update arenas;
6. allocate only compact status readback;
7. submit through real `a01_submit_with_leases`;
8. obtain real SubmissionEpoch;
9. arm compact status map request;
10. move all still-live resources into the pending object;
11. return.

No exact blocking submission wait exists in this module.

---

# 13. Exact SubmissionEpoch

The pending ActiveDeviceCandidate stores the real SubmissionEpoch emitted by the existing A01 Queue authority.

No child-private completion ordinal is introduced.

The ABI preserves a vector even though the current one-physical-batch path emits one epoch.

---

# 14. P4 lease identity

The pending object stores the exact P4:

- Atlas runtime ID;
- Atlas identity digest;
- slot index;
- lease generation;
- lease digest.

The lease remains live while the pending candidate and its semantic consumers remain live.

---

# 15. Pending state machine

`PendingActiveDeviceCandidateStateR1` contains:

- Submitted;
- PhysicalComplete;
- DeviceCandidateReady;
- SuccessorClaimed;
- Consumed;
- Failed.

A host-candidate materialization state does not exist in the Active path.

---

# 16. GPU resource ownership

`PendingLocalMuonActiveDeviceCandidateR1` owns the exact resources needed after submit, including the tracked submission, P4 identity, candidate/output arenas, compact status readback and asynchronous map state.

The object contains owned values, not stack-borrowed lifetime extensions.

---

# 17. No full candidate readback allocation

The Active pending module does not allocate readback surfaces for:

- candidate weight;
- candidate momentum;
- orthogonal update.

It allocates only the compact status readback required by the current execution/status contract.

---

# 18. Mandatory transfer evidence

`ActiveDevicePendingTransferEvidenceR1` records:

- candidate weight full D2H bytes;
- candidate momentum full D2H bytes;
- update full D2H bytes;
- compact evidence D2H bytes;
- candidate weight D2D bytes;
- candidate momentum D2D bytes;
- update D2D bytes;
- host full-candidate materialization count;
- active pending exact-wait count;
- evidence digest.

For this R1 path the first three values, host materialization count and exact-wait count must be zero.

---

# 19. Compact readback exception

Compact status readback is allowed.

It is not candidate authority and cannot contain the full numerical candidate payload under another name.

---

# 20. Nonblocking physical collection

`try_collect_active_device_successor_p5_r1` performs nonblocking device progress/completion observation.

If the real tracked submission is not complete it returns `Ok(None)`.

If compact status mapping is not ready it returns `Ok(None)`.

It does not call `a01_wait_for_submission_exact`.

---

# 21. Physical completion

Once the exact SubmissionEpoch is complete and compact status is ready, the collector validates the existing Local Muon status contract.

The collector may reclaim transient input/status/readback resources that are no longer needed.

It MUST NOT reclaim the candidate weight, candidate momentum or update arenas at this point.

---

# 22. GPU-resident successor object

The collector returns:

`LocalMuonActiveDeviceSuccessorR1`.

It owns/pins:

- candidate weight arena and buffer;
- candidate momentum arena and buffer;
- orthogonal-update arena and buffer;
- exact real SubmissionEpoch set;
- exact P4 lease context;
- exact device-candidate partition backing;
- compact status result;
- zero-full-D2H transfer evidence.

---

# 23. Device buffer access

`LocalMuonActiveDeviceSuccessorR1::device_buffers()` provides exact runtime access to the live candidate weight/momentum/update device buffers while the successor owns them.

The downstream device consumer therefore does not need a host reconstruction or re-upload.

---

# 24. B06 successor ticket

`LocalMuonActiveDeviceSuccessorR1::claim_b06_ticket()` creates exactly one:

`LocalMuonDeviceSuccessorTicketR1`.

The ticket binds:

- patch identity;
- source generation;
- candidate generation;
- pending Wave identity digest;
- P4 lease digest;
- device candidate backing/allocation identities;
- exact real SubmissionEpoch vector;
- compact status PASS;
- transfer evidence;
- ticket digest.

---

# 25. Exact-once B06 claim

A successor ticket may be claimed once.

Duplicate claim fails with:

`E_MCU_ACTIVE_DEVICE_PENDING_R1_DUPLICATE_SUCCESSOR_CLAIM`.

Claim before physical completion/device-candidate readiness fails with:

`E_MCU_ACTIVE_DEVICE_PENDING_R1_SUCCESSOR_BEFORE_PHYSICAL_COMPLETION`.

---

# 26. B06 coordinator adoption

`HybridOptimizerCommitCoordinator` gains exact Muon successor-ticket staging.

ActiveVerified B06 requires the ticket before preparing the full active commit.

Failure when absent:

`FAIL_B06_CANDIDATE_NOT_COMPLETE:muon-device-successor-missing`.

---

# 27. Submission-set parity

B06 compares the exact deduplicated SubmissionEpoch set from the successor ticket against the existing B05 Muon device-candidate ticket.

Mismatch fails with:

`FAIL_B06_CANDIDATE_NOT_COMPLETE:muon-successor-submission-drift`.

This prevents a candidate from one physical Wave being staged as the successor of another.

---

# 28. Generation parity

B06 requires exact source and target candidate generation agreement between the existing Muon candidate ticket and the new successor ticket.

No pending layer advances model or optimizer generation.

---

# 29. Active next-step consumer correction

A source inconsistency was corrected in the ProductionMuonRuntime constructor.

`HybridOptimizerCommitCoordinator::new()` already requires an active next-step device consumer when B06 mode is ActiveVerified, but the callsite previously always passed `DeviceTrainableConsumerCapability::None`.

After this revision the callsite passes:

`DeviceTrainableConsumerCapability::DeviceSegmentedGenerationV1`

only when `HybridDeviceCommitRuntimeMode::ActiveVerified` is selected.

Off and MirrorVerified continue to pass `None`.

This preserves the existing B06/C08 mode matrix instead of weakening it.

---

# 30. B06 remains metadata authority

B06 stores the sealed successor ticket/digest, not the WGPU buffers themselves.

The live GPU backing remains owned by the runtime successor object until the downstream device consumer has used it.

This separation is intentional and prevents cloneable commit metadata from becoming a second physical resource owner.

---

# 31. Runtime ownership after B06 claim

After B06 ticket claim:

- B06 owns the commit/successor identity ticket;
- the runtime successor object still owns the physical GPU arenas/buffers;
- the downstream device consumer may access the exact buffers through the successor object;
- when that device consumer is finished, `release_after_device_consumer()` consumes the successor and reclaims the candidate arenas exactly once.

---

# 32. No double reclaim

The active collector reclaims transient input/status resources but deliberately transfers candidate arenas into the successor.

The successor's final release owns the later candidate-arena reclaim.

The old monolithic cleanup path does not also reclaim those moved arenas.

---

# 33. C07 evidence remains separate authority

The compact Local Muon status used to establish DeviceCandidateReady does not replace the existing C07 `CandidateGpuEvidenceReceipt` authority.

B06 ActiveVerified still requires the existing compact candidate-evidence binding when configured to do so.

That binding must report bulk candidate readback bytes = 0.

---

# 34. P5 consumer ABI extension

`McuWaveConsumerKindR1` gains:

- `B05DeviceCandidate`;
- `B06DeviceSuccessor`;
- `C07CompactEvidence`.

The actual future production queue must acquire/release these typed consumers according to real lifetime needs.

---

# 35. P4 retirement relationship

Candidate arena release and P4 Atlas lease retirement are distinct.

A device successor may no longer need the candidate arena while C07 or another semantic consumer still keeps the Wave alive.

P4 retirement remains governed by the parent P5 semantic-consumer closure and exact P4 generation authority.

---

# 36. No slot-only lifetime

No successor claim, completion or retirement may use Atlas slot number alone as lifetime authority.

The exact lease generation remains mandatory.

---

# 37. Production callsite staging helper

ProductionMuonRuntime exposes:

`stage_b06_local_muon_active_device_successor_r1`.

It requires the exact mode matrix:

- B05 `ActiveDeviceCandidate`;
- B06 `ActiveVerified`;
- C07 `ActiveCompact`.

Then it claims the exact successor ticket and stages that ticket into B06.

---

# 38. No mode weakening

The child does not allow:

- MirrorVerified pending candidate to be reinterpreted as ActiveDeviceCandidate;
- ActiveDeviceCandidate to use the Mirror host collector;
- B06 ActiveVerified without a segmented next-step device consumer;
- C07 bulk candidate readback in active mode.

---

# 39. Production queue separation

Although the ActiveDeviceCandidate pending handoff is now structurally materialized, the production streaming-loop cutover is intentionally not enabled in this bake.

`TENSORCUBE_LOCAL_MUON_PRODUCTION_PENDING_QUEUE_CUTOVER_MATERIALIZED_P5_R1 = false`.

Therefore the child does not silently grant the parent P5 multi-Wave PASS.

---

# 40. Production cutover fail-closed

The pending-queue cutover runtime continues to require both:

- ActiveDeviceCandidate pending handoff capability;
- production pending-queue cutover capability.

Because the second is still false, full production ActiveAsync queue admission remains blocked with:

`E_MCU_P5_PRODUCTION_PENDING_QUEUE_CUTOVER_REQUIRED`.

---

# 41. Child evidence runtime

`LocalMuonActiveDevicePendingHandoffRuntimeR1` and `LocalMuonActiveDevicePendingHandoffReceiptR1` provide the child evidence schema.

They track:

- observed Waves;
- physical completions;
- successor claims;
- compact evidence completion count;
- full candidate D2H totals;
- compact evidence D2H;
- host full-candidate materialization count;
- exact-wait count;
- negative-path counters;
- final pending ActiveDeviceCandidate count.

The source bake does not fabricate physical observations.

---

# 42. Child PASS predicate

Physical child PASS requires at minimum:

- generic pending capability true;
- ActiveDeviceCandidate pending capability true;
- observed Wave count > 0;
- physical completion count == observed Wave count;
- successor claim count == observed Wave count;
- compact evidence completion count == observed Wave count;
- candidate weight full D2H = 0;
- candidate momentum full D2H = 0;
- update full D2H = 0;
- host full-candidate materialization count = 0;
- ActiveDevice pending exact-wait count = 0;
- final pending ActiveDeviceCandidate count = 0.

This bake does not claim that physical predicate was executed.

---

# 43. Static validator

Validator:

`tools/validate_ash_basetrain_unified_atlas_mcu_local_muon_active_device_pending_handoff_r1_static.py`.

It verifies at minimum:

- dedicated active pending module/export;
- ActiveDeviceCandidate mode gate;
- real submit-before-wait API;
- real SubmissionEpoch retention;
- exact P4 lease retention;
- no full candidate readback sites in the Active module;
- no exact wait symbol in the Active module;
- compact status readback only;
- exact B06 successor ticket;
- B06 missing-ticket gate;
- exact successor SubmissionEpoch parity;
- P5 B05/B06/C07 consumer kinds;
- Active handoff capability true;
- production queue cutover capability false;
- exact ProductionMuon B05/B06/C07 staging mode checks;
- ActiveVerified B06 receives `DeviceSegmentedGenerationV1` next-step consumer;
- no R8A active pending API.

---

# 44. Regression chain

The following source/static gates must remain valid:

- this child static validator;
- production pending-queue cutover static validator;
- pending submit/later collect child static validator;
- parent P5 static validator;
- P4 exact Atlas lease static validator;
- P3 transactional commit/restart static validator;
- P2 real production Wave shadow static validator;
- P1 immutable qualification bundle static validator;
- P0 physical evidence-truth static validator;
- R6 static validator;
- R7 static validator;
- MCU control-plane static validator.

R8/R8A source validators may still terminate only at their existing specification-presence checks because implementation source ZIP policy deliberately excludes `specs/*.md`.

---

# 45. Compile boundary

A release compile is mandatory before physical qualification.

This revision introduces ownership movement across WGPU resource arenas, A01 submission leases, B05 ActiveDeviceCandidate and B06 successor metadata.

Static validation cannot substitute for the Rust borrow/type checker.

---

# 46. Physical child campaign

Minimum physical child campaign after release compile:

1. configure B05 ActiveDeviceCandidate;
2. configure B06 ActiveVerified;
3. configure C07 ActiveCompact;
4. ensure segmented next-step device consumer is admitted;
5. activate valid P4 exact lease authority;
6. submit one real homogeneous Local Muon Atlas Wave through the Active pending API;
7. receive a live pending object and real SubmissionEpoch before completion;
8. prove no full candidate readback resources were created;
9. prove no per-Wave exact wait was called;
10. observe exact nonblocking physical completion;
11. collect compact status only;
12. obtain `LocalMuonActiveDeviceSuccessorR1` with live GPU candidate buffers;
13. claim and stage the exact B06 successor ticket;
14. use the runtime-owned device buffers through the downstream device consumer contract;
15. complete the existing C07 compact evidence contract with bulk candidate readback = 0;
16. release the device successor resources exactly once;
17. close the exact P5 semantic consumers;
18. retire the exact P4 lease;
19. require zero final pending ActiveDeviceCandidate state;
20. seal the child receipt only if all physical predicates pass.

---

# 47. Negative physical fixtures

Qualification should exercise at least:

- duplicate successor claim rejection;
- wrong/stale P4 lease successor rejection where a real stale identity can be constructed safely;
- successor claim before physical completion rejection.

Negative fixtures must not change the successful production counters or reclaim a current generation.

---

# 48. No full readback for Active qualification

The Active physical campaign must not temporarily enable full candidate D2H merely to inspect the answer.

If a full numerical host comparison is needed, use the separately qualified MirrorVerified campaign as the oracle.

The Active campaign itself remains faithful to the no-bulk-readback contract.

---

# 49. No D2H/H2D masquerading as device successor

A path that copies the candidate to CPU and uploads it again is not a valid ActiveDeviceCandidate handoff even if the final buffer is on GPU.

This revision permits true retained backing and, if a later existing consumer requires it, explicit D2D transfer under exact identity.

---

# 50. Current bake state

This source bake materializes:

- dedicated ActiveDeviceCandidate pending submit path;
- real submit-before-wait return;
- exact real SubmissionEpoch retention;
- exact P4 lease retention;
- compact-status-only readback;
- zero-full-candidate-D2H transfer evidence schema;
- runtime-owned GPU successor backing;
- exact-once B06 successor ticket;
- B06 exact generation/SubmissionEpoch successor validation;
- B06 Active next-step consumer callsite correction;
- P5 B05/B06/C07 consumer ABI extension;
- Active-device handoff source capability = true;
- separate production pending-queue cutover capability = false;
- child evidence runtime/receipt;
- child static validator.

This bake does not claim:

- release compile PASS;
- RTX physical child PASS;
- production peak in-flight > 1;
- parent P5 PASS;
- `active_async_enabled=true`;
- `per_wave_exact_wait_retired=true`;
- R8A multi-view ActiveAsync.

---

# 51. Exact next gate

After one real ActiveDeviceCandidate pending Wave physically passes this child, return to the production pending-queue cutover and materialize the bounded runtime queue.

That next gate must flip only:

`TENSORCUBE_LOCAL_MUON_PRODUCTION_PENDING_QUEUE_CUTOVER_MATERIALIZED_P5_R1`

when the actual Production Muon streaming loop is wired to own multiple ActiveDevice successors.

---

# 52. Parent P5 final campaign

Then run:

`submit A -> register A -> submit B while A pending -> peak in-flight > 1 -> exact completion -> B05/B06/C07 consumer closure -> P4 retirement -> drain zero`.

Only the canonical parent P5 receipt may finally derive:

`active_async_enabled = true`

and:

`per_wave_exact_wait_retired = true`.

---

# 53. After parent P5 PASS

Only after full parent P5 physical closure should the roadmap advance to:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-PHYSICAL-PRESSURE-FEATURE-PRODUCERS-AND-ROUTER-COST-ACTIVATION-R8B`.

---

# 54. Packaging policy

The implementation source ZIP excludes:

- this specification and all `specs/` content;
- Markdown patch notes;
- `BAKE_MANIFEST*`;
- generated P0-P5 receipts/evidence;
- generated ActiveDevice pending receipts;
- generated production queue qualification artifacts;
- `current.json`;
- `publication_seal.json`;
- P3 runtime transaction artifacts;
- telemetry logs;
- validation logs;
- review artifacts.

Rust/Python implementation source remains included.

---

# 55. GitHub publication policy

GitHub publication for this revision is spec-only unless implementation publication is separately requested.

---

# 56. PASS semantics

Full revision PASS means one real production-qualified homogeneous Local Muon Wave was submitted under B05 ActiveDeviceCandidate and returned a live pending object before completion, the exact candidate weight/momentum/update GPU backing survived beyond the submit call without full host materialization, exact real SubmissionEpoch and P4 lease identities remained attached, physical completion was observed nonblockingly, only compact status/evidence was read back, one exact B06 successor ticket bound the same generations/allocations/submissions, the runtime-owned GPU backing remained available to the downstream device consumer until explicit release, B06/C07/P5 authority did not require a hidden host round-trip, resource ownership was released exactly once, and final pending state drained to zero.

The source bake alone does not claim this physical PASS.

---

# 57. PASS does not mean

This child PASS does not itself prove:

- production multi-Wave ActiveAsync;
- parent P5 physical PASS;
- R8A multi-view async;
- P2 asynchronous shadow lifetime;
- R8B pressure-aware routing;
- global MCU async ownership;
- maximum throughput;
- hardware Tensor Core E3.

---

# 58. Center sentence

> **Mirror pending은 일을 GPU 밖으로 살아서 데리고 나왔지만 답까지 CPU로 끌어냈다. 이번 child는 답도 GPU에 남긴다. pending object가 candidate weight와 momentum과 update의 실제 backing을 붙잡고, B06에는 같은 generation과 SubmissionEpoch와 allocation을 봉인한 ticket만 넘긴다. 메타데이터 권위와 물리 버퍼 owner를 섞지 않는다. 이 한 Wave가 D2H 없이 끝까지 살아남는 걸 증명한 뒤에야 production이 A와 B를 동시에 들고 있어도 된다.**