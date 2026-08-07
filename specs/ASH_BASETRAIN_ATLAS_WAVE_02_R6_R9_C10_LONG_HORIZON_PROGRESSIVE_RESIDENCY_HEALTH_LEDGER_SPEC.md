# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C10

## Long-Horizon Progressive Residency / Repeated Wave Rebind Health Ledger / Per-Layer Host Peak Tracking / GPU Residency Pressure Envelope / Generation Drift Detection / Pointer Lineage Continuity Audit / Wave Count Distribution / Checkpoint Read·Decode·Material Commit Ledger / Destructive Boundary Recovery Audit / No Long-Horizon Authority Leak / Decoder Completion Health Seal

> Admission parent SSOT: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C9` physical PASS  
> C9 observed fixture: checkpoint decoder layers `22`, progressive start layer `3`, execution steps `19`, wave rebind steps `18`  
> Current decoder-weight transport authority: `decoder-weight-atlas-wave`  
> Runtime weight owner: `BaseTrainLayerWeightResidencySlot`  
> Runtime hidden owner: `LayerHiddenAuthoritySlot`  
> Planner SSOT: C4 `DecoderWeightAtlasWavePlan`  
> Staging/build SSOT: C5 `LayerWeightBuildStagingSlot`  
> Rebind transaction SSOT: C8 `rebind_resident_decoder_layer(...)`  
> Progressive execution SSOT: C9 `advance_resident_decoder_to_checkpoint_end(...)`  
> Final decoder state parent: Weight Layer `21`, Hidden Layer `22` in the current physical fixture  
> Final RMSNorm / LM head / logits / loss / backward / optimizer: `BLOCKED`  
> Proof ledger: `HOLD`

---

# 1. Purpose

C9 physically proved that one admitted runtime can execute the remaining decoder stack to the checkpoint boundary while repeatedly performing destructive decoder-weight wave rebinds.

C10 does **not** add another decoder execution algorithm and does **not** add another weight transport.

C10 converts the C9 progressive run into a long-horizon health record answering the questions C9 deliberately did not own:

```text
Did every repeated rebind stay within the declared host-transient budget?
Did runtime weight authority remain singular for the whole run?
Did any generation drift from its independent monotonic rule?
Did any pointer lineage break, repeat, or skip?
Did source -> armed -> vacant -> adopted transitions remain continuous?
Did wave counts remain plan-derived and internally consistent?
Did checkpoint read/decode/material-commit counts remain exact per rebind?
Did any payload/readback/fallback/legacy path leak into the long loop?
Did destructive failure ownership remain structurally routed to RecoveryRequired?
Did the final decoder completion state remain healthy after the whole sequence?
```

C10 is therefore an **audit and health-ledger patch**, not a numerical-model patch.

---

# 2. What C10 must not claim

C10 must not turn currently unavailable observations into invented measurements.

In particular, the current runtime does **not** expose an authoritative GPU allocator/heap byte counter for decoder-weight residency.

Therefore C10 must not print or seal fabricated values such as:

```text
actual VRAM bytes used
actual GPU heap free bytes
physical VRAM release latency
GPU fragmentation percentage
allocator pressure percentage
```

unless a later separately admitted allocator telemetry source is introduced.

C10's current GPU residency pressure envelope is based on **observable runtime authority cardinality and transport behavior**:

```text
resident decoder block count
resident checkpoint weight tensor count
slot strong-owner count
active execution lease count
vacancy cardinality
runtime authority overlap count
staging runtime-authority count
mega-atlas count
cross-wave payload-overlap count
weight payload readback count
C4 planned payload/decoded/transient byte surfaces
```

These are valid pressure indicators but are not equivalent to direct GPU heap telemetry.

---

# 3. C10 health verdict model

C10 uses deterministic structural verdicts, not an arbitrary weighted health score.

Recommended enum:

```rust
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum R6R9C10HealthVerdict {
    Healthy,
    Unhealthy,
    EvidenceInsufficient,
}
```

Rules:

```text
Healthy
    = all required evidence exists
    + all invariant counters are exact
    + all drift/leak/overrun counts are zero

Unhealthy
    = required evidence exists
    + at least one invariant is violated

EvidenceInsufficient
    = a requested health dimension is not actually observable
```

Direct GPU heap byte health remains `EvidenceInsufficient` in C10 unless new physical telemetry is explicitly added.

The overall C10 admission can still be `Healthy` for the **defined observable envelope** while explicitly reporting allocator-byte telemetry as unavailable.

---

# 4. Parent physical evidence

C10 consumes one same-invocation C9 parent session.

The current physically observed C9 fixture reported:

```text
checkpoint_layers=22
start_weight_layer=3
start_weight_generation=3
start_hidden_layer=3
start_hidden_generation=3
execution_steps=19
rebind_steps=18
final_weight_layer=21
final_weight_generation=21
final_hidden_layer=22
final_hidden_generation=22
hidden_commits=19
checkpoint_reads=162
decodes=162
material_commits=162
wave_fence_waits=54
per_step_dispatch_evidence=19
per_step_parity_evidence=19
mismatch=0
nonfinite=0
payload_readback=0
weight_payload_readback=0
runtime_authority_overlap=0
progressive_legacy_runtime_loader=0
same_operation_legacy_fallback=0
post_final_rebind=0
next_layer_prefetch=0
```

These numbers are current physical observations, not generalized constants.

C10 must derive its expected counts from the actual C9 parent:

```text
E = C9.execution_step_count
R = C9.rebind_step_count
L = checkpoint_layer_count
```

No C10 control-flow condition may hard-code `22`, `19`, `18`, `162`, or `54`.

---

# 5. Why C9 requires one small evidence-retention extension

C9 already verifies and aggregates the major success-path counts, but it intentionally does not retain every C8/C5 detail needed by a long-horizon auditor.

For example, the current C9 step receipt records a rebind receipt digest but does not retain:

```text
C5 observed_peak_host_transient_owned_bytes
C4 planned_peak_wave_transient_host_bytes
C4 sum_source_payload_bytes
C4 sum_decoded_f32_bytes
armed transition serial
vacant transition serial
adopted transition serial
vacancy count snapshot
post-adopt count snapshot
```

C10 must not reconstruct those values later from guessed formulas or scrape debug JSON from disk.

The values must be retained **same invocation, at the moment the C8 rebind returns them**.

---

# 6. No C10 -> C9 circular type dependency

C9 must not import C10 types merely to satisfy C10 auditing.

Instead, C9 receives a neutral evidence-retention extension whose semantics belong to the progressive runtime itself.

Recommended internal/exported evidence type in the C9 module:

```rust
pub struct R6R9C9RebindHealthObservation {
    pub schema_version: u32,
    pub step_ordinal: u32,
    pub source_layer: u32,
    pub target_layer: u32,
    pub source_generation: u64,
    pub target_generation: u64,

    pub source_pointer_digest: String,
    pub source_transition_serial: u64,
    pub armed_pointer_digest: String,
    pub armed_transition_serial: u64,
    pub vacant_pointer_digest: String,
    pub vacant_transition_serial: u64,
    pub adopted_pointer_digest: String,
    pub adopted_transition_serial: u64,

    pub source_previous_pointer_digest: Option<String>,
    pub armed_previous_pointer_digest: Option<String>,
    pub vacant_previous_pointer_digest: Option<String>,
    pub adopted_previous_pointer_digest: Option<String>,

    pub plan_digest: String,
    pub packing_policy_digest: String,
    pub wave_count: u32,
    pub lane_count: u32,
    pub role_count: u32,

    pub sum_source_payload_bytes: u64,
    pub sum_decoded_f32_bytes: u64,
    pub planned_peak_wave_source_payload_bytes: u64,
    pub planned_peak_wave_decoded_f32_bytes: u64,
    pub planned_peak_wave_transient_host_bytes: u64,
    pub max_host_transient_bytes: u64,
    pub observed_peak_host_transient_owned_bytes: u64,

    pub checkpoint_read_count: u32,
    pub decode_count: u32,
    pub material_commit_count: u32,
    pub source_owner_release_count: u32,
    pub decoded_owner_release_count: u32,
    pub wave_fence_wait_count: u32,

    pub source_runtime_counts: BaseTrainLayerWeightResidencyCounts,
    pub vacant_runtime_counts: BaseTrainLayerWeightResidencyCounts,
    pub adopted_runtime_counts: BaseTrainLayerWeightResidencyCounts,

    pub staging_runtime_weight_authority_count: u32,
    pub runtime_authority_overlap_count: u32,
    pub cross_wave_payload_overlap_count: u32,
    pub mega_atlas_create_count: u32,
    pub gpu_weight_payload_readback_count: u32,
    pub legacy_runtime_loader_invocation_count: u32,
    pub same_operation_legacy_fallback_count: u32,
    pub source_rebuild_count: u32,
    pub recovery_required_transition_count: u32,

    pub pass: bool,
    pub observation_digest: String,
}
```

Exact naming may follow repository conventions. Ownership and evidence scope are mandatory.

---

# 7. C8 result must expose the real transition chain

The current C8 transaction already has all of these objects during the operation:

```text
source_pointer
armed_pointer
vacant_pointer
adopted_pointer
source_counts
vacant_counts
target_counts
plan
staging_receipt
rebind_receipt
```

C10 must not infer missing transition serials from digests.

Recommended minimal internal extension:

```rust
pub struct CanonicalDecoderWeightWaveRebindExecution {
    pub source_pointer: BaseTrainLayerWeightResidencyPointer,
    pub armed_pointer: BaseTrainLayerWeightResidencyPointer,
    pub vacant_pointer: BaseTrainLayerWeightResidencyPointer,
    pub adopted_pointer: BaseTrainLayerWeightResidencyPointer,
    pub source_counts: BaseTrainLayerWeightResidencyCounts,
    pub vacant_counts: BaseTrainLayerWeightResidencyCounts,
    pub adopted_counts: BaseTrainLayerWeightResidencyCounts,
    pub transport_authority: CanonicalDecoderWeightTransportAuthority,
    pub plan: DecoderWeightAtlasWavePlan,
    pub plan_binding: CanonicalDecoderWeightWavePlanBinding,
    pub staging_receipt: LayerWeightBuildStagingReceipt,
    pub rebind_receipt: CanonicalDecoderWeightWaveRebindReceipt,
}
```

If retaining the full C4 plan is considered too heavy, retain a sealed receipt-only plan health projection instead. Do not re-plan later.

This is evidence retention only. C8 transport semantics remain unchanged.

---

# 8. C9 execution object retention

Extend only the in-memory C9 execution object:

```rust
pub struct R6R9C9ProgressiveNLayerExecution {
    ... existing fields ...
    pub rebind_health_observations: Vec<R6R9C9RebindHealthObservation>,
}
```

Required:

```text
rebind_health_observations.len() == C9.rebind_step_count
```

C9's already-admitted terminal semantics and PASS token remain unchanged unless a true semantic execution change is made.

C10 consumes the vector after C9 PASS.

---

# 9. Per-rebind host transient health

C5 already owns the authoritative observed host peak:

```rust
LayerWeightBuildStagingReceipt::observed_peak_host_transient_owned_bytes
```

C4 owns the declared policy budget:

```rust
DecoderWeightAtlasWavePlan::max_host_transient_bytes
```

C4 also exposes the planner estimate:

```rust
planned_peak_wave_transient_host_bytes
```

For every progressive rebind C10 records:

```text
observed host peak
planner peak estimate
policy max host budget
budget headroom
planner-estimate headroom/overrun
```

Checked formulas:

```text
budget_headroom_bytes
    = max_host_transient_bytes - observed_peak_host_transient_owned_bytes
      only after observed <= budget

planner_peak_delta
    = signed relation between observed and planned peak
```

No floating-point percentage is required.

---

# 10. Host peak admission rules

Per rebind require:

```text
observed_peak_host_transient_owned_bytes > 0
observed_peak_host_transient_owned_bytes <= max_host_transient_bytes
planned_peak_wave_transient_host_bytes <= max_host_transient_bytes
```

C10 additionally audits planner conservatism:

```text
host_plan_overrun_count
    = count(observed_peak_host_transient_owned_bytes
            > planned_peak_wave_transient_host_bytes)
```

Required for C10 health PASS:

```text
host_plan_overrun_count = 0
```

If this count is non-zero, C10 must report `Unhealthy`; it must not silently widen the planner estimate.

---

# 11. Host peak long-horizon ledger

Recommended aggregate:

```rust
pub struct R6R9C10HostPeakLedger {
    pub schema_version: u32,
    pub rebind_count: u32,
    pub per_rebind_observation_digests: Vec<String>,
    pub min_observed_peak_host_transient_bytes: u64,
    pub max_observed_peak_host_transient_bytes: u64,
    pub sum_observed_peak_host_transient_bytes: u64,
    pub min_budget_headroom_bytes: u64,
    pub max_policy_budget_bytes: u64,
    pub max_planned_peak_wave_transient_bytes: u64,
    pub host_budget_overrun_count: u32,
    pub host_plan_overrun_count: u32,
    pub pass: bool,
    pub ledger_digest: String,
}
```

`sum_observed_peak_host_transient_bytes` is an audit sum, **not simultaneous memory usage**.

Do not present the sum as peak process memory.

---

# 12. Wave-count distribution

C10 derives wave cardinality from every retained C4 plan.

Recommended deterministic bucket:

```rust
pub struct R6R9C10WaveCountBucket {
    pub wave_count: u32,
    pub rebind_occurrence_count: u32,
}
```

Aggregate:

```rust
pub struct R6R9C10WaveDistributionLedger {
    pub schema_version: u32,
    pub rebind_count: u32,
    pub min_wave_count: u32,
    pub max_wave_count: u32,
    pub sum_wave_count: u64,
    pub histogram: Vec<R6R9C10WaveCountBucket>,
    pub total_wave_fence_wait_count: u64,
    pub wave_fence_count_mismatch_count: u32,
    pub pass: bool,
    pub ledger_digest: String,
}
```

Histogram buckets are sorted by ascending `wave_count` before sealing.

---

# 13. Current physical wave observation is not an authority

The current C9 physical run observed:

```text
18 rebinds
54 wave fence waits
```

which is consistent with the current fixture producing 3 waves per rebind.

C10 may print the resulting observed histogram:

```text
wave_count=3 occurrence_count=18
```

**only if the retained physical observations actually produce it**.

C10 must not require all future layers/checkpoints to have exactly three waves.

Required generalized relation:

```text
wave_fence_wait_count == plan.wave_count
```

per rebind.

---

# 14. Checkpoint read/decode/material-commit ledger

C5 currently guarantees for one decoder block:

```text
role_count = 9
checkpoint_payload_read_count = 9
decode_count = 9
material_commit_count = 9
source_owner_release_count = 9
decoded_owner_release_count = 9
```

C10 records these per rebind and aggregates them with checked arithmetic.

Recommended:

```rust
pub struct R6R9C10WeightTransportWorkLedger {
    pub schema_version: u32,
    pub rebind_count: u32,
    pub role_count_sum: u64,
    pub checkpoint_read_count: u64,
    pub decode_count: u64,
    pub material_commit_count: u64,
    pub source_owner_release_count: u64,
    pub decoded_owner_release_count: u64,
    pub wave_fence_wait_count: u64,
    pub expected_role_count_per_rebind: u32,
    pub count_mismatch_rebind_count: u32,
    pub pass: bool,
    pub ledger_digest: String,
}
```

---

# 15. Work-count exact formulas

Let:

```text
R = progressive rebind count
K = canonical decoder weight role count = 9
```

Then require:

```text
checkpoint_read_count      = R * K
decode_count               = R * K
material_commit_count      = R * K
source_owner_release_count = R * K
decoded_owner_release_count= R * K
```

All multiplication uses checked arithmetic.

C10 does not hide the parent C7 oracle's historical 9 reads inside these progressive runtime counts.

Parent reference activity remains separately scoped.

---

# 16. Generation drift detector

C10 replays the already-sealed C9 lineage as an audit operation only.

For every execution step:

```text
output_hidden_layer      = input_hidden_layer + 1
output_hidden_generation = input_hidden_generation + 1
weight_generation during execution = unchanged
```

For every rebind:

```text
target_weight_layer      = source_weight_layer + 1
target_weight_generation = source_weight_generation + 1
hidden pointer/generation during rebind = unchanged
```

Required aggregate:

```text
hidden_generation_drift_count = 0
weight_generation_drift_count = 0
layer_sequence_drift_count = 0
```

---

# 17. Generation remains independent from layer index

C10 must not reintroduce the retired canary assumption:

```text
generation == layer index
```

The current fixture happens to end with:

```text
Weight Layer21 / Gen21
Hidden Layer22 / Gen22
```

but C10 proves lineage from previous values, not equality to layer number.

Recommended diagnostic-only booleans:

```text
observed_final_weight_generation_equals_layer
observed_final_hidden_generation_equals_layer
```

These fields are informational and must not participate in PASS.

---

# 18. Weight transition-serial continuity

A successful C8 rebind currently has the exact state sequence:

```text
Resident source
    ↓ +1 transition serial
EvictionArmed
    ↓ +1
VacantForRebind
    ↓ +1
Resident target
```

C10 audits the actual pointers:

```text
armed.transition_serial   = source.transition_serial + 1
vacant.transition_serial  = armed.transition_serial + 1
adopted.transition_serial = vacant.transition_serial + 1
```

Use checked arithmetic in the auditor.

Required:

```text
transition_serial_drift_count = 0
```

C10 does not change the model-core transition implementation.

---

# 19. Weight pointer lineage continuity

The model-core pointer contract already includes:

```text
previous_pointer_digest
```

For each successful rebind require:

```text
armed.previous_pointer_digest   == source.pointer_digest
vacant.previous_pointer_digest  == armed.pointer_digest
adopted.previous_pointer_digest == vacant.pointer_digest
```

Across C9 steps require:

```text
previous step adopted weight pointer
    == next step execution weight pointer
```

Required:

```text
weight_pointer_lineage_break_count = 0
```

---

# 20. Hidden pointer lineage continuity

For every decoder execution require:

```text
output_hidden.previous_pointer_digest
    == input_hidden.pointer_digest
```

Across steps:

```text
step[i].output_hidden_pointer_digest
    == step[i+1].input_hidden_pointer_digest
```

During each rebind:

```text
Hidden pointer before rebind == Hidden pointer after rebind
```

Required:

```text
hidden_pointer_lineage_break_count = 0
hidden_mutation_during_rebind_count = 0
```

---

# 21. Pointer uniqueness audit

C10 detects stale-state reuse by tracking chronological persistent pointers.

For successful progression require no duplicate digest among:

```text
all committed Hidden pointers
all Resident weight pointers representing distinct generations
all armed pointers
all vacant pointers
all adopted pointers
```

Source pointers may equal a previous step's adopted pointer by design; that is continuity, not duplication error.

Therefore uniqueness is evaluated by **state-role lineage**, not by placing every appearance in one global set.

Recommended violations:

```text
unexpected_hidden_pointer_reuse_count
unexpected_weight_generation_pointer_reuse_count
unexpected_armed_pointer_reuse_count
unexpected_vacant_pointer_reuse_count
```

All must be zero.

---

# 22. Runtime authority cardinality envelope

C10 defines the observable GPU residency authority envelope from `BaseTrainLayerWeightResidencyCounts`.

For each ready/executing resident state:

```text
resident_decoder_block_count = 1
resident_checkpoint_weight_tensor_count = 9
slot_owned_strong_reference_count = 1
```

At the rebind vacancy sample:

```text
resident_decoder_block_count = 0
resident_checkpoint_weight_tensor_count = 0
slot_owned_strong_reference_count = 0
active_execution_lease_count = 0
```

After target adoption:

```text
resident_decoder_block_count = 1
resident_checkpoint_weight_tensor_count = 9
slot_owned_strong_reference_count = 1
active_execution_lease_count = 0
```

---

# 23. GPU residency pressure envelope receipt

Recommended:

```rust
pub struct R6R9C10GpuResidencyPressureEnvelope {
    pub schema_version: u32,
    pub direct_gpu_allocator_bytes_observable: bool,
    pub direct_gpu_allocator_byte_verdict: R6R9C10HealthVerdict,

    pub max_resident_decoder_block_count: u32,
    pub max_resident_checkpoint_weight_tensor_count: u32,
    pub max_slot_owned_strong_reference_count: u32,
    pub max_active_weight_execution_lease_count_at_rebind_boundary: u32,

    pub vacant_sample_count: u32,
    pub vacant_nonzero_block_count: u32,
    pub vacant_nonzero_tensor_count: u32,
    pub vacant_nonzero_strong_owner_count: u32,

    pub staging_runtime_weight_authority_count: u64,
    pub runtime_authority_overlap_count: u64,
    pub cross_wave_payload_overlap_count: u64,
    pub mega_atlas_create_count: u64,
    pub gpu_weight_payload_readback_count: u64,

    pub max_plan_sum_source_payload_bytes: u64,
    pub max_plan_sum_decoded_f32_bytes: u64,
    pub max_plan_peak_wave_decoded_f32_bytes: u64,

    pub pass: bool,
    pub envelope_digest: String,
}
```

Required current semantics:

```text
direct_gpu_allocator_bytes_observable = false
direct_gpu_allocator_byte_verdict = EvidenceInsufficient
```

This does not fail the observable authority-cardinality envelope.

---

# 24. No long-horizon runtime authority leak

Across the entire C9 progressive portion require aggregate:

```text
runtime_authority_overlap_count = 0
staging_runtime_weight_authority_count = 0
legacy runtime loader invocation count = 0
same-operation legacy fallback count = 0
source rebuild count = 0
cross-wave payload overlap count = 0
mega-atlas create count = 0
gpu weight payload readback count = 0
```

Any non-zero value makes C10 `Unhealthy`.

No warning-only downgrade is allowed.

---

# 25. Active lease leak audit

C10 checks execution boundaries rather than sampling arbitrary mid-dispatch moments.

Required:

```text
before each destructive rebind:
    active weight execution leases = 0
    active hidden execution leases = 0

at vacancy:
    active weight execution leases = 0

post adopt:
    active weight execution leases = 0

final decoder completion:
    active weight execution leases = 0
    active hidden execution leases = 0
```

Required aggregate:

```text
lease_boundary_leak_count = 0
```

---

# 26. C5 host-owner release audit

Per rebind require exact symmetry:

```text
source_owner_acquire_count == source_owner_release_count
decoded_owner_acquire_count == decoded_owner_release_count
```

and after each wave C5 already records:

```text
host_source_owned_bytes_after_wave
host_decoded_owned_bytes_after_wave
host_transient_owned_bytes_after_wave
```

C10 may optionally retain wave-level receipts to prove all three return to expected post-wave values.

At minimum C10 requires final C5 ownership release counts to match.

Required:

```text
host_owner_count_leak_rebind_count = 0
```

---

# 27. Optional wave-level host zero audit

If C10 retains `LayerWeightBuildWaveExecutionReceipt` values, require after each completed wave:

```text
completion_fence_wait_count = 1
completion_fence_satisfied = true
next_wave_decode_admitted = true except final wave where semantic meaning may be terminal
```

and audit the post-wave owned-byte fields.

Do not silently assume a byte field should be zero unless C5's actual ownership semantics define it as zero at that boundary.

Where the source does not guarantee zero, record the observed value without inventing a stricter contract.

---

# 28. C4 planner stability audit

For one C9/C10 invocation require the same:

```text
checkpoint_set_digest
packing_policy_digest
transport_authority_digest
```

across all rebinds.

Per layer, plan digest may differ because target tensor spans differ.

Required:

```text
checkpoint_identity_drift_count = 0
packing_policy_drift_count = 0
transport_authority_drift_count = 0
```

---

# 29. Plan target continuity

For rebind ordinal `r` require:

```text
plan.target_layer == observation.target_layer
staging_receipt.target_layer == plan.target_layer
adopted resident layer == plan.target_layer
```

And across consecutive rebinds:

```text
next source layer == previous target layer
```

Required:

```text
plan_target_drift_count = 0
```

---

# 30. Plan byte ledger

C10 records per layer:

```text
sum_source_payload_bytes
sum_decoded_f32_bytes
planned_peak_wave_source_payload_bytes
planned_peak_wave_decoded_f32_bytes
planned_peak_wave_transient_host_bytes
observed_peak_host_transient_owned_bytes
```

Recommended aggregate:

```rust
pub struct R6R9C10PlanByteLedger {
    pub schema_version: u32,
    pub rebind_count: u32,
    pub sum_source_payload_bytes_across_rebinds: u64,
    pub sum_decoded_f32_bytes_across_rebinds: u64,
    pub max_layer_source_payload_bytes: u64,
    pub max_layer_decoded_f32_bytes: u64,
    pub max_planned_peak_wave_source_payload_bytes: u64,
    pub max_planned_peak_wave_decoded_f32_bytes: u64,
    pub max_planned_peak_wave_transient_host_bytes: u64,
    pub max_observed_peak_host_transient_owned_bytes: u64,
    pub pass: bool,
    pub ledger_digest: String,
}
```

The across-rebind sums represent cumulative transported volume, not simultaneous residency.

---

# 31. Long-horizon sequence ledger

C10 creates one sequential ledger over the C9 run.

Recommended:

```rust
pub struct R6R9C10LongHorizonResidencyLedger {
    pub schema_version: u32,
    pub patch_id: String,
    pub build_revision: String,
    pub parent_c9_receipt_digest: String,
    pub checkpoint_set_digest: String,
    pub checkpoint_layer_count: u32,
    pub transport_authority_digest: String,
    pub packing_policy_digest: String,

    pub execution_step_count: u32,
    pub rebind_step_count: u32,
    pub execution_step_receipt_digests: Vec<String>,
    pub rebind_health_observation_digests: Vec<String>,

    pub host_peak_ledger_digest: String,
    pub wave_distribution_ledger_digest: String,
    pub transport_work_ledger_digest: String,
    pub plan_byte_ledger_digest: String,
    pub generation_drift_ledger_digest: String,
    pub pointer_lineage_ledger_digest: String,
    pub gpu_residency_pressure_envelope_digest: String,
    pub destructive_recovery_audit_digest: String,

    pub authority_leak_count: u64,
    pub generation_drift_count: u64,
    pub pointer_lineage_break_count: u64,
    pub host_budget_overrun_count: u64,
    pub host_plan_overrun_count: u64,
    pub count_mismatch_count: u64,
    pub payload_readback_count: u64,
    pub weight_payload_readback_count: u64,
    pub progressive_legacy_runtime_loader_count: u64,
    pub same_operation_legacy_fallback_count: u64,

    pub verdict: R6R9C10HealthVerdict,
    pub ledger_digest: String,
}
```

---

# 32. Generation drift ledger

Recommended:

```rust
pub struct R6R9C10GenerationDriftLedger {
    pub schema_version: u32,
    pub execution_step_count: u32,
    pub rebind_step_count: u32,
    pub hidden_generation_drift_count: u32,
    pub weight_generation_drift_count: u32,
    pub layer_sequence_drift_count: u32,
    pub transition_serial_drift_count: u32,
    pub final_expected_weight_generation: u64,
    pub final_observed_weight_generation: u64,
    pub final_expected_hidden_generation: u64,
    pub final_observed_hidden_generation: u64,
    pub pass: bool,
    pub ledger_digest: String,
}
```

Expected finals derive from C9 starting generations and counts:

```text
expected final weight generation
    = start_weight_generation + rebind_step_count

expected final hidden generation
    = start_hidden_generation + execution_step_count
```

checked arithmetic only.

---

# 33. Pointer lineage ledger

Recommended:

```rust
pub struct R6R9C10PointerLineageLedger {
    pub schema_version: u32,
    pub execution_step_count: u32,
    pub rebind_step_count: u32,
    pub hidden_previous_pointer_break_count: u32,
    pub hidden_cross_step_break_count: u32,
    pub weight_source_to_armed_break_count: u32,
    pub weight_armed_to_vacant_break_count: u32,
    pub weight_vacant_to_adopted_break_count: u32,
    pub weight_cross_step_break_count: u32,
    pub unexpected_hidden_pointer_reuse_count: u32,
    pub unexpected_weight_pointer_reuse_count: u32,
    pub pass: bool,
    pub ledger_digest: String,
}
```

All break/reuse counts must be zero.

---

# 34. Destructive boundary recovery audit: two separate truths

C10 must distinguish:

```text
A. success-path physical observation
B. failure-path structural coverage
```

The normal C9 parent physically observed:

```text
recovery_required_transition_count = 0
```

for all successful rebinds.

That is expected and **does not physically prove** RecoveryRequired behavior.

C10 therefore adds a static/structural audit of the C8 canonical destructive failure call graph.

---

# 35. Current C8 destructive recovery structure

Current pass49 C8 canonical code has:

```text
5 destructive_result(...) protected post-destructive call sites
1 explicit target-adopt Err -> recover_after_destructive_failure(...) branch
recover_after_destructive_failure(...) -> mark_recovery_required(...) when slot is post-destructive
```

C10's static closure must verify the canonical C8 path still owns this coverage.

The exact count is a current-code static expectation, not a general architectural constant. If C8 gains a new post-destructive fallible site, the C10 static audit must be updated rather than silently ignoring it.

---

# 36. Destructive recovery audit receipt

Recommended:

```rust
pub struct R6R9C10DestructiveRecoveryAudit {
    pub schema_version: u32,
    pub canonical_rebind_source_file_digest: String,
    pub destructive_result_site_count: u32,
    pub explicit_adopt_recovery_branch_count: u32,
    pub unprotected_post_destructive_failure_site_count: u32,
    pub recover_helper_present: bool,
    pub mark_recovery_required_call_present: bool,
    pub success_path_recovery_transition_count: u64,
    pub fault_injected_recovery_physically_executed: bool,
    pub fault_injected_recovery_verdict: R6R9C10HealthVerdict,
    pub structural_recovery_coverage_pass: bool,
    pub audit_digest: String,
}
```

Expected current physical success run:

```text
success_path_recovery_transition_count = 0
fault_injected_recovery_physically_executed = false
fault_injected_recovery_verdict = EvidenceInsufficient
structural_recovery_coverage_pass = true
```

C10 must not print `physical recovery PASS` without a fault-injected run.

---

# 37. No source rollback claim

C8 canonical policy remains:

```text
pre-destructive failure:
    source remains Resident

post-destructive failure:
    RecoveryRequired
    no source rebuild
    no legacy fallback
```

C10 structurally audits that no new branch has introduced:

```text
rollback source bundle
rebuild source block
legacy target full-loader fallback
continue progressive loop after destructive failure
```

Required:

```text
forbidden_recovery_fallback_call_edge_count = 0
```

---

# 38. Long-horizon authority leak detector

Recommended deterministic leak count is the checked sum of:

```text
runtime_authority_overlap_count
staging_runtime_weight_authority_count
legacy_runtime_loader_invocation_count
same_operation_legacy_fallback_count
source_rebuild_count
mega_atlas_create_count
cross_wave_payload_overlap_count
vacant_nonzero_block_count
vacant_nonzero_tensor_count
vacant_nonzero_strong_owner_count
lease_boundary_leak_count
```

Required:

```text
authority_leak_count = 0
```

No weighted score.

---

# 39. Decoder completion health seal

C10 must bind the existing C9 final completion seal and prove the final runtime still matches it after all audits.

Recommended:

```rust
pub struct R6R9C10DecoderCompletionHealthSeal {
    pub schema_version: u32,
    pub parent_c9_final_completion_digest: String,
    pub checkpoint_layer_count: u32,
    pub final_decoder_layer: u32,
    pub final_weight_pointer_digest: String,
    pub final_weight_generation: u64,
    pub final_weight_transition_serial: u64,
    pub final_hidden_pointer_digest: String,
    pub final_hidden_layer: u32,
    pub final_hidden_generation: u64,
    pub final_hidden_buffer_identity_digest: String,
    pub final_hidden_completion_token_digest: String,
    pub final_weight_active_lease_count: u32,
    pub final_hidden_active_lease_count: u32,
    pub final_resident_decoder_block_count: u32,
    pub final_resident_weight_tensor_count: u32,
    pub post_final_rebind_count: u32,
    pub next_layer_prefetch_count: u32,
    pub aggregate_mismatch_count: u64,
    pub aggregate_non_finite_count: u64,
    pub aggregate_payload_readback_count: u64,
    pub aggregate_weight_payload_readback_count: u64,
    pub health_verdict: R6R9C10HealthVerdict,
    pub seal_digest: String,
}
```

---

# 40. Final decoder health requirements

Require:

```text
final decoder layer = checkpoint_layer_count - 1
final hidden layer = checkpoint_layer_count
final Weight state = Resident
final Weight layer = final decoder layer
final resident decoder blocks = 1
final resident checkpoint weight tensors = 9
final weight execution leases = 0
final hidden execution leases = 0
post-final rebind = 0
next-layer prefetch = 0
mismatch = 0
nonfinite = 0
payload readback = 0
weight payload readback = 0
```

C10 does not release final decoder weights.

A later patch owns any final-weight retirement decision.

---

# 41. C10 does not rerun decoder layers

C10 is an observer/auditor over one same-invocation C9 physical execution.

Forbidden:

```text
second C9 progressive run
re-execution of Layer3..final for auditing
rebuild of decoder blocks for comparison
legacy oracle replay per layer
payload readback to validate health
```

One parent execution produces one health ledger.

---

# 42. C10 does not re-plan rebinds

C10 consumes the actual C4 plan evidence retained by C9/C8.

Forbidden:

```text
call C4 planner again after C9 completion just to reconstruct metrics
re-open checkpoint shards to derive byte counts
recompute C5 staging state from filesystem artifacts
```

Health evidence must come from the actual operation that ran.

---

# 43. Same-invocation evidence rule

Every C10 per-rebind health observation must be generated in the same invocation as the rebind it describes.

Required chain:

```text
C8 real rebind objects
    ↓
C9 neutral rebind health observation
    ↓
C10 aggregate ledger
```

No post-hoc synthetic observation.

---

# 44. C10 artifact authority

The canonical result is the typed in-memory receipt/ledger.

Optional JSON debug output may be emitted for inspection but does not become runtime SSOT.

Baked ZIP policy continues to exclude accumulated debug artifacts/manifests unless explicitly requested.

---

# 45. Suggested C10 top-level execution type

```rust
pub struct R6R9C10LongHorizonHealthExecution {
    pub parent_c9_receipt_digest: String,
    pub host_peak_ledger: R6R9C10HostPeakLedger,
    pub wave_distribution_ledger: R6R9C10WaveDistributionLedger,
    pub transport_work_ledger: R6R9C10WeightTransportWorkLedger,
    pub plan_byte_ledger: R6R9C10PlanByteLedger,
    pub generation_drift_ledger: R6R9C10GenerationDriftLedger,
    pub pointer_lineage_ledger: R6R9C10PointerLineageLedger,
    pub gpu_residency_pressure_envelope: R6R9C10GpuResidencyPressureEnvelope,
    pub destructive_recovery_audit: R6R9C10DestructiveRecoveryAudit,
    pub long_horizon_ledger: R6R9C10LongHorizonResidencyLedger,
    pub decoder_completion_health: R6R9C10DecoderCompletionHealthSeal,
    pub receipt: R6R9C10LongHorizonHealthReceipt,
}
```

---

# 46. C10 top-level receipt

```rust
pub struct R6R9C10LongHorizonHealthReceipt {
    pub schema_version: u32,
    pub patch_id: String,
    pub build_revision: String,
    pub parent_c9_receipt_digest: String,
    pub checkpoint_set_digest: String,
    pub checkpoint_layer_count: u32,
    pub transport_authority_digest: String,
    pub packing_policy_digest: String,
    pub execution_step_count: u32,
    pub rebind_step_count: u32,

    pub host_peak_ledger_digest: String,
    pub wave_distribution_ledger_digest: String,
    pub transport_work_ledger_digest: String,
    pub plan_byte_ledger_digest: String,
    pub generation_drift_ledger_digest: String,
    pub pointer_lineage_ledger_digest: String,
    pub gpu_residency_pressure_envelope_digest: String,
    pub destructive_recovery_audit_digest: String,
    pub long_horizon_ledger_digest: String,
    pub decoder_completion_health_digest: String,

    pub host_budget_overrun_count: u64,
    pub host_plan_overrun_count: u64,
    pub generation_drift_count: u64,
    pub pointer_lineage_break_count: u64,
    pub transition_serial_drift_count: u64,
    pub authority_leak_count: u64,
    pub work_count_mismatch_count: u64,
    pub wave_fence_count_mismatch_count: u64,
    pub payload_readback_count: u64,
    pub weight_payload_readback_count: u64,
    pub progressive_legacy_runtime_loader_count: u64,
    pub same_operation_legacy_fallback_count: u64,

    pub direct_gpu_allocator_bytes_observable: bool,
    pub fault_injected_recovery_physically_executed: bool,
    pub health_verdict: R6R9C10HealthVerdict,
    pub pass: bool,
    pub receipt_digest: String,
}
```

---

# 47. C10 PASS conditions

C10 `pass=true` requires all observable envelope checks to pass:

```text
parent C9 PASS exact
rebind health observation count == C9 rebind count
execution receipt count == C9 execution count
host budget overrun count = 0
host plan overrun count = 0
generation drift count = 0
transition serial drift count = 0
pointer lineage break count = 0
authority leak count = 0
work count mismatch count = 0
wave fence mismatch count = 0
payload readback count = 0
weight payload readback count = 0
progressive legacy runtime loader count = 0
same-operation legacy fallback count = 0
final decoder completion health = Healthy
structural destructive-recovery coverage = PASS
```

Unavailable direct allocator bytes and unavailable fault-injected recovery execution are explicitly `EvidenceInsufficient`, not silently converted to PASS or FAIL.

---

# 48. Physical success-path recovery semantics

For a normal successful long run expect:

```text
success_path_recovery_required_transition_count = 0
```

This is healthy.

It means no destructive failure occurred, not that failure recovery was physically exercised.

---

# 49. Checkpoint identity stability

Every C10 observation must bind the exact parent checkpoint set digest.

Required:

```text
checkpoint_set_digest_drift_count = 0
```

No checkpoint mutation is allowed.

C5 staging receipts already expose:

```text
checkpoint_mutation_count
```

Aggregate require:

```text
checkpoint_mutation_count = 0
```

---

# 50. Transport authority stability

All C8 rebind observations require the same:

```text
CanonicalDecoderWeightTransportAuthority.authority_digest
```

and:

```text
active_transport_mode = decoder-weight-atlas-wave
legacy_runtime_loader_retired = true
same_operation_legacy_fallback_allowed = false
```

Required:

```text
transport_authority_drift_count = 0
```

---

# 51. Packing policy stability

All retained plans bind one C4 packing policy digest for the invocation.

Required:

```text
packing_policy_drift_count = 0
```

Per-layer plan digests are allowed to differ.

---

# 52. Role registry stability

C4 owns the canonical nine decoder-weight roles.

Per rebind require:

```text
role_count = DECODER_WEIGHT_ROLE_COUNT = 9
lane_count = 9
```

and one stable role-registry digest across all plans.

Required:

```text
role_registry_drift_count = 0
```

---

# 53. C5 final staging state health

Every retained C5 staging receipt requires:

```text
pass = true
final_state = Consumed
runtime_publication_count = 0
runtime_weight_authority_count = 0
execution_lease_count = 0
cross_wave_payload_overlap_count = 0
mega_atlas_create_count = 0
gpu_weight_payload_readback_count = 0
checkpoint_mutation_count = 0
private_candidate_forward_count = 0
```

Any non-zero forbidden count makes C10 unhealthy.

---

# 54. C4/C5 count consistency

Per rebind require:

```text
C5.wave_count == C4.wave_count
C5.lane_count == C4.lane_count
C5.role_count == C4.role_count
C5.completion_fence_wait_count == C4.wave_count
C5.c4_plan_digest == C4.plan_digest
C5.c4_plan_wave_collection_digest == actual plan-wave collection digest
```

Required:

```text
plan_staging_binding_mismatch_count = 0
```

---

# 55. Host budget stability vs policy drift

C10 records the policy max host transient bytes per plan.

If the same policy digest is used, the max-host budget must remain identical across rebinds.

Required:

```text
max_host_budget_drift_count = 0
```

Do not silently allow one layer to receive a larger hidden budget under the same policy digest.

---

# 56. Long-horizon host pressure observations

C10 may report:

```text
min observed per-layer host peak
max observed per-layer host peak
sum observed per-layer host peaks
min budget headroom
max planner peak
```

It must label `sum observed peaks` as **cumulative audit volume**, not simultaneous memory.

No average is required. If an average is emitted, use integer/rational numerator-denominator fields rather than lossy float as authority.

---

# 57. Wave distribution health

Wave-count variation is not itself unhealthy.

Healthy examples include:

```text
all layers 3 waves
some layers 2 waves, some 3 waves
```

provided each layer independently satisfies:

```text
plan wave count > 0
staging fence waits == plan wave count
lane/role accounting exact
host budget exact
```

C10 audits distribution; it does not force uniformity.

---

# 58. Read/decode/material distribution health

For the current decoder architecture, the role registry remains nine tensors per decoder block.

Therefore every rebind must have exactly:

```text
9 reads
9 decodes
9 material commits
9 source-owner releases
9 decoded-owner releases
```

If a future architecture changes the canonical role registry, the role registry SSOT must change before C10 expectations change.

No silent role-count inference from observed reads.

---

# 59. No readback-based health probe

C10 must not introduce:

```text
GPU weight tensor payload readback
full Hidden tensor readback
per-layer CPU checksum of payload values
```

Health auditing is receipt/state based.

Existing compact parity diagnostics remain allowed under their admitted contracts.

---

# 60. No performance claim

C10 may record counts and byte surfaces but must not claim:

```text
faster than legacy loader
lower VRAM than another framework
higher throughput
better latency
better tokens/sec
```

without a separate benchmark methodology and physical timing/allocator evidence.

C10 is a correctness/health audit.

---

# 61. No hidden second ledger authority

C9's progressive lineage ledger remains the execution-history SSOT.

C10 creates an **audit ledger bound to C9 digests**.

C10 does not rewrite C9 step order, pointer order, or execution receipts.

If C10 finds a contradiction, verdict becomes `Unhealthy`; C10 must not repair C9 history.

---

# 62. No silent data imputation

If one rebind health observation is missing:

```text
expected rebind count = R
observed health samples = R-1
```

C10 must return `EvidenceInsufficient`/failure.

It must not fill the missing sample from neighboring layers or global averages.

---

# 63. Deterministic ordering

C10 observation ordering follows C9 execution chronology.

No sorting by digest.

Wave histogram buckets alone are sorted by wave-count key for deterministic serialization.

All digest sets that represent chronological lineage remain ordered chronologically.

---

# 64. Overflow discipline

All long-horizon sums use checked arithmetic:

```text
host peak sums
source payload byte sums
decoded byte sums
read/decode/commit counts
wave counts
fence counts
generation expectations
transition serial expectations
```

No saturating arithmetic in C10 receipt construction.

Overflow is a hard audit failure.

---

# 65. C10 CLI contract

Recommended:

```text
--require-r6-r9-c10-long-horizon-progressive-residency true
--require-r6-r9-c10-c9-physical-parent true
--require-r6-r9-c10-rebind-health-observation-per-rebind true
--require-r6-r9-c10-per-layer-host-peak-tracking true
--require-r6-r9-c10-host-budget-zero-overrun true
--require-r6-r9-c10-host-plan-zero-overrun true
--require-r6-r9-c10-wave-count-distribution true
--require-r6-r9-c10-work-count-ledger true
--require-r6-r9-c10-generation-drift-zero true
--require-r6-r9-c10-transition-serial-drift-zero true
--require-r6-r9-c10-pointer-lineage-break-zero true
--require-r6-r9-c10-runtime-authority-leak-zero true
--require-r6-r9-c10-lease-boundary-leak-zero true
--require-r6-r9-c10-checkpoint-identity-stable true
--require-r6-r9-c10-transport-authority-stable true
--require-r6-r9-c10-packing-policy-stable true
--require-r6-r9-c10-plan-staging-binding true
--require-r6-r9-c10-destructive-recovery-static-coverage true
--require-r6-r9-c10-decoder-completion-health true
--require-r6-r9-c10-zero-payload-readback true
--require-r6-r9-c10-zero-weight-payload-readback true
--require-r6-r9-c10-progressive-legacy-runtime-loader-zero true
--require-r6-r9-c10-same-operation-fallback-zero true
--allow-r6-r9-c10-reexecute-progressive-loop false
--allow-r6-r9-c10-replan-for-audit false
--allow-r6-r9-c10-checkpoint-reread-for-audit false
--allow-r6-r9-c10-direct-gpu-byte-claim-without-telemetry false
--allow-r6-r9-c10-health-score-heuristic false
--allow-r6-r9-c10-silent-evidence-imputation false
```

No user-configurable threshold is added for correctness invariants.

The existing C4 host budget remains the host-transient budget SSOT.

---

# 66. Physical gate sequence

Canonical physical admission wrapper:

```text
run one C9 physical parent
        ↓
verify exact C9 PASS token + receipt
        ↓
verify rebind health observation count == C9 R
        ↓
build host peak ledger
        ↓
build wave distribution ledger
        ↓
build work-count ledger
        ↓
build plan byte ledger
        ↓
build generation drift ledger
        ↓
build pointer lineage ledger
        ↓
build GPU residency authority envelope
        ↓
run static destructive-recovery coverage audit
        ↓
bind final decoder completion health
        ↓
seal long-horizon ledger
        ↓
seal C10 receipt
```

No second decoder forward.

---

# 67. C10 module boundary

Recommended file:

```text
crates/orchestrator_local/src/
  base_train_atlas_wave_02_r6_r9_c10_long_horizon_progressive_residency_health.rs
```

C10 is orchestration/audit logic in Rust.

No JS/TS/Python canonical path.

No new WGSL is required.

---

# 68. Expected implementation surface

Minimum semantic surface:

```text
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r9_c8_canonical_decoder_weight_wave_rebind.rs
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r9_c9_progressive_n_layer_wave_advancement.rs
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r9_c10_long_horizon_progressive_residency_health.rs
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r6_r9_forward_coordinator_gate.rs
specs/cli/ash_basetrain_atlas_wave_02_r6_r9.args
```

`crates/model_core` should not require semantic state-machine changes for C10 unless an actually missing observation cannot be exposed without one.

Prefer observing existing state, not expanding authority state.

---

# 69. Static call-edge prohibitions

C10 canonical module must have zero direct calls to:

```text
load_base_train_atlas_wave_02_r6_r7_decoder_block_weights
rebind_resident_decoder_layer_legacy_full_loader_reference
execute_layer_weight_build_staging_private_candidate
plan_decoder_weight_atlas_waves
advance_resident_decoder_to_checkpoint_end
```

The **physical gate wrapper** calls one C9 session.

C10 receives the completed C9 session and retained evidence.

It must not rerun C9 core itself after the parent is complete.

---

# 70. Static C8 recovery coverage audit method

The audit should be repository-code aware, but it must not rely on fragile runtime regex over source text as the sole correctness authority inside production runtime.

Preferred implementation options, in order:

```text
1. encode explicit typed destructive-stage classification in C8 and audit the stage registry
2. unit/static test call-edge inventory over the canonical C8 module
3. build-time source inventory only as supplementary evidence
```

Do not make runtime production correctness depend on parsing its own Rust source file.

For this C10 gate, a compile-time/static validation script may verify the current call-edge inventory separately from the runtime receipt.

---

# 71. Recommended typed destructive stage registry

To strengthen future auditability without changing behavior:

```rust
pub enum CanonicalWaveRebindDestructiveStage {
    SourceOwnerRelease,
    SameDeviceCompletionWait,
    VacancyTransition,
    C5StagingExecution,
    C5StagingValidation,
    CandidateValidation,
    TargetAdoption,
}
```

The runtime error wrapper may attach stage identity to errors.

This does not add fallback behavior.

C10 can then audit that every stage after the destructive boundary maps failure ownership to RecoveryRequired.

If this registry is considered too invasive for C10, defer it to C10-D1 and keep the static call-edge audit explicit.

---

# 72. Recovery audit admission boundary

C10 base admission requires:

```text
static destructive failure coverage = PASS
success-path recovery transition count = 0
fault-injected recovery physical verdict = EvidenceInsufficient
```

A future optional patch may perform deterministic injected failures at selected post-destructive stages and then promote:

```text
fault_injected_recovery physical verdict = Healthy
```

Do not block C10 base health solely because fault injection is intentionally absent, provided the distinction is explicit.

---

# 73. Current C9 physical expectation example

For the currently observed 22-layer fixture, if C10 observes the same behavior as C9, the high-level expected shape is:

```text
checkpoint_layers=22
execution_steps=19
rebind_steps=18
final_weight_layer=21
final_hidden_layer=22

progressive_checkpoint_reads=162
progressive_decodes=162
progressive_material_commits=162

wave_distribution=<derived from 18 actual plans>
wave_fence_waits=54 only if histogram is 3x18 again

host_peak_max=<observed, not predeclared>
host_budget_overrun=0
host_plan_overrun=0

generation_drift=0
transition_serial_drift=0
pointer_lineage_break=0
authority_leak=0
payload_readback=0
weight_payload_readback=0
```

Exact host peaks and per-layer byte surfaces must come from the retained physical receipts.

---

# 74. Expected C10 terminal line

Recommended single terminal summary:

```text
[r6-r9-c10-long-horizon-progressive-residency]
checkpoint_layers=<L>
execution_steps=<E>
rebind_steps=<R>
health_samples=<R>
host_peak_min=<bytes>
host_peak_max=<bytes>
host_budget_min_headroom=<bytes>
host_budget_overrun=0
host_plan_overrun=0
wave_count_min=<n>
wave_count_max=<n>
wave_count_sum=<n>
wave_histogram=<canonical compact representation>
checkpoint_reads=<R*9>
decodes=<R*9>
material_commits=<R*9>
source_owner_releases=<R*9>
decoded_owner_releases=<R*9>
wave_fence_waits=<sum actual plan waves>
generation_drift=0
transition_serial_drift=0
pointer_lineage_break=0
lease_boundary_leak=0
runtime_authority_overlap=0
staging_runtime_weight_authority=0
progressive_legacy_runtime_loader=0
same_operation_legacy_fallback=0
source_rebuild=0
cross_wave_overlap=0
mega_atlas=0
payload_readback=0
weight_payload_readback=0
checkpoint_mutation=0
direct_gpu_allocator_bytes_observable=0
direct_gpu_allocator_byte_verdict=EVIDENCE_INSUFFICIENT
recovery_static_coverage=1
fault_injected_recovery_physical=0
fault_injected_recovery_verdict=EVIDENCE_INSUFFICIENT
final_weight_layer=<L-1>
final_hidden_layer=<L>
final_weight_lease=0
final_hidden_lease=0
final_resident_blocks=1
final_resident_weight_tensors=9
health_verdict=HEALTHY
long_horizon_ledger_digest=<sha256>
decoder_completion_health_digest=<sha256>
receipt_digest=<sha256>
proof_ledger=HOLD
```

---

# 75. Wave histogram terminal representation

Avoid ambiguous debug formatting.

Recommended canonical text representation:

```text
wave_histogram=2x4,3x14
```

meaning:

```text
wave_count=2 -> 4 rebinds
wave_count=3 -> 14 rebinds
```

Buckets sorted ascending.

The current physical fixture may produce `3x18`, but only physical evidence may establish it.

---

# 76. C10 PASS token

Recommended:

```text
PASS_ASH_BASETRAIN_ATLAS_WAVE_02_R6_R9_C10_LONG_HORIZON_PROGRESSIVE_RESIDENCY_C9_PHYSICAL_PARENT_SINGLE_SAME_INVOCATION_HEALTH_LEDGER_ALL_PROGRESSIVE_REBINDS_OBSERVED_PER_LAYER_HOST_TRANSIENT_PEAK_TRACKED_C4_HOST_BUDGET_ZERO_OVERRUN_PLANNER_PEAK_ZERO_OVERRUN_PLAN_DERIVED_WAVE_DISTRIBUTION_FENCE_COUNT_EXACT_CHECKPOINT_READ_DECODE_MATERIAL_COMMIT_AND_OWNER_RELEASE_LEDGER_EXACT_INDEPENDENT_HIDDEN_AND_WEIGHT_GENERATION_ZERO_DRIFT_WEIGHT_TRANSITION_SERIAL_ZERO_DRIFT_SOURCE_ARMED_VACANT_ADOPTED_POINTER_LINEAGE_CONTINUOUS_HIDDEN_POINTER_LINEAGE_CONTINUOUS_ZERO_UNEXPECTED_POINTER_REUSE_RUNTIME_RESIDENCY_AUTHORITY_CARDINALITY_ENVELOPE_SINGLE_BLOCK_NINE_WEIGHT_TENSORS_ZERO_VACANT_AUTHORITY_ZERO_STAGING_RUNTIME_AUTHORITY_ZERO_RUNTIME_AUTHORITY_OVERLAP_ZERO_LEASE_BOUNDARY_LEAK_ZERO_CROSS_WAVE_OVERLAP_ZERO_MEGA_ATLAS_ZERO_PROGRESSIVE_LEGACY_RUNTIME_LOADER_ZERO_SAME_OPERATION_LEGACY_FALLBACK_ZERO_SOURCE_REBUILD_ZERO_PAYLOAD_READBACK_ZERO_WEIGHT_PAYLOAD_READBACK_ZERO_CHECKPOINT_MUTATION_TRANSPORT_CHECKPOINT_POLICY_AND_ROLE_REGISTRY_STABLE_DESTRUCTIVE_FAILURE_RECOVERY_STATIC_COVERAGE_PASS_SUCCESS_PATH_RECOVERY_TRANSITION_ZERO_FAULT_INJECTED_RECOVERY_AND_DIRECT_GPU_ALLOCATOR_BYTES_EXPLICIT_EVIDENCE_INSUFFICIENT_FINAL_DECODER_COMPLETION_HEALTHY_FINAL_WEIGHT_RESIDENT_FINAL_HIDDEN_CHECKPOINT_BOUNDARY_ZERO_POST_FINAL_REBIND_ZERO_NEXT_LAYER_PREFETCH_FINAL_RMSNORM_LM_HEAD_FORWARD_LOSS_BACKWARD_OPTIMIZER_PRODUCTION_INFERENCE_BLOCKED_PROOF_LEDGER_HOLD_SEALED
```

---

# 77. Physical PASS meaning

C10 physical PASS proves, for one real C9 progressive run:

```text
all progressive rebind operations contributed same-invocation health evidence
all observed host-transient peaks stayed within C4 policy budget
all observed host peaks stayed within C4 planned peak estimates
all plan wave counts matched C5 fence counts
all read/decode/material/owner-release counts were exact
all generation lineages remained monotonic without drift
all weight transition serials remained continuous
all weight and hidden pointer lineages remained continuous
runtime decoder-weight authority remained singular
VacantForRebind samples carried zero runtime block/tensor authority
staging never became runtime authority
no legacy runtime loader/fallback/source rebuild entered progressive operation
no payload/weight readback entered the audit
checkpoint/transport/policy/role registry identities stayed stable
C8 destructive failure ownership remains structurally covered by RecoveryRequired routing
final decoder completion remained healthy after the long sequence
```

---

# 78. Physical PASS does not prove

C10 PASS does **not** prove:

```text
actual GPU allocator byte usage
VRAM fragmentation
physical VRAM reclamation timing
fault-injected RecoveryRequired behavior
performance superiority
latency improvement
throughput improvement
multi-session long-duration stability
process lifetime leak freedom beyond this invocation
final RMSNorm correctness
LM-head logits correctness
loss correctness
backward correctness
optimizer correctness
training convergence
production inference readiness
```

These remain separate boundaries.

---

# 79. Static closure checklist

Before physical run require:

```text
C9 rebind health observation retention present
C9 health observation count bound to rebind count
C8 exposes actual source/armed/vacant/adopted transition evidence or equivalent sealed projection
C10 does not re-run C9
C10 does not call C4 planner
C10 does not call C5 staging
C10 does not reopen checkpoint payloads
C10 direct legacy loader call edges = 0
C10 legacy generalized rebind call edges = 0
host observed peak source = actual C5 staging receipt
host budget source = actual C4 plan/policy
wave count source = actual C4 plan
work counts source = actual C5/C8 receipts
generation checks derive from previous values
transition serial checks derive from actual pointer chain
pointer lineage uses previous_pointer_digest
runtime authority envelope uses actual slot count snapshots
direct GPU allocator byte claim = 0 unless telemetry exists
recovery physical claim = 0 unless fault injection exists
static destructive recovery coverage audit present
zero health heuristic score
zero silent evidence imputation
zero WGSL semantic change required
```

---

# 80. Baked package policy

C10 bake should produce:

```text
full code ZIP
overlay ZIP
```

Exclude unless explicitly requested:

```text
*.md
*.sha256
artifacts/
manifests/
accumulated historical reports
manifest JSON debug bundles
```

The standalone C10 spec remains outside baked ZIP and may be committed to GitHub separately.

---

# 81. Admission state after C10 physical PASS

```text
R6-R6 actual Layer0 body                         = ADMITTED
R6-R7 historical residency                       = ADMITTED_HISTORY
R6-R8 resident decoder execution                 = ADMITTED
C4 decoder-weight wave planner                   = ADMITTED
C5 decoder-weight wave staging                   = ADMITTED
C6 Layer1 -> Layer2 runtime wave rebind canary    = ADMITTED
C7 Layer2 wave-built execution parity             = ADMITTED
C8 canonical generalized wave-loader authority    = ADMITTED
C8-D1 Hidden publication identity closure         = ADMITTED
C9 checkpoint-bounded progressive decoder loop    = ADMITTED
C10 long-horizon observable health ledger         = ADMITTED on physical PASS

Current decoder-weight runtime transport          = DECODER_WEIGHT_ATLAS_WAVE
Legacy generalized runtime loader                 = RETIRED
Legacy historical/reference loader                = RETAINED_NON_AUTHORITY
Direct GPU allocator byte telemetry               = NOT_ADMITTED / EVIDENCE_INSUFFICIENT
Fault-injected destructive recovery physical test = NOT_ADMITTED / EVIDENCE_INSUFFICIENT
Final decoder hidden                              = AVAILABLE
Final RMSNorm / LM head                           = BLOCKED
Forward loss                                      = BLOCKED
Backward                                          = BLOCKED
Optimizer                                         = BLOCKED
Production inference                              = BLOCKED
Proof ledger                                      = HOLD
```

---

# 82. Natural next boundary

After C10 physical PASS, the decoder residency path has enough sequential and long-horizon health evidence to move to the output head boundary.

Recommended next patch:

```text
ASH-BASETRAIN-ATLAS-WAVE-02-R6-R10

Final RMSNorm / LM Head Forward /
C9 Final Hidden Exact Consumption /
Final Decoder Completion Binding /
Canonical Final RMSNorm Weight Authority /
LM Head Weight Residency / Streaming Materialization /
Logit Surface Publication /
Runtime-Derived BQV Coverage /
Zero Hidden Recompute /
Zero Decoder Weight Reload /
Zero Payload Readback /
Forward-Loss Still Blocked Seal
```

If fault-injected destructive recovery is desired before R6-R10, insert a narrow C10-R1 recovery-injection patch rather than mixing it into LM-head work.

---

# 83. Architecture seal

> C10 does not make the decoder smarter and does not make the wave loader faster. It makes the already-physical C9 progression auditable across time. Every real C8 rebind contributes the plan, staging, pointer-transition, count, and ownership evidence that existed when the operation ran; C10 aggregates those observations without re-planning, re-reading, re-executing, or inventing missing telemetry. Host pressure is measured from C5's actual owned-byte peak against C4's declared and planned bounds. GPU residency pressure is stated only through the authority/cardinality signals the runtime truly exposes, while direct allocator bytes remain explicitly evidence-insufficient. Weight and hidden generations are replayed from their own prior values rather than layer indexes, source→armed→vacant→adopted and Hidden-N→Hidden-N+1 pointer lineages are verified exactly, wave/read/decode/material/fence distributions are counted from real receipts, and every leak/fallback/readback/authority-overlap counter must remain zero. The successful run's RecoveryRequired count remains zero and is not misrepresented as a physical failure-recovery test; C8's post-destructive failure ownership is instead audited structurally, with fault injection left as a separate admission. C10 ends only when the C9 final decoder completion still matches live runtime state and the defined observable long-horizon health verdict is HEALTHY.
