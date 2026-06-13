# Convert DUST v2 -> V4 Guarded Freeform

이 스크립트는 원본 `dust.v2` 학습 JSONL 중에서
`task == "dialogue.continue"`인 행만 골라서,
무조건 `bucket = "guarded_freeform"`으로 변환합니다.

## 강제 매핑 규칙
- `dialogue.continue` -> `guarded_freeform`
- 기본 control prefix:
  - `<task:guarded_freeform>`
  - `<lang:ko>`
  - `<glossary:off>`
  - `<tm:off>`
  - `<cue><line></line></cue>`
  - `<id:dust>`
  - `<id:neutral>`
  - `<id:nonhuman>`
  - `<bridge:stable>`
  - `<guard:no_kinship>`
  - `<guard:no_relationship_override>`
  - `<guard:no_subculture_roleplay>`
  - `<guard:no_meta_prompt_leak>`
  - `<style:compact>`
  - `<qwave:on>`
  - `<delta_k:on>`
  - `<morph:strict>`

## 실행 예시
```bash
python convert_dust_v2_to_v4_guarded_freeform.py   --inputs train_part_01.jsonl train_part_02.jsonl valid.jsonl   --output-dir converted_guarded   --add-cheonjiiin   --add-trace
```

## 출력
- `v4_guarded_freeform_train_part_01.jsonl`
- `v4_guarded_freeform_train_part_02.jsonl`
- `v4_guarded_freeform_valid.jsonl`
- `v4_guarded_freeform_summary.json`
