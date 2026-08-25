# ASH-CONTROL-RUNTIME-NATIVE-OWNER-RUNTIME-LIVE-WITNESS-EXPORT-07D

## Status

```text
Patch ID:
ASH-CONTROL-RUNTIME-NATIVE-OWNER-RUNTIME-LIVE-WITNESS-EXPORT-07D

Parent:
ASH-CONTROL-RUNTIME-NATIVE-DOMAIN-SEMANTIC-RAW-WITNESS-CLOSURE-07C

Role:
Core Raw-Witness Contract
-> Owner-Owned Immutable Live Snapshot
-> Read-Only Native Export ABI
-> Exact Session-Bound Probe Import
-> V5 Observation Envelope
-> R3 Immutable Batch
-> Manager-Only Reduction

Production authority: false
Current scheduled evidence execution closure: false
```

## Parent physical truth

07C physically closed the distinction between missing witness semantics and missing live witness capability.

Observed parent state:

```text
requestManifestDigest=
2f051108e43acb564304284c0d9f53dc47a9555766bb7a4eca214d1c5a6009f0

producerRouteRegistryDigest=
c8ab296f59f46f8114bac50b424c6d3960f6fc7299c9e3590d9035c60c5fa6c3

rawWitnessRegistryDigest=
8e147ec77a6a3c5115a32a2c21eac41b23fe0476e15510cace97ac50f61202ab

semanticContractRegistryDigest=
7e1b340005f264603269eba054663adb5b9c196b52617a016dc471c7801badd7

managerReductionRequestedCount=27
managerReductionCompletedCount=27
heldUnsupportedCapabilityCount=27
heldInsufficientRawEvidenceCount=0
managerReductionClosed=true
currentScheduledEvidenceExecutionClosed=false
productionAuthorityClaimed=false
```

The parent blocker is explicit:

```text
OWNER_LIVE_STATE_NOT_EXPORTED_TO_NATIVE_PROBE_PROCESS
```

## 07D scope correction

The current scheduled authorities are not all independent long-lived daemon processes. Many current authorities are typed runtime / receipt / artifact / file-backed authorities executed inside the existing native base-train process topology.

07D MUST NOT invent a new witness daemon or probe-owned shadow state merely to create an IPC surface.

Canonical law:

```text
Existing owner state remains SSOT.
Owner projects one immutable observation snapshot.
Probe consumes only that snapshot.
No duplicate mutable witness state exists.
```

The current transport admitted by this revision is an owner-generated immutable local export file. The transport is physical only and carries no semantic verdict authority.

## Semantic-rule SSOT correction

07D also records an important boundary discovered while binding live witness data.

The current Core `NativeEvidenceExpectation` variants identify semantic families and an `illegal_state` label, for example:

```text
StateLegal { illegal_state }
TransitionLegal { illegal_state }
CommitConsistent { illegal_state }
RecoverySafe { illegal_state }
```

The current Core catalog does not yet carry the executable relation / threshold / allowed-transition / equality law required to reduce arbitrary live raw fields into truthful `Satisfied` or `Failed` results.

Therefore 07D MUST NOT translate a valid live snapshot directly into PASS/FAIL by guessing field meaning.

07D adds the Manager-owned disposition:

```text
HeldSemanticRuleUnavailable
```

Meaning:

```text
physical live witness exists,
raw witness schema is complete,
Core semantic family binding exists,
but the executable Core semantic comparison law is not yet admitted.
```

This is distinct from:

```text
HeldInsufficientRawEvidence
HeldUnsupportedCapability
FailedInfrastructure
Failed
Satisfied
```

Expected authority progression is therefore:

```text
07B:
HeldInsufficientRawEvidence = 27

07C:
HeldInsufficientRawEvidence = 0
HeldUnsupportedCapability   = 27

07D, after all real owner exports are present:
HeldInsufficientRawEvidence   = 0
HeldUnsupportedCapability     = 0
HeldSemanticRuleUnavailable   = 27
```

No count is forced to `Satisfied` in 07D.

## Authority law

```text
Owner runtime / typed owner surface:
live-state SSOT

Core raw-witness registry:
what physical facts must be exported

Core semantic contract catalog:
semantic family identity

Owner exporter:
read-only projection of actual owner state

Probe:
exact immutable snapshot consumer

R3:
physical identity / batch integrity

Device:
physical verification only

Manager:
sole semantic disposition authority
```

## Dependency law

```text
ash_core
must not depend on
ash_control_runtime

ash_control_runtime
must not depend on
base_train

owner/base_train surfaces
may depend on
ash_core protocol types
```

07D may not introduce a reverse dependency to gain access to owner state.

## Core owner-export protocol

New Core module:

```text
crates/ash_core/src/native_owner_witness_export.rs
```

Canonical types:

```text
NativeOwnerWitnessExportRequest
NativeOwnerWitnessSnapshot
NativeOwnerWitnessExportEnvelope
NativeOwnerWitnessExporterBinding
NativeOwnerWitnessExporterRegistry
NativeOwnerWitnessExportStatus
```

Schemas:

```text
ash.control_runtime.native_owner_witness_export_request.v1
ash.control_runtime.native_owner_witness_snapshot.v1
ash.control_runtime.native_owner_witness_export.v1
ash.control_runtime.native_owner_witness_exporter_registry.v1
```

Current transport identity:

```text
owner-immutable-file-v1
```

## Exact exporter registry

The exporter registry is materialized from the exact 27-entry Core raw-witness registry.

Each binding contains:

```text
operation_key
owner_authority_id
producer_endpoint_id
raw_witness_spec_digest
exporter_id
transport_kind
exporter_program_digest
binding_digest
```

Current cardinality:

```text
ownerRuntimeWitnessExportBindingCount=27
```

Wildcard / prefix / EvidenceKind routing is forbidden.

## Exporter program identity

`exporter_program_digest` binds:

```text
07D patch identity
exporter revision
operation key
owner authority
producer endpoint
raw witness specification digest
```

The registry itself is canonically sealed as:

```text
ownerExporterRegistryDigest
```

## Owner snapshot law

`NativeOwnerWitnessSnapshot` is an immutable observation transaction, not a second state store.

It binds:

```text
operation key
owner authority
producer endpoint
raw witness spec digest
raw witness registry digest
owner runtime instance identity
owner runtime generation
snapshot epoch
raw domain fields
snapshot digest
```

The owner must project values from the actual state authority. It may not synthesize expected values or semantic PASS/FAIL fields.

## Snapshot consistency

All fields in one snapshot must belong to one owner observation boundary.

Preferred implementation order:

```text
existing immutable state view
existing generation-pinned receipt
existing epoch snapshot
short read lock
```

A long global runtime lock or stop-the-world barrier is not admitted as the default repair.

An unstable/torn snapshot fails closed. Retry must be bounded.

## No owner-side semantics

Owner export MUST NOT include or compute:

```text
is_legal
is_valid
is_safe
is_fresh
is_single_owner
is_exclusive
expected_match
qualification_passed
Satisfied
Failed
Held
```

Actual physical booleans remain legal when they are facts rather than verdicts.

## Immutable local export publication

Base-train exposes the reusable owner-side publication API:

```text
publish_native_owner_live_witness_snapshot(...)
```

The API:

```text
accepts exact exporter binding
accepts exact raw-witness registry identity
accepts exact observation session identity
accepts owner runtime identity / generation / epoch
accepts actual raw field map
seals snapshot digest
seals export envelope digest
publishes with create-new immutable semantics
```

It does NOT derive domain values itself.

Real owner callsites must invoke this API at their actual state authority boundary.

## No fabricated owner adoption

07D does not fabricate 27 snapshot files from the probe process.

If real owner callsites have not produced the export files, preflight MUST report them missing and terminate non-zero.

This is an intentional fail-closed gate, not a fallback path.

## Observation session identity

Every qualification run uses an explicit:

```text
observation_session_id
```

The same exact session identity must be present in all imported owner export envelopes.

The export root supplied to owner runtimes and the probe SHOULD be session-specific so a new runtime snapshot never overwrites an older immutable session.

Stale or mixed-session responses fail closed.

## Owner export preflight

New binary:

```text
ash_basetrain_native_owner_live_witness_export_preflight
```

The preflight rematerializes:

```text
27 exact raw-witness specifications
27 exact exporter bindings
```

and verifies the exact session export set.

It reports:

```text
ownerRuntimeWitnessExportBindingCount
ownerRuntimeWitnessExportDiscoveredCount
ownerRuntimeWitnessExportValidCount
ownerRuntimeWitnessExportMissingCount
ownerRuntimeWitnessExportInvalidCount
ownerRuntimeWitnessExportUnexpectedCount
ownerRuntimeUnavailableCount
ownerRuntimeWitnessCapabilityUnavailableCount
ownerRuntimeSnapshotBusyCount
ownerRuntimeProtocolMismatchCount
ownerRuntimeIdentityMismatchCount
ownerExporterRegistryMismatchCount
snapshotDigestMismatchCount
exportEnvelopeDigestMismatchCount
```

Closure requires all 27 real `SnapshotAvailable` exports and zero mismatch/missing/unavailable counts.

## Preflight is diagnostic authority, not a snapshot producer

Preflight never writes fake owner snapshots.

It may materialize the deterministic exporter registry and receipt, but current owner state may only enter through the owner-side publication ABI.

## V5 observation envelope

07D advances the current observation envelope to:

```text
ash.control_runtime.native_domain_probe_observation.v5
```

V5 preserves all V4 identity and adds:

```text
owner_runtime_instance_id
owner_runtime_generation
owner_snapshot_epoch
owner_snapshot_digest
owner_export_envelope_digest
owner_exporter_program_digest
owner_exporter_registry_digest
```

A live snapshot is therefore transitively bound through the R3 batch and Manager reduction receipts.

## Probe import law

The probe consumes an owner export only when all exact identities match:

```text
operation key
owner authority
producer endpoint
raw witness spec digest
raw witness registry digest
owner exporter program digest
owner exporter registry digest
observation session id
snapshot digest
export envelope digest
```

The probe does not scan owner process memory or reinterpret source code to fill missing live fields.

## V5 raw observation

After a valid owner export is imported, the probe builds the existing domain-witness raw observation with:

```text
witness_capability_available=true
witness_capability_reason=OWNER_LIVE_STATE_EXPORTED_BY_OWNER_RUNTIME
witness_source_kind=owner-live-immutable-export
witness_source_identity=<owner runtime instance id>
witness_source_digest=<owner snapshot digest>
witness_observation_epoch=<owner snapshot epoch>
```

plus the exact owner-exported family-specific fields.

Reserved common fields cannot be overwritten by the owner field map.

## R3 preservation

R3 transaction law remains unchanged:

```text
exact observation set
individual digest revalidation
canonical batch entries
manifest-last staging
atomic promotion
content-addressed immutable final directory
```

R3 is revised only to admit and verify the exact V5 envelope schema and digest chain.

Historical V4 batches are not rewritten.

## Device boundary

Device verifies V5 identity, including:

```text
owner snapshot digest
owner export envelope digest
owner exporter program digest
owner exporter registry digest
owner runtime instance identity
```

Device still has zero semantic verdict authority.

## Manager reduction after live export

When `witness_capability_available=true`, Manager first validates all family-specific raw fields required by the exact Core raw-witness specification.

If those fields are complete, raw evidence is no longer insufficient.

However 07D does not invent the missing executable semantic relation. It returns:

```text
semantic_input_sufficient=true
semantic_input_reason=CORE_EXECUTABLE_SEMANTIC_RULE_NOT_YET_ADMITTED
disposition=HeldSemanticRuleUnavailable
```

Only Manager emits this HOLD.

## Reducer program identity revision

Because Manager behavior for live witnesses changes, the reducer program revision is advanced.

The `semanticReducerRegistryDigest` must therefore change from the 07C value when 07D is active.

The Core semantic contract registry need not change merely because physical live witness transport was added.

## Manager receipt revision

Manager reduction manifest / receipt advance to v3 and add:

```text
heldSemanticRuleUnavailableCount
```

The existing counters remain distinct:

```text
heldUnsupportedCapabilityCount
heldInsufficientRawEvidenceCount
heldSemanticRuleUnavailableCount
```

## Structural success after real owner adoption

A fully physically adopted 07D session targets:

```text
ownerRuntimeWitnessExportBindingCount=27
ownerRuntimeWitnessExportValidCount=27
ownerRuntimeWitnessExportMissingCount=0
ownerRuntimeWitnessExportInvalidCount=0
ownerRuntimeWitnessExportUnexpectedCount=0
ownerRuntimeUnavailableCount=0
ownerRuntimeWitnessCapabilityUnavailableCount=0
ownerRuntimeSnapshotBusyCount=0
ownerRuntimeProtocolMismatchCount=0
ownerRuntimeIdentityMismatchCount=0
ownerExporterRegistryMismatchCount=0
snapshotDigestMismatchCount=0
exportEnvelopeDigestMismatchCount=0
liveWitnessExportClosed=true
```

Downstream:

```text
managerReductionRequestedCount=27
managerReductionCompletedCount=27
heldUnsupportedCapabilityCount=0
heldInsufficientRawEvidenceCount=0
heldSemanticRuleUnavailableCount=27
managerReductionClosed=true
allCurrentInvariantsSatisfied=false
currentScheduledEvidenceExecutionClosed=false
productionAuthorityClaimed=false
```

The final `27` is not a forced semantic outcome. It reflects the currently missing executable Core semantic rule authority.

## Current pre-adoption expected first run

If the canonical 07D code is applied before real owner callsites publish snapshots, the expected preflight is intentionally non-closed, for example:

```text
ASH_BASETRAIN_NATIVE_OWNER_LIVE_WITNESS_EXPORT_VALID=false
ownerRuntimeWitnessExportBindingCount=27
ownerRuntimeWitnessExportValidCount=0
ownerRuntimeWitnessExportMissingCount=27
liveWitnessExportClosed=false
```

The command exits non-zero.

Do not bypass this by generating probe-side fixture exports.

## Legacy isolation

Throughout 07D:

```text
ownerRuntimeSemanticVerdictCount=0
ownerRuntimeExpectedValueReadCount=0
producerSemanticVerdictCount=0
observerSemanticVerdictCount=0
deviceSemanticVerdictCount=0
legacyOracleReadCount=0
legacyVerdictImportCount=0
pythonValidatorExecutionCount=0
fixtureObservationCount=0
syntheticObservationCount=0
```

## Mandatory gates

```text
PASS_07D_PARENT_07C_IDENTITY
PASS_07D_R1_ROUTE_SSOT_PRESERVED
PASS_07D_CORE_RAW_WITNESS_SSOT_PRESERVED
PASS_07D_NO_CONTROL_RUNTIME_TO_BASE_TRAIN_DEPENDENCY

PASS_07D_OWNER_EXPORT_PROTOCOL_TYPES
PASS_07D_OWNER_EXPORTER_REGISTRY_27
PASS_07D_OWNER_EXPORTER_REGISTRY_DIGEST
PASS_07D_EXACT_OPERATION_OWNER_ENDPOINT_BINDING
PASS_07D_NO_WILDCARD_EXPORTER_BINDING

PASS_07D_OWNER_STATE_REMAINS_SSOT
PASS_07D_NO_PROBE_SHADOW_STATE
PASS_07D_READ_ONLY_OWNER_SNAPSHOT
PASS_07D_IMMUTABLE_EXPORT_PUBLICATION
PASS_07D_SESSION_BOUND_EXPORT
PASS_07D_ZERO_TORN_SNAPSHOT
PASS_07D_BOUNDED_SNAPSHOT_RETRY
PASS_07D_ZERO_EXPORT_SIDE_EFFECT

PASS_07D_ZERO_OWNER_EXPECTATION_READ
PASS_07D_ZERO_OWNER_SEMANTIC_VERDICT
PASS_07D_NO_PROBE_SIDE_LIVE_STATE_FABRICATION

PASS_07D_EXACT_27_SNAPSHOT_AVAILABLE_EXPORTS
PASS_07D_ZERO_EXPORT_MISSING
PASS_07D_ZERO_EXPORT_INVALID
PASS_07D_ZERO_EXPORT_UNEXPECTED
PASS_07D_ZERO_OWNER_RUNTIME_UNAVAILABLE
PASS_07D_ZERO_OWNER_CAPABILITY_UNAVAILABLE
PASS_07D_ZERO_SNAPSHOT_BUSY
PASS_07D_ZERO_PROTOCOL_MISMATCH
PASS_07D_ZERO_OWNER_IDENTITY_MISMATCH
PASS_07D_ZERO_EXPORTER_REGISTRY_MISMATCH
PASS_07D_ZERO_SNAPSHOT_DIGEST_MISMATCH
PASS_07D_ZERO_EXPORT_ENVELOPE_DIGEST_MISMATCH

PASS_07D_OBSERVATION_V5
PASS_07D_OWNER_SNAPSHOT_IDENTITY_BOUND
PASS_07D_R3_V5_BATCH_VALID
PASS_07D_DEVICE_V5_IDENTITY_VERIFICATION
PASS_07D_ZERO_DEVICE_SEMANTIC_VERDICT

PASS_07D_MANAGER_REDUCTION_27_OF_27
PASS_07D_ZERO_HELD_INSUFFICIENT_RAW_EVIDENCE
PASS_07D_ZERO_HELD_UNSUPPORTED_CAPABILITY
PASS_07D_SEMANTIC_RULE_UNAVAILABLE_EXPLICIT
PASS_07D_NO_FORCED_SATISFIED_OR_FAILED

PASS_07D_ZERO_LEGACY_ORACLE
PASS_07D_ZERO_PYTHON_VALIDATOR
PASS_07D_ZERO_FIXTURE_OBSERVATION
PASS_07D_ZERO_SYNTHETIC_OBSERVATION
PASS_07D_CURRENT_SCHEDULED_EXECUTION_NOT_YET_CLOSED
PASS_07D_NO_PRODUCTION_AUTHORITY_CHANGE
```

## Explicit non-goals

```text
No new witness daemon SSOT
No duplicate mutable owner state
No arbitrary memory scanning
No probe-side fake snapshot generation
No owner PASS/FAIL/HOLD
No Device PASS/FAIL/HOLD
No executable semantic-rule invention
No forced Satisfied count
No R1 route rewrite
No historical batch rewrite
No legacy oracle
No Python validator
No production promotion
No NATIVE-08 closure
```

## Completion truth

```text
Before 07D:
The system knows exactly what raw domain witness every current operation requires,
but the probe can only prove that live owner state export is unavailable.

After 07D protocol adoption:
Core owns one deterministic 27-entry owner exporter registry.
Real owner state is projected through a read-only immutable snapshot ABI.
The probe cannot fabricate those snapshots.
Every imported snapshot is bound to an explicit observation session and exact
operation / owner / endpoint / witness / exporter identities.
V5 observations bind the owner snapshot and export-envelope digests.
R3 seals those observations without changing its atomic authority law.
Device verifies physical identity only.
Manager remains the only semantic disposition owner.

When all real owner callsites have published the 27 exact snapshots,
HeldUnsupportedCapability and HeldInsufficientRawEvidence both fall to zero.

The next truthful blocker is then explicit:
HeldSemanticRuleUnavailable.

That blocker must be closed by a later Core executable-semantic-rule revision,
not by teaching owner exporters to judge themselves.

Current scheduled evidence execution remains open.
Production authority remains false.
```

## Next revision

Natural next revision after physical 07D owner-export adoption:

```text
ASH-CONTROL-RUNTIME-NATIVE-EXECUTABLE-SEMANTIC-RULE-CONTRACT-07E
```

07E should add Core-owned executable comparison/relation contracts for the fourteen expectation families and let the already-established Manager reducer consume them.
