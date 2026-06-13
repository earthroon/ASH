# QW-MCTS-00 Acceptance

## PASS
- planning envelope module exists
- MCTS node / edge / action / tree state structures exist
- deterministic self-play episode fixture exists
- expansion / simulation / backprop receipts exist
- backprop receipt hash chain is valid
- parent-child integrity is valid
- node and edge ids are unique
- Value Network is not called or trained
- model weight / checkpoint / LoRA / optimizer mutation is false
- dataset and Arrow export are false
- runtime decode bind and runtime commit are false
- trace / receipt / report artifacts exist

## FAIL
- duplicate node or edge id
- broken parent-child integrity
- broken backprop chain
- any training mutation
- any dataset/Arrow export
- runtime decode default bind
- trace/receipt/report missing
