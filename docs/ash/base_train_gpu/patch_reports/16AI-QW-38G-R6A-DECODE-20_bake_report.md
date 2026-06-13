# 16AI-QW-38G-R6A-DECODE-20 Bake Report

## Baked scope

- Added score threshold calibration policy and threshold set snapshot.
- Added human review band routing enums and deterministic routing stub.
- Added calibration sample, threshold proposal, and calibration receipt structures.
- Added eight deterministic fixtures and receipts.
- Extended `DecodeQualityScoreSnapshot` with human review band and threshold proposal slots.

## Execution boundary

- threshold_mutation_executed: false
- human_review_queue_mutation_executed: false
- candidate_commit_executed: false
- candidate_reject_executed: false
- rewrite_executed: false
- compression_executed: false
- retry_decode_executed: false
- subtitle_export_executed: false
- model_forward_executed: false
- sampling_executed: false

## Acceptance status

PASS_STATIC_SCORE_THRESHOLD_CALIBRATION_CONTRACT
