# ASH-MUON-RUNTIME-AUTHORITY-DECOMPOSITION-07

## ProductionMuonRuntime Facade / Execution·Observation·Bridge·Planning·Evidence·Control-Binding Ownership Split / Transaction Order Preservation / Single-Writer State Authority / No Mathematical or Receipt-Semantic Rewrite

## 0. Status

```text
Patch ID: ASH-MUON-RUNTIME-AUTHORITY-DECOMPOSITION-07
Direct parent: ASH-BP-DK-POLICY-R2-CLOSURE-06
Authority class: OptimizerDataPlane
Primary authority: Execution
Target BP-Delta-K data-plane revision: bp-dk-data-plane/active-fusion/v1
New BP-Delta-K data-plane revision: none
Policy generation ownership: none
Qualification generation ownership: none
```

07 changes state ownership and orchestration structure. It does not intentionally change Muon, Bridge, Fusion/Fission, BP-Delta-K, G1/G2 policy, forward/backward, gradient-accumulation, commit, or receipt mathematics.

## 1. Central SSOT

```text
ONE MUTABLE CANONICAL STATE
=
ONE AUTHORITY OWNER

ProductionMuonRuntime
=
PUBLIC ORCHESTRATION FACADE

ProductionMuonRuntime
!=
OWNER OF EVERY SUBSYSTEM STATE
```

The parent 06 runtime directly owned more than fifty mutable execution/observation/bridge/planning/evidence/control fields in one struct. 07 moves those fields into authority-owned runtime objects while preserving the top-level `ProductionMuonRuntime` API.

## 2. Actual baked owner topology

The baked 07 source keeps the owner types in the existing production-callsite module rather than scattering them across new files. This is intentional: the semantic ownership split is adopted while the public production source surface remains localized.

`ProductionMuonRuntime` now directly owns exactly nine top-level fields:

```text
static_context : ProductionMuonStaticContext
execution      : ProductionMuonExecutionRuntime
observation    : ProductionBpDkObservationRuntime
bridge         : ProductionBpDkBridgeRuntime
planning       : ProductionBpDkPlanningRuntime
control        : ProductionBpDkControlBindingRuntime
evidence       : ProductionBpDkEvidenceRuntime
telemetry      : ProductionMuonTelemetry
lifecycle      : ProductionMuonLifecycleIdentity
```

The old canonical mutable fields no longer remain as direct facade fields.

## 3. Static context authority

`ProductionMuonStaticContext` owns only immutable runtime context:

```text
FirstCandidateEligibilityRegistry
TensorCubeLocalMuonProfile
```

Registry/profile are shared by projection through the facade and are not duplicated into each subruntime as mutable authority.

## 4. Execution authority

`ProductionMuonExecutionRuntime` owns:

```text
momentum
norm subgroup probe state
selected norm-reduction path
batch executor
gradient packer
fused-pair executor
```

This remains the physical Muon-compute owner.

No Evidence/Bridge/Planning runtime receives a second mutable momentum or executor instance.

## 5. Observation authority

`ProductionBpDkObservationRuntime` owns:

```text
local BP-Delta-K observer
current-generation BP-Delta-K ledger
02 Parameter PRE snapshot execution bindings
03 freshness expectations
observer restart/rewarm state
observer state-reinitialization receipts
```

The current-generation observation ledger remains a single state authority.

03 audit consumes observation views; it does not own or mutate a duplicate ledger.

## 6. Bridge authority

`ProductionBpDkBridgeRuntime` owns:

```text
03A bridge-pair observer
03A generation/evidence state
03B temporal runtime
03B ready observations
03B warming receipts
```

07 adds owner-local methods:

```text
commit_pending_generation()
abort_pending_generation()
```

The facade calls these methods rather than directly committing the Bridge temporal object.

Bridge remains observation/temporal authority and does not gain Fusion/Fission decision authority.

## 7. Planning authority

`ProductionBpDkPlanningRuntime` owns:

```text
04 Fusion candidate graphs
old 05 Fusion/Fission planner
05 execution plans
```

It likewise exposes owner-local:

```text
commit_pending_generation()
abort_pending_generation()
```

The planner still answers what execution domain should run; the physical executor remains in Execution.

## 8. Control-binding authority

`ProductionBpDkControlBindingRuntime` owns:

```text
05 immutable runtime control/data binding
05 parameter control bindings
05 generation binding receipts
```

The 06 scope vocabulary is preserved unchanged:

```text
NotApplicable
Production
QualificationCanary
```

07 does not write active pointers, select G1/G2 policy generations, or hot-reload policy artifacts.

## 9. Evidence authority

`ProductionBpDkEvidenceRuntime` owns the read-mostly and generation/long-horizon evidence state:

```text
04 training-generation parameter/snapshot projections
03 expected generation inventory
03 completeness receipts

06 replay configuration/receipts
old 07 POST update ledger/parameter receipts
08 same-source counterfactual configuration/receipts
08B physical counterfactual configuration/receipts
09 causal/counterfactual-effect ledger
10 one-step objective probe ledger/overlays
11 long-horizon trajectory
12 calibration recommendation runtime
```

This state is physically moved out of the facade rather than copied.

No shadow evidence ledger is introduced.

## 10. Telemetry and lifecycle

`ProductionMuonTelemetry` owns the existing `ProductionMuonExecutionCounters` unchanged.

`ProductionMuonLifecycleIdentity` owns:

```text
source_generation
source_optimizer_step
```

Existing `ProductionMuonCallsiteReceipt` counter semantics remain unchanged.

## 11. Public facade compatibility

The public production type remains:

```text
ProductionMuonRuntime
```

Existing production-facing methods remain available, including:

```text
load_or_initialize
execute_muon_parameter
record_step_commit
record_step_abort
persist_candidate_state
receipt
registry
route_for_parameter
momentum_bytes
```

07 is not a callsite migration patch.

## 12. Parameter execution order preservation

The production invocation remains semantically ordered as before:

```text
route resolve
 -> gradient packing
 -> 02 Parameter PRE snapshot
 -> local BP_PRE observation
 -> freshness verification
 -> verified PRE snapshot
 -> 03A pair evidence
 -> 03B temporal evidence
 -> 04 candidate graph
 -> old 05 planner
 -> 05 control/data binding validation
 -> 02 execution binding
 -> Local/Fused physical execution
 -> replay/POST/counterfactual/objective/trajectory/calibration staging
 -> ProductionMuonParameterOutput
```

07 changes access paths such as:

```text
self.bp_dk_fusion_planner
```

to:

```text
self.planning.bp_dk_fusion_planner
```

without changing planner semantics.

## 13. Commit causality preservation

The baked 07 keeps the parent causal order:

```text
Bridge temporal commit
 -> Fusion planner commit
 -> POST update ledger commit
 -> Causal/counterfactual-effect commit
 -> Objective probe commit
 -> Trajectory commit
 -> Calibration commit
```

The dependency heads remain explicit:

```text
Causal    consumes committed POST head
Objective consumes committed Causal head
Trajectory consumes committed POST + Causal + Objective heads
```

No global atomic-commit claim is added by 07.

## 14. Abort coverage preservation

Abort order remains:

```text
Bridge
 -> Planner
 -> POST
 -> Causal
 -> Objective
 -> Trajectory
 -> Calibration
```

Generation-local observation/control/training-projection sidecars are then cleared under the same generation condition as the parent.

## 15. Persistence coverage preservation

`persist_candidate_state()` continues to orchestrate the same canonical state surfaces:

```text
Muon momentum
Fusion/Fission planner state
POST ledger
Causal-effect ledger
Objective-probe ledger
Trajectory ledger
Calibration replay evidence
```

07 does not introduce a new combined runtime-state file and does not rewrite existing checkpoint schemas.

## 16. Single-writer declaration invariant

The 07 validator enumerates every canonical facade field moved into the owner types and requires:

```text
exactly one owner declaration
no direct facade declaration
```

Representative ownership:

```text
momentum                                -> Execution
bp_dk_ledger                            -> Observation
bp_dk_bridge_temporal                   -> Bridge
bp_dk_fusion_planner                    -> Planning
bp_dk_control_data_plane_binding        -> ControlBinding
bp_dk_counterfactual_effect_ledger      -> Evidence
bp_dk_fusion_trajectory                 -> Evidence
bp_dk_fusion_calibration                -> Evidence
counters                                -> Telemetry
source_optimizer_step                   -> Lifecycle
```

## 17. No decomposition shortcuts

07 does not add:

```text
unsafe block for ownership bypass
Mutex<ProductionMuonRuntime>
RefCell<ProductionMuonRuntime>
giant replacement EverythingState object
second planner
second observation ledger
second momentum authority
```

The split is represented by typed ownership rather than interior-mutability escape hatches.

## 18. Inherited 03 compile blocker realignment

During 07 source inspection, an inherited parent defect was found in `packed_index_for_logical()`.

The parent 03 line had inserted an expected-generation check using:

```text
optimizer_step
```

inside a method that has no `optimizer_step` parameter or local variable. This is a definite Rust compile blocker inherited by 04/05/06.

07 does not silently fabricate a value for it.

The existing 03 semantic check is moved to the beginning of:

```text
execute_muon_parameter(... optimizer_step ...)
```

where the actual optimizer-step authority exists.

Therefore the intended 03 contract remains:

```text
expected generation inventory must be sealed
and must match the optimizer generation
before parameter execution
```

while `packed_index_for_logical()` returns to being a pure registry/geometry projection.

The 07 validator explicitly checks both facts:

```text
packed_index_for_logical contains no undefined optimizer_step reference
execute_muon_parameter contains the 03 expected-inventory generation gate
```

## 19. Historical validator forward compatibility

Existing BP-Delta-K static validators 01 through 12 previously matched direct facade paths such as:

```text
self.bp_dk_ledger
self.bp_dk_bridge_temporal
self.bp_dk_fusion_planner
self.bp_dk_post_update_ledger
self.momentum
self.counters
```

07 updates these validators to track the exact new owner paths, for example:

```text
self.observation.bp_dk_ledger
self.bridge.bp_dk_bridge_temporal
self.planning.bp_dk_fusion_planner
self.evidence.bp_dk_post_update_ledger
self.execution.momentum
self.telemetry.counters
```

The underlying mathematical/order/authority conditions remain checked.

The ExactSubgroup32 norm validator likewise follows the selected path at:

```text
self.execution.norm_reduction_path
```

rather than relaxing the gate.

## 20. Lineage registry and vocabulary

00 registry adds:

```text
ASH-MUON-RUNTIME-AUTHORITY-DECOMPOSITION-07
family = optimizer-runtime-reconciliation
authority = OptimizerDataPlane / Execution
status = Active
direct parent = ASH-BP-DK-POLICY-R2-CLOSURE-06
runtime parent = existing Production Muon callsite
```

The reconciliation head records:

```text
optimizer-runtime-reconciliation
 -> ASH-MUON-RUNTIME-AUTHORITY-DECOMPOSITION-07
```

Vocabulary binding:

```text
owned_data_plane_revision = None
target_data_plane_revision = bp-dk-data-plane/active-fusion/v1
owned_policy_generation = None
owned_qualification_generation = None
```

07 is not a new BP-Delta-K data-plane revision.

## 21. Tooling

New validator:

```text
tools/validate_ash_muon_runtime_authority_decomposition_07.py
```

New runner:

```text
tools/run_ash_muon_runtime_authority_decomposition_07.ps1
```

CF1 order appends 07 after 06:

```text
...
ASH-BP-DK-CONTROL-DATA-PLANE-BINDING-05
 -> ASH-BP-DK-POLICY-R2-CLOSURE-06
 -> ASH-MUON-RUNTIME-AUTHORITY-DECOMPOSITION-07
```

The standalone runner does not search for or apply overlay ZIPs.

## 22. Baked static evidence

Final work-tree evidence:

```text
ASH-LINEAGE-RECONCILIATION-00                  162 / 162 PASS
ASH-BP-DK-LINEAGE-VOCABULARY-SEAL-01          306 / 306 PASS
ASH-BP-DK-PARAMETER-PRE-SNAPSHOT-AUTHORITY-02 216 / 216 PASS
ASH-BP-DK-GENERATION-COMPLETENESS-AUDIT-03    167 / 167 PASS
ASH-TRAINING-GENERATION-PROVENANCE-CLOSURE-04 198 / 198 PASS
ASH-BP-DK-CONTROL-DATA-PLANE-BINDING-05        92 / 92 PASS
ASH-BP-DK-POLICY-R2-CLOSURE-06                143 / 143 PASS
ASH-MUON-RUNTIME-AUTHORITY-DECOMPOSITION-07    345 / 345 PASS
```

Additional regression evidence:

```text
existing BP-Delta-K *_static.py validators: 25 / 25 PASS
CF1-enumerated Python static validators: 63 / 63 PASS
modified Python validator/registry syntax: py_compile PASS
```

The CF1 Python list was executed in two bounded halves after one full sequential invocation exceeded the execution-tool timeout. Both halves were executed to completion and all validator exit codes passed.

## 23. Compile / physical execution evidence boundary

The bake environment does not provide:

```text
cargo
rustc
rustfmt
pwsh
```

Therefore:

```text
Rust compile verification = EvidenceInsufficient / not executed
PowerShell runner execution = EvidenceInsufficient / not executed
physical training execution = not executed
GPU behavior parity = not physically measured in this bake
```

Static/source validation is not represented as a substitute for compilation.

The inherited undefined-`optimizer_step` source defect described above was repaired because it is source-level deterministically invalid, not because a compiler result was available.

## 24. Parent-diff boundary

Compared with the 06 full-applied parent, 07 changes 23 code/tool files.

Runtime source change:

```text
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
```

Registry/runner/CF1 changes:

```text
tools/ash_lineage_reconciliation_00_registry.py
tools/run_ash_muon_runtime_authority_decomposition_07.ps1
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
tools/validate_ash_muon_runtime_authority_decomposition_07.py
```

Forward-compatible validator path updates:

```text
tools/validate_ash_basetrain_tensorcube_local_muon_exact_subgroup32_norm_parallel_reduction_serial_oracle_r1_static.py

tools/validate_ash_bp_dk_local_tensorcube_bp_dk_observation_01_static.py
tools/validate_ash_bp_dk_generation_revision_stale_observation_seal_02_static.py
tools/validate_ash_bp_dk_bridge_pair_evidence_source_closure_03a_static.py
tools/validate_ash_bp_dk_bridge_temporal_coupling_observation_03b_static.py
tools/validate_ash_bp_dk_fusion_candidate_graph_04_static.py
tools/validate_ash_bp_dk_fusion_fission_planner_05_static.py
tools/validate_ash_bp_dk_active_fusion_deterministic_replay_06_static.py
tools/validate_ash_bp_dk_active_fusion_post_update_effectiveness_ledger_07_static.py
tools/validate_ash_bp_dk_active_fusion_same_source_local_counterfactual_08b_static.py
tools/validate_ash_bp_dk_active_fusion_same_source_local_counterfactual_physical_execution_08b_r1_static.py
tools/validate_ash_bp_dk_active_fusion_counterfactual_effect_ledger_09_static.py
tools/validate_ash_bp_dk_fusion_local_one_step_objective_probe_10_static.py
tools/validate_ash_bp_dk_fusion_objective_long_horizon_trajectory_11_static.py
tools/validate_ash_bp_dk_fusion_policy_calibration_recommendation_12_static.py

tools/validate_ash_bp_dk_parameter_pre_snapshot_authority_02.py
tools/validate_ash_bp_dk_generation_completeness_audit_03.py
tools/validate_ash_training_generation_provenance_closure_04.py
```

No `ash_core`, WGSL, app, vendor-fork, policy-G2 control module, or optimizer-kernel source is changed by 07.

## 25. Packaging

Code ZIPs exclude:

```text
*.md
*.sha256
__pycache__
*.pyc
generated manifest JSON
generated receipt JSON
generated report JSON
artifact/manifests directories
```

Deliverables:

```text
Overlay Code ZIP
 -> exact parent-to-07 changed code/tool files

Full Applied Code ZIP
 -> complete 06 parent body with 07 applied
```

The Markdown specification remains outside both code ZIPs and is committed separately to GitHub.

## 26. Non-goals

07 does not implement:

```text
new Muon algorithm
new BP-Delta-K formula
new Bridge topology
new Fusion/Fission policy
new G2 activation semantics
new precision policy
new residency policy
parameter-level parallel execution
new checkpoint schema
historical source deletion
```

## 27. Next revision

```text
ASH-HISTORICAL-EVIDENCE-QUARANTINE-08
```

With active runtime authority now structurally explicit, 08 can classify historical GPU70K/G-series proof paths, old R2A-E roadmap evidence, and other non-production proof surfaces without confusing them with current production ownership.

## 28. Final seal

```text
ProductionMuonRuntime REMAINS THE PUBLIC FACADE

STATIC CONTEXT OWNS REGISTRY / PROFILE
EXECUTION OWNS MOMENTUM / PHYSICAL MUON COMPUTE
OBSERVATION OWNS LOCAL BP-DK / CURRENTNESS / 02 SNAPSHOT STATE
BRIDGE OWNS 03A / 03B
PLANNING OWNS GRAPH / PLANNER / PLAN
CONTROL BINDING OWNS 05 / 06 RUNTIME PROVENANCE
EVIDENCE OWNS 03 / 04 / REPLAY / POST / COUNTERFACTUAL / OBJECTIVE / TRAJECTORY / CALIBRATION
TELEMETRY OWNS COUNTERS
LIFECYCLE OWNS SOURCE GENERATION IDENTITY

ONE MUTABLE CANONICAL STATE HAS ONE OWNER

NO SHADOW LEDGER
NO SHADOW PLANNER
NO SHADOW MOMENTUM
NO PARALLEL CONTROL BINDING

BRIDGE COMMIT PRECEDES PLANNER COMMIT
PLANNER COMMIT PRECEDES POST
POST PRECEDES CAUSAL
CAUSAL PRECEDES OBJECTIVE
OBJECTIVE PRECEDES TRAJECTORY
TRAJECTORY PRECEDES CALIBRATION

ABORT COVERAGE IS PRESERVED
PERSISTENCE COVERAGE IS PRESERVED
PUBLIC CALLSITE IS PRESERVED

NO NEW UNSAFE
NO GIANT MUTEX
NO NEW GPU DISPATCH
NO NEW D2H

THE INHERITED 03 GENERATION CHECK IS MOVED TO THE METHOD THAT ACTUALLY OWNS optimizer_step
NO GENERATION VALUE IS FABRICATED

07 CHANGES WHO OWNS THE STATE
NOT WHAT THE ENGINE MEANS
```
