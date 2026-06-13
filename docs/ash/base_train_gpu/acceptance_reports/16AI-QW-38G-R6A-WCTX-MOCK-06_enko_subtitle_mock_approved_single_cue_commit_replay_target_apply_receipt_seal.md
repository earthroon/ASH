# 16AI-QW-38G-R6A-WCTX-MOCK-06 Acceptance Report

## Seal
EN-KO Subtitle Mock Approved Single-Cue Commit Replay / Target Apply Receipt Seal

## SSOT
- domain_ssot: `en_to_ko_translation_subtitle_machine`
- Ash is treated as an EN-to-KO translation subtitle-machine domain component.

## Accepted Scope
MOCK-06 consumes MOCK-05 `CommitApprovalFixtureCreated` receipts and replays their paired WCTX-15/WCTX-16 receipts through WCTX-17 single-cue commit logic. The expected happy path is:

```text
CommitApprovalFixtureCreated
→ WCTX-16 ApprovedForSingleCueCommit
→ WCTX-17 Committed
→ commit_patch_created=true
→ rollback_snapshot_created=true
→ production_subtitle_store_mutated=false
```

## Acceptance Matrix

| Check | Result |
|---|---:|
| MOCK-05 commit approval fixture input supported | PASS |
| WCTX-17 single cue commit logic reused | PASS |
| Committed receipt generated | PASS |
| commit patch generated | PASS |
| rollback snapshot generated | PASS |
| target mutation allowed inside receipt | PASS |
| production subtitle store mutation blocked | PASS |
| runtime apply blocked | PASS |
| rerank blocked | PASS |
| production commit blocked | PASS |
| deterministic replay matrix emitted | PASS |

## Summary

```json
{
  "total_cases": 12,
  "pass_cases": 12,
  "fail_cases": 0,
  "single_cue_commit_replayed_count": 12,
  "committed_count": 12,
  "commit_patch_created_count": 12,
  "rollback_snapshot_created_count": 12,
  "target_text_mutated_in_receipt_count": 12,
  "target_subtitle_committed_in_receipt_count": 12,
  "production_subtitle_store_mutation_count": 0,
  "runtime_default_apply_count": 0
}
```

## Static Validation Note
The execution environment used for this bake does not include `cargo` or `rustc`, so runtime compilation was not executed here. Static file/materialization validation is sealed as `PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE`.
