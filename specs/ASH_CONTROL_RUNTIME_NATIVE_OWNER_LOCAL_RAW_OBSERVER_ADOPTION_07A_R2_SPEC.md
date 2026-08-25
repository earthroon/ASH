# ASH-CONTROL-RUNTIME-NATIVE-OWNER-LOCAL-RAW-OBSERVER-ADOPTION-07A-R2

## Status

```text
Patch ID:
ASH-CONTROL-RUNTIME-NATIVE-OWNER-LOCAL-RAW-OBSERVER-ADOPTION-07A-R2

Parent:
ASH-CONTROL-RUNTIME-NATIVE-PRODUCER-ROUTE-SSOT-CLOSURE-07A-R1

Role:
Exact Producer Route
-> Exact Owner-Local Observer Registration
-> Physical NativeRawObservation Emission

Production authority: false
Semantic verdict authority: not admitted
Atomic observation batch authority: not admitted
```

## Authority declaration

```text
27 Exact Producer Routes /
27 Actual Owner-Local Observer Adoptions /
27 NativeRawObservation Emissions /

Exact Producer Endpoint Dispatch /
No Owner-Domain Route Policy /
No EvidenceKind Reinterpretation /

Owner Authority Identity Preserved /
Producer Endpoint Identity Preserved /
Observer Program Identity /
Observer Adoption Identity /

Request Digest Binding /
Plan Digest Binding /
Producer Route Digest Binding /
Producer Route Registry Digest Binding /

Observation Self Digest /
Observation Envelope Digest /

No Semantic Verdict At Producer /
No Semantic Verdict At Observer /
No Expected Value Read /
No Legacy Oracle Read /
No Python Validator Execution /
No Fixture Observation /
No Synthetic Observation /
No Legacy Oracle Observation /

Observer Adoption Closed /
Raw Observation Emission Closed /
Observation Batch Not Yet Published /
Semantic Evidence Not Yet Closed /
No Production Promotion
```

## Parent truth

07A-R1 physically closed the producer-route SSOT with 27 request entries, 27 exact route consumptions, zero unbound routes, zero route digest mismatches, zero endpoint mismatches, zero duplicate operation keys, zero EvidenceKind reads, zero producer route-policy branches, zero semantic verdicts, zero expected-value reads, zero legacy-oracle reads, and zero Python validator executions. Observer adoption remained intentionally open at 0 adopted / 27 pending.

R2 must not change the R1 route law or request ABI.

## R1 identity preservation

The following R1 authority sources remain unchanged by R2:

```text
crates/ash_core/src/native_producer_binding_contract.rs
crates/ash_control_runtime/src/factory/native_producer_route.rs
crates/ash_control_runtime/src/native_probe_request.rs
```

For identical parent source and scheduling scope, ProducerBindingCatalogDigest, ProducerRouteRegistryDigest, and NativeProbeRequestManifestDigest therefore remain parent identities.

## Core wire additions

`crates/ash_core/src/native_probe_protocol.rs` adds:

```text
ash.control_runtime.native_domain_probe_observation.v3
ash.basetrain.native_owner_observer_adoption.v1
```

New wire types:

```text
NativeOwnerObserverAdoptionEntry
NativeOwnerObserverAdoptionManifest
NativeDomainProbeObservationEnvelopeV3
```

The v3 envelope explicitly binds operation key, plan digest, request manifest digest, producer route digest, producer route registry digest, owner authority ID, producer kind, producer endpoint ID, observer program digest, observer adoption digest, NativeRawObservation, observation digest, and envelope digest.

The ambiguous v2 producer-identity alias is not used for R2 emission.

## Owner-local observer registry

New module:

```text
crates/base_train/src/native_owner_raw_observer.rs
```

The registry key is exactly:

```text
(owner_authority_id, producer_endpoint_id)
```

The registry does not inspect EvidenceKind, EvidencePhase, InvariantClass, expected disposition, legacy ordinal, or operation-key prefixes.

The current scheduled surface requires 20 unique owner/endpoint registrations to cover the 27 exact R1 routes. A physical implementation may serve more than one route, but every route receives its own adoption identity.

## Current owner-program bindings

Current scheduled owners are physically bound to their real native Rust implementation sources, including the production multistep scheduler, TensorCube local-Muon production callsite, BP-DK fission planner, BP-DK control/data binding, BP-DK R2 policy closure, checkpoint reload parity continuation, production activation G1, and production-aware operator review adoption G2.

These are observer implementation bindings only. They do not select routes. Route destination authority was already closed by R1 Core/Factory materialization.

## Physical raw observation law

R2 observers read physical owner-local program state from the exact bound owner source file and current native producer process metadata. Current raw fields include owner authority ID, producer endpoint ID, owner source relative path, source presence, source size, source line count, public-item count, source SHA256, current process ID, and current executable path.

These are raw physical facts only. R2 does not claim that these source-level facts are semantically sufficient to satisfy their invariant. Semantic sufficiency remains outside R2 and belongs to later raw-schema and Manager-reduction closure.

## No semantic leakage

Producer and observer APIs receive no `NativeProbeEvidenceKind`, `NativeEvidenceExpectation`, `NativeInvariantEvidenceDisposition`, expected value, expected disposition, legacy verdict, or Python validator result.

Required counters remain:

```text
producerSideEvidenceKindReadCount=0
producerSideRoutePolicyBranchCount=0
producerSemanticVerdictCount=0
observerSemanticVerdictCount=0
expectedValueReadCount=0
legacyOracleReadCount=0
pythonValidatorExecutionCount=0
fixtureObservationCount=0
syntheticObservationCount=0
legacyOracleObservationCount=0
```

## Observer program and adoption identity

Observer program identity is sealed from:

```text
Patch ID
+ Observer revision
+ OwnerAuthorityId
+ ProducerEndpointId
+ Owner source relative path
+ SHA256(actual owner source bytes)
```

Each exact route then receives an adoption entry binding operation key, route digest, owner authority, producer endpoint, observer program digest, adopted=true, and a canonical adoption digest.

The adoption manifest is sorted by operation key and binds the R1 request manifest digest and producer route registry digest.

## Observation identity

Every observation uses:

```text
ObservationDigest
= SHA256(canonical NativeRawObservation)
```

and:

```text
ObservationEnvelopeDigest
= SHA256(canonical v3 envelope with envelope digest cleared)
```

The producer recomputes observation identity before publication. A mismatch is a hard R2 failure.

## Output authority boundary

Default generated output root:

```text
artifacts/control_runtime/native_domain_probe_observations/
```

The R2 producer recreates this generated root per invocation so stale prior-session observation files cannot silently join the current 27-operation set.

Generated raw observations and the observer adoption manifest are runtime artifacts, not source authority.

R2 publishes individual observation envelopes and an adoption manifest only. It does not yet publish an authoritative atomic `NativeObservationBatchManifest`.

## Required cardinality

```text
requestEntryCount=27
consumedExactRouteCount=27
actualObserverAdoptedCount=27
actualObserverPendingCount=0
requestedObservationCount=27
emittedRawObservationCount=27
producerRouteUnboundCount=0
observerEndpointUnboundCount=0
routeDigestMismatchCount=0
endpointIdentityMismatchCount=0
duplicateOperationKeyCount=0
duplicateObservationOperationKeyCount=0
observationDigestMismatchCount=0
```

Required operation-set equality:

```text
RequestOperationSet
== RouteOperationSet
== AdoptionOperationSet
== RawObservationOperationSet
```

## Producer receipt v3

Schema:

```text
ash.basetrain.native_domain_probe_producer_receipt.v3
```

Expected terminal truth:

```text
ASH_BASETRAIN_NATIVE_DOMAIN_PROBE_OBSERVER_ADOPTION_VALID=true

requestEntryCount=27
consumedExactRouteCount=27
actualObserverAdoptedCount=27
actualObserverPendingCount=0
requestedObservationCount=27
emittedRawObservationCount=27
producerRouteUnboundCount=0
observerEndpointUnboundCount=0
routeDigestMismatchCount=0
endpointIdentityMismatchCount=0
duplicateOperationKeyCount=0
duplicateObservationOperationKeyCount=0
observationDigestMismatchCount=0
fixtureObservationCount=0
syntheticObservationCount=0
legacyOracleObservationCount=0
producerSideEvidenceKindReadCount=0
producerSideRoutePolicyBranchCount=0
producerSemanticVerdictCount=0
observerSemanticVerdictCount=0
expectedValueReadCount=0
legacyOracleReadCount=0
pythonValidatorExecutionCount=0
actualOwnerSourceReadCount=27
producerRouteRegistryValid=true
observerAdoptionClosed=true
rawObservationEmissionClosed=true
observationBatchPublished=false
productionAuthorityClaimed=false
```

A complete R2 producer run exits with code 0.

## No fallback

Forbidden:

```text
unknown endpoint -> generic fallback observer
missing owner -> source guessed by operation prefix
EvidenceKind -> observer selection
InvariantId -> observer selection
legacy validator -> observation
hard-coded expected PASS -> observation
```

Missing exact owner/endpoint registration is fail-closed.

## Semantic boundary

R2 closes:

```text
route -> observer -> raw envelope
```

R2 does not close:

```text
raw envelope -> semantic invariant disposition
```

Therefore the intended post-R2 state is:

```text
observerAdoptionClosed=true
rawObservationEmissionClosed=true
observationBatchPublished=false
currentScheduledEvidenceExecutionClosed=false
productionAuthorityClaimed=false
```

## Mandatory gates

```text
PASS_07A_R2_PARENT_R1_ROUTE_IDENTITY_PRESERVED
PASS_07A_R2_PARENT_R1_REQUEST_IDENTITY_PRESERVED
PASS_07A_R2_27_EXACT_ROUTES
PASS_07A_R2_20_UNIQUE_OWNER_ENDPOINT_REGISTRATIONS
PASS_07A_R2_27_ROUTE_LEVEL_ADOPTIONS
PASS_07A_R2_ZERO_PENDING_OBSERVER
PASS_07A_R2_ZERO_UNBOUND_ENDPOINT
PASS_07A_R2_27_RAW_OBSERVATIONS
PASS_07A_R2_ZERO_DUPLICATE_RAW_OBSERVATION
PASS_07A_R2_ZERO_OBSERVATION_DIGEST_MISMATCH
PASS_07A_R2_REQUEST_DIGEST_BINDING
PASS_07A_R2_PLAN_DIGEST_BINDING
PASS_07A_R2_ROUTE_DIGEST_BINDING
PASS_07A_R2_ROUTE_REGISTRY_DIGEST_BINDING
PASS_07A_R2_OWNER_AUTHORITY_IDENTITY_BINDING
PASS_07A_R2_PRODUCER_ENDPOINT_IDENTITY_BINDING
PASS_07A_R2_OBSERVER_PROGRAM_DIGEST
PASS_07A_R2_OBSERVER_ADOPTION_DIGEST
PASS_07A_R2_OBSERVATION_SELF_DIGEST
PASS_07A_R2_OBSERVATION_ENVELOPE_DIGEST
PASS_07A_R2_NO_EVIDENCE_KIND_REINTERPRETATION
PASS_07A_R2_NO_OWNER_DOMAIN_ROUTE_POLICY
PASS_07A_R2_NO_ROUTE_FALLBACK
PASS_07A_R2_ZERO_FIXTURE_OBSERVATION
PASS_07A_R2_ZERO_SYNTHETIC_OBSERVATION
PASS_07A_R2_ZERO_LEGACY_ORACLE_OBSERVATION
PASS_07A_R2_ZERO_PRODUCER_SEMANTIC_VERDICT
PASS_07A_R2_ZERO_OBSERVER_SEMANTIC_VERDICT
PASS_07A_R2_ZERO_EXPECTED_VALUE_READ
PASS_07A_R2_ZERO_LEGACY_ORACLE_READ
PASS_07A_R2_ZERO_PYTHON_VALIDATOR_EXECUTION
PASS_07A_R2_OBSERVER_ADOPTION_CLOSED
PASS_07A_R2_RAW_OBSERVATION_EMISSION_CLOSED
PASS_07A_R2_BATCH_AUTHORITY_NOT_YET_CLAIMED
PASS_07A_R2_SEMANTIC_EVIDENCE_NOT_YET_CLOSED
PASS_07A_R2_NO_PRODUCTION_AUTHORITY_CHANGE
```

## Completion truth

```text
Before 07A-R2:
27 exact producer routes terminate at pending observer slots.

After 07A-R2:
Every current route resolves through an exact owner/endpoint registration.
Every route receives a route-level observer adoption identity.
Every route emits one physical NativeRawObservation envelope.

The observer receives no semantic expectation and emits no semantic verdict.
Observer adoption is closed.
Raw observation emission is closed.
Atomic batch authority is not closed.
Semantic evidence reduction is not closed.
Production authority remains false.
```

## Next natural revision

```text
ASH-CONTROL-RUNTIME-NATIVE-RAW-OBSERVATION-ATOMIC-BATCH-AND-DIGEST-CLOSURE-07A-R3
```
