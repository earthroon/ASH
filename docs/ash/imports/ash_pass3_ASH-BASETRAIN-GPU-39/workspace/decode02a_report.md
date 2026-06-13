# 16AI-QW-38G-R6A-DECODE-02A Report

## 확정
- CandidatePieceHintTable SSOT를 `model_core::decode_candidate_piece_hints`에 추가했다.
- GPU `topp_scan`에 candidate piece hint buffer binding을 추가했다.
- Candidate trace entry를 V3 의미론으로 확장하여 transition risk/penalty/action/reason_mask를 기록한다.
- Probe mode에서는 transition penalty를 기록하되 weighted logit에는 적용하지 않는다.

## 추정
- 실제 런타임에서 CPU/GPU transition parity를 확인하려면 WebGPU compile/runtime validation이 필요하다.

## 판단불가
- cargo check / rustfmt / WGSL runtime compile은 현재 컨테이너에 도구가 없어 NOT_RUN이다.
