# ASH-TCU-DECODE-04-R4-R5-R1
# Bounded Oracle Reduction Production Soak / Restart Recovery Gate

- Patch ID: `ASH-TCU-DECODE-04-R4-R5-R1_BOUNDED_ORACLE_REDUCTION_PRODUCTION_SOAK_RESTART_RECOVERY_GATE`
- Parent: `ASH-TCU-DECODE-04-R4-R5_LEGACY_FRAGMENT_RETIREMENT_READINESS_ORACLE_REDUCTION_GATE`
- Runtime mode: segmented production-soak controller with active bounded oracle reduction
- Default fragment source: TensorCube
- Legacy oracle: deterministic sampled, periodic full-dual, and risk-triggered full-dual
- Legacy fallback and legacy-only boot: mandatory
- Durable publication journal, quarantine, restart recovery, and operator rollback: mandatory
- Legacy oracle removal: false
- Legacy decoder retirement: false
- PASS authorizes only: `ASH-TCU-DECODE-04-R4-R5-R2_ORACLE_REDUCTION_STEADY_STATE_PROMOTION_GATE`

## Exact parent

```text
execution_id=decode04r4r5-0eef9e9aed02619a00d1
lineage_bundle_digest=0eef9e9aed02619a00d151fee113f925b34c03fe4c1b22c74a4c75b1cdd66593
total_generations=20000
total_selected_tokens=500000
full_dual_generations=5000
reduced_oracle_generations=15000
oracle_executed_selected_tokens=218634
oracle_skipped_selected_tokens=281366
unexpected_mismatch=0
natural_quarantine=0
output_divergence=0
candidate_byte_leak=0
durable_quarantine_pass=true
restart_recovery_pass=true
operator_rollback_drill_pass=true
detection_latency_policy_pass=true
reduction_benefit_pass=true
performance_policy_pass=true
```

The exact parent manifest and all referenced policy and evidence digests are content-bound.

## Purpose

R4-R5-R1 activates the bounded oracle-reduction policy in a production-like segmented soak. It must use the live model, tokenizer, checkpoint, selected-token path, KV progression, greedy and sampled routes, cached and streaming routes. Fixture-only receipt replay cannot satisfy promotion.

The gate owns one cumulative soak ledger. Every invocation contributes one segment, writes one segment receipt, atomically updates the cumulative state, and produces either HOLD or PASS.

A short invocation cannot claim the 24-hour soak. PASS is possible only after cumulative evidence closes every budget.

## Cumulative SSOT

```text
workspace/runtime/tensorcube/soak/r4_r5_r1/
ash_tensorcube_decode_04_r4_r5_r1_cumulative_state.json
```

The ledger binds:

```text
parent execution and lineage
production-soak policy digest
segment count and active runtime seconds
total and per-route generations and selected tokens
oracle-executed and oracle-skipped counters
NotObserved parity count
traffic-class counters
restart matrix
rollback, quarantine, and identity-drift drills
legacy-only, full-dual, restart-boundary, rollback, and quarantine replay counts
natural correctness counters
restart correctness counters
stability counters
segment digests
state digest
```

State writes are atomic and the prior digest is validated before reuse.

## Segment controls

```text
--segment-active-seconds <SECONDS>
--segment-generations <COUNT>
--restart-profile none|clean|scheduled_matrix
--reset-soak-state
```

Recommended segment:

```text
active runtime=7200 seconds
generations=10000
```

Twelve such segments provide 86400 active seconds and 120000 generations. The first segment uses `scheduled_matrix` to bind the restart, rollback, quarantine, and identity-drift drill matrix. Later segments normally use `none`.

The duration field is a declared segment evidence input. The runtime must also bind the segment receipt and cumulative state; it must not silently fabricate a continuous process lifetime.

## Soak minimums

```text
active runtime seconds >= 86400
segment count >= 6
total generations >= 100000
total selected tokens >= 3000000
route generations >= 25000 per route
route selected tokens >= 600000 per route
oracle-executed selected tokens >= 1200000
oracle-skipped selected tokens >= 1200000
```

Routes:

```text
greedy_cached
sampled_cached
greedy_streaming
sampled_streaming
```

## Traffic mix

At least 25 percent of cumulative generations must be represented in each evidence class:

```text
live production-bound traffic
historical replay
adversarial or rare-surface traffic
long-tail mixed traffic
```

The corpus retains all prior 19 classes or a strict content-addressed superset.

## Oracle policy

Inherited minimum full-dual generation rates:

| Route | Minimum |
|---|---:|
| greedy cached | 1/8 |
| sampled cached | 1/4 |
| greedy streaming | 1/4 |
| sampled streaming | 1/2 |

Token spot-check minima:

```text
cached >= 1/16
streaming >= 1/8
```

Oracle selection is deterministic and must not consume production RNG.

Every selected token is exactly one of:

```text
oracle executed
oracle skipped
```

Required truth:

```text
oracle_executed + oracle_skipped == selected_tokens
oracle skipped -> parity_status=NotObserved
```

An oracle-skipped token may never be reported as parity PASS.

## Full-dual windows

```text
startup: 64 generations and 4096 selected tokens
periodic generation window: 64 full-dual generations every 512 generations
periodic token window: 512 full-dual selected tokens every 4096 selected tokens
clean restart recovery: 64 generations and 4096 tokens
unclean restart recovery: 128 generations and 8192 tokens
```

Reduction resumes only after the applicable recovery window completes.

## Restart matrix

Minimum:

```text
clean process restart=8
unclean between-generation restart=4
unclean cached-transaction restart=4
unclean streaming-transaction restart=4
machine or host session restart=2
restart with active quarantine=2
restart after operator rollback=2
restart after policy reload=2
total restart events>=28
```

Restart truth:

```text
no duplicate output
no missing committed output
no partial generation resume
no stale authority epoch reuse
no stale selector state reuse
no quarantine loss
no rollback loss
```

Uncertain cached and streaming generations are not resumed. Unsealed candidate state is discarded and the next generation starts in LegacyDefault or FullDualRun.

## Durable publication journal

The publication journal owns publication state only:

```text
generation ID
route
authority epoch
last committed fragment sequence
last committed output digest
terminal commit state
receipt flush state
```

It does not own model, KV, sampler, or RNG state.

Required:

```text
atomic temp write
flush
rename
directory flush when supported
digest validation
```

A corrupt journal fails closed and forbids partial-generation resume.

## Durable quarantine

Any detected natural mismatch or critical invariant failure:

```text
contains the current generation
persists quarantine before next-generation admission
disables oracle reduction
disables TensorCube default for the quarantine scope
selects LegacyDefault
```

Quarantine survives process, runtime, and machine restarts and policy reloads.

Clear requires:

```text
explicit operator acknowledgement
diagnostic replay PASS
legacy-only replay PASS
identity and policy revalidation
full-dual recovery window
fresh authority epoch
clear receipt
```

No automatic clear is allowed.

Minimum injected quarantine drills: 16.

## Operator rollback

Canonical kill switch:

```text
ASH_TCU_DECODE04_FORCE_LEGACY_FRAGMENT_AUTHORITY=1
```

SLA:

```text
request acknowledgement <= 1 second
next generation = LegacyDefault
durable rollback persistence <= 2 seconds
```

Minimum rollback drills: 16.

Rollback state survives restart and policy reload. Clearing requires explicit action, identity and policy revalidation, a full-dual recovery window, and a fresh authority epoch.

## Identity drift

Required drift cases:

```text
model manifest
weight bundle
tokenizer manifest
tokenizer intrinsic identity
reserved-token digest
byte-token mapping
special-token classification
runtime route
oracle policy
soak policy
```

Drift is fail-closed. No silent rebind is allowed. Reduction resumes only under a new exact identity tuple, fresh policy digest, fresh authority epoch, operator acknowledgement, and full-dual recovery evidence.

## Oracle re-expansion

Triggers:

```text
latency anomaly
memory anomaly
unknown token
unseen piece transition
telemetry warning
restart recovery
operator request
identity revalidation
quarantine clear
```

Targets:

```text
FullDualRun
LegacyDefault
```

A critical trigger permits zero candidate publications after its effective boundary.

## Replay budgets

```text
legacy-only replay >= 10000 generations
full-dual replay >= 10000 generations
restart-boundary replay >= 2000 generations
rollback replay >= 2000 generations
quarantine replay >= 1000 generations
```

Required exact equality:

```text
reduced output == full-dual output == legacy-only output
selected token sequence equal
stream chunks and boundaries equal
KV and DecodeState equal
sampler and RNG states equal
finish reason and route equal
```

TensorCube remains fragment-only.

## Performance

Per route at least one benefit:

```text
reduced throughput >= 110 percent of full-dual throughput
or
legacy oracle CPU time reduced >= 25 percent
```

Additional limits:

```text
reduced throughput >= 75 percent of legacy-only
selector p99 <= 100 us
policy lookup p99 <= 100 us
quarantine lookup p99 <= 1 ms
publication journal update p99 <= 2 ms
cold legacy fallback p99 <= 250 ms
stream TTFB <= R4-R4-R4 baseline + 5 ms
unbounded allocation count=0
```

## Natural correctness budget

Required zero:

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
quarantine loss
rollback loss
panic
deadlock
watchdog timeout
stuck generation
telemetry drop
natural abort
```

## SSOT code owners

```text
R4R5R1ProductionSoakPolicy
R4R5R1SoakSegmentReceipt
R4R5R1CumulativeSoakState
R4R5R1SteadyStateReadinessSummary

build_r4_r5_r1_production_soak_policy
new_r4_r5_r1_cumulative_state
apply_r4_r5_r1_segment
summarize_r4_r5_r1_state
run_r4_r5_r1_runtime
```

There is one production-soak policy owner, one cumulative-state reducer, one restart scheduler, one durable quarantine owner, one rollback reducer, one identity-drift reducer, one oracle re-expansion reducer, and one promotion verdict reducer.

## Binary

```text
ash_tcu_decode_04_r4_r5_r1_bounded_oracle_reduction_production_soak_restart_recovery_gate
```

## HOLD

HOLD is the expected result until cumulative evidence is complete.

HOLD writes the segment receipt, cumulative state, readiness summary, hold reasons, audit artifacts, and local manifest.

HOLD grants no R4-R5-R2 authority.

## PASS

```text
PASS_ASH_TCU_DECODE_04_R4_R5_R1_BOUNDED_ORACLE_REDUCTION_PRODUCTION_SOAK_RESTART_RECOVERY_GATE
```

PASS requires all soak duration, traffic, route, oracle, restart, journal, quarantine, rollback, identity, replay, correctness, performance, telemetry, structural, and no-repair checks.

Expected authority:

```text
decode04_r4_r5_r2_authorized=true
bounded_oracle_reduction_production_soak_proven=true
legacy_oracle_reduction_active=true
legacy_oracle_reduction_steady_state_authorized=false
legacy_oracle_removal_authorized=false
legacy_decoder_retirement_authorized=false
tensorcube_default_fragment_authority=true
production_fragment_apply_authorized=true
general_production_apply_authorized=false
production token/KV/sampler/RNG authority=false
```

## Non-goals

R4-R5-R1 does not authorize:

```text
zero-oracle operation
legacy oracle removal
legacy decoder deletion
candidate-only production
steady-state reduction promotion
TensorCube token selection
TensorCube sampler or RNG ownership
TensorCube KV or DecodeState ownership
general production apply
```

## Next gate

PASS authorizes only:

```text
ASH-TCU-DECODE-04-R4-R5-R2
Oracle Reduction Steady-State Promotion Gate
```

Legacy removal remains forbidden.