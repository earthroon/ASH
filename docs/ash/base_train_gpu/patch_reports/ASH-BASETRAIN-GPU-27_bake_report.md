# ASH-BASETRAIN-GPU-27 Bake Report

## Patch

```txt
ASH-BASETRAIN-GPU-27
GPU Backward Preflight / Stable GPU Loss Candidate To Gradient Buffer Contract No Backward No Optimizer Seal
```

## Baked Changes

- Added static GPU backward preflight module.
- Added direct bin rebind.
- Added source 26 validation receipt.
- Added backward readiness validation receipt.
- Added logits-gradient buffer contract receipt.
- Added model weight gradient denylist and body-training claim guard.
- Added proof class receipt.
- Added expected receipt JSON files.
- Added operator commands.
- Added acceptance report and handoff markdown.

## Contract

```txt
new_gpu_buffer_created = false
new_compute_dispatch_executed = false
new_readback_executed = false
new_loss_computed = false
backward_executed = false
gradient_buffer_created = false
gradient_buffer_written = false
gradient_value_computed = false
optimizer_step_executed = false
safetensors_mutation_present = false
runtime_1p1b_training_claimed = false
```

## Next

```txt
ASH-BASETRAIN-GPU-28
Gradient Buffer Allocation Candidate /
Contracted Logits Gradient Buffer Allocation No Backward No Optimizer Seal
```
