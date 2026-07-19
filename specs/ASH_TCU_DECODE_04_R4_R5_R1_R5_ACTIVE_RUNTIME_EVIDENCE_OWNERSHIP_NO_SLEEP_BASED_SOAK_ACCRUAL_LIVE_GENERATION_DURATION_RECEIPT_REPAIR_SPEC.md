# ASH-TCU-DECODE-04-R4-R5-R1-R5
# Active Runtime Evidence Ownership / No Sleep-Based Soak Accrual / Live Generation Duration Receipt Repair

- Patch ID: `ASH-TCU-DECODE-04-R4-R5-R1-R5_ACTIVE_RUNTIME_EVIDENCE_OWNERSHIP_NO_SLEEP_BASED_SOAK_ACCRUAL_LIVE_GENERATION_DURATION_RECEIPT_REPAIR`
- Parent gate: `ASH-TCU-DECODE-04-R4-R5-R1_BOUNDED_ORACLE_REDUCTION_PRODUCTION_SOAK_RESTART_RECOVERY_GATE`
- Repair parent: `ASH-TCU-DECODE-04-R4-R5-R1-R4_WINDOWS_ATOMIC_REPLACE_EXISTING_REPAIR`
- Authority change: none
- Oracle policy change: none
- Legacy removal: false
- Legacy retirement: false
- R4-R5-R2 authorization: false until repaired soak evidence completes

## Purpose

The pre-R5 soak controller accepted `--segment-active-seconds` and could fill the requested interval with `thread::sleep`. Process lifetime and sleep completion are not live generation evidence.

R5 transfers duration authority to monotonic per-generation measurement and content-addressed receipts.

```text
requested duration != earned duration
process uptime != live generation duration
sleep interval != active runtime evidence
```

Canonical equation:

```text
cumulative_live_generation_active_ns
= sum(validated promotion-eligible segment live-generation active ns)

segment_live_generation_active_ns
= sum(validated natural generation active ns)
```

No other source may increase the production-soak active-runtime counter.

## Duration owners

```text
stop-policy owner
= CLI upper bounds

per-generation duration owner
= monotonic live-generation timer

segment duration owner
= validated generation duration receipts

cumulative duration owner
= committed segment receipt ledger

promotion threshold owner
= cumulative_live_generation_active_ns
```

The operator controls how long execution is allowed to continue. The runtime controls how much active time was earned.

## Included time

Only the admitted natural-generation transaction counts:

```text
generation admission after route resolution
production selected-token loop
production KV progression
TensorCube fragment decode
legacy oracle execution when selected
comparison when oracle executes
publication transaction
finish/stop finalization
```

## Excluded time

```text
Cargo compilation
process startup
manifest/model/tokenizer/checkpoint loading
CLI parsing
parent admission
static scans
fixture-only drills
restart delay
operator pause
idle queue wait
sleep
artifact serialization and flush
report rendering
manifest writing
shutdown
```

Fixture duration remains telemetry and contributes zero natural active time.

## Monotonic clock

Per-process measurement uses `std::time::Instant`.

Forbidden duration authorities:

```text
SystemTime delta
UTC timestamp delta
filesystem timestamps
caller-provided elapsed seconds
PID lifetime estimate
process elapsed copied into active duration
```

UTC timestamps may record ordering only.

## CLI repair

Removed:

```text
--segment-active-seconds
--segment-generations
```

Added:

```text
--segment-max-wall-seconds <SECONDS>
--segment-max-generations <COUNT>
--segment-min-generations <COUNT>
--production-duration-evidence
--smoke-duration-evidence
```

Exactly one evidence mode is required.

`segment-max-wall-seconds` is a stop bound. It grants no duration credit and does not cause a wait to fill the requested interval.

## Existing ledger disposition

Any pre-R5 R4-R5-R1 ledger is content-addressed and marked:

```text
disposition=ArchivedAsPreR5Inadmissible
contribution_to_r5_active_runtime_ns=0
```

No pre-R5 active-runtime value is migrated.

The safest migration starts all promotion budgets in a fresh R5 evidence epoch.

## Evidence epoch

Every generation and segment binds:

```text
parent execution ID
parent lineage digest
repair patch ID
runtime binary digest
duration policy digest
evidence epoch ID
```

Receipts from different evidence epochs cannot be summed.

## Live generation duration receipt

Each counted generation records:

```text
evidence epoch ID
segment ID
generation ID
route
traffic class
prompt identity
model, weight, tokenizer, route, and oracle-policy identity
authority epoch
natural-generation flag
promotion-eligible flag
terminal state
selected-token count
generation active ns
decode, oracle, comparison, publication, and durability ns
excluded idle, sleep, and artifact-I/O ns
process-local monotonic ordinals
previous generation receipt digest
receipt digest
```

Required:

```text
promotion-eligible natural generation -> generation_active_ns > 0
monotonic_end >= monotonic_start
component duration sum <= generation_active_ns
excluded duration does not increase generation_active_ns
```

## Segment receipt

A segment records:

```text
process monotonic elapsed ns
measured live generation active ns
fixture active ns
excluded startup, idle, sleep, and artifact-I/O ns
natural and fixture generation counts
selected-token count
route generation, token, and active-duration maps
traffic-class counts
generation receipt chain endpoints and Merkle root
previous segment digest
stop reason
segment digest
```

Required equations:

```text
measured_live_generation_active_ns
= sum(validated natural generation_active_ns)

sum(route_active_ns)
= measured_live_generation_active_ns

measured_live_generation_active_ns
<= process_monotonic_elapsed_ns
```

## Cumulative ledger

The R5 ledger stores:

```text
evidence epoch
promotion-eligible and smoke segment counts
cumulative live-generation active ns
cumulative fixture active ns
natural generations and selected tokens
route and traffic counters
committed segment IDs
segment digest chain and Merkle root
prior-ledger disposition digest
ledger digest
```

Only promotion-eligible segments increase natural duration, generation, token, route, and traffic counters.

Smoke segments may be committed for diagnostics but add zero production-soak active duration.

## Atomicity and idempotency

Ledger update order:

```text
validate evidence epoch
validate prior ledger digest
validate segment and generation receipt chain
validate duration equations
compute new ledger
write temporary file
flush
replace existing atomically
commit update receipt
```

Windows replacement uses `MoveFileExW` with:

```text
MOVEFILE_REPLACE_EXISTING
MOVEFILE_WRITE_THROUGH
```

Duplicate key:

```text
evidence_epoch_id + segment_id + segment_receipt_digest
```

A duplicate returns `AlreadyCommitted` behavior and changes no counters.

## Restart continuity

`Instant` domains are process-local. No subtraction is allowed across restarts.

Cross-restart continuity uses:

```text
committed segment digest chain
cumulative ledger digest chain
restart receipt
fresh process clock domain
UTC ordering metadata
```

An unfinished segment contributes zero duration. Orphan generation receipts are not reconstructed into promotion evidence by default.

## Static prohibitions

The repaired soak source must contain no semantic path that:

```text
adds CLI seconds to the ledger
uses sleep to reach requested active duration
copies process elapsed into active duration
uses SystemTime as duration authority
adds fixture time to natural active time
reuses pre-R5 duration
```

The static audit scans explicit source files and avoids counting its own search literals.

## Duration-integrity drills

Required:

```text
stop-bound independence
sleep exclusion
idle exclusion
artifact-I/O exclusion
fixture exclusion
clock-domain reset
unclean segment discard
duplicate segment idempotency
duration-receipt tamper rejection
```

The sleep-exclusion drill may deliberately sleep, but the measured sleep is recorded only in `excluded_sleep_ns` and adds zero active time.

## Measurement overhead

Required telemetry:

```text
timer start/stop p50 and p99
receipt reduction p50 and p99
```

Policy:

```text
timer overhead p99 <= 100 us per generation
receipt reduction p99 <= 500 us per generation
```

## Smoke mode

Canonical controls:

```text
--segment-max-wall-seconds 30
--segment-max-generations 100
--segment-min-generations 1
--smoke-duration-evidence
```

Expected:

```text
measured_live_generation_active_ns > 0
segment_promotion_eligible=false
cumulative_live_generation_active_ns=0
```

Smoke verifies wiring and does not advance the production soak.

## Production mode

Example controls:

```text
--segment-max-wall-seconds 7200
--segment-max-generations 10000
--segment-min-generations 100
--production-duration-evidence
```

The runtime continuously admits work while bounds allow. It does not sleep to fill the wall bound. Only measured generation transaction time enters the production ledger.

## 24-hour threshold

The R4-R5-R1 budget remains:

```text
cumulative_live_generation_active_ns >= 86_400_000_000_000
```

Rounded hours or process lifetime cannot decide PASS.

If the runtime performs work quickly and then idles, earning 24 active hours may require more than 24 calendar hours. This is intentional.

## Repair binary

```text
ash_tcu_decode_04_r4_r5_r1_r5_active_runtime_evidence_ownership_repair_gate
```

## Repair gate CLI seals

```text
--authorize-active-runtime-evidence-repair
--activate-fresh-r5-evidence-epoch
--activate-live-generation-timing
--activate-generation-duration-receipts
--activate-segment-duration-receipts
--activate-cumulative-active-runtime-ledger
--activate-pre-r5-ledger-disposition
--require-no-sleep-based-soak-accrual
--require-no-cli-declared-active-duration
--require-no-process-elapsed-active-duration
--require-no-system-time-active-duration
--require-no-fixture-duration-promotion
--require-no-cross-epoch-duration-sum
--require-no-incomplete-segment-duration-promotion
--require-no-duplicate-segment-accrual
--require-monotonic-generation-timer
--require-generation-duration-digest-chain
--require-segment-duration-merkle-root
--require-ledger-digest-chain
--require-idempotent-segment-commit
--require-windows-atomic-replace-existing
--require-unclean-segment-discard
--require-cross-restart-clock-domain-separation
--run-stop-bound-independence-drill
--run-sleep-exclusion-drill
--run-idle-exclusion-drill
--run-artifact-io-exclusion-drill
--run-fixture-exclusion-drill
--run-clock-reset-drill
--run-unclean-segment-drill
--run-duplicate-segment-drill
--run-duration-receipt-tamper-drill
--require-single-duration-policy-owner
--require-single-live-generation-timer-owner
--require-single-generation-duration-reducer
--require-single-segment-duration-reducer
--require-single-cumulative-active-runtime-ledger-owner
--require-single-duration-integrity-reducer
--require-single-promotion-verdict-reducer
--write-runtime-artifacts
--write-local-manifest
```

## Repair PASS

Marker:

```text
PASS_ASH_TCU_DECODE_04_R4_R5_R1_R5_ACTIVE_RUNTIME_EVIDENCE_OWNERSHIP_NO_SLEEP_BASED_SOAK_ACCRUAL_LIVE_GENERATION_DURATION_RECEIPT_REPAIR
```

PASS requires:

```text
pre-R5 contribution = 0
fresh evidence epoch
monotonic generation timing
generation and segment receipt equations
ledger digest chain
no sleep, CLI, process-elapsed, SystemTime, or fixture accrual
duplicate commit idempotency
unclean segment discard
tamper rejection
Windows atomic replacement
all duration-integrity drills
all truth checks
```

Expected authority:

```text
r4_r5_r1_r5_active_runtime_evidence_repair_pass=true
r4_r5_r1_production_soak_may_resume=true
bounded_oracle_reduction_production_soak_proven=false
decode04_r4_r5_r2_authorized=false
legacy_oracle_reduction_active=true
legacy_oracle_reduction_steady_state_authorized=false
legacy_oracle_removal_authorized=false
legacy_decoder_retirement_authorized=false
general_production_apply_authorized=false
```

R5 repair PASS proves the clock and ledger are trustworthy. It does not complete the soak.

## Resumed R4-R5-R1 PASS

After repair, R4-R5-R1 can PASS only when measured R5 production evidence satisfies:

```text
live generation active duration >= 24 hours
promotion-eligible segments >= 6
natural generations >= 100000
selected tokens >= 3000000
all route, oracle, replay, restart, rollback, quarantine, identity, correctness, and performance budgets
```

Only then:

```text
bounded_oracle_reduction_production_soak_proven=true
decode04_r4_r5_r2_authorized=true
```

Legacy removal and decoder retirement remain forbidden.