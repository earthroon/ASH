# ASH-BP-DK-POST-CANDIDATE-TARGET-OPTIMIZER-GENERATION-BINDING-CLOSURE-R1

## Status

Implementation-bound closure for the physical N8 first failure:

```text
BpDkPostUpdateFinalizeGenerationDrift
```

The failure was reproduced only after the following boundaries passed in the exact N8 retry:

```text
Fresh Consumer Native CF1 admission                  PASS
Cross-Release Physical N2 admission                  PASS
Immutable N2 / RAM36 exact retry parent authority    PASS
N8 scheduler extension                               PASS
TensorCube Local Muon canonical bridge               PASS
TensorCube Local Muon canonical admission            PASS
```

This revision changes only BP-DeltaK post-candidate optimizer-generation ownership.

## Root cause

The active fusion candidate graph and execution plan are SOURCE-owned evidence.

Current graph identity intentionally contains:

```text
parameter_revision   = SOURCE weight generation
optimizer_generation = SOURCE optimizer generation
bp_generation        = TARGET optimizer step
```

The post-update parameter receipt incorrectly copied:

```text
optimizer_generation = graph.identity.optimizer_generation
```

and the same-source local counterfactual incorrectly copied:

```text
optimizer_generation = plan.identity.optimizer_generation
```

Therefore the post-update ledger staged SOURCE optimizer generation while persistence/finalization used the current TARGET optimizer step.

```text
SOURCE graph / plan
        |
        v
post-update receipt = SOURCE
        |
        v
pending generation  = SOURCE
        |
        v
finalize generation = TARGET
        |
        v
BpDkPostUpdateFinalizeGenerationDrift
```

The finalizer guard is correct and is not relaxed by this revision.

## Authority boundary

### SOURCE-owned

```text
Parameter Pre-Snapshot /
Fusion Candidate Graph /
Fusion Execution Plan /
Deterministic Replay Input /
```

These keep SOURCE optimizer-generation identity.

### TARGET-owned

```text
Post-Update Parameter Receipt /
Same-Source Local Counterfactual Receipt /
Physical Counterfactual Receipt /
Counterfactual Causal-Effect Ledger /
Pending Post-Update Generation /
Finalize Optimizer Generation /
```

These carry TARGET optimizer-generation identity.

## Target SSOT

TARGET is not derived arithmetically.

The production callsite binds:

```rust
let target_optimizer_generation = optimizer_step;
```

Forbidden derivations include:

```text
source_optimizer_generation + 1 /
graph.optimizer_generation + 1 /
plan.optimizer_generation + 1 /
default 0 /
SOURCE-as-TARGET fallback /
```

A non-adjacent fixture `SOURCE=5 / TARGET=13` is required so an accidental `source + 1` implementation cannot pass by coincidence.

## Baked implementation surfaces

### `crates/base_train/src/bp_delta_k_active_fusion_post_update_effectiveness.rs`

`build_post_update_parameter_receipt` now accepts explicit:

```rust
target_optimizer_generation: u64
```

The builder validates the source/target boundary and materializes:

```text
parameter_revision   = graph SOURCE parameter revision
optimizer_generation = explicit TARGET optimizer generation
bp_generation        = graph/plan TARGET BP generation
```

The graph and plan optimizer generations remain SOURCE-owned.

A focused pure boundary validator covers:

```text
SOURCE=5, TARGET=13          PASS
SOURCE=5, TARGET=5           PASS
source graph/plan drift      REJECT
explicit target drift        REJECT
```

### `crates/base_train/src/bp_delta_k_active_fusion_same_source_local_counterfactual.rs`

`build_same_source_local_counterfactual_receipt` now accepts the same explicit TARGET optimizer generation.

It requires:

```text
target_optimizer_generation == plan.identity.bp_generation
```

and materializes:

```text
optimizer_generation = TARGET
bp_generation        = TARGET
```

The plan identity itself remains unchanged.

### `crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs`

The production callsite makes the state boundary explicit:

```text
source_optimizer_generation
    -> graph / plan source evidence

optimizer_step
    -> target_optimizer_generation
    -> post-candidate target state
```

The graph is borrowed only within the builder scope. No graph clone and no hot-path graph mutation are introduced.

Runtime assertions require:

```text
Graph optimizer generation       == SOURCE
Plan optimizer generation        == SOURCE
Graph BP generation              == TARGET
Plan BP generation               == TARGET
Post-update optimizer generation == TARGET
Post-update BP generation        == TARGET
```

When constructed, downstream receipts are also checked:

```text
Same-source counterfactual optimizer/BP generation == TARGET
Physical counterfactual optimizer/BP generation    == TARGET
Causal-effect entry optimizer/BP generation         == TARGET
```

## Downstream propagation remains single-authority

No independent TARGET-generation argument is added to the physical counterfactual builder or causal-effect ledger builder.

Existing propagation remains authoritative:

```text
Same-Source Counterfactual TARGET
        |
        v
Physical Counterfactual TARGET

Post-Update TARGET + Physical Counterfactual TARGET
        |
        v
Causal-Effect Ledger TARGET
```

This avoids creating multiple competing TARGET-generation SSOTs.

## Finalizer preservation

The existing strict guard remains unchanged:

```rust
Some(active) => ensure!(
    active == optimizer_generation,
    "BpDkPostUpdateFinalizeGenerationDrift"
)
```

The repair must make upstream state satisfy this guard.

Forbidden repairs:

```text
No Finalizer Guard Relaxation /
No Generation Mismatch Masking /
No Finalizer Auto-Rebind /
No Pending Generation Override /
```

## Runtime witness

The first staged post-update parameter receipt emits:

```text
[ASH-BP-DK-POST-CANDIDATE-TARGET-OPTIMIZER-GENERATION-BINDING-CLOSURE-R1]
source_optimizer_generation=...
target_optimizer_generation=...
graph_optimizer_generation=...
plan_optimizer_generation=...
post_update_optimizer_generation=...
post_update_bp_generation=...
```

followed by:

```text
PASS_ASH_BASETRAIN_BP_DK_POST_CANDIDATE_TARGET_OPTIMIZER_GENERATION_BINDING_CLOSURE_R1
```

This token claims the generation-binding boundary only. It does not claim N8 completion.

## Static validation

Validator:

```text
tools/validate_ash_bp_dk_post_candidate_target_optimizer_generation_binding_closure_r1_static.py
```

Required checks include:

```text
Explicit TARGET argument in post-update builder /
Post-update receipt TARGET ownership /
Explicit TARGET argument in same-source builder /
Same-source receipt TARGET ownership /
Production callsite TARGET = optimizer_step /
SOURCE graph/plan preservation /
Physical TARGET propagation /
Causal TARGET propagation /
Strict finalizer preservation /
No graph generation mutation /
No plan generation mutation /
SOURCE=5 TARGET=13 fixture /
SOURCE=TARGET fixture /
Target-drift rejection fixture /
Runtime PASS token /
```

Static PASS token:

```text
PASS_ASH_BP_DK_POST_CANDIDATE_TARGET_OPTIMIZER_GENERATION_BINDING_CLOSURE_R1_STATIC
```

## Preserved invariants

```text
No Physical N2 Mutation /
No RAM36 Replacement /
No Muon Registry Rewrite /
No Muon Profile Rewrite /
No Canonical Source-Record Bridge Rewrite /
No Graph Optimizer Generation Rewrite /
No Plan Optimizer Generation Rewrite /
No Replay Identity Mutation /
No Receipt Schema Expansion /
No Sidecar Schema Rewrite /
No Finalizer Guard Relaxation /
No Source-Plus-One Target Inference /
```

## Release rule

The previously sealed binary:

```text
4218b1c19c4f0c6f5d383a14cdb6689827686b3b8c38ee02e1fba980304b83ca
```

remains historical evidence and must not be overwritten.

After this source revision passes local static/compile/tests, build production `base_train` in a fresh target directory, then seal a fresh Consumer Native CF1 and a fresh Cross-Release Physical N2 Compatibility Authority for that new executable.

```text
patched source
    -> fresh release base_train.exe
    -> fresh binary SHA256
    -> fresh Consumer Native CF1
    -> fresh Cross-Release Physical N2 authority
    -> exact N8 retry
```

Physical N2 and RAM36 remain the same immutable parent authorities.

## Exact N8 expected outcome

The next exact N8 must still pass:

```text
Cross-Release Physical N2 admission /
Immutable N2 / RAM36 exact parent gate /
Muon canonical bridge /
Muon canonical admission /
```

It must additionally emit the BP-DeltaK TARGET-generation PASS token and must not fail again with `BpDkPostUpdateFinalizeGenerationDrift`.

If a new failure occurs after that token and after finalization advances, that new failure becomes the next first failure. Closed N2/RAM36/Muon authorities are not reopened without contradictory evidence.

## Non-claims

This revision does not claim:

```text
Exact N8 durable completion /
Durable Muon momentum checkpoint /
Resume authority promotion /
Long-horizon production readiness /
```

It claims only exact closure of SOURCE-to-TARGET optimizer-generation ownership for BP-DeltaK post-candidate state.