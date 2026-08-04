Required references:

```text
embedding reference
RMSNorm reference
Q reference
K reference
V reference
RoPE Q reference
RoPE K reference
context reference
```

## 12.3 Comparison rules

Every element must be checked.

No sampled subset is sufficient.

Canonical tolerances:

| Stage | Absolute tolerance | Relative tolerance | Exact conditions |
|---|---:|---:|---|
| Embedding | 0 | 0 | bitwise F32 equality |
| Padded embedding | 0 | 0 | +0.0 bits |
| RMSNorm | `2e-5` | `2e-5` | finite |
| Q/K/V projection | `5e-5` | `5e-5` | finite |
| RoPE Q/K | `7.5e-5` | `7.5e-5` | finite |
| Context | `1e-4` | `1e-4` | finite |
| All padded Q/K/V/context | 0 | 0 | +0.0 bits |

Comparison predicate for non-exact values:

```text
abs(gpu - reference) <= abs_tol + rel_tol * abs(reference)
```

Required metrics:

```text
element count
mismatch count
max absolute error
max relative error
first mismatch index
first mismatch GPU value
first mismatch reference value
NaN count
Inf count
negative-zero count where exact +0.0 is required
```

## 12.4 Parity authority

A digest match alone is not numerical parity.

R5 PASS requires:

```text
all stage mismatch counts = 0
all NaN counts = 0
all Inf counts = 0
all exact-zero violations = 0
```

---

# 13. Padding QKV exact-zero seal

Required exact-zero surfaces for every `s >= row_valid_lengths[b]`:

```text
embedding_hidden
norm_hidden
Q before RoPE
K before RoPE
V
Q after RoPE
K after RoPE
context
```

Required bit pattern:

```text
0x00000000
```

Negative zero is not admitted for the exact-zero seal.

Required invariance control:

```text
mutate every padded token ID
rerun
all valid outputs unchanged within exact/tolerance contract
all padded outputs remain exact +0.0
```

Required mask control:

```text
corrupt one valid length upward
validator rejects or numerical parity fails
corrupt one valid length beyond seq_len
pre-dispatch validator rejects
```

---

# 14. Stage resources and dispatch receipts

Each stage must emit a receipt with:

```text
stage ID
shader source digest
entry point
pipeline identity digest
bind-group-layout digest
input buffer identity digests
resident weight address digests where applicable
output buffer identity digest
parameter digest
position digest where applicable
dispatch dimensions
queue submission serial
output byte count
readback byte count in gate mode
CPU parity receipt digest
pass
```

Canonical stage IDs:

```text
AW02R5-E-EMBEDDING
AW02R5-N-RMSNORM
AW02R5-P-QKV
AW02R5-R-ROPE
AW02R5-A-ATTENTION-ORACLE
```

In Headwise adapter mode, the last stage ID is:

```text
AW02R5-A-HEADWISE-TRAINING-ADAPTER
```

---

# 15. TensorCube live lease handoff

## 15.1 Live object

```rust
pub struct BaseTrainAtlasWave02R5TensorCubeLiveHandoff {
    pub q: wgpu::Buffer,
    pub k: wgpu::Buffer,
    pub v: wgpu::Buffer,
    pub context_oracle: wgpu::Buffer,
    pub row_valid_lengths: wgpu::Buffer,
    pub position_ids: wgpu::Buffer,
    pub runtime_holder_id: String,
    pub device_epoch: u64,
    pub queue_epoch: u64,
    pub source_weight_generation: u64,
    pub atlas_residency_generation: u64,
    pub selected_layer: u32,
    pub invocation_digest: String,
    pub lease_generation: u64,
    pub executor_kind: BaseTrainAtlasWave02R5ExecutorKind,
}
```

Equivalent wrappers are allowed.

The live handoff must own or otherwise keep all buffers alive.

## 15.2 Serialized receipt

The receipt contains:

```text
buffer identity digests
buffer byte sizes
shape and layout digests
runtime holder ID
device and queue epochs
weight and residency generations
selected layer
sequence authority digest
executor kind
lease generation
stage receipt digests
forward authority false
TensorCube Stage10 dispatch count 0
```

It contains no raw GPU handle.

## 15.3 Lease rules

```text
one writer during construction
read-only candidate lease after sealing
no buffer overwrite after handoff
no buffer reuse before lease release
no cross-runtime transfer
no JSON reconstruction
```

## 15.4 TensorCube boundary

R5 performs:

```text
TensorCube candidate handoff count 1
```

R5 performs no:

```text
Stage10 shader dispatch
Stage11 online softmax
Stage12 V accumulation
TensorCube output commit
TensorCube route mutation
```

---

# 16. Executed proof ledger

## 16.1 Ledger record

```rust
pub struct BaseTrainAtlasWave02R5ProofRecord {
    pub proof_id: String,
    pub class_id: String,
    pub polarity: ProofPolarity,
    pub expected_disposition: String,
    pub observed_disposition: String,
    pub physically_dispatched: bool,
    pub validator_executed: bool,
    pub evidence_digest: String,
    pub pass: bool,
}
```

Counts are derived from records after validation.

Literal assignment of final counts is forbidden.

## 16.2 Positive proof minimum

Minimum executed positive records: `96`.

Required class allocation:

| Class | Minimum |
|---|---:|
| Parent transaction and same-process lineage | 12 |
| AW-01 live residency and resident views | 12 |
| WGPU26 shader ABI and stage construction | 12 |
| Batch, positions, RoPE and parameter authority | 12 |
| Full numerical parity | 24 |
| Padding and causal semantics | 12 |
| TensorCube live handoff and lease | 8 |
| Mutation firewall and artifact integrity | 4 |
| **Total** | **96** |

## 16.3 Negative-control minimum

Minimum executed negative records: `128`.

Required class allocation:

| Class | Minimum |
|---|---:|
| Parent/runtime/generation mismatch | 16 |
| Resident tensor-view corruption | 16 |
| WGSL ABI and binding corruption | 16 |
| Batch/shape/parameter corruption | 16 |
| Position/RoPE corruption | 16 |
| Numerical-output corruption | 24 |
| Padding/causal corruption | 16 |
| Handoff/firewall/artifact corruption | 8 |
| **Total** | **128** |

## 16.4 Negative-control execution rule

A negative control counts only when:

```text
one named mutation is applied
its validator or physical gate is actually executed
its expected typed rejection is observed
no unrelated earlier rejection masks the target
an evidence digest is written
```

Duplicating one rejection 128 times is forbidden.

---

# 17. Required negative-control classes

## 17.1 Runtime and parent

```text
wrong AW-00 transaction digest
AW-00 state not Prepared
wrong runtime holder
changed device epoch
changed queue epoch
changed source weight generation
changed atlas residency generation
second device handle
second queue handle
missing raw bridge
receipt-only residency reconstruction
parent mutation count nonzero
```

## 17.2 Resident views

```text
wrong tensor key
wrong group ID
wrong slot index
wrong buffer identity digest
wrong address digest
misaligned byte offset
zero byte length
range end overflow
range beyond slot capacity
wrong dtype
wrong shape
wrong source slice digest
overlapping tensor views
missing STORAGE usage
replacement weight buffer
AW-02 weight queue write
```

## 17.3 WGSL ABI

```text
ptr<storage> function argument
missing entry point
wrong binding access
writeable weight binding
wrong binding index
