wrong minimum binding size
wrong parameter layout digest
hardcoded rope theta sentinel
implicit sequence-index position sentinel
shader parse failure
Naga validation failure
pipeline layout mismatch
workgroup size zero or unsupported
output range under-allocation
unchecked geometry overflow sentinel
canonical shader source digest mismatch
```

## 17.4 Batch and sequence

```text
batch zero
sequence zero
hidden zero
heads zero
head dim zero
hidden != heads * head_dim
row-valid length > sequence
token ID out of vocabulary at valid position
position buffer wrong length
position digest mismatch
non-finite rope theta
rope theta <= 1
non-finite RMS epsilon
RMS epsilon <= 0
non-finite attention scale
```

## 17.5 Numerical parity

```text
one embedding bit flipped
one RMS value perturbed
one Q value perturbed
one K value perturbed
one V value perturbed
one RoPE Q value perturbed
one RoPE K value perturbed
one context value perturbed
NaN injection
positive infinity injection
negative infinity injection
negative-zero injection in padded Q
future-key inclusion
padded-key inclusion
wrong attention scale
wrong RMS epsilon
wrong RoPE theta
wrong position ID
Q/K weight swap
K/V weight swap
transpose weight layout
missing max subtraction
wrong softmax denominator
valid output forced to zero
```

## 17.6 Handoff and firewall

```text
Stage10 dispatch count nonzero
forward authority true
missing Q lease
missing K lease
missing V lease
missing context lease
runtime holder mismatch
lease generation zero
loss count nonzero
backward count nonzero
optimizer count nonzero
weight write count nonzero
cursor write count nonzero
pointer swap count nonzero
checkpoint write count nonzero
route promotion count nonzero
```

---

# 18. Runtime and mutation firewall

## 18.1 Allowed nonzero counters

```text
native runtime bootstrap count
AW-01 checkpoint streaming bytes
AW-01 resident weight upload bytes
AW-01 bounded readback bytes
batch metadata queue-write bytes
parameter queue-write bytes
position-ID queue-write bytes
shader-module creation count
pipeline creation count
bind-group creation count
stage dispatch count
stage verification readback bytes
CPU-reference comparison count
proof-record write count
artifact write count
```

## 18.2 Required zero counters

```text
secondary WGPU instance count
secondary adapter request count
secondary device request count
secondary queue creation count
AW-02 checkpoint open count
AW-02 weight buffer create count
AW-02 weight queue-write count
AW-02 host full-tensor materialization count
AW-02 resident replacement copy count
production decode-session mutation count
KV-cache publish count
Burn fallback count
silent fallback count
TensorCube Stage10 dispatch count
TensorCube Stage11 dispatch count
TensorCube Stage12 dispatch count
TensorCube output commit count
o_proj dispatch count
residual dispatch count
MLP dispatch count
logits materialization count
loss compute count
backward count
gradient write count
optimizer state write count
optimizer step count
delta materialization count
weight write count
weight commit count
training cursor write count
pointer swap count
checkpoint write count
checkpoint finalize count
route promotion count
quality claim count
performance claim count
```

---

# 19. State model

## 19.1 Parent states

```text
AW-00 transaction state     Prepared
AW-01 residency state       ResidencyHandoffReady
```

## 19.2 R5 stage state

```rust
pub enum BaseTrainAtlasWave02R5State {
    Unbound,
    ParentBound,
    LiveResidencyBound,
    EmbeddingComplete,
    RmsNormComplete,
    QkvComplete,
    RopeComplete,
    AttentionExecutorComplete,
    NumericalParityComplete,
    TensorCubeCandidateReady,
    Invalidated,
}
```

## 19.3 Canonical transitions

```text
Unbound
  -> ParentBound
  -> LiveResidencyBound
  -> EmbeddingComplete
  -> RmsNormComplete
  -> QkvComplete
  -> RopeComplete
  -> AttentionExecutorComplete
  -> NumericalParityComplete
  -> TensorCubeCandidateReady
```

Any integrity failure transitions to `Invalidated`.

No transition from `Invalidated` is admitted in the same coordinator instance.

---

# 20. Receipt authority

## 20.1 No receipt overclaim

Every boolean claim must derive from a physical counter, validated identity, or executed proof record.

Forbidden:

```text
sameDevice = true without pointer/identity comparison
residentWeightSource = AW01 without resident-view receipts
positionsConsumed = true without a position binding
ropeApplied = true without theta and position binding
headwise = true without a Headwise adapter call
numericalParity = true from digests only
positiveAssertions = 96 as a literal
negativeControls = 128 as a literal
liveHandoff = true after buffers were dropped
```

## 20.2 Executor claim

Receipt must contain:

```text
executor_kind
executor_callsite_id
executor_dispatch_count
oracle_dispatch_count
headwise_dispatch_count
headwise_authority_receipt_digest optional
fallback_count
```

## 20.3 Residency claim

Receipt must contain:

```text
AW-01 coordinator live at dispatch
ring identity digest
slot buffer identity digest
five resident address digests
AW-02 weight upload count 0
AW-02 weight buffer create count 0
```

## 20.4 Numerical claim

Receipt must contain all comparison metrics, not only one pass boolean.

---

# 21. Failure taxonomy

## 21.1 Typed FAIL classes

```text
FAIL_ASH_BASETRAIN_ATLAS_WAVE_02_R5_WGSL_ABI_<REASON>
FAIL_ASH_BASETRAIN_ATLAS_WAVE_02_R5_PARENT_AUTHORITY_<REASON>
FAIL_ASH_BASETRAIN_ATLAS_WAVE_02_R5_LIVE_RESIDENCY_<REASON>
FAIL_ASH_BASETRAIN_ATLAS_WAVE_02_R5_WEIGHT_REUPLOAD_<REASON>
FAIL_ASH_BASETRAIN_ATLAS_WAVE_02_R5_PARAMETER_BINDING_<REASON>
FAIL_ASH_BASETRAIN_ATLAS_WAVE_02_R5_STAGE_EXECUTION_<REASON>
FAIL_ASH_BASETRAIN_ATLAS_WAVE_02_R5_NUMERICAL_PARITY_<REASON>
FAIL_ASH_BASETRAIN_ATLAS_WAVE_02_R5_PADDING_ZERO_<REASON>
FAIL_ASH_BASETRAIN_ATLAS_WAVE_02_R5_EXECUTOR_AUTHORITY_<REASON>
FAIL_ASH_BASETRAIN_ATLAS_WAVE_02_R5_PROOF_LEDGER_<REASON>
FAIL_ASH_BASETRAIN_ATLAS_WAVE_02_R5_HANDOFF_<REASON>
FAIL_ASH_BASETRAIN_ATLAS_WAVE_02_R5_RECEIPT_OVERCLAIM_<REASON>
```

## 21.2 Typed HOLD classes

HOLD is reserved for unavailable but non-corrupt external conditions:

```text
HOLD_ASH_BASETRAIN_ATLAS_WAVE_02_R5_ADAPTER_FEATURE_UNAVAILABLE
HOLD_ASH_BASETRAIN_ATLAS_WAVE_02_R5_REQUIRED_DEVICE_FEATURE_UNAVAILABLE
HOLD_ASH_BASETRAIN_ATLAS_WAVE_02_R5_PARENT_ARTIFACT_ABSENT
HOLD_ASH_BASETRAIN_ATLAS_WAVE_02_R5_CHECKPOINT_FIXTURE_ABSENT
```

An authority mismatch, shader validation failure, numerical mismatch or overclaim is FAIL, not HOLD.

---

# 22. Physical gate

## 22.1 Binary

```text
ash_basetrain_atlas_wave_02_r5_physical_gate
```

## 22.2 Required execution order

```text
1. parse response file
2. validate CLI registry
3. create output staging directory
4. validate AW-00 parent
5. bootstrap one native WGPU runtime
6. generate deterministic Safetensors fixture and plans
7. verify fixture digests
8. execute AW-01 in the same process
9. retain live ring owner
