R5-R4 may preserve one physical QKV dispatch if the shader uses Q width as the invocation domain and guards K/V writes by KV width.

Required form:

```wgsl
let q_width = params.num_heads * params.head_dim;
let kv_width = params.num_kv_heads * params.head_dim;
let total = params.batch_size * params.seq_len * q_width;
let q_lane = invocation % q_width;
let token_index = invocation / q_width;
```

Q is computed for every `q_lane`.

K and V are computed only when:

```wgsl
q_lane < kv_width
```

K/V output index:

```text
kv_output_index = token_index × kv_width + q_lane
```

K/V weight index:

```text
kv_weight_index = q_lane × hidden_size + input_lane
```

The shader must not write K/V when `q_lane >= kv_width`.

## 6.3 Admitted split dispatch

Separate Q, K and V dispatches are also admitted if all three dispatch counts are physically observed and the common source geometry remains one authority.

R5-R4 does not require split dispatch merely to increase stage count.

## 6.4 Padding behavior

For a padded token:

```text
all Q lanes  = +0.0
all K lanes  = +0.0
all V lanes  = +0.0
```

No tail region outside the logical K/V extent may be allocated as semantic output.

---

# 7. RoPE unequal-width closure

R5-R4 still uses the currently selected interleaved-pair implementation as a fixture algorithm.

This does not resolve the external RoPE convention question.

## 7.1 Q RoPE

```text
input shape  [T, QH, D]
output shape [T, QH, D]
stride       QW
pair count   T × QH × D/2
```

Q base:

```text
q_base = token_index × QW + query_head × D
```

## 7.2 K RoPE

```text
input shape  [T, KH, D]
output shape [T, KH, D]
stride       KW
pair count   T × KH × D/2
```

K base:

```text
k_base = token_index × KW + kv_head × D
```

## 7.3 Physical implementation choices

The stage may use:

```text
one WGSL module with two entry points
or
one dispatch over Q pairs with a guarded K subdomain
or
separate Q and K pipelines
```

Whichever implementation is chosen, receipts must expose the physically executed Q and K pair counts separately.

A common base using `hidden_size` for K is forbidden.

A K dispatch over `num_attention_heads` is forbidden.

## 7.4 RoPE boundary remains explicit

R5-R4 proves:

```text
GPU and CPU use the same declared fixture pairing convention
Q/K unequal-width RoPE indexing is correct for that convention
```

R5-R4 does not prove:

```text
HF Llama split-half compatibility
production checkpoint RoPE convention
external implementation parity
```

The state remains:

```text
ropePairingConvention = UNBOUND_EXTERNAL
productionAdmission = BLOCKED
```

---

# 8. Q-head to KV-head mapping

## 8.1 Canonical mapping

For contiguous GQA grouping:

```text
q_heads_per_kv = QH / KH
kv_head = query_head / q_heads_per_kv
```

For the R5-R4 fixture:

| Query head | Expected KV head |
|---:|---:|
| 0 | 0 |
| 1 | 0 |
| 2 | 1 |
| 3 | 1 |

The mapping table digest must be recorded.

## 8.2 Forbidden mappings

```text
query_head % num_key_value_heads
min(query_head, num_key_value_heads - 1)
query_head with K/V tail padding
round-robin mapping
environment-selected mapping
silent mapping fallback
```

## 8.3 No clamp

The shader must validate the host-derived geometry before dispatch.

It must not hide invalid geometry with:

```wgsl
max(params.num_kv_heads, 1u)
min(mapped_head, params.num_kv_heads - 1u)
```

Invalid geometry is a host admission failure.

---

# 9. Attention buffer strides

Required Q indexing:

```text
q_index = ((batch × seq_len + query_pos) × QW)
        + query_head × D
        + lane
```

Required K/V indexing:

```text
kv_index = ((batch × seq_len + key_pos) × KW)
         + kv_head × D
         + lane
```

Required context indexing:

```text
context_index = ((batch × seq_len + query_pos) × H)
              + query_head × D
              + lane
```

The following equivalence is forbidden:

```text
K/V stride == hidden_size
```

except when an MHA profile independently makes it true.

R5-R4 must prove that the GQA fixture uses:

```text
K/V stride = 8
hidden stride = 16
```

---

# 10. Resident K/V shape adoption

The AW-01 resident views must be bound directly with these exact shapes:

```text
Q resident weight [16, 16]
K resident weight [8, 16]
V resident weight [8, 16]
```

Required physical checks:

```text
Q view logical bytes == 16 × 16 × 4
K view logical bytes ==  8 × 16 × 4
V view logical bytes ==  8 × 16 × 4
K logical bytes < Q logical bytes
V logical bytes < Q logical bytes
```

The binding may refer to a larger atlas allocation range only when the resident view carries an exact logical offset and logical byte length.

The shader must not read beyond the logical K/V range even if the underlying atlas slot contains adjacent bytes.

Required guard evidence:

```text
last legal K/V weight scalar index
logical K/V scalar count
bound buffer offset
bound buffer size
resident address digest
geometry digest
```

No host-side K/V expansion to `[hidden_size, hidden_size]` is admitted.

No GPU copy that expands K/V into hidden-width buffers is admitted.

---

# 11. Deterministic mapping-sensitive fixture weights

R5-R4 must use deterministic weights that make the two KV heads numerically distinguishable.

The fixture generator must satisfy all of the following:

```text
K head 0 digest != K head 1 digest
V head 0 digest != V head 1 digest
correct contiguous mapping context != modulo-mapping context
