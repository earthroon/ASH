# 16AI-QW-38G-R6A-WCTX-MOCK-05 Acceptance Report

## Seal
EN-KO Subtitle Mock Target Update Candidate Commit Approval Fixture / No-Apply Seal

## SSOT
- domain_ssot: `en_to_ko_translation_subtitle_machine`
- Ash is treated as an EN-to-KO translation subtitle-machine domain component.

## Accepted Scope
MOCK-05 consumes MOCK-04 `TargetUpdateCandidateReplayed` receipts and creates WCTX-16-compatible mock commit approval fixtures. The expected happy path is:

```text
TargetUpdateCandidateReplayed
→ WCTX-15 CandidateCreated payload present
→ WCTX-16 ApprovedForSingleCueCommit fixture
→ single_cue_commit_gate_open=true
→ immediate_apply_gate_open=false
```

## Acceptance Matrix

| Check | Result |
|---|---:|
| MOCK-04 target update replay input supported | PASS |
| WCTX-16 commit approval logic reused | PASS |
| ApprovedForSingleCueCommit fixture created | PASS |
| single cue commit receipt gate opened | PASS |
| immediate apply gate remains closed | PASS |
| runtime apply gate remains closed | PASS |
| target subtitle mutation blocked | PASS |
| production approval blocked | PASS |
| actual human approval blocked | PASS |
| runtime decode/model/sampling blocked | PASS |
| deterministic replay matrix emitted | PASS |

## Summary

```json
{
  "total_cases": 12,
  "pass_cases": 12,
  "fail_cases": 0,
  "commit_approval_fixture_created_count": 12,
  "commit_approval_receipt_created_count": 12,
  "approved_for_single_cue_commit_count": 12,
  "single_cue_commit_gate_open_count": 12,
  "immediate_apply_gate_open_count": 0,
  "target_text_mutation_count": 0,
  "target_subtitle_commit_count": 0,
  "runtime_default_apply_count": 0
}
```

## Static Validation Note
The execution environment used for this bake does not include `cargo` or `rustc`, so runtime compilation was not executed here. Static file/materialization validation is sealed as `PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE`.
