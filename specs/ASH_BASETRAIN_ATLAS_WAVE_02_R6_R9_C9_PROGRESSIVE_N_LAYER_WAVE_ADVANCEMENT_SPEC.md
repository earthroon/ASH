# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C9

## Progressive N-Layer Wave Advancement / Canonical C8 Rebind Authority Loop / Resident Layer N Execution Lease / Hidden N+1 Commit / Canonical Wave Rebind N -> N+1 / Checkpoint Layer Count Bound / No Layer-Specific Canary Branch / No Legacy Runtime Loader / Per-Layer Generation·Pointer Lineage / Per-Step Dispatch·Parity Evidence / Zero Weight Payload Readback / Final Decoder Layer Completion Seal

> Admission parent SSOT: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C8-D1` physical PASS  
> Current decoder-weight transport authority: `decoder-weight-atlas-wave`  
> Runtime weight owner: `BaseTrainLayerWeightResidencySlot`  
> Runtime hidden owner: `LayerHiddenAuthoritySlot`  
> Planner SSOT: C4 `DecoderWeightAtlasWavePlan`  
> Staging/build SSOT: C5 `LayerWeightBuildStagingSlot`  
> Rebind transaction SSOT: C8 `rebind_resident_decoder_layer(...)`  
> Execution evidence lineage: R6-R8 typed decoder execution evidence, generalized for exact runtime pointers/generations  
> Legacy generalized runtime loader: `RETIRED`  
> Final RMSNorm / LM head / loss / backward / optimizer: `BLOCKED`  
> Proof ledger: `HOLD`

---

# 1. Purpose

C8 promoted the decoder-weight atlas-wave path from a Layer2/Layer3 canary into the current generalized runtime weight transport authority.

C9 must stop proving isolated rebinds and instead prove the real sequential decoder progression rule:

```text
Resident Weight N + Hidden N
        ↓
exact Weight-N execution lease
exact Hidden-N execution lease
        ↓
actual decoder Layer N execution
        ↓
Hidden N+1 single commit
        ↓
if N+1 < checkpoint layer count:
    canonical C8 wave rebind N -> N+1
    Hidden N+1 unchanged
    repeat
else:
    final decoder layer complete
```

The loop terminates only from checkpoint metadata, never from a hard-coded Layer3/Layer4 canary boundary.

---

# 2. C9 is an advancement loop, not another loader

C9 does not create a third decoder-weight transport implementation.

It orchestrates two already-admitted operations:

```text
A. execute one already-resident decoder block
B. when another decoder block remains, call C8 canonical wave rebind
```

Canonical division of responsibility:

```text
C9 = loop / step ordering / lineage / final decoder completion
C8 = destructive weight rebind transaction
C5 = target weight build staging
C4 = target weight wave planning
R6-R8 generalized execution core = resident block execution + Hidden commit
```

C9 must not duplicate checkpoint decoding, wave packing, nine-role materialization, runtime residency state transitions, or decoder numerical body code.

---

# 3. Physical parent state

The C9 physical gate starts from one same-invocation C8-D1 PASS session.

At C8-D1 exit today:

```text
weight state       = Resident
weight layer       = 3
weight generation  = 3
hidden layer       = 3
hidden generation  = 3
runtime block count = 1
runtime weight tensor count = 9
active weight execution leases = 0
active hidden execution leases = 0
transport authority = decoder-weight-atlas-wave
```

These concrete values are physical parent evidence only.

They are **not** hard-coded into the C9 progressive core.

The core derives its start from live runtime pointers.

---

# 4. Checkpoint layer-count authority

The only decoder-layer terminal bound is:

```rust
runtime.checkpoint.config.num_hidden_layers
```

C9 converts it once with checked conversion:

```rust
let checkpoint_layer_count =
    u32::try_from(runtime.checkpoint.config.num_hidden_layers)?;
```

Required:

```text
checkpoint_layer_count > 0
start_weight_layer < checkpoint_layer_count
start_hidden_layer == start_weight_layer
```

Derived final decoder layer:

```text
final_decoder_layer = checkpoint_layer_count - 1
```

Derived final hidden layer:

```text
final_hidden_layer = checkpoint_layer_count
```

No CLI key may override the checkpoint layer count as a second authority.

---

# 5. Derived loop cardinality

Let:

```text
L = checkpoint_layer_count
S = starting resident weight layer
```

Then:

```text
execution_step_count = L - S
rebind_step_count    = execution_step_count - 1
```

because the final decoder layer is executed but is not rebound to a nonexistent next decoder layer.

All arithmetic is checked.

The loop is invalid when `S >= L`.

No hard-coded expectation such as:

```text
S == 3
L == 4
rebind count == 1
```

may exist in the canonical core.

---

# 6. State waveform per step

For each decoder layer `N`:

## 6.1 Ready-to-execute state

```text
WeightSlot = Resident(N, WGen)
HiddenSlot = Hidden(N, HGen)
weight execution leases = 0
hidden execution leases = 0
resident blocks = 1
resident weight tensors = 9
```

## 6.2 After execution

```text
WeightSlot = Resident(N, WGen)      // unchanged
HiddenSlot = Hidden(N+1, HGen+1)    // one commit
```

## 6.3 If another decoder layer remains

```text
WeightSlot = Resident(N, WGen)
HiddenSlot = Hidden(N+1, HGen+1)
        ↓ C8 canonical rebind
WeightSlot = Resident(N+1, WGen+1)
HiddenSlot = Hidden(N+1, HGen+1)    // unchanged by rebind
```

Then the next iteration is ready.

## 6.4 Final decoder layer

When `N == L - 1`:

```text
execute N
commit Hidden L
DO NOT rebind
DO NOT prefetch another decoder layer
seal final decoder completion
```

---

# 7. Generation authority must be independent from layer index

Current historical R6-R8 execution contains canary-era assumptions equivalent to:

```text
weight_generation == selected_layer
hidden_generation == selected_layer
committed_hidden_generation == selected_layer + 1
```

C9 must not use those equations as authority.

Generation rules are independently monotonic:

```text
execution:
    output_hidden_generation = input_hidden_generation + 1
    weight_generation unchanged

rebind:
    target_weight_generation = source_weight_generation + 1
    hidden_generation unchanged
```

Layer rules are separately monotonic:

```text
execution:
    output_hidden_layer = executed_weight_layer + 1

rebind:
    target_weight_layer = source_weight_layer + 1
```

A generation may numerically equal a layer in the current fixture, but that equality is observational, not SSOT.

---

# 8. Required R6-R8 execution-core generalization

C9 must not manufacture fake `R6R7LayerWeightResidencySession.layer1_*` fields for arbitrary layers.

Extract the existing actual resident decoder execution body behind a generalized entry point.

Recommended contract:

```rust
pub struct CanonicalResidentDecoderLayerExecutionInput {
    pub selected_layer: u32,
    pub expected_weight_pointer: BaseTrainLayerWeightResidencyPointer,
    pub expected_hidden_pointer: LayerHiddenAuthorityPointer,
    pub parent_receipt_digest: String,
    pub parent_manifest_digest: String,
    pub output_dir: PathBuf,
    pub values: BTreeMap<String, String>,
}

pub struct CanonicalResidentDecoderLayerExecution {
    pub weight_pointer_before: BaseTrainLayerWeightResidencyPointer,
    pub input_hidden_pointer: LayerHiddenAuthorityPointer,
    pub output_hidden_pointer: LayerHiddenAuthorityPointer,
    pub execution_evidence: R6R8LayerExecutionEvidence,
    pub execution_receipt_digest: String,
    pub weight_pointer_unchanged: bool,
    pub hidden_commit_count: u32,
    pub pass: bool,
}

pub fn execute_canonical_resident_decoder_layer(
    runtime: &R6R6LiveBodySession,
    input: CanonicalResidentDecoderLayerExecutionInput,
) -> Result<CanonicalResidentDecoderLayerExecution>;
```

Exact names may follow repository convention, but the ownership contract is mandatory.

---

# 9. Historical R6-R8 wrapper preservation

Existing:

```rust
execute_resident_decoder_layer_from_session(...)
```

must remain available for historical R6-R8/R6-R9 parent gates.

Its implementation should become a compatibility wrapper over the generalized execution core.

The historical wrapper may retain Layer1-specific admission checks around the generic core.

The numerical decoder body must not be duplicated.

Required:

```text
generalized execution implementation count = 1
historical R6-R8 wrapper count              = 1
parallel decoder body implementation        = 0
```

---

# 10. Exact execution pointer binding

Before each layer execution, C9 snapshots:

```text
expected Weight pointer
expected Hidden pointer
```

The generalized execution core must require exact equality for:

## Weight

```text
state
resident layer
residency generation
transition serial
pointer digest
actual block identity digest
checkpoint tensor-set authority digest where available
```

## Hidden

```text
layer index
hidden generation
pointer digest
buffer identity digest
completion token digest
semantic BQH shape
```

No layer-number-derived generation substitute is permitted.

---

# 11. Execution lease contract

Every layer execution acquires:

```text
one BaseTrainLayerWeightExecutionLease
one LayerHiddenExecutionLease
```

Required:

```text
weight lease captured layer       = selected layer
weight lease captured generation  = expected weight generation
weight lease captured pointer     = expected weight pointer
hidden lease captured layer       = selected layer
hidden lease captured generation  = expected hidden generation
hidden lease captured pointer     = expected hidden pointer
```

The two generations do not have to be compared to each other as an authority condition.

Both leases are revalidated before use and before completion.

Both leases must be released before Hidden commit.

---

# 12. Actual decoder body per layer

C9 execution uses the already-proven real route:

```text
Input RMSNorm
Q projection
K projection
V projection
NeoX RoPE
Headwise prepared BQHD route
W5 Stage10
W6 Stage11
W7 Stage12
same-device context adoption
OProj
attention residual
post-attention RMSNorm
SwiGLU gate projection
SwiGLU up projection
SiLU multiply
down projection
FFN residual
final hidden
```

No shadow-only body, no mock block, no CPU decoder body, and no legacy full-layer reference block is inserted into C9 progressive execution.

---

# 13. Per-step dispatch evidence

C9 consumes typed `R6R8LayerExecutionEvidence` from every execution.

It constructs a receipt-only normalized projection:

```rust
pub struct R6R9C9DispatchParityEvidence {
    pub schema_version: u32,
    pub executed_layer: u32,
    pub input_norm_dispatch_count: u64,
    pub q_projection_count: u64,
    pub k_projection_count: u64,
    pub v_projection_count: u64,
    pub stage10_q_tile_dispatch_count: u64,
    pub stage10_candidate_dispatch_count: u64,
    pub stage10_oracle_dispatch_count: u64,
    pub stage10_compare_dispatch_count: u64,
    pub stage11_candidate_dispatch_count: u64,
    pub stage11_oracle_dispatch_count: u64,
    pub stage11_compare_dispatch_count: u64,
    pub stage12_candidate_dispatch_count: u64,
    pub stage12_oracle_dispatch_count: u64,
    pub stage12_normalize_verify_dispatch_count: u64,
    pub oproj_dispatch_count: u64,
    pub attention_residual_add_count: u64,
    pub post_attn_norm_dispatch_count: u64,
    pub gate_proj_dispatch_count: u64,
    pub up_proj_dispatch_count: u64,
    pub silu_multiply_dispatch_count: u64,
    pub down_proj_dispatch_count: u64,
    pub ffn_residual_add_count: u64,
    pub runtime_geometry_compared_scalar_count: u64,
    pub observed_compared_scalar_count: u64,
    pub mismatch_count: u64,
    pub non_finite_count: u64,
    pub payload_readback_count: u64,
    pub pass: bool,
    pub evidence_digest: String,
}
```

This projection is evidence only and owns no execution decisions.

---

# 14. Per-step dispatch requirements

Each step requires:

```text
input norm dispatch = 1
Q projection        = 1
K projection        = 1
V projection        = 1
Stage10 candidate dispatch > 0
Stage11 candidate dispatch > 0
Stage12 candidate dispatch > 0
OProj dispatch      = 1
gate projection     = 1
up projection       = 1
down projection     = 1
```

Stage10/11/12 exact flat counts must not be frozen to the old fixture when typed evidence already owns the true count.

The typed child evidence is authoritative.

---

# 15. Per-step parity requirements

For every layer:

```text
execution_evidence.pass = true
parity.pass = true
runtime_geometry_compared_scalar_count = checked(B * Q * H)
observed_compared_scalar_count = runtime_geometry_compared_scalar_count
mismatch_count = 0
non_finite_count = 0
payload_readback_count = 0
```

The existing execution route already binds:

```text
mixed-envelope reference parity
exact replay final parity
exact publication parity
```

C9 records those receipt digests.

C9 does not rebuild a private legacy full-layer oracle for every layer.

---

# 16. Hidden commit contract

All numerical/pre-commit parity gates must pass before the one Hidden commit owned by the execution operation.

Commit authority remains:

```rust
LayerHiddenAuthoritySlot::commit_next_layer(...)
```

Required lineage:

```text
output_hidden.layer_index
    = input_hidden.layer_index + 1

output_hidden.hidden_generation
    = input_hidden.hidden_generation + 1

output_hidden.previous_pointer_digest
    = input_hidden.pointer_digest
```

The operation ID must be unique per layer execution.

No duplicate Hidden commit is allowed.

---

# 17. Publication identity continuity

C8-D1 established that a persistent hidden buffer identity must not be silently redefined by a later observational raw bridge.

C9 therefore requires:

```text
execution evidence output hidden pointer digest
    == published Hidden pointer digest

execution evidence output buffer identity digest
    == published Hidden buffer identity digest

execution evidence output completion token digest
    == published Hidden completion token digest
```

Additional bridge-local `seam_id` values must remain observational and cannot become a second persistent Hidden identity authority.

---

# 18. Execution completion binding for C8

After each non-final layer execution, C9 builds a generalized C8 source completion binding from the actual execution evidence.

C8's current C7-specific helper is not sufficient for arbitrary layers.

Introduce a generic builder, recommended:

```rust
pub fn bind_canonical_layer_execution_completion(
    runtime: &R6R6LiveBodySession,
    source_weight_pointer: &BaseTrainLayerWeightResidencyPointer,
    execution_evidence: &R6R8LayerExecutionEvidence,
    output_hidden_pointer: &LayerHiddenAuthorityPointer,
    execution_receipt_digest: &str,
) -> Result<CanonicalLayerExecutionCompletionBinding>;
```

It must validate exact typed evidence, not digest shape alone.

---

# 19. Generic completion-binding checks

Required:

```text
execution selected layer = source weight layer
execution weight pointer = source weight pointer
execution weight generation = source weight generation
execution transition serial = source weight serial
execution block identity = source resident block identity
execution checkpoint set = runtime checkpoint set
execution output hidden pointer = current Hidden pointer
execution output hidden generation = current Hidden generation
execution output buffer identity = current Hidden buffer identity
execution output completion token = current Hidden completion token
execution output shape = current Hidden shape
parity mismatch = 0
parity nonfinite = 0
payload readback = 0
execution pass = true
```

C8 physical C7-specific source binding may become a wrapper over this generic builder plus its extra C7 parity assertions.

---

# 20. Canonical rebind invocation

For every non-final executed layer `N`, C9 calls exactly:

```rust
rebind_resident_decoder_layer(
    runtime,
    N,
    N + 1,
    &source_completion,
    &hidden_n_plus_1,
    &packing_policy,
    &transport_authority,
)
```

This is the C8 canonical wave implementation.

C9 must not call:

```text
rebind_resident_decoder_layer_legacy_full_loader_reference(...)
load_base_train_atlas_wave_02_r6_r7_decoder_block_weights(...)
C6 Layer2-only rebind canary
C7 legacy oracle builder
```

---

# 21. Rebind result checks

Every C8 rebind step must prove:

```text
source layer               = N
target layer               = N+1
source weight generation   = WGen
target weight generation   = WGen+1
runtime adopt              = 1
runtime resident blocks    = 1
runtime resident tensors   = 9
runtime authority overlap  = 0
legacy runtime loader      = 0
same-operation fallback    = 0
source rebuild             = 0
hidden mutation            = 0
target forward             = 0
next-layer prefetch        = 0
gpu weight readback        = 0
```

The C9 loop does not relax any C8 failure boundary.

---

# 22. C4/C5 remain transitively canonical

Each C9 rebind inherits C8's exact C4/C5 contracts.

Per rebind:

```text
C4 target plan = 1
role count = 9
lane count = 9
wave count = plan-derived
mega atlas = 0
cross-wave payload overlap = 0

C5 checkpoint reads = 9
C5 decodes = 9
C5 material commits = 9
source owner releases = 9
decoded owner releases = 9
wave fence waits = plan wave count
complete nine-role seal = 1
gpu weight payload readback = 0
```

C9 does not assume every layer has exactly three waves.

---

# 23. No legacy runtime loader scope must be honest

The physical C9 gate runs a C8 parent, and that parent transitively runs the historical C7 admission oracle.

Therefore C9 must **not** claim process-global legacy checkpoint-loader activity is zero.

The truthful scoped invariant is:

```text
C9 progressive loop legacy runtime loader invocation count = 0
C9 progressive loop same-operation legacy fallback count = 0
```

Parent historical/reference activity is reported separately, for example:

```text
parent_c7_reference_oracle_checkpoint_reads = 9
```

Those parent oracle reads are non-runtime-authority evidence and are not counted as C9 progressive runtime loading.

No log may hide or relabel those parent reads as zero.

---

# 24. No layer-specific canary branch

The canonical C9 core must contain zero semantic branches such as:

```text
if layer == 3
if layer == 4
match layer { 3 => ..., 4 => ... }
selected_layer == 3
expected_final_layer == 4
```

Layer-number strings may appear only in historical test names or parent evidence descriptions, not in C9 control flow.

The current physical start layer 3 is derived from C8 output.

---

# 25. Progressive step receipt

Recommended per-step receipt:

```rust
pub struct R6R9C9ProgressiveLayerStepReceipt {
    pub schema_version: u32,
    pub step_ordinal: u32,
    pub checkpoint_layer_count: u32,
    pub executed_layer: u32,
    pub weight_pointer_before_digest: String,
    pub weight_generation_before: u64,
    pub weight_transition_serial_before: u64,
    pub block_identity_digest: String,
    pub input_hidden_pointer_digest: String,
    pub input_hidden_layer: u32,
    pub input_hidden_generation: u64,
    pub input_hidden_buffer_identity_digest: String,
    pub input_hidden_completion_token_digest: String,
    pub execution_evidence_digest: String,
    pub execution_completion_binding_digest: String,
    pub dispatch_parity_evidence_digest: String,
    pub output_hidden_pointer_digest: String,
    pub output_hidden_layer: u32,
    pub output_hidden_generation: u64,
    pub output_hidden_buffer_identity_digest: String,
    pub output_hidden_completion_token_digest: String,
    pub weight_pointer_unchanged_during_execution: bool,
    pub hidden_commit_count: u32,
    pub rebind_required: bool,
    pub rebind_performed: bool,
    pub rebind_receipt_digest: Option<String>,
    pub next_weight_pointer_digest: Option<String>,
    pub next_weight_layer: Option<u32>,
    pub next_weight_generation: Option<u64>,
    pub mismatch_count: u64,
    pub non_finite_count: u64,
    pub payload_readback_count: u64,
    pub weight_payload_readback_count: u64,
    pub progressive_legacy_runtime_loader_count: u32,
    pub same_operation_legacy_fallback_count: u32,
    pub pass: bool,
    pub receipt_digest: String,
}
```

---

# 26. Step receipt invariants

Every step requires:

```text
executed layer == input hidden layer
weight pointer unchanged during execution = true
hidden commit count = 1
output hidden layer = executed layer + 1
output hidden generation = input hidden generation + 1
mismatch = 0
nonfinite = 0
payload readback = 0
weight payload readback = 0
progressive legacy runtime loader = 0
same-operation fallback = 0
```

For non-final steps:

```text
rebind_required = true
rebind_performed = true
next weight layer = executed layer + 1
next weight generation = previous weight generation + 1
```

For final decoder step:

```text
rebind_required = false
rebind_performed = false
next weight pointer = None
```

---

# 27. Progressive lineage ledger

C9 owns a sequential ledger, not a mutable map of partial states.

Recommended:

```rust
pub struct R6R9C9ProgressiveLineageLedger {
    pub schema_version: u32,
    pub checkpoint_layer_count: u32,
    pub starting_weight_pointer_digest: String,
    pub starting_weight_layer: u32,
    pub starting_weight_generation: u64,
    pub starting_hidden_pointer_digest: String,
    pub starting_hidden_layer: u32,
    pub starting_hidden_generation: u64,
    pub execution_step_count: u32,
    pub rebind_step_count: u32,
    pub step_receipt_digests: Vec<String>,
    pub final_weight_pointer_digest: String,
    pub final_weight_layer: u32,
    pub final_weight_generation: u64,
    pub final_hidden_pointer_digest: String,
    pub final_hidden_layer: u32,
    pub final_hidden_generation: u64,
    pub aggregate_payload_readback_count: u64,
    pub aggregate_weight_payload_readback_count: u64,
    pub aggregate_mismatch_count: u64,
    pub aggregate_non_finite_count: u64,
    pub progressive_legacy_runtime_loader_count: u32,
    pub same_operation_legacy_fallback_count: u32,
    pub pass: bool,
    pub ledger_digest: String,
}
```

Step digests are appended in execution order only.

No sorting by layer is needed because the loop order itself is canonical.

---

# 28. Sequential pointer lineage

For adjacent execution steps `i` and `i+1`:

```text
step[i].output_hidden_pointer
    == step[i+1].input_hidden_pointer
```

When a rebind occurs:

```text
step[i].next_weight_pointer
    == step[i+1].weight_pointer_before
```

And:

```text
step[i+1].executed_layer
    == step[i].executed_layer + 1
```

No skipped decoder layer and no duplicate execution layer are permitted.

---

# 29. Aggregate generation lineage

Let:

```text
start weight generation = WG0
start hidden generation = HG0
execution count = E
rebind count = R
```

Then final required values are:

```text
final weight generation = WG0 + R
final hidden generation = HG0 + E
```

using checked arithmetic.

C9 may additionally log whether generations numerically align with final layer indexes, but may not use that equality to prove lineage.

---

# 30. Final decoder completion seal

C9 final success requires:

```text
final_weight.state = Resident
final_weight.layer = checkpoint_layer_count - 1
final_hidden.layer = checkpoint_layer_count
final weight execution leases = 0
final hidden execution leases = 0
resident block count = 1
resident weight tensor count = 9
```

And the final step must be the actual execution of:

```text
checkpoint_layer_count - 1
```

with one Hidden commit to:

```text
checkpoint_layer_count
```

No post-final decoder rebind is allowed.

---

# 31. Final decoder completion evidence

Recommended:

```rust
pub struct R6R9C9FinalDecoderLayerCompletionSeal {
    pub schema_version: u32,
    pub checkpoint_layer_count: u32,
    pub final_executed_decoder_layer: u32,
    pub final_execution_evidence_digest: String,
    pub final_dispatch_parity_evidence_digest: String,
    pub final_weight_pointer_digest: String,
    pub final_weight_generation: u64,
    pub final_hidden_pointer_digest: String,
    pub final_hidden_layer: u32,
    pub final_hidden_generation: u64,
    pub execution_step_count: u32,
    pub rebind_step_count: u32,
    pub progressive_lineage_ledger_digest: String,
    pub post_final_rebind_count: u32,
    pub next_layer_prefetch_count: u32,
    pub mismatch_count: u64,
    pub non_finite_count: u64,
    pub payload_readback_count: u64,
    pub weight_payload_readback_count: u64,
    pub pass: bool,
    pub seal_digest: String,
}
```

Required:

```text
post_final_rebind_count = 0
next_layer_prefetch_count = 0
mismatch = 0
nonfinite = 0
payload readback = 0
weight payload readback = 0
```

---

# 32. Weight payload readback seal

C9 accumulates weight readback only from canonical rebind receipts.

For each rebind:

```text
rebind_receipt.gpu_weight_readback_count = 0
```

Aggregate:

```text
sum(all C9 rebind weight readback counts) = 0
```

Execution-route payload readback is separately required to remain zero.

No CPU fallback may satisfy either condition.

---

# 33. Runtime authority overlap

Each C8 rebind must retain:

```text
runtime_authority_overlap_count = 0
```

C9 aggregate:

```text
sum runtime authority overlap = 0
```

The progressive loop may have only one resident runtime decoder block at a time.

C5 private build staging does not count as runtime residency authority.

---

# 34. Memory cardinality invariant

During execution:

```text
runtime resident decoder blocks = 1
runtime resident checkpoint weight tensors = 9
```

During C8 vacancy:

```text
runtime resident decoder blocks = 0
runtime resident checkpoint weight tensors = 0
```

After rebind:

```text
runtime resident decoder blocks = 1
runtime resident checkpoint weight tensors = 9
```

C9 must not preload all decoder layers.

---

# 35. No prefetch in C9

C9 proves strict sequential advancement first.

Forbidden:

```text
next-layer weight prefetch
parallel target-layer decode while current layer executes
all-layer checkpoint preload
multi-layer wave overlap
future-layer runtime authority
```

Prefetch may only be introduced by a later separately admitted patch with independent memory/ordering receipts.

---

# 36. Failure boundary: execution before Hidden commit

If execution fails before Hidden commit:

```text
Weight N remains Resident
Hidden N remains current
no C8 rebind is attempted
no legacy fallback
C9 returns failure
```

No generation is advanced.

---

# 37. Failure boundary: execution after Hidden commit

The current execution path performs exact publication parity after Hidden commit.

If a late publication verification fails:

```text
Hidden N+1 may already be canonical
Weight N remains Resident
C9 must stop
C9 must not rebind
C9 must not silently roll back Hidden
C9 must not fabricate a pass receipt
```

There is currently no canonical hidden RecoveryRequired state.

C9 must report the late committed state explicitly rather than inventing one.

---

# 38. Failure boundary: rebind before destructive extraction

After successful execution, the state is:

```text
Weight N Resident
Hidden N+1 canonical
```

If C8 rebind fails before exclusive destructive source extraction:

```text
Weight N remains Resident
Hidden N+1 remains canonical
RecoveryRequired = 0
legacy fallback = 0
```

C9 stops the current invocation.

This state is a truthful inter-step retry boundary.

---

# 39. Failure boundary: rebind after destructive extraction

C8 owns this boundary.

Required:

```text
Hidden N+1 preserved
weight state -> RecoveryRequired
source rebuild = 0
legacy fallback = 0
C9 stops immediately
```

C9 may not catch the C8 destructive failure and continue to another layer.

---

# 40. Same-operation fallback prohibition

For every progressive step:

```text
legacy runtime target loader count = 0
same-operation legacy fallback count = 0
source rebuild count = 0
```

No `match Err => legacy_loader(...)` branch may exist in C9.

No environment variable may silently enable a fallback path.

---

# 41. Transport authority continuity

C9 captures one C8 current transport authority before entering the loop.

Required on every rebind:

```text
active transport = decoder-weight-atlas-wave
legacy runtime loader retired = true
same-operation legacy fallback allowed = false
authority digest unchanged across C9 loop
```

A transport authority change mid-loop is a hard failure.

---

# 42. Packing policy continuity

C9 parses one canonical C4 packing policy before the loop.

The same policy object/semantic digest is used for every C8 rebind in the C9 invocation.

C9 must not mutate budget or worker limits per layer unless a future admitted policy explicitly owns that behavior.

---

# 43. Operation identity

Each execution and rebind operation ID must include enough lineage to prevent accidental duplicate commit.

Recommended execution identity:

```text
checkpoint_set_digest
executed_layer
weight_pointer_digest
input_hidden_pointer_digest
step_ordinal
```

Recommended rebind identity remains C8-owned and includes source/target/pointer lineage.

No random nonce is used as semantic authority.

---

# 44. Step ordering SSOT

Canonical loop order is strictly:

```text
snapshot ready state
→ acquire execution leases
→ execute resident layer
→ release leases
→ Hidden N+1 commit
→ publication verification
→ seal execution evidence
→ build C8 source completion binding
→ if final layer: seal completion and stop
→ else call C8 rebind
→ validate adopted next weight and unchanged Hidden
→ append step receipt
→ next layer
```

No target rebind is allowed before the source layer execution completion binding exists.

---

# 45. Final-layer branch is structural, not layer-specific

The only branch permitted is:

```rust
let next_hidden_layer = executed_layer.checked_add(1)?;
match next_hidden_layer == checkpoint_layer_count {
    true => final_decoder_completion,
    false => canonical_rebind_to(next_hidden_layer),
}
```

This is a checkpoint-bound structural branch, not a Layer3/Layer4 canary branch.

---

# 46. C9 core API

Recommended:

```rust
pub struct R6R9C9ProgressiveNLayerExecution {
    pub transport_authority: CanonicalDecoderWeightTransportAuthority,
    pub checkpoint_layer_count: u32,
    pub starting_weight_pointer: BaseTrainLayerWeightResidencyPointer,
    pub starting_hidden_pointer: LayerHiddenAuthorityPointer,
    pub step_receipts: Vec<R6R9C9ProgressiveLayerStepReceipt>,
    pub lineage_ledger: R6R9C9ProgressiveLineageLedger,
    pub final_completion: R6R9C9FinalDecoderLayerCompletionSeal,
}

pub fn advance_resident_decoder_to_checkpoint_end(
    runtime: &R6R6LiveBodySession,
    transport_authority: &CanonicalDecoderWeightTransportAuthority,
    packing_policy: &DecoderWeightAtlasWavePackingPolicy,
    output_dir: &Path,
    values: &BTreeMap<String, String>,
) -> Result<R6R9C9ProgressiveNLayerExecution>;
```

The core receives an already-admitted runtime state.

It does not call C7 or the C8 physical canary wrapper.

---

# 47. Physical C9 gate wrapper

The test/admission wrapper may do:

```text
run C8-D1 physical parent once
validate C8 PASS evidence
obtain runtime + current transport authority
call C9 generalized core once
```

This split prevents production C9 semantics from depending on Layer2/Layer3 admission wrappers.

Required:

```text
C9 core C7 type dependencies = 0
C9 core C6 type dependencies = 0
C9 core layer-specific canary dependencies = 0
```

Parent evidence remains visible in the outer gate receipt.

---

# 48. Parent C8 evidence binding

Physical C9 gate requires:

```text
C8 final receipt pass = true
C8 pass token exact
C8 canonical transport authority = decoder-weight-atlas-wave
C8 legacy runtime loader retired = true
C8 same-operation fallback = 0
C8 runtime authority overlap = 0
C8 hidden pointer unchanged during rebind = true
C8 target forward = 0
C8 adopted weight pointer = live runtime weight pointer
C8 hidden pointer = live runtime hidden pointer
```

Then C9 starts from those live pointers, not copied expected literals.

---

# 49. C9 CLI contract

```text
--require-r6-r9-c9-progressive-n-layer-wave-advancement true
--require-r6-r9-c9-checkpoint-layer-count-authority true
--require-r6-r9-c9-c8-canonical-rebind-authority true
--require-r6-r9-c9-exact-resident-weight-execution-lease true
--require-r6-r9-c9-exact-hidden-execution-lease true
--require-r6-r9-c9-hidden-single-commit-per-layer true
--require-r6-r9-c9-generation-monotonicity true
--require-r6-r9-c9-pointer-lineage true
--require-r6-r9-c9-per-step-dispatch-evidence true
--require-r6-r9-c9-per-step-parity-evidence true
--require-r6-r9-c9-zero-mismatch true
--require-r6-r9-c9-zero-nonfinite true
--require-r6-r9-c9-zero-payload-readback true
--require-r6-r9-c9-zero-weight-payload-readback true
--require-r6-r9-c9-final-decoder-layer-completion true
--require-r6-r9-c9-no-post-final-rebind true
--require-r6-r9-c9-progressive-legacy-runtime-loader-zero true
--require-r6-r9-c9-same-operation-fallback-zero true
--allow-r6-r9-c9-layer-specific-canary-branch false
--allow-r6-r9-c9-next-layer-prefetch false
--allow-r6-r9-c9-all-layer-preload false
--allow-r6-r9-c9-parallel-layer-execution false
--allow-r6-r9-c9-generation-from-layer-index false
--allow-r6-r9-c9-silent-hidden-rollback false
```

C9 does not accept `first-layer`, `last-layer`, or `expected-final-layer` as runtime authorities.

---

# 50. Existing CLI reuse

C9 reuses existing canonical execution and C4 packing values such as batch size, sequence length, row valid lengths, position IDs, model/queue epochs, candidate nonce, final hidden tolerances, C4 weight transient budget, C4 parallel decode workers, C4 max lanes per wave, mega-atlas policy, and cross-wave overlap policy.

No duplicate C9 copy of C4 memory policy is introduced.

---

# 51. No user-selected partial decoder window in C9

Historical R6-R9 coordinator owns an execution-window concept for old canary gates.

C9 final-completion admission must not inherit historical first/last/max-step CLI settings as current C9 authorities.

C9 always advances from the live admitted start pointer to checkpoint end.

---

# 52. Historical coordinator isolation

The historical R6-R9 coordinator still calls the explicit legacy full-loader reference path and remains historical evidence only.

C9 must not reuse that loop as current authority.

Historical C1-C4 behavior remains reproducible and explicitly non-current.

---

# 53. Required implementation surface

```text
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r8_layer1_live_body.rs
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r9_c8_canonical_decoder_weight_wave_rebind.rs
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r9_c9_progressive_n_layer_wave_advancement.rs
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r6_r9_forward_coordinator_gate.rs
specs/cli/ash_basetrain_atlas_wave_02_r6_r9.args
```

No WGSL semantic change is required.

---

# 54. Static forbidden call inventory

C9 canonical module must have zero direct references to:

```text
load_base_train_atlas_wave_02_r6_r7_decoder_block_weights
rebind_resident_decoder_layer_legacy_full_loader_reference
run_r6_r9_c6_layer2_decoder_weight_wave_rebind_session
run_r6_r9_c7_layer2_wave_built_execution_parity_session
```

The physical gate wrapper may call `run_r6_r9_c8_canonical_decoder_weight_wave_loader_session()` once.

---

# 55. Static layer-hardcode inventory

In C9 canonical core, semantic occurrences of exact current canary layer literals must be zero. Current fixture values may appear only in comments/tests/expected example output, never control flow.

---

# 56. Static generation-hardcode inventory

Canonical generalized execution core must have zero authority checks equivalent to generation equals selected layer. Replace with exact pointer binding and checked previous-generation increment.

---

# 57. Runtime geometry authority

For each layer:

```text
runtime_geometry_compared_scalar_count = checked(B * Q * H)
```

No fixed `65536` authority is allowed. The current fixture may still print it as an observation.

---

# 58. Hidden shape continuity

For all decoder layers in one C9 invocation:

```text
input_hidden_shape == output_hidden_shape
```

C9 validates evidence/pointer shape exactness every step. No shape repair or implicit reshape fallback is allowed.

---

# 59. Checkpoint identity continuity

Every execution step and every C8 rebind must bind the same `runtime.checkpoint.checkpoint_set_digest`. A checkpoint digest change mid-loop is a hard failure.

---

# 60. Model/runtime identity continuity

C9 keeps one live model instance, training session, WGPU device, WGPU queue lineage, checkpoint authority, weight slot, and hidden slot throughout the progressive loop.

No second device is created per layer and no process-per-layer execution is allowed.

---

# 61. Same-device contract

C9 preserves the existing same-device route for Q/K/V bridge, RoPE, Headwise stages, context adoption, OProj/MLP continuation, and weight materialization.

Payload tensor readback remains zero.

---

# 62. C9 aggregate counts

C9 final receipt records execution/rebind counts, total checkpoint weight reads, decodes, material commits, wave fence waits, hidden commits, runtime authority overlap, progressive legacy runtime loader, same-operation fallback, payload readback, weight payload readback, mismatch, and nonfinite counts. All sums use checked arithmetic.

---

# 63. Aggregate expected formulas

Let `R = rebind_step_count` and `E = execution_step_count`.

```text
total hidden commits = E
total checkpoint weight reads = 9 * R
total weight decodes = 9 * R
total weight material commits = 9 * R
runtime authority overlap = 0
progressive legacy runtime loader = 0
same-operation fallback = 0
payload readback = 0
weight payload readback = 0
mismatch = 0
nonfinite = 0
```

Wave fence total is the checked sum of each C8 plan-derived wave count, not `3 * R` as an authority.

---

# 64. Parent counters are not C9 counters

C9 final receipt distinguishes parent C8 checkpoint reads, parent C7 oracle checkpoint reads, and C9 progressive checkpoint reads.

Do not hide parent activity inside C9 zeros and do not charge parent activity against C9 progressive invariants.

---

# 65. Final weight state rationale

After executing the final decoder layer, C9 intentionally leaves its weights resident:

```text
final Weight = Layer L-1
final Hidden = Layer L
```

A later final-norm/LM-head or memory-release patch owns any subsequent release decision.

---

# 66. No final-norm leakage

C9 stops at the decoder boundary. Final RMSNorm, LM head, logits, sampling, forward loss, backward, optimizer, and production inference remain blocked.

---

# 67. Final receipt

The top-level receipt binds the C8 parent digest, transport authority, checkpoint set/count, starting pointers, execution/rebind counts, progressive lineage ledger, final completion seal, aggregate counts, final pointers, pass state, and receipt digest.

---

# 68. Manifest

The final manifest binds patch ID, build revision, final receipt digest, parent C8 digest, transport authority digest, checkpoint set/count, execution/rebind counts, lineage ledger, final completion seal, final pointers, aggregate zero counters, PASS token, and proof ledger HOLD.

No file hash sidecars are required in baked ZIP output.

---

# 69. Expected terminal line

```text
[r6-r9-c9-progressive-n-layer-wave-advancement]
checkpoint_layers=<L>
start_weight_layer=<S>
start_weight_generation=<WG0>
start_hidden_layer=<S>
start_hidden_generation=<HG0>
execution_steps=<L-S>
rebind_steps=<L-S-1>
final_weight_layer=<L-1>
final_weight_generation=<WG0+R>
final_hidden_layer=<L>
final_hidden_generation=<HG0+E>
hidden_commits=<E>
checkpoint_reads=<9*R>
decodes=<9*R>
material_commits=<9*R>
wave_fence_waits=<sum(plan wave counts)>
per_step_dispatch_evidence=<E>
per_step_parity_evidence=<E>
mismatch=0
nonfinite=0
payload_readback=0
weight_payload_readback=0
runtime_authority_overlap=0
progressive_legacy_runtime_loader=0
same_operation_legacy_fallback=0
post_final_rebind=0
next_layer_prefetch=0
parent_c7_reference_oracle_reads=9
transport_authority_digest=<sha256>
lineage_ledger_digest=<sha256>
final_completion_digest=<sha256>
final_weight_pointer_digest=<sha256>
final_hidden_pointer_digest=<sha256>
proof_ledger=HOLD
```

---

# 70. PASS token

```text
PASS_ASH_BASETRAIN_ATLAS_WAVE_02_R6_R9_C9_PROGRESSIVE_N_LAYER_WAVE_ADVANCEMENT_C8_D1_PHYSICAL_PARENT_CANONICAL_DECODER_WEIGHT_ATLAS_WAVE_AUTHORITY_CHECKPOINT_LAYER_COUNT_DERIVED_START_AND_END_NO_LAYER_SPECIFIC_CANARY_BRANCH_RESIDENT_LAYER_N_EXACT_WEIGHT_AND_HIDDEN_EXECUTION_LEASE_ACTUAL_INPUT_RMSNORM_QKV_NEOX_ROPE_HEADWISE_W5_W6_W7_OPROJ_ATTENTION_RESIDUAL_POST_ATTN_RMSNORM_SWIGLU_GATE_UP_DOWN_FFN_RESIDUAL_HIDDEN_N_PLUS_1_SINGLE_COMMIT_PER_EXECUTED_LAYER_EXACT_POINTER_BUFFER_COMPLETION_AND_GENERATION_LINEAGE_PER_STEP_TYPED_DISPATCH_AND_PARITY_EVIDENCE_RUNTIME_DERIVED_BQH_ZERO_MISMATCH_ZERO_NONFINITE_ZERO_PAYLOAD_READBACK_CANONICAL_C8_REBIND_N_TO_N_PLUS_1_ONLY_WHEN_MORE_DECODER_LAYERS_REMAIN_C4_PLAN_AND_C5_STAGING_REUSE_EXCLUSIVE_DESTRUCTIVE_VACANT_BEFORE_TARGET_PAYLOAD_SINGLE_RUNTIME_WEIGHT_AUTHORITY_MONOTONIC_INDEPENDENT_WEIGHT_AND_HIDDEN_GENERATIONS_ZERO_PROGRESSIVE_LEGACY_RUNTIME_LOADER_ZERO_SAME_OPERATION_LEGACY_FALLBACK_ZERO_SOURCE_REBUILD_ZERO_WEIGHT_PAYLOAD_READBACK_FINAL_DECODER_LAYER_EXECUTED_FINAL_HIDDEN_LAYER_EQUALS_CHECKPOINT_LAYER_COUNT_ZERO_POST_FINAL_REBIND_ZERO_NEXT_LAYER_PREFETCH_FINAL_RMSNORM_LM_HEAD_FORWARD_LOSS_BACKWARD_OPTIMIZER_PRODUCTION_INFERENCE_BLOCKED_PROOF_LEDGER_HOLD_SEALED
```

---

# 71. Physical success criteria

C9 physical PASS requires one C8-D1 parent PASS, checkpoint layer count resolution, live C8 start state binding, all remaining decoder layers executed exactly once, all required intermediate C8 wave rebinds succeed, independent weight/hidden generation lineage, pointer lineage, per-step dispatch/parity evidence, zero mismatch/nonfinite/readback, zero progressive legacy loader/fallback/authority overlap, final decoder completion, final Hidden layer equal to checkpoint layer count, and no post-final rebind/prefetch.

---

# 72. C9 does not prove fault injection

A normal physical PASS proves success-path sequencing only. Fault-injected execution/rebind failure paths need separate admission if proof is desired.

---

# 73. Static closure checklist

```text
C9 progressive module present
C9 physical gate called after one C8-D1 parent
C9 core does not invoke C7/C6 canary sessions
checkpoint layer count is sole terminal bound
no C9 first/last layer CLI authority
no semantic Layer3/Layer4 branch in C9 core
generalized resident execution core present
historical R6-R8 wrapper preserved
numerical decoder body implementation count remains one
canonical execution generation no longer derived from layer index
exact weight pointer/generation binding present
exact hidden pointer/generation/buffer/completion binding present
one Hidden commit per executed layer
output Hidden generation uses previous generation + 1
output Hidden layer uses previous layer + 1
weight pointer unchanged during execution
generic C8 source completion builder present
C8 C7-specific physical binding preserved
C9 calls only C8 canonical rebind
C9 direct legacy loader/rebind calls = 0
C9 same-operation fallback branch = 0
all rebinds validate hidden unchanged / overlap 0 / readback 0
per-step dispatch/parity evidence typed
runtime compared count derives from BQH
no fixed 65536 authority
final decoder layer receives real execution
final Hidden layer equals checkpoint layer count
no post-final rebind / prefetch / all-layer preload
no WGSL semantic change required
```

---

# 74. Expected changed files

```text
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r8_layer1_live_body.rs
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r9_c8_canonical_decoder_weight_wave_rebind.rs
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r9_c9_progressive_n_layer_wave_advancement.rs
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r6_r9_forward_coordinator_gate.rs
specs/cli/ash_basetrain_atlas_wave_02_r6_r9.args
```

---

# 75. Baked package policy

C9 bake produces a full code ZIP and overlay ZIP, excluding `*.md`, `*.sha256`, `artifacts/`, `manifests/`, manifest JSON debug bundles, and accumulated historical reports unless explicitly requested.

---

# 76. Admission state after physical PASS

```text
R6-R6 actual Layer0 body                         = ADMITTED
R6-R7 historical residency                       = ADMITTED_HISTORY
R6-R8 exact resident execution                   = ADMITTED
C4 decoder-weight wave planner                   = ADMITTED
C5 decoder-weight wave staging                   = ADMITTED
C6 Layer1 -> Layer2 wave rebind canary            = ADMITTED
C7 Layer2 wave-built execution parity             = ADMITTED
C8 canonical generalized wave rebind authority    = ADMITTED
C8-D1 Hidden publication identity closure         = ADMITTED
C9 progressive decoder-to-checkpoint-end loop     = ADMITTED on physical PASS

Current decoder-weight runtime transport          = DECODER_WEIGHT_ATLAS_WAVE
Legacy generalized runtime loader                 = RETIRED
Legacy historical/reference loader                = RETAINED_NON_AUTHORITY
Final decoder hidden                              = AVAILABLE after C9 PASS
Final RMSNorm / LM head                           = BLOCKED
Forward loss                                      = BLOCKED
Backward                                          = BLOCKED
Optimizer                                         = BLOCKED
Production inference                              = BLOCKED
Proof ledger                                      = HOLD
```

---

# 77. What C9 PASS proves

C9 PASS proves one checkpoint-derived progressive decoder loop can run from the C8-admitted live state to the final decoder layer, all remaining resident layers execute actual GPU routes, Hidden advances once per layer, weights advance through C8 canonical atlas-wave rebind only while another decoder layer remains, C4/C5 remain the only planner/staging implementations, runtime weight authority remains singular, generation lineages remain independent and monotonic, per-step evidence is sealed, progressive legacy runtime loading/fallback/readback remain zero, and final decoder completion is checkpoint-bound.

---

# 78. What C9 PASS does not prove

C9 PASS does not prove final RMSNorm, LM-head logits, sampling, forward loss, backward, optimizer, convergence, long-horizon stability, performance superiority, prefetch safety, fault-injected recovery completeness, or production inference admission.

---

# 79. Natural next boundary

After C9 physical PASS, the recommended next boundary is:

```text
ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C10
Long-Horizon Progressive Residency / Memory Ledger / Repeated Wave Rebind Health / Peak Host·GPU Pressure / Generation Drift Detection / Recovery Boundary Audit Seal
```

or, if decoder completion is accepted as sufficiently stable:

```text
ASH-BASETRAIN-ATLAS-WAVE-02-R6-R10
Final RMSNorm / LM Head Forward / Final Hidden Consumption / Logit Surface Publication / Zero Hidden Recompute Seal
```

C10 is recommended before promotion toward production inference because C9 may exercise many sequential destructive rebinds in one invocation.

---

# 80. Architecture seal

> C9 is the point where decoder progression stops being a collection of layer-specific admissions and becomes one checkpoint-bounded state machine. The live resident Weight-N block and exact Hidden-N pointer are leased, the already-proven decoder body executes and commits exactly one Hidden-N+1, typed dispatch/parity evidence is sealed, and only when another decoder layer exists does the loop call the C8 canonical decoder-weight atlas-wave rebind to replace Weight-N with Weight-N+1 while leaving Hidden-N+1 untouched. Layer indexes and generations advance under separate checked rules; no generation is inferred from a layer number, no Layer3/Layer4 canary branch owns control flow, no legacy full-layer runtime loader or same-operation fallback exists in the progressive loop, and the final decoder layer is determined exclusively by checkpoint `num_hidden_layers`. The loop ends with the final decoder weight still resident, Hidden at exactly the checkpoint layer count, zero post-final rebind, zero next-layer prefetch, zero payload/weight readback, and a sequential pointer/generation ledger sufficient for the next final-norm or long-horizon health boundary.
