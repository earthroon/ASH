# ASH-CONTROL-RUNTIME-NATIVE-PRODUCER-ROUTE-SSOT-CLOSURE-07A-R1

## Status

```text
Patch ID: ASH-CONTROL-RUNTIME-NATIVE-PRODUCER-ROUTE-SSOT-CLOSURE-07A-R1
Parent: ASH-CONTROL-RUNTIME-NATIVE-RAW-OBSERVATION-ABI-AND-PRODUCER-ADOPTION-07A
Role: Core-owned producer binding law and Factory-owned immutable producer-route materialization
Production authority: false
Actual observer adoption expansion: forbidden
Semantic evidence execution expansion: forbidden
Python validator execution: forbidden
```

## Authority declaration

```text
Core Producer Binding Contract /
Factory Producer Route Materialization /

No Producer-Side EvidenceKind Reinterpretation /
No Owner-Domain Route Policy /

Immutable Producer Route Registry /
Route Registry Digest /

Owner Authority Identity /
Producer Endpoint Identity Separation /

27 Scheduled Operations /
27 Exact Producer Routes /
0 Unbound /
0 Duplicate /

No Semantic Verdict At Producer /
No Expected Value Read /
No Legacy Oracle Read
```

## 1. Parent problem

07A established the raw observation ABI and an owner-domain producer scaffold, but the producer still reconstructed routing from `EvidenceKind`.

```text
request EvidenceKind
  -> base_train producer_kind(...)
  -> ProducerKind
  -> producer identity
```

That makes the observation owner a second routing-policy author. 07A-R1 removes that authority from the owner domain without adopting any observer.

## 2. Final authority flow

```text
CORE
  immutable evidence semantics
  authority identity
  producer binding law
       |
       v
ORCHESTRATOR
  scheduled authority/workflow set
       |
       v
MANAGER
  lifecycle and semantic reduction only
       |
       v
FACTORY
  immutable EvidencePlan
  immutable ProducerRouteRegistry
       |
       v
DEVICE / OWNER DOMAIN
  exact pre-bound route consumption only
       |
       v
RAW OBSERVATION
```

`Core -> Orchestrator -> Manager -> Factory -> Device` is an authority flow, not a Rust reverse-dependency rule. `ash_core` remains the lowest shared contract crate.

## 3. Core Producer Binding Contract

New Core module:

```text
crates/ash_core/src/native_producer_binding_contract.rs
```

Core owns the exact binding relationship:

```text
OperationKey
+ OwnerAuthorityId
+ ProducerKind
+ ProducerEndpointId
+ BindingRevision
+ BindingDigest
```

Canonical type:

```rust
pub struct NativeProducerBindingContract {
    pub operation_key: String,
    pub owner_authority_id: String,
    pub producer_kind: NativeObservationProducerKind,
    pub producer_endpoint_id: String,
    pub binding_revision: String,
    pub binding_digest: String,
}
```

`operation_key` is the primary lookup key. Legacy validator ordinal/path, expected legacy disposition, contract ordinal, or filesystem location cannot be route authority.

## 4. EvidenceKind law

`EvidenceKind` remains Core-owned evidence semantics. It may participate in building the Core binding catalog, but the mapping is authored once in Core and materialized into explicit binding records.

Forbidden duplication:

```text
Core: EvidenceKind -> ProducerKind
AND
base_train: EvidenceKind -> ProducerKind
```

Final law:

```text
Core = sole route-policy author
Factory = materializer
Producer = route consumer
```

## 5. Owner authority and producer endpoint separation

These identities answer different questions.

```text
OwnerAuthorityId
= which native authority owns the semantic invariant

ProducerEndpointId
= which concrete native endpoint supplies the physical observation
```

They are separate fields and separate validation truths. `producer_endpoint_id = authority_id` is not an implicit alias rule.

Current explicit endpoint identities are Core constants for:

```text
NativeRuntime
NativeTypedReceipt
NativeTypedArtifact
NativeFilesystemProbe
NativeProcessProbe
NativeStructureProbe
```

No Fixture, Synthetic, LegacyOracle, PythonValidator, or ExpectedValue producer kind exists in the production binding law.

## 6. Factory Producer Route Materialization

New Factory module:

```text
crates/ash_control_runtime/src/factory/native_producer_route.rs
```

Factory input:

```text
Scheduled NativeEvidencePlan set
+ Core ProducerBindingCatalog
```

Factory output:

```text
NativeProducerRouteRegistry
```

Canonical route:

```rust
pub struct NativeProducerRoute {
    pub operation_key: String,
    pub owner_authority_id: String,
    pub producer_kind: NativeObservationProducerKind,
    pub producer_endpoint_id: String,
    pub binding_digest: String,
    pub route_digest: String,
}
```

The Factory may join and validate. It may not reinterpret `EvidenceKind`, synthesize endpoint IDs, or create a fallback route.

## 7. Immutable route registry

```rust
pub struct NativeProducerRouteRegistry {
    pub schema: String,
    pub core_binding_catalog_digest: String,
    pub route_count: u32,
    pub routes: Vec<NativeProducerRoute>,
    pub route_registry_digest: String,
}
```

Canonical schema:

```text
ash.control_runtime.native_producer_route_registry.v1
```

Routes are sorted lexically by `operation_key` before registry sealing.

Identity chain:

```text
Core ProducerBindingCatalogDigest
  -> Route BindingDigest
  -> RouteDigest
  -> ProducerRouteRegistryDigest
```

Observer adoption state is not part of route topology.

## 8. Route topology versus adoption state

07A mixed route identity with `actual_observer_adopted`. 07A-R1 separates them.

```text
ProducerRouteRegistryDigest
= immutable topology identity

Observer adoption
= runtime completion state
```

Therefore this state is valid and required for R1:

```text
ProducerRouteRegistryValid = true
ProducerAdoptionClosed = false
ActualObserverAdoptedCount = 0
ActualObserverPendingCount = 27
```

A valid route registry must not fabricate evidence execution.

## 9. Request ABI v2

Producer-facing request schema is bumped to:

```text
ash.control_runtime.native_probe_request.v2
```

Request entry becomes:

```rust
pub struct NativeProbeRequestEntry {
    pub operation_key: String,
    pub plan_digest: String,
    pub producer_route_digest: String,
}
```

Producer-facing request entries no longer contain:

```text
authority_id
contract_id
invariant_id
evidence_kind
evidence_phase
expectation
expected disposition
```

The request manifest binds the exact route registry digest:

```rust
pub struct NativeProbeRequestManifest {
    pub schema: String,
    pub workflow_mode: String,
    pub orchestration_program_digest: String,
    pub scheduled_evidence_plan_digest: String,
    pub native_probe_registry_digest: String,
    pub producer_route_registry_digest: String,
    pub entries: Vec<NativeProbeRequestEntry>,
    pub request_manifest_digest: String,
}
```

Identity order is acyclic:

```text
Core bindings
  -> route registry
  -> request manifest
```

## 10. Three-way operation-set closure

For the current scheduled surface:

```text
EvidencePlan operation keys
== ProbeRegistry operation keys
== ProducerRouteRegistry operation keys
== RequestManifest operation keys
```

Mandatory cardinality:

```text
ScheduledEvidencePlanCount = 27
NativeProbeBindingCount = 27
ProducerRouteCount = 27
RequestEntryCount = 27
```

Mandatory failures:

```text
Missing Core binding -> fail closed
Owner authority mismatch -> fail closed
Missing endpoint identity -> fail closed
Duplicate operation key -> fail closed
Duplicate route digest -> fail closed
Unexpected route -> fail closed
Probe/route set mismatch -> fail closed
Request/route set mismatch -> fail closed
```

## 11. Owner-domain producer retirement of route policy

Modified owner-domain file:

```text
crates/base_train/src/native_domain_probe_producer.rs
```

Removed authority:

```text
NativeProbeEvidenceKind import
producer_kind(evidence_kind)
route_entry(evidence_kind)
producer_identity = authority_id
```

New producer execution shape:

```text
read request manifest
  -> verify request digest
read route registry
  -> verify every route digest
  -> verify registry digest
verify request binds exact registry digest
exact operation-key join
exact route-digest match
exact endpoint identity admission
  -> observer lookup remains pending in R1
```

The producer cannot derive a route from evidence semantics, authority class, contract ID, invariant ID, legacy state, or operation-key prefix.

## 12. No owner-domain fallback

Forbidden:

```text
route missing -> NativeRuntime
unknown endpoint -> generic observer
operation key prefix -> endpoint family
EvidenceKind -> endpoint
AuthorityId -> endpoint
```

Exact endpoint lookup is allowed only after Core/Factory have already chosen the endpoint.

## 13. Producer receipt

Producer receipt becomes route-consumption evidence rather than route-authoring evidence.

Required fields include:

```text
requestManifestDigest
producerRouteRegistryDigest
requestEntryCount
consumedExactRouteCount
producerRouteUnboundCount
routeDigestMismatchCount
endpointIdentityMismatchCount
duplicateOperationKeyCount

actualObserverAdoptedCount
actualObserverPendingCount
emittedRawObservationCount

producerSideEvidenceKindReadCount
producerSideRoutePolicyBranchCount
producerSemanticVerdictCount
expectedValueReadCount
legacyOracleReadCount
pythonValidatorExecutionCount

producerRouteRegistryValid
producerAdoptionClosed
```

`producerProgramDigest` is no longer route authority.

## 14. R1 expected producer truth

```text
RequestEntryCount = 27
ConsumedExactRouteCount = 27
ProducerRouteUnboundCount = 0
RouteDigestMismatchCount = 0
EndpointIdentityMismatchCount = 0
DuplicateOperationKeyCount = 0

ProducerSideEvidenceKindReadCount = 0
ProducerSideRoutePolicyBranchCount = 0
ProducerSemanticVerdictCount = 0
ExpectedValueReadCount = 0
LegacyOracleReadCount = 0
PythonValidatorExecutionCount = 0

ActualObserverAdoptedCount = 0
ActualObserverPendingCount = 27
EmittedRawObservationCount = 0

ProducerRouteRegistryValid = true
ProducerAdoptionClosed = false
```

The producer command therefore remains intentionally fail-closed after proving route consumption, because R2 has not adopted observers yet.

## 15. New control-runtime CLI

```text
native-producer-route-registry
```

Expected success truth:

```text
ASH_CONTROL_RUNTIME_NATIVE_PRODUCER_ROUTE_SSOT_VALID=true
scheduledOperationCount=27
coreProducerBindingMatchedCount=27
factoryProducerRouteMaterializedCount=27
producerRouteUnboundCount=0
producerRouteUnexpectedCount=0
duplicateProducerOperationKeyCount=0
duplicateProducerRouteDigestCount=0
ownerAuthorityMismatchCount=0
producerEndpointMissingCount=0
probeRegistryOperationMismatchCount=0
requestRouteOperationMismatchCount=0
producerSideEvidenceKindReadCount=0
producerSideRoutePolicyBranchCount=0
producerSemanticVerdictCount=0
expectedValueReadCount=0
legacyOracleReadCount=0
pythonValidatorExecutionCount=0
actualObserverAdoptedCount=0
actualObserverPendingCount=27
emittedRawObservationCount=0
producerRouteRegistryValid=true
producerAdoptionClosed=false
currentScheduledEvidenceExecutionClosed=false
productionAuthorityClaimed=false
```

## 16. Existing evidence execution integration

`native-evidence-execute` now also carries:

```text
ProducerRouteRegistryDigest
ProducerRouteRegistryValid
NativeProducerRouteSsotClosed
```

It does not convert route closure into native evidence closure. Missing actual observations remain the expected fail-closed state.

## 17. Dependency law

Preserved:

```text
ash_control_runtime -> ash_core
base_train -> ash_core
```

Forbidden:

```text
ash_core -> ash_control_runtime
base_train -> ash_control_runtime
ash_control_runtime -> base_train
```

The shared wire types and binding law live in Core so no reverse dependency is required.

## 18. Static forbidden producer patterns

The owner-domain producer must not contain route-policy dependence on:

```text
NativeProbeEvidenceKind
entry.evidence_kind
producer_kind(evidence_kind)
expected_disposition
LegacyValidator
legacy ordinal
Python validator path
```

API-level quarantine is primary: request v2 does not transmit EvidenceKind to the producer. Text scanning is only a regression aid.

## 19. Tests

Required Core tests:

```text
producer_binding_catalog_has_unique_operation_keys
producer_binding_has_explicit_owner_and_endpoint_identity
binding_digest_is_deterministic
```

Required Factory/request tests:

```text
owner_authority_mismatch_fails_closed
route_order_is_canonical
request_v2_does_not_expose_evidence_kind_to_producer
```

Required producer invariant:

```text
producer_route_registry_valid_does_not_imply_observer_adopted
```

## 20. Explicit non-goals

```text
No Actual Observer Adoption
No Raw Observation Emission
No Observation Batch Publication
No Manager Raw Observation Reduction
No Device Semantic Conversion
No Native Evidence PASS Expansion
No Frozen Legacy Gate Migration
No RustPython Retirement
No Production Promotion
```

## 21. Mandatory gates

```text
PASS_07A_R1_PARENT_07A_IDENTITY_VALID
PASS_07A_R1_CORE_PRODUCER_BINDING_CONTRACT_EXISTS
PASS_07A_R1_CORE_IS_SOLE_ROUTE_POLICY_OWNER
PASS_07A_R1_FACTORY_PRODUCER_ROUTE_MATERIALIZATION
PASS_07A_R1_27_SCHEDULED_OPERATIONS
PASS_07A_R1_27_EXACT_PRODUCER_ROUTES
PASS_07A_R1_ZERO_UNBOUND_ROUTE
PASS_07A_R1_ZERO_UNEXPECTED_ROUTE
PASS_07A_R1_ZERO_DUPLICATE_OPERATION
PASS_07A_R1_ZERO_DUPLICATE_ROUTE_DIGEST
PASS_07A_R1_OWNER_AUTHORITY_IDENTITY_EXACT
PASS_07A_R1_PRODUCER_ENDPOINT_IDENTITY_EXPLICIT
PASS_07A_R1_OWNER_AND_ENDPOINT_IDENTITY_SEPARATED
PASS_07A_R1_ROUTE_REGISTRY_CANONICAL_ORDER
PASS_07A_R1_ROUTE_REGISTRY_DIGEST_VALID
PASS_07A_R1_REQUEST_BINDS_ROUTE_REGISTRY_DIGEST
PASS_07A_R1_EVIDENCE_PLAN_OPERATION_SET_PARITY
PASS_07A_R1_PROBE_REGISTRY_OPERATION_SET_PARITY
PASS_07A_R1_REQUEST_OPERATION_SET_PARITY
PASS_07A_R1_NO_PRODUCER_EVIDENCE_KIND_REINTERPRETATION
PASS_07A_R1_NO_OWNER_DOMAIN_ROUTE_POLICY
PASS_07A_R1_NO_ROUTE_FALLBACK
PASS_07A_R1_NO_SEMANTIC_VERDICT_AT_PRODUCER
PASS_07A_R1_NO_EXPECTED_VALUE_READ
PASS_07A_R1_NO_LEGACY_ORACLE_READ
PASS_07A_R1_NO_PYTHON_VALIDATOR_EXECUTION
PASS_07A_R1_ZERO_FAKE_OBSERVER_ADOPTION
PASS_07A_R1_ZERO_FAKE_RAW_OBSERVATION
PASS_07A_R1_ROUTE_CLOSURE_SEPARATE_FROM_ADOPTION_CLOSURE
PASS_07A_R1_NO_PRODUCTION_AUTHORITY_CHANGE
```

## 22. Completion truth

```text
The Core owns the producer binding law.

The Factory projects current scheduled evidence plans onto that law
and materializes an immutable, canonically ordered producer route registry.

Every currently scheduled operation has exactly one explicit route.

Owner authority identity and physical producer endpoint identity are
represented and validated separately.

The owner domain receives no EvidenceKind route authority and cannot
reconstruct producer routing policy.

A valid 27-route topology may coexist with zero adopted observers.
Route closure is not evidence closure.

The producer executes a destination.
It does not choose one.
```

## 23. Next natural revision

```text
ASH-CONTROL-RUNTIME-NATIVE-OWNER-LOCAL-RAW-OBSERVER-ADOPTION-07A-R2
```

R2 may begin only after:

```text
ProducerRouteRegistryValid = true
ScheduledOperationCount = 27
ProducerRouteCount = 27
Unbound = 0
Duplicate = 0
OwnerMismatch = 0
ProducerSideEvidenceKindReadCount = 0
ProducerSideRoutePolicyBranchCount = 0
```
