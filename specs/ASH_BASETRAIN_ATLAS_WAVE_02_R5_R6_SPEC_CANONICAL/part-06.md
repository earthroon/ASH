AW02R5R6ProductionConfigReadFailed
AW02R5R6ProductionConfigDigestMismatch
AW02R5R6ProductionConfigIncomplete
AW02R5R6ConfigGeometryConvergenceFailed
AW02R5R6ConfigRopeConvergenceFailed
AW02R5R6CheckpointRootModeInvalid
AW02R5R6IndexReadFailed
AW02R5R6IndexDigestMismatch
AW02R5R6IndexWeightMapInvalid
AW02R5R6ShardPathInvalid
AW02R5R6ShardMissing
AW02R5R6ShardDigestMismatch
AW02R5R6ShardByteCountMismatch
AW02R5R6SafetensorsHeaderInvalid
AW02R5R6TensorKeyDuplicateAcrossShards
AW02R5R6TensorRangeOverlap
AW02R5R6TensorRangeBeyondShard
AW02R5R6TensorByteLengthMismatch
AW02R5R6TensorNameUnresolved
AW02R5R6TensorNameAmbiguous
AW02R5R6CanonicalRoleDuplicate
AW02R5R6RequiredRoleMissing
AW02R5R6LayerContinuityFailed
AW02R5R6TensorDtypePolicyMismatch
AW02R5R6TensorShapeMismatch
AW02R5R6TiedRoleRepresentationInvalid
AW02R5R6SyntheticTensorDetected
AW02R5R6PayloadMutationDetected
AW02R5R6UnexpectedForwardAuthority
AW02R5R6NegativeControlUnexpectedPass
AW02R5R6AuthoritySealFailed
```

Errors must include the exact tensor key, shard ID or canonical role when applicable.

---

# 24. Manifest contract

The final local manifest must include:

```text
patch ID
build revision
PASS token
parent R5-R5 manifest digest
config source digest
ModelSpec digest
geometry authority digest
external RoPE authority digest
checkpoint root kind
index digest or explicit absence
ordered shard CAS list
shard-set digest
physical tensor inventory digest
canonical role inventory digest
physical tensor count
logical role count
layer count
total parameter count
total payload bytes
tied role count
synthetic tensor count
negative control receipt digest
forward dispatch count = 0
GPU upload count = 0
productionAdmitted = false
proofLedgerAdmission = HOLD
r6Admitted = false
```

The ordered shard-set digest must be deterministic and independent of filesystem enumeration order.

The ordered tensor inventory digest must sort by canonical role ID and then physical tensor ID.

---

# 25. No forward authority seal

R5-R6 must stop after tensor-set authority publication.

Forbidden calls include:

```text
same-process GPU residency creation
Q/K/V projection dispatch
RoPE dispatch
attention dispatch
Headwise dispatcher
TensorCube dispatcher
O projection
MLP
logits
loss
backward
optimizer
```

Required counters:

```text
gpu_buffer_create_count_for_payload = 0
gpu_upload_count                    = 0
forward_dispatch_count              = 0
readback_count                       = 0
training_step_count                  = 0
```

R5-R6 proves identity and topology, not numerics.

---

# 26. PASS token

The physical gate emits exactly:

```text
PASS_ASH_BASETRAIN_ATLAS_WAVE_02_R5_R6_PRODUCTION_CANDIDATE_CHECKPOINT_TENSOR_SET_AUTHORITY_SAFETENSORS_INDEX_SHARD_CAS_BINDING_ALL_LAYER_TENSOR_INVENTORY_DTYPE_SHAPE_BYTE_RANGE_CLOSURE_CONFIG_HEADER_PAYLOAD_IDENTITY_CONVERGENCE_CANONICAL_TENSOR_NAME_RESOLUTION_NO_SYNTHETIC_TENSOR_ADMISSION_NO_FORWARD_AUTHORITY_PRODUCTION_BLOCKED_PROOF_LEDGER_HOLD_R6_BLOCKED_SEALED
```

The token is forbidden unless every admission check and negative control has passed.

---

# 27. Explicit non-claims

An R5-R6 PASS does not prove:

```text
any tensor has been uploaded to GPU
any real checkpoint tensor has been numerically consumed
selected-layer forward parity
full-model forward correctness
Headwise adoption
TensorCube adoption
loss correctness
backward correctness
optimizer correctness
production training readiness
```

An R5-R6 PASS proves only:

```text
one complete immutable production-candidate checkpoint tensor set
is physically present, CAS-bound, canonically resolved,
shape/dtype/range-valid, config-convergent,
and free of synthetic tensor substitution.
```

---

# 28. Next patch dependency

The next patch may be:

```text
ASH-BASETRAIN-ATLAS-WAVE-02-R5-R7

Selected-Layer Real Checkpoint Forward /
Actual Embedding·RMSNorm·QKV Tensor Adoption /
BF16·F16 Decode Authority /
Production-Candidate GQA Consumption /
External RoPE Convention Live Consumption /
GPU-vs-CPU-f64 Selected-Surface Parity /
Resident Tensor Lease Provenance /
No Headwise Output Authority /
No Full-Model Admission Seal
```

R5-R7 must consume `CheckpointTensorSetAuthority` directly.

It must not reopen the checkpoint directory and rediscover tensor files independently.

---

# 29. Final seal

```text
Checkpoint set identity             SSOT
Config authority                    explicit
Index authority                     explicit or explicitly absent
Shard CAS                           exact
All-layer physical inventory        complete
Canonical role inventory            complete
Dtype closure                       exact
Shape closure                       exact
Byte-range closure                  exact
Layer continuity                    exact
Tied-role policy                    explicit
Synthetic tensor count              zero
Payload mutation                    zero
GPU upload                          zero
Forward authority                   none
Production admission                blocked
Proof ledger                        HOLD
R6                                  blocked
```

`ASH-BASETRAIN-ATLAS-WAVE-02-R5-R6` is sealed only when the actual checkpoint stops being “a file that appears compatible” and becomes one reproducible, immutable, fully enumerated tensor-set authority.
