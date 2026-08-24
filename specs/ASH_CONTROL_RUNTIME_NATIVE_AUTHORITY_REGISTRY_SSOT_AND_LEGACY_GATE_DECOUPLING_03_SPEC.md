# ASH-CONTROL-RUNTIME-NATIVE-AUTHORITY-REGISTRY-SSOT-AND-LEGACY-GATE-DECOUPLING-03

## Status

```text
Patch ID: ASH-CONTROL-RUNTIME-NATIVE-AUTHORITY-REGISTRY-SSOT-AND-LEGACY-GATE-DECOUPLING-03
Parent artifact: ASH-CONTROL-RUNTIME-CF1-SEMANTIC-SCAFFOLD-SEPARATION-AND-SYMBOLIC-DATAFLOW-01B-R1A-R2C
Role: promote native authority graph to Rust Core SSOT and demote CF1/Python gates to migration compatibility evidence
Production authority: false
Training math change: false
Optimizer math change: false
Legacy semantic coverage expansion: false
CF1 V2 mutation: false
104 gate migration: false
Cargo authority migration: false
```

## 1. Architectural correction

R2A through R2C proved useful as migration evidence, but their `SemanticProjected / Frozen` axis must not become the production control-runtime architecture.

The canonical execution model after NATIVE-03 is:

```text
Native Authority
    -> Native Contract
    -> Native Invariant
    -> Evidence Plan
    -> Physical Evidence
    -> Receipt
```

The historical CF1/Python lane is separately classified as:

```text
Legacy Gate
    -> Migration Alias
    -> future Native Authority / Contract / Invariant references
```

A Python validator is not a native authority and a Rust semantic program that mimics a Python validator is not, by itself, a production authority contract.

## 2. Native Core SSOT

New Core module:

```text
crates/ash_core/src/native_authority_registry.rs
```

Core owns a checked-in, filesystem-independent native registry.

The runtime identity is semantic, for example:

```text
native.training.runtime.multistep-accumulation-warmup-scheduler
native.optimizer.runtime.local-muon-callsite
native.bp-dk.observation.contract
native.bp-dk.observation.generation-freshness
native.bp-dk.fusion.fission-planner
native.optimizer.generation.transaction
native.optimizer.generation.failure-recovery
```

Historical `ASH-...` lineage patch IDs are **not** used as `NativeAuthorityId` values.

This is deliberate. A first draft that promoted historical patch tokens directly into Rust Core caused old scope gates to report `no-runtime-patch-token` regressions. That exposed a real architectural problem: migration patch identity is not runtime authority identity.

Therefore NATIVE-03 separates:

```text
NativeAuthorityId = semantic runtime identity
Legacy lineage patch_id = migration rebase evidence only
```

## 3. Exact parent inventory rebased

Migration source inventory:

```text
DescriptorCount = 48
Active = 37
QualificationOnly = 6
Superseded = 5
CurrentHeads = 19
CurrentExecutionAuthorities = 8
```

Rust Core preserves the authority semantics of those 48 descriptors:

```text
lineage family
authority class
production authority
lineage status
direct parent
runtime parent
evidence parents
control parents
supersedes
does-not-supersede
semantic tags
vocabulary binding
```

`source_paths` are intentionally not promoted into native authority. The original registry mixes Rust runtime files and Python/tooling paths, so carrying `source_paths` into Core would make filesystem layout part of authority identity again.

## 4. Native authority classes

The source vocabulary is preserved as typed Rust authority classes:

```text
TrainingDataPlane
OptimizerDataPlane
BpDkDataPlane
BpDkPolicyControlPlane
HistoricalEvidence
BuildSurfaceGovernance
```

Observed class cardinality remains migration evidence and is not used to invent new authorities.

## 5. Native production authority vocabulary

Typed vocabulary:

```text
None
Observation
Planning
Execution
ExecutionCoordination
FailureRecoveryCoordination
CompileSurfaceAdmission
HotpathOwnershipProjection
Commit
PolicySelection
OperatorApproval
```

`authority_class` and `production_authority` remain separate axes.

## 6. Native status vocabulary

Typed Rust status vocabulary preserves the source domain:

```text
Active
QualificationOnly
Reference
Historical
Superseded
```

Current physical inventory:

```text
Active = 37
QualificationOnly = 6
Superseded = 5
Reference = 0
Historical = 0
```

## 7. Four parent relations remain distinct

NATIVE-03 does not collapse lineage edges into a generic dependency field.

```text
DirectParent
RuntimeParent
EvidenceParent
ControlParent
```

Physical parent/edge inventory from the parent source:

```text
DirectParentEdgeCount = 40
RuntimeParentEdgeCount = 26
EvidenceParentEdgeCount = 107
ControlParentEdgeCount = 9
SupersedesEdgeCount = 1
DoesNotSupersedeEdgeCount = 120
```

Execution scheduling from these edges is intentionally deferred to NATIVE-05.

## 8. External non-supersession boundaries

During exact reinspection, two `does_not_supersede` references were found outside the 48-descriptor registry:

```text
legacy source boundary:
ASH-DECODE-DELTA-K-AUTHORITY
ASH-TOKEN-SEMANTIC-PRIOR-DELTA-K-AUTHORITY
```

They are not missing required parent nodes. They are explicit negative authority boundaries.

Native semantic boundary identities:

```text
external.decode.delta-k
external.token-semantic-prior.delta-k
```

Therefore the correct structural gate is:

```text
MissingRequiredInternalReferenceCount = 0
ExternalNonSupersessionReferenceCount = 2
```

not a fabricated `all referenced IDs must be among the 48` rule.

## 9. Native graph structural validation

Core validation checks:

```text
DescriptorCount = 48
Active = 37
QualificationOnly = 6
Superseded = 5
CurrentHeads = 19
CurrentExecutionAuthorities = 8
DuplicateAuthorityIdCount = 0
MissingRequiredInternalReferenceCount = 0
ExternalNonSupersessionReferenceCount = 2
DirectParentCycleCount = 0
RuntimeParentCycleCount = 0
SupersedesCycleCount = 0
```

No filesystem scan, subprocess, regex, Python parser, GPU execution, or legacy expected disposition participates in this validation.

## 10. Current heads

Current head projection is rebased to semantic NativeAuthorityId values.

Count:

```text
19
```

The ordered representation exists only for deterministic serialization. Array order is not execution authority.

## 11. Current execution authorities

Current execution-authority projection is rebased independently.

Count:

```text
8
```

The eight source roles remain:

```text
training
optimizer
fusion planning
policy selection
policy G2 selection capability
policy review head
generation transaction coordination
generation failure recovery
```

NATIVE-03 does not yet turn this list into the Orchestrator execution DAG.

## 12. Vocabulary binding

Native descriptors retain canonical revision/generation semantics:

```text
owned_data_plane_revision
target_data_plane_revision
owned_policy_generation
target_policy_generation
owned_qualification_generation
accepted_qualification_generations
generation_relations
binding_status
```

Legacy revision tokens are not part of native runtime vocabulary binding.

## 13. Migration-only rebase evidence

A non-runtime migration artifact is added:

```text
specs/migration/ASH_CONTROL_RUNTIME_NATIVE_AUTHORITY_REGISTRY_03_REBASE_MAP.json
```

It records the one-time relation:

```text
legacy lineage patch ID
    -> semantic NativeAuthorityId
```

It is never imported by `ash_core` or `ash_control_runtime`.

Rebase map:

```text
EntryCount = 48
UniqueLegacyLineagePatchIdCount = 48
UniqueNativeAuthorityIdCount = 48
ExternalBoundaryCount = 2
SHA256 = b4adfd22e6a84fb2a1b2b3233d2881016da5c2e8e39fe0839ea2e3070fe570e6
```

## 14. Native registry identity seal

NATIVE-03 canonical serialization covers:

```text
descriptors
current heads
current execution authorities
```

Expected registry digest:

```text
cfdf654dffc8182a49e67202615a6b874e3568593e4d8bcb20617cbee5ae91ee
```

The runtime receipt builder fails closed if the compiled native registry no longer hashes to this staged identity.

## 15. Native Core purity

`native_authority_registry.rs` contains no canonical dependency on:

```text
.py paths
legacy_source_sha256
expected_legacy_disposition
legacy execution ordinal
rustpython-parser
std::fs
std::process::Command
regex
```

Historical patch IDs are not stored as NativeAuthorityId values.

The NATIVE-03 patch ID itself is owned by the control-runtime receipt module, not by the Core authority registry.

## 16. Legacy CF1 registry demotion

The old Core CF1 membership function is reclassified as migration compatibility inventory:

```text
legacy_cf1_gate_registry()
validate_legacy_cf1_gate_registry()
```

Compatibility wrappers remain:

```text
cf1_canonical_validator_registry()
validate_cf1_canonical_registry()
```

so existing migration code does not break abruptly.

Existing runtime CF1 modules now explicitly consume `legacy_cf1_gate_registry()` rather than presenting it as the new native Core SSOT.

## 17. Legacy gate alias lane

New migration module:

```text
crates/ash_control_runtime/src/cf1/legacy_alias.rs
```

Alias shape:

```text
legacy validator ID
legacy path
legacy ordinal
covered native authorities
alias disposition
```

Current staged truth:

```text
LegacyActiveGateCount = 80
LegacyGateAliasMappedCount = 0
LegacyGateAliasUnmappedCount = 80
```

This is intentional.

NATIVE-03 does **not** guess that one Python validator equals one native authority. Mapping begins only after NATIVE-04 defines native contracts/invariants.

## 18. Alias mapping semantics

Future alias dispositions are typed:

```text
MigrationUnmapped
ExactHistoricalAlias
CompositeHistoricalAlias
DuplicateCoverage
Superseded
QualificationOnly
```

A LegacyGateAlias cannot create or mutate NativeAuthority membership.

## 19. Legacy migration materialization preserved

The old semantic compiler/program system is frozen as migration evidence.

Current state remains:

```text
LegacyMigrationProjectedCount = 26
LegacyMigrationFrozenCount = 54
DeclaredInactive = 1
```

No generated semantic program was added, removed, or regenerated by NATIVE-03.

Preserved sources:

```text
generated.rs       e7f2cc33388bec593647dc896cc51ca2026fb0e23378fc043eb23cf5851e7f74
generated_r1ar1.rs c96911569939dddefaa0abd054d90e3bce76fa360b467d605591fdd4534fb80f
generated_r1ar2.rs 8425b9455ed67ee5b3c92c1492a2a11a9b2368d53be4c6013e025f74adcc8cc1
generated_r2a.rs   af4dc3ce75cbcbf9841a65992bcb04362b52055318df3dfe8639e3243616ce18
```

`26 / 54` is no longer a native production-readiness KPI.

## 20. Legacy oracle regression

After native IDs were separated from historical patch tokens, all 80 active legacy validators were rerun in migration/reference mode.

Observed:

```text
ordinals 00..55 = 56 PASS
ordinal 56 = FAIL
ordinals 57..79 = 23 PASS

TOTAL = 79 PASS / 1 FAIL
FirstFailureOrdinal = 56
```

15C-R1 remains exactly:

```text
105 checks
102 PASS
3 scheduler-hash FAIL
```

No additional legacy failure is introduced by NATIVE-03.

## 21. Why native IDs are semantic IDs

An intermediate implementation stored historical lineage patch IDs directly in Rust Core. This produced legitimate legacy scope regressions including:

```text
scope:no-runtime-vocabulary-token
scope:runtime-patch-token-exact
scope:no-runtime-patch-token
```

The implementation was rejected before bake.

Final NATIVE-03 uses semantic IDs and verifies that the count of each of the 48 historical patch tokens across `crates/**/*.rs` does not increase relative to the R2C parent:

```text
LegacyLineagePatchTokenCountDrift = 0
```

This prevents a subtle migration-token-to-runtime-authority leak.

## 22. Control-runtime receipt lane

New module:

```text
crates/ash_control_runtime/src/native_authority.rs
```

Receipt schema:

```text
ash.control_runtime.native_authority_registry.v1
```

CLI:

```powershell
cargo run -p ash_control_runtime -- `
  native-authority-registry `
  --repo-root .
```

Default receipt:

```text
artifacts/control_runtime/native_authority_registry/native_authority_registry_receipt.json
```

## 23. Expected CLI truth

After local Rust qualification:

```text
ASH_CONTROL_RUNTIME_NATIVE_AUTHORITY_REGISTRY_VALID=true
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

## 24. Authority ownership after NATIVE-03

```text
Core
  NativeAuthorityRegistry
  NativeAuthorityDescriptor
  native graph structural law

Orchestrator
  no native scheduling migration yet
  future DAG projection owner

Manager
  no native contract execution migration yet

Factory
  no native evidence-plan migration yet

Device
  no native probe migration yet

Legacy CF1
  compatibility / migration oracle only
```

NATIVE-03 moves SSOT first. It deliberately does not pretend later layers are already native.

## 25. Changed surface

Added:

```text
crates/ash_core/src/native_authority_registry.rs
crates/ash_control_runtime/src/native_authority.rs
crates/ash_control_runtime/src/cf1/legacy_alias.rs
specs/migration/ASH_CONTROL_RUNTIME_NATIVE_AUTHORITY_REGISTRY_03_REBASE_MAP.json
```

Modified:

```text
crates/ash_core/src/lib.rs
crates/ash_core/src/cf1_control_authority.rs
crates/ash_control_runtime/src/lib.rs
crates/ash_control_runtime/src/main.rs
crates/ash_control_runtime/src/cf1/mod.rs
crates/ash_control_runtime/src/cf1/registry.rs
crates/ash_control_runtime/src/cf1/executable_registry.rs
crates/ash_control_runtime/src/cf1/capability_matrix.rs
crates/ash_control_runtime/src/cf1/architecture.rs
```

No file is deleted.

## 26. Key source hashes

```text
crates/ash_core/src/native_authority_registry.rs
SHA256 = aec310beb11cc5eeb38fdfda876ff3da91d8c53f4f30af814b5f7a9ae2ba89bc

crates/ash_control_runtime/src/native_authority.rs
SHA256 = 488901300c6dfe2903e61a963e5c85332801199de4f8cdb3907d04ea426535b9

crates/ash_control_runtime/src/cf1/legacy_alias.rs
SHA256 = 130be4a1bce5d932509e38490b94d13993b6b596b550e714b620e91067b8f52b

migration rebase map
SHA256 = b4adfd22e6a84fb2a1b2b3233d2881016da5c2e8e39fe0839ea2e3070fe570e6
```

## 27. Static bake qualification

Completed in the bake environment:

```text
Native descriptor source extraction = 48
Status inventory = 37 / 6 / 5
Current heads = 19
Current execution authorities = 8
Direct edges = 40
Runtime edges = 26
Evidence edges = 107
Control edges = 9
Supersedes edges = 1
Does-not-supersede edges = 120
Missing required internal references = 0
External non-supersession boundaries = 2
Direct-parent cycles = 0
Runtime-parent cycles = 0
Supersedes cycles = 0
Rebase map unique legacy IDs = 48
Rebase map unique native IDs = 48
Legacy lineage patch-token runtime-count drift = 0
Legacy translation states = 26 projected / 54 frozen / 1 inactive
Generated semantic programs changed = 0
Invalid Rust \uXXXX escapes = 0
Changed-Rust delimiter audit = PASS
Forbidden baked pycache/pyc artifacts = 0
Legacy oracle = 79 PASS / 1 FAIL
15C = 105 / 102 / 3
```

## 28. Physical Rust qualification status

The bake container does not expose a usable Cargo/Rust toolchain.

Therefore NATIVE-03 does **not** claim physical:

```text
cargo check PASS
cargo test PASS
native-authority-registry CLI PASS
```

Those are local promotion gates.

Run:

```powershell
cargo check -p ash_control_runtime
cargo test -p ash_control_runtime --no-run
cargo test -p ash_control_runtime

cargo run -p ash_control_runtime -- `
  native-authority-registry `
  --repo-root .
```

Then retain the existing migration regression:

```powershell
cargo run -p ash_control_runtime -- `
  cf1-semantic-shadow `
  --repo-root . `
  --mode diagnostic-full-matrix
```

Expected old migration semantic baseline remains:

```text
observedSemanticPassCount=25
observedSemanticFailureCount=1
firstSemanticFailureOrdinal=56
firstMaterializationHoldOrdinal=0
```

## 29. Mandatory gates

```text
PASS_NATIVE03_DESCRIPTOR_COUNT_48
PASS_NATIVE03_ACTIVE_COUNT_37
PASS_NATIVE03_QUALIFICATION_COUNT_6
PASS_NATIVE03_SUPERSEDED_COUNT_5
PASS_NATIVE03_CURRENT_HEAD_COUNT_19
PASS_NATIVE03_EXECUTION_AUTHORITY_COUNT_8

PASS_NATIVE03_DIRECT_PARENT_REBASED
PASS_NATIVE03_RUNTIME_PARENT_REBASED
PASS_NATIVE03_EVIDENCE_PARENT_REBASED
PASS_NATIVE03_CONTROL_PARENT_REBASED
PASS_NATIVE03_SUPERSEDES_REBASED
PASS_NATIVE03_DOES_NOT_SUPERSEDE_REBASED
PASS_NATIVE03_VOCABULARY_BINDING_REBASED

PASS_NATIVE03_REQUIRED_INTERNAL_REFERENCE_MISSING_ZERO
PASS_NATIVE03_EXTERNAL_NON_SUPERSESSION_BOUNDARY_TWO
PASS_NATIVE03_DIRECT_PARENT_CYCLE_ZERO
PASS_NATIVE03_RUNTIME_PARENT_CYCLE_ZERO
PASS_NATIVE03_SUPERSEDES_CYCLE_ZERO

PASS_NATIVE03_SEMANTIC_NATIVE_IDS
PASS_NATIVE03_NO_LEGACY_PATCH_ID_AS_NATIVE_AUTHORITY_ID
PASS_NATIVE03_NO_PYTHON_PATH_IN_NATIVE_AUTHORITY
PASS_NATIVE03_NO_PYTHON_SHA_IN_NATIVE_AUTHORITY
PASS_NATIVE03_NO_EXPECTED_DISPOSITION_IN_NATIVE_AUTHORITY
PASS_NATIVE03_NO_LEGACY_ORDINAL_IN_NATIVE_AUTHORITY

PASS_NATIVE03_LEGACY_GATE_REGISTRY_DEMOTED
PASS_NATIVE03_LEGACY_GATE_ALIAS_REGISTRY
PASS_NATIVE03_LEGACY_GATE_COUNT_80
PASS_NATIVE03_ALIAS_ACCOUNTING_0_80

PASS_NATIVE03_MIGRATION_26_54_PRESERVED
PASS_NATIVE03_NO_SEMANTIC_PROGRAM_COVERAGE_EXPANSION
PASS_NATIVE03_GENERATED_PROGRAMS_UNCHANGED
PASS_NATIVE03_LEGACY_ORACLE_79_1
PASS_NATIVE03_FIRST_LEGACY_FAILURE_56
PASS_NATIVE03_15C_105_102_3

PASS_NATIVE03_CORE_PURITY
PASS_NATIVE03_ONE_WAY_DEPENDENCY
PASS_NATIVE03_NO_TRAINING_MATH_CHANGE
PASS_NATIVE03_NO_OPTIMIZER_CHANGE
PASS_NATIVE03_NO_104_GATE_MIGRATION
PASS_NATIVE03_NO_CARGO_AUTHORITY_MIGRATION
PASS_NATIVE03_NO_CF1_V2_MUTATION
PASS_NATIVE03_NO_PRODUCTION_AUTHORITY
```

Physical local gates pending:

```text
PASS_NATIVE03_CARGO_CHECK
PASS_NATIVE03_CARGO_TEST
PASS_NATIVE03_NATIVE_REGISTRY_CLI
PASS_NATIVE03_NATIVE_REGISTRY_DIGEST
PASS_NATIVE03_R2B1_SEMANTIC_25_1
```

## 30. Hard HOLD conditions

```text
Native descriptor count != 48
Status inventory != 37 / 6 / 5
Current heads != 19
Current execution authorities != 8
Required internal reference missing
Direct/runtime/supersedes cycle introduced
External negative boundary count != 2
Historical lineage patch ID becomes NativeAuthorityId
Native registry stores Python path/SHA/disposition/ordinal
Legacy gate ordinal becomes native execution ordering
Legacy semantic coverage changes from 26 / 54
Generated semantic program changes
Legacy oracle changes from 79 / 1
15C changes from 105 / 102 / 3
Production authority claimed
```

## 31. Next patch

NATIVE-03 intentionally stops before translating historical gates.

Next patch:

```text
ASH-CONTROL-RUNTIME-NATIVE-CONTRACT-AND-INVARIANT-CATALOG-04
```

Its job is to answer, for the 37 active native authorities:

```text
What must actually be true?
What illegal state is prevented?
What typed evidence can prove that invariant?
```

Historical Python validators may be read as migration evidence of intent, but their syntax/check cardinality is not the native contract model.

That is the cut between translator architecture and a genuinely Rust-native control runtime.
