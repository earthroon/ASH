# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R5

## Live Candidate Payload Session / Compact GPU Health Token / Fail-Closed Session Quarantine / New-Session Fallback Activation Seal

## 0. State

```text
SPEC_ID=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R5
PARENT_SPEC=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R4
RUN_SCOPE=live-candidate-payload-canary
DEFAULT_VERDICT=HOLD
ACTIVE_PRODUCTION_ROUTE=existing-production-headwise-reference-v1
CANDIDATE_ROUTE=gqa4-cluster-production-canary-v1
FALLBACK_ROUTE=existing-production-headwise-reference-v1
LIVE_PAYLOAD_POLICY=valid-session-lease-only-v1
GPU_HEALTH_TOKEN_POLICY=compact-device-native-session-token-v1
SESSION_HEALTH_POLICY=sticky-device-latch-fail-closed-v1
FAULT_POLICY=quarantine-current-session-disable-new-candidate-admission-v1
FALLBACK_ACTIVATION_POLICY=new-session-only-generation-cas-v1
HOST_OBSERVATION_POLICY=asynchronous-token-drain-no-payload-readback-v1
ARTIFACT_LAYOUT=atlas-parallel-group-map-v1
```

R7-R5 is the first revision in this lineage that executes the actual GQA4 candidate payload under an R7-R4 production-canary session lease. It does not make GQA4 the global default route.

## 1. Parent authority

R7-R5 consumes the exact R7-R4 route authority artifact, route registry, local manifest, runtime profile, and promotion token.

Required parent truth:

```text
parent pass=true
parent promotion token exact
negative-control authority=780
route registry identity exact
candidate registration exact
fallback registration exact
session-sticky ownership pass
zero mid-decode mutation pass
atomic generation pass
rollback exact
active global route remains fallback
```

Candidate and fallback route digests are loaded from the R7-R4 route registry artifact referenced by the parent manifest. R7-R5 may not synthesize or silently rebind either route identity.

## 2. Goal

R7-R5 proves:

```text
actual candidate WGSL payload dispatch
valid candidate lease before payload execution
one encoder and one submission per candidate payload step
one compact GPU health token per accepted candidate payload step
device-native health decision before downstream commit
zero candidate payload readback
asynchronous batched compact-token drain
sticky current-session quarantine on hard fault
zero same-session fallback continuation
generation-CAS disablement of future candidate admission
exact fallback binding for newly created sessions
unchanged global default route
```

Current-session quarantine and future-session fallback activation are separate authorities.

## 3. Runtime execution surface

Each healthy candidate payload step is encoded in this exact order:

```text
1 output poison pass
2 GQA4 candidate attention pass
3 isolated fault-injection pass, normally identity
4 eight-group headwise guard-map pass
5 single guard-finalizer pass
6 compact health-token finalizer
7 device-native production-compatible downstream gate
8 compact token publication finalizer
```

All eight stages use:

```text
one command encoder
one queue submission
one session lease
one route generation
one device generation
one KV generation
```

There is no per-step host wait. The host waits only at session completion to drain the compact token snapshot.

## 4. Live candidate session contract

Candidate execution is legal only when:

```text
leased route ID == gqa4-cluster-production-canary-v1
leased route digest == parent route-registry candidate digest
leased route generation == frozen session generation
device generation exact
KV generation exact
session health latch == Healthy
candidate admission was Eligible at bind time
```

Forbidden:

```text
candidate payload without lease
per-step route rebinding
per-step lease recreation
candidate dispatch after quarantine
same-session candidate-to-fallback switch
fallback reuse of candidate KV state
CPU payload inspection before commit
```

## 5. GPU health token

Each accepted candidate payload step publishes one fixed token:

```text
token schema=compact-health-token-u32x16-v1
word count=16 u32
token size=64 bytes
alignment=16 bytes
device ring capacity=4096
readback snapshot ring capacity=4
```

Canonical layout:

| Index | Field |
|---:|---|
| 0 | magic `0x41534835` |
| 1 | schema version `1` |
| 2 | token sequence |
| 3 | session lease tag |
| 4 | decode step |
| 5 | route generation |
| 6 | device generation |
| 7 | KV generation |
| 8 | completion mask |
| 9 | fault bits |
| 10 | nonfinite count |
| 11 | output write count |
| 12 | guard failure bits |
| 13 | downstream completion mask |
| 14 | session health latch |
| 15 | integrity XOR over words 0 through 14 |

Healthy token requirements:

```text
magic exact
schema exact
token sequence exact
session lease tag exact
route generation exact
device generation exact
KV generation exact
completion mask=0x1ff
fault bits=0
nonfinite count=0
output write count=2048
guard failure bits=0
downstream completion mask=0x3
session health latch=0
integrity XOR exact
```

The 32-bit lease tag is only a compact token field. The full session lease digest remains the host-side identity authority, and every tag must map to exactly one full digest in the run receipt.

## 6. Full-overwrite and nonfinite truth

Before every candidate dispatch, the 2,048-element output is poisoned with NaN bit patterns. The candidate must overwrite all 2,048 f32 elements.

An eight-workgroup guard map scans the output on device. Each 64-lane group accounts for four values per lane and publishes an independent visited/nonfinite pair. A separate single-workgroup guard finalizer reduces the eight group receipts into:

```text
visited element count
nonfinite element count
guard failure bits
full-overwrite truth
```

The compact health-token finalizer consumes only this guard summary. It does not rescan the output payload.

Healthy authority requires:

```text
visited count=2048
nonfinite count=0
```

No output element is copied to a readback buffer.

## 7. Completion mask

Canonical completion bits:

```text
bit 0 candidate attention complete
bit 1 full-overwrite validation complete
bit 2 guard map complete
bit 3 guard finalizer complete
bit 4 health token finalized
bit 5 device decision complete
bit 6 downstream projection-compatible stage complete
bit 7 residual-compatible stage complete
bit 8 token publication complete
```

Healthy final mask is `0x1ff`.

A faulted token may publish bit 8 while bits 6 and 7 remain clear. Downstream completion without the device decision bit is forbidden.

## 8. Fault bits

Canonical hard-fault bits:

```text
bit 0 nonfinite output
bit 1 output write-count mismatch
bit 2 guard failure
bit 4 route-generation mismatch
bit 5 device-generation mismatch
bit 6 KV-generation mismatch
bit 7 token-integrity failure
bit 8 token-ring overflow
bit 9 downstream-completion mismatch
bit 10 session lease-tag mismatch
bit 11 candidate dispatch after quarantine
bit 12 output ABI mismatch
bit 13 submission-completion failure
```

Any defined fault transitions the session health latch:

```text
Healthy -> Quarantined
```

Quarantined is terminal in R7-R5.

## 9. Device-native gate

The GPU health latch is authoritative before host observation.

Required ordering:

```text
candidate output
eight-group guard-map accounting
single guard-finalizer reduction
health-token finalization
GPU latch decision
downstream dispatch only when latch is Healthy
final token publication
```

Required fault behavior:

```text
faulted output commit count=0
faulted downstream commit count=0
later candidate dispatch count=0
same-session fallback count=0
continuation rejection count>=1
```

## 10. Host observation boundary

Host-readable surfaces:

```text
compact token snapshots
session quarantine receipts
candidate-admission transition receipt
aggregate counters
```

Forbidden host-readable surfaces:

```text
candidate attention payload
fallback attention payload
Q/K/V payload
KV texture payload
per-element guard map
production-compatible downstream payload
```

Canonical counters:

```text
payload_readback_count=0
payload_host_materialization_count=0
payload_host_upload_count=0
per_step_host_wait_count=0
```

Q and KV fixtures are generated and populated by the existing same-device GPU fixture path. Control uniforms are not payload materialization.

## 11. Healthy live candidate matrix

Required healthy candidate sessions:

| Session | Payload steps | Expected state |
|---|---:|---|
| `candidate-live-short-32` | 32 | Completed |
| `candidate-live-medium-128` | 128 | Completed |
| `candidate-live-long-1024` | 1024 | Completed |

Required totals:

```text
healthy candidate sessions=3
healthy candidate payload dispatches=1184
healthy health tokens=1184
healthy downstream commits=1184
healthy quarantines=0
route mutations=0
```

## 12. Isolated fault rehearsal

Fault rehearsals use an isolated route-generation domain and independent session resources. They may not mutate the live candidate admission authority.

Required rehearsals:

| Session | Injection | Required outcome |
|---|---|---|
| `rehearsal-nonfinite` | NaN output | Quarantined |
| `rehearsal-partial-overwrite` | poisoned element retained | Quarantined |
| `rehearsal-guard-failure` | guard bit | Quarantined |
| `rehearsal-route-generation` | generation mismatch | Quarantined |
| `rehearsal-kv-generation` | KV mismatch | Quarantined |
| `rehearsal-token-overflow` | overflow fault bit | Quarantined |

Each rehearsal executes exactly one actual GQA4 payload dispatch and emits one compact token.

Required per-rehearsal truth:

```text
candidate payload dispatches=1
health tokens=1
downstream commits=0
candidate output commits=0
health transition count=1
session state=Quarantined
continuation rejected
same-session fallback count=0
```

## 13. Canonical live fault

After all healthy candidate sessions complete, R7-R5 executes:

```text
session=candidate-live-fault-nonfinite
fault=nonfinite-step-zero-v1
fault step=0
```

Required result:

```text
candidate payload dispatches=1
health tokens=1
nonfinite count>0
fault bit 0 set
downstream commits=0
candidate output commits=0
session state=Quarantined
continuation rejected
```

## 14. Candidate admission disablement

After asynchronous observation of the canonical live fault:

```text
CandidateAdmissionHealth:
Eligible -> DisabledByHealthFault
```

The transition must satisfy:

```text
expected generation == parent R7-R4 final generation
committed generation == expected generation + 1
active route ID unchanged
active route digest unchanged
candidate route registration retained
fallback route identity retained
partial write count=0
new candidate lease rejected
automatic candidate re-entry count=0
```

Candidate re-entry is not permitted in R7-R5.

## 15. New-session fallback

Fallback protects sessions created after candidate admission disablement. It does not repair or continue the faulted session.

Required fallback sessions:

| Session | Payload steps | Route |
|---|---:|---|
| `fallback-control-32` | 32 | exact fallback |
| `post-health-fault-fallback-128` | 128 | exact fallback |

Required totals:

```text
fallback sessions=2
fallback payload dispatches=160
fallback downstream commits=160
candidate dispatcher calls in fallback sessions=0
fallback quarantines=0
```

The post-fault fallback session must own a new session ID, lease identity, KV owner, scratch owner, and submission state.

## 16. Aggregate payload authority

Canonical candidate count:

```text
1184 healthy candidate steps
+ 6 isolated fault-rehearsal steps
+ 1 canonical live-fault step
= 1191 actual candidate payload dispatches
```

Canonical compact-token count:

```text
expected=1191
published=1191
drained=1191
healthy=1184
faulted=7
missing=0
duplicate sequence=0
duplicate session-step=0
integrity failure=0
```

## 17. Resource ownership

Every session creates independent:

```text
KV texture residency
source fixture ownership
candidate or fallback attention scratch
output scratch
downstream scratch
session health latch
compact token ring
uniform control state
```

Candidate and fallback sessions may share the logical ABI but may not share mutable physical session resources.

Forbidden:

```text
cross-route KV ownership reuse
cross-session health latch reuse
cross-session token ring reuse
faulted candidate scratch reuse by fallback
faulted candidate lease continuation
```

## 18. Artifact model

Required artifacts:

```text
*_parent_binding.json
*_live_payload_sessions.json
*_health_token_receipt.json
*_quarantine_receipts.json
*_fault_rehearsal_receipts.json
*_candidate_admission_receipt.json
*_new_session_fallback_receipt.json
*_fallback_sessions.json
*_negative_control_outcomes.json
*_static_checks.json
*_runtime_artifact.json
*_local_manifest.json
*_canonical_run.ps1
```

The runtime artifact uses `atlas-parallel-group-map-v1` with these groups:

```text
identity
policies
payload_execution
health_tokens
healthy_sessions
fault_rehearsals
live_quarantine
candidate_admission
fallback_activation
negative_controls
verdict
```

Each group publishes its own field count and SHA-256 digest. The root publishes the ordered group digest map and full atlas digest.

## 19. CLI contract

Exact value keys:

```text
--gqa4-r2f-r5-live-payload-policy valid-session-lease-only-v1
--gqa4-r2f-r5-health-token-policy compact-device-native-session-token-v1
--gqa4-r2f-r5-health-token-schema compact-health-token-u32x16-v1
--gqa4-r2f-r5-health-token-device-ring-capacity 4096
--gqa4-r2f-r5-health-token-readback-ring-capacity 4
--gqa4-r2f-r5-token-drain-policy asynchronous-batched-snapshot-v1
--gqa4-r2f-r5-session-health-policy sticky-device-latch-fail-closed-v1
--gqa4-r2f-r5-fault-policy quarantine-current-session-disable-new-candidate-admission-v1
--gqa4-r2f-r5-fallback-activation-policy new-session-only-generation-cas-v1
--gqa4-r2f-r5-output-consumer internal-production-compatible-canary-v1
--gqa4-r2f-r5-fault-rehearsal-policy isolated-authority-domain-v1
--gqa4-r2f-r5-healthy-session-steps 32,128,1024
--gqa4-r2f-r5-fallback-session-steps 32,128
--gqa4-r2f-r5-live-fault nonfinite-step-zero-v1
```

Required Boolean keys:

```text
--require-gqa4-r2f-r5-parent-r7-r4-pass true
--require-gqa4-r2f-r5-live-candidate-payload true
--require-gqa4-r2f-r5-valid-session-lease true
--require-gqa4-r2f-r5-one-encoder-per-step true
--require-gqa4-r2f-r5-one-submission-per-step true
--require-gqa4-r2f-r5-compact-device-health-token true
--require-gqa4-r2f-r5-one-token-per-candidate-step true
--require-gqa4-r2f-r5-token-sequence-exact true
--require-gqa4-r2f-r5-token-integrity true
--require-gqa4-r2f-r5-output-write-count-exact true
--require-gqa4-r2f-r5-nonfinite-zero-for-healthy true
--require-gqa4-r2f-r5-guard-failure-zero-for-healthy true
--require-gqa4-r2f-r5-device-native-downstream-gate true
--require-gqa4-r2f-r5-zero-faulted-output-commit true
--require-gqa4-r2f-r5-zero-faulted-downstream-commit true
--require-gqa4-r2f-r5-sticky-session-health-latch true
--require-gqa4-r2f-r5-current-session-quarantine true
--require-gqa4-r2f-r5-quarantined-session-terminal true
--require-gqa4-r2f-r5-zero-same-session-fallback true
--require-gqa4-r2f-r5-zero-cross-route-kv-reuse true
--require-gqa4-r2f-r5-async-token-drain true
--require-gqa4-r2f-r5-payload-readback-zero true
--require-gqa4-r2f-r5-hot-path-host-wait-zero true
--require-gqa4-r2f-r5-candidate-admission-disable-cas true
--require-gqa4-r2f-r5-new-session-fallback-exact true
--require-gqa4-r2f-r5-existing-healthy-session-sticky true
--require-gqa4-r2f-r5-fault-rehearsal-isolation true
--require-gqa4-r2f-r5-active-default-route-unchanged true
--forbid-gqa4-r2f-r5-candidate-auto-reentry true
--forbid-gqa4-r2f-r5-per-step-route-rebinding true
--forbid-gqa4-r2f-r5-cpu-payload-health-inspection true
--forbid-gqa4-r2f-r5-host-synthetic-health-token true
--forbid-gqa4-r2f-r5-global-default-promotion true
```

R7-R5 adds exactly 47 required CLI keys.

## 20. Static truth

Static extraction must prove:

```text
actual GQA4 candidate shader used
one live-step encoder path
eight-group guard-map pass present
independent guard-finalizer pass present
health finalizer consumes guard summary rather than payload
compact u32x16 token layout
GPU atomic session latch
GPU downstream gate reads latch
publication finalizer sets downstream and publication bits
candidate output is never passed to compact readback
no active-lease fallback rebinding path
candidate admission disablement is generation-owned
atlas group map artifact layout
```

## 21. Negative controls

Inherited authority:

```text
R7-R4 combined controls=780
```

R7-R5 groups:

```text
valid candidate lease enforcement
payload execution accounting
health-token schema
health-token sequence and integrity
completion-mask authority
nonfinite detection
full-overwrite accounting
guard-failure propagation
device-native downstream gate
sticky quarantine latch
same-session fallback prohibition
asynchronous token drain
candidate-admission CAS
new-session fallback identity
rehearsal-authority isolation
automatic candidate re-entry prohibition
```

Ten controls per group:

```text
R7-R5 controls=160
combined authority=940
```

## 22. PASS

PASS requires:

```text
parent R7-R4 exact and promoted
route registry and runtime profile exact
candidate and fallback output ABI exact
three healthy candidate sessions complete
healthy candidate dispatches=1184
healthy candidate tokens=1184
healthy candidate downstream commits=1184
six isolated fault sessions quarantine
canonical live nonfinite session quarantines
faulted output commits=0
faulted downstream commits=0
same-session fallback count=0
all token fields and integrity exact
all token sequences and session steps unique within session
candidate payload readback=0
per-step host wait=0
candidate admission disablement CAS pass
route generation increments exactly one
candidate automatic re-entry=0
new candidate lease rejected
post-fault fallback route exact
fallback dispatches=160
candidate calls in fallback sessions=0
cross-route KV reuse=0
active global route unchanged
940/940 negative controls
all artifacts emitted
```

Success token:

```text
PROMOTE_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R5_LIVE_CANDIDATE_PAYLOAD_COMPACT_GPU_HEALTH_TOKEN_FAIL_CLOSED_QUARANTINE_AND_NEW_SESSION_FALLBACK_SEALED
```

Default HOLD:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R5_LIVE_PAYLOAD_HEALTH_TOKEN_QUARANTINE_OR_FALLBACK_ACTIVATION_NOT_PROVEN
```

## 23. Non-goals

R7-R5 does not:

```text
make candidate the global default
serve non-canary production traffic through candidate
continue a faulted session on fallback
reuse faulted candidate KV state
automatically re-enable candidate admission
perform long-duration soak
apply latency or thermal drift policy
persist device quarantine across process restart
implement installed-runtime attestation
```

## 24. Final seal

```text
R7-R4 session-sticky route authority
+ actual GQA4 payload execution
+ one compact GPU token per candidate step
+ device-native downstream gating
+ zero payload readback
+ terminal current-session quarantine
+ zero same-session fallback
+ generation-CAS future admission disablement
+ exact fallback for newly created sessions
+ unchanged global default route
= live candidate canary execution without payload leakage or session-state fracture
```

Canonical interpretation:

```text
a faulted candidate session is terminated, not repaired
fallback protects the next session, not the failed session
the GPU decides whether the current payload may commit
the host decides whether future sessions may enter the candidate route
```
