# R2B-CF2
# FFN PERSISTENT FUSED DYNAMIC BINDGROUP EXACT BACKING / ACCESS PAIR ATTRIBUTION

## Revision

```text
Patch ID:
ASH-BASETRAIN-R2B-FFN-PERSISTENT-FUSED-EXACT-BACKING-PAIR-ATTRIBUTION-CF2

Build revision:
r2b-cf2-ffn-persistent-fused-exact-backing-pair-attribution

Class:
PHYSICAL WGPU BINDING ATTRIBUTION
FFN PERSISTENT EXECUTOR
DIAGNOSTIC ONLY
NO FIX
```

Direct parent: R2B-CF1 FIRST PHYSICAL FORWARD DISPATCH STORAGE ACCESS / BACKING IDENTITY ATTRIBUTION.

## 1. Parent physical evidence

```text
exit=101
wgpu error: Validation Error
In a CommandEncoder
  In a dispatch command, indirect:false
Current usage BufferUses(STORAGE_READ_ONLY)
new usage BufferUses(STORAGE_READ_WRITE)

backtrace:
wgpu::CommandEncoder::finish
→ BaseTrainFfnTensorCubePersistentExecutor::execute
→ actual_decoder_block_split_forward
→ atlas_runtime_forward_wave_execution
```

CF1 generic CubeCL tracing observed pooled same-storage disjoint-range pairs with READ_WRITE ↔ READ_WRITE. CF2 therefore narrows to the FFN persistent fused dynamic BindGroup.

## 2. Exact candidate set

```text
binding 0 = input_hidden     READ
binding 1 = gate_pre_out     READ_WRITE
binding 2 = silu_gate_out    READ_WRITE
binding 3 = up_linear_out    READ_WRITE
binding 4 = ffn_product_out  READ_WRITE

candidate pairs:
0↔1
0↔2
0↔3
0↔4
```

## 3. Exact backing authority

For every candidate output CF2 evaluates:

```rust
Arc::ptr_eq(&input_hidden.buffer, &candidate.buffer)
```

This is the authoritative CF2 same-backing test inside one executor invocation.

## 4. Diagnostic activation

```text
ASH_R2B_CF2_FFN_FUSED_ALIAS_TRACE=1
ASH_R2B_CF2_TRACE_ROOT=<trace directory>
ASH_R2B_CF2_PROCESS_RUN_ID=<run id>
```

Default OFF. Trace file:

```text
r2b_cf2_ffn_fused_alias_trace.jsonl
```

## 5. Pair witness

Every pair records execute_sequence, layer_index, source_weight_generation, tensor_set_digest, binding roles/access, same_buffer, range_relation, offset/size/len windows, shapes, primitive IDs, stream IDs, bridge modes, active states, and classification.

```text
same_buffer=true
→ FFN_FUSED_MIXED_ACCESS_SHARED_BACKING

same_buffer=false
→ DISTINCT_BACKING
```

Range relation:

```text
EXACT_RANGE
OVERLAPPING_RANGE
DISJOINT_RANGE
RANGE_OVERFLOW
```

Range disjointness does not exonerate the shared WGPU Buffer.

## 6. Complete candidate preservation

All four pairs are logged. Summary fields:

```text
shared_backing_pair_count
shared_binding_mask
mixed_access_shared_backing_present
```

Multiple true pairs remain a multi-pair attribution. CF2 never invents one winner.

## 7. Encoder finish witness

Immediately before encoder.finish() CF2 flushes:

```text
[R2B-CF2][encoder-finish-begin]
```

The original GPU path remains encoder.finish() → queue.submit(command_buffer).

## 8. Non-goals

CF2 changes no BindGroupLayout access flag, WGSL, bind ordering, allocator policy, CubeCL pooled storage, RawWgpuBufferLease ownership, Fusion semantics, residency semantics, optimizer state, model value, training math, or gradient math.

CF2 adds no GPU dispatch, GPU copy, GPU map, GPU wait, CPU fallback, selective materialization, access unification, or allocator split.

## 9. Source scope

```text
MOD crates/burn_webgpu_backend/src/base_train_ffn_tensorcube_persistent_executor.rs
ADD tools/validate_ash_r2b_cf2_ffn_fused_exact_backing_pair_static.py
DEL 0

Cargo.toml delta = 0
Cargo.lock delta = 0
shader delta = 0
CubeCL vendor delta = 0
```

## 10. Static acceptance

```powershell
python .\tools\validate_ash_r2b_cf2_ffn_fused_exact_backing_pair_static.py
```

Baked result:

```text
PASS_R2B_CF2_FFN_FUSED_EXACT_BACKING_PAIR_STATIC checks=62
```

## 11. Physical closure

Promote PASS_R2B_CF2_PHYSICAL_FFN_FUSED_ALIAS_PAIR_ATTRIBUTED only when the same release run contains an exact Arc::ptr_eq shared-backing pair, binding 0 READ, output binding READ_WRITE, ENCODER_FINISH_BEGIN for the same execute_sequence, and the canonical WGPU STORAGE_READ_ONLY / STORAGE_READ_WRITE failure.

Otherwise use:

```text
HOLD_R2B_CF2_NO_SHARED_BACKING_PAIR
HOLD_R2B_CF2_BASELINE_NOT_REPRODUCED
HOLD_R2B_CF2_TRACE_INCOMPLETE
```

## 12. Repair deferral

CF2 does not implement CF3-A ACCESS-CLASS UNIFICATION, CF3-B SELECTIVE DETACHED OUTPUT BACKING, or CF3-C RAW-LEASE / POOLED-STORAGE EXPORT AUTHORITY.

## 13. Bake hashes

```text
executor source SHA-256
b2152b16d22913810a07f1697cada6d9aeab0cb8aa6b8c3013f83c8b3ba2fbf7

validator SHA-256
9b96daa5f658a8a1e9713382f320d57e4e50aacc35b81f0462a7047d01bf3378

overlay ZIP
bf30e960eda1beb92c720c9a268a99b1f44542357d9cf5fa42e9f4313cf8c9c4
files=2
CRC=PASS

full ZIP
9b9f193878d23fd88f3e6f3b82b59ce1fe04f389cb3cc52c44e3acaec013581c
files=8483
CRC=PASS
```

## 14. Evidence state at bake time

```text
SOURCE       CONFIRMED
STATIC       PASS 62/62
ARCHIVE      CRC PASS
COMPILE      UNVERIFIED
RUNTIME      UNVERIFIED
PHYSICAL     UNVERIFIED
PERFORMANCE  UNVERIFIED
```

The bake environment has no cargo/rustc executable, so compile/runtime/physical status is not promoted.

## 15. Final law

> R2B-CF2 narrows the physical failure to exact RawWgpuBufferLease backing identity inside the FFN persistent fused dynamic BindGroup.
>
> Arc::ptr_eq() is the same-backing authority. All four candidate pairs are preserved.
>
> Range relation is diagnostic only and does not override same-buffer identity.
>
> CF2 flushes a witness immediately before encoder.finish() and then executes the original command path unchanged.
>
> No access mode, allocator, WGSL, Fusion behavior, storage ownership, optimizer state, model value, or training math is changed.
>
> If the exact shared mixed-access pair is not physically observed in the same run as the canonical WGPU failure, the correct result is HOLD.