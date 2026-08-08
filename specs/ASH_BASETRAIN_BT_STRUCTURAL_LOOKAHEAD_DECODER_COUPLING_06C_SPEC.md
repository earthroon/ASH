# ASH-BASETRAIN-BT-STRUCTURAL-LOOKAHEAD-DECODER-COUPLING-06C

## R06B Exact Physical Head Parent / R06A Exact Target Parent / H1·H2·H3·H4 Structural Lookahead / 16×16×4 Cheonjiin TensorCube / QWave Trajectory Binding / Single Canonical Shared K·V Authority / Zero Per-Branch KV Cache / Branch-Local Query Delta / Branch-Local Attention Delta / Prediction-Only Decoder Injection / Zero Ground-Truth Future Injection / Attention-to-FFN Structural Residual Path / Learned Structural Gate / Structural Projection / Top-N Decoder Gradient Admission / Base Lower-Layer Freeze Boundary / Structural Head + TensorCube + Gate + Selected Decoder Joint Gradient / ΔK Branch Activity Trigger / Repeated-Low-ΔK Petrification / TensorCube Sparse Residency / Soft·Hard Petrification State / Canonical Shared-KV Immunity / Branch-Local Delta Eviction / Hysteretic Wake Threshold / Structural-Pressure Rehydration / Periodic Probe Recovery / No Low-ΔK Falsehood Semantics / No Permanent Branch Deletion / Residency Thrash Guard / VRAM Benefit Receipt / Frozen LM-Head Parameter Authority / Canonical LM Loss Preservation / Zero Direct Structural Logit Override / Zero Sampler Mutation / Zero Decode Prior Yet / Causal Future-Support Seal

> Revision: `BT-STRUCTURAL-LOOKAHEAD-DECODER-COUPLING-06C`
>
> Parent head SSOT: `BT-STRUCTURAL-MEDUSA-HEADS-06B` physical PASS
>
> Parent target SSOT: `BT-STRUCTURAL-MEDUSA-TARGETS-06A` physical PASS
>
> Observed R06B authority: `c3e94ef26782266e7c4a3483a7b777472aa6544d9954e4f59f1499d2da19a25c`
>
> Observed R06A authority: `f3cd207c0cc0754a3973bc9284773035158f8b762d08b28b0b91ab3488313a54`
>
> Expanded local specification SHA256: `959246ed4319e70fb1da3dcc7abb2b5de3f44debbf3dd64f3c79e7a0d2621716`
>
> Proof ledger: `HOLD`

---

# 1. Goal

R06C is the first Korean structural stage that lets predicted future structure alter the decoder itself.

```text
causal selected-layer hidden
  -> H1/H2/H3/H4 structural predictions
  -> factor projectors
  -> TensorCube [16,16,4]
  -> branch-local deltaQ
  -> four branch attentions over one canonical K_base/V_base
  -> deltaC_h = C_h - C_base
  -> zero-start learned gates
  -> structural residual before FFN
```

R06A ground truth is loss-only. It is never a decoder-forward input.

---

# 2. Exact lower-boundary ownership

Current physical profile uses the 22-layer checkpoint with `top-N=1`.

```text
lower frozen layers = 21
selected trainable layer = 21
```

R6R9C9 captures the exact hidden entering the selected layer. Because `TrainingBackend = Autodiff<InferenceBackend>`, R06C wraps the captured WGPU tensor using `Tensor::from_inner`.

Required:

```text
lower_boundary_host_bridge_count=0
lower_boundary_autodiff_from_inner_count=1
lower_layer_gradient_buffer_count=0
lower_layer_parameter_update_count=0
```

No CPU hidden shuttle is admitted at the trainable boundary.

---

# 3. TensorCube

Logical TensorCube geometry is fixed:

```text
[Horizon=4, Y=16, X=16]

slab 0 = H1 / +1
slab 1 = H2 / +2
slab 2 = H3 / +3
slab 3 = H4 / +4
```

Each slab is produced only from predicted factor surfaces inherited from R06B:

```text
Hangul presence/count/descriptor
CJI18
QWLocal12
QWEdge10
```

Each factor has an independent learned projection into the 256-value slab space. Target values and target occupancy masks do not enter TensorCube forward math.

---

# 4. One canonical K/V authority

For every selected decoder layer, canonical projections are computed once:

```text
Q_base = Wq(x_norm)
K_base = Wk(x_norm)
V_base = Wv(x_norm)
```

All four horizons use the exact same `K_base` and `V_base` identities.

Required:

```text
canonical_q_projection_count_per_selected_layer=1
canonical_k_projection_count_per_selected_layer=1
canonical_v_projection_count_per_selected_layer=1

branch_kv_cache_count=0
branch_kv_clone_count=0
branch_kv_materialization_count=0
branch_kv_persistent_buffer_count=0
branch_kv_authority_count=0
branch_kv_mutation_count=0
```

No `K_H1/V_H1 ... K_H4/V_H4` authority exists.

---

# 5. Branch-local delta

Each horizon produces only an ephemeral query correction:

```text
deltaQ_h = P_deltaQ_h(T_h)
Q_h = Q_base + deltaQ_h
C_h = Attention(Q_h, K_base, V_base, canonical_causal_mask)
deltaC_h = C_h - C_base
```

The four branches are different views over the same memory, not four memories.

The exact canonical causal mask is reused. Predicting H+1..H+4 never grants attention to future token positions.

---

# 6. Structural residual and zero-start gate

For each layer/horizon:

```text
g_lh = learned gate(T_h)
```

Gate terminal weights start at exact zero. Therefore the first coupled forward is a structural no-op at the residual boundary.

```text
R_struct = sum_h g_lh * deltaC_h
```

The base attention path remains explicit and the structural correction enters before the subsequent FFN path. Hidden width is unchanged.

Because a mathematically exact zero gate blocks upstream structural-residual gradients on step 1, the first physical gate requires finite/nonzero gradients for:

```text
selected decoder
structural prediction head
structural gate
```

while TensorCube/deltaQ upstream-gradient activation is a multi-step 06D proof. This is recorded as `zero_start_gate_bootstrap`; 06C must not fabricate a nonzero TensorCube gradient claim on step 1.

---

# 7. Training objective

R06C preserves canonical LM training and adds structural auxiliary loss.

First physical V1 uses the dependency-stable Burn 0.20.0 surface:

```text
Hangul presence/count/descriptor: masked MSE
CJI18: masked MSE
QWLocal12 non-phase: masked MSE
QWLocal12 phase: 1 - cos(pred-target)
QWEdge10 non-phase: masked MSE
QWEdge10 phase-delta: 1 - cos(pred-target)
```

Current profile:

```text
lambda_lm = 1.0
lambda_struct = 0.1
optimizer = Adam
learning_rate = 1e-6
optimizer_step_count = 1
```

The LM-head parameter and final RMSNorm parameter are frozen. Structural information may influence ordinary logits only through the coupled hidden state. Direct structural vocab bias/prior is forbidden.

---

# 8. Gradient/update boundary

Trainable child namespaces:

```text
selected top-N decoder block(s)
Structural Medusa head bank
TensorCube factor projectors
TensorCube deltaQ projectors
structural gates
```

Frozen:

```text
lower decoder blocks
final RMSNorm parameters
LM-head parameters
tokenizer
R01-R06A structural/target authorities
```

Before optimizer commit, selected decoder/head/gate gradients are explicitly checked for finite values and nonzero support. One Adam step then creates the R06C child state.

No checkpoint file is committed by this first gate.

---

# 9. ΔK branch activity trigger

ΔK is an execution/residency pressure signal only.

```text
low ΔK != false
low ΔK != wrong target
low ΔK != permanent prune

low ΔK = insufficient recent evidence that continuous branch execution/residency is worth its cost
```

Configured activity revision:

```text
ash_delta_k_branch_activity_gate_deltaq_tensorcube_i_times_m2_v1
```

with explicit `I * M^2` branch activity score.

No numerical ΔK formula may become authority unless its exact revision and thresholds are bound in the CLI/manifest.

---

# 10. Petrification state machine

Every logical horizon branch remains part of TensorCube and moves through:

```text
Active
  -> Cooling
  -> SoftPetrified
  -> HardPetrified
  -> Rehydrating
  -> Active
```

One low observation never petrifies a branch. Admission requires EMA, minimum observation count, repeated-low streak, minimum residency window, and hysteresis.

Required:

```text
T_wake > T_sleep
```

Transition budgets and cooldowns guard against residency thrash.

There is no Deleted/PrunedForever state.

---

# 11. Soft and hard petrification

Soft petrification may release only branch-local working state:

```text
TensorCube slab workspace
deltaQ workspace
branch context
deltaC
branch reduction scratch
backward tape after completion
```

Branch parameters remain GPU-resident.

Hard petrification may additionally offload eligible branch-local parameter pages, but only after measured VRAM benefit, exact current child-generation backing, optimizer-state preservation, and active-consumer reference checks.

First pass69 physical profile sets:

```text
hard_petrification_enabled=false
```

Therefore hard-eviction VRAM benefit remains `HOLD` until measured. R06C does not claim bytes saved that were not physically observed.

---

# 12. Canonical shared-KV immunity

The petrification controller may never evict or reinterpret:

```text
K_base
V_base
Wk
Wv
canonical causal mask
canonical base attention authority
```

Required all zero:

```text
canonical_k_petrification_attempt_count
canonical_v_petrification_attempt_count
canonical_wk_eviction_by_branch_policy_count
canonical_wv_eviction_by_branch_policy_count
```

---

# 13. Wake and recovery

A petrified branch cannot depend solely on its own unavailable execution score. Wake pressure may come from predicted-only sibling/trajectory evidence:

```text
neighbor horizon activity
CJI trajectory change
QWave trajectory change
hidden change pressure
selected-layer gradient pressure
periodic probe
```

R06A ground truth cannot be a live wake trigger.

Periodic probes are diagnostic by default and contribute zero decoder residual until a branch is formally rehydrated.

`Rehydrating -> Active` requires parameter digest/generation, device epoch, finite preflight, and shared-K/V identity validation.

---

# 14. First physical residency profile

Pass69 starts all four horizon branches Active and physically exercises the state-machine path:

```text
repeated low score -> Cooling -> SoftPetrified
wake pressure -> Rehydrating
validation -> Active
```

It does not force live hard parameter eviction merely to manufacture evidence.

Expected:

```text
initial_active_branch_count=4
single_low_delta_k_instant_petrify_count=0
permanent_branch_delete_count=0
shared_kv_petrification_immunity=1
actual_branch_local_vram_released=0 unless a real live residency event occurs
```

---

# 15. No target leakage / no decode authority

Required zero:

```text
ground_truth_future_decoder_binding_count
target_mask_forward_binding_count
target_token_id_forward_binding_count
future_text_forward_binding_count
future_token_attention_visibility_count

direct_structural_logit_override_count
structural_vocab_prior_count
sampler_mutation_count
token_selection_mutation_count
speculative_decode_count
decode_kv_cache_count
```

R06A targets are loss-only.

---

# 16. Code surface

Pass69 changes exactly these nine paths relative to pass68R3:

```text
crates/model_core/src/base_train_structural_lookahead_decoder_coupling_authority.rs
crates/model_core/src/lib.rs
crates/model_core/src/model_layers.rs
crates/orchestrator_local/Cargo.toml
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r9_c9_progressive_n_layer_wave_advancement.rs
crates/orchestrator_local/src/base_train_structural_lookahead_decoder_coupling_06c.rs
crates/orchestrator_local/src/bin/ash_basetrain_structural_lookahead_decoder_coupling_06c_gate.rs
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c.args
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c_full.args
```

The full response file preserves the R3 single-token-authority repair: generic `--token-ids`, `--row-valid-lengths`, and `--position-ids` are absent.

---

# 17. Static bake evidence

```text
static closure = 67/67 PASS
full file count = 6929
overlay file count = 9
full ZIP CRC = PASS
overlay ZIP CRC = PASS
overlay/full changed-file byte mismatch = 0
forbidden .md/.sha256/artifacts/manifests inside ZIP = 0
```

Artifact SHA256:

```text
full = 283709fcd8d9b38b23fc2d2c6dd09afee02033880b61c575ca9eb3c16bbd9a41
overlay = 8d5e3e4635bc604e8fe07be418209689ba5834d9fa83d54e49c70166ae98baca
expanded spec = 959246ed4319e70fb1da3dcc7abb2b5de3f44debbf3dd64f3c79e7a0d2621716
```

Rust compiler execution was not available in the bake environment. Physical compile/runtime PASS therefore remains pending the operator machine.

---

# 18. Cargo run

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_structural_lookahead_decoder_coupling_06c_gate `
  -- "@specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c_full.args"
```

---

# 19. Physical PASS meaning

A physical PASS proves one causal coupled training step with:

```text
R06B/R06A exact parents
same-device detached lower boundary
16×16×4 TensorCube
one shared canonical K/V per selected layer
four branch-local deltaQ/deltaC paths
zero branch KV cache/clone/authority
zero target-forward leakage
selected decoder + structural head + zero-start gate gradient admission
one optimizer step
frozen lower stack/final norm/LM-head authority
ΔK low-streak/Cooling/SoftPetrified/Rehydrating/Active recovery state machine
shared-KV petrification immunity
zero direct logit/sampler/decode authority
```

It does not prove long-horizon training stability, useful structural prediction quality, hard-petrification VRAM savings, or decode-time benefit.

Natural next stage: `ASH-BASETRAIN-BT-STRUCTURAL-LOOKAHEAD-TRAIN-STABILITY-06D`.