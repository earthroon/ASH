# ASH BaseTrain GPU Handoff After 23

## Latest patch

```txt
ASH-BASETRAIN-GPU-23
Loss Repeatability Audit /
Repeated Local Window Target 1 Loss Scalar Stability No Backward No Optimizer Seal
```

## SSOT

- Source SSOT: `ASH-BASETRAIN-GPU-22` PASS loss scalar audit.
- Payload SSOT: raw 2048 logits payload digest `856552759fc5e7f0b0b7c7b2de78fe0f1e59f82b2ff7c935f819758572878052`.
- State owner: `ASH-BASETRAIN-GPU-23` loss repeatability audit state.

## Next route

If PASS:

```txt
ASH-BASETRAIN-GPU-24
GPU Local Loss Candidate /
Window 2048 Target 1 Loss Kernel Candidate No Backward No Optimizer Seal
```

If FAIL:

```txt
ASH-BASETRAIN-GPU-23A
Loss Repeatability Failure Triage /
Payload Loss Numeric Formula Or Boundary Blocker Detail No Optimizer Seal
```
