# 16AI-QW-35E — Base-only vs LoRA Semantic Split

## Status
PENDING_RUNTIME

## SSOT
- Patch ID: `16AI-QW-35E`
- Patch name: `Base-only vs LoRA Semantic Split`
- State owner: runtime inference LoRA attach boundary + semantic comparison runner
- Base assumption: `16AI-QW-36A` prompt template switch is available.
- Probe template: `ASH_PROMPT_TEMPLATE=ash_dialogue_ko`
- Mutation policy: no checkpoint, tokenizer, safetensors, banlist, prompt-default, KV, RoPE, or attention-mask mutation.

## Purpose
Split the current Korean word-salad failure into two observable branches:

1. `base_only` output under the same prompt/template/checkpoint/tokenizer.
2. `lora_attached` output under the same prompt/template/checkpoint/tokenizer plus the selected LoRA manifest.

This patch does not repair generation quality. It only makes the LoRA/no-LoRA boundary explicit and reportable.

## Runtime Controls
| Control | Meaning |
|---|---|
| `ASH_FORCE_NO_LORA=1` | Force base-only inference by skipping requested LoRA loads and clearing selected LoRA IDs. |
| `ASH_PROMPT_TEMPLATE=ash_dialogue_ko` | Use the SFT-style dialogue anchor introduced by QW-36A. |

## Runtime Evidence to Capture
| run_kind | stdout | stderr | required evidence |
|---|---|---|---|
| base_only | `workspace/infer_qw35e_base_only_ash_dialogue_1plus1_stdout.json` | `workspace/infer_qw35e_base_only_ash_dialogue_1plus1_stderr.log` | `loaded_loras=0`, `attached_loras=0`, `force_no_lora=true` |
| lora_attached | `workspace/infer_qw35e_lora_attached_ash_dialogue_1plus1_stdout.json` | `workspace/infer_qw35e_lora_attached_ash_dialogue_1plus1_stderr.log` | `attached_loras>0` if a valid LoRA manifest is supplied |

## Acceptance Criteria
- `compile_pass = true`
- `force_no_lora_env_exists = true`
- `force_no_lora_logged = true`
- `base_selected_lora_ids_empty = true`
- `base_loaded_loras_zero = true`
- `base_attached_loras_zero = true`
- `lora_attached_run_exists = true/false 명시`
- `prompt_template_id = ash_dialogue_ko`
- `base_output_text_preview_logged = true`
- `lora_output_text_preview_logged = true/false 명시`
- `compare_qw35e_base_vs_lora_semantic_split.json` written
- `no_weight_mutation = true`
- `no_tokenizer_mutation = true`
- `no_safetensors_mutation = true`
- `no_banlist_mutation = true`

## Decision Matrix
| Observation | Decision | Next patch |
|---|---|---|
| Base passes minimal QA, LoRA becomes word salad | LoRA drift likely | `16AI-QW-38` LM Head / Top-K Drift Audit |
| Base and LoRA both word salad | Base/shared distribution or instruction-template issue likely | `16AI-QW-39`, `16AI-QW-43` |
| Base and LoRA tail match | LoRA not primary by tail match | Minimal QA + micro SFT route |
| LoRA run missing | Probe incomplete | Supply `-LoraJson` and rerun |

## Operator Note: Runtime Structural Probes
If both base and LoRA remain word salad, the following runtime structural probes remain relevant but are not mutated by 35E:

1. RoPE position IDs / decode offset trace.
2. KV cache sequence-axis growth after K/V update.
3. Attention softmax row after causal mask application.

Those should be sealed as separate trace-only patches if distribution split does not explain the failure.

## Current Runtime Status
PENDING_RUNTIME. Run:

```powershell
.\scripts\run_16AI_QW_35E_semantic_split.ps1 -LoraJson "<path-to-adapter-manifest.json>"
```

Then inspect:

```powershell
Get-Content ".\workspace\compare_qw35e_base_vs_lora_semantic_split.json" -Encoding UTF8
```
