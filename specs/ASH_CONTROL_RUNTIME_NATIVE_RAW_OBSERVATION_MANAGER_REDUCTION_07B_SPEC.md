# ASH-CONTROL-RUNTIME-NATIVE-RAW-OBSERVATION-MANAGER-REDUCTION-07B

## Status

```text
Patch ID:
ASH-CONTROL-RUNTIME-NATIVE-RAW-OBSERVATION-MANAGER-REDUCTION-07B

Parent:
ASH-CONTROL-RUNTIME-NATIVE-RAW-OBSERVATION-ATOMIC-BATCH-AND-DIGEST-CLOSURE-07A-R3

Role:
Exact R3 Immutable Batch
-> Device Verified Raw Handoff
-> Core Evidence Specification Binding
-> Manager-Only Semantic Reduction
-> Immutable Reduction Manifest

Production authority: false
Current scheduled evidence execution closure: false
```

## Parent physical truth

07A-R3 physically closed one exact immutable 27-entry raw observation batch.

Observed parent identities from physical qualification:

```text
requestManifestDigest=
2f051108e43acb564304284c0d9f53dc47a9555766bb7a4eca214d1c5a6009f0

producerRouteRegistryDigest=
c8ab296f59f46f8114bac50b424c6d3960f6fc7299c9e3590d9035c60c5fa6c3

observerAdoptionManifestDigest=
2fe3cc4c7a107ec8a68b542b17d44b98b372d841f4a4f9c5ea34cf1e398f7d04

batchEntrySetDigest=
7a5f74c96ce62191388ac8ab1ce69dcdca73cbef357625fa3029c80b29c39415

batchManifestDigest=
c3c6fe695342a9cb900f62caa4cf8118034c247c1d1b48e5703cefab310dcb2f
```

07B consumes this batch immutably. It may not rewrite the R3 manifest or any R2 observation envelope.

## SSOT correction discovered during bake

R2's actual `NativeRawObservation` payload is a physical owner-source provenance snapshot. It contains facts such as:

```text
owner_authority_id
producer_endpoint_id
owner_source_relative_path
owner_source_present
owner_source_size
owner_source_line_count
owner_source_public_item_count
owner_source_sha256
current_process_id
current_executable
```

It does not contain domain-level facts such as legal state, transition before/after, active generation, commit witness, recovery fence state, or qualification result.

Therefore 07B MUST NOT infer `Satisfied` or `Failed` from source presence or source hashes.

The truthful current reduction is:

```text
physical raw evidence is valid
Core semantic contract is known
Manager reducer is available
but domain-semantic raw facts are insufficient
-> HeldInsufficientRawEvidence
```

This is not an infrastructure failure and is not a fabricated semantic PASS/FAIL.

## Authority law

```text
Physical observation ownership:
Owner-local observer

Physical integrity ownership:
Device

Semantic contract SSOT:
ash_core::native_evidence_spec_catalog

Semantic disposition ownership:
Manager
```

The existing `NativeInvariantEvidenceDisposition` remains Manager-owned in the current codebase. 07B extends that canonical enum rather than introducing a competing result enum.

## New semantic disposition

07B adds:

```text
HeldInsufficientRawEvidence
```

Meaning:

```text
the exact physical observation exists and is valid,
the exact Core contract is bound,
but the current raw observation schema does not contain enough domain facts
to truthfully produce Satisfied or Failed.
```

It is distinct from:

```text
HeldUnsupportedCapability
FailedInfrastructure
StaleEvidence
Failed
Satisfied
```

## Device verified raw handoff

New device surface:

```text
crates/ash_control_runtime/src/device/native_verified_observation.rs
```

The device loader takes an exact `batchManifestDigest`. There is no `latest` or mutable-current selection.

It revalidates:

```text
content-addressed batch path
exact batch root file set
batch manifest schema/count
batch entry digest
canonical batch ordering
batch entry-set digest
batch manifest digest
exact observation filename set
observation schema
operation key
plan digest
request digest binding
producer route digest
producer route registry digest
observer adoption digest
observation digest
observation envelope digest
raw owner authority identity field
raw producer endpoint identity field
```

The device returns:

```text
VerifiedNativeObservationBatch
VerifiedNativeRawObservation
```

The device does not import `NativeEvidenceExpectation` and does not produce semantic dispositions.

## No Boolean shortcut

The legacy compatibility path based on:

```text
NativeObservationFact(bool)
```

is not used by the 07B canonical command.

07B path:

```text
R3 NativeRawObservation
-> VerifiedNativeRawObservation
-> Manager reducer
```

No Device raw-to-bool pre-reduction is admitted.

## Core semantic contract binding

07B regenerates the current scheduled EvidencePlans directly from:

```text
ash_core::native_evidence_spec_catalog()
+
current native orchestration program
+
Factory materialize_plan_set()
```

It does not call the NATIVE-06 fixture execution receipt builder to obtain semantic results.

For each operation, Manager requires exact equality between the materialized plan and its Core `NativeEvidenceSpecification`:

```text
authority_id == owner_authority
contract_id == owner_contract
invariant_id == invariant_id
evidence_kind == evidence_kind
evidence_phase == evidence_phase
operation_key == request.operation_key
expectation == expectation
```

The Core specification itself is canonically hashed as `semanticContractDigest`.

## Exact plan binding

For all 27 operations:

```text
RequestEntry.operation_key
== EvidencePlan.operation_key
== BatchEntry.operation_key
== Envelope.operation_key

RequestEntry.plan_digest
== EvidencePlan.plan_digest
== BatchEntry.plan_digest
== Envelope.plan_digest
```

Any drift is fail-closed structural failure, not semantic `Failed`.

## Reducer identity

Every current Core expectation variant has an exact Manager reducer ID:

```text
StateLegal -> manager.reducer.state-legal.v1
TransitionLegal -> manager.reducer.transition-legal.v1
NonRegressing -> manager.reducer.non-regressing.v1
Fresh -> manager.reducer.fresh.v1
Exclusive -> manager.reducer.exclusive.v1
SingleOwner -> manager.reducer.single-owner.v1
AdmissionLegal -> manager.reducer.admission-legal.v1
CanonicallyOrdered -> manager.reducer.canonical-order.v1
RoutingDisjoint -> manager.reducer.routing-disjoint.v1
CommitConsistent -> manager.reducer.commit-consistent.v1
RecoverySafe -> manager.reducer.recovery-safe.v1
ProvenanceConsistent -> manager.reducer.provenance-consistent.v1
StructuralBoundaryIntact -> manager.reducer.structural-boundary.v1
QualificationSatisfied -> manager.reducer.qualification-satisfied.v1
```

Reducer selection is driven only by the Core expectation carried by the exact plan. It is not selected by operation-key prefix or raw-field guessing.

## R2 source-snapshot schema admission

The currently admitted raw observation types are exactly the R2 source-provenance families:

```text
ash.native.owner.runtime-source-snapshot.v1
ash.native.owner.typed-receipt-source-snapshot.v1
ash.native.owner.typed-artifact-source-snapshot.v1
ash.native.owner.filesystem-source-snapshot.v1
ash.native.owner.process-source-snapshot.v1
ash.native.owner.rust-structure-source-snapshot.v1
```

Their required physical provenance fields and raw types are validated before reduction.

Unknown observation type:

```text
ReductionInputSchemaMismatch
```

Missing required physical field:

```text
ReductionInputIncomplete
```

Wrong raw field type:

```text
ReductionInputTypeMismatch
```

These are structural reduction failures and do not generate semantic `Failed` results.

## Current semantic sufficiency rule

For the admitted R2 source-snapshot observations:

```text
semantic_input_sufficient=false
semantic_input_reason=R2_SOURCE_PROVENANCE_ONLY_NO_DOMAIN_SEMANTIC_FACTS
disposition=HeldInsufficientRawEvidence
```

This rule is deliberate fail-closed behavior.

07B does NOT map:

```text
owner_source_present=true -> Satisfied
source hash exists -> Satisfied
public item count > 0 -> Satisfied
```

Those facts prove source provenance only and do not prove invariant semantics.

## Reduction result

Each exact operation produces one `NativeManagerReductionResult` binding:

```text
operation_key
authority_id
contract_id
invariant_id
plan_digest
batch_manifest_digest
observation_digest
observation_envelope_digest
observation_type
semantic_reducer_id
semantic_reducer_program_digest
semantic_contract_digest
semantic_input_sufficient
semantic_input_reason
disposition
reduction_digest
```

`reduction_digest` is the canonical SHA256 of the result with its digest field cleared.

## Reduction manifest

Schema:

```text
ash.control_runtime.native_manager_reduction_manifest.v1
```

The manifest binds:

```text
request_manifest_digest
producer_route_registry_digest
observer_adoption_manifest_digest
batch_manifest_digest
semantic_contract_registry_digest
semantic_reducer_registry_digest
27 canonical results
result_set_digest
reduction_manifest_digest
```

Results are sorted lexically by `operation_key`.

## Immutable publication

Default reduction root:

```text
artifacts/control_runtime/native_manager_reductions/
```

Final path:

```text
<reductionManifestDigest>/native_manager_reduction_manifest.json
```

Publication uses a staging directory followed by atomic directory promotion.

An existing content-addressed reduction is accepted only after exact manifest revalidation. It is never silently overwritten or repaired.

## Authority-scoped telemetry

07B replaces the ambiguous global expectation/verdict view with explicit authority counters:

```text
producerSemanticVerdictCount=0
observerSemanticVerdictCount=0
deviceSemanticVerdictCount=0
managerSemanticVerdictCount=27

producerExpectedValueReadCount=0
observerExpectedValueReadCount=0
deviceExpectedValueReadCount=0
managerExpectedContractReadCount=27
```

Legacy and synthetic paths remain zero:

```text
legacyOracleReadCount=0
legacyVerdictImportCount=0
pythonValidatorExecutionCount=0
fixtureVerdictCount=0
syntheticVerdictCount=0
```

## Current expected physical outcome

Because R2 intentionally produced source-provenance snapshots rather than domain-semantic witness fields, the expected first 07B result is:

```text
batchEntryCount=27
managerReductionRequestedCount=27
managerReductionCompletedCount=27
managerReductionMissingCount=0
managerReductionDuplicateCount=0
coreContractMismatchCount=0
reducerUnavailableCount=0
reductionInputSchemaMismatchCount=0
reductionInputIncompleteCount=0
reductionInputTypeMismatchCount=0

producerSemanticVerdictCount=0
observerSemanticVerdictCount=0
deviceSemanticVerdictCount=0
managerSemanticVerdictCount=27

satisfiedCount=0
failedCount=0
heldUnsupportedCapabilityCount=0
heldInsufficientRawEvidenceCount=27
failedInfrastructureCount=0
staleEvidenceCount=0

managerReductionClosed=true
allCurrentInvariantsSatisfied=false
currentScheduledEvidenceExecutionClosed=false
productionAuthorityClaimed=false
```

The exact semantic aggregate is evidence. It must not be patched merely to make `Satisfied=27`.

## Closure meaning

```text
managerReductionClosed=true
```

means:

```text
all 27 exact R3 raw inputs were verified,
all 27 exact Core semantic contracts were resolved,
all 27 Manager reducer routes were resolved,
and all 27 reductions produced explicit dispositions without authority leakage.
```

It does NOT mean:

```text
allCurrentInvariantsSatisfied=true
```

Those are separate truths.

## Expected command

```text
native-manager-reduce
```

The exact R3 `batchManifestDigest` is mandatory. No automatic newest-batch discovery is admitted.

## Mandatory gates

```text
PASS_07B_PARENT_R3_BATCH_VALID
PASS_07B_EXACT_BATCH_DIGEST_REQUIRED
PASS_07B_DEVICE_VERIFIED_RAW_HANDOFF
PASS_07B_ZERO_DEVICE_SEMANTIC_VERDICT
PASS_07B_NO_BOOLEAN_COMPATIBILITY_SHORTCUT
PASS_07B_27_BATCH_ENTRIES
PASS_07B_EXACT_REQUEST_PLAN_BATCH_OPERATION_SET
PASS_07B_EXACT_PLAN_DIGEST_BINDING
PASS_07B_EXACT_CORE_SPEC_BINDING
PASS_07B_CORE_SEMANTIC_CONTRACT_DIGEST
PASS_07B_14_EXPECTATION_REDUCER_IDENTITIES
PASS_07B_NO_OPERATION_PREFIX_REDUCER_ROUTING
PASS_07B_R2_SOURCE_SNAPSHOT_SCHEMA_VALIDATION
PASS_07B_27_MANAGER_REDUCTION_REQUESTS
PASS_07B_27_MANAGER_REDUCTION_COMPLETIONS
PASS_07B_ZERO_MISSING_REDUCTION
PASS_07B_ZERO_DUPLICATE_REDUCTION
PASS_07B_ZERO_CORE_CONTRACT_MISMATCH
PASS_07B_ZERO_REDUCER_UNAVAILABLE
PASS_07B_ZERO_RAW_SCHEMA_MISMATCH
PASS_07B_ZERO_RAW_INPUT_INCOMPLETE
PASS_07B_ZERO_RAW_INPUT_TYPE_MISMATCH
PASS_07B_MANAGER_ONLY_SEMANTIC_DISPOSITION
PASS_07B_HELD_INSUFFICIENT_RAW_EVIDENCE_DISTINCT
PASS_07B_NO_SOURCE_PRESENCE_TO_SATISFIED_SHORTCUT
PASS_07B_RESULT_DIGEST
PASS_07B_RESULT_SET_DIGEST
PASS_07B_REDUCTION_MANIFEST_DIGEST
PASS_07B_CONTENT_ADDRESSED_REDUCTION
PASS_07B_ATOMIC_REDUCTION_PROMOTION
PASS_07B_IDEMPOTENT_REDUCTION_REPLAY
PASS_07B_ZERO_LEGACY_ORACLE
PASS_07B_ZERO_LEGACY_VERDICT_IMPORT
PASS_07B_ZERO_PYTHON_VALIDATOR
PASS_07B_ZERO_FIXTURE_VERDICT
PASS_07B_ZERO_SYNTHETIC_VERDICT
PASS_07B_MANAGER_REDUCTION_CLOSED
PASS_07B_ALL_CURRENT_INVARIANTS_NOT_FABRICATED
PASS_07B_CURRENT_SCHEDULED_EXECUTION_NOT_YET_CLOSED
PASS_07B_NO_PRODUCTION_AUTHORITY_CHANGE
```

## Explicit non-goals

```text
No R2 raw observer rewrite
No R3 batch rewrite
No live owner-state re-observation in Manager
No production authority promotion
No legacy gate supersession
No Python retirement
No forced Satisfied count
No automatic repair of Held results
```

## Completion truth

```text
Before 07B:
The system owns one exact immutable 27-entry raw evidence snapshot,
but no current canonical path interprets that snapshot.

After 07B:
Device verifies the exact R3 batch without semantic judgment.
Manager binds every verified raw observation to the exact current EvidencePlan
and the exact Core EvidenceSpecification.
Only Manager emits semantic dispositions.

All 27 current reductions complete without producer, observer, or Device verdict leakage.

Because the current R2 raw payload contains provenance-only source snapshots,
all 27 current results truthfully hold as HeldInsufficientRawEvidence rather than
fabricating domain semantic PASS/FAIL values.

Manager reduction authority is closed.
Domain-semantic evidence sufficiency is not yet closed.
Current scheduled evidence execution remains open.
Production authority remains false.
```

## Next implication

Before NATIVE-08 can honestly target `currentScheduledEvidenceExecutionClosed=true`, the owner-local observers must be upgraded with operation-specific domain-semantic raw witness fields for the held contracts, without moving semantic verdict logic out of Manager.

That follow-up should preserve the R1 route SSOT, R3 batch transaction law, and 07B Manager-only reduction authority.
