# ASH-BURN-WGPU-SOFT-PRIMITIVE-ABI-P1A

## BURN-WGPU PRIMITIVE SEND/SYNC LOCUS PROBE
## + SOFT PRIMITIVE ABI CUT BOUNDARY
## + EXACT TRAIT-OBLIGATION ISOLATION
## + BURN-FACING LIGHTWEIGHT TENSOR TOKEN
## + PHYSICAL WGPU PAYLOAD EXCLUSION
## + SOFT-MATRIX RUNTIME RESOLVE CONTRACT

### 0. Revision

```text
Patch ID:
ASH-BURN-WGPU-SOFT-PRIMITIVE-ABI-P1A

Class:
TRAIT-OBLIGATION ISOLATION
BURN-FACING ABI CUT CANDIDATE
PHYSICAL PAYLOAD EXCLUSION

Direct parent:
ASH_PASS3_WGPU_PHYSICAL_RUNTIME_CONTEXT_SSOT_P1_REFDEPTH_COMPILEFIX_CODE_ONLY.zip

Parent SHA-256:
355a9563f68438ceacdd8b6fb59738868b5818d4168e1d680e2af79ad9da95b3
```

Observed parent release blocker:

```text
error[E0275]: overflow evaluating the requirement
validation::NumericDimension: Sync
```

The observed inner proof graph reaches WGPU ShaderModule / RenderPipeline / BindGroup / Device / Queue / LifetimeTracker / PendingWrites.

P1A does not claim that inner graph alone identifies the first outer ASH/Burn obligation.

---

# 1. Purpose

P1A separates two jobs:

```text
A. Exact Send/Sync locus probe
B. Soft Primitive ABI cut boundary materialization
```

The production backend is NOT switched to the Soft Primitive in this bake.

Reason:

```text
last PASS type
first FAIL type
```

must first be obtained from an independent release probe in the user's Rust toolchain.

P1A therefore materializes the diagnostic harness and the lightweight candidate ABI while keeping:

```rust
pub type TrainBackend = Autodiff<Wgpu<f32, i32>>;
```

unchanged.

Production cutover status:

```text
HOLD
```

---

# 2. Burn contract motivating the probe

The active Burn backend contract requires the float primitive to implement `TensorMetadata`, and `TensorMetadata` requires `Clone + Send + Sync + Debug`.

Therefore P1A tests the exact concrete type chain instead of inferring the culprit from the inner WGPU long-type alone.

No local registry/cache is declared the sole cause without probe evidence.

---

# 3. Independent probe crate

Added:

```text
crates/ash_p1a_trait_probe/
    Cargo.toml
    src/main.rs
```

Package:

```text
ash_p1a_trait_probe
```

It is a workspace member but is intentionally NOT a default member.

This allows one probe to be compiled without compiling the existing `base_train` library target first.

That isolation is required because the parent `base_train --lib --release` already reproduces E0275 and would otherwise hide the probe result.

---

# 4. Probe matrix

Eight independently selectable release probes are materialized:

```text
probe-device
probe-queue
probe-runtime
probe-cube-tensor
probe-fusion-tensor
probe-backend-primitive
probe-train-primitive
probe-soft-primitive
```

Exact tested surfaces:

```text
A  ash_wgpu26_api::Device
B  ash_wgpu26_api::Queue
C  burn_wgpu::WgpuRuntime
D  burn_wgpu::CubeTensor<burn_wgpu::WgpuRuntime>
E  burn_fusion::FusionTensor<burn_wgpu::WgpuRuntime>
F  <burn::backend::Wgpu<f32, i32> as Backend>::FloatTensorPrimitive
G  <Autodiff<Wgpu<f32, i32>> as Backend>::FloatTensorPrimitive
H  SoftProbePrimitiveP1A
```

Each probe calls both:

```rust
assert_send::<T>();
assert_sync::<T>();
```

through the shared `assert_send_sync` boundary so the compiler reports the exact failing auto-trait obligation.

---

# 5. Probe interpretation

```text
Device fails
    -> raw public WGPU object proof locus

Device/Queue pass, WgpuRuntime fails
    -> runtime locus

runtime passes, CubeTensor fails
    -> eager Cube tensor physical payload locus

CubeTensor passes, FusionTensor fails
    -> Fusion client/runtime locus

FusionTensor passes, Wgpu backend primitive fails
    -> Burn backend primitive wrapper locus

Wgpu backend primitive passes, TrainBackend primitive fails
    -> Autodiff/decorator locus

all physical probes pass, parent release still fails
    -> unrelated outer Send/Sync obligation remains
```

P1A production cutover must not be activated before this matrix has a last-PASS / first-FAIL boundary.

---

# 6. Lightweight Burn-facing candidate

Added:

```text
crates/base_train/src/burn_wgpu_soft_primitive_p1a.rs
```

Candidate:

```rust
AshSoftTensorPrimitiveR1
```

It carries only lightweight identity/metadata:

```text
SoftTensorCoordR1
matrix identity digest
tensor identity digest
physical DeviceAuthorityId
storage identity digest
optional PhysicalAllocationId
byte range
semantic generation
residency generation
Shape
DType
access class
```

It implements Burn `TensorMetadata` directly.

Compile-time candidate proof:

```rust
assert_send_sync::<AshSoftTensorPrimitiveR1>();
```

No manual unsafe implementation is used.

---

# 7. Physical payload exclusion

The fields of `AshSoftTensorPrimitiveR1` contain none of:

```text
wgpu::Device
wgpu::Queue
wgpu::Buffer
ComputeClient<WgpuRuntime>
CubeTensor<WgpuRuntime>
FusionTensor<WgpuRuntime>
BindGroup
Pipeline
ShaderModule
StagingBelt
```

This is the core candidate ABI law:

> Burn-facing tensor metadata must not transitively own the physical WGPU runtime graph.

P1 physical Device/Queue authority remains the lower physical owner.

---

# 8. Soft storage identity

Materialized:

```rust
SoftStorageIdentityP1A
```

Fields:

```text
storage_identity_digest
optional PhysicalAllocationId
byte_offset
byte_len
```

The optional physical allocation identity is metadata only. It does not contain the Buffer object.

When an allocation ID is present its DeviceAuthorityId must match the primitive's physical DeviceAuthorityId.

Pointer addresses are not authority.

---

# 9. Generation separation

The candidate keeps distinct:

```text
semantic_generation
residency_generation
```

P1 runtime generation remains a separate lower-layer concept.

P1A does not collapse semantic, residency and physical-runtime lifetime into one integer.

---

# 10. Runtime resolve contract

Added:

```text
crates/base_train/src/burn_wgpu_soft_primitive_runtime_resolve_p1a.rs
```

Materialized contract:

```rust
pub trait AshSoftPrimitiveRuntimeResolverR1 {
    type Resolved<'a>
    where
        Self: 'a;

    fn resolve<'a>(
        &'a self,
        primitive: &'a AshSoftTensorPrimitiveR1,
        intent: SoftResolveIntentR1,
    ) -> Result<Self::Resolved<'a>>;
}
```

This is an operation-scoped resolve boundary.

It is intentionally not backed by a second global WGPU object store.

---

# 11. Typed resolve intents

Materialized:

```text
Read
CandidateWrite
ReadWrite
CopySource
CopyDestination
```

No boolean fallback matrix is introduced.

---

# 12. P1A metadata admission

Materialized helper:

```text
admit_soft_primitive_resolve_p1a
```

It validates:

```text
primitive schema
matrix identity
P1 physical DeviceAuthorityId
Soft Matrix coord existence
committed semantic generation
GPU residency DeviceAuthorityId
residency generation
CPU-canonical vs physical-allocation consistency
```

It returns only:

```text
SoftPrimitiveResolvePermitP1A
```

containing metadata/range/allocation identity.

It does NOT return or own a WGPU Buffer.

The actual Buffer/lease view is deferred to P2, where the existing P1 subgroup + A02/A01 authorities will be reused.

---

# 13. No hidden production cutover

This bake explicitly retains:

```rust
pub type TrainBackend = Autodiff<Wgpu<f32, i32>>;
```

Therefore:

```text
base_train release E0275 may remain after applying P1A
```

and that result is not a P1A source failure.

The purpose of this bake is to produce exact evidence required for the subsequent physical-payload cutover.

No feature silently switches production tensors to the candidate ABI.

---

# 14. No forbidden workaround

P1A adds none of:

```text
#![recursion_limit = ...]
unsafe impl Send
unsafe impl Sync
raw-pointer ownership disguise
usize WGPU object identity
thread-local physical WGPU store
global Token -> CubeTensor map
global Token -> Device/Queue/Buffer map
```

---

# 15. Cargo/lock integration

Added workspace member:

```text
crates/ash_p1a_trait_probe
```

Not added to `default-members`.

Added direct `burn-backend = =0.20.1` dependency to `base_train` for the candidate's exact `TensorMetadata` implementation.

`Cargo.lock` is updated with:

```text
ash_p1a_trait_probe
base_train -> burn-backend
```

using the already-resolved Burn 0.20.1 dependency generation.

---

# 16. Required release probe commands

Run one command at a time.

```powershell
cargo build -p ash_p1a_trait_probe --release --no-default-features --features probe-device
cargo build -p ash_p1a_trait_probe --release --no-default-features --features probe-queue
cargo build -p ash_p1a_trait_probe --release --no-default-features --features probe-runtime
cargo build -p ash_p1a_trait_probe --release --no-default-features --features probe-cube-tensor
cargo build -p ash_p1a_trait_probe --release --no-default-features --features probe-fusion-tensor
cargo build -p ash_p1a_trait_probe --release --no-default-features --features probe-backend-primitive
cargo build -p ash_p1a_trait_probe --release --no-default-features --features probe-train-primitive
cargo build -p ash_p1a_trait_probe --release --no-default-features --features probe-soft-primitive
```

Record:

```text
last PASS
first FAIL
```

Do not enable multiple probe features in the authoritative run.

---

# 17. Baseline release command

After probes:

```powershell
cargo build -p base_train --lib --release -j 1
```

The baseline may still fail because production cutover is intentionally HOLD.

Do not increase recursion limit.

---

# 18. Activation gate

Soft Primitive production adoption may proceed only if:

```text
probe-soft-primitive PASS

and one of:
    CubeTensor FAIL
    FusionTensor FAIL
    Wgpu backend primitive FAIL
    TrainBackend primitive FAIL
```

If Device or Queue is already the first failing type, do not attempt the Burn-facing cut first.

A lower WGPU object proof boundary must be addressed.

---

# 19. P2 handoff

Once the locus supports the Soft Primitive cut, P2 attaches actual storage resolution:

```text
AshSoftTensorPrimitiveR1
    ↓
SoftTensorCoordR1
    ↓
McuSoftTensorMatrixR1
    ↓
P1 Physical Runtime / subgroup
    ↓
A02 PhysicalAllocationId + exact range
    ↓
A01 lease/submission authority
    ↓
operation-scoped actual Buffer view
```

Initial family scope:

```text
AdamM
AdamV
```

P1A itself does not activate Adam/HiMuon state migration.

---

# 20. Static acceptance actually executed

P1A focused source contract:

```text
32 / 32 PASS
```

Existing regressions:

```text
R7A                    83 / 83 PASS
R7                     55 / 55 PASS
Burn/CubeCL/WGPU26    117 / 117 PASS
base_train storage     39 / 39 PASS
```

R7A1 validator:

```text
parent 81 / 82 FAIL
P1A   81 / 82 FAIL
same failure: producer A01 tracked submit
```

Classification:

```text
PRE-EXISTING BASELINE FAILURE
NOT P1A REGRESSION
```

---

# 21. Toolchain qualification

Bake environment:

```text
cargo unavailable
rustc unavailable
```

Therefore:

```text
Rust type check      NOT RUN
borrow check         NOT RUN
release codegen      NOT RUN
trait probe results  NOT RUN
native tests         NOT RUN
WGPU execution       NOT RUN
```

No compile PASS is claimed.

---

# 22. Actual source bake

```text
ADD 5
MOD 4
DEL 0
```

Added:

```text
crates/ash_p1a_trait_probe/Cargo.toml
crates/ash_p1a_trait_probe/src/main.rs
crates/base_train/src/burn_wgpu_soft_primitive_p1a.rs
crates/base_train/src/burn_wgpu_soft_primitive_runtime_resolve_p1a.rs
tools/validate_ash_burn_wgpu_soft_primitive_p1a_static.py
```

Modified:

```text
Cargo.toml
Cargo.lock
crates/base_train/Cargo.toml
crates/base_train/src/lib.rs
```

P1 physical runtime files are not modified by this revision.

---

# 23. Artifacts

Overlay:

```text
ASH_BURN_WGPU_SOFT_PRIMITIVE_ABI_P1A_OVERLAY.zip
SHA-256: 26c1c9bf769863dac03d6a6ccce78542eb22b17eb5af8c419f2c4008f733d493
Bytes: 58,425
Files: 9
CRC: PASS
Duplicate paths: 0
```

Full code-only bake:

```text
ASH_PASS3_BURN_WGPU_SOFT_PRIMITIVE_ABI_P1A_CODE_ONLY.zip
SHA-256: 7c05bbf63bedd008f9fbc4e57861dcc4e27a4ff0396d1ca064ac1cd95ec0562a
Bytes: 21,392,656
Files: 8,419
CRC: PASS
Duplicate paths: 0
```

Validation logs:

```text
ASH_BURN_WGPU_SOFT_PRIMITIVE_ABI_P1A_VALIDATION_LOGS.zip
SHA-256: 0921d59758d83c3168737d1843ecd435d8d91ec675a0fcc39ce8166b52cbfa70
```

Code ZIPs contain no generated spec/artifact root and no PowerShell file.

---

# 24. Completion law

P1A source bake is complete when:

```text
independent exact trait probes exist
lightweight Burn TensorMetadata candidate exists
physical WGPU payload is excluded from that candidate
runtime resolve contract exists
P1 physical authority remains unchanged
production TrainBackend remains unchanged pending evidence
static regressions show no P1A regression
```

P1A production cutover is complete only later, after the user's release probes identify a primitive-facing first-fail boundary and the actual TrainBackend path is switched with release/native/WGPU evidence.

---

# 25. Final law

> Burn may demand `Send + Sync` from tensor metadata, but ASH must first prove which exact concrete type turns that requirement into the recursive WGPU proof.
>
> The diagnostic probe is isolated from the already-failing `base_train` release library so it can identify the first failing type rather than repeat the same opaque long-type.
>
> The candidate Burn-facing primitive carries tensor identity, shape, dtype, physical-runtime identity, storage identity and generation only.
>
> Device, Queue, Buffer, ComputeClient, Fusion client, pipeline and staging resources remain outside the candidate primitive.
>
> Actual physical storage resolution is operation-scoped and must reuse P1 + Soft Matrix + A02/A01 authority rather than create another physical owner.
>
> No recursion-limit increase or unsafe Send/Sync workaround is accepted.
