# 16AI-QW-38G-R6A-LORA-RT-02B — Adapter Delta Norm Clamp / Mojibake Backoff Seal

## Purpose

Full `shared_hidden_token_head_lora` adapter scale `0.25` was confirmed to apply through RT-02, but it produced an unsafe output while `delta_to_base_abs_max_ratio` reached about `0.5057`. RT-02B adds a clamp/backoff layer so over-strong adapter deltas are not silently promoted.

## Implemented

- `domainAdapterNormClampEnabled=true` now defaults `domain_adapter_max_delta_to_base_ratio` to `0.35` when no explicit ratio is supplied.
- Native apply receipts now classify `delta_to_base_abs_max_ratio` into `safe`, `warning`, `backoff_required`, or `hard_disable_candidate`.
- Native apply receipts now expose `domain_adapter_norm_clamp_passed`.
- If strict guard disables adapter delta before sampling, receipt status becomes `PASS_DOMAIN_ADAPTER_DELTA_GUARD_DISABLED` instead of pretending a delta was applied.
- Added `workspace/examples/lora_rt02b_full_backoff.ps1`, a practical backoff runner:
  - starts at scale `0.25`, then tries `0.15`, `0.10`, `0.05`, `0.0`;
  - uses strict delta guard with default max ratio `0.35`;
  - detects mojibake patterns such as `?댁`, `?몄`, `?뗭`, `?곸`, `媛`, `怨`, `由ъ`, etc.;
  - writes backoff, mojibake guard, and scale retry trace receipts;
  - patches the accepted output artifact with backoff metadata.
- Added `workspace/examples/lora_rt02b_verify.ps1` for receipt review.
- Added `workspace/examples/lora_rt02b_scale_sweep_low.ps1` for low-scale-only sweep.

## Runtime SSOT

- Adapter application remains RT-02: `base_logits + scale * (alpha / rank) * (B @ (A @ hidden))`.
- RT-02B is the safety layer: norm clamp before sampling, mojibake/backoff after output observation via wrapper.
- Base checkpoint, tokenizer, LM head, final norm, and ban mask are not modified.

## Run

```powershell
.\workspace\examples\lora_rt02b_full_backoff.ps1
.\workspace\examples\lora_rt02b_verify.ps1
```

For low-scale sweep only:

```powershell
.\workspace\examples\lora_rt02b_scale_sweep_low.ps1
```

## Expected receipts

- `workspace/lora_rt02b_full_backoff_01_backoff_receipt.json`
- `workspace/lora_rt02b_full_backoff_01_mojibake_guard_receipt.json`
- `workspace/lora_rt02b_full_backoff_01_scale_retry_trace.json`

## Not run in this bake container

- `cargo check` was not run because `cargo` is unavailable in this environment.
- Actual local inference backoff must be run on the Windows ASH machine with the rebuilt `orchestrator_local.exe`.


## 16AI-QW-38G-R6A-LORA-RT-02B-A Hotfix

PowerShell wrapper scripts were rewritten as ASCII-only files.

Reason:
- Windows PowerShell may parse UTF-8-without-BOM mojibake pattern literals as ANSI.
- The previous mojibake detector stored broken Korean/CP949 residue literals directly in a string array.
- That caused parser errors before runtime.

Fix:
- Removed all non-ASCII mojibake literals from `workspace/examples/lora_rt02b_full_backoff.ps1`.
- Replaced literal pattern matching with ASCII-safe regex shapes:
  - `\?[^\x00-\x7F]` for question mark + non-ASCII clusters.
  - `[\u4E00-\u9FFF]` for CJK garbage residue.
  - `\uFFFD` for Unicode replacement character.
  - question mark density and tokenizer direct decode mismatch.
- Rewrote `lora_rt02b_scale_sweep_low.ps1` and `lora_rt02b_verify.ps1` as ASCII-only scripts.

Status:
- `lora_rt02b_full_backoff.ps1` non-ASCII byte count: 0
- `lora_rt02b_scale_sweep_low.ps1` non-ASCII byte count: 0
- `lora_rt02b_verify.ps1` non-ASCII byte count: 0

Patch id:
- 16AI-QW-38G-R6A-LORA-RT-02B-A
