# ASH-45D LoRA Artifact Lineage Binding

## Status
PASS_ASH_45D_LORA_ARTIFACT_LINEAGE_BINDING

## Sealed
- AshLoraArtifactLineageClass
- AshLoraArtifactLineageDecision
- AshLoraArtifactLineageTrace
- LoRA artifact manifest trace
- LoRA weights path trace
- registry snapshot trace
- current pointer match / mismatch seal
- lineage confidence multiplier
- lineage safety flags
- adjustment lineage eligibility
- report lineage counts

## Policy
- adapter_id alone cannot produce Strong confidence
- missing manifest cannot silently pass as valid lineage
- missing weights lowers confidence
- current pointer mismatch requires manual review
- registry mismatch requires manual review
- valid lineage does not override manual review safety
- valid lineage does not override telemetry regression safety
- applied remains false
- runtime router config is not mutated
- current pointer is not changed
- no LoRA attach/detach
- no Python validator

## Boundary
ASH-45D only binds calibration evidence to LoRA artifact lineage.
ASH-45E handles snapshot / audit output consistency.
ASH-45F handles deterministic replay.
ASH-48 handles explicit runtime apply.
