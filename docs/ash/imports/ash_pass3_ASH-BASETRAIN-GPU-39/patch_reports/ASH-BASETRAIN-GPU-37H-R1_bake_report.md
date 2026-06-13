# ASH-BASETRAIN-GPU-37H-R1 Bake Report

## Result

Baked.

## Fix Applied

`serde_json::json!` recursion-limit failure was addressed by converting the large receipt literal into an atlas-tiled, parallel-section receipt layout.

## Key Change

Before:

```txt
receipt_json() -> one huge json!({ ... })
```

After:

```txt
receipt_json()
  -> receipt_atlas_root(vec![
       ("acceptance_criteria", receipt_tile_acceptance_criteria(...)),
       ("source_binding", receipt_tile_source_binding(...)),
       ("shader_module_compile_policy", receipt_tile_shader_module_compile_policy()),
       ...
     ])
```

## Added Builders

```txt
receipt_atlas_root
receipt_tile_acceptance_criteria
receipt_tile_source_binding
receipt_tile_shader_module_compile_policy
receipt_tile_shader_module_compile_summary
receipt_tile_guards
receipt_tile_no_weight_load_guard
receipt_tile_no_pipeline_no_dispatch_guard
receipt_tile_no_backward_no_optimizer_guard
receipt_tile_next_stage
receipt_digest_tile_wgsl_contract
receipt_digest_tile_shader_candidate
receipt_digest_tile_combined
```

## Boundaries Preserved

- No source safetensors file read
- No row-block re-read
- No F32 decode
- No GPU buffer creation
- No queue upload
- No readback
- No compute pipeline creation
- No bind group creation
- No dispatch
- No forward/backward/optimizer/mutation

## Container Validation

Static checks only. Cargo/rustc unavailable in this environment.
