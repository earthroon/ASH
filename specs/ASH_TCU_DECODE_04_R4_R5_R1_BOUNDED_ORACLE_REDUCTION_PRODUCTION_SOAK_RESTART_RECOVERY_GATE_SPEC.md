# ASH-TCU-DECODE-04-R4-R5-R1
# Bounded Oracle Reduction Production Soak / Restart Recovery Gate

- Patch ID: `ASH-TCU-DECODE-04-R4-R5-R1_BOUNDED_ORACLE_REDUCTION_PRODUCTION_SOAK_RESTART_RECOVERY_GATE`
- Parent: `ASH-TCU-DECODE-04-R4-R5_LEGACY_FRAGMENT_RETIREMENT_READINESS_ORACLE_REDUCTION_GATE`
- Default fragment source: TensorCube
- Oracle reduction: active only inside segmented production-soak gate
- Legacy fallback: mandatory
- Durable publication journal: mandatory
- Durable quarantine: mandatory
- Restart recovery: mandatory
- Operator rollback: mandatory
- Legacy