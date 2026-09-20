# EVE-MCU-ACTIVE-ASYNC-PHYS-R1-COMPILEFIX1

## Result-typed campaign environment seal closure

```text
+ EXISTING ENV VALUE ARM RETURNS Result<()>
+ PROFILE CONFLICT FAIL-CLOSED PRESERVED
+ NOT-PRESENT ENV INSTALL PRESERVED
+ ENV READ FAILURE PRESERVED
+ NO CAMPAIGN SEMANTIC CHANGE
```

## Parent

```text
ASH_PASS3_EVE_MCU_ACTIVE_ASYNC_PHYS_R1_CODE_ONLY.zip
SHA-256 c44bd88fcce1667cda2da04c8faf1e26adb3c2ca1ba1def1ba62799debbe8543
```

## Compile failure

`seal_active_async_campaign_env(...) -> Result<()>` used an `ensure!` expression directly as the `Ok(value)` match arm. On success `ensure!` evaluates to `()`, so the arm failed to type-check against `Result<()>` with E0317.

## Closure

```rust
Ok(value) => {
    ensure!(
        value.trim().eq_ignore_ascii_case(expected),
        "E_ACTIVE_ASYNC_PHYS_R1_PROFILE_ENV_CONFLICT:{}:observed={}:expected={}",
        name,
        value,
        expected,
    );
    Ok(())
}
```

The failure path still returns early through `ensure!`; the success path now explicitly returns `Ok(())`.

## Changed files

```text
MOD crates/base_train/src/bin/base_train.rs
ADD tools/validate_ash_eve_mcu_active_async_phys_r1_compilefix1_static.py
```

Delta: MOD 1 / ADD 1 / DEL 0.

## Source SHA-256

```text
0f435ca033cccc122ae106694793af396afe491299594b6d740acba91b938e51  crates/base_train/src/bin/base_train.rs
966ede289d33130655688eede451295164d1558bd152e9e2733d857f85a74b19  tools/validate_ash_eve_mcu_active_async_phys_r1_compilefix1_static.py
```

## Static qualification

```text
PASS_EVE_MCU_ACTIVE_ASYNC_PHYS_R1_COMPILEFIX1_STATIC checks=6
PASS_EVE_MCU_ACTIVE_ASYNC_PHYS_R1_STATIC checks=37
PASS_TENSORCUBE_CONSUME_R2_GPU_PARALLEL_PLANE_STATIC checks=61
PASS_BP_DK_CHECKPOINT_R1_GPU_HOT_CAPTURE_STATIC checks=46
PASS_TENSORCUBE_CONSUME_R1_RELATION_AUTHORITY_STATIC checks=56
PASS_EVE_MCU_R3H_CF11_R1_CF1_CF1_CF1_CF1_CF1_CF1_RAM36_CURRENT_SOURCE_PROMOTION_STATIC checks=32
PASS_EVE_MCU_R3H_CF11_R1_BOUNDED_COW_WORKSPACE_STATIC checks=22
PASS_EVE_MCU_R3H_CF11_R1_CF1_CF1_CF1_CF1_CF1_BPDK_GENERATION_BINDING_STATIC checks=27
PASS_EVE_MCU_R3H_CF11_R1_CF1_CF1_CF1_R8A_PREDURABILITY_SEAL_STATIC checks=30
PASS_EVE_MCU_R3H_CF11_R1_CF1_CF1_MUON_PACKED_ADDRESS_STATIC checks=26
PASS_EVE_MCU_R3H_CF11_R1_CF1_PACKED_MV_DIGEST_STATIC checks=27
```

Rust compile is not claimed in the bake environment.

## Artifacts

```text
Overlay
ASH_EVE_MCU_ACTIVE_ASYNC_PHYS_R1_COMPILEFIX1_OVERLAY_CODE_ONLY.zip
SHA-256 5e254179042389e93635fb234ba3ad4c3825204a4cb26c358dab3ea52894eb91
FILES 2
CRC PASS

Full
ASH_PASS3_EVE_MCU_ACTIVE_ASYNC_PHYS_R1_COMPILEFIX1_CODE_ONLY.zip
SHA-256 01d50dfab006dfc42fe65eca02c443c07bb6cae34a01ed645cec824ad9a74153
FILES 8448
CRC PASS
```

Both exclude specs/, artifacts/, manifests/, Markdown, __pycache__, and *.pyc.

## Final law

> This compilefix changes only the successful return type of the ActiveAsync campaign environment seal helper. Conflict detection, environment installation, ActiveAsync profile identity, TensorCube R2 reachability, B06 semantics, and BP-DK hot checkpoint semantics remain unchanged.
