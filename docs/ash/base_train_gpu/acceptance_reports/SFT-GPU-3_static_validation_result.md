# SFT-GPU-3 Static Validation Result

- [PASS] sft_batch module exists
- [PASS] IGNORE_INDEX is -100
- [PASS] response_only parser exists
- [PASS] template requires {prompt}
- [PASS] template requires {response}
- [PASS] suffix after response rejected
- [PASS] shifted labels use full_ids[1..]
- [PASS] prompt labels use IGNORE_INDEX
- [PASS] response labels use token ids
- [PASS] prompt_loss_tokens guard
- [PASS] response_loss_tokens guard
- [PASS] truncation refuses remove all response
- [PASS] test covers response first token
- [PASS] lib exports sft_batch module
- [PASS] lib exports sft symbols
- [PASS] training imports sft batch
- [PASS] training parses optional loss_on
- [PASS] training prints mask start log
- [PASS] training renders template
- [PASS] training builds shifted example
- [PASS] training observes stats
- [PASS] training validates stats
- [PASS] training prints final stats
- [PASS] training defers CE/update
- [PASS] doc has SFT-GPU-3 section
- [PASS] acceptance report exists and marked static pass

Summary: 26/26 checks passed.
