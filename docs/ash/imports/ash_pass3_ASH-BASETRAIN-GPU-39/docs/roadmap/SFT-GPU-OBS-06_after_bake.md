# SFT-GPU-OBS-06 After Bake Roadmap

## Current SSOT

Latest baked stage:

```txt
SFT-GPU-OBS-06 — Action Candidate Apply Gate Preflight / Reviewed Candidate Intake Seal
```

OBS-06 consumes OBS-05 no-apply action candidate handoff packets and validates whether a candidate can be submitted to a later apply gate.

## Opened

```txt
action candidate intake
candidate source seal validation
handoff packet validation
decision receipt source validation
review item digest validation
candidate kind consistency validation
apply gate intake preflight
manual follow-up routing marker
held candidate marker
candidate preflight ledger append
preflight seal generation
```

## Still Closed

```txt
current pointer update
operator action apply
fallback activation
rollback execution
demotion apply
quarantine apply
registry mutation
promotion apply
lifecycle mutation
runtime SFT training
runtime gradient write
runtime optimizer step
partial artifact auto-repair
silent CPU fallback success
silent backend switch
silent registry correction
textureSample / sampler / normalized UV weight fetch
```

## Suggested Next Patch

```txt
SFT-GPU-OBS-07 — Reviewed Candidate Apply Plan / Dry-run Transaction Seal
```

OBS-07 should consume OBS-06 preflight-passed candidates and build a dry-run apply plan. It should still avoid actual apply/mutation. The next clean boundary is a transaction preview that maps candidate kind to a proposed operation plan while keeping all writes disabled.

## Guardrails

```txt
apply_gate_intake_allowed != apply_performed
preflight Passed != actual apply approval
candidate kind mismatch -> held/rejected, no silent rewrite
mutation flag true -> rejected
previous preflight ledger digest missing -> held
no_apply_confirmed false -> rejected
```
