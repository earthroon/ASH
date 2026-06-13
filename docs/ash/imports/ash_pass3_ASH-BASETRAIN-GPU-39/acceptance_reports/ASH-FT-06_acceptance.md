# ASH-FT-06 Acceptance

## PASS conditions

1. FT-05 compute, forward, backward, and gradient shape receipts are readable.
2. Candidate sha256 matches expected.
3. Selected group is consistent across FT-05 receipts.
4. Gradient shape is compatible.
5. Gradient element count is non-zero and bounded.
6. Gradient readback bytes do not exceed limit.
7. Gradient finite check passes.
8. Gradient checksum is present.
9. Optimizer mode is `none`.
10. Optimizer apply is false.
11. Candidate write is false.
12. Main receipt verdict is `PASS_ASH_FT06_SINGLE_GROUP_GRADIENT_RECEIPT_NO_OPTIMIZER_APPLY_NO_CANDIDATE_WRITE`.

## FAIL conditions

- FT-05 required receipt missing or non-PASS.
- Group mismatch.
- Candidate sha mismatch.
- Gradient shape mismatch.
- NaN/Inf in gradient receipt.
- Optimizer apply requested.
- Candidate write requested.
- Runtime default apply or checkpoint alias rebind attempted.
