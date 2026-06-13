# 16AI-QW-40 — Selected LoRA Gradient Scope / Base Frozen Fence Seal

## Status
PASS_STATIC_CANDIDATE_ONLY

## SSOT
- Source route matrix: `artifacts/adapter_route_loss/qw39_adapter_route_target_matrix.json`
- Gradient scope: `artifacts/selected_lora_gradient_scope/qw40_selected_lora_gradient_scope.json`
- Fence report: `artifacts/selected_lora_gradient_scope/qw40_gradient_fence_report.json`
- Scope receipt: `artifacts/selected_lora_gradient_scope/qw40_selected_lora_gradient_scope_receipt.json`
- Base fence receipt: `artifacts/selected_lora_gradient_scope/qw40_base_frozen_fence_receipt.json`

## Counts
- Adapter targets: 3
- Selected LoRA: 1
- Trainable LoRA candidates: 1
- Frozen LoRA: 4
- Forbidden LoRA: 1
- Shadow-only LoRA: 0
- Missing adapters: 0

## Selected / Trainable
```json
[
  "ash_korean_morphology_lora_candidate"
]
```

## Frozen
```json
[
  "ash_lm_head_lora_promoted",
  "ash_overstyle_lora_candidate",
  "ash_qwave_smoothness_lora_candidate",
  "ash_semantic_guard_lora_candidate"
]
```

## Forbidden
```json
[
  "ash_overstyle_lora_candidate"
]
```

## Policy Seal
- `affects_gradient_scope_candidate = true`
- `affects_actual_gradient = false`
- `affects_total_loss = false`
- `affects_optimizer = false`
- `affects_lora_weights = false`
- `affects_base_model = false`

## Mutation Guard
- backward executed: false
- optimizer step executed: false
- actual gradient created: false
- LoRA weight mutated: false
- base model mutated: false
- runtime pointer mutated: false
- adapter pointer mutated: false
- missing adapter created: false

## Compile / Runtime Note
Native Rust compile, cargo tests, and runtime backward execution were not run in this environment because the native Rust toolchain is unavailable. This patch is a static source/artifact bake and keeps the QW-40 fence default-off.
