# INFER-ONLY-DIRECT-MODE-001 Acceptance Report

## Patch

Infer Only Direct Runtime Source Priority / No Default Profile Injection Seal

## Result

BAKED_NO_CARGO_AVAILABLE

## Confirmed

- `crates/runtime/examples/infer_only.rs` was patched.
- `--model-spec` / `--tokenizer` direct mode no longer receives the implicit `specs/runtime_profile.toml` default.
- Mixed runtime source usage is rejected: `--runtime-profile` cannot be combined with direct `--model-spec` / `--tokenizer`.
- Direct mode requires both `--model-spec` and `--tokenizer`.
- Default mode is preserved: if no runtime source flags are passed, `specs/runtime_profile.toml` remains the default source.
- Explicit profile mode is preserved: `--runtime-profile <path>` still uses the provided runtime profile.

## Not Touched

- checkpoint weights
- tokenizer manifest
- model spec files
- runtime profile files
- decode guards
- sampler policy
- QW54/QW55 behavior

## Local Command

```powershell
cargo build -p runtime --example infer_only -j 1
```

Then direct v5 smoke:

```powershell
.\target\debug\examples\infer_only.exe `
  --model-spec ".\specs\model_spec_v5_48259.toml" `
  --tokenizer ".\tokenizer_v5\artifacts\tokenizer_manifest_v5_final.json" `
  --checkpoint ".\tokenizer_v5\artifacts\full_model_vocab_v5_resized.safetensors" `
  --task translation_assist `
  --text "Hello. I need to check whether this local checkpoint inference path works." `
  --max-new-tokens 16 `
  --seed 42 `
  --request-id "direct_v5_no_profile_smoke_001" `
  --json
```

## Expected Evidence

The next output should not show `runtime.profile_path = specs/runtime_profile.toml` when direct `--model-spec`/`--tokenizer` are supplied.
