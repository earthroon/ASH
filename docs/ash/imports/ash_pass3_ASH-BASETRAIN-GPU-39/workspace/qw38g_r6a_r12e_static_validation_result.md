# 16AI-QW-38G-R6A-R12A-R12E Static Validation

- status: PASS_STATIC_VALIDATION
- script: `scripts/run_16AI_QW_38G_R6A_R12A_R12E_stability_replay_and_policy_regression_lock.ps1`
- script_sha256: `42d7a1399eb3392e19090d2db46fa4dfca8a6da2ab9dfbbe0886a24946ad3035`
- runtime_executed_here: false
- note: PowerShell is not available in this container, so local execution is required.

## Command

```powershell
.\scripts\run_16AI_QW_38G_R6A_R12A_R12E_stability_replay_and_policy_regression_lock.ps1 -Build -Strict -ReplayCount 3
```

## Safety

- production_safe_confirmed: false
- root_cause_confirmed: false
- checkpoint_modified: false
- tokenizer_modified: false
- safetensors_modified: false
- lm_head_modified: false
- final_norm_modified: false
- ban_mask_modified: false
