# ASH-EVE-MCU-CLOSE-R2-PHYS-R1B-CF1-R1D

## FRESH GENESIS ONE-LANE MICRO-BATCH PRODUCTION ABI REALIGNMENT

### 1. Scope

R1D realigns FreshGenesis dataset-builder geometry with the existing R6A-R1 wave-resident production ABI.

Physical blocker entering this correction:

`PHYS_R1_PRODUCTION_ERROR:R6AR1WaveResidentBatchOneLaneRequired`

Confirmed conflict:

- previous R1A FreshGenesis `micro_batch_size = 2`
- previous R1B sealed builder identity `micro_batch_size = 2`
- canonical R6A-R1 executor requires every wave lane to have `batch_size == 1`

Classification: **CONFIRMED CONTRACT CONFLICT**.

### 2. Authority law

The production R6A-R1 one-lane geometry remains authority. FreshGenesis must be generated with `micro_batch_size = 1` before entering production.

No runtime batch splitting, no batch=2 compatibility branch, and no executor invariant weakening are admitted.

### 3. R1A FreshGenesis correction

`crates/base_train/src/eve_mcu_close_r2_physical_campaign_r1a.rs`

- adds `R1D_REQUIRED_MICRO_BATCH_SIZE = 1`
- fails closed unless the R1A request uses micro batch 1
- publishes `maxSeqLen`, `microBatchSize`, and `r6aR1OneLaneContractPass` in the FreshGenesis receipt/state evidence
- keeps generation 0 / optimizer step 0 / fresh zero Adam M,V / no historical reuse semantics

`crates/base_train/src/bin/base_train.rs`

- changes the R1A CLI default `--micro-batch-size` from 2 to 1

### 4. R1B-CF1 correction

`crates/base_train/src/eve_mcu_close_r2_physical_campaign_r1b.rs`

- patch identity becomes `ASH-EVE-MCU-CLOSE-R2-PHYS-R1B-CF1-R1D`
- `R1A_SEALED_MICRO_BATCH_SIZE = 1`
- explicit `R6A_R1_REQUIRED_MICRO_BATCH_SIZE = 1`
- validates the regenerated R1A receipt before config materialization
- rebuilds the dataset-builder identity with micro batch 1 and requires exact cursor identity equality
- sets generated BaseTrainConfig `dataset.micro_batch_size = 1`
- adds an early one-lane fail-closed gate before physical R6A execution
- publishes `configuredMicroBatchSize`, `requiredMicroBatchSize`, and `r6aR1OneLaneContractPass` in preflight and R1B receipts

### 5. Preserved production contracts

The following are intentionally unchanged:

- R6A-R1 executor `batch.batch_size == 1` invariant
- eight logical wave lanes
- optimizer gradient accumulation = 8
- dataset manifest and shard bytes
- Fresh RAM36 authority
- Fresh Muon lineage
- R1C Fresh output publication ordering
- numerical capture topology
- historical N2/N8 resume semantics

Dataset regeneration is **NOT REQUIRED**.

R1A Fresh source/cursor regeneration is **REQUIRED** because dataset-builder identity changes from micro batch 2 to 1.

Native CF1 reseal is **REQUIRED** because source/binary identity changes.

### 6. Forbidden fixes

The following remain forbidden:

- removing `R6AR1WaveResidentBatchOneLaneRequired`
- allowing `batch_size <= 2`
- runtime split from one batch=2 object into two batch=1 lanes
- batch=2 compatibility fallback
- ignoring dataset-builder identity mismatch
- deleting micro batch size from builder identity
- reusing the old R1A cursor/source receipt
- changing accumulation 8 to 16 to emulate previous effective batch size
- rolling back R1C output-authority ordering

### 7. Static bake evidence

R1A:

- required micro batch constant: line 26
- fail-closed request gate: lines 242-245
- Fresh state one-lane evidence: lines 350-351
- receipt micro batch authority: lines 389-390

R1B:

- R1D patch identity: line 29
- sealed Fresh micro batch = 1: line 38
- required production micro batch = 1: line 39
- R1A receipt one-lane admission: lines 175-180
- reconstructed builder one-lane seal: lines 269-272
- generated config one-lane gate: lines 286-291
- preflight one-lane evidence: lines 413-415

CLI:

- R1A `--micro-batch-size` default = 1: line 337

Existing executor, unchanged:

- `R6AR1WaveResidentBatchOneLaneRequired`: line 433 of `packed_runtime_native_bootstrap_accumulation_wave_residency.rs`

Existing accumulation, unchanged:

- `gradient_accumulation = 8`: line 299 of R1B-CF1

No batch=2 compatibility branch was added to the changed R1A/R1B files.

### 8. Bake identity

Changed files and SHA-256:

- `crates/base_train/src/eve_mcu_close_r2_physical_campaign_r1a.rs`
  `f6386e9c1ad75b1b1624af4db262ae2065e2daa45682175fb0922ae824797cb4`
- `crates/base_train/src/eve_mcu_close_r2_physical_campaign_r1b.rs`
  `73b494357711643ffb08eb0ebfeb95bc9d1b768015fc074ee1a15ea198900d55`
- `crates/base_train/src/bin/base_train.rs`
  `355c5d8d834d33a52ee2580e868e0fa8c80116306d236b2c6ddcc18df0ab9466`

Overlay ZIP SHA-256:

`198c8910faba5ffdd44948386a4244568e5a250fe0bcb35f1bfdaf7b37067b5b`

Full code-only ZIP SHA-256:

`10be7a902a1bc8b7ca2af8b920bb0c648ba860cbb53281c636987c14c3b9b8af`

Archive integrity:

- overlay file count: 3
- full code-only file count: 8423
- overlay ZIP CRC: PASS
- full ZIP CRC: PASS
- R6A executor byte identity vs R1C input: PASS
- R1C scheduler byte identity vs R1C input: PASS

### 9. Verification status

- contract conflict: **CONFIRMED**
- static R1D correction: **CONFIRMED**
- archive integrity: **CONFIRMED**
- release compile: **NOT VERIFIED IN BAKE ENVIRONMENT**
- Native CF1: **NOT YET VERIFIED**
- regenerated R1A physical admission: **NOT YET VERIFIED**
- A/B/C physical promotion: **NOT YET VERIFIED**

No compile or physical PASS is claimed by this specification.

### 10. Required physical closure

1. Apply R1D overlay.
2. Clean/rebuild `base_train` release.
3. Delete the old micro-batch-2 R1A source and receipt.
4. Regenerate R1A from the same admitted dataset/checkpoint with `--micro-batch-size 1`.
5. Confirm the new R1A receipt/cursor seals micro batch 1 and a new builder identity.
6. Reseal Native CF1 against the rebuilt binary.
7. Run R1B-CF1 preflight and require one-lane fields to pass.
8. Reenter A/B/C on a fresh campaign root with sufficient numerical capture budget.
9. Treat any downstream first failure as a new attribution boundary.

Final promotion remains gated on the canonical physical PASS receipts.
