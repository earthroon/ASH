# ASH-TCU-DECODE-04-R4-R5-R1-R7
# Multi-Segment Measured Soak Continuity / Cross-Restart Ledger Chain / Route Budget Accumulation Gate

- Patch ID: `ASH-TCU-DECODE-04-R4-R5-R1-R7_MULTI_SEGMENT_MEASURED_SOAK_CONTINUITY_CROSS_RESTART_LEDGER_CHAIN_ROUTE_BUDGET_ACCUMULATION_GATE`
- Parent gate: `ASH-TCU-DECODE-04-R4-R5-R1-R6_MEASURED_PRODUCTION_SEGMENT_ADMISSION_FRESH_EVIDENCE_EPOCH_BOOTSTRAP_LIVE_SOAK_ACCRUAL_GATE`
- Parent execution ID: `decode04r4r5r1r6-dee4bb6dc5ff56ad5fb2`
- Parent lineage: `dee4bb6dc5ff56ad5fb25e2f43831c8d2c628f609bb3ca91b0f7582866049676`
- Evidence epoch: `r4r5r1r5-epoch-3fe343d135e6216bf4cf`
- Parent committed segment: `0`
- Parent active duration: `4168800 ns`
- Parent generations: `200`
- Parent selected tokens: `5000`
- Parent oracle executed/skipped: `4342 / 658`
- PASS authorizes only: `ASH-TCU-DECODE-04-R4-R5-R1-R8`
- R4-R5-R2 authorization: `false`
- Legacy removal: `false`
- Legacy decoder retirement: `false`
- General production apply: `false`

## Purpose

R6 proved that one promotion-eligible production segment can commit under the repaired R5 measured-duration clock.

R7 proves that five additional independently measured worker segments can form one durable, non-forking ledger chain across process boundaries.

```text
committed indexes = 0,1,2,3,4,5
promotion-eligible segment count = 6
evidence epoch count = 1
unique committed process clock domains >= 6
```

R7 is a continuity gate. It does not complete the 24-hour soak.

## Exact parent admission

Required:

```text
verdict=decode04_r4_r5_r1_r6_first_measured_production_segment_pass
execution_id=decode04r4r5r1r6-dee4bb6dc5ff56ad5fb2
lineage_bundle_digest=dee4bb6dc5ff56ad5fb25e2f43831c8d2c628f609bb3ca91b0f7582866049676
evidence_epoch_id=r4r5r1r5-epoch-3fe343d135e6216bf4cf
segment_index=0
segment_promotion_eligible=true
segment_smoke_mode=false
pre_r5_duration_contribution_ns=0
smoke_duration_contribution_ns=0
cumulative_live_generation_active_ns=4168800
natural_generation_count=200
selected_token_count=5000
oracle_executed_selected_tokens=4342
oracle_skipped_selected_tokens=658
r4_r5_r1_r7_authorized=true
decode04_r4_r5_r2_authorized=false
legacy_oracle_removal_authorized=false
legacy_decoder_retirement_authorized=false
```

## Authority ownership

```text
coordinator owns segment sequence, worker tokens, restart schedule, durable reload and final verdict
worker owns one process clock domain, one segment execution and one atomic commit
R5 ledger owns cumulative active duration and route counters
R7 continuity journal owns accepted, orphaned, duplicate and fork events
```

A worker may commit at most one segment.

## Evidence epoch and policy immutability

Forbidden:

```text
--reset-evidence-epoch
--segment-active-seconds
--smoke-duration-evidence
```

Required across all segments:

```text
evidence_epoch_id unchanged
duration_policy_digest unchanged
oracle_policy_digest unchanged
runtime_identity_digest unchanged
```

Any change fails closed before the next worker admission.

## Segment chain

Parent owns segment `0`. R7 commits `1..5`.

```text
segment[n].previous_segment_receipt_digest
== segment[n-1].segment_receipt_digest
```

Required final chain:

```text
first_segment_index=0
last_segment_index=5
committed_segment_count=6
gap_count=0
fork_count=0
duplicate_count=0
```

Commit uses compare-and-swap inputs:

```text
expected ledger digest
expected previous segment digest
expected next segment index
```

A mismatch returns `CommitConflict`.

## Cross-process clock domains

Every committed segment executes in a separate worker process and receives a fresh monotonic clock domain.

```text
unique committed process clock domains >= 6
cross-process Instant subtraction count = 0
```

Only validated per-generation monotonic durations are added to active time.

## Restart matrix

R7 requires:

```text
clean coordinator recovery child
clean worker process boundaries
one unclean worker termination before commit
one replacement worker for the same expected index
one policy reload process boundary
```

The unclean worker test must prove:

```text
ledger unchanged
next segment index unchanged
orphan duration contribution=0
orphan generation contribution=0
orphan selected-token contribution=0
replacement worker uses a new clock domain
replacement worker commits exactly once
```

## Worker launch tokens

A coordinator-issued token binds:

```text
evidence epoch
expected segment index
expected previous segment digest
expected ledger digest
duration policy digest
oracle policy digest
runtime identity digest
single-use launch nonce
```

Token reuse is rejected.

## Per-segment workload

Each additional segment requires:

```text
production duration evidence
natural generations >=100
selected tokens >=2500
all four routes
all four traffic classes
all 19 corpus classes cumulatively
```

Route minima per segment:

```text
greedy_cached generations >=25, selected tokens >=500
sampled_cached generations >=25, selected tokens >=500
greedy_streaming generations >=25, selected tokens >=500
sampled_streaming generations >=25, selected tokens >=500
```

R7 cumulative bootstrap minima:

```text
each route generations >=175
each route selected tokens >=3750
```

## Duration equations

For every committed segment:

```text
segment_live_generation_active_ns
= sum(validated promotion-eligible natural generation active ns)
```

Cumulative:

```text
active_after
= 4168800 + sum(R7 committed segment active ns)

generations_after
= 200 + sum(R7 committed natural generations)

selected_tokens_after
= 5000 + sum(R7 committed selected tokens)
```

Excluded time has zero contribution:

```text
sleep
idle
startup
restart delay
fixture drills
artifact I/O
orphan work
```

## Route equations

For every route `r`:

```text
route_generations_after[r]
= route_generations_before[r] + sum(segment route generations[r])

route_selected_tokens_after[r]
= route_selected_tokens_before[r] + sum(segment route selected tokens[r])

route_active_ns_after[r]
= route_active_ns_before[r] + sum(segment route active ns[r])
```

All route counters are monotonic.

## Oracle equations

Each committed segment requires:

```text
oracle_executed_selected_tokens > 0
oracle_skipped_selected_tokens > 0
executed + skipped = selected tokens
```

Cumulative:

```text
executed_after = 4342 + sum(R7 segment executed)
skipped_after = 658 + sum(R7 segment skipped)
executed_after + skipped_after = total selected tokens after
```

Skipped parity remains `NotObserved`. It may not be reported as PASS.

## Full-dual and recovery continuity

The runtime retains:

```text
periodic full-dual windows
risk-triggered re-expansion
restart-recovery full-dual windows
legacy default fallback
```

After a critical boundary:

```text
candidate publications = 0
```

TensorCube remains fragment-only and does not own token selection, sampler, RNG, KV, DecodeState, finish/stop or route selection.

## Replay accumulation

Minimum additional replay per segment:

```text
legacy-only >=100
full-dual >=100
restart-boundary >=20
rollback >=20
quarantine >=10
```

Fixture replay duration contributes zero natural production active time.

## Correctness

Required zero across all additional segments:

```text
unexpected mismatch
natural quarantine
natural rollback
output divergence
candidate byte leak
double emit
missing emit
invalid UTF-8
partial scalar emit
replacement fallback
duplicate output after restart
partial generation resume
stale epoch reuse
panic
deadlock
watchdog timeout
stuck generation
telemetry drop
natural abort
```

Required parity:

```text
reduced output == full-dual output == legacy-only output
stream chunk sequence and boundary parity
token sequence parity
KV owner/content parity
DecodeState parity
sampler and RNG parity
finish/stop parity
route parity
```

## Performance continuity

Per committed segment:

```text
timer overhead p99 <=100 us
receipt reduction p99 <=500 us
unbounded allocation count=0
```

Forbidden:

```text
per-token full-ledger scan
embedding all generation receipts in the cumulative ledger
ledger growth proportional to all generation receipt bytes
```

## Canonical binary

```text
ash_tcu_decode_04_r4_r5_r1_r7_multi_segment_measured_soak_continuity_gate
```

The coordinator invokes the same executable in hidden worker and recovery modes. Users run only the coordinator command.

## Required command values

```text
--repo-root <PATH>
--r4-r5-r1-r6-parent-manifest <PATH>
--runtime-profile <PATH>
--additional-segments 5
--segment-max-wall-seconds <SECONDS>
--segment-max-generations <COUNT>
--segment-min-generations <COUNT>
--restart-profile cross_process_continuity_matrix
--production-duration-evidence
```

Required activation seals include:

```text
--authorize-multi-segment-measured-soak-continuity
--activate-r5-duration-ledger
--activate-r7-coordinator
--activate-r7-worker-processes
--activate-cross-restart-ledger-chain
--activate-route-budget-accumulation
--activate-oracle-budget-accumulation
--activate-continuity-journal
--activate-worker-launch-tokens
--activate-orphan-segment-quarantine
--activate-idempotent-segment-commit
--activate-segment-fork-rejection
--activate-policy-reload-boundary
--activate-live-production-traffic
--activate-live-four-route-runtime
--activate-periodic-full-dual-windows
--activate-risk-triggered-oracle-reexpansion
--activate-durable-publication-journal
--activate-durable-quarantine
--activate-operator-rollback-sla
--activate-identity-drift-fail-closed
```

Required continuity truth includes:

```text
exact R6 parent
unchanged evidence epoch and policies
segments 0..5
five additional committed segments
six total promotion-eligible segments
strict digest chain
unique clock domain per segment
coordinator durable recovery
unclean worker before-commit exclusion
single-use tokens
orphan contribution zero
duplicate rejection
fork rejection
route equations
oracle equations
all correctness counters zero
```

## PASS marker

```text
PASS_ASH_TCU_DECODE_04_R4_R5_R1_R7_MULTI_SEGMENT_MEASURED_SOAK_CONTINUITY_CROSS_RESTART_LEDGER_CHAIN_ROUTE_BUDGET_ACCUMULATION_GATE
```

PASS authority:

```text
r4_r5_r1_r7_multi_segment_continuity_pass=true
r4_r5_r1_six_segment_budget_complete=true
r4_r5_r1_r8_authorized=true
bounded_oracle_reduction_production_soak_proven=false
decode04_r4_r5_r2_authorized=false
legacy_oracle_reduction_active=true
legacy_oracle_reduction_steady_state_authorized=false
legacy_oracle_removal_authorized=false
legacy_decoder_retirement_authorized=false
general_production_apply_authorized=false
```

## Expected HOLD

After R7, the parent soak may remain HOLD for:

```text
active runtime
natural generations
selected tokens
final route budgets
final oracle budgets
final replay budgets
final throughput benefit
```

The six-segment count budget must be complete.

## Next gate

PASS authorizes only:

```text
ASH-TCU-DECODE-04-R4-R5-R1-R8
Measured Soak Budget Closure /
Full Route Oracle Replay Budget /
24-Hour Active Runtime Promotion Gate
```

Only R8 may authorize R4-R5-R2 after all final budgets close.
