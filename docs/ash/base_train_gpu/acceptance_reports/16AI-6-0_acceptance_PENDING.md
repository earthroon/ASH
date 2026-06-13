# 16AI-6-0 Acceptance PENDING

## 확정

- 16AI-6-0 source and runner scripts were added.
- The gate is tokenizer-only: `generation=false`, `assembly_mode=off`, `checkpoint_required=false`.
- `chatml-lite` is excluded by default and rejected when explicitly requested.
- Runtime output paths are wired:
  - `infer_debug/16AI-6-0_fragmentation_baseline.json`
  - `infer_debug/16AI-6-0_fragmentation_baseline.md`
  - `acceptance_reports/16AI-6-0_acceptance_PENDING.md`

## Acceptance Criteria

- [x] AC-16AI-6-0-1 baseline encode/decode result is written to JSON.
- [x] AC-16AI-6-0-2 plain/dialogue-ko/instruction-ko wrappers are supported.
- [x] AC-16AI-6-0-3 chatml-lite is excluded by default.
- [x] AC-16AI-6-0-4 generation is not executed.
- [x] AC-16AI-6-0-5 checkpoint is not required.
- [x] AC-16AI-6-0-6 prompt_ids/decoded_prompt/roundtrip_exact are recorded per case.
- [x] AC-16AI-6-0-7 suspicious_char_split/spaced_korean/wrapper_label_fragmented are recorded.
- [x] AC-16AI-6-0-8 fragmentation_score is emitted.
- [x] AC-16AI-6-0-9 suspicious_char_split cannot close with quality_score=100 because quality_score=100-fragmentation_score.
- [x] AC-16AI-6-0-10 baseline markdown report is generated.
- [x] AC-16AI-6-0-11 worst case/wrapper are written to summary.

## 판단불가

- Rust compile check was not executed in this container because `cargo` is unavailable.
- Actual tokenizer fragmentation values are not asserted until the binary runs locally/CI.
