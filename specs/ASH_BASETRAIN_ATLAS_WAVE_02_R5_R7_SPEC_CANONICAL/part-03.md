The binding range must contain exactly one decoded tensor and may not alias another selected tensor unless an explicit immutable atlas suballocation authority proves non-overlap.

## 10.5 Lease lifetime

The lease must remain alive until:

```text
all command buffers using it are submitted
all compact readbacks are complete
all receipts are sealed
```

Dropping a source owner while a borrowed view remains live is forbidden.

---

# 11. Token fixture authority

R5-R7 does not perform text tokenization. It consumes an explicit numeric token fixture whose IDs are already within the R5-R6 vocabulary domain.

Rev.1 fixture requirements:

```text
batch_size              1
sequence_length         4
row_valid_lengths       [3]
position_ids            [0, 1, 2, 3]
valid token IDs         all < 48259
one masked token slot   required
```

A canonical example is:

```text
token_ids               [1, 328, 336, 0]
row_valid_lengths       [3]
position_ids            [0, 1, 2, 3]
```

The exact fixture bytes and digest must be pinned in a versioned JSON file. The semantic meaning of token IDs is not required for R5-R7 admission.

Required negative fixtures:

```text
token ID = 48259
row_valid_length > sequence_length
position ID >= max_position_embeddings
position cardinality mismatch
masked slot with nonzero output
```

---

# 12. GPU selected-layer forward graph

The admitted graph is exactly:

```text
actual embedding weight
  + token IDs
    -> embedding hidden

embedding hidden
  + actual input RMSNorm weight
    -> normalized hidden

normalized hidden
  + actual Q/K/V projection weights
    -> Q, K, V

Q, K
  + position IDs
  + rope_theta
  + NeoXHalfSplit
    -> Q_rope, K_rope

Q_rope, K_rope, V
  + causal mask
  + row-valid-length mask
  + 32Q:4KV GQA mapping
    -> context
```

Dispatch count for the selected surface is expected to be five:

```text
embedding
RMSNorm
QKV projection
NeoX RoPE
attention oracle
```

A fused implementation is permitted only after a separate parity proof. R5-R7 rev.1 uses explicit stage receipts.

---

# 13. Actual embedding adoption

The embedding stage must consume the actual R5-R6 tensor:

```text
model.embed_tokens.weight
```

Required proof:

```text
binding tensor identity digest equals R5-R6
resident decode digest equals lease receipt
vocab stride = hidden_size
masked rows are exact zero
out-of-range token fixture is rejected before dispatch
embedding readback equals CPU reference exactly in f32 representation
```

The embedding output for valid rows should be bit-identical to the decoded resident rows because the stage performs a direct indexed copy.

---

# 14. Actual RMSNorm adoption

The RMSNorm stage must consume:

```text
model.layers.L.input_layernorm.weight
```

The formula is:

```text
mean_square = sum(x_i * x_i) / hidden_size
inverse_rms = 1 / sqrt(mean_square + rms_norm_eps)
y_i = x_i * inverse_rms * weight_i
```

The epsilon must come from R5-R6 config authority. No shader literal or fallback is allowed.

Required proof:

```text
rms_norm_eps bits exact
actual norm tensor identity exact
masked rows exact zero
CPU-f64 reference from same decoded source
finite output count exact
```

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
