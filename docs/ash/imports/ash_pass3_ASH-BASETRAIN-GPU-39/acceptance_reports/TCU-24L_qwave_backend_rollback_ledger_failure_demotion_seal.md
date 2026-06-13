# TCU-24L — QWave Backend Rollback Ledger / Failure Demotion Seal

## SSOT

- Source: TCU-24K `QWaveBackendApplySandboxReport`
- State owner: `crates/burn_webgpu_backend/src/qwave_backend_rollback_ledger.rs`
- Purpose: classify sandbox smoke outcomes and seal rollback/demotion/quarantine/operator-review records.

## Acceptance

1. TCU-24K sandbox report is consumed as source evidence.
2. Sandbox smoke status is mapped to deterministic failure kind/severity/demotion action.
3. `SmokePassed` keeps candidate healthy.
4. `SmokeNotRunAdapterUnavailable` is sealed as NotRun and does not demote health.
5. `SmokeFailedDispatch` demotes candidate health without automatic quarantine.
6. `SmokeFailedParity` quarantines candidate and requires rollback review.
7. Rollback backend pointer remains `LegacyElevenBuffer`.
8. Rollback may be required, but rollback execution is forbidden.
9. Candidate quarantine requires operator review, new parity pass, and new sandbox smoke pass before release.
10. Operator review receipt is created, but not bound to TCU-21 global queue yet.
11. Current backend pointer is not changed.
12. Active backend is not changed.
13. Production default is not changed.
14. Persistent runtime apply is not allowed.
15. Runtime mutation flags remain false.
16. Runtime JSON artifacts are emitted under `workspace/runtime/tensorcube`.

## Safety seal

`Rollback ledger may require rollback. Rollback ledger must not execute rollback.`
