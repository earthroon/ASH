# ASH-DK-SYN-R2A HEBBIAN CLOSED-LOOP STABILITY ADMISSION

## 0. Revision

```text
Short name:
DK-SYN-R2A

Patch ID:
ASH-DK-SYNAPSE
-HEBBIAN-CLOSED-LOOP-STABILITY-ADMISSION
-STORE-OFF-OBSERVE-ONLY-ACTIVE-SAME-SOURCE-AB
-OSCILLATION-LOCK-IN-RECEIPTS
-PROPOSAL-EFFECT-ATTRIBUTION
-PROMOTION-SEAL
-R2A
```

Static status at this bake:

```text
same-source StoreOff/store-aware comparison     = MATERIALIZED
R2 committed-store reuse                        = PRESERVED
oscillation receipts/policy                     = MATERIALIZED
lock-in receipts/policy                         = MATERIALIZED
proposal-effect attribution                     = MATERIALIZED
store revision ledger                           = MATERIALIZED
campaign stability receipt builder              = MATERIALIZED
configurable promotion policy                   = MATERIALIZED
store-specific promotion seal                   = MATERIALIZED
Active seal admission                           = MATERIALIZED
Candidate-store rejection                       = PRESERVED
Rust compile PASS                               = NOT CLAIMED BY BAKE ENVIRONMENT
stability campaign PASS                         = HOLD
production Active promotion                     = HOLD
```

Static token:

```text
PASS_ASH_DK_SYN_R2A_CLOSED_LOOP_STABILITY_AB_OSCILLATION_LOCKIN_ATTRIBUTION_PROMOTION_STATIC
```

Promotion HOLD:

```text
HOLD_ASH_DK_SYN_R2A_CLOSED_LOOP_STABILITY_AB_OSCILLATION_LOCKIN_ATTRIBUTION_PROMOTION_PENDING
```

Reserved promotion PASS:

```text
PASS_ASH_DK_SYN_R2A_CLOSED_LOOP_STABILITY_AB_OSCILLATION_LOCKIN_ATTRIBUTION_PROMOTION
```

## 1. Direct parent

```text
ASH_PASS3_DK_SYN_R2_EDGE_INSTABILITY_STORE_STATIC_SOURCE_BAKE_CODE_ONLY.zip
SHA-256 82f324e19c3acff1e3ad5e73ae7e46c5aae171d3f55a9f1cec2ad1c719692e95
entries 8,454
```

DK-SYN-R2 already closes exact-edge learned-cost storage, exact-edge evidence projection, explicit candidate/commit/rollback, committed-store router reinjection, and persistence.

R2A does not redesign those authorities. It determines whether a committed R2 loop is stable enough to receive Active routing authority.

## 2. No duplicate routing-mode SSOT

R2 already owns:

```text
AshInstabilityCostRoutingModeR2::{Disabled, ObserveOnly, Active}
```

R2A does not create a second runtime routing-mode SSOT.

R2A owns comparison, stability, campaign and promotion authority only.

## 3. Same-source A/B authority

Added:

```text
crates/ash_core/src/hebbian_closed_loop_stability_r2a.rs
```

`compare_same_source_routes_r2a(...)` runs the same registry/input/search state as:

```text
StoreOff baseline
vs
Committed-store Active candidate
```

The source ID is derived from the registry revision and complete serialized route input. The instability store digest is intentionally not part of source identity because it is the A/B experimental variable.

The receipt records baseline/candidate path IDs, ordered edge IDs, selected actions, beam truncation state, and route-difference taxonomy.

## 4. Zero-store parity

`zero_store_parity_r2a(...)` verifies a complete committed R2 store whose every edge cost is exactly zero produces the same path-integral route plan as StoreOff.

This is a mandatory structural precursor to Active promotion.

## 5. Route-difference taxonomy

R2A distinguishes:

```text
SamePath
SameEdgesDifferentProbability
DifferentParallelEdge
DifferentSuffix
DifferentPrefix
CompletelyDifferentPath
PreviouslySelectedPathPruned
```

This preserves R1 exact-edge identity in stability analysis.

## 6. Parent/child store comparison

`compare_parent_child_store_routes_r2a(...)` requires:

```text
same registry revision
child.source_snapshot_digest == parent.snapshot_digest
```

and then compares the two committed stores on identical route input.

This is the basis for proposal-effect attribution and rollback A/B.

## 7. Oscillation authority

Added:

```text
crates/ash_core/src/hebbian_oscillation_receipt_r2a.rs
```

R2A measures committed edge-cost direction changes over a configured revision window.

Receipt fields include:

```text
increase_count
decrease_count
direction_reversal_count
longest_alternating_run
min/max/latest cost
exceeds_policy
```

Monotonic repeated increases are not classified as oscillation merely because the cost keeps changing.

The thresholds are supplied by `AshHebbianOscillationAdmissionPolicyR2A`; R2A does not invent universal limits.

## 8. Lock-in authority

Added:

```text
crates/ash_core/src/hebbian_lock_in_receipt_r2a.rs
```

Lock-in suspicion requires both:

```text
persistent near-maximum learned penalty
+
selection/exposure starvation
```

Policy controls near-max fraction, allowed near-max revisions and minimum recent exposure required for recovery evidence.

R2A detects the condition only. It does not automatically force exploration or decay.

## 9. Proposal-effect attribution

Added:

```text
crates/ash_core/src/instability_proposal_effect_r2a.rs
```

Only `IncreasePathInstabilityCost` / `DecreasePathInstabilityCost` proposals are admitted.

The receipt binds:

```text
proposal_id
edge_id
parent store digest
child store digest
old/new cost
cost delta
same-source selected-route change
action delta
optional baseline/candidate outcome
```

Outcome classifications are:

```text
NoObservedRouteEffect
RouteChangedOutcomeImproved
RouteChangedOutcomeNeutral
RouteChangedOutcomeRegressed
InsufficientObservation
```

The comparison is behavioral attribution, not a claim of single-edge causal proof.

## 10. Outcome ordering

For effect classification R2A reuses existing outcome semantics with the ordering:

```text
Rejected < Fail < Warning < Pass
```

No new model-quality metric is introduced by this bake.

## 11. Revision ledger

Added to:

```text
crates/ash_core/src/hebbian_promotion_seal_r2a.rs
```

`AshInstabilityStoreRevisionLedgerR2A` records:

```text
store revision
parent digest
child digest
proposal IDs
exact changed edge IDs
promotion state
```

When a parent is supplied, the child must bind that parent via `source_snapshot_digest`.

Revisions must increase strictly.

## 12. Stability campaign receipt builder

`build_hebbian_closed_loop_stability_receipt_r2a(...)` computes campaign summary from actual receipts rather than requiring callers to hand-author every aggregate count.

It validates ObserveOnly pair receipts against the exact campaign store and registry and derives:

```text
route divergence fraction
oscillating edge count
lock-in suspected edge count
improved/regressed/inconclusive proposal effects
```

StoreOff/Active sample counts and parity/determinism results remain explicit campaign evidence inputs.

## 13. Configurable promotion policy

R2A does not hardcode quality/stability thresholds.

`AshHebbianClosedLoopPromotionPolicyR2A` supplies:

```text
minimum ObserveOnly samples
minimum Active-canary samples
maximum oscillating edges
maximum lock-in edges
maximum regressed proposal effects
maximum inconclusive proposal effects
require zero-store parity
require deterministic same-source routing
```

The promotion policy ID is included in the promotion seal.

## 14. Promotion seal

`AshHebbianClosedLoopPromotionSealR2A` binds:

```text
registry revision
store digest
campaign ID
promotion policy ID
oscillation policy ID
lock-in policy ID
ObserveOnly result
Active-canary result
oscillation result
lock-in result
proposal-effect attribution result
semantic parity result
promotion state
seal digest
pass token
```

The seal is store-specific. A new store digest does not inherit the old seal.

## 15. Active admission

`admit_hebbian_active_route_r2a(...)` requires:

```text
valid committed R2 store
matching registry revision
matching store digest
matching seal digest
promotion state == Active
PASS token
all individual promotion booleans true
```

A matching digest alone is not sufficient.

`build_promoted_active_route_r2a(...)` is the explicit seal-gated R2A Active routing seam.

## 16. Candidate store remains invisible

R2A does not weaken R2 publication state.

Candidate stores fail R2 store validation and therefore cannot receive a promotion seal or route through the promoted Active seam.

## 17. StoreOff baseline remains available

StoreOff does not require an instability store and remains the baseline/recovery route.

A missing/corrupt store is not silently recreated as an all-zero Active store.

## 18. No automatic mutation

R2A does not introduce:

```text
automatic proposal apply
automatic rollback
automatic exploration
automatic decay
automatic forgiveness
```

R2 explicit apply / candidate / commit / rollback semantics remain authoritative.

## 19. Beam contract retained

R2A retains DK-SYN-R1:

```text
finite beam = deterministic approximate search
global optimality = NOT CLAIMED
```

A store-induced beam cutoff change is observable but is not interpreted as a proof of global optimum improvement.

## 20. Static contract fixture

Added:

```text
crates/ash_core/tests/dk_syn_r2a_contract.rs
```

The fixture covers:

```text
zero-store parity
same-source snapshot binding
oscillation reversal counting
monotonic update non-oscillation
lock-in detection
revision ledger exact changed-edge recording
promotion seal store/registry binding
Candidate store promotion rejection
static receipt remains HOLD at bake
```

## 21. Static source delta

Relative to direct R2 parent:

```text
ADD 6
MOD 1
DEL 0
```

Added:

```text
crates/ash_core/src/hebbian_closed_loop_stability_r2a.rs
crates/ash_core/src/hebbian_lock_in_receipt_r2a.rs
crates/ash_core/src/hebbian_oscillation_receipt_r2a.rs
crates/ash_core/src/hebbian_promotion_seal_r2a.rs
crates/ash_core/src/instability_proposal_effect_r2a.rs
crates/ash_core/tests/dk_syn_r2a_contract.rs
```

Modified:

```text
crates/ash_core/src/lib.rs
```

No R2 store/router/apply module is modified by this bake.

## 22. Code artifacts

Full code-only artifact:

```text
ASH_PASS3_DK_SYN_R2A_CLOSED_LOOP_STABILITY_STATIC_SOURCE_BAKE_CODE_ONLY.zip
SHA-256 2a5174cde27615aeb47f1e4df860de432f683025116b2451096ace4618db8935
entries 8,460
```

Overlay:

```text
ASH_PASS3_DK_SYN_R2A_CLOSED_LOOP_STABILITY_STATIC_SOURCE_BAKE_OVERLAY.zip
SHA-256 13e6dc581ba90d7799e48657282e896141bb9957faf8c4e673bf59976659383e
entries 7
```

Tree digest:

```text
SHA-256 98693abb15797610f7bdf77131ddab31c32b274e8768881f9588902260b9398e
```

Parent + overlay reproduces the full source tree byte-for-byte.

## 23. Compile truth

The bake environment does not provide Cargo/Rustc.

Therefore compile PASS and stability admission PASS are not claimed.

Immediate local gates:

```powershell
cargo check --locked -p ash_core --all-targets
cargo check --locked -p orchestrator_local --all-targets
```

Then:

```powershell
cargo test --locked -p ash_core --test dk_syn_r1_contract
cargo test --locked -p ash_core --test dk_syn_r2_contract
cargo test --locked -p ash_core --test dk_syn_r2a_contract
```

## 24. Promotion campaign requirements

Before the reserved R2A PASS token is emitted, the campaign must provide:

```text
R1 semantic contract PASS
R2 store/apply/router contract PASS
zero-store parity PASS
deterministic same-source PASS
ObserveOnly minimum support
Active canary minimum support
oscillation within configured policy
lock-in within configured policy
proposal-effect attribution within configured policy
matching registry/store/policy seal
```

Missing evidence yields HOLD.

## 25. Explicit non-claims

R2A does not claim:

```text
Hebbian feedback is globally optimal
every proposal is causally correct
finite beam becomes exact
automatic online adaptation is enabled
exploration starvation is automatically repaired
learned penalties decay automatically
path-integral routing is the sole global runtime SSOT
```

## 26. Direct successor

Only if campaign evidence demonstrates a need:

```text
DK-SYN-R3
Hebbian Instability Policy Calibration
+ Confidence-Weighted Update Magnitude
+ Recovery / Forgiveness Policy
+ Long-Horizon Route Diversity Admission
```

R3 is not automatically required after a clean R2A pass.

## 27. Final law

> R2 connected the exact-edge Hebbian feedback loop. R2A is the admission authority for that loop.

> The R2 routing mode remains the single mode SSOT; R2A owns comparisons and promotion, not a duplicate mode enum.

> Same-source comparisons hold registry, route input, ranker/Delta-K evidence and search policy fixed while changing only instability-store authority.

> Oscillation is measured as committed cost-direction reversal across store revisions, not as any repeated update.

> Lock-in requires persistent high penalty together with selection/exposure starvation.

> Proposal effects are attributed by exact edge, parent/child store and same-source route behavior.

> Promotion thresholds are external policy, not hidden constants in R2A.

> A promotion seal is bound to one exact registry revision, store digest, campaign and stability-policy set.

> Candidate snapshots cannot route or promote.

> A new store revision does not inherit the previous store's Active seal.

> DK-SYN-R2A is complete only after compile and campaign evidence demonstrate same-source determinism, acceptable oscillation/lock-in behavior, attributable proposal effects and a valid store-specific Active promotion seal without weakening any DK-SYN-R1/R2 authority.
