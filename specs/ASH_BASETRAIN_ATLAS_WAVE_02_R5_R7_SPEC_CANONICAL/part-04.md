```text
Q head domain 32
KV head domain 4
head dimension 64
compact KV stride 256
mapping digest exact
causal mask active
row-valid-length mask active
attention scale = 1 / sqrt(64)
```

Required counterfactuals:

```text
MHA mapping q_head == kv_head
round-robin kv_head = q_head % 4
offset mapping
expanded padded KV buffer
wrong attention scale
causal mask disabled
```

---

# 18. CPU-f64 reference authority

The CPU reference must be independent of GPU output and must start from the same raw checkpoint bytes identified by R5-R6.

Reference chain:

```text
raw BF16/F16 tensor bytes
  -> direct half-to-f64 decode
  -> embedding lookup
  -> RMSNorm in f64
  -> Q/K/V matmul in f64
  -> NeoX RoPE in f64
  -> causal GQA attention in f64
  -> selected-surface reference
```

The CPU reference must not start from GPU readback or from the decoded resident f32 buffer. This keeps decode error and GPU arithmetic error observable as separate quantities.

The reference must publish full arrays for the bounded fixture:

```text
embedding
norm
Q
K
V
Q_rope
K_rope
context
```

The CPU reference may store f64 arrays in memory because the selected activation surface is bounded. It must not fully materialize the five source weight tensors as f64.

Weight access for CPU matmul must use bounded streaming or mapped chunks from the exact tensor range.

---

# 19. Selected-surface parity

## 19.1 Full bounded-surface comparison

Because the rev.1 activation surface is small, parity must compare every output element for:

```text
embedding
norm
Q
K
V
Q_rope
K_rope
context
```

This is not sampled parity.

The term `selected-surface` means all outputs of the selected batch, sequence and layer, not a subset of lanes.

## 19.2 Error predicate

For non-exact stages, each element passes when:

```text
abs(gpu - cpu) <= absolute_tolerance + relative_tolerance * abs(cpu)
```

The receipt must publish:

```text
element count
max absolute error
max relative error
mean absolute error
p99 absolute error
first failing index
first failing GPU value
first failing CPU value
```

No tolerance may be auto-expanded after observing output.

## 19.3 Rev.1 parity profile

The parity profile is a separate SHA-sealed fixture. Initial maximum bounds are:

```text
embedding   abs 0.0       rel 0.0
norm        abs 2.0e-4    rel 2.0e-4
Q           abs 1.0e-2    rel 1.0e-3
K           abs 1.0e-2    rel 1.0e-3
V           abs 1.0e-2    rel 1.0e-3
Q_rope      abs 1.2e-2    rel 1.2e-3
K_rope      abs 1.2e-2    rel 1.2e-3
context     abs 2.0e-2    rel 2.0e-3
```

These are admission ceilings, not expected errors. The receipt must preserve observed values so a later patch can tighten them.

## 19.4 Exact predicates

The following remain exact regardless of tolerance:

```text
all masked activation lanes = +0.0
all output cardinalities exact
all finite counts exact
no NaN
no Inf
Q/K/V widths exact
lease lineage exact
checkpoint reopen count zero during forward
headwise dispatch count zero
full model dispatch count zero
```

---

# 20. Readback policy

R5-R7 may read back the complete bounded activation surface because it is a physical parity gate.

It may not read back resident weights.

Required counters:

```text
activation_readback_bytes > 0
resident_weight_readback_bytes = 0
checkpoint_payload_read_bytes_during_forward = 0
```

Readback buffers must be scoped to the gate and released after receipts are sealed.

The live Q/K/V/context handoff buffers must remain independent of readback buffers.

---

# 21. No Headwise output authority

R5-R7 must not invoke the existing Headwise training dispatcher.

Required counters:

```text
headwise_dispatch_count = 0
headwise_output_publish_count = 0
headwise_route_promotion_count = 0
```

The selected-layer context is an oracle/physical-reference output only.

It must not be published as:

```text
training attention output authority
Headwise replacement
TensorCube input authority
production inference output
```

Headwise adoption remains the responsibility of `ASH-BASETRAIN-ATLAS-WAVE-02-R6`.

---

# 22. No full-model admission

The selected-layer forward stops at attention context.

Required zero counters:

```text
o_projection_dispatch_count        0
attention_residual_dispatch_count  0
post_attention_norm_dispatch_count 0
mlp_dispatch_count                 0
layer_output_publish_count         0
next_layer_dispatch_count          0
final_norm_dispatch_count          0
lm_head_dispatch_count             0
logits_publish_count               0
loss_dispatch_count                0
backward_dispatch_count            0
optimizer_step_count               0
full_model_dispatch_count          0
```

Required state:

```text
executed_layer_count      1
full_model_admission      BLOCKED
production_admission      BLOCKED
proof_ledger_admission    HOLD
r6_admission              BLOCKED
```

---

# 23. Physical gate artifacts

The gate must write a versioned runtime directory such as:

```text
workspace/runtime/basetrain/atlas_wave/02/r5_r7/selected-layer-real-forward-v1/
```

Required artifacts:

```text
00_parent_r5_r6_authority_import.json
01_parent_r5_r5_rope_authority_import.json
02_selected_layer_tensor_selection_receipt.json
03_bf16_f16_decode_authority_receipt.json
04_resident_tensor_lease_set_receipt.json
05_token_fixture_authority_receipt.json
06_actual_embedding_forward_receipt.json
07_actual_rmsnorm_forward_receipt.json
08_actual_qkv_forward_receipt.json
09_external_neox_rope_live_receipt.json
10_production_gqa_attention_receipt.json
11_cpu_f64_selected_surface_reference_receipt.json
12_gpu_cpu_selected_surface_parity_receipt.json
13_resident_lease_provenance_receipt.json
14_no_headwise_output_authority_receipt.json
15_no_full_model_admission_receipt.json
16_negative_counterfactual_ledger.json
17_selected_layer_forward_authority.json
ash_basetrain_atlas_wave_02_r5_r7_local_manifest.json
```

Every artifact must contain:
