# ASH-TCU-DECODE-MIN1-R1 Argmax Uniform 16-Byte ABI Alignment Repair

## 0. Metadata

- Parent: `ASH-TCU-DECODE-MIN1-R1 Runtime Validation Origin Repair`
- Patch class: runtime ABI alignment repair
- Functional revision increase: not authorized
- New decode capability: not authorized
- New truth-audit revision: not authorized
- New receipt or manifest hierarchy: not authorized
- General production promotion: not authorized

## 1. Confirmed failure

The MIN1 fixture recorded one first-pass dispatch and skipped the finalize pass, but encoder validation failed with:

```text
Buffer is bound with size 16 where the shader expects 32
in group[0] compact index 0
```

The captured state was:

```text
last_successful_stage=fixture_copy_record
first_validation_error_stage=fixture_encoder_finish
fixture_first_pass_group_count=1
fixture_first_pass_dispatch_count=1
fixture_finalize_dispatch_count=0
live_lane_authorized=false
live_lane_started=false
```

The validation-origin repair therefore worked. The remaining fault is an argmax uniform ABI mismatch.

## 2. Root cause

The Rust host structure occupies sixteen bytes:

```rust
#[repr(C)]
struct GpuPenaltyArgmaxUniform {
    vocab_size: u32,
    padding: [u32; 3],
}
```

The WGSL uniform used this shape:

```wgsl
struct ArgmaxUniform {
    vocab_size: u32,
    _pad0: vec3<u32>,
};
```

In the uniform address space, the `vec3<u32>` member has sixteen-byte alignment. It therefore starts at byte offset sixteen and makes the WGSL structure require thirty-two bytes.

The compact argmax output remains a valid independent sixteen-byte structure and is not the source of this failure.

## 3. Canonical uniform ABI

The shared argmax uniform contract is:

```text
lane 0 = vocab_size
lane 1 = reserved_0
lane 2 = reserved_1
lane 3 = reserved_2
size = 16 bytes
```

All reserved lanes must be initialized to zero.

## 4. First-pass WGSL repair

Target:

```text
crates/model_core/src/shaders/gpu_penalty_argmax.wgsl
```

Required structure:

```wgsl
struct ArgmaxUniform {
    params: vec4<u32>,
};
```

The vocabulary length is read from:

```wgsl
u.params.x
```

The previous `u32 + vec3<u32>` representation is forbidden.

## 5. Finalize WGSL repair

Target:

```text
crates/model_core/src/shaders/gpu_penalty_argmax_finalize.wgsl
```

The finalize shader must use the same `vec4<u32>` contract and read its partial-count value from `u.params.x`.

A first-pass-only repair is forbidden because the live vocabulary requires a multi-workgroup finalize reduction.

## 6. Rust host contract

The existing Rust representation may remain:

```rust
#[repr(C)]
struct GpuPenaltyArgmaxUniform {
    vocab_size: u32,
    padding: [u32; 3],
}
```

It serializes to four contiguous `u32` lanes and is compatible with WGSL `vec4<u32>` when its total size is exactly sixteen bytes.

Required compile-time seals:

```rust
const _: [(); 16] = [(); size_of::<GpuPenaltyArgmaxUniform>()];
const _: [(); 16] = [(); size_of::<GpuPenaltyArgmaxOut>()];
```

## 7. Purpose-scoped bind-group layout

The argmax first-pass and finalize layouts must use an argmax-specific uniform entry with:

```text
buffer type=Uniform
has_dynamic_offset=false
min_binding_size=16
```

The generic uniform helper must not be globally changed when unrelated pipelines use different uniform structures.

The following paths require the explicit sixteen-byte minimum:

```text
MIN1 fixture first-pass
MIN1 fixture finalize
live argmax first-pass
live argmax finalize
```

## 8. Compact output preservation

The compact output remains:

```rust
#[repr(C)]
struct GpuPenaltyArgmaxOut {
    token_id: u32,
    padding0: u32,
    score: f32,
    padding1: f32,
}
```

Required size:

```text
16 bytes
```

The partial-output stride, final output, copy size and readback size must not be enlarged to thirty-two bytes.

## 9. Runtime artifact evidence

The existing MIN1 artifact path and schema lineage remain.

The artifact must record:

```text
argmax_uniform_rust_size
argmax_uniform_wgsl_required_size
argmax_uniform_bound_size
argmax_uniform_abi_match
first_pass_uniform_abi_match
finalize_uniform_abi_match
```

Expected values:

```text
argmax_uniform_rust_size=16
argmax_uniform_wgsl_required_size=16
argmax_uniform_bound_size=16
argmax_uniform_abi_match=true
first_pass_uniform_abi_match=true
finalize_uniform_abi_match=true
```

These fields are structural invariants and do not independently prove physical execution.

## 10. Fixture conditions

Fixture PASS requires:

```text
fixture_first_pass_group_count=1
fixture_first_pass_dispatch_count=1
fixture_finalize_dispatch_count=0
fixture_readback_count=1
fixture_readback_bytes=16
fixture_token_parity_verified=true
fixture_score_parity_verified=true
fixture_encoder_terminal_state=finalized
fixture_lane_pass=true
```

Only fixture PASS may authorize the live lane.

## 11. Live-path continuity

The live first-pass and finalize pipelines must consume the same sixteen-byte uniform contract.

No fallback is authorized:

```text
CPU greedy
host logits materialization
legacy sampler
single-workgroup-only substitution
```

If the finalize ABI differs or cannot be established, the live lane must fail closed.

## 12. Truth-audit integration

`ASH-TRUTH-AUDIT-01-R2` may accept Decode MIN1 physical proof only when all three uniform sizes equal sixteen and all ABI match fields are true.

Evidence mapping remains:

```text
uniform ABI equality -> ComputedInvariant
fixture GPU/reference parity -> IndependentComparator
live GPU completion and compact readback -> RuntimeObservation
```

## 13. Required tests

```text
Rust argmax uniform size is sixteen bytes
Rust compact output size is sixteen bytes
first-pass WGSL contains params: vec4<u32>
finalize WGSL contains params: vec4<u32>
neither shader contains _pad0: vec3<u32>
both shaders read u.params.x
argmax layouts declare min_binding_size=16
reserved Rust lanes are zero initialized
single-workgroup fixture still performs zero finalize dispatches
multi-workgroup finalize retains the same uniform ABI
```

## 14. PASS conditions

This repair passes when:

```text
Rust uniform size=16
first-pass WGSL required size=16
finalize WGSL required size=16
first-pass bound size=16
finalize bound size=16
all ABI match fields=true
previous shader-expects-32 error absent
fixture token and score parity pass
fixture encoder reaches finalized
live lane is authorized only after fixture PASS
```

The full MIN1 PASS still requires all original live-model physical-proof conditions.

## 15. FAIL conditions

```text
first-pass shader still requires thirty-two bytes
finalize shader still requires thirty-two bytes
first-pass and finalize layouts diverge
Rust uniform size is not sixteen
bound size is not sixteen
reserved lanes are uninitialized
compact output is enlarged to hide the uniform error
validation-origin scopes are weakened or removed
fixture failure authorizes the live lane
```

## 16. Non-goals

This repair does not change:

```text
argmax mathematics
tie policy
NaN policy
compact output ABI
readback size
live Fusion resolution
same-device raw borrowing
sampled decoding
production routes
```

## 17. Canonical seal

```text
The failing sixteen-byte binding was the argmax uniform, not the compact output.

The canonical argmax uniform is four contiguous u32 lanes occupying exactly
sixteen bytes. The Rust serializer, first-pass shader, finalize shader,
bind-group layout and runtime binding share that single contract.

No fixture-only repair.
No first-pass/finalize divergence.
No implicit binding size.
No output-buffer enlargement to conceal a uniform-layout mismatch.
```
