# ASH-GENERATION-RECOVERY-PHYSICAL-FAULT-MATRIX-14

## Test-Only Deterministic Fault Injection / Real Filesystem Publication Windows / Previous·Target·Contradictory Proof / Commit·Abort Stage Matrix / Fresh-Recovery Evidence Binding / No Production Failpoint

## 0. Status

```text
Patch ID: ASH-GENERATION-RECOVERY-PHYSICAL-FAULT-MATRIX-14
Direct parent: ASH-GENERATION-FAILURE-RECOVERY-AND-LAST-GOOD-SEAL-13
Transaction parent: ASH-GENERATION-TRANSACTION-COORDINATOR-CLOSURE-12
Runtime parent: ASH-MUON-RUNTIME-AUTHORITY-DECOMPOSITION-07
Lineage family: optimizer-generation-recovery-qualification
Authority class: OptimizerDataPlane
Production authority: QualificationOnly
Target data plane: bp-dk-data-plane/active-fusion/v1
Status: QualificationOnly
```

14 does not replace 13 recovery authority. It physically qualifies the failure windows and recovery decisions introduced by 13.

## 1. Central SSOT

```text
A RECOVERY POLICY IS NOT PHYSICAL EVIDENCE
UNTIL THE FAILURE WINDOW IS ACTUALLY ENTERED.

FAULT INJECTION MUST NOT BECOME
A PRODUCTION CONTROL SURFACE.
```

Production execution authority remains:

```text
generation transaction coordination -> 12
generation failure recovery         -> 13
optimizer                            -> Production Muon callsite
```

14 owns only the qualification head.

## 2. Production failpoint firewall

The fault controllers are Rust `#[cfg(test)]` only.

14 adds no:

```text
production CLI fault flag
production environment fault selector
Cargo fault-injection feature
public production fault API
WGSL fault branch
```

The only environment variable introduced by the physical harness is:

```text
ASH_QUAL14_FIXTURE_JSON
```

and it is read only inside the `#[cfg(test)]` qualification test module.

## 3. Scheduler test-only publication controller

`production_multistep_loop_accumulation8_scheduler.rs` adds test-only one-shot fault points:

```text
PreFilesystemAbortTrigger
BeforeHistoryWrite
AfterHistoryWrite
AfterActivePartialWrite
AfterActiveReplaceBeforePostcheck
AfterActiveReplaceCorruptHistoryBeforePostcheck
```

The controller records an exact hit count and rejects a second hit of the same selected fault with:

```text
PhysicalFaultFiredMultipleTimes
```

The hooks compile out of non-test builds.

## 4. Real publication boundaries

The existing production publication order remains:

```text
write committed_training_state_step_<target>.json
→ write active_training_state.json.partial
→ replace active_training_state.json
→ reopen / postcheck
```

14 injects faults around those exact existing calls:

```text
PF-00 BeforeHistoryWrite
PF-01 AfterHistoryWrite
PF-02 AfterActivePartialWrite
PF-03 AfterActiveReplaceBeforePostcheck
PF-04 AfterActiveReplace + test-only committed-history corruption
```

No in-memory fake filesystem replaces `write_json_sync()`, file `sync_all()`, or `replace_active_file()`.

## 5. M0 real-filesystem micro matrix

New regular Rust unit test:

```text
generation_recovery_physical_fault_matrix_14_publication_micro_matrix
```

The test materializes a valid 201-parameter packed manifest and candidate state in a real temporary filesystem and calls the actual private production helper:

```text
commit_active_state(...)
```

After the injected failure it calls the actual 13 classifier:

```text
classify_generation_publication_after_failure(...)
```

Expected outcomes:

```text
PF-00 -> PreviousSourceCurrent / residue None
PF-01 -> PreviousSourceCurrent / TargetHistoryOnly
PF-02 -> PreviousSourceCurrent / TargetHistoryAndActivePartial
PF-03 -> TargetFilesystemCurrent
PF-04 -> Contradictory / Unestablished path
```

Each case requires exactly one scheduler-fault hit.

## 6. Muon transaction test-only controller

`tensorcube_local_muon_production_callsite_adoption.rs` adds test-only one-shot commit fault points:

```text
CM-00 BeforeBridgeCommit
CM-01 BeforePlannerCommit
CM-02 BeforePostCommit
CM-03 BeforeCausalCommit
CM-04 BeforeObjectiveCommit
CM-05 BeforeTrajectoryCommit
CM-06 BeforeCalibrationCommit
CM-07 BeforeTransientFinalize
```

and abort fault points:

```text
AB-00 BeforeBridgeAbort
AB-01 BeforePlannerAbort
AB-02 BeforePostAbort
AB-03 BeforeCausalAbort
AB-04 BeforeObjectiveAbort
AB-05 BeforeTrajectoryAbort
AB-06 BeforeCalibrationAbort
```

These hooks sit inside the existing typed 12 transaction APIs. They do not replace the real Bridge/Planner/POST/Causal/Objective/Trajectory/Calibration implementations.

## 7. Commit-stage semantics

A commit fault is injected only when the corresponding stage is actually admitted/pending, except `BeforeTransientFinalize`, which is the final transaction boundary.

Therefore a fixture that fails to activate a requested Fusion/evidence stage does not establish that case. A missing fault hit is not converted into PASS.

Canonical rule:

```text
faultHitCount = 0 -> EvidenceInsufficient / NotCovered
faultHitCount > expected -> Contradictory
```

## 8. Abort-stage semantics

Abort matrix cases combine:

```text
PreFilesystemAbortTrigger
+
exact AB stage hook
```

so the scheduler enters the existing 13 pre-filesystem failure path and the actual 12 abort chain.

For AB cases the expected total physical fault hits are exactly two:

```text
1 scheduler pre-filesystem trigger
1 selected abort-stage trigger
```

The durable recovery source remains PreviousSourceCurrent.

## 9. Post-filesystem candidate preservation tightening

13 already preserved candidates when `commit_active_state()` returned an error and the filesystem classified Target or Contradictory.

14 additionally makes the post-filesystem/in-memory-commit failure branch explicitly call:

```text
staging_guard.preserve_for_recovery(&candidate_dir)
```

before activating the recovery fence.

This gives CM failures explicit forensic ownership in `recoveryPreservedPaths` even though the candidate was already removed from normal deletion tracking after filesystem publication.

No rollback or active-pointer rewrite is introduced.

## 10. Ignored full R6/Muon materializer

New ignored Rust qualification test:

```text
generation_recovery_physical_fault_matrix_14_materialize
```

It consumes fixture schema:

```text
ash.generation.recovery.physical-fault-matrix14.fixture.v1
```

Required fixture fields:

```text
baseTrainConfigPath
modelSpecPath
tokenizerManifestPath
datasetManifestPath
workRoot
caseIds
```

For each requested case the test:

```text
clones the BaseTrainConfig
assigns a case-local output root
sets exactly the requested test-only fault controller(s)
boots the existing native Atlas/WGPU runtime
calls run_local_base_training_with_device(...)
requires the run to fail
requires the exact physical fault hit count
reads the 13 last-durable seal
reads staging ownership evidence
writes one bounded fault_case.json
```

The full materializer is ignored by default because it requires the real ASH R6/Muon fixture and GPU runtime.

## 11. Fault-case schema

Generated case evidence uses:

```text
ash.basetrain.generation.recovery.physical_fault_case.v1
```

and records at least:

```text
caseId
schedulerFaultHitCount
transactionFaultHitCount
expectedDisposition
observedDisposition
expectedRecoveryAction
observedRecoveryAction
runError
recoverySealPath
stagingOwnership
freshRecoveryAttempted
freshRecoverySucceeded
caseDisposition
```

Generated evidence is not included in baked code ZIPs.

## 12. Mandatory physical case set

14 registry defines 20 mandatory cases:

```text
PF: 5
CM: 8
AB: 7
Total: 20
```

Expected recovery classes:

```text
PF-00/PF-01/PF-02 + all AB
 -> PREVIOUS_SOURCE_CURRENT
 -> FRESH_RESTART_FROM_PREVIOUS_SOURCE

PF-03 + all CM
 -> TARGET_FILESYSTEM_CURRENT
 -> FRESH_RESTART_FROM_TARGET_CURRENT

PF-04
 -> UNESTABLISHED
 -> OPERATOR_INTERVENTION_REQUIRED
```

## 13. Fresh-process evidence binding

Fault materialization alone cannot establish FullMatrixEstablished.

New tool:

```text
tools/bind_ash_generation_recovery_fault_matrix_14_recovery_evidence.py
```

binds externally produced fresh-process control/recovery projections to case receipts through fixture field:

```text
recoveryEvidenceByCase
```

For every Previous/Target case, full evidence requires:

```text
freshRecoveryAttempted = true
freshRecoverySucceeded = true
controlProjectionPath exists
recoveryProjectionPath exists
```

PF-04 explicitly forbids recovery evidence because the correct behavior is fail-closed/operator intervention.

## 14. Exact matrix comparator

New comparator:

```text
tools/compare_ash_generation_recovery_physical_fault_matrix_14.py
```

It requires exact current-source 10/11 parent receipts:

```text
10 disposition = ParityEstablished
10 candidateRuntimeSourceDigest = current 14 runtime digest

11 disposition = ParityEstablished
11 currentRuntimeSourceDigest = current 14 runtime digest
```

For bound continuation evidence:

```text
control semantic projection == recovery semantic projection
```

is exact structural equality.

No new epsilon/tolerance is introduced.

## 15. Matrix dispositions

```text
FullMatrixEstablished
PartialCoverage
EvidenceInsufficient
Contradictory
```

`FullMatrixEstablished` requires all mandatory cases plus fresh-process continuation evidence where recovery is expected.

`PartialCoverage` is deliberately distinct from PASS.

## 16. Comparator self-test evidence from this bake

The 14 comparator was tested with synthetic evidence bound to the actual current runtime-source digest.

Case set with all 20 mandatory cases and equal control/recovery projections:

```text
PASS_ASH_GENERATION_RECOVERY_PHYSICAL_FAULT_MATRIX_14_FULL
```

Changing only the `CM-03` recovery projection produced:

```text
Contradictory
continuationProjectionMismatch
exit code 1
```

This proves comparator branching only. It is not physical R6 recovery evidence.

## 17. Dedicated runner

New runner:

```text
tools/run_ash_generation_recovery_physical_fault_matrix_14.ps1
```

Inputs:

```text
FixtureJson
ParentParity10Receipt
ParentParity11Receipt
WorkRoot
```

Execution order:

```text
00 lineage static
13 recovery static
14 fault-matrix static
cargo check base_train --lib
cargo check base_train --bin base_train
M0 publication micro matrix
ignored M1 fault materializer
recovery-evidence binder
exact matrix comparator
```

The runner does not search for or apply overlay ZIPs.

## 18. Lineage adoption

`ash_lineage_reconciliation_00_registry.py` adds:

```text
ASH-GENERATION-RECOVERY-PHYSICAL-FAULT-MATRIX-14

family = optimizer-generation-recovery-qualification
authority class = OptimizerDataPlane
production authority = Observation/QualificationOnly
status = QualificationOnly
direct parent = ASH-GENERATION-FAILURE-RECOVERY-AND-LAST-GOOD-SEAL-13
runtime parent = ASH-MUON-RUNTIME-AUTHORITY-DECOMPOSITION-07
```

New head:

```text
optimizer-generation-recovery-qualification
 -> ASH-GENERATION-RECOVERY-PHYSICAL-FAULT-MATRIX-14
```

14 is not inserted into `CURRENT_EXECUTION_AUTHORITIES`.

13 remains:

```text
generation_failure_recovery
 -> ASH-GENERATION-FAILURE-RECOVERY-AND-LAST-GOOD-SEAL-13
```

12 remains generation transaction coordination authority.

## 19. CF1 classification

14 static validator is added only to:

```text
RuntimeQualificationValidators
```

It is not added to:

```text
ProductionValidators
HistoricalPreservationValidators
OperationalRecoveryValidators
```

Thus:

```text
CF1 static PASS != physical fault matrix PASS
```

## 20. Parent diff boundary

Compared with the 13 full-applied parent, 14 changes exactly 9 files.

### Rust runtime/test surface

```text
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
```

### Tooling/governance

```text
tools/ash_generation_recovery_physical_fault_matrix_14_registry.py
tools/bind_ash_generation_recovery_fault_matrix_14_recovery_evidence.py
tools/compare_ash_generation_recovery_physical_fault_matrix_14.py
tools/run_ash_generation_recovery_physical_fault_matrix_14.ps1
tools/validate_ash_generation_recovery_physical_fault_matrix_14.py
tools/ash_lineage_reconciliation_00_registry.py
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
```

```text
Rust files changed = 2
WGSL files changed = 0
removed files = 0
```

## 21. Baked static evidence

Validated source tree:

```text
00  237 / 237 PASS
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
13  140 / 140 PASS
14  165 / 165 PASS
```

Additional source-tree regression evidence:

```text
existing BP-Delta-K *_static.py validators = 25 / 25 PASS
CF1-enumerated Python validators = 70 / 70 PASS
changed/new Python syntax = PASS
changed Rust delimiter/string/comment lexical sanity = 2 / 2 PASS
```

The CF1 set was executed as two bounded groups of 35 on the validated source tree.

## 22. Packaged artifact verification

```text
Overlay ZIP files = 9
Full Applied ZIP files = 7251
```

Re-extracted Full ZIP versus validated source tree:

```text
missing = 0
extra = 0
hash mismatch = 0
forbidden generated content = 0
```

The re-extracted Full ZIP also re-passed:

```text
00→14 static chain = 15 / 15 PASS
BP-Delta-K static = 25 / 25 PASS
```

A second full CF1 replay from the byte-identical re-extraction was attempted, but the execution harness exceeded its per-command time limit during the long validator group. Because the ZIP is byte-identical to the already CF1-70/70 validated source tree, no separate packaged-CF1 PASS is claimed beyond that byte-identity evidence.

## 23. Physical evidence boundary in this bake

The bake environment does not expose:

```text
cargo
rustc
rustfmt
pwsh
```

Therefore the following were **not executed here**:

```text
cargo check
M0 Rust publication micro-matrix
M1 ignored physical R6/Muon fault materializer
fresh-process production recovery runs
10 current-source physical parity
11 current-source physical resume parity
FullMatrixEstablished physical receipt
```

Current physical disposition:

```text
EvidenceInsufficient
```

Static source readiness and comparator self-tests do not upgrade this disposition.

## 24. Power-loss boundary

14 injects application/test errors at semantic filesystem boundaries. It does not emulate:

```text
machine power loss
kernel crash
controller cache loss
storage-device power interruption
```

Therefore even after a future `FullMatrixEstablished`:

```text
powerLossDurabilityEstablished = false
```

until a separate durability closure establishes that claim.

## 25. Non-goals

14 does not implement:

```text
production fault controls
automatic rollback
same-process recovery
latest/highest checkpoint search
partial-stage resume
new checkpoint schema
new optimizer formula
new BP-Delta-K formula
new GPU dispatch
new D2H
power-loss durability
```

## 26. Next revision

Only after the 14 physical runner reaches:

```text
FullMatrixEstablished
```

on the exact current source should the next structural contraction proceed.

Recommended next patch:

```text
ASH-PRODUCTION-IMPORT-SURFACE-CONTRACTION-15
```

If any physical 14 case is contradictory, 15 should not proceed. The contradiction should first be repaired as a 14 revision.

## 27. Final seal

```text
13 DEFINES THE RECOVERY POLICY
14 PROVIDES THE PHYSICAL FAULT QUALIFICATION SURFACE

FAULTS ARE TEST-ONLY
PRODUCTION HAS NO FAULT CLI
PRODUCTION HAS NO FAULT ENV SELECTOR
PRODUCTION HAS NO FAULT FEATURE

THE REAL PUBLICATION PATH IS USED
THE REAL 12 TRANSACTION PATH IS USED
THE REAL 13 CLASSIFIER IS USED
THE REAL 13 RECOVERY FENCE IS USED

PF-00 / PF-01 / PF-02 MUST PROVE PREVIOUS
PF-03 MUST PROVE TARGET
PF-04 MUST FAIL CLOSED

EVERY COMMIT STAGE HAS A DETERMINISTIC TEST-ONLY FAULT BOUNDARY
EVERY ABORT STAGE HAS A DETERMINISTIC TEST-ONLY FAULT BOUNDARY

A FAULT THAT DID NOT FIRE IS NOT PASS
AN UNCOVERED STAGE IS NOT PASS
PARTIAL COVERAGE IS NOT FULL MATRIX ESTABLISHMENT

TARGET-CURRENT FAILURES DO NOT ROLL BACK
CONTRADICTORY PUBLICATION DOES NOT GUESS
THE FAILED PROCESS DOES NOT CONTINUE

FRESH RECOVERY EVIDENCE MUST BE BOUND EXPLICITLY
CONTROL AND RECOVERY PROJECTIONS MUST MATCH EXACTLY

NO INVENTED NUMERICAL TOLERANCE
NO POWER-LOSS CLAIM

THIS BAKE PREPARES THE PHYSICAL MATRIX
BUT DOES NOT CLAIM TO HAVE EXECUTED IT
WITHOUT CARGO/RUSTC/PWSH.
```
