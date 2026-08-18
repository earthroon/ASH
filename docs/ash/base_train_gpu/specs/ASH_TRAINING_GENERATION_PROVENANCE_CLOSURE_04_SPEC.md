# ASH-TRAINING-GENERATION-PROVENANCE-CLOSURE-04

## Atlas Generation Fence / Forward·Backward·Accumulator Receipt Chain / Finalized-Gradient Batch Envelope / Optimizer-Generation Binding / Parameter PRE Snapshot Projection / Generation-Audit Closure / No Per-Gradient Provenance Inflation

## 0. Status

```text
Patch ID: ASH-TRAINING-GENERATION-PROVENANCE-CLOSURE-04
Direct parent: ASH-BP-DK-GENERATION-COMPLETENESS-AUDIT-03
Authority class: TrainingDataPlane
Primary authority: Observation
Target BP-Delta-K data-plane revision: bp-dk-data-plane/active-fusion/v1
New BP-Delta-K data-plane revision: none
Policy generation ownership: none
Qualification generation ownership: none
```

Forbidden by this revision:

```text
forward mathematics change
backward mathematics change
gradient accumulation mathematics change
AdamW / HiMuon mathematics change
Fusion/Fission semantics change
optimizer commit authority change
full gradient payload readback for provenance
per-R6FinalizedGradient duplication of generation metadata
new provenance GPU allocation / shader / synchronization authority
```

## 1. Purpose

02 established parameter-local PRE source identity.

03 established generation-end BP-Delta-K completeness evidence.

04 closes the missing upstream lineage:

```text
Atlas generation fence
 -> forward execution
 -> backward execution
 -> GPU gradient accumulator
 -> finalized gradient batch
 -> optimizer generation
 -> 02 parameter PRE snapshot projection
 -> existing durable commit
 -> 03 generation completeness audit
 -> final training-generation provenance closure
```

04 does not create a new training route. It binds evidence around the already-live production route.

## 2. Central SSOT

```text
ONE TRAINING GENERATION
 -> ONE FINALIZED GRADIENT BATCH
 -> ONE OPTIMIZER TARGET GENERATION
```

`R6FinalizedGradient` remains a gradient-member transport object.

Training-generation provenance is owned at batch level rather than copied into every finalized gradient.

## 3. Atlas fence root

The upstream root is the already-existing:

```text
BaseTrainAtlasWaveGenerationFence
```

04 consumes the **bound** fence from:

```text
route.output.bound_generation_fence
```

rather than the unbound transaction fence.

The projection retains:

```text
generation fence digest
model instance ID
checkpoint digest
source weight generation
source training cursor generation
expected candidate generation fields
Atlas schedule digest
Atlas residency generation
device epoch
queue epoch
runtime binding state
```

### 3.1 Existing optimizer-generation limitation

The current production transaction producer still constructs:

```rust
source_optimizer_state_generation: 0
source_training_cursor_generation: 0
```

inside `prepare_atlas_wave_00_runtime_transaction()`.

04 does **not** silently reinterpret that legacy zero as the actual scheduler optimizer-step generation.

The field is preserved in the fence projection as:

```text
atlas_source_optimizer_state_generation
```

and remains Atlas-fence evidence only.

Actual optimizer-generation authority is separately sealed from the production scheduler:

```text
source.optimizer_step
 -> target_step
```

through `AshOptimizerGenerationGradientBinding`.

Thus:

```text
Atlas legacy optimizer-state field
!= production scheduler optimizer-step SSOT
```

## 4. Wave-resident execution evidence

`R6AR1WaveResidentStepExecution` now exports:

```text
generation_fence
forward_receipt_set_digest
backward_receipt_set_digest
finalized_gradients
accumulator_receipt
```

### Forward receipt set

Each decoder-layer/lane forward receipt contributes its existing `receipt_digest`.

The ordered set is sealed using:

```text
r6a-r1-forward-layer-set
+
bound generation fence digest
+
ordered receipt digests
```

### Backward receipt set

Decoder-layer backward receipts and logical-gradient receipts contribute their existing receipt digests.

The ordered set is sealed using:

```text
r6a-r1-backward-gradient-set
+
bound generation fence digest
+
ordered receipt digests
```

04 does not modify forward/backward numerical operations.

## 5. Finalized-gradient batch envelope

New runtime module:

```text
crates/base_train/src/training_generation_provenance_closure.rs
```

Primary pre-optimizer authority:

```text
R6FinalizedGradientBatchEnvelope
```

The envelope seals:

```text
training-generation fence projection
forward receipt-set digest
backward receipt-set digest
accumulator receipt digest
accumulated microbatch count
finalized gradient count
finalized parameter count
gradient set digest
parameter-gradient metadata seals
provenance full-gradient readback count = 0
provenance full-gradient readback bytes = 0
envelope digest
```

## 6. No per-gradient provenance inflation

`R6FinalizedGradient` in `burn_webgpu_backend` is not extended with:

```text
generation fence digest
forward/backward receipt digests
optimizer binding digest
Atlas schedule digest
commit identity
```

The same batch lineage is therefore not replicated once per parameter/segment.

## 7. Gradient member identity

04 does not hash gradient payload bytes.

Gradient member provenance uses existing metadata:

```text
parameter ID
logical shape
segment index
logical element start
element count
lease element/byte counts
buffer offset / buffer size
seam ID
vendor access path
optional primitive ID
optional stream ID
```

Raw pointer/Arc addresses are not canonical identity.

The gradient payload remains on its existing GPU path.

## 8. Accumulator evidence

The existing `R6DeviceAccumulatorReceipt` is serialized and digested as evidence.

Envelope admission requires:

```text
accumulator_receipt.pass = true
production_gradient_payload_readback_count = 0
full_gradient_host_materialization_count = 0
```

The envelope also verifies finalized parameter cardinality against the accumulator receipt.

## 9. Optimizer-generation binding

After the batch envelope is sealed, the scheduler creates:

```text
AshOptimizerGenerationGradientBinding
```

containing:

```text
gradient batch envelope digest
source training generation
target training generation
source optimizer generation
target optimizer generation
optimizer route digest
binding digest
```

The scheduler's existing generation fields are authoritative:

```text
source.generation
source.optimizer_step
target_generation
target_step
```

04 does not increment generations itself.

## 10. Optimizer route binding

For HiMuon-enabled runtime:

```text
optimizer_route_digest = ProductionMuonRuntime registry optimizer routing digest
```

For the all-AdamW route:

```text
optimizer_route_digest = deterministic all-AdamW route identity
```

When BP-Delta-K is active, 03 expected inventory must use the exact same optimizer route digest as the 04 optimizer-generation binding.

Route mismatch is a structural contradiction rather than a silent rebind.

## 11. Parameter projection into HiMuon

The full batch envelope is not threaded through every Muon API.

For each HiMuon parameter, the scheduler projects:

```text
AshTrainingGenerationParameterProjection
```

containing:

```text
parameter ID
canonical parameter index
gradient batch envelope digest
optimizer binding digest
parameter gradient digest
projection digest
```

The projection is passed to `ProductionMuonRuntime::execute_muon_parameter()`.

## 12. 02 Parameter PRE snapshot binding

After 02 seals the `AshBpDkParameterPreSnapshot`, 04 binds the parameter projection to that exact snapshot:

```text
Training Batch
 -> Parameter Gradient Projection
 -> Parameter PRE Snapshot
```

The resulting sidecar is:

```text
AshTrainingGenerationParameterSnapshotProjection
```

It seals:

```text
parameter identity
gradient batch envelope digest
optimizer binding digest
parameter gradient digest
parameter projection digest
parameter PRE snapshot digest
snapshot projection digest
```

Duplicate canonical parameter projections inside one generation are rejected.

## 13. Generation-local projection ownership

`ProductionMuonRuntime` owns the current generation's bounded sidecar vector:

```text
training_generation_parameter_snapshot_projections
```

It is cleared when:

```text
a new BP-Delta-K expected generation inventory is sealed
or
the current generation aborts
```

The sidecar does not own gradient/weight/momentum payloads.

## 14. 03 audit projection

After existing durable commit and `record_step_commit()`, 03 runs as before.

04 verifies:

```text
03 audit optimizer generation
==
04 optimizer binding target optimizer generation
```

Then the current parameter-snapshot projection set is sealed deterministically and carried into final closure evidence.

## 15. Final training-generation provenance closure

After 03 audit, 04 seals:

```text
AshTrainingGenerationProvenanceClosure
```

The closure binds:

```text
gradient batch envelope digest
optimizer binding digest
parameter snapshot projection-set digest
source/target training generations
source/target optimizer generations
existing committed training-state digest
candidate parameter-set digest
BP-Delta-K audit projection status
optional 03 audit receipt digest
provenance status
closure digest
```

The existing `trainingStateDigest` returned from `commit_active_state()` is used as commit identity evidence.

04 does not fabricate a parallel optimizer commit receipt.

## 16. Canonical execution ordering

Production ordering is:

```text
wave-resident forward/backward/accumulation
 -> finalized gradient set
 -> seal gradient batch envelope
 -> bind scheduler optimizer generation
 -> seal 03 expected BP-Delta-K inventory
 -> optimizer execution
 -> existing durable commit
 -> BP-Delta-K record_step_commit
 -> admitted resident generation promotion
 -> 03 generation completeness audit
 -> seal parameter snapshot projection-set digest
 -> seal 04 final provenance closure
```

Required inequalities:

```text
envelope seal < optimizer binding
optimizer binding < parameter optimizer execution
commit < 03 audit
03 audit < 04 final closure
```

## 17. No global barrier

04 adds no new all-parameter PRE barrier.

The gradient batch already exists before optimizer execution by definition. The envelope is sealed at that existing boundary.

02 parameter-local execution remains unchanged.

## 18. No provenance payload observation

The provenance module does not call:

```text
map_async
read_buffer
create_buffer
create_buffer_init
dispatch_workgroups
queue submit
full gradient download
```

04 also introduces no provenance shader and no new device/queue.

## 19. Deterministic identity

Canonical provenance digests exclude:

```text
wall-clock time
process/thread IDs
random UUIDs
raw pointers
Arc addresses
HashMap iteration order
```

Stable BTree-based ordering and explicit enum digest codes are used where needed.

## 20. State ownership

```text
Atlas generation fence
 -> existing training runtime

forward/backward evidence
 -> existing wave execution

accumulator receipt
 -> existing gradient accumulator

finalized gradient member
 -> existing R6 finalized-gradient runtime

batch envelope / optimizer binding / cross-plane linkage
 -> 04

optimizer target generation / durable commit
 -> existing scheduler and commit authority

parameter PRE identity
 -> 02

generation completeness
 -> 03

Fusion planning
 -> existing 05 planner

production policy selection
 -> existing control plane
```

No authority is silently moved into 04.

## 21. Lineage registry

00 registry adds:

```text
ASH-TRAINING-GENERATION-PROVENANCE-CLOSURE-04

family = training-provenance-reconciliation
authority = TrainingDataPlane / Observation
status = Active
direct parent = ASH-BP-DK-GENERATION-COMPLETENESS-AUDIT-03
runtime parent = production R6 training runtime
evidence parents = production R6 / PRE Snapshot 02 / Completeness Audit 03
```

Current training-provenance reconciliation head becomes 04.

Current production execution authorities remain unchanged.

## 22. Vocabulary binding

01 vocabulary binding:

```text
owned_data_plane_revision = None
target_data_plane_revision = bp-dk-data-plane/active-fusion/v1
owned_policy_generation = None
owned_qualification_generation = None
```

Patch suffix `04` does not imply BP-Delta-K data-plane v4.

## 23. Tooling

New validator:

```text
tools/validate_ash_training_generation_provenance_closure_04.py
```

New runner:

```text
tools/run_ash_training_generation_provenance_closure_04.ps1
```

CF1 ordering:

```text
...
21
 -> ASH-LINEAGE-RECONCILIATION-00
 -> ASH-BP-DK-LINEAGE-VOCABULARY-SEAL-01
 -> ASH-BP-DK-PARAMETER-PRE-SNAPSHOT-AUTHORITY-02
 -> ASH-BP-DK-GENERATION-COMPLETENESS-AUDIT-03
 -> ASH-TRAINING-GENERATION-PROVENANCE-CLOSURE-04
```

## 24. Baked static evidence

Final static evidence for the baked tree:

```text
ASH-LINEAGE-RECONCILIATION-00
PASS 146 / 146

ASH-BP-DK-LINEAGE-VOCABULARY-SEAL-01
PASS 306 / 306

ASH-BP-DK-PARAMETER-PRE-SNAPSHOT-AUTHORITY-02
PASS 216 / 216

ASH-BP-DK-GENERATION-COMPLETENESS-AUDIT-03
PASS 167 / 167

ASH-TRAINING-GENERATION-PROVENANCE-CLOSURE-04
PASS 198 / 198
```

Additional regression evidence:

```text
existing BP-Delta-K *_static.py validators: 25 / 25 PASS
CF1-enumerated Python static validators: 60 / 60 PASS
production multistep scheduler parent validator: 112 / 112 PASS
wave-resident parent validator: 114 / 114 PASS
TensorCube Local Muon production-callsite parent validator: 63 / 63 PASS
modified Python validators/registry: py_compile PASS
```

These are static/source results only.

## 25. Compile / physical execution boundary

The bake environment does not provide:

```text
cargo
rustc
rustfmt
pwsh
```

Therefore:

```text
Rust compile verification = EvidenceInsufficient / not executed
PowerShell runner execution = EvidenceInsufficient / not executed
physical training execution = not executed
GPU runtime evidence = not claimed
```

Static delimiter/interface/order validation is not represented as a substitute for compilation.

## 26. Parent diff boundary

Compared with the 03 full-applied parent, 04 changes exactly nine code/tool files:

```text
crates/base_train/src/lib.rs
crates/base_train/src/packed_runtime_native_bootstrap_accumulation_wave_residency.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
crates/base_train/src/training_generation_provenance_closure.rs

tools/ash_lineage_reconciliation_00_registry.py
tools/run_ash_training_generation_provenance_closure_04.ps1
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
tools/validate_ash_training_generation_provenance_closure_04.py
```

No `ash_core`, `burn_webgpu_backend`, WGSL, app, or vendor-fork source is changed by 04.

In particular, the existing `R6FinalizedGradient` definition is byte-preserved because generation provenance is batch-owned.

## 27. Packaging

Code ZIPs exclude:

```text
*.md
*.sha256
__pycache__
*.pyc
generated manifests
generated receipts
generated reports
artifact/manifests directories
```

Deliverables:

```text
Overlay Code ZIP
 -> exactly the nine parent-to-04 changed code/tool files

Full Applied Code ZIP
 -> complete 03 parent body with 04 applied
```

The GitHub Markdown spec is kept outside both code ZIPs.

## 28. Non-goals

04 does not implement:

```text
repair of the Atlas legacy optimizer-state-generation zero field
control-plane active-pointer provenance
production policy startup-binding provenance
R2 physical canary
policy recalibration
Muon runtime authority decomposition
new Fusion topology
new precision/residency planner
```

The Atlas legacy field remains visible as a known evidence limitation rather than silently corrected.

## 29. Next revision

```text
ASH-BP-DK-CONTROL-DATA-PLANE-BINDING-05
```

05 should bind:

```text
durable active policy pointer
 -> managed startup binding
 -> exact immutable policy artifact
 -> existing 05 Fusion planner execution
 -> parameter execution receipts
```

without introducing live pointer polling or mid-generation policy mutation.

## 30. Final seal

```text
ONE TRAINING GENERATION
ONE FINALIZED GRADIENT BATCH
ONE OPTIMIZER TARGET GENERATION

THE BOUND ATLAS FENCE IS THE UPSTREAM ROOT
FORWARD EVIDENCE IS BOUND
BACKWARD EVIDENCE IS BOUND
ACCUMULATOR EVIDENCE IS BOUND
GRADIENT MEMBERSHIP IS BOUND

R6FinalizedGradient REMAINS A GRADIENT MEMBER
GENERATION PROVENANCE LIVES AT BATCH LEVEL

THE LEGACY ATLAS OPTIMIZER-STATE ZERO IS NOT PROMOTED TO SCHEDULER AUTHORITY
SCHEDULER OPTIMIZER GENERATIONS ARE SEALED EXPLICITLY

NO FULL-GRADIENT D2H FOR PROVENANCE
NO PROVENANCE GPU ALLOCATION
NO PROVENANCE SHADER
NO NEW GLOBAL SYNCHRONIZATION

02 OWNS PARAMETER PRE IDENTITY
03 OWNS GENERATION COMPLETENESS
04 OWNS CROSS-PLANE TRAINING PROVENANCE

ADAMW AND HIMUON SHARE THE SAME TRAINING BATCH ROOT
A HIMUON SNAPSHOT POINTS BACK TO ITS EXACT PARAMETER GRADIENT AND BATCH
A GENERATION AUDIT POINTS BACK TO THE EXACT OPTIMIZER GENERATION

NO GENERATION IS INFERRED
NO LEGACY ZERO IS SILENTLY REINTERPRETED
NO MIXED-GENERATION BATCH IS ADMITTED

TRAINING -> GRADIENT -> OPTIMIZER -> BP-DK -> AUDIT
IS ONE TRACEABLE GENERATION LINEAGE
```
