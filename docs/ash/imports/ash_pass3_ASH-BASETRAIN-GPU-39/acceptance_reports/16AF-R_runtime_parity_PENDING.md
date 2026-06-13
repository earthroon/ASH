# 16AF-R Runtime Parity Acceptance

## Status

```txt
build_gate = PASS by user report
runtime_parity = PENDING_LOCAL_RUN
generation_connected = false
```

## Local Command

PowerShell:

```powershell
$env:SPEC_PATH="specs/model_spec_300m_dialogue_continue_gqa8_headwise_atlas.toml"
$env:CHECKPOINT_PATH="workspace/base_train_runs/dialogue_300m_hybrid_run02_clean_v3/full_model.safetensors"
$env:LAYER_IDX="0"
$env:THRESHOLD="0.001"
.\scripts\run_16AF_R_runtime_parity.ps1
```

Bash:

```bash
SPEC_PATH="specs/model_spec_300m_dialogue_continue_gqa8_headwise_atlas.toml" \
CHECKPOINT_PATH="workspace/base_train_runs/dialogue_300m_hybrid_run02_clean_v3/full_model.safetensors" \
LAYER_IDX="0" \
THRESHOLD="0.001" \
./scripts/run_16AF_R_runtime_parity.sh
```

## PASS Criteria

```txt
shape_match = true
nan_count = 0
inf_count = 0
max_abs_delta <= threshold
mean_abs_delta <= threshold
parity_pass = true
generation_connected = false
```

## FAIL Criteria

```txt
shape_match = false
nan_count > 0
inf_count > 0
max_abs_delta > threshold
mean_abs_delta > threshold
wgpu adapter/device/shader validation failure
forbidden path reappearance
generation_connected = true before parity pass
```
