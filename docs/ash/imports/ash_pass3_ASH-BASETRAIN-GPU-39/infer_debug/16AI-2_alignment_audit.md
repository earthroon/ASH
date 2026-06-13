# 16AI-2 Tokenizer / Checkpoint Alignment Audit

- pass: `true`
- generation_connected_default: `false`
- fallback_cpu_reference: `true`
- generation_execution: `false`

## Manifest

- trainer_vocab_size: `48259`
- vocab_len: `48259`
- max_id_plus_one: `48259`
- vocab_len_matches_trainer: `true`
- max_id_matches_trainer: `true`
- trainer_vocab_matches_spec: `true`
- duplicate_id_count: `0`
- duplicate_token_count: `0`
- holes_count: `0`

## Checkpoint Shapes

- embedding: `model.embed_tokens.weight:[48259, 2048]:F32`
- lm_head: `lm_head.weight:[48259, 2048]:F32`
- embedding_rows_match_spec_vocab: `true`
- lm_head_rows_match_spec_vocab: `true`
- embedding_hidden_match_spec: `true`
- lm_head_hidden_match_spec: `true`
- embedding_lm_head_rows_match: `true`

## Special / Role Token Probes

| token | encode_len | exact_id | reserved_id | single_token_exact | roundtrip_exact | warning |
|---|---:|---:|---:|---|---|---|
| `<pad>` | 1 | 0 | 0 | true | false | roundtrip_not_exact |
| `<bos>` | 1 | 1 | 1 | true | false | roundtrip_not_exact |
| `<eos>` | 1 | 2 | 2 | true | false | roundtrip_not_exact |
| `<unk>` | 1 | 3 | 3 | true | true | none |
| `<br>` | 4 | 21 | 21 | false | false | roundtrip_not_exact |
| `<\|user\|>` | 8 | none | none | false | false | chat_special_fragmented |
| `<\|assistant\|>` | 13 | none | none | false | false | chat_special_fragmented |
| `사용자` | 3 | none | none | false | false | roundtrip_not_exact |
| `사용자:` | 4 | none | none | false | false | role_marker_fragmented |
| `어시스턴트` | 5 | none | none | false | false | roundtrip_not_exact |
| `어시스턴트:` | 6 | none | none | false | false | role_marker_fragmented |
| `###` | 3 | none | none | false | true | none |

## Wrapper Roundtrip

| wrapper | token_count | token_per_char | suspicious_char_split | roundtrip_exact |
|---|---:|---:|---|---|
| `plain` | 14 | 0.667 | true | false |
| `dialogue-ko` | 25 | 0.758 | true | false |
| `instruction-ko` | 29 | 0.763 | true | false |
| `chatml-lite` | 38 | 0.844 | true | false |

## Summary

- suspicious_wrapper_count: `4`
- fragmented_probe_count: `4`
