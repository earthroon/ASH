# ASH-TCU-K7N-D1R4 SPEC

## Shadow Completion and Readback Gate

## 1. Identity

- Patch: `ASH-TCU-K7N-D1R4_SHADOW_COMPLETION_AND_READBACK_GATE`
- Status: `PASS_ASH_TCU_K7N_D1R4_SHADOW_COMPLETION_AND_READBACK_GATE_ONE_DISPATCH_ONE_COPY_TWO_SUBMITS_ONE_BOUNDED_MAP_16_FINITE_F32_NO_PARITY_NO_OUTPUT_COMMIT`
- Path: `specs/ASH_TCU_K7N_D1R4_SHADOW_COMPLETION_AND_READBACK_GATE_SPEC.md`
- Class: bounded completion observation and scratch readback gate
- Next: `ASH-TCU-K7N-D1R5_NUMERICAL_PARITY_GATE`

D1R4 replays the sealed M1/N16/K4 fixture in a new bounded execution. It does not resurrect D1R3 process-local GPU handles. It performs one TensorCube dispatch, one ordered scratch-to-staging copy, two Queue submissions total, one bounded staging map