# Convert DUST v2 -> V4 re-adaptation JSONL

이 스크립트는 현재 학습 원본 JSONL(`dust.v2`, `chat`, `dialogue.continue`)을
내가 제안한 V4 re-adaptation 양식으로 바꿉니다.

## 관측된 원본 구조
- `schema_version`
- `kind`
- `task`
- `task_family`
- `source`
- `id`
- `group_id`
- `weight`
- `messages`
- `input_text`
- `target_text`
- `meta`
- `split`

## 출력 구조
- `id`
- `bucket`
- `input`
- `target`
- `glossary`
- `tm`
- `control`
- `trace`

## 기본 매칭 규칙
- `task == "dialogue.continue"` -> `bucket = "dialogue_continue"`
- 기본 task token -> `<task:guarded_freeform>`
- 기본 style -> `<style:compact>`
- 기본 bridge -> `<bridge:stable>`
- 기본 guard/identity token 주입:
  - `<id:dust>`
  - `<id:neutral>`
  - `<id:nonhuman>`
  - `<guard:no_kinship>`
  - `<guard:no_relationship_override>`
  - `<guard:no_subculture_roleplay>`
  - `<guard:no_meta_prompt_leak>`
  - `<qwave:on>`
  - `<delta_k:on>`
  - `<morph:strict>`

## 실행 예시
```bash
python convert_dust_v2_to_v4_readaptation.py   --inputs train_part_01.jsonl train_part_02.jsonl valid.jsonl   --output-dir converted_v4   --add-cheonjiiin   --add-trace
```

## 주의
이건 **매칭 규칙 초안**입니다.
선배가 원하면 맨 위 `DEFAULT_RULES`만 바꿔서:
- `<task:guarded_freeform>` -> `<task:freeform>`
- `bucket` 이름
- 기본 guard 주입 여부
를 바로 조정할 수 있습니다.
