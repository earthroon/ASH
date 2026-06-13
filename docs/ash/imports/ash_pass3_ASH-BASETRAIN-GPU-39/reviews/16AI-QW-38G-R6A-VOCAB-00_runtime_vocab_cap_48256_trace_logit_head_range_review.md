# 16AI-QW-38G-R6A-VOCAB-00
## Runtime Vocab Cap 48256 Trace / Logit Head Range Seal

## 1. 확정

이번 베이크에서 `48256`은 최종 runtime vocab cap으로 확정하지 않았습니다. 선배 지적대로 현재 정적 SSOT는 `48259` 쪽이 훨씬 강합니다.

| 계층 | 값 | 판정 |
|---|---:|---|
| primary `specs/model_spec.toml` | 56000 | 1.1B 상위/기획 spec 계열. 현재 weight-tokenizer 라인과 불일치 가능 |
| `specs/model_spec_v5_48259.toml` | 48259 | 현재 v5 runtime/checkpoint 후보 |
| tokenizer manifest v5 | 48259 | 강한 current tokenizer SSOT |
| tokenizer max id | 48258 | id range `0..48258` |
| checkpoint fingerprint embedding | 48259 | fingerprint 기준 48259 |
| checkpoint fingerprint lm_head | 48259 | fingerprint 기준 48259 |
| prior operator hypothesis | 48256 | runtime cap으로는 미확정. tail boundary/banlist 흔적으로 재분류 |

## 2. 48256 재분류

`48256`은 archive 안에서 확인되지만, cap SSOT가 아니라 다음 위치에서 주로 확인됩니다.

- `artifacts/tokenizer_manifest_v5_final.json` token id `48256`
- `artifacts/tokenizer_generation_banlist_v5.json` tail byte token banlist entry
- `artifacts/banned_token_ids_v4_noise.json` banned id list
- PERF-REVIEW-00의 이전 추적 리포트

즉 현재 정적 근거로는:

```text
48259 = tokenizer / v5 model spec / checkpoint fingerprint / lm_head line
48256 = token id boundary 또는 prior cap hypothesis
```

## 3. 마지막 3개 token

`48259 - 48256 = 3`이고, `id >= 48256` tail token은 아래입니다.

```json
[
  {
    "token": "<byte:FD>",
    "id": 48256,
    "score": null,
    "is_reserved": false
  },
  {
    "token": "<byte:FE>",
    "id": 48257,
    "score": null,
    "is_reserved": false
  },
  {
    "token": "<byte:FF>",
    "id": 48258,
    "score": null,
    "is_reserved": false
  }
]
```

이 셋은 `<byte:FD>`, `<byte:FE>`, `<byte:FF>` byte fallback tail입니다. 그러니까 48256 exclusive cap이 실제 sampler/logit range에 걸리면, 마지막 3개 byte fallback token은 생성 불가능해집니다. EOS/control token은 잘리지 않지만, invalid/high-byte fallback tail reachability는 줄어듭니다.

## 4. Range Matrix

```json
{
  "model_spec_primary_vocab_size": 56000,
  "v5_model_spec_vocab_size": 48259,
  "tokenizer_manifest_vocab_count": 48259,
  "tokenizer_max_id_plus_one": 48259,
  "checkpoint_fingerprint_embedding_vocab": 48259,
  "checkpoint_fingerprint_lm_head_vocab": 48259,
  "operator_prior_expected_cap": 48256,
  "current_static_runtime_candidate": 48259,
  "range_status": "CONSISTENT_48259_CURRENT_RUNTIME_CANDIDATE_WITH_56000_HIGHER_SPEC_DRIFT_AND_48256_PRIOR_UNCONFIRMED",
  "head_tokenizer_alignment": true,
  "head_matches_48256": false,
  "tokens_above_48255_count": 3,
  "tail_tokens_above_48255": [
    {
      "token": "<byte:FD>",
      "id": 48256,
      "score": null,
      "is_reserved": false
    },
    {
      "token": "<byte:FE>",
      "id": 48257,
      "score": null,
      "is_reserved": false
    },
    {
      "token": "<byte:FF>",
      "id": 48258,
      "score": null,
      "is_reserved": false
    }
  ]
}
```

## 5. 판단

현재 vocab range 판정은 다음입니다.

```text
CONSISTENT_48259_CURRENT_RUNTIME_CANDIDATE_WITH_56000_HIGHER_SPEC_DRIFT_AND_48256_PRIOR_UNCONFIRMED
```

따라서 이번 커밋의 결론은 이겁니다.

```text
현재 정적 SSOT는 48259다.
48256은 runtime cap으로 확정되지 않았다.
48256을 적용하면 tail byte fallback 3개가 잘린다.
실제 sampler/argmax/decode runtime cap은 실행 probe 전까지 판단불가다.
```

## 6. 판단불가

- 실제 runtime argmax cap
- 실제 top-k/top-p candidate range
- 실제 decode valid id range
- WebGPU vocab atlas active cap
- 48259 tail byte fallback이 실제 품질에 주는 영향

## 7. 다음 권장

실행 환경이 잡히면 `VOCAB-01`에서 sampler/argmax/decode parity를 확인하고, 바로 번역 품질 쪽으로 갈 거면 `EVAL-TRANS-00`이 맞습니다.
