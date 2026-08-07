# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C1

## Layer-2 Single-Step Canary / Checkpoint-Resolved First Target Layer / Max Layer Step Clamp / Weight-1 Eviction / Weight-2 Adoption / Hidden-2 Consumption / Actual Layer-2 RMSNorm·QKV·W5·W6·W7·OProj·MLP / Hidden-3 Single Commit / Final Weight Generation Two / Final Hidden Generation Three / No Full-Stack Auto-Run / No Re-Embedding / No Payload Readback / Production Inference·Backward·Optimizer Blocked / Proof Ledger HOLD Seal

> Parent contract: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R8-C2` physical closure  
> Working code parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9` checkpoint-resolved N-layer coordinator candidate  
> Route: BaseTrain FullPrefill  
> Scope: coordinator execution-window restriction and single-step evidence closure only  
> Decoder weight wave transport: **NOT introduced in C1**  
> Production inference: `BLOCKED`  
> Final norm / LM head: `BLOCKED`  
> Forward loss: `BLOCKED`  
> Backward / optimizer: `BLOCKED`  
> Proof ledger: `HOLD` until physical canary PASS

---

# 0. SSOT

C1 keeps the existing ownership split unchanged.

```text
resident decoder-weight authority
  = BaseTrainLayerWeightResidencySlot

hidden-state authority
  = LayerHiddenAuthoritySlot

execution ordering authority
  = R6-R9 forward coordinator
```

The coordinator owns **ordering only**. It must not become a second owner of a decoder block or hidden tensor.

C1 does not introduce `LayerWeightBuildStagingSlot` or `DecoderWeightAtlasWavePlan`; those are later boundaries.

---

# 1. Observed parent behavior

The working R6-R9 candidate currently executes:

```rust
for target_layer in 2..layer_count {
    // rebind target layer
    // execute target layer
    // commit target_layer + 1 hidden
}
```

Therefore a single invocation may continue from target layer 2 through the last decoder layer.

The same candidate also emits a final receipt whose end state assumes full-stack completion:

```text
final weight layer = checkpoint layer count - 1
final hidden layer = checkpoint layer count
r6r9 step count = checkpoint layer count - 2
```

That behavior is too broad for the first physical R6-R9 admission boundary.

C1 must preserve the reusable coordinator structure while restricting the physical gate to exactly one decoder-layer transaction.

---

# 2. Goal

C1 admits only this state transition:

```text
START
  weight slot = Resident(layer=1, generation=1)
  hidden slot = layer=2, generation=2

STEP 0
  target layer = 2

  weight layer 1
    -> arm eviction
    -> remove source block
    -> VacantForRebind
    -> load/build existing checkpoint-resolved layer-2 block
    -> adopt layer 2

  hidden layer 2
    -> acquire normal execution authority through existing R6-R8 executor
    -> execute actual decoder layer 2
    -> commit hidden layer 3 exactly once

END
  weight slot = Resident(layer=2, generation=2)
  hidden slot = layer=3, generation=3
  completed R6-R9 steps = 1
  automatic target-layer-3 execution = 0
```

C1 is a **canary**. It is not an N-layer forward-stack admission.

---

# 3. Non-goals

The following are explicitly outside C1.

```text
DecoderWeightAtlasWavePlan                     = deferred to R6-R9-C4
parallel decoder-weight checkpoint decode      = deferred to R6-R9-C4
private incomplete-block staging authority     = deferred to R6-R9-C5
weight-wave-only rebind canary                  = deferred to R6-R9-C6
legacy-vs-wave numerical parity                 = deferred to R6-R9-C7
canonical wave-loader promotion                 = deferred to R6-R9-C8
multi-layer promotion                           = deferred to R6-R9-C9
long-horizon residency ledger                   = deferred to R6-R9-C10
child receipt truth aggregation redesign        = deferred to R6-R9-C2
wave-domain naming split                        = deferred to R6-R9-C3
final RMSNorm / LM head                         = blocked
forward loss                                    = blocked
backward                                        = blocked
optimizer                                       = blocked
production inference                            = blocked
```

C1 continues to use the currently existing checkpoint-resolved decoder-block rebind path. It must not disguise that loader as the future decoder-weight wave loader.

---

# 4. Parent admission boundary

R6-R9-C1 may execute only from an R6-R8 parent session satisfying:

```text
parent weight layer = 1
parent weight generation = 1
parent resident decoder block count = 1
parent resident checkpoint weight tensor count = 9
parent weight active execution leases = 0

parent hidden layer = 2
parent hidden generation = 2
parent hidden active execution leases = 0

parent layer-2 hidden committed = true
parent receipt digest = present
parent manifest digest = present
parent payload readback count = 0
```

The physical release of C1 additionally requires the operator to have admitted the R6-R8-C2 physical parent contract.

If parent physical evidence is absent, C1 code may exist and compile, but:

```text
C1 physical admission = HOLD
proof ledger = HOLD
```

No copied receipt or metadata-only parent state substitutes for the same-process R6-R8 execution chain.

---

# 5. Checkpoint geometry precondition

Layer 2 must physically exist.

Replace the current weak boundary:

```text
num_hidden_layers >= 2
```

with the C1 requirement:

```text
num_hidden_layers >= 3
```

because C1 targets decoder layer index `2` and publishes hidden layer index `3`.

Required checks:

```text
first_target_layer < num_hidden_layers
first_target_layer == 2
max_layer_steps == 1
expected_final_weight_layer == 2
expected_final_hidden_layer == 3
```

The checkpoint remains the source of truth for total layer count. C1 does not hardcode a total decoder depth.

---

# 6. C1 execution-window contract

Add an explicit execution-window value owned by the coordinator configuration surface.

Recommended shape:

```rust
pub struct R6R9ExecutionWindow {
    pub first_target_layer: u32,
    pub max_layer_steps: u32,
    pub expected_final_weight_layer: u32,
    pub expected_final_hidden_layer: u32,
}
```

For C1, parsing is fail-closed and the only admitted values are:

```text
first_target_layer = 2
max_layer_steps = 1
expected_final_weight_layer = 2
expected_final_hidden_layer = 3
```

A caller cannot use the C1 gate as a hidden N-layer gate by passing a larger value.

Forbidden C1 values:

```text
first_target_layer != 2
max_layer_steps != 1
expected_final_weight_layer != 2
expected_final_hidden_layer != 3
```

Suggested failure classes:

```text
R6R9C1FirstTargetLayerNotTwo
R6R9C1MaxLayerStepsNotOne
R6R9C1ExpectedFinalWeightLayerNotTwo
R6R9C1ExpectedFinalHiddenLayerNotThree
R6R9C1CheckpointHasNoLayerTwo
```

---

# 7. Coordinator loop restriction

The generalized coordinator logic is retained, but the C1 gate must derive a bounded target range from the sealed execution window.

Equivalent admitted behavior:

```rust
let first_target_layer = window.first_target_layer;
let last_target_exclusive = first_target_layer
    .checked_add(window.max_layer_steps)
    .ok_or_else(|| anyhow!("R6R9C1TargetWindowOverflow"))?;

ensure!(last_target_exclusive <= layer_count, "R6R9C1TargetWindowExceedsCheckpoint");

for target_layer in first_target_layer..last_target_exclusive {
    // existing rebind -> execute -> hidden commit transaction
}
```

For C1 this resolves exactly to:

```text
2..3
```

Required result:

```text
target layer 2 execution count = 1
target layer 3+ execution count = 0
completed step count = 1
```

The pre-C1 unbounded active gate behavior:

```rust
for target_layer in 2..layer_count
```

must no longer be the execution range used by the C1 physical gate.

Do not delete the coordinator abstraction merely to force one layer. The restriction belongs to the execution window, not to a duplicated Layer-2-only decoder body.

---

# 8. Layer-2 rebind transaction

C1 reuses the existing `rebind_resident_decoder_layer(...)` path.

Required input:

```text
source layer = 1
source residency generation = 1
target layer = 2
input hidden layer = 2
input hidden generation = 2
source completion digest = R6-R8 final receipt digest
```

Required ordering:

```text
verify source slot Resident(layer=1)
  -> verify active weight execution lease count = 0
  -> verify sole slot-owned complete block
  -> arm layer-1 eviction toward target layer 2
  -> take/drop layer-1 bundle
  -> device.poll(PollType::Wait)
  -> mark VacantForRebind
  -> load/build existing checkpoint-resolved layer-2 block
  -> adopt target layer 2 into same residency slot
  -> residency generation 1 -> 2
```

Required post-rebind state before decoder execution:

```text
weight state = Resident
resident weight layer = 2
weight residency generation = 2
resident complete decoder block count = 1
resident checkpoint weight tensor count = 9
weight active execution lease count = 0
hidden layer = 2
hidden generation = 2
```

The hidden pointer must not advance as a side effect of weight rebind.

---

# 9. Actual layer-2 execution

C1 then invokes the existing generalized resident-layer executor with:

```text
selected layer = 2
input hidden layer = 2
expected output hidden layer = 3
```

The active decoder body remains the R6-R8 generalized execution path:

```text
hidden 2
  -> actual input RMSNorm
  -> single Q projection
  -> single K projection
  -> single V projection
  -> NeoX RoPE
  -> Headwise shared W5 Stage10
  -> Headwise shared W6 Stage11
  -> Headwise shared W7 Stage12
  -> actual OProj
  -> attention residual
  -> post-attention RMSNorm
  -> actual SwiGLU gate/up/SiLU/down
  -> FFN residual
  -> hidden 3 candidate
  -> hidden 3 single authority commit
```

C1 does not create a second Layer-2 implementation.

Required direct execution facts:

```text
re-embedding count = 0
weight reload during execute count = 0
block rebuild during execute count = 0
layer execution count = 1
hidden commit count = 1
payload readback count = 0
```

Detailed per-stage child dispatch aggregation is not promoted to C1 coordinator truth. R6-R9-C2 owns that redesign.

---

# 10. Final authority state

After successful C1 execution:

```text
weight state = Resident
final weight layer = 2
final weight generation = 2
resident complete decoder block count = 1
resident checkpoint weight tensor count = 9
weight active execution lease count = 0

final hidden layer = 3
final hidden generation = 3
hidden active execution lease count = 0

completed C1 step count = 1
next-layer auto continuation count = 0
payload readback count = 0
```

The gate must explicitly reject the old full-stack final conditions.

C1 must **not** require:

```text
final weight layer = num_hidden_layers - 1
final hidden layer = num_hidden_layers
completed steps = num_hidden_layers - 2
```

Those conditions belong only to later N-layer promotion.

---

# 11. C1 receipt truth boundary

C1 must stop publishing a receipt that can be mistaken for successful N-layer completion.

Recommended final receipt:

```text
00_r6_r9_c1_layer2_single_step_final.json
```

Minimum authoritative fields:

```text
patchId = ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C1
buildRevision
checkpointLayerCount
executionMode = layer2-single-step-canary
firstTargetLayer = 2
maxLayerSteps = 1
attemptedStepCount = 1
completedStepCount = 1

sourceWeightLayer = 1
sourceWeightGeneration = 1
targetWeightLayer = 2
targetWeightGeneration = 2

inputHiddenLayer = 2
inputHiddenGeneration = 2
outputHiddenLayer = 3
outputHiddenGeneration = 3

weightEvictionCount = 1
weightAdoptionCount = 1
actualLayerExecutionCount = 1
hiddenCommitCount = 1
nextLayerAutoContinuationCount = 0

reembeddingCount = 0
allLayerPayloadPreloadCount = 0
nextLayerPrefetchCount = 0
payloadReadbackCount = 0

peakResidentDecoderBlockCount = 1
peakResidentCheckpointWeightTensorCount = 9
peakDecodedPayloadLayerCount = 1

parentReceiptDigest = <R6-R8 final receipt digest>
layer2ExecutionReceiptDigest = <child final receipt digest>

productionInferenceAdmission = BLOCKED
finalNormLmHeadAdmission = BLOCKED
forwardLossAdmission = BLOCKED
backwardAdmission = BLOCKED
optimizerAdmission = BLOCKED
proofLedger = HOLD
pass = true
receiptDigest = ...
```

C1 may additionally publish start/end pointer digests already available from authority snapshots, but it must not invent synthetic per-stage counts.

Specifically, the C1 coordinator final receipt must not derive factual execution fields from expressions such as:

```text
expected_steps * 2
expected_steps * 4
65,536 * expected_steps
```

C1 does **not** need to fully aggregate child stage receipts yet. Instead it carries the child receipt digest as evidence, and R6-R9-C2 performs the full evidence-truth aggregation redesign.

---

# 12. Per-step canary receipt

Exactly one R6-R9 transaction receipt is allowed.

Recommended artifact:

```text
01_layer2_single_step_transaction.json
```

Required fields:

```text
stepOrdinal = 0
sourceLayer = 1
targetLayer = 2
sourceWeightGeneration = 1
targetWeightGeneration = 2
inputHiddenLayer = 2
inputHiddenGeneration = 2
outputHiddenLayer = 3
outputHiddenGeneration = 3
reembeddingCount = 0
weightReloadDuringExecuteCount = 0
blockRebuildDuringExecuteCount = 0
payloadReadbackCount = 0
childReceiptDigest = present
pass = true
receiptDigest = present
```

There must be no second transaction receipt for target layer 3.

---

# 13. Manifest

Recommended manifest:

```text
ash_basetrain_atlas_wave_02_r6_r9_c1_local_manifest.json
```

Minimum fields:

```text
patchId
buildRevision
executionMode = layer2-single-step-canary
checkpointLayerCount
firstTargetLayer = 2
maxLayerSteps = 1
completedStepCount = 1
finalWeightLayer = 2
finalHiddenLayer = 3
finalReceiptDigest
transactionReceiptDigest
proofLedger = HOLD
pass = true
receiptDigest
```

The manifest must not describe itself as a checkpoint-resolved full decoder stack.

---

# 14. Output directory

Replace the misleading full-stack output identity for the C1 physical gate.

Recommended:

```text
workspace/runtime/basetrain/atlas_wave/02/r6_r9/c1-layer2-single-step-canary-v1
```

Layer-local child output remains isolated beneath the C1 directory, for example:

```text
.../layer_0002/
```

C1 must not produce `layer_0003/` or any later target-layer execution directory.

---

# 15. CLI additions

Add to:

```text
specs/cli/ash_basetrain_atlas_wave_02_r6_r9.args
```

Required C1 values:

```text
--r6-r9-first-target-layer
2

--r6-r9-max-layer-steps
1

--r6-r9-expected-final-weight-layer
2

--r6-r9-expected-final-hidden-layer
3

--require-r6-r9-single-step-canary
true

--allow-r6-r9-auto-continue
false
```

Update:

```text
--r6-r9-output-dir
workspace/runtime/basetrain/atlas_wave/02/r6_r9/c1-layer2-single-step-canary-v1
```

No CLI value may silently default to a full N-layer execution window.

---

# 16. Failure atomicity

## 16.1 Failure before eviction is armed

State remains:

```text
weight = Resident(layer=1, generation=1)
hidden = layer=2, generation=2
layer2 execution count = 0
hidden3 commit count = 0
```

## 16.2 Failure after destructive vacancy but before target adoption

State becomes:

```text
weight = RecoveryRequired
hidden = layer=2, generation=2
layer2 execution count = 0
hidden3 commit count = 0
```

Forbidden:

```text
same-invocation layer-1 reconstruction
silent source rollback
Headwise fallback as replacement decoder block
continue to target layer 3
```

## 16.3 Failure after layer-2 adoption but before hidden-3 commit

State remains explicit:

```text
weight = Resident(layer=2, generation=2)
hidden = layer=2, generation=2
hidden3 commit count = 0
next-layer auto continuation count = 0
```

Do not reconstruct layer 1 merely to make the invocation appear atomic.

## 16.4 Failure after hidden-3 authority commit

If receipt publication or manifest writing fails after the authority commit:

```text
weight = Resident(layer=2, generation=2)
hidden = layer=3, generation=3
proof ledger = HOLD
```

Do not silently roll hidden authority back to layer 2.

Authority truth and proof publication truth are separate.

---

# 17. Forbidden behavior

```text
full decoder-stack auto-run from the C1 gate
max_layer_steps > 1
first_target_layer other than 2
implicit continuation to target layer 3+
all-layer checkpoint preload
next-layer prefetch
source/target complete block simultaneous residency
re-embedding between R6-R8 and layer-2 execution
layer-2 weight reload during decoder execution
layer-2 block rebuild during decoder execution
same-invocation legacy fallback after destructive vacancy
partial hidden-3 commit
payload readback used to prove the production path
production inference promotion
final RMSNorm / LM head execution
forward loss
backward
optimizer
checkpoint mutation
weight mutation
synthetic full-stack PASS receipt
```

---

# 18. Preserved behavior

C1 must preserve:

```text
same-process R6-R6 -> R6-R7 -> R6-R8 -> R6-R9 lineage
same native WGPU device / queue lineage
BaseTrainLayerWeightResidencySlot ownership
LayerHiddenAuthoritySlot ownership
existing generation-sealed rebind transaction
existing RecoveryRequired failure state
existing generalized resident decoder-layer executor
actual checkpoint-backed layer-2 weights
actual RMSNorm / QKV / OProj / MLP execution
shared Headwise W5 / W6 / W7 route
GPU completion before lease release where already required
no silent fallback
no backward / optimizer
```

No WGSL semantic change is required by C1.

---

# 19. Expected changed files

Semantic changes are expected in:

```text
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r9_forward_coordinator.rs
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r6_r9_forward_coordinator_gate.rs
specs/cli/ash_basetrain_atlas_wave_02_r6_r9.args
```

The gate source may remain structurally tiny; it should nevertheless bind the C1 revision/entrypoint explicitly so a pre-C1 full-stack coordinator cannot masquerade as the C1 gate.

No required C1 change to:

```text
crates/base_train decoder-weight loader implementation
model_core weight residency state machine
LayerHiddenAuthoritySlot API
Headwise WGSL
TensorCube WGSL
checkpoint format
```

If implementation reveals one of those must change merely to compile, treat it as a separate closure patch rather than silently widening C1.

---

# 20. Revision identity

Recommended constants:

```rust
pub const BASETRAIN_ATLAS_WAVE_02_R6_R9_C1_PATCH_ID: &str =
    "ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C1";

pub const BASETRAIN_ATLAS_WAVE_02_R6_R9_C1_BUILD_REVISION: &str =
    "r6-r9-c1-layer2-single-step-canary-v1";
```

The old R6-R9 N-layer candidate revision must not be printed as the C1 physical revision.

---

# 21. Static validation contract

Minimum bake-side checks:

```text
C1 patch ID present = true
C1 build revision present = true
execution window struct or equivalent explicit bound = present
first target layer required = 2
max layer steps required = 1
expected final weight layer = 2
expected final hidden layer = 3
checkpoint minimum hidden layer count = 3
C1 active target range resolves to 2..3
active unbounded `2..layer_count` gate range = 0
completed-step success requirement = 1
final weight layer success requirement = 2
final weight generation success requirement = 2
final hidden layer success requirement = 3
final hidden generation success requirement = 3
next-layer auto continuation count = 0
C1 layer_0003 execution directory creation path = 0
full-stack final-state requirement in C1 = 0
synthetic aggregate `expected_steps * ...` factual receipt fields = 0
fixed 65,536 * expected_steps aggregate claim = 0
reembedding count = 0
all-layer preload = 0
next-layer prefetch = 0
payload readback = 0
production inference = BLOCKED
backward = BLOCKED
optimizer = BLOCKED
WGSL semantic changed file count = 0
.sha256 sidecar count in distributed code ZIP = 0
Rust delimiter scan = PASS
```

Static validation does not imply Cargo type-check or physical WGPU PASS.

---

# 22. Physical commands

```powershell
cargo clean `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  -p model_core `
  -p base_train `
  -p orchestrator_local
```

```powershell
cargo check `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r9_forward_coordinator_gate
```

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r9_forward_coordinator_gate `
  -- "@specs/cli/ash_basetrain_atlas_wave_02_r6_r9.args"
```

---

# 23. Terminal log contract

Recommended terminal line:

```text
[r6-r9-c1-layer2-canary] checkpoint_layers=<N> first_target=2 max_steps=1 completed_steps=1 source_weight_layer=1 target_weight_layer=2 weight_generation=1->2 input_hidden_layer=2 output_hidden_layer=3 hidden_generation=2->3 weight_eviction=1 weight_adoption=1 layer_execute=1 hidden_commit=1 auto_continue=0 peak_resident_blocks=1 peak_resident_weight_tensors=9 peak_decoded_layers=1 all_layer_preload=0 prefetch=0 reembedding=0 weight_lease_after=0 hidden_lease_after=0 payload_readback=0 proof_ledger=HOLD
```

The terminal line must not claim final-decoder-stack completion.

---

# 24. PASS token

```text
PASS_ASH_BASETRAIN_ATLAS_WAVE_02_R6_R9_C1_LAYER2_SINGLE_STEP_CANARY_R6_R8_C2_PHYSICAL_PARENT_SAME_PROCESS_WEIGHT_LAYER1_GENERATION1_HIDDEN_LAYER2_GENERATION2_EXPLICIT_FIRST_TARGET_LAYER2_MAX_LAYER_STEPS_ONE_CHECKPOINT_LAYER2_PRESENT_LAYER1_WEIGHT_EVICTION_ONCE_LAYER2_CHECKPOINT_RESOLVED_WEIGHT_ADOPTION_ONCE_WEIGHT_GENERATION_ONE_TO_TWO_HIDDEN2_CONSUMPTION_ACTUAL_LAYER2_RMSNORM_QKV_SHARED_W5_W6_W7_OPROJ_SWIGLU_MLP_HIDDEN3_SINGLE_COMMIT_HIDDEN_GENERATION_TWO_TO_THREE_FINAL_WEIGHT_LAYER2_FINAL_HIDDEN_LAYER3_AUTO_CONTINUATION_ZERO_PEAK_RESIDENT_BLOCK_ONE_PEAK_RESIDENT_WEIGHT_TENSORS_NINE_NO_ALL_LAYER_PRELOAD_NO_NEXT_LAYER_PREFETCH_NO_REEMBEDDING_NO_SAME_INVOCATION_FALLBACK_ZERO_PAYLOAD_READBACK_PRODUCTION_INFERENCE_FINAL_NORM_LM_HEAD_FORWARD_LOSS_BACKWARD_OPTIMIZER_BLOCKED_PROOF_LEDGER_HOLD_SEALED
```

The token is emitted only after all C1 authority and count checks pass.

---

# 25. Admission matrix

```text
R6-R8-C2 physical parent                         = REQUIRED / separately admitted
R6-R9-C1 layer-2 single-step canary              = ADMITTED only on physical PASS
R6-R9 coordinator full N-layer execution         = BLOCKED
DecoderWeightAtlasWave transport                 = BLOCKED / C4
LayerWeightBuildStagingSlot                      = BLOCKED / C5
wave-built layer-2 rebind                        = BLOCKED / C6
wave-loader numerical execution parity           = BLOCKED / C7
canonical wave-loader adoption                   = BLOCKED / C8
progressive N-layer promotion                    = BLOCKED / C9
long-horizon residency ledger                    = BLOCKED / C10
final norm / LM head                             = BLOCKED
forward loss                                     = BLOCKED
backward                                         = BLOCKED
optimizer                                        = BLOCKED
production inference                             = BLOCKED
proof ledger                                     = HOLD
```

---

# 26. Exit criteria

C1 closes only when a physical run proves all of the following in one invocation:

```text
same-process parent chain reaches R6-R8 successfully
checkpoint contains decoder layer 2
C1 execution window is exactly target layer 2 / one step
layer-1 complete weight block is evicted once
layer-2 complete weight block is adopted once
weight residency generation advances 1 -> 2
hidden 2 remains unchanged through rebind
actual layer-2 decoder body executes once
hidden 3 is committed exactly once
hidden generation advances 2 -> 3
final weight layer = 2
final hidden layer = 3
weight active lease count = 0
hidden active lease count = 0
resident complete block count = 1
resident checkpoint weight tensor count = 9
automatic layer-3 execution = 0
all-layer preload = 0
next-layer prefetch = 0
reembedding = 0
payload readback = 0
no silent fallback
no authority rollback
```

---

# 27. Next boundary

After C1 physical closure, proceed to:

```text
ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C2

Coordinator Evidence Truth /
Child Receipt Digest Binding /
Actual Dispatch Count Aggregation /
Runtime Geometry-Derived Compared Scalar Count /
Source·Target Weight Pointer Provenance /
Input·Output Hidden Pointer Provenance /
No Arithmetic Synthetic Execution Truth Seal
```

C2 improves what the coordinator can truthfully prove. It does not yet introduce the decoder-weight wave transport.

---

## One-line architecture seal

> R6-R9-C1 keeps the generalized coordinator, but the physical gate may cross exactly one boundary: resident weight 1 + hidden 2 -> resident weight 2 + hidden 3, and then it must stop.
