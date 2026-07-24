# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R4

## Reference Dedicated Native Scratch Output /
## Burn Arena Read-Write Dealias /
## Underlying Buffer Identity Matrix Gate /
## Zero-Copy Input Preservation Seal

## 0. Identity

```text
patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R4
parent_patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R3
runtime_schema=ash.attn.headwise.causal.01b.r12.r3.r3.r3.r2.r4.runtime_artifact.v1
local_manifest_schema=ash.attn.headwise.causal.01b.r12.r3.r3.r3.r2.r4.local_manifest.v1
public_abi_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R4
reference_validation_scope_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R3
reference_scratch_ownership_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R4
buffer_identity_matrix_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R4
promotion_scope=incremental_decode_only
```

R2-R4 changes Reference measurement output storage ownership. Attention math, WGSL arithmetic, route policy, timestamp boundaries, guard ring capacities, performance thresholds and Q/K/V values remain unchanged.

## 1. Bound failure

R2-R3 captured the original WGPU validation error at production `seq_kv=8`:

```text
Current usage=STORAGE_READ_ONLY
new usage=STORAGE_READ_WRITE
STORAGE_READ_WRITE is exclusive within one compute dispatch usage scope
```

The logical Burn output tensor was distinct from Q/K/V, but Burn could allocate it as another subrange of the same underlying WGPU buffer. WGPU validates usage by native buffer identity, not logical tensor identity or disjoint offset ranges.

Required classification:

```text
observed_stage=encoder_finish
semantic_first_fault=reference_dispatch_resource_usage
root_cause=Burn arena read-only/read-write native buffer alias
```

## 2. Ownership SSOT

```text
Q/K/V owner=Burn tensor runtime
Q/K/V access=STORAGE_READ_ONLY
Q/K/V transfer=existing same-device raw native leases

Reference output owner=Headwise native Reference scratch allocator
Reference output access=STORAGE_READ_WRITE
Reference output transfer=none
```

Reference output must not be created with `Tensor::empty`, borrowed through `bridge_native_tensor_f32_live_strict`, mapped at creation or backed by a host-visible staging buffer.

## 3. Dedicated scratch

Required backend type:

```rust
pub struct HeadwiseReferenceMeasurementScratch {
    pub buffer: Arc<BackendBuffer>,
    pub buffer_identity: u64,
    pub shape: [usize; 4],
    pub len_elements: usize,
    pub len_bytes: u64,
    pub allocation_serial: u64,
    pub usage_bits: u64,
    pub burn_arena_owned: bool,
    pub mapped_at_creation: bool,
}
```

Canonical allocation:

```rust
device.create_buffer(&wgpu::BufferDescriptor {
    label: Some("headwise.reference.measurement.dedicated_output"),
    size: checked_output_bytes,
    usage: wgpu::BufferUsages::STORAGE,
    mapped_at_creation: false,
})
```

For `[1,32,1,64]` f32 output:

```text
element_count=2048
byte_length=8192
```

Checked arithmetic is mandatory.

## 4. Bind-group migration

Reference binding contract:

```text
binding 0=params uniform
binding 1=Q original native lease
binding 2=K original native lease
binding 3=V original native lease
binding 4=dedicated native Reference scratch
```

The authoritative Reference measurement APIs accept `HeadwiseReferenceMeasurementScratch`, not a Burn output tensor.

## 5. Underlying buffer identity gate

Before bind-group admission, R2-R4 records actual native buffer identities for Q, K, V and Reference scratch.

Mandatory invariants:

```text
scratch != Q backing buffer
scratch != K backing buffer
scratch != V backing buffer
read_write_alias_count=0
write_write_alias_count=0
```

Read-only aliases among Q/K/V may be receipted. Any same-buffer relation involving Reference `STORAGE_READ_WRITE` is rejected even when byte ranges do not overlap.

Policy ID:

```text
headwise.reference.buffer.alias.policy.v1
```

## 6. Zero-copy preservation

Required:

```text
Q original buffer identity=Q bound buffer identity
K original buffer identity=K bound buffer identity
V original buffer identity=V bound buffer identity

Q/K/V device copy count=0
Q/K/V host materialization count=0
Q/K/V host upload count=0
```

Forbidden repairs include copying Q/K/V into dedicated buffers, CPU readback and re-upload, permissive raw-bridge fallback and validation disablement.

## 7. Preflight integration

The R2-R3 validation preflight remains active. The order is:

```text
prepare exact Q/K/V leases
allocate dedicated Reference scratch outside timed span
run native buffer identity gate
validate pipeline resources
validate exact bind group
encode isolated Reference pass on fresh encoder
finish and submit preflight
admit production warmup and timing
```

Known conflicting usage must be prevented by the native gate and must not reach WGPU validation.

## 8. Performance boundary

Scratch allocation, identity receipt construction and preflight polling occur outside measured timestamp spans.

Required:

```text
scratch_allocation_inside_timed_span_count=0
scratch_wait_inside_timed_span_count=0
scratch_samples_in_performance_population=0
scratch_output_value_readback_count=0
scratch_output_host_materialization_count=0
scratch_output_promotion_count=0
```

The timed Reference dispatch writes directly to the already allocated scratch.

## 9. Receipts

Required backend receipts:

```text
HeadwiseReferenceScratchAllocationReceipt
HeadwiseReferenceBufferIdentityReceipt
HeadwiseReferenceZeroCopyInputReceipt
HeadwiseReferenceMeasurementPreflightReceipt
```

Required runtime artifacts:

```text
ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r4_scratch_allocation_receipts.json
ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r4_buffer_identity_matrix_receipts.json
ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r4_zero_copy_input_receipts.json
```

Runtime artifacts, local manifests, target directories and repository metadata are excluded from the source bake.

## 10. Negative controls

R2-R4 inherits 1000 controls and adds 40 controls:

```text
scratch ownership=10
identity matrix=10
zero-copy inputs=10
scratch lifecycle and timing boundary=10

total=1040
executed=1040
skipped=0
fail=0
```

## 11. Required CLI additions

```text
--reference-output-storage dedicated-native-scratch
--reference-scratch-ring-capacity 4
--require-reference-scratch-burn-arena-owner false
--require-reference-scratch-mapped-at-creation false
--require-underlying-buffer-identity-matrix true
--require-reference-read-write-alias-zero true
--require-reference-write-write-alias-zero true
--require-reference-atlas-output-dealias true
--require-q-zero-copy-identity true
--require-k-zero-copy-identity true
--require-v-zero-copy-identity true
--require-input-device-copy-zero true
--require-input-host-materialization-zero true
--require-input-host-upload-zero true
--require-reference-scratch-reuse-before-completion-zero true
--require-reference-scratch-concurrent-bind-zero true
--require-reference-scratch-ring-exhaustion-zero true
--require-reference-scratch-timed-allocation-zero true
--require-reference-scratch-timed-wait-zero true
--require-reference-scratch-performance-population-zero true
--require-reference-scratch-readback-zero true
--require-reference-scratch-host-materialization-zero true
--require-reference-scratch-promotion-zero true
--require-reference-full-overwrite true
--expected-negative-controls 1040
```

## 12. PASS boundary

PASS requires exact R2-R3 source binding, preserved dispatcher ownership and validation scopes, dedicated native Reference scratch, Burn arena owner false, mapped-at-creation false, exact scratch size, zero Q/K/V-to-scratch aliases, zero incompatible read/write aliases, exact Q/K/V zero-copy identities, zero input copies or host fallback, zero scratch readback or promotion, successful Reference preflight for every production bucket, complete probe/performance/tail/rollback truth, 1040 controls and static/digest truth.

PASS proves the known WGPU usage conflict is eliminated without copying inputs. It does not prove Reference numerical output parity, universal adapter performance, transactional KV rollback, canonical full-model decode or model-quality improvement.

## 13. Expected tokens

PASS:

```text
PASS_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R4_REFERENCE_DEDICATED_NATIVE_SCRATCH_OUTPUT_BURN_ARENA_READ_WRITE_DEALIAS_UNDERLYING_BUFFER_IDENTITY_MATRIX_ZERO_COPY_INPUT_PRESERVATION_REFERENCE_VALIDATION_AND_PRODUCTION_MEASUREMENT_TRUTH_INCREMENTAL_ONLY_NO_OUTPUT_VALUE_READBACK_NO_MODEL_QUALITY_OVERCLAIM
```

HOLD:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R4_REFERENCE_SCRATCH_OWNERSHIP_BUFFER_DEALIAS_OR_ZERO_COPY_INPUT_PRESERVATION_INCOMPLETE
```
