# ASH-BASETRAIN-GPU-35-R2C Handoff

## SSOT
- Source: ASH-BASETRAIN-GPU-35-R2A PASS / MISSING_OPERATOR_MANIFEST_FILE.
- R2C changes direction: stop manual operator manifest loop and locate existing atlas group plan receipts.
- Patch title: `Atlas Group Plan Receipt Locator / Selected Group Shape DType Byte Range Source Discovery No Weight Load No Backward No Optimizer Seal`.

## Runtime boundary
- No operator manifest write.
- No target manifest write.
- No selected group manifest materialization.
- No selected group weight load.
- No GPU buffer allocation.
- No backward.
- No optimizer.

## Expected verdict
`PASS_ASH_BASETRAIN_GPU_35_R2C_ATLAS_GROUP_PLAN_RECEIPT_LOCATOR_SELECTED_GROUP_SHAPE_DTYPE_BYTE_RANGE_SOURCE_DISCOVERY_NO_WEIGHT_LOAD_NO_BACKWARD_NO_OPTIMIZER`

## Next route
- If full source found: ASH-BASETRAIN-GPU-35-R3 — Selected Group Manifest From Atlas Plan Receipt / Derived Manifest Candidate No Invent No Weight Load Seal.
- If partial source found: ASH-BASETRAIN-GPU-35-R2D — Atlas Group Metadata Partial Source Reconciliation / Shape DType Byte Range Link Audit No Weight Load No Backward No Optimizer Seal.
- If no source found: ASH-BASETRAIN-GPU-35-R2C-AUDIT — Search Root Expansion And Receipt Inventory.
