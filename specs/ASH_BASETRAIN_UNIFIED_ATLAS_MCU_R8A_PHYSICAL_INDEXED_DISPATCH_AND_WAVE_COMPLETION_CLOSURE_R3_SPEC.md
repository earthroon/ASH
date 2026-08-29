# ASH-BASETRAIN-UNIFIED-ATLAS-MCU-R8A-PHYSICAL-INDEXED-DISPATCH-AND-WAVE-COMPLETION-CLOSURE-R3

## 1. Revision identity

Revision:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-R8A-PHYSICAL-INDEXED-DISPATCH-AND-WAVE-COMPLETION-CLOSURE-R3`

Parent:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-R8A-RUST-NATIVE-ADMISSION-AND-DEVICE-BOUND-PARENT-QUALIFICATION-CLOSURE-R2`

Semantic parent execution authority:

`native.optimizer.runtime.local-muon-callsite`

PASS token:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_R8A_PHYSICAL_INDEXED_DISPATCH_AND_WAVE_COMPLETION_CLOSURE_R3`

## 2. Purpose

Phase 1 closed ownership. Phase 2 closed Rust-native Device-bound admission. Phase 3 closes the already-existing physical execution chain.

The required chain is:

`R6 sealed descriptor epoch -> R8 sealed assignment -> R8A exact bucket view -> existing TensorCubeLocalMuonBatchExecutor -> existing Queue submission -> existing exact submission wait -> typed backend outcome -> R6 complete_epoch -> R8A retire`.

No new runner, Core authority, admission layer, physical executor, Device, Queue, routing policy, retry path, async overlap, or shader arithmetic is introduced.

## 3. Entry condition

Phase 3 is reachable only when R8A is already `ACTIVE_ADMITTED` under Phase 2.

Phase 3 does not reparse qualification receipts, reread R8 mode, rebind Device capability, or reconstruct the R7 expert manifest.

## 4. R6 descriptor authority preserved

R6 remains the sole SSOT for canonical job ordinal, Wave membership, TensorCube coordinates, source/momentum/candidate/status ranges, queue generation/epoch, and descriptor manifest identity.

R8A does not create a second semantic descriptor collection. The only new per-Wave control payload remains the packed `Vec<u32>` descriptor-index view.

## 5. R8 assignment authority preserved

R8 remains the sole authority for `canonical job -> selected expert`.

Phase 3 never recomputes routing costs, Path-Integral policy, features, tie-breaks, or expert selection.

The R8 assignment identity is already bound into the R8A bucket-view digest and remains transitively bound throughout physical execution.

## 6. One exact R8A bucket view per Wave

One admitted R8/R6 Wave owns one exact R8A view generation and digest.

The physical backend receives the exact view generation and digest in `TensorCubeLocalMuonExpertBucketExecutionPlanR8A`.

A second backend partition is forbidden. The existing backend consumes the R8A view rather than reconstructing expert membership.

## 7. View reuse closure

A new R8A view may be materialized only when the prior R8A state is `IDLE` or `RETIRED`.

`COMPLETED` is no longer sufficient for reuse.

This guarantees that an Active index view cannot be overwritten after GPU work completes but before the parent R6/Wave completion and retirement sequence has closed.

Failure:

`E_MCU_R8A_PREVIOUS_VIEW_NOT_RETIRED`.

## 8. Stable partition ordering

The packed index list remains deterministically ordered:

1. E0 jobs
2. E1 jobs
3. E2 jobs

Within each bucket, canonical descriptor order is preserved.

Every R6 job must appear exactly once. Duplicate, missing, out-of-range, and expert-mismatch states remain fail-closed before physical dispatch.

## 9. Index payload bound

Descriptor index width remains `u32`.

Maximum logical payload remains:

`16,384 jobs * 4 bytes = 65,536 bytes`.

For a physical backend outcome, logical index H2D bytes must equal:

`backend_total_job_count * 4`.

The control payload must remain `<= 65,536` bytes.

## 10. No numerical payload repack

Phase 3 preserves:

- `source_payload_repack_bytes = 0`
- `momentum_payload_repack_bytes = 0`
- `candidate_payload_repack_bytes = 0`
- `additional_bucket_payload_d2h_bytes = 0`

Expert buckets read the existing canonical resident source/momentum payload and write the existing descriptor-defined canonical outputs.

No expert-specific output merge pass is introduced.

## 11. Existing executor ownership

Physical R8A indexed execution remains inside the existing `TensorCubeLocalMuonBatchExecutor`.

No standalone R8A executor is created.

The existing indexed E0/E1/E2 pipelines remain children of that executor.

## 12. Existing Device and Queue ownership

Phase 3 creates no adapter, Device, or Queue.

The same active Device/Queue already bound by the Local Muon runtime and Phase-2 R7/R8A admission is used for R8A indexed work.

## 13. Existing physical Queue submission witness

The backend already submits through `buffer_submission_lease::submit_with_leases()`.

That function performs the real `queue.submit(...)` and returns a typed `SubmissionEpoch`:

- `device_id`
- `queue_id`
- `ordinal`

Phase 3 reuses this existing authority as the exact R8A physical Queue submission identity. It does not introduce a second R8A-global submission counter.

## 14. One submission per current R8A Wave

The existing R8A one-Wave physical batch constraint remains active.

For one R8A execution plan:

- command encoder count must be exactly 1;
- Queue submit count must be exactly 1;
- one exact R8A `SubmissionEpoch` must be observed.

Failures include:

- `E_MCU_R8A_MULTIPLE_QUEUE_SUBMISSIONS_PER_WAVE`
- `E_MCU_R8A_COMMAND_ENCODER_CARDINALITY_MISMATCH`
- `E_MCU_R8A_QUEUE_SUBMIT_CARDINALITY_MISMATCH`
- `E_MCU_R8A_SUBMISSION_EPOCH_MISSING`

The existing `E_MCU_R8A_ONE_WAVE_BATCH_CAPACITY_REQUIRED` limitation is preserved rather than silently splitting/repacking the Wave.

## 15. Expert dispatch cardinality

The existing backend dispatch order remains E0 -> E1 -> E2 with empty buckets skipped.

Required:

`r8a_expert_dispatch_count == r8a_nonempty_bucket_count`.

A qualifying heterogeneous Phase-3 witness requires at least two nonempty expert buckets.

## 16. Backend typed outcome identity

`TensorCubeLocalMuonBatchCandidateOutput` now carries R8A-specific physical identity/evidence:

- bucket-view generation;
- bucket-view digest;
- exact Queue `SubmissionEpoch`;
- Queue submission observed;
- backend outcome observed;
- exact submission wait observed;
- E0/E1/E2 job counts;
- nonempty bucket count;
- dispatch count;
- logical index H2D bytes;
- zero numerical repack counters.

This is typed Rust evidence, not console parsing.

## 17. Backend view identity must be exact

The backend-returned view generation and digest must exactly match the current executing R8A view.

Mismatch:

`E_MCU_R8A_BACKEND_OUTCOME_VIEW_IDENTITY_MISMATCH`.

## 18. Backend job identity must be exact

Required:

`backend_total_job_count == current R8A view job_count`.

Also:

- backend E0 count == current view E0 count;
- backend E1 count == current view E1 count;
- backend E2 count == current view E2 count;
- sum of backend expert counts == backend total count.

Failures:

- `E_MCU_R8A_BACKEND_TOTAL_JOB_COUNT_MISMATCH`
- `E_MCU_R8A_BACKEND_BUCKET_COUNT_MISMATCH`
- `E_MCU_R8A_BACKEND_NONEMPTY_BUCKET_COUNT_MISMATCH`

## 19. Actual submission vs plan materialization

`execution_plan_materialized` is not physical execution evidence.

Phase 3 requires the exact typed Queue submission epoch returned only after the real existing Queue submission call is reached.

`queue_submission_observed=true` is therefore grounded in the existing submission lease runtime rather than inferred from a planned dispatch count.

## 20. Existing exact wait preserved

The Local Muon backend already calls `wait_for_submission_exact()` for the tracked submission before returning the candidate output.

Phase 3 requires this exact wait to have been observed for the R8A execution.

Failure:

`E_MCU_R8A_EXACT_SUBMISSION_WAIT_NOT_OBSERVED`.

Phase 3 does not retire this synchronization and does not add a per-expert wait.

## 21. R8A physical execution observation

R8A may transition `EXECUTING -> COMPLETED` only after verifying:

- exact current view generation/digest;
- exact backend view generation/digest;
- exact total job count;
- exact E0/E1/E2 counts;
- exact nonempty bucket count;
- exact dispatch cardinality;
- exact logical index H2D bytes;
- one Queue submit;
- exact submission wait observed;
- exact submission epoch identity.

## 22. `COMPLETED` is not retirement authority

`COMPLETED` means the existing backend returned successfully after its exact submission wait with an exact R8A typed physical outcome.

It does not mean the index view can be reused.

## 23. Existing R6 completion authority preserved

The existing callsite then executes `McuGlobalTensorCubeJobQueueR6::complete_epoch(...)` with the backend logical tile count and existing omission/duplicate/alias counters.

Phase 3 does not replace or move this R6 completion authority.

## 24. Parent Wave completion binding

Only after existing R6 `complete_epoch()` succeeds may R8A call:

`observe_parent_wave_completion_after_r6_epoch(view_generation, view_digest)`.

This binds physical backend completion back into the exact parent R6 epoch.

## 25. Active retirement ordering

Active `retire_view()` now requires:

- state `COMPLETED`;
- physical indexed dispatch observed;
- typed backend outcome observed;
- exact Queue submission epoch present;
- parent Wave completion observed;
- R6 epoch completion observed.

Only then may the R8A view become `RETIRED`.

Failures include:

- `E_MCU_R8A_PHASE3_ACTIVE_RETIRE_BEFORE_COMPLETED`
- `E_MCU_R8A_PHASE3_BACKEND_OUTCOME_REQUIRED_BEFORE_RETIRE`
- `E_MCU_R8A_PHASE3_PARENT_WAVE_COMPLETION_REQUIRED_BEFORE_RETIRE`
- `E_MCU_R8A_PHASE3_SUBMISSION_EPOCH_REQUIRED_BEFORE_RETIRE`

## 26. No hidden fallback

Physical execution failure does not:

- rerun R8;
- change expert assignment;
- downgrade E2 to E1/E0;
- build another bucket view;
- retry a partial bucket;
- silently use homogeneous R8 execution.

Future R9 owns any retry/escalation semantics.

## 27. No ActiveAsync

The current index view remains WaveExecutionTransient and is reused only after exact retirement.

Phase 3 does not permit Wave N+1 to overwrite the index view while Wave N can still reference it.

`active_async_enabled=false` remains preserved.

## 28. Phase-3 child receipt

The existing R8A child receipt is extended rather than creating a competing Phase-3 receipt SSOT.

New evidence includes:

- physical execution chain revision;
- physical indexed dispatch observed;
- typed backend outcome observed;
- exact submission wait observed;
- Queue submission observed;
- parent Wave completion observed;
- R6 epoch completion observed;
- retire-after-completion evidence;
- total closed R8A Wave count;
- total closed heterogeneous R8A Wave count;
- last qualifying heterogeneous closed view generation/digest;
- exact existing submission epoch device/queue/ordinal;
- exact backend total/E0/E1/E2/nonempty/dispatch counts;
- exact logical index H2D bytes;
- Phase-3 PASS token.

## 29. Qualifying witness identity

The `last_closed_*` Phase-3 fields represent the most recent **qualifying heterogeneous closed Wave**, not merely the most recent R8A Wave.

A later homogeneous Wave does not erase an already-closed heterogeneous physical witness.

## 30. Phase-3 receipt validation

When the Phase-3 PASS token is present, Rust validation requires:

- `ACTIVE_ADMITTED`;
- physical indexed dispatch, backend outcome, exact wait, and Queue submission evidence;
- Wave/R6 completion and retire ordering evidence;
- at least one closed heterogeneous R8A Wave;
- last qualifying nonempty bucket count >= 2;
- dispatch count == nonempty bucket count;
- exact backend total count == E0+E1+E2;
- exact logical index bytes == total jobs * 4;
- nonempty last closed view identity;
- complete exact submission epoch identity;
- exact Phase-3 PASS token.

## 31. Parent Local Muon receipt binding

`ProductionMuonCallsiteReceipt` binds only the required Phase-3 child summary:

- `r8a_physical_indexed_dispatch_observed`;
- `r8a_wave_completion_observed`;
- `r8a_physical_dispatch_r3_pass_token`;
- existing R8A child receipt digest.

The full R8A evidence graph remains in the child receipt to preserve one SSOT.

## 32. Numerical parity remains separate

Phase 3 proves physical indexed execution and completion topology.

It does not claim that a direct-vs-indexed comparator was rerun in the current Wave. Existing qualification parity evidence remains separate from current-run physical dispatch evidence.

## 33. Existing R8A production PASS preserved

The pre-existing R8A heterogeneous production PASS semantics remain intact. Phase 3 adds the stronger requirement that a qualifying physical heterogeneous witness must close through the actual existing Queue submission, exact wait, R6 completion, and view retirement chain before the new Phase-3 token may appear.

## 34. Expected implementation diff

Implementation changes are limited to:

1. `crates/base_train/src/unified_atlas_mcu_gpu_resident_expert_bucket_r8a.rs`
2. `crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs`
3. `crates/burn_webgpu_backend/src/base_train_tensorcube_local_muon.rs`
4. Phase-3 patch note

No R6/R7/R8 semantic source, `ash_core`, `ash_control_runtime`, `ExistingDeviceBootstrap`, or WGSL changes are required.

## 35. Authoritative verification

Authoritative verification remains Rust-native:

- Cargo/rustc compilation;
- Rust tests;
- Native CF1 release compile authority;
- actual `base_train.exe` binary identity gate;
- actual Device-bound execution;
- exact typed Queue `SubmissionEpoch`;
- existing exact submission wait;
- R6 `complete_epoch()`;
- typed R8A/Local Muon receipts.

Python, PowerShell, Markdown, or console output are not production execution authorities.

## 36. Physical PASS semantics

Phase-3 PASS requires at least one actual Active heterogeneous R8A Wave with two or more nonempty expert buckets that:

1. was already `ACTIVE_ADMITTED`;
2. materialized one exact R8A view;
3. reached the existing indexed backend;
4. reached the actual existing Queue submission and obtained an exact `SubmissionEpoch`;
5. completed the existing exact submission wait;
6. returned an exact typed backend outcome;
7. passed existing R6 epoch completion;
8. retired the exact view only afterward.

## 37. Non-goals

Phase 3 does not:

- change R8 routing policy;
- change R7 expert arithmetic;
- reopen R8A admission;
- create a new executor, Device, Queue, Manager, Factory, Core authority, or binary;
- change indexed WGSL arithmetic;
- add expert retry/escalation;
- enable ActiveAsync;
- overlap Waves;
- split one logical Wave into multiple numerical payload batches;
- change Atlas geometry, RAM36, Physical N2, optimizer commit authority, or generation recovery;
- claim a performance improvement;
- claim current-run direct-vs-indexed numerical parity unless a separate comparator actually observes it.

## 38. Packaging rule

The Phase-3 specification is a separate Markdown artifact and separate GitHub spec commit.

**The Phase-3 specification file must not be included in either the overlay ZIP or full-source ZIP.**

## 39. Handoff

After Phase 3, ownership, admission, and physical execution-chain identity are closed.

The next work should be either:

- current-run numerical/parity witness strengthening, if required; or
- performance/dispatch-overhead measurement on the now-stable physical topology.

Retry/escalation remains a later R9 concern.

## 40. Center sentence

**Phase 3 proves that the exact R8 assignment became the exact R8A descriptor-index view, that this exact view reached the already-existing Local Muon executor and the real existing Queue submission identified by its typed SubmissionEpoch, that the existing exact GPU wait completed, and that the same Wave passed R6 completion before its index view was retired. `COMPLETED` is therefore no longer enough to reuse the view: only `RETIRED` after parent completion is.**
