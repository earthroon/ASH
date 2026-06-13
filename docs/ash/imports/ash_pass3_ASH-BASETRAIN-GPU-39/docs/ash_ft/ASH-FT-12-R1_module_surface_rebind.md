# ASH-FT-12-R1 Module Surface Rebind

This patch repairs the compile surface for ASH-FT-12 after the binary target failed to resolve the direct module path from `model_core`.

The intended runtime behavior is unchanged: metadata-only candidate slot bind dry-run, no decode, no generation, no runtime default apply.
