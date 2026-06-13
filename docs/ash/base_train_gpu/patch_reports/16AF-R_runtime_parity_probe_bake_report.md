# 16AF-R Runtime Parity Probe Bake Report

## Confirmed

```txt
base = ash_pass3_commit16AF_native_atlas_ffn_bake.zip
user_reported_build_gate = PASS
runtime_gate = layer0 native atlas FFN parity probe
scope = runner + acceptance artifact generation
```

## Files Added

```txt
crates/model_core/src/bin/af16r_runtime_parity.rs
scripts/run_16AF_R_runtime_parity.sh
scripts/run_16AF_R_runtime_parity.ps1
infer_debug/16AF-R_forbidden_path_scan.md
patch_reports/16AF-R_runtime_parity_probe_bake_report.md
```

## Runtime Runner Contract

```txt
Input:
- --spec <model_spec.toml>
- --checkpoint <full_model.safetensors> repeated or --checkpoints separated by semicolon
- --layer 0
- --threshold <float>

Output:
- acceptance_reports/16AF-R_runtime_parity.json
- acceptance_reports/16AF-R_runtime_parity.md
```

## Expected Logs

```txt
[16AF-R][start] build_gate=pass layer=0 threshold=0.001
[16AF-R][ssot] generation_connected=false runtime_gate=parity_only
[16AF-R][ffn] enable_native_atlas_ffn=true enable_silu_swiglu=true
[16AF-R][ffn] burn_cubecl_ffn_matmul_disabled=true
[16AF-R][layout] layer=0 hidden=... intermediate=...
[16AF-R][ffn-parity] layer=0 shape_match=... max_abs_delta=... mean_abs_delta=... nan_count=... inf_count=... top_index_match=... top_k_overlap=... parity_pass=...
[16AF-R][seal] PASS runtime parity closed
```

## Generation Gate

```txt
generation_connected = false
```

16AF-R does not wire the native FFN path into generation. Integration remains locked until the runtime parity report closes with parity_pass=true.

## Container Limitation

```txt
cargo = unavailable in this container
rustc = unavailable in this container
runtime_wgpu_probe = not executed here
```

Runtime parity must be executed in the user's local Rust/WGPU environment using the included runner.
