# ASH-BASETRAIN-BT-WGSL-CHECKPOINT-EXPORT-PROVENANCE-CAPTURE-ATLAS-RUNTIME-ROUTE-ADMISSION-06C-R27-R1J-R2

## Revision

- Patch ID: `ASH-BASETRAIN-BT-WGSL-CHECKPOINT-EXPORT-PROVENANCE-CAPTURE-ATLAS-RUNTIME-ROUTE-ADMISSION-06C-R27-R1J-R2`
- Build revision: `bt-wgsl-checkpoint-export-provenance-capture-atlas-runtime-route-admission-06c-r27-r1j-r2`
- Physical parent: `ASH-BASETRAIN-BT-WGSL-CHECKPOINT-EXPORT-PROVENANCE-CAPTURE-CLI-FULL-SNAPSHOT-ADMISSION-06C-R27-R1J-R1`
- Route: `AtlasGroupedSequential`
- Scope: AW00 `Prepared` transaction to explicit runtime admission to AW01 residency handoff
- Checkpoint writer semantics: unchanged
- R1J E0-E5 provenance semantics: unchanged
- Forward / training commit / checkpoint-export authority: closed
- Proof ledger: `HOLD`

## Parent condition

R1J-R1 exposes explicit full-snapshot CLI admission while preserving the separation between snapshot permission and the independent R1J capture arm. The remaining Atlas route blocker is not snapshot admission. In the prior route, `prepare_atlas_wave_00_runtime_hold()` always produced a valid AW00 `Prepared` transaction and then returned the typed AW00 HOLD before runtime residency could be entered.

R1J-R2 does not delete that safety behavior. It adds a separate explicit route-admission authority so that the unadmitted path still returns the existing AW00 HOLD while an explicitly admitted, physically bound route may proceed only as far as AW01 residency handoff.

## Explicit route admission

BaseTrain adds:

```text
--admit-atlas-runtime-route
```

Default:

```text
false
```

Therefore `--base-train-route atlas_grouped_sequential` alone continues to use the historical fail-closed AW00 path.

The R1J capture environment variable and R1J-R1 snapshot flags do not imply Atlas runtime admission. Conversely Atlas runtime admission does not imply R1J capture or full-snapshot admission.

Three independent authorities remain:

```text
A = ASH_R1J_CAPTURE_CHECKPOINT_EXPORT
B = explicit full-snapshot admission
C = --admit-atlas-runtime-route

A != B != C
```

## AW00 transaction preservation

The existing `BaseTrainAtlasWaveStepTransaction` remains a `Prepared` transaction. R1J-R2 does not rewrite its `admitted_transition_ceiling`, transaction ID, receipt digest or previous mutation-firewall evidence.

The implementation separates transaction construction from unconditional HOLD enforcement:

```text
prepare_atlas_wave_00_runtime_transaction(...)
```

builds and validates the existing AW00 `Prepared` state, while the historical unadmitted branch continues through the retained typed HOLD.

No previous AW00 zero-forward / zero-loss / zero-backward / zero-optimizer / zero-checkpoint-write receipt is retroactively changed.

## Primary GPU runtime ownership

A normal `WgpuDevice::DefaultDevice` does not expose the raw runtime handles required by the existing AW01 same-process residency authority. R1J-R2 therefore does not create a default training device and then silently bootstrap a second device.

When and only when explicit Atlas runtime admission is requested, BaseTrain creates one `ExistingDeviceBootstrap` as the primary training runtime before training begins:

```text
prepare_training_config_and_atlas_runtime_bootstrap(...)
```

The resulting Burn `WgpuDevice::Existing` and its extracted native runtime handles refer to the same primary device and queue. The admission module uses `try_extract_runtime_handles()` on that existing primary device and does not invoke a second bootstrap.

The base_train dependency enables the existing `burn-raw-access-local` feature for this exact handle extraction. The bootstrap source `base_train_r27r1j_r2_atlas_runtime_route_admission` is also admitted to the existing large-buffer-limit policy required by Atlas residency.

Required invariants:

```text
new secondary runtime bootstrap inside admission = 0
fresh-init fallback = 0
legacy full-checkpoint fallback = 0
generic attention fallback = 0
full-model checkpoint preload/materialization = 0
```

## Production plan authority

R1J-R2 requires all three runtime-plan inputs:

```text
--tensor-group-manifest
--atlas-group-plan
--sequential-load-plan
```

Presence is not sufficient. The documents must parse through the existing BaseTrain AW01 runtime schemas and join successfully through the existing plan authority.

The current runtime schema authority remains the existing Rust types. No R1J-specific parallel schema is introduced.

### Tensor group manifest

```text
groups[]
  group_id
  group_order
  tensor_keys[]
```

### Atlas group plan

```text
max_slot_bytes

groups[]
  group_id
  slices[]
    tensor_key
    logical_element_start
    logical_element_count
    slot_segment_index
    slot_byte_offset
    padded_byte_len
```

### Sequential load plan

```text
waves[]
  wave_order
  group_id
```

The existing `join_atlas_wave_01_plans()` remains the semantic join authority. A small public helper reads and validates `max_slot_bytes` using the same runtime AtlasGroupPlan schema.

## Fixture and symbolic-plan quarantine

Known `workspace/runtime/.../input_fixture/` plans remain fixtures and are explicitly rejected by R1J-R2 production admission.

The root `ASH_TOK_TENSOR_03_*` files are symbolic/planning contracts rather than the current BaseTrain AW01 runtime schema and are explicitly rejected from automatic production adoption.

Required:

```text
fixture_plan_auto_promotion=0
symbolic_plan_contract_auto_adoption=0
```

R1J-R2 does not synthesize missing production plans from a checkpoint header. Production plan materialization, if needed, is a separate frontier.

## Checkpoint binding

The admission path retains the existing CheckpointAtlas source authority. FreshInit is rejected.

The checkpoint is physically verified and its header parsed through the existing checkpoint authority. The runtime plan set must bind to the same checkpoint/model-source generation and pass existing tensor/range/plan validation before AW01 may be entered.

For the current diagnostic lineage, the base checkpoint authority remains the quarantined V5 checkpoint and its established checkpoint identity. R1J-R2 does not create a replacement checkpoint identity or rewrite the source checkpoint.

## AW01 physical residency admission

When explicit route admission, checkpoint authority and production runtime plans all pass, R1J-R2:

1. creates and validates the existing AW00 `Prepared` transaction;
2. binds the existing primary device/queue runtime handles;
3. constructs the existing `BaseTrainAtlasWave01ResidencyCoordinator`;
4. executes the existing bounded AW01 full-wave residency / seed-handoff path;
5. requires the existing `ResidencyHandoffReady` terminal state.

The existing triple-ring residency geometry and same-device runtime semantics are preserved. No alternate residency implementation is introduced.

## R2 authority ceiling

R1J-R2 admits only AW01 residency entry and handoff.

Required terminal policy:

```text
aw01_entry_admitted=true
forward_execution_admitted=false
training_commit_admitted=false
checkpoint_export_admitted=false
```

A successful physical R2 run therefore emits its R2 PASS seal and then terminates with:

```text
HOLD_ASH_BASETRAIN_R1J_R2_ATLAS_RESIDENCY_READY_FORWARD_EXECUTION_NOT_YET_ADMITTED
```

The ordinary training loop must not begin in the R2 physical-admission run. A bounded preflight batch may be built only to satisfy the existing AW00 transaction input authority.

## Mutation and fallback firewall

R1J-R2 must preserve:

```text
forward dispatch = 0
loss compute = 0
backward execution = 0
optimizer execution = 0
checkpoint write/rewrite = 0
weight value mutation = 0
R1J real export event = 0
```

AW01 may perform only the existing residency side effects such as bounded checkpoint-range reads, GPU buffer allocation/upload, queue submission, physical verification and residency lease lifecycle.

Those R2 activities are recorded in new R2 receipts and are not retroactively attributed to the old AW00 mutation firewall.

## Runtime verdicts

The R2 runtime may classify:

```text
ATLAS_RUNTIME_NOT_REQUESTED
ATLAS_RUNTIME_PLAN_AUTHORITY_UNAVAILABLE
ATLAS_RUNTIME_PLAN_SCHEMA_INVALID
ATLAS_RUNTIME_CHECKPOINT_BINDING_MISMATCH
ATLAS_RUNTIME_AW00_PARENT_INVALID
ATLAS_RUNTIME_NATIVE_RUNTIME_UNAVAILABLE
ATLAS_RUNTIME_AW01_BIND_FAILED
ATLAS_RUNTIME_RESIDENCY_HANDOFF_FAILED
ATLAS_RUNTIME_ADMITTED_RESIDENCY_READY
```

A missing or quarantined production plan set is evidence-insufficient for physical admission and must block rather than fall back.

## Structural gate contract

The structural R27 diagnostic gate retains all R1A through R1J-R1 parents and promotes R1J-R2 as the new terminal contract bridge.

The gate does not pretend that a production BaseTrain AW01 residency run occurred. Its R2 contract receipt must explicitly retain:

```text
physicalRuntimePass=false
runtimeAdmissionStatus=ATLAS_RUNTIME_NOT_REQUESTED
productionPlanAuthorityAvailableInGateContext=false
```

The R2 PASS token in this gate means the route-admission contract is present and internally consistent, not that physical AW01 admission has happened.

## Receipt architecture

R1J-R2 uses 12 semantic waves:

```text
00 R1J-R1 parent
01 AW00 Prepared transaction binding
02 explicit runtime admission request
03 checkpoint + plan-set identity
04 runtime plan schema validation
05 native WGPU runtime identity
06 AW01 coordinator bind
07 bounded checkpoint-range residency upload
08 residency lifecycle / generation fence
09 residency handoff
10 mutation / fallback firewall
11 R1J next-frontier handoff
```

Required:

```text
receipt_atlas_waves=12
receipt_chunk_max_fields<=8
parallel_chunk_build=1
streaming_chunk_write=1
deterministic_wave_merge=1
monolithic_final_json=0
```

## Gate cardinality

Exactly 48 R1J-R2 gates are required:

```text
--require-bt-wgsl-r27r1j-r2-contract-001
...
--require-bt-wgsl-r27r1j-r2-contract-048
```

They are integrated into short args, full args, a dedicated R1J-R2 contract args file and resolved-args repair.

Expected repair output includes:

```text
r27r1j_r2_required_gate_count=48
r27r1j_r2_gate_cardinality_exact=1
```

## Negative canaries

At least 26 semantic canaries cover:

- no admission flag retains AW00 HOLD;
- R1J capture alone cannot admit runtime;
- full-snapshot admission alone cannot admit runtime;
- fixture plans cannot auto-promote;
- symbolic TOK-TENSOR-03 plans cannot auto-promote;
- mixed/wrong plan and checkpoint authority rejects;
- invalid group, slice and slot geometry rejects;
- AW00 transaction/digest mutation rejects;
- FreshInit / legacy / generic-attention fallbacks reject;
- a second runtime/device path rejects;
- mixed device/queue ownership rejects;
- forward, backward, optimizer, checkpoint write and weight mutation remain prohibited in R2.

## Current physical status

R1J-R2 code/contract admission can be statically validated, but physical AW01 R2 admission still requires a production-compatible runtime plan trio. The known local plan files identified during this frontier are fixtures or symbolic contracts and are intentionally not promoted.

Therefore a physical BaseTrain R2 command must not be fabricated with those known invalid inputs. Until a production plan set exists, the correct next frontier is production Atlas plan materialization.

## PASS semantics

`PASS_ASH_BASETRAIN_BT_WGSL_CHECKPOINT_EXPORT_PROVENANCE_CAPTURE_ATLAS_RUNTIME_ROUTE_ADMISSION_06C_R27_R1J_R2` means the AW00 fail-closed contract is preserved while an explicit, independently authorized, exact-checkpoint-and-plan-bound path can transfer ownership from the immutable AW00 `Prepared` transaction into the existing same-device AW01 residency authority and reach `ResidencyHandoffReady`, without entering forward/training/checkpoint-export authority.

It does not mean forward, loss, backward, optimizer, checkpoint export, R1J provenance capture, R1I causal classification or checkpoint repair occurred.

## PASS seal

```text
PASS_ASH_BASETRAIN_BT_WGSL_CHECKPOINT_EXPORT_PROVENANCE_CAPTURE_ATLAS_RUNTIME_ROUTE_ADMISSION_06C_R27_R1J_R2
```

## Successful R2 terminal HOLD

```text
HOLD_ASH_BASETRAIN_R1J_R2_ATLAS_RESIDENCY_READY_FORWARD_EXECUTION_NOT_YET_ADMITTED
```

## Next frontier

If no production-compatible plan set exists, the next frontier is a separate production Atlas plan materialization patch. After physical AW01 residency is established, a later bridge may address Atlas runtime snapshot/export authority without falling back to a full-model Burn preload.