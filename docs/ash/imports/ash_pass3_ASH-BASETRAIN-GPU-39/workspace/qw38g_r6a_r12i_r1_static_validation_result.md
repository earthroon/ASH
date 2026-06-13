# 16AI-QW-38G-R6A-R12A-R12I-R1 Static Validation

- status: PASS_STATIC_VALIDATION
- script: `scripts/run_16AI_QW_38G_R6A_R12A_R12I_R1_metric_capture_wiring.ps1`
- script_sha256: `0064ef6bf2718a3236c0f528200c74242495f0a22bc714c365007cc2089b0622`
- cumulative R12I normalization included: True

## Checks
- status = "PASS_METRIC_CAPTURE_WIRING": True
- status = "PARTIAL_METRIC_CAPTURE_WIRING": True
- LOGIT_RANK_MARGIN_CAPTURE_WIRED_AND_PROBED: True
- METRIC_CAPTURE_PARTIALLY_WIRED_EFFECT_STILL_INCOMPLETE: True
- mock_positive_generated = $false: True
- actual_overlay_apply_allowed = $false: True
- NO_MODEL_ARTIFACT_MUTATION: True
- production_safe_confirmed = $false: True
- root_cause_confirmed = $false: True
- workspace: True
- r12i_final_artifact_normalization_present: True
- r12i_r1_script_exists: True
- capture_input_path_supported: True
- partial_capture_requires_flag_or_input: True
