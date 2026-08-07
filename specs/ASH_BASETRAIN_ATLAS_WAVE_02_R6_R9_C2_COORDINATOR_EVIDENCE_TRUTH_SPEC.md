# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C2

## Coordinator Evidence Truth / Child Receipt Digest Binding / Actual Dispatch Count Aggregation / Runtime Geometry-Derived Compared Scalar Count / Source·Target Weight Pointer Provenance / Input·Output Hidden Pointer Provenance / Weight·Hidden Generation Lineage / Per-Step Completion Digest / No Arithmetic Synthetic Execution Truth / Atlas Parallel Receipt Wave Preservation Seal

> Parent physical SSOT: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C1-D3` physical PASS  
> Route: BaseTrain FullPrefill  
> Scope: evidence ownership and coordinator truth promotion only  
> Decoder-weight transport algorithm: unchanged  
> Layer-2 execution algorithm: unchanged  
> Atlas parallel artifact wave map: preserved  
> Full N-layer execution: `BLOCKED`  
> Final RMSNorm / LM head: `BLOCKED`  
> Forward loss / backward / optimizer / production inference: `BLOCKED`  
> Proof ledger: `HOLD` until C2 physical PASS

## Parent physical state

The admitted parent chain has physically proven:

```text
R6-R6 live body = PASS
R6-R7 layer weight 0 -> 1 residency = PASS
R6-R8 hidden 1 -> 2 layer-1 forward = PASS
R6-R9-C1-D3 layer-2 single-step = PASS
checkpoint layers = 22
weight layer 1 -> 2
authority generation 1 -> 2
hidden layer 2 -> 3
hidden generation 2 -> 3
completed steps = 1
auto continue = 0
payload readback = 0
```

C2 does not re-prove that Layer 2 can execute. C2 changes what the coordinator is allowed to call truth about that execution.

## Evidence SSOT

```text
live authority snapshots and typed runtime receipts
  -> typed per-layer execution evidence
  -> child final receipt bound to execution-evidence digest
  -> R6-R9 per-step completion evidence
  -> coordinator final aggregate
  -> terminal log
```

Expected values may validate observations, but expected values may not become observations.

Weight authority remains `BaseTrainLayerWeightResidencySlot`. Hidden authority remains `LayerHiddenAuthoritySlot`. Layer execution evidence is captured inside `execute_resident_decoder_layer_from_session()`. Coordinator aggregate truth is derived only from sealed per-step evidence.

## R6-R5 shared runtime dispatch evidence

`execute_r6_r5_shared_runtime_prefill_context()` returns a typed `R6R5SharedRuntimeDispatchEvidence` built from physical W5/W6/W7 receipts before ownership moves destroy direct access to intermediate bundles.

Required evidence includes:

```text
W5/W6/W7 receipt digests
Stage10 q-tile / candidate / oracle / compare dispatch counts
Stage11 candidate / oracle / compare dispatch counts
Stage12 candidate / oracle / normalize-verify dispatch counts
chunk count
q-tile count
context element count
payload readback count
mismatch count
non-finite count
pass
evidence digest
```

Shared and deterministic replay invocation evidence remain distinct and carry independent digests.

## R6-R8 typed layer execution evidence

The generalized resident-layer executor exposes `R6R8LayerExecutionEvidence` containing:

```text
selected layer
checkpoint set digest
weight execution pointer digest / generation / transition serial
actual decoder block identity digest
input hidden pointer / generation / buffer identity / completion token / BQH shape
QKV dispatch evidence
shared attention dispatch evidence
replay attention dispatch evidence
selected continuation dispatch evidence
final parity evidence
output hidden pointer / generation / buffer identity / completion token / BQH shape
payload readback count
pass
evidence digest
```

QKV evidence is copied from `ActualQkvPreparationReceipt`. Continuation evidence is copied from `LiveDecoderBlockContinuationReceipt`. W5/W6/W7 evidence is copied from their actual typed runtime receipts.

The child final R6-R8 receipt binds:

```text
executionEvidenceDigest = R6R8LayerExecutionEvidence.evidence_digest
legacyFlatStageSummaryAuthority = RETIRED
```

Legacy flat `stage10Count`, `stage11Count`, `stage12Count` may temporarily remain inside R6-R8 compatibility receipts, but R6-R9 C2 must not use them for admission or aggregation.

## Runtime geometry truth

Compared scalar count is derived from authoritative hidden BQH geometry:

```text
runtimeGeometryComparedScalarCount = B * Q * H
```

Multiplication is checked for overflow. Required equality:

```text
input hidden BQH == output hidden BQH
QKV input shape == input hidden BQH
continuation final hidden shape == output hidden BQH
runtimeGeometryComparedScalarCount == child parity observedComparedScalarCount
```

Fixed `65536` is not an R6-R9 C2 factual authority.

## Pointer and generation provenance

Coordinator captures live snapshots before and after the transaction.

Required weight lineage:

```text
source weight pointer = live source slot snapshot
target weight pointer = live post-adoption slot snapshot
target layer = source layer + 1
target generation = source generation + 1
target transition serial > source transition serial
child weight execution pointer == target weight pointer
child decoder block identity == target pointer block identity
```

Required hidden lineage:

```text
input hidden pointer = live pre-rebind hidden snapshot
post-rebind hidden pointer == input hidden pointer
output hidden layer = input layer + 1
output hidden generation = input generation + 1
output.previousPointerDigest == input.pointerDigest
child input hidden evidence == coordinator input snapshot
child output hidden evidence == coordinator output snapshot
```

## Actual dispatch aggregate

`R6R9ActualDispatchAggregate` contains only observed receipt-derived counters:

```text
input norm
Q/K/V projection
Stage10 q-tile / candidate / oracle / compare
Stage11 candidate / oracle / compare
Stage12 candidate / oracle / normalize-verify
OProj
attention residual add
post-attention RMSNorm
gate / up / SiLU multiply / down
FFN residual add
payload readback
aggregate digest
```

Where shared and replay validation routes both contribute, totals are checked sums of the two observed typed evidences. No field is calculated from `completed_step_count * constant`.

Selected output authority and validation evidence are named separately:

```text
selectedDecoderPath = shared-runtime live hidden writer
validationReplayPath = deterministic replay evidence only
referenceOraclePath = Headwise reference evidence only
```

## Per-step completion evidence

`R6R9StepCompletionEvidence` binds:

```text
source weight pointer lineage
target weight pointer lineage
input hidden pointer lineage
output hidden pointer lineage
child final receipt digest
child execution evidence digest
runtime geometry compared scalar count
observed compared scalar count
actual dispatch digest
payload readback count
pass
completion digest
```

Canonical digest ordering is source weight -> target weight -> input hidden -> child evidence -> child receipt -> output hidden -> runtime geometry -> actual dispatch -> completion digest.

## Atlas parallel receipt wave preservation

R6-R9 artifact construction continues to use `AtlasParallelStreamingWaveMap`. Monolithic `serde_json::json!` artifact construction and recursion-limit increases are forbidden.

Transaction receipt layout:

```text
wave 0 identity-and-parent
wave 1 weight-provenance
wave 2 hidden-provenance
wave 3 runtime-truth
wave 4 completion
```

Final receipt and manifest are also assembled through deterministic parallel lane construction and streaming wave merge:

```text
wave ordinal -> lane ordinal -> lexicographic key
```

Duplicate keys, lane collisions, worker failures and ordinal mismatch fail closed.

## CLI policy

C1 single-step window remains unchanged and C2 adds:

```text
--require-r6-r9-evidence-truth true
--allow-r6-r9-synthetic-execution-counts false
--require-r6-r9-child-evidence-binding true
--require-r6-r9-runtime-geometry-count true
```

These are policy assertions, not alternate modes.

## Changed implementation surface

Semantic changes:

```text
crates/model_core/src/base_train_atlas_wave_02_r6_r5_body_splice.rs
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r8_layer1_live_body.rs
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r9_forward_coordinator.rs
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r6_r9_forward_coordinator_gate.rs
specs/cli/ash_basetrain_atlas_wave_02_r6_r9.args
```

The D3 binary-local distribution closure is preserved in the overlay so R6-R7/R6-R8 authority and loader surfaces cannot silently drift behind the coordinator.

No WGSL semantic change is introduced.

## Static bake validation

```text
C2 patch/build revision = present
R6R5SharedRuntimeDispatchEvidence = present
R6R8LayerExecutionEvidence = present
R6R9StepCompletionEvidence = present
R6R9ActualDispatchAggregate = present
child final receipt executionEvidenceDigest binding = present
coordinator child evidence digest validation = present
live source/target weight pointer capture = present
live input/output hidden pointer capture = present
weight generation lineage check = present
hidden generation lineage check = present
hidden previous-pointer lineage check = present
runtime BQH checked scalar product = present
fixed 65536 factual authority in R6-R9 = 0
expected_steps fixed-dispatch factual authority = 0
legacy stage10Count/stage11Count/stage12Count coordinator reads = 0
R6-R9 json! artifact construction sites = 0
recursion_limit workaround = 0
AtlasParallelStreamingWaveMap transaction/final/manifest = present
Rust lexical delimiter scan = PASS
WGSL semantic changed files = 0
```

Cargo/rustc are not available in the bake environment. Cargo type-check and physical WGPU execution remain operator-side gates.

## Physical command

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r9_forward_coordinator_gate `
  -- "@specs/cli/ash_basetrain_atlas_wave_02_r6_r9.args"
```

## Physical PASS requirements

```text
checkpoint layer count observed = 22 for current profile
completed step count = 1
source/target weight pointer lineage valid
input/output hidden pointer lineage valid
child execution evidence digest bound to child final receipt
QKV counts sourced from ActualQkvPreparationReceipt
W5/W6/W7 counts sourced from actual typed receipts
continuation counts sourced from LiveDecoderBlockContinuationReceipt
runtime geometry scalar count == child parity compared scalar count
mismatch count = 0
non-finite count = 0
payload product readback count = 0
step completion digest present
final coordinator receipt digest present
Atlas parallel wave-map construction PASS
```

## Admission matrix

```text
R6-R6 live body                         = ADMITTED by parent physical PASS
R6-R7 layer-weight residency            = ADMITTED by parent physical PASS
R6-R8 layer-1 forward                   = ADMITTED by parent physical PASS
R6-R9-C1 Layer-2 single-step            = ADMITTED by parent physical PASS
R6-R9-C2 coordinator evidence truth     = ADMITTED only on C2 physical PASS
R6-R9 full N-layer execution            = BLOCKED
Wave domain authority split             = BLOCKED / C3
DecoderWeightAtlasWave                  = BLOCKED / C4
LayerWeightBuildStagingSlot             = BLOCKED / C5
final norm / LM head                    = BLOCKED
forward loss / backward / optimizer     = BLOCKED
production inference                    = BLOCKED
proof ledger                            = HOLD
```

## Next boundary

```text
ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C3

Wave Domain Authority Split /
Artifact Receipt Wave Naming Isolation /
Embedding Row Micro-Atlas Wave Naming Isolation /
Decoder Weight Atlas Wave Reserved Authority /
No Cross-Domain PASS Borrowing /
No Ambiguous wave SSOT Seal
```

> C2 allows the coordinator to validate expectations, but forbids it from manufacturing observations: every execution count, geometry value, pointer, generation and completion digest must descend from live typed runtime evidence and remain bound through the child receipt into the per-step coordinator receipt.
