
---

# 15. Actual Q/K/V projection adoption

The Q/K/V stage must consume exact selected-layer tensors:

```text
model.layers.L.self_attn.q_proj.weight
model.layers.L.self_attn.k_proj.weight
model.layers.L.self_attn.v_proj.weight
```

Required output widths:

```text
Q width = 2048
K width = 256
V width = 256
```

The gate must prove that K and V do not inherit the Q width through padding or aliasing.

Required counterfactuals:

```text
K bound to V tensor
V bound to K tensor
K or V bound to Q tensor prefix
KV output allocated at Q width
Q output truncated to KV width
projection row-major/column-major swap
```

The physical tensor layout is row-major `[output_dim, input_dim]` as represented by the canonical Safetensors shape and current WGSL indexing.

---

# 16. External NeoX RoPE live consumption

R5-R7 must consume the external convention authority physically proven by R5-R5.

For head dimension 64:

```text
rotary_dim = 64
pair_count_per_head = 32
first half lanes    0..31
second half lanes   32..63
pair i              (i, i + 32)
```

For each pair:

```text
frequency_i = rope_theta ^ (-2i / head_dim)
angle_i = position * frequency_i
out_first  = first * cos(angle) - second * sin(angle)
out_second = first * sin(angle) + second * cos(angle)
```

The live full-shape shader must publish:

```text
pairing layout ID
shader source digest
parameter digest
position digest
Q input/output digests
K input/output digests
Q pair invocation count
K pair invocation count
```

Required invocation counts for batch 1 and sequence 4:

```text
Q pairs = 1 * 4 * 32 * 32 = 4096
K pairs = 1 * 4 * 4  * 32 = 512
```

The adjacent-layout counterfactual must produce a nonzero mismatch and be rejected.

The legacy adjacent full-shape shader must not remain an active alternative authority.

---

# 17. Production-candidate GQA consumption

The attention stage must use the R5-R4 mapping:

```text
q_heads_per_kv_head = num_attention_heads / num_key_value_heads = 8
kv_head = q_head / 8
```

Canonical mapping:

```text
Q heads  0..7   -> KV head 0
Q heads  8..15  -> KV head 1
Q heads 16..23  -> KV head 2
Q heads 24..31  -> KV head 3
```

The stage must consume compact K and V buffers with width 256. It must not expand K/V to 2048 before attention.

Required proof:

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
