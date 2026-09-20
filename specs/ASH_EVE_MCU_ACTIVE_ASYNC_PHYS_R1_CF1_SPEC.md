# EVE-MCU-ACTIVE-ASYNC-PHYS-R1-CF1

## R6 ACTIVE QUALIFICATION + P4 EXACT-LEASE BINDING CLOSURE

```text
+ R6 QUEUE_WITHIN_WAVE ACTIVE ADMISSION
+ EXISTING IMMUTABLE QUALIFICATION BUNDLE REUSE
+ R6 PHYSICAL QUALIFICATION RECEIPT EXACT BINDING
+ CURRENT BINARY / CURRENT DEVICE BUNDLE LINEAGE PRESERVATION
+ P4 ACTIVE EXACT LEASE -> R6 ACTIVE-QUALIFIED REQUIREMENT
+ NO SYNTHETIC QUALIFICATION RECEIPT
+ NO SHADOW-QUEUE PROMOTION SPOOF
+ NO QUALIFICATION GATE WEAKENING
+ ACTIVE-ASYNC CAMPAIGN STARTUP SEAL
+ P5 ACTIVE-ASYNC REACHABILITY
+ TENSORCUBE-CONSUME-R2 REACHABILITY
+ REAL B06 SUCCESSOR TARGET PRESERVATION
+ BP-DK CHECKPOINT R1 PRESERVATION
+ RAM36 / CF11 / R8A / PACKED-MV PRESERVATION
```

## Parent

```text
ASH_PASS3_EVE_MCU_ACTIVE_ASYNC_PHYS_R1_COMPILEFIX2_CODE_ONLY.zip
SHA-256 f7b71c52d8b24a339c874b4737fa2100b9b20ea85222aea26a03202b3373af5c
```

Parent physical first failure:

```text
E_MCU_ATLAS_LEASE_R1_R6_ACTIVE_QUALIFICATION_REQUIRED
```

The parent had already physically admitted D10 ActiveAsyncPhysicalCanary and C08 ActiveAsync.

## Closure

The production runtime already called the existing immutable qualification-bundle binder before R6 construction, but the ActiveAsync physical CLI did not seal a qualification root or R6 active mode. With no qualification root the binder correctly returned no binding, so P4 rejected R6 as unqualified.

CF1 adds a required ActiveAsync CLI argument:

```text
--mcu-qualification-root <immutable qualification root>
```

The CLI canonicalizes that root, seals:

```text
ASH_UNIFIED_ATLAS_MCU_GLOBAL_TENSORCUBE_JOB_QUEUE_R6=1
ASH_UNIFIED_ATLAS_MCU_GLOBAL_TENSORCUBE_JOB_QUEUE_R6_MODE=QUEUE_WITHIN_WAVE
ASH_UNIFIED_ATLAS_MCU_QUALIFICATION_ROOT_R1=<canonical root>
```

and calls the existing:

```text
bind_current_mcu_qualification_bundle_environment_r1_from_environment()
```

No new receipt generator is added.

The binder remains responsible for exact current-binary, current-device, current-pointer, content-addressed bundle and publication-seal validation, and binds the bundle-owned R6 receipt to:

```text
ASH_UNIFIED_ATLAS_MCU_GLOBAL_TENSORCUBE_JOB_QUEUE_R6_QUALIFICATION_RECEIPT
```

## Current-binary lineage

A bundle created for an older `base_train.exe` is deliberately rejected.

Physical procedure therefore requires:

```text
build current base_train
-> fresh Native CF1
-> materialize current-binary qualification evidence truth R2
-> publish/adopt that immutable bundle
-> run ActiveAsync canary with that qualification root
```

No stale-binary qualification reuse.

## R6/P4 gates preserved

`McuGlobalTensorCubeJobQueueR6::new()` still loads and validates the existing R6 qualification receipt.

Its structural gates remain unchanged:

```text
schema exact
patch ID exact
descriptor ABI exact
shadow membership parity pass
active output bit parity pass
stale-generation fixture pass
mutable-alias fixture pass
fixture_count > 0
divergence_count == 0
receipt digest exact
```

`qualified_for_active_execution()` remains:

```text
mode.active() && qualification.is_some()
```

and P4 still enforces:

```text
E_MCU_ATLAS_LEASE_R1_R6_ACTIVE_QUALIFICATION_REQUIRED
```

CF1 closes the missing binding rather than weakening either gate.

## Startup receipts

CLI:

```text
[ASH-EVE-MCU-ACTIVE-ASYNC-PHYS-R1-CF1][qualification-bind]
```

Runtime:

```text
[ASH-EVE-MCU-ACTIVE-ASYNC-PHYS-R1-CF1][r6-qualification]
```

The runtime receipt binds the immutable bundle digest, pointer generation, exact R6 receipt path, R6 qualification digest, R6 mode, active-qualified state, P4 Exact Lease and P5 ActiveAsync.

## Changed files

```text
MOD crates/base_train/src/bin/base_train.rs
MOD crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
MOD crates/base_train/src/unified_atlas_mcu_global_tensorcube_job_queue_r6.rs
ADD tools/validate_ash_eve_mcu_active_async_phys_r1_cf1_r6_qualification_static.py
```

Delta:

```text
MOD 3
ADD 1
DEL 0
```

## Source SHA-256

```text
824c0a4a7f604d14567a182fbff4cd7c321fc3cca1d821d7ecefb76b2489f49b  crates/base_train/src/bin/base_train.rs
81643c98fdc0d6ad3179728b6a53771ef2f9eda5c4503831e8c4f07da5d59dc4  crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
734d39856e93f7658cfb04fc2dc4121ccb93eafd71462d7ff1f4f399fe32df7a  crates/base_train/src/unified_atlas_mcu_global_tensorcube_job_queue_r6.rs
88ef6525d5454ed52582e20db670e774951f2a5a40e8187a7ee2b074a6b2e475  tools/validate_ash_eve_mcu_active_async_phys_r1_cf1_r6_qualification_static.py
```

## Static qualification

```text
PASS_EVE_MCU_ACTIVE_ASYNC_PHYS_R1_CF1_R6_QUALIFICATION_STATIC checks=16
PASS_EVE_MCU_ACTIVE_ASYNC_PHYS_R1_COMPILEFIX2_STATIC checks=7
PASS_EVE_MCU_ACTIVE_ASYNC_PHYS_R1_STATIC checks=37
PASS_TENSORCUBE_CONSUME_R2_GPU_PARALLEL_PLANE_STATIC checks=61
PASS_BP_DK_CHECKPOINT_R1_GPU_HOT_CAPTURE_STATIC checks=46
PASS_TENSORCUBE_CONSUME_R1_RELATION_AUTHORITY_STATIC checks=56
PASS RAM36 current-source checks=32
PASS CF11-R1 checks=22
PASS BP-DK generation binding checks=27
PASS R8A checks=30
PASS packed address checks=26
PASS packed M/V checks=27
PYTHON_VALIDATOR_COMPILE_PASS
DELIMITER_COUNT_PASS
```

Bake environment:

```text
RUST_TOOLCHAIN=UNAVAILABLE
COMPILE=NOT_RUN
RUNTIME=NOT_RUN
PHYSICAL=NOT_RUN
PERFORMANCE=UNMEASURED
```

## Artifacts

Overlay:

```text
ASH_EVE_MCU_ACTIVE_ASYNC_PHYS_R1_CF1_OVERLAY_CODE_ONLY.zip
SHA-256 c0da5ee8d9518865289ce36f80bc620d4459ff60b463a8932af8fd4e39b35614
FILES 4
CRC PASS
```

Full:

```text
ASH_PASS3_EVE_MCU_ACTIVE_ASYNC_PHYS_R1_CF1_CODE_ONLY.zip
SHA-256 13b6e9a10c3979f27f547e7c35e21ce367cb6128d124c22254c55d0a5124d0f5
FILES 8450
CRC PASS
```

Both exclude specs/, artifacts/, manifests/, Markdown, __pycache__, and *.pyc.

## Physical acceptance

Startup target:

```text
[ASH-EVE-MCU-ACTIVE-ASYNC-PHYS-R1-CF1][qualification-bind] ... admitted=true
[ASH-D10-ACTIVE-ASYNC-PHYS-R1][admission] ... admitted=true
[ASH-EVE-MCU-ACTIVE-ASYNC-PHYS-R1-CF1][r6-qualification]
    r6_enabled=true
    r6_mode=QUEUE_WITHIN_WAVE
    r6_active_qualified=true
    p4_exact_lease=true
    p5_active_async=true
    admitted=true
```

Required disappearance:

```text
E_MCU_ATLAS_LEASE_R1_R6_ACTIVE_QUALIFICATION_REQUIRED
```

The intended next execution stage is TensorCube Consume R2. Existing B06 completeness and submission-lineage gates remain strict.

## Final law

> ActiveAsync physical execution binds an existing immutable qualification bundle for the exact current binary and current device before R6 construction.

> R6 must be QUEUE_WITHIN_WAVE and must load the exact bundle-owned physical qualification receipt before P4 Exact Lease may execute.

> A source change that changes base_train.exe also changes qualification lineage; the current immutable bundle must therefore be materialized and published for that exact executable before physical admission.
