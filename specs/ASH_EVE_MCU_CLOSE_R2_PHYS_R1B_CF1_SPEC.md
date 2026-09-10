# ASH-EVE-MCU-CLOSE-R2-PHYS-R1B-CF1

## BASE CONFIG SELF-MATERIALIZATION + R1A DATASET IDENTITY REBIND

### Revision

```text
Patch ID: ASH-EVE-MCU-CLOSE-R2-PHYS-R1B-CF1
Direct code parent: ASH_PASS3_EVE_MCU_CLOSE_R2_PHYS_R1B_MOVE_OWNERSHIP_FIX_CODE_ONLY.zip
Parent SHA-256: d333d432c2fc2eb1d5c2ee92adfc7503bae4c907285cb6eebe380636ce2b56df
Required parent physical token: PASS_EVE_MCU_CLOSE_R2_PHYS_R1A_FRESH_SOURCE_GENESIS
Algorithm / Adam / Muon / R13 math change: NO
Historical resume relaxation: NO
```

### 1. External BaseTrainConfig retirement

`--base-config-path` is removed. R1B-CF1 uses the same root authority as normal production:

```text
ModelSpec + TokenizerManifest + DatasetManifest
    -> build_config_from_specs(...)
    -> FreshGenesis rebinding
    -> sealed generated BaseTrainConfig
```

The generated JSON is an output receipt, not an operator prerequisite.

### 2. R1A dataset-builder identity rebind

R1A physically sealed the cursor builder digest but did not persist the raw geometry tuple. The admitted R1A source was created with `max_seq_len=512`, `micro_batch_size=2`, and BOS/EOS/task/lang/glossary/TM flags all true. R1B-CF1 recomputes the canonical dataset-builder identity from that exact tuple plus `tokenizer_v5` and requires exact equality with the R1A cursor. Any mismatch rejects with `E_R1B_CF1_DATASET_BUILDER_IDENTITY_MISMATCH`.

This tuple is evidence for the current physical R1A source, not a generic production default. A later genesis revision should persist raw builder geometry directly.

### 3. Fresh tokenizer lineage correction

R1A cursor lineage is `tokenizer_v5` (`tokenizer_spec_id`) while the tokenizer manifest `manifest_id` is `tok_v5_48259_candidate`. The previous production pipeline passed `manifest_id` unconditionally and would reject the fresh cursor.

R1B-CF1 selects:

```text
FreshGenesisR1A -> tokenizer_spec_id
Historical paths -> manifest_id
```

Historical resume semantics remain unchanged.

### 4. Self-materialized production admission

Starting from `build_config_from_specs`, R1B-CF1 explicitly binds the physically admitted R1A dataset geometry, `gradient_accumulation=8`, eight optimizer steps, FreshGenesis N8 source role, no historical N2/N8 parent authority, checkpoint storage publication, RAM-resident Adam, exact RAM inventory/RAM36 authority, persistent weight pack, EVE R3/R3A/R3B/R3C/R3C1, R4 active owner/cross-invocation runtime, R4A sealed profile, EVE-MCU-CLOSE-R1/R2, MCU R7/R7A/R7B, packed-gradient multi-consumer lease/arena reuse, HiMuon R8 ownership, TensorCube local Muon new-lineage, packed R6A runtime, native wave residency, device-limit paging, canonical packed-genesis identity and subgroup32 tiled segment-gradient AdamW.

The correctness campaign keeps N8 deferred durable writeback disabled so Leg C can use `DurableCheckpointKeepResident` without weakening the historical deferred-writeback contract.

Before config publication, existing validators are authority:

```text
validate_eve_mcu_close_r1_config(...)
validate_eve_mcu_close_r2_config(...)
build_trainable_session_admission_seal_r4a(...)
```

### 5. Fresh Muon materialization

The existing first-candidate registry generator remains routing authority. R1B-CF1 materializes:

```text
genesis/current/EVE_MCU_CLOSE_R2_PHYS_R1B_CF1_MUON_REGISTRY.json
genesis/current/EVE_MCU_CLOSE_R2_PHYS_R1B_CF1_MUON_PROFILE.json
```

The profile uses the existing production-compatible local-Muon contract: LR 0.001, beta 0.9, weight decay 0.01, Nesterov, five Newton-Schulz steps, F32 working/momentum authority, and `ZERO_NEW_OPTIMIZER_LINEAGE`. `ProductionMuonRuntime` remains momentum payload authority.

### 6. Fresh scheduler materialization

R1B-CF1 adds the fresh scheduler materializer inside the existing R6 scheduler module so the existing private scheduler digest and optimizer-profile authority remain SSOT.

```text
profile_id = ash_basetrain_n8_fresh_genesis_r1b_cf1
kind = LINEAR_WARMUP_CONSTANT
warmup steps = 4
total steps = 8
base/minimum/warmup-start LR = generated BaseTrainConfig optimizer LR
```

No historical scheduler extension receipt is fabricated.

### 7. Native CF1

The self-materializer loads the supplied `NativeCF1ReleaseCompileAuthority`, hashes `std::env::current_exe()`, requires exact binary identity, and requires release profile before preflight PASS.

### 8. Authority/runtime root split

```text
<campaign-output-root>/
  genesis/current/     # generated config/profile authority
  durable_storage/     # storage authority
  physical_abc/        # existing physical A/B/C runner output
```

This preserves the parent campaign's `output_root must not exist` contract while permitting preflight materialization first.

### 9. Preflight

`--preflight-only` executes zero optimizer steps and materializes:

```text
EVE_MCU_CLOSE_R2_PHYS_R1B_CF1_BASE_CONFIG.json
EVE_MCU_CLOSE_R2_PHYS_R1B_CF1_ADMISSION_PROFILE.json
EVE_MCU_CLOSE_R2_PHYS_R1B_CF1_MUON_REGISTRY.json
EVE_MCU_CLOSE_R2_PHYS_R1B_CF1_MUON_PROFILE.json
EVE_MCU_CLOSE_R2_PHYS_R1B_CF1_SCHEDULER_PROFILE.json
EVE_MCU_CLOSE_R2_PHYS_R1B_CF1_PREFLIGHT.json
```

Expected token:

```text
PASS_EVE_MCU_CLOSE_R2_PHYS_R1B_CF1_CONFIG_SELF_MATERIALIZATION
```

### 10. Full A/B/C

The full command reuses `eve_mcu_close_physical_campaign_r1` under `physical_abc/`. R1B still validates every leg's N8 and R2 receipts. Final promotion remains:

```text
PASS_EVE_MCU_CLOSE_R2_PHYS_R1B_FULL_PRODUCTION_ABC
PASS_EVE_MCU_CLOSE_R2_FULL_PRODUCTION_SESSION_RESIDENCY_PHYSICAL
```

### 11. Source delta

```text
ADD 0
MOD 4
DEL 0
source-delta digest:
bf55cc5791f672fd0913c83a2f1cdcc130da1d43096469f777cafcef895c2530
```

Modified files:

```text
crates/base_train/src/bin/base_train.rs
  dc9925464718fa0715d8709ba8e306916cfc220f3615b3e853349353e09c5a2e
crates/base_train/src/eve_mcu_close_r2_physical_campaign_r1b.rs
  948b13fff13e11d158f4685dd8d89dc5b6122f7b98d2afdb3ca520f581ce5d47
crates/base_train/src/pipeline.rs
  13a2f3d0585b7f397ae7bd2d518c5c5c51e55b78b372041d609c264d2d07973b
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
  b90f66e8b5953de16796e2065e71612dd99dc31dddc4e5203665020ad155a4b8
```

No Cargo manifest or lockfile change.

### 12. Code-only bake

```text
Full:
ASH_PASS3_EVE_MCU_CLOSE_R2_PHYS_R1B_CF1_BASE_CONFIG_SELF_MATERIALIZATION_CODE_ONLY.zip
SHA-256: f464f21779c357f74f89f96a275fdf800af6f768a886b4e37cfd40c50ed89e00
Files: 8423
CRC: PASS

Overlay:
ASH_EVE_MCU_CLOSE_R2_PHYS_R1B_CF1_BASE_CONFIG_SELF_MATERIALIZATION_OVERLAY_CODE_ONLY.zip
SHA-256: f004ed5f2e9622d9ff5983b914db42a858ab985f1f6183bd85daabfb6a0d3a94
Files: 4
CRC: PASS
```

Generated manifest/artifact/report/spec remain outside the code-only ZIPs.

### 13. Validation boundary

Bake environment has no cargo/rustc.

```text
SOURCE: PASS
STATIC SCOPE: PASS
ZIP CRC: PASS
COMPILE: PENDING USER MACHINE
NATIVE: PENDING
CF1 PREFLIGHT: PENDING
A/B/C PHYSICAL: PENDING
PERFORMANCE: UNKNOWN
```

R1B-CF1 removes the nonexistent external config prerequisite, reuses `build_config_from_specs` as config root authority, binds only physically sealed FreshGenesis identities, materializes Muon/scheduler profiles through existing owners, and publishes config only after existing R4/R2 validators accept it.