# ASH-BASETRAIN-BT-WGSL-SELECTED-LAYER-PARAMETER-WEIGHT-ZERO-PROVENANCE-06C-R27-R1F

## Revision

- Patch ID: `ASH-BASETRAIN-BT-WGSL-SELECTED-LAYER-PARAMETER-WEIGHT-ZERO-PROVENANCE-06C-R27-R1F`
- Build revision: `bt-wgsl-selected-layer-parameter-weight-zero-provenance-06c-r27-r1f`
- Physical parent: `ASH-BASETRAIN-BT-WGSL-SELECTED-LAYER-FORWARD-PROJECTION-ZERO-CAUSE-06C-R27-R1E`
- Training-state parent: `ASH-BASETRAIN-BT-WGSL-REAL-GRADIENT-ATLAS-PRODUCTION-FIRST-COMMIT-06C-R26`
- State-carry parent: `ASH-BASETRAIN-BT-WGSL-PRODUCTION-ADAM-STATE-CARRY-MULTISTEP-06C-R27`
- R27-R1D dependency: `NONE`
- Projection executor repair authority: `CLOSED_BY_R27_R1E`
- Proof ledger: `HOLD`

## SSOT

R27-R1E physically established that the selected layer receives nonzero normalized inputs while all seven base projection weights consumed by the step2 forward are exact zero:

```text
normalized_hidden_nonzero_count=65536
normalized_ffn_input_nonzero_count=65536

Q/K/V/O/Gate/Up/Down forward-bound weight nonzero count = 0

Q/K/V/Gate/Up independent references = 0
attention_projection_root_cause=ATTENTION_QKV_WEIGHT_ZERO
ffn_projection_root_cause=FFN_GATE_UP_WEIGHT_ZERO
attention_projection_executor_repair_required=false
ffn_projection_executor_repair_required=false
```

R27-R1F does not rerun projection mathematics. It identifies the earliest physical provenance boundary at which the seven selected-layer projection weights are already zero or transition from nonzero to zero.

## Provenance chain

R27-R1F records nine ordered stages for the nine selected-layer base roles. Seven projection roles are repair candidates and two RMSNorm gamma roles are controls.

```text
P0 CHECKPOINT_RAW
P1 CHECKPOINT_DECODED
P2 LAYER21_MATERIALIZED
P3 R25_SELECTED_SOURCE
P4 R26_SOURCE
P5 R26_CANDIDATE
P6 R26_COMMITTED_ROOT_GEN1
P7 R27_SOURCE_ROOT_GEN1
P8 R27_STEP2_FORWARD_BOUND
```

Projection roles:

```text
self_attn_q_proj
self_attn_k_proj
self_attn_v_proj
self_attn_o_proj
mlp_gate_proj
mlp_up_proj
mlp_down_proj
```

Control roles:

```text
input_layernorm gamma
post_attention_layernorm gamma
```

## Checkpoint instrumentation

The checkpoint is not reopened for R1F.

The canonical existing full-tensor decode path is instrumented during its already-authoritative read. It records:

```text
raw_payload_digest
raw_scalar_zero_count
raw_scalar_nonzero_count

decoded_zero_count
decoded_nonzero_count
decoded_max_abs
decoded_l2
```

Raw zero scanning is dtype-aware for the checkpoint dtypes already admitted by the canonical decoder path:

```text
F16 / BF16: sign-insensitive numeric zero
F32: sign-insensitive numeric zero
```

Unsupported dtype remains fail-closed. No unknown dtype is silently reinterpreted as F32.

The same read/decode receipt is retained through C5 staging for the final selected layer.

Required:

```text
checkpoint_reopen=0
checkpoint_decode_replay=0
second_checkpoint_read_for_r1f=0
```

## Layer21 materialization evidence

During the existing C8 final-layer wave rebind, before the private candidate is consumed by the residency slot, the nine actual materialized Burn weight tensors are bridged as live raw leases and compactly observed.

No weight payload is read back.

The C9 progressive N-layer execution retains the final selected-layer staging receipt and the nine compact numeric evidence records so the later BaseTrain diagnostic can bind them without recreating the layer.

Required:

```text
selected_layer_index=21
selected_layer_weight_numeric_evidence_count=9
production_weight_payload_readback=0
```

## R25 and R26 physical source

R26 already bridges the actual selected resident block used as the selected-layer source. R1F preserves those 27 physical `R22SourceWeightInput` leases in `BaseTrainR26LayerOutput.source_weights`.

For the nine base roles, R1F binds the R25 semantic/version lineage to the actual R26 source lease.

Current architecture note:

```text
P3 R25_SELECTED_SOURCE
P4 R26_SOURCE
```

share the same retained physical source payload in this implementation. R1F does not invent a nonexistent copy between them. A distinct R25-to-R26 payload transition can only be diagnosed if a future architecture introduces a distinct payload boundary.

## R26 zero-update invariant

R26 physical parent currently reports:

```text
global_norm=0
update_norm=0
```

Therefore for every finite selected parameter:

```text
R26 candidate weight == R26 source weight
```

must hold exactly.

R1F performs device-local exact parity between the physical R26 source weight and R26 candidate weight.

Possible evidence:

```text
R26_ZERO_UPDATE_WEIGHT_PARITY
R26_SOURCE_NONZERO_CANDIDATE_ZERO
R26_SOURCE_CANDIDATE_MISMATCH
```

A nonzero source becoming zero at this boundary classifies `R26_ZERO_UPDATE_CANDIDATE_CORRUPTION`.

## R26 commit boundary

R26 promotes the candidate production training-state root atomically. In the current implementation this root promotion is descriptor/authority promotion rather than a second numeric weight copy.

Therefore:

```text
P5 R26_CANDIDATE
P6 R26_COMMITTED_ROOT_GEN1
```

share the same candidate payload lease in R1F.

R1F records the two semantic stages but does not fabricate a separate device copy. A numeric candidate-to-commit corruption is only physically distinguishable if the runtime later introduces a distinct committed payload.

## R27 state carry and forward override

R27 source generation1 is bound from the production root and the existing step2 base-weight binding already retains:

```text
source_lease
forward_bound_lease
semantic_id
parameter_version_id
```

R1F compactly observes both and performs exact device-local parity:

```text
R26 candidate -> R27 source
R27 source -> step2 forward-bound destination
```

Registry hit and payload correctness are separate authorities.

A `27/27` override hit proves lookup resolution, not value parity.

Strong R27 override failure evidence is:

```text
R27 source nonzero
R27 forward-bound zero
```

which classifies `R27_OVERRIDE_COPY_ZERO_CORRUPTION`.

## Numeric observation policy

All GPU-resident provenance stages use compact device-local observation:

```text
zero_count
nonzero_count
nonfinite_count
max_abs
l2_norm
```

Expected exact-copy boundaries additionally use `HeadwiseOutputParityPipeline.compare_exact`.

Required:

```text
production_weight_payload_readback=0
production_gradient_payload_readback=0
production_optimizer_payload_readback=0
```

No full production tensor payload is materialized on the host for R1F.

## First-zero authority

For each of the seven projection roles, R1F scans P0 through P8 in canonical order and publishes:

```text
first_zero_stage
first_zero_transition
```

The earliest proven zero state owns the diagnosis. Later zero stages are consequences and are not counted as independent causes.

If the earliest observable stage is already zero:

```text
FIRST_OBSERVED_STAGE_ALREADY_ZERO
```

is explicit. R1F does not invent a still-earlier cause.

If all seven projections share the same first-zero stage:

```text
shared_projection_first_zero_count=7
systemic_weight_repair_authorized=true
```

If they diverge:

```text
MIXED_PROJECTION_ZERO_PROVENANCE
per_projection_provenance_repair_required=true
```

## Base-family control pattern

The two RMSNorm gamma roles are observed alongside the seven projections.

R1F publishes:

```text
PROJECTION_ONLY_ZERO
ALL_NINE_BASE_WEIGHTS_ZERO
MIXED_BASE_WEIGHT_ZERO_PATTERN
```

This distinguishes a projection-family-specific provenance defect from whole-base-block erasure.

## Root-cause classes

R1F may publish:

```text
CHECKPOINT_PARAMETER_PAYLOAD_ZERO
CHECKPOINT_DECODE_ZERO_CORRUPTION
LAYER21_WEIGHT_MATERIALIZATION_ZERO
LAYER21_RESIDENT_ADOPTION_ZERO
R25_SELECTED_PARAMETER_SOURCE_BINDING_ZERO
R26_SOURCE_WEIGHT_BINDING_ZERO
R26_ZERO_UPDATE_CANDIDATE_CORRUPTION
R26_ATOMIC_WEIGHT_ROOT_COMMIT_CORRUPTION
R27_SOURCE_ROOT_STATE_CARRY_CORRUPTION
R27_OVERRIDE_COPY_ZERO_CORRUPTION
MIXED_PROJECTION_ZERO_PROVENANCE
WEIGHT_ZERO_PROVENANCE_EVIDENCE_INSUFFICIENT
```

The current implementation only authorizes a root cause that corresponds to a physically observable numeric transition. Semantic stages that share the same physical lease are retained for lineage but do not create fictional copy failures.

## Repair flags

R1F publishes evidence-bound flags only:

```text
checkpoint_source_repair_required
checkpoint_decode_repair_required
weight_materialization_repair_required
resident_adoption_repair_required
r25_source_binding_repair_required
r26_source_binding_repair_required
r26_candidate_repair_required
r26_commit_repair_required
r27_state_carry_repair_required
r27_override_copy_repair_required
systemic_weight_repair_authorized
per_projection_provenance_repair_required
weight_provenance_repair_target_count
```

R1F performs no repair.

Required:

```text
weight_repair_execution=0
weight_value_mutation=0
optimizer_state_mutation=0
gradient_value_mutation=0
checkpoint_write=0
attention_projection_executor_repair_required=0
ffn_projection_executor_repair_required=0
attention_backward_repair_required=0
ffn_backward_repair_required=0
h4_diagnostic_repair_attempt=0
```

## Semantic waves

R1F emits 12 sequential semantic waves:

```text
00 R1E parent
01 base role registry
02 checkpoint source/decode
03 layer21 materialization/resident evidence
04 R25 selected source
05 R26 source
06 R26 zero-update candidate
07 R26 committed generation1
08 R27 source generation1
09 R27 forward override
10 first-zero classification
11 reproducibility/canaries/handoff
```

Required receipt policy:

```text
receipt_atlas_waves=12
receipt_chunk_max_fields<=8
parallel_chunk_build=1
streaming_chunk_write=1
deterministic_wave_merge=1
monolithic_final_json=0
```

## CLI authority

Exactly 48 R1F gates are required:

```text
--require-bt-wgsl-r27r1f-contract-001
...
--require-bt-wgsl-r27r1f-contract-048
```

They must exist exactly once in dedicated, short, full and regenerated resolved args.

Expected resolved-args report:

```text
r27r1f_required_gate_count=48
r27r1f_gate_cardinality_exact=1
```

## Negative canaries

The runtime/static contract includes at least 20 canaries covering checkpoint key cross-binding, wrong selected layer, unsupported dtype reinterpretation, raw-nonzero/decode-zero, decode-nonzero/materialized-zero, resident/source/candidate/root/override zero transitions, QKV/Gate-Up/RMS range aliases, pre-completion observation, checkpoint fallback, weight mutation and R1D/H4 execution.

## Reproducibility

Two complete R1F compact provenance snapshots are collected against unchanged state.

Required:

```text
reproducibility_runs=2
reproducibility_match=1
```

The role/stage statistics, exact parity decisions, first-zero stage, root cause and repair target set must reproduce.

## Runtime summary fields

Per Q/K/V/O/Gate/Up/Down:

```text
checkpoint_raw_nonzero_count
checkpoint_decoded_nonzero_count
materialized_nonzero_count
resident_pretrain_nonzero_count
r26_source_nonzero_count
r26_candidate_nonzero_count
r26_committed_nonzero_count
r27_source_nonzero_count
r27_forward_bound_nonzero_count
first_zero_stage
first_zero_transition
```

Aggregate:

```text
projection_zero_count
rms_control_zero_count
base_weight_zero_pattern
shared_projection_first_zero_stage
shared_projection_first_zero_count
mixed_projection_zero_provenance
weight_zero_provenance_root_cause
weight_provenance_repair_target_count
```

## Post-repair requirement

Any later weight repair must be followed by a physical rerun of R27 through R1F and fresh observation of:

```text
projection weight nonzero counts
projection output nonzero counts
canonical_gradient_nonzero_count
joint_support_operation_count
global_norm
optimizer update_norm
```

No H4-only hypothesis is reopened before this rerun.

## PASS semantics

R27-R1F PASS means the seven selected-layer projection weights already proven zero by R1E were traced through the existing layer21 checkpoint read/decode, final-layer materialization, selected resident source, R26 zero-update candidate/production-root lineage, R27 source root and actual step2 forward-bound destination; all physically observable value transitions were backed by compact numeric evidence and exact device parity where exact copy was expected; stages sharing one physical payload were not falsely represented as independent copies; registry resolution was kept separate from payload correctness; the earliest supported zero provenance boundary was classified without restoring or fabricating weights; all production tensor payload readbacks and state mutations remained zero; and the result reproduced twice.

PASS does not mean the checkpoint, R26, or R27 is pre-assumed defective, that zero projection weights have been repaired, that all 27 gradients will automatically recover, or that full-model BaseTrain authority is open.

## PASS seal

```text
PASS_ASH_BASETRAIN_BT_WGSL_SELECTED_LAYER_PARAMETER_WEIGHT_ZERO_PROVENANCE_06C_R27_R1F
```
