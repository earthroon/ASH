# SFT-GPU-OBS-05 After Bake Roadmap

## Current SSOT

Latest baked state:

```txt
ash_pass3_SFT-GPU-OBS-05_decision_action_candidate_baked.zip
```

OBS-05 consumes OBS-04 operator review decision receipts and creates no-apply action-candidate handoff packets.

## Opened

```txt
operator decision to action candidate bridge
no-apply handoff packet
candidate kind mapping
candidate target/source validation
source decision digest validation
review item digest validation
handoff ledger append
action candidate seal
apply gate eligibility marker
manual follow-up marker
held marker
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

## Natural Next Step

```txt
SFT-GPU-OBS-06 — Action Candidate Apply Gate Preflight / Reviewed Candidate Intake Seal
```

OBS-06 should consume the OBS-05 no-apply handoff packet and preflight whether the candidate can be submitted to a real operator action apply path. OBS-06 should still avoid applying the action until the intended apply gate is explicitly opened.

## Guardrails for OBS-06

```txt
1. OBS-05 handoff seal must exist.
2. action_candidate_digest and handoff_packet_digest must match.
3. apply_gate_eligible=true is not apply permission by itself.
4. candidate kind must not be silently rewritten.
5. invalid/hold/blocker candidates must not be promoted into executable apply candidates.
6. runtime training, gradient write, optimizer step remain closed.
7. textureSample weight fetch remains closed.
```
