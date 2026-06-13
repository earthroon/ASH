# 16AI-QW-36A — Runtime Prompt Template Switch Probe / SFT Dialogue Anchor Candidate Seal

## Status
PASS_STATIC / PENDING_LOCAL_RUNTIME_PROBE

## SSOT
- Patch target: `crates/runtime/src/infer.rs`
- State owner: runtime inference prompt construction boundary
- Current sealed baseline: 16AI-6W-8 runtime generation banlist apply success
- Banlist expectation from latest external run: `file_banned_token_ids = 583`, `merged_banned_token_ids = 585`
- No checkpoint, tokenizer, safetensors, LoRA weight, banlist, or sampling policy mutation is included in this patch.

## Implemented
- Added `RuntimePromptTemplateId` with three selectable prompt templates:
  - `control_v5_current`
  - `ash_dialogue_ko`
  - `hybrid_task_dialogue_ko`
- Added `ASH_PROMPT_TEMPLATE` environment-variable switch.
- Preserved current default behavior by falling back to `control_v5_current`.
- Added `emit_runtime_prompt_context(...)` helper to keep glossary, TM, QWave hint, and text prior emission deterministic across control/hybrid paths.
- Added debug telemetry:
  - `[debug] prompt_template_id = ...`
  - `[debug] prompt_text_preview = ...`

## Template Contracts

### control_v5_current
Existing runtime contract remains the default:

```txt
<task:{resolved_task}>
...
{input_text}
<response:start>
<response:answer | response:subtitle | response:translation | response:json>
```

### ash_dialogue_ko
SFT dialogue anchor candidate:

```txt
사용자: {input_text}
애쉬:
```

### hybrid_task_dialogue_ko
Control metadata plus SFT dialogue anchor candidate:

```txt
<task:{resolved_task}>
<lang:ko>
...
사용자: {input_text}
애쉬:
```

## Static Validation
- Validation artifact: `target/16AI-QW-36A_static_validation.json`
- Static status: `PASS_STATIC`

## Local Runtime Probe Commands

```powershell
cargo check -p runtime 2>&1 | Tee-Object ".\target\16AI-QW-36A_runtime_check.log"
```

```powershell
$env:ASH_PROMPT_TEMPLATE="control_v5_current"
# Run the existing infer entry with identical checkpoint/tokenizer/banlist/maxNewTokens.
# Capture to: .\workspace\infer_qw36a_control_1plus1.log
```

```powershell
$env:ASH_PROMPT_TEMPLATE="ash_dialogue_ko"
# Run the existing infer entry with identical checkpoint/tokenizer/banlist/maxNewTokens.
# Capture to: .\workspace\infer_qw36a_ash_dialogue_1plus1.log
```

```powershell
$env:ASH_PROMPT_TEMPLATE="hybrid_task_dialogue_ko"
# Run the existing infer entry with identical checkpoint/tokenizer/banlist/maxNewTokens.
# Capture to: .\workspace\infer_qw36a_hybrid_1plus1.log
```

```powershell
Select-String -Path ".\workspace\infer_qw36a_*.log" `
  -Pattern "prompt_template_id|prompt_text_preview|file_banned_token_ids|merged_banned_token_ids|generated_tail_head|output_guard_first_pass|output_text_preview|mean_logprob|min_logprob" `
  -Context 0,2
```

## Acceptance Criteria
- `compile_pass = pending_local`
- `prompt_template_id_logged = true`
- `prompt_text_preview_logged = true`
- `control_v5_current_replay_exists = pending_local`
- `ash_dialogue_ko_replay_exists = pending_local`
- `hybrid_task_dialogue_ko_replay_exists = pending_local`
- `same_checkpoint = required_local`
- `same_tokenizer = required_local`
- `same_banlist = required_local`
- `same_task = required_local`
- `same_max_new_tokens = required_local`
- `no_weight_mutation = true`
- `no_tokenizer_mutation = true`
- `no_safetensors_mutation = true`

## Decision Matrix

| Observation | Decision | Next Patch |
|---|---|---|
| `ash_dialogue_ko` improves over `control_v5_current` | `runtime_prompt_contract_mismatch = likely_true` | 16AI-QW-41 |
| only `hybrid_task_dialogue_ko` improves | metadata useful, response anchor mismatch likely | 16AI-QW-41 hybrid candidate |
| all templates collapse | prompt switch alone insufficient | 16AI-QW-35 / 16AI-QW-38 |
| base-only improves but LoRA attach collapses | lm_head LoRA drift likely | 16AI-QW-38 |
| nonsense Korean still accepted | semantic guard too permissive | 16AI-QW-37 |

## Boundary
This patch is a runtime prompt probe only. It does not approve any default template switch, promotion, adapter change, safetensors surgery, tokenizer change, or guard policy hardening.

## R1 Runner Correction

`16AI-QW-36A-R1` adds runnable PowerShell scripts because this repository's actual inference example surface is:

```powershell
cargo run --manifest-path .\crates\runtime\Cargo.toml --example infer_only -- --text "1+1은?"
```

not:

```powershell
cargo run -p ash_runtime --bin infer -- --input-text "1+1은?"
```

Use:

```powershell
.\scripts\run_16AI_QW_36A_prompt_template_probe.ps1
```
