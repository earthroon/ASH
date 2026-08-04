model_core::NativeWgpu::execute_prefill_attention_via_headwise
Headwise atlas dispatcher
Headwise full-route admission
Headwise output-authority lease
```

Therefore it cannot emit a receipt claiming production or training Headwise authority.

R5 must either:

```text
A. physically call an admitted Headwise training adapter
```

or:

```text
B. identify the executor as CanonicalGpuOracle and remove Headwise claims
```

No third naming mode is admitted.

## 1.7 Current numerical proof is insufficient

Current gate verifies:

```text
output digests exist
invalid query context is exact zero
```

It does not verify the actual valid embedding, RMSNorm, Q/K/V, RoPE or context numbers against an independent reference.

R5 must compare every canonical fixture output element against a CPU-f64 reference.

## 1.8 Current proof counts are declarations, not executions

Current artifact shape includes literal values such as:

```json
{
  "positiveAssertions": 96,
  "negativeControls": 128,
  "pass": true
}
```

R5 must increment counts only after an identified proof case was physically or logically executed and produced its expected disposition.

## 1.9 External WGSL debt exists outside AW-02

Current repository scan also identifies `ptr<storage>` user-function parameters in:

```text
qwave_tensor.wgsl
qwave_gradient.wgsl
```

R5 must inventory these hits.

R5 does not silently claim those shaders were repaired unless their source is actually modified and validated in the same patch.

The R5 PASS claim is limited to the canonical AW-02 R5 shader set.

---

# 2. Scope

## 2.1 In scope

```text
WGPU26/Naga parse and validation of every AW-02 R5 shader
repository-wide WGSL ABI inventory with bounded claim scope
same-process AW-00 -> AW-01 -> AW-02 R5 physical chain
retention of one live AW-01 ring owner
STORAGE-capable AW-01 slot allocation
exact resident tensor-view binding
zero AW-02 host weight reupload
explicit token-ID binding
explicit row-valid-length binding
explicit position-ID binding
explicit RoPE-theta binding
explicit geometry and epsilon parameter binding
embedding stage
RMSNorm stage
Q/K/V projection stage
RoPE stage
training attention executor stage
executor-authority naming separation
full CPU-f64 numerical reference
full elementwise GPU/reference comparison
exact-zero padded embedding/norm/Q/K/V/context
executed positive proof ledger
executed negative-control ledger
live TensorCube candidate lease bundle
serialized receipt containing identities only
no receipt reconstruction of GPU handles
Rust-generated evidence artifacts and local manifest
```

## 2.2 Out of scope

```text
full production-size TinyLlama checkpoint residency
all decoder layers
selected layer greater than zero
GQA or MQA promotion beyond the canonical fixture
output projection
decoder residual add
MLP execution
next-layer execution
logits
loss
backward
gradient accumulation
optimizer
G206D delta consumption
weight mutation
weight commit
checkpoint write
training-cursor mutation
TensorCube Stage10, Stage11 or Stage12 execution
TensorCube output authority
production decode-session mutation
production Headwise promotion without an actual adapter call
repair of unrelated Q-wave shaders unless explicitly included
performance or throughput claim
```

---

# 3. Canonical authority map

| State or resource | Canonical owner | Permitted R5 operation | Forbidden substitute |
|---|---|---|---|
| AW-00 transaction | `model_core` | validate and bind digest | mutable copy |
| AW-01 residency contract | `model_core` | validate receipt identity | JSON-only reconstruction |
| AW-01 live ring | `base_train` + backend ring | retain and borrow views | AW-02 replacement ring |
| WGPU device and queue | `burn_webgpu_backend::NativeWgpuRuntimeHandles` | borrow existing handles | new instance/adapter/device |
| Resident weight buffers | AW-01 backend ring | read-only storage binding | host-uploaded AW-02 weights |
| Batch metadata | `base_train` | bounded queue upload | model-weight authority |
| Position IDs | AW-00 sequence authority | exact GPU binding | implicit `s` substitution |
| RoPE theta | model/fixture parameters | exact uniform binding | hardcoded 10000 |
| GPU stage outputs | AW-02 R5 backend | owned forward lease | serialized JSON payload |
| CPU-f64 reference | physical gate only | diagnostic comparison | production output authority |
| Attention result authority | selected executor enum | explicit oracle or adapter | ambiguous Headwise label |
| TensorCube candidate lease | AW-02 R5 live handoff | move live Q/K/V/context leases | receipt-only reconstruction |
| Artifact writer | `orchestrator_local` | evidence only | runtime owner |

Required dependency direction:

```text
burn_webgpu_backend
        ^
        |
model_core
        ^
        |
base_train
        ^
        |
orchestrator_local
```

The backend must not import `model_core` receipt types.

The gate must not become the long-lived owner of production buffers.

---

# 4. Parent adoption closure

## 4.1 Same-process chain is mandatory

The physical gate must perform the following in one process:

```text
bootstrap existing NativeWgpuRuntimeHandles
read and validate AW-00 transaction artifact
verify checkpoint and Safetensors header
join tensor-group, atlas and sequential plans
bind AW-01 coordinator
execute AW-01 upload wave
retain AW-01 coordinator and ring
borrow selected resident tensor views
execute AW-02 R5 stages
build TensorCube live handoff
write evidence
release after evidence completion
```

Reading a previously generated AW-01 local manifest is permitted as lineage evidence.

It is not a live residency source.

## 4.2 Required live-owner surface

One admissible shape:

```rust
pub struct BaseTrainAtlasWave01LiveResidency {
    coordinator: BaseTrainAtlasWave01ResidencyCoordinator,
    output: BaseTrainAtlasWave01CoordinatorOutput,
}

impl BaseTrainAtlasWave01LiveResidency {
    pub fn output(&self) -> &BaseTrainAtlasWave01CoordinatorOutput;

    pub fn resident_tensor_view(
        &self,
        tensor_key: &str,
    ) -> Result<BaseTrainAtlasWave01ResidentTensorView<'_>>;
}
```

Equivalent ownership is allowed only when all of the following remain true:

```text
one live coordinator
one exact backend ring
one runtime holder
one source-weight generation
no replacement buffer
no checkpoint reopen in AW-02
no buffer handle serialization
```

## 4.3 Non-consuming AW-01 execution

The implementation may change:

```rust
execute_full_wave_and_seed_handoff(mut self, ...)
```

to:

```rust
execute_full_wave_and_seed_handoff(&mut self, ...)
```

or return a wrapper that owns both coordinator and receipts.

The output receipt must still be immutable after sealing.

## 4.4 Parent transaction immutability

Required:

```text
AW-00 serialized transaction digest unchanged
AW-00 state remains Prepared
AW-01 parent transaction digest equals AW-00 receipt digest
AW-02 R5 parent transaction digest equals AW-00 receipt digest
parent mutation count 0
```
