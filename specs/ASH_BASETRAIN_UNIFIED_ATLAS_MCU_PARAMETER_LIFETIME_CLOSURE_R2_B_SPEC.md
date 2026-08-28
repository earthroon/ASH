# ASH-BASETRAIN-UNIFIED-ATLAS-MCU-PARAMETER-LIFETIME-CLOSURE-R2-B

## Parameter Generation Authority / Exact Terminal / Lease-Safe Reclamation / No Cross-Parameter Transient Survival

### 0. Revision Identity

Revision:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-PARAMETER-LIFETIME-CLOSURE-R2-B`

Parent:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-TENSOR-LIFETIME-CLASSIFICATION-AND-GENERATIONAL-RECLAMATION-R1`

Purpose: close the exact lifetime of `ParameterTransient` state at the real semantic parameter terminal.

### 1. Scope

R2-B owns only parameter-transient classification, parameter generation identity, parameter-local allocation ownership, parameter terminal detection, parameter lease closure, parameter-local backing reclamation, cross-parameter survivor rejection, parameter reclamation debt, and the parameter terminal receipt.

R2-B does not own StepTransient final reclamation, step terminal semantics, mixed precision, Muon execution-authority promotion, wave clustering, async overlap, or bulk D2H retirement. Those remain later revisions.

### 2. Core Invariant

`ScopeReturned != ParameterTerminal != BackingReclaimed`

A function returning does not prove that the last semantic consumer completed. The last semantic consumer completing does not prove that backing capacity physically retired.

### 3. Parameter Generation SSOT

Every parameter execution transaction receives one exact `parameter_generation_id` bound to:

- `parameter_index`
- `parameter_id`
- `source_generation`
- `source_optimizer_step`
- `target_generation`
- `target_optimizer_step`
- `step_generation_id`

No parameter-local generation is inferred from container position or call order.

### 4. Required Parameter Begin Witness

`[ASH-UNIFIED-ATLAS-MCU-PARAMETER-GENERATION-BEGIN-R2B]`

Required fields:

- `parameter_generation_id`
- `step_generation_id`
- `parameter_index`
- `parameter_id`
- `source_generation`
- `source_optimizer_step`
- `target_generation`
- `target_optimizer_step`
- `lifetime_class=ParameterTransient`

### 5. ParameterTransient Definition

A state is `ParameterTransient` only when its final semantic consumer belongs to one parameter execution transaction and no later parameter requires its full payload.

Current examples include `ParameterTileDescriptors`, parameter-local `PackedGradient` views, `ParameterPreSnapshot` temporary materialization, `LocalObserver` temporary transfer state, `CurrentObservationProjection`, `BridgePairPlan`, full `BridgePairEvidence`, full parameter `BridgeTemporalObservation`, `FusionCandidateGraph`, `FusionExecutionPlan`, and temporary `ParameterControlBinding` payloads. Exact classification remains source-driven.

### 6. No Convenience Promotion

Forbidden: reclassifying a difficult-to-reclaim `ParameterTransient` object as `StepTransient` merely to retain it longer.

Forbidden: retaining a full parameter object until step end solely for diagnostics when only a digest, ordinal, summary, or compact receipt is required.

### 7. Parameter Terminal Definition

Parameter terminal occurs only when every semantic consumer for that parameter has completed. For Muon this includes, where applicable, parameter preparation, BP-DK observation, bridge evidence use, fusion planning use, all Muon wave execution, all required GPU submission completion, all required readback/evidence completion, candidate validation, candidate application/commit, Muon momentum commit, orthogonal-update retirement, and parameter-local evidence closure.

Only after these may R2-B declare `parameter_terminal=true`.

### 8. Required Parameter Terminal Witness

`[ASH-UNIFIED-ATLAS-MCU-PARAMETER-TERMINAL-R2B]`

Required fields:

- `parameter_generation_id`
- `step_generation_id`
- `parameter_index`
- `parameter_id`
- `target_generation`
- `target_optimizer_step`
- `live_lease_count_after`
- `parameter_terminal=true`

### 9. Lease-Safe Terminal

Destructive reclamation requires:

- `parameter_terminal=true`
- no live parameter GPU submission dependency
- no live parameter readback dependency
- no live parameter commit dependency
- `live_parameter_lease_count=0`

If a live lease remains, reclamation is not admitted.

### 10. No Use-After-Free Repair

R2-B must not free parameter backing merely because a logical terminal was requested while GPU or deferred consumers remain live.

Required failure vocabulary:

`E_UNIFIED_ATLAS_MCU_PARAMETER_RESET_WITH_LIVE_LEASE_R2B`

### 11. Physical Reclamation

For proven parameter-local full objects, reclamation must affect backing ownership.

Allowed mechanisms include `std::mem::take`, dropping the owning container, a parameter arena generation reset, or transfer to an explicitly bounded reusable parameter pool.

`Vec::clear`, `len = 0`, scope end, or a logical retired flag alone do not prove backing reclamation.

### 12. No Hot-Path shrink_to_fit

`shrink_to_fit` is forbidden as a normal parameter-reclamation policy because it creates allocator churn, fragmentation risk, and unnecessary latency. R2-B uses ownership retirement or bounded pooling.

### 13. Current Full-Object Reclamation Set

Current R2-B may physically retire these parameter-local full runtime collections after exact last use:

- `bp_dk_bridge_pair_evidence`
- `bp_dk_bridge_temporal_observations`
- `bp_dk_bridge_temporal_warming`
- `bp_dk_fusion_candidate_graphs`
- `bp_dk_fusion_execution_plans`

### 14. Fusion Plan Compact Identity

Full `FusionExecutionPlan` payload need not survive parameter terminal merely for audit sequencing. Preserve only the required compact identity:

`canonical_parameter_index -> plan_digest`

Required semantics:

- `full_plan_payload_reclaimed=true`
- `compact_plan_identity_preserved=true`

### 15. CurrentObservationProjection

The observed 29,556,736-byte `CurrentObservationProjection` is attributed to `owner=BpDeltaK` and `lifetime=ParameterTransient` for the observed request. R2-B must prove that backing owned by a completed parameter does not remain semantically attached to that parameter after terminal unless an explicit bounded-pool transfer is recorded.

Frequent allocation alone is not proof of leak.

### 16. BridgeTemporalState

The earlier first physical allocation failure occurred while entering `BridgeTemporalState`, but R2-B must not infer that `BridgeTemporalState` was the accumulated leak owner from failure position alone. It remains a diagnostic checkpoint.

### 17. Pre-Bridge Pressure Snapshot

Immediately before `bridge_temporal_observe_parameter`, emit:

`[ASH-UNIFIED-ATLAS-MCU-MEMORY-PRESSURE-SNAPSHOT-R2B]`

Required fields include:

- `parameter_generation_id`
- `parameter_index`
- `parameter_id`
- `parameter_transient_object_count`
- `parameter_transient_minimum_container_backing_bytes`
- `step_transient_object_count`
- `step_transient_state_entry_count`
- `compact_retained_identity_count`
- `checkpoint=before_bridge_temporal_state`
- `nested_heap_bytes_not_claimed=true` when nested heap bytes are not measured

### 18. Byte Accounting

R2-B distinguishes logical object count, exact minimum top-level container backing bytes, nested heap bytes, and allocator/process memory. R2-B never claims tracked bytes equal process RSS or Windows commit without separate evidence.

### 19. Parameter Reclamation Receipt

Required:

`[ASH-UNIFIED-ATLAS-MCU-PARAMETER-RECLAMATION-R2B]`

Minimum fields:

- `parameter_generation_id`
- `parameter_index`
- `parameter_id`
- `live_allocation_object_count_before`
- `live_allocation_object_count_after`
- `minimum_container_backing_bytes_before`
- `minimum_container_backing_bytes_after`
- `released_object_count`
- `released_minimum_container_backing_bytes`
- `retained_step_object_count`
- `retained_step_state_entry_count`
- `retained_step_minimum_container_backing_bytes`
- `compact_retained_identity_count`
- `live_lease_count_after`
- `reclamation_disposition`
- `parameter_reclamation_debt_bytes`

### 20. Parameter Reclamation Debt

`ParameterReclamationDebt` is tracked `ParameterTransient` backing whose semantic parameter terminal has passed but which still belongs to that retired parameter.

Required after every successful parameter terminal:

`parameter_reclamation_debt_bytes=0`

### 21. Mandatory Terminal State

After successful parameter reclamation:

- `ParameterTransient logical objects = 0`
- `ParameterTransient tracked backing bytes = 0`
- `ParameterTransient live leases = 0`
- `Parameter reclamation debt = 0`

The only exception is explicit transfer to a declared bounded pool, in which case ownership and retained pool bytes must be reported separately.

### 22. Bounded Pool Exception

A bounded parameter pool may retain physical capacity only if pool identity and capacity are explicit, old parameter semantic ownership is removed, old parameter lease count is zero, and a later parameter receives a new-generation lease. Pool-resident bytes are not reported as released backing bytes.

### 23. Cross-Parameter Survivor

If `ParameterTransient` state belonging to parameter N remains semantically live after parameter N terminal, R2-B fails with:

`E_UNIFIED_ATLAS_MCU_CROSS_PARAMETER_TRANSIENT_SURVIVOR_R2B`

No silent survivor is admitted.

### 24. Stale Generation Access

Parameter N+1 must not access a transient handle from parameter N.

Required failure vocabulary:

`E_UNIFIED_ATLAS_MCU_STALE_LIFETIME_GENERATION_R2B`

No silent rebinding is permitted.

### 25. Parameter Abort

If parameter execution fails before terminal, `parameter_terminal=false`. Resources provably no longer leased may be released, but a successful parameter-reclamation closure receipt must not be emitted for that generation.

Abort witness:

`[ASH-UNIFIED-ATLAS-MCU-PARAMETER-ABORT-R2B]`

### 26. Persistent State Exclusion

R2-B must not reclaim current model-weight authority, Adam M, Adam V, persistent Muon state, committed BP-DK state, step-level audit authority, or Physical N2 state.

### 27. StepTransient Exclusion

R2-B may observe retained step object/state counts but does not redefine them as parameter reclamation debt. StepTransient cardinality/compaction belongs to the next closure revision.

The existing parent generational-reclamation implementation may continue to perform its already-qualified step-terminal reclamation. This R2-B parameter closure does not broaden, reorder, or replace that parent step behavior.

### 28. StepTransient Growth Does Not Block Parameter PASS

R2-B parameter closure passes when `ParameterTransient` reclamation debt is zero even if an independent StepTransient cardinality problem remains. The two failure domains must not be conflated.

### 29. Numerical Semantics

R2-B changes memory lifetime only.

Required:

- `optimizer_math_changed=false`
- `Muon_math_changed=false`
- `parameter_order_changed=false`
- `canonical_commit_order_changed=false`
- `precision_contract_changed=false`

### 30. Atlas Geometry

Remain unchanged:

- physical page = 16 MiB
- slot count = 3

R2-B does not introduce 32 MiB logical clusters or wave coalescing.

### 31. Execution Authority

Current Mirror/legacy authority remains unchanged during R2-B. Memory-lifetime closure and GPU execution-ownership promotion are separate physical closures.

### 32. Exact Wait Preservation

Existing exact waits remain intact and may serve as terminal lease evidence. Wait retirement belongs to later MCU performance revisions.

### 33. Required Static Validation

Static validation must prove:

- parameter generation authority exists
- parameter terminal exists
- parameter reclamation receipt exists
- scope end is not reclamation
- lease count is checked before reclamation
- full parameter-local payloads use ownership/backing retirement
- compact fusion-plan identity is preserved
- persistent state remains excluded
- StepTransient remains outside parameter reclamation debt
- cross-parameter survivor and stale generation vocabularies exist
- no hot-path `shrink_to_fit`
- 16 MiB geometry remains unchanged
- async execution authority remains unchanged
- pressure snapshot carries exact `parameter_generation_id`
- final Parameter Lifetime Closure receipt exists

### 34. Required Unit Tests

At minimum preserve or add focused tests for:

- scope end does not imply reclamation
- parameter reclamation requires actual backing drop
- nonzero parameter transient backing cannot pass parameter terminal
- StepTransient is not parameter reclamation debt
- persistent classes remain distinct from transient classes

### 35. Physical Qualification Sequence

`Static validation -> cargo check -> focused unit tests -> release build -> fresh Native CF1 -> fresh cross-release authority -> immutable Physical N2 -> Exact N8`

Previously generated consumer authority must not be reused after binary changes.

### 36. Physical Acceptance Gate

For every successful completed parameter:

`PARAMETER-GENERATION-BEGIN -> execution -> PARAMETER-TERMINAL -> PARAMETER-RECLAMATION`

must appear in canonical order.

Required terminal values:

- `live_allocation_object_count_after=0`
- `minimum_container_backing_bytes_after=0`
- `live_lease_count_after=0`
- `parameter_reclamation_debt_bytes=0`

### 37. Historical Failure Preservation

The historical 1,044,033,536-byte request remains unattributed unless exactly reproduced.

Required:

`historical_1044033536_owner_claimed=false`

No owner is inferred from current parameter identity, role, or byte scale.

### 38. Parameter-99 Boundary

R2-B must preserve the already-crossed generation 7 / optimizer step 7 / parameter index 99 boundary. Regression to the former pre-wave failure is not accepted.

### 39. Parameter-98 Boundary

The previous 6,176-byte `BridgeTemporalState` allocation failure boundary must also remain crossed while all preceding completed parameters retain zero parameter reclamation debt.

### 40. Runtime PASS

R2-B runtime PASS requires:

- parameter generations observed
- parameter terminal exact
- no live lease at successful terminal
- parameter full-payload backing reclaimed
- no cross-parameter `ParameterTransient` survivor
- no stale parameter-generation access
- parameter reclamation debt zero
- persistent state untouched
- StepTransient excluded from parameter reclamation debt
- historical 1 GiB owner not fabricated
- RAM36 unchanged
- Physical N2 unchanged
- Atlas geometry unchanged
- execution authority unchanged
- precision contract unchanged
- numerical semantics unchanged

### 41. Final Receipt

Required:

`[ASH-BASETRAIN-UNIFIED-ATLAS-MCU-PARAMETER-LIFETIME-CLOSURE-R2B]`

Minimum fields:

- `patch_id=ASH-BASETRAIN-UNIFIED-ATLAS-MCU-PARAMETER-LIFETIME-CLOSURE-R2-B`
- `parameter_generation_count`
- `parameter_terminal_count`
- `parameter_abort_count`
- `parameter_reclamation_count`
- `released_parameter_object_count`
- `released_parameter_minimum_container_backing_bytes`
- `peak_parameter_transient_object_count`
- `peak_parameter_transient_minimum_container_backing_bytes`
- `cross_parameter_survivor_count=0`
- `stale_parameter_generation_access_count=0`
- `parameter_reset_with_live_lease_count=0`
- `maximum_parameter_reclamation_debt_bytes=0`
- `historical_1044033536_owner_claimed=false`
- `physical_n2_mutated=false`
- `ram36_authority_changed=false`
- `atlas_geometry_changed=false`
- `execution_authority_changed=false`
- `precision_contract_changed=false`
- `numerical_behavior_changed=false`
- `verdict=PASS`

Required pass token:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_PARAMETER_LIFETIME_CLOSURE_R2B`

### 42. Explicit Non-Goals

R2-B does not close StepTransient cardinality, implement mixed precision, implement MoE expert routing, connect the Path-Integral Synapse, activate SoftMatrix/subgroup execution, change Muon precision, cluster waves, build a global tile queue, activate GPU-side precision escalation, promote Muon or AdamW MCU execution authority, retire full D2H, retire exact waits, or change checkpoint policy.

### 43. Handoff to R2-C

Successful R2-B establishes:

`Every completed parameter leaves zero ParameterTransient reclamation debt.`

The next revision may then independently ask why StepTransient state continues growing across successfully closed parameters.

Proposed next authority:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-STEP-TRANSIENT-CARDINALITY-AND-COMPACT-STATE-CLOSURE-R2-C`

### 44. Authority Declaration

Before R2-B, parameter-local semantic objects could outlive the parameter because optimizer-generation rollover, rather than exact last consumer, acted as a practical reclamation boundary. Scope completion did not prove backing destruction, so a later allocation failure could be caused by memory retained by earlier completed parameters.

After R2-B, every `ParameterTransient` object belongs to one explicit parameter generation. A parameter becomes terminal only after all exact semantic, GPU submission, readback, commit, and lease dependencies required by that parameter have completed. At that point full parameter-local payloads are physically retired or explicitly transferred into a bounded reusable pool. No `ParameterTransient` semantic state may silently survive into the next parameter.

Successful parameter terminal therefore implies zero live parameter-transient objects, zero tracked parameter-transient backing, zero live parameter leases, and zero parameter reclamation debt.

StepTransient state remains outside this parameter-lifetime authority and is handled by the next closure revision.

### 45. Center Sentence

**R2-B proves not merely that a function returned, but that the exact last consumer of the parameter finished and the transient backing owned by that parameter actually left its semantic ownership boundary. Parameter N's temporary state must not follow Parameter N+1 as an untracked survivor.**
