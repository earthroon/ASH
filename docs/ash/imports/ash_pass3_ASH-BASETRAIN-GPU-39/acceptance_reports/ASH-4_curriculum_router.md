# ASH-4 Curriculum Router / target module planner

## Status
PASS_STATIC / PASS_ASH_CURRICULUM_ROUTER

## Sealed
- CurriculumSample
- CurriculumTaskType
- SampleSignal
- FailureTag
- CurriculumSampleSource
- TrainingObjective
- CurriculumLossMode
- TargetModulePlan
- CurriculumRoute
- CurriculumRouterPolicy

## Routing
- token stability -> korean_response_stability -> lm_head
- runtime attach failure -> runtime_attach_integrity -> runtime/router policy
- logic repair -> logic_repair -> ffn/attention
- context drop -> context_binding -> attention

## Guards
- unknown capability rejected
- empty target modules rejected
- empty eval gates rejected
- difficulty clamped/validated
- Python validator forbidden

## Boundary
ash_core emits curriculum route metadata only.
ash_core does not execute LoRA training.
ash_core does not dump hidden features.
ash_core does not load or write adapter weights.
