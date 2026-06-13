# ASH-FT-03-MERGED Acceptance

## PASS conditions

```txt
1. ASH-FT-03 base files are present.
2. ASH-FT-03-R1 export surface repair files are present.
3. crates/model_core/Cargo.toml contains bin target ash_ft03_cpu_tensor_sanity_baseline.
4. crates/model_core/src/lib.rs publicly exposes ash_ft03_cpu_tensor_sanity_baseline module.
5. crates/model_core/src/lib.rs re-exports AshFt03Bundle and AshFt03Config.
6. crates/model_core/src/lib.rs re-exports ash_ft03_config_from_args.
7. crates/model_core/src/lib.rs re-exports ash_ft03_failure_summary_json.
8. crates/model_core/src/lib.rs re-exports run_ash_ft03_cpu_tensor_sanity_baseline.
9. crates/model_core/src/lib.rs re-exports write_ash_ft03_artifacts.
10. Root SSOT_ASH_FT_03_MERGED.md exists.
11. Runtime artifacts artifacts/ash_ft/*.json are not packaged.
12. target/ build outputs are not packaged.
```

Expected runtime PASS after local execution:

```txt
PASS_ASH_FT03_CPU_TENSOR_SANITY_BASELINE_NO_TRAIN
```

## FAIL conditions

```txt
1. Missing FT-03 bin target.
2. Missing FT-03 root export surface.
3. R1 overlay is not applied.
4. Runtime artifacts from artifacts/ash_ft are packaged.
5. target/ build outputs are packaged.
6. Any change enables candidate data read, tensor slice replay, GPU upload, forward, backward, optimizer, candidate write, runtime default apply, or train.
```
