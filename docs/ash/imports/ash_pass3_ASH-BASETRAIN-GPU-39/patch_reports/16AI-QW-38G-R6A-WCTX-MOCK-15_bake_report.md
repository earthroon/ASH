# 16AI-QW-38G-R6A-WCTX-MOCK-15 Bake Report

## Patch

**Patch ID:** `16AI-QW-38G-R6A-WCTX-MOCK-15`  
**Title:** Negative Chain Matrix / Missing Stage Source-Key Duplicate Runtime-Leak Block Seal  
**Domain SSOT:** `en_to_ko_translation_subtitle_machine`

## Implemented Files

- `crates/ash_core/src/word_context_mock_negative_chain_matrix.rs`
- `crates/ash_core/src/bin/ash_word_context_mock_negative_chain_matrix.rs`
- `crates/ash_core/src/lib.rs`
- `crates/ash_core/src/word_context_mock_wctx_e2e_chain_index.rs`

## Implementation Summary

MOCK-15 now creates a deterministic negative fixture matrix from the existing MOCK-14 happy-path WCTX chain input bundle. Each case mutates one boundary condition and verifies that the MOCK-14 chain index receipt blocks the corrupted chain.

The implemented negative matrix covers:

1. missing candidate fixture stage
2. missing review replay stage
3. missing approval fixture stage
4. missing target update candidate stage
5. missing commit approval stage
6. missing single cue commit stage
7. missing single cue rollback stage
8. source receipt key mismatch
9. cue id mismatch
10. duplicate receipt key
11. empty audit export packet
12. empty audit inspector packet
13. empty archive entry
14. archive query missing entry
15. runtime apply gate open leak
16. runtime apply executed leak
17. runtime default apply enabled leak
18. rerank applied leak
19. mock mislabeled as runtime
20. production safe true leak
21. production target mutation leak
22. production subtitle store mutation leak

## Existing Validator Rebind

`word_context_mock_wctx_e2e_chain_index.rs` status mapping was tightened so existing block reasons do not fall through to `BlockedUnknown`:

- `RuntimeDefaultApplyEnabled` -> `BlockedRuntimeApplyGateOpen`
- `RerankApplied` -> `BlockedMutationInvariantBreach`
- `ProductionSafeUnexpected` -> `BlockedMutationInvariantBreach`

This keeps MOCK-15 from producing vague negative results when the reason is already known.

## Runtime / Model Boundary

This patch does **not** execute:

- runtime decode
- generation
- model forward
- sampling
- checkpoint apply
- weight commit
- promotion
- production subtitle store mutation

The CLI only writes deterministic JSON receipts under `workspace/word_context_probe/` when run in a Rust environment.

## CLI

```bash
cargo run -p ash_core --bin ash_word_context_mock_negative_chain_matrix
```

Expected outputs:

- `workspace/word_context_probe/wctx_mock_15_negative_chain_cases.json`
- `workspace/word_context_probe/wctx_mock_15_negative_chain_matrix.json`
- `workspace/word_context_probe/wctx_mock_15_negative_chain_summary.json`
- `workspace/word_context_probe/wctx_mock_15_negative_chain_sample_receipt.json`

## Static Bake Status

Cargo was not executed in this container because `cargo` / `rustc` are unavailable. Static file, export, and brace-balance checks were performed.
