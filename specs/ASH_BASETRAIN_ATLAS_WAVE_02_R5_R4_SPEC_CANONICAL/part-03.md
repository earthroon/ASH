correct contiguous mapping context != single-KV-head broadcast context
```

The weight generator may use a fixed integer formula, but it must be deterministic from the fixture profile digest and fixed seed.

A conforming example is:

```text
Q(row,col) = (((row × 13 + col × 7 + 3) mod 29) - 14) / 64

K(row,col) = head_bias[kv_head]
           + (((row × 5 + col × 11 + 1) mod 23) - 11) / 64

V(row,col) = head_scale[kv_head]
           × (((row × 17 + col × 3 + 5) mod 31) - 15) / 32

head_bias  = [+0.25, -0.375]
head_scale = [+1.0,  -0.75]
```

Equivalent deterministic formulas are admitted only if the gate records their generator ID and proves the mapping-sensitive inequalities above.

Random generation without a recorded seed is forbidden.

---

# 12. CPU-f64 GQA reference

The CPU reference must become shape-aware.

## 12.1 Weight cardinalities

```text
embedding length = vocab_size × hidden_size
RMS length       = hidden_size
Q weight length  = q_projection_dim × hidden_size
K weight length  = kv_projection_dim × hidden_size
V weight length  = kv_projection_dim × hidden_size
```

A shared `hidden_size × hidden_size` assertion for Q/K/V is forbidden.

## 12.2 Activation cardinalities

```text
embedding length = T × H
norm length      = T × H
Q length         = T × QW
K length         = T × KW
V length         = T × KW
Q_RoPE length    = T × QW
K_RoPE length    = T × KW
context length   = T × H
```

## 12.3 Separate index functions

Required conceptual helpers:

```rust
hidden_index(token, lane)
q_index(token, query_head, lane)
kv_index(token, kv_head, lane)
context_index(token, query_head, lane)
```

One hidden-width index helper must not be reused for K/V.

## 12.4 Projection loops

Q output loop:

```text
output_lane in 0..QW
```

K/V output loops:

```text
output_lane in 0..KW
```

## 12.5 Mapping

CPU attention must use:

```text
kv_head = query_head / q_heads_per_kv
```

The CPU reference must not use modulo.

## 12.6 Precision wording

The reference computes intermediate arithmetic in `f64`, converts final stage surfaces to `f32`, and compares those `f32` values against GPU readback.

The receipt wording must therefore be:

```text
f64-intermediate stage reference with final f32 comparison
```

It must not claim exact real-number equivalence.

---

# 13. Independent mapping counterfactual

Because GPU and CPU can share the same wrong mapping, R5-R4 requires a separate counterfactual reference.

The gate must calculate at least:

```text
correct_context = CPU reference with quotient mapping
modulo_context  = CPU reference with query_head % num_kv_heads
```

Required assertions:

```text
GPU context matches correct_context within tolerance
GPU context does not match modulo_context
changed mapping head set == {1, 2}
modulo counterfactual mismatch count > 0
head 1 counterfactual mismatch count > 0
head 2 counterfactual mismatch count > 0
```

For query heads 0 and 3, quotient and modulo happen to select the same KV head in the 4Q/2KV profile. The receipt must not falsely claim that every head distinguishes the mapping.

The counterfactual receipt must record:

```text
correct mapping table
wrong mapping table
per-query-head mismatch counts
first counterfactual mismatch
counterfactual context digest
correct context digest
```

The counterfactual is a rejection oracle, not a second execution authority.

---

# 14. GPU buffer allocation

Required physical buffers:

| Buffer | Logical width | Byte authority |
|---|---:|---|
| embedding_hidden | H | `hidden_bytes` |
| norm_hidden | H | `hidden_bytes` |
| q_output | QW | `q_bytes` |
| k_output | KW | `kv_bytes` |
| v_output | KW | `kv_bytes` |
| q_rope | QW | `q_bytes` |
| k_rope | KW | `kv_bytes` |
| context | H | `context_bytes` |

Required checks before buffer creation:

```text
q_bytes > kv_bytes
k_output.size == kv_bytes
v_output.size == kv_bytes
k_rope.size == kv_bytes
```

No extra hidden-width tail is admitted for K, V, or K_RoPE.

---

# 15. Dispatch geometry

R5-R4 must derive dispatch dimensions from logical invocation counts.

Required logical counts:

```text
embedding invocations = T × H
RMS invocations       = T
QKV invocations       = T × QW, for an admitted fused shader
Q RoPE pairs          = T × QH × D/2
K RoPE pairs          = T × KH × D/2
attention invocations = T × QH
```

If Q and K RoPE share one dispatch, the receipt must still record both logical subdomain counts and the exact guard that prevents duplicate or out-of-range K writes.

Every physical dispatch must validate:

```text
ceil_div(logical_count, workgroup_size)
<= max_compute_workgroups_per_dimension
```

Dispatch counters must be derived from actual dispatch calls, not final literals.

---

# 16. Full bounded fixture readback

R5-R4 may read back every synthetic fixture surface because the fixture is deliberately bounded.

The correct term is:

```text
full bounded fixture readback
```

The gate must not call this compact readback.

Required readback byte counts:

```text
embedding hidden_bytes
norm      hidden_bytes
Q         q_bytes
K         kv_bytes
V         kv_bytes
Q_RoPE    q_bytes
K_RoPE    kv_bytes
context   context_bytes
```

The total readback count must be the sum of physically submitted copy ranges.

---

# 17. Stage parity

Required stage comparisons:

| Stage | GPU cardinality | CPU cardinality | Required tolerance class |
|---|---:|---:|---|
| Embedding | `T × H` | `T × H` | bitwise exact |
