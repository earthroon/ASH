# 16AI-QW-38G-R6A-R12B Patch Report

## Implemented
- Added off-by-default runtime env gate for R12B.
- Added projection-boundary contribution audit using final hidden vector and lm_head atlas rows.
- Added target row, masked row, neighbor row, and normal Korean row comparison metrics.
- Added row norm anomaly vs contribution anomaly split.
- Added JSONL trace, JSON summary, JSON receipt, and Markdown report outputs.
- Added guarded PowerShell runner.

## Guard
No model weights, safetensors, tokenizer, ban mask, or LoRA attachment are mutated by this patch.

## Runtime Note
This baked zip contains the source tree and runner. Full runtime PASS requires the local model checkpoint and prior R12/R10-R2/R38A workspace artifacts to be present in the expected paths.
