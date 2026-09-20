# EVE-MCU-ACTIVE-ASYNC-PHYS-R1-COMPILEFIX2

## D10 runtime-mode digest ordering closure

```text
+ PRE-D10 CLI CHECK = MODE TUPLE ONLY
+ D10 ASSIGNS ACTIVE-ASYNC CANARY DIGEST
+ POST-ASSIGN validate_active_candidate PRESERVED
+ RUNTIME-MODE-DIGEST GATE PRESERVED
+ NO PROFILE SPOOF
+ NO B06 / R2 / BP-DK SEMANTIC CHANGE
```

## Parent

```text
ASH_PASS3_EVE_MCU_ACTIVE_ASYNC_PHYS_R1_COMPILEFIX1_CODE_ONLY.zip
SHA-256 01d50dfab006dfc42fe65eca02c443c07bb6cae34a01ed645cec824ad9a74153
```

## Failure

The ActiveAsync CLI called `ProductionRuntimeProfile::validate_active_candidate()` before D10 unpublished-profile classification had assigned `benchmarked_runtime_mode_digest`.

`ProductionRuntimeProfile::from_environment()` correctly leaves that digest empty. Therefore the early validation failed at:

```text
FAIL_D10_RUNTIME_PROFILE_MISMATCH:runtime-mode-digest
```

before the D10 branch could assign:

```text
D10_ACTIVE_ASYNC_PHYSICAL_CANARY_R1
```

## Closure

A digest-independent mode tuple predicate is now explicit:

```rust
ProductionRuntimeProfile::exact_active_async_mode_tuple()
```

`exact_d09_physical_candidate()` delegates to the same tuple predicate, but D09 and ActiveAsync physical authority classes remain distinct.

The CLI precheck now performs only the exact B04/B05/B06/C07/C08 active-mode tuple check. It no longer calls `validate_active_candidate()` before D10 admission.

The D10 `ActiveAsyncPhysicalCanary` branch remains authoritative for:

```text
benchmarked_runtime_mode_digest = D10_ACTIVE_ASYNC_PHYSICAL_CANARY_R1
seal()
validate_active_candidate()
```

Thus the runtime-mode-digest gate is preserved and executed at the correct lifecycle point.

## Changed files

```text
MOD crates/base_train/src/bin/base_train.rs
MOD crates/base_train/src/d10_production_ssot_publication.rs
ADD tools/validate_ash_eve_mcu_active_async_phys_r1_compilefix2_static.py
```

Delta: MOD 2 / ADD 1 / DEL 0.

## Source SHA-256

```text
05d3b5c5ef80e1a8d91d775ed937d1cfbe0dafdae5ee9367f83c74176cea2ff0  crates/base_train/src/bin/base_train.rs
bcd60feab7e13c0bac3578cd4c00cad91a76e7de4daaf3ef10774f1da073657a  crates/base_train/src/d10_production_ssot_publication.rs
95a1fd07f87531dc4fe0e0b9aac6de243a272308fde80a70ec7ffa97d28b795b  tools/validate_ash_eve_mcu_active_async_phys_r1_compilefix2_static.py
```

## Static qualification

```text
PASS_EVE_MCU_ACTIVE_ASYNC_PHYS_R1_COMPILEFIX2_STATIC checks=7
PASS_EVE_MCU_ACTIVE_ASYNC_PHYS_R1_STATIC checks=37
PASS_TENSORCUBE_CONSUME_R2_GPU_PARALLEL_PLANE_STATIC checks=61
PASS_BP_DK_CHECKPOINT_R1_GPU_HOT_CAPTURE_STATIC checks=46
PASS_TENSORCUBE_CONSUME_R1_RELATION_AUTHORITY_STATIC checks=56
PASS RAM36 current-source checks=32
PASS CF11-R1 checks=22
PASS BP-DK pending snapshot checks=37
PASS BP-DK generation binding checks=27
PASS R8A checks=30
PASS packed address checks=26
PASS packed M/V checks=27
```

Rust compile is not claimed in the bake environment.

## Artifacts

```text
Overlay
ASH_EVE_MCU_ACTIVE_ASYNC_PHYS_R1_COMPILEFIX2_OVERLAY_CODE_ONLY.zip
SHA-256 709e01f85ea8a51772cc19b24c5453c29f76d59bd1b2ba4cf904f120e52824c4
FILES 3
CRC PASS

Full
ASH_PASS3_EVE_MCU_ACTIVE_ASYNC_PHYS_R1_COMPILEFIX2_CODE_ONLY.zip
SHA-256 f7b71c52d8b24a339c874b4737fa2100b9b20ea85222aea26a03202b3373af5c
FILES 8449
CRC PASS
```

## Final law

> The ActiveAsync CLI may verify the requested active mode tuple before D10 classification, but it must not validate a D10 runtime-mode digest before D10 has assigned the distinct ActiveAsync physical-canary digest.

> D10 remains the sole authority that assigns, seals, and validates `D10_ACTIVE_ASYNC_PHYSICAL_CANARY_R1`.
