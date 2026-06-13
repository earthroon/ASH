# R7-R1 Static Validation

- status: STATIC_PASS_R7_ARTIFACT_WRITER_DEPTH_CLAMP
- `ConvertTo-Json -Depth 120` removed from R7 runner.
- Safe JSON depth clamp added with max depth 100.
- R7 trace record flattened; deep event payload remains in raw trace JSONL.
- No model/checkpoint/tokenizer/lm_head/final_norm/ban_mask mutation.
