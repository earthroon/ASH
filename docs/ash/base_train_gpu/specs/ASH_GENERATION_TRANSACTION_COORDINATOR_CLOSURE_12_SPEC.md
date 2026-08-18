# ASH-GENERATION-TRANSACTION-COORDINATOR-CLOSURE-12

## Explicit Target Generation / Filesystem Commit Witness / Typed Bridge→Planner→POST→Causal→Objective→Trajectory→Calibration Coordination / Typed Abort / No Global Atomicity Claim

## 0. Status

```text
Patch ID: ASH-GENERATION-TRANSACTION-COORDINATOR-CLOSURE-12
Direct parent: ASH-MUON-LOAD-RESUME-CHECKPOINT-PARITY-11
Runtime parent: ASH-MUON-RUNTIME-AUTHORITY-DECOMPOSITION-07
Lineage family: optimizer-generation-transaction
Authority class: OptimizerDataPlane
Production authority: ExecutionCoordination
Target data plane: bp-dk-data-plane/active-fusion/v1
Status: Active
```

12 changes generation transaction orchestration only. It does not change Muon mathematics, BP-Delta-K mathematics, Fusion/Fission planning semantics, checkpoint format, GPU shaders, G1/G2 policy semantics, or the scheduler's filesystem publication authority.

## 1. Central SSOT

```text
ONE GENERATION TRANSACTION
= ONE EXPLICIT TRAINING GENERATION
+ ONE EXPLICIT OPTIMIZER STEP
+ ONE SUCCESSFUL FILESYSTEM COMMIT WITNESS
```

The runtime no longer exposes the old production authority:

```text
record_step_commit()
record_step_abort(step)
```

The canonical APIs are now context-bound:

```text
record_generation_commit(&AshMuonGenerationCommitContext)
record_generation_abort(&AshMuonGenerationAbortContext)
```

No generation is inferred from "whatever happens to be pending" at commit time.

## 2. Filesystem authority remains in the scheduler

The existing scheduler order remains:

```text
candidate persistence
→ observer persistence
→ Bridge temporal persistence
→ transaction.validated.json
→ transaction.ready_for_commit.json
→ commit_active_state(...)
→ staging_guard.mark_committed(...)
→ Muon in-memory generation commit
```

`ProductionMuonRuntime` does not call `commit_active_state()` and does not acquire filesystem publication authority.

After successful filesystem publication, the scheduler constructs:

```text
AshMuonFilesystemGenerationCommitWitness
```

from already-authoritative values:

```text
trainingGeneration
optimizerStep
trainingStateDigest
packedStateManifestDigest
candidateParameterSetDigest
```

The witness constructor is crate-controlled and rejects empty digests.

## 3. Commit context

```text
AshMuonGenerationCommitContext
```

contains:

```text
training generation
optimizer step
filesystem commit witness
```

The context constructor verifies that witness generation/optimizer-step identity exactly matches the transaction target.

## 4. Full pending-generation preflight

Before the first commit mutation, 12 inspects the pending optimizer generation of every participating owner:

```text
Bridge Temporal
Fusion/Fission Planner
POST Update
Causal Effect
Objective Probe
Fusion Trajectory
Calibration Replay
```

Each stage is classified as:

```text
NotPending
Pending { optimizerStep }
```

`Some(otherGeneration)` produces:

```text
GenerationTransactionPendingGenerationMismatch
```

before any coordinator-owned commit mutation begins.

Therefore:

```text
Preflight failure → no stage commit has started
```

This guarantee does not extend to a failure after stage execution has started.

## 5. Exact commit order

The canonical ordered chain is:

```text
BridgeTemporal
→ FusionPlanner
→ PostUpdate
→ CausalEffect
→ ObjectiveProbe
→ FusionTrajectory
→ CalibrationReplay
→ TransientFinalize
```

The order is explicit in both the runtime implementation and the 12 registry.

## 6. Typed dependency propagation

12 keeps the existing ledger authority rather than recomputing upstream semantics in the coordinator.

### POST → Causal

After POST commit, 12 captures an `AshCommittedPostWitness` containing the actual committed POST head.

Causal commit consumes that typed head.

### Causal → Objective

After Causal commit, 12 captures an `AshCommittedCausalWitness`.

Objective commit consumes the actual committed Causal head.

### POST + Causal + Objective → Trajectory

Trajectory commit consumes typed committed POST, Causal, and Objective heads.

### Trajectory → Calibration

Trajectory remains ordered before Calibration. 12 does not invent a new data dependency requiring Calibration to accept a trajectory-head parameter where the existing API does not.

```text
ORDER DEPENDENCY != INVENTED DATA DEPENDENCY
```

## 7. Stage progress

Each transaction stage is represented as:

```text
NotPending
Committed { stateCount }
```

This preserves the distinction between an inactive stage and a stage that actually performed a commit operation.

Existing subsystem return values retain their existing semantics. 12 does not reinterpret a `stateCount` as files, parameters, tensors, or pairs.

## 8. Typed successful receipt

`AshMuonGenerationCommitReceipt` records:

```text
schema revision
training generation
optimizer step
filesystem training-state digest
packed-state manifest digest
candidate parameter-set digest
stage progress
POST head digest
Causal head digest
Objective head digest
Trajectory head digest
Calibration head digest
transaction receipt digest
```

The scheduler consumes the receipt and verifies its generation, step, and filesystem/candidate digests against the same authoritative values used to construct the witness.

The receipt is an in-memory transaction witness, not a new checkpoint state file.

## 9. Typed commit failure

`AshMuonGenerationCommitFailure` exposes:

```text
training generation
optimizer step
transaction phase
failed stage
completed stage progress
stable error code
source error
```

Stage-specific codes include:

```text
GenerationTransactionBridgeCommitFailed
GenerationTransactionPlannerCommitFailed
GenerationTransactionPostCommitFailed
GenerationTransactionCausalCommitFailed
GenerationTransactionObjectiveCommitFailed
GenerationTransactionTrajectoryCommitFailed
GenerationTransactionCalibrationCommitFailed
GenerationTransactionFinalizeFailed
```

The first failed stage stops further stage execution.

No hidden retry and no stage skipping are added.

## 10. No global atomicity claim

12 does not claim that the in-memory chain is globally atomic.

Example:

```text
filesystem commit succeeded
Bridge committed
Planner committed
POST committed
Causal failed
```

is a possible partial in-memory state.

12 exposes this state through typed failure progress. It does not fabricate an `uncommit` operation for Bridge, Planner, or POST.

```text
FAILURE WITNESS != ROLLBACK ENGINE
```

## 11. Post-filesystem failure boundary

If `record_generation_commit()` fails after filesystem publication, the scheduler reports:

```text
FilesystemCommittedInMemoryCommitIncomplete
```

and does **not** automatically call generation abort.

At that point durable filesystem state has already advanced, so treating it as a normal pre-publication abort would conflate two different authorities.

Recovery from this condition is deliberately reserved for patch 13.

## 12. Typed abort context

The old step-only abort entrypoint is replaced by:

```text
AshMuonGenerationAbortContext
```

which carries:

```text
training generation
optimizer step
abort reason
```

Current explicit reasons are:

```text
PreFilesystemCommitFailure
FilesystemCommitFailure
```

The scheduler uses the first for failures before filesystem commit is attempted and the second when `commit_active_state()` itself fails.

## 13. Abort preflight and order

Abort also preflights pending generation identities before mutation.

Canonical abort order remains:

```text
Bridge
→ Planner
→ POST
→ Causal
→ Objective
→ Trajectory
→ Calibration
→ generation-local transient cleanup
```

`AshMuonGenerationAbortReceipt` records per-stage aborted counts and whether generation-local transient inventory was cleared.

`AshMuonGenerationAbortFailure` records the failed abort stage and the stages already completed.

12 does not implement rollback of an abort that itself partially fails.

## 14. Generation-local cleanup remains scoped

After a successful abort chain, existing generation-local cleanup semantics are preserved:

```text
expected inventory
freshness expectations
02 parameter PRE snapshot bindings
05 parameter control bindings
training-generation snapshot projections
objective sparse overlays
```

12 does not broaden cleanup into unrelated durable ledgers or checkpoint history.

## 15. 07 ownership topology remains intact

`ProductionMuonRuntime` retains its nine top-level owner fields:

```text
static_context
execution
observation
bridge
planning
control
evidence
telemetry
lifecycle
```

No mutable `transaction_coordinator` field is introduced.

The coordinator contract is stateless orchestration around the existing owners.

## 16. Existing telemetry remains authoritative

Existing stage counters remain in use, including:

```text
bridge_temporal_state_commit_count
fusion_planner_state_commit_count
post_update_ledger_state_commit_count
causal_ledger_state_commit_count
objective_probe_ledger_state_commit_count
fusion_trajectory_state_commit_count
```

12 does not duplicate those counters under a parallel telemetry authority.

`production_muon_callsite_invocation_count` advances only after the complete commit/finalize chain succeeds.

## 17. Checkpoint / GPU boundaries

12 adds:

```text
new checkpoint schema = 0
new checkpoint state file = 0
WGSL changes = 0
GPU dispatch authority = 0
D2H authority = 0
new optimizer formula = 0
new BP-Delta-K formula = 0
```

The coordinator does not persist a giant runtime snapshot.

## 18. Lineage adoption

`tools/ash_lineage_reconciliation_00_registry.py` adds:

```text
ASH-GENERATION-TRANSACTION-COORDINATOR-CLOSURE-12

family = optimizer-generation-transaction
authority class = OptimizerDataPlane
production authority = ExecutionCoordination
status = Active
direct parent = ASH-MUON-LOAD-RESUME-CHECKPOINT-PARITY-11
runtime parent = ASH-MUON-RUNTIME-AUTHORITY-DECOMPOSITION-07
```

Current head:

```text
optimizer-generation-transaction
→ ASH-GENERATION-TRANSACTION-COORDINATOR-CLOSURE-12
```

Current execution-authority map adds only:

```text
generation_transaction_coordination
→ ASH-GENERATION-TRANSACTION-COORDINATOR-CLOSURE-12
```

The optimizer itself remains:

```text
ASH-BASETRAIN-TENSORCUBE-LOCAL-MUON-PRODUCTION-CALLSITE-ADOPTION-R1
```

12 therefore coordinates generation transition but does not become the Muon mathematical executor.

## 19. Vocabulary

```text
owned data-plane revision = None
target data-plane revision = bp-dk-data-plane/active-fusion/v1
owned policy generation = None
owned qualification generation = None
```

The reconciliation patch number `12` is not the same identity as the historical BP-DK Calibration patch numbered 12.

```text
PATCH NUMBER != LINEAGE IDENTITY
```

## 20. Validator compatibility updates

Because 12 intentionally removes the old `record_step_commit/abort` production API, historical/current static validators that previously matched those function names were updated to follow the same underlying authority through:

```text
record_generation_commit
record_generation_abort
explicit target optimizer step
typed POST/Causal/Objective witnesses
```

This includes BP-DK 03B/05/07/08A/09/10/11/12 and production policy gates that asserted the old callback spelling.

One unrelated brittle validator was also narrowed: the ExactSubgroup32 norm validator previously treated the first `Ok(Self {` in the whole production source as the runtime constructor. 12 adds typed constructors earlier in the file, so the validator now searches for the `Ok(Self {` belonging specifically to `load_or_initialize()`. The SerialLane0 runtime requirement itself is unchanged.

## 21. New tooling

```text
tools/ash_generation_transaction_coordinator_12_registry.py
tools/validate_ash_generation_transaction_coordinator_closure_12.py
tools/run_ash_generation_transaction_coordinator_closure_12.ps1
```

The runner performs:

```text
00 lineage static validation
07 runtime decomposition static validation
11 resume-parity contract static validation
12 transaction coordinator static validation
cargo check base_train --lib
cargo check base_train --bin base_train
```

No overlay application step is included.

## 22. Baked static evidence

Validated work tree and re-extracted full ZIP both produced:

```text
00  220 / 220 PASS
01  306 / 306 PASS
02  216 / 216 PASS
03  167 / 167 PASS
04  198 / 198 PASS
05   92 /  92 PASS
06  143 / 143 PASS
07  347 / 347 PASS
08   82 /  82 PASS
09   68 /  68 PASS
10   66 /  66 PASS
11   91 /  91 PASS
12  156 / 156 PASS
```

Additional regression evidence:

```text
existing BP-Delta-K *_static.py validators: 25 / 25 PASS
CF1-enumerated Python validators: 68 / 68 PASS
modified Python source py_compile: PASS
Rust delimiter lexical-balance check on both changed Rust files: PASS
```

CF1 was executed in two bounded groups of 34 validators so every exit code completed within the execution-tool time limit.

## 23. Physical compile evidence boundary

The bake environment does not expose:

```text
cargo
rustc
rustfmt
pwsh
```

Therefore:

```text
Rust cargo check = EvidenceInsufficient / not executed here
PowerShell runner = EvidenceInsufficient / not executed here
physical R6 integration = EvidenceInsufficient / not executed here
10 physical parity requalification on 12 source = not executed here
11 physical resume requalification on 12 source = not executed here
```

12 changes Rust control flow, so any previously produced physical 10/11 receipt for an older runtime-source digest must be treated as stale and rerun against the 12 body before a new end-to-end physical closure claim.

Static PASS is not compile PASS.

## 24. Parent diff boundary

Compared with the 11 full-applied parent:

```text
changed files = 31
Rust files changed = 2
WGSL files changed = 0
```

Runtime Rust changes are limited to:

```text
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
```

The remaining changes are registry, validator, CF1, and runner compatibility/tooling changes required to make the new typed transaction authority observable without weakening prior semantic gates.

## 25. Packaging

```text
Overlay Code ZIP: 31 files
Full Applied Code ZIP: 7243 files
```

Full ZIP re-extraction versus validated work tree:

```text
missing = 0
extra = 0
hash mismatch = 0
forbidden generated content = 0
```

Code ZIPs contain no Markdown specs, `*.sha256`, `*.pyc`, or `__pycache__` output.

## 26. Non-goals

12 does not implement:

```text
global atomic rollback
uncommit of ledgers
post-filesystem automatic abort
last-good checkpoint fallback
crash-window recovery
new checkpoint schema
new policy decision
new planner decision
new optimizer update
new BP-Delta-K calculation
performance optimization
```

## 27. Next revision

The natural next patch is:

```text
ASH-GENERATION-FAILURE-RECOVERY-AND-LAST-GOOD-SEAL-13
```

12 now exposes exactly the information 13 needs:

```text
target generation
target optimizer step
filesystem committed identity
completed commit stages
failed stage
committed upstream head digests
```

13 can therefore reason about fail-stop/reload/last-durable-state behavior without inventing rollback semantics.

## 28. Final seal

```text
ONE TRANSACTION HAS ONE EXPLICIT TARGET

THE TARGET IS NOT INFERRED FROM PENDING STATE

FILESYSTEM COMMIT PRECEDES IN-MEMORY GENERATION PROMOTION

A FILESYSTEM COMMIT WITNESS IS REQUIRED

ALL PARTICIPATING PENDING GENERATIONS ARE PREFLIGHTED BEFORE FIRST MUTATION

PREFLIGHT FAILURE MUTATES NO COMMIT STAGE

BRIDGE → PLANNER → POST → CAUSAL → OBJECTIVE → TRAJECTORY → CALIBRATION
IS THE CANONICAL ORDER

CAUSAL CONSUMES THE ACTUAL COMMITTED POST HEAD
OBJECTIVE CONSUMES THE ACTUAL COMMITTED CAUSAL HEAD
TRAJECTORY CONSUMES THE ACTUAL COMMITTED POST / CAUSAL / OBJECTIVE HEADS

A COMMIT FAILURE EXPOSES ITS FAILED STAGE AND COMPLETED PROGRESS

PARTIAL IN-MEMORY COMMIT IS NOT HIDDEN
PARTIAL IN-MEMORY COMMIT IS NOT CLAIMED ATOMIC

NO ROLLBACK IS INVENTED
NO UNCOMMIT IS INVENTED
NO SILENT RETRY IS INVENTED
NO STAGE SKIP IS INVENTED

AFTER FILESYSTEM SUCCESS, IN-MEMORY COMMIT FAILURE IS NOT AUTO-ABORTED

ABORT HAS ITS OWN EXPLICIT CONTEXT AND REASON

07 DEFINED STATE OWNERSHIP
11 DEFINED RESTART RECONSTRUCTION
12 DEFINES THE EXPLICIT ORDERED GENERATION TRANSITION ACROSS THOSE OWNERS
```
