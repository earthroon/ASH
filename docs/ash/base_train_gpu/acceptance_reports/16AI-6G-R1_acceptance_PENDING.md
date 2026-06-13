# 16AI-6G-R1 Acceptance

Status: PENDING_RUNTIME

## Scope

- Patch type: loader schema fallback fix
- generation: unchanged
- checkpoint_required: unchanged
- assembly_commit_mode: compare-only
- default_commit: false
- token_ids_mutated: false
- committed_prompt_ids: branch-local compare only

## Acceptance Criteria

- [x] `load_assembly_cases` accepts tokenizer reference for baseline fallback.
- [x] result-level `baseline_token_ids` / `assembled_token_ids` remain supported.
- [x] nested `assembly_results[0].baseline_token_ids` / `assembled_token_ids` are supported.
- [x] nested `assembly_result` / `assembly` / `assembly_view` are supported.
- [x] baseline ids may fall back to `tokenizer.encode(wrapped_text)`.
- [x] assembled ids are not silently fabricated when absent.
- [x] compare-only default commit behavior is preserved.
- [x] token_ids_mutated=false is preserved.

## Runtime Pending

Run:

```powershell
.\scripts\run_16AI_6G_wrapper_quality_recompare.ps1
```

Expected next target:

```txt
No `missing baseline ids` error in load_assembly_cases.
```
