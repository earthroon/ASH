# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6-R5-R1-R2

## Paired No-Probe Shadow Cohort / Between-Step Queue-State Equivalence / Diagnostic Workload Interference Attribution / Control-KV Stability / Localization Validity Seal

## 0. State

```text
PARENT=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6-R5-R1-R1
PARENT_VERDICT=HOLD
RUN_SCOPE=full-authority-plus-paired-probe-shadow-interference-seal
DEFAULT_VERDICT=HOLD
ACTIVE_ROUTE=existing-production-headwise-reference-v1
CANDIDATE_ROUTE=gqa4-cluster-production-canary-v1
PAIR_POLICY=same-kv-role-profile-step-ordinal-probe-shadow-v1
QUEUE_POLICY=observable-between-step-queue-state-accounting-v1
SHADOW_POLICY=zero-diagnostic-pass-production-identical-shadow-v1
INTERFERENCE_POLICY=exact-paired-tail-and-duration-asymmetry-v1
CONTROL_POLICY=shadow-first-control-kv-stability-v1
LOCALIZATION_VALIDITY_POLICY=probe-independence-required-localization-validity-v1
THRESHOLD_POLICY=r6-thresholds-immutable-v1
RAW_SAMPLE_POLICY=retain-all-zero-filtering-v1
ARTIFACT_LAYOUT=atlas-parallel-group-map-v1
```

The revision determines whether the diagnostic workload changed the production-step distribution that the R1-R1 topology cohort attempted to observe. It does not repair the kernel and does not promote the candidate route.

## 1. Parent evidence

Required parent facts:

```text
full sessions=72/72
topology sessions=8/8
total sessions=80/80
candidate steps=69120/69120
page passes=30720/30720
workgroup passes=65536/65536
cross passes=28672/28672
kernel distribution drift=true
guarded distribution drift=true
kernel temporal persistence=false
guarded temporal persistence=false
observer=true
thermal=true
payload readback=0
fallback exact=true
global default unchanged=true
generation=14
```

Parent topology evidence remains immutable. `DiffuseKernelTail` is provisional until probe independence is proven.

## 2. Runtime population

```text
full authority sessions=72
Probe sessions=8
Shadow sessions=8
total sessions=88

full authority candidate steps=52736
Probe candidate steps=16384
Shadow candidate steps=16384
total candidate steps=85504
total compact tokens=85504
```

Probe and Shadow pairs cover:

```text
KV=256,384,512,768
role=Reference,Evaluation
profile=2048 steps
8 exact pairs
```

## 3. Real between-step topology execution

R1-R2 does not run all diagnostics after the production session. In Probe sessions the backend submits:

```text
production step N
then diagnostic page/workgroup/cross work scheduled for N
then production step N+1
```

Shadow sessions submit the same production path and record the same synthetic exposure classes, but submit zero diagnostic work.

Required:

```text
Probe diagnostic passes=124928
Shadow diagnostic passes=0
Diagnostic query batches=1952
Diagnostic session-end drains=8
Production query batches=360
Production session-end drains=88
```

No host wait, map, or device poll with Wait may occur between production steps.

## 4. Pair identity and counterbalance

Canonical pair key:

```text
KV length
role
profile steps
production shader digest
runtime profile digest
route generation
device generation
```

Order:

```text
parity=(KV index + role index) mod 2
parity 0: Probe then Shadow
parity 1: Shadow then Probe
```

Required:

```text
Probe-first pairs=4
Shadow-first pairs=4
```

Session IDs, leases, KV owners, scratch owners, and token domains never overlap.

## 5. Exposure classes

Each production step is classified before execution:

```text
SessionStart: step=0
Clean: even step >0
PageWorkgroup: odd step and previous even step is not divisible by 8
CrossSchedule: odd step and previous even step is divisible by 8
```

Per 2048-step session:

```text
SessionStart=1
Clean=1023
PageWorkgroup=768
CrossSchedule=256
```

Expected diagnostic work between prior and current production step:

| KV | Clean | PageWorkgroup | CrossSchedule |
|---:|---:|---:|---:|
| 256 | 0 | 10 | 10 |
| 384 | 0 | 11 | 35 |
| 512 | 0 | 12 | 44 |
| 768 | 0 | 14 | 14 |

Shadow actual diagnostic work is always zero while expected Probe work remains recorded.

## 6. Observable queue-state authority

Every production step records:

```text
pair ID
role and pair kind
KV and phase
session step
exposure class
production submit ordinal
previous production submit ordinal
diagnostic command buffers since prior production
diagnostic page/workgroup/cross passes
query resolve bytes
copy bytes
host waits
Wait polls
map operations
route generation
device generation
```

Probe and Shadow must be identical in production path identity. Only diagnostic command buffers, query resolves, and diagnostic copies may differ.

This proves observable queue-state equivalence. It does not claim direct visibility into cache contents, clocks, or internal scheduler state.

## 7. Shadow-derived common q99 ruler

Only Shadow Reference sessions construct the common boundary.

For each:

```text
surface=kernel,guarded
KV=256,384,512,768
phase=0,1,2,3
samples=512
cells=32
```

Boundary:

```text
1.40 × exact Shadow Reference lower-confidence q99
```

The same boundary is applied to Probe Evaluation and Shadow Evaluation. Probe Reference samples never influence the common ruler.

## 8. Shadow and Probe reproduction

For each pair kind, surface, and KV:

```text
samples=2048
q99 budget=0.01
exact one-sided Clopper-Pearson confidence
```

States:

```text
Noninferior
Drift
Inconclusive
```

Classes:

```text
ReproducedDrift
DirectionallyConsistentInconclusive
InconclusiveBelowBudget
NotReproduced
```

## 9. Exact paired interference units

Authoritative units:

```text
4 KV × 2 surfaces × 3 exposure classes=24
family alpha=0.05
unit alpha=0.05/24 or stricter
```

Each unit pairs Probe and Shadow at the same Evaluation step.

Duration evidence:

```text
delta=Probe duration-Shadow duration
exact one-sided sign test
positive/negative/tie accounting
median delta
median Probe/Shadow ratio
```

Tail evidence:

```text
Probe tail / Shadow tail
Probe-only tail
Shadow-only tail
neither tail
exact one-sided McNemar binomial test
```

Normal approximation and unpaired tests are forbidden.

Unit verdicts:

```text
NoDetectedInterference
ConfirmedProbeInterference
ShadowSlower
ConflictingEvidence
Underpowered
```

Confirmed Probe interference requires both paired duration and paired tail evidence to point in the Probe-slower direction at familywise-adjusted alpha.

## 10. Control-KV stability

Controls:

```text
KV 256
KV 768
```

Classes:

```text
ShadowStable
ProbeOnlyControlDrift
IntrinsicControlDrift
ControlInconclusive
ControlEvidenceInvalid
```

Shadow Drift is intrinsic control instability. Probe-only Drift requires a corresponding exact paired interference unit.

A ProbeOnlyControlDrift invalidates prior localization globally. IntrinsicControlDrift seals control instability and prevents target-specific localization from being treated as cleanly anchored.

## 11. Target authority

Targets:

```text
KV 384
KV 512
```

Classes:

```text
IntrinsicTargetDrift
ProbeInducedTargetDrift
MixedIntrinsicAndProbeInterference
TargetDriftNotReproduced
TargetValidityInconclusive
```

KV 512 `DiffuseKernelTail` is valid only when:

```text
Shadow Drift reproduces
Probe Drift reproduces
no ConfirmedProbeInterference unit exists for KV 512
controls remain ShadowStable
queue evidence is complete
```

KV 384 cannot become source-localization valid in this revision because the parent localization was inconclusive. It may become not applicable, remain inconclusive, or be marked probe-confounded.

## 12. Overall localization validity

Canonical classes:

```text
LocalizationValiditySealed
DiagnosticInterferenceConfirmed
MixedInterferenceAndIntrinsicDrift
ControlKvInstabilitySealed
TargetDriftNotReproducedInShadow
PartialLocalizationValiditySealed
LocalizationValidityInconclusive
```

All classes except `LocalizationValidityInconclusive` are diagnostic PASS states. PASS means the measurement effect was classified and candidate admission remained closed. It does not mean candidate promotion.

## 13. Distribution and temporal SSOT split

The parent full-authority distribution and temporal fields remain separate:

```text
kernel_distribution_drift
guarded_distribution_drift
kernel_temporal_persistence
guarded_temporal_persistence
```

Probe/Shadow evidence may validate or invalidate localization, but may not rewrite the full-authority temporal verdict.

## 14. Admission

```text
parent generation=14
open generation=15
terminal generation=16
```

Open state:

```text
EligibleForProbeShadowInterferenceOnly
```

Terminal HOLD states:

```text
LocalizationValiditySealedHold
DiagnosticInterferenceConfirmedHold
MixedInterferenceAndIntrinsicDriftHold
ControlKvInstabilitySealedHold
TargetDriftNotReproducedInShadowHold
PartialLocalizationValiditySealedHold
LocalizationValidityInconclusiveHold
```

Every state rejects new candidate leases and leaves the global route unchanged.

## 15. Exact fallback

After terminal closure:

```text
one 128-step fallback session
candidate dispatches=0
fallback dispatches=128
payload readback=0
same-session fallback=0
cross-route KV reuse=0
```

## 16. CLI contract

```text
29 exact-value keys
56 Boolean keys
85 new keys
```

The explicit registry is authoritative.

## 17. Negative controls

Thirty groups, ten controls each:

```text
parent HOLD identity
parent topology evidence
threshold identity
full population
Probe population
Shadow population
pair identity
pair order
production identity
Shadow zero-diagnostic
Probe pass accounting
exposure classes
exposure populations
intervening-work LUT
queue-state records
observable queue equivalence
Shadow Reference authority
common q99 boundary
paired duration test
paired tail test
familywise alpha
control stability
target reproduction
localization validity
distribution authority
temporal authority
terminal precedence
observer/device/thermal authority
raw evidence retention
admission/fallback/atlas integrity
```

```text
new controls=300
sealed R5 authority=940
combined expected=1240
```

## 18. PASS

PASS requires:

```text
parent R1-R1 HOLD exact
88/88 sessions
85504/85504 candidate steps and compact tokens
8/8 exact pairs
Probe-first=4
Shadow-first=4
Probe diagnostic passes=124928
Shadow diagnostic passes=0
production query batches=360
diagnostic query batches=1952
32768 queue-state records
32 Shadow Reference cells
24 paired units
ConflictingEvidence=0
Underpowered=0
both controls classified
both targets classified
overall validity != LocalizationValidityInconclusive
payload readback=0
fallback exact
default route unchanged
auto re-entry=0
1240/1240 negative controls
all artifacts and atlas digests exact
```

## 19. Verdicts

Success:

```text
PROMOTE_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_R5_R1_R2_PAIRED_NO_PROBE_SHADOW_QUEUE_STATE_EQUIVALENCE_DIAGNOSTIC_INTERFERENCE_CONTROL_STABILITY_AND_LOCALIZATION_VALIDITY_SEALED
```

Default HOLD:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_R5_R1_R2_PROBE_SHADOW_INTERFERENCE_CONTROL_STABILITY_OR_LOCALIZATION_VALIDITY_NOT_PROVEN
```

## 20. Final seal

```text
preserved R1-R1 HOLD
+ actual 72-session parent rerun
+ eight interleaved Probe sessions
+ eight production-identical no-probe Shadow sessions
+ same-step pairing
+ counterbalanced pair order
+ exact diagnostic-work accounting
+ common Shadow-derived q99 ruler
+ exact paired sign test
+ exact paired McNemar test
+ control KV 256/768 stability
+ target KV 384/512 shadow reproduction
+ probe-independent localization validity
+ zero threshold relaxation
+ zero tail filtering
+ terminal candidate hold
= proof of whether the measuring instrument observed the tail or helped create it
```
