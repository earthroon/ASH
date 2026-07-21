# ASH-TRUTH-AUDIT-01-R3-R2

## Independent Verifier Provenance Qualification / Local Contract Validator Reclassification / Function-Prefix False-Positive Elimination / Required Claim Policy Recompute and Phantom HOLD Retirement

## 0. Metadata

- Patch ID: `ASH-TRUTH-AUDIT-01-R3-R2`
- Parent: `ASH-TRUTH-AUDIT-01-R3-R1`
- Runtime binary: `crates/lora_train/src/bin/ash_truth_audit_01_r3.rs`
- Runtime schema: `ash.truth_audit.01.r3.runtime_artifact.v1`
- Runtime artifact: `workspace/runtime/truth_audit/ash_truth_audit_01_r3_runtime_artifact.json`
- Patch class: semantic evidence-classification false-positive repair
- Claim deletion: forbidden
- Direct repository PASS override: forbidden
- Evidence-strength relaxation: forbidden
- LoRA/Decode physical-proof changes: forbidden
- Atlas report group changes: forbidden unless field ownership is explicitly revised

## 1. Confirmed starting state

R3-R1 compiles and runs. The Atlas report seal passes:

```text
report_atlas_group_count=11
report_atlas_lane_count=4
report_atlas_field_count=59
report_atlas_duplicate_field_count=0
report_atlas_missing_required_field_count=0
report_atlas_validation_pass=true
```

The repository remains `HoldExplained` because four source findings are classified as required `IndependentVerifierInvocation` claims without accepted result artifacts.

```text
required_claim_count=6
required_claim_pass_count=2
required_claim_hold_count=4
independent_verifier_invocation_count=4
repository_hold_reason_ids=["HOLD_VERIFIER_RESULT_MISSING"]
```

LoRA MIN1 and Decode MIN1 remain accepted:

```text
runtime_observation_count=2
independent_comparator_count=2
independent_physical_verification_count=2
lora_min1_physical_proof_pass=true
decode_min1_physical_proof_pass=true
```

## 2. Confirmed false-positive claims

The following claim identities remain stable:

```text
CLAIM_SOURCE_C16AEE65A8AFA109
CLAIM_SOURCE_F680AEDABB1D6D3D
CLAIM_SOURCE_B6F8A5CB96A283A7
CLAIM_SOURCE_FA30C01C4F98EAA1
```

They originate from:

```text
validate_artifact_paths(...)
validate_dataset_paths(...)
validate_output_paths(...)
validate_log_path(...)
```

The calls occur inside producer-owned SFT artifact-capture and preflight builders, accumulate local failures/issues, and produce boolean path-contract fields. They do not expose independent verifier identities, separate execution boundaries, target-claim contracts, terminal result contracts, or verifier result artifacts.

## 3. Root cause

The R3 classifier previously used a verifier-like function prefix as final authority:

```text
validate_* | verify_* | check_*
-> IndependentVerifierInvocation
-> required governance claim
-> missing result artifact
-> repository HOLD
```

A function prefix is lexical evidence only. It cannot establish independent verifier provenance.

## 4. Repair objective

Required flow:

```text
source finding
-> lexical role candidate
-> primitive context collection
-> independent verifier provenance qualification
-> local contract validator qualification
-> final evidence-class assignment
-> required-claim policy recompute
-> active verifier registry rebuild
-> predicate/HOLD/roadmap recompute
```

## 5. Verifier-name candidate

`validate_*`, `verify_*`, and `check_*` calls may create an internal `VerifierNameCandidate` signal.

The signal:

```text
does not increment independent_verifier_invocation_count
does not create a verifier receipt
does not mark a claim required
does not select IndependentVerifierInvocation
```

## 6. Independent verifier provenance contract

A finding qualifies as `IndependentVerifierInvocation` only when all mandatory evidence exists:

```text
explicit verifier identity
separate execution or authority boundary
producer/verifier separation
target claim binding
terminal result-state contract
result artifact or result-digest contract
```

Allowed authority sources include an explicit verifier registry, verifier contract ID, separate verifier binary/module, independent artifact consumer, or accepted upstream verifier receipt.

A source-location hash identifies a finding. It does not establish verifier authority.

## 7. Local contract validator contract

A verifier-like lexical candidate qualifies as a local contract validator when it lacks independent verifier provenance and one or more of the following holds:

```text
producer/builder/preflight context
artifact-capture context
local &mut failures accumulator
local &mut issues accumulator
path/dataset/output/log validation relation
producer-owned boolean result field
```

Default final class:

```text
ComputedInvariant
```

Default domain:

```text
preflight_contract
```

Default policy:

```text
required=false
terminal_allowed=true
result=pass
promotion_eligible=false
```

## 8. Qualification failure IDs

Required stable IDs:

```text
VERIFIER_QUALIFICATION_PREFIX_ONLY
VERIFIER_QUALIFICATION_ID_MISSING
VERIFIER_QUALIFICATION_EXECUTION_BOUNDARY_MISSING
VERIFIER_QUALIFICATION_PRODUCER_SEPARATION_MISSING
VERIFIER_QUALIFICATION_TARGET_CLAIM_MISSING
VERIFIER_QUALIFICATION_RESULT_CONTRACT_MISSING
VERIFIER_QUALIFICATION_RESULT_ARTIFACT_CONTRACT_MISSING
VERIFIER_QUALIFICATION_LOCAL_BUILDER_CONTEXT
VERIFIER_QUALIFICATION_LOCAL_FAILURE_ACCUMULATOR
VERIFIER_QUALIFICATION_PATH_VALIDATION_ONLY
```

## 9. Current four-claim reclassification

Required:

```text
CLAIM_SOURCE_C16AEE65A8AFA109
  IndependentVerifierInvocation -> ComputedInvariant

CLAIM_SOURCE_F680AEDABB1D6D3D
  IndependentVerifierInvocation -> ComputedInvariant

CLAIM_SOURCE_B6F8A5CB96A283A7
  IndependentVerifierInvocation -> ComputedInvariant

CLAIM_SOURCE_FA30C01C4F98EAA1
  IndependentVerifierInvocation -> ComputedInvariant
```

The claim IDs and source references remain unchanged.

No hardcoded claim-ID bypass may be used as implementation authority. Exact IDs may appear in regression tests only.

## 10. Claim receipt additions

Each source claim exposes:

```text
lexical_verifier_candidate
verifier_provenance_qualified
local_contract_validator_qualified
classification_reason_ids
required_policy_reason
```

Expected current receipt shape:

```text
required=false
domain=preflight_contract
current_class=ComputedInvariant
terminal_allowed=true
result=pass
lexical_verifier_candidate=true
verifier_provenance_qualified=false
local_contract_validator_qualified=true
required_policy_reason=local_contract_validator_optional_by_policy
```

## 11. Requiredness authority

Requiredness may derive only from:

```text
explicit required claim ID
explicit repository policy domain rule
qualified verifier-role policy
explicit physical-proof policy
```

Requiredness must not derive from:

```text
function prefix
field suffix `_verified`
source path keyword
lexical verifier candidate
```

## 12. Verifier registry authority

Active verifier receipts are created only from findings whose final class is `IndependentVerifierInvocation` and whose provenance qualification passes.

Authoritative count:

```text
number of qualified active verifier receipts
```

Not authoritative:

```text
number of validate_/verify_/check_ lexical matches
```

## 13. Vacuous universal policy

The policy explicitly records:

```text
zero_qualified_verifier_invocations_satisfy_all_bound_results=true
```

Therefore, when no qualified verifier is invoked:

```text
REPO_INVOKED_VERIFIERS_HAVE_ACCEPTED_BOUND_RESULTS=true
```

This does not fabricate a verifier. A minimum verifier-count requirement would require a separate named policy predicate.

## 14. New repository predicates

Required:

```text
REPO_VERIFIER_CANDIDATES_PROVENANCE_QUALIFIED
REPO_NO_PREFIX_ONLY_VERIFIER_CLASSIFICATION
REPO_LOCAL_CONTRACT_VALIDATORS_NOT_REQUIRED_VERIFIER_CLAIMS
REPO_VERIFIER_RECEIPT_COUNT_MATCH_QUALIFIED_FINDINGS
REPO_RECLASSIFICATION_RECEIPT_COMPLETE
```

All are blocking because recurrence would make the repository verdict semantically unreliable.

## 15. Semantic classifier strengthening

`semantic_classifier_pass` requires:

```text
no direct performed claims
existing direct-performed repair pass
all lexical verifier candidates resolved as qualified verifiers or local validators
no IndependentVerifierInvocation assigned without provenance qualification
all source findings have nonempty final classes
```

## 16. Aggregate separation

After reclassification:

```text
computed_invariant_count includes local validators
structural_invariant_count excludes local contract validators
```

Expected delta for the current source tree:

```text
computed_invariant_count: 31 -> 35
structural_invariant_count: 31 -> 31
independent_verifier_invocation_count: 4 -> 0
```

Runtime output remains authoritative.

## 17. Promotion recompute

The four false-positive claims no longer request promotion to `IndependentPhysicalVerification`.

Expected current-source delta:

```text
promotion_eligible_claim_count: 29 -> 25
promotion_blocked_claim_count: 29 -> 25
```

Lineage-only optional claims retain their passthrough eligibility receipts.

## 18. Phantom HOLD retirement

When no unresolved qualified verifier remains:

```text
repository_hold_reason_count=0
repository_hold_reason_ids=[]
```

`HOLD_VERIFIER_RESULT_MISSING` must not survive solely because historical false-positive verifier receipts existed.

## 19. Phantom roadmap retirement

The following current tasks disappear when their source claims are reclassified:

```text
TRUTH-CLOSURE-0001
TRUTH-CLOSURE-0002
TRUTH-CLOSURE-0003
TRUTH-CLOSURE-0004
```

No result artifact is required for a local path validator.

## 20. Repository verdict recompute

The final verdict remains derived from named blocking predicates.

Forbidden:

```text
special-case the four claim IDs
ignore HOLD_VERIFIER_RESULT_MISSING
set repository_truth_audit_pass=true directly
change required counts after verdict computation
```

Required:

```text
classify primitive facts
rebuild claims
rebuild active verifiers
recompute predicates
recompute HOLD reasons
recompute roadmap
derive verdict last
```

## 21. Expected repaired state

Provided no unrelated blocker appears:

```text
PASS_ASH_TRUTH_AUDIT_01_R3
verdict=pass
repository_verdict_state=Pass
semantic_classifier_pass=true
repository_truth_audit_pass=true
repository_predicate_fail_count=0
repository_predicate_unavailable_count=0
repository_blocking_fail_count=0
repository_failed_predicates=[]
repository_blocking_failed_predicates=[]
required_claim_count=2
required_claim_pass_count=2
required_claim_hold_count=0
repository_hold_reason_count=0
repository_hold_reason_ids=[]
independent_verifier_invocation_count=0
lexical_verifier_candidate_count=4
qualified_verifier_finding_count=0
local_contract_validator_count=4
verifier_false_positive_count=4
active_repository_verifier_count=0
runtime_observation_count=2
independent_comparator_count=2
independent_physical_verification_count=2
lora_min1_physical_proof_pass=true
decode_min1_physical_proof_pass=true
all_truth_checks_pass=true
```

## 22. Atlas preservation

Required unchanged:

```text
report_atlas_group_count=11
report_atlas_lane_count=4
report_atlas_field_count=59
report_atlas_duplicate_field_count=0
report_atlas_missing_required_field_count=0
report_atlas_validation_pass=true
```

New provenance details remain nested inside `claim_evidence_receipt`; no new top-level field ownership is introduced.

## 23. Physical proof preservation

Required unchanged:

```text
lora_min1_physical_proof_pass=true
decode_min1_physical_proof_pass=true
runtime_observation_count=2
independent_comparator_count=2
independent_physical_verification_count=2
```

## 24. Static checks

```text
PATCH_ID=ASH-TRUTH-AUDIT-01-R3-R2
prefix-only direct verifier assignment=0
verifier provenance qualification function present
local contract validator qualification present
required policy computed after final classification
active verifier receipts derived only from qualified findings
hardcoded current claim-ID bypass=0
Atlas group count retained at 11
Atlas field ownership retained at 59
```

## 25. Regression tests

Required:

```text
local validate_artifact_paths call -> ComputedInvariant
local validate_output_paths call -> ComputedInvariant
explicitly qualified verifier call -> IndependentVerifierInvocation
current four claim IDs remain stable
current four claims required=false
current four claims domain=preflight_contract
current four claims current_class=ComputedInvariant
current four claims produce no active verifier receipt
```

## 26. Negative tests

```text
function prefix without provenance cannot become IndependentVerifierInvocation
_verified field name alone cannot create a verifier
registered verifier without accepted result remains HOLD
qualified verifier receipt count must match qualified findings
local validator marked required fails named predicate
classification reason receipt missing fails named predicate
```

## 27. Implementation scope

Only:

```text
crates/lora_train/src/bin/ash_truth_audit_01_r3.rs
```

No changes to R2, LoRA MIN1, Decode MIN1, optimizer, comparator, or source preflight implementations.

## 28. Compile command

```powershell
cargo check -p lora_train --bin ash_truth_audit_01_r3
```

## 29. Runtime command

```powershell
cargo run --release -p lora_train --bin ash_truth_audit_01_r3 -- --repo-root . --lora-min1-artifact workspace/runtime/lora/min1/ash_lora_min1_r1_runtime_artifact.json --decode-min1-artifact workspace/runtime/tensorcube/min1/ash_tcu_decode_min1_r1_runtime_artifact.json --write-runtime-artifact --print-repository-predicate-receipt --print-claim-evidence-receipt --print-claim-promotion-receipt --print-verifier-receipt --print-repository-hold-roadmap
```

## 30. PASS conditions

```text
lexical verifier candidates are nonterminal
independent verifier provenance is explicit
local validators classify as ComputedInvariant
current four claim identities remain visible
current four claims become optional preflight-contract claims
active verifier registry excludes the four false positives
required claim policy recomputes after classification
phantom HOLD and roadmap retire
repository PASS emerges from named predicates
LoRA and Decode remain accepted
Atlas report validation remains passing
artifact digest and promotion remain valid
```

## 31. FAIL conditions

```text
hardcoded claim-ID exception drives production behavior
source findings are deleted
prefix still assigns final verifier class
local validator still creates an active verifier receipt
old phantom HOLD survives with zero qualified verifiers
old roadmap tasks survive after reclassification
repository PASS is forced directly
requiredness is calculated before final classification
LoRA/Decode proof semantics change
Atlas ownership drifts silently
```

## 32. Canonical seal

```text
A verifier is an authority boundary.
It is not a prefix.
It is not a field suffix.
It is not a helper call.
It is not a boolean named verified.

Lexical evidence proposes a candidate.
Primitive context establishes locality.
Provenance establishes independence.
Policy establishes requiredness.
Predicates establish the verdict.

The four findings remain.
Their claim identities remain.
Their source references remain.
Only the false verifier class retires.
Only the phantom requiredness retires.
Only the phantom HOLD retires.
Only the phantom roadmap retires.

Primitive facts first.
Provenance second.
Evidence class third.
Policy fourth.
Verdict last.
```
