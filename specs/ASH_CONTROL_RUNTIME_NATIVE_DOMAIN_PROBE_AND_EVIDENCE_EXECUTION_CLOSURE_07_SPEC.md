# ASH-CONTROL-RUNTIME-NATIVE-DOMAIN-PROBE-AND-EVIDENCE-EXECUTION-CLOSURE-07

## Status

```text
Patch ID: ASH-CONTROL-RUNTIME-NATIVE-DOMAIN-PROBE-AND-EVIDENCE-EXECUTION-CLOSURE-07
Parent: ASH-CONTROL-RUNTIME-NATIVE-TYPED-EVIDENCE-FACTORY-AND-DEVICE-06
Role: bind the current 27 scheduled native evidence plans to typed actual-native observation producers and execute fail-closed reduction
Production authority: false
Fixture production evidence: forbidden
Synthetic production evidence: forbidden
Legacy oracle production evidence: forbidden
Python validator execution: forbidden
```

## 1. Parent physical truth

NATIVE-06 is physically closed for DiagnosticFullDag:

```text
ASH_CONTROL_RUNTIME_NATIVE_TYPED_EVIDENCE_VALID=true
receiptHash=3cd02abb2c0ef720e3ee30cdfb0911c64625b57364fd90b8de42fa2150e1c686
DefinedInvariantCount=84
EvidenceSpecCount=84
ScheduledAuthorityCount=13
ScheduledContractCount=13
ScheduledInvariantCount=27
CatalogMaterializedEvidencePlanCount=84
ScheduledMaterializedEvidencePlanCount=27
EvidencePlanningClosed=true
EvidenceExecutionClosed=false
ProductionAuthorityClaimed=false
```

Parent identity seals remain unchanged:

```text
NativeAuthorityRegistryDigest = cfdf654dffc8182a49e67202615a6b874e3568593e4d8bcb20617cbee5ae91ee
NativeContractCatalogDigest = edbb1f1bf03c627007ff2da05e9a823e5bf2938e08ef2a74d0a509c76d5866cd
NativeInvariantCatalogDigest = ea05cfbf4b71dc8edb5dbf13b9a9d6c80fcea2b6a05dba3dba62f1731e4061a6
NativeEvidenceSpecCatalogDigest = 6bd5f82066902173e7792b26d8ca8664d46b97c337aacf634b322d18335b5e02
AuthorityExecutionDagDigest = 559c72185b854c2214880473f53980d8e217f83adc9308f282603b649b55528f
ContractExecutionDagDigest = e8e8a3d4f19a914c0cdd75401a2528ad2778b28934f85474e40ef6ef0688a22d
Diagnostic ScheduledEvidencePlanDigest = cb5340c66ad5fc7e163e58058e89e87eb3d1cb8abb58bc154ecc42d6dd8a1ad2
```

## 2. Scheduled evidence distribution

The actual NATIVE-05/06 current-root projection contains exactly 27 invariants:

```text
NativeStateTransition = 9
TypedReceipt = 9
NativeBehavior = 4
ProcessBehavior = 2
TypedArtifact = 1
FilesystemBehavior = 1
RustStructure = 1
CargoSurface = 0
PhysicalGpuQualification = 0
WgslStructure = 0
Total = 27
```

NATIVE-07 implements only the current scheduled evidence surface. It does not fabricate execution of the 57 unscheduled invariants.

## 3. Critical architecture finding

`ash_control_runtime` intentionally does not depend on `base_train .

```text
ash_control_runtime -> ash_core
ash_control_runtime X-> base_train
```

The actual production state machines and policy implementations live in the base-train/runtime domain. Adding `base_train` as a control-runtime dependency merely to make NATIVE-07 probes pass would invert the established authority boundary and recreate a shadow-validator/compiler architecture.

Therefore NATIVE-07 does not link production algorithms into the control runtime.

Instead it introduces an explicit typed observation producer boundary:

```text
Production native domain
  -> typed native observation envelope
  -> Device observation
  -> Manager reducer
```

The control runtime never invents the observation.

## 4. Probe registry

New runtime modules:

```text
crates/ash_control_runtime/src/probe/mod.rs
crates/ash_control_runtime/src/probe/registry.rs
```

Every scheduled NATIVE-06 operation key receives exactly one probe binding.

```text
ScheduledInvariantCount = 27
ScheduledProbeBoundInvariantCount = 27
ScheduledProbeUnboundInvariantCount = 0
```

Probe identity is derived from the native operation key, not from a legacy validator, path or ordinal.

Registry validation rejects:

```text
duplicate probe IDs
duplicate operation keys
unbound scheduled plans
legacy validator/path/python bindings
```

## 5. Typed external-native observation protocol

New Device module:

```text
crates/ash_control_runtime/src/device/native_domain_probe.rs
```

Observation schema:

```text
ash.control_runtime.native_domain_probe_observation.v1
```

Envelope:

```text
schema
operation_key
producer_kind
producer_identity
producer_receipt_digest
fact
```

Allowed producer kinds:

```text
NativeRuntime
NativeTypedReceipt
NativeTypedArtifact
NativeFilesystemProbe
NativeProcessProbe
NativeStructureProbe
```

There is no Fixture, Synthetic or LegacyOracle producer kind in the production observation ABI.

Default observation directory:

```text
artifacts/control_runtime/native_domain_probe_observations/
```

Each operation key maps deterministically to one JSON observation filename by replacing non-alphanumeric characters with `_` and appending `.json`.

A missing observation is not semantic failure and is not silently replaced. It is reduced through the existing NATIVE-06 unsupported-capability/HOLD path.

## 6. Observation/verdict authority remains unchanged

```text
Factory = immutable plan only
Device = physical/typed observation only
Manager = semantic reduction only
Orchestrator = authority scheduling only
```

NATIVE-07 preserves:

```text
FactorySemanticVerdictCount = 0
DeviceSemanticVerdictCount = 0
```

An observation file contains a typed observation fact, not an invariant verdict. The Manager still compares the observation fact against the Core-owned NATIVE-06 expectation.

## 7. Execution coordinator

New module:

```text
crates/ash_control_runtime/src/native_evidence_execution.rs
```

Execution sequence:

```text
NATIVE-06 parent validation
-> rebuild current NATIVE-05 program
-> rebuild current scheduled NATIVE-06 plans
-> verify scheduled plan digest
-> build/validate 27-entry probe registry
-> preflight/read typed native observations
-> Device observation envelope validation
-> Manager reduction
-> strict execution closure calculation
```

The 27-plan identity must remain identical to NATIVE-06.

## 8. Execution validity versus execution closure

NATIVE-07 deliberately separates registry validity from evidence closure.

```text
NativeProbeRegistryValid
CurrentScheduledEvidenceExecutionClosed
NativeDomainEvidenceValid
```

Registry validity means the 27 scheduled plans have deterministic non-legacy probe bindings.

Execution closure requires all 27 actual native observations to exist and reduce successfully:

```text
ActualNativeInvariantEvidenceExecutionCount = 27
ScheduledInvariantSatisfiedCount = 27
ScheduledInvariantFailedCount = 0
ScheduledInvariantHeldCount = 0
ScheduledInvariantInfrastructureFailureCount = 0
ScheduledInvariantStaleCount = 0
```

Only then:

```text
CurrentScheduledEvidenceExecutionClosed=true
NativeDomainEvidenceValid=true
```

## 9. Initial physical blocker is explicit

At bake time there are no typed producer observation envelopes for the new NATIVE-07 operation-key protocol. This is not repaired by fixtures, source-string checks, expected-value echo or an `ash_control_runtime -> base_train` dependency.

Therefore the expected first local `native-evidence-execute` run is fail-closed until the actual native domain producers emit those envelopes.

Expected initial shape before producer adoption:

```text
NativeProbeRegistryValid=true
ScheduledProbeBoundInvariantCount=27
ScheduledProbeUnboundInvariantCount=0
RequiredObservationCount=27
AvailableNativeObservationCount=0
MissingNativeObservationCount=27
ActualNativeInvariantEvidenceExecutionCount=0
ScheduledInvariantHeldCount=27
CurrentScheduledEvidenceExecutionClosed=false
NativeDomainEvidenceValid=false
ProductionAuthorityClaimed=false
```

This is a truthful integration HOLD, not a NATIVE-07 PASS.

## 10. Why no shadow implementation was added

Forbidden repairs:

```text
observation = expected value
reimplement base_train state machine inside ash_control_runtime
source grep standing in for NativeBehavior
JSON text grep standing in for TypedReceipt
path existence standing in for TypedArtifact
link base_train into control runtime only for probe access
fixture observation counted as actual native evidence
```

The next implementation work inside the NATIVE-07 lineage is producer adoption in the actual owning native domains, not a second copy of their logic inside the control plane.

## 11. CLI

```powershell
cargo run -p ash_control_runtime -- `
  native-evidence-execute `
  --repo-root . `
  --mode diagnostic-full-dag
```

Optional explicit observation root:

```powershell
cargo run -p ash_control_runtime -- `
  native-evidence-execute `
  --repo-root . `
  --mode diagnostic-full-dag `
  --observation-root .\artifacts\control_runtime\native_domain_probe_observations
```

FailFast uses the corresponding NATIVE-06 FailFast plan generation:

```powershell
cargo run -p ash_control_runtime -- `
  native-evidence-execute `
  --repo-root . `
  --mode fail-fast
```

## 12. Receipt fields

Schema:

```text
ash.control_runtime.native_domain_evidence_execution.v1
```

Key fields:

```text
nativeProbeRegistryDigest
scheduledInvariantCount
scheduledProbeBoundInvariantCount
scheduledProbeUnboundInvariantCount
duplicateProbeIdCount
duplicateOperationKeyCount
legacyProbeBindingCount
requiredObservationCount
availableNativeObservationCount
missingNativeObservationCount
actualNativeInvariantEvidenceExecutionCount
scheduledInvariantSatisfiedCount
scheduledInvariantFailedCount
scheduledInvariantHeldCount
scheduledInvariantInfrastructureFailureCount
scheduledInvariantStaleCount
fixtureObservationCount
syntheticObservationCount
legacyOracleObservationCount
pythonValidatorExecutionCount
factorySemanticVerdictCount
deviceSemanticVerdictCount
nativeProbeRegistryValid
currentScheduledEvidenceExecutionClosed
catalogWideEvidenceExecutionClosed
nativeDomainEvidenceValid
productionAuthorityClaimed
```

## 13. Closure law

```text
CurrentScheduledEvidenceExecutionClosed =
    ScheduledProbeUnboundInvariantCount == 0
 && ActualNativeInvariantEvidenceExecutionCount == 27
 && ScheduledInvariantSatisfiedCount == 27
 && ScheduledInvariantFailedCount == 0
 && ScheduledInvariantHeldCount == 0
 && ScheduledInvariantInfrastructureFailureCount == 0
 && ScheduledInvariantStaleCount == 0
```

Catalog-wide execution remains false because 57 catalog invariants are outside the current root projection.

```text
CatalogWideEvidenceExecutionClosed=false
ProductionAuthorityClaimed=false
```

## 14. Parent identity preservation

NATIVE-07 must not mutate Core NATIVE-03/04/06 catalog identities or NATIVE-05 topology identities. No `ash_core` file is changed by the NATIVE-07 consumer-side bake.

Legacy generated semantic program files also remain byte-identical to NATIVE-06.

## 15. Changed source surface

New:

```text
crates/ash_control_runtime/src/probe/mod.rs
crates/ash_control_runtime/src/probe/registry.rs
crates/ash_control_runtime/src/device/native_domain_probe.rs
crates/ash_control_runtime/src/native_evidence_execution.rs
```

Modified:

```text
crates/ash_control_runtime/src/device/mod.rs
crates/ash_control_runtime/src/lib.rs
crates/ash_control_runtime/src/main.rs
```

No Core catalog, NATIVE-05 graph builder, NATIVE-06 factory or NATIVE-06 manager reducer is rewritten.

## 16. Mandatory gates

```text
PASS_NATIVE07_PARENT_NATIVE06_PHYSICAL_CLOSURE
PASS_NATIVE07_PARENT_IDENTITY_UNCHANGED
PASS_NATIVE07_SCHEDULED_INVARIANT_27
PASS_NATIVE07_SCHEDULED_PROBE_BOUND_27_27
PASS_NATIVE07_SCHEDULED_PROBE_UNBOUND_ZERO
PASS_NATIVE07_DUPLICATE_PROBE_ZERO
PASS_NATIVE07_DUPLICATE_OPERATION_ZERO
PASS_NATIVE07_LEGACY_PROBE_BINDING_ZERO
PASS_NATIVE07_NO_BASE_TRAIN_CONTROL_RUNTIME_DEPENDENCY
PASS_NATIVE07_NO_EXPECTED_VALUE_ECHO
PASS_NATIVE07_NO_SHADOW_PRODUCTION_ALGORITHM
PASS_NATIVE07_NO_FIXTURE_PRODUCTION_EVIDENCE
PASS_NATIVE07_NO_SYNTHETIC_PRODUCTION_EVIDENCE
PASS_NATIVE07_NO_LEGACY_ORACLE_PRODUCTION_EVIDENCE
PASS_NATIVE07_PYTHON_VALIDATOR_EXECUTION_ZERO
PASS_NATIVE07_FACTORY_VERDICT_ZERO
PASS_NATIVE07_DEVICE_VERDICT_ZERO
PASS_NATIVE07_MISSING_OBSERVATION_FAIL_CLOSED
PASS_NATIVE07_CATALOG_UNSCHEDULED_57_NOT_FABRICATED
PASS_NATIVE07_NO_PRODUCTION_AUTHORITY
```

Physical execution-closure gates remain pending until native producer adoption:

```text
PENDING_NATIVE07_ACTUAL_NATIVE_OBSERVATION_27_27
PENDING_NATIVE07_SATISFIED_27_27
PENDING_NATIVE07_CURRENT_SCHEDULED_EVIDENCE_EXECUTION_CLOSED
```

## 17. Hard HOLD

```text
control runtime adds base_train dependency solely to read production state
probe returns expectation instead of observation
production algorithm is copied into the control runtime
fixture/synthetic/legacy observation is accepted as production evidence
missing observation is converted to PASC
unsupported observation producer is converted to semantic FAIL
legacy validator identity/path/ordinal enters probe registry
57 unscheduled invariants are counted as executed
parent catalog or DAG identity drifts
production authority is claimed
```

## 18. Next integration step inside NATIVE-07 lineage

The blocker is now explicit and typed:

```text
27 consumer probe bindings exist
0 actual native producer observations exist
```

The next repair must be producer-side adoption in the true owning native domains. Each owner must emit `ash.control_runtime.native_domain_probe_observation.v1` from its real implementation/receipt/artifact/process/filesystem observation path. Once 27 producer envelopes exist, the existing NATIVE-07 consumer/reducer can close the current scheduled evidence loop without changing truth authority.

After that physical 27/27 closure, proceed to:

```text
ASH-CONTROL-RUNTIME-LEGACY-CF1-ORACLE-QUARANTINE-AND-NATIVE-CANONICAL-CUTOVER-08
```
