# 16AI-QW-38G-R6A-EVAL-TRANS-00
## EN-KO Subtitle Actual Output Eval / Translation Quality Baseline Seal

## 1. 확정

- 도메인 SSOT: `en_to_ko_translation_subtitle_machine`
- 모델 기준: `Ash 1.1B`
- vocab 기준: `48259`
- stale 300M spec 사용: `false`
- 평가셋: `>=120` EN→KO subtitle cases
- 실제 모델 출력 생성: `false`
- 번역 품질 점수화: `false`
- 상태: `PASS_EVAL_FIXTURE_BASELINE_READY`

## 2. 평가셋 구성

| category | count |
|---|---:|
| `short_dialogue` | 12 |
| `interjection` | 8 |
| `negative_sentence` | 8 |
| `proper_noun` | 10 |
| `number_time_date` | 10 |
| `rough_speech` | 8 |
| `honorific_candidate` | 10 |
| `casual_candidate` | 10 |
| `context_dependent` | 10 |
| `compression_needed` | 10 |
| `linebreak_subtitle` | 8 |
| `idiom_slang` | 8 |
| `emotion_subtext` | 8 |
| `ambiguous_pronoun` | 8 |
| `subtitle_timing_pressure` | 10 |

## 3. 실행 상태

이번 베이크 환경에서는 실제 모델 추론을 실행하지 않았다. `workspace/eval_trans_00_model_outputs.jsonl`은 의도적으로 비어 있으며, reference를 output으로 복사하지 않았다.

```json
{
  "model_outputs_generated": false,
  "fake_model_output": false,
  "reference_leak_as_model_output": false,
  "false_translation_quality_claim": false
}
```

## 4. 실행 방법

외부 Cargo/runtime 환경에서 아래 runner를 사용한다.

```bash
python3 tools/run_eval_trans_00_actual_output.py \
  --eval eval/eval_trans_00/en_ko_subtitle_actual_eval_138.jsonl \
  --output workspace/eval_trans_00_model_outputs.jsonl \
  --vocab-size 48259

python3 tools/score_eval_trans_00_outputs.py
```

실제 모델 실행 명령은 `ASH_EVAL_TRANS_COMMAND` 또는 `--command`로 제공해야 한다. runner는 번역을 직접 생성하지 않는다.

## 5. 판단불가

- 실제 EN→KO 번역 품질
- hallucination 비율
- word salad 비율
- 후편집 필요도
- WebGPU/Cargo runtime 속도
- production safe 여부

## 6. 다음 패치

`16AI-QW-38G-R6A-EVAL-TRANS-00-R1` — Actual Output Runner Execution / Runtime Availability Receipt Seal
