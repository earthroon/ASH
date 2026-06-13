# 16AI Tokenizer / Prompt Wrapper / Sampling Conditioning Matrix

- commit: 16AI
- mode: tokenizer
- generation_connected_default: false
- fallback_cpu_reference: true
- tokenizer_cases: 4
- generation_cases: 0
- generation_passed: 0
- generation_failed: 0
- suspicious_tokenization_cases: 4
- pass: true

```json
{
  "attention_native": false,
  "cache": null,
  "candidate_runtime_enabled": false,
  "commit": "16AI",
  "fallback_cpu_reference": true,
  "generation_connected_default": false,
  "generation_matrix": [],
  "kv_cache_native": false,
  "max_new_tokens": 1,
  "mode": "tokenizer",
  "native_ffn_primary_suspect_excluded_by_16AF_G5": true,
  "prompt_raw": "브라질 장수풍뎅이의 장점은 무엇인가요?",
  "runtime_gate": "tokenizer_prompt_wrapper_sampling_conditioning_matrix",
  "sampling_presets": [
    {
      "name": "greedy",
      "seed": 0,
      "temperature": 0.0,
      "top_k": 0
    }
  ],
  "summary": {
    "generation_cases": 0,
    "generation_failed": 0,
    "generation_passed": 0,
    "pass": true,
    "suspicious_tokenization_cases": 4,
    "tokenizer_cases": 4
  },
  "tokenizer_audits": [
    {
      "char_count": 21,
      "decoded_text": "브라 질 장 수 풍 뎅 이 의 장 점은 무 엇 인가요?",
      "ids": [
        28934,
        1044,
        1851,
        2137,
        9585,
        43406,
        373,
        369,
        1851,
        21944,
        5600,
        47763,
        7913,
        334
      ],
      "raw_text": "브라질 장수풍뎅이의 장점은 무엇인가요?",
      "roundtrip_exact": false,
      "suspicious_char_split": true,
      "token_count": 14,
      "token_per_char": 0.6666666666666666,
      "wrapped_text": "브라질 장수풍뎅이의 장점은 무엇인가요?",
      "wrapper": "plain"
    },
    {
      "char_count": 33,
      "decoded_text": "사 용 자: 브라 질 장 수 풍 뎅 이 의 장 점은 무 엇 인가요?\n어 시 스 턴 트:",
      "ids": [
        1638,
        2899,
        1115,
        48061,
        28934,
        1044,
        1851,
        2137,
        9585,
        43406,
        373,
        369,
        1851,
        21944,
        5600,
        47763,
        7913,
        334,
        21,
        852,
        877,
        1551,
        15030,
        2391,
        48061
      ],
      "raw_text": "브라질 장수풍뎅이의 장점은 무엇인가요?",
      "roundtrip_exact": false,
      "suspicious_char_split": true,
      "token_count": 25,
      "token_per_char": 0.7575757575757576,
      "wrapped_text": "사용자: 브라질 장수풍뎅이의 장점은 무엇인가요?\n어시스턴트:",
      "wrapper": "dialogue-ko"
    },
    {
      "char_count": 38,
      "decoded_text": "### 사 용 자\n브라 질 장 수 풍 뎅 이 의 장 점은 무 엇 인가요?\n\n### 답 변\n",
      "ids": [
        48038,
        48038,
        48038,
        1638,
        2899,
        1115,
        21,
        28934,
        1044,
        1851,
        2137,
        9585,
        43406,
        373,
        369,
        1851,
        21944,
        5600,
        47763,
        7913,
        334,
        21,
        21,
        48038,
        48038,
        48038,
        19586,
        13121,
        21
      ],
      "raw_text": "브라질 장수풍뎅이의 장점은 무엇인가요?",
      "roundtrip_exact": false,
      "suspicious_char_split": true,
      "token_count": 29,
      "token_per_char": 0.7631578947368421,
      "wrapped_text": "### 사용자\n브라질 장수풍뎅이의 장점은 무엇인가요?\n\n### 답변\n",
      "wrapper": "instruction-ko"
    },
    {
      "char_count": 45,
      "decoded_text": "<|u s e r|>\n브라 질 장 수 풍 뎅 이 의 장 점은 무 엇 인가요?\n<| a s s i s t a n t|>\n",
      "ids": [
        48063,
        48127,
        48120,
        47874,
        47783,
        47951,
        48127,
        48065,
        21,
        28934,
        1044,
        1851,
        2137,
        9585,
        43406,
        373,
        369,
        1851,
        21944,
        5600,
        47763,
        7913,
        334,
        21,
        48063,
        48127,
        43430,
        47874,
        47874,
        47742,
        47874,
        47956,
        43430,
        47743,
        47956,
        48127,
        48065,
        21
      ],
      "raw_text": "브라질 장수풍뎅이의 장점은 무엇인가요?",
      "roundtrip_exact": false,
      "suspicious_char_split": true,
      "token_count": 38,
      "token_per_char": 0.8444444444444444,
      "wrapped_text": "<|user|>\n브라질 장수풍뎅이의 장점은 무엇인가요?\n<|assistant|>\n",
      "wrapper": "chatml-lite"
    }
  ],
  "vocab_limit": 56253,
  "wrappers": [
    "plain",
    "dialogue-ko",
    "instruction-ko",
    "chatml-lite"
  ]
}
```
