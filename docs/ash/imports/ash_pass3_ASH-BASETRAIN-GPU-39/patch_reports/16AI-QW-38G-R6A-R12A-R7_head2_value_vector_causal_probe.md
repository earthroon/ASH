# 16AI-QW-38G-R6A-R12A-R7 — Head2 Value Vector Causal Probe / Layer21 Value-Direction Suppression Seal

## Status
BAKED_STATIC

## Purpose
R7 adds a diagnostic-only causal probe for the R6 finding `HEAD2_VALUE_DIRECTION_DOMINANT_UNIFORM_ATTENTION`.
It does not mutate checkpoint, tokenizer, safetensors, lm_head, final_norm, or ban mask.

## Implemented
- R7 env gate in `native_wgpu.rs`
- Layer21/head2 value intervention raw trace writer
- Baseline head2 contribution metric
- Head2 full value suppression counterfactual metric
- Position20 / position55 value suppression counterfactual metrics
- Target-direction projection removal counterfactual metric
- R7 runner that builds, runs, scores interventions, and emits summary/receipt/report artifacts

## Guard
- diagnostic_intervention_only: true
- root_cause_confirmed: false
- mutation_performed: false
