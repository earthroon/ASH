# ASH-CONTROL-RUNTIME-NATIVE-DOMAIN-SEMANTIC-RAW-WITNESS-CLOSURE-07C

## Status

```text
Patch ID:
ASH-CONTROL-RUNTIME-NATIVE-DOMAIN-SEMANTIC-RAW-WITNESS-CLOSURE-07C

Parent:
ASH-CONTROL-RUNTIME-NATIVE-RAW-OBSERVATION-MANAGER-REDUCTION-07B

Role:
R2 Provenance-Only Observation
-> Exact Core Raw-Witness Specification
-> Owner-Local Domain-Witness Capability Fact
-> V4 Raw Observation
-> R3 Immutable Batch
-> 07B Manager-Only Disposition

Production authority: false
Current scheduled evidence execution closure: false
```

## Parent truth

07B physically proved:

```text
batchEntryCount=27
managerReductionRequestedCount=27
managerReductionCompletedCount=27
coreContractMismatchCount=0
reducerUnavailableCount=0
reductionInputSchemaMismatchCount=0
reductionInputIncompleteCount=0
reductionInputTypeMismatchCount=0
producerSemanticVerdictCount=0
observerSemanticVerdictCount=0
deviceSemanticVerdictCount=0
managerSemanticVerdictCount=27
heldInsufficientRawEvidenceCount=27
managerReductionClosed=true
productionAuthorityClaimed=false
```

The open condition was raw-evidence sufficiency. R2 observations proved owner-source provenance but did not expose an explicit domain-witness capability contract.

## Authority law

```text
Route authority:
R1 Core / Factory

Physical observer authority:
owner-local producer

Raw witness schema authority:
Core

Batch integrity authority:
R3 control runtime

Semantic contract authority:
Core

Semantic disposition authority:
Manager only
```

07C does not move PASS/FAIL/HOLD authority into producer, observer, or Device.

## Raw witness SSOT

New Core module:

```text
crates/ash_core/src/native_raw_witness_contract.rs
```

Core defines:

```text
NativeRawWitnessFamily
NativeRawWitnessValueKind
NativeRawWitnessFieldSpecification
NativeDomainRawWitnessSpecification
NativeDomainRawWitnessRegistry
```

Registry schema:

```text
ash.control_runtime.native_domain_raw_witness_registry.v1
```

The current registry is materialized from the exact 27 request operation keys. It binds each operation to:

```text
operation_key
owner_authority_id
producer_endpoint_id
witness_family
observation_type
required raw fields
fields required when live witness capability is available
witness_spec_digest
```

It contains no expected disposition and no semantic PASS/FAIL value.

## Current scheduled witness families

The current 27-operation schedule physically contains ten invariant families:

```text
StateLegality             2
TransitionLegality        2
Routing                    1
CommitIntegrity            4
Ownership                  3
Admission                  4
Provenance                 3
Structural                 1
Qualification              4
RecoveryIntegrity          3
                          --
Total                     27
```

The Core raw-witness family enum also reserves the remaining semantic families so later schedules do not require a competing registry type.

## Exact registry digest

Every specification is sealed independently:

```text
RawWitnessSpecDigest
= SHA256(canonical spec with witness_spec_digest cleared)
```

The current exact registry is then sealed:

```text
RawWitnessRegistryDigest
= SHA256(canonical ordered registry with raw_witness_registry_digest cleared)
```

Specifications are ordered lexically by `operation_key`.

## No producer semantic reinterpretation

The producer receives an exact `NativeDomainRawWitnessSpecification` already materialized by Core.

Forbidden producer inputs/branches remain:

```text
NativeEvidenceExpectation
NativeInvariantEvidenceDisposition
EvidenceKind-based witness routing
expected disposition
legacy verdict
Python validator output
```

The producer may read the raw-witness family and field contract because those define what physical facts belong to the envelope, not what semantic result they imply.

## Current owner-process capability truth

The current physical producer executable is an out-of-band native probe process. It is not the live training/optimizer owner process, and current owner runtimes do not export their live mutable state through a native probe ABI into that process.

07C must not fabricate live state such as:

```text
actual_state
before_state
after_state
active_generation
lease_owner
commit witness
qualification measurement
```

when that state is not physically available.

Therefore the current exact raw witness reports:

```text
witness_capability_available=false
witness_capability_reason=OWNER_LIVE_STATE_NOT_EXPORTED_TO_NATIVE_PROBE_PROCESS
```

This Boolean is a physical capability fact. It is not a semantic HOLD verdict.

## Domain-witness raw observation

Current observation type:

```text
ash.native.domain-witness.v1
```

Required physical fields:

```text
owner_authority_id
producer_endpoint_id
witness_family
witness_capability_available
witness_capability_reason
witness_source_kind
witness_source_identity
witness_source_digest
witness_observation_epoch
probe_process_id
probe_executable
```

The current source identity/digest remains audit provenance, but the envelope is no longer classified as an R2 source-snapshot observation. It explicitly states the domain-witness capability boundary.

## Reserved family fields

When a future owner runtime exports live witness capability, the same Core registry already defines the raw shape expected for the fourteen families.

Examples:

```text
StateLegal:
actual_state / state_revision / state_epoch

TransitionLegal:
before_state / after_state / transition_epoch / transition_sequence

NonRegressing:
previous_revision / current_revision

Fresh:
subject_epoch / observation_epoch

Exclusive:
active_holder_count / active_holder_ids / active_lease_ids

SingleOwner:
observed_owner_count / observed_owner_ids

AdmissionLegal:
current_state / candidate_state / admission_gate_ids / admission_gate_states /
available_capability_ids

CanonicallyOrdered:
observed_order_keys / observed_order_ordinals / observed_item_count

RoutingDisjoint:
route_subject_ids / route_owner_ids / route_endpoint_ids / route_partition_ids

CommitConsistent:
candidate_digest / committed_digest / materialized_digest / declared_parent_digest /
commit_epoch / commit_marker_present

RecoverySafe:
lease_record_present / lease_owner_id / lease_expiry_epoch / observation_epoch /
recovery_claimant_id / recovery_generation / active_generation /
last_committed_generation / external_effect_state

ProvenanceConsistent:
source_identity / source_digest / derived_identity / derived_digest /
declared_parent_digest / producer_program_digest / provenance_chain

StructuralBoundaryIntact:
component_ids / dependency_edges / authority_edges / mutable_owner_ids

QualificationSatisfied:
capability_available / measurement_names / measurement_values_scaled /
measurement_scales / sample_count / qualification_artifact_digests /
qualification_epoch
```

Those fields are required only when `witness_capability_available=true`.

## Witness != verdict

Forbidden raw fields include semantic conclusions such as:

```text
is_legal
is_valid
is_safe
is_fresh
is_exclusive
is_single_owner
passed
failed
satisfied
expected_match
qualification_passed
```

An actual physical Boolean such as `witness_capability_available` is permitted because it reports capability state, not invariant satisfaction.

## V4 envelope

07C adds:

```text
ash.control_runtime.native_domain_probe_observation.v4
```

`NativeDomainProbeObservationEnvelopeV4` preserves the R3/R2 identity chain and adds:

```text
raw_witness_spec_digest
raw_witness_registry_digest
```

Full binding remains:

```text
operation key
plan digest
request manifest digest
producer route digest
producer route registry digest
owner authority
producer endpoint
observer program digest
observer adoption digest
raw witness spec digest
raw witness registry digest
raw observation digest
raw envelope digest
```

## R1 route preservation

07C does not alter:

```text
native_producer_binding_contract.rs
factory/native_producer_route.rs
native_probe_request.rs
```

Raw witness schema is not route topology.

## Observer adoption

The exact R2 route-level observer registry remains the destination registry. 07C changes the observer implementation revision and therefore the observer program/adoption identity may legitimately change.

This does not mutate R1 producer-route identity.

## Producer receipt v4

Schema:

```text
ash.basetrain.native_domain_probe_producer_receipt.v4
```

Required current closure counters:

```text
rawWitnessSpecificationCount=27
rawWitnessReaderBindingCount=27

domainSemanticWitnessRequestedCount=27
domainSemanticWitnessEmittedCount=27
domainSemanticWitnessMissingCount=0

provenanceOnlyObservationCount=0

rawWitnessSpecUnboundCount=0
rawWitnessReaderUnboundCount=0
rawWitnessSpecDigestMismatchCount=0
rawWitnessRegistryDigestMismatchCount=0
rawWitnessOwnerMismatchCount=0
rawWitnessEndpointMismatchCount=0
rawWitnessSchemaMismatchCount=0
rawWitnessMissingFieldCount=0
rawWitnessTypeMismatchCount=0
witnessSnapshotUnstableCount=0

domainRawWitnessClosure=true
productionAuthorityClaimed=false
```

Legacy semantic isolation remains:

```text
producerSemanticVerdictCount=0
observerSemanticVerdictCount=0
expectedValueReadCount=0
legacyOracleReadCount=0
pythonValidatorExecutionCount=0
fixtureObservationCount=0
syntheticObservationCount=0
```

## R3 reuse

R3 keeps its batch-v2 transaction law:

```text
27 exact V4 observations
-> individual rehash
-> exact operation set
-> canonical entries
-> manifest-last
-> atomic promotion
-> content-addressed batch
```

R3 now admits the current V4 envelope schema. Batch structure is not semantically reinterpreted.

A new V4 observation set produces a new `batchManifestDigest`; historical R3 directories are not rewritten.

## Device boundary

The Device verifies V4 envelope identity and digest integrity, including the presence of 64-hex raw-witness spec/registry digests.

Device does not resolve Core semantic expectations and does not produce a semantic disposition.

## Manager exact raw-witness binding

Before reduction, Manager independently rematerializes the Core raw-witness registry from the exact request operation set.

For each operation:

```text
plan.operation_key
== witness_spec.operation_key

authority_id
== witness_spec.owner_authority_id

producer endpoint
== witness_spec.producer_endpoint_id

envelope.raw_witness_spec_digest
== Core witness spec digest

envelope.raw_witness_registry_digest
== current Core raw witness registry digest
```

Mismatch is a structural reduction failure, not semantic `Failed`.

## Current semantic disposition

For the current physical producer:

```text
witness_capability_available=false
```

is sufficient evidence for Manager to produce:

```text
HeldUnsupportedCapability
```

Manager sets:

```text
semantic_input_sufficient=true
semantic_input_reason=OWNER_LIVE_STATE_NOT_EXPORTED_TO_NATIVE_PROBE_PROCESS
```

This is intentionally different from the parent state:

```text
HeldInsufficientRawEvidence
```

The system now knows *why* the domain-semantic result cannot be evaluated: the live owner witness capability itself is absent.

## No forced PASS

07C does not require:

```text
satisfiedCount=27
```

The current expected first result is conservatively:

```text
satisfiedCount=0
failedCount=0
heldUnsupportedCapabilityCount=27
heldInsufficientRawEvidenceCount=0
failedInfrastructureCount=0
staleEvidenceCount=0
```

This is a valid 07C structural closure because no semantic value was fabricated.

## Manager reduction identity v2

07C changes Manager reducer input handling for exact domain-witness capability facts. Therefore the reducer program revision and resulting `semanticReducerRegistryDigest` change. This is an implementation identity revision, not a transfer of semantic authority away from Manager.

The Manager reduction manifest/receipt schema revision is advanced to v2 so the exact `raw_witness_registry_digest` is explicitly bound beside:

```text
R3 batch digest
semantic contract registry digest
semantic reducer registry digest
```

The Manager remains the sole semantic disposition owner.

## Required downstream proof

07C qualification requires:

```text
R3 observationBatchValid=true
07B managerReductionClosed=true
heldInsufficientRawEvidenceCount=0
producerSemanticVerdictCount=0
observerSemanticVerdictCount=0
deviceSemanticVerdictCount=0
managerSemanticVerdictCount=27
```

`HeldUnsupportedCapability` is permitted and must remain distinct from insufficient raw evidence.

## Explicit non-goals

```text
No live state fabrication
No source-present -> Satisfied shortcut
No observer PASS/FAIL/HOLD
No Device PASS/FAIL/HOLD
No expected-value read outside Manager
No R1 route rewrite
No old content-addressed batch rewrite
No Python validator
No legacy oracle
No production promotion
No current-scheduled execution closure
```

## Mandatory gates

```text
PASS_07C_PARENT_07B_MANAGER_REDUCTION_VALID
PASS_07C_R1_ROUTE_SSOT_PRESERVED
PASS_07C_RAW_WITNESS_REGISTRY_27
PASS_07C_RAW_WITNESS_REGISTRY_DIGEST
PASS_07C_RAW_WITNESS_SPEC_DIGESTS
PASS_07C_EXACT_OPERATION_OWNER_ENDPOINT_BINDING
PASS_07C_ZERO_WITNESS_SPEC_UNBOUND
PASS_07C_ZERO_WITNESS_READER_UNBOUND
PASS_07C_NO_EVIDENCE_KIND_WITNESS_ROUTING
PASS_07C_NO_EXPECTATION_READ_AT_PRODUCER
PASS_07C_NO_EXPECTATION_READ_AT_OBSERVER
PASS_07C_DOMAIN_WITNESS_V4_IDENTITY
PASS_07C_27_DOMAIN_WITNESS_ENVELOPES
PASS_07C_ZERO_PROVENANCE_ONLY_CURRENT_OBSERVATIONS
PASS_07C_ZERO_WITNESS_SCHEMA_MISMATCH
PASS_07C_ZERO_WITNESS_MISSING_FIELD
PASS_07C_ZERO_WITNESS_TYPE_MISMATCH
PASS_07C_NO_LIVE_STATE_FABRICATION
PASS_07C_CAPABILITY_FACT_NOT_SEMANTIC_VERDICT
PASS_07C_ZERO_PRODUCER_SEMANTIC_VERDICT
PASS_07C_ZERO_OBSERVER_SEMANTIC_VERDICT
PASS_07C_R3_V4_BATCH_VALID
PASS_07C_DEVICE_ZERO_SEMANTIC_VERDICT
PASS_07C_MANAGER_EXACT_WITNESS_REGISTRY_BINDING
PASS_07C_MANAGER_REDUCTION_27_OF_27
PASS_07C_ZERO_HELD_INSUFFICIENT_RAW_EVIDENCE
PASS_07C_HELD_UNSUPPORTED_DISTINCT
PASS_07C_NO_FORCED_SATISFIED_COUNT
PASS_07C_ZERO_LEGACY_ORACLE
PASS_07C_ZERO_PYTHON_VALIDATOR
PASS_07C_DOMAIN_RAW_WITNESS_CLOSED
PASS_07C_CURRENT_SCHEDULED_EXECUTION_NOT_YET_CLOSED
PASS_07C_NO_PRODUCTION_AUTHORITY_CHANGE
```

## Completion truth

```text
Before 07C:
The physical observation path was valid, but the raw envelope only proved source provenance.
Manager could not tell whether domain-semantic witness capability existed, so all 27 results
correctly held as HeldInsufficientRawEvidence.

After 07C:
Core owns one exact raw-witness specification per current operation.
Each V4 observation is bound to the exact witness-spec and witness-registry digests.
The owner probe reports the actual current capability boundary rather than fabricating live state.
R3 seals the new V4 observations without changing its atomic publication law.
Device verifies them without semantic judgment.
Manager rematerializes the exact Core raw-witness registry and remains the only semantic judge.

For the current standalone probe surface, all 27 operations truthfully report that live owner-state
witness export is not available. Manager therefore produces HeldUnsupportedCapability rather than
HeldInsufficientRawEvidence or fabricated Satisfied/Failed results.

Domain-witness capability identity is closed.
HeldInsufficientRawEvidence is closed to zero.
Live owner-state export itself remains a later capability milestone.
Current scheduled native execution remains open.
Production authority remains false.
```

## Next implication

The next work should not bypass this HOLD. A later owner-runtime witness-export revision must bind
actual state/transition/ownership/commit/recovery/qualification measurements into the reserved V4
family fields. Once those live exporters exist, the same Manager authority can convert the
`HeldUnsupportedCapability` results into actual `Satisfied` / `Failed` / capability-specific outcomes.
