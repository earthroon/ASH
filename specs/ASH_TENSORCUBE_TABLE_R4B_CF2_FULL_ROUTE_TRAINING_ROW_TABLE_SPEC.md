# TENSORCUBE-TABLE-R4B-CF2

## FULL ROUTE TRAINING ROW TABLE
## + ADAMW / HIMUON UNIFIED GENERATION VIEW
## + WEIGHT / GRADIENT / OPTIMIZER RESIDENCY MATRIX
## + SINGLE PARAMETER COMPLETION PLANE
## + GENERATION COMMIT-READY TABLE

## 0. Revision

```text
Patch ID:
TENSORCUBE-TABLE-R4B-CF2

Canonical name:
ASH-BASETRAIN-TENSORCUBE-TABLE-R4B-CF2-
FULL-ROUTE-TRAINING-ROW-TABLE-
UNIFIED-GENERATION-VIEW-
SINGLE-PARAMETER-COMPLETION-
COMMIT-READY-TABLE

Direct parent:
TENSORCUBE-TABLE-R4B-CF1
```

Class:

```text
GENERATION STATE UNIFICATION
+ ROUTE COVERAGE
+ COMMIT READINESS PROJECTION

NO ADAM MATH CHANGE
NO HIMUON MATH CHANGE
NO OPTIMIZER ROUTING CHANGE
NO GENERATION COMMIT AUTHORITY CHANGE
```

## 1. Parent authorities preserved

CF2 consumes without redefining:

```text
TENSORCUBE-TABLE-R4B generation-resident directory
TENSORCUBE-TABLE-R4B-CF1 device-hot Adam execution
TENSORCUBE-TABLE-R4A-CF2-CF1 direct HiMuon shared-arena path
FirstCandidateEligibilityRegistry
optimizer_routing_digest
R6DeviceGradientAccumulator
MuonDeviceSegmentedGenerationR1
AdamWDeviceSegmentedGenerationR1
FullTrainableCoverageReceipt
FullModelDeviceCommitPermit
R3B Eve CandidateComplete
TrainableSubmissionEpochUnionR3C
FullTrainableGenerationCommitPermitR3C
R3C1 no-fail production cutover
```

## 2. Source closure in this bake

This source bake materially adds:

```text
one generation-lifetime typed full-route table
HiMuon TensorCube rows from the verified first-candidate registry
AdamW route-span rows from the same routing registry
exact target-device completion projection
single parameter completion plane
full-generation coverage reduction
generation commit-ready view
R3C prepare parity observation
R4B parent child-materialization gate closure
```

The Table remains evidence/readiness authority. It never performs trainable-generation commit.

## 3. Canonical routing SSOT

No new optimizer classifier is introduced.

Canonical route authority remains:

```text
FirstCandidateEligibilityRegistry
optimizer_routing_digest
FirstCandidateParameterRoute
ProductionMuonRuntime routing semantics
```

At Table construction the exact routing digest and registry digest are sealed into the generation runtime.

Required source registry invariants:

```text
overlap_element_count = 0
unclassified_element_count = 0
muon_eligible_element_count + adamw_element_count
    = total_trainable_element_count
```

## 4. Typed row model

Materialized enum:

```text
TrainingRowKindR4BCF2

HiMuonTensorCube
AdamWRouteSpan
```

HiMuon rows preserve canonical TensorCube geometry.

AdamW rows preserve contiguous canonical AdamW route spans. They are not assigned fake TensorCube identities.

Physical AdamW scheduler segments are recorded separately as completion evidence because one canonical route span may be split into several bounded physical segments.

## 5. HiMuon row construction

For every admitted Muon grid:

```text
one 16x16 TensorCube = one HiMuon Table row
```

Rows are derived using the existing registry tile resolver.

Stored row identity includes:

```text
canonical parameter index
TensorCube execution ordinal
logical top-left element offset
logical element count = 256
```

No second TensorCube geometry calculator is introduced.

## 6. AdamW route-span construction

AdamW rows are derived from the exact same routing geometry used by production route-span decisions.

For pure AdamW parameters:

```text
one full parameter route span
```

For mixed parameters:

```text
Muon 16x16 regions remain HiMuon rows
right-edge / tail residual regions become AdamW route-span rows
```

Required:

```text
route span length > 0
AdamW route range may never cross a Muon-owned interval
```

## 7. Full route row identity

The generation Table therefore contains:

```text
TOTAL TRAINING ROWS
= HiMuon TensorCube rows
+ AdamW route-span rows
```

Table row ordinal is a physical metadata coordinate only.

Semantic identities remain route-specific.

## 8. Residency matrix

Each row carries explicit runtime residency state for:

```text
source Weight
gradient
optimizer source state
candidate Weight
candidate optimizer state
```

Materialized states include:

```text
NotApplicable
NotPresent
RamResident
DeviceHot
DeviceInFlight
CandidateDeviceHot
CandidateRamResident
Terminal
Failed
```

No payload bytes are stored inside the metadata Table.

## 9. Generation identity

One CF2 runtime binds:

```text
source training generation G
target training generation G+1
source optimizer step S
target optimizer step S+1
optimizer routing digest
registry digest
```

The same Table row geometry is rebound after a successful generation commit.

## 10. Target device generation binding

CF2 observes the actual:

```text
FullTrainableDeviceGenerationR1
```

before R3C1 consumes its ownership.

Required:

```text
target generation exact
FullTrainableCoverageReceipt complete
overlap = 0
unclassified = 0
duplicate writes = 0
missing = 0
```

## 11. HiMuon physical completion projection

CF2 consumes the real Muon generation publication receipt and exact per-parameter descriptors.

For every parameter:

```text
published Muon element count
== registry expected Muon element count
```

When exact, every expected HiMuon TensorCube row for that parameter may become route-complete.

CF2 does not infer HiMuon completion merely from chunk submission.

## 12. AdamW physical completion projection

`AdamWDeviceSegmentedGenerationR1` gains a read-only projection:

```text
segment_ranges_r4b_cf2()
```

It exposes only:

```text
canonical parameter index
element start
element count
```

It does not transfer candidate ownership.

Every observed physical Adam range must lie entirely within the registry's AdamW route domain.

Per-parameter actual AdamW element coverage must equal registry AdamW element coverage exactly.

## 13. Physical Adam segmentation versus logical Table rows

CF2 explicitly distinguishes:

```text
AdamWRouteSpan
= canonical routing row

AdamW physical segment
= bounded scheduler execution partition
```

Receipt tracks both:

```text
expected_adamw_route_spans
completed_adamw_route_spans
actual_adamw_physical_segments
```

This avoids redefining route identity from current stream-chunk geometry.

## 14. Real accumulation parent

CF2 reuses the existing real `R6DeviceAccumulatorReceipt`.

Required:

```text
microbatch_count = 8
accumulator_dtype = F32
production_gradient_payload_readback_count = 0
full_gradient_host_materialization_count = 0
```

No second gradient accumulator is created.

## 15. Adam device-hot parent

CF2 preserves the R4B-CF1 ActiveDevice Adam path.

AdamW rows therefore observe:

```text
source optimizer execution residency = DeviceHot
candidate optimizer state = bounded RAM candidate after R3B
```

Full Adam M/V permanent GPU residency remains false.

## 16. HiMuon optimizer state parent

HiMuon rows retain the existing HiMuon momentum/update authority.

CF2 records its residency state but does not reinterpret HiMuon momentum as Adam M/V.

## 17. Single parameter completion plane

Materialized:

```text
ParameterCompletionR4BCF2
```

Fields include:

```text
expected / completed HiMuon rows
expected / completed AdamW route spans
actual AdamW physical segments
expected / completed Muon elements
expected / completed AdamW elements
failed row count
route coverage complete
candidate Weight complete
optimizer state complete
parameter terminal
```

## 18. Mixed-parameter completion

For one mixed parameter:

```text
parameter_terminal
=
exact Muon completion
AND exact AdamW completion
AND Muon + AdamW element coverage == parameter element count
AND candidate Weight complete
AND route-required optimizer state complete
AND failed_row_count == 0
```

Neither optimizer route may terminate the whole parameter independently.

## 19. Pure-route completion

For pure HiMuon parameters:

```text
expected AdamW route spans = 0
```

For pure AdamW parameters:

```text
expected HiMuon rows = 0
```

Zero expected work is vacuously complete. No fake optimizer work is synthesized.

## 20. Full generation completion reduction

The parameter plane reduces into generation coverage:

```text
terminal parameter count
failed parameter count
expected trainable elements
completed trainable elements
Muon expected/completed elements
AdamW expected/completed elements
```

Required successful coverage:

```text
completed trainable elements = expected trainable elements
failed parameter count = 0
pending required rows = 0
```

## 21. Existing FullTrainableCoverage reuse

CF2 stores the actual `FullTrainableCoverageReceipt` from the existing target device generation.

It does not synthesize a competing external full-trainable coverage authority.

At commit time the stored receipt is carried into the CF2 step receipt.

## 22. Generation commit-ready view

Materialized:

```text
GenerationCommitReadyR4BCF2
```

Commit-ready requires all of:

```text
all Table parameters terminal
no failed parameters
no pending required rows
full trainable coverage complete
Eve R3B CandidateComplete
HiMuon target coverage complete
Weight successor prepared
B06 active-device permit ready
exact target SubmissionEpoch union nonempty and duplicate-free
```

## 23. Table does not commit

Hard source constant:

```text
TENSORCUBE_TABLE_R4B_CF2_TABLE_DIRECT_COMMIT_AUTHORITY = false
```

Runtime receipt includes:

```text
table_direct_commit_attempt_count = 0
```

The new module contains no call to the R3C committed-state mutation function.

## 24. R3C prepare parity

After Table commit-ready calculation, production still calls the existing:

```text
prepare_full_trainable_generation_commit_r3c(...)
```

CF2 records whether R3C preparation admits the same target.

Successful ActiveVerified relation:

```text
Table generation_commit_ready = true
R3C prepare admitted = true
```

If R3C rejects a Table-ready state, CF2 fails closed. R3C is not weakened.

## 25. R3C1 no-fail tail preserved

R4B-CF2 does not replace the R3C1 mutation tail.

The final committed generation still comes from the existing R3C/R3C1 authority chain.

No Table scan, hashing, route reconstruction, GPU poll or filesystem operation is inserted into the no-fail mutation tail.

## 26. R3C attempt-before-ready firewall

CF2 records:

```text
r3c_prepare_attempt_before_table_ready
```

ActiveVerified requires:

```text
r3c_prepare_attempt_before_table_ready = 0
```

## 27. Generation rebind

After successful canonical generation commit:

```text
source G := G+1
optimizer S := S+1
```

The same generation runtime resets mutable row completion/residency state while retaining route geometry.

No per-wave or per-parameter Table reconstruction is introduced.

## 28. R4B parent gate closure

Historical R4B constants remain unchanged:

```text
TENSORCUBE_TABLE_R4B_DEVICE_HOT_OPTIMIZER_STATE_MATERIALIZED = false
TENSORCUBE_TABLE_R4B_FULL_ROUTE_GPU_ROW_TABLE_MATERIALIZED = false
```

R4B now recognizes ActiveVerified child revision admission through:

```text
ASH_TENSORCUBE_TABLE_R4B_CF1_MODE
ASH_TENSORCUBE_TABLE_R4B_CF2_MODE
```

This preserves historical revision truth while allowing the child lineage to close the parent gate.

## 29. R4B-CF1 child preservation

Historical CF1 full-route HOLD token remains source history.

When CF2 child mode is ActiveVerified, CF1 reports physical-pending rather than pretending the full-route child is still absent.

## 30. Activation

Modes:

```text
ASH_TENSORCUBE_TABLE_R4B_CF2_MODE=OFF
ASH_TENSORCUBE_TABLE_R4B_CF2_MODE=OBSERVE_ONLY
ASH_TENSORCUBE_TABLE_R4B_CF2_MODE=ACTIVE_VERIFIED
```

CF2 enabled requires R4B enabled.

CF2 ActiveVerified additionally requires:

```text
R4B ActiveVerified
R4B-CF1 ActiveVerified
routing registry bound
R3C/R3C1 production path present
```

## 31. ObserveOnly behavior

ObserveOnly constructs the typed full-route Table and compares real execution/commit evidence.

It does not execute AdamW or HiMuon a second time.

It does not alter the existing generation commit decision.

## 32. ActiveVerified behavior

ActiveVerified makes CF2 the canonical runtime readiness directory.

Authority split remains:

```text
R4B-CF2 = readiness SSOT
R3C/R3C1 = commit authority
```

## 33. Runtime receipt

Output:

```text
tensorcube_table_r4b_cf2_full_route_training_row_table_receipt.json
```

Log:

```text
[ASH-TENSORCUBE-TABLE-R4B-CF2][route-table-open]
[ASH-TENSORCUBE-TABLE-R4B-CF2][commit-ready]
```

Receipt includes:

```text
routing digest
registry digest
parameter count
full Table row count
HiMuon row count
AdamW route-span count
Muon/AdamW element counts
generation rebind count
observed generation count
commit-ready count
R3C attempt/admission counts
early-R3C attempt count
direct commit attempt count
```

## 34. Static materialization

New source:

```text
crates/base_train/src/tensorcube_table_r4b_cf2_full_route_training_table.rs
```

New validator:

```text
tools/validate_ash_tensorcube_table_r4b_cf2_full_route_training_table_static.py
```

Current static result:

```text
118 / 118 PASS
PASS_TENSORCUBE_TABLE_R4B_CF2_FULL_ROUTE_TRAINING_ROW_TABLE_UNIFIED_GENERATION_VIEW_STATIC
```

## 35. Parent regression

Current bake retains:

```text
R4B                 58 / 58 PASS
R4B-CF1             77 / 77 PASS
R4A-CF2-CF1         90 / 90 PASS
R4A-CF2             40 / 40 PASS
R4A-CF1             90 / 90 PASS
Full-device successor static PASS
R3C                  18 / 18 PASS
```

R3C1 validator remains:

```text
25 / 30 PASS
```

The exact same five textual-count failures reproduce on the unmodified R4B-CF1 parent:

```text
scheduler precomputes seal
single tail Eve no-fail
single tail Muon/B06 no-fail
single tail Weight no-fail
generation seal installed last
```

Therefore this is a parent validator/source drift baseline, not an R4B-CF2 regression.

## 36. Source sanity

All modified/new Rust files pass structural balanced-delimiter checks.

The new Python validator passes `py_compile`.

The bake environment exposes no Cargo/Rustc toolchain, so Rust compile PASS is not claimed.

## 37. Exact implementation delta

Compared with the supplied R4B-CF1 full code-only parent:

```text
MOD 5
ADD 2
DEL 0
```

Modified:

```text
crates/base_train/src/lib.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/tensorcube_table_r4b_generation_resident_training_state.rs
crates/base_train/src/tensorcube_table_r4b_cf1_device_hot_optimizer_page.rs
crates/base_train/src/unified_atlas_mcu_full_model_device_segmented_successor_r1.rs
```

Added:

```text
crates/base_train/src/tensorcube_table_r4b_cf2_full_route_training_table.rs
tools/validate_ash_tensorcube_table_r4b_cf2_full_route_training_table_static.py
```

## 38. Artifact seal

```text
Overlay ZIP
SHA-256 25683319efb975900d48c36b8a10c5309bbf2f7ab9c64e152b0b21c14cd721b9
files 7
CRC PASS

Full code-only ZIP
SHA-256 2e45d651dd3179690a25e7bbdceb04a372bbed50c4c68212e35cc1219357030f
files 8,503
CRC PASS
```

## 39. Evidence boundary

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

## 40. Compile acceptance

```powershell
cargo test `
  -p base_train `
  --lib tensorcube_table_r4b_cf2_ `
  --release `
  --locked

cargo test `
  -p base_train `
  --lib tensorcube_table_r4b_cf1_ `
  --release `
  --locked

cargo test `
  -p base_train `
  --lib tensorcube_table_r4b_ `
  --release `
  --locked

cargo test `
  -p base_train `
  --lib eve_himuon_full_trainable_generation_commit_ `
  --release `
  --locked

cargo build `
  -p base_train `
  --bin base_train `
  --release `
  --locked
```

## 41. First physical campaign

First campaign should use ObserveOnly:

```powershell
$env:ASH_TENSORCUBE_TABLE_R4B_MODE="OBSERVE_ONLY"
$env:ASH_TENSORCUBE_TABLE_R4B_CF1_MODE="OBSERVE_ONLY"
$env:ASH_TENSORCUBE_TABLE_R4B_CF2_MODE="OBSERVE_ONLY"
```

Required observation:

```text
parameter_count > 0
HiMuon row count > 0
AdamW route-span count > 0
Muon element count > 0
AdamW element count > 0
route overlap = 0
route gap = 0
completed trainable elements = expected trainable elements
all parameters terminal
Table commit-ready = true
R3C prepare admitted = true
Table direct commit attempt = 0
```

## 42. ActiveVerified physical qualification

After ObserveOnly parity:

```powershell
$env:ASH_TENSORCUBE_TABLE_R4B_MODE="ACTIVE_VERIFIED"
$env:ASH_TENSORCUBE_TABLE_R4B_CF1_MODE="ACTIVE_VERIFIED"
$env:ASH_TENSORCUBE_TABLE_R4B_CF2_MODE="ACTIVE_VERIFIED"
```

Physical PASS requires at least:

```text
real HiMuon route coverage > 0
real AdamW route coverage > 0
exact parameter coverage
no route gaps/overlap
no failed parameters
no pending required rows
exact B06 coverage
exact R3B CandidateComplete
exact Weight successor readiness
exact SubmissionEpoch union
Table generation commit-ready = true
R3C prepare admitted = true
R3C1 final trainable generation seal installed
partial generation observations = 0
```

## 43. Reserved physical token

```text
PASS_TENSORCUBE_TABLE_R4B_CF2_FULL_ROUTE_TRAINING_ROW_TABLE_UNIFIED_GENERATION_VIEW_PHYSICAL
```

Until a real run proves it:

```text
HOLD_TENSORCUBE_TABLE_R4B_CF2_FULL_ROUTE_TRAINING_ROW_TABLE_PHYSICAL_PENDING
```

## 44. Non-goals

CF2 does not claim:

```text
full model permanent VRAM residency
full Adam M/V permanent VRAM residency
zero PCIe traffic
GPU-driven cross-wave refill
new optimizer routing
new generation commit system
new checkpoint format
cross-device training
```

## 45. Direct successor

After physical closure:

```text
TENSORCUBE-TABLE-R4C

CROSS-WAVE COMPUTE / TRANSFER OVERLAP
+ DEVICE-DRIVEN RESIDENCY REFILL
+ NO GLOBAL WAVE WAIT
+ CURRENT / NEXT / NEXT+1 TRAINING PIPELINE
```

## 46. Final law

> R4B created the generation-lifetime training-state directory.
>
> R4B-CF1 bound actual device-hot Adam execution into that directory.
>
> R4B-CF2 unifies AdamW and HiMuon routing, residency and completion into one typed generation view while preserving their distinct semantic identities.
>
> Parameter completion becomes a single exact plane over both routes.
>
> Generation readiness becomes one compact view over exact parameter coverage, Eve CandidateComplete, HiMuon target completion, Weight successor readiness, B06 coverage and SubmissionEpoch lineage.
>
> The Table may prove that a generation is ready.
>
> The Table may not commit that generation.
>
> R3C remains the permit authority and R3C1 remains the no-fail committed-state mutation authority.
