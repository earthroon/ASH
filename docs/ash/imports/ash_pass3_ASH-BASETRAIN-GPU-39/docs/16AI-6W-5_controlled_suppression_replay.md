# 16AI-6W-5 Controlled Suppression Replay

This patch adds a controlled replay probe for dry-commit eligible byte-token suppression candidates.

The probe is non-default and non-mutating:

- `controlled_replay_only=true`
- `default_sampler_mutated=false`
- `output_mutated=false`
- `runtime_default_committed=false`
- `global_default_commit=false`
- `gpu_default=false`

It reads the 16AI-6W-4 dry commit gate output and evaluates 2-token and 8-token controlled horizons for the approved candidates.

This patch is a safe bake: runtime JSON and acceptance placeholders are not included in the project zip.
