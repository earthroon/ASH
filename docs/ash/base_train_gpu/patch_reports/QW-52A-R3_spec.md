# QW-52A-R3
## Cheonjiin Projection Alignment Probe / Hidden-Space Similarity Receipt

## SSOT
- Base patch: QW-52A-R2
- Rust owns hidden snapshot, alignment trace, receipt, validation, and state judgment.
- Python is injector only.

## Goal
Observe whether the QW-52A-R2 Cheonjiin projection dry-run output is dimensionally and directionally compatible with Ash hidden-space snapshots.

## Non-goals
- No hidden-state fusion.
- No residual stream mutation.
- No logit mutation.
- No sampler mutation.
- No token selection change.
- No adapter apply.
- No new projection math.
- No WebGPU shader addition.
- No Python analyzer or validator.

## Implemented surfaces
- `crates/model_core/src/cheonjiin_projection_alignment_probe.rs`
- `crates/model_core/src/bin/qw52a_r3_projection_alignment_validate.rs`
- `crates/model_core/src/hangul_qwave_candidate_awareness.rs` additive alignment field binding
- `crates/model_core/src/lib.rs` public exports

## Trace additions
Candidate awareness payload may now include:

```json
{
  "cheonjiin_projection_alignment": {
    "projection": {},
    "alignment": {},
    "repeat_context": {},
    "policy": {
      "observe_only": true,
      "hidden_state_fusion": false,
      "logit_mutation": false,
      "sampler_mutation": false,
      "token_ban_added": false,
      "adapter_projection_applied": false
    }
  }
}
```

## Validation policy
The validator checks that the alignment probe exists, writes receipt from Rust, attaches additive candidate payload, and preserves all mutation flags as false.
