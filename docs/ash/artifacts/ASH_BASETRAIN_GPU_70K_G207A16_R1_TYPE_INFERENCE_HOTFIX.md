# ASH-BASETRAIN-GPU-70K-G207A16-R1 Type Inference Hotfix

PatchId: `ASH-BASETRAIN-GPU-70K-G207A16`  
HotfixId: `ASH-BASETRAIN-GPU-70K-G207A16-R1`  
SourcePackage: `ash_pass3_ASH-BASETRAIN-GPU-70K-G207A16_production_pointer_stability_soak_baked_no_artifacts_no_ps1_no_py.zip`  
TargetRuntimeBinary: `ash_basetrain_gpu_70k_g207a16_production_pointer_stability_soak`

## Purpose

R1 fixes Rust `E0283` / `E0282` type inference failure in `validate_args`.

The original writer used this pattern for numeric guard checks:

```rust
match args.soak_min_pass_count == args.soak_run_count {
    true => Ok(()),
    false => bail!("soak_min_pass_count must equal soak_run_count"),
}?;
```

In that local expression, Rust could not infer the error type parameter for `Ok(())` before `?` conversion into `anyhow::Result<()>`.

## Fix

The ambiguous `match -> Ok(()) / bail!()` guard was replaced with `anyhow::ensure!`:

```rust
ensure!(args.soak_run_count >= 3, "soak_run_count must be >= 3");
ensure!(
    args.soak_min_pass_count == args.soak_run_count,
    "soak_min_pass_count must equal soak_run_count"
);
```

The import was updated from:

```rust
use anyhow::{bail, Result};
```

to:

```rust
use anyhow::{bail, ensure, Result};
```

## Scope

- No runtime artifact was prebaked.
- No CLI contract was changed.
- No PASS target was changed.
- No production pointer behavior was changed.
- No quality claim was added.
- No checkpoint/safetensors/base weight mutation was added.

## Static Surface

```text
target_writer_json_macro_count=0
target_writer_recursion_limit_count=0
target_writer_ensure_macro_count=2
ambiguous_local_result_guard_count=0
```
