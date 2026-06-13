# 16AI-QW-38G-R6A — Shader Dispatch Hook Exposure / Debug Buffer Binding Surface Seal

## Status
PENDING_RUNTIME / PASS_DEBUG_BINDING_SURFACE / FAIL_DEBUG_BINDING_SURFACE_UNAVAILABLE

## SSOT
- Base patch: `16AI-QW-38G-R6 — Shader Debug Buffer Design / Explicit Intermediate Export Candidate Seal`
- Prior result: R6 reported `FAIL_SHADER_DEBUG_TAP_UNAVAILABLE` with `GPU_DEBUG_BUFFER_INSERTION_POINT_UNAVAILABLE`.
- Current objective: expose or reject a debug storage-buffer binding surface without performing shader writes.

## Implemented Surface
- Env gate: `ASH_SHADER_DEBUG_BINDING=1`
- Dry-run only: `ASH_SHADER_DEBUG_BINDING_DRY_RUN=1` by default
- Map output: `workspace/qw38g_r6a_debug_binding_map.json`
- Receipt output: `workspace/qw38g_r6a_debug_binding_receipt.json`
- Debug write performed: false
- Full vector readback: not used

## Expected Runtime Decision
If the current hot path still exposes only Burn tensor matmul / vocab atlas projection without a directly owned bind group layout, runtime should write:

```txt
status = FAIL_DEBUG_BINDING_SURFACE_UNAVAILABLE
warning_codes = [NO_BIND_GROUP_LAYOUT_SURFACE, DEBUG_SHADER_VARIANT_REQUIRED, DEBUG_BINDING_SURFACE_UNAVAILABLE]
```

If a future pipeline layout surface is exposed, runtime may report:

```txt
status = PASS_DEBUG_BINDING_SURFACE
debug_binding_surface_available = true
```

## Acceptance Criteria
- `shader_debug_binding_env_gate_exists = true`
- `shader_debug_binding_default_off = true`
- `dry_run_default = true`
- `debug_write_not_performed = true`
- `binding_map_written = true`
- `binding_receipt_written = true`
- `debug_binding_surface_available = true/false 명시`
- `pipeline_cache_key_extended = true/false 명시`
- `shader_variant_required = true/false 명시`
- `no_weight_mutation = true`
- `no_tokenizer_mutation = true`
- `no_safetensors_mutation = true`
- `no_banlist_mutation = true`

## Runtime Command

```powershell
.\scripts\run_16AI_QW_38G_R6A_debug_binding.ps1 -Build
```

## Output Files

```txt
workspace/qw38g_r6a_debug_binding_map.json
workspace/qw38g_r6a_debug_binding_receipt.json
workspace/infer_qw38g_r6a_debug_binding_live.log
```
