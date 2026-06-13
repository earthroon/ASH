# QW-TOK-FORGE-01-S4-R1A Acceptance

## PASS

- S3 hash/size missing is not recorded as mismatch.
- Candidate local evidence is read-only probed.
- Candidate exists, candidate SHA256 is present, and candidate header evidence is OK.
- Forbidden range rebind passed.
- Mutation scope rebind passed.
- S3 training/loss/row-norm evidence passed.
- No checkpoint write, rename, delete, overwrite, temp promote, GPU kernel, decode, or legacy graft occurred.

## FAIL

- Candidate missing.
- Candidate local integrity failed.
- Forbidden range missing/mismatch.
- Mutation scope failed.
- Embedding/lm_head hash change not confirmed.
- S3 training/loss/row-norm evidence missing or failed.
- Any checkpoint rewrite action occurred.
