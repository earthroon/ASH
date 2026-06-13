# Acceptance — 16AI-QW-38G-R6A-R12A-R7

## Static Acceptance
- R7 env gate exists
- R7 raw trace path exists
- R7 runner exists
- R7 intervention scoreboard paths declared
- R7 preserves all no-mutation guards

## Runtime Acceptance
Run:

```powershell
.\scripts\run_16AI_QW_38G_R6A_R12A_R7_head2_value_vector_causal_probe.ps1 -Build
```

Expected artifacts:
- workspace/qw38g_r6a_r12a_r7_head2_value_vector_causal_probe_receipt.json
- workspace/qw38g_r6a_r12a_r7_intervention_scoreboard.json
- workspace/qw38g_r6a_r12a_r7_causal_margin_delta_matrix.json
- workspace/qw38g_r6a_r12a_r7_head2_value_vector_causal_probe_report.md
