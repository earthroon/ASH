# ASH-BASETRAIN-UNIFIED-ATLAS-MCU-HOTPATH-INSTRUMENTATION-COMPRESSION-AND-SEMANTIC-FAILURE-RING-R3

## Hotpath Scope Churn Retirement / Typed Semantic Context SSOT / Fixed Failure History / Failure-Only Expansion

### 0. Revision identity

Revision:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-HOTPATH-INSTRUMENTATION-COMPRESSION-AND-SEMANTIC-FAILURE-RING-R3`

Parent:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-STEP-TRANSIENT-CARDINALITY-AND-COMPACT-STATE-CLOSURE-R2-C`

Environment gates:

- `ASH_UNIFIED_ATLAS_MCU_HOTPATH_INSTRUMENTATION_R3=1`
- `ASH_UNIFIED_ATLAS_MCU_VERBOSE_SEMANTIC_TRACE_R3=0` for intended production mode
- `ASH_UNIFIED_ATLAS_MCU_INSTRUMENTATION_MIRROR_PARITY_R3=1` only for qualification/mirror observation

Purpose: remove routine per-semantic-operation BEGIN/END console churn from the BaseTrain hotpath while preserving exact owner/role/phase attribution in typed MCU state and a fixed-size failure history ring.

### 1. Parent authority preservation

R3 preserves:

- R2-A typed allocation owner/role/domain/lifetime/phase authority and admission decisions;
- R2-B exact ParameterTransient terminal and reclamation closure;
- R2-C StepTransient compact-state/bounded-pending closure;
- 16 MiB physical Atlas page and 3-slot geometry;
- current MirrorVerified/legacy execution authority;
- current precision contract and numerical behavior;
- current exact wait/async authority.

R3 is instrumentation architecture only.

### 2. Core invariant

`Observability != print every semantic transition`.

Exact semantic execution state must exist independently of whether a console line was emitted. The production SSOT is typed MCU semantic context, not the most recent console line.

### 3. Current problem

R2-A currently emits `ALLOCATION-SCOPE-BEGIN-R2A` and `ALLOCATION-SCOPE-END-R2A` around many roles for every Muon parameter, including ParameterTileDescriptors, PackedGradient, ParameterPreSnapshot, LocalObserver, CurrentObservationProjection, bridge roles, FusionCandidateGraph, FusionPlannerSnapshot, FusionExecutionPlan, ParameterControlBinding, and FusionCalibrationReplayCapture.

These receipts are useful for forensic attribution, but normal successful execution pays formatting/output/cardinality cost for every scope transition. R3 closes that observation topology. R3 does not claim this logging is the dominant cause of the multi-minute optimizer step.

### 4. Typed semantic context

R3 introduces `McuSemanticContextR3` with fixed fields for:

- transition ordinal;
- exact R2-B step generation ID;
- exact R2-B parameter generation ID;
- parameter index;
- source/target generation and optimizer step;
- optional wave ID;
- owner;
- role;
- phase;
- domain;
- lifetime class;
- stable callsite ID.

Owner/role/phase/domain/lifetime strings are derived from the existing typed R2-A enums. R3 does not create a second free-form semantic registry.

### 5. Exact parameter binding

R3 parameter instrumentation begins only after `begin_parameter_generation_r2b` has supplied exact `parameter_generation_id` and `step_generation_id`.

A semantic transition whose parameter/generation fields disagree with the active parameter is rejected with:

`E_UNIFIED_ATLAS_MCU_SEMANTIC_CONTEXT_MISMATCH_R3`.

A stale or missing active context is rejected with:

`E_UNIFIED_ATLAS_MCU_STALE_SEMANTIC_CONTEXT_R3`.

### 6. Parent gates

When R3 is enabled, the already-qualified parent chain is required:

- R2-A allocation admission;
- R2-B generational reclamation / parameter lifetime closure;
- R2-C step transient compaction.

R3 must fail closed rather than silently run under a different lifetime/admission topology.

### 7. Context transition cost

A normal semantic scope enter/exit updates:

- fixed typed current context;
- fixed context stack;
- fixed semantic ring;
- scalar counters.

No normal transition history `Vec`, `BTreeMap`, or unbounded registry is admitted by R3.

### 8. No hotpath string ownership

Normal semantic transitions reuse static owner/role/phase/domain/lifetime/callsite identities. R3 must not allocate a new dynamic String merely to record every transition.

Failure formatting may allocate only outside the normal hotpath, but the ring itself is pre-existing fixed storage.

### 9. Fixed context stack

Nested semantic scopes are represented by a fixed context stack with versioned capacity:

`MCU_SEMANTIC_CONTEXT_STACK_CAPACITY_R3 = 16`.

Overflow is a hard failure:

`E_UNIFIED_ATLAS_MCU_SEMANTIC_CONTEXT_STACK_OVERFLOW_R3`.

R3 must not grow the stack dynamically.

### 10. Fixed semantic failure ring

R3 introduces a circular `McuSemanticFailureRingEntryR3` array with:

`MCU_SEMANTIC_FAILURE_RING_CAPACITY_R3 = 16`.

Old entries are overwritten in ring order. Successful operation never archives an unbounded history of completed semantic scopes.

### 11. Ring event classes

The typed event vocabulary includes at least:

- `EnterSemanticRole`;
- `ExitSemanticRole`;
- `AllocationRequest` / `AllocationAdmission` vocabulary;
- `AllocationReject`;
- `LargeAllocation`;
- `WaveBind`;
- `ParameterTerminal`;
- `ParameterAbort`;
- `StepTerminal`.

No arbitrary per-event text payload is required in ring storage.

### 12. Normal scope output retirement

When R3 is enabled and both verbose trace and mirror qualification are disabled:

- R2-A scope IDs may remain internal because allocation admission still uses them;
- `ALLOCATION-SCOPE-BEGIN-R2A` console output is suppressed;
- `ALLOCATION-SCOPE-END-R2A` console output is suppressed;
- exact semantic context and ring entries still advance.

Thus R2-A allocation semantics are preserved while console scope churn is retired.

### 13. Verbose trace

`ASH_UNIFIED_ATLAS_MCU_VERBOSE_SEMANTIC_TRACE_R3=1` may print R3 semantic ENTER/EXIT transitions for diagnostics.

Verbose mode is observation only and must not alter execution order, admission, lifetime, reclamation, GPU submission, or optimizer math.

### 14. Mirror qualification

`ASH_UNIFIED_ATLAS_MCU_INSTRUMENTATION_MIRROR_PARITY_R3=1` retains legacy R2-A scope console output while R3 derives its context from the exact same typed R2-A semantic values.

The migration receipt is:

`[ASH-UNIFIED-ATLAS-MCU-INSTRUMENTATION-MIRROR-PARITY-R3]`.

Because both paths consume the same typed semantic source, any owner/role/phase/callsite mismatch is a closure failure.

### 15. Large allocation visibility

R3 preserves individual visibility for allocation requests at or above the R2-A 16 MiB large-allocation threshold.

Successful large allocations emit:

`[ASH-UNIFIED-ATLAS-MCU-LARGE-ALLOCATION-R3]`.

The witness includes request ID, step/parameter generation IDs, parameter index, owner, role, phase, requested bytes, and disposition.

### 16. Allocation rejection visibility

Rejected large allocation admission emits:

`[ASH-UNIFIED-ATLAS-MCU-ALLOCATION-REJECTION-R3]`

and then expands the failure ring.

R3 does not suppress parent R2-A rejection semantics or change the admitted bound.

### 17. Raw allocator failure

If `try_reserve_exact` fails after R2-A admission, R3 attempts to dump the already-populated fixed failure ring before returning the existing structured allocation error.

The failure ring is not constructed after OOM. Its backing already exists.

### 18. Failure ring witness

Failure expansion header:

`[ASH-UNIFIED-ATLAS-MCU-SEMANTIC-FAILURE-RING-R3]`.

It includes failure class, exact current step/parameter generation identity, parameter index, ring capacity, valid entry count, and first/last transition ordinal.

Each entry is emitted oldest-to-newest via:

`[ASH-UNIFIED-ATLAS-MCU-SEMANTIC-FAILURE-RING-ENTRY-R3]`.

### 19. No root-cause inference from final context

The final ring entry identifies the immediate semantic boundary, not necessarily the upstream root cause. A failure while entering BridgeTemporalState does not prove BridgeTemporalState accumulated the exhausted memory.

The historical 1,044,033,536-byte request owner remains unproven unless exactly reproduced and attributed.

### 20. Parameter abort

R3 uses an RAII parameter instrumentation guard. If a parameter exits without successful instrumentation terminal, the guard expands the failure ring, clears the active semantic context, and emits:

`[ASH-UNIFIED-ATLAS-MCU-PARAMETER-ABORT-R3]`.

No successful R3 parameter closure is claimed for that parameter.

### 21. Wave identity

Each logical Muon wave records a compact `WaveBind` ring event and increments a scalar wave counter. R3 does not create per-wave historical containers.

Existing Muon wave/retirement receipts remain outside R3 scope and are not silently removed by this revision.

### 22. Parameter terminal summary

After R2-B parameter reclamation and R2-C parameter compaction have succeeded, R3 emits one compact:

`[ASH-UNIFIED-ATLAS-MCU-PARAMETER-TERMINAL-SUMMARY-R3]`.

It reports exact parameter/step generation identity, wave count, large allocation count, allocation rejection count, zero parameter reclamation debt, zero step compaction debt for the successful boundary, and semantic transition count.

### 23. Step terminal summary

After parent step reclamation succeeds, R3 emits:

`[ASH-UNIFIED-ATLAS-MCU-STEP-TERMINAL-SUMMARY-R3]`.

It reports total semantic transition count, normal R3 printed-event count, suppressed successful transition count, large allocation count, failure-ring dump count, and context mismatch/stale-context counts.

### 24. Instrumentation cardinality

The intended production structure is:

- active semantic context = O(1);
- context stack = O(fixed 16);
- semantic failure ring = O(fixed 16);
- parameter counters = O(1);
- step counters = O(1).

No R3 instrumentation history scales with parameter count, wave count, or TensorCube tile count.

### 25. Printed event shape

Normal R3 semantic instrumentation output scales approximately with:

`O(parameters + large allocations + failures + terminal summaries)`

instead of:

`O(parameters * semantic roles * BEGIN/END)`.

No arbitrary compression percentage is claimed until physical telemetry is observed.

### 26. No tile/subgroup/matrix logging

R3 does not introduce one console event per TensorCube tile, subgroup, lane, matrix operation, or Newton-Schulz iteration.

Future R4+ execution work inherits this rule unless an explicit diagnostic-only mode is used.

### 27. Allocation authority remains R2-A

R2-A remains the admission authority and continues to own scope IDs internally, large-request counters, bounds, and rejection decisions. R3 only changes observation/output topology and validates the semantic context against the same typed values.

### 28. R2-B preservation

R3 must preserve R2-B parameter generation, exact terminal, lease-safe reclamation, `parameter_reclamation_debt_bytes=0`, and persistent-state exclusions.

### 29. R2-C preservation

R3 must preserve R2-C compact generation audit, topology-bounded BridgeTemporal/FusionPlanner pending state, step compaction debt rules, and final step reclamation.

A parent R2-B/R2-C failure may trigger R3 failure-ring output, but R3 must not mask or repair the parent error.

### 30. Numerical and execution non-goals

R3 does not change:

- F32 numerical contract;
- Muon Newton-Schulz arithmetic;
- SerialLane0/subgroup selection;
- optimizer route;
- wave execution order;
- canonical commit order;
- MirrorVerified B05/B06 authority;
- exact waits;
- async retirement mode;
- physical Atlas page/slots;
- RAM36 authority;
- Physical N2.

### 31. No unsupported performance claim

A successful R3 receipt proves instrumentation compression, not GPU-utilization closure. Known later bottlenecks still include MirrorVerified bulk readback, per-wave exact waits, dormant ExactSubgroup32 path, unfused wave scheduling, and CPU pre-wave work.

### 32. Static validation requirements

Static validation must prove:

- R3 module/export exists;
- R3 environment/patch/pass identities exist;
- semantic context type exists;
- ring and context stack are fixed arrays of capacity 16;
- no `Vec` is used for R3 history;
- mismatch/stale-context errors exist;
- parameter RAII instrumentation guard exists;
- failure-ring expansion exists;
- large-allocation and rejection witnesses exist;
- R2-A scope printing is conditional under R3 rather than removed from parent source;
- raw `try_reserve_exact` failure invokes failure-ring expansion;
- production callsite begins R3 after R2-B exact generation identity;
- one wave bind event is recorded per logical wave;
- parameter and step terminal summaries exist;
- R2-B and R2-C finalization remain in the production path;
- 16 MiB Atlas geometry is unchanged;
- no subgroup/F16/cluster/ActiveAsync promotion is introduced by R3.

### 33. Unit-test requirements

R3 source bakes focused tests for fixed ring capacity, fixed context stack capacity, and stable event vocabulary. Additional local qualification should cover ring wrap order, stale context rejection, allocation mismatch rejection, verbose equivalence, and failure-boundary reconstruction.

These are not considered physically observed until Rust tooling runs them.

### 34. Physical qualification sequence

`R3 static -> R2-C/R2-B/R2-A/MCU/Muon static regressions -> cargo check -> focused Rust tests -> release build -> fresh Native CF1 -> fresh cross-release authority -> immutable Physical N2 -> Exact N8`.

No stale binary-derived consumer authority may be reused after R3 source changes.

### 35. Physical acceptance

A production-mode Exact N8 must show:

- `legacy_scope_console_enabled=false`;
- `verbose_semantic_trace_enabled=false`;
- semantic context mismatch count = 0;
- stale context count = 0;
- fixed ring capacity = 16;
- semantic transitions greatly exceed printed normal R3 instrumentation events;
- R2-B parameter closure remains PASS;
- R2-C compact-state closure remains PASS;
- no Atlas, RAM36, Physical N2, execution-authority, precision, or numerical change.

A synthetic failure fixture should prove that the ring reconstructs immediate semantic history without relying on the old BEGIN/END console sequence.

### 36. Final runtime receipt

Required:

`[ASH-BASETRAIN-UNIFIED-ATLAS-MCU-HOTPATH-INSTRUMENTATION-COMPRESSION-AND-SEMANTIC-FAILURE-RING-R3]`

Minimum fields:

- patch ID;
- semantic transition count;
- printed normal instrumentation event count;
- suppressed successful transition event count;
- failure ring capacity;
- failure ring dump count;
- large allocation event count;
- allocation rejection event count;
- semantic context mismatch count = 0;
- stale semantic context count = 0;
- legacy scope console enabled boolean;
- verbose semantic trace enabled boolean;
- `parameter_lifetime_closure_preserved=true`;
- `step_compact_state_closure_preserved=true`;
- `historical_1044033536_owner_claimed=false`;
- `physical_n2_mutated=false`;
- `ram36_authority_changed=false`;
- `atlas_geometry_changed=false`;
- `execution_authority_changed=false`;
- `precision_contract_changed=false`;
- `numerical_behavior_changed=false`;
- `verdict=PASS`.

Required pass token:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_HOTPATH_INSTRUMENTATION_COMPRESSION_AND_SEMANTIC_FAILURE_RING_R3`.

### 37. Explicit non-goals

R3 does not activate subgroup32, SoftMatrix16, parallel norm, F16/BF16, mixed-precision experts, Path-Integral expert routing, wave clustering, cross-layer batching, global TensorCube scheduling, active device candidate/commit authority, bulk D2H retirement, exact-wait retirement, async overlap, or checkpoint changes.

### 38. Handoff

Successful R3 establishes an instrumentation-clean performance foundation. The recommended next revision is:

`ASH-BASETRAIN-TENSORCUBE-MUON-EXACT-SUBGROUP32-DEVICE-CAPABILITY-AND-SOFTMATRIX16-ABI-R4`

R4 should establish exact subgroup capability authority and a SoftMatrix16 backend abstraction while preserving F32 semantics. Mixed precision remains a later revision so matrix-backend effects and precision effects remain separable.

### 39. Authority declaration

Before R3, semantic execution state was visible primarily through a high-cardinality stream of scope BEGIN/END console events. The events were useful, but observation and output were tightly coupled.

After R3, exact typed semantic state exists continuously inside MCU instrumentation state. A fixed circular ring retains only the immediately preceding semantic history. Normal successful scope transitions no longer require console output. Large allocations and terminal summaries remain visible, while failure expands the bounded history already present before the fault.

Observability therefore becomes state authority first and logging second.

### 40. Center sentence

**R3 does not remove observability. It removes the console from the SSOT position. During a healthy parameter the MCU quietly carries exact owner/role/phase state in fixed memory; when something breaks, only the last bounded semantic history is unfolded.**
