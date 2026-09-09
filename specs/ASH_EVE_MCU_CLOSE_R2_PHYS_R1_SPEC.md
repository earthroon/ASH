# ASH-EVE-MCU-CLOSE-R2-PHYS-R1

## PHYSICAL INPUT GENESIS + CANONICAL `base_train.exe` CF1 BINDING + R2 RESIDENCY CANARY

## 0. Revision

```text
Patch ID:
ASH-EVE-MCU-CLOSE-R2-PHYS-R1

Direct code parent:
ASH_PASS3_EVE_MCU_CLOSE_R2_PRODUCTION_SESSION_RESIDENCY_CODE_ONLY.zip

Parent SHA-256:
0dcf28ce1afac158f56390e41075813cffefd6568f31b1ca6b5d1b53c894a703

Class:
PHYSICAL INPUT GENESIS
CANONICAL EXECUTABLE AUTHORITY
CHECKPOINT HEADER GEOMETRY ADMISSION
DATASET LINEAGE PROJECTION WITH SHARD BYTE PRESERVATION
REAL WGPU R2 EXECUTION-RESIDENCY CANARY
FULL PRODUCTION A/B/C HOLD GATE

Algorithm change: NO
Optimizer math change: NO
R13 math change: NO
Mixed precision policy change: NO
Checkpoint payload mutation: NO
Dataset shard mutation: NO
WGPU package graph change: NO
```

## 1. Parent evidence

Input evidence already established on the user machine:

```text
PASS_ASH_WGSL_WGPU26_EXACT_NAGA26_PARSE_R1
PASS_WGPU26_VENDOR_R2_SINGLE_PACKAGE_GRAPH
base_train --lib --release: PASS
base_train native tests: 209 passed / 0 failed / 1 physical-only ignored
```

These are prerequisites. They are not promoted to R2 physical residency evidence by this specification.

## 2. Target external input lineage

Canonical target:

```text
model_spec_id:
model_tinyllama_1p1b_v5_48259

vocab_size:          48259
hidden_size:         2048
num_layers:          22
attention_heads:     32
kv_heads:            4
intermediate_size:   5632

tokenizer_spec_id:
tokenizer_v5
```

Canonical input candidates selected by the operator:

```text
specs/model_spec_v5_48259.toml
artifacts/tokenizer_manifest_v5_final.json
specs/dataset_manifest_v5_guarded_phaseA.json
models/ash_v5_native_genesis_full.safetensors
```

The dataset file is a seed only. Its source lineage is v4 / tokenizer_v5_final and therefore cannot be the PHYS-R1 target authority unchanged.

## 3. Dataset materialization law

PHYS-R1 loads the seed `DatasetManifest`, resolves every train/eval/test shard, streams SHA-256 over every inherited shard, and rejects missing/duplicate shards.

It materializes under the physical output root:

```text
genesis/current/EVE_MCU_CLOSE_R2_PHYS_R1_DATASET_MANIFEST.json
genesis/current/EVE_MCU_CLOSE_R2_PHYS_R1_DATASET_SHARD_EVIDENCE.json
```

Generated lineage:

```text
dataset_manifest_id:
eve_mcu_close_r2_phys_r1_v5_48259_phaseA

model_spec_id:
model_tinyllama_1p1b_v5_48259

tokenizer_spec_id:
tokenizer_v5
```

The shard lists and shard bytes are not rewritten. PHYS-R1 changes manifest identity/lineage/hashes only.

No retokenized corpus is generated.

## 4. Checkpoint header admission

PHYS-R1 reads only the safetensors 8-byte header prefix plus declared JSON header before full payload hashing.

The expected canonical parameter inventory comes from existing:

```text
canonical_inventory_from_model_spec(spec)
```

For the v5_48259 target this is the existing 201-parameter authority.

Every expected parameter must have:

```text
exact parameter ID
exact logical shape
F32 dtype
```

The header may contain `__metadata__`; other unexpected tensors reject.

Receipt:

```text
genesis/current/EVE_MCU_CLOSE_R2_PHYS_R1_CHECKPOINT_ADMISSION.json
```

No checkpoint bytes are changed by PHYS-R1.

## 5. Canonical executable authority

### Meaning change from the initial proposal

The initial PHYS-R1 draft proposed that `base_train.exe` build and seal itself before running the campaign.

That is retired.

On Windows the running executable must not rebuild/replace itself while also claiming exact binary identity.

The authoritative flow is two-stage:

```text
ash_control_runtime
    -> cargo build --locked --release -p base_train --bin base_train
    -> seal exact target/release/base_train.exe SHA-256
    -> publish Native CF1 authority externally

exact target/release/base_train.exe
    -> load that CF1 authority
    -> hash std::env::current_exe()
    -> exact CF1 equality
    -> PHYS-R1 input genesis / R2 canary
```

No harness executable is allowed to impersonate `base_train.exe`.

## 6. Canonical CLI entry

`base_train.exe` now has a dedicated early-dispatch CLI:

```text
--eve-mcu-close-r2-physical-campaign
--workspace-root
--model-spec-path
--tokenizer-manifest-path
--dataset-seed-manifest-path
--init-checkpoint-path
--physical-output-root
--native-cf1-release-authority
--preflight-only
--require-full-production-abc
```

The PHYS-R1 selector is checked before the existing normal `Cli::parse()` path.

When the PHYS-R1 flag is absent, the parent base_train CLI remains the execution path.

## 7. Input genesis receipt

Materialized:

```text
genesis/current/EVE_MCU_CLOSE_R2_PHYS_R1_INPUT_GENESIS.json
```

It binds:

```text
model spec path / SHA / model_spec_id
tokenizer path / SHA / manifest_id / tokenizer_spec_id / vocab size
seed dataset path / SHA
generated dataset path / SHA / manifest ID
inherited shard set digest
checkpoint admission path / checkpoint SHA
Native CF1 path
CF1 canonical binary SHA
runtime current_exe SHA
exact binary match
```

## 8. Real WGPU R2 residency canary

After input genesis, unless `--preflight-only` is selected, PHYS-R1 calls the existing physical WGPU bootstrap:

```text
bootstrap_existing_device("eve_mcu_close_r2_phys_r1_residency_canary")
```

It then creates one:

```text
TrainableSessionExecutionResidencyR2
```

and calls `bind_or_materialize` three times:

```text
generation 0: first materialization
generation 0: restore/reuse
generation 1: generation refresh with same execution allocations
```

Required exact Arc continuity:

```text
FFN executor identity unchanged
R13 execution identity unchanged
```

## 9. R13 physical status-slot canary

PHYS-R1 creates two 64-element F32 buffers on the same physical Device/Queue and executes:

```text
r13_add2_with_execution_r2(...)
r13_add2_with_execution_r2(...)
```

through the same session-resident R13 executor.

This executes the real R13 session pipeline, real compact status readback, A01 SubmissionEpoch path, A03 compact readback authority and exact completion wait.

Required telemetry:

```text
execution_residency_construct_count = 1
execution_residency_restore_count >= 2
execution_residency_release_count = 1
generation_refresh_count = 1
generation_regression_reject_count = 0
device_queue_identity_mismatch_count = 0
ffn_executor_bound = true
r13_execution_bound = true
r13_pipeline_slab_build_count = 1
r13_pipeline_slab_reuse_count >= 2
r13_hotpath_pipeline_create_count = 0
status_slot_acquire_count >= 2
status_slot_reuse_count >= 1
status_slot_exhaust_count = 0
status_slot_inflight_reuse_reject_count = 0
```

Receipt:

```text
qualification/EVE_MCU_CLOSE_R2_PHYS_R1_RESIDENCY_CANARY.json
```

Pass token for this exact scope:

```text
PASS_EVE_MCU_CLOSE_R2_PHYS_R1_RESIDENCY_CANARY
```

This is physical evidence for R2 executor/status-slot residency mechanics. It is not the full production A/B/C promotion token.

## 10. Full production A/B/C conflict discovered during bake

The parent R6 production path cannot consume the raw v5 genesis checkpoint as a truthful fresh source state.

Current source admission requires a pre-existing R6/R5/N8 training state with exact:

```text
generation / optimizer step
DatasetCursorV1
dataset manifest ID
dataset manifest physical SHA
tokenizer lineage
scheduler state
candidate/packed weight state
optimizer state
```

The historical immutable N2/N8 parent cannot be reused for the newly generated v5_48259 dataset authority because R6 verifies:

```text
source.cursor.dataset_manifest_id == current dataset manifest ID
source.cursor.tokenizer_lineage_id == current tokenizer manifest ID
source.cursor.dataset_manifest_sha256 == physical current dataset manifest SHA
```

Relabeling the historical state would create source-history fiction and is prohibited.

Therefore this bake does NOT fabricate generation-3/5 state or zero Adam state and claim it was previously trained.

## 11. Full A/B/C HOLD law

When:

```text
--require-full-production-abc
```

is requested, this revision first performs exact input genesis and the real R2 residency canary, then emits:

```text
HOLD_EVE_MCU_CLOSE_R2_PHYS_R1_FULL_PRODUCTION_SOURCE_STATE_GENESIS_PENDING
```

and records:

```text
full_production_abc_promoted = false
```

No `PASS_EVE_MCU_CLOSE_R2_PHYS_R1_PRODUCTION_SESSION_RESIDENCY` token exists in this bake.

The next revision must materialize a truthful fresh R6 source-state genesis from the admitted checkpoint or establish a separately proven exact v5 descendant authority before A/B/C may be promoted.

## 12. No hidden source-state fallback

Forbidden:

```text
reuse old N2 state with rewritten dataset ID
rewrite old cursor SHA to new manifest SHA
pretend zero Adam M/V are generation-5 trained optimizer state
infer missing scheduler history
silently use the old physical harness binary
```

## 13. Actual source delta

Relative to EVE-MCU-CLOSE-R2:

```text
ADD 1
MOD 2
DEL 0
```

Added:

```text
crates/base_train/src/eve_mcu_close_r2_physical_campaign_r1.rs
```

Modified:

```text
crates/base_train/src/bin/base_train.rs
crates/base_train/src/lib.rs
```

No Cargo manifest or lockfile change.

Source-delta digest:

```text
e84c3cf7def360d1d22f89498e28e0061e676fd5534166035a0bc1f6bf894ca4
```

Changed file SHA-256:

```text
crates/base_train/src/eve_mcu_close_r2_physical_campaign_r1.rs
c58a673a2b2ba36515f84f8a5f5ead0f4f6afe35af289eed049209545d370bab

crates/base_train/src/bin/base_train.rs
4b2fc8a641ece7226f070af344ce7274ca560ec95fd324e92b75ee438f021667

crates/base_train/src/lib.rs
1a60f1b974d266e18ea4aed8a6ecc9a07a322491e37d75cdc8a380ee1420b58d
```

## 14. Static checks actually executed in bake environment

```text
parent file count                              8420
current file count                             8421
source delta                                   ADD1 / MOD2 / DEL0
root Cargo.toml byte-identical                 PASS
root Cargo.lock byte-identical                 PASS
crates/base_train/Cargo.toml byte-identical    PASS
changed-source delimiter balance               PASS
new PHYS-R1 Rust source `if` token count        0
full-production PASS token in implementation   0
full_production_abc_promoted=true               0
Full ZIP CRC                                    PASS
Overlay ZIP CRC                                 PASS
```

The delimiter check is static text validation, not Rust compilation.

## 15. Validation boundary

Bake environment:

```text
cargo: unavailable
rustc: unavailable
```

Therefore this revision currently admits only:

```text
SOURCE / STATIC BAKE
```

Not yet admitted from this environment:

```text
COMPILE
NATIVE
PHYSICAL CANARY
FULL PRODUCTION PHYSICAL
PERFORMANCE
```

The user machine must compile and run the commands in §17-19.

## 16. Code-only bake identity

Full code-only ZIP:

```text
ASH_PASS3_EVE_MCU_CLOSE_R2_PHYS_R1_PHYSICAL_INPUT_GENESIS_CODE_ONLY.zip
SHA-256:
59d3b7c21ab2deb5d68d64381e3eb5f549e310485a0f833f53134191f8564002
Files: 8421
CRC: PASS
```

Review-only overlay:

```text
ASH_EVE_MCU_CLOSE_R2_PHYS_R1_PHYSICAL_INPUT_GENESIS_OVERLAY_REVIEW_ONLY_CODE_ONLY.zip
SHA-256:
e25d580d076d602ee7c1329fa4cfc1cccf7f8385af48c253dfc98c0556c5d03e
Files: 3
CRC: PASS
```

Generated manifest / qualification artifact / report / specification are excluded from both ZIPs.

## 17. User-machine compile sequence

After applying the code bake:

```powershell
cargo test -p base_train --lib --locked

cargo build -p base_train --bin base_train --release --locked -j 1
```

Do not use a separate R1 physical harness for PHYS-R1 promotion.

## 18. Native CF1 materialization

The canonical binary must be sealed externally:

```powershell
$OUT = ".\workspace\runtime\eve_mcu_close_r2_phys_r1"
$CF1_ROOT = Join-Path $OUT "cf1"

cargo run -p ash_control_runtime --release --locked -- `
  native-cf1-release-compile-authority `
  --repo-root . `
  --authority-root $CF1_ROOT `
  --package base_train `
  --bin base_train `
  --profile release

$CF1 = (
  Get-ChildItem $CF1_ROOT -Recurse -File `
    -Filter "native_cf1_release_compile_authority.json" |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 1
).FullName
```

The CF1 command itself rebuilds the canonical `base_train.exe` and seals those exact bytes. Do not rebuild `base_train.exe` after this step before executing PHYS-R1.

## 19. PHYS-R1 commands

### Input-genesis preflight only

```powershell
.\target\release\base_train.exe `
  --eve-mcu-close-r2-physical-campaign `
  --workspace-root . `
  --model-spec-path ".\specs\model_spec_v5_48259.toml" `
  --tokenizer-manifest-path ".\artifacts\tokenizer_manifest_v5_final.json" `
  --dataset-seed-manifest-path ".\specs\dataset_manifest_v5_guarded_phaseA.json" `
  --init-checkpoint-path ".\models\ash_v5_native_genesis_full.safetensors" `
  --physical-output-root $OUT `
  --native-cf1-release-authority $CF1 `
  --preflight-only
```

Expected only if all inputs really match:

```text
PASS_EVE_MCU_CLOSE_R2_PHYS_R1_INPUT_GENESIS_PREFLIGHT
```

### Real WGPU residency canary

```powershell
.\target\release\base_train.exe `
  --eve-mcu-close-r2-physical-campaign `
  --workspace-root . `
  --model-spec-path ".\specs\model_spec_v5_48259.toml" `
  --tokenizer-manifest-path ".\artifacts\tokenizer_manifest_v5_final.json" `
  --dataset-seed-manifest-path ".\specs\dataset_manifest_v5_guarded_phaseA.json" `
  --init-checkpoint-path ".\models\ash_v5_native_genesis_full.safetensors" `
  --physical-output-root $OUT `
  --native-cf1-release-authority $CF1
```

Expected only after actual WGPU execution succeeds:

```text
PASS_EVE_MCU_CLOSE_R2_PHYS_R1_RESIDENCY_CANARY
```

### Full production A/B/C gate probe

```powershell
.\target\release\base_train.exe `
  --eve-mcu-close-r2-physical-campaign `
  --workspace-root . `
  --model-spec-path ".\specs\model_spec_v5_48259.toml" `
  --tokenizer-manifest-path ".\artifacts\tokenizer_manifest_v5_final.json" `
  --dataset-seed-manifest-path ".\specs\dataset_manifest_v5_guarded_phaseA.json" `
  --init-checkpoint-path ".\models\ash_v5_native_genesis_full.safetensors" `
  --physical-output-root $OUT `
  --native-cf1-release-authority $CF1 `
  --require-full-production-abc
```

This bake intentionally returns/records:

```text
HOLD_EVE_MCU_CLOSE_R2_PHYS_R1_FULL_PRODUCTION_SOURCE_STATE_GENESIS_PENDING
```

until the next source-state genesis revision is implemented.

## 20. Promotion states

```text
SourceBaked
InputGenesisCompileReady
InputGenesisPreflightPass
R2ResidencyCanaryPhysicalPass
FullProductionSourceStateGenesisPending
FullProductionAbcPhysicalPass
PerformanceMeasured
```

This source bake reaches only `SourceBaked` in the bake environment.

## 21. Next exact revision

After the canary is physically proven, the remaining blocker is narrow:

```text
EVE-MCU-CLOSE-R2-PHYS-R1A
FRESH R6 SOURCE-STATE GENESIS
+ CHECKPOINT -> CANONICAL WEIGHT STATE
+ ZERO-OPTIMIZER GENESIS AS GENERATION ZERO
+ NEW DATASET CURSOR GENESIS
+ SCHEDULER GENESIS
+ NO HISTORICAL N2 IDENTITY FICTION
+ A/B/C PRODUCTION PROMOTION
```

The generation-zero optimizer state must be explicitly defined as fresh optimizer genesis, not represented as a historical generation-3/5 state.

## 22. Final law

> PHYS-R1 materially closes the missing v5_48259 input genesis, exact canonical executable binding, and real WGPU R2 execution-residency canary path.

> It does not rewrite Phase-A shard bytes or the candidate checkpoint.

> It does not reuse a historical N2/N8 source state whose dataset/tokenizer cursor identity conflicts with the newly materialized v5_48259 dataset authority.

> The R13 canary executes twice through one session-resident R13 pipeline slab and bounded compact status authority, while the same FFN/R13 Arc identities survive restore and a generation refresh.

> Full production A/B/C remains HOLD until a truthful generation-zero R6 source-state genesis exists. This HOLD is preferable to fabricating optimizer/dataset/scheduler history.
