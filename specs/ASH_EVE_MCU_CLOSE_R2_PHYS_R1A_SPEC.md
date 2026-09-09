# ASH-EVE-MCU-CLOSE-R2-PHYS-R1A

## FRESH R6 SOURCE-STATE GENESIS + GENERATION-ZERO AUTHORITY + R6 LOADER ADMISSION

### 0. Revision

```text
Patch ID:
ASH-EVE-MCU-CLOSE-R2-PHYS-R1A

Direct parent:
ASH-EVE-MCU-CLOSE-R2-PHYS-R1

Parent physical evidence:
PASS_EVE_MCU_CLOSE_R2_PHYS_R1_RESIDENCY_CANARY

Class:
FRESH SOURCE-STATE GENESIS
GENERATION-ZERO WEIGHT AUTHORITY
FRESH ZERO ADAM M/V GENESIS
DATASET CURSOR GENESIS
R6 SOURCE ABI CUTOVER
N8 FRESH-GENESIS FULL-PRODUCTION HOLD
```

### 1. Compile-fix parent refresh

The PHYS-R1 source uses `chrono::Utc`. R1A makes `chrono = "0.4"` a direct dependency of `base_train` and refreshes the existing Cargo.lock `base_train` dependency list. The already present chrono package version is reused. No second chrono lineage is intended.

### 2. Fresh source schema

R1A adds:

```text
ash.basetrain.training_state.fresh_genesis.r1a
```

with explicit:

```text
sourceOrigin = FreshGenesis
trainingGeneration = 0
optimizerStep = 0
historicalParent = null
historicalIdentityReused = false
optimizerStateOrigin = FRESH_GENESIS_ZERO_ADAM_MV
```

Historical `ash.basetrain.training_state.v2` remains a distinct branch and retains its generation-3 / step-3 contract.

### 3. Checkpoint to canonical weight state

The R1A materializer uses the canonical 201-parameter inventory from `canonical_inventory_from_model_spec`.

For every parameter it requires exact:

```text
parameter ID
F32 dtype
logical shape
payload byte span = element_count * 4
```

The safetensors payload is streamed directly from the admitted checkpoint into the generation-zero candidate parameter file. No checkpoint payload mutation occurs.

### 4. Generation-zero optimizer genesis

For every canonical parameter R1A creates fresh Adam M/V payloads with exact parameter byte length and zero contents.

Receipt semantics:

```text
optimizerStateOrigin = FRESH_GENESIS_ZERO_ADAM_MV
historicalOptimizerReused = false
```

This is initial optimizer state, not recovery or resume state.

### 5. Candidate source materialization

R1A publishes:

```text
<physical-output-root>/genesis_r1a/current/training_state/
  active_training_state.json
  candidate_step_000000/
    candidate_parameter_manifest.json
    dataset_cursor_candidate.json
    pNNN_*.weight.f32.bin
    pNNN_*.m.f32.bin
    pNNN_*.v.f32.bin
```

The staging tree is created under `genesis_r1a/.staging` and atomically renamed to `genesis_r1a/current` only after all parameter payloads and receipts are complete.

### 6. Dataset cursor genesis

Fresh cursor is created with:

```text
consumedBatchCount = 0
lastCommittedBatchOrdinal = 0
nextBatchOrdinal = 0
trainingGeneration = 0
optimizerStep = 0
cursorRevision = 0
previousCursorDigest = ""
lastBatchIdentity = GENESIS_UNCOMMITTED
```

The cursor binds exact:

```text
dataset manifest ID
dataset manifest physical SHA-256
tokenizer lineage ID
dataset builder identity
```

Dataset-builder identity uses the same R6 identity formula and therefore requires the actual runtime dataset geometry:

```text
max_seq_len
micro_batch_size
include_bos
include_eos
include_task_tokens
include_lang_tokens
include_glossary_tokens
include_tm_tokens
```

### 7. R6 loader cutover

The existing R6 `initial` source path is split explicitly:

```text
Historical initial:
  schema = ash.basetrain.training_state.v2
  generation = 3
  optimizer step = 3
  cursor next = 3

R1A fresh initial:
  schema = ash.basetrain.training_state.fresh_genesis.r1a
  sourceOrigin = FreshGenesis
  historicalIdentityReused = false
  generation = 0
  optimizer step = 0
  cursor next = 0
  consumed batches = 0
  cursor revision = 0
```

The historical branch is not weakened.

The fresh source is tagged internally as:

```text
packed_source_kind = R1A_FRESH_GENESIS
```

rather than being mislabeled as `R5_LEGACY`.

### 8. No historical identity reuse

The R1A receipt requires all of the following to be false:

```text
historicalN2StateReused
historicalN8StateReused
historicalCursorReused
historicalOptimizerReused
historicalSchedulerReused
```

No old generation, cursor SHA, optimizer moments, scheduler progress, N2 digest or N8 digest is rebound to the new lineage.

### 9. Full production A/B/C blocker discovered during bake

R1A fresh R6 source-state materialization is now implemented, but the current R2 production route still enters the N8 admission branch.

That branch currently requires:

```text
r6_parent_r5_run_dir = forbidden
r6_resume_training_state_dir = required
source generation = promoted generation 5 lineage
n8_physical_n2_promotion_dir = required
```

Therefore the R1A fresh generation-zero root cannot truthfully enter the current N8 route without an additional explicit N8 fresh-genesis cutover.

Changing generation 0 to 5, rewriting the N2 promotion authority, or synthesizing historical N8 resume evidence is forbidden.

This bake therefore does not emit:

```text
PASS_EVE_MCU_CLOSE_R2_PHYS_R1A_FULL_PRODUCTION_ABC
```

and instead retains:

```text
HOLD_EVE_MCU_CLOSE_R2_PHYS_R1A_N8_FRESH_GENESIS_CUTOVER_PENDING
```

### 10. Next exact cutover

The remaining production cutover is narrow:

```text
EVE-MCU-CLOSE-R2-PHYS-R1B
N8 FRESH-GENESIS SOURCE ROLE
+ GENERATION-ZERO N8 ADMISSION
+ FRESH RAM-ADAM AUTHORITY
+ FRESH MUON RUNTIME AUTHORITY
+ NO PHYSICAL N2 PARENT REQUIREMENT FOR FRESH ORIGIN
+ A/B/C FULL PRODUCTION EXECUTION
```

Historical N8 resume retains all existing physical N2 requirements. Only explicit `FreshGenesis` source origin receives the new route.

### 11. Actual source delta

```text
ADD 1
MOD 5
DEL 0
```

Added:

```text
crates/base_train/src/eve_mcu_close_r2_physical_campaign_r1a.rs
```

Modified:

```text
Cargo.lock
crates/base_train/Cargo.toml
crates/base_train/src/bin/base_train.rs
crates/base_train/src/lib.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
```

Source delta digest:

```text
fab94609a24308d4bcc641e8add3093561ea7e011868c6ccd8e47bae0e53684a
```

### 12. Code-only bake

Full:

```text
ASH_PASS3_EVE_MCU_CLOSE_R2_PHYS_R1A_FRESH_R6_SOURCE_GENESIS_CODE_ONLY.zip
SHA-256:
7195be83001159cdafd982bbd7352776f0b1cda65529d19a9a11d28d9995f873
Files: 8422
CRC: PASS
```

Overlay:

```text
ASH_EVE_MCU_CLOSE_R2_PHYS_R1A_FRESH_R6_SOURCE_GENESIS_OVERLAY_REVIEW_ONLY_CODE_ONLY.zip
SHA-256:
de3c3a8f62aa6e3d7c0cd12a3abdae6f84e589964470a3ee383b2feda5aa8103
Files: 6
CRC: PASS
```

Generated manifest, static artifact, report and this specification are excluded from both code-only ZIPs.

### 13. Validation boundary

Bake environment has no `cargo` or `rustc`.

Current evidence:

```text
SOURCE: baked
STATIC: baked
COMPILE: pending user machine
NATIVE: pending
PHYSICAL SOURCE GENESIS: pending
FULL A/B/C: HOLD
PERFORMANCE: unknown
```

### 14. Fresh source-genesis command

After applying the R1A bake and rebuilding/sealing a new CF1, execute:

```powershell
$OUT = ".\workspace\runtime\eve_mcu_close_r2_phys_r1"
$DATASET = Join-Path $OUT "genesis\current\EVE_MCU_CLOSE_R2_PHYS_R1_DATASET_MANIFEST.json"

.\target\release\base_train.exe `
  --eve-mcu-close-r2-phys-r1a-source-genesis `
  --model-spec-path ".\specs\model_spec_v5_48259.toml" `
  --init-checkpoint-path ".\models\ash_v5_native_genesis_full.safetensors" `
  --dataset-manifest-path $DATASET `
  --tokenizer-manifest-id "tokenizer_v5" `
  --physical-output-root $OUT `
  --max-seq-len 512 `
  --micro-batch-size 2 `
  --include-bos true `
  --include-eos true `
  --include-task-tokens true `
  --include-lang-tokens true `
  --include-glossary-tokens true `
  --include-tm-tokens true
```

The dataset geometry arguments must be changed if the actual production configuration differs. They are authority inputs, not cosmetic defaults.

Expected only after successful materialization:

```text
PASS_EVE_MCU_CLOSE_R2_PHYS_R1A_FRESH_SOURCE_GENESIS
```

### 15. Compile sequence

```powershell
cargo test -p base_train --lib --locked
cargo build -p base_train --bin base_train --release --locked -j 1
```

Any successful R1A build changes `base_train.exe`, so PHYS-R1's previous CF1 cannot be reused. Regenerate Native CF1 after the final build.

### 16. Final law

> R1A establishes a truthful generation-zero R6 source state from the admitted v5_48259 checkpoint and PHYS-R1 dataset authority.

> Checkpoint weight bytes become generation-zero weight bytes; Adam M/V begin from fresh zero state; cursor begins at batch zero; no old N2/N8 history is copied or renamed.

> Existing historical R6 source behavior remains intact.

> Full R2 A/B/C is not promoted by this bake because the current N8 route still requires a promoted historical generation-5 resume and physical N2 parent. The next cutover must add an explicit N8 FreshGenesis source role instead of fabricating that history.
