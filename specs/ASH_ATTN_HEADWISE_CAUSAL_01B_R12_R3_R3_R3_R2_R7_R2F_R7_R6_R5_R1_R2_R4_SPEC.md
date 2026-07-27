# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6-R5-R1-R2-R4

## Raw Pair Replay SSOT / Conflict Tuple Exposure / Deterministic Offline Re-Adjudication / Runtime·Replay Verdict Parity Seal

## 0. State

```text
PARENT=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6-R5-R1-R2-R3
PARENT_VERDICT=PASS
SOURCE_RUNTIME=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6-R5-R1-R2
SOURCE_RUNTIME_TERMINAL=HOLD
RUN_SCOPE=sealed-parent-import-plus-zero-gpu-deterministic-offline-replay-v1
DEFAULT_VERDICT=HOLD
ACTIVE_ROUTE=existing-production-headwise-reference-v1
CANDIDATE_ROUTE=gqa4-cluster-production-canary-v1
RAW_PAIR_POLICY=parent-bound-complete-probe-shadow-pair-graph-v1
REPLAY_POLICY=pure-rust-independent-adjudicator-bit-exact-v1
CONFLICT_POLICY=all-conflicting-units-full-tuple-and-step-exposure-v1
PARITY_POLICY=runtime-replay-all-authority-layer-exact-v1
NUMERIC_POLICY=finite-f64-bit-exact-authority-no-tolerance-v1
ORDER_POLICY=canonical-kv-role-surface-exposure-step-order-v1
ADMISSION_POLICY=evidence-only-no-device-no-candidate-no-route-mutation-v1
GENERATION_POLICY=parent-18-child-19-20-evidence-lineage-v1
ARTIFACT_LAYOUT=atlas-parallel-group-map-v1
ATLAS_DIGEST_POLICY=atlas-parallel-group-map-carried-canonical-payload-v4-r1
```

R2-R4 proves whether the R1-R2 statistical publication can be regenerated solely from the retained raw Probe/Shadow pair evidence by an independent, device-free Rust adjudicator. It reproduces the existing R1-R2 HOLD without repairing or reinterpreting the adjudication lattice.

A replayed HOLD is a successful R2-R4 result when every authority object and terminal reason matches the runtime publication exactly.

## 1. Frozen authority

R2-R4 must not change:

```text
kernel q99 ratio=1.40
q99 exceedance budget=0.01
boundary family alpha=0.05/32
reproduction family alpha=0.05/8
paired family alpha=0.05
paired family size=24
paired unit alpha=0.05/24
control KVs=256,768
target KVs=384,512
profile steps=2048
phase count=4
surfaces=kernel,guarded
exposures=Clean,PageWorkgroup,CrossSchedule
source R1-R2 terminal=HOLD
candidate admission=closed
payload readback=0
```

Forbidden:

```text
GPU adapter or device creation
native bootstrap
shader or pipeline creation
command encoding or submission
timestamp query allocation
new Probe, Shadow, or fallback session
parent R2-R3 process launch
parent R1-R2 process launch
source artifact mutation
sample deletion or duplication
outlier filtering or winsorization
threshold relaxation or alpha expansion
unpaired substitution
normal approximation
conflict reinterpretation
target-state lattice repair
candidate dispatch or lease
route pointer mutation
automatic re-entry
```

## 2. Direct parent contract

The direct parent is the successful R2-R3 evidence-binding seal.

Required parent facts:

```text
parent pass=true
parent terminal generation=18
parent contract valid=true
parent required files=17/17
parent authority artifacts=12/12
parent atlas groups=13/13
parent manifest closed=true
runtime profile immutable=true
parent admission closed=true
child admission independent=true
parent fallback exact=true
R2-R3 fallback exact=true
candidate dispatches=0
payload readback=0
default route unchanged=true
inherited R1-R2 negative=1230/1240
R2-R3 negative=320/320
```

R2-R4 resolves every source path through the R2-R3 `parent_artifact_closure.required_files` map. Hard-coded source-path substitution is forbidden.

## 3. Required source graph

R1-R2 source artifacts:

```text
*_probe_shadow_pairs.json
*_shadow_reference_boundaries.json
*_probe_shadow_reproduction.json
*_paired_interference_units.json
*_control_kv_stability.json
*_target_kv_validity.json
*_localization_validity.json
*_negative_control_outcomes.json
*_runtime_artifact.json
*_local_manifest.json
```

R2-R3 binding artifacts:

```text
*_parent_terminal_contract.json
*_parent_evidence_snapshot.json
*_parent_artifact_closure.json
*_parent_manifest_closure.json
*_parent_atlas_revalidation.json
*_runtime_profile_identity.json
*_route_generation_lineage.json
*_child_admission_receipt.json
*_fallback_continuity.json
*_runtime_artifact.json
*_local_manifest.json
```

Every source file must:

```text
exist as a regular file
resolve beneath workspace/runtime/attention
match the SHA-256 recorded by R2-R3
remain byte-identical before and after replay
have no duplicate canonical path
have no traversal, symlink, or junction escape
```

## 4. Evidence-only execution boundary

Required execution counts:

```text
parent process launches=0
GPU adapter requests=0
native bootstrap calls=0
device creations=0
queue creations=0
shader module creations=0
pipeline creations=0
command encoder creations=0
command submissions=0
timestamp queries=0
new timestamp samples=0
payload readbacks=0
candidate dispatches=0
fallback dispatches=0
```

The R2-R4 binary may only read sealed source artifacts, execute pure Rust replay logic, and write child evidence artifacts.

## 5. Raw pair replay SSOT

The sole statistical source is the typed `pairs` array in `*_probe_shadow_pairs.json`.

Required inventory:

```text
pair records=8
KVs=256,384,512,768
roles=Reference,Evaluation
Probe sessions=8
Shadow sessions=8
sessions=16
steps per session=2048
production timestamp samples=32768
queue-state records=32768
```

Canonical pair key:

```text
kv_length
role
pair_id
```

Canonical order:

```text
KV 256 Reference
KV 256 Evaluation
KV 384 Reference
KV 384 Evaluation
KV 512 Reference
KV 512 Evaluation
KV 768 Reference
KV 768 Evaluation
```

The replay parser must deserialize statistical fields into replay-owned typed Rust structures. Runtime summary receipts may be compared after replay but may not be copied into replay output.

## 6. Sample and queue identity

Every Probe and Shadow session must prove:

```text
requested steps=2048
accepted payload dispatches=2048
published health tokens=2048
faulted health tokens=0
payload readback=0
payload host materialization=0
payload host upload=0
per-step host waits=0
invalid timestamps=0
timestamp samples=2048
pass=true
```

Every session must contain exactly one finite, positive kernel and guarded duration for every decode step `0..2047`, with no missing or duplicate step.

Canonical raw sample key:

```text
pair_id / pair_kind / decode_step
```

Every Probe and Shadow queue record must also exist for every production step. Replay independently derives the exposure class and checks it against the publication.

Exposure definition:

```text
SessionStart: step=0
Clean: even step >0
PageWorkgroup: odd step and previous even step is not divisible by 8
CrossSchedule: odd step and previous even step is divisible by 8
```

Per session:

```text
SessionStart=1
Clean=1023
PageWorkgroup=768
CrossSchedule=256
```

Expected Probe diagnostic work:

| KV | Clean | PageWorkgroup | CrossSchedule |
|---:|---:|---:|---:|
| 256 | 0 | 10 | 10 |
| 384 | 0 | 11 | 35 |
| 512 | 0 | 12 | 44 |
| 768 | 0 | 14 | 14 |

Shadow actual diagnostic work is always zero while the synthetic expected Probe workload remains retained.

## 7. Numeric and ordering policy

All authority calculations use finite IEEE-754 binary64 values.

Required numeric domain:

```text
NaN count=0
positive infinity count=0
negative infinity count=0
zero duration count=0
negative duration count=0
```

Canonical duration selector:

```text
surface=kernel  -> kernel_duration_ns
surface=guarded -> guarded_duration_ns
```

Canonical phase is the R1-R2 runtime phase:

```text
phase=floor(decode_step * 4 / 2048), clamped to 0..3
```

This quartile phase is authoritative. `decode_step mod 4` is forbidden.

Authority parity for f64 values is bit-exact:

```text
left.to_bits() == right.to_bits()
```

No ULP tolerance is allowed for runtime/replay authority comparison. The existing 1-ULP rule remains limited to non-authoritative atlas `fields` mirror validation.

## 8. Independent boundary replay

Only Shadow Reference production timestamps build the common ruler.

For every:

```text
KV=256,384,512,768
surface=kernel,guarded
phase=0,1,2,3
```

Replay must:

```text
select the Shadow Reference pair
select the surface duration
select quartile-phase samples
require sample count=512
sort finite f64 durations ascending
compute the exact lower order-statistic index for q=0.99 and alpha=0.05/32
select lower_q99_ns
compute boundary_ns=lower_q99_ns * 1.40
```

Required output:

```text
boundary receipts=32
all sample counts=512
all lower indices exact
all lower q99 bits exact
all boundary bits exact
```

Runtime boundary array order is not authoritative. Canonical key parity is authoritative.

## 9. Probe and Shadow reproduction replay

For each pair kind, surface, and KV:

```text
pair kind=Probe,Shadow
surface=kernel,guarded
KV=256,384,512,768
samples=2048
alpha=0.05/8
budget=0.01
```

Replay must count duration values above the phase-matched replayed boundary, calculate exact one-sided Clopper-Pearson lower and upper bounds, classify `Noninferior / Drift / Inconclusive`, and reproduce the existing R1-R2 reproduction class without reinterpretation.

Required output:

```text
reproduction receipts=16
all counts exact
all f64 fields bit-exact
all state and class strings exact
```

## 10. Paired interference unit replay

Only Evaluation pairs enter paired interference authority.

Canonical units:

```text
4 KVs × 2 surfaces × 3 exposures = 24 units
SessionStart excluded
```

For each matched step:

```text
pd=Probe duration
sd=Shadow duration
delta=pd-sd
ratio=pd/sd
boundary=replayed boundary for KV/surface/quartile phase
probe_tail=pd>boundary
shadow_tail=sd>boundary
```

Duration counts:

```text
positive: delta>0
negative: delta<0
tie: delta==0
```

Tail table:

```text
A=Probe tail and Shadow tail
B=Probe tail and Shadow non-tail
C=Probe non-tail and Shadow tail
D=neither tail
```

Exact tests:

```text
sign_p_probe_slower=binomial_survival(positive+negative,0.5,positive)
sign_p_shadow_slower=binomial_survival(positive+negative,0.5,negative)
mcnemar_p_probe_slower=binomial_survival(B+C,0.5,B)
mcnemar_p_shadow_slower=binomial_survival(B+C,0.5,C)
unit alpha=0.05/24
```

The replay must reproduce every aggregate, median, ratio, p-value, Boolean predicate, and verdict for all 24 units with bit-exact f64 parity.

## 11. Conflict tuple exposure

The source runtime published exactly two `ConflictingEvidence` units. R2-R4 must rediscover exactly two, not copy the count.

Each conflict tuple must include:

```text
unit key: KV / surface / exposure
runtime verdict
replay verdict
sample count
positive / negative / tie
median delta
median Probe/Shadow ratio
A / B / C / D
all four exact p-values
unit alpha
duration Probe-slower significant
duration Shadow-slower significant
tail Probe-slower significant
tail Shadow-slower significant
duration direction
tail direction
conflict predicate set
```

Every contributing matched step must be retained with:

```text
decode step
quartile phase
Probe and Shadow durations
delta
ratio
boundary
Probe and Shadow tail flags
queue-state identity
expected and actual diagnostic work
route and device generation
```

Required:

```text
conflict tuples=2
omitted conflict units=0
omitted contributing steps=0
duplicate contributing steps=0
all aggregate counts reconstructed from contributing steps
```

Conflict classification is historical reproduction only. R2-R4 may not rename, merge, split, repair, or reinterpret the conflicts.

## 12. Control, target, localization, and terminal replay

Replay must independently rebuild:

```text
control KV 256 classification
control KV 768 classification
target KV 384 classification
target KV 512 classification
overall localization validity
primary terminal reason
secondary terminal reasons
failed components
final admission state
terminal token
```

Required historical result:

```text
controls=2/2 ShadowStable
targets=2/2 TargetDriftNotReproduced
overall localization=LocalizationValidityInconclusive
source terminal=HOLD
source pass=false
```

This result is not treated as proof that the scientific lattice is correct. It proves only that the publication is reproducible from its retained raw evidence.

## 13. Runtime/replay parity matrix

Canonical parity objects:

```text
32 boundary receipts
16 reproduction receipts
24 paired interference units
2 control receipts
2 target receipts
1 localization receipt
1 terminal receipt
```

Total:

```text
78 authority objects
```

Every object compares:

```text
canonical key
integer counts
Boolean predicates
enum and class strings
f64 authority fields by to_bits()
```

Required:

```text
parity rows=78/78
integer mismatches=0
Boolean mismatches=0
string mismatches=0
f64 bit mismatches=0
missing runtime objects=0
missing replay objects=0
extra runtime objects=0
extra replay objects=0
```

## 14. Deterministic replay

The gate must execute:

```text
Replay A from the original parsed input
Replay B from a fresh parse of the same source bytes
Replay P from semantically identical JSON with object-key order permuted
```

Required:

```text
Replay A digest == Replay B digest
Replay A digest == Replay P digest
conflict tuple digest equal across A/B/P
parity matrix digest equal across A/B/P
source pre/post digests unchanged
```

Array order representing semantic sequences remains significant. Object-key order is non-authoritative.

## 15. Admission and generation

Parent terminal generation:

```text
18
```

Open:

```text
generation 18 -> 19
state=EligibleForRawPairReplayOnly
```

Terminal:

```text
generation 19 -> 20
state=RawPairReplayParitySealedHold
```

Both states require:

```text
candidate dispatches=0
candidate leases=0
fallback dispatches=0
route mutations=0
automatic re-entry=0
default route unchanged=true
```

R2-R4 PASS seals replay reproducibility while preserving terminal candidate HOLD.

## 16. Artifact outputs

Required outputs:

```text
*_source_binding.json
*_source_digest_closure.json
*_raw_pair_inventory.json
*_raw_session_inventory.json
*_queue_exposure_replay.json
*_boundary_replay.json
*_reproduction_replay.json
*_paired_unit_replay.json
*_conflict_tuples.json
*_conflict_steps.json
*_control_replay.json
*_target_replay.json
*_localization_terminal_replay.json
*_runtime_replay_parity.json
*_determinism_receipt.json
*_admission_receipt.json
*_negative_control_outcomes.json
*_static_checks.json
*_runtime_artifact.json
*_local_manifest.json
*_canonical_args.txt
*_canonical_run.cmd
```

The runtime artifact uses a thin root and exactly 18 atlas groups:

```text
identity
parent_binding
source_binding
source_digest_closure
raw_pair_inventory
raw_session_inventory
queue_exposure
boundaries
reproduction
paired_units
conflict_tuples
conflict_steps
control_target
localization_terminal
runtime_replay_parity
determinism
admission
verdict
```

Each group retains `group_id`, `field_count`, canonical payload, payload SHA-256, and group digest. The manifest must close every child artifact, group digest, atlas digest, source digest, CLI digest, and binary identity.

## 17. CLI contract

The R2-R4 registry inherits the complete R2-R3 registry and adds:

```text
exact-value keys=34
Boolean keys=60
total new keys=94
```

Unknown, duplicate, missing, wrong-value, and wrong-polarity keys are terminal HOLD.

## 18. Negative controls

R2-R4 adds 36 groups of 10 controls:

```text
new controls=360
inherited R1-R2 visible=1230/1240
inherited R2-R3 visible=320/320
combined visible expected=1910/1920
```

The inherited ten R1-R2 failures remain visible and unchanged. They do not fail R2-R4 because the scientific HOLD itself is the object being replay-audited.

## 19. PASS

PASS requires all of the following:

```text
parent R2-R3 PASS exact
parent generation=18
source R1-R2 HOLD exact
source files resolve through R2-R3 closure
all source SHA-256 values exact
source files immutable
zero parent process launch
zero GPU/device/queue work
8/8 raw pairs
16/16 sessions
32768/32768 timestamps
32768/32768 queue records
all decode steps exact
all durations finite and positive
all exposures independently reproduced
32/32 boundaries replayed and runtime-parity exact
16/16 reproductions replayed and runtime-parity exact
24/24 paired units replayed and runtime-parity exact
2/2 conflict tuples exposed
all conflict contributing steps retained
2/2 controls runtime-parity exact
2/2 targets runtime-parity exact
1/1 localization runtime-parity exact
1/1 terminal runtime-parity exact
78/78 parity rows pass
zero f64 authority bit mismatch
Replay A/B digest parity exact
object-key permutation replay parity exact
source runtime remains HOLD
candidate dispatches=0
candidate leases=0
route mutations=0
fallback dispatches=0
open generation=19
terminal generation=20
18/18 atlas groups exact
360/360 new negative controls
all child artifact and manifest digests exact
```

R2-R4 PASS does not require the source R1-R2 to pass, the conflict count to become zero, localization to become valid, or candidate promotion eligibility.

## 20. HOLD

HOLD occurs on any parent identity failure, source binding failure, source digest mismatch, source mutation, process or GPU execution attempt, raw pair schema failure, missing or duplicate pair or step, non-finite duration, exposure mismatch, boundary mismatch, reproduction mismatch, paired unit mismatch, conflict omission, conflict aggregate mismatch, control or target mismatch, localization or terminal mismatch, f64 bit mismatch, nondeterministic replay, key-order dependence, admission mutation, generation mismatch, atlas mismatch, manifest mismatch, or negative-control failure.

No automatic retry or selective source substitution is allowed.

## 21. Verdicts

Success:

```text
PROMOTE_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_R5_R1_R2_R4_RAW_PAIR_REPLAY_CONFLICT_TUPLE_EXPOSURE_DETERMINISTIC_OFFLINE_READJUDICATION_AND_RUNTIME_REPLAY_VERDICT_PARITY_SEALED
```

Default HOLD:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_R5_R1_R2_R4_RAW_PAIR_SOURCE_CONFLICT_EXPOSURE_REPLAY_DETERMINISM_OR_RUNTIME_PARITY_NOT_PROVEN
```

Successful summary form:

```text
[r2f-r7-r6-r5-r1-r2-r4][summary]
parent_r2_r3=PASS
source_r1_r2=HOLD
source_bound=true
gpu_calls=0
pairs=8/8
sessions=16/16
timestamp_samples=32768/32768
queue_records=32768/32768
boundaries=32/32
reproductions=16/16
paired_units=24/24
conflicts=2/2
conflict_steps=<exact>/<exact>
controls=2/2
targets=2/2
localization=1/1
parity_rows=78/78
f64_bit_mismatches=0
replay_repeat_equal=true
key_order_independent=true
candidate_dispatches=0
fallback_dispatches=0
source_negative=1230/1240
parent_negative=320/320
new_negative=360/360
combined_negative_visible=1910/1920
pass=true
```

## 22. Final seal

```text
preserved R1-R2 scientific HOLD
+ preserved R2-R3 evidence-contract PASS
+ zero parent rerun
+ zero GPU bootstrap
+ exact sealed source graph import
+ eight complete raw Probe/Shadow pairs
+ 32768 timestamp samples
+ 32768 queue-state records
+ independent exposure reconstruction
+ independent 32-cell Shadow Reference ruler replay
+ independent 16-receipt reproduction replay
+ independent 24-unit paired duration and tail replay
+ complete exposure of both conflicting units
+ every contributing conflict step retained
+ exact control, target, localization, and terminal replay
+ 78-object runtime/replay parity matrix
+ bit-exact f64 authority comparison
+ repeated replay determinism
+ object-key-order independence
+ zero threshold relaxation
+ zero tail filtering
+ zero candidate execution
+ zero route mutation
+ terminal candidate hold
= proof that the published conflict and HOLD verdict are reproducible from the retained raw pair evidence before any adjudication repair is attempted
```
