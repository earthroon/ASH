# SFT-GPU-OBS-07 After Bake Roadmap

## Current SSOT
Latest baked line:

```txt
SFT-GPU-OBS-07 — Reviewed Candidate Apply Plan / Dry-run Transaction Seal
```

OBS-07 converts an OBS-06 preflight-approved candidate into a dry-run transaction plan. It records what would happen during a later apply, but performs nothing.

## Opened
```txt
reviewed candidate apply plan generation
dry-run transaction plan
candidate kind to plan kind deterministic mapping
planned operation would_* summary
apply plan ledger append
no-apply dry-run seal
```

## Still Closed
```txt
current pointer update
fallback activation
rollback execution
demotion apply
quarantine apply
registry mutation
lifecycle mutation
runtime SFT training
runtime gradient write
runtime optimizer step
textureSample / sampler / normalized UV weight fetch
```

## Natural Next Step
```txt
SFT-GPU-OBS-08 — Dry-run Apply Plan Review Receipt / Final Apply Candidate Seal
```

OBS-08 should review the dry-run plan and produce a final apply candidate seal, still without applying. Actual mutation should remain behind a separate operator-reviewed apply gate.

## Local Verification
```bash
cargo test -p ash_core sft_gpu_obs_07 -- --nocapture
cargo test -p lora_train gpu_candidate_apply_plan -- --nocapture
cargo test -p burn_webgpu_backend gpu_candidate_apply_plan_signals -- --nocapture
cargo test -p ash_core sft_gpu_obs_06 -- --nocapture
```
