# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6

## Live Canary Soak / Token-Sequence Continuity / Latency·Thermal Drift / Device Fault Quarantine and Admission Hold Seal

## 0. State

```text
PARENT=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R5
RUN_SCOPE=live-candidate-soak
DEFAULT_VERDICT=HOLD
ACTIVE_ROUTE=existing-production-headwise-reference-v1
CANDIDATE_ROUTE=gqa4-cluster-production-canary-v1
FALLBACK_ROUTE=existing-production-headwise-reference-v1
SOAK_ADMISSION=explicit-revision-owned-soak-epoch-v1
TOKEN_CONTINUITY=global-cohort-monotonic-exact-v1
LATENCY=windowed-gpu-timestamp-drift-v1
THERMAL_EVIDENCE=timestamp-derived-plateau-proxy-v1
DEVICE_FAULT=device-generation-quarantine-v1
RECOVERY=no-automatic-reentry-v1
ARTIFACT_LAYOUT=atlas-parallel-group-map-v1
```

R7-R6 consumes the exact R7-R5 live-payload seal. It proves extended candidate stability without promoting GQA4 to the global default route.

R7-R6 does not claim physical temperature in Celsius. Thermal evidence is derived only from late GPU-timestamp plateau and normalized duration slope.

## 1. Parent authority

Required R7-R5 truth:

```text
parent pass=true
promotion token exact
candidate payload dispatches=1191
healthy candidate commits=1184
health token integrity pass
payload readback=0
same-session fallback=0
candidate admission state=DisabledByHealthFault
route generation=6
active global route=fallback
negative controls=940/940
```

R7-R5 intentionally ended candidate admission after its canonical fault. R7-R6 may not silently reset that state.

## 2. Explicit soak epoch

R7-R6 opens a revision-owned cohort through:

```text
BeginSoakCohort
```

Required CAS:

```text
pre-state=DisabledByHealthFault
post-state=EligibleForExplicitSoakOnly
expected generation=6
committed generation=7
active route ID and digest unchanged
candidate and fallback digests exact
partial writes=0
automatic re-entry=0
```

This is an explicit gate transition, not automatic health recovery.

## 3. Device identity

The cohort is bound to one exact device identity derived from:

```text
backend
adapter name
vendor and device IDs
device type
driver and driver information
requested feature bits
requested limit set
subgroup size
timestamp period
device generation
```

Process pointers, allocation order, and startup time are excluded from the digest.

Required:

```text
subgroup size=32
timestamp period finite and positive
device generation constant=1
required timestamp features present
```

## 4. Population

KV buckets:

```text
128,256,384,512,768,1024,1536,2048
```

Warmup:

```text
8 sessions
128 steps per bucket
1024 candidate steps
```

Measured sessions per bucket:

```text
32 steps
128 steps
1024 steps
2048 steps
```

Totals:

```text
warmup sessions=8
measured sessions=32
total sessions=40
warmup steps=1024
measured steps=25856
total candidate payload steps=26880
```

Execution order:

```text
warmup schedule A
32-step schedule B
128-step schedule A
1024-step schedule B
2048-step schedule A

A=128,2048,256,1536,384,1024,512,768
B=768,512,1024,384,1536,256,2048,128
```

Only one candidate soak session may be active at once.

## 5. Live payload pipeline

Every step executes the exact production-shaped R7-R5 path:

```text
output poison
GQA4 attention
identity fault-injection stage
8-group guard map
single guard finalizer
compact health-token finalizer
device-native downstream gate
token publication
GPU timestamp resolve
```

Per step:

```text
one encoder
one submission
one valid session lease
one route generation
one device generation
one KV generation
one compact token
four GPU timestamp values
```

Healthy token authority remains:

```text
completion mask=0x1ff
fault bits=0
nonfinite count=0
output write count=2048
guard failure bits=0
downstream mask=0x3
health latch=Healthy
integrity exact
```

## 6. Timestamp atlas

Each candidate step records:

```text
T0 candidate begin
T1 candidate end
T2 full guarded pipeline begin
T3 full guarded pipeline end
```

Derived surfaces:

```text
kernel duration=T1-T0
guarded duration=T3-T2
```

Timestamp query batches contain no more than 256 payload steps. Query resolve and compact readback happen only after each batch, never after each step.

Required:

```text
zero per-step timestamp readback
zero per-step host wait
all raw timestamp pairs retained
invalid timestamp count=0
```

## 7. Token sequence continuity

Three domains remain separate:

```text
cohort-global token sequence
session-local decode step
cohort snapshot sequence
```

Global range:

```text
0..26879
```

Required:

```text
first=0
last=26879
published=26880
drained=26880
missing=0
duplicate=0
regression=0
wrap=0
```

For every session:

```text
decode step range=0..requested_steps-1
missing=0
duplicate=0
regression=0
```

Snapshot ranges must be contiguous, non-overlapping, generation-locked, and cover the full cohort.

## 8. Statistical windows

Warmup timestamps are retained but excluded from drift authority.

Measured population:

```text
25856 timestamps
256 samples per statistical window
101 exact windows
```

Each window publishes absolute GPU ns:

```text
kernel min, median, p95, p99, max, MAD
guarded min, median, p95, p99, max, MAD
bucket composition
session composition
first and last token sequence
```

No sample, failed window, or outlier may be removed or replaced.

## 9. KV-conditioned normalization

Absolute durations across KV buckets are not directly interchangeable. Before global-window drift evaluation, each sample is normalized by its own KV bucket baseline.

Bucket baseline:

```text
first 160 measured samples per KV bucket
= 32-step session + 128-step session
```

Required retained evidence:

```text
absolute raw ns
bucket baseline ns
normalized window ratios
```

Normalization must not remove or rewrite raw timestamps.

## 10. Frozen global baseline

The first sixteen normalized statistical windows form the frozen global baseline.

Required:

```text
baseline windows=0..15
all baseline tokens healthy
all timestamps valid
baseline never reconstructed from later windows
```

Baseline surfaces:

```text
kernel normalized median, p95, p99
guarded normalized median, p95, p99
```

## 11. Latency drift gates

Per-window limits:

```text
kernel median ratio <=1.15
kernel p95 ratio <=1.25
kernel p99 ratio <=1.40

guarded median ratio <=1.15
guarded p95 ratio <=1.25
guarded p99 ratio <=1.40
```

Consecutive-window limits:

```text
no three consecutive median failures
no two consecutive p95 failures
```

KV-conditioned limits:

```text
each bucket later median / bucket baseline median <=1.20
each bucket later p95 / bucket baseline p95 <=1.30
```

A global average may not hide a long-KV regression.

## 12. Thermal plateau proxy

```text
thermal_sensor_observed=false
thermal_evidence_kind=timestamp-derived-plateau-proxy-v1
```

Late plateau:

```text
final 16 normalized windows
```

Required:

```text
late kernel median ratio <=1.10
late guarded median ratio <=1.10
late kernel p95 ratio <=1.20
late guarded p95 ratio <=1.20
```

Slope authority:

```text
Theil-Sen slope of normalized window medians
kernel slope <=0.002 per window
guarded slope <=0.002 per window
```

Long-KV plateau:

```text
KV 1024,1536,2048
late median / bucket baseline median <=1.15
```

## 13. Soft drift hold

Soft conditions:

```text
window latency threshold failure
consecutive drift failure
bucket-conditioned drift failure
thermal plateau failure
thermal slope failure
token or snapshot continuity failure without device loss
```

Transition:

```text
EligibleForExplicitSoakOnly
-> AdmissionHeldByDrift
```

Effect:

```text
current healthy session may finish
new candidate sessions rejected
new sessions bind fallback
active global route unchanged
automatic re-entry forbidden
```

## 14. Hard device quarantine

Hard conditions:

```text
device lost
queue submission failure
uncaptured validation error
device generation change
required feature or limit disappearance
timestamp subsystem failure
token-ring integrity failure
repeated token integrity failure
```

Transition:

```text
EligibleForExplicitSoakOnly
-> DeviceQuarantined
```

Effect:

```text
affected session quarantined
all leases on affected device generation invalidated
candidate downstream commit blocked
new candidate sessions rejected
new sessions bind fallback
same-session fallback forbidden
automatic device re-entry forbidden
```

## 15. Successful terminal hold

A successful soak does not leave candidate admission open.

Required transition:

```text
EligibleForExplicitSoakOnly
-> SoakCompleteHold

generation 7 -> 8
```

Meaning:

```text
soak evidence passed
candidate remains non-default
new candidate sessions require a later explicit promotion revision
fallback remains active global route
```

## 16. New-session fallback

After any terminal state:

```text
SoakCompleteHold
AdmissionHeldByDrift
DeviceQuarantined
```

new sessions must bind the exact fallback route with:

```text
new session ID
new lease
new KV owner
new scratch owner
candidate dispatcher calls=0
candidate token publications=0
```

R7-R6 executes one 128-step post-hold fallback session.

## 17. Isolated fault rehearsals

Required isolated cases:

```text
sequence gap -> AdmissionHeldByDrift
sequence duplicate -> AdmissionHeldByDrift
snapshot overlap -> AdmissionHeldByDrift
sustained latency drift -> AdmissionHeldByDrift
late thermal plateau drift -> AdmissionHeldByDrift
device generation change -> DeviceQuarantined
submission failure -> DeviceQuarantined
device lost -> DeviceQuarantined
```

Each rehearsal must prove:

```text
new candidate admission rejected
new fallback session accepted
same-session fallback=0
automatic re-entry=0
live soak authority mutation=0
```

## 18. Host observation boundary

Allowed host readback:

```text
compact health tokens
GPU timestamp results
window receipts
device fault event receipt
route transition receipts
```

Forbidden:

```text
candidate output payload
fallback output payload
Q/K/V payload
KV texture payload
per-element guard map
downstream output payload
```

Required counters:

```text
payload readback=0
payload host materialization=0
payload host upload=0
per-step host wait=0
compact telemetry readback>0
timestamp readback>0
```

## 19. Artifact set

Required outputs:

```text
*_parent_binding.json
*_soak_cohort_authority.json
*_device_identity.json
*_soak_sessions.json
*_token_sequence_ledger.json
*_timestamp_raw_samples.json
*_latency_windows.json
*_bucket_conditioned_drift.json
*_thermal_plateau_proxy.json
*_device_quarantine_receipt.json
*_admission_hold_receipt.json
*_fallback_session_receipt.json
*_fault_rehearsal_receipts.json
*_negative_control_outcomes.json
*_static_checks.json
*_runtime_artifact.json
*_local_manifest.json
*_canonical_run.ps1
```

Runtime artifact groups:

```text
identity
soak_epoch
device_identity
population
token_continuity
timestamp_atlas
latency_baseline
latency_drift
thermal_plateau
admission_hold
fallback_activation
fault_rehearsals
negative_controls
verdict
```

Every group has an independent field count and SHA-256 digest. The root publishes group order, group digests, and full atlas digest.

## 20. CLI contract

R7-R6 adds:

```text
25 exact-value keys
42 Boolean keys
67 required CLI keys
```

Exact values include population, timestamp-window, baseline, plateau, and drift thresholds exactly as defined above.

Required Boolean policy includes:

```text
parent R7-R5 exact
explicit soak epoch CAS
default route unchanged
sequential session execution
session stickiness
device identity and generation lock
token, session-step, and snapshot continuity
timestamp atlas and raw retention
exact 101-window population
frozen baseline
kernel, guarded, and bucket drift gates
thermal plateau and slope gates
soft hold and hard quarantine
new-session fallback
zero same-session fallback
zero cross-route KV reuse
final SoakCompleteHold
fault-rehearsal isolation
payload readback zero
atlas artifact layout
```

Forbidden policies include automatic re-entry, baseline reconstruction, token or timestamp filtering, selective window rerun, mid-session switching, global-default promotion, and physical-temperature claims.

## 21. Negative controls

Inherited:

```text
R7-R5=940
```

R7-R6 adds eighteen groups with ten controls each:

```text
parent identity
explicit soak admission
device identity
global sequence
session steps
snapshot ranges
timestamp continuity
window population
frozen baseline
kernel drift
guarded drift
bucket drift
thermal plateau
soft hold
hard quarantine
device-generation invalidation
fallback and no re-entry
raw evidence and atlas integrity
```

Total:

```text
R7-R6=180
combined=1120
```

## 22. PASS

PASS requires:

```text
parent R7-R5 exact
BeginSoakCohort generation 6->7 CAS
40/40 sessions healthy
26880/26880 candidate payload steps
26880/26880 compact tokens
25856/25856 measured timestamps
101/101 statistical windows
token continuity pass
latency drift pass
bucket-conditioned drift pass
thermal plateau proxy pass
device faults=0
session quarantines=0
payload readback=0
per-step host wait=0
isolated fault rehearsals pass
SoakCompleteHold generation 7->8 CAS
post-hold fallback exact
active global route unchanged
1120/1120 negative controls
all artifacts and atlas digests exact
```

Success:

```text
PROMOTE_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_LIVE_CANARY_SOAK_TOKEN_CONTINUITY_LATENCY_THERMAL_DRIFT_DEVICE_QUARANTINE_AND_ADMISSION_HOLD_SEALED
```

Default HOLD:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_SOAK_CONTINUITY_DRIFT_DEVICE_HEALTH_OR_ADMISSION_HOLD_NOT_PROVEN
```

A failed run must close admission as either `AdmissionHeldByDrift` or `DeviceQuarantined`.

## 23. Non-goals

R7-R6 does not:

```text
make candidate the global default
run concurrent candidate sessions
claim Celsius temperature
use vendor-specific temperature APIs
automatically recover a quarantined device
automatically reopen candidate admission
perform fleet rollout
perform public percentage rollout
inspect payload values on the host
```

## 24. Final seal

```text
R7-R5 live candidate payload authority
+ explicit generation-owned soak epoch
+ 40 deterministic sessions
+ 26880 actual candidate payload steps
+ exact compact-token continuity
+ 25856 retained GPU timestamp samples
+ KV-conditioned normalization
+ frozen 101-window latency authority
+ timestamp-derived thermal plateau proxy
+ soft drift admission hold
+ hard device quarantine
+ exact new-session fallback
+ no automatic re-entry
+ unchanged global default route
= long-running candidate evidence without silent sequence loss, KV-cost misattribution, drift concealment, or unhealthy re-admission
```
