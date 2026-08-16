# `ASH-BASETRAIN-FFN-TENSORCUBE-PHYSICAL-PERF-HARNESS-AND-BASELINE-CAPTURE-R1`

## Status

```text
Patch ID
ASH-BASETRAIN-FFN-TENSORCUBE-PHYSICAL-PERF-HARNESS-AND-BASELINE-CAPTURE-R1

Build revision
basetrain-ffn-tensorcube-physical-perf-harness-and-baseline-capture-r1

Parent
ASH-BASETRAIN-FFN-TENSORCUBE-GPU-TIMESTAMP-AND-RESOURCE-CHURN-PERF-GUARD-R1

Execution role
Dedicated physical FFN performance harness and baseline-capture surface

Production FFN implementation
unchanged
```

This revision does not change the FFN kernel, resource-lifetime policy, texture-content eligibility, optimizer, checkpoint state, Down projection or backward math. It adds a dedicated executable that invokes the exact existing `BaseTrainFfnTensorCubePersistentExecutor` and drains the parent GPU timestamp ticket explicitly between measured invocations.

---

## 1. Core authority

The harness measures the production executor. It does not implement a benchmark-only FFN.

```text
benchmark execution path
=
BaseTrainFfnTensorCubePersistentExecutor::execute(...)
```

The harness may generate deterministic synthetic input and Gate/Up payloads for standalone physical GPU validation, but this payload source is explicitly classified and is not silently promoted to production-model-weight authority.

---

## 2. Weight-source classification

```rust
FfnPerfWeightSourceKind::DeterministicFixtureWeights
FfnPerfWeightSourceKind::ProductionModelWeights
```

The baked standalone harness currently executes:

```text
DeterministicFixtureWeights
```

Therefore:

```text
productionBaselineEligible = false
```

The result is a physical production-executor baseline with deterministic payloads, not a production-model-weight optimization decision authority.

A future production-weight-backed caller may use the ABI distinction without rewriting the meaning of the standalone receipt.

---

## 3. Binary

```text
crates/base_train/src/bin/
ash_basetrain_ffn_tensorcube_physical_perf_harness_r1.rs
```

Cargo binary:

```text
ash_basetrain_ffn_tensorcube_physical_perf_harness_r1
```

Default runtime artifact path:

```text
workspace/runtime/basetrain/ffn/perf/
ffn_tensorcube_physical_perf_baseline_r1.json
```

Runtime artifacts are not included in baked code ZIPs.

---

## 4. Parent production implementation preservation

R1 does not add a new FFN WGSL file.

The parent remains authoritative for:

```text
one persistent Gate/Up RGBA32F texture slot
exact FfnTextureContentKey
same-allocation texture repopulation
static texture bind-group reuse
dynamic source/input/tape bind-group lifetime
@workgroup_size(64)
16x16x16 fused geometry
integer textureLoad
exact SiLU
four training-tape outputs
existing Down
existing backward
```

---

## 5. Deterministic fixture contract

Default geometry:

```text
hidden       = 2048
intermediate = 5632
seed         = 160
```

Deterministic values are generated from:

```text
index
seed
salt
```

No runtime-random seed is introduced.

The standalone harness creates two independent physical Gate/Up weight pairs:

```text
WeightPair A
WeightPair B
```

with distinct raw primitive/stream identities so source-identity miss behavior can be exercised physically.

---

## 6. Required sequence matrix

```text
seq_len =
1
15
16
17
31
32
33
64
128
```

Required batch matrix:

```text
batch = 1
batch = 2
```

The full sequence/batch matrix is exercised for `WarmContentHit` under both:

```text
Forward
BackwardRecompute
```

consumer classifications.

Transition classes are measured separately on the canonical configurable geometry, default:

```text
batch   = 1
seq_len = 32
```

This keeps transition attribution isolated while preserving the full 16-row boundary sweep for steady-state fused timing.

---

## 7. Consumer classification

The harness preserves parent consumer identity:

```rust
FfnPerfConsumerKind::Forward
FfnPerfConsumerKind::BackwardRecompute
```

Forward and backward-recompute warm-hit baselines are stored under distinct baseline identities.

---

## 8. Execution classes

The harness physically exercises:

```text
ColdExecutor
WarmContentHit
WarmContentMiss
LayerTransition
GenerationTransition
```

and includes a dedicated:

```text
SourceIdentityDriftNegativeControl
```

receipt.

---

## 9. ColdExecutor fixture

Each cold sample constructs a fresh `BaseTrainFfnTensorCubePersistentExecutor`, then performs one exact production execution and explicit timestamp drain.

Default:

```text
coldIterations = 3
```

Cold samples therefore retain parent resource receipt evidence for:

```text
pipeline slab build
texture allocation
texture-view creation
static bind-group creation
uniform creation
initial population
```

Cold data is stored separately from warm steady-state aggregates.

---

## 10. WarmContentHit fixture

A fresh executor is first primed with the exact content key. Subsequent measured calls keep:

```text
same layer
same source weight generation
same Gate identity
same Up identity
same tensor set
same packing
```

Expected measured invariants:

```text
executionClass = WarmContentHit
textureContentHit = true
texturePopulationExecuted = false
textureCreateCount = 0
textureViewCreateCount = 0
staticBindGroupCreateCount = 0
hotPathBlockingPollCount = 0
```

---

## 11. WarmContentMiss fixture

The harness alternates WeightPair A and WeightPair B while keeping:

```text
layer unchanged
generation unchanged
```

Expected:

```text
executionClass = WarmContentMiss
textureContentHit = false
texturePopulationExecuted = true
textureCreateCount = 0
```

This proves content-key source identity participates in physical eligibility.

---

## 12. LayerTransition fixture

The harness alternates:

```text
layer 0
layer 1
```

while keeping the same physical weight pair and generation.

Expected:

```text
executionClass = LayerTransition
texture allocation retained
population executed
textureCreateCount = 0
```

---

## 13. GenerationTransition fixture

The harness alternates:

```text
Generation 1 + WeightPair A
Generation 2 + WeightPair B
```

at the same layer.

Expected:

```text
executionClass = GenerationTransition
texture allocation retained
population executed
textureCreateCount = 0
```

This standalone transition is deterministic-fixture evidence. It is not labeled as a real optimizer successor generation.

---

## 14. Source identity drift negative control

A dedicated control performs:

```text
same layer
same generation
WeightPair A -> WeightPair B
```

Required receipt:

```text
generationUnchanged = true
layerUnchanged = true
sourceIdentityChanged = true
executionClass = WarmContentMiss
textureContentHit = false
texturePopulationExecuted = true
pass = true
```

This prevents generation number equality from becoming a hidden cache-hit shortcut.

---

## 15. Timestamp ticket ordering

The harness uses the parent one-outstanding-ticket contract exactly:

```text
execute
-> timestamp ticket
-> collect_pending_perf_sample_blocking(ticket)
-> next execute
```

The blocking drain belongs to the dedicated harness boundary only.

No blocking timing drain is added to the production hot path.

---

## 16. Timestamp unsupported behavior

When the device does not provide parent timestamp support:

```text
timestampCapability = Unsupported or Unknown
fusedGpuNs = None
populationGpuNs = None
disposition = InsufficientEvidence
```

Host encode/submit/lock timings remain host fields and are not substituted into GPU fields.

---

## 17. Warmup and measured windows

Defaults:

```text
warmup  = 5
measured = 20
```

Warmup samples are retained in raw receipts with:

```text
warmup = true
```

but are excluded from statistical aggregates.

The warmup count is never silent.

---

## 18. Raw samples

Every invocation records a `FfnPhysicalPerfSample` including:

```text
fixture digest
baseline identity digest
scenario
consumer kind
execution class
layer
source weight generation
batch / seq / token count
content-key digest
HIT/MISS state
population execution state
timestamp capability/ticket
population GPU ns when physically executed
fused GPU ns when collected
whole texture-path GPU ns
host encode/submit/lock wait ns
resource creation/reuse counters
production/resource receipt PASS state
sample digest
```

Raw samples are preserved in the runtime baseline artifact.

---

## 19. Aggregate statistics

The harness reuses the parent aggregation helper and records, per exact baseline identity:

```text
minimum
median
mean
p95
maximum
```

for fused GPU duration.

Population GPU statistics are independently aggregated only for samples where population physically executed.

Warm HIT therefore retains:

```text
population aggregate = None
```

rather than fabricating a 0-ns population timing.

---

## 20. Baseline identity

Each aggregate is bound to:

```text
patch revision
model-source digest
tensor-set digest
device identity digest
hidden
intermediate
batch
seq_len
consumer kind
scenario
weight-source kind
```

Cross-device, cross-shape and cross-consumer samples are not merged into one baseline identity.

---

## 21. Device identity

The physical artifact seals adapter-visible identity including:

```text
name
vendor
device id
device type
backend
driver
driver info
```

into a device digest.

A baseline from another device is not silently treated as the same baseline.

---

## 22. Resource churn evidence

Aggregates preserve raw parent counters for:

```text
pipeline slab build/reuse
texture create
texture-view create
static bind-group create/reuse
dynamic population bind-group create
dynamic fused bind-group create
uniform-buffer create
uniform writes
blocking device polls
content hits/misses
population dispatches/skips
```

This is measurement of actual parent receipts, not inferred reuse percentages.

---

## 23. Canonical non-finite check

After a canonical production-executor invocation, the harness runs a diagnostic GPU scan over:

```text
gate_pre
silu_gate
up_linear
ffn_product
```

The diagnostic shader uses F32 exponent-bit classification:

```text
(bitcast<u32>(value) & 0x7f800000) == 0x7f800000
```

rather than `isNan`/`isInf` builtins.

Only one diagnostic `u32` non-finite counter is read back.

Required:

```text
canonicalNonfiniteCount = 0
```

The output tensor payload itself is not read back for this check.

---

## 24. Optimization recommendation boundary

R1 defines the recommendation ABI but does not automatically select a production optimization.

Current standalone behavior:

```text
recommendation = InsufficientEvidence
evidenceSufficientForAutomaticOptimizationSelection = false
```

Reason:

```text
deterministic fixture weights validate the exact physical executor and timing surface,
but do not become production-model-weight optimization decision authority.
```

The user's/operator's review remains the next-patch selection authority.

---

## 25. No mutation counters

Top-level artifact seals:

```text
parentMathMutationCount = 0
parentResidencyPolicyMutationCount = 0
optimizerMutationCount = 0
checkpointMutationCount = 0
```

No benchmark run commits model or optimizer state.

---

## 26. Static validator

New:

```text
tools/
validate_basetrain_ffn_tensorcube_physical_perf_harness_and_baseline_capture_r1_static.py
```

Current baked result:

```text
72 / 72 PASS
```

It verifies at minimum:

```text
exact persistent production executor use
explicit execute -> timestamp-drain ordering
no alternate FFN WGSL
all execution-class fixtures
source-identity negative control
exact seq/batch matrices
5 warmup / 20 measured defaults
Forward and BackwardRecompute separation
raw sample preservation
min/median/mean/p95/max aggregation
device/model/geometry/generation/content identity
no host timer substitution
resource-churn assertions
GPU finite counter check
no optimizer/checkpoint/math/residency mutation
parent exact SiLU/workgroup/textureLoad/single-slot contracts
```

---

## 27. Parent regressions

Current baked static results:

```text
Physical Perf Harness R1
72 / 72 PASS

GPU Timestamp and Resource Churn Perf Guard R1
101 / 101 PASS

Persistent Resource Slab R1
66 / 66 PASS

16x16x16 Fused Production R1
45 / 45 PASS

Local Muon PAD17
52 / 52 PASS
```

---

## 28. Compile and physical status

The bake environment does not provide:

```text
cargo
rustc
rustfmt
physical WGPU device execution
```

Therefore this bake does not claim:

```text
Rust compile PASS
physical timestamp PASS
physical baseline numbers
GPU speedup
```

Those remain the user's local runtime authority.

---

## 29. Local compile/static validation

```powershell
cd D:\1111113232\DUST\1\ash_pass3

cargo fmt --all -- --check
cargo check -p burn_webgpu_backend --release
cargo check -p model_core --release
cargo check -p base_train --release

python tools\validate_basetrain_ffn_tensorcube_physical_perf_harness_and_baseline_capture_r1_static.py
python tools\validate_basetrain_ffn_tensorcube_gpu_timestamp_and_resource_churn_perf_guard_r1_static.py
python tools\validate_basetrain_ffn_tensorcube_persistent_resource_slab_and_bindgroup_reuse_r1_static.py
python tools\validate_basetrain_ffn_tensorcube_16x16x16_gate_up_swiglu_fused_production_r1_static.py
python tools\validate_tensorcube_local_muon_x_pad17_workgroup_bank_conflict_reduction_r1_static.py
```

---

## 30. Physical harness command

```powershell
cargo run --release `
  -p base_train `
  --bin ash_basetrain_ffn_tensorcube_physical_perf_harness_r1
```

Optional explicit receipt location:

```powershell
cargo run --release `
  -p base_train `
  --bin ash_basetrain_ffn_tensorcube_physical_perf_harness_r1 -- `
  --receipt-path workspace\runtime\basetrain\ffn\perf\ffn_tensorcube_physical_perf_baseline_r1.json
```

N8 is not part of this patch.

---

## 31. Packaging closure

Current baked package changes exactly three source/validation files:

```text
crates/base_train/Cargo.toml
crates/base_train/src/bin/ash_basetrain_ffn_tensorcube_physical_perf_harness_r1.rs
tools/validate_basetrain_ffn_tensorcube_physical_perf_harness_and_baseline_capture_r1_static.py
```

Current archives:

```text
full body files = 7038
overlay files   = 3
```

Excluded from ZIP:

```text
*.md
*.sha256
*manifest*.json
*artifact*.json
*report*.json
runtime perf baseline JSON
```

Both ZIPs passed archive integrity verification.

---

## 32. Next decision boundary

After the physical harness is run on the user's GPU, the next optimization must be selected from the actual artifact.

Candidate directions remain:

```text
population-heavy + frequent layer misses
-> multi-slot texture residency review

warm-hit fused stage dominant
-> fused-kernel fetch/input-staging review

host dynamic binding dominant
-> dynamic binding slab/lease reuse review

measured texture path no longer dominant
-> Down projection timestamp attribution
```

R1 itself does not choose among them.

---

## Final seal

```text
The parent put a clock inside the production FFN.
This revision creates the controlled room in which that clock is read.

The harness does not invent another FFN.
It invokes the persistent production executor itself.

Cold is kept separate from warm.
HIT is kept separate from MISS.
Layer transition is kept separate from generation transition.
Forward is kept separate from backward recomputation.
Seq 15, 16 and 17 are not blended together, nor are 31, 32 and 33.

Every GPU timing ticket is drained explicitly before another ticket is requested.
A stage that does not execute has no fake 0-ns GPU duration.
A device without timestamp evidence gets InsufficientEvidence, not a CPU number wearing a GPU label.

Standalone deterministic weights are honest physical fixtures.
They are not silently renamed production model weights.

The output tensors are checked for non-finite values on the GPU and only a four-byte diagnostic counter is returned.

No optimizer state changes.
No checkpoint changes.
No kernel changes.
No residency-policy changes.

The result is a physical baseline surface.
The next optimization remains an operator decision made after reading that surface.
```
