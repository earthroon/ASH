# ASH-EVE-MCU-CLOSE-R2-PHYS-R1B-CF1 N8 REQUIRED-BATCH FRESH-SOURCE FIX

## Observed physical failure

```text
PHYS_R1_PRODUCTION_ERROR:N8ResumeRunMissing
```

The error occurred after the real WGPU native bootstrap succeeded. Therefore FreshGenesis input/config/CF1 admission reached the production dataset sizing path.

## Root cause

`r6_required_batch_count()` retained a historical-only assumption:

```text
admit_n8_long_horizon_continuity = true
-> r6_resume_training_state_dir required
```

R1B FreshGenesis deliberately has no resume run. Its initial authority is the R1A generation-zero source under `r6_parent_r5_run_dir`.

The main production scheduler had already split FreshGenesis from historical N8, but this pre-dataset required-batch helper had not.

## Correction

`r6_required_batch_count()` now matches explicitly on:

```text
(admit_n8_long_horizon_continuity, admit_n8_fresh_genesis_r1b)
```

Fresh branch:

```text
load R1A initial source through existing load_source authority
require schema = ash.basetrain.training_state.fresh_genesis.r1a
require generation = 0
require optimizer step = 0
require cursor next = 0
use cursor.next_batch_ordinal as required-batch origin
```

Historical N8 retains the existing `r6_resume_training_state_dir`, generation-5/resume-cut schema and cursor validation unchanged.

For the R1B-CF1 eight-step, accumulation-8 campaign:

```text
required batch origin = 0
required optimizer steps = 8
logical microbatches per optimizer step = 8
required batch count = 64
```

## Scope

```text
MOD 1
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
SHA-256:
a91093d166ce248673e64f661d41107ccf9a3e57f842b0aeb8f7d2be6cd22bdd
```

No Cargo manifest/lock change. No optimizer, Muon, R13, R4/R2, dataset, checkpoint or historical-resume semantics changed.

## Bake identity

```text
Full:
ASH_PASS3_EVE_MCU_CLOSE_R2_PHYS_R1B_CF1_N8_REQUIRED_BATCH_FRESH_SOURCE_FIX_CODE_ONLY.zip
SHA-256:
e227abbffd6499eb1413f69ddce773684bdc4fc2a4a0e3ba569d2be354db0b27
Files: 8423
CRC: PASS

Overlay:
ASH_EVE_MCU_CLOSE_R2_PHYS_R1B_CF1_N8_REQUIRED_BATCH_FRESH_SOURCE_FIX_OVERLAY_CODE_ONLY.zip
SHA-256:
2c85661baf6fb4e7f381afc0101b24d40aa8843e86d229932f45490a1a5a0ca6
Files: 1
CRC: PASS
```

## Validation boundary

Current bake evidence is SOURCE/STATIC/ZIP CRC only. User-machine compile, Native CF1 reseal and A/B/C physical execution remain required.

The historical `N8ResumeRunMissing` guard intentionally remains present in the historical branch and must not be removed globally.