# ASH-BASETRAIN-BT-WGSL-R27R1A-OPERAND-IDENTITY-DIGEST-NORMALIZATION-06C-R27-R1A-R2

## Revision

- Patch ID: `ASH-BASETRAIN-BT-WGSL-R27R1A-OPERAND-IDENTITY-DIGEST-NORMALIZATION-06C-R27-R1A-R2`
- Build revision: `bt-wgsl-r27r1a-operand-identity-digest-normalization-06c-r27-r1a-r2`
- Physical parent: `ASH-BASETRAIN-BT-WGSL-R27R1A-SOURCE-OBSERVATION-PARITY-REPAIR-06C-R27-R1A-R1`
- Diagnostic ancestor: `ASH-BASETRAIN-BT-WGSL-REAL-PARAMETER-GRADIENT-DW-FRONTIER-06C-R27-R1A`
- Carrier ancestor: `ASH-BASETRAIN-BT-WGSL-REAL-GRADIENT-OBSERVABILITY-ATLAS-06C-R27-R1`
- Proof ledger: `HOLD`

## SSOT

R27-R1A-R2 repairs exactly one observation-authority defect: the same physical operand must produce the same operand identity digest whether the caller presents it as one direct lease or as a one-element operand-part list.

The physical parent showed:

```text
parameter_gradient_operation_count=27
canonical_operand_descriptor_count=54
observer_false_zero_count=0
observer_false_nonzero_count=0
source_identity_mismatch_operand_count=42
downproj_parent_source_identity_match=1
downproj_parent_nonzero_count=14336
downproj_r1a_dy_nonzero_count=14336
downproj_r1a_dy_active_row_count=7
downproj_source_parity_verdict=DOWNPROJ_SOURCE_PARITY_OK
r1a_source_observation_authority_ready=0
revalidated_aggregate_root_cause=SOURCE_BINDING_MISMATCH
```

The 42 mismatch cardinality corresponds exactly to the current operation registry:

```text
21 single-part operations x 2 operands = 42 single-part operands
6 four-part factor operations x 2 operands = 12 composite operands
42 + 12 = 54
```

The pre-normalization mismatch therefore represents an identity encoding-domain mismatch, not evidence that 42 production buffers are physically misbound.

## Canonical operand identity owner

One helper owns operand identity semantics:

```text
r27r1a_operand_identity_digest(parts)
```

Its exact contract is:

```text
zero parts  -> fail closed
one part    -> SINGLE_RAW, canonical raw lease digest
many parts  -> MULTI_COMPOSITE, ordered composite of canonical raw lease digests
```

R27-R1A and R27-R1A-R1 both consume this helper. Caller-specific single/composite digest decisions are retired.

## Raw lease identity

The existing raw lease identity remains the physical one-part identity authority. It binds stable runtime metadata already used by R27-R1A, including logical shape/element count, byte range and active-handle seam/vendor/runtime identity fields.

Observer labels are not added to physical identity.

## Ordered composite identity

A multi-part operand is identified as the ordered list of canonical raw part digests.

For the six structural factor operations the H1/H2/H3/H4 order remains authoritative. No sorting or unordered-set digest is permitted.

## Explicit receipt schema

Every R27-R1A operation receipt publishes for X and dY:

```text
source_identity_digest
source_identity_kind
source_part_count
```

Identity kinds are:

```text
SINGLE_RAW
MULTI_COMPOSITE
```

R27-R1A-R1 compares digest, kind and part count together.

## Registry-derived partition

The current 27-operation registry must derive:

```text
single_part_operation_count=21
multi_part_operation_count=6
single_part_operand_count=42
multi_part_operand_count=12
normalized_operand_identity_count=54
```

These are runtime-derived from receipt metadata and then checked against the current physical-parent contract. They are not used as a replacement for registry traversal.

## Historical encoding canary

For each current single-part operand R27-R1A-R2 reconstructs the old incompatible encoding:

```text
old = CompositeDigest([RawDigest(A)])
new = RawDigest(A)
```

The current-parent acceptance target is:

```text
legacy_single_encoding_mismatch_count=42
```

This confirms that the prior 42 mismatches are explained by the old one-element composite domain.

## Normalized single-part closure

After the canonical helper is used on both sides:

```text
normalized_single_part_identity_mismatch_count=0
```

A nonzero value is a real failure of the normalization target.

## Composite preservation

The 12 existing factor composite operands must retain their identity semantics:

```text
composite_identity_regression_mismatch_count=0
composite_operand_preservation_canary=1
```

The repair must not solve the 42 single-part mismatches by changing the H1-H4 composite identity contract.

## Factor slice observation remains separate

R27-R1A-R1 exact strided-slice observation remains unchanged.

Physical lease identity and logical factor slice geometry remain separate pieces of the canonical operand descriptor. Identity normalization must not revert exact factor slice observation to a full 523-wide value observation.

The legacy full-tensor versus exact-slice mismatch is reported separately:

```text
legacy_full_tensor_vs_exact_slice_mismatch_count=<runtime>
```

It is not source identity corruption.

## Source mismatch after normalization

After canonical normalization the system recomputes:

```text
source_identity_match_operand_count
source_identity_mismatch_operand_count
```

The current-parent target is:

```text
source_identity_match_operand_count=54
source_identity_mismatch_operand_count=0
```

Any mismatch that remains after normalization is no longer silently attributed to encoding and becomes a real source-binding diagnostic frontier.

## Aggregate classification

R27-R1A-R2 distinguishes:

```text
SOURCE_IDENTITY_ENCODING_SCHEMA_MISMATCH
REAL_SOURCE_BINDING_MISMATCH
OBSERVATION_AUTHORITY_FAILURE
RMS_FORWARD_TAPE_OBSERVATION_CONTRADICTION
REAL_FORWARD_SOURCE_ZERO
REAL_BACKWARD_SOURCE_ZERO
SOURCE_SUPPORT_DISJOINT
SOURCE_OBSERVATION_PARITY_OK
EVIDENCE_INSUFFICIENT
```

Encoding-schema mismatch has priority only while the canonical identity schema itself is not admitted. After schema normalization, residual identity mismatches are physical/metadata diagnostic targets.

## DownProj proof preservation

The already-passing DownProj parent witness must remain unchanged:

```text
downproj_parent_source_identity_match=1
downproj_source_parity_verdict=DOWNPROJ_SOURCE_PARITY_OK
```

The patch does not alter DownProj values, support geometry or backward mathematics.

## Observer parity preservation

Existing repaired observation evidence must remain:

```text
observer_false_zero_count=0
observer_false_nonzero_count=0
```

R27-R1A-R2 changes identity metadata plumbing only. Element observation, row-support observation and strided-slice observation mathematics remain unchanged.

## Revalidated frontier authority

Only after normalized source identity admission may the following be treated as model-gradient frontier evidence:

```text
revalidated_source_x_zero_count
revalidated_source_dy_zero_count
revalidated_source_support_disjoint_count
revalidated_aggregate_root_cause
```

R27-R1A-R2 consumes the repaired R27-R1A-R1 values after identity normalization and republishes them as the post-normalization authority.

## Observation gate

`r1a_source_observation_authority_ready=1` requires the parent observation authority plus:

```text
source_identity_encoding_schema_mismatch_count=0
source_identity_mismatch_operand_count=0
```

`r1a_gradient_frontier_revalidated=1` requires source observation authority and the parent repaired frontier admission.

`basetrain_gradient_repair_authorized=1` means only that later repair selection may trust the source observation. It does not open BaseTrain production training authority.

## No model mutation

Required:

```text
element_observer_math_change=0
row_support_shader_math_change=0
strided_slice_observer_math_change=0
forward_math_change=0
backward_math_change=0
gradient_value_mutation=0
optimizer_change=0
weight_mutation=0
checkpoint_write=0
```

No source payload or gradient payload is copied to the host.

Required:

```text
production_forward_payload_readback=0
production_backward_payload_readback=0
production_gradient_payload_readback=0
```

## Receipt architecture

R27-R1A-R2 preserves the sequential-parallel receipt policy:

```text
semantic waves sequential
bounded independent metadata/receipt chunks parallel
deterministic ordinal merge
streaming receipt write
```

Required:

```text
receipt_chunk_max_fields<=8
parallel_chunk_build=1
streaming_chunk_write=1
deterministic_wave_merge=1
monolithic_final_json=0
```

Duplicate receipt keys fail closed.

## Semantic waves

R27-R1A-R2 emits 8 semantic waves:

```text
Wave 0  parent + registry partition
Wave 1  canonical identity schema
Wave 2  single-part normalization / historical encoding canary
Wave 3  composite identity preservation / legacy factor slice separation
Wave 4  54-operand identity parity
Wave 5  DownProj + observer physical canaries
Wave 6  revalidated source-zero frontier
Wave 7  reproducibility + handoff
```

Required:

```text
receipt_atlas_waves=8
```

## CLI authority

R27-R1A-R2 introduces exactly 40 required gates:

```text
--require-bt-wgsl-r27r1ar2-contract-001
...
--require-bt-wgsl-r27r1ar2-contract-040
```

The exact set is present in dedicated, short and full args, and is regenerated exactly once by `tools/repair_r13r2r2_resolved_args.ps1`.

Required repair output:

```text
r27r1ar2_required_gate_count=40
r27r1ar2_gate_cardinality_exact=1
```

## Classifier canaries

The implementation carries 12 nonpublishing structural canaries covering registry cardinality, single/multi kind and part-count invariants, DownProj parent parity and observer false-zero/false-nonzero preservation.

These canaries validate diagnostic authority only and do not become model gradient evidence.

## Reproducibility

The normalized identity parity result is constructed twice without source mutation.

Required:

```text
reproducibility_runs=2
reproducibility_match=1
```

## Expected physical summary

```text
r27r1ar1_physical_parent=1
parameter_gradient_operation_count=27
canonical_operand_descriptor_count=54
single_part_operation_count=21
multi_part_operation_count=6
single_part_operand_count=42
multi_part_operand_count=12
normalized_operand_identity_count=54
legacy_single_encoding_mismatch_count=42
normalized_single_part_identity_mismatch_count=0
composite_identity_regression_mismatch_count=0
source_identity_encoding_schema_mismatch_count=0
source_identity_match_operand_count=54
source_identity_mismatch_operand_count=0
legacy_full_tensor_vs_exact_slice_mismatch_count=<runtime>
observer_false_zero_count=0
observer_false_nonzero_count=0
downproj_parent_source_identity_match=1
downproj_source_parity_verdict=DOWNPROJ_SOURCE_PARITY_OK
single_operand_normalization_canary=1
composite_operand_preservation_canary=1
rms_forward_tape_observation_contradiction_count=0
revalidated_source_x_zero_count=<runtime>
revalidated_source_dy_zero_count=<runtime>
revalidated_source_support_disjoint_count=<runtime>
r1a_source_observation_authority_ready=<runtime>
r1a_gradient_frontier_revalidated=<runtime>
revalidated_aggregate_root_cause=<runtime>
basetrain_gradient_repair_authorized=<runtime>
element_observer_math_change=0
row_support_shader_math_change=0
strided_slice_observer_math_change=0
forward_math_change=0
backward_math_change=0
gradient_value_mutation=0
optimizer_change=0
weight_mutation=0
checkpoint_write=0
production_forward_payload_readback=0
production_backward_payload_readback=0
production_gradient_payload_readback=0
receipt_atlas_waves=8
parallel_chunk_build=1
streaming_chunk_write=1
deterministic_wave_merge=1
monolithic_final_json=0
required_gate_count=40
negative_canaries=12
reproducibility_runs=2
reproducibility_match=1
proof_ledger=HOLD
```

## Handoff

If normalization closes with `source_identity_mismatch_operand_count=0`, the new `revalidated_source_*` values become the first R27-R1A zero-frontier counts admitted through the repaired identity gate.

If dY operands remain exact-zero with identity and element/support parity admitted, continue from the exact named operation as `REAL_BACKWARD_SOURCE_ZERO`.

If X operands remain exact-zero with identity and element/support parity admitted, continue from the exact named operation as `REAL_FORWARD_SOURCE_ZERO`. RMS X-zero may open a dedicated RMS forward-tape lineage frontier if the RMS tape evidence requires it.

If any normalized identity mismatch remains, model repair remains unauthorized until the physical source mismatch is classified.

## PASS semantics

R27-R1A-R2 PASS means the R27-R1A/R27-R1A-R1 operand identity systems use one canonical identity owner; zero-part operands fail closed; one-part operands use canonical raw identity; multi-part operands use ordered composite identity; the current 42 raw-versus-one-element-composite encoding-domain mismatches are reproduced as a historical canary and removed by normalization; the existing 12 factor composite identities remain stable; DownProj parent parity and element/support observation mathematics remain unchanged; all 54 normalized source identities are re-compared; post-normalization source-zero frontier values are republished only after identity admission; no model/gradient/optimizer/checkpoint semantics or production tensor payload is changed; and the result is reproducible.

PASS does not mean the underlying model-gradient zero is repaired or that BaseTrain training authority is open.

## PASS seal

```text
PASS_ASH_BASETRAIN_BT_WGSL_R27R1A_OPERAND_IDENTITY_DIGEST_NORMALIZATION_06C_R27_R1A_R2
```
