# ASH-BASETRAIN-BT-WGSL-ATTENTION-BACKWARD-ZERO-CAUSE-FRONTIER-06C-R27-R1B

## Revision

- Patch ID: `ASH-BASETRAIN-BT-WGSL-ATTENTION-BACKWARD-ZERO-CAUSE-FRONTIER-06C-R27-R1B`
- Build revision: `bt-wgsl-attention-backward-zero-cause-frontier-06c-r27-r1b`
- Physical parent: `ASH-BASETRAIN-BT-WGSL-REAL-PARAMETER-GRADIENT-DW-FRONTIER-06C-R27-R1A`
- Attention backward ancestor: `ASH-BASETRAIN-BT-WGSL-POST-RMSNORM-OPROJ-ACTUAL-CHAIN-06C-R14`
- Forward state ancestor: TensorCube Stage11 online-softmax merge
- Proof ledger: `HOLD`

## SSOT

R27-R1B is a read-only attention-backward zero-cause diagnostic.

R27-R1A separates parameter-gradient zero into exact forward operand `X`, operation-specific backward operand `dY`, semantic reference and production/canonical dW boundaries. R27-R1B continues one level upstream when Q/K/V/OProj-related parameter-gradient input is zero and determines where the live attention-backward signal becomes zero.

The physical diagnostic chain is:

```text
Stage11 forward global-softmax state
        -> actual OProj dContext
        -> base / H1 / H2 / H3 / H4 dContext split
        -> five G204D live attention-backward lanes
        -> per-lane dQ / dK / dV receipts
        -> deterministic ordered merge5
        -> R14 merged Q/K/V publication
        -> R15 exact source consumption
```

R27-R1B does not change attention forward mathematics, backward mathematics, mask policy, structural gate policy, optimizer policy, weight values, checkpoint state or production `require_aggregate_nonzero` semantics.

## Physical-parent geometry seal

The current R27 lineage is fixed at B1/Q32. R27-R1B explicitly seals this physical parent rather than silently generalizing the Stage11 capacity relationship to future dynamic geometry.

Required:

```text
batch_size=1
q_seq=32
stage11_state_record_count=q_seq*q_heads
```

The base Stage11 state and all four structural branch Stage11 states must have the exact current-parent capacity. Dynamic B/Q geometry remains a later authority.

## R14 observation lifetime extension

R14 previously retained merged Q/K/V outputs but discarded several live zero-cause boundaries. R27-R1B extends observation lifetime only. No new backward computation is introduced.

`BaseTrainR14LayerOutput` retains:

```text
attention_actual_dcontext
attention_base_dcontext
attention_branch_dcontexts[4]
attention_base_dq_lane
attention_dk_lanes[5]
attention_dv_lanes[5]
attention_base_receipt
attention_branch_receipts[4]
```

The retained G204D receipts remain compact status authority and contain existing values including:

```text
all_masked_row_count
invalid_global_state_count
non_finite_gpu_count
bounds_violation_count
dq_rowdot_dispatch_count
dkdv_dispatch_count
dq_row_fault_count
dkdv_row_fault_count
dq/dk/dv nonzero_count
dq/dk/dv xor_fingerprint
dq/dk/dv ROLE_LOCAL_ZERO/NONZERO verdict
```

## Stage11 direct state scan

R27-R1B adds a dedicated GPU compact scan over the exact retained Stage11 `candidate_global_state` buffers.

Shader:

```text
base_train_r27r1b_stage11_state_scan.wgsl
```

It uses the same canonical state flags and validity semantics required by G204D:

```text
FLAG_VALID
FLAG_ALL_MASKED
FLAG_FINAL_WRITE
```

Compact output:

```text
record_count
valid_row_count
all_masked_row_count
invalid_row_count
nonfinite_row_count
final_write_row_count
xor_fingerprint
```

The Stage11 payload is not copied to the host.

## Stage11 to G204D state-lineage authority

For BASE and H1-H4, R27-R1B binds the backward receipt to the corresponding retained Stage11 handle using:

```text
invocation_identity_digest
forward tape digest
partition_generation
partition_digest
canonical_chunk_order_digest
q_seq
q_heads
head_dim
active record count
all-masked row count
```

The compact forward state scan and G204D receipt must agree on the current B1/Q32 active state geometry.

A mismatch is classified as:

```text
GLOBAL_STATE_TRANSFER_FAILURE
```

If the exact forward Stage11 base state is already entirely all-masked, the frontier is:

```text
FORWARD_ALL_MASKED_STATE
```

R27-R1B does not use the invalid implication:

```text
all_masked_row_count == 0 => dContext == 0
```

When all-masked is rejected, diagnosis continues through dContext and lane-local evidence.

## Actual dContext authority

The exact R14 OProj backward `dx` lease is retained as `attention_actual_dcontext` and observed using the existing compact R27-R1 observer.

Compact evidence includes finite/nonfinite, exact-zero/nonzero, max-abs and stable norm telemetry without payload readback.

If the actual dContext is exact zero, R27-R1B publishes:

```text
ACTUAL_DCONTEXT_ZERO
```

This is a causal frontier, not by itself a declaration that OProj mathematics is defective.

## Five-way dContext split authority

R27-R1B observes:

```text
base_dcontext
H1_dcontext
H2_dcontext
H3_dcontext
H4_dcontext
```

and all four exact structural gate leases.

It independently validates the production split with a compact GPU checker:

```text
base = actual * (1 - g0 - g1 - g2 - g3)
Hn   = actual * gn
```

Shader:

```text
base_train_r27r1b_split_validate.wgsl
```

The checker reports only compact mismatch counts and never creates a replacement production dContext.

A physical mismatch is classified as:

```text
DCONTEXT_SPLIT_FAILURE
```

rather than being hidden behind a hardcoded zero/nonzero expectation.

## Current zero-gate-parent conditional check

R27-R1B observes the actual four structural gate values. When all four exact current-parent gates are zero, the current parent implies:

```text
base coefficient = 1
branch coefficients = 0
```

Under that exact observed parent only, R27-R1B checks that the base split preserves the actual dContext nonzero cardinality and H1-H4 split outputs are zero.

Failure is:

```text
CURRENT_PARENT_BASE_SPLIT_FAILURE
```

This is explicitly not a permanent model invariant.

Required policy receipts:

```text
production_require_aggregate_nonzero_change=0
permanent_base_nonzero_invariant=0
parent_conditional_base_expectation=1
```

## Per-lane G204D zero-cause consumption

The five physical G204D receipts are consumed before merge.

For each lane:

```text
BASE
H1
H2
H3
H4
```

and each role:

```text
DQ
DK
DV
```

R27-R1B resolves the existing low-level `ROLE_LOCAL_ZERO` into one of:

```text
ROLE_NONZERO
ROLE_NONFINITE
ROLE_LOCAL_ZERO_ALL_MASKED
ROLE_LOCAL_ZERO_DCONTEXT_ZERO
ROLE_LOCAL_ZERO_WITH_NONZERO_DCONTEXT
```

Required:

```text
unconsumed_role_local_zero_count=0
```

A role-local zero with a live dContext is a diagnostic frontier, not automatically an authorized kernel repair. It is emitted as:

```text
DQ_ROLE_SPECIFIC_ZERO_WITH_LIVE_INPUT
DK_ROLE_SPECIFIC_ZERO_WITH_LIVE_INPUT
DV_ROLE_SPECIFIC_ZERO_WITH_LIVE_INPUT
```

when it occurs on the BASE lane.

## DQ/DK/DV independent authority

R27-R1B does not use aggregate `dq || dk || dv` nonzero as the sole health authority.

DQ, DK and DV are diagnosed independently because a state such as:

```text
DQ=ZERO
DK=NONZERO
DV=NONZERO
```

would otherwise pass an aggregate-nonzero check while hiding a DQ-local frontier.

No new production `require_aggregate_nonzero=true` gate is introduced by R27-R1B.

## Ordered merge5 reference

R12 canonical merge semantics are:

```text
(((base + H1) + H2) + H3) + H4
```

R27-R1B retains the five lane inputs for DQ, DK and DV and executes an independent nonpublishing compact merge reference.

Shader:

```text
base_train_r27r1b_merge5_reference.wgsl
```

The reference computes only compact statistics:

```text
nonfinite_count
nonzero_count
exact_zero_count
max_abs
xor_fingerprint
```

No merged reference tensor becomes production authority.

Merge verdicts are independently emitted for DQ, DK and DV:

```text
ALL_LANES_ZERO
MERGE_PRESERVED_NONZERO
MERGE_CANCELLATION_CONFIRMED
MERGE_EXECUTOR_FAILURE
```

`MERGE_CANCELLATION_CONFIRMED` means one or more input lanes contain nonzero values while the exact ordered semantic reference resolves to zero and the production merge also resolves to zero.

`MERGE_EXECUTOR_FAILURE` means the production merged zero/nonzero state disagrees with the independent ordered reference, or production exposes an impossible nonzero state relative to all-zero inputs/reference.

The XOR fingerprint is compact identity evidence only and is not promoted to full numerical parity authority.

## R14 to R15 source lineage

R15 stores a deterministic identity digest of the exact R14 Q/K/V source lease consumed by its backward path.

The digest binds stable lease metadata including:

```text
label
shape
logical element/byte count
bytes per element
buffer offset
buffer span
active-handle seam identity
vendor access path
```

R27-R1B recomputes the same identity from the retained R14 published leases and requires exact equality for Q, K and V.

This provides an actual source identity comparison rather than an unconditional `lineage_match=true` marker.

Mismatch is:

```text
R14_TO_R15_LINEAGE_FAILURE
```

## Aggregate attention zero cause

The current implementation publishes one aggregate cause from the first physically established boundary:

```text
GLOBAL_STATE_TRANSFER_FAILURE
FORWARD_ALL_MASKED_STATE
ACTUAL_DCONTEXT_ZERO
DCONTEXT_SPLIT_FAILURE
CURRENT_PARENT_BASE_SPLIT_FAILURE
MERGE_EXECUTOR_FAILURE
R14_TO_R15_LINEAGE_FAILURE
DQ_ROLE_SPECIFIC_ZERO_WITH_LIVE_INPUT
DK_ROLE_SPECIFIC_ZERO_WITH_LIVE_INPUT
DV_ROLE_SPECIFIC_ZERO_WITH_LIVE_INPUT
MERGE_CANCELLATION_CONFIRMED
ALL_LANES_ZERO_WITH_LIVE_INPUT
ATTENTION_BACKWARD_PATH_HEALTHY
EVIDENCE_INSUFFICIENT
```

No A/B-only forced classification is used.

`attention_backward_repair_required=1` is limited to structurally established failures in the current implementation:

```text
GLOBAL_STATE_TRANSFER_FAILURE
DCONTEXT_SPLIT_FAILURE
CURRENT_PARENT_BASE_SPLIT_FAILURE
MERGE_EXECUTOR_FAILURE
R14_TO_R15_LINEAGE_FAILURE
```

Value-zero frontiers such as `ACTUAL_DCONTEXT_ZERO` and role-specific zero-with-live-input remain diagnostic boundaries until a narrower mathematical reference proves a defective operation.

## Readback and mutation boundary

Required:

```text
production_attention_payload_readback=0
production_dcontext_payload_readback=0
production_qkv_gradient_payload_readback=0
compact_zero_cause_readback=1
attention_forward_math_change=0
attention_backward_math_change=0
optimizer_change=0
weight_mutation=0
checkpoint_write=0
```

The new GPU kernels emit compact status/statistics only.

## Reproducibility

The complete live observation snapshot is collected twice without source mutation and must compare exactly.

The snapshot includes:

```text
five Stage11 state scans
actual dContext observation
five split dContext observations
four gate observations
split validation
merged DQ/DK/DV observations
three merge-reference observations
```

Required:

```text
reproducibility_runs=2
reproducibility_match=1
```

## Semantic receipt waves

R27-R1B publishes exactly 10 semantic waves:

```text
Wave 0  R27-R1A parent + B1/Q32 geometry
Wave 1  five Stage11 state scans + backward-state lineage result
Wave 2  actual OProj dContext observation
Wave 3  five split dContexts + four gates + split validation
Wave 4  BASE G204D receipt
Wave 5  H1-H4 G204D receipts
Wave 6  15 lane-role zero-cause records
Wave 7  merged DQ/DK/DV + independent merge references + merge verdicts
Wave 8  R14 -> R15 Q/K/V lease-identity comparisons
Wave 9  aggregate zero cause + handoff + canaries + reproducibility
```

Required:

```text
receipt_atlas_waves=10
receipt_field_count_derived_from_registry=1
receipt_chunk_count_derived_from_wave_geometry=1
monolithic_final_json=0
```

## CLI authority

R27-R1B introduces exactly 48 contiguous required gates:

```text
--require-bt-wgsl-r27r1b-contract-001
...
--require-bt-wgsl-r27r1b-contract-048
```

The 48-gate set is present in:

```text
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c_r27r1b_contract.args
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c.args
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c_full.args
```

`tools/repair_r13r2r2_resolved_args.ps1` removes stale R27-R1B gates, generates `1..48`, appends them exactly once and verifies exact cardinality.

## Classifier canaries

The bake contains eight nonpublishing merge-classifier canaries covering:

```text
all lanes zero
preserved nonzero
confirmed cancellation
reference-vs-production merge failure
impossible production-nonzero combinations
```

These validate the merge verdict classifier only. They are not claimed as physical production fault injection and are not promoted to attention gradient evidence.

## Expected physical summary

```text
r27r1a_physical_parent=1
stage11_state_lineage_match=<runtime>
stage11_all_masked_row_count=<runtime>
actual_dcontext_nonzero_count=<runtime>
base_dcontext_nonzero_count=<runtime>
h1_dcontext_nonzero_count=<runtime>
h2_dcontext_nonzero_count=<runtime>
h3_dcontext_nonzero_count=<runtime>
h4_dcontext_nonzero_count=<runtime>
split_reconstruction_mismatch_count=<runtime>
base_all_masked_row_count=<runtime>
h1_all_masked_row_count=<runtime>
h2_all_masked_row_count=<runtime>
h3_all_masked_row_count=<runtime>
h4_all_masked_row_count=<runtime>
base_dq_nonzero_count=<runtime>
base_dk_nonzero_count=<runtime>
base_dv_nonzero_count=<runtime>
h1_dq_nonzero_count=<runtime>
h2_dq_nonzero_count=<runtime>
h3_dq_nonzero_count=<runtime>
h4_dq_nonzero_count=<runtime>
merged_dq_nonzero_count=<runtime>
merged_dk_nonzero_count=<runtime>
merged_dv_nonzero_count=<runtime>
dq_merge_verdict=<runtime>
dk_merge_verdict=<runtime>
dv_merge_verdict=<runtime>
r14_to_r15_dq_lineage_match=<runtime>
r14_to_r15_dk_lineage_match=<runtime>
r14_to_r15_dv_lineage_match=<runtime>
unconsumed_role_local_zero_count=0
aggregate_attention_zero_cause=<runtime>
attention_backward_frontier_resolved=<runtime>
attention_backward_repair_required=<runtime>
attention_backward_gradient_path_healthy=<runtime>
production_attention_payload_readback=0
production_dcontext_payload_readback=0
production_qkv_gradient_payload_readback=0
production_require_aggregate_nonzero_change=0
permanent_base_nonzero_invariant=0
parent_conditional_base_expectation=1
receipt_atlas_waves=10
required_gate_count=48
negative_canaries=8
reproducibility_runs=2
reproducibility_match=1
proof_ledger=HOLD
```

## Repair handoff

R27-R1B does not silently repair the detected frontier.

Handoff rules:

```text
FORWARD_ALL_MASKED_STATE
-> inspect Stage11 forward mask/state authority

GLOBAL_STATE_TRANSFER_FAILURE
-> repair Stage11 -> G204D state lineage/binding

ACTUAL_DCONTEXT_ZERO
-> continue upstream OProj / attention-residual dContext causality

DCONTEXT_SPLIT_FAILURE
or CURRENT_PARENT_BASE_SPLIT_FAILURE
-> repair dContext split path

DQ/DK/DV_ROLE_SPECIFIC_ZERO_WITH_LIVE_INPUT
-> add/execute the narrower role-specific semantic backward reference before repair

MERGE_CANCELLATION_CONFIRMED
-> do not repair merge solely because the merged value is zero

MERGE_EXECUTOR_FAILURE
-> repair ordered merge execution/binding

R14_TO_R15_LINEAGE_FAILURE
-> repair publication/consumption lineage
```

## PASS semantics

R27-R1B PASS means the exact current B1/Q32 REAL-loss attention-backward source path was observed from retained Stage11 state through actual dContext, five-way split, five physical G204D lanes, per-lane DQ/DK/DV status, deterministic merge, R14 publication and R15 consumption; Stage11 all-masked state was separated from dContext zero; lane-local zero was separated from merge cancellation; the merge was independently checked without creating a production reference tensor; R14-to-R15 source identity was actually digested and compared; no production payload or parameter was mutated; 10 semantic waves and 48 gates were admitted; and the diagnostic snapshot was reproducible.

PASS does not mean the underlying gradient defect has been repaired, that every DQ/DK/DV role must be nonzero, that an all-masked-free attention row mathematically guarantees nonzero gradients, that BaseTrain production admission is open, or that R27-R2 is automatically admitted.

## PASS seal

```text
PASS_ASH_BASETRAIN_BT_WGSL_ATTENTION_BACKWARD_ZERO_CAUSE_FRONTIER_06C_R27_R1B
```
