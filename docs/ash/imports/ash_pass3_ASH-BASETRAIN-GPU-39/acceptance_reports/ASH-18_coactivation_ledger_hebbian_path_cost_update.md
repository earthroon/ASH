# ASH-18 Coactivation Ledger / Hebbian Path Cost Update

## Status
PASS_COACTIVATION_LEDGER_HEBBIAN_UPDATE

## Sealed
- AshInferenceOutcomeKind
- AshCoactivationFailureTag
- AshCoactivationEvent
- AshAdapterCoactivationPairStat
- AshCoactivationLedger
- AshHebbianUpdateProposalKind
- AshHebbianUpdateProposal
- AshHebbianUpdateProposalSet
- coactivation event validation
- pair stat accumulation
- fail ratio / confidence recomputation
- Hebbian-style update proposal generation
- ledger-based instability penalty lookup
- explicit apply gate

## Policy
- ASH-17 path result becomes coactivation evidence.
- ASH-18 does not mutate LoRA tensors.
- ASH-18 does not silently mutate the synapse registry.
- All weight changes are proposals.
- All proposals require explicit apply.
- Silent fallback cannot be Pass.
- Base-only cannot have activated adapters.
- Pair keys are stable and deterministic.
- Python validator is forbidden.

## Boundary
- ash_core computes ledger/proposals.
- runtime emits inference telemetry.
- orchestrator_local reports audit evidence.
- artifact_store preserves ledger/proposal snapshots.
