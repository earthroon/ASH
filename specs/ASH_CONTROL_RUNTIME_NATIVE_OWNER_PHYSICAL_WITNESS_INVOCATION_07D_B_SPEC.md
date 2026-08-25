# ASH-CONTROL-RUNTIME-NATIVE-OWNER-PHYSICAL-WITNESS-INVOCATION-07D-B

## 1. Parent

`ASH-CONTROL-RUNTIME-NATIVE-OWNER-LIVE-WITNESS-CALLSITE-ADOPTION-07D-A`

07D-A physically established the current request/raw/exporter/callsite registries and session contract, while the observed owner export set remained `valid=0 / missing=27` with every mismatch counter zero.

Preserved parent identities:

```text
requestManifestDigest=2f051108e43acb564304284c0d9f53dc47a9555766bb7a4eca214d1c5a6009f0
rawWitnessRegistryDigest=acd1b15d85cba85f74a725d47b02a94ef12d7f69dfab4fcd7f4abd2ae25f1df5
ownerExporterRegistryDigest=9865b161ca9a720244a6796ab53d71ac64315d3c64c68906797a81f6f00b02af
ownerCallsiteRegistryDigest=1b72518cec48e7eca6deff6cf5feedbd6cc660da984204c5a889d48fb43c641b
```

07D-B does not revise these registries or observation schemas.

## 2. Purpose

07D-B introduces a physical invocation authority boundary above the existing 07D-A publisher.

```text
Actual Owner Typed State
  -> Existing 07D-A Owner-Local Hook
  -> 07D-B Physical Invocation Wrapper
  -> Existing Immutable Owner Export
  -> Immutable Invocation Entry
  -> Exact 27-Operation Invocation Receipt
```

The wrapper does not create owner state, raw facts, expected values, or semantic dispositions. It records an invocation only after the canonical 07D-A publisher has successfully emitted an owner-generated immutable export.

## 3. No schema churn

07D-B preserves:

```text
ash.control_runtime.native_domain_raw_witness_registry.v2
ash.control_runtime.native_owner_witness_snapshot.v2
ash.control_runtime.native_owner_witness_export.v2
ash.control_runtime.native_domain_probe_observation.v6
ash.basetrain.native_owner_witness_callsite_registry.v1
ash.control_runtime.native_owner_witness_publication_session.v1
```

New schemas are invocation bookkeeping only:

```text
ash.basetrain.native_owner_physical_witness_invocation.v1
ash.basetrain.native_owner_physical_witness_invocation_receipt.v1
```

## 4. Physical invocation entry

Each successful real hook invocation seals:

```text
operation_key
owner_authority_id
producer_endpoint_id
observation_session_id
callsite_binding_digest
projector_program_digest
publication_boundary_id
owner_runtime_instance_id
owner_runtime_generation
owner_snapshot_digest
owner_export_envelope_digest
invocation_status
invocation_digest
```

Allowed status in the current implementation:

```text
Published
```

A physical invocation entry can only be created after `publish_native_owner_callsite_witness(...)` returns a valid immutable export envelope.

## 5. Immutable invocation identity

Invocation entries live under the exact session export root:

```text
<session export root>/_physical_invocations/<sanitized exact operation key>.json
```

Same operation/session with byte-identical entry is idempotent. Same operation/session with different bytes is an invocation collision and fails closed.

There is no last-write-wins behavior.

## 6. Eight owner-local surfaces

The existing eight 07D-A hooks are advanced to route through the 07D-B physical wrapper:

```text
production_multistep_loop_accumulation8_scheduler.rs                               2
tensorcube_local_muon_production_callsite_adoption.rs                            13
bp_delta_k_fusion_fission_planner.rs                                              2
bp_delta_k_control_data_plane_binding.rs                                          3
bp_delta_k_policy_r2_closure.rs                                                   2
checkpoint_reload_parity_step2_continuation.rs                                    1
bp_delta_k_fusion_policy_explicit_production_activation.rs                        2
bp_delta_k_fusion_policy_production_aware_recommendation_operator_review_adoption.rs 2
```

Total current operation cardinality remains 27.

The 07D-B wrapper does not replace these owner-local allowlists. It sits below them, so a foreign operation still fails at the exact owner surface before publication.

## 7. Invocation receipt

New binary:

```text
ash_basetrain_native_owner_physical_witness_invocation
```

Inputs:

```text
--repo-root <repo>
--request-manifest <native_probe_request.json>
--session-descriptor <native_owner_witness_session.json>
```

The binary rematerializes the current raw/exporter/callsite registries, validates them against the explicit immutable session descriptor, reads only 07D-B invocation entries, and emits:

```text
artifacts/control_runtime/native_owner_physical_witness_invocation_receipt.json
```

Expected physical closure:

```text
ASH_BASETRAIN_NATIVE_OWNER_PHYSICAL_WITNESS_INVOCATION_VALID=true
scheduledOperationCount=27
ownerAuthorityCount=13
ownerEndpointBindingCount=20
physicalSourceSurfaceCount=8
physicalInvocationRequestedCount=27
physicalInvocationCompletedCount=27
physicalInvocationMissingCount=0
physicalInvocationDuplicateCount=0
ownerSemanticVerdictCount=0
ownerExpectedValueReadCount=0
physicalWitnessInvocationClosed=true
productionAuthorityClaimed=false
```

If fewer than 27 real owner hook invocations have occurred, the binary fails closed and reports the exact completed/missing counts.

## 8. Explicit session law

07D-B does not discover sessions through current-directory scans, latest-session lookup, mutable globals, or process-wide singleton state.

The same 07D-A explicit session descriptor remains the authority. A caller must already possess a validated `NativeOwnerWitnessPublicationContext` derived from that descriptor.

## 9. Semantic isolation

07D-B is physical invocation bookkeeping only.

```text
ownerSemanticVerdictCount=0
ownerExpectedValueReadCount=0
```

Forbidden in the invocation layer:

```text
is_valid
is_legal
is_safe
parity_passed
matches_expected
satisfied
failed
```

Manager remains the only semantic disposition owner.

## 10. Physical closure law

The critical equation is:

```text
physicalInvocationCompletedCount
=
ownerRuntimeWitnessExportDiscoveredCount
=
ownerRuntimeWitnessExportValidCount
=
27
```

and:

```text
physicalInvocationMissingCount=0
ownerRuntimeWitnessExportMissingCount=0
ownerRuntimeWitnessExportInvalidCount=0
ownerRuntimeWitnessExportUnexpectedCount=0
all identity/digest mismatch counters=0
```

07D-B does not claim closure merely because eight hook functions exist. Closure requires those hooks to have been invoked by the actual owner execution paths under the explicit session.

## 11. Current implementation boundary

The 07D-B baked code installs the invocation wrapper, immutable invocation entries, exact-set receipt, and routes all eight 07D-A owner-local hooks through that wrapper.

It deliberately does not synthesize the 27 owner states and does not fabricate an all-operations harness. Therefore a session with no actual owner hook execution truthfully remains:

```text
physicalInvocationCompletedCount=0
physicalInvocationMissingCount=27
```

Actual owner entrypoint/session propagation remains a physical execution requirement, not something the receipt generator is allowed to fake.

## 12. Mandatory gates

```text
PASS_07DB_PARENT_07DA_IDENTITIES_PRESERVED
PASS_07DB_NO_RAW_WITNESS_SCHEMA_REVISION
PASS_07DB_NO_EXPORT_SCHEMA_REVISION
PASS_07DB_NO_OBSERVATION_SCHEMA_REVISION
PASS_07DB_8_OWNER_LOCAL_SURFACES_ROUTE_THROUGH_PHYSICAL_WRAPPER
PASS_07DB_IMMUTABLE_INVOCATION_ENTRY
PASS_07DB_INVOCATION_DIGEST
PASS_07DB_EXACT_SESSION_BOUND_INVOCATION_ROOT
PASS_07DB_ZERO_LAST_WRITE_WINS
PASS_07DB_27_EXACT_INVOCATION_RECEIPT_TARGET
PASS_07DB_ZERO_OWNER_SEMANTIC_VERDICT
PASS_07DB_ZERO_OWNER_EXPECTED_VALUE_READ
PASS_07DB_ZERO_SYNTHETIC_OWNER_STATE
PASS_07DB_ZERO_FIXTURE_EXPORT
PASS_07DB_ZERO_PROBE_GENERATED_OWNER_STATE
PASS_07DB_FAIL_CLOSED_WHEN_COMPLETED_LT_27
PASS_07DB_PRODUCTION_AUTHORITY_FALSE
```

Physical-current-session closure gates remain runtime-evidence gates:

```text
PASS_07DB_27_ACTUAL_OWNER_HOOK_INVOCATIONS
PASS_07DB_PHYSICAL_INVOCATION_COMPLETED_27
PASS_07DB_PHYSICAL_INVOCATION_MISSING_0
PASS_07DB_OWNER_EXPORT_VALID_27
PASS_07DB_OWNER_EXPORT_MISSING_0
PASS_07DB_LIVE_WITNESS_EXPORT_CLOSED
```

They must not be claimed until observed.

## 13. Non-goals

```text
No synthetic 27-export harness
No owner-state fabrication
No source-code inference
No provenance-only fallback
No global mutable session
No legacy oracle
No Python validator
No semantic rule implementation
No forced Satisfied/Failed result
No production promotion
```

## 14. Next revision gate

`ASH-CONTROL-RUNTIME-NATIVE-EXECUTABLE-SEMANTIC-RULE-CONTRACT-07E` is admissible only after a current explicit session proves:

```text
physicalInvocationCompletedCount=27
ownerRuntimeWitnessExportValidCount=27
ownerRuntimeWitnessExportMissingCount=0
```

Until then, physical owner invocation remains open and semantic-rule promotion is not admitted.
