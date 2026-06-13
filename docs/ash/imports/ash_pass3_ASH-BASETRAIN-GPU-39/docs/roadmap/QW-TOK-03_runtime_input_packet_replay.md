# QW-TOK-03 Roadmap

1. QW-TOK-02 packet schema를 재검증한다.
2. `input_ids`, `attention_mask`, `position_ids` shape를 확인한다.
3. 모든 input id가 `0..48258`인지 확인한다.
4. runner schema contract를 확인한다.
5. infer smoke candidate descriptor를 생성하되 실행하지 않는다.
6. no-generation seal을 receipt에 박는다.

## 다음 후보

`QW-TOK-04 — Tokenizer V5 First Controlled Infer Smoke / No Sampler Mutation Seal`
