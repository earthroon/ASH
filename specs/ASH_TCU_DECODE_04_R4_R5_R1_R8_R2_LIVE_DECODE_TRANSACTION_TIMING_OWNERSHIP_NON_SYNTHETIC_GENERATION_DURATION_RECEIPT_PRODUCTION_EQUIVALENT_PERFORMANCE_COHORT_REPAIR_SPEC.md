# ASH-TCU-DECODE-04-R4-R5-R1-R8-R2
# Live Decode Transaction Timing Ownership / Non-Synthetic Generation Duration Receipt / Production-Equivalent Performance Cohort Repair

- Patch ID: `ASH-TCU-DECODE-04-R4-R5-R1-R8-R2_LIVE_DECODE_TRANSACTION_TIMING_OWNERSHIP_NON_SYNTHETIC_GENERATION_DURATION_RECEIPT_PRODUCTION_EQUIVALENT_PERFORMANCE_COHORT_REPAIR`
- Parent execution: `decode04r4r5r1r8-e36e97b993bfbd5c7fe3`
- Parent lineage: `e36e97b993bfbd5c7fe3493b157fbe552fa91093d483df44dd5ff879ca1c1ba8`
- Parent epoch: `r4r5r1r5-epoch-3fe343d135e6216bf4cf`
- PASS authorizes only: `ASH-TCU-DECODE-04-R4-R5-R1-R8-R3`
- R8 final closure: `false`
- R4-R5-R2 authorization: `false`
- Legacy removal and retirement: `false`
- General production apply: `false`

## Problem

The parent R8 HOLD reported 34200 natural generations, 855000 selected tokens and only 68335200 ns of cumulative active time. The eight R8 workers added 32000 generations and 800000 selected tokens but only 22337100 ns. The measured interval therefore did not enclose the real decode transaction.

The parent performance cohort also reported throughput benefit `280506 ppm`, CPU benefit `-1098593 ppm`, and throughput floor `476509 ppm`. These values do not prove production-equivalent performance.

## Prior evidence disposition

R6 through current R8 evidence is retained only as structural audit evidence.

```text
parent disposition=ArchivedAsStructuralAuditOnly
parent promotion duration contribution=0
parent promotion generation contribution=0
parent promotion selected-token contribution=0
parent promotion oracle contribution=0
parent promotion performance contribution=0
```

Retained structural evidence includes segment-chain layout, restart recovery, fork and duplicate rejection, orphan exclusion, artifact compatibility, HOLD authority, and R4-R5-R2 non-authorization.

## Fresh measurement epoch

R8-R2 creates `r4r5r1r8r2-live-<measurement epoch digest>` with all promotion counters at zero. The parent epoch remains immutable and read-only.

The new epoch binds model, weights, tokenizer, runtime profile, duration policy, instrumentation digest, oracle policy, route policy, release binary, feature set, and hardware identity.

## Duration ownership

The only promotion-duration owner is `LiveDecodeTransactionGuard`.

The timer starts immediately before actual native model generation dispatch. It ends only after selected-token finalization, KV and DecodeState progression, sampler and RNG progression, stream and finish/stop journaling, and durable generation publication commit.

Excluded phases include startup, model/tokenizer/checkpoint load, sleep, idle, operator pause, fixture injection, report rendering, manifest serialization, post-commit aggregation, and shutdown.

## Non-synthetic live receipt

Every promotion-eligible generation receipt requires:

```text
model forward dispatch count > 0
GPU submission count > 0
GPU completion observed
selected token count > 0
selected tokens from live sampler
KV progression
DecodeState progression
durable publication receipt
positive monotonic transaction duration
oracle executed + oracle skipped == selected tokens
```

Rejected sources include constants, CLI values, counter-derived duration, throughput-derived duration, planned duration, replay-only metadata, fixture-only paths, and report reducers. R8-R2 injects at least eight invalid synthetic receipts and requires all to be rejected.

## Live smoke

Required:

```text
live natural generations >=400
live selected tokens >=10000
each route generations >=100
each route selected tokens >=2500
all four routes
all four traffic classes
all 19 corpus classes
all generation durations positive
no timing anomaly quarantine
```

Routes are `greedy_cached`, `sampled_cached`, `greedy_streaming`, and `sampled_streaming`.

## Production-equivalent performance cohorts

Fresh cohorts are `LegacyOnly`, `FullDual`, and `BoundedReduced`.

All cohorts use the same release binary, model, weights, tokenizer, runtime profile, route distribution, traffic distribution, corpus distribution, prompt and generation lengths, KV state class, hardware identity, warmup policy, and measurement implementation. Only the already-authorized oracle branch differs.

R8-R2 smoke requires at least 100 generations per cohort and 25 generations per route per cohort.

Canonical formulas:

```text
tokens_per_second_ppm = selected_tokens * 1000000000000000 / decode_transaction_active_ns
throughput_benefit_ppm = (reduced_tps - full_dual_tps) * 1000000 / full_dual_tps
cpu_benefit_ppm = (legacy_cpu_ns - reduced_cpu_ns) * 1000000 / legacy_cpu_ns
throughput_floor_ppm = reduced_tps * 1000000 / legacy_tps
```

Negative CPU benefit is never clamped. Throughput floor is measured, not estimated. R8-R2 proves the measurement pipeline only; final R8 performance budgets remain for R8-R3 and continuation.

## Instrumentation overhead

Required:

```text
timer p99 <100 us
receipt collection p99 <500 us
digest reduction p99 <500 us
journal update p99 <2 ms
```

No unbounded receipt buffer, recursive timing, full-ledger per-token scan, or generation-receipt embedding is allowed.

## Correctness and parity

All natural correctness counters must remain zero, including mismatch, quarantine, rollback, output divergence, candidate leak, duplicate or missing emit, invalid UTF-8, partial scalar, replacement fallback, stale state, panic, deadlock, watchdog, stuck generation, telemetry drop, and natural abort.

Required parity includes reduced/full-dual/legacy output equality, stream sequence and boundaries, token sequence, KV, DecodeState, sampler, RNG, finish/stop, and route parity.

TensorCube remains fragment-only and does not own token selection, sampler, RNG, KV, DecodeState, route, or finish/stop.

## Canonical binary

```text
ash_tcu_decode_04_r4_r5_r1_r8_r2_live_decode_transaction_timing_ownership_repair_gate
```

Required values:

```text
--repo-root <PATH>
--r4-r5-r1-r8-parent-manifest <PATH>
--runtime-profile <PATH>
--release-binary <PATH>
--measurement-epoch-action create_fresh
--duration-source live_decode_transaction
--performance-cohort-profile production_equivalent
--worker-generations 400
--worker-selected-token-target 10000
--performance-generations-per-cohort 100
```

Forbidden values include continuing or mutating the parent epoch, crediting parent counters, synthetic duration estimation, forced R8 PASS, forced R4-R5-R2, candidate-only, zero-oracle, and legacy removal.

## PASS marker

```text
PASS_ASH_TCU_DECODE_04_R4_R5_R1_R8_R2_LIVE_DECODE_TRANSACTION_TIMING_OWNERSHIP_NON_SYNTHETIC_GENERATION_DURATION_RECEIPT_PRODUCTION_EQUIVALENT_PERFORMANCE_COHORT_REPAIR
```

PASS authority:

```text
r4_r5_r1_r8_r2_live_timing_repair_pass=true
r4_r5_r1_r8_r3_authorized=true
r8_final_budget_closure_authorized=false
bounded_oracle_reduction_production_soak_proven=false
decode04_r4_r5_r2_authorized=false
legacy_oracle_reduction_active=true
legacy_oracle_reduction_steady_state_authorized=false
legacy_oracle_removal_authorized=false
legacy_decoder_retirement_authorized=false
general_production_apply_authorized=false
```

## Next gate

`ASH-TCU-DECODE-04-R4-R5-R1-R8-R3 Fresh Live Measurement Epoch Bootstrap / Real Decode Soak Restart / Promotion Budget Re-Accrual Gate`

R8-R3 consumes the exact R8-R2 PASS manifest and starts all promotion-sensitive soak counters from zero under the fresh measurement epoch.