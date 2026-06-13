# 16AI-QW-38G-R6A-R12A-R12F Static Validation

- status: PASS_STATIC_VALIDATION
- script: scripts/run_16AI_QW_38G_R6A_R12A_R12F_policy_locked_canary_case_expansion.ps1
- script_sha256: 22aef06752c1a4392376430b37bd35fbcb8b7ea47cf2078d260fe6c97eadb2e5
- source lock prefix: qw38g_r6a_r12e
- output prefix: qw38g_r6a_r12f
- expected runtime status: PASS_POLICY_LOCKED_CANARY_CASE_EXPANSION
- expected adjudication: CANARY_CASES_RESPECT_POLICY_LOCK
- next patch: 16AI-QW-38G-R6A-R12A-R12G_CANARY_REPLAY_STABILITY_AND_THRESHOLD_EDGE_SWEEP

## Guardrails

- R12E policy regression lock is loaded, not rewritten.
- Canary cases are additive only: cpv_* and cnc_*.
- production_safe_confirmed remains false.
- root_cause_confirmed remains false.
- checkpoint/tokenizer/safetensors/lm_head/final_norm/ban_mask mutation flags remain false.
