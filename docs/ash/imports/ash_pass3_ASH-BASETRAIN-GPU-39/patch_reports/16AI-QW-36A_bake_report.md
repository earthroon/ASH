# 16AI-QW-36A Bake Report

## Baked Target
`16AI-QW-36A — Runtime Prompt Template Switch Probe / SFT Dialogue Anchor Candidate Seal`

## Files Changed
- `crates/runtime/src/infer.rs`
- `acceptance_reports/16AI-QW-36A_runtime_prompt_template_switch_probe.md`
- `target/16AI-QW-36A_static_validation.json`

## Code Changes
- Added `RuntimePromptTemplateId` enum.
- Added `ASH_PROMPT_TEMPLATE` environment-variable prompt switch.
- Added `control_v5_current`, `ash_dialogue_ko`, and `hybrid_task_dialogue_ko` prompt branches.
- Added prompt template telemetry before tokenization.
- Preserved the previous control-token template as the default path.

## Validation
- Static source validation: `PASS_STATIC`.
- `cargo fmt` / `cargo check`: not executed in this container because `cargo` is not installed in the execution environment.

## No-Mutation Guarantees
- No safetensors file changed.
- No tokenizer manifest changed.
- No banlist changed.
- No LoRA adapter changed.
- No base checkpoint changed.
- No default runtime behavior changed unless `ASH_PROMPT_TEMPLATE` is explicitly set.

## Required Local Verification
Run on the Windows project machine:

```powershell
cargo check -p runtime 2>&1 | Tee-Object ".\target\16AI-QW-36A_runtime_check.log"
```

Then run three identical inference probes with:

```powershell
$env:ASH_PROMPT_TEMPLATE="control_v5_current"
$env:ASH_PROMPT_TEMPLATE="ash_dialogue_ko"
$env:ASH_PROMPT_TEMPLATE="hybrid_task_dialogue_ko"
```

Compare:

```powershell
Select-String -Path ".\workspace\infer_qw36a_*.log" `
  -Pattern "prompt_template_id|prompt_text_preview|file_banned_token_ids|merged_banned_token_ids|generated_tail_head|output_guard_first_pass|output_text_preview|mean_logprob|min_logprob" `
  -Context 0,2
```
