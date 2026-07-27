# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6-R5

## Timestamp Observer Decontamination / Deferred Readback Ring / Baseline Non-Adjudication / Kernel·Guarded Independent Drift Authority / Tail-Spike Attribution Seal

## 0. State

```text
PARENT=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6
PARENT_VERDICT=HOLD
RUN_SCOPE=timestamp-observer-decontaminated-live-canary-soak
DEFAULT_VERDICT=HOLD
ACTIVE_ROUTE=existing-production-headwise-reference-v1
CANDIDATE_ROUTE=gqa4-cluster-production-canary-v1
OBSERVER_POLICY=deferred-readback-ring-noninterfering-v1
BASELINE_POLICY=construction-only-non-adjudicated-v1
KERNEL_DRIFT_AUTHORITY=independent-post-baseline-v1
GUARDED_DRIFT_AUTHORITY=independent-post-baseline-v1
TAIL_ATTRIBUTION=boundary-distance-stage-bucket-exact-v1
RAW_SAMPLE_POLICY=retain-all-zero-filtering-v1
ARTIFACT_LAYOUT=atlas-parallel-group-map-v1
```

R6-R5 preserves the R6 HOLD as immutable parent evidence. It repairs the observer topology and authority partition, then reruns the complete candidate cohort. It does not weaken thresholds, remove tail samples, selectively rerun failed windows, or promote the candidate route globally.

## 1. Parent HOLD authority

Required parent truth:

```text
parent pass=false
parent verdict=HOLD_..._R7_R6_SOAK_CONTINUITY_DRIFT_DEVICE_HEALTH_OR_ADMISSION_HOLD_NOT_PROVEN
sessions=40/40
candidate steps=26880/26880
tokens=26880/26880
token continuity=true
windows=101/101
latency drift=false
thermal proxy=true
device faults=0
payload readback=0
final admission=AdmissionHeldByDrift
route generation=8
negative controls=1100/1120
active global route unchanged
```

The parent HOLD must not be reinterpreted or overwritten. R6-R5 starts a new revision-owned repair cohort.

## 2. Repair cohort CAS

Canonical transition:

```text
BeginObserverDecontaminatedCohort
AdmissionHeldByDrift
-> EligibleForObserverDecontaminatedSoakOnly
expected generation=8
committed generation=9
automatic re-entry=0
active global route unchanged
```

A successful run closes through:

```text
EligibleForObserverDecontaminatedSoakOnly
-> ObserverDecontaminatedSoakCompleteHold
expected generation=9
committed generation=10
```

PASS does not leave candidate admission open.

## 3. Non-negotiable repair rules

Forbidden:

```text
threshold relaxation
baseline population reduction
measured population reduction
p95 or p99 removal
outlier filtering
winsorization
tail clipping
boundary sample deletion
failed-window deletion
selective rerun
sample replacement
baseline reconstruction
automatic candidate re-entry
global-default promotion
```

Required repair principle:

```text
repair observer topology
separate statistical authorities
retain every raw observation
rerun the complete cohort
```

## 4. Authority SSOTs

R6-R5 introduces independent authorities:

```text
TimestampObserverAuthority
DeferredReadbackRingAuthority
BaselineConstructionAuthority
KernelDriftAuthority
GuardedDriftAuthority
TailSpikeAttributionAuthority
```

No single aggregate Boolean may stand in for both kernel and guarded drift.

## 5. Full cohort population

KV buckets:

```text
128,256,384,512,768,1024,1536,2048
```

Population:

```text
warmup sessions=8
measured sessions=32
total sessions=40
warmup steps=1024
measured steps=25856
total candidate steps=26880
compact tokens=26880
```

Session profiles per KV bucket:

```text
warmup 128
measured 32
measured 128
measured 1024
measured 2048
```

Mirrored execution schedule remains identical to R6.

## 6. Production-shaped payload path

Every candidate step executes:

```text
output poison
GQA4 candidate attention
fault-injection identity stage
eight-group guard map
guard finalizer
compact health-token finalizer
device-native downstream gate
token publication
GPU timestamp recording
```

Required per step:

```text
one candidate command encoder
one candidate submission
one route-sticky session lease
one route generation
one device generation
one KV generation
one compact token
four GPU timestamps
```

Payload readback and per-step host wait remain zero.

## 7. Deferred readback ring

Canonical topology:

```text
readback ring capacity=4
resolve ring capacity=4
query batch maximum=256 payload steps
minimum deferred batch distance=2
```

Each session owns four query-set/resolve-buffer slots. Query batches are assigned by:

```text
slot index=batch index mod 4
slot generation=floor(batch index / 4)
```

Every batch resolves and copies into a unique session aggregate readback range. Mapping and host wait occur once at session end, not at each 256-step boundary.

Required healthy cohort counts:

```text
observer query batches=120
session-end timestamp waits=40
normal batch-boundary waits=0
ring-exhaustion waits=0
early slot reuse=0
```

The 120 query batches and 101 statistical windows are different domains. Session boundaries create partial 32-step and 128-step query batches, while statistical windows are formed over the complete 25856-sample measured stream.

## 8. Ring state contract

Conceptual states:

```text
Free -> Recording -> Submitted -> Resolved -> Copied -> SessionAggregate -> Consumed -> Free
```

Forbidden:

```text
slot overwrite before ordered resolve/copy
aggregate range overlap
map during candidate timed span
host wait at normal batch boundary
ring exhaustion accepted as healthy
```

GPU queue ordering must preserve resolve/copy before later writes to the reused query slot.

## 9. Observer exclusion from timed surfaces

Kernel timestamp surface:

```text
candidate attention dispatch only
```

Guarded timestamp surface:

```text
candidate attention through token publication
```

Observer operations outside both timed surfaces:

```text
query resolve
resolve-buffer copy
aggregate-buffer map
host poll or wait
CPU timestamp decoding
window aggregation
artifact serialization
```

Required counters:

```text
observer resolve inside timed span=0
observer copy inside timed span=0
observer map inside timed span=0
observer wait inside timed span=0
```

## 10. Token continuity

Global sequence:

```text
first=0
last=26879
expected=26880
published=26880
drained=26880
missing=0
duplicate=0
regression=0
wrap=0
```

Each session-local decode sequence must start at zero and end at `requested_steps-1`, with no missing, duplicate, or regressing step.

Snapshot ranges remain contiguous and non-overlapping.

## 11. Statistical windows

Warmup timestamps are retained but excluded from drift authority.

Measured population:

```text
25856 samples
256 samples per statistical window
101 exact windows
```

Every window retains:

```text
absolute kernel min, median, p95, p99, max, MAD
absolute guarded min, median, p95, p99, max, MAD
normalized kernel median, p95, p99 ratios
normalized guarded median, p95, p99 ratios
session composition
KV composition
first and last token sequence
```

## 12. KV-conditioned normalization

Each KV bucket uses its first 160 measured samples as the bucket baseline:

```text
32-step session + 128-step session
```

Every sample retains both:

```text
absolute GPU nanoseconds
KV-conditioned normalized ratio
```

Normalization may not replace or delete the absolute timestamp.

## 13. Baseline construction authority

Global baseline windows:

```text
indices 0..15
count=16
```

Baseline windows are checked for:

```text
exact 256-sample population
token continuity
finite positive timestamps
healthy compact tokens
exact route/device/KV generation
```

Baseline windows are not adjudicated as drift windows.

Required fields for baseline windows:

```text
baseline_member=true
drift_adjudication_eligible=false
kernel_window_pass=null
guarded_window_pass=null
```

Required receipt:

```text
baseline construction pass=true
valid windows=16
baseline drift adjudication count=0
baseline reconstruction count=0
```

Diagnostic ratios may be emitted for baseline windows but have no promotion authority.

## 14. Post-baseline scope

Only windows `16..100` are drift-adjudicated.

```text
post-baseline window count=85
```

Forbidden implementation pattern:

```rust
windows.iter().all(|window| window.pass)
```

when the iterator includes baseline windows.

Required partition:

```text
baseline_construction_pass
kernel_post_baseline_drift_pass
guarded_post_baseline_drift_pass
```

## 15. Independent kernel drift authority

Thresholds are unchanged from R6:

```text
kernel median ratio <=1.15
kernel p95 ratio <=1.25
kernel p99 ratio <=1.40
```

Consecutive limits:

```text
fewer than 3 consecutive median failures
fewer than 2 consecutive p95 failures
```

Bucket-conditioned limits:

```text
later median / bucket baseline median <=1.20
later p95 / bucket baseline p95 <=1.30
```

Receipt fields include independent median, p95, p99, consecutive, and bucket failure counts.

## 16. Independent guarded drift authority

Thresholds are unchanged from R6:

```text
guarded median ratio <=1.15
guarded p95 ratio <=1.25
guarded p99 ratio <=1.40
```

The same consecutive and bucket-conditioned limits apply independently.

Kernel and guarded drift receipts must use different Boolean verdict fields and different failure counters.

## 17. Combined latency authority

```text
latency_drift_pass =
    baseline_construction_pass
    AND kernel_drift_pass
    AND guarded_drift_pass
    AND kernel_bucket_conditioned_pass
    AND guarded_bucket_conditioned_pass
    AND observer_decontamination_pass
```

Thermal plateau remains separate:

```text
performance_stability_pass = latency_drift_pass AND thermal_proxy_pass
```

## 18. Thermal proxy

R6 thresholds remain unchanged:

```text
thermal sensor observed=false
late windows=16
late median ratio <=1.10
late p95 ratio <=1.20
normalized Theil-Sen slope <=0.002 per window
long-KV plateau <=1.15 for KV 1024,1536,2048
```

No Celsius-temperature claim is permitted.

## 19. Tail classification

Every measured sample is classified independently for kernel and guarded surfaces:

```text
NonTail
P95Tail
P99Tail
ExtremeTail
```

Definitions:

```text
P95Tail: duration >= its statistical-window p95
P99Tail: duration >= its statistical-window p99
ExtremeTail: normalized ratio >=1.60
```

Classification is descriptive. No classified sample may be removed.

## 20. Tail stage attribution

Each tail sample is assigned one stage class:

```text
kernel-only
guarded-only
shared-kernel-guarded
```

Interpretation:

```text
kernel-only: candidate attention path candidate
guarded-only: guard/finalizer/downstream/publication candidate
shared: queue, device, session, or observer-boundary candidate
```

Required counts include kernel-only, guarded-only, and shared p95/p99 populations.

## 21. Tail boundary attribution

Every tail record retains:

```text
global token sequence
session ID
session step
KV bucket
statistical-window index
query-batch index
query-batch step index
readback slot index
readback slot generation
observer-boundary distance
host-wait boundary distance
session-boundary distance
bucket-transition distance
kernel duration
guarded duration
kernel class
guarded class
stage class
```

Canonical observer bands:

```text
near: distance <=3
far: distance >=16
```

Required counts and rates:

```text
near population
far population
near tail count
far tail count
near tail rate
far tail rate
relative risk
```

## 22. Observer contamination probe

Observer contamination is reported when:

```text
near tail count >=8
AND near/far relative risk >=2.0
```

This classification does not delete samples and does not alter any latency threshold.

If the far-tail rate is zero, the artifact emits a finite fail-closed relative-risk sentinel greater than the configured limit. JSON infinity is forbidden.

## 23. Window receipt semantics

Baseline windows:

```text
pass=baseline_valid
kernel_window_pass=null
guarded_window_pass=null
```

Post-baseline windows:

```text
kernel_window_pass=kernel median/p95/p99 conjunction
guarded_window_pass=guarded median/p95/p99 conjunction
pass=kernel_window_pass AND guarded_window_pass
```

Each window also publishes observer-near, observer-far, session-boundary, and bucket-transition tail counts.

## 24. Terminal admission states

Successful run:

```text
ObserverDecontaminatedSoakCompleteHold
```

Observer topology or attribution failure:

```text
ObserverContaminationHold
```

Independent performance failures:

```text
KernelDriftHold
GuardedDriftHold
CombinedDriftHold
```

Hard device failure:

```text
DeviceQuarantined
```

Every terminal state rejects new candidate leases and preserves exact fallback binding for new sessions.

## 25. Post-hold fallback

R6-R5 executes an exact 128-step fallback session after terminal admission closure.

Required:

```text
candidate dispatcher calls=0
fallback dispatches=128
new session lease
new KV ownership
same-session fallback=0
cross-route KV reuse=0
active global route unchanged
```

## 26. Fault rehearsals

Isolated rehearsals:

```text
baseline self-adjudication
readback-slot early reuse
ring exhaustion wait
map inside timed span
host wait inside timed span
kernel-only drift
guarded-only drift
shared drift
tail boundary cluster
raw-sample removal
selective window rerun
baseline reconstruction
```

Each rehearsal uses an isolated authority domain and must leave the live cohort unchanged.

## 27. Raw evidence retention

Required retained evidence:

```text
all compact tokens
all raw timestamp values
all normalized ratios
all baseline inputs
all statistical-window assignments
all query-batch assignments
all ring slot generations
all tail classifications
all admission transitions
```

Forbidden:

```text
sample deletion
window deletion
tail clipping
outlier filtering
sample substitution
window substitution
baseline reconstruction
selective rerun
```

## 28. Runtime artifacts

Required outputs:

```text
*_parent_binding.json
*_observer_authority.json
*_deferred_readback_ring_receipt.json
*_soak_sessions.json
*_token_sequence_ledger.json
*_timestamp_raw_samples.json
*_timestamp_batch_receipts.json
*_baseline_construction_receipt.json
*_latency_windows.json
*_kernel_drift_receipt.json
*_guarded_drift_receipt.json
*_bucket_conditioned_drift.json
*_tail_spike_attribution.json
*_observer_boundary_attribution.json
*_thermal_plateau_proxy.json
*_admission_hold_receipt.json
*_fallback_session_receipt.json
*_fault_rehearsal_receipts.json
*_negative_control_outcomes.json
*_static_checks.json
*_runtime_artifact.json
*_local_manifest.json
*_canonical_run.cmd
*_canonical_args.txt
```

## 29. Atlas groups

```text
identity
parent_binding
observer_topology
readback_ring
soak_population
token_continuity
timestamp_batches
baseline_construction
kernel_drift
guarded_drift
bucket_drift
tail_attribution
observer_attribution
thermal_plateau
admission_hold
fallback_activation
fault_rehearsals
negative_controls
verdict
```

Each group has an independent field count and SHA-256 digest. The root records ordered group digests and the atlas digest.

## 30. Static truth

Static extraction must prove:

```text
one observer aggregate authority
four-slot ring
minimum deferred distance two
session aggregate timestamp readback
zero batch-boundary wait
baseline non-adjudication
post-baseline scope split
independent kernel verdict
independent guarded verdict
no shared kernel/guarded aggregate signal
tail stage and boundary attribution
raw timestamp retention
threshold immutability
repair cohort CAS
terminal complete hold
payload readback zero
atlas layout
65-key CLI extension
```

## 31. CLI exact-value contract

```text
--gqa4-r2f-r6-r5-observer-policy deferred-readback-ring-noninterfering-v1
--gqa4-r2f-r6-r5-baseline-policy construction-only-non-adjudicated-v1
--gqa4-r2f-r6-r5-kernel-drift-authority independent-post-baseline-v1
--gqa4-r2f-r6-r5-guarded-drift-authority independent-post-baseline-v1
--gqa4-r2f-r6-r5-tail-attribution-policy boundary-distance-stage-bucket-exact-v1
--gqa4-r2f-r6-r5-readback-ring-capacity 4
--gqa4-r2f-r6-r5-resolve-ring-capacity 4
--gqa4-r2f-r6-r5-minimum-deferred-batch-distance 2
--gqa4-r2f-r6-r5-query-batch-steps 256
--gqa4-r2f-r6-r5-baseline-window-count 16
--gqa4-r2f-r6-r5-observer-near-distance 3
--gqa4-r2f-r6-r5-observer-far-distance 16
--gqa4-r2f-r6-r5-tail-enrichment-ratio 2.0
--gqa4-r2f-r6-r5-tail-enrichment-minimum-count 8
--gqa4-r2f-r6-r5-kernel-median-drift-ratio 1.15
--gqa4-r2f-r6-r5-kernel-p95-drift-ratio 1.25
--gqa4-r2f-r6-r5-kernel-p99-drift-ratio 1.40
--gqa4-r2f-r6-r5-guarded-median-drift-ratio 1.15
--gqa4-r2f-r6-r5-guarded-p95-drift-ratio 1.25
--gqa4-r2f-r6-r5-guarded-p99-drift-ratio 1.40
--gqa4-r2f-r6-r5-raw-sample-policy retain-all-zero-filtering-v1
--gqa4-r2f-r6-r5-final-admission-state observer-decontaminated-soak-complete-hold-v1
```

Exactly 22 exact-value keys are added.

## 32. CLI Boolean contract

Required true:

```text
--require-gqa4-r2f-r6-r5-parent-r6-hold
--require-gqa4-r2f-r6-r5-parent-evidence-exact
--require-gqa4-r2f-r6-r5-explicit-repair-cohort-cas
--require-gqa4-r2f-r6-r5-deferred-readback-ring
--require-gqa4-r2f-r6-r5-readback-slot-generation
--require-gqa4-r2f-r6-r5-zero-early-slot-reuse
--require-gqa4-r2f-r6-r5-zero-ring-exhaustion
--require-gqa4-r2f-r6-r5-zero-normal-batch-boundary-wait
--require-gqa4-r2f-r6-r5-zero-map-inside-timed-span
--require-gqa4-r2f-r6-r5-zero-copy-inside-timed-span
--require-gqa4-r2f-r6-r5-zero-resolve-inside-timed-span
--require-gqa4-r2f-r6-r5-baseline-construction-valid
--require-gqa4-r2f-r6-r5-baseline-non-adjudicated
--require-gqa4-r2f-r6-r5-baseline-frozen
--require-gqa4-r2f-r6-r5-kernel-drift-independent
--require-gqa4-r2f-r6-r5-guarded-drift-independent
--require-gqa4-r2f-r6-r5-kernel-post-baseline-only
--require-gqa4-r2f-r6-r5-guarded-post-baseline-only
--require-gqa4-r2f-r6-r5-tail-stage-attribution
--require-gqa4-r2f-r6-r5-tail-boundary-attribution
--require-gqa4-r2f-r6-r5-tail-bucket-attribution
--require-gqa4-r2f-r6-r5-tail-session-attribution
--require-gqa4-r2f-r6-r5-queue-reentry-attribution
--require-gqa4-r2f-r6-r5-observer-contamination-probe
--require-gqa4-r2f-r6-r5-raw-timestamp-retention
--require-gqa4-r2f-r6-r5-raw-token-retention
--require-gqa4-r2f-r6-r5-window-population-exact
--require-gqa4-r2f-r6-r5-token-continuity
--require-gqa4-r2f-r6-r5-payload-readback-zero
--require-gqa4-r2f-r6-r5-per-step-host-wait-zero
--require-gqa4-r2f-r6-r5-route-sticky
--require-gqa4-r2f-r6-r5-default-route-unchanged
--require-gqa4-r2f-r6-r5-independent-negative-controls
--require-gqa4-r2f-r6-r5-atlas-artifact-layout
--forbid-gqa4-r2f-r6-r5-threshold-relaxation
--forbid-gqa4-r2f-r6-r5-outlier-filtering
--forbid-gqa4-r2f-r6-r5-tail-sample-removal
--forbid-gqa4-r2f-r6-r5-selective-window-rerun
--forbid-gqa4-r2f-r6-r5-baseline-reconstruction
--forbid-gqa4-r2f-r6-r5-baseline-self-adjudication
--forbid-gqa4-r2f-r6-r5-shared-kernel-guarded-verdict
--forbid-gqa4-r2f-r6-r5-automatic-candidate-reentry
--forbid-gqa4-r2f-r6-r5-global-default-promotion
```

Exactly 43 Boolean keys are added. R6-R5 adds 65 CLI keys total.

## 33. Negative controls

R6-R5 executes 20 groups with 10 controls each:

```text
parent HOLD identity
repair cohort CAS
deferred ring state machine
deferred batch distance
early slot reuse rejection
ring exhaustion rejection
timed-span observer exclusion
baseline construction validity
baseline non-adjudication
baseline freeze
kernel independent authority
guarded independent authority
kernel post-baseline scope
guarded post-baseline scope
stage tail attribution
observer-boundary attribution
bucket tail attribution
raw evidence retention
threshold immutability
atlas and admission integrity
```

Promotion authority:

```text
sealed R5 authority=940
R6-R5 new controls=200
combined expected=1140
```

The failed R6 controls remain historical HOLD evidence and are not carried forward as passed controls.

## 34. PASS conditions

PASS requires:

```text
parent R6 HOLD exact
repair cohort generation 8->9 CAS
40/40 sessions
26880/26880 candidate steps
26880/26880 compact tokens
25856/25856 measured timestamps
101/101 statistical windows
120/120 observer query batches
40/40 session-end timestamp drains
zero normal batch-boundary wait
zero ring exhaustion
zero early slot reuse
zero observer operation inside timed spans
token continuity pass
baseline construction 16/16
baseline adjudication count=0
baseline reconstruction count=0
post-baseline windows=85
kernel independent drift pass
guarded independent drift pass
kernel bucket drift pass
guarded bucket drift pass
tail attribution complete
observer contamination absent
thermal proxy pass
payload readback=0
per-step host wait=0
terminal generation 9->10 CAS
final admission=ObserverDecontaminatedSoakCompleteHold
post-hold fallback exact
active global route unchanged
1140/1140 negative controls
all artifacts and atlas digests exact
```

## 35. HOLD conditions

HOLD on any of:

```text
parent mismatch
repair CAS mismatch
ring slot early reuse
ring exhaustion
normal batch-boundary blocking wait
observer operation inside timed span
baseline self-adjudication
baseline reconstruction
invalid baseline sample
kernel drift failure
guarded drift failure
bucket drift failure
observer contamination classification
missing tail attribution
missing raw timestamp
sample filtering
selective rerun
payload readback
automatic candidate re-entry
global route mutation
negative-control failure
artifact digest mismatch
```

## 36. Verdicts

Success:

```text
PROMOTE_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_R5_TIMESTAMP_OBSERVER_DECONTAMINATION_DEFERRED_READBACK_BASELINE_NONADJUDICATION_INDEPENDENT_DRIFT_AND_TAIL_ATTRIBUTION_SEALED
```

Default HOLD:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_R5_OBSERVER_BASELINE_DRIFT_AUTHORITY_OR_TAIL_ATTRIBUTION_NOT_PROVEN
```

## 37. Final seal

```text
preserved R6 HOLD
+ explicit repair-cohort CAS
+ complete 26880-step rerun
+ four-slot GPU query/resolve ring
+ 120 ordered query batches
+ 40 session-end aggregate drains
+ zero normal batch-boundary wait
+ baseline construction without self-adjudication
+ independent kernel drift authority
+ independent guarded drift authority
+ exact tail stage/session/KV/boundary attribution
+ zero threshold relaxation
+ zero raw-sample filtering
+ terminal candidate admission hold
= drift evidence that measures the candidate rather than the observer
```
