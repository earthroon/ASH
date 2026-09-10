# ASH-EVE-MCU-CLOSE-R2-PHYS-R1B-CF1

## BASE CONFIG SELF-MATERIALIZATION + R1A DATASET IDENTITY REBIND + SEALED R4/R4A/R2 PROFILE

### Revision

```text
Patch ID: ASH-EVE-MCU-CLOSE-R2-PHYS-R1B-CF1
Direct code parent: ASH_PASS3_EVE_MCU_CLOSE_R2_PHYS_R1B_MOVE_OWNERSHIP_FIX_CODE_ONLY.zip
Parent SHA-256: d333d432c2fc2eb1d5c2ee92adfc7503bae4c907285cb6eebe380636ce2b56df
Required parent physical token: PASS_EVE_MCU_CLOSE_R2_PHYS_R1A_FRESH_SOURCE_GENESIS
Algorithm / Adam / Muon / R13 math change: NO
Historical resume relaxation: NO
```

### 1. Retired external config premise

`--base-config-path` is removed from the R1B CLI. The codebase has no canonical standalone `BaseTrainConfig` JSON for normal production. R1B-CF1 now uses the same root authority as ordinary `base_train`:

```text
ModelSpec + TokenizerManifest + DatasetManifest
    -> build_config_from_specs(...)
    -> exact FreshGenesis rebinding
    -> sealed campaign config output
```

The generated JSON is a receipt/output, not an operator prerequisite.

### 2. R1A dataset-builder authority

R1A physically sealed a cursor digest but did not persist the raw builder tuple. The admitted R1A campaign was created with:

```text
max_seq_len = 512
micro_batch_size = 2
include_bos = true
include_eos = true
include_task_tokens = true
include_lang_tokens = true
include_glossary_tokens = true
include_tm_tokens = true
```

R1B-CF1 does not silently assume that tuple. It recomputes the canonical dataset-builder identity from the tuple and `tokenizer_v5`, then requires exact equality with the R1A cursor `dataset_builder_identity`. Any drift rejects with `E_R1B_CF1_DATASET_BUILDER_IDENTITY_MISMATCH`.

A later genesis revision should persist raw geometry directly in its receipt. This correction does not mutate the already-passed R1A source.

### 3. Fresh tokenizer lineage correction

R1A cursor lineage is `tokenizer_v5` (`tokenizer_spec_id`). The tokenizer manifest's separate `manifest_id` is `tok_v5_48259_candidate`.

The previous production pipeline passed `manifest_id` unconditionally into R6 source validation, which would reject the valid R1A fresh cursor. R1B-CF1 now selects:

```text
FreshGenesisR1A -> tokenizer_spec_id
Historical paths -> manifest_id
```

Historical resume semantics therefore remain unchanged.

### 4. Self-materialized production profile

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

Original CF1 source delta relative to R1B move-fix:

```text
ADD 0
MOD 4
DEL 0
source-delta digest:
bf55cc5791f672fd0913c83a2f1cdcc130da1d43096469f777cafcef895c2530
```

### 12. R1 base-plan seal correction

Observed full-campaign failure:

```text
Error: E_EVE_MCU_CLOSE_R1_PLAN_INVALID
```

Root cause: the CF1 self-materializer persisted `BaseTrainConfig` with `admit_eve_mcu_close_r1=true` but an empty `eve_mcu_close_r1_invocations` vector. Only a temporary validation clone carried the canonical `[8, CloseAfterDurableWriteback]` plan. The parent physical campaign prepares the persisted base config before substituting per-leg A/B/C plans, so the R1 validator correctly rejected the empty base plan.

Correction: seal the canonical single-invocation A plan into the generated base config itself before validation/publication:

```text
optimizer_steps = 8
exit = CloseAfterDurableWriteback
```

The parent physical campaign later replaces only this invocation plan for B/C. Workload identity remains unchanged because the parent workload digest explicitly removes `eve_mcu_close_r1_invocations`.

Correction scope:

```text
MOD 1
crates/base_train/src/eve_mcu_close_r2_physical_campaign_r1b.rs
SHA-256: b255e90ad8c8adbb5f5e86526d4d068e4774196594adb8ef0a8c2fdfe5727b82
```

Current corrected bake:

```text
Full:
ASH_PASS3_EVE_MCU_CLOSE_R2_PHYS_R1B_CF1_R1_PLAN_SEAL_FIX_CODE_ONLY.zip
SHA-256: f3e293f396536c0e0626148a50892782c3507ebd5e6f962170ee3d5bc72d6bb7
Files: 8423
CRC: PASS

Overlay:
ASH_EVE_MCU_CLOSE_R2_PHYS_R1B_CF1_R1_PLAN_SEAL_FIX_OVERLAY_CODE_ONLY.zip
SHA-256: 0fdfa8a8d1e83138a235d07f483fe12af3caab0336f6fc8710d2d0a931baf0d0
Files: 1
CRC: PASS
```

### 13. Validation boundary

Bake environment has no cargo/rustc. The corrected bake is SOURCE/STATIC only until the user machine rebuilds, reseals Native CF1, and reruns the full physical campaign.

R1B-CF1 removes the nonexistent external config prerequisite, reuses `build_config_from_specs` as config root authority, and now also guarantees that the generated BaseTrainConfig is itself a valid R1 close-plan authority before parent A/B/C campaign preparation.