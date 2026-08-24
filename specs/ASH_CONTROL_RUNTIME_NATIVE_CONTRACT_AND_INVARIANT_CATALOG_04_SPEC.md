# ASH-CONTROL-RUNTIME-NATIVE-CONTRACT-AND-INVARIANT-CATALOG-04

## Status

```text
Patch ID: ASH-CONTROL-RUNTIME-NATIVE-CONTRACT-AND-INVARIANT-CATALOG-04
Parent: ASH-CONTROL-RUNTIME-NATIVE-AUTHORITY-REGISTRY-SSOT-AND-LEGACY-GATE-DECOUPLING-03
Role: define Rust-native contract and invariant SSOT over the NATIVE-03 authority graph
Production authority: false
Evidence execution: none
Legacy semantic coverage expansion: false
Python validator translation: forbidden
CF1 V2 mutation: false
104 gate migration: false
Cargo authority migration: false
```

## 1. Parent physical truth

NATIVE-03 was physically observed locally as:

```text
ASH_CONTROL_RUNTIME_NATIVE_AUTHORITY_REGISTRY_VALID=true
receiptHash=fda61ae48c5a239e858289ce0b6ab59405e9e0699d866829eb445d9fa9eccb8c
nativeAuthorityDescriptorCount=48
activeAuthorityCount=37
qualificationOnlyAuthorityCount=6
supersededAuthorityCount=5
currentHeadCount=19
currentExecutionAuthorityCount=8
missingRequiredReferenceCount=0
externalNonSupersessionReferenceCount=2
legacyActiveGateCount=80
legacyMigrationProjectedCount=26
legacyMigrationFrozenCount=54
legacyGateAliasMappedCount=0
legacyGateAliasUnmappedCount=80
nativeRegistryUsesPythonSourceHash=false
nativeRegistryUsesExpectedLegacyDisposition=false
nativeRegistryUsesLegacyOrdinal=false
productionAuthorityClaimed=false
```

NATIVE-04 does not mutate the NATIVE-03 authority graph.

Native authority registry source remains byte-identical:

```text
crates/ash_core/src/native_authority_registry.rs
SHA256 = aec310beb11cc5eeb38fdfda876ff3da91d8c53f4f30af814b5f7a9ae2ba89bc
```

Canonical authority registry digest remains:

```text
cfdf654dffc8182a49e67202615a6b874e3568593e4d8bcb20617cbee5ae91ee
```

## 2. Architectural purpose

NATIVE-03 answered:

```text
Who owns authority?
```

NATIVE-04 answers:

```text
What must be true for that authority to remain semantically valid?
```

Canonical direction becomes:

```text
Native Authority
    -> Native Contract
    -> Native Invariant
    -> Illegal State
    -> Evidence Requirement
```

NATIVE-04 does not execute evidence. It defines the native law catalog that NATIVE-05/06/07 will orchestrate, materialize and execute.

## 3. Python translation is not the contract model

The new Core catalog contains no canonical dependency on:

```text
Python validator path
Python validator SHA
legacy expected disposition
legacy ordinal
TextFind
RegexSearch
StaticComprehension
Python check cardinality
```

Static source audit of `native_contract_catalog.rs`:

```text
legacy_source_sha256 = 0
expected_legacy_disposition = 0
legacy_ordinal = 0
rustpython = 0
TextFind = 0
RegexSearch = 0
StaticComprehension = 0
.py = 0
```

Historical Python gates remain migration evidence only.

## 4. Core catalog types

New Core module:

```text
crates/ash_core/src/native_contract_catalog.rs
```

Typed domains:

```text
NativeContractClass
NativeInvariantClass
NativeInvariantSeverity
NativeEvidenceKind
NativeEvidencePhase
NativeInvariantProvenance
NativeInvariantStatus
NativeEvidenceRequirement
NativeContractDescriptor
NativeInvariantDescriptor
NativeContractCatalogValidation
```

Contract classes:

```text
StateTransition
Freshness
Ownership
Admission
Planning
Execution
Routing
Commit
Recovery
EvidenceProvenance
BuildSurface
Qualification
```

Invariant classes:

```text
StateLegality
TransitionLegality
Monotonicity
Freshness
Exclusivity
Ownership
Admission
Ordering
Routing
CommitIntegrity
RecoveryIntegrity
Provenance
Structural
Qualification
```

## 5. Evidence requirement vocabulary

NATIVE-04 defines only the evidence kind and phase required to prove an invariant.

```text
NativeBehavior
NativeStateTransition
TypedReceipt
TypedArtifact
RustStructure
CargoSurface
WgslStructure
FilesystemBehavior
ProcessBehavior
PhysicalGpuQualification
```

Evidence phases:

```text
StaticQualification
RuntimeQualification
PhysicalQualification
```

No Device, filesystem, Cargo, process or GPU evidence is executed in Core.

## 6. Illegal-state-first semantics

The catalog is behavioral/state-law oriented.

Examples physically grounded in existing Rust state and validation surfaces include:

```text
active generation cannot regress
observation generation must match active generation
duplicate current-generation tensorcube observation is illegal
bridge endpoints must belong to the same parameter
planner commit/abort must match pending generation
incomplete generation cannot be reported complete
g2 canary binding cannot be production active
all generation transaction stages must bind the target generation
a failed generation stage cannot publish a success receipt
active recovery fence must block a conflicting transaction
production activation barrier requires quiescence and durable checkpoint
restart continuity identity cannot drift
```

These are not source-string presence checks.

## 7. Current catalog cardinality

Actual NATIVE-04 staged catalog:

```text
ContractCount = 43
DefinedInvariantCount = 84
UnresolvedInvariantIntentCount = 0

RequiredInvariantCount = 78
QualificationRequiredInvariantCount = 6
AdvisoryInvariantCount = 0
```

The 43 contracts cover all non-superseded NATIVE-03 authorities:

```text
37 Active
6 QualificationOnly
```

The 5 Superseded authorities own no current contract.

## 8. Native authority coverage

Static validation result:

```text
ActiveAuthorityCount = 37
ActiveAuthorityWithDefinedContractCount = 37
ActiveAuthorityWithoutDefinedContractCount = 0

QualificationOnlyAuthorityCount = 6
QualificationAuthorityWithDefinedContractCount = 6

CurrentHeadCount = 19
CurrentHeadWithDefinedContractCount = 19

CurrentExecutionAuthorityCount = 8
CurrentExecutionAuthorityWithDefinedContractCount = 8
```

This is contract-definition coverage only. It is not runtime evidence closure and does not claim production authority.

## 9. Evidence requirement distribution

Actual staged counts:

```text
NativeBehavior = 16
NativeStateTransition = 21
TypedReceipt = 25
TypedArtifact = 11
RustStructure = 4
CargoSurface = 2
WgslStructure = 0
FilesystemBehavior = 1
ProcessBehavior = 2
PhysicalGpuQualification = 2
```

Phase distribution:

```text
RuntimeQualification = 71
PhysicalQualification = 7
StaticQualification = 6
```

No evidence has been executed in NATIVE-04:

```text
EvidenceExecutionCount = 0
```

## 10. Provenance distribution

Catalog invariants are grounded by native surfaces/architecture rather than Python check syntax:

```text
NativeStateTransition = 21
NativeTypeContract = 11
NativeRuntimeBehavior = 17
NativeReceiptContract = 25
ArchitecturalSpecification = 10
```

Qualification contracts whose physical runners remain outside Core are represented as architectural qualification laws, not imported Python behavior.

## 11. Current execution authorities receive behavioral law

All 8 current execution authorities have defined contracts:

```text
native.training.runtime.multistep-accumulation-warmup-scheduler
native.optimizer.runtime.local-muon-callsite
native.bp-dk.fusion.fission-planner
native.optimizer.generation.transaction
native.optimizer.generation.failure-recovery
native.bp-dk.policy.production-activation.g1
native.bp-dk.policy.r2-closure
native.bp-dk.policy.operator-review-adoption.g2
```

Their catalog laws are expressed in state transition, routing, commit, recovery, admission or typed receipt terms rather than legacy validator structure.

## 12. Structural catalog validation

Core validation requires:

```text
DuplicateContractIdCount = 0
DuplicateInvariantIdCount = 0
MissingOwnerAuthorityCount = 0
MissingInvariantReferenceCount = 0
MissingContractReferenceCount = 0
ContractDependencyCycleCount = 0
InvariantDependencyCycleCount = 0
SupersededContractOwnerCount = 0
```

Current staged result satisfies all of the above.

Contract/invariant dependencies are intentionally empty in NATIVE-04 unless a semantic dependency is independently established. NATIVE-03 lineage edges are not blindly copied into contract dependencies.

## 13. Catalog identity seals

Canonical contract catalog digest:

```text
edbb1f1bf03c627007ff2da05e9a823e5bf2938e08ef2a74d0a509c76d5866cd
```

Canonical invariant catalog digest:

```text
ea05cfbf4b71dc8edb5dbf13b9a9d6c80fcea2b6a05dba3dba62f1731e4061a6
```

Control-runtime fails closed if either compiled catalog digest drifts from these NATIVE-04 identities.

## 14. Runtime receipt lane

New runtime module:

```text
crates/ash_control_runtime/src/native_contract.rs
```

Receipt schema:

```text
ash.control_runtime.native_contract_catalog.v1
```

CLI:

```powershell
cargo run -p ash_control_runtime -- `
  native-contract-catalog `
  --repo-root .
```

Default receipt:

```text
artifacts/control_runtime/native_contract_catalog/native_contract_catalog_receipt.json
```

## 15. Expected physical CLI truth

After local Rust qualification:

```text
ASH_CONTROL_RUNTIME_NATIVE_CONTRACT_CATALOG_VALID=true
nativeAuthorityRegistryDigest=cfdf654dffc8182a49e67202615a6b874e3568593e4d8bcb20617cbee5ae91ee
nativeContractCatalogDigest=edbb1f1bf03c627007ff2da05e9a823e5bf2938e08ef2a74d0a509c76d5866cd
nativeInvariantCatalogDigest=ea05cfbf4b71dc8edb5dbf13b9a9d6c80fcea2b6a05dba3dba62f1731e4061a6
nativeAuthorityDescriptorCount=48
activeAuthorityCount=37
activeAuthorityWithDefinedContractCount=37
activeAuthorityWithoutDefinedContractCount=0
qualificationOnlyAuthorityCount=6
qualificationAuthorityWithDefinedContractCount=6
currentHeadCount=19
currentHeadWithDefinedContractCount=19
currentExecutionAuthorityCount=8
currentExecutionAuthorityWithDefinedContractCount=8
contractCount=43
definedInvariantCount=84
unresolvedInvariantIntentCount=0
requiredInvariantCount=78
qualificationRequiredInvariantCount=6
duplicateContractIdCount=0
duplicateInvariantIdCount=0
missingOwnerAuthorityCount=0
missingInvariantReferenceCount=0
contractDependencyCycleCount=0
invariantDependencyCycleCount=0
legacyActiveGateCount=80
legacyGateAliasMappedCount=0
legacyGateAliasUnmappedCount=80
legacyMigrationProjectedCount=26
legacyMigrationFrozenCount=54
catalogUsesPythonSourceHash=false
catalogUsesExpectedLegacyDisposition=false
catalogUsesLegacyOrdinal=false
catalogUsesPythonSyntaxCapability=false
evidenceExecutionCount=0
activeAuthorityContractCoverageClosed=true
currentHeadContractCoverageClosed=true
currentExecutionAuthorityContractCoverageClosed=true
productionAuthorityClaimed=false
```

Deterministic staged receipt hash expected after physical run:

```text
3f366134363be69008993852410bc81b10a2e144b8853702281cd61cd59264ac
```

This hash remains a promotion expectation until observed from local Rust execution.

## 16. Legacy migration isolation

NATIVE-04 performs no legacy semantic materialization work.

Preserved migration state:

```text
LegacyActiveGateCount = 80
LegacyMigrationProjectedCount = 26
LegacyMigrationFrozenCount = 54
LegacyGateAliasMappedCount = 0
LegacyGateAliasUnmappedCount = 80
```

Generated legacy semantic programs remain byte-identical to NATIVE-03:

```text
generated.rs       e7f2cc33388bec593647dc896cc51ca2026fb0e23378fc043eb23cf5851e7f74
generated_r1ar1.rs c96911569939dddefaa0abd054d90e3bce76fa360b467d605591fdd4534fb80f
generated_r1ar2.rs 8425b9455ed67ee5b3c92c1492a2a11a9b2368d53be4c6013e025f74adcc8cc1
generated_r2a.rs   af4dc3ce75cbcbf9841a65992bcb04362b52055318df3dfe8639e3243616ce18
```

R2C capability matrix source is also byte-identical to the NATIVE-03 parent.

## 17. Legacy regression qualification

The bake environment's full 80-validator sequential run exceeds the container execution window, so NATIVE-04 does not falsely claim a fresh monolithic 80-validator subprocess run.

Instead the changed-source impact set was closed explicitly:

```text
Active legacy gates = 80
Gates directly bound to changed ash_core/lib.rs = 25
Active repo-query/rglob gates = 22
Known ordinal-56 semantic failure gate = 1
Union of affected gates = 37
Unaffected exact-bound gates = 43
```

Observed affected set:

```text
36 affected gates = PASS
ordinal 56 = existing FAIL
```

The 25 direct-bound gates all pass. One validator with a no-argument CLI was rerun using its actual command surface and reports:

```text
CHECK_COUNT=146
PASS_COUNT=146
FAIL_COUNT=0
```

All 22 active repo-query/rglob validators pass after the new files are present.

Ordinal 56 remains exactly:

```text
FAIL scheduler-hash:validate_ash_bp_dk_fusion_policy_production_soak_and_rollback_health_16_static.py
FAIL scheduler-hash:validate_ash_bp_dk_fusion_policy_production_long_horizon_stability_17_static.py
FAIL scheduler-hash:validate_ash_bp_dk_fusion_policy_production_evidence_recalibration_bridge_18_static.py
3 / 105 failures
```

The remaining 43 active gates have unchanged exact input bindings relative to the physically observed NATIVE-03 parent. Therefore the migration oracle disposition remains structurally bounded to the existing:

```text
79 PASS / 1 FAIL
FirstFailureOrdinal = 56
```

A local full run remains the final physical regression gate.

## 18. Changed source surface

Exactly five source files change from NATIVE-03:

```text
crates/ash_core/src/native_contract_catalog.rs           NEW
crates/ash_core/src/lib.rs
crates/ash_control_runtime/src/native_contract.rs        NEW
crates/ash_control_runtime/src/lib.rs
crates/ash_control_runtime/src/main.rs
```

SHA256:

```text
native_contract_catalog.rs 3162856786b151f31e8301e1bbd5db258721583de2ba92e08dde9af0f3cab2b6
ash_core/src/lib.rs         3cc79e7bd13fac818daecc61ea760e0ae9373e5a1409d91b871c25a73b3fe1b4
native_contract.rs          e0eaeedc0f7213f6bee0659eb94de8bf052c901563775c75bda1cc27ac0345bc
ash_control_runtime/lib.rs  46a98e6bf6ad70b9e7ea46d6e6a23b64c98121fab3240b6c3e2bf059ace886fb
ash_control_runtime/main.rs 64d7025709a43f26168c88e4869d37687131bfb437adaf312240fb68f14cd547
```

## 19. Static bake qualification

```text
Changed Rust delimiter audit = PASS
Invalid Rust \uXXXX escape count = 0
Forbidden baked pycache/pyc/pyo = 0
Baked file count = 8231
Contract owners unique = 43 / 43
Non-superseded authority coverage = 43 / 43
Active coverage = 37 / 37
Qualification coverage = 6 / 6
Current head coverage = 19 / 19
Current execution coverage = 8 / 8
Duplicate contracts = 0
Duplicate invariants = 0
Unresolved invariant intent = 0
```

## 20. Physical Rust qualification status

The bake container does not expose `cargo`, `rustc` or `rustfmt`.

Therefore NATIVE-04 does not claim local physical Rust compile/test PASS from the bake environment.

Required local commands:

```powershell
cargo check -p ash_control_runtime
cargo test -p ash_control_runtime --no-run
cargo test -p ash_control_runtime
```

Then NATIVE-03 regression:

```powershell
cargo run -p ash_control_runtime -- `
  native-authority-registry `
  --repo-root .
```

Then NATIVE-04:

```powershell
cargo run -p ash_control_runtime -- `
  native-contract-catalog `
  --repo-root .
```

Then legacy semantic migration regression:

```powershell
cargo run -p ash_control_runtime -- `
  cf1-semantic-shadow `
  --repo-root . `
  --mode diagnostic-full-matrix
```

Expected legacy semantic baseline remains:

```text
observedSemanticPassCount=25
observedSemanticFailureCount=1
firstSemanticFailureOrdinal=56
firstMaterializationHoldOrdinal=0
```

The semantic-shadow command remains exit code 1 because 54 legacy migration gates are still Frozen. That is not a NATIVE-04 failure.

## 21. Mandatory gates

```text
PASS_NATIVE04_PARENT_NATIVE03_VALID
PASS_NATIVE04_AUTHORITY_REGISTRY_DIGEST_UNCHANGED
PASS_NATIVE04_AUTHORITY_48_37_6_5_PRESERVED
PASS_NATIVE04_HEAD_COUNT_19_PRESERVED
PASS_NATIVE04_EXECUTION_AUTHORITY_COUNT_8_PRESERVED

PASS_NATIVE04_CONTRACT_COUNT_43
PASS_NATIVE04_DEFINED_INVARIANT_COUNT_84
PASS_NATIVE04_UNRESOLVED_INTENT_ZERO
PASS_NATIVE04_REQUIRED_INVARIANT_78
PASS_NATIVE04_QUALIFICATION_REQUIRED_INVARIANT_6

PASS_NATIVE04_ACTIVE_AUTHORITY_CONTRACT_COVERAGE_37_37
PASS_NATIVE04_QUALIFICATION_AUTHORITY_CONTRACT_COVERAGE_6_6
PASS_NATIVE04_CURRENT_HEAD_CONTRACT_COVERAGE_19_19
PASS_NATIVE04_EXECUTION_AUTHORITY_CONTRACT_COVERAGE_8_8

PASS_NATIVE04_DUPLICATE_CONTRACT_ZERO
PASS_NATIVE04_DUPLICATE_INVARIANT_ZERO
PASS_NATIVE04_MISSING_OWNER_ZERO
PASS_NATIVE04_MISSING_INVARIANT_REFERENCE_ZERO
PASS_NATIVE04_MISSING_CONTRACT_REFERENCE_ZERO
PASS_NATIVE04_CONTRACT_DEPENDENCY_CYCLE_ZERO
PASS_NATIVE04_INVARIANT_DEPENDENCY_CYCLE_ZERO
PASS_NATIVE04_SUPERSEDED_CONTRACT_OWNER_ZERO

PASS_NATIVE04_ILLEGAL_STATE_TYPED
PASS_NATIVE04_EVIDENCE_KIND_TYPED
PASS_NATIVE04_EVIDENCE_PHASE_TYPED
PASS_NATIVE04_PROVENANCE_TYPED

PASS_NATIVE04_NO_PYTHON_VALIDATOR_TRANSLATION
PASS_NATIVE04_NO_PYTHON_SOURCE_HASH
PASS_NATIVE04_NO_EXPECTED_LEGACY_DISPOSITION
PASS_NATIVE04_NO_LEGACY_ORDINAL
PASS_NATIVE04_NO_PYTHON_SYNTAX_CAPABILITY

PASS_NATIVE04_EVIDENCE_EXECUTION_ZERO
PASS_NATIVE04_CORE_NO_FS_PROCESS_GPU_EXECUTION

PASS_NATIVE04_LEGACY_MIGRATION_26_54_PRESERVED
PASS_NATIVE04_LEGACY_ALIAS_0_80_PRESERVED
PASS_NATIVE04_GENERATED_LEGACY_PROGRAMS_UNCHANGED
PASS_NATIVE04_ORDINAL56_15C_105_102_3_PRESERVED

PASS_NATIVE04_NO_104_GATE_MIGRATION
PASS_NATIVE04_NO_CARGO_AUTHORITY_MIGRATION
PASS_NATIVE04_NO_CF1_V2_MUTATION
PASS_NATIVE04_NO_PRODUCTION_AUTHORITY
```

Physical local gates pending:

```text
PASS_NATIVE04_CARGO_CHECK
PASS_NATIVE04_CARGO_TEST
PASS_NATIVE04_NATIVE03_REGRESSION
PASS_NATIVE04_NATIVE_CONTRACT_CLI
PASS_NATIVE04_RECEIPT_HASH_3F366134...
PASS_NATIVE04_LEGACY_SEMANTIC_25_1
```

## 22. Hard HOLD conditions

```text
NativeAuthorityRegistryDigest != NATIVE-03 digest
Active contract coverage != 37/37
Current head contract coverage != 19/19
Current execution contract coverage != 8/8
Unresolved invariant intent > 0
Any contract owned by a Superseded authority
Any contract/invariant identity derived from Python validator identity
Python source SHA / expected disposition / ordinal enters native catalog
Source-string search substitutes for existing typed native behavior
Core performs filesystem/process/GPU evidence execution
Legacy materialization changes from 26/54
Generated legacy program changes
Ordinal 56 ceases to be the known 3/105 failure without an explicit repair patch
Production authority claimed
```

## 23. Next patch

NATIVE-04 closes only the native law catalog.

Next:

```text
ASH-CONTROL-RUNTIME-NATIVE-AUTHORITY-DAG-ORCHESTRATION-05
```

Its input is exclusively:

```text
NATIVE-03 Authority Graph
+
NATIVE-04 Contract / Invariant Catalog
```

It must retire legacy CF1 ordinal ordering from the native lane and derive actual orchestration from native authority/dependency semantics.
