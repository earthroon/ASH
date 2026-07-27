# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6-R5-R1-R1

## Mid-KV Tail Topology / Page·Workgroup·Phase Attribution / Distribution Drift vs Temporal Persistence Split / Primary Terminal Reason Precedence / Exact Tail Source Localization Seal

## 0. State

```text
PARENT=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6-R5-R1
PARENT_VERDICT=HOLD
RUN_SCOPE=full-authority-rerun-plus-mid-kv-tail-localization
DEFAULT_VERDICT=HOLD
ACTIVE_ROUTE=existing-production-headwise-reference-v1
CANDIDATE_ROUTE=gqa4-cluster-production-canary-v1
FALLBACK_ROUTE=existing-production-headwise-reference-v1
DISTRIBUTION_POLICY=matched-phase-exact-quantile-distribution-v2
TEMPORAL_POLICY=window-profile-late-region-persistence-v2
TOPOLOGY_POLICY=predeclared-page-workgroup-decomposition-v1
LOCALIZATION_POLICY=exact-component-drift-and-tail-cooccurrence-v1
TERMINAL_REASON_POLICY=strongest-evidence-primary-plus-secondary-reasons-v1
THRESHOLD_POLICY=r6-thresholds-immutable-v1
RAW_SAMPLE_POLICY=retain-all-zero-filtering-v1
ARTIFACT_LAYOUT=atlas-parallel-group-map-v1
```

R6-R5-R1-R1 preserves the R6-R5-R1 HOLD, reruns its complete 72-session authority through the exact parent binary, and adds an isolated eight-session GPU topology cohort for KV 256, 384, 512, and 768.

Localization PASS seals the source topology. It does not repair the candidate, reopen candidate admission, or promote the candidate route globally.

### 0.1 CLI count reconciliation

The explicit CLI list contains:

```text
30 exact-value keys
53 Boolean keys
83 new keys total
```

The earlier `52 Boolean / 82 total` summary was an arithmetic mismatch. The explicit key list is authoritative, so this specification canonically seals 83 keys. No listed policy key is silently removed.

## 1. Parent authority

The revision requires a fresh child-process rerun of the exact R6-R5-R1 gate binary with the inherited R6-R5-R1 CLI subset.

Required parent result:

```text
parent process exits HOLD
parent schema exact
parent patch ID exact
parent verdict exact
sessions=72/72
candidate steps=52736/52736
compact tokens=52736/52736
authoritative units=48/48
Noninferior units=36
Drift units=2
Inconclusive units=10
final admission=QuantileConfidenceInconclusiveHold
generation=12
active global route unchanged
```

Exact parent Drift units:

```text
kernel / KV 384 / q99
kernel / KV 512 / q99
```

Parent temporal facts:

```text
q99 confidence-backed drift windows=1
q99 two-of-three=false
q99 rolling-eight maximum=1
profile persistence=false
late concentration=false
```

Canonical interpretation:

```text
kernel distribution drift=true
kernel temporal persistence=false
```

The parent HOLD artifact and parent rerun log remain retained evidence.

## 2. Authority separation

The following SSOTs remain independent:

```text
DistributionDriftAuthority
TemporalPersistenceAuthority
DispatchTopologyAuthority
PageTailAuthority
WorkgroupTailAuthority
PageWorkgroupInteractionAuthority
TailSourceLocalizationAuthority
TerminalReasonAuthority
ObserverAuthority
ThermalAuthority
DeviceAuthority
AdmissionAuthority
```

Forbidden collapse:

```text
temporal_persistence = distribution_drift
kernel_persistence = any_authoritative_kernel_unit_is_drift
```

## 3. Threshold immutability

The revision retains:

```text
kernel q99 ratio=1.40
q99 exceedance budget=0.01
localization family alpha=0.05
```

Forbidden:

```text
threshold relaxation
q99 budget relaxation
post-observation alpha expansion
tail filtering
winsorization
outlier deletion
selective rerun
post-hoc page merge
post-hoc workgroup remap
post-hoc probe-step selection
```

## 4. Full authority cohort

The complete R6-R5-R1 cohort is rerun by the exact parent binary:

```text
warmup sessions=8
Reference sessions=32
Evaluation sessions=32
full authority sessions=72
full authority candidate steps=52736
full authority compact tokens=52736
observer batches=232
session-end drains=72
```

This rerun remains the sole authority for:

```text
distribution Drift
quantile Inconclusive
temporal persistence
thermal stability
route identity
device identity
```

The diagnostic shader must not replace or modify the production candidate shader used by this rerun.

## 5. Diagnostic shader isolation

The production shader file and digest remain unchanged.

The topology cohort uses a separate WGSL source that copies the candidate attention computation body and adds uniform diagnostic selectors:

```text
diagnostic mode
selected logical page
selected workgroup band
```

Required isolation:

```text
separate diagnostic WGSL source
separate output scratch
separate timestamp query sets
separate resolve buffers
separate readback buffer
canonical output writes=0
health-latch writes=0
route-generation writes=0
KV-ownership mutation=0
payload readback=0
```

## 6. Topology cohort

Fixed KV set:

```text
targets=384,512
controls=256,768
```

Each KV runs:

```text
Reference role
Evaluation role
profile steps=2048
```

Population:

```text
topology sessions=8
topology candidate steps=16384
topology compact tokens=16384
```

Combined runtime population:

```text
total sessions=80
total candidate steps=69120
total compact tokens=69120
```

Role order alternates by KV index to prevent role-order confounding.

## 7. Page topology

Canonical page size:

```text
PAGE_TOKENS=128
```

| KV | Logical pages | Physical capacity |
|---:|---:|---:|
| 256 | 2 | 2 |
| 384 | 3 | 3 |
| 512 | 4 | 4 |
| 768 | 6 | 6 |

Every page record retains:

```text
logical page
physical slot
page-table generation
residency generation
first and last KV token
valid token count
role
phase
session step
```

Physical-slot alias within one residency generation is forbidden.

## 8. Workgroup topology

Canonical bands:

```text
8 workgroup bands
4 query heads per band
2 bands per KV head
subgroup size=32
```

For band `b`:

```text
query_head_first=b×4
query_head_last=b×4+3
kv_head_owner=floor(b/2)
```

Band grouping is fixed before execution.

## 9. Probe predicates

Page and workgroup probes:

```text
session_step mod 2 = 0
```

Cross probes for target KVs only:

```text
session_step mod 8 = 0
```

Observed tails may not change probe ordinals.

## 10. Diagnostic pass counts

Page passes:

```text
KV 256: 2 roles × 1024 steps × 2 pages = 4096
KV 384: 2 roles × 1024 steps × 3 pages = 6144
KV 512: 2 roles × 1024 steps × 4 pages = 8192
KV 768: 2 roles × 1024 steps × 6 pages = 12288
page total=30720
```

Workgroup passes:

```text
8 sessions × 1024 steps × 8 bands=65536
```

Cross passes:

```text
KV 384: 2 roles × 256 steps × 3 pages × 8 bands=12288
KV 512: 2 roles × 256 steps × 4 pages × 8 bands=16384
cross total=28672
```

Combined:

```text
total diagnostic passes=124928
```

## 11. Topology observer

Canonical observer:

```text
ring capacity=8
maximum 64 diagnostic passes per query batch
minimum deferred distance=2 batches
one final map/wait per topology session
```

Required:

```text
normal boundary waits=0
ring exhaustion=0
early slot reuse=0
map inside timed span=0
copy inside timed span=0
invalid timestamps=0
```

The implementation reuses query slots only through ordered GPU resolve and copy operations. Host waiting occurs only at session completion.

## 12. Topology full-step reproduction

Every topology session first executes the exact production-shaped candidate session.

The topology Reference role builds phase-matched q99 lower-confidence boundaries for each KV.

Evaluation samples are classified using:

```text
boundary=1.40 × exact Reference lower-confidence q99
budget=0.01
```

Per KV reproduction classes:

```text
ReproducedDrift
DirectionallyConsistentInconclusive
InconclusiveBelowBudget
NotReproduced
```

Localization eligibility requires:

```text
at least one target=ReproducedDrift
and the other target is ReproducedDrift or DirectionallyConsistentInconclusive
```

## 13. Component authority

Source units:

```text
page units=15
workgroup units=32
cross units=56
total source units=103
```

Familywise policy:

```text
alpha family=0.05
alpha unit=0.05/103 or stricter
```

Every component uses:

```text
exact Reference q99 order-statistic lower bound
fixed ratio 1.40
exact Evaluation exceedance count
exact one-sided Clopper-Pearson bounds
Noninferior / Drift / Inconclusive state
```

Point estimates alone cannot produce localization.

## 14. Tail co-occurrence

For each component:

```text
A=full tail and component exceedance
B=full tail and component non-exceedance
C=full non-tail and component exceedance
D=full non-tail and component non-exceedance
```

Required outputs:

```text
tail coverage=A/(A+B)
non-tail component rate=C/(C+D)
relative risk
conservative exact relative-risk lower bound
one-sided Fisher exact p-value
phase replication count
```

## 15. Localization candidate

A source unit is a candidate only if all hold:

```text
component state=Drift
Fisher p <= 0.05/103
tail coverage >=0.60
relative-risk lower bound >1.0
replication in at least two phases
```

No candidate criterion changes q99 ratio or q99 budget.

## 16. Localization classes

Canonical classes:

```text
PageLocalized
WorkgroupLocalized
PageWorkgroupInteractionLocalized
MultiCellLocalized
DiffuseKernelTail
InconclusiveLocalization
TailDriftNotReproduced
```

Cross localization takes precedence when a page × workgroup source passes the exact criteria.

`DiffuseKernelTail` requires:

```text
full-step Drift reproduced
no exact source candidate
exceedances spread across at least half of pages
exceedances spread across at least half of bands
no source tail coverage >=0.60
```

`InconclusiveLocalization` and `TailDriftNotReproduced` remain HOLD.

## 17. Distribution vs temporal matrix

The full-cohort distribution and temporal authorities are emitted separately:

| Distribution | Temporal | Meaning |
|---|---|---|
| false | false | No confirmed drift |
| true | false | Stable-rate distribution tail drift |
| false | true | Time-localized persistence anomaly |
| true | true | Persistent distribution degradation |

An authoritative KV Drift cannot set temporal persistence automatically.

## 18. Terminal reason authority

Every run emits:

```text
primary_terminal_reason
secondary_terminal_reasons[]
failed_components[]
final_admission_state
```

Canonical precedence:

```text
1 DeviceQuarantined
2 ObserverAuthorityHold
3 ReferenceBankInvalidHold
4 TopologyEvidenceInvalidHold
5 CombinedDistributionAndTemporalDriftHold
6 CombinedDistributionDriftHold
7 KernelDistributionDriftHold
8 GuardedDistributionDriftHold
9 CombinedTemporalPersistenceHold
10 KernelTemporalPersistenceHold
11 GuardedTemporalPersistenceHold
12 QuantileConfidenceInconclusiveHold
13 ExactTailSourceLocalizedHold
14 DiffuseKernelTailLocalizedHold
15 TailDriftNotReproducedHold
```

A confirmed Drift reason always precedes Inconclusive.

The final admission state may be `ExactTailSourceLocalizedHold` while the primary evidence reason remains `KernelDistributionDriftHold`. This preserves both the defect and successful localization.

## 19. Admission CAS

Parent state:

```text
QuantileConfidenceInconclusiveHold
generation=12
```

Open:

```text
BeginMidKvTailLocalizationCohort
generation 12 -> 13
post-state=EligibleForMidKvTailLocalizationOnly
```

Successful diagnostic close:

```text
generation 13 -> 14
post-state=ExactTailSourceLocalizedHold
or DiffuseKernelTailLocalizedHold
```

Candidate admission remains closed after PASS.

## 20. Exact fallback

Every terminal state executes one exact 128-step fallback session.

Required:

```text
candidate dispatcher calls=0
fallback dispatches=128
new session and KV owner
same-session fallback=0
cross-route KV reuse=0
payload readback=0
active global route unchanged
```

## 21. Runtime artifacts

Required outputs include:

```text
*_parent_rerun.args
*_parent_rerun.log
*_parent_binding.json
*_distribution_temporal_matrix.json
*_topology_sessions.json
*_topology_reference_boundaries.json
*_drift_reproduction.json
*_component_tail_authority.json
*_tail_source_localization.json
*_terminal_reason_receipt.json
*_observer_receipt.json
*_admission_receipt.json
*_fallback_receipt.json
*_negative_control_outcomes.json
*_static_checks.json
*_runtime_artifact.json
*_local_manifest.json
*_canonical_args.txt
*_canonical_run.cmd
```

Large evidence uses `atlas-parallel-group-map-v1` and independent group digests.

## 22. Static truth

Static extraction must prove:

```text
production shader unchanged
separate topology shader present
parent gate binary rerun path present
83-key CLI extension
full 72-session authority retained
8 topology sessions
fixed KV targets and controls
page/workgroup/cross pass counts exact
distribution and temporal fields distinct
primary and secondary terminal reasons distinct
Drift precedence above Inconclusive
payload readback absent
tail filtering absent
post-hoc topology mutation absent
global promotion absent
```

## 23. CLI contract

### Exact-value keys, 30

```text
--gqa4-r2f-r6-r5-r1-r1-distribution-policy matched-phase-exact-quantile-distribution-v2
--gqa4-r2f-r6-r5-r1-r1-temporal-policy window-profile-late-region-persistence-v2
--gqa4-r2f-r6-r5-r1-r1-topology-policy predeclared-page-workgroup-decomposition-v1
--gqa4-r2f-r6-r5-r1-r1-localization-policy exact-component-drift-and-tail-cooccurrence-v1
--gqa4-r2f-r6-r5-r1-r1-terminal-reason-policy strongest-evidence-primary-plus-secondary-reasons-v1
--gqa4-r2f-r6-r5-r1-r1-final-admission-policy localized-tail-evidence-hold-v1
--gqa4-r2f-r6-r5-r1-r1-target-kv-buckets 384,512
--gqa4-r2f-r6-r5-r1-r1-control-kv-buckets 256,768
--gqa4-r2f-r6-r5-r1-r1-page-tokens 128
--gqa4-r2f-r6-r5-r1-r1-workgroup-band-count 8
--gqa4-r2f-r6-r5-r1-r1-topology-profile-steps 2048
--gqa4-r2f-r6-r5-r1-r1-page-probe-step-modulus 2
--gqa4-r2f-r6-r5-r1-r1-page-probe-step-remainder 0
--gqa4-r2f-r6-r5-r1-r1-cross-probe-step-modulus 8
--gqa4-r2f-r6-r5-r1-r1-cross-probe-step-remainder 0
--gqa4-r2f-r6-r5-r1-r1-topology-observer-ring-capacity 8
--gqa4-r2f-r6-r5-r1-r1-topology-query-batch-passes 64
--gqa4-r2f-r6-r5-r1-r1-localization-family-size 103
--gqa4-r2f-r6-r5-r1-r1-localization-family-alpha 0.05
--gqa4-r2f-r6-r5-r1-r1-tail-coverage-minimum 0.60
--gqa4-r2f-r6-r5-r1-r1-localization-relative-risk-minimum 1.0
--gqa4-r2f-r6-r5-r1-r1-localization-phase-replication 2
--gqa4-r2f-r6-r5-r1-r1-dominance-margin 0.20
--gqa4-r2f-r6-r5-r1-r1-kernel-q99-ratio 1.40
--gqa4-r2f-r6-r5-r1-r1-q99-budget 0.01
--gqa4-r2f-r6-r5-r1-r1-full-authority-sessions 72
--gqa4-r2f-r6-r5-r1-r1-topology-sessions 8
--gqa4-r2f-r6-r5-r1-r1-total-sessions 80
--gqa4-r2f-r6-r5-r1-r1-total-candidate-steps 69120
--gqa4-r2f-r6-r5-r1-r1-total-diagnostic-passes 124928
```

### Boolean keys, 53

The exact Boolean list is the registry list implemented in `headwise_r7_r2f_r7_r6_r5_r1_r1_cli_registry.rs`. It covers parent identity, topology counts, diagnostic isolation, exact statistical authority, all localization classes, distribution/temporal separation, terminal precedence, observer/device/thermal authority, evidence retention, admission/fallback, and all forbidden mutation paths.

## 24. Negative controls

Twenty-eight groups, ten controls each:

```text
parent HOLD identity
parent Drift-unit identity
threshold identity
full-cohort population
topology-cohort population
fixed probe plan
page topology
workgroup topology
cross topology
page pass accounting
workgroup pass accounting
cross pass accounting
diagnostic isolation
component order statistics
component exact binomial
Fisher co-occurrence
page localization
workgroup localization
cross localization
diffuse classification
distribution authority
temporal authority
evidence matrix
terminal precedence
observer authority
thermal and device authority
raw evidence retention
admission, fallback, atlas integrity
```

```text
new controls=280
sealed R5 authority=940
combined expected=1220
```

## 25. PASS

PASS requires:

```text
exact parent binary rerun HOLD
parent Drift targets exact
production shader identity preserved
generation 12->13 CAS
72/72 full sessions
8/8 topology sessions
80/80 total sessions
69120/69120 candidate steps and tokens
30720/30720 page passes
65536/65536 workgroup passes
28672/28672 cross passes
103/103 source units
at least one target ReproducedDrift
other target at least DirectionallyConsistentInconclusive
every target receives exact non-inconclusive localization class
distribution/temporal SSOT split
terminal precedence exact
observer boundary waits=0
ring exhaustion=0
diagnostic canonical-output writes=0
diagnostic health-latch writes=0
payload readback=0
generation 13->14 CAS
final admission ExactTailSourceLocalizedHold or DiffuseKernelTailLocalizedHold
fallback exact
default route unchanged
automatic re-entry=0
1220/1220 negative controls
all artifacts and atlas digests exact
```

## 26. HOLD

HOLD on any parent identity, production shader identity, topology count, diagnostic isolation, confidence, co-occurrence, localization, distribution/temporal split, terminal precedence, observer, device, route, fallback, evidence, or digest failure.

`InconclusiveLocalization` and `TailDriftNotReproduced` remain HOLD.

## 27. Verdicts

Success:

```text
PROMOTE_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_R5_R1_R1_MID_KV_TAIL_TOPOLOGY_PAGE_WORKGROUP_PHASE_ATTRIBUTION_DISTRIBUTION_TEMPORAL_SPLIT_PRIMARY_REASON_AND_EXACT_SOURCE_LOCALIZATION_SEALED
```

Default HOLD:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_R5_R1_R1_MID_KV_TAIL_SOURCE_TOPOLOGY_OR_TERMINAL_AUTHORITY_NOT_PROVEN
```

## 28. Final seal

```text
preserved R6-R5-R1 HOLD
+ actual 72-session parent rerun
+ unchanged production candidate shader
+ isolated diagnostic topology shader
+ fixed 8-session mid-KV cohort
+ 30720 page probes
+ 65536 workgroup probes
+ 28672 cross probes
+ exact component q99 confidence
+ exact tail co-occurrence
+ page/workgroup/phase identity
+ distribution and temporal SSOT split
+ strongest-evidence terminal precedence
+ zero threshold relaxation
+ zero tail filtering
+ terminal candidate hold
= exact source localization without contaminating the production ruler
```
