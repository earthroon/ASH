# SFT-GPU-3 Acceptance

## Status

STATIC PASS / RUNTIME PENDING

## Scope

response-only label mask seal

## Required Contract

- `dataset.loss_on = response_only`
- prompt tokens are condition-only
- response tokens are supervised-only
- labels use `IGNORE_INDEX = -100` for prompt predictions
- shifted causal labels are built in the batch builder
- prompt_loss_tokens = 0
- response_loss_tokens > 0

## Gates

- [x] `sft_batch.rs` owns the response-only mask SSOT
- [x] template must contain `{prompt}`
- [x] template must contain `{response}`
- [x] non-empty suffix after `{response}` is rejected in v1
- [x] response text tokenizes to at least 1 token
- [x] shifted `input_ids` and `labels` have the same length
- [x] prompt predicted tokens get label `-100`
- [x] response predicted tokens get real token ids
- [x] response first token is included in loss
- [x] `prompt_loss_tokens == 0`
- [x] `response_loss_tokens > 0`
- [x] truncation never removes all response tokens
- [x] direct JSONL path prints SFT mask stats
- [x] direct JSONL path stops before unsupported CE/update for response-only labels

## Non-goals

- GPU CE loss implementation is not part of this commit.
- LoRA A/B update is not part of this commit.
- Runtime logits delta verification is not part of this commit.

## Expected log

```txt
[lora_train][sft_mask] loss_on=response_only shift=builder ignore_index=-100
[lora_train][sft_mask][sample0] prompt_len=... response_len=... input_len=... prompt_loss_tokens=0 response_loss_tokens=...
[lora_train][sft_mask] examples=... input_tokens=... prompt_tokens=... response_tokens=... prompt_loss_tokens=0 response_loss_tokens=...
```

## Expected next boundary

```txt
SFT-GPU-3 response-only mask sealed; direct CE/lm_head LoRA update is deferred to SFT-GPU-4
```
