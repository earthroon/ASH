# TENSORCUBE-CONSUME-R2-COMPILEFIX1

## Rust type-inference / R6 shadow-stride compile closure

```text
+ R6 LEGACY SHADOW STRIDE TYPE PARITY
+ R2 COALESCER OUTPUT TYPE ANNOTATION
+ NO EXECUTION SEMANTIC CHANGE
+ NO RELATION GEOMETRY CHANGE
+ NO GPU CONSUME CHANGE
+ NO CHECKPOINT HOT-CAPTURE CHANGE
```

## Parent

```text
ASH_PASS3_BPDK_CHECKPOINT_R1_GPU_HOT_SNAPSHOT_CAPTURE_CODE_ONLY.zip
SHA-256 29f5c73edd85bdf650b09bf4880794908e550f12a4d274fb22593f1621db5492
```

## Compile failures

```text
E0308 / E0277:
legacy TensorCubeLocalMuonBatchTileDescriptor.gradient_row_stride_elements is usize,
but R6 shadow validation compared it with u32::try_from(R6_TILE_SIDE).

E0282:
coalesce_ranges_r2 output Vec element type was not inferable before first push.
```

## Closure

```rust
d.gradient_row_stride_elements != usize::try_from(R6_TILE_SIDE)?
```

and:

```rust
let mut out: Vec<TensorCubeConsumePhysicalRangeR2> =
    Vec::with_capacity(ranges.len());
```

The R6 physical descriptor itself remains u32 and its construction is unchanged.

## Changed files

```text
MOD crates/base_train/src/unified_atlas_mcu_global_tensorcube_job_queue_r6.rs
MOD crates/base_train/src/tensorcube_consume_plane_r2.rs
ADD tools/validate_ash_tensorcube_consume_r2_compilefix1_static.py
```

## Static qualification

```text
PASS_TENSORCUBE_CONSUME_R2_COMPILEFIX1_STATIC checks=4
PASS_TENSORCUBE_CONSUME_R2_GPU_PARALLEL_PLANE_STATIC checks=61
PASS_BP_DK_CHECKPOINT_R1_GPU_HOT_CAPTURE_STATIC checks=46
PASS_TENSORCUBE_CONSUME_R1_RELATION_AUTHORITY_STATIC checks=56
PASS R6
PASS RAM36 current-source checks=32
PASS CF11-R1 checks=22
PASS BP-DK generation binding checks=27
PASS R8A checks=30
PASS packed address checks=26
PASS packed M/V checks=27
```

Rust toolchain is unavailable in the bake environment; COMPILE is not claimed here.

## Artifacts

```text
Overlay
ASH_BPDK_CHECKPOINT_R1_TENSORCUBE_R2_COMPILEFIX1_OVERLAY_CODE_ONLY.zip
SHA-256 fc815358add62775beab66ae9944238d7d02679c03e9bc7c8088afc7c20b4791
FILES 3
CRC PASS

Full
ASH_PASS3_BPDK_CHECKPOINT_R1_TENSORCUBE_R2_COMPILEFIX1_CODE_ONLY.zip
SHA-256 42dc9393dddf7e14bab9071fa8a89fe19aac6ecbc3d8a35077065ccf9c701adf
FILES 8446
CRC PASS
```

## Final law

> This revision changes only Rust type agreement and inference. R6 geometry, R1 relation authority, R2 D2D consume topology, B06 ordering, and BP-DK hot checkpoint capture semantics are unchanged.
