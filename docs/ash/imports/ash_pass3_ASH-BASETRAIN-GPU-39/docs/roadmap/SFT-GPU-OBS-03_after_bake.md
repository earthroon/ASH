# SFT-GPU-OBS-03 After-Bake Roadmap

## Completed

SFT-GPU-OBS-03 adds an operator-facing health review queue over OBS-02 long-horizon GPU adapter health ledger output.

Opened:
- operator health review queue
- long-horizon attention queue
- Critical / Held event projection
- operator_attention_required item extraction
- health review console projection
- priority sorting
- review item digest
- review queue seal

Still closed:
- current pointer update
- operator action apply
- fallback activation
- rollback execution
- demotion apply
- quarantine apply
- registry mutation
- promotion apply
- lifecycle mutation
- runtime SFT training
- runtime gradient write
- runtime optimizer step
- partial artifact auto-repair
- silent CPU fallback success
- silent backend switch
- silent registry correction
- textureSample / sampler / normalized UV weight fetch

## Suggested next patches

### SFT-GPU-OBS-04 — Operator Review Receipt Intake / Attention Queue Decision Seal

Purpose:
- consume OBS-03 review queue items
- record operator decisions without applying them directly
- produce reviewed attention item receipt
- preserve queue append-only history

Closed:
- actual action apply
- current pointer switch
- demotion/quarantine apply
- rollback execution

### SFT-GPU-OBS-05 — Reviewed Health Decision to RUN-13 Action Candidate Bridge

Purpose:
- map reviewed OBS-04 decisions into RUN-13-compatible operator action apply candidates
- require explicit action kind and target adapter/slot
- reject recommendation mismatch

Closed:
- unreviewed action apply
- silent registry correction

### SFT-GPU-OBS-06 — Health Review Console Projection Fixture / CLI Smoke

Purpose:
- add deterministic fixtures for review queue projection
- expose CLI or test fixture rendering summaries
- keep action controls disabled

Closed:
- real UI mutation buttons
- lifecycle mutation
