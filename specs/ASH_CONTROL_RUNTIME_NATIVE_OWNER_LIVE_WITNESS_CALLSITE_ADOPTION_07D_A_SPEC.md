# ASH-CONTROL-RUNTIME-NATIVE-OWNER-LIVE-WITNESS-CALLSITE-ADOPTION-07D-A

## 1. Status

```text
Patch:
ASH-CONTROL-RUNTIME-NATIVE-OWNER-LIVE-WITNESS-CALLSITE-ADOPTION-07D-A

Parent:
ASH-CONTROL-RUNTIME-NATIVE-OWNER-RUNTIME-LIVE-WITNESS-EXPORT-07D

Authority:
Owner runtime = live mutable state SSOT
Core = raw-witness + semantic-contract SSOT
Owner projector = physical fact projection only
Probe = immutable snapshot consumer
R3 = physical batch integrity
Device = identity/digest verification only
Manager = sole semantic disposition authority

Production authority: false
Current scheduled evidence execution closure: false
```

## 2. Parent physical truth

07D preflight established an exact protocol/registry surface but no actual owner publications:

```text
rawWitnessSpecificationCount=27
ownerRuntimeWitnessExportBindingCount=27
ownerRuntimeWitnessExportDiscoveredCount=0
ownerRuntimeWitnessExportValidCount=0
ownerRuntimeWitnessExportMissingCount=27
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
liveWitnessExportClosed=false
productionAuthorityClaimed=false
```

Known parent identities:

```text
requestManifestDigest=
2f051108e43acb564304284c0d9f53dc47a9555766bb7a4eca214d1c5a6009f0

producerRouteRegistryDigest=
c8ab296f59f46f8114bac50b424c6d3960f6fc7299c9e3590d9035c60c5fa6c3
```

07D-A MUST preserve R1 request/route topology. The open condition is owner-side publication adoption.

## 3. Current physical topology

```text
Scheduled operations:       27
Owner authorities:          13
Owner/endpoint bindings:    20
Physical source surfaces:    8
```

Eight current surfaces:

```text
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs                 2
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs              13
crates/base_train/src/bp_delta_k_fusion_fission_planner.rs                                2
crates/base_train/src/bp_delta_k_control_data_plane_binding.rs                            3
crates/base_train/src/bp_delta_k_policy_r2_closure.rs                                     2
crates/base_train/src/checkpoint_reload_parity_step2_continuation.rs                      1
crates/base_train/src/bp_delta_k_fusion_policy_explicit_production_activation.rs          2
crates/base_train/src/bp_delta_k_fusion_policy_production_aware_recommendation_operator_review_adoption.rs 2
```

Shared typed state may feed multiple exact operation projectors. Operation identity MUST remain 27/27 exact.

## 4. Raw Witness Registry v2

07D-A advances the raw-witness contract from family-only shape to exact operation-specific measurement shape:

```text
registry schema:
ash.control_runtime.native_domain_raw_witness_registry.v2

observation type:
ash.native.domain-witness.v2
```

Current specification binds:

```text
operation_key
owner_authority_id
producer_endpoint_id
witness_family
required_fields
required_fields_when_available
operation_required_fields
witness_spec_digest
```

Three layers are distinct:

```text
common required fields     = protocol/provenance
family required fields     = family-level physical shape
operation required fields  = exact current invariant physical facts
```

No layer may contain semantic PASS/FAIL/HOLD values.

### 4.1 Physical fact law

Allowed:

```text
source_generation=41
candidate_generation=42
production_pointer_digest_before=<digest>
production_pointer_digest_after=<digest>
```

Forbidden:

```text
generation_contiguous=true
routing_disjoint=true
pointer_unchanged=true
parity_passed=true
```

## 5. Exact current operation witness additions

| # | Exact invariant suffix | Operation-specific physical fields |
|---|---|---|
| 1 | staging-generation-must-be-contiguous | source_generation, candidate_generation, staging_marker_state, staging_marker_digest |
| 2 | staging-source-and-candidate-slots-must-not-collide | source_slot_identity, candidate_slot_identity, source_generation, candidate_generation |
| 3 | optimizer-parameter-owner-must-be-disjoint | parameter_ids, parameter_owner_ids, route_ids |
| 4 | generation-filesystem-witness-must-match-training-and-optimizer-generation | training_generation, optimizer_generation, filesystem_witness_generation, filesystem_witness_digest |
| 5 | production-muon-state-cannot-split-authority | muon_state_component_ids, muon_state_owner_ids |
| 6 | planner-commit-and-abort-must-match-pending-generation | pending_generation, planner_terminal_action, planner_action_generation, planner_state_snapshot_digest |
| 7 | planner-state-sidecar-cannot-split-authority | planner_state_component_ids, planner_state_owner_ids, sidecar_state_component_ids, sidecar_state_owner_ids, planner_state_snapshot_digest |
| 8 | g2-canary-runtime-binding-cannot-be-production-active | runtime_binding_generation, runtime_binding_mode, runtime_binding_digest, production_active_pointer_generation, production_active_pointer_digest |
| 9 | startup-binding-policy-generation-and-digests-must-match-active-binding | startup_policy_generation, active_policy_generation, startup_policy_digest, active_policy_digest, startup_binding_digest, active_binding_digest |
| 10 | partial-control-data-binding-transport-is-illegal | required_binding_component_ids, observed_binding_component_ids, binding_generation, runtime_binding_digest |
| 11 | g2-canary-qualification-cannot-mutate-production-pointer | production_pointer_digest_before, production_pointer_digest_after, canary_generation, canary_receipt_digest |
| 12 | g2-production-activation-requires-qualified-generation-bound-intent | activation_intent_generation, target_generation, qualified_generation, activation_intent_digest, qualification_receipt_digest |
| 13 | production-muon-runtime-must-have-single-writer-authority | mutable_state_ids, writer_authority_ids |
| 14 | execution-observation-and-planning-authorities-cannot-collapse-into-one-implicit-owner | execution_authority_ids, observation_authority_ids, planning_authority_ids |
| 15 | optimizer-decomposition-requires-compile-and-behavior-parity-before-qualification | compile_receipt_digest, compile_result_code, behavior_receipt_digest, behavior_result_code, qualification_request_identity |
| 16 | load-resume-optimizer-state-must-match-continuous-execution-semantics | checkpoint_optimizer_state_digest, resumed_optimizer_state_digest, continuous_optimizer_state_digest, checkpoint_model_digest, resumed_model_digest, continuous_model_digest, continuation_step, qualification_artifact_digest |
| 17 | every-pending-commit-stage-must-bind-the-target-generation | transaction_target_generation, pending_stage_ids, pending_stage_generations |
| 18 | failed-generation-stage-cannot-publish-successful-transaction-receipt | failed_stage_ids, failed_stage_generations, transaction_receipt_state, transaction_receipt_generation, transaction_receipt_digest |
| 19 | filesystem-commit-witness-must-match-transaction-generation | transaction_generation, filesystem_witness_generation, filesystem_commit_witness_digest |
| 20 | active-recovery-fence-must-block-conflicting-generation-transaction | recovery_fence_present, recovery_fence_generation, candidate_transaction_generation, candidate_transaction_state |
| 21 | generation-abort-must-target-the-pending-failed-generation | pending_failed_generation, abort_target_generation, abort_marker_present, abort_receipt_digest |
| 22 | recovery-path-cannot-fabricate-unobserved-successful-commit | observed_successful_commit_generations, recovery_reported_commit_generation, recovery_receipt_digest |
| 23 | fault-injected-recovery-must-preserve-last-durable-generation-seal | fault_point_id, pre_fault_last_durable_generation, post_recovery_last_durable_generation, pre_fault_generation_seal_digest, post_recovery_generation_seal_digest, qualification_artifact_digest |
| 24 | production-activation-barrier-requires-quiescence-and-durable-checkpoint | observed_partial_count, observed_tmp_count, observed_staging_count, committed_transaction_residue_count, unresolved_pending_state_count, durable_checkpoint_present, durable_checkpoint_generation, durable_checkpoint_digest, activation_target_generation, activation_barrier_digest |
| 25 | production-policy-change-cannot-bypass-restart-bound-activation | startup_runtime_instance_id, current_runtime_instance_id, startup_policy_generation, requested_policy_generation, active_policy_generation, startup_policy_digest, requested_policy_digest, active_policy_digest |
| 26 | production-aware-review-must-carry-required-reason-and-policy-consistent-evidence-request | review_decision, review_reason_present, review_reason_digest, target_policy_digest, evidence_request_policy_digest, review_receipt_digest |
| 27 | production-aware-review-target-snapshot-must-have-valid-pointer-identity | review_target_policy_generation, review_target_policy_digest, active_pointer_policy_generation, active_pointer_policy_digest, review_target_snapshot_digest |

Types remain explicit through `NativeRawWitnessValueKind`; required physical facts may not be weakened to optional merely to pass a gate.

## 6. Callsite Registry

New owner-side registry:

```text
ash.basetrain.native_owner_witness_callsite_registry.v1
```

Each exact binding seals:

```text
operation_key
owner_authority_id
producer_endpoint_id
owner_source_relative_path
publication_boundary_id
projector_id
raw_witness_spec_digest
exporter_binding_digest
projector_program_digest
callsite_binding_digest
```

Registry invariants:

```text
binding_count=27
owner_authority_count=13
owner_endpoint_binding_count=20
physical_source_surface_count=8
```

`ownerCallsiteRegistryDigest` is the canonical lexical operation-key ordered registry digest.

Source line numbers are not identity material.

## 7. Owner-local hook adoption

Each of the eight physical source surfaces exposes one thin 07D-A owner-local publication hook.

Hook law:

```text
explicit NativeOwnerWitnessPublicationContext
exact operation allowlist for that source surface
actual raw field map supplied by owner code
foreign operation -> fail closed
publish through canonical 07D owner publisher
```

Operation distribution:

```text
training scheduler           2
local-muon                  13
fission planner              2
control data-plane           3
policy R2                    2
load/resume                  1
production activation        2
operator review              2
                           ---
total                       27
```

There is no giant semantic switch and no source-scanner fallback.

## 8. Code Adoption vs Physical Invocation

These gates are deliberately separate.

### 8.1 Code Adoption

Static code adoption proves:

```text
27 exact raw-witness specifications
27 exact callsite bindings
27 exact projector bindings
13 exact owner authorities
20 exact owner/endpoint bindings
8 exact source surfaces
27 source-hook operation literals verified
0 source-hook missing
```

The static receipt schema is:

```text
ash.basetrain.native_owner_witness_callsite_adoption.v1
```

Expected code-adoption truth:

```text
ASH_BASETRAIN_NATIVE_OWNER_WITNESS_CALLSITE_ADOPTION_VALID=true
scheduledOperationCount=27
ownerAuthorityCount=13
ownerEndpointBindingCount=20
physicalSourceSurfaceCount=8
callsiteBindingCount=27
callsiteUnboundCount=0
callsiteDuplicateOperationCount=0
projectorBindingCount=27
projectorUnboundCount=0
rawWitnessSpecificationCount=27
sourceHookVerifiedCount=27
sourceHookMissingCount=0
semanticVerdictCount=0
expectedValueReadCount=0
callsiteAdoptionClosed=true
productionAuthorityClaimed=false
```

`callsiteAdoptionClosed` here means code-level exact hook availability.

### 8.2 Physical Invocation

Physical closure requires the real runtime/qualification entrypoints to receive the explicit publication context and invoke those hooks with actual typed owner state.

If they have not done so, the 07D physical preflight may truthfully remain:

```text
valid=0
missing=27
liveWitnessExportClosed=false
```

No fixture, synthetic export, or probe-generated owner snapshot may be used to hide that state.

## 9. Explicit publication session

New session schema:

```text
ash.control_runtime.native_owner_witness_publication_session.v1
```

It binds:

```text
observation_session_id
request_manifest_digest
raw_witness_registry_digest
owner_exporter_registry_digest
owner_callsite_registry_digest
export_root
expected_operation_count=27
session_digest
```

New creator binary:

```text
ash_basetrain_native_owner_witness_session_create
```

Session discovery MUST be explicit. Forbidden:

```text
latest-session lookup
implicit current-directory scan
global mutable session singleton
```

## 10. Owner publisher identity revision

Snapshot schema advances to:

```text
ash.control_runtime.native_owner_witness_snapshot.v2
```

Export envelope schema advances to:

```text
ash.control_runtime.native_owner_witness_export.v2
```

New identity binds:

```text
owner_callsite_binding_digest
owner_callsite_registry_digest
owner_projector_program_digest
publication_boundary_id
```

The exporter registry receives a new digest because raw-witness specification digests changed.

Immutable publication remains create-new/content-stable:

```text
same session + operation + identical canonical bytes -> idempotent
same session + operation + different bytes           -> fail closed
```

No last-write-wins authority exists.

## 11. V6 Observation

Current observation schema advances to:

```text
ash.control_runtime.native_domain_probe_observation.v6
```

V6 binds V5 owner-snapshot identities plus:

```text
owner_callsite_binding_digest
owner_callsite_registry_digest
owner_projector_program_digest
publication_boundary_id
```

The probe consumes exact immutable owner exports. It may not reconstruct unavailable live state from source text or R2 provenance snapshots.

## 12. Preflight v2

07D-A extends physical preflight identity validation with distinct counters:

```text
ownerCallsiteRegistryMismatchCount
ownerCallsiteBindingMismatchCount
ownerProjectorProgramMismatchCount
publicationBoundaryMismatchCount
```

A physically complete current session requires:

```text
ownerRuntimeWitnessExportBindingCount=27
ownerRuntimeWitnessExportDiscoveredCount=27
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
ownerCallsiteRegistryMismatchCount=0
ownerCallsiteBindingMismatchCount=0
ownerProjectorProgramMismatchCount=0
publicationBoundaryMismatchCount=0
snapshotDigestMismatchCount=0
exportEnvelopeDigestMismatchCount=0
liveWitnessExportClosed=true
```

## 13. R3 / Device preservation

R3 retains its authority law:

```text
exact observation set
individual digest revalidation
canonical batch entries
manifest-last staging
atomic promotion
content-addressed immutable final directory
```

07D-A only admits V6 identity. Historical batches are not rewritten.

Device validates physical identity/digests only, including callsite and projector identities. Device semantic verdict count remains zero.

## 14. Manager boundary

Manager rematerializes raw-witness registry v2 and validates both family and operation-specific fields.

After physical owner invocation closes:

```text
heldInsufficientRawEvidenceCount=0
heldUnsupportedCapabilityCount=0
```

The current Core semantic catalog still lacks executable comparison/relation laws. Therefore 07D-A does not invent `Satisfied` or `Failed`; the next truthful Manager blocker remains:

```text
HeldSemanticRuleUnavailable
```

Expected downstream structural state after real 27/27 publication:

```text
managerReductionRequestedCount=27
managerReductionCompletedCount=27
managerReductionMissingCount=0
managerReductionDuplicateCount=0
reductionInputSchemaMismatchCount=0
reductionInputIncompleteCount=0
reductionInputTypeMismatchCount=0
heldInsufficientRawEvidenceCount=0
heldUnsupportedCapabilityCount=0
heldSemanticRuleUnavailableCount=27
managerReductionClosed=true
allCurrentInvariantsSatisfied=false
currentScheduledEvidenceExecutionClosed=false
productionAuthorityClaimed=false
```

The value `27` is the current expected quarantine state, not a forced final semantic outcome.

## 15. Semantic authority isolation

Throughout 07D-A:

```text
ownerRuntimeSemanticVerdictCount=0
producerSemanticVerdictCount=0
observerSemanticVerdictCount=0
deviceSemanticVerdictCount=0

ownerRuntimeExpectedValueReadCount=0
producerExpectedValueReadCount=0
observerExpectedValueReadCount=0
deviceExpectedValueReadCount=0
```

Manager remains the sole semantic disposition owner.

Legacy isolation remains:

```text
legacyOracleReadCount=0
legacyVerdictImportCount=0
pythonValidatorExecutionCount=0
fixtureObservationCount=0
syntheticObservationCount=0
fixtureVerdictCount=0
syntheticVerdictCount=0
```

## 16. Dependency law

Must remain true:

```text
ash_core !-> ash_control_runtime
ash_control_runtime !-> base_train
```

Owner-side implementation may depend on Core protocol types. Control runtime must not reverse-import owner implementation to obtain live state.

## 17. Mandatory gates

```text
PASS_07DA_PARENT_07D_EXACT_MISSING_27
PASS_07DA_R1_REQUEST_SSOT_PRESERVED
PASS_07DA_R1_ROUTE_SSOT_PRESERVED
PASS_07DA_RAW_WITNESS_REGISTRY_V2
PASS_07DA_27_OPERATION_SPECIFIC_RAW_WITNESS_CONTRACTS
PASS_07DA_13_OWNER_AUTHORITIES
PASS_07DA_20_OWNER_ENDPOINT_BINDINGS
PASS_07DA_8_PHYSICAL_SOURCE_SURFACES
PASS_07DA_27_EXACT_CALLSITE_BINDINGS
PASS_07DA_ZERO_CALLSITE_UNBOUND
PASS_07DA_ZERO_CALLSITE_DUPLICATE
PASS_07DA_27_PROJECTOR_BINDINGS
PASS_07DA_ZERO_PROJECTOR_UNBOUND
PASS_07DA_27_SOURCE_HOOKS_VERIFIED
PASS_07DA_ZERO_SOURCE_HOOK_MISSING
PASS_07DA_OWNER_CALLSITE_REGISTRY_DIGEST
PASS_07DA_PROJECTOR_PROGRAM_DIGESTS
PASS_07DA_EXPLICIT_SESSION_DESCRIPTOR
PASS_07DA_NO_LATEST_SESSION_DISCOVERY
PASS_07DA_NO_GLOBAL_MUTABLE_SESSION
PASS_07DA_TYPED_OWNER_STATE_FIRST
PASS_07DA_ZERO_PROBE_SHADOW_STATE
PASS_07DA_ZERO_SOURCE_SCANNER_FALLBACK
PASS_07DA_ZERO_PROVENANCE_ONLY_FALLBACK
PASS_07DA_OWNER_EXPORT_ENVELOPE_V2
PASS_07DA_OBSERVATION_V6
PASS_07DA_CALLSITE_IDENTITY_BOUND_END_TO_END
PASS_07DA_ZERO_OWNER_EXPECTATION_READ
PASS_07DA_ZERO_OWNER_SEMANTIC_VERDICT
PASS_07DA_ZERO_PRODUCER_SEMANTIC_VERDICT
PASS_07DA_ZERO_OBSERVER_SEMANTIC_VERDICT
PASS_07DA_ZERO_DEVICE_SEMANTIC_VERDICT
PASS_07DA_R3_ATOMIC_BATCH_LAW_PRESERVED
PASS_07DA_MANAGER_ONLY_SEMANTIC_DISPOSITION
PASS_07DA_NO_FORCED_SATISFIED
PASS_07DA_NO_FORCED_FAILED
PASS_07DA_ZERO_LEGACY_ORACLE
PASS_07DA_ZERO_PYTHON_VALIDATOR
PASS_07DA_ZERO_FIXTURE_OBSERVATION
PASS_07DA_ZERO_SYNTHETIC_OBSERVATION
PASS_07DA_CODE_ADOPTION_CLOSED
PASS_07DA_PHYSICAL_INVOCATION_REMAINS_EXPLICIT
PASS_07DA_CURRENT_SCHEDULED_EXECUTION_NOT_YET_CLOSED
PASS_07DA_NO_PRODUCTION_AUTHORITY_CHANGE
```

## 18. Explicit non-goals

```text
No probe-generated owner snapshot
No witness daemon as new mutable SSOT
No duplicate mutable owner state
No global stop-the-world snapshot
No hidden session discovery
No source-code semantic inference
No family-field string stuffing
No semantic verdict inside owner projector
No expected-value read inside owner projector
No last-write-wins witness file
No synthetic 27-export qualification
No executable semantic-rule invention
No forced Satisfied count
No legacy oracle
No Python validator
No production promotion
No NATIVE-08 closure
```

## 19. Completion truth

```text
Before 07D-A:

07D has a valid 27-entry exporter registry and exact-set preflight.
The physical result is valid=0 / missing=27 with zero protocol, identity, registry, or digest mismatch.

After 07D-A code adoption:

The 27 current operations map exactly to 13 owner authorities, 20 owner/endpoint bindings,
and 8 real source surfaces.

Raw witness contracts become operation-specific rather than family-only.

Every operation has exact callsite and projector identities.

Every physical source surface exposes a read-only owner-local publication hook with an exact
operation allowlist.

An explicit session descriptor binds the request, raw-witness, exporter, and callsite registries.

Owner snapshot/export v2 and observation v6 bind callsite/projector identity end-to-end.

No semantic authority moves into owner code, producer, observer, or Device.

Code-level adoption and physical runtime invocation are intentionally separate gates.

Until real entrypoints invoke the hooks with actual typed owner state, physical preflight may
truthfully remain missing=27. Synthetic repair is forbidden.

Once real 27/27 publications exist, raw-insufficiency and unsupported-capability HOLDs can close.
The next explicit blocker is the missing Core executable semantic-rule contract.

Current scheduled native execution remains open.
Production authority remains false.
```

## 20. Next revision

After physical owner invocation reaches `valid=27 / missing=0`, the natural next revision is:

```text
ASH-CONTROL-RUNTIME-NATIVE-EXECUTABLE-SEMANTIC-RULE-CONTRACT-07E
```

07E must add Core-owned executable semantic relations. It must not teach owner projectors to judge their own facts.
