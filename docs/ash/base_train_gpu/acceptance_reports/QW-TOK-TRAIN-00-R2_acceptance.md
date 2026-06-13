# QW-TOK-TRAIN-00-R2 Acceptance

## Verdict

`PARTIAL_QW_TOK_TRAIN00_R2_LOCAL_CHECKPOINT_NOT_INCLUDED_OR_OPERATOR_APPROVAL_REQUIRED`

## Confirmed in bake

- R2 commit module added.
- R2 CLI bin added.
- `lib.rs` export added.
- Safetensors rewrite path is guarded by `--approve-write-new-checkpoint`.
- In-place overwrite is forbidden.
- No training, no decode, no tensor mutation receipt is generated.
- Candidate output is a new file only.

## Pending locally

The bake container does not include `full_model_vocab_v5_resized.safetensors`, so payload parity cannot be executed here. Run the R2 bin locally with `--approve-write-new-checkpoint` to produce the candidate checkpoint and parity receipt.
