# ASH-DK-SYN-EDGE-AUTHORITATIVE-PATH-IDENTITY-FAIL-CLOSED-EVIDENCE-SIGNED-ACTION-BEAM-CONTRACT-R1

## 0. Revision

```text
Short name:
DK-SYN-R1

Patch ID:
ASH-DK-SYNAPSE
-EDGE-AUTHORITATIVE-PATH-IDENTITY
-FAIL-CLOSED-EVIDENCE-ADMISSION
-SIGNED-ACTION-COST-CONTRACT
-BEAM-CORRECTNESS-CONTRACT
-R1
```

Static source status at this bake:

```text
edge-authoritative path identity             = MATERIALIZED
parallel-edge path preservation              = MATERIALIZED
coactivation/replay ordered-edge lineage     = MATERIALIZED
missing-ranker fail-closed admission         = MATERIALIZED
missing-Delta-K fail-closed admission        = MATERIALIZED
explicit bootstrap authority                 = MATERIALIZED
finite signed action contract                = MATERIALIZED
SoftEnsemble signed-action alignment         = MATERIALIZED
deterministic finite-beam contract            = MATERIALIZED
global optimality claim                      = EXPLICITLY NOT CLAIMED
Hebbian instability-cost store               = NOT IN R1 / NEXT REVISION
post-bake Rust compile                       = NOT CLAIMED BY BAKE ENVIRONMENT
semantic admission PASS                      = HOLD
```

Static token:

```text
PASS_ASH_DK_SYN_EDGE_AUTHORITATIVE_PATH_ID_FAIL_CLOSED_EVIDENCE_SIGNED_ACTION_BEAM_CONTRACT_R1_STATIC
```

Semantic HOLD:

```text
HOLD_ASH_DK_SYN_EDGE_AUTHORITATIVE_PATH_ID_FAIL_CLOSED_EVIDENCE_SIGNED_ACTION_BEAM_CONTRACT_R1_PENDING
```

Reserved semantic PASS:

```text
PASS_ASH_DK_SYN_EDGE_AUTHORITATIVE_PATH_ID_FAIL_CLOSED_EVIDENCE_SIGNED_ACTION_BEAM_CONTRACT_R1
```

## 1. Direct parent

```text
ASH_PASS3_DK_PERF_R1A1_R2A_PHYS_R2_COMPILE_FIX_CODE_ONLY.zip
SHA-256 b60c16252ea61d51f53eb66cdb0ea2d9df0111ff8a80306475225a5a401b2c61
```

DK-SYN-R1 does not alter the Delta-K GPU performance line, Muon mathematics, WGPU generation, optimizer authority, or TensorCube execution geometry.

It modifies the existing synapse/path-integral evidence contract that precedes a future Hebbian instability-cost-store closure.

## 2. Existing system retained

The source already contains a substantial synapse feedback system, including:

```text
adapter synapse registry
path-integral synapse router
weighted synapse router
soft ensemble composer
coactivation ledger
Hebbian update proposals
replay -> Hebbian feedback
proposal apply gate
registry/promotion surfaces
```

Existing Hebbian proposal kinds already include:

```text
IncreasePathInstabilityCost
DecreasePathInstabilityCost
```

The apply gate intentionally leaves them unapplied because no authoritative instability-cost store exists yet.

R1 does not replace this system. It repairs identity, evidence admission, signed-action, and beam-search contracts so the existing feedback path can later target exact edges safely.

## 3. Edge-authoritative PathIdentity

The legacy canonical path identity was derived from adapter IDs only. That collapses distinct parallel-edge traversals such as:

```text
A --edge_1--> B
A --edge_2--> B
```

into one adapter-sequence identity.

R1 introduces `AshSynapsePathIdentityR1` in:

```text
crates/ash_core/src/synapse_contract_r1.rs
```

Canonical identity material is:

```text
registry version
seed adapter identity
ordered edge identity sequence
terminal adapter identity
```

The public path ID is derived with SHA-256 from length-prefixed identity material.

The SHA-256 digest is a derived representation. The ordered edge sequence remains the semantic authority used for equality/deduplication.

## 4. Parallel-edge preservation

Candidate deduplication now compares edge-authoritative path semantics rather than adapter-only path IDs.

Two paths with identical adapter sequence but different ordered edge IDs are distinct candidates.

Required invariant:

```text
ordered edge sequence differs
=> canonical path identity differs
```

This is required before any learned instability cost can use `edge_id` as an SSOT key.

## 5. Registry-backed path-step identity

Canonical registry-backed path steps must carry non-empty `edge_id` lineage.

R1 does not reconstruct an edge identity from `from`, `to`, or weight because parallel edges may legally share endpoints.

Malformed registry path steps fail validation rather than silently becoming adapter-only identities.

## 6. Coactivation lineage upgrade

`AshCoactivationEvent` now carries:

```text
selected_path_id
selected_edge_ids[]
```

where `selected_edge_ids` is the ordered edge sequence of the selected route.

`bind_coactivation_path_lineage_r1(...)` binds the selected route's canonical path ID and exact edge sequence into the coactivation event.

Adapter-pair coactivation statistics remain valid aggregate evidence, but they are no longer treated as exact edge identity authority.

## 7. Replay / hard-negative lineage

Ordered edge lineage is propagated through:

```text
coactivation event
-> hard negative replay case
-> replay evaluation case/result
-> replay Hebbian feedback event
-> coactivation feedback event
```

New fields are serde-defaulted for historical artifact compatibility.

Historical evidence without ordered edge lineage remains readable but does not become edge-authoritative merely by deserialization.

## 8. SFT edge ambiguity closure

The SFT synapse binding candidate no longer silently selects the first edge of a multi-edge selected path when no explicit edge is provided.

Implicit edge inference is accepted only when the selected path contains exactly one edge identity.

Multi-edge ambiguity remains unresolved/fail-closed rather than incorrectly attributing the full path outcome to its first edge.

## 9. Ranker evidence fail-open retirement

Legacy ranker behavior could reduce missing ranker evidence to zero ranker-loss contribution, which is semantically indistinguishable from an ideal ranker result.

R1 introduces typed admission policy:

```text
RequireQualified
ExplicitBootstrap
```

Default is `RequireQualified`.

For strict admission, missing/empty or snapshot-inconsistent ranker evidence is rejected before path action calculation.

Missing evidence is no longer encoded as a valid zero-cost ranker observation.

## 10. Explicit ranker bootstrap

Cold-start operation without qualified ranker evidence must opt into:

```text
AshSynapseEvidenceAdmissionPolicyR1::ExplicitBootstrap
```

Bootstrap may contribute the existing neutral numerical term, but it is now a named policy state with explicit warning/telemetry rather than silent `None -> 0` behavior.

Thus:

```text
Missing != BootstrapExplicit
```

## 11. Delta-K evidence fail-open retirement

R1 classifies an edge as Delta-K-dependent when its routing semantics require Delta-K, including conditional activation, configured Delta-K bounds, or nonzero Delta-K priority contribution.

For a Delta-K-dependent edge under strict admission:

```text
missing Delta-K -> rejected
nonfinite Delta-K -> rejected
missing required snapshot identity -> rejected
```

Missing Delta-K no longer means zero mismatch cost.

## 12. Conditional-edge fail-closed law

Legacy conditional-edge behavior could admit a conditional edge when Delta-K was absent.

R1 changes the production contract to:

```text
Delta-K-dependent conditional edge
+ missing Delta-K
+ RequireQualified
=> not admitted
```

An explicit bootstrap policy may separately authorize cold-start behavior.

## 13. Evidence admission order

Canonical order is now:

```text
edge discovery
-> edge/path identity validation
-> evidence admission
-> action computation
-> beam insertion
```

Rejected evidence does not remain inside the beam with a fabricated zero or sanitized finite score.

## 14. Signed edge-action contract

Existing base edge action remains:

```text
C_edge = -ln(runtime_weight)
```

Therefore:

```text
0 < runtime_weight < 1  -> positive action
runtime_weight = 1      -> zero action
runtime_weight > 1      -> negative action
```

Finite negative edge action is explicitly legal.

R1 does not impose an artificial `runtime_weight <= 1` restriction.

## 15. Signed total path action

Finite total path action may be:

```text
negative
zero
positive
```

Only nonfinite action is intrinsically invalid.

The path-integral router continues to use stabilized softmin/Boltzmann-style probability calculation compatible with signed action.

## 16. SoftEnsemble signed-action alignment

The downstream SoftEnsemble previously rejected negative total/mean path action despite `-ln(runtime_weight)` permitting it.

R1 removes that contradiction.

Finite negative path action remains valid through SoftEnsemble composition.

To avoid double-rewarding negative action after path probability has already incorporated it, the additional ensemble attenuation applies only to positive mean action:

```text
positive_action_penalty = max(mean_path_action, 0)
```

No negative-action invalidation or clamp-to-zero of the path's semantic action is introduced.

## 17. Deterministic beam contract

Finite-width beam routing remains a deterministic approximate search.

R1 explicitly separates:

```text
DeterministicBeamCorrectness = REQUIRED
GlobalOptimality             = NOT CLAIMED
```

Given identical graph, registry revision, evidence, policy, beam width, depth, path limit, temperature, and tie-break contract, retained frontier/final path ordering must be reproducible.

## 18. Signed action and beam pruning

Because future edges may have legal negative action, current accumulated partial-path action is not a monotonic lower bound on completed path action.

R1 therefore makes no branch-and-bound/global-optimality claim from accumulated action alone.

A future exact search revision would require an independently valid completion bound or exhaustive bounded search.

## 19. Beam tie-break and truncation telemetry

Partial paths are ordered deterministically by:

```text
1. accumulated signed action ascending
2. canonical path ID as deterministic tie-break
```

When finite beam width truncates legal candidates, the route plan records/warns that the search is approximate and global optimality is not claimed.

When no truncation occurs over the configured reachable frontier, the invocation may be described as bounded-exhaustive within that configured frontier, not globally optimal beyond configured limits.

Public helper contracts include:

```text
beam_truncation_occurred_r1(...)
beam_global_optimality_claimed_r1() == false
```

## 20. Instability cost store explicitly remains absent

R1 does not create an instability-cost store.

Existing apply-gate handling for:

```text
IncreasePathInstabilityCost
DecreasePathInstabilityCost
```

remains separate from edge-weight mutation.

R1 does not remap path instability cost into excitatory weight, `mean_path_action`, or evidence-report strings.

The future store must use exact edge identity after R1 lineage is qualified.

## 21. Static regression fixture

Added:

```text
crates/ash_core/tests/dk_syn_r1_contract.rs
```

The fixture covers:

```text
parallel-edge path IDs remain distinct
missing ranker strict rejection
explicit ranker bootstrap admission
missing Delta-K strict rejection for dependent edge
explicit Delta-K bootstrap admission
negative edge action from runtime_weight > 1
negative signed action accepted by SoftEnsemble
finite beam truncation observed
global optimality remains false
coactivation -> hard-negative ordered edge lineage preservation
static receipt never claims semantic PASS at bake
```

Existing replay/evaluation tests were updated only to carry the new serde-defaulted edge-lineage fields.

## 22. Static source delta

Relative to direct parent:

```text
ADD 2
MOD 12
DEL 0
```

Added:

```text
crates/ash_core/src/synapse_contract_r1.rs
crates/ash_core/tests/dk_syn_r1_contract.rs
```

Modified:

```text
crates/ash_core/src/atlas_sft_synapse_binding_candidate.rs
crates/ash_core/src/coactivation_ledger.rs
crates/ash_core/src/hard_negative_replay.rs
crates/ash_core/src/hard_negative_replay_eval.rs
crates/ash_core/src/lib.rs
crates/ash_core/src/path_integral_synapse_router.rs
crates/ash_core/src/replay_hebbian_feedback.rs
crates/ash_core/src/soft_ensemble_composer.rs
crates/ash_core/tests/ash_27_hard_negative_replay_eval.rs
crates/ash_core/tests/ash_27_replay_promotion_gate.rs
crates/ash_core/tests/ash_32_replay_hebbian_feedback.rs
crates/orchestrator_local/tests/ash_27_hard_negative_replay_eval_report.rs
```

No instability-cost store, optimizer kernel, WGPU shader, Muon kernel, or Delta-K GPU performance module is added by R1.

## 23. Code artifacts

Full code-only artifact:

```text
ASH_PASS3_DK_SYN_R1_EDGE_ID_FAIL_CLOSED_SIGNED_BEAM_STATIC_SOURCE_BAKE_CODE_ONLY.zip
SHA-256 6e77d5c78c5948aa27058cde5d0c812bab76233297e84f55ffa16c6622b40959
entries 8,449
```

Overlay artifact:

```text
ASH_PASS3_DK_SYN_R1_EDGE_ID_FAIL_CLOSED_SIGNED_BEAM_STATIC_SOURCE_BAKE_OVERLAY.zip
SHA-256 b1112be4fd00db445aacbdacf2281b34b62f1bcb7b7fff0bea4cd0317404d66c
entries 14
```

Tree digest:

```text
SHA-256 4d053e302cb484036c69704ce27ae71ba9692093d379b329221dd157daf8b3b2
files 8,449
```

Applying the overlay to the direct parent reproduces the full baked source tree byte-for-byte.

## 24. Compile truth

The artifact-construction environment does not provide Cargo/Rustc.

Therefore this source bake does not claim a Rust compile PASS or semantic PASS.

Immediate local gates:

```powershell
cargo check --locked -p ash_core --all-targets
cargo check --locked -p orchestrator_local --all-targets
```

Compiler/test output overrides all static source assumptions.

## 25. Semantic admission requirements

Before the reserved semantic PASS token may be emitted, qualification must verify at minimum:

```text
parallel-edge path identity preservation
ordered edge lineage across coactivation/replay
strict missing-ranker rejection
strict missing-Delta-K rejection
conditional-edge missing-Delta-K rejection
explicit bootstrap distinction
finite negative action accepted end-to-end
deterministic beam output
global optimality remains explicitly unclaimed
no adapter-only canonical path-ID fallback where edge lineage exists
```

## 26. Explicit non-claims

Even after R1 compile/test PASS, this revision does not claim:

```text
path-integral router is the sole production runtime routing SSOT
finite beam is globally optimal
Hebbian instability cost is persisted
Hebbian instability feedback loop is closed
adapter-pair coactivation key uniquely identifies a directed/parallel edge
instability proposal automatically mutates edge weight
```

## 27. Direct successor

```text
DK-SYN-R2

Edge-Identity Hebbian Instability Cost Store
+ Coactivation Ledger Binding
+ Proposal Apply Authority
+ Router Cost Reinjection
+ Snapshot / Commit / Rollback Closure
```

The future store key SHALL be exact `edge_id`, not sorted adapter pair, path ID alone, mean path action, or an evidence-report string.

## 28. Final law

> A synapse path is the ordered traversal of actual registry edges, not merely a sequence of adapters.

> Parallel and directed edges remain distinguishable through route, coactivation, replay, and Hebbian evidence lineage.

> Missing ranker evidence is not ideal ranker evidence.

> Missing Delta-K evidence is not zero Delta-K mismatch.

> Explicit bootstrap is a named authority, not a silent fail-open fallback.

> `-ln(runtime_weight)` is signed. Finite negative edge and path action are legal.

> Finite-width beam routing is deterministic approximate search. Global optimality is not claimed.

> DK-SYN-R1 is complete only when these identity/admission/action/search contracts survive compile and semantic fixtures without reintroducing adapter-only identity or silent evidence fail-open behavior.
