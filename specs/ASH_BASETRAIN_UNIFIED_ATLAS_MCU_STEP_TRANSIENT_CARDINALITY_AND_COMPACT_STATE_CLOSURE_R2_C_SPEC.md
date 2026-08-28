# ASH-BASETRAIN-UNIFIED-ATLAS-MCU-STEP-TRANSIENT-CARDINALITY-AND-COMPACT-STATE-CLOSURE-R2-C

## Exact Step Ownership / Parameter-Terminal Audit Compaction / Topology-Bounded Pending State / No Unqualified Tile-Proportional Step Retention

### 0. Revision identity

Revision:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-STEP-TRANSIENT-CARDINALITY-AND-COMPACT-STATE-CLOSURE-R2-C`

Parent:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-PARAMETER-LIFETIME-CLOSURE-R2-B`

Environment gate:

`ASH_UNIFIED_ATLAS_MCU_STEP_TRANSIENT_COMPACTION_R2C=1`

Purpose: close StepTransient representation and cardinality after R2-B has already proven exact ParameterTransient reclamation.

### 1. Parent authority preservation

R2-C preserves the R2-B invariant that every successful parameter terminal leaves zero tracked ParameterTransient objects, backing, live leases, and parameter reclamation debt. R2-C must not weaken parameter-terminal reclamation, change lifetime ownership merely to hide cardinality, or silently move StepTransient payload back into ParameterTransient.

### 2. Core invariant

`StepTransient != everything useful until step end`.

A later step-terminal consumer may require information derived from a producer without requiring the producer's full object graph. When identity, digest, count, ordinal, range, status, or summary is sufficient, full producer payload must not remain retained merely because the optimizer step is still active.

### 3. Source-derived R2-C target

The pre-R2-C generation path can retain three tile-proportional audit structures across successfully completed parameters:

- materialized expected TensorCube ID vectors in `AshBpDkGenerationExpectedInventory`;
- current-generation full observations in `AshBpDkCurrentGenerationLedger`;
- per-TensorCube `bp_dk_generation_freshness_expectations`.

R2-C replaces these generation-audit representations with:

- a compact expected inventory that streams the canonical TensorCube IDs into the unchanged inventory digest without retaining the IDs;
- parameter-local observation/freshness state consumed before parameter return;
- one compact parameter audit summary retained per Muon parameter.

### 4. Legitimate bounded algorithmic pair state

R2-C does **not** claim that all tile-related StepTransient state disappears.

`AshBpDkBridgeTemporalRuntime.pending` and `AshBpDkFusionFissionPlannerRuntime.pending` are real next-generation candidate state. They may scale with the number of admitted bridge pairs because later generation commit consumes them.

They are classified as `BoundedPendingState`, not leak/diagnostic state, and are admitted only under an exact topology-derived structural bound.

### 5. StepTransient semantic classes

R2-C recognizes:

- `CompactAccumulator`: bounded compact state used by later audit/commit;
- `BoundedPendingState`: unresolved algorithmic state with a known future consumer and structural bound;
- `TerminalAuditState`: bounded records required until step/generation terminal;
- `DiagnosticEphemeral`: diagnostic data that must not accumulate in the normal step path.

### 6. Step generation SSOT

Each active optimizer step is bound to one exact `step_generation_id`, target generation, target optimizer step, expected Muon parameter count, expected TensorCube count, and a structural compaction policy.

Required begin witness:

`[ASH-UNIFIED-ATLAS-MCU-STEP-GENERATION-BEGIN-R2C]`

### 7. Compact expected inventory

R2-C adds `AshBpDkGenerationCompactExpectedInventoryR2C` and `AshBpDkExpectedParameterCompactR2C`.

Each compact parameter descriptor preserves:

- parameter ID;
- canonical parameter index;
- logical shape;
- full tile rows/columns;
- expected TensorCube count;
- the canonical parameter inventory digest.

It must not retain `Vec<String>` containing every expected TensorCube ID.

Required witness:

`[ASH-UNIFIED-ATLAS-MCU-STEP-COMPACT-EXPECTED-INVENTORY-R2C] ... materialized_tensorcube_id_count=0 ...`

### 8. Digest parity requirement

The compact expected-inventory path must preserve the existing digest contracts:

- `ash.bp_dk.generation_expected_parameter_inventory.v1`;
- `ash.bp_dk.generation_expected_inventory.digest.v1`.

TensorCube IDs are generated in the same canonical row/column order and streamed directly into the hasher. R2-C is a representation/lifetime change, not an expected-inventory identity change.

### 9. Parameter-local audit evidence

Under R2-C, the current parameter owns its temporary:

- `Vec<AshBpPreDeltaKObservation>`;
- `BTreeMap<String, AshBpDkFreshnessExpectation>`.

These are not appended to generation-wide step containers. They are consumed while the parameter remains semantically live to produce `AshBpDkCompactParameterAuditR2C`.

### 10. Compact parameter audit

`AshBpDkCompactParameterAuditR2C` preserves the exact `AshBpDkParameterCompletenessSummary`, observed-parameter presence, unexpected TensorCube identities when present, and unexpected binding count.

Its summary preserves current/missing/stale/unverifiable/contradictory counts, expected and observed inventory digests, and snapshot/binding digests.

The compact audit record count is bounded by the expected Muon parameter count.

### 11. Generation completeness reconstruction

At generation audit, R2-C reconstructs `AshBpDkGenerationCompletenessAuditReceipt` from:

- compact expected inventory;
- ordered compact parameter audit summaries.

Final canonical ordering is by canonical parameter index, not completion timing.

The generation audit must preserve the same schema and receipt validation path used by the legacy audit authority.

### 12. Compact parameter snapshot-set digest

The step-terminal parameter snapshot-set digest is reconstructed from ordered compact execution-binding digests. Full `AshBpDkParameterPreSnapshotExecutionBinding` objects need not remain alive solely for generation-completeness audit after their compact identity has been consumed.

### 13. Control-data generation binding

R2-C provides a compact expected-inventory variant of the control-data-plane generation binding seal. It preserves expected parameter identity/cardinality and optimizer-route binding without requiring the materialized expected TensorCube ID vectors.

Parameter control bindings remain bounded terminal-audit state until their existing exact consumer completes.

### 14. Fusion plan identity

`bp_dk_fusion_execution_plan_digest_by_parameter` remains the already-established compact generation-level D09 diagnostic identity authority.

It is reported separately from R2-C StepTransient debt because its later D09 consumer exists after the step-terminal reclamation point. R2-C does not misclassify it as a full StepTransient payload.

### 15. Bounded BridgeTemporal pending state

BridgeTemporal pending cardinality is bounded by the exact number of admissible right/down neighbor pairs induced by every Muon grid:

`right = rows * max(cols - 1, 0)`

`down = max(rows - 1, 0) * cols`

The structural bound is the sum of these exact pair counts across admitted Muon parameters.

### 16. Bounded FusionPlanner pending state

FusionPlanner pending state receives the same topology-derived maximum bridge-pair bound. Exceeding this structural bound is a hard closure failure, not a reason to allocate more state silently.

Required error:

`E_UNIFIED_ATLAS_MCU_STEP_PENDING_STATE_BOUND_EXCEEDED_R2C`

### 17. No unqualified tile-proportional retention

R2-C forbids tile-proportional normal StepTransient retention that exists only to support audit, diagnostics, or delayed identity reconstruction.

R2-C explicitly permits tile-pair-proportional `BoundedPendingState` only when it is an actual algorithmic authority with a proven future consumer and topology-derived bound.

Therefore the final receipt uses:

`unqualified_tile_proportional_step_retention_detected=false`

rather than claiming that no tile-related pending state exists.

### 18. Optional evidence base bound

Base R2-C qualification assumes replay/counterfactual/objective-probe optional evidence modes remain disabled as in the current R2-B qualification route.

The base structural bound for optional evidence entries is zero. Enabling an optional mode requires an explicit separate structural bound and cannot silently consume base R2-C capacity.

Required error:

`E_UNIFIED_ATLAS_MCU_STEP_OPTIONAL_EVIDENCE_UNBOUNDED_R2C`

### 19. Cardinality snapshot

`McuStepCardinalitySnapshotR2C` tracks:

- total classified StepTransient logical objects;
- bounded pending state entries;
- exact top-level backing bytes available from the parent ledger;
- compact audit entry count;
- compact identity count;
- BridgeTemporal pending count;
- FusionPlanner pending count;
- optional evidence count;
- legacy/full generation-audit payload count.

### 20. Full step payload count

The `full_step_payload_object_count` specifically detects R2-C-retired generation-audit payloads:

- legacy materialized expected TensorCube IDs;
- legacy generation observation ledger entries;
- legacy generation freshness expectation entries.

After every successful R2-C parameter compaction boundary this count must be zero.

### 21. Step compaction debt

`StepCompactionDebt` is full StepTransient audit payload whose full semantic content is no longer required but whose generation-wide representation remains retained.

Required successful state:

`step_compaction_debt_objects=0`.

Required errors:

- `E_UNIFIED_ATLAS_MCU_STEP_COMPACTION_DEBT_NONZERO_R2C`;
- `E_UNIFIED_ATLAS_MCU_CROSS_PARAMETER_FULL_STEP_PAYLOAD_SURVIVOR_R2C`.

### 22. Parameter-terminal compaction boundary

After the compact parameter audit has been sealed and R2-B has reclaimed full parameter-local bridge/fusion payloads, R2-C observes the step state and validates it against the structural envelope.

Required witness:

`[ASH-UNIFIED-ATLAS-MCU-STEP-COMPACTION-R2C]`.

Required fields include step/parameter generation identities, before/after object/state/backing counts, compact entries, bounded pending entries, growth class, and `nested_heap_bytes_not_claimed=true`.

### 23. Growth classification

R2-C classifies observed state as:

- `CONSTANT`;
- `PER_PARAMETER_COMPACT`;
- `BOUNDED_PENDING`;
- `UNBOUNDED`;
- `UNKNOWN_NESTED`.

`UNBOUNDED` is a closure failure. `UNKNOWN_NESTED` blocks unsupported physical-memory claims but does not by itself prove semantic cardinality failure.

### 24. Structural cardinality envelope

The base R2-C object envelope is derived only from:

- exact BridgeTemporal pair-state bound;
- exact FusionPlanner pair-state bound;
- bounded per-parameter compact/terminal-audit records;
- explicitly admitted optional evidence bound.

No empirical corpus slack is added.

Required error:

`E_UNIFIED_ATLAS_MCU_STEP_CARDINALITY_ENVELOPE_EXCEEDED_R2C`.

### 25. High-water witness

When a tracked R2-C high-water mark increases, emit:

`[ASH-UNIFIED-ATLAS-MCU-STEP-CARDINALITY-HIGH-WATER-R2C]`.

It records object/state/top-level backing counts, compact accumulator count, bounded pending count, growth class, and `nested_heap_bytes_not_claimed=true`.

### 26. Byte semantics

R2-C inherits the parent meaning of `minimum_container_backing_bytes`: exact top-level tracked `Vec` capacity only.

It does not claim nested Strings, nested Vecs, BTreeMap node allocation, allocator metadata, process RSS/commit, GPU allocation, or driver allocation unless separately measured.

Required:

`nested_heap_bytes_not_claimed=true` where applicable.

### 27. No count-to-RSS inference

A large logical object/state count is evidence of cardinality shape, not proof of a particular byte total. R2-C must not convert millions of objects to a fabricated RAM size without exact ownership accounting.

### 28. No semantic repair by deletion

R2-C must not reduce cardinality by dropping required evidence, failed parameter identity, canonical ordering, provenance links, control binding, or algorithmic pending state.

Compaction is admitted only when later consumers require the compact representation rather than the full producer representation.

### 29. No serialization repair

R2-C must not serialize full step state to disk solely to free RAM and later reload it. That is a different execution/lifetime architecture and is outside R2-C.

### 30. No reordering repair

R2-C must not reorder parameters, waves, fusion operations, or canonical commits to reduce simultaneous state.

### 31. Step terminal

Before R2-C step terminal:

- every expected Muon parameter has one compact audit record;
- all bounded BridgeTemporal/FusionPlanner pending state has reached its existing generation-commit consumer and is resolved;
- full step audit payload count is zero;
- R2-C compaction debt is zero;
- canonical compact audit order is complete.

Required witness:

`[ASH-UNIFIED-ATLAS-MCU-STEP-TERMINAL-R2C]`.

### 32. Step terminal ordering preservation

R2-C preserves the parent order: filesystem generation commit, in-memory optimizer commit, BP-DK generation completeness audit, training-generation provenance closure, and control-data-plane generation binding complete before destructive step-state reclamation.

### 33. Step reclamation

After the existing final consumers complete, R2-C removes its compact expected inventory and compact parameter audit map while the parent R2-B step reclamation removes the already-qualified step-scoped diagnostic/projection/binding collections.

Required witness:

`[ASH-UNIFIED-ATLAS-MCU-STEP-RECLAMATION-R2C]`.

Successful final state requires zero R2-C StepTransient logical objects, state entries, tracked top-level backing, optional evidence, bounded pending state, full audit payload, compaction debt, and reclamation debt.

### 34. Parameter-lifetime closure preservation

The final R2-C receipt must state:

`parameter_lifetime_closure_preserved=true`.

R2-C does not replace or broaden R2-B parameter reclamation semantics.

### 35. Persistent-state exclusion

R2-C does not reclaim model weights, Adam M/V, persistent Muon state, committed BP-DK temporal/planner state required by the next generation, Physical N2 state, or other explicitly persistent authority.

### 36. Numerical semantics

R2-C changes representation and lifetime only.

Required final declarations:

- `precision_contract_changed=false`;
- `numerical_behavior_changed=false`;
- canonical ordering preserved.

### 37. Atlas and execution authority

R2-C preserves:

- physical Atlas page = 16 MiB;
- Atlas slot count = 3;
- current MirrorVerified/legacy execution authority;
- current exact synchronization/wait behavior.

R2-C does not introduce 32 MiB logical clusters, subgroup kernels, mixed precision, async overlap, D2H retirement, or active MCU execution ownership.

### 38. Historical failure authority

The historical 1,044,033,536-byte allocation owner remains unproven.

Required:

`historical_1044033536_owner_claimed=false`.

R2-C must not attribute the old 6,176-byte failure to BridgeTemporal merely because it occurred at that entry boundary.

### 39. RAM36 / Physical N2

Required final declarations:

- `physical_n2_mutated=false`;
- `ram36_authority_changed=false`;
- `atlas_geometry_changed=false`;
- `execution_authority_changed=false`.

### 40. Static validation requirements

Static validation must prove:

- R2-C environment, patch, runtime/static pass tokens exist;
- compact expected inventory exists and does not contain `expected_tensorcube_ids`;
- canonical expected TensorCube IDs are streamed into the legacy digest contract;
- parameter-local observations/freshness are used under R2-C instead of global generation insertion;
- compact parameter audits are retained at O(parameter_count);
- compact generation completeness and compact control-data generation seal exist;
- materialized expected TensorCube ID witness is zero;
- BridgeTemporal/FusionPlanner pending state is validated against a topology-derived pair bound;
- optional evidence base bound is zero;
- full generation-audit payload survivors are rejected;
- step terminal requires zero unresolved bounded pending state and zero compaction debt;
- R2-B parameter closure is still invoked;
- 16 MiB Atlas and current execution authority remain unchanged;
- no mixed-precision/subgroup/cluster activation is introduced by R2-C.

### 41. Unit-test requirements

At minimum preserve/add tests for:

- compact expected inventory digest contract equals the legacy expected inventory digest contract for equivalent semantic input;
- tile count is admitted only inside explicit bounded pending authority;
- full step payload survivor is not compact state;
- existing R2-B lifetime class separation remains intact.

These tests are source-baked; they are not considered observed until run by Rust tooling.

### 42. Physical qualification sequence

`R2-C static -> parent static regressions -> cargo check -> focused Rust tests -> release build -> fresh Native CF1 -> fresh cross-release authority -> immutable Physical N2 -> Exact N8`.

No binary-derived authority may be reused across source changes.

### 43. Runtime acceptance gate

A physically passing Exact N8 must show:

- R2-B parameter reclamation debt remains zero;
- materialized expected TensorCube ID count is zero under R2-C;
- global generation observation/freshness retention is absent under R2-C;
- one compact parameter audit exists per expected Muon parameter;
- BridgeTemporal/FusionPlanner pending state never exceeds exact topology-derived bounds;
- all pending pair state resolves by step terminal;
- full step payload/compaction debt is zero;
- step reclamation debt is zero;
- no numerical, Atlas, ordering, execution-authority, RAM36, or Physical N2 change.

### 44. Final runtime receipt

Required:

`[ASH-BASETRAIN-UNIFIED-ATLAS-MCU-STEP-TRANSIENT-CARDINALITY-AND-COMPACT-STATE-CLOSURE-R2C]`

Minimum fields:

- patch ID;
- step generation count;
- completed parameter count;
- parameter compaction count;
- full step payload object release count;
- compact step record count;
- maximum StepTransient object/state/top-level backing counts;
- maximum bounded pending state count;
- cross-parameter full step payload survivor count = 0;
- pending-state bound exceeded count = 0;
- step compaction debt objects = 0;
- step reclamation debt bytes = 0;
- `unqualified_tile_proportional_step_retention_detected=false`;
- `bounded_algorithmic_pair_state_retained=<observed boolean>`;
- `parameter_lifetime_closure_preserved=true`;
- `historical_1044033536_owner_claimed=false`;
- `physical_n2_mutated=false`;
- `ram36_authority_changed=false`;
- `atlas_geometry_changed=false`;
- `execution_authority_changed=false`;
- `precision_contract_changed=false`;
- `numerical_behavior_changed=false`;
- `verdict=PASS`.

Required pass token:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_STEP_TRANSIENT_CARDINALITY_AND_COMPACT_STATE_CLOSURE_R2C`

### 45. Explicit non-goals

R2-C does not activate subgroup execution, SoftMatrix16, mixed precision, optimizer MoE, Path-Integral expert routing, wave clustering, global TensorCube job scheduling, GPU-side precision escalation, active Muon/AdamW MCU ownership, bulk D2H retirement, exact-wait retirement, checkpoint policy changes, RAM36 changes, or Physical N2 mutation.

### 46. Handoff

Successful R2-C establishes:

- parameter-local transient payload dies at exact parameter terminal;
- generation audit evidence is compacted per parameter rather than retained per tile;
- algorithmically necessary pair state survives only as explicitly topology-bounded pending state;
- step-terminal audit identity remains exact;
- unqualified cumulative tile-proportional StepTransient retention is closed.

Recommended next revision:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-HOTPATH-INSTRUMENTATION-COMPRESSION-AND-SEMANTIC-FAILURE-RING-R3`

### 47. Center sentence

**R2-C does not pretend that every tile-related state can disappear. It removes tile-proportional audit representations that no longer need full payload, while keeping real BridgeTemporal/FusionPlanner future-dependency state only under an exact topology-derived bound. Step state may grow with semantic necessity, never merely because every tile left another object behind.**
