# TENSORCUBE-TABLE-R4B

## GENERATION-RESIDENT TRAINING STATE TABLE
## + GPU ACCUMULATION8 BINDING
## + DEVICE-HOT OPTIMIZER STATE PROMOTION BOUNDARY

## 0. Revision

```text
Patch ID:
TENSORCUBE-TABLE-R4B

Canonical name:
ASH-BASETRAIN-TENSORCUBE-TABLE-R4B-
GENERATION-RESIDENT-TRAINING-STATE-
GPU-ACCUMULATION8-
DEVICE-HOT-OPTIMIZER-STATE
```

Direct parent:

```text
TENSORCUBE-TABLE-R4A-CF2-CF1
DIRECT PRODUCER OUTPUT -> CF1 SHARED ARENA
```

Semantic parents preserved:

```text
R6A-R1 accumulation-wave residency
RAM-resident Adam M/V
RAM weight-pack persistent residency
MCU SESSION R7
MCU resource R7A
R7A1 packed-gradient lifetime
P4 exact lease
P5 ActiveAsync
R3C/R3C1 generation commit
```

## 1. Target architecture

R4B raises the TensorCube Table lifetime from chunk/wave orchestration to the training-generation runtime.

Target law:

```text
TensorCube Table
= generation-long residency/lifecycle directory

Payload bytes
= specialized GPU/RAM arenas
```

The Table does not become a giant tensor payload buffer.

## 2. First source materialization in this bake

This first R4B source bake materially closes:

```text
one generation-lifetime runtime opened before the optimizer loop
real source-generation / optimizer-step binding
real R6DeviceAccumulatorReceipt binding per optimizer transaction
exact accumulation8 observation
F32 accumulator authority
201 logical model parameters
zero gradient payload readback
zero full gradient host materialization
generation/optimizer rebind after every committed step
resident-weight authority observation
RAM-resident optimizer authority observation
ordinary weight-source disk-byte attribution
ordinary optimizer-state disk-byte attribution
one runtime table-directory creation
zero per-wave R4B directory creation
zero per-parameter R4B directory creation
```

The new production runtime is:

```text
TensorCubeTableR4BGenerationRuntime
```

and survives the complete production optimizer loop for one invocation.

## 3. Existing real GPU accumulation authority

R4B does not invent a second accumulator.

It binds the already-live:

```text
burn_webgpu_backend::R6DeviceGradientAccumulator
```

through its real:

```text
R6DeviceAccumulatorReceipt
```

Required per observed optimizer step:

```text
microbatch_count = 8
accumulator_dtype = F32
logical_parameter_count = 201
nonfinite_count = 0
production_gradient_payload_readback_count = 0
full_gradient_host_materialization_count = 0
```

This establishes a real GPU accumulation8 parent for later table-owned residency cutover.

## 4. Generation directory identity

The runtime opens with:

```text
source_generation = G
optimizer_step = S
```

Every observed step must be:

```text
candidate_generation = G + 1
optimizer_step = S + 1
```

After canonical commit:

```text
current source generation := G + 1
current optimizer step     := S + 1
```

The runtime records one generation rebind per committed optimizer transaction.

## 5. Current residency classification

This bake introduces explicit residency tiers:

```text
NotPresent
DurableCold
RamResident
DeviceHot
CandidateDeviceHot
Retiring
Failed
```

Current real observations are classified as:

```text
Gradient accumulator = DeviceHot
Persistent source weight = RamResident when admitted
Adam M/V full run-local backing = RamResident when admitted
```

## 6. Honest materialization boundary

Current source constants are intentionally:

```text
TENSORCUBE_TABLE_R4B_GENERATION_DIRECTORY_MATERIALIZED = true
TENSORCUBE_TABLE_R4B_GPU_ACCUMULATION8_BINDING_MATERIALIZED = true
TENSORCUBE_TABLE_R4B_DEVICE_HOT_OPTIMIZER_STATE_MATERIALIZED = false
TENSORCUBE_TABLE_R4B_FULL_ROUTE_GPU_ROW_TABLE_MATERIALIZED = false
```

Therefore this first bake does **not** claim:

```text
Adam M/V device-hot paging complete
full optimizer state VRAM residency
all AdamW/HiMuon route rows materialized into one GPU table
full model VRAM residency
cross-wave device-driven refill
zero PCIe traffic
```

## 7. Activation modes

```text
ASH_TENSORCUBE_TABLE_R4B_MODE=OFF
ASH_TENSORCUBE_TABLE_R4B_MODE=OBSERVE_ONLY
ASH_TENSORCUBE_TABLE_R4B_MODE=ACTIVE_VERIFIED
```

First physical campaign target:

```text
OBSERVE_ONLY
```

`ACTIVE_VERIFIED` is fail-closed until both missing authorities are materialized.

Reserved HOLD:

```text
HOLD_TENSORCUBE_TABLE_R4B_DEVICE_HOT_OPTIMIZER_STATE_NOT_YET_MATERIALIZED
```

and the source also rejects full-route promotion while the full route GPU row table remains unmaterialized.

## 8. Runtime receipt

Output:

```text
tensorcube_table_r4b_generation_resident_training_state_receipt.json
```

Minimum fields include:

```text
openedSourceGeneration
openedOptimizerStep
finalSourceGeneration
finalOptimizerStep

generationDirectoryMaterialized
gpuAccumulation8BindingMaterialized
deviceHotOptimizerStateMaterialized
fullRouteGpuRowTableMaterialized

tableCreateCount
generationRebindCount
perWaveTableCreateCount
perParameterTableCreateCount

optimizerStepObservationCount
accumulation8StepCount
logicalParameterCount
gradientSegmentCount
logicalAccumulatorBytesPeak

residentWeightAuthorityPresent
ramOptimizerAuthorityPresent
observedWeightSourceDiskReadBytes
productionGradientPayloadReadbackCount
fullGradientHostMaterializationCount
ordinaryStepOptimizerDiskReadBytes
ordinaryStepOptimizerDiskWriteBytes

fullModelGpuResidency
fullAdamMvGpuResidency
activeVerifiedAdmitted
proofLedger
receiptDigest
```

## 9. Production logging

Runtime emits:

```text
[ASH-TENSORCUBE-TABLE-R4B][generation-table-open]
[ASH-TENSORCUBE-TABLE-R4B][generation-table]
```

The final log binds actual accumulation coverage and current storage/residency attribution.

## 10. No new WGPU execution path

The R4B directory module contains no:

```text
map_async
queue.submit
create_shader_module
create_compute_pipeline
wgpu::Buffer payload owner
Vec<f32> tensor payload
```

The first bake changes ownership/authority binding only and reuses existing production compute.

## 11. Parent preservation

Preserved unchanged:

```text
R4A-CF2-CF1 direct candidate arena path
R4A-CF2 producer authority
R4A-CF1 shared successor consumer
R4A multi-chunk authority
R3 bounded scheduler
R2A compaction
R6A-R1 accumulation math
RAM Adam M/V semantics
persistent weight-pack semantics
B06
BP-DK
R3C/R3C1 commit
```

## 12. Static qualification

Current results:

```text
R4B       58/58 PASS
R4A-CF2-CF1 90/90 PASS
R4A-CF2   40/40 PASS
R4A-CF1   90/90 PASS
R4A       66/66 PASS
R3-CF1    51/51 PASS
R3        PASS
R2A       PASS
R2        PASS
R1        PASS
```

Modified Rust delimiter sanity:

```text
PASS
```

Python validator compile:

```text
PASS
```

## 13. Parent baseline drift attribution

The supplied code-only parent omits historical qualification-only files required by two validators:

```text
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c_r27r1j_r6a_r1_contract.args

tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
```

Therefore R6A-R1 and RAM-Adam validators stop at those missing prerequisites on both parent and R4B.

Persistent-weight validator reproduces the same pre-existing:

```text
66/67
candidate successor direct immutable promotion
```

failure on the unmodified CF2-CF1 parent. It is not attributed to R4B.

## 14. Exact implementation delta

Compared with the supplied CF2-CF1 full parent:

```text
MOD 2
ADD 2
DEL 0
```

Modified:

```text
crates/base_train/src/lib.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
```

Added:

```text
crates/base_train/src/tensorcube_table_r4b_generation_resident_training_state.rs
tools/validate_ash_tensorcube_table_r4b_generation_resident_training_state_static.py
```

## 15. Source SHA-256

```text
bce86164934eaa2b8fff8cf934e732d79a99fb9b78f623566690257b54436b61  crates/base_train/src/lib.rs
c09f308e554b26a2f644bf8b36c2913b995b9d654fe60ec0009e10e82100e765  crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
736f1d6c916c19a6b23ac3688a9e5b1c01de25f02404142e926f7a46600b700f  crates/base_train/src/tensorcube_table_r4b_generation_resident_training_state.rs
c8eb0833884de4cc2df0f2e721f6eabb6559d4c7f0ee12ac030408dc6f471e60  tools/validate_ash_tensorcube_table_r4b_generation_resident_training_state_static.py
```

## 16. Artifact seal

```text
Overlay ZIP
SHA-256 6340eeec8379c09257f52f7ad40fc6abb98377e9cf0175c5b911e83154a392f7
files 4
CRC PASS

Full code-only ZIP
SHA-256 f2587b48667eeb4585ca47a6ec444d29efa2a98ca3c4eea7a44b4578608b271e
files 8,499
CRC PASS
```

## 17. Evidence boundary

```text
SOURCE       PASS
STATIC       PASS
ARCHIVE      PASS
COMPILE      NOT RUN
RUNTIME      NOT RUN
PHYSICAL     NOT RUN
PERFORMANCE  UNMEASURED
PROMOTED     NO
```

No compile/runtime/physical/performance claim is made by this bake environment.

## 18. Compile acceptance

```powershell
cargo test -p base_train --lib tensorcube_table_r4b_ --release --locked
cargo test -p base_train --lib tensorcube_table_r4a_cf2_cf1_ --release --locked
cargo test -p base_train --lib tensorcube_table_r4a_cf2_ --release --locked
cargo test -p base_train --lib tensorcube_table_r4a_cf1_ --release --locked
cargo build -p base_train --bin base_train --release --locked
```

## 19. ObserveOnly physical acceptance

Run with:

```text
ASH_TENSORCUBE_TABLE_R4B_MODE=OBSERVE_ONLY
```

Required first evidence:

```text
tableCreateCount = 1
perWaveTableCreateCount = 0
perParameterTableCreateCount = 0
optimizerStepObservationCount > 0
accumulation8StepCount == optimizerStepObservationCount
logicalParameterCount = 201
productionGradientPayloadReadbackCount = 0
fullGradientHostMaterializationCount = 0
generationRebindCount == optimizerStepObservationCount
```

When persistent weight and RAM Adam authorities are admitted:

```text
residentWeightAuthorityPresent = true
ramOptimizerAuthorityPresent = true
```

Observed disk-byte fields remain measurements and are not hardcoded.

## 20. Direct successor

Exact next child:

```text
TENSORCUBE-TABLE-R4B-CF1

DEVICE-HOT OPTIMIZER PAGE BINDING
+ ADAM M/V RAM→GPU PREFETCH
+ GPU ACCUMULATOR DIRECT ADAMW CONSUMPTION
+ DIRTY M/V GPU→RAM CIRCULATION
+ ROUTE-SCOPED TENSORCUBE ROW TABLE
+ ACTIVE_VERIFIED PROMOTION
```

## 21. Final law

> R4B begins the ownership cutover from a scheduling-only TensorCube Table to a generation-resident training-state directory.
>
> The first source materialization binds the real accumulation8 GPU authority, the real persistent-weight authority, the real RAM optimizer authority and the committed generation progression under one generation-lifetime runtime.
>
> It does not falsely claim that Adam M/V are already device-hot or that every optimizer route is already a GPU TensorCube row.
>
> ActiveVerified remains fail-closed until those physical authorities are materialized.
