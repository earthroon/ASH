# 16AI-QW-38G-R6A-DECODE-00 — Token Decode SSOT / Word Salad Distribution Probe Seal

## 확정

- `tokenizer_core::decode_ssot`를 추가해 token id / piece / text 변환 규칙의 canonical owner로 지정했다.
- `NativeTokenizer::decode`는 자체 decode 로직을 유지하지 않고 `decode_manifest_token_sequence()` thin wrapper로 낮췄다.
- `runtime/src/infer/output_text.rs`의 final output detokenize 경로는 `decode_ssot::decode_piece_sequence_to_text()`를 사용한다.
- `model_core/src/sampling_helpers.rs`의 streaming detokenize 경로도 같은 `decode_ssot`를 사용한다.
- `DecodeStepProbe` / `TopTokenProbe` 구조를 추가해 selected id/piece/text, top-N, eos rank/logit, sampler requested/applied/fallback 여부를 같은 영수증에 담을 수 있게 했다.
- `workspace/decode00_distribution_probe_schema.json`과 `workspace/decode00_distribution_probe.jsonl` 샘플을 추가했다.

## 추정

- `[29899, 2]` 류의 tail은 이제 `▁이어가고 + <eos>`를 output text에서는 `이어가고`로, probe에서는 `<eos>` control token으로 분리해 볼 수 있다.
- `?댁뼱媛怨?` 같은 mojibake preview는 decode SSOT의 `mojibake_suspected` 플래그로 감지 가능하다.

## 판단불가

- 컨테이너에 `cargo`, `rustc`, `rustfmt`가 없어 컴파일/테스트/포맷 검증은 실행하지 못했다.
- 실제 top-N logits dump 연결은 후속 런타임 실행 환경에서 검증해야 한다.

## 비범위

- CPU oracle sampler 구현
- WebGPU active-set renormalization
- ΔK/QWave weighted Min-P
- context router 학습
