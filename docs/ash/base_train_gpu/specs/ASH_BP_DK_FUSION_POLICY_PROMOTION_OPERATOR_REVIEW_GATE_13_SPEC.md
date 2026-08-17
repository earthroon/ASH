# ASH-BP-DK-FUSION-POLICY-PROMOTION-OPERATOR-REVIEW-GATE-13

## Status

```text
Patch ID: ASH-BP-DK-FUSION-POLICY-PROMOTION-OPERATOR-REVIEW-GATE-13
Direct parent: ASH-BP-DK-FUSION-POLICY-CALIBRATION-RECOMMENDATION-12
Purpose: human/operator-owned review gate for immutable 12 policy recommendations

13 authority:
operator review decision + qualification-ticket issuance only

13 is NOT:
production policy activation
active-pointer mutation
hot reload
planner mutation
candidate replay
recommendation recomputation
training commit authority
```

Current source status after this bake:

```text
13_OPERATOR_REVIEW_SOURCE_PATH_WIRED
13_IMMUTABLE_REVIEW_RECEIPT_WIRED
13_QUALIFICATION_TICKET_WIRED
13_STATIC_SOURCE_CONTRACT_CLOSED
12_AND_05_PARENT_SOURCES_BYTE_PRESERVED
PRODUCTION_POLICY_ACTIVATION_NOT_GRANTED
USER_LOCAL_RUST_EXECUTION_UNVERIFIED
```

---

## 1. Authority separation

The policy lineage is now explicitly separated into four authorities:

```text
05
= current production Fusion/Fission policy and planner semantics

12
= non-authoritative evidence-backed candidate recommendation

13
= explicit human/operator review decision

14
= candidate qualification / canary authority

15
= future explicit production activation authority
```

An operator decision of:

```text
AcceptForQualification
```

means only:

```text
this exact candidate may be handed to 14 for qualification
```

It does **not** mean:

```text
activate this candidate in production
```

13 does not write the active 05 policy, policy pointer, checkpoint policy state, or planner state.

---

## 2. Direct-parent preservation

13 is an offline review layer. The 12 recommendation implementation and the 05 production planner remain byte-preserved.

Validated parent anchors:

```text
12 core
8ec7bf2908153124af6af5392dd9f8f90a32847e07d5bba69b6bdde69ac5730a

12 base
73c06d8259d04c4ba199f77305e48a346eb81c4a83fca15ee616739043f23944

12 offline recommendation binary
c695093b811649419be3c97aafee792343a23656e4af1d67f988fbeb8ce561a9

05 planner core
53a51cf384e60c5d17d6259081339b1703a90e3da5c14cf75b8d0ecfd9ab2897

05 planner base
70e6d4f08e89d4693c1999ff4508ec09ad4fcfe9850e2bb914127702f5f618cc
```

13 introduces no production callsite adoption and no 05 planner replay execution.

---

## 3. Immutable 12 recommendation admission

The primary review input is the exact:

```text
AshBpDkFusionCalibrationRecommendation
```

13 revalidates it with the exact 12 recommendation guard used to seal it.

Required:

```text
recommendation schema valid
recommendation digest valid
recommendation-policy digest valid
12 authority-leak counters = 0
candidate digest valid when candidate exists
```

13 does not trust a text label saying the recommendation was previously validated.

---

## 4. Exact source-policy snapshot is required

13 requires two policy inputs:

```text
source policy snapshot
current production policy
```

They serve different purposes.

### Source policy snapshot

The source policy is the exact 05 policy that 12 used to generate the recommendation.

Required:

```text
source_policy.canonical_digest()
== recommendation.source_policy_digest

source_policy.revision
== recommendation.source_policy_revision
```

The source snapshot is necessary because the 12 receipt contains the source digest/revision but does not embed the complete source policy object. Exact hidden-field diff verification cannot be honestly performed from a digest alone.

### Current production policy

The current policy is read independently at review time and is used for freshness.

```text
current_policy_digest
== recommendation.source_policy_digest
```

is required for an Accept decision.

If production policy has changed since recommendation creation:

```text
freshness = SourcePolicyChanged
```

and Accept is forbidden.

13 never rebases an old recommendation diff onto a newer current policy.

---

## 5. Exact candidate-policy diff verification

For `CandidateRecommended`, 13 compares all eleven semantic 05 policy controls between the exact source policy and candidate policy:

```text
fuse_cosine_min
fuse_information_max
fuse_material_min
fuse_delta_k_max
fuse_confirm_generations

fission_cosine_floor
fission_information_min
fission_material_floor
fission_delta_k_min
fission_confirm_generations

cooldown_generations
```

The actual semantic diff must exactly equal:

```text
recommendation.proposed_changes
```

For numeric fields, exact F32 bit identity is used for old/new values.

For integer fields, exact integer identity is used.

Hidden semantic changes cause:

```text
ASH_BP_DK_FUSION_OPERATOR_REVIEW_HIDDEN_POLICY_DIFF
```

No unrelated field may change silently.

The candidate revision is expected to be explicitly bumped relative to the source revision.

---

## 6. Canonical 05 candidate validation is reused

13 reruns:

```text
AshBpDkFusionFissionPolicy::validate()
```

and candidate canonical digest verification.

It does not define a new hysteresis validator.

12 validity is not treated as a substitute for the 13 trust-boundary validation.

---

## 7. R1 supported recommendation scope

The 12 R1 automatic recommendation authority is intentionally conservative. Therefore 13 R1 accepts qualification candidates only for the currently supported automatic candidate kinds:

```text
IncreaseFusionConfirmation
IncreaseCooldown
```

Exact shape requirements:

```text
IncreaseFusionConfirmation
-> exactly one FuseConfirmGenerations positive integer change

IncreaseCooldown
-> exactly one CooldownGenerations positive integer change
```

An externally constructed CandidateRecommended receipt containing an unsupported R1 recommendation scope cannot be accepted.

If such a structurally sealed recommendation is reviewed, R1 permits only an explicit Reject outcome.

13 does not use whole-step objective context to invent an unsupported cosine/I/M/DeltaK field adjustment.

---

## 8. Operator decision authority

13 defines:

```text
AcceptForQualification
Reject
Defer
RequestMoreEvidence
AcknowledgeKeepCurrent
```

There is no autonomous decision function that converts confidence, objective direction, replay exposure, or reason codes directly into acceptance.

No default decision exists.

No timeout acceptance exists.

No `--yes`, `--force`, or ignore-validation bypass exists in R1.

---

## 9. Status admission matrix

The 12 recommendation status constrains which operator decisions are semantically legal.

```text
CandidateRecommended
  -> AcceptForQualification / Reject / Defer / RequestMoreEvidence

KeepCurrentPolicy
  -> AcknowledgeKeepCurrent / Defer / RequestMoreEvidence

ReviewRequired
  -> Reject / Defer / RequestMoreEvidence

ConflictingEvidence
  -> Reject / Defer / RequestMoreEvidence

InsufficientEvidence
  -> Defer / RequestMoreEvidence

InsufficientReplayEvidence
  -> Defer / RequestMoreEvidence

CurrentReplayMismatch
  -> Reject / RequestMoreEvidence

CandidateInvalid
  -> Reject
```

Therefore these statuses can never produce an Accept ticket in R1:

```text
InsufficientEvidence
InsufficientReplayEvidence
ReviewRequired
ConflictingEvidence
CurrentReplayMismatch
CandidateInvalid
```

Structural evidence failure is not an operator override surface.

---

## 10. Review freshness

13 computes a typed freshness state:

```text
Current
EvidenceAdvanced
SourcePolicyChanged
Superseded
Invalid
```

Freshness is digest-based, not file modification-time based.

### SourcePolicyChanged

```text
current 05 policy digest
!= recommendation source-policy digest
```

### Superseded

A supplied latest recommendation from the same source-policy / trajectory-segment lineage has a different recommendation digest.

### EvidenceAdvanced

The latest committed evidence heads differ from the exact heads used by 12:

```text
latest 11 trajectory head
!= recommendation.trajectory_head_digest

or

latest 12 replay-evidence head
!= recommendation.replay_head_digest
```

### Current

Source policy, latest recommendation lineage, and evidence heads all remain exact.

---

## 11. R1 Accept requires fully current freshness

`AcceptForQualification` requires:

```text
freshness == Current
```

R1 does not permit stale-source, evidence-advanced, or superseded recommendations to reach 14.

If evidence advanced after recommendation generation, operator may still Reject or Defer where allowed, but qualification requires a fresh 12 recommendation from the latest evidence.

---

## 12. Latest recommendation requirement

The default 13 review policy requires an explicit latest-recommendation input for Accept.

It must belong to the same:

```text
source policy digest
trajectory segment digest
```

and its recommendation digest must equal the recommendation under review.

Passing an unrelated recommendation merely to satisfy the presence check is not accepted.

---

## 13. Review safety policy

13 owns a workflow safety policy independent from 05:

```text
AshFusionPolicyOperatorReviewPolicy
```

R1 fields include:

```text
revision
minimum Accept confidence
require latest evidence
require latest recommendation
allowed qualification scopes
```

R1 defaults:

```text
minimum Accept confidence = Supported
require latest evidence = true
require latest recommendation = true
```

R1 validation does not permit those freshness requirements to be disabled and does not permit the minimum confidence to be lowered to:

```text
Insufficient
Exploratory
```

This prevents a custom review-policy JSON from silently weakening the R1 admission floor.

---

## 14. Confidence admission

By default, qualification acceptance requires:

```text
Supported
or
StronglySupported
```

`Exploratory` evidence may be Reject/Defer/MoreEvidence according to the 12 status, but it cannot be accepted into 14 under the R1 review policy.

---

## 15. Qualification scope is explicit

Accept requires an explicit scope:

```text
OfflineReplayQualification
ShadowCanary
BoundedTrainingCanary
```

The CLI has no default qualification scope.

An Accept decision without an explicit allowed scope fails.

13 does not decide which canary class should be used by guessing from recommendation strength.

---

## 16. Operator identity boundary

13 records:

```text
operator_id
authority_domain
```

through:

```text
AshFusionPolicyOperatorIdentity
```

These fields bind the enclosing operator-system identity supplied to the review command.

13 does **not** claim legal identity verification or cryptographic human signature unless a separate authentication/signing layer is introduced later.

Accept requires a non-empty operator identity, and R1 requires operator identity for every recorded review decision for audit consistency.

---

## 17. Structured operator reasons

Review receipts bind explicit operator review reasons such as:

```text
EvidenceAccepted
EvidenceInsufficient
ConflictingEvidence
CandidateTooAggressive
CandidateScopeTooBroad
ReplayExposureConcern
RequiresLongerCanary
SourcePolicyStale
RecommendationSuperseded
StructuralInvalidity
Other
```

At least one operator reason is required.

The optional prose note is not semantic decision authority. Only its SHA-256 digest is stored in the canonical receipt.

---

## 18. RequestMoreEvidence domains

`RequestMoreEvidence` requires one or more typed evidence requests:

```text
MoreReplayGenerations
MoreObjectiveQualifiedSamples
MoreLongHorizonSamples
ResolveConflictingEvidence
```

Duplicate request domains are rejected.

Other decisions must not carry requested-evidence domains.

13 does not automatically change 10/11/12 runtime modes after a MoreEvidence decision. The operator remains responsible for the next run configuration.

---

## 19. Immutable review receipt

Every successful review decision produces:

```text
AshBpDkFusionPolicyOperatorReviewReceipt
```

It binds:

```text
recommendation digest
source policy digest
current policy digest
optional candidate policy digest
12 recommendation status/confidence
12 evidence sufficiency
12 reason codes
12 current/candidate replay exposure summaries
freshness state
13 review-policy digest
operator identity
explicit decision
operator reasons
requested evidence domains
optional qualification scope
optional note digest
review sequence
previous review digest
authority-leak counters
decision digest
```

The receipt digest is canonical and excludes its own digest field while sealing.

---

## 20. Review lineage

13 supports explicit review lineage:

```text
review_sequence
previous_review_digest
```

A first review has:

```text
review_sequence = 1
previous_review_digest = none
```

A subsequent review must provide and validate the prior receipt for the same recommendation lineage and increments the sequence.

Existing review files are never overwritten with different bytes.

---

## 21. Accept side effect is qualification ticket only

An accepted review produces exactly one additional derived artifact:

```text
AshBpDkFusionPolicyQualificationTicket
```

The ticket binds:

```text
recommendation digest
13 review-receipt digest
source policy digest
candidate policy digest
exact candidate policy
operator identity
qualification scope
ticket digest
```

The ticket contains no `ApprovedForProduction` or equivalent authority field.

It is a 14 admission ticket only.

---

## 22. Non-Accept side effects

```text
Reject
Defer
RequestMoreEvidence
AcknowledgeKeepCurrent
```

produce an immutable review receipt only.

They do not produce a qualification ticket.

---

## 23. Immutable artifact layout

13 writes derived evidence under the operator-selected output root:

```text
<output-root>/
  reviews/
    <recommendation-digest>/
      review-<decision-digest>.json

  qualification-tickets/
    <candidate-policy-digest>/
      ticket-<ticket-digest>.json
```

Writes are collision-safe:

```text
existing identical bytes -> idempotent success
existing different bytes -> fail closed
```

The recommendation input, source/current policy files, training checkpoint, and production active pointer are not modified.

---

## 24. Read-only witnesses

The 13 offline binary records pre-run file digests and verifies after output generation that these inputs remain unchanged:

```text
12 recommendation file
source-policy snapshot file
current production policy file
```

If an optional active-policy pointer path is supplied, its pre/post file digest must also remain identical.

This is a physical file-level read-only witness around the operator review process.

---

## 25. No recommendation recomputation

13 does not call:

```text
build_policy_calibration_recommendation()
```

and does not execute 12 candidate generation again.

The exact immutable recommendation is the review target.

---

## 26. No candidate replay

13 does not call the 05 planner runtime and does not replay current/candidate policies.

The historical decision-exposure summaries already sealed by 12 are review evidence.

Additional replay belongs to a new 12 recommendation or later qualification stage, not to the human decision boundary.

---

## 27. No objective prediction

13 schema and implementation contain no:

```text
predicted candidate objective
predicted candidate loss
expected training improvement
expected accuracy gain
```

10 whole-step objective context remains observational upstream evidence only.

---

## 28. Zero physical/model authority

13 adds zero:

```text
GPU dispatch
model forward
backward
gradient access
gradient D2H
Local Muon execution
Fused Muon execution
```

The review telemetry hard-zero surface includes:

```text
policy_mutation_count = 0
active_pointer_mutation_count = 0
hot_reload_count = 0
planner_mutation_count = 0

gpu_dispatch_count = 0
forward_count = 0
backward_count = 0
gradient_access_count = 0
muon_execution_count = 0
```

---

## 29. Offline binary

13 adds:

```text
crates/base_train/src/bin/
ash_bp_dk_fusion_policy_operator_review_gate_13.rs
```

Required review inputs include:

```text
--recommendation
--source-policy
--current-policy
--latest-checkpoint
--operator-id
--decision
--reason
--output-root
```

For Accept under the default R1 review policy, also supply:

```text
--latest-recommendation
--qualification-scope
```

Optional inputs include:

```text
--recommendation-policy
--review-policy
--previous-review
--active-policy-pointer
--request-evidence
--note
```

There is no `--yes` or `--force` acceptance shortcut.

---

## 30. Runner

13 adds:

```text
tools/run_ash_bp_dk_fusion_policy_operator_review_gate_13.ps1
```

The runner assumes the overlay has already been applied.

It performs:

```text
13 static validator
cargo fmt --check
cargo check -p base_train --bin ash_bp_dk_fusion_policy_operator_review_gate_13
explicit review binary execution
```

The runner performs no `Expand-Archive` and no overlay discovery/application.

---

## 31. Changed files

The 13 overlay contains exactly eight files:

```text
crates/ash_core/src/fusion_policy_operator_review_gate.rs
crates/ash_core/src/lib.rs
crates/base_train/src/bin/ash_bp_dk_fusion_policy_operator_review_gate_13.rs
crates/base_train/src/bp_delta_k_fusion_policy_operator_review_gate.rs
crates/base_train/src/lib.rs
tools/run_ash_bp_dk_fusion_policy_operator_review_gate_13.ps1
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
tools/validate_ash_bp_dk_fusion_policy_operator_review_gate_13_static.py
```

No production TensorCube/Muon callsite file is changed.

No 05 or 12 implementation file is changed.

---

## 32. New source anchors

```text
13 core
4bf4b117cb60176a04d8746a579360f941259d823792cf55049eb7bf48977644

13 base
632d20e6e041200db6e41c98cd899e1ccc65023ae36758aa07e03519a19a5ba8

13 offline review binary
7517d5642c25683db445f239cb28edb750e69e7c1991b96018e43bccc88b5286
```

---

## 33. Static validation

New gate:

```text
validate_ash_bp_dk_fusion_policy_operator_review_gate_13_static.py
247/247 PASS
```

The 13 gate validates:

```text
12 direct-parent byte anchors
05 planner byte anchors
immutable recommendation input
source/current policy separation
exact eleven-field semantic diff verification
candidate digest verification
canonical 05 policy validation
status admission matrix
strict current freshness for Accept
latest recommendation requirement
Supported-or-stronger confidence floor
explicit qualification scope
operator identity and explicit decision
review lineage
immutable receipt/ticket outputs
no recommendation recomputation
no 05 replay
no production callsite wiring
no policy/pointer/planner mutation
no GPU/forward/backward/gradient/Muon execution
12 -> 13 CF1 order
```

---

## 34. Parent regression

After the 13 bake, the BP-DeltaK static lineage was rerun through 12 and remained PASS.

Key counted gates include:

```text
01 Local BP-DK                                  134/134 PASS
02 Generation/Revision/Stale Seal               243/243 PASS
03A Bridge Pair Evidence                        148/148 PASS
05 Active Fusion/Fission Planner                293/293 PASS
06 Deterministic Replay                         210/210 PASS
07 POST Update Ledger                           206/206 PASS
08A Physical Qualification                      236/236 PASS
08B Same-Source Local Counterfactual            221/221 PASS
08B-R1 Physical Counterfactual                  146/146 PASS
09 Counterfactual Effect Ledger                 148/148 PASS
10 One-Step Objective Probe                     259/259 PASS
11 Long-Horizon Trajectory                      145/145 PASS
12 Policy Calibration Recommendation            227/227 PASS
13 Operator Review Gate                         247/247 PASS
```

The Local Muon lineage also remained PASS, including:

```text
optimizer                                         101/101 PASS
FirstCandidate registry                            97/97 PASS
multi-tile batch                                   PASS
production callsite                                PASS
canonical-loader repair                            PASS
ExactSubgroup32 norm                               PASS
X PAD17                                            PASS
generation-sealed immutable cache                  66/66 PASS
immutable-cache backend rebind                     35/35 PASS
```

---

## 35. CF1 wiring

13 is appended after 12:

```text
$AllValidators += $BpDkFusionPolicyCalibrationRecommendation12Validator
$AllValidators += $BpDkFusionPolicyOperatorReviewGate13Validator
```

Earlier validator-chain semantics are preserved.

---

## 36. Packaging

Delivered 13 artifacts:

```text
full-body bake
18,590,810 bytes
7,161 files
ZIP integrity PASS

overlay bake
36,298 bytes
exactly 8 files
ZIP integrity PASS
```

Both archives contain zero:

```text
target/
__pycache__/
*.sha256
generated artifacts/
generated reports/
generated manifests/
```

Generated review receipts and qualification tickets are intentionally not included in the bake because they must be produced by the user's actual review decision.

---

## 37. Bake-environment boundary

The bake environment does not provide:

```text
cargo
rustc
rustfmt
physical WGPU runtime
```

Therefore this bake does not claim:

```text
Rust compilation success
actual operator review execution
actual immutable review receipt generation
actual qualification ticket generation
actual active-pointer witness on the user's environment
14 canary qualification
production activation
```

The current evidence level is:

```text
source wired
static contract closed
physical/user-local execution unverified
```

---

## 38. Required user-local gates

Before promoting 13 runtime status:

```text
cargo fmt --check
cargo check -p base_train --bin ash_bp_dk_fusion_policy_operator_review_gate_13
CF1 reaches 13
```

Then exercise at minimum:

```text
valid CandidateRecommended -> AcceptForQualification
valid CandidateRecommended -> Reject
valid CandidateRecommended -> Defer
RequestMoreEvidence
KeepCurrent -> AcknowledgeKeepCurrent

InsufficientEvidence cannot Accept
InsufficientReplayEvidence cannot Accept
CurrentReplayMismatch cannot Accept
CandidateInvalid cannot Accept
ReviewRequired cannot Accept
ConflictingEvidence cannot Accept

candidate digest tamper
hidden policy field mutation
source policy changed since recommendation
evidence advanced since recommendation
superseded recommendation
Exploratory confidence
missing qualification scope
unsupported R1 recommendation scope

review receipt immutability
review sequence linkage
source/current policy file pre/post equality
optional active-policy pointer pre/post equality
```

---

## 39. Claim boundary

After a successful user-local Accept review, the strongest permitted statement is:

```text
An operator explicitly reviewed this exact fresh 12 recommendation,
its exact source/candidate policy diff and evidence summaries passed the 13 gates,
and the operator admitted the exact candidate to the selected 14 qualification scope.
```

Still forbidden:

```text
candidate is production approved
candidate improves loss
candidate is globally superior
candidate is safe to activate without qualification
```

---

## 40. Natural successor

The next authority stage is:

```text
ASH-BP-DK-FUSION-POLICY-CANDIDATE-CANARY-QUALIFICATION-14
```

14 should consume only a valid 13 qualification ticket and evaluate the exact candidate policy in a bounded non-production qualification/canary context.

A later explicit stage should remain responsible for production activation:

```text
14 candidate qualification
-> 15 explicit production activation
```

---

## Bake seal

```text
BAKE_ASH_BP_DK_FUSION_POLICY_PROMOTION_OPERATOR_REVIEW_GATE_13

12_DIRECT_PARENT
05_CURRENT_POLICY_AUTHORITY_UNCHANGED
12_RECOMMENDATION_IMMUTABLE_INPUT

SOURCE_POLICY_SNAPSHOT_REQUIRED
CURRENT_POLICY_SNAPSHOT_REQUIRED
SOURCE_POLICY_DIGEST_EXACT
SOURCE_POLICY_REVISION_EXACT

RECOMMENDATION_DIGEST_EXACT
RECOMMENDATION_GUARD_DIGEST_EXACT
CANDIDATE_POLICY_DIGEST_EXACT
CANONICAL_05_POLICY_VALIDATOR_REUSED

ALL_11_SEMANTIC_POLICY_FIELDS_EXACT_DIFFED
PROPOSED_CHANGE_SET_EXACT
NO_HIDDEN_POLICY_FIELD_REWRITE
CANDIDATE_REVISION_EXPLICIT

R1_SUPPORTED_CANDIDATE_SCOPE_ONLY
INCREASE_FUSION_CONFIRMATION_SUPPORTED
INCREASE_COOLDOWN_SUPPORTED
UNSUPPORTED_SCOPE_CANNOT_ACCEPT

STATUS_ADMISSION_MATRIX_EXPLICIT
INSUFFICIENT_EVIDENCE_CANNOT_ACCEPT
INSUFFICIENT_REPLAY_EVIDENCE_CANNOT_ACCEPT
CURRENT_REPLAY_MISMATCH_CANNOT_ACCEPT
CANDIDATE_INVALID_CANNOT_ACCEPT
REVIEW_REQUIRED_CANNOT_ACCEPT_R1
CONFLICTING_EVIDENCE_CANNOT_ACCEPT_R1

SOURCE_POLICY_FRESHNESS_REQUIRED
LATEST_11_EVIDENCE_REQUIRED
LATEST_12_REPLAY_EVIDENCE_REQUIRED
LATEST_RECOMMENDATION_REQUIRED
ACCEPT_REQUIRES_CURRENT_FRESHNESS

MIN_ACCEPT_CONFIDENCE_SUPPORTED
R1_REVIEW_POLICY_CANNOT_LOOSEN_FRESHNESS
R1_REVIEW_POLICY_CANNOT_LOWER_CONFIDENCE_BELOW_SUPPORTED

EXPLICIT_OPERATOR_IDENTITY
EXPLICIT_OPERATOR_DECISION
EXPLICIT_OPERATOR_REASON
NO_AUTO_ACCEPT
NO_DEFAULT_ACCEPT
NO_TIMEOUT_ACCEPT
NO_FORCE_OVERRIDE

ACCEPT_FOR_QUALIFICATION
REJECT
DEFER
REQUEST_MORE_EVIDENCE
ACKNOWLEDGE_KEEP_CURRENT

EXPLICIT_QUALIFICATION_SCOPE_REQUIRED

IMMUTABLE_REVIEW_RECEIPT
REVIEW_SEQUENCE_LINKAGE
IMMUTABLE_QUALIFICATION_TICKET

ACCEPT_CREATES_14_QUALIFICATION_TICKET_ONLY
NO_PRODUCTION_APPROVAL_FIELD

RECOMMENDATION_FILE_READ_ONLY_WITNESS
SOURCE_POLICY_FILE_READ_ONLY_WITNESS
CURRENT_POLICY_FILE_READ_ONLY_WITNESS
OPTIONAL_ACTIVE_POINTER_READ_ONLY_WITNESS

NO_RECOMMENDATION_RECOMPUTE
NO_CANDIDATE_REPLAY
NO_OBJECTIVE_PREDICTION

NO_CURRENT_POLICY_MUTATION
NO_ACTIVE_POINTER_MUTATION
NO_HOT_RELOAD
NO_PLANNER_MUTATION
NO_CHECKPOINT_MUTATION

NO_GPU_DISPATCH
NO_MODEL_FORWARD
NO_BACKWARD
NO_GRADIENT_ACCESS
NO_MUON_EXECUTION

NO_NEW_DELTAK_FORMULA
NO_NEW_FUSION_POLICY_SEMANTICS
PRECISION_AUTHORITY_UNCHANGED
RESIDENCY_AUTHORITY_UNCHANGED
NO_PERFORMANCE_PROMOTION

STATIC_13_247_OF_247_PASS
PARENT_STATIC_LINEAGE_PASS
USER_LOCAL_RUST_EXECUTION_UNVERIFIED

13_OPERATOR_REVIEW_ONLY
14_CANARY_QUALIFICATION_REQUIRED
15_EXPLICIT_PRODUCTION_ACTIVATION_REQUIRED
```
