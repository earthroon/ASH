# 16AI-QW-38G-R6A-R3 Bake Report

## Patch
Backend Debug Binding Extension Spec / No-Apply Design Seal

## Base
`ash_pass3_16AI-QW-38G-R6A-R2_burn_wgpu_owner_audit_baked.zip`

## Changes
- Added no-apply backend debug binding extension spec writer in `crates/model_core/src/native_wgpu.rs`.
- Added env gates:
  - `ASH_BACKEND_DEBUG_BINDING_SPEC`
  - `ASH_BACKEND_DEBUG_BINDING_SPEC_NO_APPLY`
  - `ASH_BACKEND_DEBUG_BINDING_SPEC_OUT`
  - `ASH_BACKEND_DEBUG_BINDING_SPEC_RECEIPT`
- Added runtime JSON outputs for policy spec and design receipt.
- Added live runner using `--text-file` to avoid PowerShell/cmd Unicode quoting issues.

## Mutation Guard
No shader write, pipeline layout mutation, bind group mutation, generation output mutation, tokenizer mutation, safetensors mutation, or banlist mutation is performed.

## Static Validation
PASS_STATIC
