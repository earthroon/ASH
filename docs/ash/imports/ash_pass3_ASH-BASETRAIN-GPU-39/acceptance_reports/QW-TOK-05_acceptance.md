# QW-TOK-05 Acceptance

## PASS 조건

- QW-TOK-05 module exists
- lib module wired
- output id source probe exists
- output id range recheck exists
- tokenizer decode probe exists
- decoded output text record exists
- control token leak report exists
- decode sanity receipt exists
- no quality claim seal exists
- no runtime mutation seal exists
- expected vocab size is 48259
- expected max token id is 48258
- output id 48259 or greater fails range recheck
- decode error cannot pass
- quality claim flags are blocked
- model inference/token generation/sampler/QW/MCTS remain blocked
- trace/receipt/report artifacts exist

## Current baked status

`PENDING_QW_TOK05_OUTPUT_IDS_OR_TOKENIZER_UNAVAILABLE`

Reason: QW-TOK-04 real output ids and local tokenizer loader are not available inside the bake sandbox.
