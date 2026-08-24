# ASH-CONTROL-RUNTIME-NATIVE-AUTHORITY-DAG-ORCHESTRATION-05

## Status

```text
Patch ID: ASH-CONTROL-RUNTIME-NATIVE-AUTHORITY-DAG-ORCHESTRATION-05
Parent: ASH-CONTROL-RUNTIME-NATIVE-CONTRACT-AND-INVARIANT-CATALOG-04
Role: native authority scheduling projection and contract lifecycle ownership
Production authority: false
Evidence execution: none
Legacy semantic coverage expansion: false
Python gate ordering: forbidden
Legacy ordinal scheduling: forbidden
CF1 V2 mutation: false
104 gate migration: false
Cargo authority migration: false
```

## 1. Parent physical truth

NATIVE-03 and NATIVE-04 are physically closed.

```text
NativeAuthorityRegistryValid = true
NativeAuthorityDescriptorCount = 48
Active = 37
QualificationOnly = 6
Superseded = 5
CurrentHeads = 19
CurrentExecutionAuthorities = 8

NativeContractCatalogValid = true
ContractCount = 43
DefinedInvariantCount = 84
ActiveAuthorityContractCoverage = 37 / 37
QualificationAuthorityContractCoverage = 6 / 6
CurrentHeadContractCoverage = 19 / 19
CurrentExecutionAuthorityContractCoverage = 8 / 8
EvidenceExecutionCount = 0
```

Parent identity seals remain unchanged:

```text
NativeAuthorityRegistryDigest =
cfdf654dffc8182a49e67202615a6b874e3568593e4d8bcb20617cbee5ae91ee

NativeContractCatalogDigest =
edbb1f1bf03c627007ff2da05e9a823e5bf2938e08ef2a74d0a509c76d5866cd

NativeInvariantCatalogDigest =
ea05cfbf4b71dc8edb5dbf13b9a9d6c80fcea2b6a05dba3dba62f1731e4061a6
```

## 2. Scheduling authority and layer ownership

Native scheduling input is exclusively the NATIVE-03 authority registry plus the NATIVE-04 contract/invariant catalogs. The native lane does not consume LegacyValidatorId, legacy ordinal, legacy path, legacy source SHA, expected legacy disposition, or Python validator execution order. The old CF1 `0 -> 79` sequence remains migration-oracle behavior only.

```text
Core
  immutable authority / contract / invariant facts

Orchestrator
  root selection
  scheduling projection
  authority DAG session state
  dependency-derived Ready / Blocked / NotExecuted
  fail-fast workflow mode

Manager
  one authority's contract lifecycle
  Pending -> Ready -> Running -> terminal transitions

Factory
  no scheduling state in NATIVE-05

Device
  no scheduling policy in NATIVE-05
```

## 3. Critical bake correction: evidence_parent is provenance, not hard precedence

The initial design considered runtime_parent, control_parent and evidence_parent all as hard prerequisites. Actual NATIVE-03 data proves that this is wrong. Projecting all three classes as executable precedence creates an 11-node strongly connected component involving the fission planner, physical qualification, same-source counterfactual chain, objective chain, calibration, operator review, canary qualification and production activation.

That feedback is meaningful evidence/provenance flow, not a legal execution order.

Final NATIVE-05 law:

```text
runtime_parent  -> hard RuntimePrerequisite
control_parent  -> hard ControlPrerequisite

evidence_parent -> EvidenceProvenance relation only
                   NOT a Ready/Blocked scheduling edge
```

This is an explicit SSOT correction. Evidence relations remain fully projected and identity-sealed separately.

```text
evidenceParentSchedulingEdgeCount = 0
```

The following also remain non-scheduling relations:

```text
direct_parent
does_not_supersede
supersedes
external non-supersession boundaries
```

## 4. Roots and lane separation

The 8 NATIVE-03 current execution authorities remain the Active roots:

```text
native.bp-dk.fusion.fission-planner
native.bp-dk.policy.operator-review-adoption.g2
native.bp-dk.policy.production-activation.g1
native.bp-dk.policy.r2-closure
native.optimizer.generation.failure-recovery
native.optimizer.generation.transaction
native.optimizer.runtime.local-muon-callsite
native.training.runtime.multistep-accumulation-warmup-scheduler
```

```text
CurrentExecutionAuthorityRootCount = 8
```

Qualification scheduling is separate. The default Qualification roots are the NATIVE-03 current heads whose status is QualificationOnly:

```text
native.optimizer.generation.recovery-physical-qualification
native.optimizer.qualification.compile-behavior-parity
native.optimizer.qualification.load-resume-checkpoint-parity
```

```text
QualificationLaneRootCount = 3
```

The remaining three QualificationOnly authorities are not silently promoted into the current-root schedule.

## 5. Actual hard authority DAG

The root union expands through hard runtime_parent and control_parent prerequisites only.

```text
AuthorityDagNodeCount = 13
AuthorityDagEdgeCount = 17
RuntimePrerequisiteEdgeCount = 10
ControlPrerequisiteEdgeCount = 7
EvidenceParentSchedulingEdgeCount = 0

ScheduledActiveAuthorityCount = 10
UnscheduledActiveAuthorityCount = 27
ScheduledQualificationAuthorityCount = 3
UnscheduledQualificationAuthorityCount = 3
ScheduledSupersededAuthorityCount = 0
CrossLaneHardDependencyCount = 3
```

All three cross-lane hard dependencies are Active runtime prerequisites of current QualificationOnly roots.

Structural validity:

```text
AuthorityDagCycleCount = 0
MissingAuthorityDependencyCount = 0
SelfAuthorityDependencyCount = 0
ScheduledSupersededAuthorityCount = 0
ExternalBoundaryScheduledNodeCount = 0
```

## 6. Evidence provenance projection

For the 13 scheduled authorities, declared evidence_parent relations are projected independently of scheduling.

```text
EvidenceProvenanceRelationCount = 52
ScheduledEvidenceRelationCount = 23
UnscheduledCurrentEvidenceRelationCount = 29
SupersededHistoricalEvidenceRelationCount = 0
```

An evidence authority may sit outside the current execution closure without becoming an executable prerequisite. NATIVE-06/07 may later bind particular invariant evidence requirements to concrete evidence production/admission laws. NATIVE-05 does not invent that ordering.

## 7. Contract DAG

NATIVE-04 currently has no explicit contract dependencies. NATIVE-05 does not synthesize contract-to-contract edges from authority relations.

```text
ContractCount = 43
ScheduledContractCount = 13
UnscheduledContractCount = 30
ScheduledActiveContractCount = 10
ScheduledQualificationContractCount = 3
ContractDagNodeCount = 13
ExplicitContractDependencyEdgeCount = 0
ContractDagCycleCount = 0
MissingContractDependencyCount = 0
ContractOwnerMismatchCount = 0
```

Cross-authority ordering is enforced by the authority barrier, not fabricated contract edges.

## 8. Dependency-derived state and native fail-fast

Before any evidence executes:

```text
InitialReadyAuthorityCount = 3
InitialPendingAuthorityCount = 10
InitialBlockedAuthorityCount = 0
```

Initial Ready set:

```text
native.bp-dk.policy.operator-review-adoption.g2
native.bp-dk.policy.production-activation.g1
native.training.runtime.multistep-accumulation-warmup-scheduler
```

Typed authority states:

```text
Pending
Ready
Running
Satisfied
Failed
BlockedDependency
NotExecutedFailFast
```

Workflow modes:

```text
DiagnosticFullDag
FailFast
```

DiagnosticFullDag keeps independent branches schedulable after a failure. FailFast stops new unrelated admission, but actual hard-dependency descendants remain BlockedDependency rather than being mislabeled NotExecutedFailFast. Graph causality wins over global stop policy.

## 9. Manager contract lifecycle

New Manager-native lifecycle:

```text
Pending
Ready
Running
Satisfied
Failed
BlockedDependency
NotExecutedFailFast
```

Legal core transitions:

```text
Pending -> Ready
Pending -> BlockedDependency
Pending -> NotExecutedFailFast
Ready -> Running
Ready -> NotExecutedFailFast
Running -> Satisfied
Running -> Failed
```

Terminal re-entry is illegal. Manager cannot add graph edges, change execution roots or independently declare authority readiness.

## 10. No fake evidence completion

NATIVE-05 executes no native invariant evidence.

```text
EvidenceExecutionCount = 0
ProductionAuthorityClaimed = false
```

Structural schedulability must never be converted into fabricated contract PASS.

## 11. Identity seals

```text
AuthorityExecutionDagDigest =
559c72185b854c2214880473f53980d8e217f83adc9308f282603b649b55528f

EvidenceProjectionDigest =
c806976663d5be7bbd9ddd5e53cc74cd3ddfb03baa750fd5738d5adf4f051de3

ContractExecutionDagDigest =
e8e8a3d4f19a914c0cdd75401a2528ad2778b28934f85474e40ef6ef0688a22d
```

Mode-specific orchestration program digests:

```text
DiagnosticFullDag =
4092cc05891ea5913a6c5cc0bc617044f5f3271e52413227bfecb8aca5c6c8fb

FailFast =
b8b34cdc1ea651b0d7f07d7c34d1fbd2ad75918a3654cc1772984ca4fe9db40e
```

Staged expected receipt hashes after local Rust execution:

```text
DiagnosticFullDag =
bfc5dc7dd48d01decf501baffdda51b50e82a509f4aff12c9c3bb05b90d883a0

FailFast =
0fec8d5f70014a1e5ac72c45894de6c7614f411e894e0497d21585da529233c0
```

These are promotion expectations until physically observed from the local Rust binary.

## 12. Runtime surface

New modules:

```text
crates/ash_control_runtime/src/orchestrator/native.rs
crates/ash_control_runtime/src/manager/native_contract.rs
crates/ash_control_runtime/src/native_dag.rs
```

Modified routing modules:

```text
crates/ash_control_runtime/src/orchestrator/mod.rs
crates/ash_control_runtime/src/manager/mod.rs
crates/ash_control_runtime/src/lib.rs
crates/ash_control_runtime/src/main.rs
```

No ash_core source changes are made by NATIVE-05.

Changed source SHA256:

```text
orchestrator/native.rs 8e66e4845ee2792e55836baab3fd3b44b88e1e9b4cc86f485d1a2773d123fa99
orchestrator/mod.rs    efd4bffca0c0161ae5c8707c8d08a83778ae41333bc11f4897626be418f95ec2
manager/native_contract.rs 4f5a16b7d81a75577aea099c0c5fc62aa4f45607e99dab9c84ecd97806e22626
manager/mod.rs         b1b9eaf8fde76eee17daef3ebfddd03ba8e61097af79caf08a4b5c8ad174d4e0
native_dag.rs          7b4413c0406ce1360c0e4a08de7eb5a8c2fd39795f28a2f7081c48a9a533cb25
lib.rs                 e6311481b7de3c260fc9ca20029f91fb6625c248302cb6eb800fcbd538f9fdf7
main.rs                270bb2f6422d5c68295ac28c15659b6af46a6c97e2443a3e1eb8f59f887ccbe7
```

Parent Core files remain byte-identical:

```text
native_authority_registry.rs
aec310beb11cc5eeb38fdfda876ff3da91d8c53f4f30af814b5f7a9ae2ba89bc

native_contract_catalog.rs
3162856786b151f31e8301e1bbd5db258721583de2ba92e08dde9af0f3cab2b6
```

## 13. Legacy migration regression

All 80 active legacy validators were rerun using the compile-chain no-argument invocation surface.

```text
ordinals 00..55 = 56 PASS
ordinal 56 = FAIL
ordinals 57..79 = 23 PASS
TOTAL = 79 PASS / 1 FAIL
FirstFailureOrdinal = 56
```

Ordinal 56 remains the unchanged 15C-R1 scheduler-hash failure:

```text
105 total
102 PASS
3 FAIL
```

Legacy migration remains:

```text
LegacyMigrationProjectedCount = 26
LegacyMigrationFrozenCount = 54
```

and is not a native scheduling input.

## 14. Static bake qualification

```text
Hard root projection = 8 Active + 3 Qualification roots
Hard scheduling nodes = 13
Hard scheduling edges = 17
Runtime edges = 10
Control edges = 7
Hard evidence edges = 0
Evidence provenance relations = 52
Authority hard-DAG cycle count = 0
Contract DAG cycle count = 0
Scheduled Superseded authority count = 0
External boundary scheduled count = 0
Initial Ready = 3
Initial Pending = 10
Initial Blocked = 0
Legacy oracle = 79 PASS / 1 FAIL
Invalid Rust unicode-escape scan = 0
Forbidden baked pycache/pyc/pyo = 0
```

The bake environment has no usable Cargo/Rust toolchain, so physical cargo check/test PASS is not claimed.

## 15. CLI and expected diagnostic truth

Diagnostic DAG:

```powershell
cargo run -p ash_control_runtime -- `
  native-authority-dag `
  --repo-root . `
  --mode diagnostic-full-dag
```

Fail-fast mode:

```powershell
cargo run -p ash_control_runtime -- `
  native-authority-dag `
  --repo-root . `
  --mode fail-fast
```

Expected diagnostic output includes:

```text
ASH_CONTROL_RUNTIME_NATIVE_AUTHORITY_DAG_VALID=true
workflowMode=DiagnosticFullDag
currentExecutionAuthorityRootCount=8
qualificationLaneRootCount=3
scheduledActiveAuthorityCount=10
unscheduledActiveAuthorityCount=27
scheduledQualificationAuthorityCount=3
unscheduledQualificationAuthorityCount=3
scheduledSupersededAuthorityCount=0
authorityDagNodeCount=13
authorityDagEdgeCount=17
runtimePrerequisiteEdgeCount=10
controlPrerequisiteEdgeCount=7
evidenceParentSchedulingEdgeCount=0
evidenceProvenanceRelationCount=52
scheduledEvidenceRelationCount=23
unscheduledCurrentEvidenceRelationCount=29
supersededHistoricalEvidenceRelationCount=0
authorityDagCycleCount=0
missingAuthorityDependencyCount=0
selfAuthorityDependencyCount=0
scheduledContractCount=13
unscheduledContractCount=30
contractDagCycleCount=0
crossLaneHardDependencyCount=3
initialReadyAuthorityCount=3
initialPendingAuthorityCount=10
usesLegacyValidatorId=false
usesLegacyOrdinal=false
usesPythonGateOrdering=false
evidenceExecutionCount=0
productionAuthorityClaimed=false
```

Expected DiagnosticFullDag receipt hash:

```text
bfc5dc7dd48d01decf501baffdda51b50e82a509f4aff12c9c3bb05b90d883a0
```

## 16. Required local qualification

```powershell
cargo check -p ash_control_runtime
cargo test -p ash_control_runtime --no-run
cargo test -p ash_control_runtime

cargo run -p ash_control_runtime -- `
  native-authority-registry `
  --repo-root .

cargo run -p ash_control_runtime -- `
  native-contract-catalog `
  --repo-root .

cargo run -p ash_control_runtime -- `
  native-authority-dag `
  --repo-root . `
  --mode diagnostic-full-dag

cargo run -p ash_control_runtime -- `
  cf1-semantic-shadow `
  --repo-root . `
  --mode diagnostic-full-matrix
```

The legacy semantic-shadow remains expected to exit 1 because 54 migration gates are Frozen.

## 17. Mandatory gates

```text
PASS_NATIVE05_PARENT_NATIVE03_VALID
PASS_NATIVE05_PARENT_NATIVE04_VALID
PASS_NATIVE05_AUTHORITY_REGISTRY_DIGEST_UNCHANGED
PASS_NATIVE05_CONTRACT_CATALOG_DIGEST_UNCHANGED
PASS_NATIVE05_INVARIANT_CATALOG_DIGEST_UNCHANGED
PASS_NATIVE05_CURRENT_EXECUTION_ROOTS_8
PASS_NATIVE05_QUALIFICATION_ROOTS_3
PASS_NATIVE05_NO_LEGACY_ORDINAL_SCHEDULING
PASS_NATIVE05_NO_0_TO_79_EXECUTION_ORDER
PASS_NATIVE05_NO_PYTHON_GATE_ORDERING
PASS_NATIVE05_RUNTIME_PARENT_HARD_PROJECTION
PASS_NATIVE05_CONTROL_PARENT_HARD_PROJECTION
PASS_NATIVE05_EVIDENCE_PARENT_PROVENANCE_PROJECTION
PASS_NATIVE05_EVIDENCE_PARENT_HARD_EDGE_ZERO
PASS_NATIVE05_DIRECT_PARENT_NOT_SCHEDULING_EDGE
PASS_NATIVE05_SUPERSEDES_NOT_SCHEDULING_EDGE
PASS_NATIVE05_DOES_NOT_SUPERSEDE_NOT_SCHEDULING_EDGE
PASS_NATIVE05_AUTHORITY_DAG_13_NODES_17_EDGES
PASS_NATIVE05_AUTHORITY_DAG_CYCLE_ZERO
PASS_NATIVE05_MISSING_AUTHORITY_DEP_ZERO
PASS_NATIVE05_SELF_AUTHORITY_DEP_ZERO
PASS_NATIVE05_SUPERSEDED_SCHEDULED_ZERO
PASS_NATIVE05_EXTERNAL_BOUNDARY_SCHEDULED_ZERO
PASS_NATIVE05_CONTRACT_DAG_13_NODES
PASS_NATIVE05_EXPLICIT_CONTRACT_EDGE_ZERO
PASS_NATIVE05_CONTRACT_DAG_CYCLE_ZERO
PASS_NATIVE05_CONTRACT_OWNER_MISMATCH_ZERO
PASS_NATIVE05_NO_FAKE_CROSS_CONTRACT_DEPENDENCY
PASS_NATIVE05_ACTIVE_QUALIFICATION_LANE_SEPARATION
PASS_NATIVE05_DEPENDENCY_DERIVED_READY
PASS_NATIVE05_DEPENDENCY_DERIVED_BLOCKED
PASS_NATIVE05_DEPENDENCY_DERIVED_NOT_EXECUTED
PASS_NATIVE05_BLOCKED_NOT_EQUAL_FAILFAST_NOT_EXECUTED
PASS_NATIVE05_NATIVE_FAILFAST_STATE_MACHINE
PASS_NATIVE05_DIAGNOSTIC_FULL_DAG_STATE_MACHINE
PASS_NATIVE05_ORCHESTRATOR_SCHEDULING_SSOT
PASS_NATIVE05_MANAGER_CONTRACT_LIFECYCLE
PASS_NATIVE05_FACTORY_NO_SCHEDULING_AUTHORITY
PASS_NATIVE05_DEVICE_NO_SCHEDULING_AUTHORITY
PASS_NATIVE05_EVIDENCE_EXECUTION_ZERO
PASS_NATIVE05_LEGACY_MIGRATION_26_54_PRESERVED
PASS_NATIVE05_LEGACY_ORACLE_79_1
PASS_NATIVE05_FIRST_LEGACY_FAILURE_56
PASS_NATIVE05_15C_105_102_3
PASS_NATIVE05_NO_104_GATE_MIGRATION
PASS_NATIVE05_NO_CARGO_AUTHORITY_MIGRATION
PASS_NATIVE05_NO_CF1_V2_MUTATION
PASS_NATIVE05_NO_PRODUCTION_AUTHORITY
```

Physical local gates remain pending for cargo check/test and the two mode-specific receipt hashes.

## 18. Hard HOLD conditions

```text
Legacy ordinal influences native scheduling
Python validator ID appears in native authority DAG
0 -> 79 order is reused in native lane
Evidence parent is blindly promoted to hard scheduling precedence
Direct parent becomes execution prerequisite
Supersedes or does-not-supersede becomes execution prerequisite
External negative boundary becomes executable node
Current execution root count != 8
Scheduled Superseded authority count > 0
Authority hard-DAG cycle > 0
Missing dependency is silently ignored
QualificationOnly authority is promoted to Active lane
Authority relation is fabricated as a contract-to-contract dependency
Manager mutates graph topology
Factory or Device decides authority readiness
Fail-fast overwrites actual dependency-blocked causality
Contract is marked Satisfied without evidence execution
NATIVE-03 or NATIVE-04 digest drifts
Legacy 26/54 changes
Production authority is claimed
```

## 19. Next patch

```text
ASH-CONTROL-RUNTIME-NATIVE-TYPED-EVIDENCE-FACTORY-AND-DEVICE-06
```

NATIVE-06 must consume NATIVE-04 NativeEvidenceRequirement values and materialize immutable evidence plans without granting Factory or Device authority over membership, scheduling or contract truth.

```text
Core Invariant
    -> Orchestrator scheduling admission
    -> Manager contract lifecycle
    -> Factory immutable EvidencePlan
    -> Device generic physical observation
    -> typed EvidenceResult
```

NATIVE-05 deliberately stops before actual evidence execution.
