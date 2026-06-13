# 16AI-QW-38G-R6A-WCTX-RT-08 Acceptance Report

## Acceptance Matrix

- Positive cases: 4
- Negative cases: 42
- Total cases: 46

## Required invariants

- Draft shadow receipt bind is allowed.
- New draft shadow generation is blocked.
- Production candidate text is blocked.
- Review-ready / commit-ready candidate leaks are blocked.
- Candidate envelope finalization and candidate id issuance are blocked.
- Review queue insert, review queue candidate creation, and review receipt finalization are blocked.
- Auto accept, auto commit, target mutation, runtime apply, and production subtitle mutation are blocked.
- Training, backward, and weight commit are blocked.

## Local commands

```bash
cargo check -p ash_core --bin ash_word_context_rt_candidate_draft_shadow_receipt_bind
cargo run -p ash_core --bin ash_word_context_rt_candidate_draft_shadow_receipt_bind
```

## Status

`BAKED_STATIC_NO_CARGO`
