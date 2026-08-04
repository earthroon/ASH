PASS_ASH_BASETRAIN_ATLAS_WAVE_02_R5_R4_GQA_PHYSICAL_GEOMETRY_AUTHORITY_UNEQUAL_QUERY_KV_HEAD_PROFILE_DISTINCT_Q_K_V_PROJECTION_WIDTH_KV_BUFFER_STRIDE_CLOSURE_CONTIGUOUS_Q_HEAD_TO_KV_HEAD_MAPPING_RESIDENT_K_V_SHAPE_ADOPTION_CPU_F64_INTERMEDIATE_GQA_NUMERICAL_PARITY_MODULO_COUNTERFACTUAL_REJECTED_PADDING_EXACT_ZERO_LIVE_HANDOFF_GEOMETRY_ROPE_PAIRING_EXTERNAL_UNBOUND_NO_PRODUCTION_ADMISSION_PROOF_LEDGER_HOLD_R6_BLOCKED_SEALED
```

The token must not contain:

```text
PRODUCTION_READY
HF_ROPE_PARITY
NO_RECEIPT_OVERCLAIM_REQUALIFIED
HEADWISE_PRODUCTION_ADOPTED
TENSORCUBE_STAGE10_READY
LOSS_READY
BACKWARD_READY
OPTIMIZER_READY
```

---

# 28. Admission state

After R5-R4 physical PASS:

```text
R5-R2 artifact lineage                  PASS
R5-R3 ModelSpec geometry authority      PHYSICAL PASS
R5-R4 synthetic GQA physical execution  PHYSICAL PASS
unequal Q/KV projection widths          PHYSICAL PASS
quotient Q-to-KV mapping                PHYSICAL PASS
CPU-f64-intermediate GQA parity          PHYSICAL PASS
modulo counterfactual rejection         PASS
RoPE external convention                UNBOUND
production checkpoint GQA execution     UNPROVEN
proof ledger admission                  HOLD
no-receipt-overclaim requalification    REVOKED_PENDING_REQUALIFICATION
production admission                    BLOCKED
R6 admission                            BLOCKED
```

R5-R4 does not convert a synthetic fixture into production authority.

---

# 29. Completion criteria

R5-R4 is complete only when all of the following are true:

```text
[ ] fixture has 4 query heads and 2 KV heads
[ ] Q projection width is 16
[ ] K/V projection width is 8
[ ] resident Q shape is [16,16]
[ ] resident K/V shapes are [8,16]
[ ] K/V are not expanded on host
[ ] K/V are not expanded on GPU
[ ] physical K/V buffers use half the Q logical bytes
[ ] QKV stage indexes K/V through KV width
[ ] K RoPE indexes through KV width
[ ] attention mapping table is [0,0,1,1]
[ ] modulo mapping is physically rejected by numerical counterfactual
[ ] CPU reference uses distinct Q and KV index domains
[ ] Q/K/V/Q_RoPE/K_RoPE/context parity all pass
[ ] per-surface padding exact-zero checks pass
[ ] live handoff records unequal Q/KV shapes and strides
[ ] TensorCube Stage10 remains unexecuted
[ ] loss/backward/optimizer remain unexecuted
[ ] production admission remains false
[ ] RoPE external convention remains unbound
[ ] global proof-ledger admission remains HOLD
```

---

# 30. Explicit non-goals

R5-R4 does not implement or claim:

```text
actual TinyLlama checkpoint execution
HF config ingestion
HF split-half RoPE parity
RoPE scaling variants
production Headwise dispatcher adoption
TensorCube Stage10
attention backward
loss
optimizer
weight mutation
checkpoint commit
multi-layer execution
production admission
proof-ledger requalification
repository-wide WGSL cleanup
```

---

# 31. Next patch

After R5-R4 physical PASS, the next semantic spine patch is:

```text
ASH-BASETRAIN-ATLAS-WAVE-02-R5-R5

External RoPE Convention Authority /
Checkpoint Architecture Binding /
Split-Half·Interleaved Explicit Enum /
Independent Reference Vector /
HF-Compatible Position Frequency Contract /
Q·K Unequal-Width RoPE Parity /
No Self-Mirroring Reference Seal /
No Production Admission Seal
```

The proof-counter and global evidence requalification work remains after the model-semantic spine:

```text
R5-R6 physical runtime counters
R5-R7 failure-recordable proof ledger
R5-R8 distinct mutation coverage
...
```

---

# 32. Final seal

R5-R4 establishes this boundary:

```text
Static GQA geometry is not physical GQA execution.

Physical GQA requires:
  unequal resident Q/K/V shapes,
  unequal activation buffer widths,
  unequal RoPE strides,
  quotient query-to-KV mapping,
  mapping-sensitive numerical data,
  and a CPU reference that does not mirror MHA assumptions.
```

The only admitted authority flow is:

```text
ModelGeometryAuthority
  -> q_projection_dim / kv_projection_dim / q_heads_per_kv
  -> resident logical views
  -> physical GPU buffer extents
  -> WGSL index domains
  -> quotient mapping
  -> f64-intermediate CPU reference
  -> cardinality-correct parity receipts
  -> synthetic GQA physical PASS
```

Production admission remains sealed until external RoPE convention and production checkpoint semantics are independently bound.
