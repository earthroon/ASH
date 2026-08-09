# ASH-BASETRAIN-BT-WGSL-STRUCTURAL-DELTAQ-GATE-PROJECTOR-BACKWARD-06C-R17

## Revision identity

```text
Patch ID: ASH-BASETRAIN-BT-WGSL-STRUCTURAL-DELTAQ-GATE-PROJECTOR-BACKWARD-06C-R17
Build revision: bt-wgsl-structural-deltaq-gate-projector-backward-06c-r17
Physical parent: ASH-BASETRAIN-BT-WGSL-TENSORCUBE-BACKWARD-MATMUL-ACCELERATION-06C-R16
Proof ledger: HOLD
```

## One-line SSOT

R17 consumes the four actual `dDeltaQ` and four actual `dGate` carriers preserved through R14-R16, applies no RoPE transform to DeltaQ because the structural projector output already lives directly in the post-RoPE additive Q space, computes exact backward through the four horizon-local DeltaQ projectors and the retained-sigmoid `2*sigmoid(z)-1` Gate transform/projectors, publishes structural projection parameter-gradient tiles, deterministically merges DeltaQ-side and Gate-side source gradients into four canonical `dStructuralCube_H1..H4` authorities, and stops there. Factor-projector, horizon fused-head, prepared-block residual backward, and the final structural/base input-gradient merge remain R18 authority.

## Parent authority

Required same-invocation parent state:

```text
r16_physical_parent = 1
r16_tensorcube_backward_compute_authority = 1
r16_base_decoder_dinput_authority = 1
base_forward_tape_owner_pins = 16
structural_deltaq_carrier_count = 4
structural_gate_carrier_count = 4
```

R16 `dInputHiddenTotal` is preserved as the already-closed base decoder path authority. R17 does not reinterpret it as including structural branch source gradients.

## Exact structural forward boundary

```text
prepared_block.residual
  -> horizon fused head Hh
  -> factor slices
  -> factor projectors
  -> sum
  -> Structural Cube Hh [B,Q,256]
       |                         |
       v                         v
  DeltaQ projector          Gate projector
  [2048,256]                [1,256]
       |                         |
       v                         v
  DeltaQ [B,Q,2048]         z_gate
       |                         |
  reshape BQHD               sigmoid
       |                         |
       v                      *2 - 1
  q_base_post_rope + DeltaQ      |
                                 v
                               Gate
```

R17 reverses only the boundary from `Structural Cube` through the DeltaQ and Gate projectors.

## Structural forward tape extension

Each horizon retains read-only GPU evidence:

```text
structural_cube                [B,Q,256]
gate_sigmoid                   [B,Q,1]
deltaq_projector_weight        [2048,256]
gate_projector_weight          [1,256]
deltaq_weight_identity
gate_weight_identity
delta_q_post_rope              [B,Q,32,64]
gate                            [B,Q,1]
```

The Gate forward is captured without semantic change as:

```text
z_h = GateProjector_h(cube_h)
s_h = sigmoid(z_h)
gate_h = 2*s_h - 1
```

Production backward reuses retained `s_h`; sigmoid recomputation is forbidden.

### Allocator ownership

Per horizon, six Burn-origin tensors remain owner-pinned until R17 completion:

```text
structural_cube
gate_sigmoid
delta_q_post_rope
gate
deltaq_projector_weight
gate_projector_weight
```

Thus:

```text
structural_projection_owner_pins_per_horizon = 6
horizon_count = 4
structural_projection_owner_pin_count = 24
base_forward_owner_pin_count = 16
owner_release_before_r17_completion = 0
```

## Projector identities

Per horizon:

```text
W_delta_h = [2048,256]
bias = none
W_gate_h = [1,256]
bias = none
```

DeltaQ weights preserve the existing deterministic `ash.06c.deltaq` seed identity. Current Gate weights are independently allocated zero-weight tensors. Equal Gate values do not imply parameter aliasing.

## DeltaQ projector backward

DeltaQ is defined directly in post-RoPE additive Q space:

```text
Cube_h [M,256]
WDelta_h [2048,256]
DeltaQ_h = Cube_h * WDelta_h^T
M = B*Q = 32
```

R17 treats actual `dDeltaQ_Hh [B,Q,32,64]` as a zero-copy `[32,2048]` linear-output gradient view. It performs no inverse RoPE, no head remap, and no second attention scale.

Exact backward:

```text
dCubeFromDeltaQ_h = dDeltaQ_h * WDelta_h
dWDelta_h = dDeltaQ_h^T * Cube_h
```

Current shapes:

```text
dCubeFromDeltaQ_h = [32,256]
dWDelta_h = [2048,256]
```

The admitted 1024-output-row R13 tile policy gives two DeltaQ dW tiles per horizon, eight total.

## Gate transfer and projector backward

The exact actual-chain `dGate_Hh` carrier is consumed without regeneration.

Forward:

```text
s = sigmoid(z)
g = 2*s - 1
```

Exact retained-sigmoid VJP:

```text
dZ = dGate * 2*s*(1-s)
```

Gate linear backward:

```text
ZGate_h = Cube_h * WGate_h^T
dCubeFromGate_h = dZ_h * WGate_h
dWGate_h = dZ_h^T * Cube_h
```

Current shapes:

```text
dCubeFromGate_h = [32,256]
dWGate_h = [1,256]
```

One Gate dW tile is published per horizon, four total.

## Current zero Gate-weight semantics

Current physical parent constructs:

```text
WGate_h[:] = 0
bias = none
```

R17 must verify the actual retained Gate weight against an explicit GPU zero buffer with exact same-device parity.

Therefore current semantics are:

```text
z = 0
s = 0.5
g = 0
dZ = 0.5*dGate
dCubeFromGate = 0
```

`dWGate` remains separately valid and may be nonzero. Zero Gate-source gradient is an observation, not a failure.

## Structural source merge

For each horizon:

```text
dStructuralCube_h = dCubeFromDeltaQ_h + dCubeFromGate_h
```

Canonical order is fixed:

```text
DELTAQ -> GATE
```

The admitted deterministic R13 Add2 executor is reused. R17 publishes exactly four canonical `[B,Q,256]` structural source-gradient authorities:

```text
dStructuralCube_H1
dStructuralCube_H2
dStructuralCube_H3
dStructuralCube_H4
```

## Linear executor authority

The eight new structural projection roles are established with the physically admitted R13 semantic linear backward executor:

```text
DELTAQ_H1..H4
GATE_H1..H4
```

R16 TensorCube authority remains unchanged and limited to the seven already-promoted roles:

```text
DOWN
GATE_FFN
UP
OPROJ
Q
K
V
```

R17 performs zero automatic TensorCube role escalation. Structural TensorCube promotion requires a separate exact-parity admission after R17 semantics exist.

## Oracles

R17 includes isolated synthetic validation that cannot become production gradient authority.

### DeltaQ linear CPU-f64 oracle

A nonzero fixture compares the R13 GPU semantic executor against CPU f64 for:

```text
dCube = dY * W
dW = dY^T * Cube
```

### Gate CPU-f64 oracle

A nonzero Gate fixture checks:

```text
dZ = dG * 2*s*(1-s)
dCube = dZ * W
dW = dZ^T * Cube
```

### Gate directional finite difference

For:

```text
L(Cube,W) = <dG, 2*sigmoid(Cube*W^T)-1>
```

central finite differences independently validate Cube and Weight directions.

### Zero-weight Gate oracle

An isolated zero-weight fixture must prove:

```text
dCube = exact zero
dW may be nonzero
```

### Nonzero-weight future canary

A separate nonzero-weight fixture must prove `dCubeFromGate` can be nonzero. This prevents a hardcoded-zero implementation from passing the current zero-weight parent.

## Zero and fail-closed policy

There is intentionally no `BTR17GradientZero` failure. Production carrier, parameter, or structural source gradients may be zero if finite, complete, correctly covered, correctly bound, oracle-validated, and reproducible.

Forbidden:

```text
NaN/Inf clamp
gradient clamp
silent row zeroing
gradient fabrication
sigma/log/lambda amplification
silent numerical fallback
```

Any production nonfinite blocks publication.

## Production readback boundary

Production payload readback remains zero for structural cube, `dDeltaQ`, `dGate`, Gate preactivation gradient, DeltaQ/Gate cube gradients, merged structural cube gradients, and projector dW tiles. Only compact status, exact-parity counters, lifecycle counters, and digests may cross to host. Synthetic oracle readback is isolated.

## Micro-Atlas lifecycle

The reused R13 projector backward path preserves:

```text
PLANNED -> RESIDENT -> DISPATCHED -> GPU_COMPLETED
-> COMMITTED -> GC_ELIGIBLE -> RELEASED
```

Required:

```text
commit_before_gc = 1
premature_release = 0
orphan_page = 0
payload_copy = 0
host_shuttle = 0
```

## Double-run reproducibility

The complete R17 structural projector chain executes twice. GPU exact parity compares all four horizons for:

```text
dGatePre
dCubeFromDeltaQ
dCubeFromGate
dStructuralCube
DeltaQ dW tiles
Gate dW tiles
```

Required:

```text
reproducibility_runs = 2
reproducibility_match = 1
```

## R17 stopping boundary

R17 explicitly does not execute:

```text
factor projector backward
horizon fused-head backward
factor-slice gradient publication
prepared_block.residual structural backward
base + structural selected-layer input-gradient merge
```

The R16 base-path input gradient is carried unchanged.

## R18 handoff

R17 output packet contains:

```text
layer_index
d_input_hidden_base_path
d_structural_cube_actual[4]
deltaq_weight_gradients[4]
gate_weight_gradients[4]
```

`r18_handoff_ready = 1` means R18 may consume `dStructuralCube_H1..H4`. R18 owns factor-projector backward, fused-factor gradient reassembly, horizon fused-head backward, horizon structural residual gradients, deterministic horizon merge, and final merge with the preserved base path.

## CLI gates

Exactly 52 R17 keys are required exactly once in both canonical response templates and regenerated `resolved.args`:

```text
--require-bt-wgsl-r17-r16-physical-parent
--require-bt-wgsl-r17-r16-tensorcube-authority-preserved
--require-bt-wgsl-r17-r16-dinput-base-path-preserved
--require-bt-wgsl-r17-structural-carrier-exact-handoff
--require-bt-wgsl-r17-four-horizon-order
--require-bt-wgsl-r17-structural-projection-tape
--require-bt-wgsl-r17-structural-owner-pins
--require-bt-wgsl-r17-deltaq-projector-weight-identity
--require-bt-wgsl-r17-gate-projector-weight-identity
--require-bt-wgsl-r17-zero-gate-weight-parent-binding
--require-bt-wgsl-r17-deltaq-post-rope-direct-layout
--require-bt-wgsl-r17-zero-structural-rope-backward
--require-bt-wgsl-r17-deltaq-h1-backward
--require-bt-wgsl-r17-deltaq-h2-backward
--require-bt-wgsl-r17-deltaq-h3-backward
--require-bt-wgsl-r17-deltaq-h4-backward
--require-bt-wgsl-r17-gate-transfer-exact-vjp
--require-bt-wgsl-r17-gate-h1-backward
--require-bt-wgsl-r17-gate-h2-backward
--require-bt-wgsl-r17-gate-h3-backward
--require-bt-wgsl-r17-gate-h4-backward
--require-bt-wgsl-r17-deltaq-weight-gradient-tiles
--require-bt-wgsl-r17-gate-weight-gradient-tiles
--require-bt-wgsl-r17-zero-projection-bias-gradient
--require-bt-wgsl-r17-deltaq-gate-source-deterministic-merge
--require-bt-wgsl-r17-four-source-gradient-publication
--require-bt-wgsl-r17-r13-linear-semantic-authority
--require-bt-wgsl-r17-zero-structural-tensorcube-role-escalation
--require-bt-wgsl-r17-r16-linear-authority-unchanged
--require-bt-wgsl-r17-current-zero-gate-source-observation
--require-bt-wgsl-r17-zero-observation-not-failure
--require-bt-wgsl-r17-gate-cpu-f64-oracle
--require-bt-wgsl-r17-gate-directional-finite-difference
--require-bt-wgsl-r17-deltaq-linear-oracle
--require-bt-wgsl-r17-gate-zero-weight-oracle
--require-bt-wgsl-r17-gate-nonzero-weight-future-canary
--require-bt-wgsl-r17-fail-closed-numerics
--require-bt-wgsl-r17-production-payload-readback-zero
--require-bt-wgsl-r17-micro-atlas-lifecycle-preserved
--require-bt-wgsl-r17-zero-forward-recompute
--require-bt-wgsl-r17-zero-checkpoint-reopen
--require-bt-wgsl-r17-zero-decoder-clone
--require-bt-wgsl-r17-zero-factor-projector-backward
--require-bt-wgsl-r17-zero-horizon-head-backward
--require-bt-wgsl-r17-zero-structural-source-residual-merge
--require-bt-wgsl-r17-zero-gradient-atlas
--require-bt-wgsl-r17-zero-optimizer
--require-bt-wgsl-r17-zero-weight-mutation
--require-bt-wgsl-r17-final-loss-authority-deferred
--require-bt-wgsl-r17-atlas-wave-streaming-receipt
--require-bt-wgsl-r17-zero-monolithic-final-json
--require-bt-wgsl-r17-double-run-reproducibility
```

The resolved-args repair utility fails closed on stale pre-R17 response files and validates exact one-time cardinality for all 52 keys.

## Atlas receipt

R17 final receipt uses seven ordered waves with parallel lane construction and deterministic streaming merge:

```text
wave ordinal -> lane ordinal -> lexicographic key
receipt_atlas_waves = 7
parallel_receipt_lane_build = 1
streaming_receipt_merge = 1
deterministic_receipt_merge = 1
monolithic_final_json = 0
```

## Source surface

Relative to the R16 REBAKED parent, R17 changes exactly eight files:

```text
ADD crates/burn_webgpu_backend/src/base_train_r17_structural_projector_backward.rs
ADD crates/burn_webgpu_backend/src/shaders/base_train_r17_gate_transfer_backward.wgsl
MOD crates/burn_webgpu_backend/src/lib.rs
MOD crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r8_layer1_live_body.rs
MOD crates/orchestrator_local/src/base_train_structural_lookahead_decoder_coupling_06c.rs
MOD specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c.args
MOD specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c_full.args
MOD tools/repair_r13r2r2_resolved_args.ps1
```

The forward-execution modification is mandatory for exact structural cube, retained sigmoid, output, projector weight, and allocator-owner lifetime authority.

## Physical verification boundary

The bake environment has no Cargo/rustc or physical WGPU adapter. Static source, gate-cardinality, archive, and structural checks are bake authority only. Rust/WGSL compilation, 24 structural owner pins, Gate zero-weight GPU parity, four DeltaQ projector backward paths, four Gate backward paths, 12 dW tiles, four `dStructuralCube` publications, synthetic GPU/CPU oracles, double-run exact parity, and the final R17 PASS token remain operator-machine physical authority.

## Expected terminal summary

```text
[bt-wgsl-structural-deltaq-gate-projector-backward-06c-r17]
r16_physical_parent=1
r16_tensorcube_authority_preserved=1
r16_dinput_base_path_preserved=1
horizon_count=4
deltaq_carriers_adopted=4
gate_carriers_adopted=4
base_forward_owner_pins=16
structural_projection_owner_pins=24
structural_cube_tapes=4
gate_sigmoid_tapes=4
deltaq_projector_count=4
gate_projector_count=4
deltaq_weight_alias=0
gate_weight_alias=0
gate_parent_zero_weight=1
deltaq_post_rope_direct_layout=1
structural_rope_backward=0
deltaq_projector_backward_count=4
gate_transfer_vjp_count=4
gate_projector_backward_count=4
deltaq_dw_tiles=8
gate_dw_tiles=4
structural_projection_dw_tiles=12
projection_bias_gradient_count=0
dstructural_cube_delta_published=4
dstructural_cube_gate_published=4
dstructural_cube_total_published=4
source_merge_order_deltaq_then_gate=1
current_gate_source_gradient_zero_observed=1
factor_projector_backward=0
horizon_head_backward=0
structural_residual_merge=0
r13_linear_semantic_executor=1
structural_tensorcube_role_adoption=0
deltaq_cpu_f64_oracle=1
gate_cpu_f64_oracle=1
gate_directional_finite_difference=1
gate_zero_weight_oracle=1
gate_nonzero_weight_future_canary=1
micro_atlas_lifecycle=1
page_commit_before_gc=1
premature_release=0
orphan_page=0
production_gradient_payload_readback=0
production_weight_payload_readback=0
forward_recompute=0
checkpoint_reopen=0
decoder_clone=0
gradient_atlas=0
optimizer=0
weight_mutation=0
final_loss_authority=0
dfinal_deterministic_fixture_lineage=1
reproducibility_runs=2
reproducibility_match=1
r18_handoff_ready=1
receipt_atlas_waves=7
parallel_receipt_lane_build=1
streaming_receipt_merge=1
deterministic_receipt_merge=1
monolithic_final_json=0
proof_ledger=HOLD
```

## PASS seal

```text
PASS_ASH_BASETRAIN_BT_WGSL_STRUCTURAL_DELTAQ_GATE_PROJECTOR_BACKWARD_06C_R17
```

## Final SSOT

R17 is the first consumer of the preserved structural branch gradient carriers and closes only the horizon-local DeltaQ/Gate projection boundary. DeltaQ remains in its direct post-RoPE additive space; Gate uses retained sigmoid for exact VJP. Current zero Gate weights correctly yield zero Gate-to-Cube source gradients while independent parameter gradients remain valid, and nonzero synthetic evidence prevents a hardcoded-zero implementation. Four DeltaQ-side and Gate-side source derivatives merge in deterministic DeltaQ-then-Gate order into canonical `dStructuralCube_H1..H4`. R16 base-path input gradient stays unchanged. Factor/projector/head/residual propagation and the complete base+structural selected-layer input-gradient authority remain R18-only.