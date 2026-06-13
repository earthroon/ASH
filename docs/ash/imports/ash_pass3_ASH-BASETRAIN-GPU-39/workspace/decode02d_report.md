# 16AI-QW-38G-R6A-DECODE-02D — Transition Guard Runtime Evidence / Controlled On Candidate Seal

## 확정
- 기준 입력: `ash_pass3_16AI-QW-38G-R6A-DECODE-02C_probe_integrity_baked.zip`
- `decode_transition_validation`을 DECODE-02D runtime evidence receipt 체계로 승격했습니다.
- `Decode02dRuntimeEvidenceReceipt`, `Decode02dControlledOnSummary`, `Decode02dPromotionDecision`을 추가했습니다.
- `candidate_trace_version >= 4`, `probe_integrity.status == PASS`, transition action/reason/hardblock parity를 ON 후보 승격 필수 조건으로 묶었습니다.
- 기본 transition mode는 계속 `off`입니다. ON 기본값 변경은 없습니다.

## 판단불가
- cargo/rustfmt/WebGPU runtime은 이 환경에서 실행하지 못했습니다.
- 실제 runtime evidence receipt는 `NOT_RUN`이며, `promotion_status`는 `NOT_RUN`/blocked 기준으로 봉인했습니다.

## 비범위
- transition rule redesign
- transition default-on
- dynamic QWave/DeltaK
- Min-P formula change
- semantic prior default enable
- LoRA/SFT training
