# ASH-FT-05 Acceptance

## PASS

```txt
1. ASH-FT-04 upload plan/receipt/snapshot are readable.
2. FT-04 receipt status is PASS.
3. selected group is identical to the FT-04 upload group unless explicit mismatch fails closed.
4. candidate sha256 matches expected.
5. local compute shader module is created.
6. local compute pipelines are created.
7. forward smoke dispatch succeeds.
8. backward smoke dispatch succeeds.
9. bounded readback stays within max_readback_bytes.
10. forward output contains no NaN/Inf.
11. backward gradient output contains no NaN/Inf.
12. gradient shape is compatible with selected smoke element count.
13. optimizer mode is none.
14. optimizer step/state write is false.
15. candidate weight write is false.
16. runtime default apply is false.
17. decode/generation/full model forward/train are false.
```

## FAIL

```txt
1. FT-04 upload receipt is missing or not PASS.
2. selected group mismatch without explicit receipt.
3. candidate sha256 mismatch.
4. shader module or compute pipeline creation fails.
5. forward/backward dispatch fails.
6. forward/backward output contains NaN/Inf.
7. gradient shape is incompatible.
8. readback exceeds max_readback_bytes.
9. optimizer step/state write occurs.
10. candidate safetensors write occurs.
11. runtime default apply occurs.
12. decode/generation/full model forward/train occurs.
```
