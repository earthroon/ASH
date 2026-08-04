# ASH-BASETRAIN-ATLAS-WAVE-02-R5

## WGPU26 WGSL ABI Audit /
## Same-Process AW01 Live Residency Adoption /
## No Host Weight Reupload /
## Explicit Position·RoPE Parameter Binding /
## Embedding·RMSNorm Stage Split /
## QKV Projection Stage Split /
## Training Headwise Adapter or Oracle Naming Separation /
## CPU-f64 Numerical Parity /
## Padding QKV Exact-Zero /
## Executed Positive·Negative Control Counting /
## TensorCube Live Lease Handoff /
## No Receipt Overclaim Seal

> Status: SPEC RELEASE rev.1  
> Patch ID: `ASH-BASETRAIN-ATLAS-WAVE-02-R5`  
> Build revision: `ATLAS-WAVE-02-R5-wgpu26-live-residency-staged-parity-v1`  
> Direct code parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R4`  
> Normative semantic parent: `ASH-BASETRAIN-ATLAS-WAVE-02`  
> Live residency parent: `ASH-BASETRAIN-ATLAS-WAVE-01-R1`  
> Transaction parent: `ASH-BASETRAIN-ATLAS-WAVE-00-R1`  
> Correction class: ABI, ownership, numerical-proof, and receipt-authority closure  
> Parent AW-02 PASS eligibility: suspended until R5 physical gate passes  
> Training-step parent state: `Prepared`, immutable  
> Maximum admitted child state: `ForwardWaveActive`  
> TensorCube Stage10·11·12 authority: none  
> Loss·backward·optimizer·delta·apply·commit authority: none

---

# 0. Purpose

`ASH-BASETRAIN-ATLAS-WAVE-02-R5` replaces the original AW-02 monolithic physical fixture with a source-grounded, same-process, staged GPU proof.

R5 exists because the current AW-02 implementation does not yet prove all claims made by the AW-02 receipt surface.

Confirmed current-source conditions:

```text
1. The AW-02 WGSL passes a storage pointer as a user-function argument.
2. WGPU 26 / Naga rejects that pointer form.
3. The AW-02 shader hardcodes batch, sequence, hidden, head count and RoPE base.
4. The position-ID array created by the gate is not bound to the shader.
5. The Rust `rope_theta` input is not consumed by the shader.
6. The AW-02 backend accepts host slices for embedding, RMS and Q/K/V weights.
7. The AW-02 backend allocates new weight buffers and uploads those host slices.
8. The AW-01 coordinator consumes itself and returns receipts, not a live ring owner.
9. The AW-01 ring buffers are created with COPY_SRC | COPY_DST only.
10. The current AW-02 compute is one workgroup-size-1 monolithic oracle kernel.
11. The current gate records output digests but does not compare full numerical outputs.
12. The current coverage artifact writes constant counts instead of executed proof counts.
13. Padded queries receive zero context, but padded Q/K/V are not required to be zero.
14. The current receipt names the path Headwise although it does not call the existing Headwise dispatcher.
```

R5 must convert that state into the following physically supported chain:

```text
AW-00 immutable Prepared transaction
  -> one native WGPU bootstrap
  -> AW-01 checkpoint verification and live triple-ring upload in the same process
  -> live resident tensor views borrowed from the exact AW-01 ring owner
  -> no AW-02 checkpoint read
  -> no AW-02 weight buffer allocation
  -> no AW-02 weight queue write
  -> explicit token, valid-length, position and parameter bindings
  -> staged embedding kernel
  -> staged RMSNorm kernel
  -> staged QKV projection kernel
  -> staged RoPE kernel
  -> explicitly named training attention executor
  -> CPU-f64 full-output parity
  -> exact-zero padding proof
  -> live TensorCube candidate lease handoff
  -> stop before TensorCube Stage10, o_proj, residual, MLP, logits or loss
```

R5 is not a performance-promotion patch.

It is an authority-correction and physical-proof patch.

---

# 1. Source-grounded audit findings

## 1.1 WGPU26 storage-pointer function argument is invalid

Current shader surface:

```text
crates/burn_webgpu_backend/src/shaders/base_train_atlas_wave_02_headwise_prefill.wgsl
```

Current pattern:

```wgsl
fn proj(
    b: u32,
    s: u32,
    o: u32,
    w: ptr<storage, array<f32>, read>
) -> f32
```

Observed WGPU 26 / Naga failure:

```text
Argument 'w' ... is a pointer of space Storage ... which can't be passed into functions
```

R5 canonical shaders must contain no user-function parameter whose type is:

```text
ptr<storage, ...>
ptr<uniform, ...>
ptr<workgroup, ...> crossing a resource-authority boundary
```

Q, K and V projection functions may read their respective global bindings directly:

```wgsl
fn dot_q(...) -> f32 { ... q_weight[...] ... }
fn dot_k(...) -> f32 { ... k_weight[...] ... }
fn dot_v(...) -> f32 { ... v_weight[...] ... }
```

or use one entry point that directly references all three global resources.

A selector that aliases Q, K and V through one generic storage pointer is forbidden.

## 1.2 AW-01 currently loses the live ring owner at handoff

Current signature:

```rust
pub fn execute_full_wave_and_seed_handoff(
    mut self,
    ...
) -> Result<BaseTrainAtlasWave01CoordinatorOutput>
```

The coordinator owns:

```text
BaseTrainAtlasWave01BackendRing
three physical wgpu::Buffer slot arenas
slot-active-group ownership
lease generation
runtime identity
same-device generation fence
```

The returned output owns receipts only.

Therefore a later process or later call cannot infer live buffers from the JSON receipt.

R5 must preserve the coordinator or an equivalent live owner until AW-02 R5 completes.

## 1.3 AW-01 ring buffers are not compute-bindable

Current usage:

```rust
wgpu::BufferUsages::COPY_DST | wgpu::BufferUsages::COPY_SRC
```

R5 requires the original AW-01 ring allocation to include:

```rust
wgpu::BufferUsages::COPY_DST
    | wgpu::BufferUsages::COPY_SRC
    | wgpu::BufferUsages::STORAGE
```

This adds buffer capability only.

It does not grant AW-01 shader, pipeline or forward authority.

A second AW-02 compute-copy of the weights is forbidden.

## 1.4 Current AW-02 reuploads host weights

Current input surface contains:

```rust
pub embedding: &'a [f32]
pub rms_weight: &'a [f32]
pub q_weight: &'a [f32]
pub k_weight: &'a [f32]
pub v_weight: &'a [f32]
```

Current backend creates new buffers and executes `queue.write_buffer` for every weight.

That is not AW-01 live residency adoption.

R5 backend input must receive typed resident views, not host weight slices.

## 1.5 Position IDs and RoPE parameters are receipt-only in the current path

Current gate creates:

```rust
let positions = [0, 1, 2, 3, 0, 0, 0, 0];
```

The current backend does not accept a position-ID slice.

Current shader derives angle from sequence index:

```wgsl
let a = f32(s) * freq;
```

Current shader hardcodes:

```wgsl
pow(10000.0, ...)
```

The Rust input field `rope_theta` is therefore not an execution authority.

R5 must bind both exact position IDs and exact RoPE theta physically.

## 1.6 Current kernel is an oracle fixture, not existing Headwise authority

Current kernel:

```text
workgroup_size(1)
one dispatch
embedding + RMSNorm + QKV + RoPE + softmax + V accumulation in one function
```

It does not call:

```text
