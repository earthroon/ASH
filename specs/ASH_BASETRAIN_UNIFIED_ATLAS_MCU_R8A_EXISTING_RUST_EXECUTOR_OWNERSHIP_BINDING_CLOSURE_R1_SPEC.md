# ASH-BASETRAIN-UNIFIED-ATLAS-MCU-R8A-EXISTING-RUST-EXECUTOR-OWNERSHIP-BINDING-CLOSURE-R1

## Existing Local-Muon Authority Adoption / Rust-Native State Ownership / R8 Assignment-to-R8A Materialization Binding / Existing Backend Device-Queue Continuity / No New Runner / No New Core Authority

## 0. Revision identity

Revision:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-R8A-EXISTING-RUST-EXECUTOR-OWNERSHIP-BINDING-CLOSURE-R1`

Parent implementation:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-GPU-RESIDENT-EXPERT-BUCKET-VIEW-AND-HETEROGENEOUS-DISPATCH-R8A`

Semantic parent authority:

`native.optimizer.runtime.local-muon-callsite`

PASS token:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_R8A_EXISTING_RUST_EXECUTOR_OWNERSHIP_BINDING_CLOSURE_R1`

This revision is an ownership/binding closure. It does not introduce a new routing algorithm, execution expert, GPU Device owner, process entrypoint, control plane, or Core authority.

## 1. Purpose

R8A already exists in the production Rust path. This revision makes that ownership explicit and receipt-bound instead of leaving it implicit across several source files.

Required production chain:

`base_train.exe -> ProductionMuonExecutionRuntime -> R6 -> R7 -> R8 -> R8A -> existing TensorCubeLocalMuonBatchExecutor -> existing wgpu Device/Queue`.

## 2. No new Core authority

R8A remains a concrete runtime child of the existing Core authority:

`native.optimizer.runtime.local-muon-callsite`.

No `ash_core` authority registry entry is added for R8A.

Required receipt fields:

- `new_core_authority_created=false`
- `parent_execution_authority=native.optimizer.runtime.local-muon-callsite`

## 3. No new Rust binary

The production training entrypoint remains `base_train.exe` from `crates/base_train/src/bin/base_train.rs`.

R8A must not add an `r8a_runner`, launcher, native host, or standalone production process.

Required receipt field:

`new_rust_binary_created=false`.

## 4. Build authority preservation

Build authority remains Rust-native:

`ash_control_runtime -> Native CF1 Release Compile Authority -> cargo build --locked --release -> base_train.exe SHA256`.

This revision does not add a PowerShell or Python build gate.

## 5. External script authority prohibition

Required runtime declarations:

- `python_runtime_dependency=false`
- `powershell_runtime_dependency=false`
- `markdown_runtime_dependency=false`
- `patch_note_runtime_dependency=false`

Python validators, PowerShell helpers, specs, and patch notes are not production admission authorities.

## 6. Existing runtime owner

Concrete R8A state remains owned by `McuGpuResidentExpertBucketAuthorityR8A`, which is already a field of `ProductionMuonExecutionRuntime`.

The authority is not recreated per job, expert bucket, or WGSL dispatch.

## 7. R6 ownership preservation

R6 remains the SSOT for canonical job identity, descriptor storage, queue generation/epoch, TensorCube ordinal, source ranges, candidate ranges, status ranges, Wave membership, and descriptor manifest identity.

R8A stores only descriptor indices and child execution state.

## 8. R7 ownership preservation

R7 remains the SSOT for E0/E1/E2 expert definitions, numerical contracts, qualification, active Device F16 capability, and expert manifest identity.

R8A does not independently qualify an expert.

## 9. R8 ownership preservation

R8 remains the sole routing authority.

R8A consumes the sealed `McuExpertAssignmentManifestR8` and never recomputes feature vectors, costs, Path-Integral state, tie-breaks, or expert IDs.

Required receipt field:

`router_policy_recomputed=false`.

## 10. R8A ownership

R8A owns only:

- exact assignment binding;
- stable E0/E1/E2 descriptor-index partition;
- bucket-view generation and digest;
- coverage validation;
- indexed execution state;
- physical dispatch accounting;
- R8A child receipt.

## 11. Explicit state machine

R8A runtime state is typed in Rust:

- `IDLE`
- `ASSIGNMENT_BOUND`
- `COVERAGE_VALIDATED`
- `EXECUTION_PREPARED`
- `EXECUTING`
- `COMPLETED`
- `RETIRED`
- `FAILED`

The normal Active transition is:

`IDLE/RETIRED -> ASSIGNMENT_BOUND -> COVERAGE_VALIDATED -> EXECUTION_PREPARED -> EXECUTING -> COMPLETED -> RETIRED`.

Shadow materialization closes as:

`IDLE/RETIRED -> ASSIGNMENT_BOUND -> COVERAGE_VALIDATED -> RETIRED`.

## 12. View-generation binding

The authority stores the current bucket-view generation and digest. Execution preparation, execution, observation, and retirement must match both.

Required failures include:

- `E_MCU_R8A_STALE_BUCKET_VIEW_GENERATION`
- `E_MCU_R8A_STALE_BUCKET_VIEW`
- `E_MCU_R8A_PREVIOUS_VIEW_NOT_RETIRED`
- `E_MCU_R8A_STATE_NOT_COVERAGE_VALIDATED`
- `E_MCU_R8A_STATE_NOT_EXECUTION_PREPARED`
- `E_MCU_R8A_STATE_NOT_EXECUTING`
- `E_MCU_R8A_VIEW_RETIRE_STATE_INVALID`

## 13. Existing Local Muon executor reuse

R8A indexed execution remains a child path inside the already-existing `TensorCubeLocalMuonBatchExecutor`.

No `R8AStandaloneGpuExecutor` is created.

Required receipt field:

`existing_local_muon_executor_reused=true`.

## 14. Existing Device and Queue reuse

R8A does not request an adapter, create a new wgpu Device, or create an independent queue.

The indexed path receives the same Device/Queue already used by the Local Muon production execution call.

Required receipt fields:

- `existing_device_reused=true`
- `existing_queue_reused=true`

`ExistingDeviceBootstrap` remains unchanged by this revision.

## 15. Backend plan identity extension

`TensorCubeLocalMuonExpertBucketExecutionPlanR8A` carries `bucket_view_generation_id` in addition to the pre-existing bucket-view digest and descriptor-index list.

This field is control identity only. It is not a new job identity.

## 16. Execution preparation boundary

After R8A materializes and validates a view, Active mode explicitly calls `mark_execution_prepared(view_generation, view_digest)` before constructing the backend indexed execution plan.

## 17. Execution boundary

Immediately before the existing Local Muon executor receives the indexed plan, the Rust parent calls `mark_executing(view_generation, view_digest)`.

The backend does not mutate R8A state.

## 18. Physical observation boundary

After the existing backend returns a typed candidate output, R8A calls `observe_physical_execution` with the same view generation/digest plus the backend's typed dispatch/upload counters.

Successful observation moves state to `COMPLETED`.

## 19. Retirement boundary

The view is retired only after the R6 epoch completion gate has executed.

A Shadow view is retired immediately after materialization evidence because it has no indexed physical execution.

## 20. Wave completion is not optimizer commit

R8A `COMPLETED`/`RETIRED` does not mean optimizer commit readiness.

Existing generation/commit authorities remain unchanged.

## 21. Parent receipt binding

The R8A child receipt now carries a deterministic `receipt_digest`.

`ProductionMuonCallsiteReceipt` explicitly stores:

- `r8a_parent_execution_authority`
- `r8a_child_receipt_digest`
- `r8a_existing_rust_executor_ownership_binding_r1_pass_token`

This binds the child evidence back into the existing Local Muon production receipt instead of creating a parallel top-level receipt authority.

## 22. Child receipt validation

The R8A receipt validates in Rust before publication.

Validation requires the exact parent execution authority, no new Core authority/binary, no Python/PowerShell/document runtime dependency, existing executor/Device/Queue reuse, no router recomputation, canonical job/output identity preservation, parent receipt binding, and exact receipt digest.

## 23. Runtime receipt digest

The R8A runtime receipt digest is computed over the canonical serialized receipt with its `receipt_digest` field blanked.

Receipt publication occurs only after the digest is set and `validate()` succeeds.

## 24. Structural vs physical parity evidence

R8A previously exposed `indexed_execution_divergence_count=0` without distinguishing qualification evidence from a current-run comparator.

This closure separates the meanings:

- `qualification_indexed_parity_divergence_count`: imported from the validated R8A qualification receipt when present;
- `current_run_indexed_parity_observed=false`: current production execution does not claim to rerun direct-vs-indexed parity every Wave;
- `current_run_indexed_parity_divergence_count=None`: no fabricated current-run zero.

The legacy aggregate `indexed_execution_divergence_count` is populated from qualification evidence when available for compatibility.

## 25. Current-run structural evidence

Current execution may directly claim the Rust-observed values it actually owns, including:

- materialized Wave count;
- heterogeneous Wave count;
- physical heterogeneous Wave count;
- E0/E1/E2 job counts;
- index H2D bytes;
- expert dispatch count;
- queue submit count;
- bucket-view generation/digest;
- state.

## 26. Qualification-only evidence

Direct-vs-indexed numerical parity remains qualification evidence unless a future runtime comparator explicitly observes it in the current run.

This revision does not add a new parity comparator.

## 27. R8A ownership PASS semantics

The Phase-1 ownership PASS is separate from the existing R8A heterogeneous physical PASS.

Ownership binding may PASS after at least one R8A Wave is materialized under the existing Local Muon parent. In Active mode it additionally requires at least one indexed expert dispatch.

It does not imply R8A heterogeneous numerical qualification.

## 28. Existing R8A production PASS preservation

The existing R8A production PASS remains stricter:

- Active mode;
- R8A qualification receipt present;
- at least one physically heterogeneous Wave;
- maximum nonempty bucket count >= 2.

This revision does not weaken that gate.

## 29. Backward receipt deserialization

New fields in `ProductionMuonCallsiteReceipt` use serde defaults so older persisted parent receipts remain readable by the updated binary.

## 30. No Core registry change

Expected source diff in `crates/ash_core`: zero files.

`native.optimizer.runtime.local-muon-callsite` remains the semantic umbrella.

## 31. No control-runtime change

Expected source diff in `crates/ash_control_runtime`: zero files.

The control/build authority boundary remains unchanged.

## 32. No Device-bootstrap change

Expected source diff in `crates/burn_webgpu_backend/src/existing_device_bootstrap.rs`: zero.

R8A does not create a second Device ownership path.

## 33. No routing-policy change

Expected source diff in the R8 router implementation: zero for Phase 1.

R8A's existing child-delegation contract is preserved.

## 34. No R6 semantic change

Expected source diff in the R6 queue authority: zero for Phase 1.

R6 remains the descriptor SSOT.

## 35. No shader arithmetic change

Expected WGSL diff: zero files.

R8A indexed shader numerical behavior is not modified by this ownership closure.

## 36. Changed implementation files

The intended implementation diff is limited to:

1. `crates/base_train/src/unified_atlas_mcu_gpu_resident_expert_bucket_r8a.rs`
2. `crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs`
3. `crates/burn_webgpu_backend/src/base_train_tensorcube_local_muon.rs`
4. this specification
5. the Phase-1 patch note

The backend change is only the bucket-view generation identity field in the existing R8A execution plan.

## 37. Rust-native verification

Authoritative verification is expected through the existing Rust toolchain/runtime:

- Cargo/rustc compile;
- Rust unit tests;
- Native CF1 release compile authority;
- `base_train.exe` binary identity gate;
- actual Local Muon runtime receipts.

Python static validators and PowerShell wrappers are not Phase-1 authority.

## 38. Required Rust tests

The R8A module adds stable tests for:

- existing parent authority ID;
- typed state names;
- existing 64 KiB bucket-index bound;
- E0/E1/E2 stable span order.

Runtime integration tests should additionally exercise legal/illegal state transitions when the Windows Rust toolchain is available.

## 39. Reproducibility contract

Given the same binary identity, R6 descriptor manifest, R7 expert manifest, R8 policy/assignment digests, R8A qualification identity, and active Device capability, the ownership path must produce the same bucket-view generation sequence, view digest, and dispatch expert sequence independent of console timing or external scripts.

## 40. Explicit non-goals

This revision does not:

- add a new Core authority;
- add a new binary;
- add a new Manager/Factory/Device abstraction;
- modify `ash_control_runtime`;
- modify `ExistingDeviceBootstrap`;
- change R8 routing;
- change R7 expert arithmetic;
- change R6 job identity;
- change indexed WGSL arithmetic;
- add retry/escalation;
- enable ActiveAsync;
- retire Wave waits/readback;
- change Atlas geometry, RAM36, or Physical N2.

## 41. Handoff

After this ownership closure, Phase 2 should review only the existing Rust-native R8A admission path: typed mode parse, parent admission, qualification receipt validation, stale qualification rejection, and fail-closed behavior. It should not create another execution layer.

## 42. Authority declaration

Before this closure, R8A already executed in the correct Rust process and backend, but its ownership relationship was implicit across the callsite, R8A authority, and backend plan.

After this closure, the runtime receipt explicitly states `native.optimizer.runtime.local-muon-callsite` as R8A's parent, the R8A authority owns a typed view lifecycle, the backend plan carries the exact view generation, the existing Local Muon executor remains the physical executor, the existing Device/Queue remain the physical Device authority, and the parent Local Muon receipt binds the R8A child receipt digest.

No new runner or authority hierarchy is introduced.

## 43. Center sentence

R8A does not receive a new throne. The existing `native.optimizer.runtime.local-muon-callsite` remains the semantic parent, `ProductionMuonExecutionRuntime` owns the concrete R8A state, R8 decides the expert assignment, R6 owns the descriptors, and the already-existing Local Muon executor performs indexed work on the already-existing Device and Queue. Phase 1 only makes that ownership chain explicit, typed, digest-bound, and reproducible.
