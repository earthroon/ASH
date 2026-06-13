# 16AI-QW-38G-R6A-SAMPLER-01 Bake Report

## Scope
- Added Min-P sampling config plumbing (`minP`, `min_p`, `samplingMinP`, `sampling_min_p`).
- Added WebGPU logit-domain Min-P mask support in sampling uniform and WGSL candidate mask stage.
- Added legacy GPU select Min-P parity path.
- Added CPU/reference subset Min-P filter for structure-rerank subset sampling.
- Added sampler01 receipt and step trace emission in `orchestrator_local`.

## Sampling order sealed
`raw_logits -> repetition_penalty -> ban_mask -> eos_step_guard -> temperature_scale -> top_k_filter -> min_p_filter -> top_p_filter -> final_sample`

## Min-P formula
`scaled_logit >= max_scaled_logit + ln(min_p)`

## Notes
- This bake does not mutate checkpoint/tokenizer/safetensors/lm_head/final_norm/ban_mask.
- Cargo build was not executed in the bake container because `cargo` is unavailable.
- Top-P active-set renormalization is audited but not fully changed here; follow-up can be `SAMPLER-01A`.
