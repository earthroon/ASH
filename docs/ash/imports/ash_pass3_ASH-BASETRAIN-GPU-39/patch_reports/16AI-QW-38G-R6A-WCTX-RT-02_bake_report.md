# 16AI-QW-38G-R6A-WCTX-RT-02 Bake Report

## Patch

- `16AI-QW-38G-R6A-WCTX-RT-02`
- `Token Selection Shadow Probe / No Decode No Candidate Commit Seal`
- Domain SSOT: `en_to_ko_translation_subtitle_machine`

## Baked Files

- `crates/ash_core/src/word_context_rt_token_selection_shadow_probe.rs`
- `crates/ash_core/src/bin/ash_word_context_rt_token_selection_shadow_probe.rs`
- `crates/ash_core/src/lib.rs`
- `patch_reports/16AI-QW-38G-R6A-WCTX-RT-02_bake_report.md`
- `acceptance_reports/16AI-QW-38G-R6A-WCTX-RT-02.md`
- `WCTX_RT_02_STATIC_CHECKS.txt`
- `WCTX_RT_02_BAKE_MANIFEST.json`

## Scope

RT-02 permits token selection only as a shadow computation over prior RT-01 forward output shape evidence.
It does not decode, generate candidate text, finalize a candidate envelope, insert into the review queue, auto-accept, auto-commit, mutate target text, runtime-apply, train, backward, or commit weights.

## Cases

Positive shadow cases:

- `rt02:greedy_shadow_selection_probe`
- `rt02:top_k_shadow_selection_probe`
- `rt02:nucleus_shadow_selection_probe`
- `rt02:safety_masked_greedy_shadow_probe`

Negative blocked cases cover:

- missing upstream RT-01/RT-00/MOCK-20/source/envelope/provenance/review receipt keys
- unsupported source
- logits shape/finite/digest/full-logits violations
- shadow selection not allowed/missing/token missing/digest missing/tie-break missing
- selection commit leak
- decode/generation/stochastic sampling/token decoded leaks
- decoded text/candidate text/candidate envelope/review queue leaks
- auto accept/auto commit/target mutation/runtime apply leaks
- training/backward/weight commit leaks
- production safe leak

## Verification Status

- Static file insertion: PASS
- `lib.rs` export insertion: PASS
- Brace balance check: PASS
- Cargo check/run: NOT RUN; container has no `cargo`/`rustc`.

## Local Commands

```bash
cargo check -p ash_core --bin ash_word_context_rt_token_selection_shadow_probe
cargo run -p ash_core --bin ash_word_context_rt_token_selection_shadow_probe
```

Expected outputs:

```text
workspace/word_context_probe/wctx_rt_02_token_selection_shadow_probe_cases.json
workspace/word_context_probe/wctx_rt_02_token_selection_shadow_probe_receipts.json
workspace/word_context_probe/wctx_rt_02_token_selection_shadow_probe_matrix.json
workspace/word_context_probe/wctx_rt_02_token_selection_shadow_probe_summary.json
workspace/word_context_probe/wctx_rt_02_token_selection_shadow_probe_sample_receipt.json
```
