selected_layer == 0
rope_theta finite and > 1
rms_epsilon finite and > 0
attention_scale finite and > 0
batch * seq * hidden checked for overflow
all output byte sizes checked for overflow
```

## 8.3 Position IDs

Position IDs are a separate storage binding.

Required:

```text
length = batch_size * seq_len
position IDs digest equals sequence-authority receipt
valid positions contain exact authoritative values
invalid padded positions may contain zero but carry no attention authority
shader reads positions[batch * seq + token]
```

Forbidden:

```text
angle derived from `s` when a position buffer is present
position IDs recorded only in JSON
position IDs regenerated independently inside WGSL
```

## 8.4 RoPE theta

Required:

```text
shader reads params.rope_theta
no literal 10000 or 500000 is the authority
receipt records observed theta bits
CPU reference consumes the same theta
negative control with changed theta changes Q/K and leaves V unchanged
```

---

# 9. Staged kernel architecture

## 9.1 Stage E: embedding

Inputs:

```text
token IDs
row-valid lengths
resident embedding table view
parameter block
```

Output:

```text
embedding_hidden [batch, seq, hidden]
```

Required behavior:

```text
valid token: exact table gather
invalid padded token position: exact +0.0 in all hidden lanes
out-of-range valid token ID: FAIL
padded token ID value cannot influence valid outputs
```

The embedding stage is bitwise-comparable for the canonical F32 fixture.

## 9.2 Stage N: RMSNorm

Inputs:

```text
embedding_hidden
row-valid lengths
resident RMS weight view
parameter block
```

Output:

```text
norm_hidden [batch, seq, hidden]
```

Canonical equation:

```text
mean_square = sum(x[d] * x[d]) / hidden_size
inv_rms = 1 / sqrt(mean_square + rms_epsilon)
y[d] = x[d] * inv_rms * rms_weight[d]
```

Invalid padded positions must remain exact zero.

## 9.3 Stage P: QKV projection

Inputs:

```text
norm_hidden
row-valid lengths
resident Q weight view
resident K weight view
resident V weight view
parameter block
```

Outputs:

```text
Q [batch, seq, num_heads, head_dim]
K [batch, seq, num_kv_heads, head_dim]
V [batch, seq, num_kv_heads, head_dim]
```

Canonical R5 fixture uses:

```text
num_heads = 2
num_kv_heads = 2
head_dim = 4
hidden_size = 8
```

Weight layout:

```text
[out_feature, in_feature]
```

Q, K and V must have independent binding identities and output digests.

Invalid padded positions must be exact zero before RoPE.

## 9.4 Stage R: RoPE

Inputs:

```text
Q
K
position IDs
parameter block
```

Outputs:

```text
Q_rope
K_rope
```

V is not an input and must not be mutated.

Required:

```text
pairwise rotation over head dimension
position read from explicit buffer
base read from rope_theta
invalid padded positions exact zero
Q and K may be in-place only when each invocation owns one non-overlapping pair
```

## 9.5 Stage A: training attention executor

Inputs:

```text
Q_rope
K_rope
V
row-valid lengths
parameter block
```

Output:

```text
context [batch, seq, num_heads, head_dim]
```

Canonical mask:

```text
query_valid = q_index < row_valid_lengths[batch]
key_valid   = k_index < row_valid_lengths[batch]
causal      = k_index <= q_index
admitted    = query_valid && key_valid && causal
```

Required:

```text
invalid key excluded before max and denominator
future key excluded before max and denominator
stable max-subtracted softmax
invalid query context exact zero
nonzero denominator for every valid query
finite output only
```

---

# 10. Training Headwise adapter or oracle naming separation

## 10.1 Executor enum

```rust
pub enum BaseTrainAtlasWave02R5ExecutorKind {
    CanonicalGpuOracle,
    HeadwiseTrainingAdapter,
}
```

No stringly typed third mode is admitted.

## 10.2 Canonical GPU oracle mode

This mode owns the staged Stage A shader described above.

Required receipt values:

```text
executor_kind                         CanonicalGpuOracle
oracle_dispatch_count                 1
headwise_dispatch_count               0
headwise_output_authority              false
production_output_authority            false
decode_session_mutation_count          0
kv_cache_mutation_count                0
fallback_count                         0
```

Required naming:

```text
module names include oracle, not headwise
shader labels include oracle, not headwise
PASS token includes ORACLE_NAMING_SEPARATION
```

## 10.3 Headwise training adapter mode

This stronger mode is admitted only when the implementation physically invokes a training-safe adapter backed by the existing Headwise dispatcher and same runtime handles.

Required:

```text
actual dispatcher call observed
same device and queue exact
training-specific admission context
no BoundDecodeSessionContract fabrication
no production decode-session mutation
no KV-cache publish
no Burn fallback
no silent fallback
Headwise authority receipt present
```

Required receipt values:

```text
executor_kind                         HeadwiseTrainingAdapter
oracle_dispatch_count                 0
headwise_dispatch_count               1
headwise_output_authority              true for the selected training context only
production_decode_output_authority     false
```

If those conditions are not met, the code must use `CanonicalGpuOracle`.

## 10.4 Forbidden overclaim

Forbidden labels in oracle mode:

```text
headwise training prefill live dispatch
headwise output authority
production headwise committed
existing headwise dispatcher consumed
```

The original AW-02 PASS token must not be printed by R5 unless its Headwise-specific claim is physically true.

---

# 11. Canonical physical fixture

## 11.1 Geometry

```text
batch size       2
sequence length  4
row valid        [4, 1]
vocabulary       32
hidden size      8
query heads      2
KV heads         2
head dimension   4
selected layer   0
RMS epsilon      1e-5
RoPE theta       10000.0
attention scale  0.5
```

## 11.2 Batch

```text
row 0 token IDs  [1, 2, 3, 4]
row 1 token IDs  [5, 0, 0, 0]
position IDs     [0, 1, 2, 3, 0, 0, 0, 0]
```

Padded token IDs are intentionally mutated in negative controls to prove exclusion.

## 11.3 Checkpoint fixture

The Rust gate generates one deterministic F32 Safetensors checkpoint containing exactly the five required tensors.

Required:

```text
checkpoint SHA-256 sealed
header topology validated
one authoritative group
five tensor slices
one current resident slot
non-overlapping offsets
no unplanned tensor read
```

The checkpoint and plan files are generated before AW-01 execution and are treated as immutable after digest publication.

---

# 12. CPU-f64 numerical oracle

## 12.1 Independence

The CPU oracle must be implemented in a module that does not call the GPU backend implementation.

It consumes:

```text
canonical fixture values
batch metadata
position IDs
RMS epsilon
RoPE theta
attention scale
```

It executes all arithmetic in f64 and casts each stage output to f32 only for the final comparison surface.

## 12.2 Stage references

