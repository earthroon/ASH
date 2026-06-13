# QW-TOK-00-R7 Acceptance

## PASS
- R7 replay module exists
- R5/R6 receipt hashes are referenced
- R6 evidence packet validation exists
- R5 replay input snapshot exists
- R5 builder is called instead of duplicating reconciliation logic
- replay report/receipt/trace artifacts exist
- no apply/no resize/no runtime bind flags remain false

## FAIL
- R5 logic duplicated or replay result silently altered
- invalid evidence packet treated as pending/pass
- R5 failed/pending result promoted to pass
- runtime/checkpoint/model/tokenizer mutation occurs
