NEG-GQA-GEOM-002 num_key_value_heads > num_attention_heads
NEG-GQA-GEOM-003 num_attention_heads % num_key_value_heads != 0
NEG-GQA-GEOM-004 kv_projection_dim != num_key_value_heads × head_dim
NEG-GQA-GEOM-005 q_projection_dim == kv_projection_dim
NEG-GQA-GEOM-006 q_heads_per_kv independently changed to 1
NEG-GQA-GEOM-007 q_heads_per_kv independently changed to 4
NEG-GQA-GEOM-008 mapping table digest mismatch
```

## 23.2 Resident shape mutations

```text
NEG-GQA-RESIDENT-001 K shape changed to [16,16]
NEG-GQA-RESIDENT-002 V shape changed to [16,16]
NEG-GQA-RESIDENT-003 K shape changed to [7,16]
NEG-GQA-RESIDENT-004 V shape changed to [8,15]
NEG-GQA-RESIDENT-005 K logical byte length enlarged to Q byte length
NEG-GQA-RESIDENT-006 K logical byte length truncated by one scalar
NEG-GQA-RESIDENT-007 K/V address digest swapped
NEG-GQA-RESIDENT-008 geometry digest changed after resident binding
```

## 23.3 Buffer and stride mutations

```text
NEG-GQA-STRIDE-001 K stride = hidden_size
NEG-GQA-STRIDE-002 V stride = hidden_size
NEG-GQA-STRIDE-003 K_RoPE stride = hidden_size
NEG-GQA-STRIDE-004 K byte count = q_bytes
NEG-GQA-STRIDE-005 V byte count = q_bytes
NEG-GQA-STRIDE-006 K output allocation smaller than kv_bytes
NEG-GQA-STRIDE-007 V output allocation smaller than kv_bytes
NEG-GQA-STRIDE-008 K readback range exceeds logical bytes
```

## 23.4 Mapping mutations

```text
NEG-GQA-MAP-001 modulo mapping [0,1,0,1]
NEG-GQA-MAP-002 clamp mapping [0,1,1,1]
NEG-GQA-MAP-003 broadcast mapping [0,0,0,0]
NEG-GQA-MAP-004 reversed groups [1,1,0,0]
NEG-GQA-MAP-005 boundary-only error [0,1,1,1]
NEG-GQA-MAP-006 query head 1 mapped to KV1
NEG-GQA-MAP-007 query head 2 mapped to KV0
NEG-GQA-MAP-008 mapping selected from environment
```

## 23.5 Numerical mutations

```text
NEG-GQA-NUM-001 K head 0 and head 1 made identical
NEG-GQA-NUM-002 V head 0 and head 1 made identical
NEG-GQA-NUM-003 one K scalar corrupted
NEG-GQA-NUM-004 one V scalar corrupted
NEG-GQA-NUM-005 one K_RoPE scalar corrupted
NEG-GQA-NUM-006 one context scalar corrupted in query head 1
NEG-GQA-NUM-007 one context scalar corrupted in query head 2
NEG-GQA-NUM-008 modulo reference incorrectly marked accepted
```

Each mutation must have a distinct mutation digest and expected rejection site.

Record first, admit or reject after recording.

---

# 24. Mutation firewall

R5-R4 must preserve all R5 mutation denials.

Required zero mutations:

```text
weight write
weight pointer swap
optimizer state write
training cursor write
checkpoint finalize
checkpoint pointer update
route promotion
TensorCube Stage10 execution
loss execution
backward execution
optimizer execution
decode session mutation
KV-cache publication
host K/V expansion
resident-to-replacement K/V copy
silent CPU fallback
silent Headwise fallback
production admission
```

The mutation firewall must observe actual event sinks where available.

It must not construct a zero-filled receipt and then validate the same zeroes.

Global mutation-firewall requalification remains outside R5-R4.

---

# 25. Error taxonomy

Required error families:

```text
AW02R5R4GqaProfileKindMismatch
AW02R5R4QueryKvHeadEqualityUnexpected
AW02R5R4GqaGroupSizeInvalid
AW02R5R4QueryProjectionWidthMismatch
AW02R5R4KvProjectionWidthMismatch
AW02R5R4ResidentKShapeMismatch
AW02R5R4ResidentVShapeMismatch
AW02R5R4ResidentKvLogicalByteMismatch
AW02R5R4QBufferCardinalityMismatch
AW02R5R4KBufferCardinalityMismatch
AW02R5R4VBufferCardinalityMismatch
AW02R5R4QRopeCardinalityMismatch
AW02R5R4KRopeCardinalityMismatch
AW02R5R4KvStrideMismatch
AW02R5R4QueryToKvMappingMismatch
AW02R5R4ModuloCounterfactualNotRejected
AW02R5R4MappingSensitiveFixtureDegenerate
AW02R5R4CpuReferenceWeightCardinalityMismatch
AW02R5R4CpuReferenceActivationCardinalityMismatch
AW02R5R4GqaNumericalParityFailed
AW02R5R4PaddingNotPositiveZero
AW02R5R4LiveHandoffGeometryMismatch
AW02R5R4UnexpectedProductionAdmission
AW02R5R4UnexpectedTensorCubeDispatch
AW02R5R4UnexpectedTrainingMutation
```

Errors must identify the first relevant logical index when applicable.

---

# 26. Physical gate

Required binary:

```text
ash_basetrain_atlas_wave_02_r5_r4_gqa_physical_gate
```

Required CLI response file:

```text
specs/cli/ash_basetrain_atlas_wave_02_r5_r4.args
```

The gate must execute in this order:

```text
1. expand response-file arguments
2. verify immutable parent specification and lineage receipt
3. verify R5-R3 physical PASS evidence
4. create the synthetic GQA fixture profile
5. create ModelSpec and fixture checkpoint from that profile
6. bind checkpoint header and ModelSpec into geometry authority
7. derive Params
8. create or join AW-01 same-process residency
9. validate distinct Q/K/V resident shapes and logical byte ranges
10. execute embedding
11. execute RMSNorm
12. execute unequal-width Q/K/V projection
13. execute unequal-width Q/K RoPE
14. execute grouped attention with quotient mapping
15. perform full bounded fixture readback
16. build the f64-intermediate CPU GQA reference
17. compare every stage at its own cardinality
18. build and reject the modulo mapping counterfactual
19. validate positive-zero padding at per-surface widths
20. publish live handoff geometry receipt
21. verify mutation denials
22. publish R5-R4 manifest
23. emit PASS token
```

The gate must fail before PASS publication when any required receipt cannot be written atomically to a fresh run directory.

---

# 27. Required PASS token

```text
