# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R12

## Causal Loss Backward Seed / Logit Gradient Surface

> Parent SSOT: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R11` physical PASS
> Parent loss authority: `ForwardLossAuthoritySlot` Resident
> Parent logits authority: `LogitSurfaceAuthoritySlot` Resident
> Parent target authority: `R6R11CausalTargetShiftAuthority`
> Canonical output: one GPU-resident `LogitGradientSurfaceAuthoritySlot [B,Q,V]`
> Upstream loss seed: `1.0`
> Mean-loss scale: `1 / N_valid`
> Full softmax surface: forbidden
> Full second BQV reference gradient: forbidden
> LM-head / final RMSNorm / decoder backward: blocked
> Optimizer / weight mutation / production inference: blocked
> Proof ledger: HOLD

---

# 1. Goal

R6-R12 is the first true backward state transition in the BaseTrain chain. It consumes the exact canonical forward loss admitted by R6-R11 and the exact canonical logit surface admitted by R6-R10, reuses the already admitted R6-R11 causal target map, and publishes only `dL/dlogits`.

It does not recompute forward loss, logits, final RMSNorm, LM-head projection, hidden state, or decoder output.

Canonical flow:

```text
R6-R11 ForwardLossAuthority exact lease
        +
R6-R10 LogitSurfaceAuthority exact lease
        +
R6-R11 CausalTargetShiftAuthority exact reuse
        ↓
unit loss seed = 1.0
        ↓
mean scale = 1 / N_valid
        ↓
stable row softmax normalizer
        ↓
(softmax - one_hot) / N_valid
        ↓
private zero-initialized full [B,Q,V] gradient
        ↓
per-wave independent GPU reference parity
        ↓
coverage + masked-zero + finite + row-sum audits
        ↓
ONE LogitGradientSurfaceAuthoritySlot adoption
```

---

# 2. Mathematical contract

For every valid causal target row `i` with logits `z_i` and target token `y_i`:

```text
m_i = max_v z_i[v]
p_i[v] = exp(z_i[v] - m_i) / sum_u exp(z_i[u] - m_i)
L = (1/N_valid) * sum_i NLL_i
```

R6-R12 fixes:

```text
dL/dL = 1.0
```

Therefore:

```text
dL/dz_i[v] = (p_i[v] - 1[v=y_i]) / N_valid
```

Any `(b,q)` row absent from the admitted R6-R11 target authority has:

```text
dL/dz[b,q,v] = 0
```

for every vocabulary column.

No dynamic loss scaling, gradient clipping, or accumulation is admitted in R6-R12.

---

# 3. Current physical fixture expectations

The admitted R6-R11 parent observed:

```text
B=1
Q=32
V=48259
BQV=1544288
N_valid=31
```

Expected current-domain observations:

```text
valid_gradient_scalars = 31 * 48259 = 1496029
masked_zero_scalars     = 48259
target_upload_bytes     = 31 * 8 = 248
```

The final `q=31` row has no admitted next-token target and must remain exact zero across all 48,259 vocabulary columns.

These values are fixture observations, not architectural constants. Runtime code derives all counts from live B/Q/V and target authority.

---

# 4. Parent execution ownership

The physical gate invokes R6-R12 once. R6-R12 invokes one R6-R11 parent session. R6-R11 continues to own its single R6-R10 parent invocation.

Required:

```text
R6-R11 parent session count = 1
R6-R12 backward-seed execution count = 1
```

R6-R12 must not separately rerun R6-R10, R6-R11, decoder execution, final RMSNorm, or LM-head projection.

---

# 5. Forward-loss exact lease

R6-R12 acquires exactly one `ForwardLossExecutionLease`.

Exact binding includes:

```text
forward-loss pointer digest
checkpoint set digest
source logit pointer digest
source logit completion token
input sequence authority digest
target-shift authority digest
valid target count
reduction plan digest
loss-sum buffer identity
mean-loss buffer identity
loss completion token
publication generation
writer id
operation id
```

Required lease lifecycle:

```text
before active leases = 0
acquire count = 1
during active leases = 1
after active leases = 0
slot remains Resident
```

The numerical mean-loss payload is not needed for differentiation and is not read back by R6-R12.

---

# 6. Mean-loss policy binding

R6-R12 proves that its parent loss was the admitted mean loss, not a sum loss.

Required parent facts:

```text
canonical_loss_publication_count = 1
label_smoothing = 0
valid_target_count = gpu_valid_target_count
loss policy digest matches the R6-R11 fixed policy
```

Backward seed authority:

```rust
pub struct R6R12LossBackwardSeedAuthority {
    pub schema_version: u32,
    pub source_forward_loss_pointer_digest: String,
    pub source_forward_loss_completion_token_digest: String,
    pub source_logit_pointer_digest: String,
    pub target_shift_authority_digest: String,
    pub valid_target_count: u32,
    pub upstream_seed_bits: u32,
    pub mean_scale_bits: u32,
    pub seed_mode: String,
    pub authority_digest: String,
}
```

Canonical values:

```text
upstream_seed = 1.0f32
mean_scale = 1.0f32 / N_valid
seed_mode = unit_seed_mean_loss
```

No CLI seed override or dynamic scale fallback is allowed.

---

# 7. Canonical logit exact lease

R6-R12 acquires exactly one `LogitSurfaceExecutionLease` from the canonical R6-R10 logit slot exposed through typed R6-R11 accessors.

Required:

```text
logit pointer == forward-loss source logit pointer
logit completion == forward-loss source logit completion
shape == parent R6-R11 BQV shape
scalar count == checked(B*Q*V)
```

The logits buffer remains read-only and unchanged before/after R6-R12.

Required:

```text
logit mutation = 0
logit republication = 0
logit payload readback = 0
```

---

# 8. Target authority exact reuse

R6-R12 reuses `R6R11CausalTargetShiftAuthority` directly.

It must not rebuild targets from token IDs, reparse CLI token IDs, rerun tokenizer/frontend logic, or invent a terminal target.

Integrity verification includes:

```text
entries.len == valid_target_count
entries_digest exact
ordinals contiguous
flat logit row indices unique and < B*Q
target token id < V
query+1 < admitted row valid length
source_next_token_flat_index == flat_logit_row_index + 1
```

The target authority digest must equal both the R6-R11 receipt target digest and the forward-loss pointer target digest.

The compact target GPU representation may be uploaded again because the R6-R11 upload was operation-private. Packed entry remains:

```text
u32 flat_logit_row_index
u32 target_token_id
```

so target upload bytes are `N_valid * 8`.

---

# 9. Canonical gradient state

New model-core state domain:

```text
LogitGradientSurfaceAuthoritySlot
```

Recommended state:

```rust
pub enum LogitGradientSurfaceAuthorityState {
    Vacant,
    Resident,
}
```

Recommended pointer:

```rust
pub struct LogitGradientSurfaceAuthorityPointer {
    pub schema_version: u32,
    pub checkpoint_set_digest: String,
    pub source_forward_loss_pointer_digest: String,
    pub source_forward_loss_completion_token_digest: String,
    pub source_logit_pointer_digest: String,
    pub source_logit_completion_token_digest: String,
    pub target_shift_authority_digest: String,
    pub backward_seed_authority_digest: String,
    pub shape_bqv: [u32; 3],
    pub scalar_count: u64,
    pub valid_target_count: u32,
    pub valid_gradient_scalar_count: u64,
    pub masked_zero_scalar_count: u64,
    pub gradient_wave_plan_digest: String,
    pub buffer_identity_digest: String,
    pub completion_token_digest: String,
    pub publication_generation: u64,
    pub writer_id: String,
    pub operation_id: String,
    pub pointer_digest: String,
}
```

The slot owns exactly one raw WGPU F32 `[B,Q,V]` buffer after adoption.

---

# 10. Private gradient initialization

R6-R12 allocates one private full BQV gradient buffer. This full surface is required because it becomes the next backward SSOT.

Before any valid-target gradient publication, the buffer is zeroed on GPU with an exact buffer clear.

Required:

```text
private_gradient_zero_clear = 1
CPU zero-payload upload = 0
canonical gradient authority before final adoption = Vacant
```

Only target-authority rows are writable later. Therefore rows without admitted targets remain zero by construction and are independently audited before adoption.

---

# 11. No full softmax surface

R6-R12 must not allocate `[B,Q,V]` probabilities or log-softmax.

Candidate row normalizer is compact `O(N_valid)` state, containing only enough row statistics to evaluate a gradient column on demand, such as:

```text
row_max
inv_sum_exp
```

Required:

```text
full_softmax_surface = 0
full_log_softmax_surface = 0
candidate normalizer canonical authority = 0
```

---

# 12. Candidate row normalizer

Candidate normalizer computes stable row statistics for each valid target row using the canonical logits:

```text
row_max = max_v logit[v]
sum_exp = sum_v exp(logit[v] - row_max)
inv_sum_exp = 1 / sum_exp
```

Required:

```text
row_max finite
sum_exp finite and > 0
normalizer rows = N_valid
```

It does not publish probabilities or become canonical state.

---

# 13. Independent reference normalizer

Reference path computes its own row statistics with a structurally different decomposition/order.

Current design:

```text
reference max: reverse vocab traversal
reference sum: reverse vocab traversal
```

Reference max/sum buffers are separate from the candidate normalizer. Candidate-to-reference copying is forbidden.

Reference remains non-authoritative.

---

# 14. Vocab-column wave plan

R6-R12 avoids a second full BQV reference gradient by partitioning vocabulary columns into runtime-derived contiguous waves.

Recommended plan:

```rust
pub struct R6R12GradientWavePlan {
    pub schema_version: u32,
    pub valid_target_count: u32,
    pub vocab_size: u32,
    pub total_bqv_scalar_count: u64,
    pub valid_gradient_scalar_count: u64,
    pub masked_gradient_scalar_count: u64,
    pub max_storage_binding_size: u64,
    pub max_buffer_size: u64,
    pub columns_per_wave: u32,
    pub wave_count: u32,
    pub waves: Vec<R6R12GradientWavePlanEntry>,
    pub plan_digest: String,
}
```

Each entry contains wave ordinal, vocab start/count/end, compact scalar count/bytes, and digest.

Required:

```text
first start = 0
last end = V
sum column counts = V
wave spans contiguous
wave spans non-overlapping
```

`columns_per_wave` is derived from runtime storage/max-buffer/parity limits. No fixed 48,259 or fixed 31 branch is allowed.

If one column cannot be admitted, fail closed. Do not fall back to a full reference BQV gradient.

---

# 15. Candidate gradient wave

For every valid target entry `i` and column `v` in the current vocab wave:

```text
prob = exp(logit - row_max) * inv_sum_exp
one_hot = 1 when v == target_token_id else 0
grad = (prob - one_hot) * mean_scale * upstream_seed
```

Compact candidate shape:

```text
[N_valid, R_wave]
```

No output for masked rows is computed in this compact path.

---

# 16. Independent reference gradient wave

Reference uses its independently computed row statistics and an algebraically equivalent decomposition:

```text
scaled_probability = exp(logit-ref_max) / ref_sum_exp * mean_scale * seed
scaled_one_hot = one_hot * mean_scale * seed
reference_gradient = scaled_probability - scaled_one_hot
```

Compact reference shape equals candidate shape. No candidate gradient may be copied into reference state.

Full reference BQV materialization count must remain zero.

---

# 17. Per-wave GPU parity

Candidate and reference compact waves are compared with the admitted GPU mixed-envelope comparator or an equivalent compact GPU comparator.

Per wave require:

```text
compared = N_valid * R_wave
nonfinite = 0
envelope_violation = 0
tensor payload readback = 0
```

Fixed startup tolerances:

```text
--r6-r12-grad-absolute-tolerance 0.001
--r6-r12-grad-relative-tolerance 0.001
--r6-r12-grad-relative-floor 0.00000001
```

No tolerance widening after failure.

Only a parity-passing candidate wave may publish into the private full gradient surface.

---

# 18. Gradient publication

Publication mapping is:

```text
target entry i -> flat logit row r_i
wave-local column c -> vocab v=wave_start+c
private_grad[r_i*V + v] = candidate_grad[i,c]
```

Required:

```text
one writer per valid gradient scalar
zero writes outside target-authority rows
zero writes outside current vocab wave
zero overlap between waves
```

No atomic accumulation is required because every valid gradient scalar has exactly one writer.

---

# 19. Runtime-derived coverage

Checked runtime identities:

```text
BQV = checked(B*Q*V)
valid_gradient_scalar_count = checked(N_valid*V)
masked_zero_scalar_count = BQV - valid_gradient_scalar_count
```

After all waves require:

```text
published_valid_gradient_scalars = N_valid*V
coverage_gap = 0
coverage_overlap = 0
wave_count = planner wave_count
```

No payload readback is required for combinatorial coverage proof.

---

# 20. Masked-zero audit

Independent GPU audit visits every excluded row/column and requires:

```text
visited = masked_zero_scalar_count
masked nonzero violation = 0
masked nonfinite = 0
```

For the current fixture expected visited count is 48,259.

No zero repair is allowed after audit. A violation fails closed.

---

# 21. Full finite audit

Before canonical adoption, one full BQV GPU finite scan requires:

```text
visited = BQV
nonfinite = 0
payload readback = 0
```

Only compact counters may be read back.

---

# 22. Valid-row gradient-sum audit

For each valid causal target row:

```text
sum_v dL/dz_i[v] ~= 0
```

because both softmax and one-hot sum to one.

GPU row-sum audit requires:

```text
row_sum_compared = N_valid
row_sum_nonfinite = 0
row_sum_violation = 0
```

Fixed tolerance:

```text
--r6-r12-grad-row-sum-absolute-tolerance 0.001
```

No post-audit correction or tolerance widening.

---

# 23. Canonical adoption

`LogitGradientSurfaceAuthoritySlot` starts Vacant.

Adoption is permitted only after:

```text
forward-loss exact lease pass
canonical logit exact lease pass
target authority exact reuse/integrity pass
backward seed authority pass
candidate normalizer pass
reference normalizer pass
all gradient waves parity pass
exact valid-domain coverage pass
masked-zero audit pass
full finite audit pass
valid-row sum-zero audit pass
same-device completion binding pass
```

Required:

```text
canonical_logit_gradient_publication = 1
parallel canonical gradient authority = 0
```

The private gradient buffer becomes canonical only at this point.

---

# 24. Parent state immutability

After gradient adoption, R6-R12 releases both parent leases and snapshots their authorities again.

Required exact before/after equality for the canonical forward-loss pointer and canonical logit pointer.

Required:

```text
forward_loss_pointer_unchanged = 1
logit_pointer_unchanged = 1
forward loss slot remains Resident
logit slot remains Resident
active parent leases after = 0
```

---

# 25. Failure boundaries

Any failure before canonical gradient adoption leaves:

```text
LogitGradientSurfaceAuthoritySlot = Vacant
canonical forward loss unchanged
canonical logits unchanged
no LM-head backward
no final-norm backward
no decoder backward
no optimizer
```

Forbidden same-operation fallbacks:

```text
GPU gradient failure -> CPU softmax gradient
candidate/reference parity failure -> accept candidate
masked-zero failure -> rewrite masked rows to zero and continue
finite failure -> replace NaN/Inf
row-sum failure -> renormalize gradient
planner failure -> allocate full reference BQV gradient
```

Same-operation fallback count must remain zero.

---

# 26. Payload-readback seal

Required:

```text
forward loss payload readback = 0
canonical logit payload readback = 0
candidate gradient payload readback = 0
reference gradient payload readback = 0
canonical gradient payload readback = 0
```

Compact parity/audit counters may be read back and are reported separately.

---

# 27. Backward scope boundary

R6-R12 is only the loss-to-logit backward seed.

Required zeros:

```text
forward_loss_recompute = 0
NLL republication = 0
LM-head weight reload = 0
LM-head backward = 0
final RMSNorm backward = 0
decoder backward = 0
gradient clipping = 0
gradient accumulation = 0
optimizer = 0
weight mutation = 0
production inference = 0
```

No checkpoint weights are reread by R6-R12.

---

# 28. CLI contract

Required true:

```text
--require-r6-r12-causal-loss-backward-seed
--require-r6-r12-r6-r11-physical-parent
--require-r6-r12-forward-loss-exact-lease
--require-r6-r12-canonical-logit-exact-lease
--require-r6-r12-target-shift-authority-reuse
--require-r6-r12-unit-upstream-loss-seed
--require-r6-r12-mean-loss-scale
--require-r6-r12-stable-row-normalizer
--require-r6-r12-gradient-wave-plan
--require-r6-r12-independent-gpu-reference
--require-r6-r12-per-wave-gradient-parity
--require-r6-r12-zero-masked-invalid-rows
--require-r6-r12-runtime-derived-bqv-coverage
--require-r6-r12-full-gradient-finite-scan
--require-r6-r12-valid-row-gradient-sum-zero
--require-r6-r12-canonical-logit-gradient-single-adoption
--require-r6-r12-zero-logit-payload-readback
--require-r6-r12-zero-gradient-payload-readback
--require-r6-r12-zero-lm-head-weight-reload
--require-r6-r12-lm-head-backward-blocked
--require-r6-r12-final-norm-backward-blocked
--require-r6-r12-decoder-backward-blocked
--require-r6-r12-optimizer-blocked
--require-r6-r12-weight-mutation-blocked
```

Fixed tolerances:

```text
--r6-r12-grad-absolute-tolerance 0.001
--r6-r12-grad-relative-tolerance 0.001
--r6-r12-grad-relative-floor 0.00000001
--r6-r12-grad-row-sum-absolute-tolerance 0.001
```

Allowed false:

```text
--allow-r6-r12-loss-seed-override
--allow-r6-r12-dynamic-loss-scaling
--allow-r6-r12-target-rebuild
--allow-r6-r12-full-softmax-surface
--allow-r6-r12-full-reference-gradient-surface
--allow-r6-r12-cpu-gradient
--allow-r6-r12-gradient-payload-readback
--allow-r6-r12-tolerance-widening
--allow-r6-r12-gradient-clipping
--allow-r6-r12-gradient-accumulation
--allow-r6-r12-lm-head-backward
--allow-r6-r12-final-norm-backward
--allow-r6-r12-decoder-backward
--allow-r6-r12-optimizer
```

---

# 29. Implementation surface

Semantic implementation surface:

```text
crates/burn_webgpu_backend/src/
  base_train_logit_gradient.rs
  base_train_logit_gradient_reference.rs
  base_train_logit_gradient_publish.rs
  base_train_logit_gradient_audit.rs
  lib.rs

crates/burn_webgpu_backend/src/shaders/
  base_train_logit_grad_candidate_stats.wgsl
  base_train_logit_grad_candidate_wave.wgsl
  base_train_logit_grad_reference_max.wgsl
  base_train_logit_grad_reference_sum.wgsl
  base_train_logit_grad_reference_wave.wgsl
  base_train_logit_grad_publish.wgsl
  base_train_logit_grad_masked_zero_audit.wgsl
  base_train_logit_grad_finite_audit.wgsl
  base_train_logit_grad_row_sum_audit.wgsl

crates/model_core/src/
  base_train_output_head_authority.rs

crates/orchestrator_local/src/
  base_train_atlas_wave_02_r6_r11_causal_forward_loss.rs
  base_train_atlas_wave_02_r6_r12_causal_loss_backward_seed.rs

crates/orchestrator_local/src/bin/
  ash_basetrain_atlas_wave_02_r6_r9_forward_coordinator_gate.rs

specs/cli/
  ash_basetrain_atlas_wave_02_r6_r9.args
```

Core runtime remains Rust + WGPU/WGSL. No JS/TS/Python canonical path.

---

# 30. Static closure requirements

Before physical admission require:

```text
R6-R11 parent called exactly once
forward-loss exact lease present
canonical logit exact lease present
source logit identities exact across loss/logit/receipt
R6-R11 target authority reused, not rebuilt
upstream seed exactly 1.0
mean scale derived from N_valid
no B*Q denominator
private full gradient GPU zero-clear present
full softmax surface creation = 0
full reference BQV gradient creation = 0
candidate row normalizer present
independent reference normalizer present
gradient wave plan runtime-derived
candidate/reference compact gradient wave present
per-wave GPU parity present
publication writes target-authority rows only
valid gradient coverage = N_valid*V
masked scalar count = BQV-N_valid*V
masked-zero GPU audit present
full finite GPU audit present
valid-row sum-zero GPU audit present
canonical gradient adoption exactly once
forward-loss pointer unchanged
logit pointer unchanged
forward-loss/logit/gradient payload readback = 0
LM-head weight reload/backward = 0
final norm backward = 0
decoder backward = 0
optimizer/weight mutation = 0
raw `.parent.parent` chain in R6-R12 = 0
new WGSL reserved identifier collision = 0
```

Current implementation static closure: `79/79 PASS` before physical Cargo/WGPU execution.

---

# 31. Expected terminal evidence

```text
[r6-r12-causal-loss-backward-seed]
forward_loss_pointer_exact_bound=1
forward_loss_lease_acquire=1
logit_pointer_exact_bound=1
logit_lease_acquire=1
logit_shape_bqv=<B>x<Q>x<V>
logit_scalar_count=<BQV>
target_authority_reused=1
valid_target_count=<N>
upstream_loss_seed=1.0
mean_scale=<1/N>
target_upload_count=1
target_upload_bytes=<N*8>
private_gradient_zero_clear=1
gradient_columns_per_wave=<runtime>
gradient_waves=<runtime>
candidate_normalizer_rows=<N>
reference_normalizer_rows=<N>
gradient_parity_compared=<N*V>
gradient_parity_nonfinite=0
gradient_parity_violation=0
published_valid_gradient_scalars=<N*V>
coverage_gap=0
coverage_overlap=0
masked_zero_scalars=<BQV-N*V>
masked_zero_violation=0
full_gradient_finite_visited=<BQV>
full_gradient_nonfinite=0
row_sum_compared=<N>
row_sum_violation=0
canonical_logit_gradient_publication=1
forward_loss_pointer_unchanged=1
logit_pointer_unchanged=1
forward_loss_payload_readback=0
logit_payload_readback=0
gradient_payload_readback=0
full_softmax_surface=0
full_reference_gradient_surface=0
lm_head_weight_reload=0
lm_head_backward=0
final_norm_backward=0
decoder_backward=0
optimizer=0
weight_mutation=0
production_inference=0
backward_seed_authority_digest=<sha256>
gradient_wave_plan_digest=<sha256>
gradient_surface_pointer_digest=<sha256>
gradient_completion_token_digest=<sha256>
receipt_digest=<sha256>
proof_ledger=HOLD
```

Current fixture expected non-wave counts:

```text
B=1
Q=32
V=48259
BQV=1544288
N_valid=31
valid_gradient_scalars=1496029
masked_zero_scalars=48259
target_upload_bytes=248
```

Wave count is runtime-plan-dependent and must not be predeclared.

---

# 32. PASS token

```text
PASS_ASH_BASETRAIN_ATLAS_WAVE_02_R6_R12_CAUSAL_LOSS_BACKWARD_SEED_R6_R11_PHYSICAL_PARENT_CANONICAL_FORWARD_LOSS_EXACT_POINTER_BUFFER_COMPLETION_AND_POLICY_BINDING_CANONICAL_LOGIT_SURFACE_EXACT_POINTER_BUFFER_COMPLETION_AND_BQV_LEASE_R6_R11_CAUSAL_TARGET_SHIFT_AUTHORITY_EXACT_REUSE_ZERO_TARGET_REBUILD_UNIT_UPSTREAM_LOSS_SEED_EXACT_MEAN_OVER_VALID_TARGET_SCALE_STABLE_PER_VALID_ROW_SOFTMAX_NORMALIZER_ZERO_FULL_SOFTMAX_SURFACE_RUNTIME_DERIVED_VOCAB_COLUMN_GRADIENT_WAVE_PLAN_SOFTMAX_MINUS_ONEHOT_DIVIDED_BY_EXACT_VALID_TARGET_COUNT_CANDIDATE_AND_INDEPENDENT_SAME_DEVICE_REFERENCE_COMPACT_GRADIENT_PER_WAVE_GPU_MIXED_ENVELOPE_PARITY_ZERO_NONFINITE_ZERO_ENVELOPE_VIOLATION_PARITY_GATED_PRIVATE_FULL_BQV_LOGIT_GRADIENT_PUBLICATION_EXACT_ZERO_INITIALIZED_MASKED_ROWS_RUNTIME_DERIVED_VALID_GRADIENT_COVERAGE_ZERO_GAP_ZERO_OVERLAP_MASKED_ZERO_AUDIT_ZERO_VIOLATION_FULL_BQV_FINITE_AUDIT_ZERO_NONFINITE_VALID_ROW_GRADIENT_SUM_ZERO_AUDIT_SINGLE_CANONICAL_LOGIT_GRADIENT_SURFACE_ADOPTION_FORWARD_LOSS_POINTER_UNCHANGED_LOGIT_POINTER_UNCHANGED_ZERO_FORWARD_LOSS_PAYLOAD_READBACK_ZERO_LOGIT_PAYLOAD_READBACK_ZERO_GRADIENT_PAYLOAD_READBACK_ZERO_LM_HEAD_WEIGHT_RELOAD_ZERO_LM_HEAD_BACKWARD_ZERO_FINAL_RMSNORM_BACKWARD_ZERO_DECODER_BACKWARD_ZERO_GRADIENT_CLIPPING_ZERO_GRADIENT_ACCUMULATION_ZERO_SAME_OPERATION_FALLBACK_OPTIMIZER_WEIGHT_MUTATION_AND_PRODUCTION_INFERENCE_BLOCKED_PROOF_LEDGER_HOLD_SEALED
```

---

# 33. Physical PASS meaning

R6-R12 physical PASS proves:

```text
canonical R6-R11 forward loss is exact backward parent
canonical R6-R10 logits are exact differentiation source
R6-R11 causal target authority is reused without rebuild
upstream seed is one for the admitted mean-loss policy
valid rows receive stable softmax-minus-onehot divided by N_valid
rows without admitted target remain exact zero
candidate gradient agrees with independently decomposed same-device GPU reference
all valid gradient scalars are published exactly once
no coverage gaps or overlaps exist
full BQV gradient is finite
valid gradient-row sums are zero under fixed tolerance
one canonical GPU logit-gradient surface is published
forward loss and logits remain immutable/resident
no tensor payload readback occurs
no LM-head/final-norm/decoder backward or optimizer mutation occurs
```

It does not prove LM-head backward, final-norm backward, decoder backward, gradient clipping/accumulation, mixed-precision loss scaling, optimizer correctness, training convergence, or production inference.

---

# 34. Admission state after physical PASS

```text
R6-R6 actual decoder Layer0                       = ADMITTED
R6-R8 resident decoder execution                  = ADMITTED
R6-R9-C8 canonical decoder weight wave loader     = ADMITTED
R6-R9-C9 full checkpoint-bounded decoder loop     = ADMITTED
R6-R9-C10 long-horizon residency health           = ADMITTED
R6-R9-C10-D1 role identity classification         = ADMITTED
R6-R10 final RMSNorm + streamed LM-head logits    = ADMITTED
R6-R11 causal forward loss                        = ADMITTED
R6-R12 causal loss backward seed + logit gradient = ADMITTED on physical PASS

Canonical logits surface                          = RESIDENT
Canonical forward loss                            = RESIDENT
Canonical logit-gradient surface                  = AVAILABLE after R6-R12 PASS
LM-head backward                                  = BLOCKED
Final RMSNorm backward                            = BLOCKED
Decoder backward                                  = BLOCKED
Optimizer                                          = BLOCKED
Weight mutation                                    = BLOCKED
Production inference                               = BLOCKED
Proof ledger                                       = HOLD
```

---

# 35. Natural next boundary

```text
ASH-BASETRAIN-ATLAS-WAVE-02-R6-R13

LM Head Backward /
Canonical Logit Gradient Exact Lease /
R6-R10 Final-Norm Activation Exact Reuse /
Untied-or-Tied LM-Head Source Authority Reuse /
Vocab-Row Streaming Backward /
Normalized-Hidden Gradient Accumulation /
LM-Head Weight Gradient Wave Publication /
Tied-Embedding Gradient Alias Semantics /
Zero Logit Recompute /
Zero Forward-Loss Recompute /
Final RMSNorm Backward Still Blocked Seal
```

R6-R13 must define a bounded canonical LM-head weight-gradient residency model and must not silently allocate a full `[V,H]` gradient if doing so violates the established streaming residency design.

---

# 36. Architecture seal

> R6-R12 is the first true backward state transition in the BaseTrain chain, but it deliberately stops at the logit boundary. It binds the exact canonical R6-R11 forward-loss pointer and exact canonical R6-R10 logits, reuses the already admitted causal target map, and seals a unit upstream seed for the parent's mean-loss policy. Stable row normalization generates `(softmax - one_hot) / N_valid` only for admitted target rows. The required full `[B,Q,V]` gradient is built privately because it becomes the next backward SSOT, while independent reference checking stays bounded through runtime-derived vocab-column waves. A GPU zero clear protects excluded rows, and exact valid-domain coverage, masked-zero preservation, full finiteness, valid-row gradient-sum conservation, and per-wave same-device parity are mandatory before one `LogitGradientSurfaceAuthoritySlot` adoption. Parent logits and forward loss remain unchanged, payload readback remains zero, and LM-head, final RMSNorm, decoder backward, optimizer mutation, clipping, accumulation, and production inference remain sealed for later admissions.
