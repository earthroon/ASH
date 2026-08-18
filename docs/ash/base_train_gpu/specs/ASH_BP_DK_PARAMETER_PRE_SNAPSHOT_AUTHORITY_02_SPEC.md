# ASH-BP-DK-PARAMETER-PRE-SNAPSHOT-AUTHORITY-02

## Parameter-Local PRE-Optimizer Atomic Snapshot / Weight·Momentum·Gradient·Routing·Policy Source Seal / Same-Parameter Fusion Domain Closure / Cross-Snapshot Mixing Rejection / Global PRE Barrier Supersession

## 0. Status

```text
Patch ID: ASH-BP-DK-PARAMETER-PRE-SNAPSHOT-AUTHORITY-02
Governance/spec parent: ASH-BP-DK-LINEAGE-VOCABULARY-SEAL-01
Runtime-registry semantic parent: ASH-BP-DK-FUSION-FISSION-PLANNER-05
Runtime parent: ASH-BASETRAIN-TENSORCUBE-LOCAL-MUON-PRODUCTION-CALLSITE-ADOPTION-R1
Authority class: BpDkDataPlane
Primary authority: Observation
Target data-plane revision: bp-dk-data-plane/active-fusion/v1
New data-plane revision: none
Policy generation ownership: none
Qualification generation ownership: none
```

This distinction is intentional. The 00 registry admits the five production/evidence authority classes and does not fabricate a `LineageGovernance` class solely to register 01. The approved documentation lineage therefore remains `01 -> 02`, while the runtime registry records the real BP-Delta-K semantic parent as 05 plus explicit evidence parents 02/03A/03B/04/05.

## 1. Purpose

The production HiMuon path already executes parameter-locally:

```text
R6 Finalized Gradient(parameter)
 -> packed gradient
 -> Local BP_PRE observation
 -> freshness verification
 -> 03A same-parameter pair evidence
 -> 03B temporal Bridge
 -> 04 Fusion candidate graph
 -> 05 Fusion/Fission plan
 -> Local/Fused Muon candidate
```

The missing authority was a single immutable statement that all PRE inputs consumed by those stages belonged to the same parameter invocation and the same pre-optimizer source state.

02 introduces that authority without changing Muon mathematics, Bridge mathematics, Fusion thresholds, TensorCube geometry, or production policy-selection semantics.

## 2. Core SSOT

```text
ONE PARAMETER
+
ONE OPTIMIZER INVOCATION
+
ONE PRE-OPTIMIZER SOURCE SNAPSHOT
=
ONE PARAMETER PRE SNAPSHOT AUTHORITY
```

A matching parameter ID alone is insufficient:

```text
same parameter != same snapshot
```

## 3. Atomic scope

The snapshot belongs to exactly one parameter, not one TensorCube cell.

```text
Parameter PRE Snapshot
 |- canonical 16x16 cell 0
 |- canonical 16x16 cell 1
 |- ...
 |- Right pair candidates
 `- Down pair candidates
```

Every Ready local observation, admitted 03A endpoint, 03B current observation, 04 graph, and 05 plan participating in one invocation must be traceable to the same parameter PRE snapshot.

Cross-parameter and cross-snapshot mixing remain invalid.

## 4. Global PRE barrier supersession

02 does not restore the historical all-parameter PRE collection barrier.

Canonical execution remains:

```text
Parameter A snapshot -> observe -> verify -> bridge -> plan -> execute
Parameter B snapshot -> observe -> verify -> bridge -> plan -> execute
...
```

Generation-wide completeness is a separate audit concern and is deferred to:

```text
ASH-BP-DK-GENERATION-COMPLETENESS-AUDIT-03
```

Thus:

```text
02 = parameter-local atomic truth
03 = generation-wide completeness truth
```

## 5. Runtime module

New module:

```text
crates/base_train/src/bp_delta_k_parameter_pre_snapshot.rs
```

Exported through:

```text
crates/base_train/src/lib.rs
```

The module defines:

```text
AshBpDkParameterPreSnapshotStatus
AshBpDkParameterIdentity
AshBpDkWeightSourceSeal
AshBpDkOptimizerSourceSeal
AshBpDkGradientSourceSeal
AshBpDkRoutingSourceSeal
AshBpDkObservationContractSeal
AshBpDkBridgeContractSeal
AshBpDkFusionContractSeal
AshBpDkPhysicalCapabilitySeal
AshBpDkParameterPreSnapshot
AshBpDkVerifiedParameterPreSnapshot
AshBpDkParameterPreSnapshotExecutionBinding
AshBpDkParameterPreSnapshotBuildRequest
```

Status vocabulary remains explicit:

```text
Current
Stale
Unverifiable
Contradictory
```

`Unverifiable` is not silently collapsed into `Stale` or `Contradictory`.

## 6. Snapshot source seals

### Parameter identity

The snapshot seals:

```text
parameter_id
canonical_parameter_index
logical_shape
tensorcube_plan_digest
```

Topology authority comes from the canonical FirstCandidate registry/grid. Parameter strings are not parsed to reconstruct topology.

### Weight source

The snapshot seals:

```text
source weight generation
weight binding digest
existing source weight content digest when already authoritative
```

02 does not read the full GPU weight payload to manufacture provenance.

### Optimizer/momentum source

The snapshot seals:

```text
optimizer generation
momentum binding digest
```

The binding digest is metadata-derived from parameter identity, optimizer generation, profile identity, momentum region, and Muon element count.

Current bake deliberately records:

```text
momentum_content_digest = None
```

rather than hashing the full CPU momentum slice again merely for snapshot construction.

### Gradient source

The snapshot seals deterministic metadata for the already-produced packed gradient:

```text
parameter ID
logical shape
dtype tag
segment-plan digest
lease-identity digest
packed-gradient provenance digest
```

Lease identity uses reproducible metadata such as:

```text
logical element starts
shape/length
buffer offset/size
seam ID
vendor access path
optional primitive/stream IDs
```

Raw Rust/GPU object addresses are not canonical identity.

### Routing source

The snapshot seals:

```text
registry digest
optimizer routing digest
tensorcube routing digest
```

A sealed snapshot cannot silently rebuild topology from another registry revision.

### Observation / Bridge / Fusion contracts

The snapshot seals:

```text
local observer contract revision/policy digest
03A pair contract digest
03B temporal contract digest
04 graph contract digest
05 planner policy digest
physical Fusion capability digest
```

The policy digest here means the exact semantics consumed by the parameter invocation. Why that policy became production-active remains control-plane provenance and is deferred to the later control/data-plane binding revision.

## 7. No payload ownership

The snapshot owns identity, not buffers.

Forbidden by this patch:

```text
snapshot-owned weight tensor
snapshot-owned momentum tensor
snapshot-owned gradient buffer
new GPU allocation for snapshot provenance
full weight D2H for provenance
full momentum D2H for provenance
full gradient D2H for provenance
shader dispatch solely to construct snapshot identity
```

## 8. Local observation binding

`assemble_bp_local_dk_product()` receives the sealed parameter PRE snapshot digest.

Ready BackpropPre observations now bind:

```text
source_snapshot_id = Some(parameter_pre_snapshot_digest)
```

and include that digest in their source IDs.

This intentionally advances the old 01 assumption where `source_snapshot_id` was explicitly `None`. The 01 static validator is forward-compatible only when the 02 module exists and the exact explicit snapshot binding is present; otherwise it continues to require the historical 01 representation.

## 9. Freshness and verified snapshot

Existing freshness authority remains authoritative.

```text
ParameterPreSnapshot
 -> Ready local observations
 -> existing verify_bp_pre_observation_current
 -> current verified observation subset
 -> VerifiedParameterPreSnapshot
```

The verified snapshot records:

```text
expected_tensorcube_count
verified_tensorcube_count
observation_inventory_complete
verified tensorcube IDs
verified observation IDs
verified observation-set digest
freshness-verification digest
verified snapshot digest
```

Warm-up/partial Ready inventory is not silently called complete:

```text
observation_inventory_complete
=
verified_tensorcube_count == expected_tensorcube_count
```

02 does not introduce a new blocking warm-up/global completeness barrier. Generation completeness judgment belongs to 03.

## 10. 03A binding

03A pair evidence is checked against the verified snapshot.

Required:

```text
same parameter ID
same canonical parameter index
same weight generation
same optimizer generation
same BP generation
same source weight digest
lhs observation belongs to verified set
rhs observation belongs to verified set
```

No cross-parameter Bridge is introduced.

## 11. 03B binding

03B current temporal observations are checked against the same current snapshot identity while retaining their own pair-owned temporal history.

Historical temporal state does not replace current weight/gradient snapshot authority.

## 12. 04 graph binding

The existing 04 serialized graph schema is not rewritten.

Instead the new snapshot authority verifies that the existing graph identity and every node correspond to the same verified parameter source state.

This preserves the old 04 ABI while closing provenance externally.

## 13. 05 plan binding

The existing 05 execution-plan schema is likewise preserved.

Before the plan is admitted into the runtime sidecar binding, 02 verifies:

```text
parameter identity
weight generation
optimizer generation
BP generation
planner policy digest
physical capability digest
exact graph identity
```

No Local/Fused mathematical formula changes.

## 14. Execution binding sidecar

02 intentionally avoids injecting new fields into the serialized 03A/03B/04/05 schemas.

Instead it creates:

```text
AshBpDkParameterPreSnapshotExecutionBinding
```

containing:

```text
parameter ID / canonical index
parameter PRE snapshot digest
verified parameter PRE snapshot digest
03A evidence-set digest
03B evidence-set digest
04 topology/evidence digests
05 plan digest
planner policy digest
capability digest
binding digest
```

The runtime keeps the binding in a parameter-indexed generation sidecar vector and exposes a read-only getter.

The vector is cleared when the BP-Delta-K optimizer generation rolls.

## 15. Existing schema preservation

02 does not add `parameter_pre_snapshot_digest` fields to:

```text
crates/ash_core/src/delta_k_bridge_pair_evidence.rs
crates/ash_core/src/delta_k_bridge_temporal_observation.rs
crates/ash_core/src/bp_dk_fusion_candidate_graph.rs
crates/ash_core/src/bp_dk_fusion_fission_planner.rs
```

Their existing digests remain authoritative. The 02 execution-binding sidecar connects them transitively to the verified PRE snapshot.

## 16. Production callsite ordering

Canonical integrated ordering:

```text
resolve parameter
 -> pack exact gradient
 -> resolve observer / Bridge / graph / planner contracts
 -> probe current physical Fusion capability
 -> seal ParameterPreSnapshot
 -> local BP_PRE observe
 -> assemble Ready observations with source_snapshot_id
 -> existing freshness verification
 -> seal VerifiedParameterPreSnapshot
 -> 03A pair planning/evidence
 -> verify 03A against snapshot
 -> 03B temporal observation
 -> verify 03B against snapshot
 -> 04 graph
 -> verify graph against snapshot
 -> 05 plan
 -> verify plan against snapshot
 -> seal execution binding
 -> existing calibration/replay/execution/commit flow
```

## 17. Failure behavior

02 introduces typed fail-stop conditions for structural mismatch, including:

```text
gradient parameter mismatch
gradient shape mismatch
observation missing snapshot identity
observation cross-snapshot
observation cross-parameter
Bridge cross-parameter
Bridge endpoint outside verified set
temporal cross-parameter
graph cross-parameter
graph node outside verified set
plan cross-parameter
plan policy drift
plan capability drift
duplicate per-generation parameter binding
```

02 does not introduce:

```text
snapshot validation failure -> silent Local fallback
snapshot validation failure -> latest policy substitution
snapshot mismatch -> automatic generation bump
```

Source changes require a new snapshot rather than mutation of the old snapshot.

## 18. Counter authority

`ProductionMuonExecutionCounters` adds:

```text
bp_dk_parameter_pre_snapshot_seal_count
bp_dk_parameter_pre_snapshot_verified_count
bp_dk_parameter_pre_snapshot_binding_count
bp_dk_parameter_pre_snapshot_cross_parameter_mix_count
bp_dk_parameter_pre_snapshot_cross_snapshot_mix_count
bp_dk_parameter_pre_snapshot_full_tensor_readback_count
bp_dk_parameter_pre_snapshot_full_tensor_readback_bytes
```

The authority-leak gates require the cross-parameter, cross-snapshot, and full-tensor-readback counters to remain zero.

## 19. Historical validator compatibility

Policy validators 14 through 21 historically pinned the production Muon callsite SHA as forever byte-identical.

02 intentionally changes that callsite, so these validators are made narrowly forward-compatible:

```text
old exact parent SHA still passes
OR
02 module exists AND the callsite contains all of:
  seal_parameter_pre_snapshot
  seal_verified_parameter_pre_snapshot
  seal_parameter_pre_snapshot_execution_binding
  parameter_pre_snapshot.snapshot_digest
```

No other parent hash exception is introduced.

Thus 14-21 policy mathematics and source anchors remain pinned while the explicit 02 provenance adoption is admitted.

## 20. Registry and vocabulary

00 registry adds 02 as:

```text
family = bp-dk-reconciliation-runtime
authority = BpDkDataPlane / Observation
status = Active
runtime semantic parent = 05
runtime parent = Production Muon callsite
evidence parents = stale 02 / 03A / 03B / 04 / 05
```

It explicitly does not supersede the old stale-observation 02, 03A, 03B, 04, 05, 15, or 21.

01 vocabulary binding is:

```text
owned_data_plane_revision = None
target_data_plane_revision = bp-dk-data-plane/active-fusion/v1
owned_policy_generation = None
owned_qualification_generation = None
```

02 therefore does not fabricate a new `v2` data plane merely because its patch suffix is `02`.

## 21. Static validator

New validator:

```text
tools/validate_ash_bp_dk_parameter_pre_snapshot_authority_02.py
```

New runner:

```text
tools/run_ash_bp_dk_parameter_pre_snapshot_authority_02.ps1
```

CF1 ordering:

```text
...
21 static validator
 -> ASH-LINEAGE-RECONCILIATION-00
 -> ASH-BP-DK-LINEAGE-VOCABULARY-SEAL-01
 -> ASH-BP-DK-PARAMETER-PRE-SNAPSHOT-AUTHORITY-02
```

## 22. Bake evidence

Static/source evidence from the baked tree:

```text
ASH-LINEAGE-RECONCILIATION-00: 135/135 PASS
ASH-BP-DK-LINEAGE-VOCABULARY-SEAL-01: 306/306 PASS
ASH-BP-DK-PARAMETER-PRE-SNAPSHOT-AUTHORITY-02: 216/216 PASS
```

All existing BP-Delta-K static validators from observation contract 00 through production-aware operator review 21 were re-run after the 02 adoption and passed, including the forward-compatible 01 and 14-21 gates.

Unrelated critical source areas changed by 02:

```text
crates/ash_core/               0 files
crates/burn_webgpu_backend/    0 files
apps/                          0 files
vendor_fork_scaffold/          0 files
```

02 runtime changes are confined to `crates/base_train` plus tool validators/registry/CF1 wiring.

## 23. Compile evidence boundary

The bake environment used for this revision does not provide:

```text
cargo
rustc
rustfmt
```

Therefore:

```text
Rust compile verification = EvidenceInsufficient / not executed in this bake environment
```

No cargo-check/build PASS is claimed by this document.

The static validator includes delimiter/source-order/interface checks, but these are not represented as a substitute for Rust compilation.

## 24. Packaging

Delivered code ZIPs must exclude:

```text
*.md
*.sha256
__pycache__
*.pyc
generated manifests
generated receipts
generated reports
artifact directories
```

Overlay contains only files changed by 02.

Full applied code contains the complete 01 parent body with 02 applied.

## 25. Non-goals

02 does not implement:

```text
generation-wide completeness blocking
generation-wide PRE barrier
Atlas forward/backward generation provenance closure
production active-pointer provenance inside execution receipts
new R2 physical canary
ProductionMuonRuntime decomposition
new Fusion topology
cross-parameter Fusion
new precision/residency policy
```

## 26. Next revision

```text
ASH-BP-DK-GENERATION-COMPLETENESS-AUDIT-03
```

03 should reclaim the existing generation-wide `verify_all` concept as a non-mutating end-of-generation audit rather than reintroducing a global PRE execution barrier.

## 27. Final seal

```text
ONE PARAMETER
ONE OPTIMIZER INVOCATION
ONE PRE SOURCE SNAPSHOT

WEIGHT SOURCE IS SEALED
OPTIMIZER/MOMENTUM SOURCE IS SEALED
GRADIENT SOURCE IS SEALED
ROUTING IS SEALED
OBSERVATION CONTRACT IS SEALED
BRIDGE CONTRACT IS SEALED
FUSION POLICY IS SEALED
PHYSICAL CAPABILITY IS SEALED

SAME PARAMETER DOES NOT MEAN SAME SNAPSHOT

NO CROSS-PARAMETER BRIDGE
NO CROSS-SNAPSHOT BRIDGE
NO CROSS-SNAPSHOT FUSION

NO GLOBAL PRE BARRIER
NO SILENT FALLBACK
NO SILENT SNAPSHOT REPAIR

NO FULL-TENSOR D2H FOR PROVENANCE
NO BUFFER DUPLICATION FOR PROVENANCE

SNAPSHOT OWNS IDENTITY, NOT THE BUFFER
FRESHNESS OWNS CURRENTNESS, NOT EXECUTION
PLANNER OWNS FUSION DECISION, NOT THE SNAPSHOT
COMMIT AUTHORITY REMAINS WHERE IT ALREADY LIVES

PARAMETER-LOCAL ATOMICITY IS EXPLICIT
```
