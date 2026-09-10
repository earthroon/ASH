# ASH-EVE-MCU-CLOSE-R2-PHYS-R1B

## N8 FRESH-GENESIS SOURCE ROLE + FULL R2 PHYSICAL PROMOTION

### Revision

```text
Patch ID: ASH-EVE-MCU-CLOSE-R2-PHYS-R1B
Direct parent: ASH-EVE-MCU-CLOSE-R2-PHYS-R1A corrected parent
Required parent physical token: PASS_EVE_MCU_CLOSE_R2_PHYS_R1A_FRESH_SOURCE_GENESIS
Algorithm / Adam math / Muon math / R13 math change: NO
Historical resume relaxation: NO
```

### 1. Fresh source role

R1B adds explicit N8 role `FRESH_GENESIS_R1A`. It is admitted only when the R1A source is schema `ash.basetrain.training_state.fresh_genesis.r1a`, generation 0, optimizer step 0 and cursor-next 0.

Fresh mode forbids physical-N2 promotion, cross-release parent compatibility, legacy migration descendant authority, resume-cut authority, immutable-N2 RAM36 parent authority and a historical RAM36 parent inventory receipt. Supplying any such evidence to the fresh branch is a reject.

Historical `PromotedParent` and `LegacyMigrationDescendant` branches retain their existing validators and pass tokens. R1B does not translate generation zero to generation five.

### 2. Fresh packed state

The existing deterministic genesis-pack/cache authority is extended to accept the exact R1A generation-zero source. The packed manifest records generation 0 / optimizer step 0 and the existing parameter/optimizer digests. It does not rewrite the source as an R5 generation-3 state.

### 3. RAM-Adam

Fresh RAM-Adam uses the existing `RamResidentAdamMv` hydrate authority against the packed R1A zero M/V state. The scheduler does not create a second zero optimizer state. Historical resume hydration remains unchanged.

### 4. Muon

Fresh Muon requires the existing `admit_tensorcube_local_muon_new_lineage` path. Existing new-lineage zero momentum semantics remain authority. R1B adds no Muon arithmetic and does not import historical momentum sidecars into FreshGenesis.

### 5. Scheduler

Fresh source has no historical scheduler state. R1B materializes `n8_fresh_genesis_scheduler_admission_r1b.json` with initial scheduler step 0, extension count 0 and replay count 0. The N8 finalizer reads this fresh receipt instead of fabricating `n8_scheduler_horizon_extension_receipt.json`. Historical finalization remains unchanged.

### 6. Fresh N8 exact window

Required identity for one eight-step fresh window:

```text
source generation       0
source optimizer step   0
source cursor next      0
final generation        8
final optimizer step    8
final cursor last       63
final cursor next       64
final cursor consumed   64
```

Pass token:

```text
PASS_ASH_BASETRAIN_N8_FRESH_GENESIS_EXACT_8_WINDOW_GEN0_TO_GEN8_OPT0_TO_OPT8_CURSOR0_TO64_R1B
```

### 7. A/B/C orchestration

R1B reuses the existing `eve_mcu_close_physical_campaign_r1` production orchestration instead of duplicating R4/R2 close semantics. The generated base config enables FreshGenesis, disables N8 deferred durable writeback for the correctness campaign, removes every historical N2/N8 parent input, enables the existing Muon new-lineage path, and preserves the base production profile.

A/B/C plans remain the parent physical campaign's canonical plans. R1B validates each leg's N8 receipt and R2 residency receipt after the parent campaign returns.

Required per-leg R2 evidence includes construct count 1, release count 1, FFN/R13 bound, R13 slab build 1, hotpath pipeline create 0, generation regression 0, device/queue mismatch 0, status-slot exhaust 0 and in-flight reuse reject 0. B and C additionally require restore count > 0.

### 8. Promotion

Only after A, B and C all validate does R1B write `EVE_MCU_CLOSE_R2_PHYS_R1B_FULL_PRODUCTION_PROMOTION.json` with:

```text
fullProductionAbcPromoted = true
fullR2PhysicalPromoted = true
passToken = PASS_EVE_MCU_CLOSE_R2_PHYS_R1B_FULL_PRODUCTION_ABC
fullR2PhysicalPassToken = PASS_EVE_MCU_CLOSE_R2_FULL_PRODUCTION_SESSION_RESIDENCY_PHYSICAL
```

Preflight emits neither full-production nor full-R2 promotion.

### 9. Required input config

R1B accepts `--base-config-path` to an already valid production `BaseTrainConfig` JSON. R1B intentionally does not synthesize scheduler/model/optimizer/MCU policy from guesses. It overrides only the physical input paths, FreshGenesis source binding, N8 fresh mode, CF1 authority, eight-step budget and correctness-campaign fields.

The base config must already admit the required R4/R2/RAM-Adam/RAM-weight/Muon production parents.

### 10. Actual source delta

```text
ADD 1
MOD 7
DEL 0
source-delta digest: bb9527f765639b4e72b9a657fafe8c91714ca7fed8b508123e9f7b8cea43f9f9
```

Added: `crates/base_train/src/eve_mcu_close_r2_physical_campaign_r1b.rs`.

Modified: `bin/base_train.rs`, `config.rs`, `eve_mcu_close_physical_campaign_r1.rs`, `lib.rs`, `n8_long_horizon_continuity.rs`, `pipeline.rs`, `production_multistep_loop_accumulation8_scheduler.rs`.

### 11. Code-only bake identity

Current corrected full bake:

```text
Full: ASH_PASS3_EVE_MCU_CLOSE_R2_PHYS_R1B_MOVE_OWNERSHIP_FIX_CODE_ONLY.zip
SHA-256: d333d432c2fc2eb1d5c2ee92adfc7503bae4c907285cb6eebe380636ce2b56df
Files: 8423
CRC: PASS

Overlay: ASH_EVE_MCU_CLOSE_R2_PHYS_R1B_MOVE_OWNERSHIP_FIX_OVERLAY_CODE_ONLY.zip
SHA-256: 36ce6969280e885479e320b87bca0ff997e1a2aca4a4f48f3d7630c21695f46d
Files: 1
CRC: PASS
```

Generated manifest/artifact/report/spec are excluded from both code-only ZIPs.

### 11A. Campaign output ownership correction

Observed compile failure:

```text
error[E0382]: use of moved value: request.campaign_output_root
```

Root cause: `request.campaign_output_root` was moved into `PhysicalCampaignInputR1.output_root` and then read again after the parent campaign returned.

The corrected R1B runner does not add a clone. The parent campaign already returns its promotion receipt path, so R1B derives the authoritative campaign root from that receipt:

```rust
let campaign_root = promotion
    .parent()
    .context("E_R1B_PARENT_CAMPAIGN_ROOT_MISSING")?;
```

The campaign-root consumer calls now borrow that recovered `&Path`. This changes no A/B/C, FreshGenesis, N8, RAM-Adam, Muon, R2, or promotion semantics.

Corrected source file:

```text
crates/base_train/src/eve_mcu_close_r2_physical_campaign_r1b.rs
SHA-256: ab16e8c9cc547d7a3af6b952ee86bd50ca09b7c2ad59b0b753c424affb0de43c
```

### 12. Validation boundary

Bake environment has no cargo/rustc. Current evidence is SOURCE/STATIC only. COMPILE, NATIVE, A/B/C PHYSICAL and PERFORMANCE must be established on the user machine.

### 13. Final law

R1B gives N8 a truthful FreshGenesis source role instead of weakening or forging the historical generation-5 physical-N2 contract. Fresh RAM-Adam and Muon use their existing owners. Full R2 physical promotion is emitted only after the real production A/B/C leg receipts satisfy the fresh N8 and R2 residency contracts. Performance remains a separate later claim.
