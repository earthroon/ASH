# ASH-BASETRAIN-UNIFIED-ATLAS-MCU-REAL-PRODUCTION-PARAMETER-WAVE-ACTIVE-TRANSACTIONAL-COMMIT-AND-RESTART-CLOSURE-R1

## Revision

Parent: `ASH-BASETRAIN-UNIFIED-ATLAS-MCU-REAL-PRODUCTION-PARAMETER-WAVE-SHADOW-ADOPTION-AND-CANDIDATE-PARITY-CLOSURE-R1`

PASS: `PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_REAL_PRODUCTION_PARAMETER_WAVE_ACTIVE_TRANSACTIONAL_COMMIT_AND_RESTART_CLOSURE_R1`

## 1. Purpose

P2 proves that the current immutable MCU authority can replay actual production Muon Waves and reproduce the authoritative candidate. P3 closes the state-transition boundary: a P2-promoted production candidate may become the durable target generation only when weight, Adam M/V and Muon momentum are already physically restartable, and a fresh process must rebind that target without optimizer re-execution.

## 2. Source-derived authority model

The current source already owns the canonical generation transaction:

`candidate payload -> transaction.validated -> transaction.ready_for_commit -> commit_active_state() -> active_training_state.json -> record_generation_commit()`.

P3 MUST reuse this topology. It MUST NOT create a second optimizer commit coordinator, second training-state head, second GPU executor, or legacy-vs-MCU authority that the source no longer owns.

The durable commit point remains the validated atomic replacement of `training_state/active_training_state.json`. P3 PREPARE is a durable readiness seal before that point, not an irrevocable commit decision.

## 3. Runtime mode

Environment:

`ASH_UNIFIED_ATLAS_MCU_ACTIVE_TRANSACTIONAL_COMMIT_R1=OFF|ACTIVE_TRANSACTIONAL`

CLI:

`--admit-unified-atlas-mcu-active-transactional-commit-r1`

The CLI requires both `--admit-unified-atlas-mcu-real-production-wave-shadow-r1` and `--mcu-qualification-root`.

## 4. Mandatory parent gates

P3 Active requires:

- one valid P1 current immutable bundle;
- one P2 promotion receipt from the same ProductionMuonRuntime campaign;
- `P2.status=PROMOTED`;
- P2 PASS token present;
- all admitted real Waves passed;
- exact/bounded/nonfinite/status divergence counts all zero;
- all P2 shadow mutation counters zero;
- exact P1 bundle digest and pointer generation equality between P2 and P3.

No P2 promotion means no P3 PREPARE.

## 5. Generation invariant

Required:

`targetTrainingGeneration = sourceTrainingGeneration + 1`

`targetOptimizerGeneration = sourceOptimizerGeneration + 1`

A preexisting `committed_training_state_step_<target>.json` is an optimizer-generation fork and rejects PREPARE.

## 6. Durable domain boundary

P3 R1 admits only a target whose optimizer state is already durable under the parent packed-state authority.

Accepted: `R6A_PACK_PUBLICATION_STATE`.

Rejected: `R6A_PACK_RUN_LOCAL_RAM_MV_STATE`.

Failure: `E_MCU_P3_DURABLE_OPTIMIZER_STATE_REQUIRED`.

This is deliberate. P3 MUST NOT claim restart closure for Adam state that exists only in process RAM. A later Physical-N2/exact durable RAM child may widen this domain.

## 7. P3 restart participants

Current mandatory restart payload participants are:

1. `MODEL_WEIGHT_PACK`
2. `ADAM_M_PACK`
3. `ADAM_V_PACK`
4. `MUON_MOMENTUM`

Each participant binds role, logical file identity, target training generation, target optimizer generation, byte length and SHA-256.

The participant manifest is canonically sorted before hashing.

## 8. Physical evidence before PREPARE

Before PREPARE, P3 physically reopens all four participant files and requires exact size and SHA-256 parity with their authoritative manifests.

Muon momentum additionally requires:

`momentumManifest.generation == targetTrainingGeneration`

`momentumManifest.optimizerStep == targetOptimizerGeneration`.

A manifest-only readiness claim is insufficient.

## 9. PREPARE

Runtime artifact:

`<candidate-dir>/transaction.mcu_p3.prepare.json`

Schema: `ash.basetrain.mcu.active_transactional_commit.prepare.r1`.

PREPARE binds:

- source/target training generations;
- source/target optimizer generations;
- P1 bundle digest and pointer generation;
- P2 promotion receipt digest/status;
- candidate slot;
- candidate parameter-set digest;
- packed-state manifest physical digest;
- exact restart participants;
- participant-manifest digest;
- durable restart payload complete declaration;
- target-history preexistence observation;
- mutation-before-PREPARE count;
- prepare digest.

PREPARE is written only after the parent wrote `transaction.validated.json` and `transaction.ready_for_commit.json`, and before `commit_active_state()`.

Write protocol: create-new temp -> write -> `sync_all` -> rename -> reopen -> validate.

Existing identical PREPARE is idempotent. Different content at the same target is a transaction collision.

## 10. Existing durable head remains SSOT

P3 does not introduce another state-head file.

`training_state/active_training_state.json` remains the sole durable current-generation head.

P3 reuses the parent's `commit_active_state()` behavior: write committed history, write active partial, atomic replace, reopen, training-state digest validation, committed-history parity validation.

## 11. Failure boundary

Before target active-state publication: previous filesystem source may remain authority and the existing abort/recovery path applies.

After target active state is verified current: recovery must use the target filesystem state. The optimizer numerical transaction is not rerun merely to reconstruct the target.

The existing generation recovery fence remains authoritative for failures after filesystem publication.

## 12. Existing in-memory commit remains SSOT

P3 does not replace `ProductionMuonRuntime::record_generation_commit()`.

The existing BridgeTemporal, FusionPlanner, PostUpdate, CausalEffect, ObjectiveProbe, FusionTrajectory, CalibrationReplay, B04, B05 and B06 transitions remain owned by the existing generation transaction.

P3 only gates and witnesses the durable MCU state boundary around that transaction.

## 13. P3 commit receipt

Runtime artifact:

`<candidate-dir>/transaction.mcu_p3.commit_receipt.json`

It may be emitted only after:

1. `commit_active_state()` returned a validated target training-state digest;
2. `record_generation_commit()` succeeded;
3. P3 independently reopened `active_training_state.json`;
4. target generation, optimizer step, candidate set, packed manifest, candidate slot and training-state digest all matched PREPARE.

The receipt binds the transaction digest, P1/P2 authority, participant manifest, target state digest, filesystem target publication, in-memory generation commit, durable target reopen and the P3 PASS token.

`generationGapCount` is derived from source/target arithmetic. `generationForkCount` is derived from the target-history observation. `partialCommitCount` is derived from filesystem-current plus in-memory-commit observation. They are not caller-selected PASS booleans.

## 14. Restart rebind

When P3 Active is enabled, after ProductionMuonRuntime and P1 binding exist, startup checks the loaded source candidate directory for P3 PREPARE.

If no PREPARE exists, the source predates P3 and no P3 rebind claim is made.

If PREPARE exists, restart reopens the current `active_training_state.json` and requires exact parity for:

- training generation;
- optimizer generation;
- candidate parameter-set digest;
- packed-state manifest digest;
- candidate slot;
- training-state digest;
- P1 current bundle digest.

All P3 participant files are then reopened and rehashed.

## 15. Restart receipt

Runtime artifact:

`<candidate-dir>/transaction.mcu_p3.restart_rebind_receipt.json`

A valid rebind requires:

- exact weight rebind;
- exact Adam optimizer-state rebind;
- exact Muon momentum rebind;
- target filesystem state is current;
- `optimizerReexecuted=false`;
- P3 PASS token.

The P3 commit receipt may be absent if the previous process died after target publication or after in-memory commit but before P3 receipt persistence. Exact target-current + PREPARE + participant validation is sufficient to prove rebind without numerical optimizer re-execution.

## 16. No hidden authority expansion

P3 does not:

- commit P2 shadow candidate tensors;
- mutate R8 policy or expert selection;
- create Device/Queue/executor authority;
- retire exact GPU waits;
- invent Atlas lease generation;
- qualify fused-pair execution;
- claim RAM-local Adam durability;
- claim Physical-N2 closure where no exact child is produced;
- claim performance improvement.

## 17. Static gate

Validator:

`tools/validate_ash_basetrain_unified_atlas_mcu_active_transactional_commit_and_restart_r1_static.py`.

It verifies:

- P3 module/export and CLI gate;
- P1/P2 authority getters;
- exact durable participant roles;
- PREPARE after parent ready marker and before `commit_active_state()`;
- P3 finalize after `record_generation_commit()`;
- restart validation after ProductionMuonRuntime/P1 binding;
- durable optimizer-state gate;
- no second executor or shadow-commit API.

PASS token:

`PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_ACTIVE_TRANSACTIONAL_COMMIT_AND_RESTART_R1_STATIC`.

## 18. Physical qualification campaign

Minimum physical closure:

1. current P1 immutable bundle valid;
2. P2 ShadowObserved enabled and reaches PROMOTED on real production Waves;
3. P3 ActiveTransactional enabled;
4. target uses fully durable packed weight/Adam state;
5. Muon momentum target payload is durable;
6. P3 PREPARE seals;
7. existing `commit_active_state()` publishes target current;
8. existing `record_generation_commit()` completes;
9. P3 COMMITTED receipt appears;
10. process terminates;
11. fresh process loads target;
12. P3 restart rebind validates weight, Adam state and Muon momentum;
13. `optimizerReexecuted=false`.

Failure injection should cover faults before PREPARE, after PREPARE, after committed-history write, after active partial write, after active replace, after filesystem target publication but before in-memory commit, during B04/B05/B06 finalize, and after in-memory commit but before the P3 receipt.

## 19. Packaging policy

Implementation source ZIP excludes:

- this specification and all `specs/` content;
- Markdown patch notes;
- `BAKE_MANIFEST*`;
- generated qualification receipts/evidence;
- generated P3 prepare/commit/restart JSON;
- `current.json` and `publication_seal.json` runtime artifacts;
- checkpoint/N2 runtime payload artifacts;
- validation logs and review reports.

Rust/Python source implementing these concepts remains included.

GitHub publication for this revision is spec-only unless implementation publication is separately requested.

## 20. PASS semantics

P3 PASS means the current P1 authority had reached P2 real-Wave promotion, the exact target weight, Adam M/V and Muon momentum payloads were physically durable and digest-valid before P3 PREPARE, source and target generations were exact +1, no target history already existed, the existing atomic active-training-state publication remained the sole durable commit point, the existing ProductionMuon generation coordinator remained the sole in-process commit authority, and a fresh process rebound the exact committed target state without optimizer numerical re-execution.

P3 PASS does not mean RAM-local deferred Adam state is restart-closed, exact Atlas lease generation exists, ActiveAsync is enabled, exact waits are retired, fused-pair is qualified, hardware Tensor Core E3 is active, or long-horizon optimization quality is closed.

## 21. Next revision

Next:

`ASH-BASETRAIN-UNIFIED-ATLAS-MCU-EXACT-ATLAS-SLOT-LEASE-GENERATION-THREADING-AND-STALE-RESIDENCY-CLOSURE-R1`.

Exact slot + lease generation should be threaded through allocation -> R6 descriptor -> R8 assignment -> R8A indexed execution -> submission -> completion -> reclamation before ActiveAsync exact-wait retirement.

## Center sentence

**P2는 실제 Wave에서 같은 답을 내는지 증명했다. P3는 그 답이 디스크와 메모리 사이에서 찢어지지 않게 한다. PREPARE는 건널 준비가 끝났다는 봉인이고, 진짜 강 건너편은 기존 `active_training_state.json`이다. 그 파일이 target을 가리킨 뒤 재시작하면 계산을 다시 하지 않고 exact target state를 다시 잡는다.**