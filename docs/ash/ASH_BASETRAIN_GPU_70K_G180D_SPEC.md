# ASH-BASETRAIN-GPU-70K-G180D

## Explicit Reopen Request Approval Gate

PatchId: `ASH-BASETRAIN-GPU-70K-G180D`

SourcePatchId: `ASH-BASETRAIN-GPU-70K-G179D`

RuntimePassTarget: `PASS_ASH_BASETRAIN_GPU_70K_G180D_EXPLICIT_REOPEN_REQUEST_APPROVAL_GATE_REOPEN_REQUEST_CANDIDATE_TO_OPERATOR_REOPEN_DECISION_NO_REOPEN_EXECUTION_NO_ROUTE_SWITCH_NO_PRODUCTION_CLAIM`

G180D consumes the G179D explicit reopen request candidate and binds an explicit operator reopen decision.

This is a decision-binding gate. It is not a reopen execution gate, not a route switch gate, and not a production promotion gate.

Allowed operator decisions:

- `explicit-reopen-approval`
- `explicit-reopen-denial`

Expected binary:

`ash_basetrain_gpu_70k_g180d_explicit_reopen_request_approval_gate`

Expected local spec in baked ZIP:

`specs/ASH_BASETRAIN_GPU_70K_G180D_SPEC.md`

Expected next patch on approval:

`ASH-BASETRAIN-GPU-70K-G181A` approved reopen execution preflight.

Expected next patch on denial:

`ASH-BASETRAIN-GPU-70K-G181D` reopen request denial routing.
