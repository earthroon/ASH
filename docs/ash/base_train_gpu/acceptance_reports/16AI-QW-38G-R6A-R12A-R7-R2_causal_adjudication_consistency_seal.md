# Acceptance — 16AI-QW-38G-R6A-R12A-R7-R2

## Required Checks
- r12a_r7_source_loaded = true
- r12a_r7_status_pass = true
- r12a_r6_source_loaded = true
- r12a_r6_status_pass = true
- intervention_axis_table_written = true
- source_axis_table_written = true
- adjudication_consistency_matrix_written = true
- r8_target_decision_written = true
- top_causal_intervention_preserved = true
- final_adjudication_preserved = true
- value_direction_result_preserved = true
- top_intervention_vs_adjudication_difference_explained = true
- separate_decision_axes_declared = true
- r8_target_confirmed = true
- root_cause_confirmed = false
- mutation_performed = false

## Run
```powershell
.\scriptsun_16AI_QW_38G_R6A_R12A_R7_R2_causal_adjudication_consistency_seal.ps1 -Build
```
