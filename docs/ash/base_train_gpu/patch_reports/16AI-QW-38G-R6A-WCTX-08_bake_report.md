# 16AI-QW-38G-R6A-WCTX-08 Bake Report

## Patch

```text
16AI-QW-38G-R6A-WCTX-08
EN-KO Subtitle Controlled ContextPlan Injection Candidate / Approval Gate Seal
```

## SSOT

```text
Ash = EN-to-KO translation subtitle-machine domain
domain_ssot = en_to_ko_translation_subtitle_machine
```

## Input baseline

```text
ash_pass3_16AI-QW-38G-R6A-WCTX-07_enko_subtitle_contextplan_shadow_replay_no_prompt_mutation_baked.zip
```

## Materialized files

```text
crates/ash_core/src/word_context_context_plan_injection.rs
crates/ash_core/src/bin/ash_word_context_context_plan_injection_candidate.rs
workspace/word_context_probe/wctx_08_enko_context_plan_injection_cases.json
workspace/word_context_probe/wctx_08_enko_context_plan_injection_matrix.json
workspace/word_context_probe/wctx_08_enko_context_plan_injection_summary.json
workspace/word_context_probe/wctx_08_enko_context_plan_injection_sample_receipt.json
workspace/word_context_probe/wctx_08_static_validation.json
acceptance_reports/16AI-QW-38G-R6A-WCTX-08_enko_subtitle_controlled_contextplan_injection_candidate_approval_gate_seal.md
patch_reports/16AI-QW-38G-R6A-WCTX-08_bake_report.md
```

## Modified files

```text
crates/ash_core/src/lib.rs
```

## Implemented structures

```text
EnKoContextPlanInjectionPlacement
EnKoInjectionApprovalStatus
EnKoPromptInjectionBlock
EnKoContextPlanInjectionCandidate
EnKoPromptDiffKind
EnKoPromptInjectionDiff
EnKoInjectionApprovalGate
EnKoInjectionRollbackSnapshot
EnKoContextPlanInjectionCandidateRisk
EnKoContextPlanInjectionCandidateReceipt
EnKoContextPlanInjectionCandidateMatrix
```

## Core behavior

```text
WCTX-06 ContextPlan receipt + WCTX-07 Replay receipt
→ candidate ContextPlan injection block
→ candidate prompt preview
→ no-active-prompt mutation diff
→ pending approval gate
→ rollback snapshot
→ deterministic receipt
```

## Static result

```text
total_cases = 24
pass_cases = 24
candidate_created_count = 24
candidate_prompt_created_count = 24
candidate_prompt_applied_count = 0
active_prompt_mutation_count = 0
generation_input_mutation_count = 0
pending_approval_count = 24
approval_granted_count = 0
runtime_default_apply_count = 0
rerank_applied_count = 0
marker_missing_count = 0
diff_missing_count = 0
rollback_missing_count = 0
```

## Toolchain note

```text
cargo/rustc unavailable in bake container.
status = PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE
```

## Next patch

```text
16AI-QW-38G-R6A-WCTX-09
EN-KO Subtitle ContextPlan Injection Approval Receipt / Manual Apply Gate Seal
```
