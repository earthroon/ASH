attention-scale derivation                            1
resident view shape validation                        5
atlas logical count derivation                        5
atlas byte-length derivation                          5
fixture single-source geometry audit                  1
production admission false                            1
GQA physical execution false                          1
RoPE pairing authority unbound                        1
```

Every proof must identify the source receipt and observed value.

R5-R3 does not repair the general R5 proof-ledger schema; that remains a later evidence patch.

---

# 18. Negative controls

R5-R3 must execute distinct geometry mutations.

Minimum classes:

## 18.1 ModelSpec mutations

```text
zero vocab size
zero hidden size
zero query head count
zero KV head count
zero head dimension
odd head dimension
hidden != query_heads × head_dim
KV heads > query heads
query heads not divisible by KV heads
selected layer >= num_layers
invalid theta
invalid RMS epsilon
```

## 18.2 Header mutations

```text
missing embedding key
missing RMS key
missing Q key
missing K key
missing V key
wrong embedding first dimension
wrong embedding hidden dimension
wrong RMS length
wrong Q output dimension
wrong Q input dimension
wrong K output dimension
wrong K input dimension
wrong V output dimension
wrong V input dimension
wrong dtype
shape product overflow
```

## 18.3 Source-binding mutations

```text
ModelSpec digest mismatch
ModelSpec ID mismatch
checkpoint identity mismatch
header digest mismatch
fixture profile digest mismatch
transaction ModelSpec mismatch
```

## 18.4 Params derivation mutations

```text
caller-authored Params rejected by gate policy
literal attention scale mismatch
batch size mismatch
sequence length mismatch
theta conversion non-finite
RMS epsilon conversion non-finite
```

## 18.5 Scope mutations

```text
ProductionCandidate attempts physical PASS
Synthetic fixture claims production admission
GQA fixture attempts R5-R3 dispatch
RoPE pairing claims bound
```

Mutation IDs must map to distinct input mutations. Repeating one mutation with different IDs is forbidden.

---

# 19. State and admission

## 19.1 Parent states

Required input state:

```text
R5-R2 lineage admission         PASS
R5 physical execution           PASS_OBSERVED
R5 evidence admission           HOLD
R6 admission                    BLOCKED
```

## 19.2 R5-R3 completion state

After R5-R3 PASS:

```text
artifact lineage                PASS
model geometry authority        PASS_FIXTURE_ONLY
ModelSpec -> Params direction   SEALED
header shape reconciliation     PASS_FIXTURE_ONLY
projection shape derivation     PASS
GQA geometry representation     PASS_STATIC
GQA physical execution          NOT_EXECUTED
RoPE parameter binding          PASS
RoPE pairing convention         UNBOUND
production model admission      BLOCKED
proof-ledger admission          HOLD
no-receipt-overclaim claim      REVOKED_PENDING_REQUALIFICATION
R6 admission                    BLOCKED
```

R5-R3 PASS must not be interpreted as R5 evidence requalification.

---

# 20. Mutation firewall

R5-R3 must preserve:

```text
TensorCube Stage10 dispatch        0
TensorCube Stage11 dispatch        0
TensorCube Stage12 dispatch        0
loss computation                   0
backward execution                 0
optimizer execution                0
delta materialization              0
resident weight write              0
training cursor write              0
pointer swap                        0
checkpoint finalize                0
route promotion                    0
decode mutation                    0
production admission               0
```

Allowed new operations:

```text
ModelSpec file read
ModelSpec parse
ModelSpec validation
header tensor lookup
shape derivation
shape reconciliation
geometry receipt creation
fixture-only canonical dispatch already admitted by R5
```

No new model weights may be created or uploaded by AW-02.

---

# 21. Error taxonomy

Required errors include:

```text
AW02R5R3ModelSpecSourceMissing
AW02R5R3ModelSpecParseFailed
AW02R5R3ModelSpecDigestMismatch
AW02R5R3ModelSpecIdMismatch
AW02R5R3ModelSpecTransactionMismatch
AW02R5R3ModelSpecConsistencyFailed
AW02R5R3CheckpointIdentityMismatch
AW02R5R3HeaderDigestMismatch
AW02R5R3RequiredTensorMissing
AW02R5R3TensorDtypeMismatch
AW02R5R3EmbeddingShapeMismatch
AW02R5R3RmsShapeMismatch
AW02R5R3QProjectionShapeMismatch
AW02R5R3KProjectionShapeMismatch
AW02R5R3VProjectionShapeMismatch
