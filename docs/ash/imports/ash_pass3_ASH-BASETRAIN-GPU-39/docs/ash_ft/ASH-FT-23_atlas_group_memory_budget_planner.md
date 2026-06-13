# ASH-FT-23
## Atlas Group Memory Budget Planner / No OOM Full Tensor Load Seal

### SSOT

ASH-FT-23 reads the ASH-FT-22 manifest-derived atlas registry and creates a group-only memory budget registry. It must not load tensor payloads, create GPU resources, allocate runtime gradients/optimizer state, update weights, mutate the base checkpoint, or promote any candidate.

### Confirmed base

- Base required: ASH-FT-22 PASS
- Mainline: atlas_group_sequential_finetune_stack
- Input authority: ASH-FT-22 family registry, layer partition, and trainable scope registry
- Output authority: ASH-FT-23 group memory budget registry

### Allowed mutations

- `artifacts/ash_ft/ash_ft23_budget_plan.json`
- `artifacts/ash_ft/ash_ft23_group_memory_budget_registry.json`
- `artifacts/ash_ft/ash_ft23_dtype_width_table.json`
- `artifacts/ash_ft/ash_ft23_optimizer_budget_profile.json`
- `artifacts/ash_ft/ash_ft23_oom_risk_review_queue.json`
- `artifacts/ash_ft/ash_ft23_no_full_tensor_load_guard.json`
- `artifacts/ash_ft/ash_ft23_no_runtime_allocation_guard.json`
- `artifacts/ash_ft/ash_ft23_next_patch_route.json`
- `artifacts/ash_ft/ASH-FT-23_receipt.json`

### Forbidden

- full tensor payload load
- full model upload
- GPU resource creation
- full gradient buffer allocation
- full optimizer state allocation
- group runtime allocation inside the planner
- forward/backward
- optimizer step
- weight update
- base checkpoint mutation
- delta stack mutation
- promotion

### Budget policy

- Parameter bytes are calculated only when shape/param count and dtype width are known.
- Unknown dtype or shape is not silently estimated; it is routed to review.
- Activation budget is hint-only in FT-23.
- OOM risk is conservative and remains `UNKNOWN_REVIEW` when device limits or activation budget are not available.

### Expected PASS

```txt
PASS_ASH_FT23_ATLAS_GROUP_MEMORY_BUDGET_PLANNER_NO_OOM_FULL_TENSOR_LOAD
```

### Next

```txt
ASH-FT-24
Sequential Atlas Group Training Schedule / Deterministic Group Order Seal
```
