# QW-TOK-FORGE-01-R3-R1 Acceptance

## Patch

QW-TOK-FORGE-01-R3-R1 — RejectGpuUpload Config Field Bind / Build Unblock Seal

## Acceptance Criteria

- `QwTokForge01S0Config` declares `reject_gpu_upload: bool`.
- Existing default initialization `reject_gpu_upload: true` remains valid.
- CLI flags `--reject-gpu-upload` and `--allow-gpu-upload-execution` compile against the config.
- R2/R3 config builders can read `cfg.reject_gpu_upload`.
- Top-level runtime `artifacts/*.json` are not included in the bake archive.

## Status

BAKED_STATIC_PATCH
