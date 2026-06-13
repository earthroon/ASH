# ASH-BASETRAIN-GPU-04R2-R2-R1 Bake Report

## Title

R2 Source R1B External Shard Probe Field Bind Fix / Compile Closure No Runtime No Upload Seal

## Fixed error

`AshBaseTrainGpu04r2R1bActualWgpuDeviceQueueProbeBundle` does not expose `source_04r2_r1_external_shard_ref_resolution_probe`.
The existing field is `external_shard_ref_resolution_probe`.

## Applied change

```rust
let source_04r2_r1_external_shard_ref_resolution_probe = source_r1b
    .external_shard_ref_resolution_probe
    .clone();
```

The emitted R2 bundle field remains named `source_04r2_r1_external_shard_ref_resolution_probe`; only the source bundle access path was corrected.

## Runtime boundary

No runtime execution, payload read, GPU buffer creation, queue write, compute dispatch, forward dispatch, optimizer step, or safetensors mutation was performed in this bake environment.
