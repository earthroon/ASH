# ASH-FT-30
## Shadow Candidate Numeric Drift Probe / No Runtime Apply Seal

SSOT: ASH-FT-30 reads the ASH-FT-29 shadow candidate manifest and shadow tensor map, probes shape/dtype parity, finite/NaN/Inf status, tensor drift, group drift and drift risk, and writes numeric stability receipts only. It must not mutate the base checkpoint, canonical safetensors, runtime default binding, checkpoint alias, promotion registry, or run generation/training.

Key guards:
- `runtime_default_apply_executed: false`
- `checkpoint_alias_rebind_executed: false`
- `promotion_executed: false`
- `generation_executed: false`
- `training_executed: false`

Blocked states are explicit:
- `BLOCKED_ASH_FT30_FT29_NOT_EXECUTED`
- `BLOCKED_ASH_FT30_EMPTY_SHADOW_TENSOR_MAP`
- `BLOCKED_ASH_FT30_NUMERIC_PAYLOAD_UNAVAILABLE`
- `BLOCKED_ASH_FT30_DRIFT_RISK_BLOCKED`
- `BLOCKED_ASH_FT30_HIGH_DRIFT_REVIEW_REQUIRED`

Expected pass verdict:
`PASS_ASH_FT30_SHADOW_CANDIDATE_NUMERIC_DRIFT_PROBE_NO_RUNTIME_APPLY`
