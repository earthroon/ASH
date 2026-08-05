# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R3-C4

## Shader Loader Revision and Embedded Source Preflight Seal

> Parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R3-C3`  
> Kernel profile: `tensorcube-stage11-sg32-atlas-parallel-streaming-wave-finite-f32-v2`  
> Production admission: blocked  
> Proof ledger: HOLD

## SSOT

The Rust translation unit that owns the `include_str!` Stage11 shader sources must change revision together with finite-predicate WGSL changes. The runtime validates the embedded shader strings before `Device::create_shader_module`.

## Required preflight

```text
embedded R6-R3 shader isFinite identifier count = 0
candidate finite_f32 helper present = true
oracle finite_f32 helper present = true
parity finite_f32 helper present = true
invariant finite_f32 helper present = true
fixture finite_f32 helper present = true
IEEE-754 exponent mask 0x7f800000u present = true
kernel profile revision = finite-f32-v2
```

## Failure behavior

An unapplied or stale shader source must fail before shader-module creation with one of:

```text
AW02R6R3UndefinedWgslIsFiniteIdentifier:<label>
AW02R6R3FiniteF32PredicateMissing:<label>
AW02R6R3FiniteF32ExponentMaskMissing:<label>
```

A stale release executable is not accepted as evidence.
