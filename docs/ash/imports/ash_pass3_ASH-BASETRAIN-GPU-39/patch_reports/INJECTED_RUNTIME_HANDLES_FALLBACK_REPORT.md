# Injected runtime handles fallback

## What changed
- Replaced `burn-wgpu-local` runtime-handle extractor stub with a real standalone WebGPU device/queue initializer cached in `OnceLock`.
- Added `pollster` dependency to `burn-wgpu-local` for synchronous adapter/device creation.
- Relaxed `model_core` native trace submit so zero-copy is no longer mandatory; host-upload bridge mode is allowed and logged.

## Why
The previous extractor always returned `None`, so native trace submit always fell back before any GPU-side trace work could start. This patch makes runtime handles available even when same-device extraction is unavailable, allowing the native trace pipeline to proceed with host-upload bridging.

## Tradeoff
This is not same-device zero-copy. It is a practical injected fallback path intended to replace the stub and let the native trace path execute.
