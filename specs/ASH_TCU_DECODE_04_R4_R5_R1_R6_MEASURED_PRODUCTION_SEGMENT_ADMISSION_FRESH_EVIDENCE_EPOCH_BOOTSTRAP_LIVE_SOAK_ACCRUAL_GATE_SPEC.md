# ASH-TCU-DECODE-04-R4-R5-R1-R6
# Measured Production Segment Admission / Fresh Evidence Epoch Bootstrap / Live Soak Accrual Gate

- Patch ID: `ASH-TCU-DECODE-04-R4-R5-R1-R6_MEASURED_PRODUCTION_SEGMENT_ADMISSION_FRESH_EVIDENCE_EPOCH_BOOTSTRAP_LIVE_SOAK_ACCRUAL_GATE`
- Parent repair: `ASH-TCU-DECODE-04-R4-R5-R1-R5_ACTIVE_RUNTIME_EVIDENCE_OWNERSHIP_NO_SLEEP_BASED_SOAK_ACCRUAL_LIVE_GENERATION_DURATION_RECEIPT_REPAIR`
- Parent soak: `ASH-TCU-DECODE-04-R4-R5-R1_BOUNDED_ORACLE_REDUCTION_PRODUCTION_SOAK_RESTART_RECOVERY_GATE`
- Runtime role: first promotion-eligible R5 production segment
- Duration SSOT: validated R5 live-generation nanosecond ledger
- PASS authorizes only: `ASH-TCU-DECODE-04-R4-R5-R1-R7_MULTI_SEGMENT_MEASURED_SOAK_CONTINUITY_RESTART_MATRIX_GATE`
- R4-R5-R2 authorization: false
- Legacy removal: false
- Legacy decoder retirement: false
- General production apply: false

## Purpose

R5 proved in smoke mode that active runtime is measured by monotonic live-generation receipts and that sleep, idle, fixture, startup, and artifact-I/O intervals contribute zero production duration.

R6 performs the first production-eligible commit under that repaired clock.

R6 proves:

```text
fresh production evidence epoch
segment_index=0
production_duration_evidence=true
smoke_duration_evidence=false
pre-R5 duration contribution=0
R5 smoke duration contribution=0
live four-route generations
measured generation duration receipts
validated segment duration equation
first cumulative-ledger commit
restart/rollback/quarantine/identity matrix rebind
parent soak remains HOLD
```

R6 starts trustworthy measured soak accumulation. It does not complete the 24-hour soak.

## Exact parents

R5 parent:

```text
execution_id=decode04r4r5r1r5-6d66e112ea02d69d1b51
lineage_bundle_digest=6d66e112ea02d69d1b510d8b8dc6fa0581f7bdcd40ddc2e77ce97280e478fc4a
r4_r5_r1_r5_active_runtime_evidence_repair_pass=true
r4_r5_r1_production_soak_may_resume=true
pre_r5_duration_contribution_ns=0
segment_smoke_mode=true
segment_promotion_eligible=false
cumulative_live_generation_active_ns=0
bounded_oracle_reduction_production_soak_proven=false
decode04_r4_r5_r2_authorized=false
legacy_oracle_removal_authorized=false
legacy_decoder_retirement_authorized=false
```

R4-R5 parent:

```text
execution_id=decode04r4r5-0eef9e9aed02619a00d1
lineage_bundle_digest=0eef9e9aed02619a00d151fee113f925b34c03fe4c1b22c74a4c75b1cdd66593
legacy_fragment_retirement_readiness_proven=true
bounded_oracle_reduction_ready=true
tensorcube_default_fragment_authority=true
production_fragment_apply_authorized=true
general_production_apply_authorized=false
legacy_oracle_removal_authorized=false
legacy_decoder_retirement_authorized=false
```

## Duration ownership

```text
CLI max-wall/max-generations/min-generations = stop-policy inputs only
per-generation active duration = monotonic live-generation timer
segment active duration = sum(validated promotion-eligible natural generation receipts)
cumulative active duration = committed R5 segment ledger
```

Forbidden accrual sources:

```text
segment-active-seconds
sleep
process elapsed
SystemTime delta
startup
idle
restart delay
fixture drills
artifact serialization or flush
manifest writing
pre-R5 state
R5 smoke state
```

## Fresh production epoch

The existing R5 smoke epoch is archived as repair-only evidence.

```text
smoke duration contribution=0
pre-R5 duration contribution=0
```

A new production epoch and empty cumulative ledger are created.

Before first commit:

```text
segment_count=0
promotion_eligible_segment_count=0
cumulative_live_generation_active_ns=0
```

After first commit:

```text
segment_count=1
promotion_eligible_segment_count=1
smoke_segment_count=0
cumulative_live_generation_active_ns>0
```

## First production segment bootstrap

Required routes:

```text
greedy_cached
sampled_cached
greedy_streaming
sampled_streaming
```

Bootstrap minimum:

```text
natural generations >=100
selected tokens >=2500
generations per route >=25
selected tokens per route >=500
all four traffic classes
all 19 corpus classes
```

The implementation selects a parent-receipt-backed 200-generation bootstrap, 50 per route, with enough full-dual generations to satisfy:

```text
startup full-dual generations >=64
startup full-dual selected tokens >=4096
```

It also selects reduced-mode parent receipts so both values are positive:

```text
oracle_executed_selected_tokens>0
oracle_skipped_selected_tokens>0
```

Required accounting:

```text
oracle_executed_selected_tokens + oracle_skipped_selected_tokens = selected_token_count
```

Skipped-oracle parity remains `NotObserved` and is never reported as PASS.

## Duration equations

```text
segment_live_generation_active_ns = sum(validated promotion-eligible natural generation_active_ns)
sum(route_active_ns) = segment_live_generation_active_ns
cumulative_active_ns_before=0
cumulative_active_ns_after = segment_live_generation_active_ns
```

Required:

```text
segment_live_generation_active_ns>0
segment_live_generation_active_ns<=process_monotonic_elapsed_ns
fixture duration contribution=0
sleep contribution=0
idle contribution=0
artifact-I/O contribution=0
```

## Receipt and ledger integrity

Required:

```text
generation receipt digest chain
unique generation IDs
strict monotonic ordinals
segment generation Merkle root
token timing root
output receipt root
oracle decision root
segment digest
ledger digest chain
atomic replace-existing write
idempotent segment commit
segment fork rejection
```

Duplicate submission contributes zero additional duration, generations, tokens, or segment count.

## Restart and safety matrix rebind

Required:

```text
restart events >=28
rollback drills >=16
quarantine drills >=16
identity-drift drills >=10
fixture duration contribution=0
```

Restart time outside admitted natural generations contributes zero active runtime.

No cross-process `Instant` subtraction is permitted.

Unfinished segments are not committed and orphan duration is excluded.

## Replay bootstrap

```text
legacy-only replay generations >=100
full-dual replay generations >=100
restart-boundary replay generations >=20
rollback replay generations >=20
quarantine replay generations >=10
```

Replay bootstrap fixtures contribute zero natural production active duration.

## Correctness

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
stream chunk sequence
stream chunk boundary
token sequence
KV owner/content
DecodeState
sampler state
RNG state
finish/stop
runtime route
```

TensorCube remains fragment-only and does not own token selection, sampler, RNG, KV, DecodeState, finish/stop, or route selection.

## Performance bootstrap

```text
timer overhead p99 <=100 us
receipt reduction p99 <=500 us
unbounded allocation count=0
```

The final production benefit threshold remains a parent-soak budget and may remain HOLD after R6.

## Canonical owners

```text
R4R5R1R6FirstProductionSegmentPolicy
R4R5R1R6ProductionSegmentAdmissionReceipt
R4R5R1R6EpochBootstrapReceipt
R4R5R1R6MatrixRebindReceipt
R4R5R1R6ProductionSegmentCommitReceipt
R4R5R1R6HoldSummary
R4R5R1R6PromotionVerdict
```

Single-owner requirement:

```text
first production-segment policy owner=1
production-segment admission reducer=1
epoch bootstrap reducer=1
runtime matrix rebind reducer=1
segment commit reducer=1
HOLD summary reducer=1
promotion verdict reducer=1
```

## Canonical binary

```text
ash_tcu_decode_04_r4_r5_r1_r6_measured_production_segment_admission_gate
```

## Required CLI values

```text
--repo-root <PATH>
--r4-r5-parent-manifest <PATH>
--r4-r5-r1-r5-parent-manifest <PATH>
--runtime-profile <PATH>
--segment-max-wall-seconds <SECONDS>
--segment-max-generations <COUNT>
--segment-min-generations <COUNT>
--restart-profile scheduled_matrix
--reset-evidence-epoch
--production-duration-evidence
```

`--segment-active-seconds` and `--smoke-duration-evidence` are forbidden.

Required activation seals include:

```text
--authorize-first-measured-production-segment
--activate-r5-duration-ledger
--activate-live-generation-timing
--activate-generation-duration-receipts
--activate-segment-duration-receipts
--activate-cumulative-active-runtime-ledger
--activate-bounded-oracle-reduction-production-soak
--activate-live-production-traffic
--activate-live-four-route-runtime
--activate-periodic-full-dual-windows
--activate-risk-triggered-oracle-reexpansion
--activate-durable-publication-journal
--activate-durable-quarantine
--activate-restart-recovery
--activate-operator-rollback-sla
--activate-identity-drift-fail-closed
```

Required truth seals include:

```text
--require-parent-r5-pass
--require-parent-r5-repair-pass
--require-parent-soak-may-resume
--require-parent-pre-r5-contribution-zero
--require-parent-smoke-not-promotion-eligible
--require-parent-cumulative-active-zero
--require-parent-r4-r5-pass
--require-production-duration-evidence
--require-no-smoke-duration-evidence
--require-no-segment-active-seconds
--require-no-sleep-based-accrual
--require-no-process-elapsed-accrual
--require-no-system-time-accrual
--require-no-pre-r5-duration-contribution
--require-no-smoke-duration-contribution
--require-first-promotion-eligible-segment-index-zero
--require-idempotent-segment-commit
--require-no-segment-fork
--require-generation-duration-receipts
--require-segment-duration-equation
--require-route-duration-equation
--require-cumulative-before-zero
--require-cumulative-after-equals-segment
--require-cumulative-after-positive
--require-oracle-accounting-exact
--require-minimum-28-restart-events
--require-minimum-16-rollback-drills
--require-minimum-16-quarantine-drills
--require-minimum-10-identity-drift-drills
--require-fixture-duration-contribution-zero
--require-zero-unexpected-mismatch
--require-zero-output-divergence
--require-zero-candidate-byte-leak
--require-hold-after-first-segment
--require-no-r4-r5-r2-authorization
--require-no-legacy-removal
--require-no-legacy-retirement
--require-no-general-production-apply
--write-runtime-artifacts
--write-local-manifest
```

## PASS marker

```text
PASS_ASH_TCU_DECODE_04_R4_R5_R1_R6_MEASURED_PRODUCTION_SEGMENT_ADMISSION_FRESH_EVIDENCE_EPOCH_BOOTSTRAP_LIVE_SOAK_ACCRUAL_GATE
```

PASS authority:

```text
r4_r5_r1_r6_first_production_segment_pass=true
r4_r5_r1_measured_production_soak_started=true
r4_r5_r1_r7_authorized=true
bounded_oracle_reduction_production_soak_proven=false
decode04_r4_r5_r2_authorized=false
legacy_oracle_reduction_active=true
legacy_oracle_reduction_steady_state_authorized=false
legacy_oracle_removal_authorized=false
legacy_decoder_retirement_authorized=false
general_production_apply_authorized=false
```

R6 PASS means the first measured production segment is valid and committed. The parent soak must remain HOLD.

## Next gate

```text
ASH-TCU-DECODE-04-R4-R5-R1-R7
Multi-Segment Measured Soak Continuity /
Cross-Restart Ledger Chain /
Route Budget Accumulation Gate
```