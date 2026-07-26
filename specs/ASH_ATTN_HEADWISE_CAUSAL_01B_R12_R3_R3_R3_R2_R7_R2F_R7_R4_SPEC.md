# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R4

## Production Canary Route Binding / Session-Sticky Candidate Ownership / Atomic Route Generation / Exact Fallback and Zero Mid-Decode Mutation Seal

## 0. Authority and scope

```text
PARENT=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R3
DEFAULT_VERDICT=HOLD
ACTIVE_ROUTE=existing-production-headwise-reference-v1
CANDIDATE_ROUTE=gqa4-cluster-production-canary-v1
FALLBACK_ROUTE=existing-production-headwise-reference-v1
CANARY_DEFAULT_BASIS_POINTS=0
ROUTE_AUTHORITY=atomic-generation-owned-v1
SESSION_POLICY=session-sticky-zero-mid-decode-mutation-v1
ROLLBACK_POLICY=exact-fallback-generation-cas-v1
```

R7-R4 is the control-plane binding gate after the R7-R3 GPU payload evidence seal. It does not repeat the R7-R3 8,192-pair performance population and does not claim a new payload-performance result. The runtime artifact must publish:

```text
execution_surface=route-binding-control-plane-probe-v1
payload_dispatch_count=0
```

The evidence under test is route identity, authority ownership, atomic generation transitions, immutable session leases, exact fallback restoration, and cross-route resource isolation.

## 1. Parent authority

The gate consumes the exact R7-R3 runtime artifact and local manifest. Required parent truth:

```text
schema exact
patch_id exact
pass=true
promotion token exact
production_route_shadow_eligibility_pass=true
negative_control_expected=640
```

The candidate route digest must bind the exact parent artifact digest, candidate WGSL digest, candidate dispatcher source digest, runtime-profile digest, and production-compatible output ABI digest.

## 2. SSOT split

Two authorities are required and may not be merged.

### 2.1 ProductionRouteAuthority

Global single-writer SSOT:

```text
authority_revision
authority_digest
active_route_id
candidate_route_id
fallback_route_id
active_route_digest
candidate_route_digest
fallback_route_digest
route_generation
promotion_epoch
rollback_anchor_generation
canary_policy_id
canary_percentage_basis_points
candidate_registration_state
candidate_activation_state
writer_owner_id
writer_epoch
last_committed_transition_id
last_committed_transition_digest
```

### 2.2 SessionRouteLease

Per-session immutable route SSOT:

```text
session_id
leased_route_id
leased_route_digest
leased_route_generation
fallback_route_id
fallback_route_digest
fallback_route_generation
model_identity_digest
device_identity_digest
runtime_profile_digest
kv_cache_owner_id
kv_cache_generation
device_generation
lease_created_before_first_decode
first_decode_started
last_decode_completed
decode_step_count
route_dispatch_probe_count
payload_dispatch_count
route_mutation_count
rejected_route_mutation_attempt_count
route_identity_revalidation_count
route_identity_revalidation_failure_count
lease_state
release_reason
lease_receipt_digest
```

Allowed lifecycle:

```text
Uninitialized -> Bound -> Active -> Completed -> Released
Bound -> Invalid
Active -> Quarantined
```

Forbidden:

```text
Active(candidate) -> Active(fallback)
Active(fallback) -> Active(candidate)
Released -> Active
Quarantined -> Active
```

## 3. Route registry

Exactly two registered entries are required:

```text
existing-production-headwise-reference-v1
gqa4-cluster-production-canary-v1
```

Each entry publishes:

```text
route identity and revision
dispatcher owner
pipeline owner
bind-group owner
submission owner
scratch-factory owner
KV compatibility identity
input/output/scratch/guard/downstream ABI digests
model-shape digest
runtime-profile digest
device-capability digest
parent-artifact digest
kernel identity digest
WGSL digest
pipeline-layout digest
registration and eligibility state
```

Candidate and fallback must have distinct dispatcher, pipeline, bind-group, submission, and scratch-factory owners. Logical KV compatibility does not permit physical KV owner alias.

## 4. Output ABI identity

Both routes must publish the same production output ABI:

```text
q_heads=32
head_dim=64
values=2048
bytes=8192
element=f32
full_overwrite=true
same_device=true
payload_readback=0
host_upload=0
```

Output ABI equality does not imply route-resource ownership equality.

## 5. Canary default and selection

Default global canary percentage is exactly zero. Candidate sessions are selected only through an explicit internal-session selector before lease binding.

Forbidden selection dimensions:

```text
per token
current KV length
current latency
current temperature
worker-local random state
implicit error fallback
```

After a session enters `Bound`, later canary-policy changes may not change that session route.

## 6. Atomic route generation

All global transitions use a compare-and-swap contract:

```text
expected_generation == current_generation
proposed_generation == current_generation + 1
expected active route ID and digest exact
expected fallback route ID and digest exact
writer owner and epoch exact
transition ID not previously committed
intent digest exact
```

On failure:

```text
authority byte-equivalent to pre-transition state
route generation unchanged
candidate activation unchanged
last transition identity unchanged
partial write count=0
```

Permitted transition kinds in R7-R4:

```text
RegisterCandidate
ActivateInternalCanary
DeactivateInternalCanary
RollbackToFallback
```

`PromoteCandidate` as global default is forbidden and must be actively rejected.

## 7. Session stickiness

A session binds one route before the first decode-control step. Every step revalidates:

```text
session identity
leased route ID
leased route digest
leased route generation
KV owner and generation
device generation
runtime-profile identity
```

A global route-generation change affects only sessions bound afterward. Existing candidate sessions continue under their frozen generation until completion or quarantine.

Canonical invariant:

```text
all successful session route_mutation_count=0
```

A mutation attempt must increment only the rejected-attempt counter. It may not alter the lease.

## 8. Exact fallback

Fallback is the exact pre-canary active route, not a candidate route with a disabled flag. Required:

```text
fallback route ID exact
fallback route digest exact
fallback dispatcher independent
fallback pipeline independent
fallback bind groups independent
fallback scratch owner independent
fallback KV owner independent
```

Normal rollback changes global authority for new sessions only. It never splices an active candidate session into fallback.

A hard device or KV-generation mismatch quarantines the active session. The same KV cache may not continue under fallback.

## 9. Test matrix

Control-plane route-dispatch probes:

| Session | Route | Steps | Global transition while active | Expected result |
|---|---|---:|---|---|
| fallback-control-32 | fallback | 32 | none | complete |
| candidate-short-32 | candidate | 32 | none | complete |
| candidate-medium-128 | candidate | 128 | deactivate canary | remains candidate |
| candidate-mutation-probe | candidate | 2 | lease rewrite attempt | rewrite rejected, completes candidate |
| candidate-device-generation-probe | candidate | 0 accepted | device generation mismatch | quarantine |
| candidate-kv-generation-probe | candidate | 0 accepted | KV generation mismatch | quarantine |
| candidate-long-1024 | candidate | 1024 | rollback CAS at step 512 | remains candidate and completes |
| post-rollback-fallback-128 | fallback | 128 | none | complete |

Minimum authority:

```text
completed candidate sessions >=3
completed fallback sessions >=2
completed candidate control steps >=1184
completed fallback control steps >=160
actual mid-session route mutations=0
expected quarantines=2
post-rollback candidate binds=0
```

## 10. Replay and stale protection

Required active probes:

```text
stale expected generation
reused committed transition ID
global PromoteCandidate intent
```

All must be rejected with unchanged authority state.

Required counters outside negative controls:

```text
accepted stale transitions=0
accepted duplicate transitions=0
accepted global promotion transitions=0
partial route writes=0
```

## 11. Runtime artifacts

Required output files:

```text
ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r2f_r7_r4_parent_binding.json
ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r2f_r7_r4_route_registry.json
ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r2f_r7_r4_session_lease_receipts.json
ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r2f_r7_r4_transition_receipts.json
ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r2f_r7_r4_rollback_receipt.json
ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r2f_r7_r4_negative_control_outcomes.json
ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r2f_r7_r4_static_checks.json
ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r2f_r7_r4_route_authority_artifact.json
ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r2f_r7_r4_local_manifest.json
ash_attn_headwise_causal_01b_r12_r3_r3_r3_r2_r7_r2f_r7_r4_canonical_run.ps1
```

## 12. CLI extension

Exact values:

```text
--gqa4-r2f-r4-route-authority-policy atomic-generation-owned-v1
--gqa4-r2f-r4-route-registry-policy exact-identity-registered-v1
--gqa4-r2f-r4-session-route-policy session-sticky-zero-mid-decode-mutation-v1
--gqa4-r2f-r4-canary-selection-policy explicit-internal-session-v1
--gqa4-r2f-r4-canary-percentage-basis-points 0
--gqa4-r2f-r4-candidate-route-id gqa4-cluster-production-canary-v1
--gqa4-r2f-r4-fallback-route-id existing-production-headwise-reference-v1
--gqa4-r2f-r4-route-generation-policy monotonic-cas-plus-one-v1
--gqa4-r2f-r4-rollback-policy exact-fallback-generation-cas-v1
--gqa4-r2f-r4-kv-ownership-policy session-route-generation-locked-v1
--gqa4-r2f-r4-active-session-transition-policy drain-or-quarantine-never-switch-v1
```

Required Boolean keys:

```text
--require-gqa4-r2f-r4-parent-r7-r3-pass true
--require-gqa4-r2f-r4-candidate-registration-exact true
--require-gqa4-r2f-r4-fallback-registration-exact true
--require-gqa4-r2f-r4-canary-default-zero true
--require-gqa4-r2f-r4-explicit-canary-selection true
--require-gqa4-r2f-r4-route-generation-cas true
--require-gqa4-r2f-r4-route-generation-monotonic true
--require-gqa4-r2f-r4-route-transition-single-writer true
--require-gqa4-r2f-r4-route-transition-partial-write-zero true
--require-gqa4-r2f-r4-session-route-lease-before-decode true
--require-gqa4-r2f-r4-session-route-sticky true
--require-gqa4-r2f-r4-zero-mid-decode-route-mutation true
--require-gqa4-r2f-r4-kv-owner-route-exact true
--require-gqa4-r2f-r4-device-generation-lock true
--require-gqa4-r2f-r4-candidate-fallback-resource-alias-zero true
--require-gqa4-r2f-r4-output-abi-exact true
--require-gqa4-r2f-r4-fallback-restoration-exact true
--require-gqa4-r2f-r4-stale-transition-rejection true
--require-gqa4-r2f-r4-transition-replay-zero true
--require-gqa4-r2f-r4-active-session-drain-or-quarantine true
--forbid-gqa4-r2f-r4-global-default-promotion true
--forbid-gqa4-r2f-r4-per-token-route-selection true
--forbid-gqa4-r2f-r4-mid-session-fallback-switch true
--forbid-gqa4-r2f-r4-kv-cache-cross-route-reuse true
--forbid-gqa4-r2f-r4-silent-route-rebinding true
```

R7-R4 adds exactly 36 required CLI keys.

## 13. Negative controls

Inherited R7-R3 authority:

```text
640
```

R7-R4 groups:

```text
route registry identity
candidate parent identity
route generation monotonicity
atomic CAS
partial-write rejection
session lease lifecycle
session stickiness
zero mid-decode mutation
KV ownership
candidate/fallback alias isolation
exact fallback restoration
stale/replay rejection
canary default-zero enforcement
global-promotion prohibition
```

Ten controls per group:

```text
R7-R4 controls=140
combined authority=780
```

## 14. PASS

PASS requires:

```text
parent R7-R3 exact and promoted
registry identity exact
candidate and fallback registration exact
output ABI exact
candidate/fallback resource alias zero
initial canary basis points=0
explicit canary selection only
valid transitions use generation CAS
valid generation sequence is monotonic +1
single transition writer
failed transitions produce zero partial writes
all leases exist before first step
all successful sessions stay on one route
mid-session route mutation count=0
KV owner exact
device generation mismatch quarantined
KV generation mismatch quarantined
candidate/fallback test matrix complete
rollback restores exact fallback for new sessions
active candidate session remains candidate through rollback
stale transition rejected
duplicate transition rejected
global promotion rejected
active global default route unchanged
payload dispatch count=0 in this control-plane gate
780/780 negative controls
all artifacts emitted
```

Success token:

```text
PROMOTE_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R4_PRODUCTION_CANARY_ROUTE_BINDING_SESSION_STICKY_OWNERSHIP_ATOMIC_GENERATION_AND_EXACT_FALLBACK_SEALED
```

Default HOLD:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R4_ROUTE_AUTHORITY_SESSION_STICKINESS_OR_EXACT_FALLBACK_NOT_PROVEN
```

## 15. Non-goals

R7-R4 does not:

```text
make GQA4 the global default
ramp production traffic
perform payload performance measurement
repeat R7-R3 GPU benchmarks
switch routes per token
continue a failed candidate session on fallback
reuse KV cache across routes
perform long-duration soak
implement automatic live health-token fallback
```

The next live-payload stage must consume the R7-R4 route authority and perform candidate execution under a valid session lease without changing this control-plane SSOT.

## 16. Final seal

```text
exact R7-R3 candidate identity
+ exact route registry
+ global single-writer authority
+ generation CAS
+ immutable session lease
+ zero mid-decode switching
+ exact fallback for new sessions
+ zero cross-route KV reuse
+ default-zero explicit canary selection
= production canary route binding without session-state fracture
```
