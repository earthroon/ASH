# 16AI-QW-38G-R6A-DECODE-02C — Transition Probe Integrity Counters / Safe On Enable Gate Seal

## 확정
- 기준 입력: `ash_pass3_16AI-QW-38G-R6A-DECODE-02B_transition_runtime_probe_baked.zip`
- candidate trace를 V4 계약으로 올리고 `weighted_logit_before_transition`, `weighted_logit_after_transition`, `mask_before_transition`, `mask_after_transition` 계측 슬롯을 추가했습니다.
- `sampler_parity`와 `decode_transition_validation`에 probe mode mutation 판정 상태를 추가했습니다.
- `TRANSITION_ON_CANDIDATE_READY`는 runtime proof 없이는 산출하지 않습니다.

## 판단불가
- cargo/rustfmt/WebGPU runtime은 이 환경에서 실행하지 못했습니다.
- WGSL 실제 validation은 NOT_RUN입니다.

## 비범위
- transition rule redesign
- dynamic QWave/DeltaK
- semantic prior default enable
