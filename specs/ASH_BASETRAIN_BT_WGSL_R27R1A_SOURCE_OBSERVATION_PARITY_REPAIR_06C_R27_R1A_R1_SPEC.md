# ASH-BASETRAIN-BT-WGSL-R27R1A-SOURCE-OBSERVATION-PARITY-REPAIR-06C-R27-R1A-R1

## Revision

- Patch ID: `ASH-BASETRAIN-BT-WGSL-R27R1A-SOURCE-OBSERVATION-PARITY-REPAIR-06C-R27-R1A-R1`
- Build revision: `bt-wgsl-r27r1a-source-observation-parity-repair-06c-r27-r1a-r1`
- Physical parents:
  - `ASH-BASETRAIN-BT-WGSL-REAL-GRADIENT-OBSERVABILITY-ATLAS-06C-R27-R1`
  - `ASH-BASETRAIN-BT-WGSL-REAL-PARAMETER-GRADIENT-DW-FRONTIER-06C-R27-R1A`
- Diagnostic sibling: `ASH-BASETRAIN-BT-WGSL-ATTENTION-BACKWARD-ZERO-CAUSE-FRONTIER-06C-R27-R1B`
- Proof ledger: `HOLD`

## SSOT

R27-R1A-R1 repairs and verifies the R27-R1A observation authority before any model-gradient repair is authorized.

The physical contradiction is:

```text
R27-R1:
  real dFinalHidden             NONZERO
  R25 real upstream            NONZERO
  mandatory carrier frontier   NO_ZERO_FRONTIER

R27-R1A:
  parameter operations         27
  active-X operations          25
  active-dY operations         2
  joint-support operations     0
  source-X-zero verdicts       2
  source-dY-zero verdicts      25
```

The R27-R1A aggregate cannot be used as a model-repair authority until the element observer, row-support observer and physical source binding are proven to refer to the same exact operand range.

Required policy:

```text
model_gradient_repair_authorized=0
```

until repaired source-observation authority passes.

## Scope

R27-R1A-R1 changes diagnostic observation only.

It does not change:

```text
forward mathematics
backward mathematics
linear dW mathematics
RMS dGamma mathematics
residual VJP semantics
attention backward mathematics
optimizer mathematics
weights
checkpoint state
production gradient values
```

No gradient fabrication, epsilon injection, NaN-to-zero conversion or silent fallback is admitted.

## 27 operations / 54 canonical operands

The existing R27-R1A 27-operation registry remains authoritative:

```text
25 linear dW operations
2 RMS dGamma operations
```

Each operation contributes two observation operands:

```text
X
dY
```

Therefore R27-R1A-R1 validates exactly:

```text
canonical_operand_descriptor_count=54
```

## R27-R1A source identity publication repair

R27-R1A now publishes deterministic source identity digests for the exact X and dY operands consumed by each operation receipt:

```text
x_source_identity_digest
dy_source_identity_digest
```

The digest binds stable physical lease metadata used by the runtime, including shape, logical element count, byte offset/span and active-handle seam/vendor-path identity.

Observer-assigned labels are intentionally excluded from raw lease identity so that two observers can compare the same physical source without creating different identities solely because they name the source differently.

## Hardcoded source-binding retirement

The previous unconditional form:

```text
source_binding_match=true
```

is retired as authority.

R27-R1A now validates that the lease and active handle refer to the same underlying buffer and compatible shape/range/element-count metadata before setting source-binding success.

Wave-level source-binding mismatch counts are derived from runtime operation receipts rather than emitted as a literal zero.

## Canonical operand descriptor

R27-R1A-R1 constructs one immutable descriptor per operand and uses that descriptor as the single source for both value observation and row-support observation.

The descriptor binds:

```text
operation ordinal
operation identity
operand role
lease
logical shape
logical element count
byte offset
byte span
row count
row width
optional strided slice geometry
source identity digest
```

No element/support observer may independently guess a different shape or slice.

## Exact strided-slice observation

Several structural factor operations consume a row-strided subrange of the fused forward tensor rather than the entire physical width.

A full-tensor element observer compared against a sliced row-support observer would create false parity.

R27-R1A-R1 therefore adds:

```text
base_train_r27r1ar1_strided_slice_observe.wgsl
```

and the backend entry:

```text
r27r1ar1_observe_strided_slice(...)
```

The exact logical mapping is:

```text
row          = logical_index / width
column       = logical_index % width
source_index = row * stride + col_start + column
```

This observer emits compact statistics only and never publishes a source or gradient payload.

## Element observation authority

For the exact canonical operand range, R27-R1A-R1 obtains compact value evidence including:

```text
element count
nonfinite count
exact-zero count
nonzero count
positive count
negative count
max abs
```

No full X or dY payload is read to the host.

## Row-support authority

For the exact same canonical operand descriptor, the existing R27-R1A joint-row-support backend evaluates row activity.

Per operand R27-R1A-R1 retains:

```text
active_row_count
row geometry
nonfinite support evidence
```

The element observer and support observer therefore consume the same physical range authority.

## Element/support consistency

For finite operands with valid positive geometry:

```text
element_nonzero_count == 0
<=>
active_row_count == 0
```

Per-operand parity verdicts are:

```text
ZERO_ZERO_PARITY
NONZERO_NONZERO_PARITY
ELEMENT_NONZERO_SUPPORT_ZERO
ELEMENT_ZERO_SUPPORT_NONZERO
```

The two contradictory states are observation-authority failures and may not be converted into a model `SOURCE_X_ZERO` or `SOURCE_DY_ZERO` verdict.

## Legacy aggregate-name retirement

The old R27-R1A summary fields:

```text
x_nonzero_operation_count
dy_nonzero_operation_count
```

were derived from row-activity evidence and are therefore ambiguous when interpreted as element-level nonzero counts.

R27-R1A-R1 publishes separate repaired metrics:

```text
x_element_nonzero_operation_count
x_active_row_operation_count

dy_element_nonzero_operation_count
dy_active_row_operation_count
```

The repaired fields are the diagnostic authority.

## Reobservation of legacy R27-R1A receipts

R27-R1A-R1 reobserves each exact source and compares the repaired element/support result with the operation receipt emitted by R27-R1A.

A legacy mismatch is reported explicitly:

```text
legacy_r1a_reobservation_mismatch_count
```

This field is diagnostic evidence, not automatic failure of the repaired authority. In particular, a legacy full-tensor observation can legitimately differ from the repaired exact strided-slice observation for factor operations.

## Source identity parity

For all 27 operations, R27-R1A-R1 compares freshly constructed canonical source identities against the X/dY source identity digests stored by R27-R1A.

Required aggregates include:

```text
source_identity_match_operand_count
source_identity_mismatch_operand_count
```

A source identity mismatch takes priority over zero-value model interpretation.

## Mandatory DownProj parent canary

The strongest parent contradiction is explicitly checked:

```text
R24 real_dfinal_hidden
        -> R25 real upstream
        -> R13 d_down_output / DownProj dY
        -> R27-R1A mlp_down_proj dY
```

R27-R1A-R1 requires exact physical lease parity between:

```text
R24 real_dfinal_hidden
R13 d_down_output
```

and reobserves both.

Required receipt fields include:

```text
downproj_parent_source_identity_match
downproj_parent_nonzero_count
downproj_r1a_dy_nonzero_count
downproj_r1a_dy_active_row_count
downproj_source_parity_verdict
```

Possible DownProj verdicts include:

```text
DOWNPROJ_SOURCE_PARITY_OK
DOWNPROJ_ROW_SUPPORT_FALSE_ZERO
DOWNPROJ_ELEMENT_OBSERVER_FALSE_ZERO
DOWNPROJ_SOURCE_BINDING_MISMATCH
DOWNPROJ_SOURCE_MUTATED_OR_REUSED
```

No residual-split defect may be inferred while this parent parity remains unresolved.

## RMS forward-tape sanity

R27-R1A-R1 separately observes the two RMS raw inputs and their downstream normalized outputs:

```text
Input RMS:
  input_hidden
  normalized_hidden

Post-attention RMS:
  after_attention
  normalized_ffn_input
```

If a raw input is observed exact-zero while the corresponding normalized output is observed nonzero under the current no-additive-term RMS semantics, R27-R1A-R1 publishes:

```text
RMS_FORWARD_TAPE_OBSERVATION_CONTRADICTION
```

This is an observation/tape frontier and does not automatically authorize an RMS kernel repair.

## Revalidated gradient-frontier counts

Only after source identity and element/support parity are evaluated does R27-R1A-R1 publish repaired frontier counts:

```text
revalidated_source_x_zero_count
revalidated_source_dy_zero_count
revalidated_source_support_disjoint_count
```

The old R27-R1A aggregate is not reused as repaired authority.

## Observation authority gate

R27-R1A-R1 publishes:

```text
r1a_source_observation_authority_ready
r1a_gradient_frontier_revalidated
basetrain_gradient_repair_authorized
```

Observation authority requires the repaired 54-operand source observation set to have no new element/support contradiction, no canonical source identity mismatch, a resolved mandatory DownProj parent canary, and no RMS forward-tape observation contradiction.

Only then may the repaired model-gradient frontier be consumed by a later patch.

## Revalidated aggregate root cause

The repaired aggregate is evidence-ordered rather than count-majority based.

Possible classes include:

```text
SOURCE_BINDING_MISMATCH
SOURCE_LIFETIME_OR_ALIAS_FAILURE
OBSERVATION_AUTHORITY_FAILURE
RMS_FORWARD_TAPE_OBSERVATION_CONTRADICTION
REAL_FORWARD_SOURCE_ZERO
REAL_BACKWARD_SOURCE_ZERO
SOURCE_SUPPORT_DISJOINT
SOURCE_OBSERVATION_PARITY_OK
EVIDENCE_INSUFFICIENT
```

Observer/source failure has higher priority than model-gradient zero interpretation.

## No majority-vote diagnosis

A summary such as:

```text
25 dY-zero verdicts
2 X-zero verdicts
```

does not authorize a model repair if the underlying source-observation parity is invalid.

The first physically established authority failure wins.

## Readback boundary

Allowed:

```text
compact counts
compact max-abs statistics
row-support statistics
source identity digests
status words
verdicts
```

Forbidden:

```text
full forward X payload readback
full backward dY payload readback
full parameter-gradient payload readback
host concatenated diagnostic tensor
```

Required:

```text
production_forward_payload_readback=0
production_backward_payload_readback=0
production_gradient_payload_readback=0
```

## Sequential-parallel Atlas execution

The diagnostic preserves ASH wave semantics:

```text
semantic waves                sequential
independent observations      parallel where safe
bounded observer chunks       parallel
wave/chunk merge              deterministic ordinal order
receipt output                streaming
```

No mega observation atlas or unordered floating-point authority is introduced.

## Receipt construction

The R27-R1A/R1A-R1 receipt path follows the repaired chunk-streaming policy:

```text
chunk_max_fields <= 8
parallel_chunk_build=1
streaming_chunk_write=1
deterministic_wave_merge=1
monolithic_final_json=0
```

Duplicate receipt keys fail closed.

## Semantic waves

R27-R1A-R1 publishes exactly 10 semantic waves:

```text
Wave 0  parent + operation registry
Wave 1  canonical source descriptor / source identity summary
Wave 2  R13 FFN source observations
Wave 3  R14/R15 base attention + RMS source observations
Wave 4  R17/R18 structural source observations
Wave 5  row-support observation summary
Wave 6  element/support parity
Wave 7  parent-source parity + mandatory DownProj canary
Wave 8  repaired 27-operation frontier + aggregate diagnosis
Wave 9  classifier canaries + reproducibility + handoff
```

Required:

```text
receipt_atlas_waves=10
```

## CLI authority

R27-R1A-R1 introduces exactly 48 required gates:

```text
--require-bt-wgsl-r27r1ar1-contract-001
...
--require-bt-wgsl-r27r1ar1-contract-048
```

The same set is present in:

```text
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c_r27r1ar1_contract.args
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c.args
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c_full.args
```

`tools/repair_r13r2r2_resolved_args.ps1` regenerates these gates, removes stale copies, appends each exactly once and verifies exact cardinality.

Required repair output:

```text
r27r1ar1_required_gate_count=48
r27r1ar1_gate_cardinality_exact=1
```

## Classifier canaries

The current implementation carries eight nonpublishing classifier canaries for the source-observation parity verdict path.

Required:

```text
negative_canaries=8
```

These canaries validate diagnostic classification only and do not become production gradient evidence.

## Reproducibility

The repaired source-observation result is generated twice against unchanged physical sources.

Required:

```text
reproducibility_runs=2
reproducibility_match=1
```

The comparison covers repaired operation/source identities, compact element observations, row-support observations, parity verdicts, DownProj parent canary and repaired aggregate diagnosis.

## Expected physical summary

```text
r27r1_physical_parent=1
r27r1a_physical_parent=1
parameter_gradient_operation_count=27
canonical_operand_descriptor_count=54

x_element_nonzero_operation_count=<runtime>
x_active_row_operation_count=<runtime>
dy_element_nonzero_operation_count=<runtime>
dy_active_row_operation_count=<runtime>

element_nonzero_support_zero_count=<runtime>
element_zero_support_nonzero_count=<runtime>

source_identity_match_operand_count=<runtime>
source_identity_mismatch_operand_count=<runtime>
legacy_r1a_reobservation_mismatch_count=<runtime>

revalidated_source_x_zero_count=<runtime>
revalidated_source_dy_zero_count=<runtime>
revalidated_source_support_disjoint_count=<runtime>

downproj_parent_source_identity_match=<runtime>
downproj_parent_nonzero_count=<runtime>
downproj_r1a_dy_nonzero_count=<runtime>
downproj_r1a_dy_active_row_count=<runtime>
downproj_source_parity_verdict=<runtime>

rms_forward_tape_observation_contradiction_count=<runtime>

observer_false_zero_count=<runtime>
observer_false_nonzero_count=<runtime>

r1a_source_observation_authority_ready=<runtime>
r1a_gradient_frontier_revalidated=<runtime>
revalidated_aggregate_root_cause=<runtime>
basetrain_gradient_repair_authorized=<runtime>

production_forward_payload_readback=0
production_backward_payload_readback=0
production_gradient_payload_readback=0

receipt_atlas_waves=10
parallel_chunk_build=1
streaming_chunk_write=1
deterministic_wave_merge=1
required_gate_count=48
negative_canaries=8
reproducibility_runs=2
reproducibility_match=1
proof_ledger=HOLD
```

## Handoff

If:

```text
DOWNPROJ_ROW_SUPPORT_FALSE_ZERO
```

then repair the R27-R1A support geometry/binding, not R13 backward.

If:

```text
DOWNPROJ_ELEMENT_OBSERVER_FALSE_ZERO
```

then repair the compact element observation path.

If:

```text
SOURCE_BINDING_MISMATCH
```

then repair canonical R1A source descriptor/lease binding.

If observation parity passes and repaired evidence still proves the real linear dY source is zero, only then may diagnosis move upstream in the physical model graph.

If RMS X-zero survives repaired observation parity, open a dedicated RMS forward-tape lineage frontier.

## BaseTrain admission

R27-R1A-R1 does not open BaseTrain training admission.

`basetrain_gradient_repair_authorized=1` means only that the observer authority is trustworthy enough for a later repair patch to choose a model target.

## PASS semantics

R27-R1A-R1 PASS means the R27-R1A source observer itself was physically re-audited before model-gradient repair: all 27 parameter-gradient operations were represented by exact X/dY operand descriptors; element and row-support observation used the same exact logical source range, including strided factor slices; hardcoded source-binding success was retired; source identities stored by R27-R1A were compared against fresh canonical descriptors; the R27-R1/R1A DownProj contradiction was checked against the physical R24/R13 lineage; RMS raw/normalized forward-tape sanity was observed; ambiguous legacy active-row counts were separated from repaired element-nonzero counts; repaired gradient zero verdicts were withheld when observation authority failed; no model/optimizer/weight/checkpoint semantics or production tensor payload were changed; 10 sequential semantic waves used bounded parallel observation and deterministic streaming receipt construction; 48 gates and eight classifier canaries were admitted; and the repaired diagnostic result was reproducible.

PASS does not mean:

```text
the underlying model-gradient defect is repaired
25 linear dY operands are necessarily real zero
R13 residual handling is defective
OProj is defective
RMS forward tapes are confirmed defective
BaseTrain production admission is open
```

## PASS seal

```text
PASS_ASH_BASETRAIN_BT_WGSL_R27R1A_SOURCE_OBSERVATION_PARITY_REPAIR_06C_R27_R1A_R1
```
