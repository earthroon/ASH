# 16AI-QW-38G-R6A-SALAD-01A Patch Report

## 확정

`SALAD-01A`는 `SALAD-01` 빌드 실패 핫픽스다. 업로드된 로그의 핵심 오류는 `crates/ash_core/src/decision.rs:250`에서 `temperature.min(stable_profile.temperature)`를 호출할 때 `temperature`가 `{float}`로 남아 Rust가 `f32/f64`를 결정하지 못한 것이다.

반영 내용:

```rust
let temperature: f32 = match resolved_task.as_str() {
    "subtitle_polish" => 0.15_f32,
    "translation_assist" => 0.18_f32,
    "json_array_polish" => 0.12_f32,
    _ => 0.20_f32,
};
```

`SAFE_KOREAN_STABLE_V1`의 정책값, repetition penalty, top_p, max_new_tokens 의미는 변경하지 않았다.

## 추정

이 패치로 `error[E0689]`는 해소되어야 한다. 뒤에 다른 컴파일 오류가 숨어 있으면 다음 cargo build에서 새로 드러날 수 있다.

## 판단불가

베이크 컨테이너에는 `cargo` / `rustc`가 없어 실제 빌드는 수행하지 못했다. 로컬에서 `cargo build` 또는 기존 실행 커맨드 재시도가 필요하다.

## Mutation Flags

- checkpoint_modified = false
- tokenizer_modified = false
- safetensors_modified = false
- lm_head_modified = false
- final_norm_modified = false
- ban_mask_modified = false

## Local Check Command

```powershell
cargo build
```

또는 선배가 방금 돌린 동일 커맨드를 재실행하면 된다.
