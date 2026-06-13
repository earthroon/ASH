# ASH-FT-02-R1 Bin Target Surface Rebind

The previous ASH-FT-02 bake contained the source implementation and intended bin entrypoint, but the user's local Cargo target surface did not list `ash_ft02_full_coverage_slice_read_probe`.

This patch explicitly registers the bin in `crates/model_core/Cargo.toml`:

```toml
[[bin]]
name = "ash_ft02_full_coverage_slice_read_probe"
path = "src/bin/ash_ft02_full_coverage_slice_read_probe.rs"
```

No probe semantics are changed. The ASH-FT-02 contract remains bounded read-only slice probing with no GPU upload, no forward/backward, no optimizer step, no candidate write, and no runtime default apply.
