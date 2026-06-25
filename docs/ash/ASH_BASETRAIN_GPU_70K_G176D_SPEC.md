# ASH-BASETRAIN-GPU-70K-G176D

## Denied Candidate Hold State Audit

PatchId: `ASH-BASETRAIN-GPU-70K-G176D`

SourcePatchId: `ASH-BASETRAIN-GPU-70K-G175D`

RuntimePassTarget: `PASS_ASH_BASETRAIN_GPU_70K_G176D_DENIED_CANDIDATE_HOLD_STATE_AUDIT_HELD_PROMOTION_CANDIDATE_EVIDENCE_PRESERVATION_REVIEW_NO_REOPEN_NO_ROUTE_SWITCH_NO_PRODUCTION_CLAIM`

G176D consumes the G175D denied candidate hold-state packet and audits that the FreshInit tiny promotion candidate remains in Hold state.

This is a hold-state audit and evidence preservation review gate, not a reopen gate and not a route switch gate.

Expected binary:

`ash_basetrain_gpu_70k_g176d_denied_candidate_hold_state_audit`

Expected local spec in baked ZIP:

`specs/ASH_BASETRAIN_GPU_70K_G176D_SPEC.md`

Expected next patch:

`ASH-BASETRAIN-GPU-70K-G177D` denied candidate hold ledger archive.
