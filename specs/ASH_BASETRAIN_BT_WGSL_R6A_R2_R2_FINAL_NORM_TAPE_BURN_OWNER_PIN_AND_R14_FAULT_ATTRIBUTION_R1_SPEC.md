# ASH-BASETRAIN-BT-WGSL-R6A-R2-R2-FINAL-NORM-TAPE-BURN-OWNER-PIN-AND-R14-FAULT-ATTRIBUTION-R1

## 1. Purpose

This patch closes the production final-RMSNorm tape ownership frontier and decomposes the legacy R14 aggregate non-finite status into compact, condition-specific physical attribution without changing training math.

The patch is intentionally diagnostic and ownership-scoped. It does not alter RMSNorm forward/backward formulas, gradient accumulation, optimizer math, loss normalization, subgroup reduction, or AdamW behavior.

## 2. Parent authority

Parent runtime lineage remains:

`R6 -> R6A -> R6A-R1 -> R6A-R2 -> R6A-R2-R1 -> R6A-R2-R2 -> CF1 compile authority`

Production admission continues to require:

- `AtlasGroupedSequential`
- the R5 physical parent state
- `gradient_accumulation == 8`
- R6A/R2/R2 admission flags
- a valid CF1 compile receipt bound to the authoritative binary

No accumulation-1 diagnostic exception is introduced.

## 3. AtlasRuntimeRealLossTape burn-owner authority

`AtlasRuntimeRealLossTape` is the authoritative lifetime owner for the final-norm tensors consumed by backward.

Each lane must retain exactly four Burn tensor owners:

1. pre-final hidden
2. normalized hidden
3. final-norm inverse RMS
4. final-norm gamma

A raw WGPU lease without its allocator-owning Burn tensor in the same tape is not admissible.

The owner lifetime begins at final-norm forward materialization and must survive:

`raw bridge -> lane tape -> eight-lane fanout -> LM-head micro-atlas work -> final-norm backward completion`

The owner may only be released after the corresponding backward use is complete under the existing runtime completion authority.

## 4. Raw-owner binding and alias rules

The raw bridge must be created from the exact owner variable later stored in the tape.

Runtime validation requires:

- raw bridge mode remains `RawBorrowed`
- the lease buffer and active-handle buffer identity match
- lease range and active-handle range match
- same-lane final-norm lease ranges do not unexpectedly overlap
- non-gamma final-norm ranges do not overlap across lanes
- LM-head micro-atlas pages do not overlap any pinned final-norm range

Cross-lane gamma-to-gamma overlap is the sole explicitly admitted alias class because it is the immutable shared model parameter.

Failure families:

- `BTR14_FINAL_NORM_TAPE_OWNER_PIN_MISSING`
- `BTR14_FINAL_NORM_TAPE_RAW_OWNER_IDENTITY_MISMATCH`
- `BTR14_FINAL_NORM_TAPE_UNEXPECTED_ALIAS`

## 5. R14 status ABI

Existing status indices remain semantically unchanged:

| Slot | Meaning |
|---:|---|
| 0 | legacy aggregate non-finite/fault count |
| 1 | row-dot completion |
| 2 | dx completion |
| 3 | dgamma completion |

New detailed attribution slots append after the legacy ABI:

| Slot | Meaning |
|---:|---|
| 4 | inverse RMS non-finite row count |
| 5 | inverse RMS non-positive row count |
| 6 | x non-finite row count |
| 7 | dy non-finite row count |
| 8 | gamma non-finite row count |
| 9 | row-dot accumulator non-finite row count |
| 10 | dx elements rejected by upstream/input fault |
| 11 | dx computed-value non-finite element count |
| 12 | dgamma columns rejected by input fault |
| 13 | dgamma accumulator non-finite column count |

The production status readback is therefore `14 * u32 = 56 bytes`.

## 6. Classification rules

### Inverse RMS

Classification is exclusive:

- non-finite `r` increments slot 4
- otherwise `r <= 0` increments slot 5

The same row must not be double-attributed to both slots.

### Row inputs

The row-dot kernel classifies the first encountered invalid input into exactly one of:

- x -> slot 6
- dy -> slot 7
- gamma -> slot 8

Existing early-return semantics are preserved.

### Row-dot accumulator

A non-finite accumulator after valid inputs increments slot 9.

### DX

An element rejected due to invalid upstream/input state increments slot 10.

A finite-input element whose computed dx becomes non-finite increments slot 11.

### Dgamma

A column that encounters an invalid input increments slot 12 once for that column.

A column with valid inputs but non-finite accumulation increments slot 13.

## 7. Legacy aggregate partition seal

Every increment of legacy `status[0]` must have exactly one detailed attribution slot in `status[4..13]`.

Host validation requires:

`status[0] == sum(status[4..13])`

Any mismatch fails closed with:

`R14_FAULT_ATTRIBUTION_PARTITION_MISMATCH`

The legacy error family remains:

`R14RmsBackwardNonFinite`

and is extended with compact detailed context rather than replaced.

## 8. Physical context

Production final-norm backward binds compact host-known context to the R14 fault receipt:

- lane index
- total rows
- hidden width
- active loss row count

No expected row count is hard-coded. Values such as the previously observed `208997` are observations, not constants.

## 9. Compact receipt policy

Allowed production readback:

- 56-byte R14 status only
- host-known geometry
- raw lease identity/range metadata

Forbidden production diagnostic readback:

- full inverse RMS payload
- full x payload
- full dy payload
- full gamma payload
- full dx payload
- full dgamma payload

Owner-pin and fault diagnostics must therefore remain compact metadata receipts.

## 10. Math freeze

The following are frozen by this patch:

- RMSNorm mean-square calculation
- epsilon addition
- square-root reciprocal
- RMSNorm row-dot formula
- RMSNorm dx formula
- RMSNorm dgamma formula
- gradient accumulation count
- loss scaling/normalization
- segment accumulation
- subgroup reduction
- AdamW formula

The patch must not add numerical repair or suppression such as clamps, NaN replacement, silent zeroing, or fallback math.

The required behavior is:

`detect -> attribute -> fail`

not:

`detect -> replace value -> continue`.

## 11. CF1 integration

The CF1 compile chain must execute the dedicated static validator:

`tools/validate_r27r1j_r6a_r2_r2_final_norm_tape_burn_owner_pin_r14_fault_attribution_static.py`

The regenerated CF1 receipt remains the binary/source authority for the subsequent N=2 run.

Because this patch changes Rust/WGSL source, the previous CF1 binary receipt is stale and must be regenerated before physical N=2 execution.

## 12. Static acceptance

Static acceptance requires all parent validators to remain green and additionally verifies:

- four owner pins exist and are tape-owned
- raw bridge source variables are the pinned owner variables
- raw internal identity/range validation exists
- lane and micro-atlas alias checks exist
- legacy status 0..3 semantics are preserved
- slots 4..13 have exact fixed meanings
- 56-byte compact status readback
- legacy/detail partition parity
- lane/rows/hidden/active-row context
- no payload readback
- RMSNorm formulas unchanged
- accumulation-8 unchanged
- no numerical repair path

## 13. Physical validation

After regenerating CF1 compile authority, rerun the exact N=2 production configuration with the same:

- model spec
- tokenizer manifest
- dataset manifest
- R5 physical parent
- scheduler profile
- AtlasGroupedSequential route
- gradient accumulation 8
- optimizer-step count 2

The patch itself is the intended independent variable.

## 14. Expected physical interpretation

If owner pinning eliminates the R14 fault and N=2 proceeds, the stale/raw-lifetime hypothesis is physically supported.

If R14 still fails, detailed attribution must identify the next frontier, for example inverse-RMS non-finite rows, inverse-RMS non-positive rows, input contamination, row-dot accumulation, dx value failure, or dgamma accumulation.

A detailed, correctly partitioned failure is a successful diagnostic result even when physical N=2 promotion remains on hold.

## 15. Promotion tokens

Static/code closure:

`PASS_ASH_BASETRAIN_BT_WGSL_R6A_R2_R2_FINAL_NORM_TAPE_BURN_OWNER_PIN_AND_R14_FAULT_ATTRIBUTION`

Physical N=2 not yet proven:

`HOLD_ASH_BASETRAIN_BT_WGSL_R6A_R2_R2_FINAL_NORM_TAPE_BURN_OWNER_PIN_AND_R14_FAULT_ATTRIBUTION_PHYSICAL_N2_NOT_YET_PROVEN`

Physical N=2 promotion may only be claimed after the same production run advances the expected training generation/optimizer/cursor progression without R14 fault suppression.
