# ASH-BP-DK-FUSION-POLICY-CANDIDATE-CANARY-QUALIFICATION-14

## Status

```text
Patch ID: ASH-BP-DK-FUSION-POLICY-CANDIDATE-CANARY-QUALIFICATION-14
Direct parent: ASH-BP-DK-FUSION-POLICY-PROMOTION-OPERATOR-REVIEW-GATE-13
Purpose: physically qualify an exact 13-approved Fusion/Fission policy candidate in an isolated bounded canary without granting production activation authority

14 authority:
canary admission
isolated branch orchestration
actual branch evidence collection
runtime qualification
comparative qualification
activation-review eligibility only

14 is NOT:
production policy activation
production active-pointer mutation
production checkpoint promotion
production planner mutation
unbounded training authority
automatic 15 invocation
```

Current source status after this bake:

```text
14_CANARY_QUALIFICATION_SOURCE_PATH_WIRED
14_BOUNDED_TRAINING_CANARY_ORCHESTRATOR_WIRED
14_STATIC_SOURCE_CONTRACT_CLOSED
PARENT_00_13_AND_LOCAL_MUON_STATIC_LINEAGE_PASS
USER_LOCAL_CANARY_RUNTIME_EXECUTION_UNVERIFIED
PRODUCTION_POLICY_ACTIVATION_NOT_GRANTED
```

---

## 1. Central authority separation

14 is the first stage where a 13-approved candidate policy may alter a real isolated training trajectory.

The authority chain is:

```text
12 recommendation
-> 13 explicit operator review
-> exact 13 qualification ticket
-> 14 bounded canary qualification
-> 15 future explicit production activation
```

The critical distinction is:

```text
12 candidate replay
= historical planner-decision/exposure replay only

14 bounded canary
= actual independent training trajectory under the candidate policy
```

A successful 14 receipt means the exact candidate was physically exercised under an explicit canary contract. It does not mean the candidate is production active.

---

## 2. Direct-parent admission

14 requires the exact 13 artifacts:

```text
AshBpDkFusionPolicyOperatorReviewReceipt
AshBpDkFusionPolicyQualificationTicket
```

Admission validates at minimum:

```text
review decision == AcceptForQualification
qualification ticket review-receipt digest == exact review receipt digest
ticket recommendation digest == review recommendation digest
ticket source-policy digest == review source-policy digest
ticket candidate-policy digest == canonical candidate-policy digest
candidate policy passes canonical 05 validation
qualification scope is exactly the 13-approved scope
```

A candidate JSON by itself is not a valid 14 admission surface.

---

## 3. Qualification scopes

13 defines three qualification scopes:

```text
OfflineReplayQualification
ShadowCanary
BoundedTrainingCanary
```

14 R1 treats them distinctly.

### OfflineReplayQualification

This is a low-tier admission/packaging qualification result. It performs no actual candidate training branch and cannot become activation-review eligible.

Successful state:

```text
OfflineReplayQualified
```

### ShadowCanary

R1 does **not** claim a production-safe live shadow planner hook exists.

Therefore ShadowCanary is explicit non-support in this revision:

```text
ShadowQualificationUnavailableR1
```

14 does not silently emulate ShadowCanary using historical replay or another weaker path.

### BoundedTrainingCanary

This is the physical R1 canary tier.

It executes:

```text
same source checkpoint
-> isolated current-policy baseline branch
-> release branch runtime resources
-> isolated candidate-policy branch
-> compare exact branch evidence
```

Only `BoundedTrainingCanary` can reach:

```text
QualifiedForActivationReview
```

---

## 4. Same source checkpoint authority

Baseline and candidate branches start from the same source checkpoint directory.

14 does not copy the source checkpoint into production authority or mutate it in place.

R1 uses a bounded checkpoint witness based on the existing authoritative training-state surfaces rather than recursively hashing every potentially large payload file.

The witness binds the exact current active training state and its referenced packed-state authority, including:

```text
training_state/active_training_state.json
training-state digest/generation identity
referenced packed-state manifest identity
referenced packed-state manifest physical file digest
```

This is the R1 source-checkpoint immutability witness.

It does not claim that every large checkpoint payload byte is recursively rehashed by 14.

The bounded witness is captured before and after the canary and must remain unchanged.

---

## 5. Source policy freshness

At canary admission, the current production policy must still equal the source policy approved by 13:

```text
current production policy digest
== ticket source-policy digest
```

If the production policy has changed since 13 review:

```text
StaleSourcePolicy
```

and the ticket is not rebased onto the new policy.

A new 12 -> 13 lineage is required.

---

## 6. Exactly one intended intervention

For BoundedTrainingCanary, the intended semantic difference is:

```text
baseline branch:
05 policy = current source policy

candidate branch:
05 policy = exact 13 ticket candidate policy
```

All other canary-defining authority is required to remain common:

```text
source checkpoint
BaseTrain executable
model specification
training/common arguments
data/intake identity
explicit canary horizon
precision/runtime revision
stochastic contract
```

Policy intervention is branch-local. No production policy file is rewritten.

---

## 7. Sequential isolated execution

R1 does not require two whole training models to remain resident concurrently.

Canonical physical ordering is:

```text
baseline child process
-> complete / close
-> candidate child process
-> complete / close
```

This preserves the existing VRAM/RAM/HDD residency authorities instead of forcing double whole-model residency.

Each branch owns an independent writable output/runtime/checkpoint workspace.

There is no shared writable:

```text
model state
optimizer state
Muon momentum
03B temporal state
05 planner state
07/09/10/11/12 branch evidence
```

between baseline and candidate branches.

---

## 8. Existing BaseTrain runtime is reused

14 does not implement another training engine.

The offline canary orchestrator launches the existing canonical `base_train` binary as a child process for both branches.

The same user-supplied common BaseTrain arguments are used for baseline and candidate after 14 validates that branch-owned arguments are not already injected by the caller.

R1 rejects conflicting common arguments for surfaces owned by the canary orchestrator, including output/resume/step/storage/Atlas-plan-output authority.

This prevents the caller from quietly sending baseline and candidate to different semantic run configurations.

---

## 9. Existing BaseTrain horizon rules remain authoritative

14 requires an explicit canary generation count and binds it into the branch schedule.

However 14 does not bypass or reinterpret the existing BaseTrain production-loop step-budget rules.

The explicit 14 generation count is passed to the existing BaseTrain optimizer-step surface. If the parent runtime rejects that horizon under its existing N8/production-loop rules, the canary fails closed.

Therefore:

```text
14 explicit horizon
!= authority to override parent BaseTrain horizon law
```

No hidden universal canary horizon is introduced.

The 14 qualification policy may place an upper canary safety ceiling, but that safety ceiling does not expand what the parent runtime permits.

---

## 10. Stochastic contract

R1 supports:

```text
DeterministicNoStochasticity
```

for the bounded physical canary.

The model specification is validated so the supported R1 dropout surfaces are exactly zero:

```text
residual dropout == 0
attention dropout == 0
embedding dropout == 0
```

R1 does not claim an exact RNG snapshot/restore authority for a stochastic model and does not silently disable stochastic behavior to force comparability.

A later revision may add an explicit RNG replay authority.

---

## 11. Branch-local 05 / 11 / 12 bindings

Each physical branch is launched with branch-local policy/evidence authority:

```text
05 planner mode = ACTIVE
05 policy path = branch-local exact policy file
11 trajectory mode = DECISION_AND_UPDATE
12 calibration mode = CAPTURE
```

This is important because 14 needs the **actual branch** planner behavior, not the historical 12 recommendation replay summary.

The branch-local 12 capture produces actual current-canary replay evidence including the current 04 graph and actual 05 plans.

The branch-local 11 trajectory provides actual transition/fission/cooldown history for that branch.

---

## 12. Actual policy-exposure evidence

14 derives branch exposure from the branch's newly created physical evidence.

It does **not** substitute 12's earlier hypothetical candidate replay exposure.

Actual branch exposure includes surfaces such as:

```text
Fusion entry count
Retained Fusion count
fused pair-generation exposure
FusedRight domains
FusedDown domains
Local tile-generation exposure
Soft Fission count
Hard Fission count
Cooldown observations
state-flip observations
```

The baseline and candidate exposure values represent what actually occurred in those isolated canary runs.

---

## 13. Training objective evidence

14 reads actual physical BaseTrain production-step receipts from each branch.

The canonical training objective observation is the existing step receipt `loss_mean` under the branch's real training execution.

For comparison, baseline and candidate step receipts must exact-match the schedule identity used by 14, including the relevant batch/cursor/scheduler identity and learning-rate bit surfaces.

A candidate objective is never fabricated from 10 historical counterfactual evidence.

The signed comparison is:

```text
candidate training objective
-
baseline training objective
```

with objective direction interpreted explicitly.

---

## 14. Optional fixed-probe evidence

14 may also consume explicitly supplied fixed-probe receipts for baseline and candidate.

This probe path is external evidence supplied for the exact canary branches. It is not reconstructed from historical 10 observations.

Exact comparison requires matching:

```text
probe batch identity
objective identity
objective direction
precision identity
observation ordinal/generation identity
```

If fixed-probe evidence is required by the 14 qualification policy and insufficient observations exist, the result is:

```text
ComparativeEvidenceInsufficient
```

rather than a fabricated pass/fail result.

---

## 15. Qualification policy authority

14 uses an explicit:

```text
AshFusionPolicyCanaryQualificationPolicy
```

separate from the 05 optimizer policy.

R1 policy surfaces include:

```text
maximum canary generations
minimum completed generations
minimum fixed-probe observations
require same capability
require exact schedule
allowed runtime failures
allowed nonfinite observations
optional maximum training-objective regression
optional maximum fixed-probe regression
optional final-probe-not-worse requirement
```

These are canary workflow/qualification rules, not Fusion/Fission thresholds.

No universal hidden objective threshold is embedded into 14.

---

## 16. Default R1 qualification does not fabricate comparative approval

The default 14 qualification policy contains no objective-regression threshold and requires zero fixed-probe observations.

Therefore a physically healthy default BoundedTrainingCanary can establish runtime qualification, but the absence of an explicit comparative objective gate does not justify activation-review eligibility.

The default path may reach:

```text
CandidateRuntimeQualified
```

but not automatically:

```text
QualifiedForActivationReview
```

To reach activation-review eligibility, an explicit comparative qualification policy must provide a real comparison gate and that gate must pass.

---

## 17. Qualification state machine

14 distinguishes admission, runtime health, comparability, and activation-review eligibility.

States include:

```text
AdmissionValidated
OfflineReplayQualified
ShadowQualificationUnavailableR1

BaselineQualified
BaselineUnhealthy

CandidateRuntimeQualified
CandidateRuntimeFailed

NonComparable
ComparativeEvidenceInsufficient
ComparativeQualified
ComparativeNotQualified

QualifiedForActivationReview
```

`CandidateRuntimeQualified` means the candidate branch completed the physical runtime safety contract. It does not mean the candidate performed better than baseline.

---

## 18. Baseline health is prerequisite evidence

Baseline is executed first.

If the current-policy baseline cannot complete the canary health contract, 14 returns:

```text
BaselineUnhealthy
```

and does not attribute the broken comparison environment to the candidate.

Baseline health checks include branch receipt availability, horizon completion, finite state, policy stability, planner-fallback/replan absence, and expected branch evidence closure.

---

## 19. Candidate runtime health

The candidate branch is independently required to complete the same runtime contract.

Hard candidate failures include surfaces such as:

```text
child-process failure
incomplete horizon
nonfinite evidence
policy digest drift
planner fallback/replan
missing output authority
mixed-policy generation
```

The candidate is not silently rescued by switching failing Fusion decisions to Local.

---

## 20. No silent physical fallback

Existing Fusion execution fail-closed semantics remain authoritative.

A candidate physical Fusion failure does not permit:

```text
retry as Local and keep the canary green
```

Fallback/replan evidence is qualification-significant and disqualifies the corresponding physical branch under the R1 safety contract.

---

## 21. Exact schedule comparability

Baseline and candidate are comparable only when the actual observed branch schedule identity matches.

14 constructs/validates exact schedule evidence from the physical branch receipts rather than trusting only the planned command-line arguments.

A mismatch produces:

```text
NonComparable
```

not a candidate-performance judgment.

No nearest-generation or nearest-batch matching is allowed.

---

## 22. Same physical capability

When required by the qualification policy, baseline and candidate must expose the same actual capability identity in their captured branch evidence.

A capability mismatch is:

```text
NonComparable
```

rather than candidate failure.

14 does not infer equal capability merely because both branches ran on the same machine name.

---

## 23. Allowed divergence

The following may legitimately diverge because they are downstream of the policy intervention:

```text
05 planner state
Fusion/Fission decisions
model weights
optimizer state
Muon momentum
training objective trajectory
fixed-probe objective trajectory
final branch checkpoint digest
```

Different final model digests are not themselves a qualification failure.

---

## 24. Required invariants

The comparison authority expects the canary-defining upstream conditions to remain fixed:

```text
source checkpoint authority
training/common argument authority
model specification
explicit canary horizon
executable identity
stochastic contract
schedule identity
physical capability when required
```

The only intended optimizer-policy intervention is the 05 policy digest.

---

## 25. Branch checkpoints are quarantined

Baseline and candidate branches may write their own isolated checkpoints because actual branched training must be reproducible.

Those checkpoints are canary artifacts only.

They are not:

```text
production restart authority
production active model pointer
production optimizer checkpoint
```

14 does not promote either branch checkpoint into production.

---

## 26. Production immutability boundary

14's production authority counters remain zero:

```text
production_policy_mutation_count = 0
production_active_pointer_mutation_count = 0
production_checkpoint_mutation_count = 0
production_planner_state_mutation_count = 0
production_hot_reload_count = 0
automatic_activation_count = 0
```

Candidate-branch local model/optimizer/planner mutation is legitimate physical canary training and must not be confused with production mutation.

---

## 27. Production/source read-only witnesses

The offline orchestrator seals important input files before and after execution.

The source checkpoint authority witness must remain unchanged.

When a production active-pointer file is explicitly provided, its pre/post digest must remain unchanged.

The 13 ticket, 13 review receipt, current policy, model specification, BaseTrain binary and common-arguments input are also treated as fixed inputs to the canary run.

---

## 28. No concurrent double residency requirement

14 does not require baseline and candidate model states to coexist in VRAM/RAM.

The physical orchestration is sequential and process-isolated.

Therefore 14 does not revise the existing BaseTrain memory hierarchy or 36-GiB RAM ceiling authority.

Any branch remains subject to the parent runtime's existing residency rules.

---

## 29. Comparison receipt

When physical branch comparison exists, 14 seals a comparison receipt containing the exact baseline/candidate branch identities and multi-axis evidence.

The comparison remains inspectable across separate axes such as:

```text
training-objective deltas
optional fixed-probe deltas
Fusion exposure delta
Fission exposure delta
Cooldown exposure delta
state-flip delta
```

There is no opaque weighted "benefit score" combining those axes.

---

## 30. Explicit objective direction

Objective regression is interpreted using an explicit objective direction.

For a Minimize objective:

```text
candidate - baseline > 0
```

is the regression direction.

For Maximize it is reversed.

14 does not hardcode lower-is-better across arbitrary objectives.

---

## 31. Comparative evidence can remain insufficient

A healthy physical candidate is not forced into pass/fail comparative judgment when the configured evidence contract has not been met.

Valid state:

```text
ComparativeEvidenceInsufficient
```

This is an epistemic result, not candidate failure.

---

## 32. Activation-review eligibility

The R1 activation-review eligibility path requires all of:

```text
scope == BoundedTrainingCanary
baseline health qualified
candidate runtime health qualified
branches comparable
explicit comparative qualification gate exists
comparative evidence sufficient
comparative qualification passed
production/source immutability witnesses valid
```

Only then may 14 seal:

```text
QualifiedForActivationReview
```

This state still does not activate production policy.

---

## 33. No automatic 15 invocation

A successful 14 canary does not call a production activation routine.

The only next authority is a future explicit stage:

```text
ASH-BP-DK-FUSION-POLICY-EXPLICIT-PRODUCTION-ACTIVATION-15
```

15 must separately revalidate candidate/current-policy freshness and hold the actual activation/pointer-swap authority.

---

## 34. Core schemas

14 adds core schemas for:

```text
canary branch kind
R1 stochastic policy
runtime health state
canary admission state
canary qualification state
canary schedule
training-objective observations
optional fixed-probe observations
actual policy exposure
branch receipt
canary qualification policy
comparison receipt
production-authority hard-zero counters
final qualification receipt
```

All exact identities/digests are bound canonically rather than by human-readable file names.

---

## 35. BaseTrain canary orchestrator

14 adds the offline orchestration implementation under BaseTrain ownership.

It validates the 13 authority, constructs isolated workspaces, launches the canonical BaseTrain child process sequentially, reads physical branch receipts/evidence, performs exact comparability checks, evaluates the explicit qualification policy and writes immutable 14 evidence.

It does not modify the production scheduler or training-loop authority.

---

## 36. Offline binary

14 adds:

```text
crates/base_train/src/bin/
ash_bp_dk_fusion_policy_candidate_canary_qualification_14.rs
```

Primary inputs include:

```text
--ticket
--review-receipt
--current-policy
--source-checkpoint
--model-spec-path
--base-train-binary
--common-args-json
--generation-count
--output-root
```

Optional qualification/probe/pointer inputs are explicit.

The binary contains no production activation flag such as:

```text
--activate
--promote
--yes
--force
```

---

## 37. Runner

14 adds:

```text
tools/run_ash_bp_dk_fusion_policy_candidate_canary_qualification_14.ps1
```

The runner assumes the overlay is already applied.

It performs:

```text
14 static validation
cargo fmt --check
cargo check of the 14 canary binary
release execution of the 14 canary binary
```

There is no overlay discovery or `Expand-Archive` stage.

---

## 38. Changed files

The 14 overlay contains exactly eight files:

```text
crates/ash_core/src/fusion_policy_candidate_canary_qualification.rs
crates/ash_core/src/lib.rs
crates/base_train/src/bin/ash_bp_dk_fusion_policy_candidate_canary_qualification_14.rs
crates/base_train/src/bp_delta_k_fusion_policy_candidate_canary_qualification.rs
crates/base_train/src/lib.rs
tools/run_ash_bp_dk_fusion_policy_candidate_canary_qualification_14.ps1
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
tools/validate_ash_bp_dk_fusion_policy_candidate_canary_qualification_14_static.py
```

Not modified by 14:

```text
production scheduler
base_train production entrypoint
TensorCube/Muon production callsite
05 planner core/base
12 recommendation implementation
13 review implementation
Fusion/Muon WGSL/backend mathematics
```

---

## 39. New 14 source anchors

```text
14 core
1090082dc7ffb3daace2b37f1a05ad904843966bb3cad2c10fc6e0c929ed9e80

14 base
08529a1cd31211863647bfc216822d44812d9ec08779647925c85f8e2f3f60b7

14 canary binary
883f7cc6b71ffd8f8a999a241f95b5f3fc65fa2e424bff402632d8a2f589a371

14 runner
f41eef6ee41fddfe35a940fbba90c3d0100c7de58828c453c6111ceb0c022691

14 static validator
250a9f8eae03467f56c81b05d3a5e3d569e0feeac9769153927eabbf7567b405
```

Important preserved production anchors include:

```text
TensorCube/Muon production callsite
658057cb28df64ac35296cedae093f78e40ffb9087b55d88072596006be7e32c

production scheduler
33d096c9d2b6d90cef0e27d763eb1658cc56daa4d4c4d3988ff004deed120e99

base_train production binary
20c767d68b91e7b8aa4a0bee1f9fb356daebe1bbb4c6deef6784a08831863e54
```

---

## 40. Static validation

New gate:

```text
validate_ash_bp_dk_fusion_policy_candidate_canary_qualification_14_static.py
347/347 PASS
```

The gate seals, among other things:

```text
13 direct-parent source anchors
exact 13 ticket/review admission
candidate/current policy identity
ShadowCanary explicit R1 non-support
BoundedTrainingCanary physical child-process path
existing BaseTrain reuse
no parent horizon-rule bypass
R1 deterministic-no-stochasticity/dropout contract
bounded checkpoint witness
sequential isolated branches
branch-local 05/11/12 environment
actual branch exposure from new physical evidence
actual training objective receipt comparison
no 10 historical objective reuse
optional fixed-probe exact identity
explicit comparative qualification gate requirement
no production scheduler/callsite/05/12/13 modification
no production activation
12 -> 13 -> 14 CF1 order
```

---

## 41. Parent regression

After the 14 bake, all relevant static BP-DeltaK gates were rerun and remained PASS:

```text
00 Observation Contract                         149/149 PASS
01 Local BP-DK                                  134/134 PASS
02 Generation/Revision/Stale Seal               243/243 PASS
03A Bridge Pair Evidence                        148/148 PASS
03B Bridge Temporal Coupling                    157/157 PASS
04 Fusion Candidate Graph                       235/235 PASS
05 Active Fusion/Fission Planner                293/293 PASS
06 Active Fusion Deterministic Replay           210/210 PASS
07 POST Update Effectiveness Ledger             206/206 PASS
08A Physical Qualification                      236/236 PASS
08B Same-Source Local Counterfactual            221/221 PASS
08B-R1 Counterfactual Physical Execution        146/146 PASS
09 Counterfactual Effect Ledger                 148/148 PASS
10 One-Step Objective Probe                     259/259 PASS
11 Long-Horizon Trajectory                      145/145 PASS
12 Policy Calibration Recommendation            227/227 PASS
13 Operator Review Gate                         247/247 PASS
14 Candidate Canary Qualification               347/347 PASS
```

Local Muon regression remained PASS:

```text
optimizer                                         101/101 PASS
FirstCandidate registry                            97/97 PASS
multi-tile batch                                   61/61 PASS
production callsite                                63/63 PASS
canonical-loader repair                            38/38 PASS
ExactSubgroup32 norm                              128/128 PASS
X PAD17                                            52/52 PASS
generation-sealed immutable cache                  66/66 PASS
immutable-cache backend rebind                     35/35 PASS
```

---

## 42. CF1 wiring

14 is appended after 13 in the static chain:

```text
12 recommendation validator
-> 13 operator-review validator
-> 14 candidate-canary validator
```

Earlier closure semantics are preserved.

---

## 43. Packaging

Delivered 14 artifacts:

```text
full-body bake
18,684,323 bytes
7,166 files
ZIP integrity PASS

overlay bake
43,021 bytes
exactly 8 files
ZIP integrity PASS
```

Both archives contain zero:

```text
target/
__pycache__/
*.sha256
generated artifact directories
generated report directories
generated manifest directories
```

No generated canary branch/checkpoint/qualification evidence is included because those artifacts must be produced by the user's real canary execution.

---

## 44. Bake-environment boundary

The bake environment does not provide:

```text
cargo
rustc
rustfmt
physical WGPU runtime/adapter
```

Therefore this bake does not claim:

```text
Rust compilation success
actual baseline child-process training success
actual candidate child-process training success
actual GPU canary qualification
actual training-objective comparison
actual capability parity
actual checkpoint immutability witness on the user filesystem
actual QualifiedForActivationReview result
```

Current evidence is static source-contract evidence only.

---

## 45. Required user-local gates

Before runtime promotion of 14 status:

```text
cargo fmt --check
cargo check -p base_train --bin ash_bp_dk_fusion_policy_candidate_canary_qualification_14
CF1 reaches 14
```

Then validate at minimum:

```text
13 ticket/review exact admission
current source-policy freshness
source checkpoint witness pre/post equality

OfflineReplayQualification -> no physical activation eligibility
ShadowCanary -> explicit ShadowQualificationUnavailableR1

BoundedTrainingCanary:
baseline child process completes
candidate child process completes
actual batch schedule digests match
actual capability identities match when required
actual branch policy digests stay fixed
planner fallback/replan remains zero
no mixed-policy generation
no nonfinite state
actual branch 11/12 evidence closes

training objective receipts exact-match their schedules
optional fixed-probe receipts exact-match their probe identities

without explicit comparative gate:
CandidateRuntimeQualified at most

with explicit comparative gate and sufficient evidence:
ComparativeQualified
-> QualifiedForActivationReview

production active pointer remains unchanged
production policy remains unchanged
source checkpoint witness remains unchanged
no canary checkpoint becomes production restart authority
```

---

## 46. Claim boundary

After a real user-local BoundedTrainingCanary that reaches `QualifiedForActivationReview`, the strongest supported statement is:

```text
Starting from the same sealed source checkpoint and the same explicit canary schedule,
the current-policy baseline and the exact 13-approved candidate policy were executed as isolated actual BaseTrain trajectories.
The candidate completed the runtime-safety contract, remained comparable to the baseline under the required schedule/capability contract, and passed the explicitly configured comparative qualification gates.
The exact candidate is therefore eligible for a separate production-activation review.
```

Still not established:

```text
candidate is universally better
candidate generalizes better
candidate is safe for unlimited training
candidate is production active
candidate should automatically replace current policy
```

---

## 47. Natural successor

The next authority stage is:

```text
ASH-BP-DK-FUSION-POLICY-EXPLICIT-PRODUCTION-ACTIVATION-15
```

15 must be a separate explicit authority layer that consumes a valid 14 activation-review-eligible receipt, revalidates current-policy/candidate freshness, performs any required final operator approval and owns the atomic production policy activation/rollback boundary.

14 never performs that activation itself.

---

## Bake seal

```text
BAKE_ASH_BP_DK_FUSION_POLICY_CANDIDATE_CANARY_QUALIFICATION_14

13_DIRECT_PARENT
VALID_13_REVIEW_RECEIPT_REQUIRED
VALID_13_QUALIFICATION_TICKET_REQUIRED
ACCEPT_FOR_QUALIFICATION_REQUIRED

EXACT_SOURCE_POLICY_DIGEST
EXACT_CANDIDATE_POLICY_DIGEST
CANONICAL_05_POLICY_VALIDATION

OFFLINE_REPLAY_QUALIFICATION_SUPPORTED
SHADOW_CANARY_EXPLICITLY_UNAVAILABLE_R1
BOUNDED_TRAINING_CANARY_PHYSICAL_TIER
ONLY_BOUNDED_TRAINING_CANARY_CAN_REACH_ACTIVATION_REVIEW_ELIGIBILITY

SAME_SOURCE_CHECKPOINT_AUTHORITY
BOUNDED_ACTIVE_STATE_AND_PACKED_MANIFEST_CHECKPOINT_WITNESS
NO_UNBOUNDED_FULL_PAYLOAD_REHASH_CLAIM
SOURCE_CHECKPOINT_READ_ONLY

SEQUENTIAL_ISOLATED_BASELINE_AND_CANDIDATE_PROCESSES
NO_CONCURRENT_DOUBLE_WHOLE_MODEL_RESIDENCY_REQUIREMENT

EXISTING_BASE_TRAIN_BINARY_REUSED
NO_DUPLICATE_TRAINING_ENGINE
COMMON_ARGUMENT_AUTHORITY_VALIDATED
BRANCH_OWNED_OUTPUT_RESUME_STEP_STORAGE_ARGS

EXPLICIT_CANARY_GENERATION_COUNT
PARENT_BASETRAIN_HORIZON_N8_RULES_REMAIN_AUTHORITY
NO_HORIZON_RULE_BYPASS

R1_DETERMINISTIC_NO_STOCHASTICITY
MODEL_RESIDUAL_DROPOUT_ZERO
MODEL_ATTENTION_DROPOUT_ZERO
MODEL_EMBEDDING_DROPOUT_ZERO
NO_FAKE_EXACT_RNG_REPLAY

BASELINE_05_ACTIVE_SOURCE_POLICY
CANDIDATE_05_ACTIVE_EXACT_TICKET_POLICY
11_DECISION_AND_UPDATE_ON_BOTH_BRANCHES
12_CAPTURE_ON_BOTH_BRANCHES

ACTUAL_BRANCH_04_GRAPH_AND_05_PLAN_EVIDENCE
ACTUAL_BRANCH_11_TRANSITION_HISTORY
NO_HISTORICAL_12_REPLAY_EXPOSURE_SUBSTITUTION

ACTUAL_PRODUCTION_STEP_LOSS_MEAN
ACTUAL_BATCH_SCHEDULE_IDENTITY
NO_HISTORICAL_10_OBJECTIVE_REUSE
OPTIONAL_EXTERNAL_FIXED_PROBE_EXACT_IDENTITY

BASELINE_HEALTH_REQUIRED
CANDIDATE_RUNTIME_HEALTH_REQUIRED
NO_NONFINITE
NO_PLANNER_FALLBACK
NO_RUNTIME_REPLAN
NO_MIXED_POLICY_GENERATION
NO_POLICY_DIGEST_DRIFT

EXACT_SCHEDULE_COMPARABILITY
EXACT_CAPABILITY_COMPARABILITY_WHEN_REQUIRED
NONCOMPARABLE_IS_EXPLICIT

EXPLICIT_14_QUALIFICATION_POLICY
NO_HIDDEN_UNIVERSAL_OBJECTIVE_THRESHOLD
DEFAULT_POLICY_DOES_NOT_CREATE_COMPARATIVE_APPROVAL
EXPLICIT_COMPARATIVE_GATE_REQUIRED_FOR_ACTIVATION_REVIEW_ELIGIBILITY

CANDIDATE_RUNTIME_QUALIFIED_SEPARATE_FROM_COMPARATIVE_QUALIFIED
COMPARATIVE_EVIDENCE_INSUFFICIENT_EXPLICIT
COMPARATIVE_NOT_QUALIFIED_EXPLICIT
QUALIFIED_FOR_ACTIVATION_REVIEW_EXPLICIT

CANARY_BRANCH_CHECKPOINTS_QUARANTINED
CANARY_CHECKPOINT_NOT_PRODUCTION_RESTART_AUTHORITY

PRODUCTION_POLICY_MUTATION_COUNT_ZERO
PRODUCTION_ACTIVE_POINTER_MUTATION_COUNT_ZERO
PRODUCTION_CHECKPOINT_MUTATION_COUNT_ZERO
PRODUCTION_PLANNER_MUTATION_COUNT_ZERO
PRODUCTION_HOT_RELOAD_COUNT_ZERO
AUTOMATIC_ACTIVATION_COUNT_ZERO

PRODUCTION_SCHEDULER_BYTE_PRESERVED
BASE_TRAIN_PRODUCTION_ENTRYPOINT_BYTE_PRESERVED
TENSORCUBE_MUON_PRODUCTION_CALLSITE_BYTE_PRESERVED
05_PLANNER_BYTE_PRESERVED
12_RECOMMENDATION_BYTE_PRESERVED
13_OPERATOR_REVIEW_BYTE_PRESERVED

NO_NEW_FUSION_MUON_WGSL
NO_NEW_DELTAK_FORMULA
NO_NEW_FUSION_TOPOLOGY
NO_NEW_MUON_MATHEMATICS
PRECISION_AUTHORITY_UNCHANGED
RESIDENCY_AUTHORITY_UNCHANGED
NO_PERFORMANCE_PROMOTION

STATIC_14_347_OF_347_PASS
PARENT_STATIC_LINEAGE_PASS
USER_LOCAL_CANARY_RUNTIME_EXECUTION_UNVERIFIED

14_CANARY_QUALIFICATION_ONLY
15_EXPLICIT_PRODUCTION_ACTIVATION_REQUIRED
```
