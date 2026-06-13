# QW-54I Roadmap

## Patch

`QW-54I — Recent Attractor Orbit Cooldown / Escaped Set Re-entry Refractory Gate Seal`

## Why

QW-54H blocks greedy fallback when the current greedy token is a closed-attractor member. Logs showed a remaining orbit case: the attractor set is still detected, but the selected greedy token is temporarily outside the set and QW-54H reports `GreedyNotAttractorMember`.

QW-54I adds a short-lived refractory ledger for recently escaped attractor sets.

## Implementation units

- Add `qw54i_orbit_cooldown_gate.rs`
- Export module in `model_core/src/lib.rs`
- Call QW-54I after QW-54H in `generation_sampling.rs`
- Add CLI flags to `runtime/examples/infer_only.rs`
- Add runtime profile section
- Add wrapper `scripts/run_qw54i_orbit_cooldown_vulkan.cmd`

## Validation lane

```powershell
cargo check -p model_core --lib
cargo check -p runtime --all-targets
```

Then run:

```powershell
.\target\release\examples\infer_only.exe `
  --runtime-profile .\specs\runtime_profile.toml `
  --task subtitle_polish `
  --text "I thought you were going to leave me behind." `
  --max-new-tokens 160 `
  --seed 42 `
  --enable-qw54i `
  --qw54i-trace `
  --json
```

## Expected traces

```txt
workspace/runtime_traces/qw54i_orbit_cooldown_trace.jsonl
workspace/trace/qw54i_orbit_cooldown_receipt.json
artifacts/qw54i_orbit_cooldown_report.json
```
