# 16AI-QW-38G-R6A-MEM-03

## Native Cache Owner Audit / Hard Purge Hook Seal

## Summary

This bake adds a real native-runtime-side MEM-03 cache owner audit and hard purge hook. MEM-02 only emitted an orchestrator lifecycle receipt and could not directly touch model-core cache owners. MEM-03 moves the owner inspection and purge execution into `NativeWgpuModel`, where the actual owners live.

## Implemented

- Added MEM-03 request fields to `StandardInferRequest` and `ResolvedStandardInferRequest`.
- Wired MEM-03 payload fields from `orchestrator_local` into `runtime`.
- Added `NativeWgpuModel::mem03_write_cache_owner_receipts(...)`.
- Added owner snapshots for:
  - `native_vocab_atlas_cache`
  - `native_embedding_row_gather_cache`
  - `native_readback_staging_buffers`
  - `domain_adapter_weight_cache`
  - `domain_adapter_delta_buffer`
  - `kv_cache`
  - `model_instance_cache`
  - `gpu_sampling_state_cache`
- Added best-effort hard purge actions for optional native owners:
  - `domain_adapter = None`
  - `vocab_atlas = None`
  - `atlas_dispatcher = None`
  - `runtime_handles = None`
  - `gpu_sampling_runtime = None`
  - active adapter/penalty/text-density buffers cleared
  - row gather byte marker reset
- Writes:
  - `mem03_cache_owner_audit_receipt.json`
  - `mem03_hard_purge_receipt.json`
  - `mem03_cache_owner_ledger.jsonl`
- Embeds MEM-03 receipts back into output artifacts and response JSON when present.
- Adds PowerShell examples for one-shot run, verification, and process memory loop.

## Honesty note

MEM-03 now reaches into `NativeWgpuModel` optional owners and clears the available optional runtime/cache fields. It still cannot force the OS/WGPU backend to immediately shrink WorkingSet. Therefore receipts explicitly preserve:

- `gpu_backend_release_may_be_deferred = true`
- process memory snapshot source is not provided from model_core without platform-specific APIs
- `model_instance_cache` core field is not optional and drops with `NativeWgpuModel`

Use `PrivateMemorySize64` vs `WorkingSet64` loop checks to separate real private heap growth from Windows/GPU deferred or standby-cache effects.

## Validation

Container has no `cargo`, so local cargo check was not executed here.

Recommended local check:

```powershell
cargo check -p orchestrator_local --bin orchestrator_local --message-format short
```

## Files changed

See `workspace/mem03_changed_files.txt`.
