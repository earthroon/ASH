# ASH-BASETRAIN-N8-HIMUON-PRODUCTION-HOTPATH-BIND-R1

## 1. Patch identity

```text
ASH-BASETRAIN-N8-HIMUON-PRODUCTION-HOTPATH-BIND-R1

Existing TensorCube Local Muon Production Admission /
Managed BP-DeltaK Active Fusion Policy Authority /
AdamW·Muon Disjoint Hybrid Optimizer Routing /
Planned Fusion·Physical Fused Executor Parity /
Legacy HiMuon Counter Non-Reuse /
N8 Optimizer Attribution Truth Repair /
No Silent Activation·No Double Optimizer /
Eight-Step Production Execution Seal
```

Build revision:

```text
n8-himuon-production-hotpath-bind-r1
```

Receipt schema:

```text
ash.basetrain.n8_himuon_production_hotpath_bind.v1
```

## 2. Purpose

The current N8 wall-time attribution run proved that the canonical eight-step production
route executed AdamW while both local Muon and fused HiMuon execution were absent. That
run therefore cannot be used to judge HiMuon performance.

The missing execution is not solved by inventing another optimizer or by silently turning
Muon on for all N8 runs. This patch binds the already-existing TensorCube Local Muon
production callsite and BP-DeltaK fused-pair execution path to an explicitly admitted,
managed production run and repairs the N8 attribution authority so physical HiMuon
execution is read from the fused executor receipt rather than from a legacy zero-invariant
counter.

Performance improvement is not a promotion condition for this patch. R1 first proves that
planned fused domains actually execute on the physical production path while AdamW
ownership, resident state, and N8 deferred durability remain intact.

## 3. Existing production Muon admission remains authoritative

R1 reuses the existing BaseTrain CLI admission:

```text
--admit-tensorcube-local-muon-production-callsite
```

and the existing inputs:

```text
--tensorcube-local-muon-first-candidate-registry <path>
--tensorcube-local-muon-profile <path>
```

The existing new-lineage admission remains:

```text
--admit-tensorcube-local-muon-new-lineage
```

R1 does not add a second Muon enable switch and does not automatically activate Muon from
N8 long-horizon admission, registry presence, policy presence, or HiMuon observation.

The new CLI flag is an assertion only:

```text
--require-n8-himuon-active-fusion
```

It means that this explicit N8 run must have valid managed ACTIVE fusion authority and
must physically execute at least one fused HiMuon domain. It does not create that
authority by itself.

## 4. Parent admission chain

The existing ProductionMuonRuntime parent requirements remain fail-closed:

```text
--admit-ram-resident-adam-mv
--admit-ram-weight-pack-persistent-residency
--admit-ram-budget-exact-inventory
--admit-ram36-process-budget-authority
```

The R1 assertion additionally requires:

```text
--admit-n8-long-horizon-continuity
--production-loop-optimizer-steps 8
--admit-tensorcube-local-muon-production-callsite
```

No parent gate is weakened.

## 5. Muon lineage authority

ProductionMuonRuntime loads durable Muon momentum from the source candidate directory:

```text
tensorcube_local_muon_momentum.f32.bin
tensorcube_local_muon_momentum_manifest.json
```

Exact semantics are preserved:

```text
sidecars present + new_lineage=false -> resume existing Muon lineage
sidecars absent  + new_lineage=true  -> initialize zero momentum for a new lineage
sidecars present + new_lineage=true  -> hard fail
sidecars absent  + new_lineage=false -> hard fail
```

Therefore R1 never guesses lineage. The caller must inspect the source checkpoint and
supply `--admit-tensorcube-local-muon-new-lineage` only when the source has no existing
Muon momentum sidecars and a new lineage is intentionally authorized.

## 6. Managed BP-DeltaK ACTIVE fusion authority

The fusion planner default remains disabled when no production authority is supplied.
R1 does not treat a raw environment variable as a production authorization shortcut.

The canonical production launch path is the existing explicit activation wrapper:

```text
ash_bp_dk_fusion_policy_explicit_production_activation_15
run-managed-production
```

The managed launcher resolves the active pointer and startup binding and launches the
existing BaseTrain binary with the controlled planner environment.

When `--require-n8-himuon-active-fusion` is asserted, ProductionMuonRuntime must expose a
control/data-plane binding satisfying all of the following:

```text
planner mode = Active
binding scope = Production
binding status = Exact
active pointer digest is present
startup binding digest is present
binding policy digest == planner policy digest
```

Failures include:

```text
N8HiMuonActivePlannerRequired
N8HiMuonManagedPolicyBindingMissing
N8HiMuonPolicyDigestDrift
```

## 7. Hybrid optimizer routing remains disjoint

The existing first-candidate eligibility registry remains the routing authority.
Muon admission does not retire AdamW.

Canonical invariants:

```text
Muon-owned elements + AdamW-owned elements = total trainable elements
overlap elements = 0
unclassified elements = 0
writable overlap elements = 0
```

Muon-eligible ranges use Muon/HiMuon execution domains. Registry-designated AdamW ranges
continue through the existing AdamW route.

The assertion requires a preserved AdamW route rather than treating AdamW as a hidden
fallback.

## 8. Planner execution domains

The existing BP-DeltaK fusion/fission planner produces execution domains including:

```text
LOCAL
FUSED_RIGHT
FUSED_DOWN
```

LOCAL domains are TensorCube Local Muon execution and must not be mislabeled as HiMuon.

FUSED_RIGHT and FUSED_DOWN domains are eligible for physical fused-pair execution through
the existing TensorCubeFusedPairMuonExecutor.

## 9. HiMuon physical execution definition

For this patch:

```text
HiMuon physical execution
=
a planner-owned FUSED_RIGHT or FUSED_DOWN production domain
that actually executes through the fused-pair Muon executor
```

A policy artifact, fusion candidate, or planned fused domain without a physical dispatch
is not HiMuon execution.

Likewise, a physical fused dispatch without a corresponding planner-owned fused domain is
an authority violation.

## 10. Physical execution truth

R1 uses the already-existing production Muon counters:

```text
fusion_planner_local_domain_count
fusion_planner_fused_right_domain_count
fusion_planner_fused_down_domain_count

fused_muon_right_pair_count
fused_muon_down_pair_count
fused_muon_dispatch_count
fused_muon_physical_batch_count
fused_muon_workgroup_count
```

The canonical physical predicate is based on the fused executor receipt, not a legacy
observer counter.

Required right/down parity:

```text
planned FUSED_RIGHT domains == physical fused right pairs
planned FUSED_DOWN domains  == physical fused down pairs
```

Additional fail-closed conditions:

```text
planned fused domains > 0 and fused dispatch count == 0 -> fail
planned fused domains == 0 and physical fused execution > 0 -> fail
physical fused execution without physical pair receipt -> fail
```

Representative failures:

```text
N8HiMuonFusedPlanPhysicalParityDrift
N8HiMuonFusedPlanPhysicalExecutionMissing
N8HiMuonUnplannedPhysicalExecution
N8HiMuonFusedPairReceiptMissing
```

## 11. Legacy HiMuon counter is deliberately not repurposed

The existing field:

```text
bp_dk_himuon_fusion_execution_count
```

is currently a legacy no-authority counter with a zero invariant in the production Muon
receipt. R1 preserves that semantic contract.

It must remain zero and must not become the new physical HiMuon counter.

A nonzero value is treated as semantic drift:

```text
N8HiMuonLegacyCounterSemanticDrift
```

This avoids a silent ABI/receipt meaning change.

## 12. N8 phase attribution truth repair

`ASH-BASETRAIN-N8-PHASE-WALL-TIME-ATTRIBUTION-R1` previously derived HiMuon execution
from the legacy zero counter. This patch repairs that observation path.

The phase receipt now carries explicit fields for:

```text
localMuonExecuted
himuonFusedExecuted
himuonFusedDispatchCount
himuonFusedRightPairCount
himuonFusedDownPairCount
legacyBpDkHiMuonFusionExecutionCount
legacyCounterIsExecutionAuthority = false
```

`himuonExecuted` and the compatibility execution-count field are derived from the
physical fused dispatch receipt.

GPU subphase time remains unavailable unless a non-stalling GPU timestamp domain is
separately established. R1 does not fabricate HiMuon GPU time from host wall time.

## 13. N8 production cardinality

When production Muon admission is enabled for the canonical eight-step N8 transaction,
the existing production callsite invocation count must equal the optimizer-step budget:

```text
optimizer steps = 8
Muon production callsite invocations = 8
```

With `--require-n8-himuon-active-fusion`, the following are additionally required:

```text
planned fused domains > 0
physical fused pair count > 0
physical fused dispatch count > 0
HiMuon physical executed = true
AdamW preserved parameter count > 0
```

## 14. Gradient, weight, and commit invariants

HiMuon production binding must not reintroduce data-plane regressions.

Required:

```text
Muon gradient payload readback bytes = 0
BP-DeltaK full gradient readback bytes = 0
Muon weight disk read bytes = 0
optimizer disk weight read bytes = 0
partial Muon commit count = 0
partial AdamW commit count = 0
```

Muon momentum remains the existing F32 TensorCube Local Muon momentum authority. HiMuon
does not allocate an independent second momentum lineage.

Muon-owned ranges must not read or write Adam M/V state, and AdamW-owned ranges must not
consume Muon momentum.

## 15. N8 Deferred Durable Writeback compatibility

The already-promoted N8 deferred resident transaction remains authoritative.

Muon/HiMuon consumes the resident weight source and must not require intermediate
`weights.r6pack` materialization.

Steps 1-7 retain zero packed payload writes. Step 8 retains final triple-pack
materialization and packed sync cardinality three. This patch does not alter checkpoint
serialization, durability timing, storage publication, or archive semantics.

## 16. Runtime receipt and diagnostic

New receipt:

```text
n8_himuon_production_hotpath_bind_receipt.json
```

It records, at minimum:

```text
production Muon admission
planner mode
managed production binding state
policy revision and digest
optimizer step count
Muon callsite and parameter invocation counts
local planned domain count
fused right/down planned domain counts
fused right/down physical pair counts
fused dispatch / physical batch / workgroup counts
HiMuon physical executed
AdamW preserved parameter count
Muon parameter count
overlap / unclassified / writable-overlap counts
Muon gradient readback bytes
Muon weight disk read bytes
partial optimizer commit counts
legacy HiMuon counter
legacy-counter execution-authority flag
```

Runtime diagnostic:

```text
[ASH-N8-HIMUON-PRODUCTION-R1]
```

When the assertion is active and all physical gates pass, the diagnostic must show a
managed ACTIVE production binding, eight Muon callsite invocations, nonzero fused plan
and physical execution, preserved AdamW ownership, zero overlap/unclassified elements,
zero gradient readback, zero weight disk reads, and the legacy counter explicitly marked
non-authoritative.

## 17. Assertion semantics

`--require-n8-himuon-active-fusion` is a verification assertion.

When false, R1 may write an observation receipt and HOLD without forcing fusion.

When true, failures are hard and include:

```text
N8HiMuonOptimizerStepWindowMismatch
N8HiMuonProductionCallsiteCardinalityDrift
N8HiMuonActivePlannerRequired
N8HiMuonManagedPolicyBindingMissing
N8HiMuonPolicyDigestDrift
N8HiMuonRequiredButNoFusedDomainPlanned
N8HiMuonFusedPlanPhysicalExecutionMissing
N8HiMuonUnplannedPhysicalExecution
N8HiMuonAdamwPreservedRouteMissing
```

The assertion never silently activates a new Muon lineage or fabricates a fused domain.

## 18. Implementation surface

Baked R1 overlay contains exactly the following 18 changed files:

```text
crates/base_train/src/bin/base_train.rs
crates/base_train/src/config.rs
crates/base_train/src/lib.rs
crates/base_train/src/n8_himuon_production_hotpath_bind.rs
crates/base_train/src/n8_phase_wall_time_attribution.rs
crates/base_train/src/pipeline.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs

tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
tools/validate_ash_basetrain_n8_himuon_production_hotpath_bind_r1_static.py
tools/validate_ash_basetrain_n8_phase_wall_time_attribution_r1_static.py

tools/validate_ash_bp_dk_fusion_policy_candidate_canary_qualification_14_static.py
tools/validate_ash_bp_dk_fusion_policy_explicit_production_activation_15_static.py
tools/validate_ash_bp_dk_fusion_policy_production_soak_and_rollback_health_16_static.py
tools/validate_ash_bp_dk_fusion_policy_production_long_horizon_stability_17_static.py
tools/validate_ash_bp_dk_fusion_policy_production_evidence_recalibration_bridge_18_static.py
tools/validate_ash_bp_dk_fusion_policy_production_evidence_calibration_adoption_19_static.py
tools/validate_ash_bp_dk_fusion_policy_production_aware_calibration_recommendation_20_static.py
tools/validate_ash_bp_dk_fusion_policy_production_aware_recommendation_operator_review_adoption_21_static.py
```

The 14-21 validator changes are a same-class parent-SHA fanout closure caused by the
`base_train.rs` CLI admission change. The previous parent SHA is removed from all eight
validators in one pass.

The baked overlay excludes generated artifacts, manifests, `.sha256` sidecars, and
Python cache output.

## 19. Static evidence

Observed in the reconstructed cumulative source tree:

```text
N8 HiMuon production hotpath bind R1:                         86/86 PASS
N8 phase wall-time attribution R1:                            77/77 PASS
N8 Deferred Durable Writeback + closures:                    118/118 PASS
N8 source-weight generation SSOT:                             28/28 PASS
N8 long-horizon continuity:                                   70/70 PASS
RAM-resident Adam M/V final writeback:                        73/73 PASS
RAM weight-pack persistent residency / Atlas readahead:       67/67 PASS
VRAM hot-weight-page residency:                               70/70 PASS
GPU successor weight commit continuity:                       52/52 PASS
Storage-root authority:                                       39/39 PASS
RAM36 process-budget authority:                               63/63 PASS
BP-DeltaK policy qualification 14:                           347/347 PASS
BP-DeltaK explicit production activation 15:                 274/274 PASS
BP-DeltaK production soak/rollback 16:                       177/177 PASS
BP-DeltaK production long-horizon 17:                        225/225 PASS
BP-DeltaK production recalibration bridge 18:                298/298 PASS
BP-DeltaK production calibration adoption 19:                230/230 PASS
BP-DeltaK production recommendation 20:                      237/237 PASS
BP-DeltaK production operator review/adoption 21:            265/265 PASS
```

The reduced bake tree does not contain every production profile/CLI fixture consumed by
older standalone validators, and the bake container has no Rust toolchain. The local
Release CF1 chain is therefore the compilation/type/borrow and full-fixture promotion
authority.

## 20. Physical acceptance

A canonical asserted HiMuon N8 production run must prove:

```text
Muon production admission = true
ProductionMuonRuntime exists
planner mode = ACTIVE
binding scope = Production
binding status = Exact
managed active pointer and startup binding are present
policy digest parity = true
optimizer steps = 8
Muon callsite invocations = 8
Muon parameter invocations > 0
planned fused right/down domains > 0
physical fused right/down pairs > 0
fused dispatch count > 0
physical fused batch/workgroup evidence > 0
HiMuon physical executed = true
AdamW preserved parameter count > 0
overlap elements = 0
unclassified elements = 0
writable overlap elements = 0
Muon gradient readback bytes = 0
Muon weight disk read bytes = 0
partial Muon commit count = 0
partial AdamW commit count = 0
legacy BP-DeltaK HiMuon counter = 0
legacy counter execution authority = false
training generation 5 -> 13
N8 Deferred Durable Writeback remains promoted
```

## 21. Performance comparison boundary

The previously measured no-Muon N8 run remains the baseline observation:

```text
training_compute_wall_ms = 1,037,232
adamw_wall_ms = 94,294
local Muon executed = false
HiMuon fused executed = false
```

The first asserted HiMuon run is compared primarily by training-compute and optimizer
phase time. End-to-end storage publication variance is not used to claim optimizer speed.

This patch promotes execution correctness, not speed. A separate performance verdict is
made only after physical fused execution is proven.

## 22. Promotion tokens

Structural:

```text
PASS_ASH_BASETRAIN_N8_HIMUON_PRODUCTION_HOTPATH_BIND_STRUCTURAL_R1
```

Managed policy authority:

```text
PASS_ASH_BASETRAIN_N8_HIMUON_MANAGED_ACTIVE_POLICY_BIND_R1
```

Hybrid routing:

```text
PASS_ASH_BASETRAIN_N8_HIMUON_ADAMW_DISJOINT_HYBRID_ROUTING_R1
```

Physical fused execution:

```text
PASS_ASH_BASETRAIN_N8_HIMUON_FUSED_EXECUTOR_PHYSICAL_R1
```

N8 physical:

```text
PASS_ASH_BASETRAIN_N8_HIMUON_PRODUCTION_HOTPATH_PHYSICAL_R1
```

Final:

```text
PROMOTE_ASH_BASETRAIN_N8_HIMUON_PRODUCTION_HOTPATH_BIND_R1
```

## 23. Final SSOT

```text
N8 never claims HiMuon execution from the legacy BP-DeltaK HiMuon observation counter.
That counter retains its existing zero/no-authority meaning.

TensorCube Local Muon production execution remains explicitly admitted. AdamW and Muon
ownership remain disjoint under the canonical optimizer registry.

Managed BP-DeltaK production authority supplies the ACTIVE planner policy. The HiMuon
assertion verifies that authority; it does not create it.

HiMuon physical execution means that planner-owned FUSED_RIGHT/FUSED_DOWN domains were
actually dispatched through the existing fused-pair Muon executor. Planned/physical
right and down domains must match exactly.

No gradient full readback, weight disk regression, hidden AdamW fallback, double optimizer,
partial commit, or synthetic new lineage is permitted.

N8 phase attribution reads physical fused executor evidence and explicitly marks the
legacy counter as non-authoritative.

Only after physical HiMuon execution is established may its performance be compared with
the no-Muon N8 baseline.
```
