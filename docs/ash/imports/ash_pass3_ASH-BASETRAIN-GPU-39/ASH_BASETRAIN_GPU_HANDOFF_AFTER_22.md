# ASH BaseTrain GPU Handoff After 22

## Current SSOT

ASH-BASETRAIN-GPU-22 should audit the ASH-BASETRAIN-GPU-21 local-window loss scalar:

- local_nll_loss = 7.624619041439192
- local_logsumexp = 7.624618969470094
- target_logit = -0.00000007196909734830115
- payload digest = 856552759fc5e7f0b0b7c7b2de78fe0f1e59f82b2ff7c935f819758572878052

## Next patch if PASS

ASH-BASETRAIN-GPU-23  
Loss Repeatability Audit / Repeated Local Window Target 1 Loss Scalar Stability No Backward No Optimizer Seal

## Guardrail

Do not open full-vocab loss, dataset training loss, backward, optimizer, delta apply, or weight commit from 22.
