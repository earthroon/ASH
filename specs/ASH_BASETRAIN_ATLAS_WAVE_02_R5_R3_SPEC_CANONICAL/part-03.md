upload_byte_len       = logical_element_count × W
padded_byte_len       = alignment_round_up(upload_byte_len)
```

Forbidden fixture literals include:

```text
embedding logical count 256 authored independently
Q/K/V logical count 64 authored independently
embedding byte length 1024 authored independently
Q/K/V byte length 256 authored independently
```

Those values may appear in sealed output receipts only as results of checked derivation.

Slot offsets must be produced by one deterministic allocator from the derived byte lengths and required alignment.

The allocator receipt must prove:

```text
no overlap
all slices within slot capacity
exact tensor key set
exact shape digest parity
exact element count parity
exact byte count parity
```

---

# 10. Shader geometry consumption

R5-R3 does not redesign the five canonical shaders, but all dispatch geometry and indexing limits must originate from the derived Params and geometry authority.

Required:

```text
no shader-side literal vocab size
no shader-side literal hidden size
no shader-side literal head count
no shader-side literal KV head count
no shader-side literal head dimension
no shader-side literal batch size
no shader-side literal sequence length
```

Workgroup size constants are execution policy and may remain literal if they do not encode model geometry.

The QKV stage must conceptually distinguish:

```text
Q output width  = q_projection_dim
K output width  = kv_projection_dim
V output width  = kv_projection_dim
```

R5-R3 canonical fixture may still execute MHA widths where both values are 8.

Actual unequal-width GQA dispatch is reserved for R5-R4.

---

# 11. Fixture isolation

## 11.1 Canonical fixture admission

R5-R3 may physically execute only when:

```text
profile_kind == SyntheticMhaFixture
num_attention_heads == num_key_value_heads
selected_layer == 0
checkpoint generated from the same fixture profile
ModelSpec generated from the same fixture profile
batch generated from the same fixture profile
production_admission == false
```

Required explicit HOLD reason for unequal heads in R5-R3 fixture gate:

```text
AW02R5R3GqaPhysicalExecutionDeferredToR5R4
```

This is not a generic Params rejection. It is a patch-scope admission boundary.

## 11.2 Production candidate audit

A real model ModelSpec and header may be reconciled in audit-only mode.

Audit-only output may report:

```text
geometry reconciled
GQA present
projection shapes derived
RoPE convention unresolved
production admission false
```

It may not dispatch the R5-R3 fixture kernels or print the R5-R3 physical PASS token.

## 11.3 No fixture identity promotion

The following are forbidden:

```text
renaming SyntheticMhaFixture to production
using fixture model_spec_id for a real checkpoint
accepting fixture tensor keys as sufficient production proof
claiming GQA support because generic validation no longer rejects it
claiming RoPE correctness because theta is bound
```

---

# 12. RoPE boundary in R5-R3

R5-R3 binds only the following RoPE facts from ModelSpec:

```text
kind
theta
scaling
head_dim
rotary_dim currently equal to head_dim
```

R5-R3 does not establish the lane-pairing convention.

Required receipt state:

```text
rope_parameter_binding       PASS
rope_pairing_convention      UNBOUND
external_rope_reference      NOT_EXECUTED
production_rope_admission    false
```

The current CPU and GPU oracle may continue to use the same fixture convention for regression, but that parity is not evidence of external model compatibility.

R5-R5 remains responsible for:

```text
split-half vs interleaved authority
checkpoint-family convention binding
independent external reference vectors
```

---

# 13. GQA boundary in R5-R3

R5-R3 must remove the false generic invariant:

```text
hidden_size == num_kv_heads × head_dim
```

R5-R3 must derive distinct K/V shapes.

However, R5-R3 does not claim successful unequal-head GPU execution.

Required states:

```text
GQA geometry representable        true
GQA header reconciliation         testable
GQA resident shape validation     testable
GQA physical dispatch             false
GQA numerical parity              false
GQA production admission          false
```

R5-R4 must later prove:

```text
num_heads > num_kv_heads
K/V output width = kv_projection_dim
KV buffer stride correctness
Q-head to KV-head mapping
attention oracle parity
```

---

# 14. New receipts

R5-R3 introduces the following append-only artifacts.

```text
01_r5_r2_parent_lineage_receipt.json
