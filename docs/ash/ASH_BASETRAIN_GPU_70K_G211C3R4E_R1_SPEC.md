# ASH-BASETRAIN-GPU-70K-G211C3R4E-R1

## R4C Amortization Class Accept Pair Hotfix / Verdict Class Split Repair / No Attribution Logic Mutation

Seal: Entry Validation Hotfix Only / No Attribution Logic Mutation / No Runtime Splice / No Promotion Reopen.

## SSOT

`70K-G211C3R4E-R1` repairs only the R4E entry validation for the R4C verdict/class pair.

The valid current R4C pair is:

```text
batch_timing_verdict = SMALL_SHAPE_KERNEL_OR_TILE_LOSS_REMAINS
small_shape_amortization_class = KERNEL_OR_TILE_LOSS_REMAINS
```

`70K-G211C3R4E-R1` must accept that pair and must not treat the verdict string as the amortization class string.

`70K-G211C3R4E-R1` must not mutate attribution logic, tile utilization logic, padding pressure logic, controlled shape pair geometry, artifact schema, runtime route, `tensorcube_runtime_splice`, production WGSL, production tile/workgroup layout, model weights, checkpoints, optimizer/training state, promotion state, or G211C4 entry state.

## Predecessor

```text
ASH-BASETRAIN-GPU-70K-G211C3R4E
Kernel Tile Padding Attribution /
Odd Shape And Tile Utilization Probe /
No Runtime Splice No Promotion Reopen
```

Observed failure:

```text
ERR_70K_G211C3R4E_R4C_AMORTIZATION_CLASS_MISMATCH
```

The failure is an entry validation mismatch, not an attribution result.

## Scope

Included:

```text
1. Split R4C verdict and class validation.
2. Accept SMALL_SHAPE_KERNEL_OR_TILE_LOSS_REMAINS with KERNEL_OR_TILE_LOSS_REMAINS.
3. Read small_shape_amortization_class from the R4C main receipt root or summary field.
4. Add R1 accept-pair hotfix receipt.
5. Keep the main R4E PASS marker and output schema stable.
```

Excluded:

```text
1. Attribution metric changes.
2. Tile utilization metric changes.
3. Padding pressure metric changes.
4. Controlled shape pair changes.
5. Verdict selection logic changes.
6. Timing loop changes.
7. GPU dispatch implementation changes.
8. Runtime splice or promotion reopen.
9. G211C4 entry generation.
```

## Validation Repair Contract

Required validation shape:

```rust
match (
    r4c_batch_timing_verdict.as_str(),
    r4c_small_shape_amortization_class.as_str(),
) {
    (
        "SMALL_SHAPE_KERNEL_OR_TILE_LOSS_REMAINS",
        "KERNEL_OR_TILE_LOSS_REMAINS",
    ) => {
        // accept current R4C path
    }
    _ => {
        bail!("ERR_70K_G211C3R4E_R4C_AMORTIZATION_CLASS_MISMATCH");
    }
}
```

The implementation may read `small_shape_amortization_class` from either:

```text
small_shape_amortization_class
summary.small_shape_amortization_class
```

because the current R4C main receipt stores the class inside `summary`.

## Local Rust Binary

The binary name remains unchanged.

```text
crates/base_train/src/bin/ash_basetrain_gpu_70k_g211c3r4e_kernel_tile_padding_attribution.rs
```

Suggested command from ASH root:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g211c3r4e_kernel_tile_padding_attribution
```

Explicit args:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g211c3r4e_kernel_tile_padding_attribution -- --g211c3-dir artifacts/g211c3 --g211c3r4b-dir artifacts/g211c3r4b --g211c3r4c-dir artifacts/g211c3r4c --g211c3r4d-dir artifacts/g211c3r4d --g211c3r4d-r2-dir artifacts/g211c3r4d_r2 --out-dir artifacts/g211c3r4e --probe-shapes B0,B1,B5 --diagnostic-pairs B5_PAD8,B5_NEAR_EVEN
```

Expected R1 hotfix stdout fields:

```text
PASS_ASH_BASETRAIN_GPU_70K_G211C3R4E_R1_ACCEPT_PAIR_HOTFIX
r4e_r1_accept_pair_hotfix=true
r4c_batch_timing_verdict=SMALL_SHAPE_KERNEL_OR_TILE_LOSS_REMAINS
r4c_small_shape_amortization_class=KERNEL_OR_TILE_LOSS_REMAINS
verdict_class_split_repaired=true
attribution_logic_mutated=false
```

Expected final R4E PASS marker remains:

```text
PASS_ASH_BASETRAIN_GPU_70K_G211C3R4E_KERNEL_TILE_PADDING_ATTRIBUTION
```

## Required Output Addendum

R4E-R1 may add this hotfix receipt:

```text
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_R1_ACCEPT_PAIR_HOTFIX.json
```

Required fields:

```json
{
  "patch_id": "ASH-BASETRAIN-GPU-70K-G211C3R4E-R1",
  "hotfix_name": "R4C Amortization Class Accept Pair Hotfix",
  "status": "PASS_ASH_BASETRAIN_GPU_70K_G211C3R4E_R1_ACCEPT_PAIR_HOTFIX",
  "target_patch_id": "ASH-BASETRAIN-GPU-70K-G211C3R4E",
  "failed_error_before_hotfix": "ERR_70K_G211C3R4E_R4C_AMORTIZATION_CLASS_MISMATCH",
  "r4c_batch_timing_verdict": "SMALL_SHAPE_KERNEL_OR_TILE_LOSS_REMAINS",
  "r4c_small_shape_amortization_class": "KERNEL_OR_TILE_LOSS_REMAINS",
  "accept_pair_verified": true,
  "verdict_class_split_repaired": true,
  "attribution_logic_mutated": false,
  "tile_metric_logic_mutated": false,
  "padding_metric_logic_mutated": false,
  "artifact_schema_mutated": false,
  "runtime_splice_allowed": false,
  "promotion_allowed": false,
  "g211c4_entry_generated": false
}
```

Forbidden output:

```text
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_NEXT_ENTRY_PACKET_G211C4.json
```

## PASS Criteria

```text
PASS-01 R4C batch_timing_verdict found.
PASS-02 R4C small_shape_amortization_class found at root or summary path.
PASS-03 R4C accept pair matched exactly.
PASS-04 R4E entry validation no longer rejects the valid R4C pair.
PASS-05 R1 hotfix receipt written.
PASS-06 attribution_logic_mutated=false.
PASS-07 tile_metric_logic_mutated=false.
PASS-08 padding_metric_logic_mutated=false.
PASS-09 artifact_schema_mutated=false.
PASS-10 runtime_splice_allowed=false.
PASS-11 promotion_allowed=false.
PASS-12 G211C4 entry packet not generated.
PASS-13 main R4E attribution execution continues after entry validation.
PASS-14 main R4E PASS marker remains unchanged.
```

## PASS Meaning

PASS means R4E-R1 repaired the R4C verdict/class accept pair validation so that the valid R4C SSOT pair is accepted by R4E.

PASS does not mean R4E attribution succeeded unless the main R4E PASS marker is printed. PASS does not mean TensorCube is faster. PASS does not mean tile/padding attribution is correct by itself. PASS does not mean promotion is reopened. PASS does not mean G211C4 is allowed.

## Recommended Commit Message

```text
ASH-BASETRAIN-GPU-70K-G211C3R4E-R1 accept R4C verdict class pair

- Repair R4E entry validation for R4C verdict/class split
- Accept SMALL_SHAPE_KERNEL_OR_TILE_LOSS_REMAINS with KERNEL_OR_TILE_LOSS_REMAINS
- Read amortization class from R4C root or summary path
- Preserve attribution, tile utilization, padding, and diagnostic pair logic
- Add R1 accept-pair hotfix receipt
- Preserve R4E main PASS marker
- Preserve no runtime splice, no G211C4 entry, no production route, no promotion
```
