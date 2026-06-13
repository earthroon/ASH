# 16AI-QW-38G-R6A-LORA-RT-02B-F

## Rust Native Backoff Runner / UTF-8 Request File Seal

## SSOT

RT-02B-E proved that the previous PowerShell backoff wrapper failed before inference completion with:

```txt
Error: stream did not contain valid UTF-8
```

This patch removes the PowerShell scale-loop wrapper from the execution SSOT. Backoff now runs inside `orchestrator_local` as a Rust-native command path.

## Implemented

- Added `crates/orchestrator_local/src/domain_adapter_backoff_runner.rs`.
- Added `run.domain_adapter_backoff` command handling inside `orchestrator_local`.
- Added `run_request_file(...)` for UTF-8 JSON request-file execution.
- Added CLI support for:

```powershell
.\target\debug\orchestrator_local.exe --request-file .\workspace\examples\lora_rt02b_f_backoff_request.json
```

and:

```powershell
.\target\debug\orchestrator_local.exe --mode domain-adapter-backoff --request-file .\workspace\examples\lora_rt02b_f_backoff_request.json
```

- Scale attempts are executed in the same Rust process through the internal infer path.
- No `std::process::Command` recursion is used.
- No stdin pipe is used for the backoff request.
- `scale=0.00` is adapter-off baseline:

```txt
domainAdapterEnabled = false
```

- PowerShell backoff scripts are deprecated and fail fast with a clear instruction to use the Rust request-file path.

## Receipts

Expected outputs:

```txt
workspace/lora_rt02b_f_backoff_receipt.json
workspace/lora_rt02b_f_scale_retry_trace.json
workspace/lora_rt02b_f_mojibake_guard_receipt.json
```

## Mutation Contract

```txt
checkpoint_modified = false
tokenizer_modified = false
base_safetensors_modified = false
lm_head_modified = false
final_norm_modified = false
ban_mask_modified = false
```

## Local verification

Cargo is not available in the bake container. Local verification required:

```powershell
cargo build -p orchestrator_local --bin orchestrator_local
.\target\debug\orchestrator_local.exe --request-file .\workspace\examples\lora_rt02b_f_backoff_request.json
```
