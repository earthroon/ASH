# 16AI-QW-38G-R6A-LORA-RT-02B-B

## PowerShell Native Stderr Wrapper / No NativeCommandError Seal

## SSOT

RT-02B-A fixed non-ASCII mojibake literals, but the backoff scripts still used `2>&1 | Tee-Object`. In Windows PowerShell, native stderr lines such as `[debug] incoming banned_token_ids len = 0` can be promoted into `NativeCommandError` records before the script can inspect receipts.

## Patch

- Replaced the native command pipeline with `Invoke-OrchestratorRequest`.
- stdout is redirected to `workspace/<request>.log`.
- stderr is redirected to `workspace/<request>.err.log`.
- stderr is appended to the main log after process exit.
- only nonzero native exit code throws.
- no model/checkpoint/tokenizer mutation.

## Expected behavior

`orchestrator_local.exe` debug lines on stderr no longer abort the PowerShell wrapper when the process exits successfully.
