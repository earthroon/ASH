# ASH-FT-31 Mini Corpus Shadow Eval

FT-31 compares base and shadow candidate on a mini corpus after FT-30 numeric drift validation.

## Boundary
Allowed:
- mini corpus dataset scan
- base/shadow loss receipt generation when metrics/backend are available
- base vs shadow comparison
- eval risk classification

Forbidden:
- runtime default apply
- checkpoint alias rebind
- promotion
- training
- optimizer step
- weight update
- checkpoint mutation

## JSONL corpus schema
```json
{"id":"sample_0001","input":"...","target":"...","base_loss":1.23,"shadow_loss":1.20,"weight":1.0}
```
`base_loss` and `shadow_loss` may be supplied by an external eval backend. If absent and no backend is wired, FT-31 blocks rather than fabricating values.
