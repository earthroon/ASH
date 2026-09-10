# ASH-EVE-MCU-CLOSE-R2-PHYS-R1B-CF1 SOURCE LOAD WITNESS SCOPE FIX

## Observed physical failure

```text
PHYS_R1_PRODUCTION_ERROR:E_EVE_MCU_CLOSE_PHYS_R1B_SOURCE_LOAD_SCOPE_DRIFT
```

The failure occurred after Native WGPU bootstrap and after the prior FreshGenesis required-batch correction.

## Root cause

The FreshGenesis branch of `r6_required_batch_count()` called:

```rust
load_source(cfg, SourceLoadWitnessContextR1B::Disabled)?
```

while `cfg.training.eve_mcu_close_phys_r1` was active. PHYS-R1B source-load evidence requires the durable source loader to be entered through the live R4-owned witness during the authoritative session bootstrap. A disabled-witness load before the R4 session therefore correctly fails with `E_EVE_MCU_CLOSE_PHYS_R1B_SOURCE_LOAD_SCOPE_DRIFT`.

It would also create an extra durable source read before the one source-read event that the physical receipt is designed to prove.

## Correction

Fresh required-batch sizing performs no source I/O. It checks only the static FreshGenesis source routing shape:

```text
r6_parent_r5_run_dir = SOME
r6_resume_training_state_dir = NONE
```

and uses the R1A FreshGenesis contractually sealed origin:

```text
next_batch_ordinal = 0
```

The canonical `load_source()` remains the sole runtime authority for actual source schema, generation, optimizer step, cursor digest, dataset identity, tokenizer lineage and source bytes after the R4 source-load witness has opened.

Current exact window:

```text
batch origin = 0
optimizer steps = 8
R6 accumulation = 8
required batch count = 64
```

Historical non-fresh N8 keeps its existing `r6_resume_training_state_dir` read and generation/cursor validation unchanged.

## Scope

```text
MOD 1
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
SHA-256:
6636e0e0d1dc7d905069c4037c3bcaec4d64c19aaa70566c375687955cff4175
```

No Cargo manifest/lock change. No Adam, Muon, R13, R4/R2, dataset, checkpoint, source-load witness or historical resume semantics changed.

## Bake identity

```text
Full:
ASH_PASS3_EVE_MCU_CLOSE_R2_PHYS_R1B_CF1_SOURCE_LOAD_WITNESS_SCOPE_FIX_CODE_ONLY.zip
SHA-256:
3ad39e8b4d05a58e70ed2ebfdbec383b2588347a6c8519f1d40da4bd84ac8076
Files: 8423
CRC: PASS

Overlay:
ASH_EVE_MCU_CLOSE_R2_PHYS_R1B_CF1_SOURCE_LOAD_WITNESS_SCOPE_FIX_OVERLAY_CODE_ONLY.zip
SHA-256:
884536d71c2617dae0741f11a86c2c93d56d9984242b2628f6709fc160879f2a
Files: 1
CRC: PASS
```

## Validation boundary

Current evidence is SOURCE/STATIC/ZIP CRC only. User-machine compile, Native CF1 reseal and full A/B/C physical execution remain required.

The historical `N8ResumeRunMissing` check remains present in the historical branch by design.