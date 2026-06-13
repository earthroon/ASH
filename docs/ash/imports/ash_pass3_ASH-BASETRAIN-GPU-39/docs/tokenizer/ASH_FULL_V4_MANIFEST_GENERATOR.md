# ASH full V4 manifest generator

## 목적

`tokenizer_manifest_clean_v4.draft.json`은 **reserved token SSOT scaffold**입니다. 이 파일만으로는 실제 런타임에 바로 쓸 수 없습니다.

이 생성기는 아래 3가지를 합쳐서 **full `tokenizer_manifest_clean_v4.json`**을 만듭니다.

1. 기존 V3 manifest
2. V4 draft scaffold
3. 새 tokenizer build에서 나온 candidate token 목록

핵심은 단순 append가 아니라, 아래 계약을 지키는 것입니다.

- V4 reserved token ids `0..71` 고정
- byte fallback block은 tail에 유지
- V3 non-reserved vocab은 fallback seed로 사용
- candidate token이 있으면 candidate 우선, 없으면 V3 fallback
- 생성 후 `hashes.manifest_hash`, `vocab_hash`, `reserved_tokens_hash` 재계산

## 왜 이 생성기가 필요한가

현재 프로젝트 기준으로 V3는 아래처럼 어긋나 있습니다.

- `tokenizer_spec.toml`: `vocab_size = 56000`
- 실제 `tokenizer_manifest_clean_v3.json`: `vocab.len() = 56253`

즉 생성기는 `spec` 숫자만 믿으면 안 되고, **실제 manifest vocab 길이와 byte block 구조를 같이 봐야** 합니다.

## 입력 형식

### 필수
- `--source-manifest`
- `--target-draft`
- `--out-manifest`

### 선택 candidate 입력
- `--candidate-json`
  - JSON list: `["토큰", {"token":"먼지", "score":123.0}]`
  - Hugging Face `tokenizer.json`
  - tokenizers export의 `model.vocab`
- `--candidate-manifest`
  - 기존 manifest의 `vocab`를 후보로 수집
- `--candidate-tsv`
  - `token<TAB>score`
- `--candidate-jsonl`
  - `{"token":"...","score":...}`

## 기본 병합 규칙

1. V4 reserved token은 draft에서 그대로 고정
2. external candidate non-byte token을 먼저 사용
3. 모자라면 V3 non-byte vocab으로 fallback
4. 마지막 tail은 source manifest의 byte block을 재사용

## 주의

현재 V4 draft는 reserved scaffold라서, **candidate token 없이 full target size를 다 채우지 못할 수 있습니다.**
이 경우 report에 `shortfall`이 찍힙니다.

V3 기준 계산 예시:

- source total vocab: `56253`
- source reserved: `32`
- source byte block: `256`
- source non-byte non-reserved: `55965`
- target total vocab: `56832`
- target reserved: `72`
- target non-byte slots: `56504`
- 즉 source fallback만 쓸 경우 shortfall이 발생합니다.

## 추천 실행 순서

### 1. shortfall 확인용 dry-run

```bash
python ash_full_v4_manifest_generator.py \
  --source-manifest ./tokenizer_manifest_clean_v3.json \
  --target-draft ./tokenizer_manifest_clean_v4.draft.json \
  --out-manifest ./tokenizer_manifest_clean_v4.json \
  --out-report ./tokenizer_manifest_v4_report.json \
  --dry-run
```

### 2. candidate token을 얹은 real run

```bash
python ash_full_v4_manifest_generator.py \
  --source-manifest ./tokenizer_manifest_clean_v3.json \
  --target-draft ./tokenizer_manifest_clean_v4.draft.json \
  --candidate-json ./tokenizer_build_vocab.json \
  --out-manifest ./tokenizer_manifest_clean_v4.json \
  --out-report ./tokenizer_manifest_v4_report.json \
  --imported-from ./tokenizer_build_vocab.json \
  --import-format tokenizer_json \
  --default-top-k 6000
```

## 출력

### manifest
- `manifest_id`
- `tokenizer_spec_id`
- `trainer`
- `normalization`
- `special_tokens`
- `reserved_tokens`
- `vocab`
- `lineage`
- `hot_token_cache`
- `hashes`

### report
- target / generated vocab size
- shortfall
- reserved / byte count
- candidate 사용량
- source fallback 사용량
- dedupe 통계

## 다음 단계

이 생성기로 full V4 manifest를 만든 뒤에는 다음으로 넘어갑니다.

1. `ash_v3_to_v4_migrate.py`로 embedding/lm_head remap
2. `runtime_profile_v2.toml`로 런타임 전환
3. probe/result 로그로 A/B 검증
