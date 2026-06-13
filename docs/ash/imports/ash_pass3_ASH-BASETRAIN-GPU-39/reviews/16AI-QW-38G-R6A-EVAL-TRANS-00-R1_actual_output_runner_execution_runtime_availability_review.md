# 16AI-QW-38G-R6A-EVAL-TRANS-00-R1
## Actual Output Runner Execution / Runtime Availability Receipt Seal

### 1. 확정

- domain_ssot: `en_to_ko_translation_subtitle_machine`
- preceded_by: `16AI-QW-38G-R6A-EVAL-TRANS-00`
- model_family: `Ash 1.1B`
- vocab_size: `48259`
- eval dataset: `eval/eval_trans_00/en_ko_subtitle_actual_eval_138.jsonl`
- eval_case_count: `138`
- runner_executed: `true`
- model_outputs_generated: `false`
- output_case_count: `0`
- output_schema_valid: `false`
- fake_model_output: `false`
- reference_leak_as_model_output: `false`
- false_output_claim: `false`
- eval_trans_r1_status: `BLOCKED_CARGO_UNAVAILABLE`

### 2. 실행 환경 분류

- cargo_available: `false`
- rustc_available: `false`
- runtime_bin_available: `false`
- checkpoint_available: `false`
- tokenizer_available: `true`
- reason: `cargo_unavailable`

### 3. 판단불가

아직 실제 model output이 없으므로 다음은 확정하지 않는다.

```text
실제 EN→KO 번역 품질
adequacy / fluency / subtitle_fit 점수
hallucination 비율
word salad 비율
후편집 필요도
상용 번역기 대비 성능
```

### 4. 다음 패치

`16AI-QW-38G-R6A-BUILD-ENV-02-R1`
