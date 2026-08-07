# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C8

## Canonical Decoder Weight Wave Loader Adoption / Generalized Sequential Rebind Authority / Legacy Full-Layer Runtime Loader Retirement / C4 Planner + C5 Staging Canonical Binding / Resident N -> VacantForRebind -> Wave Build -> Resident N+1 / Generation Monotonicity / Single Runtime Weight Authority / RecoveryRequired Failure Boundary / No Same-Operation Legacy Fallback / C6·C7 Canary Evidence Promotion Seal

> Admission parent SSOT: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C6` physical PASS  
> Execution parity parent SSOT: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C7` physical PASS  
> Compile closure parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C6-D1`  
> Current parent runtime at C8 entry: wave-built resident weight Layer 2 / generation 2, hidden Layer 3 / generation 3  
> C8 physical promotion canary: source Layer 2 -> target Layer 3  
> Current runtime decoder-weight transport after C8 PASS: `decoder-weight-atlas-wave`  
> Legacy full-layer loader: historical/reference/diagnostic only  
> Layer-3 forward in C8: `BLOCKED`  
> Progressive multi-layer loop: `BLOCKED / C9`  
> Proof ledger: `HOLD`

---

# 1. Purpose

C6 proved a real Layer1 -> Layer2 destructive runtime rebind using C4 planning and C5 staging with no legacy target fallback.

C7 proved that the C6-adopted wave-built Layer2 block executes the real decoder route and produces exact Hidden3 full-surface parity with a private legacy-loader oracle while preserving the wave-built block as the only runtime authority.

C8 promotes those canary facts into the current generalized sequential decoder-weight rebind authority.

Canonical invariant:

```text
Resident weight Layer N
+ completed execution of Layer N
+ exact output Hidden N+1
        ↓
C4 target N+1 plan
        ↓
exclusive destructive source extraction
        ↓
source owner release + same-device completion wait
        ↓
VacantForRebind
        ↓
C5 target N+1 wave staging
        ↓
exact nine-role complete block
        ↓
BaseTrainLayerWeightResidencySlot::adopt()
        ↓
Resident weight Layer N+1
```

No same-operation legacy fallback is allowed.

---

# 2. Authority change

Before C8:

```text
historical generalized runtime rebind = checkpoint-resolved-full-layer-loader
wave planner                          = admitted
wave private build                    = admitted
wave runtime adoption                 = Layer1 -> Layer2 canary
wave execution parity                 = Layer2 canary
```

After physical C8 PASS:

```text
canonical generalized runtime rebind  = decoder-weight-atlas-wave
legacy generalized runtime authority  = RETIRED
legacy loader implementation          = RETAINED_NON_AUTHORITY
```

No runtime caller may dynamically choose between two equal transport authorities.

---

# 3. Physical C8 canary

C7 PASS leaves:

```text
weight state             = Resident
weight layer             = 2
weight generation        = 2
hidden layer             = 3
hidden generation        = 3
active weight leases     = 0
active hidden leases     = 0
resident decoder blocks  = 1
resident weight tensors  = 9
```

Therefore C8 physical promotion is exactly:

```text
source layer = 2
target layer = 3
max rebind steps = 1
```

Required checkpoint condition:

```text
num_hidden_layers > 3
```

C8 ends after Layer3 weight adoption. Layer3 forward remains zero.

---

# 4. State ownership SSOT

Runtime weight owner:

```text
BaseTrainLayerWeightResidencySlot
```

Runtime hidden owner:

```text
LayerHiddenAuthoritySlot
```

Checkpoint inventory:

```text
BaseTrainAtlasWave02R5CheckpointTensorSetAuthority
```

C4 owns decoder-weight transport planning.

C5 owns checkpoint read/decode, host ownership accounting, lane decode, device material commit, nine-role completeness and private block construction.

C8 owns transaction orchestration and current transport authority selection.

No second runtime weight registry, hidden registry, checkpoint parser, or block owner is permitted.

---

# 5. Canonical public rebind symbol

After C8 the current semantic public entry point is:

```rust
pub fn rebind_resident_decoder_layer(
    runtime: &R6R6LiveBodySession,
    source_layer_index: u32,
    target_layer_index: u32,
    source_completion: &CanonicalLayerExecutionCompletionBinding,
    input_hidden_pointer: &LayerHiddenAuthorityPointer,
    policy: &DecoderWeightAtlasWavePackingPolicy,
    transport_authority: &CanonicalDecoderWeightTransportAuthority,
) -> Result<CanonicalDecoderWeightWaveRebindExecution>
```

This symbol belongs to the C8 wave module.

The historical full-layer implementation is explicitly renamed:

```text
rebind_resident_decoder_layer_legacy_full_loader_reference(...)
```

Historical C1-C4 reproduction may use the explicit legacy name. Current runtime advancement may not.

---

# 6. Legacy loader scopes

Remaining direct legacy loader call sites must be classified only as:

```text
historical parent gate
reference oracle
diagnostic fixture
```

The canonical C8 module must have zero call edges to:

```text
load_base_train_atlas_wave_02_r6_r7_decoder_block_weights(...)
rebind_resident_decoder_layer_legacy_full_loader_reference(...)
```

No fallback helper, feature-flag fallback, catch-all fallback, or debug fallback may redirect a failed wave transaction to the legacy loader.

---

# 7. Historical C4 transport truth is preserved

C4 historically sealed:

```text
planned_transport_mode = decoder-weight-atlas-wave
active_transport_mode  = checkpoint-resolved-full-layer-loader
```

Those values remain historical evidence and are not rewritten.

C8 introduces a separate current runtime authority:

```rust
pub struct CanonicalDecoderWeightTransportAuthority {
    pub schema_version: u32,
    pub authority_epoch: u64,
    pub active_transport_mode: String,
    pub planner_patch_id: String,
    pub staging_patch_id: String,
    pub promotion_patch_id: String,
    pub legacy_runtime_loader_retired: bool,
    pub same_operation_legacy_fallback_allowed: bool,
    pub authority_digest: String,
}
```

Required values:

```text
authority_epoch                       = 1
active_transport_mode                 = decoder-weight-atlas-wave
planner_patch_id                      = ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C4
staging_patch_id                      = ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C5
promotion_patch_id                    = ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C8
legacy_runtime_loader_retired         = true
same_operation_legacy_fallback_allowed = false
```

---

# 8. C4 planner remains SSOT

C8 reuses:

```rust
plan_decoder_weight_atlas_waves(
    &runtime.checkpoint,
    target_layer_index,
    policy,
)
```

C8 must not duplicate the nine-role registry, checkpoint span resolution, shape validation, byte accounting, packing algorithm, lane assignment, or canonical commit ordering.

C8 binds a structural projection:

```rust
pub struct CanonicalDecoderWeightWavePlanBinding {
    pub schema_version: u32,
    pub target_layer: u32,
    pub plan_digest: String,
    pub plan_wave_collection_digest: String,
    pub role_count: u32,
    pub lane_count: u32,
    pub wave_count: u32,
    pub max_host_transient_bytes: u64,
    pub max_parallel_decode_workers: u32,
    pub max_lanes_per_wave: u32,
    pub mega_atlas_allowed: bool,
    pub cross_wave_payload_overlap_allowed: bool,
    pub structural_binding_digest: String,
}
```

C8 does not copy C4 historical `active_transport_mode` into current authority.

---

# 9. C5 staging becomes canonical builder

C8 reuses exactly:

```rust
execute_layer_weight_build_staging_private_candidate(...)
```

C8 must not duplicate checkpoint seek/read, F16/BF16/F32 decode, host ownership ledger, scoped parallel decode, single-writer material commit, per-wave device completion fence, nine-role seal, or private block construction.

Required staging facts:

```text
roles                        = 9
lanes                        = 9
wave count                   = C4 plan-derived
checkpoint reads             = 9
decodes                      = 9
material commits             = 9
source owner releases        = 9
decoded owner releases       = 9
completion fence waits       = plan.wave_count
complete nine-role seal      = 1
runtime publication          = 0
runtime weight authority     = 0
cross-wave overlap           = 0
mega atlas                   = 0
gpu weight payload readback  = 0
observed host peak           <= C4 budget
```

---

# 10. Generalized source execution completion

C8 uses a typed binding:

```rust
pub struct CanonicalLayerExecutionCompletionBinding {
    pub schema_version: u32,
    pub source_layer_index: u32,
    pub source_weight_pointer_digest: String,
    pub source_weight_generation: u64,
    pub source_weight_transition_serial: u64,
    pub source_block_identity_digest: String,
    pub execution_evidence_digest: String,
    pub final_receipt_digest: String,
    pub output_hidden_layer_index: u32,
    pub output_hidden_pointer_digest: String,
    pub output_hidden_generation: u64,
    pub output_hidden_buffer_identity_digest: String,
    pub output_hidden_completion_token_digest: String,
    pub output_hidden_shape_bqh: [u32; 3],
    pub mismatch_count: u64,
    pub non_finite_count: u64,
    pub payload_readback_count: u64,
    pub pass: bool,
    pub binding_digest: String,
}
```

The binding must cross-check actual execution evidence against current runtime pointers.

For physical C8, source authority is the C7 wave candidate execution, never the C7 legacy oracle.

Required:

```text
source selected layer           = 2
source weight pointer           = current Weight2 pointer
source weight generation        = 2
source block identity           = current resident block
execution evidence              = C7 candidate evidence
output hidden pointer           = published Hidden3 pointer
output hidden generation        = 3
output hidden buffer identity   = current Hidden3 buffer identity
output hidden completion token  = current Hidden3 completion token
output BQH                      = current Hidden3 BQH
mismatch                        = 0
nonfinite                       = 0
payload readback                = 0
```

A digest-shaped 64-character string alone is not sufficient evidence.

---

# 11. Hidden lineage

At canonical rebind entry:

```text
input hidden layer == target layer
```

because source Layer N execution produces Hidden N+1 and target weights are Layer N+1.

Hidden generation is not derived from layer number as an independent authority.

The exact hidden pointer must equal the source completion binding output, including pointer digest, generation, buffer identity, completion token and BQH shape.

---

# 12. Checked monotonicity

Canonical layer rule:

```text
target_layer = source_layer.checked_add(1)
```

Canonical generation rule:

```text
target_generation = source_generation.checked_add(1)
```

These relations are checked independently.

C8 may not use layer index equality as the primary generation authority.

Physical fixture:

```text
source layer       = 2
source generation  = 2
target layer       = 3
target generation  = 3
```

---

# 13. Pre-destructive preflight

Before exclusive source extraction, C8 must complete all checks that require no target payload read:

```text
current transport authority == decoder-weight-atlas-wave
source state == Resident
source layer exact
source pointer exact
source execution completion exact
active source weight leases == 0
resident block count == 1
resident tensor count == 9
slot strong owner count == 1
input hidden exact completion binding
active hidden leases == 0
target range valid
C4 policy valid
C4 target plan constructed
C4 role count == 9
C4 lane count == 9
C4 plan digest sealed
C4 plan-wave collection digest sealed
target tensor provenance derived
operation id derived
```

No C5 checkpoint payload read is permitted before the vacancy boundary.

---

# 14. Exclusive destructive boundary

C8 uses the existing rollback-safe primitive:

```rust
begin_exclusive_destructive_rebind(...)
```

The canonical path must not use the older split:

```text
arm_eviction()
take_armed_bundle()
```

Before successful exclusive extraction, failure leaves source Resident and does not enter RecoveryRequired.

The operational destructive boundary is successful exclusive source bundle extraction from the residency slot.

---

# 15. Source release and vacancy

After exclusive extraction:

```text
validate source bundle layer and identity
release source Rust owner
same-device device.poll(Wait)
mark VacantForRebind
```

No claim of immediate physical VRAM reclamation is made from Rust drop alone.

At vacancy:

```text
resident block count     = 0
resident tensor count    = 0
slot strong owner count  = 0
active weight leases     = 0
hidden pointer           = unchanged
```

Only after this observation may C5 target payload staging begin.

---

# 16. Post-destructive failure ownership

After successful exclusive source extraction, every failure before successful adoption is destructive.

Examples:

```text
source completion wait failure
vacancy transition failure
C5 checkpoint read failure
C5 decode failure
material construction failure
wave fence failure
nine-role seal failure
candidate validation failure
target provenance failure
runtime adopt failure
```

Required response:

```text
mark RecoveryRequired
return failure
```

Forbidden:

```text
source rollback
source rebuild
legacy target reload
same-operation legacy fallback
```

If RecoveryRequired escalation itself fails, the error must report both the original destructive failure and recovery escalation failure.

---

# 17. Target provenance

C8 reuses:

```rust
seal_decoder_block_tensor_set_authority_digest(...)
```

Target keys and tensor identity digests are taken from the exact nine C4 target spans in canonical registry order.

The adopted Layer3 pointer must bind the Layer3 target tensor-set digest and exact target identity list.

No legacy full-layer load may be executed merely to produce provenance.

---

# 18. Atomic adoption

Only after C5 has produced one complete sealed target block may C8 call:

```text
BaseTrainLayerWeightResidencySlot::adopt(...)
```

Required candidate facts:

```text
selected layer                       = target layer
actual decoder block instances       = 1
checkpoint payload reads             = 9
checkpoint weight uploads            = 9
module identity digest               = sealed
runtime LoRA set                      = current canonical block construction result
trainable LoRA slot count             = 0
```

After adoption:

```text
state                        = Resident
resident layer               = target layer
residency generation         = source generation + 1
resident decoder blocks      = 1
resident weight tensors      = 9
slot strong owners           = 1
active execution leases      = 0
last execution completion    = source completion binding digest
```

---

# 19. Single runtime weight authority

Runtime authority waveform:

```text
source Resident : blocks=1 tensors=9
Vacant          : blocks=0 tensors=0
target Resident : blocks=1 tensors=9
```

Required:

```text
peak runtime resident block authority = 1
runtime source-target authority overlap = 0
```

C5 staging is construction authority, not runtime residency authority.

---

# 20. Hidden immutability

C8 is a weight rebind gate only.

Before and after canonical 2 -> 3 rebind require exact equality of the Hidden3 pointer and hidden slot counts.

Required final hidden state:

```text
hidden layer       = 3
hidden generation  = 3
hidden pointer     = unchanged
active hidden lease count = 0
```

C8 produces no Hidden4.

---

# 21. No target forward or prefetch

C8 target Layer3 forward count is zero.

Forbidden:

```text
Layer3 input norm
Layer3 QKV
Layer3 Headwise
Layer3 OProj
Layer3 MLP
Hidden4 commit
Layer4 checkpoint prefetch
Layer4 plan execution
all-layer preload
parallel multi-layer staging
```

Progressive execution belongs to C9.

---

# 22. C6·C7 promotion evidence

The C8 gate consumes one same-invocation C7 parent session, which already owns its C6 parent.

Promotion evidence binds actual:

```text
C6 transaction receipt digest
C7 final receipt digest
C7 wave-candidate execution evidence digest
C7 dispatch parity evidence digest
C7 Hidden3 parity evidence digest
C7 published Hidden3 pointer digest
C7 mismatch count = 0
C7 nonfinite count = 0
C7 payload readback = 0
```

The gate must not hardcode `c6_pass=true` or `c7_pass=true` as a substitute for real parent evidence.

No second C7 session may be run after one parent has already been obtained.

---

# 23. Current transport authority epoch

C8 authority epoch is:

```text
canonical decoder weight transport authority epoch = 1
```

This epoch is independent from historical C4 plan schema.

Logging-only changes do not bump it. A future semantic transport authority change must.

---

# 24. CLI contract

```text
--require-r6-r9-c8-canonical-decoder-weight-wave-loader true
--r6-r9-c8-source-layer 2
--r6-r9-c8-target-layer 3
--r6-r9-c8-max-rebind-steps 1
--require-r6-r9-c8-c6-c7-promotion-evidence true
--require-r6-r9-c8-current-wave-transport-authority true
--require-r6-r9-c8-generalized-source-completion-binding true
--require-r6-r9-c8-c4-plan-binding true
--require-r6-r9-c8-c5-canonical-staging true
--require-r6-r9-c8-exclusive-destructive-begin true
--require-r6-r9-c8-vacant-before-target-payload true
--require-r6-r9-c8-generation-monotonicity true
--require-r6-r9-c8-single-runtime-weight-authority true
--require-r6-r9-c8-recovery-after-destructive-failure true
--require-r6-r9-c8-legacy-runtime-loader-retired true
--allow-r6-r9-c8-same-operation-legacy-fallback false
--allow-r6-r9-c8-source-rebuild false
--allow-r6-r9-c8-target-forward false
--allow-r6-r9-c8-hidden-mutation false
--allow-r6-r9-c8-next-layer-prefetch false
--allow-r6-r9-c8-all-layer-preload false
```

Existing C4 packing policy keys are reused. C8 does not create a second hidden byte-budget policy.

---

# 25. Implementation surface

Semantic files:

```text
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r7_layer_weight_residency.rs
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r9_c8_canonical_decoder_weight_wave_rebind.rs
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r9_forward_coordinator.rs
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r6_r9_forward_coordinator_gate.rs
specs/cli/ash_basetrain_atlas_wave_02_r6_r9.args
```

No WGSL semantic change is required.

No JS/TS/Python canonical runtime path is introduced.

---

# 26. Static closure

Before physical run require:

```text
canonical public `rebind_resident_decoder_layer` = C8 wave implementation
legacy generalized rebind explicit historical/reference name = present
canonical call graph to legacy loader = 0
canonical failure call graph to legacy loader = 0
historical coordinator explicitly calls legacy historical helper = present
C4 planner reuse = present
C5 staging executor reuse = present
second checkpoint parser = absent
second nine-role registry = absent
second staging implementation = absent
typed generalized source completion binding = present
checked source layer + 1 = present
checked source generation + 1 = present
exclusive destructive begin = present
split arm/take in canonical path = absent
source owner drop before vacancy = present
same-device completion wait before vacancy = present
vacancy before C5 payload staging = present
wave count compared with plan = present
roles = 9
lanes = 9
completion fences = plan wave count
observed host peak <= C4 budget
shared target provenance helper = present
adopt only after complete candidate = present
hidden pointer exact unchanged = present
target Layer3 forward = 0
next-layer prefetch = 0
all-layer preload = 0
runtime authority overlap = 0
WGSL semantic changes = 0
```

---

# 27. Physical success facts

Expected C8 physical run:

```text
source_layer                         = 2
target_layer                         = 3
source_generation                    = 2
target_generation                    = 3
promotion_evidence_bound             = 1
canonical_wave_transport_authority   = 1
legacy_runtime_loader_retired        = 1
source_completion_bound              = 1
exclusive_destructive_eviction       = 1
vacant_boundary                      = 1
staging_after_vacancy                = 1
roles                                = 9
lanes                                = 9
plan_waves                           = plan-derived
checkpoint_reads                     = 9
decodes                              = 9
material_commits                     = 9
source_owner_releases                = 9
decoded_owner_releases               = 9
wave_completion_fences               = plan_waves
complete_nine_role_seal              = 1
runtime_adopt                        = 1
runtime_resident_blocks              = 1
runtime_resident_weight_tensors      = 9
runtime_authority_overlap            = 0
legacy_runtime_loader_invocations    = 0
same_operation_legacy_fallback       = 0
source_rebuild                       = 0
hidden_pointer_unchanged             = 1
target_forward                       = 0
next_layer_prefetch                  = 0
gpu_weight_readback                  = 0
recovery_required_transition         = 0 on success path
```

Success does not physically exercise fault-injected RecoveryRequired branches.

---

# 28. Expected terminal line

```text
[r6-r9-c8-canonical-decoder-weight-wave-loader]
source_layer=2
target_layer=3
source_generation=2
target_generation=3
promotion_evidence_bound=1
canonical_wave_transport_authority=1
legacy_runtime_loader_retired=1
source_completion_bound=1
exclusive_destructive_eviction=1
vacant_boundary=1
staging_after_vacancy=1
plan_waves=<plan>
lanes=9
roles=9
checkpoint_reads=9
decodes=9
material_commits=9
source_owner_release=9
decoded_owner_release=9
wave_fence_waits=<plan>
complete_nine_role_seal=1
runtime_adopt=1
runtime_resident_blocks=1
runtime_resident_weight_tensors=9
runtime_authority_overlap=0
legacy_runtime_loader=0
same_operation_legacy_fallback=0
source_rebuild=0
hidden_layer=3
hidden_generation=3
hidden_pointer_unchanged=1
target_forward=0
next_layer_prefetch=0
gpu_weight_readback=0
recovery_required_transition=0
transport_authority_digest=<digest>
promotion_digest=<digest>
source_completion_digest=<digest>
c4_plan_digest=<digest>
c5_staging_digest=<digest>
target_tensor_set_digest=<digest>
adopted_pointer_digest=<digest>
proof_ledger=HOLD
```

---

# 29. PASS meaning

C8 PASS proves:

```text
C6 runtime-adoption evidence and C7 execution-parity evidence are bound
current decoder-weight transport authority is decoder-weight-atlas-wave
canonical generalized rebind works beyond the original canary through 2 -> 3
source completion is evidence-bound
C4 remains single planner
C5 remains single staging implementation
source runtime authority is removed before target payload staging
Layer3 is built and atomically adopted through the existing runtime SSOT
weight generation advances 2 -> 3
Hidden3 remains unchanged
legacy full-layer target loader is absent from canonical transaction
same-operation fallback is absent
runtime weight authority remains single
post-destructive failure ownership is RecoveryRequired
```

C8 PASS does not prove:

```text
Layer3 forward numerical parity
Hidden4 correctness
all-layer progressive execution
long-horizon memory stability
physical VRAM reclamation timing
performance improvement
prefetch safety
final RMSNorm
LM head
forward loss
backward
optimizer
production inference
fault-injected recovery branches
```

---

# 30. Admission after physical PASS

```text
R6-R6 live body                                 = ADMITTED
R6-R7 historical layer residency                = ADMITTED_HISTORY
R6-R8 Layer1 forward                            = ADMITTED
R6-R9-C4 decoder-weight wave planner            = ADMITTED
R6-R9-C4-D1 plan collection closure             = ADMITTED
R6-R9-C5 wave staging/build                      = ADMITTED
R6-R9-C6 Layer1 -> Layer2 wave rebind canary     = ADMITTED
R6-R9-C7 Layer2 wave-built execution parity      = ADMITTED
R6-R9-C8 canonical generalized wave loader       = ADMITTED on physical PASS

Current decoder-weight transport authority       = DECODER_WEIGHT_ATLAS_WAVE
Legacy generalized runtime loader authority      = RETIRED
Legacy historical/reference loader               = RETAINED_NON_AUTHORITY
Progressive N-layer advancement                   = BLOCKED / C9
Long-horizon residency ledger                     = BLOCKED / C10
Final RMSNorm / LM head                           = BLOCKED
Forward loss                                      = BLOCKED
Backward                                          = BLOCKED
Optimizer                                         = BLOCKED
Production inference                              = BLOCKED
Proof ledger                                      = HOLD
```

---

# 31. Next boundary

```text
ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C9

Progressive N-Layer Wave Advancement /
Canonical C8 Rebind Authority Loop /
Resident Layer N Execution Lease /
Hidden N+1 Commit /
Canonical Wave Rebind N -> N+1 /
Checkpoint Layer Count Bound /
No Layer-Specific Canary Branch /
No Legacy Runtime Loader /
Per-Layer Generation·Pointer Lineage /
Per-Step Dispatch·Parity Evidence /
Zero Weight Payload Readback /
Final Decoder Layer Completion Seal
```

---

# Architecture seal

> C8 promotes the physically proven C6 runtime-adoption canary and C7 execution-parity canary into one current decoder-weight transport authority. The canonical generalized `rebind_resident_decoder_layer` no longer resolves target weights through the legacy full-layer loader: it binds completed source execution, constructs the existing C4 target plan, crosses the rollback-safe exclusive destructive boundary, publishes VacantForRebind before any target payload read, executes the existing C5 wave staging implementation, atomically adopts one complete target decoder block through the existing residency SSOT, advances weight generation by exactly one, leaves the current hidden state untouched, and treats every post-destructive failure as RecoveryRequired with no same-operation legacy fallback. Historical legacy gates and the C7 reference oracle retain the old loader only under explicit non-authoritative names and do not compete with the C8 runtime SSOT.
