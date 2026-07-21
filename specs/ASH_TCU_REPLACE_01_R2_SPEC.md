# ASH-TCU-REPLACE-01-R2

## Primitive Writer Edge Identity Deduplication / Canonical Edge Key Uniqueness / Replacement Lexical Domain and Unicode Replacement Character Isolation / TensorCube Route-Replacement Symbol Allowlist / Runtime Writer Zero-State Witness / Conflict Pair Metric Materialization / Non-Conflict Exclusion Deduplication / Semantic and Execution Dual Digest Closure / Premature REPLACE-02 Readiness Reblock / No Runtime Behavior Change / No Replacement Enablement Seal

## 0. Patch Metadata

- Patch ID: `ASH-TCU-REPLACE-01-R2`
- Parent: `ASH-TCU-REPLACE-01-R1`
- Parent runtime schema: `ash.tcu.replace.01.r1.ownership_audit.runtime_artifact.v1`
- Parent semantic inventory digest: `4e70e449660dac130d56930dbd3abf91c5889d3ed1d5eabc2198bf2515ad3e12`
- R2 runtime schema: `ash.tcu.replace.01.r2.ownership_audit.runtime_artifact.v1`
- Runtime binary: `crates/orchestrator_local/src/bin/ash_tcu_replace_01_legacy_replacement_boolean_ownership_audit.rs`
- Primary runtime artifact: `workspace/runtime/tensorcube/ash_tcu_replace_01_r2_ownership_audit_runtime_artifact.json`
- Local manifest: `artifacts/ASH_TCU_REPLACE_01_R2_LOCAL_MANIFEST.json`
- Runtime behavior change, GPU acquisition, command submission, route mutation, replacement enablement, production promotion, performance claim, and REPLACE-02 policy implementation are forbidden.

## 1. Purpose

R2 repairs the remaining graph-authority defects in R1 while preserving all R1 safety truth. R1 correctly established self-scan exclusion, generated vocabulary isolation, comment/projection/test/guard writer repair, parent digest retirement, and no runtime behavior change. R2 closes duplicate primitive edge identity, lexical-domain contamination, unproven runtime-writer zero state, incomplete pair metric materialization, duplicate non-conflict receipts, dual digest separation, and premature REPLACE-02 readiness.

## 2. Parent Truth Partition

Preserved:

```text
self_scan_occurrence_count=0
comment_writer_count=0
projection_runtime_writer_count=0
test_runtime_writer_count=0
guard_writer_count=0
runtime_behavior_changed=false
replacement_enabled_by_patch=false
production_replacement_executed_by_patch=false
performance_claim_allowed_by_patch=false
```

Superseded and historical only:

```text
R1 primitive writer graph identity
R1 conflict pair metrics
R1 semantic inventory digest
R1 repository_ready_for_replace_02=true
```

The R1 digest may remain in lineage metadata but may not serve as the REPLACE-02 parent.

## 3. Raw Candidate and Canonical Edge Split

The scanner must distinguish raw syntax candidates from canonical semantic edges.

```rust
struct RawWriterEdgeCandidate {
    candidate_id: String,
    source_occurrence_id: String,
    payload: WriterEdgePayload,
}

struct CanonicalPrimitiveWriterEdge {
    edge_id: String,
    canonical_edge_key: CanonicalEdgeKey,
    payload: WriterEdgePayload,
    raw_candidate_ids: Vec<String>,
}
```

Only canonical edges enter the authority graph, conflict pair universe, semantic digest, and readiness derivation.

## 4. Canonical Edge Identity

```rust
struct CanonicalEdgeKey {
    source_occurrence_id: String,
    canonical_state_key: CanonicalStateKey,
    authority_root_id: String,
    authority_scope_key: String,
    writer_semantic_class: WriterSemanticClass,
    write_operation: WriteOperation,
    value_expression_digest: String,
    condition_digest: Option<String>,
}
```

`edge_id` is the SHA-256 of canonical JSON for this key. Canonical inputs are repository-relative and deterministic. Traversal order, timestamps, absolute paths, output paths, and JSON presentation are forbidden inputs.

Required processing order:

```text
source enumeration
→ parsing
→ raw finding classification
→ lexical-domain classification
→ route allowlist gate
→ raw edge candidate creation
→ canonical edge key construction
→ canonical edge deduplication
→ graph construction
→ pair construction
→ digest construction
```

Deduplication after pair counting or digest construction is forbidden.

## 5. Edge Deduplication and Collision Rules

Exact duplicate candidates collapse into one canonical edge and retain sorted unique candidate IDs as provenance.

Required counters:

```text
raw_writer_edge_candidate_count
route_graph_eligible_raw_candidate_count
canonical_primitive_writer_edge_count
unique_canonical_edge_key_count
unique_edge_id_count
exact_duplicate_candidate_count
duplicate_edge_id_count
canonical_edge_id_collision_count
canonical_edge_payload_divergence_count
```

Required invariants:

```text
canonical_primitive_writer_edge_count
= unique_canonical_edge_key_count
= unique_edge_id_count

duplicate_edge_id_count=0
canonical_edge_id_collision_count=0
canonical_edge_payload_divergence_count=0
```

Same edge ID with a different canonical key is blocking. The same key with divergent semantic payload is also blocking.

## 6. Replacement Lexical Domains

```rust
enum ReplacementLexicalDomain {
    TensorCubeRouteReplacement,
    TensorCubeProductionReplacementGovernance,
    UnicodeReplacementCharacter,
    TokenizerDecodeReplacement,
    TextSubstitution,
    ResourceOrArtifactReplacement,
    AtlasResourceReplacement,
    GenericBusinessReplacement,
    AuditGeneratedReplacementVocabulary,
    Unknown,
}
```

A substring match on `replacement` may create a lexical candidate only. It may not create a TensorCube route edge.

Unicode replacement-character families such as `contains_replacement_char`, `replacement_character`, `replacement_char_count`, `forbid_replacement_char`, `LegacyReplacementCharacterObserved`, and U+FFFD must not enter the route graph.

Tokenizer, SentencePiece, UTF-8 assembly, generation-hygiene, resource, file, checkpoint, artifact, and atlas replacement semantics remain isolated.

Required:

```text
unicode_replacement_character_route_edge_count=0
tokenizer_decode_replacement_route_edge_count=0
resource_replacement_route_edge_count=0
atlas_replacement_route_edge_count=0
unknown_replacement_domain_count=0
```

Unknown findings fail closed and are emitted in a dedicated receipt.

## 7. TensorCube Route-Replacement Allowlist SSOT

All route-graph admission flows through one immutable allowlist registry.

```rust
struct RouteReplacementSymbolRule {
    rule_id: String,
    symbol_pattern: SymbolPattern,
    required_module_patterns: Vec<String>,
    forbidden_module_patterns: Vec<String>,
    canonical_state_key: CanonicalStateKey,
    allowed_roles: Vec<ReplacementOccurrenceRole>,
    allowed_writer_classes: Vec<WriterSemanticClass>,
}
```

Admitted families may include exact, context-proven TensorCube symbols such as:

```text
tensorcube_matmul_replacement_enabled
matmul_replacement_enabled
replacement_enabled
production_replacement_allowed
production_replacement_executed
production_default_change_allowed
production_default_changed
direct_replacement_allowed
runtime_apply_allowed
backend_policy_mutation_allowed
shadow_route_opened
tensorcube_shadow_route_opened
default_route_adopted
route_adoption
performance_claim_allowed
performance_claim
```

Generic names require a TensorCube route or governance context and an explicit allowlist rule.

Forbidden contexts include tokenizer, Unicode, UTF-8, SentencePiece, replacement-character, generation-hygiene, artifact, atlas, resource, and checkpoint replacement.

Required:

```text
no_substring_only_route_admission=true
```

## 8. Runtime Writer Zero-State Witness

Runtime writer classes are limited to:

```text
RegistryMutationWrite
RuntimeStateWrite
OutputAuthorityWrite
PromotionAuthorityWrite
```

Construction, configuration, projection, derived-local, test, comment, and read-only guard writes are not runtime writers.

The mutation primitive registry must cover route registry insert/replace/remove, active/default/production route pointer assignment, route epoch increment, prepared transaction commit, runtime route bind/unbind, output owner commit, and production replacement commit.

```rust
enum RuntimeWriterZeroStateClass {
    ProvenNoRuntimeRouteReplacementWriter,
    RuntimeWriterExists,
    ScannerCoverageIncomplete,
    RuntimeWriterClassificationAmbiguous,
}
```

If `runtime_writer_count=0`, PASS requires:

```text
zero_state_class=PROVEN_NO_RUNTIME_ROUTE_REPLACEMENT_WRITER
missing_required_runtime_surface_count=0
unclassified_runtime_mutation_candidate_count=0
runtime_writer_scanner_coverage_pass=true
```

A zero count without surface coverage is blocking.

## 9. Conflict Pair Universe and Metrics

Conflict analysis operates on unique canonical edges only. For `n = canonical_primitive_writer_edge_count`:

```text
candidate_edge_pair_count = n * (n - 1) / 2
```

Checked integer arithmetic is mandatory. Each unordered pair has one canonical key with lexicographically ordered edge IDs.

Required metrics:

```text
candidate_edge_pair_count
expected_candidate_edge_pair_count
same_state_pair_count
different_state_pair_count
same_state_same_scope_pair_count
same_state_non_overlapping_scope_pair_count
independent_authority_root_pair_count
related_authority_root_pair_count
runtime_writer_pair_count
non_runtime_writer_pair_count
compatible_pair_count
conflict_pair_count
blocking_conflict_pair_count
non_blocking_conflict_pair_count
non_conflict_exclusion_pair_count
unresolved_pair_count
duplicate_non_conflict_pair_count
```

Required conservation:

```text
candidate_edge_pair_count
= same_state_pair_count + different_state_pair_count

candidate_edge_pair_count
= conflict_pair_count
+ non_conflict_exclusion_pair_count
+ unresolved_pair_count
```

Required:

```text
pair_count_formula_pass=true
pair_conservation_pass=true
unresolved_pair_count=0
```

## 10. Non-Conflict Exclusion Deduplication

Each non-conflicting unordered pair emits exactly one canonical receipt.

```rust
struct CanonicalNonConflictExclusion {
    pair_key: CanonicalEdgePairKey,
    canonical_state_key: Option<CanonicalStateKey>,
    primary_reason: NonConflictReason,
    secondary_reasons: Vec<NonConflictReason>,
}
```

Primary reason precedence:

```text
DifferentCanonicalState
NonRuntimeWriterClass
ProjectionOnly
TestOnly
ArtifactOnly
NonOverlappingScope
SameAuthorityRoot
ParentChildAuthorityRelation
CompatibleWriteSemantics
DifferentLifecycleStage
```

Required:

```text
duplicate_non_conflict_pair_count=0
canonical_non_conflict_exclusion_count=non_conflict_exclusion_pair_count
```

## 11. Semantic and Execution Dual Digest

R2 emits:

```text
semantic_inventory_digest
execution_artifact_digest
```

The semantic digest represents repository ownership semantics and binds the allowlist digest, lexical-domain registry, unique canonical edges, authority roots, runtime-writer witness semantic fields, pair metrics, conflicts, and canonical exclusions.

The execution digest represents the canonical emitted runtime artifact.

Execution digest self-cycle avoidance:

```text
1. construct the artifact
2. set execution_artifact_digest=null
3. canonicalize
4. hash
5. write the digest into the closure and verdict
6. serialize the final artifact
```

The primary artifact and execution-digest closure receipt may be declared self-digest boundary exclusions. All non-self-referential supporting receipts are bound by repository-relative path, semantic digest, and pretty-file digest.

The R2 semantic digest must differ from the R1 digest.

## 12. R1 Readiness Reblock and R2 Readiness Formula

R1 readiness is historical only:

```text
historical_result=true
promotion_authority_valid=false
superseded_by=ASH-TCU-REPLACE-01-R2
```

R2 readiness initializes false and becomes true only when every blocking R2 predicate passes, including edge uniqueness, lexical isolation, allowlist enforcement, runtime-writer proof, pair formula and conservation, zero unresolved pairs, zero blocking conflicts, non-conflict deduplication, dual digest closure, digest change, and all no-change/no-enablement guards.

`recommended_next_patch` may name REPLACE-02 only when `repository_ready_for_replace_02=true`.

## 13. Required Runtime Outputs

```text
workspace/runtime/tensorcube/
  ash_tcu_replace_01_r2_ownership_audit_runtime_artifact.json
  ash_tcu_replace_01_r2_r1_readiness_reblock_receipt.json
  ash_tcu_replace_01_r2_lexical_domain_registry.json
  ash_tcu_replace_01_r2_route_replacement_symbol_allowlist.json
  ash_tcu_replace_01_r2_lexical_domain_classification_receipt.json
  ash_tcu_replace_01_r2_excluded_replacement_domain_receipt.json
  ash_tcu_replace_01_r2_unknown_replacement_domain_receipt.json
  ash_tcu_replace_01_r2_raw_writer_edge_candidate_inventory.json
  ash_tcu_replace_01_r2_canonical_primitive_writer_edge_graph.json
  ash_tcu_replace_01_r2_edge_identity_dedup_receipt.json
  ash_tcu_replace_01_r2_edge_id_collision_receipt.json
  ash_tcu_replace_01_r2_runtime_mutation_primitive_registry.json
  ash_tcu_replace_01_r2_runtime_writer_zero_state_witness.json
  ash_tcu_replace_01_r2_conflict_pair_metric_receipt.json
  ash_tcu_replace_01_r2_conflict_pair_evaluation_digest.json
  ash_tcu_replace_01_r2_authority_conflict_receipt.json
  ash_tcu_replace_01_r2_non_conflict_exclusion_receipt.json
  ash_tcu_replace_01_r2_non_conflict_exclusion_dedup_receipt.json
  ash_tcu_replace_01_r2_semantic_digest_closure.json
  ash_tcu_replace_01_r2_execution_digest_closure.json
  ash_tcu_replace_01_r2_receipt_digest_registry.json
  ash_tcu_replace_01_r2_no_runtime_behavior_change_guard.json
  ash_tcu_replace_01_r2_no_replacement_enablement_guard.json
  ash_tcu_replace_01_r2_no_production_promotion_guard.json
  ash_tcu_replace_01_r2_no_performance_claim_guard.json
  ash_tcu_replace_01_r2_static_checks.json
  ash_tcu_replace_01_r2_verdict.json

artifacts/
  ASH_TCU_REPLACE_01_R2_LOCAL_MANIFEST.json
```

## 14. Blocking Predicates

```text
TCU_REPLACE_01_R2_R1_SELF_SCAN_EXCLUSION_PRESERVED
TCU_REPLACE_01_R2_COMMENT_WRITER_COUNT_ZERO
TCU_REPLACE_01_R2_PROJECTION_RUNTIME_WRITER_COUNT_ZERO
TCU_REPLACE_01_R2_TEST_RUNTIME_WRITER_COUNT_ZERO
TCU_REPLACE_01_R2_READ_ONLY_GUARD_WRITER_COUNT_ZERO
TCU_REPLACE_01_R2_CANONICAL_EDGE_KEYS_UNIQUE
TCU_REPLACE_01_R2_EDGE_ID_COLLISION_COUNT_ZERO
TCU_REPLACE_01_R2_EDGE_PAYLOAD_DIVERGENCE_COUNT_ZERO
TCU_REPLACE_01_R2_REPLACEMENT_LEXICAL_DOMAINS_ISOLATED
TCU_REPLACE_01_R2_UNKNOWN_REPLACEMENT_DOMAIN_COUNT_ZERO
TCU_REPLACE_01_R2_ROUTE_REPLACEMENT_ALLOWLIST_ENFORCED
TCU_REPLACE_01_R2_RUNTIME_WRITER_ZERO_STATE_WITNESS_VALID
TCU_REPLACE_01_R2_CANDIDATE_PAIR_COUNT_FORMULA_VALID
TCU_REPLACE_01_R2_PAIR_CONSERVATION_INVARIANTS_PASS
TCU_REPLACE_01_R2_UNRESOLVED_PAIR_COUNT_ZERO
TCU_REPLACE_01_R2_DUPLICATE_NON_CONFLICT_PAIR_COUNT_ZERO
TCU_REPLACE_01_R2_BLOCKING_CONFLICT_PAIR_COUNT_ZERO
TCU_REPLACE_01_R2_SEMANTIC_DIGEST_CREATED
TCU_REPLACE_01_R2_EXECUTION_ARTIFACT_DIGEST_CREATED
TCU_REPLACE_01_R2_SEMANTIC_AND_EXECUTION_DIGESTS_DISTINCT
TCU_REPLACE_01_R2_R2_DIGEST_DIFFERS_FROM_R1
TCU_REPLACE_01_R2_DIGESTS_DETERMINISTIC
TCU_REPLACE_01_R2_PREMATURE_R1_REPLACE_02_READINESS_REBLOCKED
TCU_REPLACE_01_R2_NO_RUNTIME_BEHAVIOR_CHANGE
TCU_REPLACE_01_R2_NO_REPLACEMENT_ENABLEMENT
TCU_REPLACE_01_R2_NO_PRODUCTION_PROMOTION
TCU_REPLACE_01_R2_NO_PERFORMANCE_CLAIM
TCU_REPLACE_01_R2_ALL_BLOCKING_PREDICATES_PASS
```

## 15. Required Tests

At minimum:

```text
identical_raw_candidates_collapse_to_one_edge
same_edge_id_different_key_fails
same_key_different_payload_fails
canonical_edge_id_is_order_independent
contains_replacement_char_is_unicode_domain
invalidate_on_atlas_replacement_is_atlas_resource_domain
production_replacement_executed_is_governance_domain
substring_replacement_does_not_admit_route_edge
zero_runtime_writer_requires_coverage_witness
pair_count_n_edges_is_n_choose_two
unordered_pair_key_is_canonical
one_pair_emits_one_non_conflict_receipt
pair_conservation_invariants_hold
semantic_digest_ignores_duplicate_candidate_order
execution_digest_has_no_self_hash_cycle
r1_self_scan_exclusion_still_passes
g209t0_writer_count_remains_zero
unicode_replacement_character_route_edge_count_zero
runtime_writer_zero_state_witness_present
unresolved_pair_count_zero
duplicate_non_conflict_pair_count_zero
```

## 16. Safety Guards

All of the following remain false:

```text
gpu_adapter_requested
gpu_device_requested
command_encoder_created
command_submitted
route_registry_mutated
route_epoch_incremented
default_route_changed
production_route_changed
output_owner_changed
model_output_changed
training_output_changed
decode_output_changed
model_weights_mutated
optimizer_state_mutated
replacement_enabled_by_patch
production_replacement_executed
performance_claim_allowed
```

## 17. REPLACE-02 Boundary

REPLACE-02 may begin only when R2 proves canonical edge uniqueness, route lexical-domain purity, allowlist-only admission, runtime-writer zero-state or complete nonzero writer proof, complete pair materialization, one exclusion per non-conflict pair, zero unresolved pairs, zero blocking conflicts, dual digest closure, and `repository_ready_for_replace_02=true`.

REPLACE-02 binds the R2 semantic inventory digest and allowlist digest. It must not bind the R1 digest.

## 18. PASS and HOLD Markers

PASS:

```text
PASS_ASH_TCU_REPLACE_01_R2_PRIMITIVE_WRITER_EDGE_IDENTITIES_DEDUPLICATED_CANONICAL_EDGE_KEYS_UNIQUE_REPLACEMENT_LEXICAL_DOMAINS_ISOLATED_TENSORCUBE_ROUTE_REPLACEMENT_ALLOWLIST_ENFORCED_RUNTIME_WRITER_ZERO_STATE_OR_COMPLETE_WRITER_SET_PROVEN_CONFLICT_PAIR_METRICS_MATERIALIZED_NON_CONFLICT_EXCLUSIONS_DEDUPLICATED_SEMANTIC_AND_EXECUTION_DUAL_DIGESTS_CLOSED_PREMATURE_REPLACE_02_READINESS_REBLOCKED_AND_REDERIVED_NO_RUNTIME_BEHAVIOR_CHANGE_NO_REPLACEMENT_ENABLEMENT
```

HOLD:

```text
HOLD_ASH_TCU_REPLACE_01_R2_ROUTE_REPLACEMENT_OWNERSHIP_GRAPH_NOT_YET_CANONICAL
```

## 19. Final Seal

R2 passes only when every primitive edge has one canonical identity, duplicate scanner candidates do not become duplicate graph nodes, Unicode/tokenizer/resource/atlas replacement semantics cannot enter the TensorCube route graph, only allowlisted context-proven symbols enter, a zero runtime writer count is supported by mutation-surface coverage, every unique pair has one result, every non-conflicting pair has one canonical exclusion, semantic and execution digest domains are closed, R1 readiness is historical only, and no runtime behavior, replacement enablement, production promotion, or performance claim occurs.
