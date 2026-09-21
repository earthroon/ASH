# TENSORCUBE-TABLE-R3

## PERSISTENT DEVICE SCHEDULER
## CROSS-WAVE AUTONOMOUS REFILL
## GENERATION-SCOPED INDIRECT DISPATCH CHAIN

```text
+ R2A PARALLEL COMPACTION PRESERVATION
+ GENERATION-SCOPED DEVICE SCHEDULER STATE
+ CROSS-WAVE AUTONOMOUS READY REFILL
+ DEVICE-SIDE QUIESCENCE DETECTION

+ MUON READY -> CONSUME -> STATUS -> REFILL CHAIN
+ BP-DK PARAMETER READY CLAIM PLANE
+ SUCCESSOR READY CLAIM PLANE

+ DEVICE-RESIDENT PROGRESS / TERMINAL STATE
+ BOUNDED SCHEDULER SUPER-WAVE
+ FAIL-CLOSED ROUND-LIMIT / NO-PROGRESS / LIVELOCK GATES

+ ZERO HOST WAVE ENUMERATION
+ ZERO READY-COUNT HOST ROUNDTRIP
+ ZERO PER-WAVE HOST RANGE REBUILD
+ ZERO FULL-TABLE READBACK

+ B06 PUBLICATION AUTHORITY PRESERVATION
+ BP-DK DURABILITY AUTHORITY PRESERVATION
+ GENERATION COMMIT AUTHORITY PRESERVATION
+ NO NUMERICAL CHANGE
+ NO UNBOUNDED GPU LOOP
+ NO HIDDEN CPU FALLBACK
```

## Parent

```text
TENSORCUBE-TABLE-R2A
ASH_PASS3_TENSORCUBE_TABLE_R2A_PARALLEL_COMPACTION_INDIRECT_DISPATCH_CODE_ONLY.zip
SHA-256 366622d278d7a51e06755efe0832f5566c7f70d1fcf3d49b778eeb12d72a115f
```

R2A remains the sole ready-set, stable-prefix-compaction, device-ready-count and indirect-dispatch primitive. R3 composes R2A rather than forking it.

## Core law

Within one sealed TensorTable generation, the host may admit and submit a bounded scheduler epoch, but it must not enumerate ready rows, map ready counts, or rebuild consumer ranges between scheduler rounds.

Persistent means persistent scheduler state and bounded device-controlled progression. It does not mean an unbounded WGSL loop or GPU-side queue submission.

## Concrete execution model

This bake encodes one bounded scheduler super-wave into the caller's command encoder:

```text
HOST
  admit epoch
  encode bounded scheduler super-wave
        |
ROUND 0
  R2A parallel ready views
  scheduler claims
  failure gate
  Muon indirect consume
  atomic lifecycle transition
  terminal/progress pass
        |
ROUND 1
  R2A parallel ready views
  newly-ready successor/BP-DK claims
  Muon consume if any
  terminal/progress pass
        |
...
        |
QUIESCENT / FAILED
```

No CPU row-membership decision exists inside the round loop.

## Bounded round authority

Current dependency depth is:

```text
COMPUTE -> MUON -> SUCCESSOR
```

R3 seals:

```text
TENSORCUBE_TABLE_R3_LIFECYCLE_DEPTH = 3
TENSORCUBE_TABLE_R3_TERMINAL_CONFIRMATION_ROUNDS = 1
TENSORCUBE_TABLE_R3_MAX_SCHEDULER_ROUNDS = 4
TENSORCUBE_TABLE_R3_NO_PROGRESS_LIMIT = 1
```

The fourth round is a terminal-confirmation round. This is a finite graph bound, not a polling loop.

## Scheduler control block

GPU-resident control metadata includes:

```text
terminal_state
failure_code
round_ordinal
progress_total
muon_claim_total
bpdk_claim_total
successor_claim_total
previous_claim_total
no_progress_rounds
last_progress_delta
last_raw_muon
last_raw_bpdk
last_raw_successor
max_rounds
epoch_id
source_generation
target_generation
no_progress_limit
active_consumer_mask
```

No W/M/V/update tensor payload is duplicated.

## Terminal states

```text
RUNNING
QUIESCENT
FAILED
CANCELLED
```

## Identity seal

R3 binds exact:

```text
TensorTable digest
source generation
target generation
row capacity
parameter capacity
scheduler epoch id
```

R3 validation also calls the parent R2A identity validator. Table/generation drift is fail-closed before production consumer encoding.

## R2A reuse

Every scheduler round reuses:

```text
TensorCubeTableGpuSchedulerR2A::encode_ready_views()
TensorCubeTableGpuSchedulerR2A::encode_muon_indirect_consume()
```

No second prefix scan, stable scatter, ready-count or indirect-dispatch implementation is introduced.

## Scheduler-private claim planes

R3 materializes metadata-only claim planes:

```text
muon_claimed[row]
bpdk_claimed[parameter_record]
successor_claimed[row]
```

BP-DK/successor readiness may remain externally visible because durability/publication belongs to other authorities. Claims prevent scheduler rediscovery from being mistaken for new semantic work without forging external completion bits.

Muon claims are single-use. A repeated ready Muon row after prior claim is classified as a livelock/failure and suppresses further Muon mutation.

BP-DK claims deduplicate parameter records. Successor claims deduplicate rows handed toward the successor boundary.

## Claim dispatch

Claims use R2A's device-generated status-dispatch geometry:

```text
dispatch_workgroups_indirect(indirect_args, 12)
```

No host ready-count map is required.

## Semantic progress

The terminal pass computes:

```text
current_claim_total =
  muon_claim_total
+ bpdk_claim_total
+ successor_claim_total

progress_delta =
  current_claim_total
- previous_claim_total
```

Scheduler pass execution alone does not count as progress.

Muon claims are counted as round progress only after the already-encoded R2A consumer/status sequence and only if overflow remains clear.

## Failure gate

R2A clears count/overflow words at each ready-view build. If a previous R3 round is FAILED/CANCELLED, R3 reasserts fail-closed overflow before any later pre-encoded consumer mutation.

The gate is run again after claim passes, so identity/livelock failure in the current round suppresses Muon consumption immediately.

QUIESCENT is not converted into an error. Bounded tail rounds may still execute metadata scans, but claims return immediately and no legal new Muon work exists after proven quiescence in this sealed graph.

## Quiescence

R3 enters QUIESCENT when:

```text
progress_delta == 0
AND raw_muon_ready == 0
```

Already-claimed BP-DK/successor identities may remain raw-ready because their final durability/publication is outside R3 authority.

## No-progress / livelock gates

If Muon-ready work remains but no new semantic claim is possible:

```text
raw_muon_ready > 0
AND progress_delta == 0
```

R3 fails closed.

A duplicate Muon claim is classified immediately as `DuplicateMuonClaim`, sets scheduler FAILED, and sets the Muon plane overflow bit before physical consumption.

Claim counters are monotonic. Counter regression is fail-closed.

If semantic progress continues through the sealed maximum round, R3 fails with `RoundLimit` rather than extending into an unbounded loop.

## Authority boundaries

R3 does not own:

```text
generation commit
BP-DK filesystem durability
checkpoint payload SHA / manifest publication / fsync
B06 successor publication or ticket authority
```

Source contract:

```text
generation_commit_owned=false
bpdk_durability_owned=false
b06_publication_owned=false
```

## No host scheduler authority

Active source contract:

```text
host_wave_enumeration_count=0
host_ready_membership_decision_count=0
ready_count_host_map_count=0
full_table_readback_count=0
host_range_rebuild_count=0
hidden_cpu_fallback=false
```

These are source-path contracts, not runtime measurements.

## WGPU execution boundary

R3 does not claim WGSL can call `queue.submit()`. WGPU command submission stays host-owned.

The reduction comes from encoding a bounded multi-round device-controlled topology into one caller-owned command encoder while work membership and dispatch sizes remain device-resident.

## New WGSL

```text
crates/base_train/src/shaders/
  tensorcube_table_scheduler_claim_r3.wgsl
  tensorcube_table_scheduler_failure_gate_r3.wgsl
  tensorcube_table_scheduler_terminal_r3.wgsl
```

Maximum new R3 binding count is 6.

## Changed files

```text
MOD crates/base_train/src/lib.rs
ADD crates/base_train/src/tensorcube_table_persistent_scheduler_r3.rs
ADD crates/base_train/src/shaders/tensorcube_table_scheduler_claim_r3.wgsl
ADD crates/base_train/src/shaders/tensorcube_table_scheduler_failure_gate_r3.wgsl
ADD crates/base_train/src/shaders/tensorcube_table_scheduler_terminal_r3.wgsl
ADD tools/validate_ash_tensorcube_table_r3_persistent_scheduler_static.py
```

Delta: MOD 1 / ADD 5 / DEL 0.

## Static qualification

```text
PASS_TENSORCUBE_TABLE_R3_PERSISTENT_SCHEDULER_STATIC checks=52
PASS_TENSORCUBE_TABLE_R2A_PARALLEL_COMPACTION_STATIC checks=39
PASS_TENSORCUBE_TABLE_R2_GPU_PARALLEL_CONSUMER_STATIC checks=28
PASS_TENSORCUBE_TABLE_R1_STATIC checks=20
PASS_TENSORCUBE_CONSUME_R2_GPU_PARALLEL_PLANE_STATIC checks=61
PASS_TENSORCUBE_CONSUME_R1_RELATION_AUTHORITY_STATIC checks=56
PASS_ASH_WGSL_WGPU26_GLOBAL_COMPATIBILITY_STRUCTURAL_R1
PYTHON_VALIDATOR_COMPILE_PASS
```

WGSL structural state:

```text
standalone_wgsl_count=319
new_r3_wgsl_module_count=3
new_r3_max_binding_count=6
unsupported_finite_callsite_count=0
subgroup_elect_callsite_count=0
unsupported_subgroup_enable_count=0
disallowed_function_pointer_arg_count=0
```

## Evidence boundary

```text
RUST_TOOLCHAIN=UNAVAILABLE

SOURCE=PASS
STATIC=PASS
COMPILE=NOT_RUN
RUNTIME=NOT_RUN
PHYSICAL=NOT_RUN
PERFORMANCE=UNMEASURED
PROMOTED=NO
```

No compile/runtime/physical/performance claim is made.

## Artifacts

```text
ASH_TENSORCUBE_TABLE_R3_PERSISTENT_SCHEDULER_OVERLAY_CODE_ONLY.zip
SHA-256 9f5ae09c335c88acc6a436769e1a7554964661c49bba431ef224f7dc28cf9baa
FILES 6
CRC PASS

ASH_PASS3_TENSORCUBE_TABLE_R3_PERSISTENT_DEVICE_SCHEDULER_CODE_ONLY.zip
SHA-256 97b2784042b95e5abc27da44f8a83c8e04514ec6086ec9bde7cf04021894b633
FILES 8476
CRC PASS
```

## Compile acceptance

First local gate:

```text
cargo test -p base_train --lib tensorcube_table_r3_
```

Then rerun R2A/R2/R1 tests and current WGPU26/Naga validation.

## Physical acceptance

Compare identical-source:

```text
R2A host-orchestrated execution
vs
R3 bounded persistent scheduler
```

Require final lifecycle parity, Muon byte parity, BP-DK ready-plan identity parity, successor coverage parity, zero illegal duplicate Muon claims, no hidden CPU scheduler fallback, and preserved B06/BP-DK transaction boundaries.

## Performance acceptance

R3 exists to remove orchestration cost. Promotion therefore requires measured evidence including:

```text
R2A host_submission_count
R3 host_submission_count
R2A host_encode_us
R3 host_encode_us
R2A host_wait_us
R3 host_wait_us
scheduler_epoch_us
GPU scan/compact/consume attribution
```

## Final law

> R1 made TensorCube a GPU-resident table row. R2 made the GPU select ready rows. R2A made ready selection parallel and kept dispatch counts on-device. R3 removes host row/wave membership decisions from bounded generation progression itself.

> R3 is persistent in scheduler state, not an infinite shader. It composes a finite device-controlled scheduler super-wave using existing R2A primitives and explicit terminal state.

> BP-DK durability, B06 publication, and generation commit remain outside scheduler authority. A scheduler that cannot prove bounded forward progress fails closed rather than spinning or falling back to CPU scheduling.
