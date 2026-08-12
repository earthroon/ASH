# ASH-BASETRAIN-BT-WGSL-CHECKPOINT-EXPORT-PROVENANCE-CAPTURE-CLI-FULL-SNAPSHOT-ADMISSION-06C-R27-R1J-R1

## Revision

- Patch ID: `ASH-BASETRAIN-BT-WGSL-CHECKPOINT-EXPORT-PROVENANCE-CAPTURE-CLI-FULL-SNAPSHOT-ADMISSION-06C-R27-R1J-R1`
- Build revision: `bt-wgsl-checkpoint-export-provenance-capture-cli-full-snapshot-admission-06c-r27-r1j-r1`
- Physical parent: `ASH-BASETRAIN-BT-WGSL-CHECKPOINT-EXPORT-PROVENANCE-CAPTURE-AND-WRITER-LINEAGE-06C-R27-R1J`
- Scope: BaseTrain CLI to existing `TrainingConfig` / `FullSnapshotGate` admission bridge
- Checkpoint writer semantics: unchanged
- R1J provenance capture semantics: unchanged
- Training / backward / optimizer math: unchanged
- Proof ledger: `HOLD`

## Parent SSOT

R27-R1J has a live checkpoint-export provenance capture wrapper armed by:

```text
ASH_R1J_CAPTURE_CHECKPOINT_EXPORT=1
```

R1J does not itself authorize a full checkpoint write. Current BaseTrain defaults remain:

```text
save_full_checkpoint=false
allow_full_snapshot_readback=false
require_explicit_full_snapshot_approval=true
```

Therefore a live R1J export requires two independent authorities:

```text
A. R1J capture arm
B. explicit full-snapshot CLI admission
```

The capture environment variable must never silently elevate snapshot permissions, and snapshot admission must never silently enable R1J capture.

## CLI contract

`base_train` exposes exactly these additional controls:

```text
--save-full-checkpoint
--allow-full-snapshot-readback
--full-snapshot-approval-token <FULL_SNAPSHOT_APPROVAL_TOKEN>
--full-snapshot-reason <FULL_SNAPSHOT_REASON>
```

Default invocation without these options preserves the previous full-snapshot-denied behavior.

## State ownership

The authority chain remains:

```text
CLI input
  -> BaseTrainArgs
  -> BaseTrainConfig.training
  -> existing FullSnapshotGate
  -> existing canonical checkpoint writer
  -> existing R1J live-capture wrapper
```

Ownership is separated as follows:

```text
CLI = explicit execution intent
TrainingConfig = runtime snapshot policy
FullSnapshotGate = explicit snapshot approval
checkpoint writer = checkpoint payload authority
R1J = provenance observation authority
```

No duplicate checkpoint-write authority is introduced.

## Exact CLI mapping

`--save-full-checkpoint` maps only to:

```text
cfg.training.save_full_checkpoint=true
```

`--allow-full-snapshot-readback` maps from one CLI source value to both existing readback owners:

```text
cfg.training.allow_full_snapshot_readback=true
cfg.training.full_snapshot_gate.allow_full_snapshot_readback=true
```

The two effective readback states must match. A split fails closed as:

```text
BASETRAIN_FULL_SNAPSHOT_READBACK_AUTHORITY_SPLIT
```

`--full-snapshot-approval-token` maps to:

```text
cfg.training.full_snapshot_gate.approval_token
```

Blank or whitespace-only token values are treated as missing. No token is synthesized from run identity, checkpoint path, output directory, host identity or the R1J capture environment.

`--full-snapshot-reason` maps to:

```text
cfg.training.full_snapshot_gate.reason
```

Reason handling remains owned by the existing gate; R1J-R1 does not invent a stricter or weaker reason policy.

The existing:

```text
cfg.training.require_explicit_full_snapshot_approval
```

continues to bind:

```text
cfg.training.full_snapshot_gate.require_explicit_approval
```

and is not disabled by this patch.

## Two-key admission

R1J live capture is possible only when:

```text
ASH_R1J_CAPTURE_CHECKPOINT_EXPORT=1
AND
save_full_checkpoint=true
AND
existing full-snapshot admission passes
```

The states are intentionally independent:

```text
capture env only -> no snapshot authorization
snapshot authorization only -> checkpoint export may occur without R1J capture
```

The CLI admission receipt may report `r1j_live_export_possible=true`, but that is not a physical export event. `real_export_event_observed` remains owned by R1J's writer-side capture.

## Input/output mutation boundary

The initial checkpoint remains source/read authority only. For the current BaseTrain diagnosis the physical input authority is:

```text
D:\1111113232\DUST\1\ash_pass3\models\quarantine\ash_v5_native_genesis_full.decode04_r3_tail_norm_repaired.safetensors
```

When a full snapshot is requested, the canonicalized initial checkpoint artifact path is compared with the planned final output checkpoint path. Exact artifact alias fails closed:

```text
BASETRAIN_FULL_SNAPSHOT_INPUT_OUTPUT_ALIAS
```

R1J-R1 must not mutate, repair, promote or overwrite the quarantine input checkpoint.

The explicit `--output-dir` remains output authority. No silent diagnostic directory, rename, suffix increment or fallback directory is introduced.

## Output-directory preflight

When full checkpoint saving is requested, BaseTrain probes the configured output directory for writability before training proceeds. This probe does not create snapshot authority and does not change the output path.

## Admission receipt

Before `prepare_training_config_and_device` and before training begins, BaseTrain prints:

```text
[base-train-full-snapshot-cli-admission-r27-r1j-r1]
```

The receipt contains at minimum:

```text
save_full_checkpoint_requested
allow_full_snapshot_readback_requested
approval_token_present
approval_reason_present
explicit_approval_required
effective_save_full_checkpoint
effective_allow_full_snapshot_readback
training_gate_readback_authority_match
r1j_capture_env_enabled
r1j_capture_snapshot_admission_separated
r1j_live_export_possible
init_checkpoint_output_alias
output_dir_writable
admission_verdict
```

The approval-token payload is never logged. Only presence is observable.

## Admission verdicts

Allowed verdict classes are:

```text
FULL_SNAPSHOT_NOT_REQUESTED
FULL_SNAPSHOT_REQUESTED_ADMITTED
FULL_SNAPSHOT_REQUESTED_APPROVAL_REQUIRED
FULL_SNAPSHOT_REQUESTED_READBACK_NOT_ALLOWED
FULL_SNAPSHOT_REQUESTED_INPUT_OUTPUT_ALIAS
FULL_SNAPSHOT_REQUESTED_CONFIG_AUTHORITY_MISMATCH
```

Stable CLI errors include:

```text
BASETRAIN_FULL_SNAPSHOT_APPROVAL_TOKEN_REQUIRED
BASETRAIN_FULL_SNAPSHOT_READBACK_NOT_ALLOWED
BASETRAIN_FULL_SNAPSHOT_INPUT_OUTPUT_ALIAS
BASETRAIN_FULL_SNAPSHOT_READBACK_AUTHORITY_SPLIT
```

No missing token/readback permission is silently repaired.

## Writer and training freeze

R1J-R1 must not alter:

```text
checkpoint writer implementation
checkpoint tensor ordering
checkpoint dtype policy
checkpoint offset policy
checkpoint serialization
R1J E0-E5 provenance semantics
intermediate full_step_* checkpoint route
base-train route selection
checkpoint-load semantics
LoRA semantics
backend semantics
model specification
tokenizer manifest
dataset manifest
training math
backward math
optimizer math
```

The existing `write_full_checkpoint_safetensors_with_r1j_capture()` remains the final checkpoint wrapper.

## R1J-R1 gate authority

The structural gate retains R1J and promotes R1J-R1 as the terminal diagnostic handoff.

R1J-R1 validates the CLI admission policy descriptor and semantic canaries without pretending that the gate invocation itself is a BaseTrain CLI export. In gate context:

```text
r1j_live_export_possible=false
```

is expected because the gate is not the actual training/export process.

## Receipt architecture

R1J-R1 emits 10 semantic waves:

```text
00 R1J parent
01 CLI declaration authority
02 default policy preservation
03 save-full-checkpoint mapping
04 readback mapping
05 approval token/reason mapping
06 capture-vs-snapshot authority separation
07 input/output mutation boundary
08 negative canaries / reproducibility
09 R1J live-export handoff
```

Required receipt contract:

```text
receipt_atlas_waves=10
receipt_chunk_max_fields<=8
parallel_chunk_build=1
streaming_chunk_write=1
deterministic_wave_merge=1
monolithic_final_json=0
```

## CLI gate contract

Exactly 48 R1J-R1 contract gates are required:

```text
--require-bt-wgsl-r27r1j-r1-contract-001
...
--require-bt-wgsl-r27r1j-r1-contract-048
```

They must be present in short args, full args, the dedicated R1J-R1 contract args and regenerated resolved args.

Expected repair-script output:

```text
r27r1j_r1_required_gate_count=48
r27r1j_r1_gate_cardinality_exact=1
```

## Negative canaries

At least 20 canaries preserve:

```text
default save=false
default readback=false
capture env does not imply save
save does not imply capture
save does not imply readback
readback does not imply save
token/reason alone do not imply save
blank token does not approve
token payload is not logged
input/output alias fails closed
quarantine source mutation remains zero
R1J PASS is not owned by CLI admission
checkpoint writer semantics remain unchanged
intermediate writer route remains unchanged
capture-disabled checkpoint export remains valid
```

## Reproducibility

The policy descriptor and semantic-canary set are built twice and must match exactly:

```text
reproducibility_runs=2
reproducibility_match=1
```

## Runtime handoff

An explicitly admitted live run has the intended path:

```text
BaseTrain CLI admission
  -> existing full-snapshot gate
  -> final checkpoint source snapshot collection
  -> write_full_checkpoint_safetensors_with_r1j_capture
  -> existing checkpoint writer
  -> R1J live capture journal
  -> R1J gate finalization
  -> ASH_CHECKPOINT_EXPORT_PROVENANCE_V1.json
  -> subsequent R1I E0-E6 diagnosis
```

## PASS semantics

R27-R1J-R1 PASS means the BaseTrain CLI physically exposes explicit full-checkpoint save, full-snapshot readback and approval metadata controls; those controls map to the existing configuration/gate owners; default denial is preserved; R1J capture and snapshot admission remain separate authorities; input/output aliasing is fail-closed; token payloads are not logged; and an explicitly approved BaseTrain run can reach the existing final checkpoint writer without changing writer, serialization, training or provenance semantics.

PASS does not mean:

```text
a checkpoint was exported
R1J captured provenance
R1J physical PASS occurred
R1I consumed provenance
the zero frontier was identified
the original checkpoint was repaired
```

## PASS seal

```text
PASS_ASH_BASETRAIN_BT_WGSL_CHECKPOINT_EXPORT_PROVENANCE_CAPTURE_CLI_FULL_SNAPSHOT_ADMISSION_06C_R27_R1J_R1
```
