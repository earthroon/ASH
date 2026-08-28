# ASH-BASETRAIN-UNIFIED-ATLAS-MCU-TENSOR-LIFETIME-CLASSIFICATION-AND-GENERATIONAL-RECLAMATION-R1

## 0. Revision identity

Revision:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-TENSOR-LIFETIME-CLASSIFICATION-AND-GENERATIONAL-RECLAMATION-R1`

Short name: `ASH MCU R2-B`.

Parent:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-LARGE-TRANSIENT-ALLOCATION-OWNER-AND-PREALLOCATION-ADMISSION-R1`

Admission environment:

`ASH_UNIFIED_ATLAS_MCU_GENERATIONAL_RECLAMATION_R2B=1`

Static PASS token:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_GENERATIONAL_RECLAMATION_R2B_STATIC`

Runtime PASS token:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_GENERATIONAL_RECLAMATION_R2B`

## 1. Purpose

R2-A established semantic allocation attribution and showed that lexical scope return is not sufficient evidence of physical memory lifetime.

The first R2-A physical run crossed the former generation-7 / optimizer-step-7 / parameter-99 raw `1,044,033,536`-byte failure boundary. The historical 1GB request did not reproduce and remains unattributed.

The same run later failed at parameter index 98 (`model.layers.10.mlp.up_proj.weight`) after entering the R2-A `BpDeltaK / BridgeTemporalState / ParameterTransient / PreWave` scope, when a host allocation of only `6,176` bytes failed.

The directly observed large parameter-local allocation before that failure was the repeated `BpDeltaK / CurrentObservationProjection / ParameterTransient` request of `29,556,736` bytes.

R2-B therefore establishes exact semantic terminal boundaries and physically retires proven parameter-local full-object retention instead of treating `SCOPE-END returned=true` as reclamation.

## 2. Core invariant

`ScopeReturned != BackingReclaimed`

Required lifecycle:

`allocation -> lifetime generation -> semantic consumers -> terminal -> lease closure -> reclamation -> next generation`

A function returning does not create reclamation authority.

## 3. Lifetime classes

Canonical lifetime classes:

- `ImmutablePersistent`
- `MutablePersistent`
- `WaveTransient`
- `ParameterTransient`
- `StepTransient`

No generic production lifetime named `Temporary`, `Unknown`, `Misc`, or equivalent is admitted.

## 4. Persistent-state exclusion

R2-B must not reclaim authoritative persistent state at parameter or step terminal.

The following existing authorities remain outside transient reclamation:

- `ResidentWeightPack` current weight;
- `ResidentWeightPackBuilder` successor authority;
- `RamResidentAdamMv.M`;
- `RamResidentAdamMv.V`;
- persistent TensorCube Muon momentum/state;
- existing persistent BP-DK committed temporal/planner state;
- vocab / embedding / LM-head weight authorities.

R2-B changes lifetime/retention only. It does not change numerical ownership.

Required:

- `data_plane_authority_changed=false`
- `numerical_behavior_changed=false`

## 5. WaveTransient policy

Existing bounded wave slabs / atlas slots retain their current reuse policy.

Wave transient retirement remains:

`completion -> commit -> logical retirement -> bounded backing reusable`

R2-B does not reintroduce per-wave malloc/free churn and does not use `shrink_to_fit` as a hotpath repair.

## 6. Parameter generation

Each successfully entered Muon parameter transaction under R2-B receives one monotonic `parameter_generation_id` bound to:

- parameter index;
- parameter ID;
- target training generation;
- target optimizer step;
- active R2-B step generation.

Required witness:

`[ASH-UNIFIED-ATLAS-MCU-PARAMETER-GENERATION-BEGIN-R2B]`

A failed parameter transaction drops its generation guard and emits an abort witness without claiming reclamation success.

## 7. Step generation

The first R2-B parameter in one target optimizer step creates one `step_generation_id`.

Every later parameter in the same target generation / optimizer step must bind to that same step generation.

Advancing to a different step while the old R2-B step generation remains active fails closed.

Required witness:

`[ASH-UNIFIED-ATLAS-MCU-STEP-GENERATION-BEGIN-R2B]`

## 8. Physical parameter-retention closure introduced by this revision

Source review shows several full semantic objects were appended for every parameter and kept until optimizer generation rollover even though their final full-object consumer is still inside `execute_muon_parameter`.

R2-B changes the retention of these specific full objects:

- `bp_dk_bridge_pair_evidence`
- `bp_dk_bridge_temporal_observations`
- `bp_dk_bridge_temporal_warming`
- `bp_dk_fusion_candidate_graphs`
- `bp_dk_fusion_execution_plans`

These full objects are `ParameterTransient` under R2-B.

After the parameter's Muon execution, post-update construction, evidence checks, readbacks and existing exact waits are complete, R2-B performs parameter terminal reclamation by moving the generation-owned vectors out with `std::mem::take` and dropping them.

This is backing retirement, not only logical `clear()`.

No `shrink_to_fit` loop is introduced.

## 9. Compact fusion-plan lineage preservation

The full `AshBpDkFusionExecutionPlan` contains a parameter-sized `domains` vector and is not retained after parameter terminal under R2-B.

D09 only requires the canonical plan digest sequence.

R2-B therefore preserves:

`canonical_parameter_index -> plan_digest`

in a compact ordered `BTreeMap<u32, String>`.

The D09 fusion-plan sequence hash continues to hash the same ordered `plan_digest` values by canonical parameter index.

Full execution plans are not retained merely to reproduce this digest.

## 10. Duplicate-parameter protection preservation

Before accepting a new graph/plan, duplicate protection checks both:

- the current in-flight full graph/plan vectors; and
- the compact completed-parameter plan-digest map.

Therefore reclaiming prior full plans does not remove cross-parameter duplicate detection.

## 11. StepTransient state

State whose final semantic consumer is generation commit/audit remains `StepTransient`.

Examples currently tracked include generation-scoped:

- parameter pre-snapshot execution bindings;
- freshness expectations;
- parameter control bindings;
- training-generation parameter snapshot projections;
- active replay receipts where enabled;
- post-update parameter receipts;
- counterfactual receipts where enabled;
- counterfactual effect entries where enabled;
- objective-probe sparse overlays where enabled;
- pending bridge temporal state;
- pending fusion planner state.

The pending bridge/planner state is not reclaimed at parameter terminal because its exact final consumer is generation commit/abort.

## 12. Step terminal

R2-B step terminal is called only after:

1. filesystem generation commit;
2. in-memory Muon generation commit;
3. BP-DK generation completeness audit;
4. training-generation provenance closure;
5. control-data-plane generation binding receipt.

Only then may the generation-scoped diagnostic/full-object arrays be physically retired.

Required witnesses:

- `[ASH-UNIFIED-ATLAS-MCU-STEP-TERMINAL-R2B]`
- `[ASH-UNIFIED-ATLAS-MCU-STEP-RECLAMATION-R2B]`

The committed BP-DK temporal/planner state remains persistent and is not included in step reclamation.

## 13. Lease safety

R2-B does not combine lifetime reclamation with async-retirement activation.

`AsyncRetirementRuntimeMode::ActiveAsync` is rejected at the destructive R2-B parameter/step reclamation points.

The current exact-wait / MirrorVerified execution topology remains the safe-point authority for this revision.

Required:

- parameter reset with a live lease fails closed;
- step reset with a live lease fails closed;
- R2-B does not retire existing exact waits;
- R2-B does not activate true async overlap.

## 14. Retention ledger

R2-B emits a tracked collection ledger separating:

- parameter-transient object count;
- minimum top-level container backing bytes;
- step-transient object count;
- step-transient pending-state entry count;
- minimum top-level step container backing bytes;
- compact retained identity count.

Required witness:

`[ASH-UNIFIED-ATLAS-MCU-LIVE-BYTE-LEDGER-R2B]`

The byte field is intentionally named `minimum_container_backing_bytes`.

It is exact for the top-level `Vec` backing being retired but does not pretend to include every nested `String`, `Vec`, `BTreeMap` node, allocator header, or process-heap overhead.

Required witness field:

`nested_heap_bytes_not_claimed=true`

where the pressure snapshot is emitted.

## 15. Memory-pressure snapshot

Immediately before `bridge_temporal_observe_parameter`, R2-B emits:

`[ASH-UNIFIED-ATLAS-MCU-MEMORY-PRESSURE-SNAPSHOT-R2B]`

Checkpoint:

`before_bridge_temporal_state`

This witness is deliberately before the current 6,176-byte failure site so that a fresh physical failure still leaves an owner/lifetime snapshot even if parameter terminal is never reached.

## 16. BridgeTemporalState interpretation

The current first failed allocation is inside `BridgeTemporalState`.

R2-B does not declare `BridgeTemporalState` to be the historical accumulated-memory owner from failure location alone.

The pressure snapshot distinguishes:

- already-retained ParameterTransient full objects;
- legitimate StepTransient pending state;
- compact retained identities;
- the immediate allocation victim.

The current `6,176`-byte failure is a boundary, not automatically the root cause.

## 17. CurrentObservationProjection interpretation

The repeated `29,556,736`-byte `CurrentObservationProjection` request is a direct R2-A observation.

It is ParameterTransient.

Its local backing naturally drops with the parameter callsite and is not falsely counted as generation-persistent merely because the request was large.

R2-B instead targets full semantic structures demonstrably retained in runtime generation vectors.

## 18. Step-final tracked reclamation

After generation audit/control sealing, R2-B physically retires tracked generation-scoped full arrays using `std::mem::take`.

This includes the full diagnostic/projection/binding arrays whose final consumer has completed.

The compact final-generation plan digest map remains available for D09 semantic identity and is cleared when a new BP-DK generation inventory is sealed.

## 19. Reclamation dispositions

Canonical vocabulary:

- `NO_RECLAIM_PERSISTENT`
- `LOGICAL_RESET_RETAIN_CAPACITY`
- `RETURN_TO_BOUNDED_POOL`
- `RESET_PARAMETER_ARENA`
- `RESET_STEP_ARENA`
- `RELEASE_BACKING`
- `HOLD_LIVE_LEASE`

The currently baked parameter and step full-object retirement path uses `RELEASE_BACKING`.

## 20. Reclamation debt

For the R2-B tracked ParameterTransient collection set:

`parameter_terminal_reclamation_debt_bytes = 0`

is required after each successful parameter terminal.

For the R2-B tracked StepTransient collection set:

`step_terminal_reclamation_debt_bytes = 0`

is required after step terminal.

These claims apply to the explicit R2-B tracked collection authority. They do not claim equality with Windows process RSS/commit or uninstrumented allocator internals.

## 21. No process-RSS equivalence claim

R2-B does not claim:

`tracked backing bytes == Windows RSS`

or:

`tracked backing bytes == process commit`

Allocator caching, nested heap allocations, driver allocations and unrelated process memory remain separate diagnostics.

## 22. No historical 1GB owner claim

The previous `1,044,033,536`-byte request did not reproduce in the latest R2-A physical run.

R2-B therefore preserves:

`historical_1044033536_owner_claimed=false`

No byte-size or parameter-99 inference may flip that claim.

## 23. Old parameter-99 boundary preservation

The latest physical run crossed the former parameter-99 generation-7 / optimizer-step-7 boundary and entered Muon wave execution.

R2-B must not regress to the former raw 1GB allocation failure before that point.

## 24. Current physical target

Fresh R2-B Exact N8 must reach at least:

- target generation `7`;
- optimizer step `7`;
- parameter index `98`;
- parameter ID `model.layers.10.mlp.up_proj.weight`;
- checkpoint `before_bridge_temporal_state`.

The previous raw 6,176-byte failure boundary should be crossed.

If a failure still occurs, the last R2-B memory-pressure snapshot becomes the attribution authority for the next patch.

## 25. Physical PASS conditions

R2-B physical closure requires:

- parameter-generation witnesses active;
- parameter terminal after successful Muon parameter execution;
- full ParameterTransient graph/plan/evidence arrays physically retired;
- compact plan digest identity preserved;
- tracked parameter reclamation debt zero;
- step terminal after generation audit/control seal;
- tracked step reclamation debt zero;
- no live-lease reset;
- no stale lifetime generation use;
- old 6,176-byte failure boundary crossed;
- old parameter-99 boundary remains crossed;
- RAM36 unchanged;
- Physical N2 unchanged;
- numerical behavior unchanged;
- async ownership unchanged.

Exact N8 completion is desirable but is not required to call the lifetime boundary itself closed if a later independent failure is encountered with all R2-B invariants passing.

## 26. Error tokens

Required failure vocabulary includes:

- `E_UNIFIED_ATLAS_MCU_PARAMETER_RESET_WITH_LIVE_LEASE_R2B`
- `E_UNIFIED_ATLAS_MCU_STEP_RESET_WITH_LIVE_LEASE_R2B`
- `E_UNIFIED_ATLAS_MCU_CROSS_PARAMETER_TRANSIENT_SURVIVOR_R2B`
- `E_UNIFIED_ATLAS_MCU_CROSS_STEP_TRANSIENT_SURVIVOR_R2B`
- `E_UNIFIED_ATLAS_MCU_STALE_LIFETIME_GENERATION_R2B`
- `E_UNIFIED_ATLAS_MCU_UNBOUNDED_TRANSIENT_CAPACITY_GROWTH_R2B`
- `E_UNIFIED_ATLAS_MCU_RECLAMATION_DEBT_NONZERO_R2B`

## 27. Static acceptance

The R2-B static validator must prove at least:

- R2-B module exported from `base_train`;
- canonical env/patch/PASS tokens;
- typed persistent/wave/parameter/step lifetime vocabulary;
- parameter and step generation authority;
- memory-pressure snapshot before bridge temporal observation;
- parameter terminal reclaim call after full Muon/post-update use;
- `std::mem::take` backing retirement for full graph/plan/bridge arrays;
- compact plan digest map preservation;
- planner pending-state count observation;
- step reclamation after control-data-plane generation binding receipt;
- no `shrink_to_fit` repair;
- R2-A historical exact-request semantics preserved;
- 16 MiB R2-A threshold unchanged;
- no 32 MiB geometry adoption;
- no async activation.

## 28. Required unit tests

At minimum:

- `scope_end_does_not_imply_reclamation`
- `parameter_reclamation_requires_actual_backing_drop`
- persistent classes remain distinct from transient classes.

Fresh Cargo validation should additionally run existing R2-A and Muon host-retirement tests.

## 29. Previous closure preservation

R2-B must preserve:

- Unified Atlas MCU R1 control-plane static closure;
- R2-A allocation-admission static closure;
- Muon full candidate host materialization retirement;
- Muon full source host scratch retirement;
- persistent source/momentum slab reuse;
- per-tile source heap retirement;
- RAM36 hard authority;
- immutable Physical N2 authority;
- B05/B06/C07/C08 mode matrix.

## 30. Explicit non-goals

R2-B does not:

- change 16 MiB Atlas physical pages;
- introduce 32 MiB two-wave clusters;
- change canonical commit width;
- activate AdamW MCU execution ownership;
- activate Muon MCU execution ownership;
- retire exact waits;
- retire bulk candidate D2H;
- add tracing GC;
- use disk spill;
- reorder parameters;
- reorder batches;
- mutate Physical N2;
- increase RAM36;
- claim the historical 1GB owner.

## 31. Final runtime receipt

Required final witness:

`[ASH-BASETRAIN-UNIFIED-ATLAS-MCU-GENERATIONAL-RECLAMATION-R2B]`

It must report at least:

- parameter generation count;
- step generation count;
- parameter reset count;
- step reset count;
- parameter abort count;
- released parameter object count;
- minimum released top-level parameter container backing bytes;
- released step object count;
- minimum released top-level step container backing bytes;
- peak tracked parameter container backing bytes;
- peak tracked step container backing bytes;
- survivor / stale-generation / live-lease error counters;
- historical 1GB owner remains unclaimed;
- Physical N2 unchanged;
- RAM36 unchanged;
- Atlas geometry unchanged;
- execution authority unchanged;
- numerical behavior unchanged;
- async overlap inactive;
- hotpath waits not retired.

## 32. Authority statement

Before R2-B, full fusion graphs, execution plans, bridge evidence and bridge temporal products could be retained in generation-owned vectors after the parameter's full semantic use had already completed. R2-A could identify allocation scopes but could not distinguish scope return from retained backing.

After R2-B, those proven parameter-local full objects receive one explicit parameter generation and are physically dropped at the parameter terminal safe point. Only the compact canonical fusion-plan digest identity required by D09 survives. Genuine step-owned pending bridge/planner state remains alive until the generation commit boundary and is not reclaimed early. Step-owned diagnostic/projection arrays are physically retired only after the generation audit and control-data-plane receipt consume them.

The runtime therefore stops using optimizer-generation rollover as the default garbage collector for parameter-local semantic objects and instead reclaims them at their actual last-consumer boundary without changing numerical state, scheduler order, RAM36, Atlas geometry or async execution authority.
