# ASH-GENERATION-FAILURE-RECOVERY-AND-LAST-GOOD-SEAL-13

## Filesystem Publication Outcome Classification / Last-Durable Generation Seal / Process Recovery Fence / Fresh-Process Reconstruction / No Automatic Rollback

## 0. Status

```text
Patch ID: ASH-GENERATION-FAILURE-RECOVERY-AND-LAST-GOOD-SEAL-13
Direct parent: ASH-GENERATION-TRANSACTION-COORDINATOR-CLOSURE-12
Runtime parent: ASH-MUON-RUNTIME-AUTHORITY-DECOMPOSITION-07
Lineage family: optimizer-generation-failure-recovery
Authority class: OptimizerDataPlane
Production authority: FailureRecoveryCoordination
Target data plane: bp-dk-data-plane/active-fusion/v1
Status: Active
```

13 does not add optimizer mathematics, BP-Delta-K mathematics, a new checkpoint format, automatic rollback, or a latest-checkpoint fallback. It classifies the exact filesystem publication outcome after a generation failure and fences the failed process so recovery can occur only through a fresh process from an explicitly sealed source.

## 1. Central SSOT

```text
FAILURE DOES NOT IMPLY ROLLBACK

LAST-GOOD IS THE EXACT FILESYSTEM WORLD
THAT CAN BE PROVED CURRENT

PREVIOUS BY DEFAULT IS FORBIDDEN
TARGET BY GUESS IS FORBIDDEN
HIGHEST HISTORY FALLBACK IS FORBIDDEN
```

Three dispositions exist:

```text
PreviousSourceCurrent
TargetFilesystemCurrent
Unestablished
```

Recovery actions are correspondingly:

```text
FreshRestartFromPreviousSource
FreshRestartFromTargetCurrent
OperatorInterventionRequired
```

## 2. Why commit_active_state() Err is not enough

The existing R6 publication path remains:

```text
validate candidate
→ write committed_training_state_step_<target>.json
→ write active_training_state.json.partial
→ replace active_training_state.json
→ reopen active
→ verify trainingStateDigest
→ verify history == active
```

Therefore `commit_active_state()` may return an error after target history creation or even after active-file replacement. 13 removes the old assumption:

```text
commit_active_state Err
→ filesystem definitely still previous
```

That assumption is no longer permitted.

## 3. Failure-only filesystem publication probe

New scheduler helper:

```text
classify_generation_publication_after_failure(...)
```

The probe runs only after filesystem publication failure. The normal successful commit hot path performs no new recovery directory scan or probe.

The probe reads only exact known paths:

```text
training_state/active_training_state.json
training_state/active_training_state.json.partial
training_state/committed_training_state_step_<target>.json
exact target candidate directory
exact packed_state_manifest.json
```

It does not scan for the newest, latest, highest, or most recently modified state.

## 4. PreviousSourceCurrent

Previous is accepted only when exact identity is established.

For a later step in the same output root, the active state must match the source generation and optimizer step, have a valid `trainingStateDigest`, match the source candidate/manifest identity, and match the exact previous committed-history file byte-for-byte.

For the first output publication, where the canonical previous source is an external R5/R6-parent root and the new output has no active file yet, that already-validated `SourceState` remains previous authority.

A target history file existing by itself does not promote the target.

```text
TARGET HISTORY EXISTS != TARGET CURRENT
```

When previous is verified, the pending in-memory generation may be aborted using the existing typed 12 abort contract, then the process is recovery-fenced and returns a fresh-process-restart-required failure.

## 5. TargetFilesystemCurrent

Target is accepted only when all exact target identity checks succeed, including:

```text
active training generation == target
active optimizer step == target step
active trainingStateDigest valid
exact target history exists
SHA256(history) == SHA256(active)
active packedStateSlot == candidate slot
active candidateDirectory == candidate slot
active packedStateManifestDigest == candidate manifest digest
active candidateManifestDigest == candidate manifest digest
active candidateParameterSetDigest == target candidate-set digest
physical packed_state_manifest.json digest == candidate manifest digest
```

When target is verified after `commit_active_state()` returned an error:

```text
NO generation abort
NO rollback to previous
NO candidate deletion
```

The target candidate is preserved for recovery and the process is fenced. Recovery source is the current output root.

## 6. Contradictory publication

If active cannot be proven as either exact previous or exact target, or target active/history/candidate identities contradict one another:

```text
LastGoodDisposition = Unestablished
RecoveryAction = OperatorInterventionRequired
```

The target candidate is preserved for forensic/recovery inspection. No abort and no automatic previous-generation fallback are performed.

## 7. Staging guard recovery preservation

`OwnedRunStagingGuard` now distinguishes:

```text
tracked
recovery_preserved
committed/disarmed
```

New operation:

```text
preserve_for_recovery(path)
```

moves the exact candidate out of the deletion-tracked set and into `recoveryPreservedPaths` in `run_staging_ownership.json`.

`Drop` still reclaims only `tracked` paths. Recovery-preserved candidates are not removed.

This closes the dangerous window where active publication may already reference a target slot even though the publication function returned an error.

## 8. Post-filesystem in-memory commit failure

12 already produces typed progress for:

```text
Bridge
→ Planner
→ POST
→ Causal
→ Objective
→ Trajectory
→ Calibration
```

If filesystem publication succeeded but `record_generation_commit()` fails at any in-memory stage:

```text
failure class = InMemoryCommitFailureAfterFilesystemCommit
last-good = TargetFilesystemCurrent
recovery = FreshRestartFromTargetCurrent
```

The exact 12 `failed_stage` and transaction progress are copied into the 13 last-durable seal.

No automatic `record_generation_abort()` is called after filesystem publication has succeeded.

```text
PARTIAL IN-MEMORY PROGRESS IS FORENSIC EVIDENCE
NOT A RESUME PROGRAM COUNTER
```

A fresh process reconstructs state from the durable target checkpoint through the existing R6/Muon loader path.

## 9. Pre-filesystem failure

For the existing objective-probe failure path before filesystem publication:

```text
record_generation_abort(PreFilesystemCommitFailure)
```

remains the pending-state cleanup authority.

After abort success or abort failure, the process is fenced and recovery is sealed to the exact previous source. Same-process retry is not admitted.

If abort itself partially fails, the failed abort stage is preserved and the failure class becomes:

```text
AbortFailureBeforeFilesystemCommit
```

while the durable filesystem source remains previous.

## 10. Process-local recovery fence

`ProductionMuonLifecycleIdentity` now owns:

```text
generation_recovery_fence: Option<AshMuonGenerationRecoveryFence>
```

This keeps the 07 top-level owner count at nine. No tenth runtime owner is introduced.

The fence stores:

```text
attempted training generation
attempted optimizer step
failure class
failed stage if known
last-good disposition
```

A fresh `ProductionMuonRuntime::load_or_initialize()` always starts with:

```text
generation_recovery_fence = None
```

The fence is not checkpointed.

## 11. Fence-enforced fail-stop

Once the fence is active, the current process cannot continue through canonical mutable paths. The runtime now checks the fence before:

```text
execute_muon_parameter
persist_candidate_state
persist_bp_dk_observer_state
persist_bp_dk_bridge_temporal_state
seal_bp_dk_generation_expected_inventory
record_generation_commit
record_generation_abort
```

The canonical failure is:

```text
GenerationRecoveryFenceActive
```

There is no clear/retry API for the current process. A fresh process is the recovery mechanism.

## 12. Last-durable generation seal

13 writes recovery evidence under a diagnostic namespace outside `training_state`:

```text
<output>/generation_recovery/generation_failure_step_<target>.json
```

Schema:

```text
ash.basetrain.generation.last_durable_generation_seal.v1
```

The seal records:

```text
failure class
attempted generation / optimizer step
last-good disposition
last-good generation / step when established
last-good state-authority digest when established
restart source kind
restart source path as diagnostic convenience
recovery action
publication residue
failed 12 transaction stage if known
12 transaction progress if known
automaticRollbackCount = 0
automaticFallbackCount = 0
sameProcessContinueCount = 0
seal digest
```

The absolute restart path is diagnostic and is not used as a replacement for the canonical active-training-state authority.

## 13. Publication residue

13 records bounded residue classification:

```text
None
TargetHistoryOnly
ActivePartialOnly
TargetHistoryAndActivePartial
```

Residue is evidence, not current-state authority.

13 does not automatically delete orphan target history or partial active files. Failed-run evidence remains available for diagnosis, while recovery uses a fresh output run.

## 14. Existing loader remains authority

The fresh recovery process uses the existing exact R6 source loader. The loader still requires exactly one explicit source route and reads:

```text
training_state/active_training_state.json
```

It continues to verify generation/step, cursor, active-state digest, packed-state manifest, payload digests, scheduler state, and committed-history parity.

13 introduces no `read_dir`/mtime/highest-generation recovery path.

## 15. Recovery source semantics

### Previous-source recovery

```text
fresh process
→ exact previous source root
→ new output root
→ retry target generation
```

### Target-current recovery

```text
fresh process
→ exact current output root
→ reconstruct target owner state
→ continue with the next optimizer generation
```

A partially committed in-memory stage is never resumed stage-by-stage.

## 16. No automatic rollback

13 intentionally does not implement:

```text
uncommit Bridge
uncommit Planner
uncommit POST
restore previous active pointer
delete target history and pretend publication never happened
```

Those operations have no existing canonical inverse transaction contract.

Counters/fields in the recovery seal explicitly state:

```text
automatic rollback = 0
automatic fallback = 0
same-process continuation = 0
```

## 17. Power-loss durability boundary

The current implementation already uses file flush/fsync behavior in `write_json_sync()` and uses Windows `MOVEFILE_WRITE_THROUGH` for active-file replacement.

On non-Windows, active replacement remains:

```text
fs::rename(source, destination)
```

No new parent-directory fsync closure is added by 13.

Therefore 13 claims application/process failure recovery only. It does not claim proven machine-power-loss/controller durability.

```text
power-loss durability = EvidenceInsufficient
```

## 18. Lineage adoption

`tools/ash_lineage_reconciliation_00_registry.py` adds:

```text
ASH-GENERATION-FAILURE-RECOVERY-AND-LAST-GOOD-SEAL-13

family = optimizer-generation-failure-recovery
authority class = OptimizerDataPlane
production authority = FailureRecoveryCoordination
status = Active
direct parent = ASH-GENERATION-TRANSACTION-COORDINATOR-CLOSURE-12
runtime parent = ASH-MUON-RUNTIME-AUTHORITY-DECOMPOSITION-07
```

New head:

```text
optimizer-generation-failure-recovery
→ ASH-GENERATION-FAILURE-RECOVERY-AND-LAST-GOOD-SEAL-13
```

Execution-authority map adds only:

```text
generation_failure_recovery
→ ASH-GENERATION-FAILURE-RECOVERY-AND-LAST-GOOD-SEAL-13
```

Existing authorities remain:

```text
optimizer
→ Production Muon callsite

generation_transaction_coordination
→ ASH-GENERATION-TRANSACTION-COORDINATOR-CLOSURE-12
```

13 does not become optimizer computation authority.

## 19. Vocabulary

```text
owned data-plane revision = None
target data-plane revision = bp-dk-data-plane/active-fusion/v1
owned policy generation = None
owned qualification generation = None
```

The reconciliation patch number 13 is distinct from the historical BP-DK operator-review patch numbered 13.

```text
PATCH NUMBER != LINEAGE IDENTITY
```

## 20. New tooling

```text
tools/ash_generation_failure_recovery_13_registry.py
tools/validate_ash_generation_failure_recovery_and_last_good_seal_13.py
tools/run_ash_generation_failure_recovery_and_last_good_seal_13.ps1
```

The dedicated runner executes:

```text
00 lineage validation
12 transaction-coordinator validation
13 recovery validation
cargo check base_train --lib
cargo check base_train --bin base_train
```

No overlay application command is included.

## 21. Forward-compatible validator repair

13 changes the scheduler spelling from:

```text
let training_state_digest = commit_active_state(...)
```

to:

```text
let training_state_digest = match commit_active_state(...) { ... }
```

because publication failure now requires explicit classification.

Existing static validators that had pinned the old source spelling were narrowed to recognize the same publication authority under the 13 match wrapper. Their substantive ordering/policy constraints remain intact.

This includes the 03/04/11/12 reconciliation gates, production R6/Muon/residency gates, and BP-DK policy qualification validators whose production-scheduler fallback anchor depended on the old line spelling.

## 22. Parent diff boundary

Compared with 12 full-applied:

```text
changed files = 25
Rust files changed = 2
WGSL files changed = 0
Python files changed/added = 21
PowerShell files added/modified = 2
```

The only runtime Rust files changed are:

```text
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
```

No WGSL or GPU compute implementation is changed.

## 23. Baked static evidence

Validated work tree and re-extracted full ZIP both pass the 00→13 chain.

```text
00  228 / 228 PASS
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
```

Additional regression evidence:

```text
existing BP-Delta-K *_static.py validators: 25 / 25 PASS
CF1-enumerated Python validators: 69 / 69 PASS
changed Python source syntax: 21 / 21 PASS
changed Rust delimiter/string/comment lexical sanity: 2 / 2 PASS
```

CF1 was executed in bounded groups of 35 and 34 so every validator exit code completed within the execution-tool limit.

## 24. Physical evidence boundary

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
PowerShell dedicated runner = EvidenceInsufficient / not executed here
physical filesystem-failure fault matrix = EvidenceInsufficient / not executed here
physical fresh-process recovery continuation = EvidenceInsufficient / not executed here
10 physical behavior parity on 13 source = not executed here
11 physical resume parity on 13 source = not executed here
```

Because 13 changes Rust runtime control flow, any physical 10/11 receipts from an older runtime-source digest are stale and must be rerun against the 13 body before an end-to-end physical production closure claim.

Static PASS is not compile PASS.

## 25. Packaging

```text
Overlay Code ZIP: 25 files
Full Applied Code ZIP: 7246 files
```

Re-extracted full ZIP versus validated work tree:

```text
missing = 0
extra = 0
hash mismatch = 0
forbidden generated content = 0
```

Code ZIPs exclude Markdown specs, `*.sha256`, `*.pyc`, `__pycache__`, generated report/receipt/manifest output, and artifact/manifests directories.

## 26. Non-goals

13 does not implement:

```text
automatic previous-generation rollback
automatic last-good checkpoint search
same-process retry
partial in-memory stage resume
checkpoint schema redesign
giant runtime snapshot
R2E recovery substitution
GPU70K historical execution
optimizer formula changes
BP-Delta-K formula changes
GPU dispatch changes
D2H changes
power-loss durability closure
```

## 27. Recommended physical qualification order

On a Rust-capable host, the correct order is:

```text
cargo check
→ 10 decomposition behavior parity on 13 source
→ 11 load/resume parity on 13 source
→ 12 typed transaction failure tests
→ 13 publication/recovery fault matrix
```

The 13 fault matrix should cover at least:

```text
failure before target history write
failure after target history write but before active replacement
failure after active replacement before publication postcheck completes
Causal in-memory commit failure after filesystem publication
Objective/Trajectory/Calibration commit failures
abort failure before filesystem publication
active/history contradiction fail-closed
```

Test-only fault injection should remain qualification-only and must not create a production environment-variable failpoint.

## 28. Final seal

```text
AN ERROR DOES NOT CHOOSE THE RECOVERY GENERATION

THE FILESYSTEM CURRENT AUTHORITY CHOOSES IT

PREVIOUS IS ACCEPTED ONLY WHEN PREVIOUS IS EXACTLY PROVED CURRENT
TARGET IS ACCEPTED ONLY WHEN TARGET IS EXACTLY PROVED CURRENT
OTHERWISE RECOVERY SOURCE IS UNESTABLISHED

TARGET HISTORY ALONE IS NOT CURRENT AUTHORITY

commit_active_state() ERROR DOES NOT PROVE PUBLICATION DID NOT ADVANCE

TARGET-CURRENT FAILURE IS NEVER ABORTED BACK TO PREVIOUS
TARGET-CURRENT CANDIDATE IS NEVER RECLAIMED AS FAILED STAGING
CONTRADICTORY PUBLICATION PRESERVES EVIDENCE AND FAILS CLOSED

FILESYSTEM SUCCESS + IN-MEMORY COMMIT FAILURE
RECOVERS FROM TARGET CURRENT

PRE-FILESYSTEM FAILURE
RECOVERS FROM PREVIOUS CURRENT

THE FAILED PROCESS IS RECOVERY-FENCED
THE FENCE IS PROCESS-LOCAL
THE FENCE IS NOT CHECKPOINTED

NO SAME-PROCESS RETRY
NO AUTO ROLLBACK
NO LATEST CHECKPOINT GUESS
NO MTIME GUESS
NO HIGHEST GENERATION GUESS
NO PARTIAL-STAGE RESUME

FRESH-PROCESS RECONSTRUCTION
IS THE RECOVERY MECHANISM

12 TELLS US WHERE THE ORDERED IN-MEMORY TRANSACTION STOPPED
13 TELLS US WHICH EXACT FILESYSTEM WORLD A NEW PROCESS MAY WAKE UP IN

PROCESS/APPLICATION FAILURE RECOVERY IS IN SCOPE
UNPROVEN POWER-LOSS DURABILITY IS NOT CLAIMED
```
