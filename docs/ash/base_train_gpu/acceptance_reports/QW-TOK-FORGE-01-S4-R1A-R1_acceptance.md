# QW-TOK-FORGE-01-S4-R1A-R1 Acceptance

## PASS
- S2-R2 evidence bind passes.
- S3-R1 evidence bind passes.
- Candidate exists, size/hash/header/shape pass.
- Embedding and lm_head hashes changed relative to forge00.
- Forbidden range hash matches relative to forge00.
- No retrain, checkpoint write, rename, delete, overwrite, GPU kernel, or decode generation.

## PARTIAL
- Original S3 loss/row norm receipts remain clobbered, but S3-R1 candidate evidence passes.
- Candidate is shadow-promotable only; runtime default promotion remains false.

## FAIL
- Missing S2-R2 or S3-R1 evidence.
- Candidate missing or hash mismatch.
- Candidate header parse fail.
- Embedding/lm_head change not confirmed.
- Forbidden range mismatch or missing.
- Any retrain or checkpoint mutation occurs.
