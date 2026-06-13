# QW-54F Acceptance

## Required local commands

```powershell
cargo check -p model_core --lib
cargo check -p runtime --all-targets
cargo build --release --manifest-path .\crates\runtime\Cargo.toml --example infer_only -j 1
```

## Expected runtime evidence

```powershell
.\target\release\examples\infer_only.exe `
  --runtime-profile .\specs\runtime_profile.toml `
  --task subtitle_polish `
  --text "I thought you were going to leave me behind." `
  --max-new-tokens 160 `
  --seed 42 `
  --enable-qw54f `
  --qw54f-trace `
  --json
```

Expected files:

- `workspace/runtime_traces/qw54f_candidate_rerank_trace.jsonl`
- `workspace/trace/qw54f_real_infer_apply_receipt.json`
- `artifacts/qw54f_real_infer_rerank_report.json`

## Invariants

- `hard_ban_used = false`
- `token_masked = false`
- `vocab_removed = false`
- `rerank_delta` is finite
