# ASH-BASETRAIN-BT-STRUCTURAL-LOOKAHEAD-DECODER-COUPLING-06C-R2

## Atlas-Wave Parallel Update Map / Zero Burn Optimizer Adaptor / Deterministic Wave-Lane Merge / Same-Gradient-Snapshot Candidate Build / Atomic Child-State Commit Seal

> Parent: `BT-STRUCTURAL-LOOKAHEAD-DECODER-COUPLING-06C-R1`
>
> Failure evidence: Burn/WGPU optimizer adaptor recursion overflow at `optimizer.step(...)`
>
> Repair class: training update transport/commit authority
>
> Structural decoder/TensorCube/shared-KV semantics: unchanged
>
> Proof ledger: `HOLD`

## 1. Failure classification

The R1 compile progressed through:

```text
06C authority exports
Burn Module derive
selected block constructor
shared-KV structural forward
Autodiff gradient construction
```

and stopped at Burn's generic optimizer adaptor `Optimizer::step`, where the `Send` requirement recursively expanded through the WGPU core resource graph and overflowed trait evaluation.

R2 does **not** raise Rust recursion limits and does **not** retain Burn `OptimizerAdaptor` in the 06C hot path.

## 2. Atlas-Wave update authority

R2 replaces:

```text
GradientsParams::from_grads
AdamConfig::new().init
optimizer.step
```

with an ASH-local Atlas-Wave Parallel Update Map.

Exactly one raw gradient snapshot is produced by the admitted 06C backward.

The update plan is divided into three waves:

```text
Wave 0: selected_decoder
  input norm
  post-attention norm
  Q/K/V/O projections
  FFN gate/up/down projections

Wave 1: shared_structural
  H1/H2/H3/H4 structural heads
  TensorCube factor projectors

Wave 2: branch_local
  H1/H2/H3/H4 deltaQ projectors per selected layer
  H1/H2/H3/H4 structural gate projectors per selected layer
```

For the current `top-N=1` physical profile this creates three bounded wave groups rather than one monolithic parameter atlas.

## 3. Parallel map semantics

Inside a wave every lane:

```text
reads the same pre-update parameter generation
reads the same raw gradient snapshot
has no dependency on another update lane
builds its own same-device update candidate
```

Candidate rule for R2 V1:

```text
P_candidate = P_parent - learning_rate * dP
```

This is the first simple physical update rule. It is intentionally not labeled Adam.

R2 therefore changes the optimizer receipt identity to:

```text
ASH_ATLAS_WAVE_PARALLEL_MAP_SGD_V1
```

Long-horizon optimizer-state schemes remain a later stage.

## 4. No giant parameter atlas

Required:

```text
monolithic_parameter_atlas=false
```

The map is an Atlas-Wave lane map, not a single concatenated copy of all selected decoder parameters.

This avoids manufacturing a large temporary VRAM allocation merely to bypass the Burn optimizer trait.

## 5. Wave validation before commit

Each lane builds:

```text
gradient energy scalar
candidate parameter energy scalar
```

Within a wave those scalars reduce to one wave-level validation scalar.

Required before any model mutation:

```text
all three wave gradient energies finite
all three wave gradient energies > 0
all three wave candidate energies finite
all target identities/ranks/indexes valid
```

Only after **all waves** pass validation may child-state commit begin.

## 6. Zero-start upstream allowance

The existing zero-start structural gate means first-step gradients for:

```text
TensorCube factor projectors
deltaQ projectors
```

may be absent/zero while the gate has not opened.

R2 permits missing gradient zero-fill only for those explicitly identified zero-start upstream lanes.

It does not permit missing gradients for:

```text
selected decoder parameters
H1-H4 structural prediction heads
structural gate projectors
```

This preserves the R06C first-step bootstrap semantics without fabricating active upstream gradients.

## 7. Deterministic merge

After global wave validation, staged child parameters commit in exact order:

```text
wave_ordinal ascending
then lane_ordinal ascending
```

Required receipt:

```text
deterministic_merge_order = wave_ordinal_then_lane_ordinal
atomic_commit_after_all_wave_validation = true
partial_optimizer_commit_count = 0
```

The update candidates are detached from the first backward graph before becoming the new parameter generation.

## 8. Burn optimizer retirement boundary

Required:

```text
burn_optimizer_adaptor_count=0
GradientsParams call count=0
AdamConfig call count=0
Optimizer::step call count=0
```

This is a targeted 06C update-path retirement only.

It does not remove Burn Autodiff. Burn remains authoritative for:

```text
forward graph
loss graph
backward graph
raw gradient production
```

ASH Atlas-Wave owns only the post-backward parameter update transport and commit.

## 9. Existing 06C invariants preserved

Unchanged:

```text
16x16x4 TensorCube
H1/H2/H3/H4
single canonical K/V per selected layer
zero branch-local KV caches
branch-local deltaQ/deltaC
prediction-only decoder injection
R06A ground truth loss-only
lower frozen boundary
frozen final norm / LM-head parameters
DeltaK branch activity and petrification authority
zero direct structural logit override
zero sampler mutation
zero speculative decode
```

## 10. New policy flags

Required true:

```text
--require-bt-struct-lookahead-atlas-wave-parallel-update-map
--require-bt-struct-lookahead-zero-burn-optimizer-adaptor
--require-bt-struct-lookahead-deterministic-wave-lane-merge
```

Required false:

```text
--allow-bt-struct-lookahead-burn-optimizer-adaptor
```

The R3 single-token-authority repair remains intact in the merged full response file.

## 11. Required runtime receipt

New artifact:

```text
atlas_wave_parallel_update_receipt.json
```

Required fields include:

```text
revision
wave_count
lane_count
parallel_lane_map
same_raw_gradient_snapshot
monolithic_parameter_atlas
burn_optimizer_adaptor_count
deterministic_merge_order
atomic_commit_after_all_wave_validation
per-wave lane map
per-wave total element count
per-wave gradient energy
per-wave candidate energy
missing zero-fill count
receipt digest
```

## 12. Expected terminal evidence

```text
optimizer_step_count=1
burn_optimizer_adaptor_count=0
atlas_wave_parallel_update_map=1
atlas_wave_count=3
atlas_update_lane_count=<runtime>
selected_decoder_parameter_changed=1
structural_gate_parameter_changed=1
```

For current top-N=1 the expected lane families are:

```text
Wave0 selected decoder: 9 lanes
Wave1 shared structural: 4 horizon heads + factor projector lanes
Wave2 branch local: 4 deltaQ + 4 gate lanes
```

Exact Wave1 total depends on the inherited R06B factor manifest and is runtime-derived.

## 13. Compile-error closure target

The R2 patch must remove the compile path that generated:

```text
E0275 overflow evaluating NumericType: Sync
burn::optim::Optimizer::step
```

without adding:

```text
#![recursion_limit]
```

as a workaround.

## 14. Scope

R2 changes:

```text
crates/orchestrator_local/src/base_train_structural_lookahead_decoder_coupling_06c.rs
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c.args
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c_full.args
```

No R01-R06B semantic authority is modified.

## 15. Physical verdict boundary

Static bake can establish code/response closure only.

Physical compile/runtime PASS remains operator-machine evidence.

`proof_ledger=HOLD` remains valid until the R2 Cargo invocation physically completes.
