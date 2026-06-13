# QW-TOK-FORGE-01-S4 Acceptance

## PASS

1. output path is not input forge00 path.
2. forge00 original overwrite is impossible by guard.
3. checkpoint write requires approval.
4. temp file is used before final output exists.
5. lock file is created and released.
6. input checkpoint is copied to temp before patching.
7. temp size equals input size.
8. only `model.embed_tokens.weight` and `lm_head.weight` ranges are patched.
9. patch byte length equals tensor byte length.
10. patch ranges do not overlap forbidden ranges.
11. final output is created by rename/promote after verification.
12. existing output is not silently removed.
13. forbidden aggregate hash is checked when executable inputs exist.
14. rollback/orphan receipt exists for failure cases.
15. GPU/decode/legacy graft remain false.

## PARTIAL

1. dry-run writer plan only.
2. local forge00 checkpoint missing in bake environment.
3. S3 updated buffers unavailable, so atomic writer cannot execute in isolation.
4. fsync unsupported but explicitly recorded.
5. forbidden range hash pending because no local checkpoint exists.

## FAIL

1. output path equals input checkpoint path.
2. forge00 overwrite attempted.
3. output checkpoint is silently overwritten.
4. final output receives partial direct writes.
5. temp file is not used.
6. stale lock is silently deleted.
7. embedding/lm_head patch range overlaps forbidden tensor range.
8. transformer/attention/ffn/norm/rotary changes.
9. dtype conversion is silent.
10. atomic rename failure is marked PASS.
