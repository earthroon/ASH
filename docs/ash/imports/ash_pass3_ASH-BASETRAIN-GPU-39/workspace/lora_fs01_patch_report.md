# 16AI-QW-38G-R6A-LORA-FS-01 Bake Report

## Scope

Feature Store Manifest Audit / Single Domain Adapter Export Plan Seal.

## Changed Files

- crates/orchestrator_local/src/lib.rs
- crates/orchestrator_local/src/lora_feature_store_audit.rs

## Implemented

- Registered `lora.feature_store.audit` command.
- Added manifest/shard audit handler.
- Reads safetensors headers only for tensor metadata instead of loading full tensors.
- Writes audit receipt, export plan, and patch report.
- Uses `serde_json::Map` insertion for large receipts to avoid `json_internal!` recursion failures.
- Does not train, merge, attach, or mutate model files.

## Static Validation

Status: `PASS_STATIC_LORA_FS01_AUDIT_BAKE_PENDING_LOCAL_CARGO_BUILD`

Cargo check: `NOT_RUN_CARGO_NOT_AVAILABLE_IN_BAKE_ENV`
