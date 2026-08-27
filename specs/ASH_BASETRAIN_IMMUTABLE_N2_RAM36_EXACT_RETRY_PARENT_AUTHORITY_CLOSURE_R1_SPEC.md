# ASH-BASETRAIN-IMMUTABLE-N2-RAM36-EXACT-RETRY-PARENT-AUTHORITY-CLOSURE-R1

## Status

Implementation-bound closure for the current direct promoted N8 retry parent.

This revision seals two already-existing authorities as one exact retry admission pair without merging their ownership:

- immutable Physical N2 = durable training-state parent authority
- RAM36 exact inventory = host-memory admission parent authority

The pair is a conjunction gate only. It does not create a replacement training-state SSOT, replacement RAM inventory, or replacement physical promotion receipt.

## Current sealed Physical N2

```text
Promotion directory:
E:\ASH\base_train_runs\physical_n2_promotions\promotion_20260826_095930

Physical N2 run:
E:\ASH\base_train_runs\physical_n2\n2_20260826_023007

Generation:      5
Optimizer step:  5
Cursor next:     19

Active state SHA256:
b1c236c113ca3994796f56f2a05f730557b42bfaa81d278069c1688eb9c58115

Packed manifest SHA256:
d9872144177d442a17a5b5c36aff8f886d9addee324faeb5be796478e815dc82

Weight pack SHA256:
13f340c75840f1417f5663c95fc321a89ecd2a56b455b8b288608ea1f9ac6182

Adam-M pack SHA256:
7e3ae9a74297bacbc47db9b3e68751e12d58ac1351ea9534fb09178e0586242e

Adam-V pack SHA256:
4a06f712f3a3566ce8ae16713775ef699fe2f627cd8140043ee2e3b54067120d
```

## Current sealed RAM36 parent

```text
Parent exact-inventory receipt:
D:\1111113232\DUST\1\ash_pass3\workspace\base_train_runs\n8_d10_baseline_smoke_20260822_181612\basetrain_ram_exact_inventory_receipt.json

Receipt SHA256:
827814b7dd1c8de3a6aff0887e8cc961930606e6c7629470836814e35eddc477

Hard process limit:
38,654,705,664 bytes
36 GiB exact
```

An older or newly regenerated inventory receipt is not substitutable merely because its numerical RAM totals are similar.

## Ownership rule

```text
Physical N2 owns:
- training generation
- optimizer step
- dataset cursor
- active training state
- packed-state manifest identity
- weight payload
- Adam-M payload
- Adam-V payload

RAM36 owns:
- exact parent inventory identity
- process-memory admission lineage
- exact 36 GiB process hard limit

Physical N2 does not authorize RAM usage.
RAM36 does not authorize training-state identity.
```

## Exact retry parent conjunction

```text
ExactRetryParentValid =
    ExactPhysicalN2
AND ExactRAM36Parent
```

No semantic-equivalent substitution is permitted.

The runtime gate requires exact material identity rather than matching only generation numbers, tensor counts, byte counts, or semantic values.

## Implementation boundary

New source authority module:

```text
crates/base_train/src/immutable_n2_ram36_exact_retry_parent_authority.rs
```

Runtime admission flag:

```text
--admit-immutable-n2-ram36-exact-retry-parent-authority
```

The flag is valid only for the direct promoted N8 parent with RAM36 exact-inventory/process-budget admission enabled.

Legacy-migration descendant source authority is outside this exact direct-parent closure.

Existing authorities are reused rather than cloned:

- `N8ParentBinding`
- `PhysicalN2PromotionReceipt`
- `HostProcessRamBudget::load_parent_inventory`
- `RAM36_PROCESS_BUDGET_HARD_LIMIT_BYTES`

The closure emits an in-memory witness and a console PASS token. It does not write a new manifest or mutate the parent.

## Runtime validation order

For the direct promoted N8 + RAM36 route:

```text
N8 promoted-parent binding
-> same/cross-release consumer compatibility validation
-> immutable N2 / RAM36 exact retry parent validation
-> storage preflight
-> source load
-> training
```

The closure therefore validates the parent before training-state execution advances.

## Physical N2 requirements

All are mandatory:

```text
Exact promotion directory /
Exact physical N2 run directory /
GEN5 /
OPT5 /
CURSOR19 /
Exact active-state SHA256 /
Exact packed-manifest SHA256 /
Exact weight SHA256 /
Exact Adam-M SHA256 /
Exact Adam-V SHA256 /
```

The packed-state manifest is physically rehashed from the selected slot instead of trusting only a receipt field.

The active state and weight/Adam payloads are also physically rehashed.

## Mutation / replay / rewrite closure

The promotion receipt must show zero for the relevant mutation and replay channels:

```text
promotionPayloadCopyCount = 0
promotionPayloadMutationCount = 0
receiptToStateSynthesisCount = 0
stateRewriteCount = 0
trainingReplayCount = 0
optimizerReplayCount = 0
previousParentMutation = 0
physicalN2SourceMutation = 0
```

No failure in a later N8 stage grants permission to repair the current parent by replaying, rematerializing, reordering, or rewriting it.

## RAM36 requirements

All are mandatory:

```text
Exact parent receipt path /
Exact parent receipt SHA256 /
Existing exact-inventory schema/pass validation /
Existing release-CF1 inventory evidence validation /
All owners classified /
All current-route owned payload exact /
No opaque nested allocator authority /
36 GiB exact process hard limit /
```

No independent RAM-limit override is introduced by this closure.

## Fail-closed cases

The runtime rejects at least the following:

```text
Physical promotion path drift /
Physical run path drift /
Generation drift /
Optimizer-step drift /
Cursor drift /
Active-state digest drift /
Packed-manifest digest drift /
Weight digest drift /
Adam-M digest drift /
Adam-V digest drift /
Physical parent mutation /
Physical parent replay /
Physical parent rewrite /
RAM36 parent path drift /
RAM36 receipt digest drift /
RAM36 hard-limit drift /
Direct-parent closure requested for legacy descendant /
Direct promoted N8 + RAM36 without this explicit authority /
```

There is no warning-only continuation and no automatic replacement receipt search.

## Preserved authority boundaries

```text
No N2 Mutation /
No N2 Replay Repair /
No N2 Reorder /
No N2 Rematerialization /
No RAM36 Parent Replacement /
No Numerically-Similar Inventory Substitution /
No RAM Inventory As Training-State Authority /
No Physical N2 As Runtime-Budget Authority /
No Failed-Run Parent Promotion /
No Partial Child Promotion /
```

## Cross-release relationship

A fresh `base_train` binary still requires a fresh Consumer Native CF1 and, when the physical N2 producer release differs from the consumer release, a fresh Cross-Release Physical N2 Compatibility Authority.

This does not require rebuilding the immutable Physical N2 or replacing the sealed RAM36 parent.

```text
Immutable N2 + RAM36 stay fixed
        |
        +-> fresh consumer binary
        +-> fresh Consumer CF1
        +-> fresh cross-release compatibility authority
        +-> exact N8 retry
```

## Non-claims

PASS does not mean:

```text
Training production success /
Activation authority /
Kernel-math parity /
Source-tree equality /
Durable Muon checkpoint success /
Resume authority promotion /
```

PASS means only that the exact current direct Physical N2 parent and exact RAM36 memory parent were both revalidated and admitted as the retry pair.

## Pass token

```text
PASS_ASH_BASETRAIN_IMMUTABLE_N2_RAM36_EXACT_RETRY_PARENT_AUTHORITY_CLOSURE_R1
```

## Next boundary

After this parent pair is closed, the current first failure remains owned by the next open runtime boundary unless new evidence directly demonstrates parent identity drift.

For the current handoff that next open boundary is:

```text
ASH-BP-DK-POST-CANDIDATE-TARGET-OPTIMIZER-GENERATION-BINDING-CLOSURE-R1
```
