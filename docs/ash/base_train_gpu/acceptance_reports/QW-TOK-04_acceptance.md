# QW-TOK-04 Acceptance

## PASS

- QW-TOK-04 module exists
- lib module wired
- max_new_tokens <= 8
- output id range guard exists
- static sampler receipt exists
- sampler mutation blocked
- QW/MCTS/Value/Reward blocked
- no quality claim seal exists
- trace / receipt / report exists

## FAIL

- output id 48259 이상을 valid 처리
- sampler mutation 수행
- QW/MCTS execution 수행
- training/checkpoint/model/runtime/tokenizer mutation 수행
- quality claim 수행
