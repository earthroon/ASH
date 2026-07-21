# ASH-TRUTH-AUDIT-01-R3

## Repository Verdict Predicate Surface / Lineage-Only Claim Promotion Eligibility / Structural Invariant vs Independent Verification Separation / Final HOLD Cause Receipt and Closure Roadmap

## 0. Metadata

- Patch ID: `ASH-TRUTH-AUDIT-01-R3`
- Parent: `ASH-TRUTH-AUDIT-01-R2`
- Runtime schema: `ash.truth_audit.01.r3.runtime_artifact.v1`
- Policy ID: `ash.repository.truth.policy.v1`
- Artifact: `workspace/runtime/truth_audit/ash_truth_audit_01_r3_runtime_artifact.json`
- Automatic PASS, promotion, evidence relaxation, and claim deletion: forbidden

## 1. Confirmed input

R2 currently reports:

```text
semantic_classifier_pass=true
repository_truth_audit_pass=false
independent_verifier_invocation_count=4
unknown_requires_review_count=0
lora_min1_physical_proof_pass=true
decode_min1_physical_proof_pass=true
runtime_observation_count=2
independent_comparator_count=2
independent_physical_verification_count=2
```

LoRA MIN1 and Decode MIN1 are accepted physical proofs. R3 must preserve them.

The current repository HOLD is caused by four verifier-like source invocations. The aggregates `lineage_only_verification_count=25` and `structural_invariant_count=31` remain visible but are not universal zero thresholds.

## 2. Objective

Replace `repository_truth_audit_pass=false` with:

```text
repository policy receipt
stable claim registry
named non-short-circuiting predicates
claim evidence and promotion receipts
verifier result-state receipts
HOLD root-cause receipts
closure roadmap
```

Every blocking failure must expose predicate IDs, claim IDs, expected and actual values, current and required evidence classes, blocker IDs, and evidence-producing work.

## 3. Evidence classes

```text
DirectPerformed
DirectVerifiedPassthrough
ComputedInvariant
LineageOnly
StructuralInvariant
IndependentVerifierInvocation
RuntimeObservation
IndependentComparator
IndependentPhysicalVerification
NegativeFixtureMutation
UnknownRequiresReview
ConfirmedFalseVerification
```

Forbidden substitutions:

```text
StructuralInvariant -> RuntimeObservation
IndependentVerifierInvocation -> IndependentPhysicalVerification
LineageOnly -> DirectVerifiedPassthrough without a verified source artifact
NegativeFixtureMutation -> positive runtime proof
```

## 4. Claim registry

Each scanned source finding receives a stable ID:

```text
CLAIM_SOURCE_<16 uppercase SHA-256 hex>
```

The digest input is repository-relative path, line, function, and field. IDs are independent of array and console ordering.

Required claim categories:

```text
DirectPerformed source claims
UnknownRequiresReview source claims
IndependentVerifierInvocation source claims
CLAIM_LORA_MIN1_PHYSICAL_PROOF
CLAIM_DECODE_MIN1_PHYSICAL_PROOF
```

Lineage, structural, runtime observation, comparator, and negative-fixture source findings remain optional unless a later explicit policy revision marks them required.

## 5. Closed physical claims

```text
CLAIM_LORA_MIN1_PHYSICAL_PROOF
CLAIM_DECODE_MIN1_PHYSICAL_PROOF
```

Allowed terminal class:

```text
IndependentPhysicalVerification
```

These claims remain `pass` while their source artifacts are independently accepted.

## 6. Claim receipt

```json
{
  "claim_id": "CLAIM_SOURCE_...",
  "title": "path:line field",
  "required": true,
  "domain": "governance",
  "current_evidence_class": "IndependentVerifierInvocation",
  "allowed_terminal_evidence_classes": ["IndependentPhysicalVerification"],
  "terminal_class_allowed": false,
  "result": "hold",
  "promotion_eligible": true,
  "eligible_target_classes": ["IndependentPhysicalVerification"],
  "promotion_blocker_ids": [
    "PROMOTION_VERIFIER_RESULT_MISSING",
    "PROMOTION_SOURCE_CLAIM_UNBOUND"
  ],
  "evidence_refs": ["source:crates/...:line"]
}
```

States: `pass`, `hold`, `fail`, `unavailable`, `contradicted`, `not_applicable`.

## 7. Lineage promotion eligibility

Lineage-only findings remain informational under the reconstructed R2 policy. Eligibility does not perform promotion.

Blocker IDs include:

```text
PROMOTION_SOURCE_ARTIFACT_MISSING
PROMOTION_SOURCE_DIGEST_INVALID
PROMOTION_SOURCE_CLAIM_UNBOUND
PROMOTION_SEMANTIC_IDENTITY_MISMATCH
PROMOTION_EVIDENCE_STALE
```

Direct verified passthrough requires a canonical source artifact, valid digest, exact source claim identity, accepted source result, semantic identity, and no newer contradiction.

## 8. Structural separation

Structural evidence is terminal only for structural claims such as module existence, schema identity, registry uniqueness, or forbidden-symbol absence.

It is not terminal proof of GPU dispatch, runtime ownership, mutation, numerical parity, or physical execution.

R3 reports:

```text
lineage_only_required_claim_count
structural_only_required_claim_count
```

Only required claims with insufficient terminal classes block PASS.

## 9. Verifier registry

Each verifier-like finding receives:

```text
VERIFIER_SOURCE_<16 uppercase SHA-256 hex>
```

Initial receipt:

```json
{
  "verifier_id": "VERIFIER_SOURCE_...",
  "claim_id": "CLAIM_SOURCE_...",
  "invoked": true,
  "started": false,
  "completed": false,
  "result_state": "Unbound",
  "result_artifact_present": false,
  "result_artifact_digest_valid": false,
  "result_accepted": false,
  "covered_claim_ids": [],
  "unbound_claim_ids": ["CLAIM_SOURCE_..."],
  "source_ref": "source:crates/...:line"
}
```

`invoked=true` preserves R2 source classification. `started=false` and `completed=false` mean no runtime result receipt was observed.

Only `CompletedAccepted` with an exact claim binding may become terminal independent verification.

## 10. Repository predicate receipt

```json
{
  "predicate_id": "REPO_...",
  "category": "Verifier",
  "expected": true,
  "actual": false,
  "pass": false,
  "available": true,
  "blocking": true,
  "failure_kind": "VerifierResultMissing",
  "claim_ids": ["CLAIM_SOURCE_..."],
  "evidence_refs": []
}
```

All safely evaluable predicates run without short-circuiting.

## 11. Required predicates

Policy and registry:

```text
REPO_POLICY_PRESENT
REPO_POLICY_SCHEMA_SUPPORTED
REPO_CLAIM_IDS_UNIQUE
REPO_REQUIRED_CLAIMS_REGISTERED
```

Semantic and coverage:

```text
REPO_SEMANTIC_CLASSIFIER_PASS
REPO_NO_REQUIRED_UNKNOWN_CLAIMS
REPO_NO_REQUIRED_CONFIRMED_FALSE_CLAIMS
REPO_ALL_REQUIRED_CLAIMS_EVALUATED
REPO_ALL_REQUIRED_CLAIMS_USE_ALLOWED_TERMINAL_CLASS
```

Verifier:

```text
REPO_INVOKED_VERIFIERS_HAVE_ACCEPTED_BOUND_RESULTS
```

Physical proof:

```text
REPO_LORA_MIN1_PHYSICAL_PROOF_PASS
REPO_DECODE_MIN1_PHYSICAL_PROOF_PASS
```

Aggregate consistency:

```text
REPO_VERIFIER_INVOCATION_COUNT_MATCH
REPO_RUNTIME_OBSERVATION_COUNT_MATCH
REPO_INDEPENDENT_COMPARATOR_COUNT_MATCH
REPO_INDEPENDENT_PHYSICAL_VERIFICATION_COUNT_MATCH
```

Contradiction and verdict:

```text
REPO_NO_UNRESOLVED_REQUIRED_CLAIM_CONTRADICTIONS
REPO_ALL_BLOCKING_PREDICATES_PASS
REPO_VERDICT_RECOMPUTED_MATCH_REPORTED
```

`REPO_ALL_BLOCKING_PREDICATES_PASS` is a summary predicate and is not included in its own input set.

## 12. Current expected blocker

```text
HOLD_VERIFIER_RESULT_MISSING
```

It deduplicates failures from:

```text
REPO_INVOKED_VERIFIERS_HAVE_ACCEPTED_BOUND_RESULTS
REPO_ALL_REQUIRED_CLAIMS_USE_ALLOWED_TERMINAL_CLASS
```

The current source tree is expected to produce four verifier claims, two closed physical claims, and no required lineage-only or structural-only claim. Runtime output remains authoritative.

## 13. HOLD receipt

```json
{
  "hold_reason_id": "HOLD_VERIFIER_RESULT_MISSING",
  "blocking": true,
  "predicate_ids": [
    "REPO_INVOKED_VERIFIERS_HAVE_ACCEPTED_BOUND_RESULTS",
    "REPO_ALL_REQUIRED_CLAIMS_USE_ALLOWED_TERMINAL_CLASS"
  ],
  "claim_ids": [],
  "summary": "Verifier-like source invocations have no accepted result artifacts bound to their claims",
  "required_actions": [
    "Assign each verifier a runtime contract",
    "Execute it and emit a result artifact",
    "Verify the result digest",
    "Bind it to the exact claim ID",
    "Add required negative-fixture coverage",
    "Rerun R3"
  ]
}
```

## 14. Closure roadmap

One task is emitted per unresolved verifier claim:

```json
{
  "task_id": "TRUTH-CLOSURE-0001",
  "priority": 5,
  "blocking": true,
  "claim_ids": ["CLAIM_SOURCE_..."],
  "predicate_ids": [
    "REPO_INVOKED_VERIFIERS_HAVE_ACCEPTED_BOUND_RESULTS",
    "REPO_ALL_REQUIRED_CLAIMS_USE_ALLOWED_TERMINAL_CLASS"
  ],
  "hold_reason_ids": ["HOLD_VERIFIER_RESULT_MISSING"],
  "current_evidence_class": "IndependentVerifierInvocation",
  "target_evidence_class": "IndependentPhysicalVerification",
  "required_work": [],
  "expected_artifacts": [],
  "rerun_commands": []
}
```

Tasks must produce evidence. Relabeling a class is not closure work.

## 15. Verdict states

```text
Invalid
HoldUnexplained
HoldExplained
Pass
```

The expected initial result is:

```text
repository_verdict_state=HoldExplained
repository_truth_audit_pass=false
```

R3 diagnostic implementation is successful when every blocking failure is explained, even if repository PASS remains false.

## 16. Runtime artifact

Required fields include policy, named predicate counts and receipts, required claim counts, claim evidence receipts, verifier receipts, HOLD reason receipts, closure roadmap, preserved R2 aggregate counters, LoRA and Decode physical proof states, and `artifact_digest`.

## 17. Artifact integrity

R3 uses:

```text
one pretty JSON candidate serialization
fixed-width artifact_digest placeholder
canonical recursive key ordering
SHA-256
fixed-width byte patch
JSON reparse verification
temporary byte readback parity
digest readback parity
atomic promotion
previous artifact restoration on failure
```

The report digest neutralizes only `/artifact_digest`.

## 18. CLI

```text
--repo-root
--lora-min1-artifact
--decode-min1-artifact
--runtime-artifact
--write-runtime-artifact
--require-pass
--print-repository-predicate-receipt
--print-claim-evidence-receipt
--print-claim-promotion-receipt
--print-verifier-receipt
--print-repository-hold-roadmap
--claim-filter <CLAIM_ID>
--verifier-filter <VERIFIER_ID>
```

## 19. Expected first run

```text
HOLD_ASH_TRUTH_AUDIT_01_R3
verdict=hold
repository_verdict_state=HoldExplained
semantic_classifier_pass=true
repository_truth_audit_pass=false
repository_hold_reason_ids=["HOLD_VERIFIER_RESULT_MISSING"]
required_claim_pass_count=2
required_claim_hold_count=4
lineage_only_required_claim_count=0
structural_only_required_claim_count=0
lora_min1_physical_proof_pass=true
decode_min1_physical_proof_pass=true
independent_physical_verification_count=2
all_truth_checks_pass=false
```

Exact counts are runtime-owned.

## 20. Final PASS

```text
repository_verdict_state=Pass
repository_truth_audit_pass=true
repository_blocking_fail_count=0
repository_blocking_failed_predicates=[]
repository_hold_reason_count=0
repository_hold_reason_ids=[]
required_claim_hold_count=0
required_claim_fail_count=0
required_claim_unavailable_count=0
required_claim_contradicted_count=0
all_truth_checks_pass=true
```

## 21. Static and negative tests

Required static checks:

```text
R3 patch ID and artifact path are distinct
R2 remains unchanged
claim and verifier IDs are stable
report digest verifies after fixed-width patch
verifier invocation maps to required HOLD
LoRA and Decode map to closed physical claims
repository PASS derives from named blocking predicates
```

Required mutations:

```text
remove or duplicate a required claim
mark verifier accepted without claim binding
attach invalid result digest
classify a physical claim as StructuralInvariant
change reported verdict without predicates
corrupt aggregate verifier count
corrupt R3 artifact digest
```

Each must fail a named predicate or artifact integrity check.

## 22. Implementation scope

```text
crates/lora_train/src/bin/ash_truth_audit_01_r3.rs
```

R2 remains unchanged. Cargo auto-discovers R3 from `src/bin`.

## 23. Run command

```powershell
cargo run --release -p lora_train --bin ash_truth_audit_01_r3 -- --repo-root . --lora-min1-artifact workspace/runtime/lora/min1/ash_lora_min1_r1_runtime_artifact.json --decode-min1-artifact workspace/runtime/tensorcube/min1/ash_tcu_decode_min1_r1_runtime_artifact.json --write-runtime-artifact --print-repository-predicate-receipt --print-claim-promotion-receipt --print-verifier-receipt --print-repository-hold-roadmap
```

## 24. PASS conditions

```text
explicit policy
stable claim identities
required and optional separation
no implicit lineage or structural threshold
invocation separated from accepted verification
named non-short-circuiting predicates
blocking defects mapped to claims
promotion blockers exposed
HOLD causes deduplicated
roadmap produces evidence
LoRA and Decode proofs preserved
artifact digest and readback parity verified
reproducible verdict
```

## 25. FAIL conditions

```text
opaque repository boolean remains
aggregate count becomes hidden policy
lineage or structural evidence is auto-promoted
verifier call existence becomes verification success
result artifact lacks claim binding
required claims are deleted for PASS
failure output lacks expected or actual values
roadmap merely renames evidence
closed physical proofs are reopened without contradiction
runtime artifact digest is not independently verified
```

## 26. Canonical seal

```text
A repository HOLD is not a diagnosis.
A count is not a policy.
A lineage is not execution.
A structure is not observation.
A verifier invocation is not an accepted result.

LoRA MIN1 is accepted.
Decode MIN1 is accepted.
Their physical proofs remain closed.

The remaining verifier claims receive stable identities,
explicit result states, explicit blockers, and evidence-producing work.

No opaque repository boolean.
No automatic promotion.
No structural-to-runtime substitution.
No invocation-to-verification substitution.
No hidden aggregate threshold.
No claim deletion for PASS.

One policy.
One claim registry.
One predicate surface.
One HOLD map.
One closure roadmap.
One reproducible verdict.
```
