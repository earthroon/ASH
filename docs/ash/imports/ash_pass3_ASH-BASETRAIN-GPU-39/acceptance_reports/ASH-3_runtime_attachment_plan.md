# ASH-3 Runtime Attachment Plan contract

## Status
PASS_STATIC / PASS_ASH_RUNTIME_ATTACHMENT_PLAN

## Sealed
- AshRuntimeAttachmentMode
- AshAdapterAttachment
- AshRuntimeAttachmentPolicy
- AshRuntimeAttachmentPlan
- AshRuntimeAttachmentPlanStatus
- AshRuntimeAttachmentPlanDto
- AshRuntimeAttachmentPlanDtoEntry

## Default behavior
- promoted default-enabled adapters become attachments
- base-only mode must be explicit
- adapter-enabled mode must contain attachments

## Guards
- no silent fallback
- no target auto-remap
- no missing adapter pass
- runtime_scale must be positive
- manifest/model paths are required by strict policy
- Python validator forbidden

## Boundary
ash_core emits runtime attachment plan metadata only.
ash_core does not load safetensors.
ash_core does not call runtime forward.
ash_core does not import runtime crate.
