# ASH-BASETRAIN-GPU-36F Acceptance Report

## Patch

ASH-BASETRAIN-GPU-36F  
CPU Tensor View Candidate Materialization Preflight / Candidate Envelope To Bounded Row View Plan No Full Tensor No GPU Upload Seal

## SSOT

Input SSOT is an explicit ASH-BASETRAIN-GPU-36E PASS receipt:

```powershell
.\artifacts\ASH_BASETRAIN_GPU_36E_BOUNDED_WEIGHT_SLICE_ROW_CONTINUITY_PROMOTION_GATE.json
```

The baked ZIP intentionally does not include that live input receipt path, to avoid overwriting the operator's local PASS receipt.

## Static baked result

```txt
BLOCKED_36E_RECEIPT_NOT_FOUND
```

This is the expected sealed result for the bake environment, because no local 36E PASS receipt is bundled.

## Runtime PASS target

```txt
PASS_ASH_BASETRAIN_GPU_36F_CPU_TENSOR_VIEW_CANDIDATE_MATERIALIZATION_PREFLIGHT_CANDIDATE_ENVELOPE_TO_BOUNDED_ROW_VIEW_PLAN_NO_FULL_TENSOR_NO_GPU_UPLOAD
```

## Acceptance criteria

- 36E receipt path is explicitly provided.
- 36E verdict is PASS.
- promotion gate decision is `PROMOTED_TO_CPU_TENSOR_VIEW_CANDIDATE`.
- CPU tensor view candidate envelope is present and valid.
- candidate digest and combined promotion gate digest are present.
- digest chain fields are 64-char lowercase hex strings.
- bounded row view plan contains three evidence rows.
- planned row view bytes equal 24576.
- planned F32 sample count equals 6144.
- no file open/read is performed.
- no F32 decode is performed.
- no CPU tensor view is materialized.
- no full tensor load, GPU upload, forward, backward, optimizer, checkpoint write, or safetensors mutation is performed.

## Expected row view plan

```txt
row_000000_full_view: offset 395361664..395369856
row_024129_full_view: offset 593026432..593034624
row_048258_full_view: offset 790691200..790699392
```

## Next stage

ASH-BASETRAIN-GPU-36G  
Bounded Row View Read Smoke / Row View Plan To Limited Full Row Bytes No Full Tensor No GPU Upload Seal
