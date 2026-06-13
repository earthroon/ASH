# 16AI-QW-38G-R6A-R12A-R12H Static Validation

- status: PASS_STATIC_VALIDATION
- validation_scope: script_and_artifact_contract_static_only
- R12G-R1 cumulative repair included: true
- R12G script SHA256: `2896da302b2bfe475b182adf5a8903cf42439bc62b701631e94c42bd17c384ef`
- R12H script SHA256: `0e9e79eb6bf7eb1e37a4a3a340cd1aaaa5465b2ed395beac58117e625451f3ff`

## Script
`scripts/run_16AI_QW_38G_R6A_R12A_R12H_guard_locked_limited_apply_trial.ps1`

## Expected command
```powershell
.\scripts\run_16AI_QW_38G_R6A_R12A_R12H_guard_locked_limited_apply_trial.ps1 -Build -Strict -TrialPromptVariantCount 3 -TrialNegativeControlCount 3
```

## Note
PowerShell runtime was not available in this environment, so this bake is statically validated. Runtime validation should be performed locally after overlaying the zip onto `ash_pass3`.
