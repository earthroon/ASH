# ASH-BASETRAIN-GPU-70K-G175D

## FreshInit Tiny Approval Denial Routing

PatchId: `ASH-BASETRAIN-GPU-70K-G175D`

SourcePatchId: `ASH-BASETRAIN-GPU-70K-G174`

RuntimePassTarget: `PASS_ASH_BASETRAIN_GPU_70K_G175D_FRESHINIT_TINY_APPROVAL_DENIAL_ROUTING_DENIED_PROMOTION_CANDIDATE_TO_HOLD_STATE_NO_ROUTE_SWITCH_NO_PRODUCTION_CLAIM`

G175D consumes the G174 explicit denial receipt and routes the denied FreshInit tiny promotion candidate into Hold state.

This is a denial routing and hold-state sealing gate, not an execution gate. It must not reinterpret denial as evidence failure.

Expected binary:

`ash_basetrain_gpu_70k_g175d_freshinit_tiny_approval_denial_routing`

Expected local spec in baked ZIP:

`specs/ASH_BASETRAIN_GPU_70K_G175D_SPEC.md`

Expected next patch:

`ASH-BASETRAIN-GPU-70K-G176D` denied candidate hold state audit.
