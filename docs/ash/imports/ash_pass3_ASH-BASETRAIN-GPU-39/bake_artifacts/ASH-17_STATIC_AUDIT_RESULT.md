# ASH-17 Static Audit Result

## Status
PASS_STATIC

## Checked
- path_integral_router: `crates/ash_core/src/path_integral_synapse_router.rs`
- ash_core_lib: `crates/ash_core/src/lib.rs`
- ash_core_tests: `crates/ash_core/tests/ash_17_path_integral_synapse_router.rs`
- orchestrator_report: `crates/orchestrator_local/src/ash_17_path_integral_route_report.rs`
- orchestrator_bin: `crates/orchestrator_local/src/bin/ash_17_path_integral_synapse_audit.rs`
- orchestrator_tests: `crates/orchestrator_local/tests/ash_17_path_integral_synapse_report.rs`
- acceptance: `acceptance_reports/ASH-17_path_integral_lora_synapse_router.md`

## Required markers
- ASH_17_ROUTE_PASS_STATUS
- AshPathIntegralSelectionMode
- AshPathIntegralSynapseRouterInput
- AshSynapsePathStep
- AshSynapsePathCandidate
- AshPathIntegralSynapseRoutePlan
- generate_path_candidates_deterministic_beam
- normalize_path_probability_weights
- build_path_integral_synapse_route_plan
- PASS_PATH_INTEGRAL_LORA_SYNAPSE_ROUTER

## Python validator present
False

## Failures
- none
