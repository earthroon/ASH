# ASH-BP-DK-FUSION-MANAGED-TRAINER-AUTHORITY-WINDOWS-LOCK-DURABILITY-RECOVERY-15B-R1

## Patch identity

```text
ASH-BP-DK-FUSION-MANAGED-TRAINER-AUTHORITY-
WINDOWS-LOCK-DURABILITY-RECOVERY-15B-R1

Windows Directory Durability Backend Repair /
Managed Trainer Lock Immediate Cleanup Ownership /
Crash-Safe Stale Lock Classification /
PID-Reuse Guard /
Atomic Stale Lock Quarantine /
Bounded Lock Reacquisition /
File-Level Flush Preservation /
Active Pointer Write-Through Preservation /
No Silent Directory-Fsync Emulation /
Activation 15·15A Authority Semantics Preservation Seal
```

Parents:

```text
ASH-BP-DK-FUSION-POLICY-EXPLICIT-PRODUCTION-ACTIVATION-15
ASH-BP-DK-FUSION-POLICY-LEGACY-RESTART-BARRIER-CLOSURE-15A-R1
```

15B repairs Windows lock lifecycle and platform durability only. Policy qualification, operator review, managed activation, LEGACY_UNBOUND classification, first managed policy adoption, checkpoint binding, and one-way legacy-to-managed semantics remain owned by 15 and 15A.

## Observed Windows failure

A physical `seal-legacy-restart-barrier` invocation produced:

```text
Error: Access is denied. (os error 5)
```

and left a 144-byte lock:

```json
{
  "ownerPid": 75684,
  "purpose": "LEGACY_RESTART_BARRIER",
  "schemaRevision": "ash.bp_dk.fusion_policy.managed_trainer_authority_lock.r1"
}
```

The owner PID was no longer present.

The previous acquisition order was:

```text
create_new(lock)
payload write
lock file sync_all
Windows sync_directory(parent)
construct cleanup guard
```

The Windows `sync_directory()` implementation opened a directory read-only with `FILE_FLAG_BACKUP_SEMANTICS` and then called `File::sync_all()`. The call can fail with access denied, and because the cleanup guard did not yet exist, the lock remained stale.

The same `sync_directory()` helper is reused by policy-store, bootstrap, activation, rollback, and active-pointer transactions. Therefore fixing only the lock callsite would merely move the same Windows failure to the next policy transaction.

## Platform durability contract

15B makes the platform contract explicit.

Unix:

```text
UNIX_FILE_SYNC_PLUS_DIRECTORY_FSYNC
```

Durable files use `file.sync_all()` and directory namespace commits retain directory fsync.

Windows:

```text
WINDOWS_FILE_SYNC_PLUS_WRITE_THROUGH_NAMESPACE
```

Durable files retain `file.sync_all()`. Active-pointer replacement retains `MoveFileExW` with `MOVEFILE_REPLACE_EXISTING | MOVEFILE_WRITE_THROUGH`. Windows `sync_directory()` verifies that the namespace path is an actual directory but does not issue the old read-only directory `sync_all()` call.

15B does not claim that Windows performed Unix directory-fsync semantics.

## Durable artifact preservation

The following remain unchanged as durability authorities:

```text
write_json_sync -> file.sync_all()
write_immutable_json -> file.sync_all()
replace_active_file on Windows -> MoveFileExW(... MOVEFILE_WRITE_THROUGH)
```

The two revision-1 bootstrap pointer commits now also use `replace_active_file()` instead of raw `fs::rename(&temp, &active_path)`, giving the bootstrap path the same Windows write-through namespace primitive already used by normal pointer activation.

## Managed trainer lock lifecycle

The coordination lock remains:

```text
runtime/bp_dk_fusion_managed_trainer_authority.lock
```

It is ephemeral single-writer coordination state, not policy history.

The critical ownership rule is now:

```text
create_new succeeds
-> cleanup guard exists immediately
-> payload construction/write/flush/namespace verification
```

Any error after namespace creation therefore drops the guard and removes the half-created lock.

The old post-create orphan window is closed.

## Windows lock schema R2

New Windows acquisitions write:

```text
ash.bp_dk.fusion_policy.managed_trainer_authority_lock.r2
```

Fields:

```text
schemaRevision
ownerPid
ownerProcessCreationTime
ownerExecutablePath
purpose
createdUnixMillis
lockInstanceNonce
```

`ownerProcessCreationTime` is read with Windows `OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION)` plus `GetProcessTimes`.

The canonical live-owner identity on Windows is:

```text
(owner PID, process creation time)
```

Executable path is a diagnostic witness, not the primary identity.

## Existing-lock classification

15B classifies an existing Windows lock as one of:

```text
LIVE_EXACT_OWNER
STALE_OWNER_ABSENT
STALE_PID_REUSED
LEGACY_R1_STALE_OWNER_ABSENT
LEGACY_R1_OWNER_IDENTITY_UNVERIFIABLE
```

R2 behavior:

```text
PID absent -> stale owner absent
PID present + creation time exact -> live exact owner
PID present + creation time different -> stale PID reuse
```

Legacy R1 behavior:

```text
PID absent -> recoverable stale lock
PID present -> fail closed, because R1 has no creation-time identity and PID reuse cannot be disproven
```

Unknown/malformed lock schemas fail closed. Lock age is never used as stale authority.

## No time-based reclaim

15B deliberately does not use:

```text
lock older than N minutes
heartbeat TTL
lease expiration
```

A legitimate BaseTrain production run may remain active for hours. Stale recovery is based on process identity, not elapsed time.

## Stale quarantine

A proven stale lock is not first deleted in place.

It is atomically renamed to:

```text
<policy_root>/runtime/stale/
bp_dk_fusion_managed_trainer_authority.<nonce>.stale.lock
```

A recovery receipt is then written next to it:

```text
bp_dk_fusion_managed_trainer_authority.<nonce>.recovery.json
```

The receipt records:

```text
recovery reason
previous lock schema
previous owner PID
quarantine path and SHA-256 digest
recovering PID
recovering process creation time
recovery timestamp
reacquire attempt count
Windows directory durability mode
```

The original stale lock bytes are preserved as evidence.

## Bounded reacquisition

The acquisition loop is capped at:

```text
ASH_BP_DK_FUSION_MANAGED_TRAINER_MAX_REACQUIRE_ATTEMPTS = 2
```

A typical recovery is:

```text
attempt 1
existing R1 dead-owner lock
classify LEGACY_R1_STALE_OWNER_ABSENT
quarantine

attempt 2
create_new succeeds
R2 lock acquired
```

If authority still cannot be acquired within the bounded window, the operation fails with:

```text
ASH_BP_DK_FUSION_MANAGED_TRAINER_AUTHORITY_REACQUIRE_EXHAUSTED
```

No spin loop is permitted.

## Live owner exclusion

A live exact R2 owner continues to produce:

```text
ASH_BP_DK_FUSION_MANAGED_TRAINER_AUTHORITY_BUSY
```

A live legacy R1 PID produces:

```text
ASH_BP_DK_FUSION_MANAGED_TRAINER_AUTHORITY_OWNER_IDENTITY_UNVERIFIABLE
```

15B never terminates another process. No `TerminateProcess`, taskkill, or process-kill path exists in the recovery implementation.

## Representative failure codes

```text
ASH_BP_DK_FUSION_MANAGED_TRAINER_AUTHORITY_BUSY
ASH_BP_DK_FUSION_MANAGED_TRAINER_AUTHORITY_CREATE_FAILED
ASH_BP_DK_FUSION_MANAGED_TRAINER_AUTHORITY_OWNER_IDENTITY_UNVERIFIABLE
ASH_BP_DK_FUSION_MANAGED_TRAINER_AUTHORITY_LOCK_MALFORMED
ASH_BP_DK_FUSION_MANAGED_TRAINER_AUTHORITY_STALE_QUARANTINE_FAILED
ASH_BP_DK_FUSION_MANAGED_TRAINER_AUTHORITY_REACQUIRE_EXHAUSTED
ASH_BP_DK_FUSION_WINDOWS_DURABILITY_DIRECTORY_REQUIRED
```

## Activation 15 and 15A preservation

The following semantic boundaries remain intact:

```text
normal Activation-15 barrier still requires replay evidence
normal managed-to-managed transition remains separate
LEGACY_UNBOUND still means binding absent + replay absent
partial managed state still hard-fails
legacy target policy still requires qualification/review lineage
legacy source checkpoint remains read-only
first managed pointer remains revision 1 with no previous pointer
legacy-to-managed closure remains one-way
```

15B changes no policy-selection or training-math decision.

## Implementation surface

The baked overlay contains exactly seven files:

```text
crates/base_train/src/bp_delta_k_fusion_policy_explicit_production_activation.rs

tools/validate_ash_bp_dk_fusion_policy_explicit_production_activation_15_static.py
tools/validate_ash_bp_dk_fusion_managed_trainer_authority_windows_lock_durability_recovery_15b_r1_static.py
tools/validate_ash_bp_dk_fusion_policy_production_soak_and_rollback_health_16_static.py
tools/validate_ash_bp_dk_fusion_policy_production_long_horizon_stability_17_static.py
tools/validate_ash_bp_dk_fusion_policy_production_evidence_recalibration_bridge_18_static.py
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
```

No `*.sha256`, generated artifact tree, manifest bundle, or Python cache is included.

## Parent SHA fanout

Before 15B, the Activation-15 BaseTrain source SHA-256 was:

```text
e38572fe8aa513b1ff5e28519f7fabb236cb076632a187723fc3d0573e4e1a8a
```

After 15B:

```text
1e110a99c0087db2ad25bd98397ed70bf6f8722a89140ae061688220a6f69bc8
```

Exact occurrence search shows only production validators 16, 17, and 18 pin this source hash. Those three parent pins are rebaked. 19-21 do not require a new source-hash edit.

## CF1 order

The new validator is inserted as:

```text
14
-> 15
-> 15A
-> 15B
-> 16
-> 17
-> 18
-> 19
-> 20
-> 21
```

## Static evidence

Observed on the reconstructed cumulative source tree:

```text
15B Windows Lock Durability Recovery:                          91/91 PASS
Activation 15:                                               279/279 PASS
Legacy Restart Barrier Closure 15A:                          153/153 PASS
Production Soak/Rollback 16:                                 177/177 PASS
Production Long Horizon 17:                                  225/225 PASS
Production Recalibration Bridge 18:                          298/298 PASS
Production Calibration Adoption 19:                          230/230 PASS
Production Aware Recommendation 20:                          237/237 PASS
Production Operator Review/Adoption 21:                      265/265 PASS
N8 HiMuon Production Hotpath Bind:                             86/86 PASS
N8 Phase Wall-Time Attribution:                                77/77 PASS
N8 Deferred Durable Writeback:                                 PASS
```

The bake container does not contain a Rust toolchain. The authoritative Windows Release CF1 remains the compilation/type/borrow and physical platform authority.

## Windows physical acceptance

The first physical 15B acceptance should prove:

```text
Release CF1 PASS
existing dead-owner R1 lock is automatically classified stale
stale lock is quarantined under runtime/stale
recovery JSON is emitted
new R2 lock is acquired
no Windows os error 5 during lock acquisition
seal-legacy-restart-barrier exits 0
legacy barrier receipt physically exists
managed trainer lock is absent after the command returns
```

Continuation through the 15A bootstrap should additionally prove:

```text
qualified target immutable policy is written
legacy adoption intent is written
revision-1 active pointer is created
no Windows os error 5 in policy/bootstrap directory transactions
```

## Promotion tokens

Structural:

```text
PASS_ASH_BP_DK_FUSION_MANAGED_TRAINER_AUTHORITY_WINDOWS_LOCK_DURABILITY_STRUCTURAL_15B_R1
```

Windows durability backend:

```text
PASS_ASH_BP_DK_FUSION_WINDOWS_PLATFORM_DURABILITY_BACKEND_15B_R1
```

Post-create cleanup:

```text
PASS_ASH_BP_DK_FUSION_MANAGED_TRAINER_LOCK_POST_CREATE_FAILURE_CLEANUP_15B_R1
```

Stale recovery:

```text
PASS_ASH_BP_DK_FUSION_MANAGED_TRAINER_AUTHORITY_STALE_LOCK_RECOVERY_15B_R1
```

Live-owner exclusion:

```text
PASS_ASH_BP_DK_FUSION_MANAGED_TRAINER_AUTHORITY_LIVE_OWNER_EXCLUSION_15B_R1
```

Physical Windows:

```text
PASS_ASH_BP_DK_FUSION_MANAGED_TRAINER_AUTHORITY_WINDOWS_PHYSICAL_15B_R1
```

Final:

```text
PROMOTE_ASH_BP_DK_FUSION_MANAGED_TRAINER_AUTHORITY_WINDOWS_LOCK_DURABILITY_RECOVERY_15B_R1
```

Static-only state remains:

```text
HOLD_ASH_BP_DK_FUSION_MANAGED_TRAINER_AUTHORITY_WINDOWS_PHYSICAL_VALIDATION_REQUIRED_15B_R1
```

until the Windows CF1 and physical lock/barrier sequence are observed.

## Final SSOT

```text
The managed trainer authority lock is ephemeral single-writer coordination state, not durable policy history.

Cleanup ownership begins immediately after create_new succeeds. A post-create initialization failure must not leave an ownerless namespace lock.

A dead process must not permanently own managed trainer authority. On Windows, R2 live-owner identity is PID plus process creation time. PID reuse is stale, not live ownership.

A proven stale lock is quarantined with evidence before bounded reacquisition. A live exact owner is never reclaimed. A live legacy R1 PID remains fail-closed because R1 cannot disprove PID reuse.

Windows does not pretend to provide Unix directory fsync semantics. Durable files retain file.sync_all(), and active-pointer namespace replacement retains MoveFileExW WRITE_THROUGH. Unix directory fsync remains unchanged.

Activation 15 and 15A policy semantics are unchanged. 15B repairs lifecycle and platform durability only.
```
