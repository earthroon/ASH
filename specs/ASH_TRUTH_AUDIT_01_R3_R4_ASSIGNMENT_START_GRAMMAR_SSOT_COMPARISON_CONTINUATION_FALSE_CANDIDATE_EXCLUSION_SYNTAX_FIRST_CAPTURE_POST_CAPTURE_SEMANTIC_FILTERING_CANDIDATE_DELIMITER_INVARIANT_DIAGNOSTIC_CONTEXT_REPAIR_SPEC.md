# ASH-TRUTH-AUDIT-01-R3-R4

## Assignment-Start Grammar SSOT / Comparison Continuation False-Candidate Exclusion / Syntax-First Capture and Post-Capture Semantic Filtering / Candidate-Delimiter Invariant and Diagnostic Context Repair

## 0. Metadata

- Patch ID: `ASH-TRUTH-AUDIT-01-R3-R4`
- Parent: `ASH-TRUTH-AUDIT-01-R3-R3`
- Runtime binary: `crates/lora_train/src/bin/ash_truth_audit_01_r3.rs`
- Runtime schema: `ash.truth_audit.01.r3.runtime_artifact.v1`
- Runtime artifact: `workspace/runtime/truth_audit/ash_truth_audit_01_r3_runtime_artifact.json`
- Failure class: assignment-candidate and delimiter-authority split
- Claim deletion or claim-ID rewrite: forbidden
- Direct repository PASS override: forbidden
- LoRA and Decode physical-proof changes: forbidden
- Atlas top-level field changes: forbidden

## 1. Confirmed failure

The R3-R3 binary exits before repository predicate evaluation:

```text
Error: assignment candidate has no assignment delimiter
```

The failure state is:

```text
is_assignment_candidate(line) == true
assignment_delimiter(line) == None
```

A scanner entry state accepted by one function is rejected by another function.
This is an SSOT violation.

## 2. Confirmed false-candidate mechanism

The old candidate detector uses substring matching:

```text
trimmed.contains("_verified =")
```

A comparison such as:

```rust
execution.source_plus_delta_verified == Some(true)
```

contains the substring `_verified =` because the first character of `==` matches the suffix.

The delimiter parser correctly rejects `==`, producing the fatal split state.

## 3. Confirmed comparison-continuation fixtures

The following lines are not assignment starts:

```text
crates/model_core/src/runtime_lora.rs:4966
&& execution.source_plus_delta_verified == Some(true)

crates/lora_train/src/native_e2e_step.rs:879
commit.commit_readback_verified == Some(true)

crates/lora_train/src/native_e2e_step.rs:880
&& commit.source_plus_delta_verified == Some(true)

crates/lora_train/src/native_e2e_step.rs:883
.unwrap_or(execution.commit_readback_verified == Some(true));

crates/lora_train/src/runtime_health.rs:1370
&& value.commit_readback_verified == Some(true)

crates/lora_train/src/runtime_health.rs:1371
&& value.source_plus_delta_verified == Some(true)
```

They belong to enclosing assignments and must never create independent claim IDs.

## 4. Enclosing assignment starts

The enclosing semantic assignments begin at:

```text
crates/model_core/src/runtime_lora.rs:4965
commit_execution_validated: ...

crates/lora_train/src/native_e2e_step.rs:877
let commit_execution_validated = ...

crates/lora_train/src/runtime_health.rs:1367
let validated = ...
```

Their destination names do not necessarily contain `_verified`.
The scanner must identify them through assignment grammar and the broader verified/validated target contract.

## 5. Authority chain

Required order:

```text
physical source line
-> function and lexical context
-> assignment-start grammar
-> target-based capture admission
-> complete RHS capture
-> post-capture semantic classification
-> provenance classification
-> requiredness policy
-> repository predicate verdict
```

Forbidden order:

```text
semantic substring
-> candidate=true
-> delimiter rediscovery
-> capture
```

## 6. AssignmentStart SSOT

Introduce:

```rust
struct AssignmentStart {
    kind: AssignmentStartKind,
    delimiter_kind: AssignmentDelimiterKind,
    delimiter_index: usize,
    lhs_source: String,
    target_symbol: String,
    source_line: usize,
}
```

An accepted assignment start owns:

```text
assignment kind
delimiter kind
delimiter byte index
left-hand source
target identity
source line
```

Capture, RHS extraction and claim field identity reuse this object.
No later phase rediscovers the delimiter.

## 7. Assignment kinds

```text
LetBinding
LocalAssignment
StructFieldInitializer
```

Required recognized forms:

```rust
let verified = expression;
let mut verified = expression;
let verified: bool = expression;
verified = expression;
self.verified = expression;
verified: expression,
```

## 8. Delimiter kinds

```text
Equals
FieldColon
```

A typed let binding uses `=` as the assignment delimiter:

```rust
let verified: bool = expression;
```

The type annotation colon is not field-initializer authority.

## 9. Comparison and operator exclusions

The assignment-start grammar explicitly rejects:

```text
==
!=
<=
>=
=>
+=
-=
*=
/=
%=
&=
|=
^=
```

Comparison-only lines return:

```text
Ok(None)
```

They do not produce an error.

## 10. Continuation-prefix exclusion

The following line prefixes cannot open assignment capture:

```text
&&
||
.
)
]
,
?
+
-
*
/
%
==
!=
<=
>=
```

A colon is accepted only after a valid identifier LHS.

## 11. LHS grammar

Simple identifiers follow:

```text
[A-Za-z_][A-Za-z0-9_]*
```

Raw identifiers using `r#` are accepted.

Local assignment paths may use:

```text
identifier(.identifier)*
```

Forbidden LHS forms include:

```text
quoted strings
numeric literals
leading operators
function calls
macro invocations
labels
match arms
paths containing `::`
```

## 12. Function-body scope

Assignment scanning operates only in an active function body.

The source prepass records per-line:

```text
function name
function scope ID
function-body active state
line-start lexical code state
```

Function-local symbol tables are cleared when the scope ID changes.

## 13. Lexical line-start state

Lines beginning inside any of the following are not code assignment starts:

```text
block comments
ordinary strings
character literals
raw strings
```

This prevents embedded report templates such as:

```text
parity_pass = {}
```

inside raw strings from becoming source claims.

The lexical state persists across physical lines.

## 14. Syntax-first capture admission

Every physical line is first evaluated by `detect_assignment_start()`.

Only a valid `AssignmentStart` may proceed to capture admission.

Capture admission is target-owned and includes:

```text
verified
*_verified
validated
*_validated
*parity_pass*
*performed_on_gpu*
explicit registered verifier invocation surfaces
```

This admission is not final evidence classification.
It limits report-audit capture scope after syntax has already established a real assignment.

## 15. Post-capture semantic filtering

Final semantic relevance is evaluated only from a complete `CapturedExpression`.

The final filter may inspect:

```text
target identity
complete RHS
negative-fixture context
explicit verifier provenance
local symbol provenance
configuration source authority
```

Comparison continuations cannot reach this phase because they have no `AssignmentStart`.

## 16. CapturedExpression contract

```rust
struct CapturedExpression {
    start_line: usize,
    end_line: usize,
    source_text: String,
    rhs: String,
    target_symbol: String,
    assignment_kind: AssignmentStartKind,
    delimiter_kind: AssignmentDelimiterKind,
    multiline: bool,
    terminated: bool,
    delimiter_balance_pass: bool,
}
```

The target symbol is copied from `AssignmentStart`.
It is not reconstructed from source text.

## 17. Capture termination

For equals assignments:

```text
top-level semicolon
```

For struct-field initializers:

```text
top-level comma
```

Capture tracks:

```text
parentheses
brackets
braces
line comments
nested block comments
ordinary strings
character literals
raw strings
```

Maximum capture span remains 256 physical lines.

## 18. Nested expression handling

Capture must tolerate:

```text
closures
match expressions
function calls
nested arrays
nested structs
comparison chains
unwrap_or expressions
```

Internal comparison lines remain part of the enclosing assignment.
They are not standalone assignments.

## 19. Delimiter invariant

The state:

```text
accepted assignment start without a delimiter
```

is structurally impossible because `AssignmentStart` contains the delimiter.

`capture_assignment()` validates that the stored delimiter still exists at the stored byte index.
A mismatch is an internal invariant failure.

## 20. Diagnostic context

Replace the context-free error:

```text
assignment candidate has no assignment delimiter
```

with:

```text
truth_audit_r3_assignment_start_invariant_failed
path=<repository-relative path>
line=<physical line>
function=<function identity>
kind=<assignment kind>
lhs=<left-hand source>
delimiter=<delimiter kind>
delimiter_index=<byte index>
source=<physical source line>
```

Normal non-assignment lines never emit this error.

## 21. Scanner metrics

Required console metrics:

```text
assignment_start_detected_count
assignment_capture_admitted_count
assignment_capture_completed_count
assignment_capture_failed_count
comparison_continuation_rejected_count
comparison_continuation_capture_start_count
post_capture_semantic_candidate_count
assignment_start_invariant_failure_count
```

Expected hard invariants:

```text
comparison_continuation_capture_start_count=0
assignment_start_invariant_failure_count=0
assignment_capture_admitted_count =
    assignment_capture_completed_count + assignment_capture_failed_count
```

## 22. Required repository predicates

```text
REPO_ASSIGNMENT_START_GRAMMAR_SSOT_PASS
REPO_ASSIGNMENT_STARTS_HAVE_EMBEDDED_DELIMITERS
REPO_COMPARISON_CONTINUATIONS_NOT_CAPTURE_STARTS
REPO_CAPTURE_PRECEDES_SEMANTIC_FILTER
REPO_CAPTURED_ASSIGNMENTS_USE_START_DELIMITER_AUTHORITY
REPO_ASSIGNMENT_START_INVARIANT_FAILURE_COUNT_ZERO
```

All are blocking semantic-integrity predicates.

## 23. Existing R3-R3 preservation

R3-R4 preserves:

```text
multiline expression capture
local verified-symbol provenance
configuration-intent separation
explicit requiredness authority
exact failing-claim receipts
```

The patch repairs capture entry authority only.

## 24. Claim identity

Existing claim identities remain based on:

```text
repository-relative source path
real assignment start line
function name
target field or symbol
```

Comparison continuation lines receive no claim identity.

Recovered enclosing assignments may create deterministic claims from their true start lines.

## 25. No hardcoded source exceptions

Forbidden:

```text
path and line allowlists
`_verified ==` string guards
six-line skip tables
silent delimiter-missing continue guards
```

The six fixtures pass because of grammar, not because of identity exceptions.

## 26. Raw-string and comment exclusion

The scanner must reject assignment-like text inside:

```text
r#"..."#
"..."
/* ... */
// ...
```

This prevents report and markdown templates embedded in Rust sources from inflating evidence claims.

## 27. Positive fixtures

### Struct field initializer

```rust
commit_execution_validated:
    execution.commit_readback_verified == Some(true)
        && execution.source_plus_delta_verified == Some(true),
```

Expected:

```text
kind=StructFieldInitializer
delimiter=FieldColon
target=commit_execution_validated
terminated=true
```

### Multiline let binding

```rust
let validated = reasons.is_empty()
    && value.commit_readback_verified == Some(true);
```

Expected:

```text
kind=LetBinding
delimiter=Equals
target=validated
terminated=true
```

### Typed let binding

```rust
let verified: bool = receipt.pass;
```

Expected delimiter:

```text
Equals
```

## 28. Negative fixtures

The following produce no assignment start:

```rust
value.verified == Some(true)
value.verified != Some(false)
Some(value) => value.verified,
"verified": true,
'outer: loop {
```

A struct declaration outside a function body also produces no assignment start:

```rust
verified: bool,
```

## 29. Six-line regression seal

Each confirmed comparison continuation must satisfy:

```text
assignment_start_detected=false
capture_started=false
finding_created=false
error=false
```

The three enclosing assignments must be captured from their real start lines.

## 30. Determinism

Repeated repository scans must produce identical:

```text
assignment-start set
capture ranges
target identities
claim IDs
classification ordering
repository predicates
```

Thread or filesystem traversal order must not alter the result.

## 31. Performance boundary

Required safeguards:

```text
one source prepass for function and lexical context
one assignment-start grammar per physical line
bounded capture admission
maximum 256 lines per admitted assignment
function-local provenance maps only
no whole-repository AST graph
```

Syntax detection may inspect all code lines, but full capture is limited to admitted verification surfaces.

## 32. Atlas preservation

Required unchanged:

```text
report_atlas_group_count=11
report_atlas_lane_count=4
report_atlas_field_count=59
report_atlas_duplicate_field_count=0
report_atlas_missing_required_field_count=0
report_atlas_validation_pass=true
```

New scanner predicates remain inside the existing predicate receipt.
No new top-level report field is required.

## 33. Artifact preservation

Required unchanged:

```text
single report serialization
fixed-width digest placeholder
canonical digest verification
byte patch
readback parity
atomic promotion
prior artifact preservation on failure
```

No runtime artifact is promoted when source scanning exits with an internal invariant failure.

## 34. Physical-proof preservation

Required unchanged:

```text
lora_min1_physical_proof_pass=true
decode_min1_physical_proof_pass=true
runtime_observation_count=2
independent_comparator_count=2
independent_physical_verification_count=2
```

## 35. Static checks

```text
PATCH_ID=ASH-TRUTH-AUDIT-01-R3-R4
is_assignment_candidate absent
assignment_delimiter absent
field-name delimiter rediscovery absent
RHS delimiter rediscovery absent
detect_assignment_start present
capture_assignment receives AssignmentStart
comparison operator exclusion present
continuation-prefix exclusion present
line-start lexical code state present
post-capture semantic filter present
old context-free error absent
source-qualified invariant error present
```

## 36. Implementation scope

Only:

```text
crates/lora_train/src/bin/ash_truth_audit_01_r3.rs
```

No changes to:

```text
R2 truth audit
LoRA MIN1 producer
Decode MIN1 producer
base-train producers
runtime_lora implementation
native_e2e implementation
runtime-health implementation
optimizer
comparator
```

## 37. Compile command

```powershell
cargo check -p lora_train --bin ash_truth_audit_01_r3
```

## 38. Test command

```powershell
cargo test -p lora_train --bin ash_truth_audit_01_r3
```

## 39. Diagnostic runtime command

```powershell
cargo run --release -p lora_train --bin ash_truth_audit_01_r3 -- --repo-root . --lora-min1-artifact workspace/runtime/lora/min1/ash_lora_min1_r1_runtime_artifact.json --decode-min1-artifact workspace/runtime/tensorcube/min1/ash_tcu_decode_min1_r1_runtime_artifact.json --write-runtime-artifact --print-repository-predicate-receipt --print-claim-evidence-receipt --print-claim-promotion-receipt --print-verifier-receipt --print-repository-hold-roadmap
```

## 40. PASS-enforced runtime command

Run only after the diagnostic command reaches predicate evaluation:

```powershell
cargo run --release -p lora_train --bin ash_truth_audit_01_r3 -- --repo-root . --lora-min1-artifact workspace/runtime/lora/min1/ash_lora_min1_r1_runtime_artifact.json --decode-min1-artifact workspace/runtime/tensorcube/min1/ash_tcu_decode_min1_r1_runtime_artifact.json --write-runtime-artifact --require-pass --print-repository-predicate-receipt --print-claim-evidence-receipt
```

## 41. R3-R4 PASS conditions

```text
assignment start has one grammar SSOT
accepted starts embed delimiter authority
comparison continuations create no starts
six confirmed false candidates produce no error
three enclosing assignments are captured from real starts
raw-string assignment-like text is excluded
capture receives a prevalidated AssignmentStart
RHS and target extraction reuse start authority
semantic filtering runs after complete capture
typed let bindings use equals authority
source-qualified invariant diagnostics exist
R3-R3 classification and requiredness remain active
LoRA and Decode proofs remain accepted
Atlas validation remains passing
```

## 42. R3-R4 FAIL conditions

```text
`_verified ==` string exception used
file-line exception table used
candidate detection remains substring-first
delimiter rediscovery remains
comparison continuation creates a finding
raw-string template creates a finding
typed let colon wins over equals
normal non-assignment line produces fatal error
context-free delimiter error remains
repository PASS is directly assigned
LoRA or Decode evidence is weakened
Atlas field ownership changes silently
```

## 43. Completion definition

The patch is complete when normal repository source can no longer produce:

```text
assignment candidate has no assignment delimiter
```

The scanner must reach repository predicate evaluation with:

```text
comparison_continuation_capture_start_count=0
assignment_start_invariant_failure_count=0
```

Repository PASS remains evidence-derived.
A new legitimate HOLD is reported through named predicates rather than hidden by the scanner repair.

## 44. Canonical seal

```text
A semantic word is not a grammar.
A comparison is not an assignment.
A continuation is not a start.
A report string is not executable source.

The assignment start owns its delimiter.
Capture reuses that delimiter.
RHS extraction reuses that delimiter.
Target identity reuses that LHS.

No substring-first capture.
No delimiter rediscovery.
No comparison false candidate.
No raw-string source inflation.
No context-free scanner failure.
No file-line pardon table.

Syntax first.
Admission second.
Capture third.
Semantics fourth.
Provenance fifth.
Policy sixth.
Verdict last.
```
