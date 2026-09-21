# R2B-CF1
# FIRST PHYSICAL FORWARD DISPATCH STORAGE ACCESS / BACKING IDENTITY ATTRIBUTION

## Revision

```text
Patch ID:
ASH-BASETRAIN-BT-WGSL-CHECKPOINT-EXPORT-PROVENANCE-CAPTURE-ATLAS-RUNTIME-FORWARD-WAVE-STORAGE-ALIAS-ATTRIBUTION-06C-R27-R1J-R2B-CF1

Build revision:
bt-wgsl-checkpoint-export-provenance-capture-atlas-runtime-forward-wave-storage-alias-attribution-06c-r27-r1j-r2b-cf1

Class:
PHYSICAL DISPATCH ATTRIBUTION
WGPU STORAGE-USAGE COLLISION DIAGNOSTIC
NO FIX
```

Direct parent:

```text
R27-R1J-R2
ATLAS_RUNTIME_ADMITTED_RESIDENCY_READY
+
R27-R1J-R2A-CF1
V5 GENESIS STRUCTURAL FILL
```

## 1. Authoritative failure input

Current physical run passes:

```text
admission_verdict=ATLAS_RUNTIME_ADMITTED_RESIDENCY_READY
PASS_ASH_BASETRAIN_BT_WGSL_CHECKPOINT_EXPORT_PROVENANCE_CAPTURE_ATLAS_RUNTIME_ROUTE_ADMISSION_06C_R27_R1J_R2
```

then terminates in a physical WGPU dispatch:

```text
wgpu error: Validation Error
In a CommandEncoder
  In a dispatch command, indirect:false
Attempted to use Buffer with '' label with conflicting usages.
Current usage BufferUses(STORAGE_READ_ONLY)
new usage BufferUses(STORAGE_READ_WRITE)
EXIT=101
```

## 2. Evidence boundary

```text
CONFIRMED
- R2 route admission passed.
- ResidencyHandoffReady was reached.
- The crash class is a WGPU compute-dispatch storage usage collision.

SUPPORTED
- CubeCL-managed storage is the primary attribution surface.
- Layer-0 Q materialization is the highest-value first execution bracket.

UNKNOWN
- exact kernel
- exact binding pair
- exact logical tensor pair
- whether the backing collision is same StorageId or external alias
- whether CUBECL task aggregation is required for reproduction
```

CF1 MUST NOT promote UNKNOWN items without a physical witness.

## 3. Purpose

R2B-CF1 answers only:

```text
Q1. What is the final successfully entered R2B stage before the panic?
Q2. What exact CubeCL dispatch immediately precedes the panic?
Q3. Which binding pair shares a backing candidate with incompatible effective access?
Q4. Does CUBECL_WGPU_MAX_TASKS=1 change the failure boundary?
```

## 4. Non-goals

CF1 MUST NOT change:

```text
allocator policy
WGSL
bind-group ordering
binding access semantics
Fusion semantics
external alias ownership
storage lifetime
model values
optimizer state
training math
gradient math
Atlas scheduling
checkpoint format
R2A plan authority
```

CF1 MUST NOT add:

```text
CPU fallback
GPU readback
extra GPU upload
extra GPU dispatch
queue synchronization
alias materialization
copy-on-write repair
storage split repair
production tasks_max override
```

## 5. Stage ledger

When `ASH_R2B_CF1_STORAGE_ALIAS_TRACE=1`, base_train appends to:

```text
bt_wgsl_r27_r1j_r2b_cf1_stage_trace.jsonl
```

Required events:

```text
R2_ROUTE_RECEIPT_PUBLISHED
R2B_EMBEDDING_BEGIN
R2B_EMBEDDING_PHYSICAL_COMPLETE
R2B_EMBEDDING_ADOPTION_COMPLETE
R2B_LAYER_WAVE_ACTIVATED
R2B_LAYER_BLOCK_LOADED
R2B_PREPARED_SET_ENQUEUED
R2B_Q_RESOLVE_BEGIN
R2B_Q_RESOLVE_END
R2B_K_RESOLVE_BEGIN
R2B_K_RESOLVE_END
R2B_V_RESOLVE_BEGIN
R2B_V_RESOLVE_END
```

The ledger is append-only and host-side. Every record is flushed before continuing. It performs no GPU synchronization.

## 6. CubeCL dispatch witness

The active fork remains:

```text
vendor_fork_scaffold/cubecl-wgpu-ash
```

CF1 carries diagnostic metadata through:

```text
CompiledKernel
  -> pipeline creation
  -> cached R2bCf1PipelineTraceMeta
  -> ScheduleTask::Execute
  -> WgpuStream::register_pipeline
```

Captured pipeline metadata:

```text
kernel_id_debug
entrypoint_name
compiler_visibility[]
effective_visibility[]
exclusive_memory_only_compiled
```

The effective access used by the actual BindGroupLayout is authoritative for the diagnostic.

## 7. Storage identity witness

`WgpuResource` carries diagnostic-only fields:

```text
r2b_cf1_storage_id_debug
r2b_cf1_external_alias_state
```

For internal CubeCL resources the StorageId comes from the actual resolved StorageHandle.

For external aliases the same logical StorageId is retained and the alias state is recorded from the existing resolution path. CF1 performs no second alias lookup solely for diagnostics.

## 8. Native buffer identity law

The trace records:

```text
native_buffer_debug_identity
native_buffer_identity_authoritative=false
```

The debug representation is diagnostic only. It MUST NOT be promoted as an authoritative native-buffer identity.

Strong backing evidence in CF1 is:

```text
same StorageId
```

Distinct StorageIds with matching debug representation remain a candidate only.

## 9. Range relation

For each pair:

```text
SAME_EXACT_RANGE
RANGE_OVERLAP
RANGE_DISJOINT
```

Range disjointness does not exonerate a shared WGPU Buffer from usage-scope validation.

## 10. Dispatch trace

Output:

```text
bt_wgsl_r27_r1j_r2b_cf1_cubecl_dispatch_trace.jsonl
```

Minimum record:

```text
patch_id
process_run_id
dispatch_sequence
kernel_id
entrypoint_name
dispatch_kind
dispatch_xyz
tasks_count_before
tasks_max
compute_pass_reused
exclusive_memory_only_compiled
binding_count
bindings[]
```

Each binding records:

```text
ordinal
compiler_visibility
effective_visibility
storage_id_debug
resource_offset
resource_size
external_alias_state
native_buffer_debug_identity
native_buffer_identity_authoritative=false
```

## 11. Collision trace

Output:

```text
bt_wgsl_r27_r1j_r2b_cf1_collision_trace.jsonl
```

Pair classifications:

```text
SAME_STORAGE_MIXED_ACCESS
SAME_STORAGE_SAME_ACCESS
EXTERNAL_ALIAS_MIXED_ACCESS_CANDIDATE
SAME_NATIVE_DEBUG_MIXED_ACCESS_NON_AUTHORITATIVE
NO_BACKING_COLLISION
```

A mixed-access collision requires:

```text
READ + READ_WRITE
or
READ_WRITE + READ
```

The detector logs and continues into the original dispatch. It never repairs or suppresses the dispatch.

## 12. Trace cap

```text
R2B_CF1_TRACE_CAP = 512 physical CubeCL dispatches
```

After the cap the trace emits `TRACE_CAP_EXHAUSTED`. Silent truncation is forbidden.

## 13. Task aggregation control

Baseline keeps the existing runtime authority.

Control run changes only:

```text
CUBECL_WGPU_MAX_TASKS=1
```

This is attribution only and MUST NOT be promoted as a production fix in CF1.

Interpretation:

```text
32 fails + 1 fails same way
  -> aggregation not required; intra-dispatch alias gains support

32 fails + 1 moves/passes
  -> AGGREGATION_SENSITIVE_ALIAS_OR_ORDERING

baseline no longer reproduces
  -> HOLD_BASELINE_NOT_REPRODUCED
```

## 14. Exact promotion law

Physical promotion requires the same run to contain:

```text
one exact dispatch sequence
+
one exact mixed-access binding pair
+
authoritative same-StorageId backing evidence
+
canonical WGPU STORAGE_READ_ONLY / STORAGE_READ_WRITE validation failure
```

Then:

```text
PASS_R2B_CF1_PHYSICAL_WGPU_STORAGE_ALIAS_ATTRIBUTED
```

Otherwise:

```text
HOLD_R2B_CF1_ALIAS_ORIGIN_UNRESOLVED
```

or:

```text
HOLD_R2B_CF1_BASELINE_NOT_REPRODUCED
```

## 15. Baked source delta

```text
MOD crates/base_train/src/atlas_runtime_forward_wave_execution.rs
MOD vendor_fork_scaffold/cubecl-wgpu-ash/src/backend/base.rs
MOD vendor_fork_scaffold/cubecl-wgpu-ash/src/compute/schedule.rs
MOD vendor_fork_scaffold/cubecl-wgpu-ash/src/compute/server.rs
MOD vendor_fork_scaffold/cubecl-wgpu-ash/src/compute/storage.rs
MOD vendor_fork_scaffold/cubecl-wgpu-ash/src/compute/stream.rs
ADD tools/validate_ash_r27_r1j_r2b_cf1_storage_alias_attribution_static.py
```

No Cargo.toml or Cargo.lock change.

## 16. Static acceptance

Required static validator:

```powershell
python .\tools\validate_ash_r27_r1j_r2b_cf1_storage_alias_attribution_static.py
```

Baked result:

```text
PASS_R2B_CF1_STORAGE_ALIAS_ATTRIBUTION_STATIC checks=48
```

## 17. Compile acceptance

The bake environment used to produce this archive has no cargo/rustc executable. Therefore COMPILE is not promoted by the bake itself.

Authoritative local compile sequence:

```powershell
cargo check -p cubecl-wgpu --lib --release --locked
cargo check -p burn_webgpu_backend --lib --release --locked
cargo check -p base_train --bin base_train --release --locked -j 1
```

Only actual local success may promote COMPILE PASS.

## 18. Bake artifacts

```text
Overlay:
ASH_R27_R1J_R2B_CF1_STORAGE_ALIAS_ATTRIBUTION_OVERLAY_CODE_ONLY.zip
SHA-256 b53fcfce6fe7fae4593214ed11c391c1a9165fb4f68f14425679b22850065b76
files=7
CRC=PASS

Full:
ASH_PASS3_R27_R1J_R2B_CF1_STORAGE_ALIAS_ATTRIBUTION_CODE_ONLY.zip
SHA-256 43ade76d3b937b5678f4ca9ea3f574d0112b6c05e1a6d8bdf8a52107b8eb35ff
files=8482
CRC=PASS
```

## 19. Evidence state at bake time

```text
SOURCE       CONFIRMED
STATIC       PASS 48/48
ARCHIVE      CRC PASS
COMPILE      UNVERIFIED
RUNTIME      UNVERIFIED
PHYSICAL     UNVERIFIED
PERFORMANCE  UNVERIFIED
```

## 20. Final law

> R2 route admission remains closed and is not reopened by CF1.
>
> CF1 only transports diagnostic metadata and emits crash-surviving host traces around the first R2B physical forward execution.
>
> No allocator, WGSL, binding semantics, Fusion semantics, external alias ownership, task default, model value, optimizer state or training math is changed.
>
> Same StorageId with mixed effective access inside the dispatch that immediately precedes the canonical WGPU failure is the strongest CF1 attribution.
>
> Native Buffer debug text is non-authoritative and cannot independently close the issue.
>
> `CUBECL_WGPU_MAX_TASKS=1` is a same-source control, never the repair.
>
> If one exact physical backing/access pair is not proven, the correct result is HOLD.
