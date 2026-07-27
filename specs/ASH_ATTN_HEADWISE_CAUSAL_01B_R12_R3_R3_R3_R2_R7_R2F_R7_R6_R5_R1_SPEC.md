# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6-R5-R1

## Matched-Phase Quantile Baseline / Exact Order-Statistic Confidence / Persistence-Aware Drift Authority / Tail Exceedance-Rate Accounting / Zero Threshold Relaxation Seal

## 0. State

```text
PARENT=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6-R5
PARENT_VERDICT=HOLD
RUN_SCOPE=matched-phase-quantile-confidence-live-canary-soak
DEFAULT_VERDICT=HOLD
ACTIVE_ROUTE=existing-production-headwise-reference-v1
CANDIDATE_ROUTE=gqa4-cluster-production-canary-v1
REFERENCE_POLICY=role-separated-matched-phase-reference-bank-v1
PHASE_POLICY=four-quartile-within-session-phase-v1
QUANTILE_POLICY=exact-nonparametric-order-statistic-v1
CONFIDENCE_POLICY=familywise-one-sided-exact-v1
PERSISTENCE_POLICY=confidence-backed-window-persistence-v1
TAIL_RATE_POLICY=exact-binomial-exceedance-accounting-v1
THRESHOLD_POLICY=r6-thresholds-immutable-v1
RAW_SAMPLE_POLICY=retain-all-zero-filtering-v1
ARTIFACT_LAYOUT=atlas-parallel-group-map-v1
```

R6-R5-R1 preserves the exact R6-R5 HOLD. It replaces the underpowered 160-sample point-quantile reference and every-window conjunction with role-separated matched-phase confidence authority. It does not change any latency ratio threshold.

## 1. Parent authority

Required parent truth:

```text
parent pass=false
parent verdict=HOLD_..._R7_R6_R5_OBSERVER_BASELINE_DRIFT_AUTHORITY_OR_TAIL_ATTRIBUTION_NOT_PROVEN
sessions=40/40
candidate steps=26880/26880
tokens=26880/26880
windows=101/101
baseline construction=true
baseline adjudicated=0
observer contamination=false
thermal proxy=true
bucket kernel drift=true
bucket guarded drift=true
kernel drift=false
guarded drift=false
final admission=CombinedDriftHold
route generation=10
negative controls=1120/1140
active global route unchanged
```

The parent HOLD remains immutable historical evidence.

## 2. Threshold immutability

Canonical table:

| Surface | Quantile | Ratio |
|---|---:|---:|
| kernel | q50 | 1.15 |
| kernel | q95 | 1.25 |
| kernel | q99 | 1.40 |
| guarded | q50 | 1.15 |
| guarded | q95 | 1.25 |
| guarded | q99 | 1.40 |

The gate hashes this table and rejects any CLI mutation before candidate execution.

Forbidden:

```text
threshold increase
confidence alpha expansion after observing data
sample deletion
outlier filtering
winsorization
tail clipping
reference/evaluation overlap
role reassignment
phase reassignment
failed-window replacement
selective rerun
baseline reconstruction
inconclusive-as-pass
automatic candidate re-entry
global default promotion
```

## 3. Role-separated cohort

Warmup:

```text
8 sessions
1024 steps
```

Measured roles:

```text
Reference: 32 sessions / 25856 steps
Evaluation: 32 sessions / 25856 steps
```

Full population:

```text
total sessions=72
total candidate steps=52736
total compact tokens=52736
```

Each role executes the complete matrix:

```text
8 KV buckets × profiles 32,128,1024,2048 = 32 sessions
```

Reference and Evaluation have distinct session IDs, leases, KV ownership, health latches, scratch ownership, and token-sequence domains.

## 4. Counterbalanced execution

For each `KV × profile` cell:

```text
parity=(KV index + profile index) mod 2
parity 0: Reference then Evaluation
parity 1: Evaluation then Reference
```

Required:

```text
reference-first cells=16
evaluation-first cells=16
role-order imbalance=0
```

Role ownership is fixed before the first GPU submission and cannot be changed by execution order.

## 5. Matched phases

Each measured session is divided by session-relative step:

```text
phase=floor(session_step × 4 / session_steps)
phase ∈ {0,1,2,3}
```

Samples per phase, per KV, per role:

```text
32 profile: 8
128 profile: 32
1024 profile: 256
2048 profile: 512
total=808
```

Required:

```text
64 role×KV×phase cells
808 samples in every cell
```

## 6. Exact order-statistic reference bank

For each reference `surface × KV × phase` cell:

```text
n=808
surfaces=kernel, guarded
quantiles=q50,q95,q99
```

Samples are sorted deterministically by:

```text
duration ns
token sequence
session ID
session step
```

The gate emits point, lower, and upper integer order indices. Final indices are selected from the exact discrete `Binomial(n,q)` distribution. Normal approximation, interpolated pseudo-observations, and bootstrap-only authority are forbidden.

Familywise authority:

```text
family size=48
family alpha=0.05
alpha unit=0.05/48 or stricter
```

Every reference cell records requested and achieved coverage, selected indices, quantile values, and sorted-identity digest.

## 7. Sample-specific matched boundaries

Each Evaluation sample matches only:

```text
same surface
same KV bucket
same relative phase
```

For quantile `q`:

```text
boundary(q)=immutable ratio threshold(q) × reference exact lower-confidence quantile(q)
```

The lower reference confidence bound is intentionally conservative. A weak reference bank cannot create a generous threshold.

Per sample, retain:

```text
raw duration
matched reference digest
q50/q95/q99 boundaries
q50/q95/q99 exceedance indicators
role, KV, phase, profile, session, step, token sequence
```

## 8. Exact exceedance-rate authority

Canonical exceedance budgets:

```text
q50=0.50
q95=0.05
q99=0.01
```

These are quantile definitions, not replacement latency thresholds.

For each authoritative unit:

```text
KV × surface × quantile
4 phases pooled with identity retained
n=3232
```

Compute exact one-sided Clopper-Pearson bounds by discrete binomial inversion.

Unit state:

```text
Noninferior:
upper confidence bound <= budget

Drift:
lower confidence bound > budget

Inconclusive:
otherwise
```

Promotion requires:

```text
48/48 Noninferior
Drift=0
Inconclusive=0
```

Inconclusive always remains HOLD.

## 9. Evaluation persistence windows

Only Evaluation samples form drift windows:

```text
25856 samples
256 samples per window
101 windows
```

Reference samples are never used as evaluation evidence.

For each window, surface, and quantile, emit:

```text
exceedance count
point rate
exact lower and upper confidence bounds
state=Clear | Warning | ConfidenceBackedDrift
```

Definitions:

```text
Clear: upper bound <= budget
ConfidenceBackedDrift: lower bound > budget
Warning: otherwise
```

Warning is retained and is not silently converted to PASS or Drift.

## 10. Persistence rules

### q50

Persistent when any holds:

```text
3 consecutive ConfidenceBackedDrift windows
5 drift windows in a rolling 16-window span
authoritative KV q50 unit=Drift
```

### q95

Persistent when any holds:

```text
2 consecutive ConfidenceBackedDrift windows
3 drift windows in a rolling 8-window span
authoritative KV q95 unit=Drift
```

### q99

Persistent when any holds:

```text
2 of 3 consecutive windows are ConfidenceBackedDrift
3 drift windows in a rolling 8-window span
same KV×phase fails in two distinct profiles
authoritative KV q99 unit=Drift
```

A single p99 spike remains evidence but cannot alone prove persistent drift.

## 11. Profile and late-region persistence

Profile identity remains attached to every sample.

Profile persistence:

```text
same KV × phase × surface × quantile
ConfidenceBackedDrift in at least two distinct profiles
```

Evaluation windows are split:

```text
early 0..33
middle 34..67
late 68..100
```

Late concentration:

```text
late drift rate >=2 × early drift rate
and late drift-window count >=3
```

Kernel and Guarded persistence are separate SSOTs.

## 12. Observer authority

R6-R5 deferred observer topology is rerun, not merely inherited.

Expected healthy counts:

```text
warmup batches=8
Reference measured batches=112
Evaluation measured batches=112
total query batches=232
session-end drains=72
normal boundary waits=0
ring exhaustion=0
early slot reuse=0
observer operations inside timed spans=0
```

The readback ring remains four-slot, with minimum deferred distance two.

## 13. Thermal authority

Reference and Evaluation streams each independently retain:

```text
late median ratio <=1.10
late p95 ratio <=1.20
Theil-Sen normalized slope <=0.002 per window
long-KV late/early median <=1.15
thermal sensor observed=false
```

No Celsius claim is permitted. Thermal PASS does not replace quantile PASS.

## 14. Token sequence authority

Separate domains:

```text
Warmup: 0..1023
Reference: 0..25855
Evaluation: 0..25855
Fallback: independent
```

Each domain requires:

```text
missing=0
duplicate=0
regression=0
wrap=0
session-step errors=0
token-integrity failures=0
```

## 15. Admission CAS

Parent state:

```text
CombinedDriftHold
generation=10
```

Open transition:

```text
BeginMatchedPhaseConfidenceCohort
CombinedDriftHold
-> EligibleForMatchedPhaseConfidenceSoakOnly
generation 10 -> 11
```

Successful terminal transition:

```text
EligibleForMatchedPhaseConfidenceSoakOnly
-> MatchedPhaseConfidenceSoakCompleteHold
generation 11 -> 12
```

PASS still closes candidate admission. Global default remains exact fallback.

Failure states:

```text
ReferenceBankInvalidHold
QuantileConfidenceInconclusiveHold
KernelPersistentDriftHold
GuardedPersistentDriftHold
CombinedPersistentDriftHold
ObserverAuthorityHold
DeviceQuarantined
```

## 16. Exact post-hold fallback

After any terminal state, execute one 128-step exact fallback session.

Required:

```text
candidate dispatcher calls=0
fallback dispatches=128
payload readback=0
per-step host wait=0
new lease and KV owner
same-session fallback=0
cross-route KV reuse=0
active global route unchanged
```

## 17. Evidence retention

Required retained evidence:

```text
all 52736 compact tokens
all Reference and Evaluation raw timestamps
all role and phase assignments
all sorted reference identities
all exact order indices and coverage
all sample-specific boundaries
all exceedance indicators
all window confidence states
all profile and late-region scans
all admission transitions
```

No sample, warning, drift window, or isolated spike may be removed.

## 18. Runtime artifacts

Required outputs include:

```text
*_parent_binding.json
*_threshold_identity.json
*_role_assignment.json
*_phase_assignment.json
*_reference_sessions.json
*_evaluation_sessions.json
*_reference_token_ledger.json
*_evaluation_token_ledger.json
*_reference_raw_timestamps.json
*_evaluation_raw_timestamps.json
*_matched_phase_reference_bank.json
*_order_statistic_indices.json
*_sample_specific_boundaries.json
*_kv_quantile_authority.json
*_window_exceedance_rates.json
*_kernel_persistence.json
*_guarded_persistence.json
*_observer.json
*_thermal.json
*_admission_hold_receipt.json
*_fallback_receipt.json
*_negative_control_outcomes.json
*_static_checks.json
*_runtime_artifact.json
*_local_manifest.json
*_canonical_args.txt
*_canonical_run.cmd
```

Runtime root uses `atlas-parallel-group-map-v1` with independent group digests.

## 19. CLI contract

R6-R5-R1 adds:

```text
24 exact-value keys
48 Boolean keys
72 required CLI keys
```

The additional Boolean `require-gqa4-r2f-r6-r5-r1-role-specific-sequence-domains` explicitly seals the separate Warmup, Reference, and Evaluation token ledgers.

## 20. Negative controls

Twenty-four groups, ten controls each:

```text
parent HOLD identity
threshold identity
role predeclaration
role disjointness
role-order counterbalance
phase identity
phase population
reference-bank digest
evaluation-bank digest
order-statistic indices
order-statistic coverage
exact binomial confidence
familywise alpha
three-state verdict
sample-specific boundaries
tail exceedance accounting
kernel persistence
guarded persistence
profile persistence
late-region persistence
observer ring
thermal/device authority
raw evidence retention
admission/fallback/atlas integrity
```

```text
R6-R5-R1 new controls=240
sealed R5 authority=940
combined expected=1180
```

Parent failed aggregate controls remain historical evidence and are not counted as passed.

## 21. PASS

PASS requires:

```text
parent R6-R5 HOLD exact
threshold digest exact
generation 10->11 CAS
72/72 sessions
52736/52736 candidate steps and compact tokens
32/32 Reference sessions
32/32 Evaluation sessions
16/16 counterbalanced cell order
64/64 role×KV×phase cells
808/808 samples per cell
Reference and Evaluation ledgers exact
exact order-statistic coverage complete
48/48 authoritative units Noninferior
0 Drift units
0 Inconclusive units
kernel persistent drift=false
guarded persistent drift=false
profile persistence=false
late concentration=false
232/232 observer batches
72/72 session-end drains
boundary waits=0
ring exhaustion=0
thermal authority pass
payload readback=0
per-step host wait=0
generation 11->12 terminal CAS
final admission=MatchedPhaseConfidenceSoakCompleteHold
fallback exact
active global route unchanged
1180/1180 negative controls
all artifacts and atlas digests exact
```

## 22. HOLD

HOLD on any parent, role, phase, confidence, persistence, observer, thermal, token, route, fallback, negative-control, or artifact mismatch.

Any authoritative unit in `Drift` or `Inconclusive` causes HOLD. Any persistent kernel or guarded drift causes HOLD. No automatic re-entry is permitted.

## 23. Verdicts

Success:

```text
PROMOTE_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_R5_R1_MATCHED_PHASE_QUANTILE_BASELINE_EXACT_ORDER_STATISTIC_CONFIDENCE_PERSISTENCE_AWARE_DRIFT_AND_TAIL_EXCEEDANCE_RATE_SEALED
```

Default HOLD:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_R5_R1_MATCHED_PHASE_REFERENCE_CONFIDENCE_PERSISTENCE_OR_TAIL_RATE_NOT_PROVEN
```

## 24. Final seal

```text
preserved R6-R5 HOLD
+ immutable Reference/Evaluation roles
+ counterbalanced execution
+ exact four-phase matching
+ 808 samples per KV-phase-role cell
+ exact discrete order-statistic confidence
+ exact binomial exceedance authority
+ Noninferior/Drift/Inconclusive verdicts
+ confidence-backed persistence
+ profile and late-region accounting
+ zero threshold relaxation
+ zero tail filtering
+ terminal admission hold
= a quantile ruler with enough marks to separate sparse spikes from persistent latency drift
```
