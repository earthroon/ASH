# QW-TOK-MAP-07

Embedding Row Gather Dry-run / No Transformer Forward Seal.

## SSOT
- target_vocab_size: 48259
- target_max_token_id: 48258
- embedding_rows: 48259
- embedding_dim: 2048
- token_id == embedding_row_index identity mapping

## Allowed
- embedding table shape read
- input id row bounds check
- metadata-only embedding row gather dry-run
- gather shape receipt
- metadata sample hash receipt

## Blocked
- transformer forward
- attention / MLP / layer norm compute
- lm_head logits
- token generation / sampler
- checkpoint or model weight mutation
- runtime apply
