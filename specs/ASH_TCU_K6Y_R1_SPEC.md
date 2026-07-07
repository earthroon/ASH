# ASH TCU K6Y R1

Export hotfix for K6Y operator canary decision gate.

Fixes the unresolved import for run_ash_tcu_k6y_operator_canary_decision_gate_audit by using the tensorcube_k6y_contract_audit module path in the orchestrator bin and report re-export, and by adding an explicit lib root re-export.

No behavior change. No auto promotion, broad rollout, production replacement, rollback execution, or runtime artifact bake.

PASS target remains PASS_ASH_TCU_K6Y_OPERATOR_CANARY_DECISION_GATE_NO_AUTO_PROMOTION_SEAL.
