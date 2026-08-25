# ASH-CONTROL-RUNTIME-NATIVE-RAW-OBSERVATION-ATOMIC-BATCH-AND-DIGEST-CLOSURE-07A-R3

## Status

```text
Patch ID:
ASH-CONTROL-RUNTIME-NATIVE-RAW-OBSERVATION-ATOMIC-BATCH-AND-DIGEST-CLOSURE-07A-R3

Parent:
ASH-CONTROL-RUNTIME-NATIVE-OWNER-LOCAL-RAW-OBSERVER-ADOPTION-07A-R2

Role:
27 Individual NativeRawObservation Envelopes
-> Exact Immutable Observation Batch
-> Manifest-Last Commit
-> Content-Addressed Atomic Publication
-> End-to-End Digest Closure

Production authority: false
Semantic verdict authority: not admitted
Manager semantic reduction: not admitted
Legacy oracle: forbidden
Python validator execution: forbidden
```

## Parent physical truth

07A-R2 closed the physical observer surface:

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
observerAdoptionClosed=true
rawObservationEmissionClosed=true
observationBatchPublished=false
productionAuthorityClaimed=false
```

R3 must preserve the parent request, producer-route, and observer-adoption identities. It may consume them but may not rewrite them.

## Single purpose

R2 proves that twenty-seven physical raw observations exist. It does not yet prove that those files form one exact immutable snapshot.

R3 closes only:

```text
27 Raw Observation Envelopes
        -> individual digest revalidation
        -> exact operation-set validation
        -> canonical batch entries
        -> batch entry-set digest
        -> batch manifest digest
        -> manifest-last staging commit
        -> atomic directory promotion
        -> content-addressed immutable batch
```

R3 does not evaluate whether the observed facts satisfy any invariant.

## Core batch ABI

The legacy batch-v1 wire types remain available. R3 adds an explicit v2 ABI:

```text
schema:
ash.control_runtime.native_observation_batch.v2

NativeObservationBatchEntryV2
NativeObservationBatchManifestV2
```

A v2 entry binds:

```text
operation_key
plan_digest
producer_route_digest
observer_adoption_digest
observation_digest
observation_envelope_digest
observation_file_name
batch_entry_digest
```

A v2 manifest binds:

```text
request_manifest_digest
producer_route_registry_digest
observer_adoption_manifest_digest
expected_entry_count
entries
batch_entry_set_digest
batch_manifest_digest
```

No semantic verdict, expected value, expected disposition, legacy result, or Python-validator output may enter the batch ABI.

## Authority split

```text
Core
  batch ABI and digest law

Owner producer
  R2 physical raw observation emission only

Control Runtime R3 coordinator
  exact-set validation and publication lifecycle

Device primitive
  physical file read/write/sync/directory rename only

Manager
  no semantic reduction in R3
```

`ash_control_runtime` does not gain a compile dependency on `base_train`.

## R2 parent preservation

R3 does not modify the R1 route materializer, R1 request builder, R2 owner observer registry, or R2 producer.

For identical parent files, the following identities remain the R1/R2 values:

```text
ProducerRouteRegistryDigest
NativeProbeRequestManifestDigest
ObserverAdoptionManifestDigest
```

R3 derives a new batch identity beneath those parent identities.

## Input scope

R3 consumes explicit paths for:

```text
native_probe_request.json
native_producer_route_registry.json
observer_adoption_manifest.json
native_domain_probe_observations/
```

Default paths are under:

```text
artifacts/control_runtime/
```

The publisher never recursively searches the repository for candidate observation files.

The observation root is a strict input scope. Any unexpected non-observation entry is a failure, not a silently ignored fallback.

## Parent digest revalidation

R3 independently recomputes and verifies:

```text
request_manifest_digest
producer route digest for every route
producer_route_registry_digest
observer adoption digest for every adoption entry
observer_adoption_manifest_digest
```

Length-only digest validation is insufficient.

## Observation revalidation

Every `NativeDomainProbeObservationEnvelopeV3` is reparsed and rebound to the current parent identities.

Required exact bindings:

```text
envelope.operation_key
== request entry operation key
== route operation key
== adoption operation key

envelope.plan_digest
== request entry plan digest

envelope.producer_route_digest
== request entry route digest
== route registry route digest

envelope.producer_route_registry_digest
== current route registry digest

envelope.observer_adoption_digest
== exact adoption entry digest

envelope.owner_authority_id
== route owner authority
== adoption owner authority

envelope.producer_endpoint_id
== route endpoint
== adoption endpoint

envelope.observer_program_digest
== adoption observer program digest
```

## Observation self-digest

R3 does not trust the producer's stored digest without recomputation.

```text
ObservationDigest
= SHA256(canonical NativeRawObservation)
```

The stored `observation_digest` must equal the recomputed value.

## Observation envelope digest

R3 also recomputes:

```text
ObservationEnvelopeDigest
= SHA256(canonical envelope with observation_envelope_digest cleared)
```

The stored envelope digest must equal the recomputed value.

R3 never repairs a mismatched digest in place.

## Exact operation-set closure

The following sets must be exactly equal:

```text
RequestOperationSet
== ProducerRouteOperationSet
== ObserverAdoptionOperationSet
== RawObservationOperationSet
== BatchEntryOperationSet
```

Current qualification cardinality:

```text
27 == 27 == 27 == 27 == 27
```

No 26/27 success, wildcard route, latest-file selection, or silent filtering is admitted.

## Missing, duplicate, unexpected, foreign, stale

Missing observation:

```text
expected operation has no envelope
-> ObservationBatchIncomplete
```

Duplicate observation:

```text
same operation key appears more than once
-> ObservationDuplicate
```

Unexpected observation:

```text
operation key is outside current request
-> ObservationUnexpected
```

Foreign observation:

```text
wrong observation schema or non-current physical envelope
-> ObservationForeign
```

Stale observation:

```text
request digest mismatch
or plan digest mismatch
or route digest mismatch
or route-registry digest mismatch
or adoption digest mismatch
or owner/endpoint/program identity mismatch
-> ObservationBatchStale
```

The publisher does not choose a convenient subset from a dirty input directory.

## Canonical filename binding

The R3 publisher reproduces the deterministic operation-key filename encoding used by R2 and requires the physical source filename to match that exact encoding.

Filename is a location binding, not the primary evidence identity. Primary identity remains operation key plus cryptographic envelope identity.

## Batch entry digest

For every validated observation, R3 materializes one batch entry and seals:

```text
BatchEntryDigest
= SHA256(canonical entry with batch_entry_digest cleared)
```

Entries are sorted lexically by `operation_key` before batch-set sealing.

Filesystem enumeration order, observer completion order, mtime, and creation order are not authority.

## Batch entry-set digest

```text
BatchEntrySetDigest
= SHA256(canonical ordered Vec<BatchEntryDigest>)
```

The order is derived only from canonical operation-key ordering.

## Batch manifest digest

```text
BatchManifestDigest
= SHA256(canonical batch manifest with batch_manifest_digest cleared)
```

The manifest binds the exact request, route-registry, adoption-manifest, entry count, canonical entry list, and batch entry-set digest.

## Staging transaction

Default batch root:

```text
artifacts/control_runtime/native_observation_batches/
```

Non-authoritative staging generations live under:

```text
native_observation_batches/.staging/
  <requestDigest>.<processId>.<nonce>/
```

Process ID and nonce are collision-avoidance material only. They are not included in batch identity.

## Manifest-last law

A fresh batch is staged in this order:

```text
1. create generation staging directory
2. create staged observations directory
3. copy all 27 already-validated raw envelopes
4. fsync each staged file
5. serialize sealed batch manifest
6. write and fsync batch manifest LAST
7. atomically rename the completed staging directory to final digest path
8. re-open and revalidate the final batch
```

The manifest is the commit marker inside a generation, but a staging generation is never published authority.

## Content-addressed final path

Final path:

```text
artifacts/control_runtime/native_observation_batches/
  <batchManifestDigest>/
    native_observation_batch_manifest.json
    observations/
      27 exact envelopes
```

No mutable `latest/`, `current/`, or active-directory name is batch authority.

## Atomic promotion

The publication boundary is a directory rename on the same batch-root filesystem:

```text
completed staging generation
-> <batchManifestDigest>/
```

A failure before promotion leaves no published batch.

A staging directory is always non-authoritative.

## Idempotent replay

If the content-addressed final path already exists, R3 does not overwrite it.

It must revalidate:

```text
exact root file set
exact manifest content
batch manifest digest
batch entry-set digest
all 27 entry digests
exact 27 observation filename set
all 27 observation digests
all 27 envelope digests
```

Only an exact existing batch is accepted as an idempotent success.

Any extra file, missing file, changed payload, or manifest mismatch is existing-batch corruption and fails closed.

## No destructive repair

Forbidden:

```text
existing final batch invalid
-> delete it
-> regenerate it
-> PASS
```

A content-addressed corruption must remain visible for explicit recovery.

## Publication receipt

Schema:

```text
ash.control_runtime.native_observation_batch_publication_receipt.v1
```

Required success telemetry includes:

```text
requestManifestDigest
producerRouteRegistryDigest
observerAdoptionManifestDigest

discoveredObservationCount=27
validatedObservationCount=27
missingObservationCount=0
duplicateObservationCount=0
unexpectedObservationCount=0
foreignObservationCount=0
staleObservationCount=0

observationDigestMismatchCount=0
observationEnvelopeDigestMismatchCount=0
requestDigestMismatchCount=0
planDigestMismatchCount=0
producerRouteDigestMismatchCount=0
producerRouteRegistryDigestMismatchCount=0
observerAdoptionDigestMismatchCount=0
ownerAuthorityMismatchCount=0
producerEndpointMismatchCount=0

batchEntryCount=27
batchDuplicateOperationKeyCount=0
batchEntrySetDigest=<sha256>
batchManifestDigest=<sha256>

manifestWrittenLast=true
atomicPromotionSucceeded=true
observationBatchPublished=true
observationBatchValid=true

semanticVerdictCount=0
fixtureObservationCount=0
syntheticObservationCount=0
legacyOracleObservationCount=0
expectedValueReadCount=0
legacyOracleReadCount=0
pythonValidatorExecutionCount=0

currentScheduledEvidenceExecutionClosed=false
productionAuthorityClaimed=false
```

The receipt has its own canonical `receiptHash`. The receipt is execution evidence, not batch identity.

## CLI

New command:

```text
native-observation-batch-publish
```

Default invocation:

```powershell
cargo run -p ash_control_runtime -- `
  native-observation-batch-publish `
  --repo-root .
```

Explicit input/output paths may be provided with:

```text
--request-manifest
--producer-route-registry
--observer-adoption-manifest
--observation-root
--batch-root
--receipt
```

## Expected terminal truth

```text
ASH_CONTROL_RUNTIME_NATIVE_OBSERVATION_BATCH_VALID=true

discoveredObservationCount=27
validatedObservationCount=27
missingObservationCount=0
duplicateObservationCount=0
unexpectedObservationCount=0
foreignObservationCount=0
staleObservationCount=0
observationDigestMismatchCount=0
observationEnvelopeDigestMismatchCount=0
batchEntryCount=27
batchDuplicateOperationKeyCount=0
manifestWrittenLast=true
atomicPromotionSucceeded=true
observationBatchPublished=true
observationBatchValid=true
semanticVerdictCount=0
expectedValueReadCount=0
legacyOracleReadCount=0
pythonValidatorExecutionCount=0
currentScheduledEvidenceExecutionClosed=false
productionAuthorityClaimed=false
failureReason=None
```

A complete R3 publication exits with code 0.

## Semantic boundary

`observationBatchValid=true` means only:

```text
the physical snapshot is exact, complete, immutable, identity-bound, and digest-valid
```

It does not mean:

```text
any invariant is satisfied
any transition is legal
any recovery is safe
any qualification passed
```

R3 imports no `NativeEvidenceExpectation` and produces no `NativeInvariantEvidenceDisposition`.

## Failure separation

R3 provides explicit structural failure identities including:

```text
ObservationBatchMissing
ObservationBatchIncomplete
ObservationBatchStale
ObservationDuplicate
ObservationUnexpected
ObservationForeign
ObservationDigestMismatch
ObservationEnvelopeDigestMismatch
BatchEntrySetMismatch
BatchManifestDigestMismatch
ExistingBatchCorrupt
```

These are physical/identity failures, not semantic invariant verdicts.

## Explicit non-goals

```text
No Manager Semantic Reduction
No NativeEvidenceObservation Boolean Conversion
No StateLegal / TransitionLegal Verdict
No Raw Schema Semantic Catalog Closure
No Legacy Gate Supersession
No RustPython Retirement
No Production Promotion
No Parent Manifest Rewrite
No Raw Observation Rewrite
No Destructive Existing-Batch Repair
```

## Mandatory gates

```text
PASS_07A_R3_PARENT_R2_OBSERVER_ADOPTION_VALID
PASS_07A_R3_PARENT_REQUEST_DIGEST_PRESERVED
PASS_07A_R3_PARENT_ROUTE_REGISTRY_DIGEST_PRESERVED
PASS_07A_R3_PARENT_ADOPTION_DIGEST_PRESERVED
PASS_07A_R3_DISCOVERED_OBSERVATION_COUNT_27
PASS_07A_R3_VALIDATED_OBSERVATION_COUNT_27
PASS_07A_R3_ZERO_MISSING_OBSERVATION
PASS_07A_R3_ZERO_DUPLICATE_OBSERVATION
PASS_07A_R3_ZERO_UNEXPECTED_OBSERVATION
PASS_07A_R3_ZERO_FOREIGN_OBSERVATION
PASS_07A_R3_ZERO_STALE_OBSERVATION
PASS_07A_R3_OBSERVATION_SELF_DIGEST_RECOMPUTED
PASS_07A_R3_OBSERVATION_ENVELOPE_DIGEST_RECOMPUTED
PASS_07A_R3_ZERO_OBSERVATION_DIGEST_MISMATCH
PASS_07A_R3_ZERO_ENVELOPE_DIGEST_MISMATCH
PASS_07A_R3_REQUEST_DIGEST_EXACT_BINDING
PASS_07A_R3_PLAN_DIGEST_EXACT_BINDING
PASS_07A_R3_PRODUCER_ROUTE_DIGEST_EXACT_BINDING
PASS_07A_R3_ROUTE_REGISTRY_DIGEST_EXACT_BINDING
PASS_07A_R3_OBSERVER_ADOPTION_DIGEST_EXACT_BINDING
PASS_07A_R3_OWNER_AUTHORITY_EXACT_BINDING
PASS_07A_R3_PRODUCER_ENDPOINT_EXACT_BINDING
PASS_07A_R3_OPERATION_SET_EXACT_EQUALITY
PASS_07A_R3_BATCH_ENTRY_COUNT_27
PASS_07A_R3_BATCH_ENTRY_CANONICAL_ORDER
PASS_07A_R3_BATCH_ENTRY_DIGEST_VALID
PASS_07A_R3_BATCH_ENTRY_SET_DIGEST_VALID
PASS_07A_R3_BATCH_MANIFEST_DIGEST_VALID
PASS_07A_R3_MANIFEST_WRITTEN_LAST
PASS_07A_R3_STAGING_NON_AUTHORITATIVE
PASS_07A_R3_CONTENT_ADDRESSED_FINAL_PATH
PASS_07A_R3_ATOMIC_PROMOTION
PASS_07A_R3_IDEMPOTENT_REPLAY
PASS_07A_R3_NO_DESTRUCTIVE_REPAIR
PASS_07A_R3_OBSERVATION_BATCH_PUBLISHED
PASS_07A_R3_OBSERVATION_BATCH_VALID
PASS_07A_R3_ZERO_SEMANTIC_VERDICT
PASS_07A_R3_ZERO_EXPECTED_VALUE_READ
PASS_07A_R3_ZERO_LEGACY_ORACLE_READ
PASS_07A_R3_ZERO_PYTHON_VALIDATOR_EXECUTION
PASS_07A_R3_CURRENT_SCHEDULED_EVIDENCE_NOT_YET_CLOSED
PASS_07A_R3_NO_PRODUCTION_AUTHORITY_CHANGE
```

## Completion truth

```text
R1 sealed where every scheduled observation must go.
R2 attached actual owner-local observers and emitted 27 physical raw envelopes.
R3 revalidates those envelopes without rewriting them, proves exact operation-set equality,
seals a canonical 27-entry manifest, writes the manifest last, and atomically promotes the
completed generation into a content-addressed immutable batch.

The evidence envelope is now sealed.
No semantic judgment has yet occurred.
Production authority remains false.
```

## Next natural revision

```text
ASH-CONTROL-RUNTIME-NATIVE-RAW-OBSERVATION-MANAGER-REDUCTION-07B
```
