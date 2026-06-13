# SFT-GPU-ACCEPT-02 Acceptance

## 확정

- Generation hygiene acceptance is now designed to execute in a subprocess.
- Parent-side receipt sealing is implemented for native child crashes.
- `STATUS_ACCESS_VIOLATION` / `0xc0000005` is classified as `windows_status_access_violation`.
- Adapter artifacts are preserved when the acceptance child crashes.

## 추정

- This should prevent the main `lora_train` process from dying when WGPU/device/native generation crashes during acceptance.
- If the child crashes, downstream quality eval is intentionally skipped to avoid re-entering the unstable native generation path in-process.

## 판단불가

- Cargo build/test status is unknown in this container because Rust tooling is unavailable.
- Exact native crash origin remains unknown: WGPU request/device, driver, burn-wgpu-local, feature request, or repeated bootstrap.

## Reproduction command

```powershell
cargo test -p lora_train --test generation_hygiene_subprocess_isolation -- --nocapture
cargo test -p lora_train --test generation_hygiene_acceptance_device_isolation -- --nocapture
cargo run -p lora_train -- .\configs\ash_ko_short_sft_lm_head_lora_v1_smoke.json 1
```
