# ASH-19 Explicit Synapse Proposal Apply Gate / Soft Ensemble Composer

## Status
PASS_SYNAPSE_PROPOSAL_APPLY_GATE_SOFT_ENSEMBLE

## Sealed
- AshSynapseProposalApplyMode
- AshSynapseProposalApplyDecision
- AshSynapseProposalApplyConfig
- AshAppliedSynapseProposalRecord
- AshSynapseProposalApplyReport
- apply_synapse_update_proposals
- AshSoftEnsembleAdapterWeight
- AshSoftEnsembleConfig
- AshSoftEnsembleRoutePlan
- compose_soft_ensemble_route
- orchestrator ASH-19 report bridge
- audit bin: ash_19_synapse_apply_soft_ensemble_audit

## Policy
- ASH-18 proposals require explicit apply.
- The source registry is never silently mutated.
- DryRun never emits patched_registry.
- ApplyToClone only patches a cloned registry candidate.
- Unsupported instability cost proposals are skipped, not remapped to edge weight.
- SoftEnsemble computes adapter probability mass from ASH-17 path candidates.
- Individual adapter weights are not silently clamped.
- Ensemble total normalization is recorded as a warning.
- Base-only remains empty attachment.
- No Python validator.

## Boundary
ash_core computes apply gate and ensemble route.
runtime executes selected adapter attachments.
orchestrator_local reports audit evidence.
artifact_store preserves registry/report snapshots.
