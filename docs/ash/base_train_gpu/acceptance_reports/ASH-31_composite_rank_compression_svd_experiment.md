# ASH-31 Composite Rank Compression / SVD Bake Experiment

## Status
PASS_COMPOSITE_RANK_COMPRESSION_SVD_EXPERIMENT

## Sealed
- AshCompositeRankCompressionMode
- AshRankCompressionPolicy
- AshModuleCompressionDecision
- AshCompositeRankCompressionConfig
- AshCompositeSourceModuleDescriptor
- AshCompositeModuleCompressionPlan
- AshCompositeRankCompressionPlan
- AshSingularValueSummary
- AshCompositeModuleCompressionResult
- AshCompressedCompositeLoraArtifact
- AshCompositeRankCompressionReport
- AshCompressedCompositeArtifactBridge
- SVD rank selection contract
- singular value energy retention summary
- reconstruction error validation
- compressed manifest contract
- experimental staging output
- compressed artifact bridge

## Policy
- ASH-31 does not overwrite source artifact
- ASH-31 does not change current pointer
- ASH-31 does not auto-promote compressed artifact
- Compression errors are explicit
- High-error modules are rejected or kept original by config
- Compressed artifacts require runtime smoke test
- Compressed artifacts require manual review
- Compressed artifacts require current pointer gate
- No Python validator

## Boundary
ash_core defines compression contracts.
orchestrator_local reports compression evidence.
artifact_store preserves experimental compressed artifacts.
runtime consumes only after later smoke/promotion gate.
