# ASH-BP-DK-FUSION-POLICY-PRODUCTION-EVIDENCE-RECALIBRATION-BRIDGE-18

## Status

```text
Patch ID: ASH-BP-DK-FUSION-POLICY-PRODUCTION-EVIDENCE-RECALIBRATION-BRIDGE-18
Direct parent: ASH-BP-DK-FUSION-POLICY-PRODUCTION-LONG-HORIZON-STABILITY-17
Purpose: export operator-selected production evidence from one exact 15 activation epoch into an immutable, provenance-preserving recalibration package that a future explicit calibration-adoption revision may consume

18 production policy authority: none
18 active-pointer mutation authority: none
18 rollback authority: none
18 recommendation authority: none
18 candidate-policy generation authority: none
18 planner execution authority: none
18 training/GPU/model/gradient/Muon authority: none

12 R1 recommendation implementation: byte-preserved
15 production activation authority: byte-preserved
16 production soak authority: byte-preserved
17 long-horizon authority: byte-preserved
19 explicit calibration adoption: required future boundary
```

Current bake status:

```text
18_OPERATOR_SELECTION_SOURCE_PATH_WIRED
18_IMMUTABLE_RECALIBRATION_INTENT_WIRED
18_PRODUCTION_EVIDENCE_PACKAGE_WIRED
18_FROZEN_SOURCE_WITNESS_WIRED
18_PACKAGE_VERIFICATION_WIRED
18_STATIC_SOURCE_CONTRACT_CLOSED
PARENT_00_17_AND_LOCAL_MUON_STATIC_LINEAGE_PASS
USER_LOCAL_RUST_AND_RECALIBRATION_PACKAGE_EXECUTION_UNVERIFIED
```

---

## 1. Central authority separation

The authority stack remains:

```text
12 = calibration recommendation authority
13 = operator qualification-review authority
14 = physical candidate-canary qualification authority
15 = production active-policy / rollback execution authority
16 = committed-production soak / policy-only rollback-readiness authority
17 = production longitudinal stability authority
18 = production evidence export / recalibration-package authority only
```

18 does not call or replace the 12 recommendation builder.

It does not produce a new 05 policy object, candidate policy, threshold recommendation, activation request or rollback transaction.

The only successful forward state introduced by 18 is:

```text
READY_FOR_CALIBRATION_ADOPTION
```

which means a future explicit adapter may consume the package. It does not mean calibration has been applied.

---

## 2. One package, one exact activation epoch

R1 binds each package to exactly one 15 production activation lineage.

The package must preserve the exact chain:

```text
12 recommendation
-> 13 operator review receipt
-> 13 qualification ticket
-> 14 candidate qualification receipt
-> 15 production activation receipt
-> 15 activation intent
-> 15 first production-generation witness
-> 16 production evidence provenance
-> 17 long-horizon evidence
-> 18 selection / intent / package
```

A package cannot mix two activation digests, even when the candidate policy digest is identical.

This matters because identical policy bytes do not imply identical model starting state, checkpoint lineage, runtime segment or post-rollback history.

---

## 3. Exact upstream lineage admission

18 revalidates the canonical upstream objects without invoking recommendation generation.

Admission includes:

```text
canonical source recommendation digest
13 review receipt digest / source policy / candidate policy lineage
13 qualification-ticket lineage
14 QualifiedForActivationReview receipt
14 BoundedTrainingCanary scope
15 ActivationClosed receipt
15 activation-intent lineage
15 first-production-generation witness lineage
candidate policy digest equality across all relevant artifacts
source policy digest equality across all relevant artifacts
```

An orphaned production history whose originating recommendation/review/canary lineage cannot be established is rejected.

---

## 4. Operator decision is mandatory

18 defines explicit operator decisions:

```text
EXPORT_FOR_RECALIBRATION
DEFER
REJECT_FOR_RECALIBRATION
```

A 17 health or stability state never automatically becomes `EXPORT_FOR_RECALIBRATION`.

Operator reason is typed:

```text
NEW_CALIBRATION_CYCLE_REQUESTED
LONG_HORIZON_STABLE_REFERENCE
RUNTIME_HEALTH_INVESTIGATION
TRAJECTORY_HEALTH_INVESTIGATION
OBJECTIVE_HEALTH_INVESTIGATION
ROLLBACK_READINESS_INVESTIGATION
CANDIDATE_RETIREMENT_ANALYSIS
```

An optional human note is represented only by its SHA-256 digest inside the canonical intent.

---

## 5. Explicit selection modes

R1 provides three selection modes:

```text
FULL_ACTIVATION_EPOCH
EXPLICIT_RESTART_SEGMENTS
EXPLICIT_GENERATION_RANGE
```

### FullActivationEpoch

Selects all available 17 restart segments for the activation epoch and allows no operator exclusion list.

Coverage kind:

```text
FULL_AVAILABLE_EPOCH_EVIDENCE
```

### ExplicitRestartSegments

Selects exact restart-segment digests and records unselected restart segments as explicit exclusions.

Coverage kind:

```text
CURATED_SUBSET
```

### ExplicitGenerationRange

R1 generation-range selection is deliberately restricted to **exact restart-segment boundaries**.

The requested first optimizer generation must equal:

```text
restart.resume_optimizer_generation + 1
```

and the requested last optimizer generation must equal the final optimizer generation of the selected contiguous restart block.

R1 does not claim that it can slice arbitrary historical generations out of a restart after the bounded 16 hot history has been evicted.

Coverage kind:

```text
RANGE_SUBSET
```

A future revision may add an immutable per-generation archive index if true intra-restart slicing becomes necessary.

---

## 6. Selection bias and evidence loss remain different concepts

Operator-curated exclusions are not counted as observation gaps.

For example:

```text
restart 1 selected
restart 2 intentionally excluded
restart 3 selected
```

is a curated subset with an explicit exclusion, not fabricated evidence loss.

Actual evidence gaps derive from the 17 authority itself:

```text
authority_gap_count
= 17 authority-continuity failures
  + 17 checkpoint-continuity failures

observation_gap_count
= 17 observation-continuity failures
```

18 therefore does not merge deliberate selection with missing/contradictory evidence.

---

## 7. Selection exclusions are first-class provenance

For curated modes the package preserves exclusion records containing:

```text
source digest
reason code
```

Supported reason categories include:

```text
OUTSIDE_REQUESTED_RANGE
DIFFERENT_RUNTIME_SEGMENT
DIFFERENT_CAPABILITY_SEGMENT
EVIDENCE_UNAVAILABLE
OBSERVATION_GAP
OPERATOR_EXCLUDED
```

18 never claims that a curated subset is an unbiased/full-epoch sample.

---

## 8. Evidence origin and evidence class are separate

Evidence origin:

```text
CANARY_QUALIFICATION
PRODUCTION_SOAK
PRODUCTION_LONG_HORIZON
```

Evidence class:

```text
CANARY_QUALIFICATION
PRODUCTION_AUTHORITY
PRODUCTION_RUNTIME_HEALTH
PRODUCTION_TRAJECTORY
PRODUCTION_OBJECTIVE
PRODUCTION_ROLLBACK_HEALTH
```

The separation is intentional. An objective observation from a canary and an objective observation from production are not interchangeable causal evidence merely because both are “objective” evidence.

---

## 9. Evidence block identity

Each selected evidence block preserves:

```text
origin
class
source digest
optional activation digest
optional restart-segment digest
optional stability-segment digest
optional exact optimizer-generation range
evidence-block digest
```

No evidence block is generated by interpolating missing generations.

---

## 10. Runtime/capability segment identity is preserved

17 already separates longitudinal evidence by actual R1 segment identity including:

```text
CF1 authoritative BaseTrain binary SHA-256
16 capability digest
16 planner revision
```

18 keeps selected stability-segment digests intact.

Multiple selected segments remain a collection of distinct evidence blocks. They are not collapsed into a single averaged runtime/capability segment.

18 introduces no unsupported independent Fusion-backend or Muon-norm revision claim beyond what the parent receipts physically expose.

---

## 11. Objective attribution boundary remains unchanged

18 can export only objective context already admitted by the upstream evidence lineage.

Existing 10/11 whole-step semantics remain authoritative:

```text
actual_minus_local
= whole fused-set intervention context
```

18 does not reinterpret that value as:

```text
one pair's causal effect
one threshold's causal effect
candidate policy vs previous source-policy effect
```

The actual candidate-vs-baseline physical comparison remains a 14 canary authority.

---

## 12. No zero fill, interpolation or historical reconstruction

Missing objective/trajectory evidence remains missing.

18 does not write:

```text
missing objective = 0
missing trajectory = stable
missing generation = previous generation
```

Observation gaps remain explicit package coverage metadata.

18 also does not bypass 16/17 by reconstructing a missing longitudinal history directly from raw 12 replay data.

---

## 13. Open 17 epoch vs historical closed epoch

17 has two valid package-source forms.

### Current open epoch

The exact 17 stability receipt must bind the current 17 head digest directly.

If the active pointer still matches the selected activation, package freshness is:

```text
CURRENT_PRODUCTION_EPOCH
```

### Historical closed epoch

17 closure reseals the mutable head after writing the closure receipt. Therefore the closed head digest is intentionally different from the pre-close head digest observed by the last stability receipt.

18 verifies the exact chain:

```text
current closed 17 head
-> closure digest
-> exact closure receipt
-> closure.final_long_horizon_head_digest
-> exact final pre-close 17 head digest
-> 17 stability receipt
```

A valid closed epoch is classified as:

```text
HISTORICAL_CLOSED_EPOCH
```

Historical does not mean invalid. It means the package must not claim that the epoch is the current production authority.

---

## 14. Exact 16 evidence resolution

Some 16 heads/health/readiness objects are mutable projections and may no longer exist at their historical paths after later observation cycles.

`build-package` therefore accepts repeated explicit source-evidence roots and resolves exact 16 source objects by canonical digest.

R1 source scanning is bounded:

```text
maximum JSON files scanned: 20,000
maximum individual JSON size: 4 MiB
symlink traversal: forbidden
```

The scan indexes only valid canonical 16 objects whose own digest validates.

If a requested historical 16 object cannot be resolved, 18 does not invent it. It records an unresolved reference and the package cannot become `ReadyForCalibrationAdoption`.

---

## 15. Frozen-source witness boundary

A digest reference alone is insufficient for durable future verification when a small parent receipt is a mutable projection that may later be replaced.

18 therefore freezes the **small JSON authority/evidence receipts actually used by the package** into:

```text
packages/<package-digest>/frozen_sources/
```

Frozen witnesses may include exact bytes for:

```text
12 recommendation
13 review receipt
13 qualification ticket
14 qualification receipt
15 activation receipt
15 activation intent
15 first-generation witness
18 selection
18 intent
17 current head
17 stability receipt
17 closure receipt when historical
selected 17 restart segments
selected 17 longitudinal entries
selected 17 stability segments
resolved 16 soak heads
resolved 16 health receipts
resolved 16 rollback-readiness receipts
```

This is **not** a second production SSOT.

The frozen copy proves which exact source bytes were validated when the package was built.

18 does **not** duplicate:

```text
model tensor payloads
optimizer tensor payloads
full checkpoint trees
training datasets
large production runtime payloads
```

---

## 16. Evidence index

The package contains an immutable `evidence_index.json`.

Each referenced artifact records:

```text
authority kind
canonical digest
optional package-local frozen-source locator
resolved flag
```

A resolved reference must have a package-local locator.

An unresolved reference must not pretend to have one.

Digest is identity. File location is only a locator.

---

## 17. Package verification is self-contained for frozen metadata receipts

`verify-package` revalidates:

```text
package canonical digest
evidence-index digest
bridge-receipt digest
18 selection and intent digests
every resolved frozen-source receipt by its own canonical upstream type/digest
package/index/receipt cross-bindings
```

Thus the package does not need a live mutable 16/17 workspace merely to verify the exact metadata evidence that was frozen at build time.

Unresolved evidence references remain visible and prevent a `ReadyForCalibrationAdoption` claim.

---

## 18. Coverage authority

`AshFusionRecalibrationCoverage` seals exact counts and availability rather than an opaque percentage:

```text
selected committed generations
selected restart segments
selected stability segments
authority gap count
observation gap count
unresolved referenced artifact count
objective evidence available
trajectory evidence available
coverage kind
```

No “82% confidence/coverage” score is introduced.

Selected committed generation count is derived from the selected restart segments' exact resume/final optimizer boundaries.

---

## 19. Package state

R1 states include:

```text
SELECTION_VALIDATED
PACKAGE_BUILT
READY_FOR_CALIBRATION_ADOPTION
EVIDENCE_INSUFFICIENT
OBSERVATION_GAP_PRESENT
SEGMENT_CONFLICT
AUTHORITY_INTEGRITY_FAILURE
INVALID_SELECTION
REJECTED
DEFERRED
```

Export decision evaluation is fail-closed:

```text
authority gaps
-> AUTHORITY_INTEGRITY_FAILURE

observation gaps
-> OBSERVATION_GAP_PRESENT

unresolved exact source artifacts
-> EVIDENCE_INSUFFICIENT

requested trajectory evidence unavailable
-> EVIDENCE_INSUFFICIENT

requested objective evidence unavailable
-> EVIDENCE_INSUFFICIENT

otherwise
-> READY_FOR_CALIBRATION_ADOPTION
```

`DEFER` and `REJECT_FOR_RECALIBRATION` remain explicit non-adoption outcomes.

---

## 20. Recalibration package schema

The package binds:

```text
production activation digest
production policy digest
source recommendation digest
source review-receipt digest
source qualification-ticket digest
source canary-qualification digest
17 long-horizon head digest
17 long-horizon stability digest
18 selection digest
18 intent digest
typed evidence blocks
coverage
package state
package digest
```

It contains no proposed 05 field changes and no candidate policy object.

---

## 21. Bridge receipt

The final 18 receipt binds:

```text
activation digest
production policy digest
17 long-horizon head/stability digests
selection digest
intent digest
package digest
evidence-index digest
freshness
package state
hard-zero authority counters
bridge digest
```

The receipt does not claim that 12 consumed the package.

---

## 22. Hard-zero authority counters

18 requires zero for:

```text
production policy mutation
active-pointer swap
automatic rollback
automatic recalibration
recommendation generation
candidate-policy generation
planner execution
GPU dispatch
model forward
backward
gradient access
Muon execution
```

These counters are semantic authority boundaries, not performance counters.

---

## 23. Explicit no-call boundaries

The 18 BaseTrain bridge does not call:

```text
build_policy_calibration_recommendation
plan_bp_dk_fusion_candidates
commit_fusion_policy_activation
rollback_active_policy_pointer
bootstrap_managed_fusion_policy_authority
run_managed_base_train_process
std::process::Command
```

There is no WGPU/cudarc execution path in 18.

---

## 24. CLI

18 adds:

```text
crates/base_train/src/bin/
ash_bp_dk_fusion_policy_production_evidence_recalibration_bridge_18.rs
```

Commands:

```text
select
build-package
verify-package
show
```

There is no:

```text
recalibrate
recommend
activate
rollback
train
force
promote
```

subcommand.

### Select

Accepts the activation receipt, long-horizon root, operator identity/decision/reason, selection mode and mode-specific restart/generation boundaries, then writes immutable selection and intent artifacts.

### BuildPackage

Accepts the exact 12/13/14/15 lineage, 17 root, 18 selection/intent and optional repeated source-evidence roots, resolves selected evidence and builds the package/index/bridge receipt.

### VerifyPackage

Revalidates the package-local frozen evidence and all package cross-bindings without mutating production authority.

---

## 25. Filesystem layout

R1 recalibration root uses immutable digest-named artifacts:

```text
<recalibration-root>/
  selections/
    <selection-digest>.json

  intents/
    <intent-digest>.json

  packages/
    <package-digest>/
      package.json
      evidence_index.json
      frozen_sources/
        ... selected validated JSON witnesses ...

  receipts/
    <bridge-digest>.json
```

Same-path same-bytes reuse is idempotent.

Same canonical identity/path with different bytes fails closed.

---

## 26. Runner

18 adds:

```text
tools/run_ash_bp_dk_fusion_policy_production_evidence_recalibration_bridge_18.ps1
```

Actions:

```text
Validate
Select
BuildPackage
VerifyPackage
Show
```

The runner assumes the overlay is already applied.

It contains no overlay discovery/application and no `Expand-Archive` step.

Validation runs:

```text
18 static validator
cargo fmt --all -- --check
cargo check -p base_train --bin ash_bp_dk_fusion_policy_production_evidence_recalibration_bridge_18
```

The Cargo/Rust gates remain user-local because the bake environment does not provide Rust tooling.

---

## 27. Changed files

Relative to the clean 17 full-body parent, the final 18 bake differs in exactly eight files:

```text
NEW crates/ash_core/src/fusion_policy_production_evidence_recalibration_bridge.rs
MOD crates/ash_core/src/lib.rs
NEW crates/base_train/src/bin/ash_bp_dk_fusion_policy_production_evidence_recalibration_bridge_18.rs
NEW crates/base_train/src/bp_delta_k_fusion_policy_production_evidence_recalibration_bridge.rs
MOD crates/base_train/src/lib.rs
NEW tools/run_ash_bp_dk_fusion_policy_production_evidence_recalibration_bridge_18.ps1
MOD tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
NEW tools/validate_ash_bp_dk_fusion_policy_production_evidence_recalibration_bridge_18_static.py
```

Counts:

```text
added: 5
modified: 3
deleted: 0
```

No production BaseTrain/scheduler/TensorCube-Muon/05/12/13/14/15/16/17 implementation file is modified.

---

## 28. Final 18 source anchors

```text
18 core
db2415d704c837b9b7898f753f582347f6ec83fdd0c987abe090d64b9b8dc7a1

ash_core lib export
d08de26789012a2cf384f70f486e0502db156aad9253dbcdcc89efca5f0313c3

18 binary
1bbf36250c486e7dbfdca54dd5f5f0ee45305e68cd169670c64daac2f7d6fccf

18 BaseTrain bridge
d8fe4b5a4506359b75629e156174d914b68a949feaa780233a4c6785939591ed

base_train lib export
ff24693a8251076765610a34945769cd0c43e8b6e290e48eea7542e05b00cc59

18 runner
a2fb68afe29491901537207bac41516fe791df210edc4d80024186e4ce77c4e1

CF1 chain
5a7edf44e70e21f76e64628aa8080091fe7b01bb83746f24cd7007019367a323

18 static validator
803bf990eae61e05a66dede119a794db04ca7a45433e5a116c74167469548d35
```

Important preserved parent anchors include:

```text
17 core
9a40563709f1a6458cebea38040e405a8585a79e89016a0b0abc80e79d809c7c

17 BaseTrain observer
bc98441a9d32ce5d090748063c1c0615d6125ddb0569226a69946797075bcbc3

17 binary
17d55e39d45d34d8f4ede1e2de0a0289872d8825c10a0f21f8f37a926f1e6aa8

16 core
c534c6cf0025a1494535577fed9887fb5d807147be253a12252a7ef246d937c9

15 core
28b70cbf38c6700c36e7859cdf69ef4bd5096abd8812fcafd66130fd514709d5

12 core
8ec7bf2908153124af6af5392dd9f8f90a32847e07d5bba69b6bdde69ac5730a

12 BaseTrain recommendation
73c06d8259d04c4ba199f77305e48a346eb81c4a83fca15ee616739043f23944

12 recommendation binary
c695093b811649419be3c97aafee792343a23656e4af1d67f988fbeb8ce561a9

05 planner core
53a51cf384e60c5d17d6259081339b1703a90e3da5c14cf75b8d0ecfd9ab2897

05 BaseTrain planner runtime
70e6d4f08e89d4693c1999ff4508ec09ad4fcfe9850e2bb914127702f5f618cc

production BaseTrain entrypoint
20c767d68b91e7b8aa4a0bee1f9fb356daebe1bbb4c6deef6784a08831863e54

production scheduler
33d096c9d2b6d90cef0e27d763eb1658cc56daa4d4c4d3988ff004deed120e99

TensorCube/Muon production callsite
658057cb28df64ac35296cedae093f78e40ffb9087b55d88072596006be7e32c
```

---

## 29. Static validation

Final 18 gate:

```text
validate_ash_bp_dk_fusion_policy_production_evidence_recalibration_bridge_18_static.py
298/298 PASS
```

The gate seals, among other things:

```text
17 direct-parent byte anchors
12/15/16/17 preservation
exact activation/review/canary lineage
one package / one activation epoch
explicit operator decision
three explicit selection modes
restart-boundary-only generation range R1
selection exclusion provenance
closed-epoch closure-chain validation
current-vs-historical freshness distinction
typed evidence origin/class
runtime/capability segment preservation
actual gap counters distinct from curation
bounded no-symlink source-evidence scan
small JSON frozen-source witnesses
package-local frozen selection/intent verification
unresolved exact source => non-ready package
whole-step objective attribution preservation
no recommendation/candidate/planner generation
no 15 activation/rollback call
zero GPU/model/gradient/Muon authority
17 -> 18 CF1 order
```

---

## 30. Parent regression

Final relevant BP-DeltaK gates remain PASS:

```text
12 Policy Calibration Recommendation             227/227 PASS
13 Operator Review Gate                          247/247 PASS
14 Candidate Canary Qualification                347/347 PASS
15 Explicit Production Activation                274/274 PASS
16 Production Soak / Rollback Health             177/177 PASS
17 Production Long-Horizon Stability             225/225 PASS
18 Production Evidence Recalibration Bridge      298/298 PASS
```

Earlier 00-11 BP-DeltaK validators were also rerun in the full lineage and returned PASS.

Local Muon/cache regression remained:

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

## 31. CF1 wiring

18 is appended after 17:

```text
15 Explicit Production Activation
-> 16 Production Soak / Rollback Health
-> 17 Production Long-Horizon Stability
-> 18 Production Evidence Recalibration Bridge
```

No earlier closure validator is replaced.

---

## 32. Packaging

The first draft full-body package was rejected during final QA because it contained 97 files not present in the 17 parent even though the source SHA diff was only eight files.

That contaminated package was discarded and rebuilt from a **fresh extraction of the exact 17 parent plus only the final eight-file overlay**.

Final delivered packages:

```text
full-body bake
18,769,263 bytes
7,186 files
ZIP integrity PASS
parent diff: +5 / ~3 / -0

overlay bake
44,613 bytes
exactly 8 files
ZIP integrity PASS
```

Both final archives contain zero:

```text
target/
__pycache__/
*.sha256
```

The full-body file count is exactly consistent with:

```text
17 parent: 7,181 files
+ 5 new files
= 18 full body: 7,186 files
```

---

## 33. Bake-environment boundary

The bake environment does not provide:

```text
cargo
rustc
rustfmt
physical WGPU runtime/adapter
```

Therefore this bake does **not** claim:

```text
Rust compilation success
real operator selection execution
real historical source-evidence resolution
real frozen-source package build
real package verification on the user's filesystem
real ReadyForCalibrationAdoption result
real 19 calibration adoption
```

Current evidence level is static source-contract / archive-integrity evidence.

---

## 34. Required user-local gates

Before promoting 18 physical runtime status:

```text
cargo fmt --all -- --check
cargo check -p base_train --bin ash_bp_dk_fusion_policy_production_evidence_recalibration_bridge_18
CF1 reaches 18
```

Then exercise at minimum:

```text
FullActivationEpoch current-open package
historical closed-epoch package through exact closure chain
ExplicitRestartSegments curated package with exclusions
ExplicitGenerationRange aligned exactly to restart boundaries
arbitrary intra-restart generation slice rejected
same-policy different-activation merge rejected
cross-activation evidence rejected
actual 17 observation gap preserved separately from curated exclusions
resolved exact 16 sources frozen into package
missing historical 16 source => EvidenceInsufficient
requested trajectory/objective evidence unavailable => EvidenceInsufficient
source scan symlink ignored / scan bounds enforced
frozen selection and intent revalidated by verify-package
frozen parent receipts canonical digests revalidated
package collision with different bytes rejected
verify-package idempotence
recommendation/candidate/pointer mutation counters remain zero
```

---

## 35. Claim boundary

After a real user-local package reaches `ReadyForCalibrationAdoption`, the strongest supported statement is:

```text
For this exact production activation epoch, the explicitly selected 15/16/17 evidence has been packaged with its originating recommendation/review/canary lineage, selection and exclusion provenance, runtime/capability segment identities, evidence gaps and exact frozen metadata witnesses preserved; the immutable package is structurally ready for a future explicit calibration-adoption layer to consume.
```

It still does not establish:

```text
a policy has been recalibrated
a new candidate policy exists
12 recommends a threshold change
a particular 05 threshold caused a production symptom
the production policy should be rolled back
a new candidate is qualified for canary or production
```

---

## 36. Natural successor

The next authority boundary is:

```text
ASH-BP-DK-FUSION-POLICY-PRODUCTION-EVIDENCE-CALIBRATION-ADOPTION-19
```

19 may introduce an explicit typed adapter from the immutable 18 package into a revised calibration evidence context.

It must keep evidence origin explicit, for example:

```text
HistoricalReplay
CanaryQualification
ProductionLongHorizon
```

and must not collapse them into an untyped evidence list.

Any recommendation created from the future extended calibration path must still pass:

```text
13 operator review
-> 14 physical canary qualification
-> 15 explicit production activation
```

No production-to-recommendation auto-loop is introduced by 18.

---

## Bake seal

```text
BAKE_ASH_BP_DK_FUSION_POLICY_PRODUCTION_EVIDENCE_RECALIBRATION_BRIDGE_18

17_DIRECT_PARENT
EXACT_12_13_14_15_16_17_LINEAGE

ONE_PACKAGE_ONE_ACTIVATION_EPOCH
NO_CROSS_ACTIVATION_MERGE
NO_SAME_POLICY_DIFFERENT_ACTIVATION_MERGE_R1

EXPLICIT_OPERATOR_DECISION
NO_DEFAULT_EXPORT

FULL_ACTIVATION_EPOCH_SELECTION
EXPLICIT_RESTART_SEGMENT_SELECTION
EXPLICIT_GENERATION_RANGE_SELECTION

GENERATION_RANGE_RESTART_BOUNDARY_ALIGNED_R1
NO_FAKE_INTRA_RESTART_HISTORICAL_SLICING

CURATED_EXCLUSION_IS_NOT_OBSERVATION_GAP
17_AUTHORITY_AND_OBSERVATION_GAPS_PRESERVED

EVIDENCE_ORIGIN_TYPED
EVIDENCE_CLASS_TYPED
CANARY_AND_PRODUCTION_CAUSAL_SCOPE_PRESERVED

RUNTIME_CAPABILITY_SEGMENT_IDENTITY_PRESERVED
NO_CROSS_SEGMENT_SILENT_AVERAGE

WHOLE_STEP_OBJECTIVE_ATTRIBUTION_PRESERVED
NO_PAIR_CAUSALITY_FABRICATION
NO_CANDIDATE_VS_SOURCE_OBJECTIVE_FABRICATION

NO_ZERO_FILL
NO_INTERPOLATION
NO_RAW_12_HISTORY_RECONSTRUCTION

OPEN_17_HEAD_DIRECT_STABILITY_BINDING
CLOSED_17_HEAD_CLOSURE_CHAIN_VALIDATED
CURRENT_AND_HISTORICAL_FRESHNESS_EXPLICIT

BOUNDED_16_SOURCE_EVIDENCE_SCAN
MAX_20000_JSON_FILES
MAX_4_MIB_PER_JSON
NO_SYMLINK_TRAVERSAL

UNRESOLVED_EXACT_SOURCE_REMAINS_UNRESOLVED
UNRESOLVED_SOURCE_PREVENTS_READY_STATE

SMALL_JSON_FROZEN_SOURCE_WITNESSES
NO_MODEL_TENSOR_DUPLICATION
NO_CHECKPOINT_TREE_DUPLICATION
FROZEN_WITNESS_IS_NOT_SECOND_PRODUCTION_SSOT

IMMUTABLE_SELECTION
IMMUTABLE_RECALIBRATION_INTENT
IMMUTABLE_PACKAGE
IMMUTABLE_EVIDENCE_INDEX
IMMUTABLE_BRIDGE_RECEIPT

DIGEST_IS_IDENTITY
LOCATION_IS_LOCATOR_ONLY

VERIFY_PACKAGE_REVALIDATES_FROZEN_SOURCE_TYPES_AND_DIGESTS
FROZEN_SELECTION_AND_INTENT_REVALIDATED

COVERAGE_EXACT_COUNTS_NOT_PERCENTAGE_SCORE

READY_FOR_CALIBRATION_ADOPTION_ONLY
NO_CALIBRATION_APPLIED_CLAIM

NO_12_INVOCATION_R1
NO_12_R1_CONTRACT_MUTATION
NO_05_PLANNER_EXECUTION
NO_RECOMMENDATION_GENERATION
NO_CANDIDATE_POLICY_GENERATION

NO_15_ACTIVATION_OR_ROLLBACK_CALL
NO_PRODUCTION_POLICY_MUTATION
NO_ACTIVE_POINTER_SWAP

NO_AUTOMATIC_RECALIBRATION
NO_AUTOMATIC_ROLLBACK
NO_AUTOMATIC_ACTIVATION

NO_GPU_DISPATCH
NO_MODEL_FORWARD
NO_BACKWARD
NO_GRADIENT_ACCESS
NO_MUON_EXECUTION

NO_NEW_DELTAK_FORMULA
NO_NEW_FUSION_POLICY_SEMANTICS
NO_NEW_FUSION_TOPOLOGY
NO_NEW_MUON_MATHEMATICS

PRECISION_AUTHORITY_UNCHANGED
RESIDENCY_AUTHORITY_UNCHANGED
36_GIB_RAM_AUTHORITY_UNCHANGED

FINAL_FULL_BODY_CLEAN_PARENT_PLUS_EXACT_8_FILE_OVERLAY
STATIC_18_298_OF_298_PASS
PARENT_STATIC_LINEAGE_PASS
USER_LOCAL_RUST_AND_RECALIBRATION_PACKAGE_EXECUTION_UNVERIFIED

18_IS_PRODUCTION_EVIDENCE_EXPORT_AND_RECALIBRATION_PACKAGE_AUTHORITY_ONLY
19_EXPLICIT_CALIBRATION_ADOPTION_REQUIRED
```
