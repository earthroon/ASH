# QW-54G Roadmap — Closed Attractor Set Breaker

## Implemented in this bake

- Added `qw54g_closed_attractor_set_breaker.rs` in `model_core`.
- Added QW-54G call after QW-54F and before final argmax selection.
- Added explicit CLI flags to `infer_only`:
  - `--enable-qw54g`
  - `--qw54g-trace`
  - `--qw54g-max-penalty`
  - `--qw54g-window`
- Added QW-54G runtime trace, receipt, and report paths.
- Added Windows command wrapper `scripts/run_qw54g_closed_attractor_vulkan.cmd`.

## Next tuning lane

If QW-54G detects the set but does not break selection, tune in this order:

1. Increase `ASH_QW54G_MAX_PENALTY` from `1.35` to `1.75`.
2. Lower `ASH_QW54G_MIN_REPEAT_COUNT` from `3` to `2` only for lab runs.
3. Increase TopK pool size in the QW-54F candidate hook if too few non-attractor alternatives appear.
4. Add tokenizer piece lookup into QW-54G trace so the report shows real pieces instead of token placeholders.

## Known limitation

This bake uses token IDs as the authoritative closed-set key. The QW-54G trace currently records placeholder pieces such as `<token:29871>` because the native candidate hook does not yet carry tokenizer pieces at this layer.
