# ASH-CONTROL-RUNTIME-NATIVE-TYPED-EVIDENCE-FACTORY-AND-DEVICE-06

## Status

```text
Patch ID: ASH-CONTROL-RUNTIME-NATIVE-TYPED-EVIDENCE-FACTORY-AND-DEVICE-06
Parent: ASH-CONTROL-RUNTIME-NATIVE-AUTHORITY-DAG-ORCHESTRATION-05
Role: typed native evidence specification, immutable plan materialization, observation/verdict authority separation
Production authority: false
Production invariant evidence execution: 0
Legacy semantic coverage expansion: false
Python validator translation: forbidden
```

## 1. Physical parent identity

NATIVE-03/04/05 identities remain unchanged:

```text
NativeAuthorityRegistryDigest =
cfdf654dffc8182a49e67202615a6b874e3568593e4d8bcb20617cbee5ae91ee

NativeContractCatalogDigest =
edbb1f1bf03c627007ff2da05e9a823e5bf2938e08ef2a74d0a509c76d5866cd

NativeInvariantCatalogDigest =
ea05cfbf4b71dc8edb5dbf13b9a9d6c80fcea2b6a05dba3dba62f1731e4061a6

AuthorityExecutionDagDigest =
559c72185b854c2214880473f53980d8e217f83adc9308f282603b649b55528f

ContractExecutionDagDigest =
e8e8a3d4f19a914c0cdd75401a2528ad2778b28934f85474e40ef6ef0688a22d
```

NATIVE-05 physical mode receipts are already closed:

```text
DiagnosticFullDag = bfc5dc7dd48d01decf501baffdda51b50e82a509f4aff12c9c3bb05b90d883a0
FailFast          = 0fec8d5f70014a1e5ac72c45894de6c7614f411e894e0497d21585da529233c0
```

## 2. Authority split

```text
Core
  invariant law
  evidence kind / phase
  evidence request identity
  typed expectation

Orchestrator
  authority admission / dependency scheduling only

Manager
  evidence reduction
  invariant disposition
  contract lifecycle

Factory
  deterministic immutable EvidencePlan only

Device
  generic typed observation only
```

Hard rules:

```text
Observation != Verdict
Device success != Invariant PASS
Infrastructure failure != Semantic FAIL
Unsupported capability != Semantic FAIL
Factory cannot emit PASS/FAIL
Device cannot emit Satisfied/Failed
Orchestrator cannot evaluate evidence semantics
```

## 3. Core EvidenceSpec catalog

New Core module:

```text
crates/ash_core/src/native_evidence_spec_catalog.rs
```

NATIVE-04 currently owns 84 Defined invariants. NATIVE-06 deterministically projects one primary typed EvidenceSpecification per Defined invariant.

```text
DefinedInvariantCount = 84
EvidenceSpecCount = 84
EvidenceSpecMissingCount = 0
EvidenceSpecUnresolvedCount = 0
DuplicateEvidenceSpecCount = 0
MissingInvariantForEvidenceSpecCount = 0
EvidenceKindMismatchCount = 0
EvidencePhaseMismatchCount = 0
```

The specification is not `GenericCheck / MustPass`. It binds:

```text
Invariant ID
Owner Contract
Owner Authority
NATIVE-04 EvidenceKind
NATIVE-04 EvidencePhase
Invariant-specific operation key
Typed expectation class
Illegal-state identity
```

Expectation vocabulary is typed by NATIVE-04 invariant semantics:

```text
StateLegal
TransitionLegal
NonRegressing
Fresh
Exclusive
SingleOwner
AdmissionLegal
CanonicallyOrdered
RoutingDisjoint
CommitConsistent
RecoverySafe
ProvenanceConsistent
StructuralBoundaryIntact
QualificationSatisfied
```

Concrete domain probe implementation remains NATIVE-07 work. NATIVE-06 defines the typed request/expectation ABI without fabricating a production observation.

## 4. EvidenceKind preservation

Exact NATIVE-04 evidence distribution is preserved:

```text
TypedReceipt             = 25
NativeStateTransition    = 21
NativeBehavior           = 16
TypedArtifact            = 11
RustStructure            = 4
CargoSurface             = 2
ProcessBehavior           = 2
PhysicalGpuQualification = 2
FilesystemBehavior       = 1
WgslStructure            = 0
```

No evidence kind is silently downgraded or substituted.

## 5. EvidenceSpec identity seal

```text
NativeEvidenceSpecCatalogDigest =
6bd5f82066902173e7792b26d8ca8664d46b97c337aacf634b322d18335b5e02
```

The catalog contains no canonical dependency on Python path/SHA, expected legacy disposition, legacy ordinal, TextFind, RegexSearch or StaticComprehension.

## 6. Factory plan materialization

New Factory module:

```text
crates/ash_control_runtime/src/factory/native_evidence.rs
```

Factory materializes:

```text
NativeEvidenceSpecification
+ OrchestrationProgramDigest
+ Planning Capability ABI
-> immutable NativeEvidencePlan
```

Plan binds:

```text
Authority ID
Contract ID
Invariant ID
EvidenceKind
EvidencePhase
Device operation
Typed expectation
OrchestrationProgramDigest
PlanDigest
```

Factory contains no semantic verdict type or invariant PASS/FAIL branch.

Planning capability ABI represents operation-schema materializability, not local physical execution availability. All ten EvidenceKind operation families have a planning representation:

```text
PlanningCapabilityCount = 10
DeviceCapabilityDigest =
1fa7526b8eacad8a374a5660e9094408c11a70c8daaf5736107bbbe90e314d57
```

Physical execution availability is deliberately deferred to NATIVE-07/device admission and must not be inferred from this planning count.

## 7. Catalog plans versus current scheduled plans

Full Core scope:

```text
CatalogMaterializedEvidencePlanCount = 84
```

Current NATIVE-05 root projection:

```text
ScheduledAuthorityCount = 13
ScheduledContractCount = 13
ScheduledInvariantCount = 27
ScheduledMaterializedEvidencePlanCount = 27
```

The other 57 invariant plans are catalog-materializable but are not current execution plans.

## 8. Orchestration-generation binding

Evidence plans bind the NATIVE-05 orchestration program digest. Therefore DiagnosticFullDag and FailFast have distinct plan identities.

DiagnosticFullDag:

```text
OrchestrationProgramDigest =
4092cc05891ea5913a6c5cc0bc617044f5f3271e52413227bfecb8aca5c6c8fb

NativeEvidencePlanCatalogDigest =
b66159f5bddd4268bfda49a7ca745f91b62b960918f134821c253cf5df7c2a6d

ScheduledEvidencePlanDigest =
cb5340c66ad5fc7e163e58058e89e87eb3d1cb8abb58bc154ecc42d6dd8a1ad2
```

FailFast:

```text
OrchestrationProgramDigest =
b8b34cdc1ea651b0d7f07d7c34d1fbd2ad75918a3654cc1772984ca4fe9db40e

NativeEvidencePlanCatalogDigest =
fa5c7cbaec434ba9ca0913e4804c23d67fecc486227744f20d2714c422334c7f

ScheduledEvidencePlanDigest =
4ef4d279fb4468aa88997c47e2a635a63ec9765f1edf48e6c8b22194fcbb8750
```

A plan produced under another orchestration digest is stale and cannot be silently rebound.

## 9. Device observation boundary

New Device module:

```text
crates/ash_control_runtime/src/device/native_evidence.rs
```

Device ABI accepts only a generic NativeDeviceOperation and returns NativeEvidenceObservation or NativeDeviceError.

It does not receive NativeInvariantId as a policy argument and contains no invariant-ID switch. It does not know contract satisfaction or workflow fail-fast policy.

Typed observation facts are transport facts only:

```text
StateLegal(bool)
TransitionLegal(bool)
NonRegressing(bool)
Fresh(bool)
Exclusive(bool)
SingleOwner(bool)
AdmissionLegal(bool)
CanonicallyOrdered(bool)
RoutingDisjoint(bool)
CommitConsistent(bool)
RecoverySafe(bool)
ProvenanceConsistent(bool)
StructuralBoundaryIntact(bool)
QualificationSatisfied(bool)
```

The Device does not know which boolean value the Core expectation requires. Manager performs that comparison.

NATIVE-06 provides a FixtureNativeEvidenceDevice only for framework qualification. Production domain devices/probes are NATIVE-07 work.

## 10. Manager reducer

New Manager module:

```text
crates/ash_control_runtime/src/manager/native_evidence.rs
```

Reducer:

```text
EvidencePlan + Typed Observation
-> NativeInvariantEvidenceDisposition
```

Typed dispositions:

```text
Satisfied
Failed
HeldUnsupportedCapability
FailedInfrastructure
StaleEvidence
```

Rules:

```text
Observation matches typed expectation -> Satisfied
Observation contradicts typed expectation -> Failed
Capability unavailable -> HeldUnsupportedCapability
Timeout / invocation / malformed observation -> FailedInfrastructure
Plan identity mismatch -> StaleEvidence
```

Infrastructure failure is never converted to semantic invariant failure.

## 11. Reducer qualification fixtures

The NATIVE-06 runtime command contains five framework cases:

```text
matching observation -> Satisfied
contradicting observation -> Failed
stale plan binding -> StaleEvidence
capability unavailable -> HeldUnsupportedCapability
timeout -> FailedInfrastructure
```

Expected local receipt:

```text
ReducerFixtureCaseCount = 5
ReducerFixturePassCount = 5
ReducerFixtureFailCount = 0
DeviceFixtureExecutionCount = 2
```

These are framework fixtures, not production invariant evidence.

```text
ProductionInvariantEvidenceExecutionCount = 0
EvidenceExecutionClosed = false
ProductionAuthorityClaimed = false
```

## 12. Authority leak gates

Expected local receipt remains:

```text
FactorySemanticVerdictCount = 0
DeviceSemanticVerdictCount = 0
DeviceAuthorityPolicyReferenceCount = 0
DeviceContractPolicyReferenceCount = 0
DeviceInvariantPolicyReferenceCount = 0
OrchestratorEvidenceSemanticBranchCount = 0
```

Static bake inspection found no NativeInvariantId/LegacyValidator/expected_disposition/legacy_ordinal/rustpython/TextFind/RegexSearch policy branch in the new Factory or Device implementation.

## 13. Legacy migration isolation

Legacy semantic programs are byte-identical:

```text
generated.rs       e7f2cc33388bec593647dc896cc51ca2026fb0e23378fc043eb23cf5851e7f74
generated_r1ar1.rs c96911569939dddefaa0abd054d90e3bce76fa360b467d605591fdd4534fb80f
generated_r1ar2.rs 8425b9455ed67ee5b3c92c1492a2a11a9b2368d53be4c6013e025f74adcc8cc1
generated_r2a.rs   af4dc3ce75cbcbf9841a65992bcb04362b52055318df3dfe8639e3243616ce18
```

Migration counts remain:

```text
LegacyActiveGateCount = 80
LegacyMigrationProjectedCount = 26
LegacyMigrationFrozenCount = 54
```

NATIVE-06 changed-source/repo-query impact analysis found 36 affected active legacy gates. All 36 were physically rerun and passed. The remaining 44 active gates have no changed exact-input or repo-query exposure relative to the physically closed NATIVE-05 parent. The known ordinal-56 gate is in that unchanged set and was separately rerun:

```text
15C-R1 = 3 / 105 failures
```

with the same three scheduler-hash failures. Therefore NATIVE-06 introduces no new legacy disposition. A fresh monolithic 80-validator run is not claimed from the bake environment.

## 14. Changed source surface

New:

```text
crates/ash_core/src/native_evidence_spec_catalog.rs
crates/ash_control_runtime/src/factory/native_evidence.rs
crates/ash_control_runtime/src/device/native_evidence.rs
crates/ash_control_runtime/src/manager/native_evidence.rs
crates/ash_control_runtime/src/native_evidence.rs
```

Modified:

```text
crates/ash_core/src/lib.rs
crates/ash_control_runtime/src/factory/mod.rs
crates/ash_control_runtime/src/device/mod.rs
crates/ash_control_runtime/src/manager/mod.rs
crates/ash_control_runtime/src/lib.rs
crates/ash_control_runtime/src/main.rs
```

SHA256:

```text
native_evidence_spec_catalog.rs b967b17d99ed48f8a586b7b20fa3202bafaa9c0c16e347c2129d02db7a86f463
ash_core/lib.rs                 ef871c03974db9c19a8e8ed06c7de98eb3ae4d69401f406fbca83fc5a9149646
factory/native_evidence.rs      756e47a811c2480a579bb91c996eacdd6ae9b1824be89a67b6a0703dd48c24dd
factory/mod.rs                  b1635c0e26f160673736b647ab31ef21845555104b139749c24b28dacfb57995
device/native_evidence.rs       1a599c73791982e924a2cc57452e8e672cc9347a63c74645368c3eb8d1d34521
device/mod.rs                   3496dc06092216e46b354b63349e2bd37bae4d2c67fc814ac1f72cb3a62e22ee
manager/native_evidence.rs      1f867d2c9f92e7439eae8753eae139981be63ceed5647ecbbc3c4114c4c60349
manager/mod.rs                  541c20c185b1293ec0ada3ce7dd73178ef8b620e5116a0a6a5465266fab98d38
native_evidence.rs              fb79c2412c40447134f31cb8c507b607f029c3c08efe314790b3f65db68e720f
ash_control_runtime/lib.rs      37de29bb5a154dcb9f3fba5d58960c65a31c59f3e1f58b350a8ea7f99f70091f
ash_control_runtime/main.rs     a02f564985974d742e6a5ba56f594f3dc24a73a208ec2d240145273eb29826de
```

## 15. Staged expected physical receipts

DiagnosticFullDag expected receipt hash:

```text
3cd02abb2c0ef720e3ee30cdfb0911c64625b57364fd90b8de42fa2150e1c686
```

FailFast expected receipt hash:

```text
801793d4b4e259d4bc4f957174a60bf6d845a6476d9cd82a6aa2c8c0ea7bb543
```

These hashes are staged deterministic expectations and must be physically observed from local Rust before being treated as closed.

## 16. Expected CLI truth

```text
ASH_CONTROL_RUNTIME_NATIVE_TYPED_EVIDENCE_VALID=true

definedInvariantCount=84
evidenceSpecCount=84
evidenceSpecMissingCount=0
evidenceSpecUnresolvedCount=0
duplicateEvidenceSpecCount=0
evidenceKindMismatchCount=0
evidencePhaseMismatchCount=0

scheduledAuthorityCount=13
scheduledContractCount=13
scheduledInvariantCount=27

catalogMaterializedEvidencePlanCount=84
scheduledMaterializedEvidencePlanCount=27
heldEvidencePlanCount=0
unsupportedCapabilityPlanCount=0
planningCapabilityCount=10

factorySemanticVerdictCount=0
deviceSemanticVerdictCount=0

reducerFixtureCaseCount=5
reducerFixturePassCount=5
reducerFixtureFailCount=0
deviceFixtureExecutionCount=2
productionInvariantEvidenceExecutionCount=0

usesLegacyValidatorId=false
usesLegacyOrdinal=false
usesExpectedLegacyDisposition=false

evidencePlanningClosed=true
evidenceExecutionClosed=false
productionAuthorityClaimed=false
```

## 17. Physical Rust qualification status

The bake environment has no usable cargo/rustc/rustfmt, so no physical Rust compile/test claim is made here.

Run locally:

```powershell
cargo check -p ash_control_runtime
cargo test -p ash_control_runtime --no-run
cargo test -p ash_control_runtime

cargo run -p ash_control_runtime -- `
  native-evidence-plans `
  --repo-root . `
  --mode diagnostic-full-dag

cargo run -p ash_control_runtime -- `
  native-evidence-plans `
  --repo-root . `
  --mode fail-fast
```

Parent regressions should also remain closed:

```powershell
cargo run -p ash_control_runtime -- native-authority-registry --repo-root .
cargo run -p ash_control_runtime -- native-contract-catalog --repo-root .
cargo run -p ash_control_runtime -- native-authority-dag --repo-root . --mode diagnostic-full-dag
```

## 18. Mandatory gates

```text
PASS_NATIVE06_PARENT_NATIVE03_DIGEST_UNCHANGED
PASS_NATIVE06_PARENT_NATIVE04_DIGEST_UNCHANGED
PASS_NATIVE06_PARENT_NATIVE05_DAG_DIGEST_UNCHANGED
PASS_NATIVE06_EVIDENCE_SPEC_84_84
PASS_NATIVE06_EVIDENCE_SPEC_MISSING_ZERO
PASS_NATIVE06_EVIDENCE_SPEC_UNRESOLVED_ZERO
PASS_NATIVE06_EVIDENCE_KIND_EXACT
PASS_NATIVE06_EVIDENCE_PHASE_EXACT
PASS_NATIVE06_NO_STRING_DSL
PASS_NATIVE06_FACTORY_PLAN_ONLY
PASS_NATIVE06_FACTORY_VERDICT_ZERO
PASS_NATIVE06_DEVICE_OBSERVATION_ONLY
PASS_NATIVE06_DEVICE_VERDICT_ZERO
PASS_NATIVE06_MANAGER_REDUCER_AUTHORITY
PASS_NATIVE06_OBSERVATION_NOT_VERDICT
PASS_NATIVE06_INFRA_FAILURE_NOT_SEMANTIC_FAILURE
PASS_NATIVE06_PLAN_ORCHESTRATION_BINDING
PASS_NATIVE06_NO_DYNAMIC_EVIDENCE_FALLBACK
PASS_NATIVE06_SCHEDULED_INVARIANT_27
PASS_NATIVE06_CATALOG_PLAN_84
PASS_NATIVE06_SCHEDULED_PLAN_27
PASS_NATIVE06_PRODUCTION_EVIDENCE_EXECUTION_ZERO
PASS_NATIVE06_LEGACY_MIGRATION_26_54_PRESERVED
PASS_NATIVE06_IMPACTED_LEGACY_GATE_36_36
PASS_NATIVE06_15C_105_102_3
PASS_NATIVE06_NO_PRODUCTION_AUTHORITY
```

## 19. Hard HOLD

```text
Factory returns semantic PASS/FAIL
Device returns Satisfied/Failed
Device branches on NativeInvariantId policy
Orchestrator evaluates evidence expectation
EvidenceKind silently changes from NATIVE-04
Plan lacks Authority/Contract/Invariant binding
Plan is reused across orchestration digest drift
Infrastructure error is reported as semantic Failed
Unsupported execution capability is reported as semantic Failed
Production evidence is claimed from fixture execution
NATIVE-03/04/05 identity drifts
Legacy 26/54 changes
Production authority is claimed
```

## 20. Next patch

```text
ASH-CONTROL-RUNTIME-NATIVE-DOMAIN-PROBE-AND-EVIDENCE-EXECUTION-CLOSURE-07
```

NATIVE-07 must replace fixture-only observation sources with actual typed native domain probes and physical qualification devices while preserving the NATIVE-06 authority split:

```text
Core law
-> Orchestrator admission
-> Manager lifecycle
-> Factory immutable plan
-> Device observation
-> Manager reduction
```
