# ASH-TCU-DECODE-04-R4-R5
# Legacy Fragment Retirement Readiness / Oracle Reduction Gate

- Patch ID: `ASH-TCU-DECODE-04-R4-R5_LEGACY_FRAGMENT_RETIREMENT_READINESS_ORACLE_REDUCTION_GATE`
- Parent: `ASH-TCU-DECODE-04-R4-R4-R4_TENSORCUBE_DEFAULT_FRAGMENT_AUTHORITY_LEGACY_ORACLE_RETENTION_GATE`
- Default fragment source: TensorCube
- Parent oracle mode: 100 percent mandatory legacy oracle
- Gate mode: bounded deterministic oracle-reduction readiness evaluation
- Legacy fallback: mandatory
- Durable quarantine: mandatory
- Restart recovery: mandatory
- General production apply: false
- Legacy retirement: false
- PASS authorizes only: `ASH-TCU-DECODE-04-R4-R5-R1_BOUNDED_ORACLE_REDUCTION_PRODUCTION_SOAK_RESTART_RECOVERY_GATE`

## Parent admission

Known parent:

```text
execution_id=decode04r4r4r4-b319267894cf540535e2
lineage_bundle_digest=b319267894cf540535e2aa73dd8ad4bc6b91ee5ba36f48d463255d85fda6561b
default source=tensorcube
route coverage=4/4
default-authority generations=10000
selected tokens=241200
legacy oracle fragments=241200
legacy oracle bypass=0
natural mismatch=0
natural revocation=0
natural quarantine=0
output divergence=0
candidate byte leak=0
performance policy pass=true
```

The exact parent manifest, parent policy evidence, model, weights, tokenizer, runtime route, quarantine matrix, and performance evidence are content-bound.

## Purpose

R4-R5 evaluates whether legacy oracle execution can be reduced from 100 percent under a deterministic, route-aware, reversible policy while preserving output correctness, mismatch detection, exact fallback, legacy-only boot, durable quarantine, restart recovery, operator rollback, identity invalidation, and telemetry integrity.

R4-R5 does not activate reduced-oracle production. It proves readiness for a later controlled soak.

## Non-authority

This gate does not authorize:

```text
legacy decoder deletion
legacy oracle removal
candidate-only production
zero-oracle steady state
TensorCube token selection
TensorCube sampler or RNG ownership
TensorCube KV or DecodeState ownership
general production apply
```

## Oracle execution modes

```text
FullDualRun
DeterministicGenerationSample
DeterministicTokenSample
PeriodicFullWindow
TriggeredFullDualRun
QuarantineLegacyOnly
OperatorForcedLegacyOnly
```

No permanent disabled-oracle mode exists. Every reduced mode must transition to full-dual or legacy-only at the next safe boundary.

## Route policy

Minimum generation-level full-dual coverage:

| Route | Minimum |
|---|---:|
| greedy cached | 1/8 |
| sampled cached | 1/4 |
| greedy streaming | 1/4 |
| sampled streaming | 1/2 |

Minimum token-level oracle spot checks outside full-dual generations:

| Route class | Minimum |
|---|---:|
| cached | 1/16 |
| streaming | 1/8 |

Streaming keeps higher oracle coverage because skipped steps cannot provide immediate compare-before-emit detection.

## Deterministic selector

The selector binds policy digest, authority epoch, generation ID, route, prompt identity digest, sampler profile digest, seed identity, and selected-token step.

Selection uses a stable SHA-256-derived integer modulo the route denominator.

Forbidden selector inputs:

```text
production RNG
wall clock
PID
thread ID
pointer or allocation address
host name
environment ordering
```

The same identity tuple must produce the same oracle decision across process and host restarts.

## Parity truth

```text
oracle executed -> parity may be Pass or Fail
oracle skipped -> parity status must be NotObserved
```

An oracle-skipped step may never be reported as parity true.

## Full-dual windows

Startup window:

```text
at least 32 full-dual generations
and at least 2048 full-dual selected tokens
reduction begins only after both complete
```

Post-restart window:

```text
at least 64 full-dual generations
and at least 4096 full-dual selected tokens
```

Periodic windows:

```text
at least 32 full-dual generations every 512 generations
at least 256 full-dual selected tokens every 4096 selected tokens
```

Model, tokenizer, route, or policy identity change disables reduction and requires new full-dual evidence.

## Risk-triggered escalation

Triggers include unknown token classification, unseen token ID, unseen piece transition, pending-byte anomaly, invalid UTF-8 candidate, stream sink atomicity loss, latency or memory outlier, telemetry integrity warning, and operator diagnostic request.

Required severity examples:

```text
unknown token classification -> Quarantine
invalid UTF-8 -> AbortBeforeOutput
telemetry integrity failure -> Quarantine
stream sink atomicity loss -> AbortBeforeOutput
latency or memory outlier -> EscalateNextGeneration
```

No retroactive parity claim is allowed for already skipped steps.

## Detection-latency policy

Oracle-skipped mismatch injections must prove bounded delayed detection.

| Route class | Generations | Selected tokens |
|---|---:|---:|
| cached | 512 | 4096 |
| streaming | 128 | 1024 |

The gate records first full-dual detection and quarantine activation boundaries.

## Durable quarantine

Canonical active record:

```text
workspace/runtime/tensorcube/quarantine/
ash_tensorcube_decode_04_r4_r5_active_quarantine.json
```

Required:

```text
atomic write
record digest validation
restart and reboot persistence
corrupt record fails closed to LegacyDefault
operator acknowledgement required
no timer-based clear
no restart auto-clear
no file-deletion-only clear
```

Clearing requires diagnostic replay PASS, full-dual recovery PASS, explicit operator acknowledgement, and a fresh authority epoch.

## Restart recovery

Required cases:

```text
clean shutdown during reduced mode
unclean shutdown between generations
unclean cached transaction
unclean streaming transaction
restart with active quarantine
restart with corrupt quarantine
restart after operator rollback
restart after policy change
```

Uncertain generations never resume partially. Unsealed candidate state is discarded, duplicate and mixed output are forbidden, and restart begins in LegacyDefault or FullDualRun.

## Operator rollback drills

Required drills:

```text
pre-boot force legacy
runtime-session force legacy
rollback after reduced generation
rollback after full-dual generation
rollback during pending escalation
rollback with active quarantine
rollback after restart
```

Rollback becomes effective no later than the next generation boundary. Clearing requires explicit action, identity and policy revalidation, a full-dual recovery window, and a fresh authority epoch.

## Corpus and evidence

Minimum readiness evidence:

```text
total generations >= 20000
total selected tokens >= 500000
route coverage = 4/4
corpus classes = 19/19
per route generations >= 5000
per route selected tokens >= 100000
full-dual generations >= 5000
reduced-oracle generations >= 15000
oracle-executed selected tokens >= 200000
oracle-skipped selected tokens >= 200000
legacy-only replay generations >= 2000
```

The corpus includes all R4-R4-R3 and R4-R4-R4 identities or a strict content-addressed superset. Long-context and generation-length bands contain both full-dual and reduced-oracle evidence.

## Failure injection

Required classes:

```text
candidate byte mismatch
decision mismatch
context mismatch
pending-byte mismatch
sequence-index mismatch
candidate invariant failure
invalid UTF-8
stream sink atomicity loss
telemetry integrity failure
quarantine corruption
rollback corruption
policy mismatch
identity drift
cached crash
streaming crash
```

Injections cover oracle-executed steps, oracle-skipped steps, startup boundaries, periodic-window boundaries, and post-restart boundaries.

## Output and state parity

Natural reduced-oracle output must match both legacy-only and full-dual replay for selected-token sequence, output bytes, stream chunks and boundaries, KV, DecodeState, sampler, RNG, finish reason, and route.

TensorCube production mutation outside fragment publication remains zero.

## Performance

Measured modes include legacy-only, 100 percent full-dual, generation-sampled, token-sampled, periodic-window, triggered full-dual, and quarantine legacy-only.

Per route, at least one benefit must pass:

```text
reduced throughput >= 110 percent of full-dual throughput
or
legacy oracle CPU time reduced >= 25 percent
```

Additional limits:

```text
reduced throughput >= 70 percent of legacy-only
selector overhead p99 <= 100 us
quarantine lookup p99 <= 1 ms
cold legacy fallback p99 <= 250 ms
unbounded allocation = 0
```

## Legacy path integrity

Required:

```text
legacy source present
legacy tokenizer binding present
legacy state constructor reachable
legacy-only runtime route reachable
fallback and restart drills pass
legacy-only replay >= 2000 generations
```

Dead-code-only legacy retention fails readiness.

## SSOT

```text
R4R5OracleReductionPolicy
R4R5OracleExecutionMode
R4R5OracleSelectionDecision
R4R5DeterministicOracleSelector
R4R5FullDualWindow
R4R5RiskTrigger
R4R5DurableQuarantineRecord
R4R5RestartRecoveryReceipt
R4R5OperatorRollbackDrillReceipt
R4R5DetectionLatencySummary
R4R5RetirementReadinessSummary
R4R5RetirementReadinessVerdict
```

There is one owner each for policy, selector, full-window schedule, risk trigger, quarantine, restart recovery, rollback drill, and verdict reduction.

## Static and no-repair audit

Required zero:

```text
candidate-only steady-state mode
permanent oracle-disabled mode
production-RNG selector
route-local policy owner
self-referential static audit
lossy UTF-8
replacement fallback
fragment trim
whitespace collapse
Unicode normalization
invalid-byte skip
silent fragment drop
silent mismatch suppression
skipped-oracle parity pass
ignored quarantine
ignored rollback
ignored restart uncertainty
```

## Binary and PASS

```text
ash_tcu_decode_04_r4_r5_legacy_fragment_retirement_readiness_oracle_reduction_gate
PASS_ASH_TCU_DECODE_04_R4_R5_LEGACY_FRAGMENT_RETIREMENT_READINESS_ORACLE_REDUCTION_GATE
```

Expected authorization:

```text
decode04_r4_r5_r1_authorized=true
legacy_fragment_retirement_readiness_proven=true
bounded_oracle_reduction_ready=true
legacy_oracle_reduction_active=false
legacy_oracle_removal_authorized=false
legacy_decoder_retirement_authorized=false
tensorcube_default_fragment_authority=true
production_fragment_apply_authorized=true
general_production_apply_authorized=false
production token/KV/sampler/RNG authority=false
```

HOLD or FAIL grants no new authority.

## Next gate

`ASH-TCU-DECODE-04-R4-R5-R1 Bounded Oracle Reduction Production Soak / Restart Recovery Gate`

R4-R5-R1 may activate bounded oracle reduction in a controlled production soak while retaining periodic full-dual windows, risk-triggered escalation, durable quarantine, legacy-only restart, operator rollback, and identity invalidation.

Legacy removal remains forbidden.