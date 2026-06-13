# SFT-GPU-8 Acceptance

## Status

PENDING until cargo/WGPU execution in the user environment.

## Scope

base-vs-lora sample report / quality eval fixture pack

## Required Contract

- fixture pack exists
- deterministic decode settings are fixed
- base and LoRA use the same prompt/input conditions
- KV cache resets between generations through the runtime smoke path
- base output is recorded
- LoRA output is recorded
- hygiene metrics are computed for both
- comparison metrics are computed
- JSON report is written
- Markdown report is written

## Gates

- [ ] `fixtures/sft_gpu_quality_fixture_ko.json` exists
- [ ] fixture `schema_version = 1`
- [ ] decode mode is `greedy`
- [ ] base generation runs for each prompt
- [ ] LoRA generation runs for each prompt
- [ ] base/LoRA prompt hashes match
- [ ] generation hygiene metrics are computed
- [ ] LoRA output has no replacement char
- [ ] LoRA output has no Hangul char-split pattern
- [ ] LoRA output is non-empty
- [ ] severe repetition is not detected
- [ ] `base_vs_lora_samples.json` is written
- [ ] `base_vs_lora_samples.md` is written
- [ ] `quality_eval_summary.json` is written
- [ ] `quality_eval_summary.md` is written

## Non-goals

- This commit does not claim LoRA is stylistically better.
- This commit does not automate literary judgment.
- This commit does not replace human review.
