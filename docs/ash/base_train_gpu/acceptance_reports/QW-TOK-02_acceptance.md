# QW-TOK-02 Acceptance

## PASS

- runtime input binding dry-run module exists
- id range guard exists
- attention mask / position ids shape contract exists
- no model inference seal exists
- trace / receipt / report artifacts exist

## FAIL/BLOCK

- token id 48259 accepted as valid
- model inference / embedding lookup / logits / sampler/QW/MCTS execution attempted
- runtime decode bind attempted
- trace / receipt 없이 PASS 처리
