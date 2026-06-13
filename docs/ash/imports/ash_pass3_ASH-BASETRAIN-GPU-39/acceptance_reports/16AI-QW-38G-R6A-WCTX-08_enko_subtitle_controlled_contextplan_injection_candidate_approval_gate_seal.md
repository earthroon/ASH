# 16AI-QW-38G-R6A-WCTX-08 Acceptance Report

## EN-KO Subtitle Controlled ContextPlan Injection Candidate / Approval Gate Seal

### SSOT

```text
Ash is an EN-to-KO translation subtitle-machine domain component.
domain_ssot = en_to_ko_translation_subtitle_machine
```

### Status

```text
PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE
```

`cargo` / `rustc` were not available in the bake container, so this report records static artifact/materialization evidence only. Local Rust toolchain verification remains required.

### Added files

```text
crates/ash_core/src/word_context_context_plan_injection.rs
crates/ash_core/src/bin/ash_word_context_context_plan_injection_candidate.rs
workspace/word_context_probe/wctx_08_enko_context_plan_injection_cases.json
workspace/word_context_probe/wctx_08_enko_context_plan_injection_matrix.json
workspace/word_context_probe/wctx_08_enko_context_plan_injection_summary.json
workspace/word_context_probe/wctx_08_enko_context_plan_injection_sample_receipt.json
workspace/word_context_probe/wctx_08_static_validation.json
```

### Modified files

```text
crates/ash_core/src/lib.rs
```

### Core APIs

```rust
pub fn default_enko_context_plan_injection_candidate_pairs(
) -> Vec<(EnKoContextPlanShadowReceipt, EnKoContextPlanReplayReceipt)>

pub fn build_enko_context_plan_injection_candidate(
    context_plan_receipt: &EnKoContextPlanShadowReceipt,
    replay_receipt: &EnKoContextPlanReplayReceipt,
    active_prompt_snapshot: Option<&str>,
    generation_input_snapshot: Option<&str>,
    placement: EnKoContextPlanInjectionPlacement,
) -> EnKoContextPlanInjectionCandidateReceipt

pub fn run_enko_context_plan_injection_candidate_matrix(
    pairs: &[(EnKoContextPlanShadowReceipt, EnKoContextPlanReplayReceipt)],
    placement: EnKoContextPlanInjectionPlacement,
) -> EnKoContextPlanInjectionCandidateMatrix
```

### Candidate-only invariants

```json
{
  "candidate_created_count": 24,
  "candidate_prompt_created_count": 24,
  "candidate_prompt_applied_count": 0,
  "active_prompt_mutation_count": 0,
  "generation_input_mutation_count": 0,
  "pending_approval_count": 24,
  "approved_count": 0,
  "approval_granted_count": 0,
  "runtime_default_apply_count": 0,
  "rerank_applied_count": 0,
  "marker_missing_count": 0,
  "diff_missing_count": 0,
  "rollback_missing_count": 0,
  "source_text_mutation_count": 0,
  "target_text_mutation_count": 0,
  "timing_mutation_count": 0
}
```

### Matrix summary

```json
{
  "patch_id": "16AI-QW-38G-R6A-WCTX-08",
  "domain_ssot": "en_to_ko_translation_subtitle_machine",
  "total_cases": 24,
  "pass_cases": 24,
  "fail_cases": 0,
  "deterministic_failures": 0,
  "risk_failures": 0,
  "candidate_created_count": 24,
  "candidate_prompt_created_count": 24,
  "candidate_prompt_applied_count": 0,
  "active_prompt_mutation_count": 0,
  "generation_input_mutation_count": 0,
  "pending_approval_count": 24,
  "approved_count": 0,
  "rejected_count": 0,
  "approval_granted_count": 0,
  "runtime_default_apply_count": 0,
  "rerank_applied_count": 0,
  "marker_missing_count": 0,
  "diff_missing_count": 0,
  "rollback_missing_count": 0,
  "source_text_mutation_count": 0,
  "target_text_mutation_count": 0,
  "timing_mutation_count": 0
}
```

### Required markers

The candidate injection block must contain all of the following:

```text
[ASH_WCTX_CONTEXT_PLAN_BEGIN]
[ASH_WCTX_CONTEXT_PLAN_END]
mode: candidate_only
apply: false
```

### Approval gate seal

WCTX-08 always creates a pending approval gate:

```text
status = Pending
requires_operator_approval = true
requires_receipt_review = true
requires_diff_review = true
can_apply_to_runtime = false
approval_granted = false
```

### Non-goals preserved

```text
active prompt mutation: no
generation input mutation: no
candidate prompt applied: no
runtime default apply: no
rerank applied: no
glossary auto apply: no
preserve auto apply: no
particle/ending correction: no
source/target/timing mutation: no
```

### Local verification command

```bash
cargo run -p ash_core --bin ash_word_context_context_plan_injection_candidate
```

### Final seal

WCTX-08 creates a controlled candidate ContextPlan injection payload for review only. It materializes candidate prompt preview, diff, rollback snapshot, and pending approval gate, while keeping active prompt, generation input, rerank, runtime default apply, source English, target Korean, and timing unchanged.
