# R2B-CF2
# FFN PERSISTENT FUSED DYNAMIC BINDGROUP EXACT BACKING / ACCESS PAIR ATTRIBUTION

## Revision

```text
Patch ID:
ASH-BASETRAIN-R2B-FFN-PERSISTENT-FUSED-EXACT-BACKING-PAIR-ATTRIBUTION-CF2

Build revision:
basetrain-r2b-ffn-persistent-fused-exact-backing-pair-attribution-cf2

Class:
PHYSICAL WGPU BINDING ATTRIBUTION
FFN PERSISTENT EXECUTOR
DIAGNOSTIC ONLY
NO FIX
```

Direct parent:

```text
R2B-CF1
FIRST PHYSICAL FORWARD DISPATCH STORAGE ACCESS / BACKING IDENTITY ATTRIBUTION
```

## 1. Authoritative parent evidence

Release execution reproduced the canonical WGPU failure:

```text
wgpu error: Validation Error
In a CommandEncoder
  In a dispatch command, indirect:false
Attempted to use Buffer with conflicting usages
STORAGE_READ_ONLY
STORAGE_READ_WRITE
EXIT=101
```

The physical backtrace closed the local execution locus to:

```text
wgpu::CommandEncoder::finish
↓
burn_webgpu_backend::base_train_ffn_tensorcube_persistent_executor::
BaseTrainFfnTensorCubePersistentExecutor::execute
↓
model_core::actual_decoder_block_split_forward
↓
atlas_runtime_forward_wave_execution
```

CF1 also observed CubeCL pooled storage sharing across disjoint ranges, but those observed generic dispatch pairs were `READ_WRITE ↔ READ_WRITE`, not the canonical mixed-access pair.

## 2. Exact fused dynamic binding authority

The existing fused dynamic bind-group layout remains unchanged:

```text
binding 0  input_hidden      STORAGE_READ_ONLY
binding 1  gate_pre_out      STORAGE_READ_WRITE
binding 2  silu_gate_out     STORAGE_READ_WRITE
binding 3  up_linear_out     STORAGE_READ_WRITE
binding 4  ffn_product_out   STORAGE_READ_WRITE
```

Population dynamic buffers remain read-only and are excluded from the primary mixed-access candidate set by source.

## 3. Purpose

R2B-CF2 answers only:

```text
Q1. Which binding 1..4 shares the exact same Arc<BackendBuffer> with binding 0?
Q2. What are the two binding windows and their range relation?
Q3. Are multiple output bindings sharing the input backing simultaneously?
Q4. Does the canonical WGPU failure follow the attributed fused binding set in the same execute invocation?
```

## 4. Non-goals

CF2 does not change:

```text
WGSL
BindGroupLayout access flags
bind ordering
allocator policy
CubeCL pooled storage policy
Fusion behavior
RawWgpuBufferLease ownership
residency policy
model values
optimizer state
gradient math
training math
```

CF2 does not add GPU copies, GPU maps, GPU waits, fallback execution, detached output buffers, or access-class repair.

## 5. Diagnostic activation

```text
ASH_R2B_CF2_FFN_FUSED_ALIAS_TRACE=1
ASH_R2B_CF2_TRACE_ROOT=<trace root>
ASH_R2B_CF2_PROCESS_RUN_ID=<run id>
```

Default is OFF. With the trace gate absent, the new exact-pair instrumentation path is not entered.

Output:

```text
r2b_cf2_ffn_fused_alias_trace.jsonl
```

Each event is host-side append + flush only and adds no GPU work.

## 6. Exact backing authority

For every output candidate CF2 evaluates:

```rust
Arc::ptr_eq(&input_hidden.buffer, &candidate.buffer)
```

Candidate set:

```text
0 ↔ 1 gate_pre_out
0 ↔ 2 silu_gate_out
0 ↔ 3 up_linear_out
0 ↔ 4 ffn_product_out
```

`Arc::ptr_eq()` is the authoritative CF2 same-backing test inside the FFN executor. Debug label equality, size equality, and textual identity are not used for promotion.

## 7. Range relation

Using the exact bind windows:

```text
buffer_offset
buffer_size
len_bytes
```

CF2 classifies each pair as:

```text
EXACT_RANGE
OVERLAPPING_RANGE
DISJOINT_RANGE
```

Disjoint byte ranges do not exonerate a shared WGPU Buffer from usage-scope validation.

## 8. Pair event

For all four candidates CF2 emits `FFN_FUSED_ALIAS_PAIR` with:

```text
execute_sequence
layer_index
source_weight_generation
tensor_set_digest
binding_a=0
role_a=input_hidden
access_a=READ
offset_a
size_a
len_a
shape_a
primitive_id_a
stream_id_a
binding_b
role_b
access_b=READ_WRITE
offset_b
size_b
len_b
shape_b
primitive_id_b
stream_id_b
same_buffer
range_relation
classification
```

Classification:

```text
same_buffer=true
  -> FFN_FUSED_MIXED_ACCESS_SHARED_BACKING

same_buffer=false
  -> DISTINCT_BACKING
```

All four pairs are emitted; CF2 does not stop at the first match.

## 9. Summary event

CF2 emits `FFN_FUSED_ALIAS_SUMMARY` with:

```text
shared_backing_pair_count
shared_binding_mask
exact_range_count
overlap_count
disjoint_count
shared_bindings
mixed_access_shared_backing_present
```

The bit mask maps candidate bindings 1..4 to bits 0..3.

## 10. Encoder-finish crash witness

Immediately before the existing:

```rust
self.queue.submit(Some(encoder.finish()));
```

CF2 emits and flushes:

```text
ENCODER_FINISH_BEGIN
```

with the exact pair summary. The original `encoder.finish()` behavior is preserved and the WGPU validation panic is not intercepted or suppressed.

## 11. Promotion law

Physical attribution requires, in the same release process run:

```text
one or more FFN_FUSED_MIXED_ACCESS_SHARED_BACKING records
+
ENCODER_FINISH_BEGIN for the same execute_sequence
+
canonical WGPU STORAGE_READ_ONLY / STORAGE_READ_WRITE validation failure
```

If exactly one output binding shares backing:

```text
EXACT_FFN_FUSED_ALIAS_PAIR_ISOLATED
```

If multiple output bindings share backing:

```text
MULTI_FFN_FUSED_ALIAS_PAIR_ISOLATED
```

Do not arbitrarily select one pair when multiple are present.

If no `0 ↔ 1..4` pair shares backing while the canonical failure still reproduces:

```text
HOLD_R2B_CF2_NO_SHARED_BACKING_PAIR
```

## 12. Repair deferral

CF2 does not implement any repair. Only after exact physical closure may a later revision compare:

```text
access-class unification
selective detached backing
raw-lease / pooled-storage export authority
```

## 13. Baked source delta

```text
MOD crates/burn_webgpu_backend/src/base_train_ffn_tensorcube_persistent_executor.rs
ADD tools/validate_ash_r2b_cf2_ffn_fused_exact_backing_pair_static.py
DEL 0
```

No `Cargo.toml`, `Cargo.lock`, WGSL, or CubeCL source delta.

Source-delta digest:

```text
8222f14279b5f58691d29ae376223432ebb21616636a34516057e5e1d16ec0ce
```

Changed source SHA-256:

```text
base_train_ffn_tensorcube_persistent_executor.rs
b388912d2e936f0f0ec7ed67f938f62b807ef65120118b6f3ca27f2e0357c81b

validate_ash_r2b_cf2_ffn_fused_exact_backing_pair_static.py
fdce2fa86fc1ad665e1b2e02ffa6f7e975a139d35850cc11176745c2804f4962
```

## 14. Static acceptance

```powershell
python .\tools\validate_ash_r2b_cf2_ffn_fused_exact_backing_pair_static.py
```

Baked result:

```text
PASS_R2B_CF2_FFN_FUSED_EXACT_BACKING_PAIR_STATIC checks=48
```

## 15. Compile acceptance

The bake environment does not expose `cargo` or `rustc`, therefore compile evidence is not promoted by this bake.

Authoritative local checks:

```powershell
cargo check -p burn_webgpu_backend --lib --release --locked
cargo check -p base_train --bin base_train --release --locked -j 1
```

## 16. Bake artifacts

```text
Overlay:
ASH_R2B_CF2_FFN_FUSED_EXACT_BACKING_PAIR_ATTRIBUTION_OVERLAY_CODE_ONLY.zip
SHA-256 0a5fb0fc7dd2c29c6ba8d0c5494483d20e7e01d0de5d6d9e4a34d77cf118a92f
files=2
CRC=PASS

Full:
ASH_PASS3_R2B_CF2_FFN_FUSED_EXACT_BACKING_PAIR_ATTRIBUTION_CODE_ONLY.zip
SHA-256 eff71d5f25fec6111fce747d971b6cc87c4cd70850a5501b255c3c726d8e8512
files=8483
CRC=PASS
```

## 17. Evidence state at bake time

```text
SOURCE       CONFIRMED
STATIC       PASS 48/48
ARCHIVE      CRC PASS
COMPILE      UNVERIFIED
RUNTIME      UNVERIFIED
PHYSICAL     UNVERIFIED
PERFORMANCE  UNVERIFIED
```

## 18. Final law

> R2B-CF2 instruments only the FFN persistent fused dynamic buffer set that the release backtrace identified.
>
> Binding 0 remains READ and bindings 1..4 remain READ_WRITE; no access semantics are modified.
>
> Exact shared backing is admitted only through `Arc::ptr_eq()` on the live `RawWgpuBufferLease.buffer` values.
>
> All four input/output relations are recorded and flushed before `encoder.finish()`.
>
> The canonical WGPU validation failure must remain observable in the same execute invocation.
>
> No repair is permitted until the exact physical pair set is closed.
