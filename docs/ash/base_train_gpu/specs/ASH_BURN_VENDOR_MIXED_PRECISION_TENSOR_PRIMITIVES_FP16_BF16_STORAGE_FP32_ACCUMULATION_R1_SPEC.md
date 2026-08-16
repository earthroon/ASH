# ASH-BURN-VENDOR-MIXED-PRECISION-TENSOR-PRIMITIVES-FP16-BF16-STORAGE-FP32-ACCUMULATION-R1

## Patch

```text
ASH-BURN-VENDOR-MIXED-PRECISION-TENSOR-PRIMITIVES-FP16-BF16-STORAGE-FP32-ACCUMULATION-R1

Explicit Precision Profile Authority /
F32 Safe Baseline /
Packed FP16 Storage /
Packed BF16 Storage /
FP32 Working Arithmetic /
FP32 Matrix Accumulation /
FP32 Reduction /
Caller-Owned Encoder /
No Primitive-Owned Submit /
No Primitive-Owned Readback /
No Primitive-Owned Blocking Poll /
No Muon Formula Mutation /
No Softmax Semantic Mutation /
No Optimizer Formula Mutation
```

## Parent SSOT

```text
ASH-BURN-VENDOR-GPU-RESIDENT-VERIFICATION-COMPACT-READBACK-RECEIPT-ASYNC-STAGING-RING-AND-SUBMISSION-COALESCING-R1
```

This patch extends the local Burn vendor scaffold with reusable mixed-precision tensor primitives. It does not promote mixed precision into Muon, attention softmax, or optimizer commit policy.

## Authority

```text
FP32 master tensor / optimizer commit
= canonical authority

FP16/BF16 packed buffers
= derived execution representation

burn-wgpu-local
= physical conversion / matrix / reduction primitive producer

burn_webgpu_backend / BaseTrain
= semantic and policy authority
```

## Precision profiles

```text
F32Safe
Fp16StorageF32Accum
Bf16StorageF32Accum
```

`F32Safe` remains the production baseline authority.

`Fp16StorageF32Accum` stores operands as packed IEEE FP16 pairs in `u32`, expands them to `f32` for working arithmetic, and accumulates matrix/reduction state in `f32`.

`Bf16StorageF32Accum` stores deterministic rounded BF16 bit pairs in `u32`, expands them to `f32`, and accumulates in `f32`.

Native shader-F16 capability is observed but is not required for the R1 packed path. No native-BF16 arithmetic claim is made.

## Storage contract

```text
MIXED_PRECISION_STORAGE_REVISION = PACKED_HALF_U32_PAIR_R1
MIXED_PRECISION_ACCUMULATION_REVISION = FP32_ACCUMULATION_R1
MIXED_PRECISION_TILE_REVISION = GENERIC_MNK_ROW_MAJOR_R1
```

Two 16-bit elements share one physical `u32` word. Odd element counts zero the unused upper lane during quantization.

## GPU shader primitives

New WGSL:

```text
vendor_fork_scaffold/burn-wgpu-local/src/shaders/mixed_precision_tensor_primitives.wgsl
```

Entry points:

```text
quantize_fp16
quantize_bf16
decode_fp16
decode_bf16
matmul_fp16
matmul_bf16
reduce_fp16
reduce_bf16
```

FP16 storage conversion uses WGSL `pack2x16float` / `unpack2x16float`.

BF16 storage conversion uses deterministic round-to-nearest-even bit projection and exact BF16-to-F32 expansion.

Matrix kernels keep `var acc: f32` for the dot-product accumulator.

Reduction keeps `f32` workgroup sum-of-squares and maximum-absolute-value state, plus an explicit nonfinite counter.

## Rust primitive surface

New module:

```text
vendor_fork_scaffold/burn-wgpu-local/src/mixed_precision.rs
```

Main physical surface:

```text
VendorMixedPrecisionTensorPrimitives::new
VendorMixedPrecisionTensorPrimitives::encode_quantize
VendorMixedPrecisionTensorPrimitives::encode_decode
VendorMixedPrecisionTensorPrimitives::encode_matmul
VendorMixedPrecisionTensorPrimitives::encode_reduction
VendorMixedPrecisionTensorPrimitives::reduction_scratch
VendorMixedPrecisionTensorPrimitives::telemetry
```

All encode methods receive a caller-owned `CommandEncoder`. The primitive does not call `queue.submit`, does not create `MAP_READ` buffers, and does not call `PollType::Wait`.

## Persistent reduction scratch

One reusable 16-byte GPU reduction output buffer is allocated when the primitive runtime is created.

Telemetry distinguishes `reduction_scratch_allocation_count` and `reduction_scratch_reuse_count`. The reduction scratch is transient execution infrastructure and never becomes tensor, optimizer, generation, or checkpoint authority.

## Telemetry

```text
fp16_quantize_dispatch_count
bf16_quantize_dispatch_count
fp16_decode_dispatch_count
bf16_decode_dispatch_count
fp16_matmul_dispatch_count
bf16_matmul_dispatch_count
fp16_reduction_dispatch_count
bf16_reduction_dispatch_count
fp32_accumulation_dispatch_count
packed_operand_storage_bytes
f32_equivalent_storage_bytes
storage_bytes_avoided
reduction_scratch_allocation_count
reduction_scratch_reuse_count
queue_submit_count
full_tensor_readback_count
blocking_poll_count
```

R1 primitive-owned values for the final three counters are designed to remain zero. Submission and physical readback are caller/harness responsibilities.

## Canonical backend projection

`burn_webgpu_backend` re-exports the vendor primitive only under the existing `burn-raw-access-local` feature. This keeps `burn-wgpu-local` as the implementation primitive and `burn_webgpu_backend` as the canonical ASH backend public boundary without moving Muon/softmax/optimizer policy into the vendor crate.

## Physical harness

New BaseTrain binary:

```text
ash_burn_vendor_mixed_precision_tensor_primitives_harness_r1
```

The harness performs, for both FP16-storage and BF16-storage candidates:

```text
F32 source upload
packed quantization
packed decode to F32
2x4 x 4x2 matrix multiply with FP32 accumulation
FP32 sum-of-squares / max-abs reduction
physical GPU readback in harness only
finite gate
storage-byte-avoidance receipt
primitive submit/readback/blocking-poll zero receipt
```

The harness owns the queue submission and its diagnostic readback. That readback is not inside the vendor primitive hot path.

## Correctness status

Static validator:

```text
tools/validate_ash_burn_vendor_mixed_precision_tensor_primitives_r1_static.py
70/70 PASS
```

Parent regression gates retained in the bake environment:

```text
Vendor compact readback                       64/64 PASS
Generation-sealed Muon cache                  66/66 PASS
Muon backend surface rebind                   35/35 PASS
Local Muon multi-tile                         61/61 PASS
Local Muon production                         62/62 PASS
Local Muon PAD17                              52/52 PASS
FFN multi-slot                                78/78 PASS
FFN persistent slab                           66/66 PASS
FFN GPU timestamp/perf                       101/101 PASS
FFN physical perf                             72/72 PASS
FFN fused production                          45/45 PASS
GPU70K G45                                    42/42 PASS
GPU70K G27                                    35/35 PASS
GPU70K export                                 13/13 PASS
Atlas/HOTPATH                                 56/56 PASS
HOTPATH allocation                            26/26 PASS
```

## Evidence boundary

The bake environment does not contain `cargo`, `rustc`, or `rustfmt`.

Therefore:

```text
STATIC_BAKED_READY
NO_LOCAL_RUST_COMPILE_CLAIM
PHYSICAL_GPU_HARNESS_REQUIRED
NO_MIXED_PRECISION_PRODUCTION_PROMOTION
```

User-local Cargo and GPU harness output remain the final execution SSOT.

## Non-goals

```text
No FP16 accumulator
No BF16 accumulator
No native-BF16 arithmetic claim
No stochastic rounding
No dynamic loss scaling
No half-precision master parameter
No half-precision checkpoint authority
No mixed-precision Muon production adoption
No mixed-precision softmax production adoption
No automatic precision tuner
No automatic production default switch
```

## Next adoption line

```text
ASH-BURN-VENDOR-VARIABLE-ROW-ONLINE-SOFTMAX-DESCRIPTOR-DISPATCH-AND-FP32-STATE-REDUCTION-R1

ASH-BASETRAIN-HIMUON-HIERARCHICAL-TILE-SCHEDULE-CROSS-LAYER-BATCHING-AND-MIXED-PRECISION-ADOPTION-R1
```

Those patches must establish their own numerical parity and stability gates. Vendor primitive PASS alone does not prove mixed-precision Muon or softmax safety.

## Promotion target

```text
PROMOTE_ASH_BURN_VENDOR_MIXED_PRECISION_TENSOR_PRIMITIVES_FP16_BF16_STORAGE_FP32_ACCUMULATION_R1

EXPLICIT_PRECISION_PROFILE
F32_SAFE_BASELINE
PACKED_FP16_STORAGE
PACKED_BF16_STORAGE
FP32_WORKING_ARITHMETIC
FP32_MATRIX_ACCUMULATION
FP32_REDUCTION
PERSISTENT_REDUCTION_SCRATCH
CALLER_OWNED_ENCODER
NO_PRIMITIVE_SUBMIT
NO_PRIMITIVE_READBACK
NO_PRIMITIVE_BLOCKING_POLL
NO_MUON_FORMULA_MUTATION
NO_SOFTMAX_SEMANTIC_MUTATION
NO_OPTIMIZER_FORMULA_MUTATION
NO_AUTOMATIC_PRODUCTION_PROMOTION
SEALED
```