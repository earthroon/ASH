# ASH-TCU-DECODE-04-R4-R5-R1-R8
# Measured Soak Budget Closure / Full Route Oracle Replay Budget / 24-Hour Active Runtime Promotion Gate

- Patch ID: `ASH-TCU-DECODE-04-R4-R5-R1-R8_MEASURED_SOAK_BUDGET_CLOSURE_FULL_ROUTE_ORACLE_REPLAY_BUDGET_24_HOUR_ACTIVE_RUNTIME_PROMOTION_GATE`
- Parent: `ASH-TCU-DECODE-04-R4-R5-R1-R7_MULTI_SEGMENT_MEASURED_SOAK_CONTINUITY_CROSS_RESTART_LEDGER_CHAIN_ROUTE_BUDGET_ACCUMULATION_GATE`
- Parent execution: `decode04r4r5r1r7-180456f976c1439274b9`
- Parent lineage: `180456f976c1439274b9bd82b1ee4be0b04c3a4397d9d365f626ca096295d386`
- Evidence epoch: `r4r5r1r5-epoch-3fe343d135e6216bf4cf`
- PASS authorizes only: `ASH-TCU-DECODE-04-R4-R5-R2`
- Legacy removal: `false`
- Legacy decoder retirement: `false`
- General production apply: `false`

## Purpose

R8 is the final R4-R5-R1 budget-closure gate.

It resumes the exact R7 ledger chain over any number of explicit invocations. Each invocation may commit bounded additional measured production segments and then returns:

```text
HOLD while any final budget remains
PASS only when every final budget closes
FAIL on any truth, identity, chain, durability, or correctness violation
```

R8 never converts process uptime, sleep, CLI duration, fixture duration, estimated counters, or static performance arithmetic into production evidence.

## Exact parent

Required parent facts:

```text
execution_id=decode04r4r5r1r7-180456f976c1439274b9
lineage_bundle_digest=180456f976c1439274b9bd82b1ee4be0b04c3a4397d9d365f626ca096295d386
evidence_epoch_id=r4r5r1r5-epoch-3fe343d135e6216bf4cf
committed_segment_count=6
cumulative_live_generation_active_ns=45998100
cumulative_natural_generations=2200
cumulative_selected_tokens=55000
oracle_executed_selected_tokens=47670
oracle_skipped_selected_tokens=7330
r4_r5_r1_r8_authorized=true
decode04_r4_r5_r2_authorized=false
legacy_oracle_removal_authorized=false
legacy_decoder_retirement_authorized=false
```

## Resumable ownership

```text
R5 cumulative ledger
= active duration, segment chain, routes, traffic

R8 budget ledger
= oracle, replay, performance cohorts, final closure

R8 coordinator
= next segment index, deficit plans, worker token issuance, final verdict

R8 worker
= one process clock domain, one measured production segment, one CAS commit
```

The two durable ledgers must agree after every commit on:

```text
evidence epoch
segment count
last segment digest
active duration
generations
selected tokens
route generations
route selected tokens
route active duration
traffic classes
```

## Evidence continuity

Forbidden:

```text
--reset-evidence-epoch
--segment-active-seconds
--smoke-duration-evidence
sleep-based active accrual
process-elapsed active accrual
SystemTime active accrual
fixture-to-natural duration bridge
```

Required:

```text
evidence epoch unchanged
duration policy unchanged
oracle policy unchanged
runtime identity unchanged
strict segment index order
exact previous-segment digest chain
zero accepted forks
zero committed duplicates
one process-local monotonic clock domain per segment
zero cross-process Instant subtraction
```

## Final budgets

```text
live generation active duration >= 86400000000000 ns
promotion-eligible segments >= 6
natural generations >= 100000
selected tokens >= 3000000
```

Per route:

```text
generations >= 25000
selected tokens >= 600000
```

Oracle:

```text
executed selected tokens >= 1200000
skipped selected tokens >= 1200000
executed + skipped == cumulative selected tokens
```

Replay:

```text
natural production replay >= 10 percent of cumulative generations
legacy-only replay >= 10000
full-dual replay >= 10000
legacy-only replay per route >= 2500
full-dual replay per route >= 2500
restart-boundary replay >= 2000
rollback replay >= 2000
quarantine replay >= 1000
```

Traffic:

```text
live production-bound >= 25 percent
historical replay >= 25 percent
adversarial or rare-surface >= 25 percent
long-tail mixed >= 25 percent
all 19 corpus classes represented
```

## Performance closure

Final promotion requires a production-equivalent build profile and all sample budgets:

```text
legacy-only generations >= 10000
full-dual generations >= 10000
bounded-reduced generations >= 10000
per route, per performance class >= 2500 generations
```

Benefit policy:

```text
reduced throughput benefit >= 10 percent
OR reduced CPU-time benefit >= 25 percent
```

Floor:

```text
reduced throughput >= 75 percent of legacy-only throughput
```

Development-profile measurements remain diagnostic and cannot close final promotion.

## Correctness

Required zero over the full evidence epoch:

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
stale selector-state reuse
quarantine loss
rollback loss
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

TensorCube remains fragment-only.

## Canonical binary

```text
ash_tcu_decode_04_r4_r5_r1_r8_measured_soak_budget_closure_gate
```

The same executable runs hidden internal workers. Users run only the coordinator command.

Recommended bounds:

```text
--max-additional-segments-per-invocation 8
--segment-max-wall-seconds 3600
--segment-max-generations 20000
--segment-min-generations 100
--restart-profile budget_closure_continuity_matrix
--production-duration-evidence
--continue-existing-evidence-epoch
```

Operational bounds do not grant evidence credit.

## HOLD

HOLD is expected while any budget remains.

```text
bounded_oracle_reduction_production_soak_proven=false
decode04_r4_r5_r2_authorized=false
legacy_oracle_reduction_steady_state_authorized=false
legacy_oracle_removal_authorized=false
legacy_decoder_retirement_authorized=false
general_production_apply_authorized=false
```

The same command is rerun without resetting the epoch.

## PASS

Marker:

```text
PASS_ASH_TCU_DECODE_04_R4_R5_R1_R8_MEASURED_SOAK_BUDGET_CLOSURE_FULL_ROUTE_ORACLE_REPLAY_BUDGET_24_HOUR_ACTIVE_RUNTIME_PROMOTION_GATE
```

PASS requires all final budgets, correctness, identity, chain, recovery, durability, and performance checks.

PASS authority:

```text
bounded_oracle_reduction_production_soak_proven=true
decode04_r4_r5_r2_authorized=true
legacy_oracle_reduction_active=true
legacy_oracle_reduction_steady_state_authorized=false
legacy_oracle_removal_authorized=false
legacy_decoder_retirement_authorized=false
general_production_apply_authorized=false
```

R8 authorizes R4-R5-R2 review. It does not activate steady-state production.

## Next gate

```text
ASH-TCU-DECODE-04-R4-R5-R2
Bounded Oracle Reduction Steady-State Promotion /
Production Admission Transaction /
Rollback and Telemetry Gate
```