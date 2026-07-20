# ASH-TRUTH-AUDIT-01-R2
# Semantic Evidence Classifier Refinement / Direct Performed-Claim Verification Repair / Computed Invariant and Upstream Receipt Separation / Negative Fixture Exclusion / Promotion Eligibility Reclassification Seal

- Parent: `ASH-TRUTH-AUDIT-01-R1`
- Patch class: truth-audit semantic repair
- Decode revision increase: not authorized
- LoRA feature revision increase: not authorized
- New governance hierarchy: not authorized
- Mass field rename: not authorized
- General production promotion: not authorized

## 1. Purpose

R1 correctly found one direct performed-claim self-attestation, but its broad source classifier mixed caller claim passthrough, computed invariants, verifier calls, upstream receipt propagation, negative fixtures, and runtime evidence into one promotion-ineligible count.

R2 must:

1. Repair only the confirmed direct performed-claim verification.
2. Classify the remaining candidates by evidence semantics.
3. Preserve governance freeze and MIN1 requirements.
4. Avoid mass mutation of unrelated crates.

## 2. Confirmed direct self-attestation

The following field used a performed claim as verification:

```rust
gpu_side_token_block_reduce_verified:
    plan.gpu_side_token_block_reduce_enabled
        && plan.token_block_reduces
            .iter()
            .all(|record| {
                record.reduce_performed_on_gpu
                    && !record.cpu_reduce_used
            })
```

Path:

```text
crates/lora_train/src/batch_parallel_vocab_tile_pass2_grad.rs
```

This expression does not read GPU submission completion, result-buffer state, or an independent numerical reference. It is reported evidence only.

## 3. Required direct repair

The receipt must separate:

```text
gpu_side_token_block_reduce_reported
gpu_side_token_block_reduce_observed
gpu_side_token_block_reduce_parity_verified
```

The performed-record expression may populate only `reported`.

Until runtime-owned physical evidence and an independent comparator are bound:

```text
gpu_side_token_block_reduce_reported=<performed claim>
gpu_side_token_block_reduce_observed=false
gpu_side_token_block_reduce_parity_verified=false
gpu_side_token_block_reduce_verified=false
evidence_level=Reported
independent_reference_used=false
promotion_authority=false
```

The old `gpu_side_token_block_reduce_verified` field may remain only as a fail-closed compatibility field.

## 4. Semantic evidence classes

### DirectPerformedClaim

A performed flag contributes directly to a verified result.

```text
promotion_eligible=false
requires_repair=true
```

### DirectVerifiedPassthrough

An upstream verified field is copied or combined without a new independent comparison.

```text
lineage_only=true
new_independent_verification=false
promotion_eligible=false
requires_semantic_rename=true
```

### ComputedInvariant

A structural rule is calculated from input or plan state.

Examples include lease validity, positive dimensions, enabled axes, or non-empty plan records.

```text
not self-attested
not physical execution verification
promotion_eligible=false as physical proof
```

### IndependentVerifierInvocation

A verifier-like function is called. The verifier body must be audited before it can be promoted to a comparator.

```text
requires_manual_review=true
promotion_eligible=false until provenance is established
```

### RuntimeObservation

Runtime-owned evidence shows execution or a physical state transition.

```text
evidence_level=Observed
physical_execution_evidence=true
independent_correctness_verification=false
```

### IndependentComparator

A physical result is compared with an independent expected result under an explicit rule.

```text
evidence_level=Verified
independent_reference=true
promotion_eligible=true
```

### NegativeFixtureMutation

A negative test deliberately changes a verified field to false or corrupts a receipt.

```text
negative_fixture=true
requires_repair=false
promotion_relevance=false
```

### UnknownRequiresReview

Static inspection cannot determine evidence provenance.

```text
requires_manual_review=true
promotion_eligible=false
automatic_repair=false
```

## 5. Classification precedence

```text
1. NegativeFixtureMutation
2. DirectPerformedClaim
3. DirectVerifiedPassthrough
4. IndependentComparator
5. RuntimeObservation
6. IndependentVerifierInvocation
7. ComputedInvariant
8. UnknownRequiresReview
```

A negative fixture assignment must not be counted as false verification merely because it contains a verified field name.

## 6. Context requirements

The audit must record at least:

```text
path
line
function
field
source_text
semantic_class
evidence_level
physical_execution_evidence
independent_reference
new_independent_verification
lineage_only
negative_fixture
promotion_eligible
requires_repair
requires_semantic_rename
requires_manual_review
reason
```

Test-like context includes explicit tests, test directories, negative matrices, fixtures, corruption helpers, and tamper helpers. A test context is not automatically excluded; only deliberate negative-state mutation receives `NegativeFixtureMutation`.

## 7. Audit artifact V2

Canonical artifact:

```text
workspace/runtime/truth_audit/ash_truth_audit_01_r2_runtime_artifact.json
```

Schema:

```text
ash.truth_audit.01.r2.runtime_artifact.v2
```

Required counters:

```text
direct_performed_claim_count
direct_verified_passthrough_count
computed_invariant_count
independent_verifier_invocation_count
runtime_observation_count
independent_comparator_count
negative_fixture_mutation_count
unknown_requires_review_count
confirmed_false_verification_count
lineage_only_verification_count
structural_invariant_count
physical_observation_count
independent_physical_verification_count
```

The R1 mixed counter may remain for compatibility only with:

```text
deprecated=true
mixed_semantics=true
promotion_authority=false
```

## 8. Promotion rules

The following are not independent physical verification authority:

```text
DirectPerformedClaim
DirectVerifiedPassthrough
ComputedInvariant
IndependentVerifierInvocation
RuntimeObservation
NegativeFixtureMutation
UnknownRequiresReview
```

Only `IndependentComparator` may provide new independent verification authority, and only when:

```text
observed_execution_count > 0
verified_result_count > 0
independent_reference=true
comparison_rule_present=true
```

Zero direct performed claims with zero independent comparators is not physical-proof PASS.

## 9. LoRA triage order

1. Repair `gpu_side_token_block_reduce_verified` as reported-only.
2. Classify planner-state names such as dispatch, axis, grid, and cache-key verification as structural invariants.
3. Review caller-provided dispatch-count provenance before calling it observed.
4. Rename non-zero delta checks as observation unless reference parity exists.
5. Do not mass-edit base-train or tokenizer fields in this patch.

## 10. Static tests

The classifier must distinguish:

```text
verified: plan.reduce_performed_on_gpu
→ DirectPerformedClaim

verified: input.upstream_verified
→ DirectVerifiedPassthrough

verified: lease.active && !lease.expired && lease.expires_at > requested_at
→ ComputedInvariant

verified: validate_artifact_paths(...)
→ IndependentVerifierInvocation

receipt.some_verified = false in negative fixture
→ NegativeFixtureMutation

verified: compare_gpu_and_reference(...)
→ IndependentComparator
```

## 11. PASS

R2 semantic repair PASS requires:

```text
direct_performed_claim_count=0
confirmed direct performed claim repaired
negative fixture mutation classified separately
computed invariants not counted as self-attestation
upstream verified propagation marked lineage-only
all findings carry semantic metadata
automatic mass rename count=0
automatic cross-crate mutation count=0
new governance hierarchy count=0
```

## 12. HOLD

HOLD remains valid when:

```text
unknown_requires_review_count > 0
independent verifier body review is pending
LoRA MIN1 is missing
Decode MIN1 is missing
```

HOLD must not synthesize verified authority.

## 13. FAIL

FAIL conditions include:

```text
performed claim still emits verified=true
negative fixture counted as false authority
computed invariant automatically downgraded to caller report
upstream passthrough treated as a new independent verification
caller-owned count treated as runtime observation
unknown candidate silently promoted
mixed candidates mass-renamed without semantic review
```

## 14. Governance freeze

R2 does not authorize a new gate family, receipt hierarchy, manifest authority chain, decode revision suffix, or LoRA feature revision.

Allowed work is limited to:

```text
truth classifier correction
confirmed self-attestation repair
field semantic separation
LoRA MIN1 physical proof
Decode MIN1 physical proof
```

## 15. Canonical seal

```text
Reading an input is not self-attestation.
Copying an input claim into a verification result is self-attestation.
Computing an invariant from input state is structural validation,
not physical execution verification.
Propagating an upstream verified field is lineage,
not a new independent verification.
Mutating a verified field to false inside a negative fixture
is test construction, not false authority.
Only a runtime-owned physical result compared against an independent
expected result may create new verification authority.
The audit must distinguish these meanings before it repairs code.
```
