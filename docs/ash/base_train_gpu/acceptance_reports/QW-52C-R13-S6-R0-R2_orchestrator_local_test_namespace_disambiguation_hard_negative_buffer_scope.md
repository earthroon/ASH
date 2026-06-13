# QW-52C-R13-S6-R0-R2
## Orchestrator Local Test Namespace Disambiguation / Hard Negative Buffer Scope Seal

## 1. SSOT
- base_patch: QW-52C-R13-S6-R0-R1
- parent_ssot: QW-52C-R13 / PassNoApply / NoPromotion
- runtime_apply_allowed: false
- promotion_eligible: false
- weight_commit_allowed: false
- safe_profile_apply_allowed: false
- policy_promotion_allowed: false

## 2. Applied Repairs
- Qualified ambiguous orchestrator audit report calls in four orchestrator_local tests.
- Added explicit `ash_core::hard_negative_replay::AshHardNegativeReplayBuffer` import for the hard negative replay eval test.
- Did not modify S6 replay logic, runtime trace artifacts, sampler, logits, or token selection.

## 3. Changed Files
- `crates/orchestrator_local/tests/ash_42_sft_training_run_report.rs`
- `crates/orchestrator_local/tests/ash_43_event_tag_runtime_router_report.rs`
- `crates/orchestrator_local/tests/ash_41_plasticity_dataset_export_report.rs`
- `crates/orchestrator_local/tests/ash_35_event_sft_sampling_report.rs`
- `crates/orchestrator_local/tests/ash_27_hard_negative_replay_eval_report.rs`

## 4. Static Validation
- qualified_orchestrator_audit_calls_present: true
- hard_negative_buffer_explicit_import_present: true
- crates_js_ts_added: false
- cargo_check_verified: false in bake environment

## 5. Local Verification Commands
```powershell
cargo check --workspace --all-targets
cargo run --bin qw52c_r13_s6_runtime_topk_shadow_observation_replay
cargo run --bin qw52c_r13_s6_runtime_topk_shadow_observation_replay_validate
```

## 6. Next Patch Recommendation
- If cargo check passes: `QW-52C-R13-S6-R1 Real Runtime TopK Trace Capture / Re-run S6 Seal`
- If new blockers appear: cut `QW-52C-R13-S6-R0-R3` with the exact remaining compile blocker set.
