# ASH-TRUTH-AUDIT-01-R3-R3

## Multiline Assignment Expression Capture / Local Verified-Symbol Provenance Resolution / Configuration Intent vs Evidence Separation / Explicit Requiredness Authority and Exact Blocking Claim Receipt Repair

## 0. Metadata

- Patch ID: `ASH-TRUTH-AUDIT-01-R3-R3`
- Parent: `ASH-TRUTH-AUDIT-01-R3-R2`
- Runtime binary: `crates/lora_train/src/bin/ash_truth_audit_01_r3.rs`
- Runtime schema: `ash.truth_audit.01.r3.runtime_artifact.v1`
- Runtime artifact: `workspace/runtime/truth_audit/ash_truth_audit_01_r3_runtime_artifact.json`
- Claim deletion or claim-ID regeneration: forbidden
- Direct repository PASS override: forbidden
- Unknown-to-required fallback: forbidden
- LoRA/Decode physical-proof changes: forbidden
- Atlas top-level field changes: forbidden

## 1. Confirmed starting state

R3-R2 correctly retires the four function-prefix verifier false positives:

```text
independent_verifier_invocation_count=0
lexical_verifier_candidate_count=4
qualified_verifier_finding_count=0
local_contract_validator_count=4
verifier_false_positive_count=4
active_repository_verifier_count=0
computed_invariant_count=35
```

The repository remains `HoldExplained` because seven source findings are classified as required `UnknownRequiresReview` claims:

```text
required_claim_count=9
required_claim_pass_count=2
required_claim_unavailable_count=7
unknown_requires_review_count=7
repository_hold_reason_ids=["HOLD_REQUIRED_CLAIM_UNMAPPED"]
```

LoRA MIN1, Decode MIN1 and Atlas report construction remain accepted:

```text
runtime_observation_count=2
independent_comparator_count=2
independent_physical_verification_count=2
lora_min1_physical_proof_pass=true
decode_min1_physical_proof_pass=true
report_atlas_group_count=11
report_atlas_lane_count=4
report_atlas_field_count=59
report_atlas_validation_pass=true
```

## 2. Seven-claim groups

### Multiline computed assignments

```text
CLAIM_SOURCE_5EF2AA09D226E516
CLAIM_SOURCE_CA8143113253BD24
CLAIM_SOURCE_1AF86387C6E10C68
```

These begin with `let recheck_verified = recheck_read` and continue through logical, identity, digest and forbidden-boundary checks before the terminating semicolon.

### Same-function local verified-symbol aliases

```text
CLAIM_SOURCE_4EB8E20100268DCD
CLAIM_SOURCE_D0327865BC4F7D89
```

These forward `g103_promotion_recheck_decision_verified`, whose dominating prior definition is itself a computed conjunction.

### Configuration intent assignments

```text
CLAIM_SOURCE_5DD4F5BF88432D1D
CLAIM_SOURCE_437D070CC9C62CDF
```

These copy `cfg.verify_zeroed_before_dispatch` and `cfg.verify_written_after_dispatch` into verified-looking receipt fields. They are verification configuration, not observed verification results.

## 3. Root causes

```text
physical-line RHS capture
local symbol provenance loss
configuration request/result conflation
destination `_verified` suffix authority
UnknownRequiresReview -> required=true fallback
failed predicate receipts containing passing required claims
```

## 4. Authority chain

```text
source file
-> function scope
-> assignment start
-> complete expression capture
-> primitive facts
-> local symbol provenance
-> configuration intent detection
-> final evidence class
-> explicit requiredness policy
-> exact predicate failure set
-> HOLD or PASS
```

## 5. Complete assignment capture

Recognized assignment forms:

```text
let NAME = EXPR;
let mut NAME = EXPR;
FIELD: EXPR,
NAME = EXPR;
self.FIELD = EXPR;
```

Capture continues until the applicable top-level terminator:

```text
`;` for statements
`,` for struct-field initializers
```

The terminator is valid only when delimiter depth is zero and the scanner is not inside a string, character, raw-string, line comment or block comment.

Maximum capture span is 256 physical lines. Incomplete capture fails closed.

Required receipt fields:

```text
expression_start_line
expression_end_line
expression_multiline
expression_terminated
expression_delimiter_balance_pass
```

Claim identity continues to use the assignment start line and field identity.

## 6. Multiline computed classification

A complete multiline expression containing deterministic logical relations such as `&&`, `||`, `==`, `!=`, negation, field reads and pure contract helpers classifies as `ComputedInvariant` when it does not claim new physical runtime execution.

Required reclassification:

```text
CLAIM_SOURCE_5EF2AA09D226E516 -> ComputedInvariant
CLAIM_SOURCE_CA8143113253BD24 -> ComputedInvariant
CLAIM_SOURCE_1AF86387C6E10C68 -> ComputedInvariant
```

Required claim state:

```text
required=false
domain=artifact_recheck_contract
current_class=ComputedInvariant
terminal_allowed=true
result=pass
```

Reason IDs:

```text
MULTILINE_ASSIGNMENT_CAPTURED
MULTILINE_LOGICAL_EXPRESSION_COMPUTED
```

## 7. Function-scoped local symbol provenance

The scanner maintains a symbol table keyed by repository-relative source path and enclosing function identity.

A definition records:

```text
symbol
source line
complete RHS
final evidence class
alias depth
```

Resolution requires a prior dominating definition in the same function with no intervening redefinition. Cross-function and cross-module name-only resolution are forbidden.

Required reclassification:

```text
CLAIM_SOURCE_4EB8E20100268DCD -> ComputedInvariant
CLAIM_SOURCE_D0327865BC4F7D89 -> ComputedInvariant
```

Required claim state:

```text
required=false
domain=promotion_decision_contract
current_class=ComputedInvariant
terminal_allowed=true
result=pass
local_symbol_alias_candidate=true
local_symbol_provenance_resolved=true
local_symbol_alias_depth=1
```

Reason IDs:

```text
LOCAL_VERIFIED_SYMBOL_PROVENANCE_RESOLVED
LOCAL_SYMBOL_ALIAS_COMPUTED_INVARIANT
```

Alias cycles and excessive depth fail closed.

## 8. Configuration intent separation

Configuration roots include:

```text
cfg.*
config.*
options.*
settings.*
policy.*
args.*
```

RHS authority has precedence over destination naming. A verified-looking destination receiving a `cfg.*` boolean remains configuration intent.

Required reclassification:

```text
CLAIM_SOURCE_5DD4F5BF88432D1D -> StructuralInvariant
CLAIM_SOURCE_437D070CC9C62CDF -> StructuralInvariant
```

Required claim state:

```text
required=false
domain=configuration_contract
current_class=StructuralInvariant
terminal_allowed=true
result=pass
configuration_intent_detected=true
configuration_source_root=cfg
```

Reason IDs:

```text
CONFIGURATION_INTENT_SOURCE_AUTHORITY
VERIFIED_DESTINATION_NOT_RUNTIME_EVIDENCE
```

## 9. Explicit requiredness authority

Requiredness is evaluated only after final evidence classification.

Authority order:

```text
explicit required claim ID
explicit optional claim ID
physical-proof policy
explicit required domain rule
qualified independent-verifier policy
default optional source-evidence policy
```

Forbidden requiredness sources:

```text
UnknownRequiresReview
field suffix
function prefix
source path keyword
classifier uncertainty
```

An unclassified source claim with no explicit policy remains visible but optional.

Expected required set:

```text
CLAIM_LORA_MIN1_PHYSICAL_PROOF
CLAIM_DECODE_MIN1_PHYSICAL_PROOF
```

Expected counts:

```text
required_claim_count=2
required_claim_pass_count=2
required_claim_unavailable_count=0
```

## 10. Exact blocking claim receipts

Repository predicate results expose:

```text
evaluated_claim_ids
failing_claim_ids
claim_ids
```

For failed predicates, `claim_ids` equals `failing_claim_ids`. Passing claims must not appear in unrelated failed predicate receipts.

Exact failure sets:

```text
REPO_NO_REQUIRED_UNKNOWN_CLAIMS
  required && UnknownRequiresReview

REPO_ALL_REQUIRED_CLAIMS_EVALUATED
  required && unavailable/not-evaluated

REPO_ALL_REQUIRED_CLAIMS_USE_ALLOWED_TERMINAL_CLASS
  required && terminal_allowed=false
```

The summary predicate, HOLD receipt and roadmap use the deduplicated union of exact blocking failure sets.

## 11. Required predicates

```text
REPO_MULTILINE_ASSIGNMENTS_CAPTURE_COMPLETE
REPO_CLASSIFIED_ASSIGNMENTS_HAVE_TERMINATED_EXPRESSIONS
REPO_LOCAL_SYMBOL_ALIASES_RESOLVED_OR_EXPLICITLY_UNKNOWN
REPO_CONFIGURATION_INTENT_NOT_RUNTIME_EVIDENCE
REPO_VERIFIED_DESTINATION_SUFFIX_NOT_AUTHORITY
REPO_CONFIGURATION_CLAIMS_OPTIONAL_UNLESS_EXPLICIT
REPO_REQUIRED_CLAIMS_HAVE_EXPLICIT_POLICY_AUTHORITY
REPO_UNKNOWN_CLASS_DOES_NOT_CREATE_REQUIREDNESS
REPO_REQUIRED_POLICY_REASON_RESOLVABLE
```

These are blocking semantic-integrity or policy predicates.

## 12. Expected aggregate recompute

```text
UnknownRequiresReview: 7 -> 0
ComputedInvariant: 35 -> 40
StructuralInvariant: 31 -> 33
independent_verifier_invocation_count=0
runtime_observation_count=2
independent_comparator_count=2
independent_physical_verification_count=2
```

Runtime remains authoritative.

## 13. Expected HOLD retirement

When no unrelated blocker appears:

```text
repository_hold_reason_count=0
repository_hold_reason_ids=[]
```

`HOLD_REQUIRED_CLAIM_UNMAPPED` is retired because the seven source claims are mapped and optional.

## 14. Expected repaired state

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
required_claim_unavailable_count=0
repository_hold_reason_count=0
repository_hold_reason_ids=[]
unknown_requires_review_count=0
all_truth_checks_pass=true
```

PASS must emerge from predicate recomputation and may not be hardcoded.

## 15. Atlas and artifact preservation

Required unchanged:

```text
report_atlas_group_count=11
report_atlas_lane_count=4
report_atlas_field_count=59
report_atlas_duplicate_field_count=0
report_atlas_missing_required_field_count=0
report_atlas_validation_pass=true
```

New fields remain nested in claim and predicate receipts. The artifact keeps the existing fixed-width digest patch, canonical digest verification, readback parity and atomic promotion contract.

## 16. Physical-proof preservation

```text
lora_min1_physical_proof_pass=true
decode_min1_physical_proof_pass=true
runtime_observation_count=2
independent_comparator_count=2
independent_physical_verification_count=2
```

## 17. Static and regression checks

```text
PATCH_ID=ASH-TRUTH-AUDIT-01-R3-R3
line-only RHS classifier path absent
complete expression capture present
function-scoped local symbol table present
local alias provenance resolution present
configuration intent detector present
destination `_verified` authority absent
UnknownRequiresReview -> required=true fallback absent
explicit requiredness reasons present
exact failing claim fields present
Atlas groups=11
Atlas fields=59
```

Stable expectations:

```text
CLAIM_SOURCE_5EF2AA09D226E516 -> ComputedInvariant
CLAIM_SOURCE_CA8143113253BD24 -> ComputedInvariant
CLAIM_SOURCE_1AF86387C6E10C68 -> ComputedInvariant
CLAIM_SOURCE_4EB8E20100268DCD -> ComputedInvariant
CLAIM_SOURCE_D0327865BC4F7D89 -> ComputedInvariant
CLAIM_SOURCE_5DD4F5BF88432D1D -> StructuralInvariant
CLAIM_SOURCE_437D070CC9C62CDF -> StructuralInvariant
```

Exact IDs are regression evidence, not classifier exceptions.

## 18. Implementation scope

```text
crates/lora_train/src/bin/ash_truth_audit_01_r3.rs
```

R2, LoRA MIN1, Decode MIN1, optimizer, comparator, base-train producer logic and GPU buffer-hygiene implementation remain unchanged.

## 19. Commands

Compile:

```powershell
cargo check -p lora_train --bin ash_truth_audit_01_r3
```

Tests:

```powershell
cargo test -p lora_train --bin ash_truth_audit_01_r3
```

Runtime:

```powershell
cargo run --release -p lora_train --bin ash_truth_audit_01_r3 -- --repo-root . --lora-min1-artifact workspace/runtime/lora/min1/ash_lora_min1_r1_runtime_artifact.json --decode-min1-artifact workspace/runtime/tensorcube/min1/ash_tcu_decode_min1_r1_runtime_artifact.json --write-runtime-artifact --print-repository-predicate-receipt --print-claim-evidence-receipt --print-claim-promotion-receipt --print-verifier-receipt --print-repository-hold-roadmap
```

## 20. PASS conditions

```text
multiline expressions captured to syntax completion
logical-chain claims classified from complete RHS
local aliases resolved in function scope
configuration intent separated from runtime evidence
RHS authority overrides destination suffix
unknown does not create requiredness
required claims have explicit policy reasons
seven claim IDs remain stable
five become ComputedInvariant
two become StructuralInvariant
all seven become optional
failed predicate claim lists are exact
LoRA/Decode proofs remain accepted
Atlas report remains valid
repository verdict is recomputed normally
```

## 21. FAIL conditions

```text
hardcoded seven-ID classifier exceptions
source finding deletion
line-oriented truncation remains
alias crosses function boundaries
configuration request becomes runtime proof
`_verified` suffix determines evidence authority
unknown fallback marks source claims required
passing claims appear in failure sets
repository PASS is assigned directly
LoRA/Decode evidence is weakened
Atlas ownership drifts silently
```

## 22. Canonical seal

```text
A line is not an expression.
An assignment ends when its syntax ends.
A local symbol has provenance.
A configuration flag requests evidence; it is not the evidence it requests.
A destination named verified does not make its source verified.
Unknown is classification uncertainty, not policy authority.
Requiredness belongs to policy.
Failure receipts belong only to claims that failed.

Capture the whole expression.
Resolve the local source.
Respect the RHS authority.
Consult the explicit policy.
Report the exact blockers.
Derive the verdict last.
```
