# ASH-ATTN-HEADWISE-CAUSAL-01A-R4

## Atlas Parallel Group Map /
## KV-Head Group Ownership /
## Workgroup-Y Parallel Dispatch /
## Primary Artifact Macro Recursion Closure

```text
patch_id=ASH-ATTN-HEADWISE-CAUSAL-01A-R4
parent_patch_id=ASH-ATTN-HEADWISE-CAUSAL-01A-R3
correction_class=atlas_parallel_group_map_execution_and_artifact_compile_truth_closure
```

## Problem

The previous gate still represented the headwise atlas dispatch as one globally flattened output domain and emitted the primary artifact through one large `serde_json::json!` invocation.

This created two issues:

```text
1. the primary artifact exceeded serde_json macro recursion depth
2. the runtime did not make the atlas GQA parallel-group map an explicit GPU input and dispatch axis
```

A recursion-limit increase is not accepted as the fix because it preserves the wrong artifact assembly shape and does not close atlas group ownership.

## Parallel group map SSOT

For the canonical model topology:

```text
q_heads=32
kv_heads=4
query_heads_per_kv=8
```

The atlas parallel map is:

```text
group 0: kv_head=0, q_head_start=0,  q_head_count=8
group 1: kv_head=1, q_head_start=8,  q_head_count=8
group 2: kv_head=2, q_head_start=16, q_head_count=8
group 3: kv_head=3, q_head_start=24, q_head_count=8
```

Add the GPU-visible ABI:

```rust
#[repr(C)]
pub struct HeadwiseAtlasParallelGroupEntry {
    pub group_id: u32,
    pub kv_head: u32,
    pub q_head_start: u32,
    pub q_head_count: u32,
}
```

The complete map must be stored in the cached `HeadwiseAtlasPlan`, uploaded as one storage buffer, and bound to the active shader.

## Dispatch ownership

One compute pass and one queue submission encode the complete parallel atlas operation.

Canonical axes:

```text
workgroup_x = flat output element within one atlas group
workgroup_y = atlas group id / KV-head owner
workgroup_z = batch index
```

Required dispatch:

```text
dispatch_x=ceil(max_group_output_elements/64)
dispatch_y=group_count
dispatch_z=batch
```

Forbidden:

```text
single global total_out flat map as the sole ownership model
one queue submission per head group
one command encoder per head group
CPU loop that commits group outputs separately
implicit q_head/kv_head reconstruction without group-map validation
```

## Shader contract

The active shader must consume:

```wgsl
@group(0) @binding(6)
var<storage, read> parallel_group_map: array<AtlasParallelGroup>;
```

For each invocation:

```text
group_id=global_invocation_id.y
batch=global_invocation_id.z
q_head=group.q_head_start+q_head_offset
kv_head=group.kv_head
```

The shader must reject invalid group ids, invalid KV heads, out-of-range Q heads, and group entries inconsistent with the canonical GQA mapping.

The causal `visible_count` contract remains unchanged and is applied independently inside every parallel group.

## Runtime receipts

Add:

```text
workspace/runtime/attention/ash_attn_headwise_causal_01a_parallel_group_map.json
```

Required fields:

```text
map_id
owner=kv_head
group_count
entries
dispatch_axes
single_compute_pass=true
single_queue_submit=true
all_route_maps_valid
pass
```

Every route receipt must bind:

```text
parallel_group_count
parallel_group_map
parallel_group_map_valid
parallel_dispatch=[x,y,z]
```

PASS requires exact Q-head coverage with no gap or overlap and exactly one owner KV head per group.

## Primary artifact compile closure

The large primary artifact must not be emitted through one recursive `json!({...})` call.

Required construction:

```text
serde_json::Map
field-by-field insertion
Value::Object(primary_map)
```

Adding `#![recursion_limit]` without restructuring is forbidden.

## Scope preservation

This correction does not change:

```text
absolute query-position SSOT
KV visibility upper bound
prefill/incremental/chunked route definitions
future-key poisoning criteria
GQA topology
text-density freeze
shadow-only authority boundary
production replacement default=false
model-quality non-claim
```

## PASS addition

The existing 01A PASS formula additionally requires:

```text
parallel_group_map_pass=true
parallel_group_count=kv_heads
parallel dispatch Y dimension=group_count
parallel dispatch Z dimension=batch
exact Q-head coverage
no group overlap
no group gap
single compute pass
single queue submission
```
