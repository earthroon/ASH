# RT-02B-F Rust Native Backoff Runner

PowerShell backoff wrappers are deprecated for this seal.

Build:

```powershell
cargo build -p orchestrator_local --bin orchestrator_local
```

Run with a UTF-8 JSON request file:

```powershell
.\target\debug\orchestrator_local.exe --request-file .\workspace\examples\lora_rt02b_f_backoff_request.json
```

Optional explicit mode:

```powershell
.\target\debug\orchestrator_local.exe --mode domain-adapter-backoff --request-file .\workspace\examples\lora_rt02b_f_backoff_request.json
```

Receipts:

- `workspace/lora_rt02b_f_backoff_receipt.json`
- `workspace/lora_rt02b_f_scale_retry_trace.json`
- `workspace/lora_rt02b_f_mojibake_guard_receipt.json`
