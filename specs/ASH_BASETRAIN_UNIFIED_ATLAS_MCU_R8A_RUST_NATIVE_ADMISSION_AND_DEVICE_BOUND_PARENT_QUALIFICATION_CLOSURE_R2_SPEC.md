# ASH-BASETRAIN-UNIFIED-ATLAS-MCU-R8A-RUST-NATIVE-ADMISSION-AND-DEVICE-BOUND-PARENT-QUALIFICATION-CLOSURE-R2

## Strict typed configuration / R8 Active-parent admission / Device-bound R7 expert-manifest binding / qualification staleness closure / no external gate

### 0. Revision identity

Revision:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-R8A-RUST-NATIVE-ADMISSION-AND-DEVICE-BOUND-PARENT-QUALIFICATION-CLOSURE-R2`

Parent:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-R8A-EXISTING-RUST-EXECUTOR-OWNERSHIP-BINDING-CLOSURE-R1`

Semantic parent execution authority:

`native.optimizer.runtime.local-muon-callsite`

PASS token:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_R8A_RUST_NATIVE_ADMISSION_AND_DEVICE_BOUND_PARENT_QUALIFICATION_CLOSURE_R2`

### 1. Purpose

Phase 1 closed ownership. Phase 2 closes the question: **when does the already-existing R8A Rust authority have permission to become physically executable?**

No new runner, Core authority, Manager, Factory, Device abstraction, backend executor, or qualification generator is introduced.

### 2. Core separation

`Configured != ParentAdmitted != DeviceBound != QualificationAdmitted != ExecutionPermitted`.

These states must not collapse into `enabled=true` or `receipt.is_some()`.

### 3. Admission-state owner

Admission state belongs to the existing:

`McuGpuResidentExpertBucketAuthorityR8A`.

It remains owned by `ProductionMuonExecutionRuntime` under the existing Local Muon production callsite.

### 4. Admission state is separate from Wave/view state

Existing R8A view state remains:

`IDLE -> ASSIGNMENT_BOUND -> COVERAGE_VALIDATED -> EXECUTION_PREPARED -> EXECUTING -> COMPLETED -> RETIRED`.

Phase 2 adds a separate typed admission state:

- `OFF`
- `SHADOW_ADMITTED`
- `ACTIVE_PENDING_DEVICE_BINDING`
- `ACTIVE_ADMITTED`
- `FAILED`

Wave retirement does not reset runtime admission.

### 5. Strict enable parsing

`ASH_UNIFIED_ATLAS_MCU_GPU_RESIDENT_EXPERT_BUCKET_R8A` accepts only:

True: `1`, `TRUE`, `YES`, `ON`

False: `0`, `FALSE`, `NO`, `OFF`

Unset means disabled.

Any other explicit value fails with:

`E_MCU_R8A_ENABLE_FLAG_INVALID:<value>`.

Malformed input must not silently disable R8A.

### 6. Disabled configuration coherence

When R8A is disabled, a nonempty explicit R8A mode is rejected with:

`E_MCU_R8A_MODE_WITH_FEATURE_DISABLED`.

A nonempty explicit R8A qualification receipt path is rejected with:

`E_MCU_R8A_QUALIFICATION_WITH_FEATURE_DISABLED`.

This catches stale operator environment state instead of ignoring it.

### 7. Typed R8 parent input

R8A construction consumes the already-parsed `McuExpertRouterModeR8` from the existing R8 authority.

R8A does not reread `ASH_UNIFIED_ATLAS_MCU_DETERMINISTIC_PRECISION_EXPERT_ROUTER_R8_MODE`.

R8 remains the parent mode SSOT.

### 8. Stage-A parent admission

Enabled R8A requires R8 enabled and a nonempty R8 policy digest.

Active R8A additionally requires:

`R8 mode == ACTIVE_DETERMINISTIC_ROUTER`.

Failure:

`E_MCU_R8A_R8_ACTIVE_PARENT_REQUIRED`.

This is checked at Rust authority construction instead of being postponed to Wave routing.

### 9. Shadow Stage-A result

`SHADOW_BUCKET_VIEW` produces:

`admission_state=SHADOW_ADMITTED`.

No physical R8A qualification receipt is required.

### 10. Active Stage-A result

A structurally valid Active configuration does **not** immediately become executable.

It produces:

`admission_state=ACTIVE_PENDING_DEVICE_BINDING`.

This prevents R8A from claiming Device-bound authority before the actual active wgpu Device has been observed through R7.

### 11. Qualification receipt parsing authority

R8A qualification is read entirely in Rust:

`fs::read -> serde_json -> typed receipt -> semantic validation -> digest validation`.

Read failures carry `E_MCU_R8A_QUALIFICATION_READ_FAILED:<path>` context.

JSON parse failures carry `E_MCU_R8A_QUALIFICATION_PARSE_FAILED` context.

No external JSON validator is required.

### 12. Existing qualification schema retained

Phase 2 retains:

`ash.basetrain.mcu.gpu_resident_expert_bucket_r8a.qualification.v1`.

No schema bump is required because the identities needed for Device-bound admission already exist in the receipt.

### 13. Qualification structural closure

The existing receipt validation remains and is strengthened to require:

- exact schema, patch ID, and bucket ABI;
- nonzero fixture/heterogeneous fixture evidence;
- maximum nonempty bucket count in `2..=3`;
- zero indexed parity divergence;
- zero duplicate/missing/expert-mismatch/out-of-range counts;
- zero source/momentum/candidate repack bytes;
- zero additional bucket D2H;
- heterogeneous physical materialization true;
- PASS verdict;
- exact receipt digest.

### 14. Qualified expert-mask closure

Only R7 expert bits are legal:

- bit 0 = E0
- bit 1 = E1
- bit 2 = E2

Unknown bits fail with:

`E_MCU_R8A_QUALIFICATION_UNKNOWN_EXPERT_MASK`.

E0 is mandatory:

`qualified_expert_mask & 0b001 != 0`.

Missing E0 fails with:

`E_MCU_R8A_QUALIFICATION_SAFE_E0_MISSING`.

### 15. Physical expert-mask closure

The physical mask must contain no unknown bits and must be a subset of the qualified mask.

Failures:

- `E_MCU_R8A_QUALIFICATION_UNKNOWN_PHYSICAL_EXPERT_MASK`
- `E_MCU_R8A_QUALIFICATION_EXECUTED_UNQUALIFIED_EXPERT`

Because the receipt claims heterogeneous physical materialization, the physical mask must contain at least two experts.

### 16. Three-bucket consistency

If `three_bucket_fixture_count > 0`, Phase 2 requires:

- `maximum_nonempty_bucket_count == 3`
- `physically_executed_expert_mask == 0b111`

A three-bucket claim cannot be made without physical E0/E1/E2 execution evidence.

### 17. Index-control bound

Qualification must satisfy:

`maximum_bucket_index_h2d_bytes <= 65,536`.

Failure:

`E_MCU_R8A_QUALIFICATION_INDEX_PAYLOAD_BOUND_EXCEEDED`.

### 18. R8 policy binding

Any supplied R8A qualification receipt is immediately bound to the current R8 policy digest.

Mismatch:

`E_MCU_R8A_QUALIFICATION_POLICY_DIGEST_MISMATCH`.

Absolute receipt path is not semantic authority. The validated receipt digest is retained as runtime identity.

### 19. Why R7 manifest admission is deferred

R7 expert availability is bound to the actual active Device. At initial R8A construction time, `shader_f16_enabled_on_device` has not necessarily been physically bound.

Therefore Phase 2 does not fabricate a Device-bound expert manifest during constructor Stage A.

### 20. Existing Device binding point reused

The existing Local Muon executor construction already performs:

`device.features().contains(wgpu::Features::SHADER_F16)`

then:

`R7.bind_active_device_capability(shader_f16_enabled)`.

Phase 2 reuses this exact point. No second Device probe or new Device owner is introduced.

### 21. Minimal R7 child-safe query

R7 exposes only whether active Device capability has already been physically bound:

`active_device_capability_bound_for_r8()`.

This reflects the existing `shader_f16_enabled_on_device: Option<bool>` state.

No R7 arithmetic or qualification algorithm changes.

### 22. Stage-B Device-bound admission

Immediately after R7 binds the actual Device capability, the existing R8A authority executes:

`admit_device_bound_parent(&R7)`.

This occurs at both existing Local Muon executor construction callsites.

### 23. Stage-B live authority inputs

Stage B consumes only R7-owned live identities:

- `expert_manifest_digest_for_r8()`
- `qualified_expert_mask_for_r8()`
- `active_device_capability_bound_for_r8()`

R8A does not recreate R7 manifest or qualification logic.

### 24. Device-bound safe expert invariant

Live R7 qualified mask must contain E0.

Failure:

`E_MCU_R8A_LIVE_SAFE_E0_MISSING`.

### 25. Qualification-to-live manifest binding

If a qualification receipt exists:

`qualification.r7_expert_manifest_digest == live R7 expert manifest digest`.

Mismatch:

`E_MCU_R8A_QUALIFICATION_EXPERT_MANIFEST_MISMATCH`.

This closes stale receipt reuse after Device/expert state changes.

### 26. Qualification-to-live expert-mask binding

Phase 2 requires exact equality:

`qualification.qualified_expert_mask == live R7 qualified expert mask`.

Mismatch:

`E_MCU_R8A_QUALIFICATION_EXPERT_MASK_MISMATCH`.

A newly qualified or removed expert therefore requires a matching R8A qualification receipt rather than implicit superset/subset adoption.

### 27. Stage-B completion

Only exact Device-bound agreement promotes Active R8A from:

`ACTIVE_PENDING_DEVICE_BINDING`

to:

`ACTIVE_ADMITTED`.

### 28. Idempotent same-Device admission

Repeated Stage-B admission against the same R7 expert manifest and mask is allowed.

If a later call observes a different admitted manifest or mask, fail with:

`E_MCU_R8A_DEVICE_BOUND_PARENT_DRIFT`.

R7's own `E_MCU_R7_DEVICE_CAPABILITY_DRIFT` remains the earlier authority when the physical Device capability itself changes inconsistently.

### 29. Heterogeneous delegation permission

`permits_heterogeneous_materialization()` is redefined as:

`admission_state == ACTIVE_ADMITTED`.

It no longer means `Active + qualification receipt exists`.

This is the central Phase-2 closure.

### 30. Routing callsite simplification

The late callsite check that re-tested `R8 Active` during heterogeneous delegation is removed because parent mode admission is already closed at R8A construction.

The callsite now asks only the typed R8A authority whether heterogeneous delegation is permitted.

### 31. Materialization admission gate

R8A `materialize_view()` requires:

- Shadow: `SHADOW_ADMITTED`
- Active: `ACTIVE_ADMITTED`

Active pending Device binding fails with:

`E_MCU_R8A_ACTIVE_ADMISSION_INCOMPLETE`.

### 32. Shadow Device semantics

Shadow R8A may materialize without claiming physical R8A execution authority.

If the actual Device has already been bound, any explicitly supplied R8A qualification receipt is checked against the live R7 manifest/mask.

Shadow without a qualification receipt does not invent a physical qualification requirement.

### 33. Active execution-state gates

`mark_execution_prepared`, `mark_executing`, and `observe_physical_execution` all require:

`admission_state == ACTIVE_ADMITTED`.

No Active indexed dispatch can proceed from `ACTIVE_PENDING_DEVICE_BINDING`.

### 34. No fallback

Active admission failure does not silently:

- downgrade to Shadow;
- use homogeneous R8 execution;
- change E2 to E1/E0;
- rewrite the qualification receipt.

The Rust error propagates through the existing Local Muon production callsite.

### 35. Admission lifetime vs Wave lifetime

Admission belongs to the Local Muon runtime/Device lifetime.

Bucket view state belongs to Wave lifetime.

Retiring a view does not revoke `ACTIVE_ADMITTED` for the same admitted Device/expert identity.

A future Device recreation would require re-admission; Phase 2 itself does not add Device-loss recreation.

### 36. Runtime receipt extension

The R8A child receipt now includes:

- admission revision/state;
- typed R8 parent mode and Active flag;
- R8 policy digest;
- qualification receipt presence/digest;
- R7 Device-bound flag;
- admitted R7 expert manifest digest;
- admitted R7 qualified expert mask;
- policy/manifest/mask match evidence;
- Phase-2 admission PASS token.

### 37. Receipt validation

For Active mode, the R8A Rust receipt validates only when:

- `admission_state == ACTIVE_ADMITTED`;
- R8 parent is Active;
- qualification receipt is present;
- R7 Device capability is bound;
- R8 policy binding matches;
- R7 expert manifest binding matches;
- R7 expert-mask binding matches;
- the Phase-2 admission PASS token is present.

### 38. Parent Local Muon receipt binding

`ProductionMuonCallsiteReceipt` additionally exposes:

- `r8a_admission_state`
- `r8a_rust_native_admission_r2_pass_token`

alongside the existing R8A child receipt digest and Phase-1 ownership token.

The parent binds the child admission evidence; it does not duplicate R8A's full admission graph.

### 39. Existing physical execution authority preserved

Phase 2 does not modify:

- `TensorCubeLocalMuonBatchExecutor`
- indexed WGSL shaders
- R8A bucket partition algorithm
- R6 descriptor semantics
- R8 routing policy
- actual wgpu Device/Queue ownership

### 40. Expected implementation diff

The implementation scope is intentionally limited to:

1. `crates/base_train/src/unified_atlas_mcu_gpu_resident_expert_bucket_r8a.rs`
2. `crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs`
3. `crates/base_train/src/unified_atlas_mcu_mixed_precision_execution_expert_r7.rs`
4. Phase-2 patch note

No backend, WGSL, R6, R8, `ash_core`, or `ash_control_runtime` implementation changes are expected.

### 41. Rust-native verification authority

Authoritative verification remains:

- Cargo/rustc compile;
- Rust tests;
- Native CF1 release compile authority;
- `base_train.exe` binary identity gate;
- typed runtime receipts;
- actual Device-bound R7/R8A execution.

Python/PowerShell/Markdown are not production admission gates.

### 42. Required Rust test classes

Tests should cover:

- strict enable parsing;
- explicit disabled-mode/receipt contradictions;
- default Shadow when enabled mode is unset;
- Active R8A + Shadow R8 early rejection;
- Active receipt requirement;
- policy digest mismatch;
- expert-mask structural rules;
- Active pending Device binding;
- exact Device-bound manifest/mask admission;
- stale manifest/mask rejection;
- idempotent same-parent admission;
- pending admission cannot permit heterogeneous materialization;
- Active admitted can permit it;
- Active materialize/execute paths reject incomplete admission;
- Active receipt validation requires complete admission evidence.

### 43. PASS meaning

The Phase-2 PASS means the existing R8A authority has a complete Rust-native, fail-closed, Device-bound production admission path.

It does **not** claim new numerical qualification, improved performance, new expert arithmetic, or a new physical execution substrate.

### 44. Packaging rule

The Phase-2 specification is distributed as a separate Markdown artifact and committed separately to GitHub.

**The Phase-2 specification file must not be included in either the overlay ZIP or the full-source ZIP.**

The ZIPs contain implementation/package payload only.

### 45. Explicit non-goals

Phase 2 does not:

- create a Core authority;
- create a Rust binary;
- create Manager/Factory/Device layers;
- alter `ash_control_runtime`;
- alter R6 job identity;
- alter R8 policy math;
- alter R7 expert arithmetic;
- alter backend pipelines or WGSL;
- add retry/escalation;
- enable ActiveAsync;
- change Wave commit/readback authority;
- mutate Atlas geometry, RAM36, or Physical N2.

### 46. Handoff

After Phase 2, Phase 3 should inspect only the already-admitted physical path:

`R8 sealed assignment -> R8A exact bucket view -> existing indexed executor -> actual Device submit -> typed backend outcome -> existing Wave completion`.

No additional admission architecture should be added.

### 47. Authority declaration

Before Phase 2, R8A could have Active mode and a valid-looking qualification receipt before the actual Device-bound R7 expert authority had been compared against that receipt. Heterogeneous delegation permission was effectively `Active + receipt present`, while R8 parent mode and live expert-manifest checks were distributed later in the call chain.

After Phase 2, configuration is parsed once into typed Rust state. Active R8A requires an Active R8 parent immediately and enters only `ACTIVE_PENDING_DEVICE_BINDING`. The existing Local Muon Device binding point then produces the live R7 expert manifest and qualified mask from the actual active wgpu Device. Only exact agreement with the already Rust-validated R8A qualification receipt promotes the existing R8A authority to `ACTIVE_ADMITTED`. Only that state permits heterogeneous delegation and indexed Active execution.

### 48. Center sentence

**Phase 2 removes “a receipt exists, therefore execute.” R8A may physically delegate heterogeneous work only after the typed R8 Active parent, exact R8 policy digest, Rust-validated R8A qualification, actual Device-bound R7 expert manifest, and exact R7 qualified-expert mask all converge on one `ACTIVE_ADMITTED` state.**
