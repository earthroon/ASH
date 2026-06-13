# 16AI-QW-38G-R6A-WCTX-RT-07 Bake Report

## Patch

`16AI-QW-38G-R6A-WCTX-RT-07 — Candidate Text Draft Shadow / No Review Insert No Commit Seal`

## SSOT

`domain_ssot = en_to_ko_translation_subtitle_machine`

## Baked implementation

- Added `crates/ash_core/src/word_context_rt_candidate_text_draft_shadow.rs`.
- Added `crates/ash_core/src/bin/ash_word_context_rt_candidate_text_draft_shadow.rs`.
- Updated `crates/ash_core/src/lib.rs` exports.
- Added deterministic fixture matrix for RT-07 candidate text draft shadow.
- Added positive draft-shadow cases and negative production/review/commit leak cases.

## Guard boundary

RT-07 may create a candidate text draft shadow from the RT-06 surface-chain bind receipt, but it must not create production candidate text, issue a candidate id, finalize a candidate envelope, insert into review, auto-accept, auto-commit, mutate target subtitles, runtime-apply, train, run backward, or commit weights.

## Local verification commands

```bash
cargo check -p ash_core --bin ash_word_context_rt_candidate_text_draft_shadow
cargo run -p ash_core --bin ash_word_context_rt_candidate_text_draft_shadow
```

## Container status

Cargo/rustc were not available in this environment, so this bake is sealed as static-only.
