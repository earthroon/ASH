# ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF6

## N8 FRESH-GENESIS SOURCE IDENTITY LIFETIME ATTRIBUTION

### Revision

```text
Patch ID:
ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF6

Class:
SOURCE-LIFETIME ATTRIBUTION
GENESIS / CACHE / PARENT-BINDING / ADAM-HYDRATION WITNESS
DIAGNOSTIC ONLY
NO SOURCE REWRITE
NO IDENTITY-GUARD RELAXATION
```

Direct parent:

```text
ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF5
```

Current physical first failure before CF6:

```text
EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_FIRST_FAILURE:
RamResidentAdamMvN8FreshGenesisSourceIdentity
```

## 1. Purpose

CF5 separated FreshGenesis source identity from the execution horizon:

```text
FreshGenesisR1A source identity:
    generation = 0
    optimizer_step = 0
    cursor.next_batch_ordinal = 0

execution budget:
    CANARY = 2
    Full R1B = 8
```

Physical execution nevertheless continued to report `RamResidentAdamMvN8FreshGenesisSourceIdentity`.

CF6 does not repair or rewrite the source. It observes the same FreshGenesis source at four lifecycle boundaries so the first identity divergence becomes physically attributable.

## 2. Attribution stages

CF6 adds exactly four lifecycle witnesses:

```text
stage 0 PRE-CACHE SOURCE
stage 1 POST-CACHE SOURCE
stage 2 PARENT-BINDING
stage 3 PRE-ADAM-HYDRATION
```

All are scoped to the N8 FreshGenesisR1A path.

## 3. Pre-cache source witness

Marker:

```text
[ASH-EVE-MCU-CANARY-CF6][pre-cache-source]
```

Baked line: `8535`.

It records before the scheduler-level `N8FreshGenesisR1ASourceIdentity` guard:

```text
source role
generation
optimizer step
cursor next batch ordinal
training-state schema
source lineage digest
parent training-state digest
canary mode
requested budget
expected budget
source identity exactness
```

The existing guard remains at line `8562`.

## 4. Post-cache source witness

Marker:

```text
[ASH-EVE-MCU-CANARY-CF6][post-cache-source]
```

Baked line: `8645`.

It records the source after packed-genesis adoption/cache resolution and before FreshGenesis parent binding:

```text
generation
optimizer step
cursor
packed source kind
packed slot
genesis cache key
source lineage digest
source identity exactness
```

CF6 does not bypass cache construction.

## 5. Parent-binding witness

Marker:

```text
[ASH-EVE-MCU-CANARY-CF6][parent-binding]
```

Baked line: `8734`.

It binds the post-cache source to the newly materialized `N8ParentBinding` and records:

```text
source / parent generation
source / parent optimizer step
source / parent cursor
source lineage digest
parent lineage digest
source / parent active-state digest
same generation
same optimizer step
same cursor
same active-state digest
```

No parent identity is rewritten on mismatch.

## 6. Pre-Adam-hydration witness

Marker:

```text
[ASH-EVE-MCU-CANARY-CF6][pre-adam-hydration]
```

Baked line: `9286`.

This witness is emitted before the existing RAM Adam FreshGenesis identity guard and records:

```text
source generation / optimizer step / cursor
parent generation / optimizer step / cursor
canary mode
requested budget
expected budget
per-axis exactness
overall source identity exactness
budget exactness
parent parity
active-state digest parity
source lineage digest
parent lineage digest
```

Only after the witness does the existing guard execute:

```text
RamResidentAdamMvN8FreshGenesisSourceIdentity
```

Baked line: `9324`.

CF5 budget-specific guards remain:

```text
RamResidentAdamMvCanaryBudgetMustBeTwo   line 9329
RamResidentAdamMvN8BudgetMustBeEight     line 9333
```

## 7. Witness-before-ensure law

For the CF6-covered scheduler boundaries:

```text
OBSERVE
→ CLASSIFY
→ ENSURE
```

The previous guard is not removed. It is moved only at the pre-Adam seam so the CF6/CF5 witnesses are guaranteed to be emitted first.

## 8. Source lineage digest

CF6 adds a stable source-lineage digest domain:

```text
ash.eve.mcu.canary.cf6.n8.source.lineage
```

Inputs:

```text
source role
training-state schema
generation
optimizer step
cursor next batch ordinal
dataset manifest identity
dataset manifest physical digest
tokenizer lineage identity
parent training-state digest
```

No pointer address, timestamp, or mutable process-local identity is included.

## 9. Parent-binding lineage digest

CF6 adds:

```text
ash.eve.mcu.canary.cf6.n8.parent_binding.lineage
```

Inputs:

```text
source role
source generation
source optimizer step
source cursor
active-state SHA-256
weight pack SHA-256
Adam M pack SHA-256
Adam V pack SHA-256
producer Native CF1 authority receipt hash
```

This is diagnostic evidence only. It does not replace the existing N8 parent binding authority.

## 10. No source mutation

CF6 does not assign or rewrite:

```text
source.generation
source.optimizer_step
source.cursor.next_batch_ordinal
parent source identity
N8 source role
Adam state
```

No zeroing, rebinding, cache bypass, or direct Adam initialization fallback is introduced.

## 11. Existing guard preservation

Counts relative to CF5 parent:

```text
RamResidentAdamMvN8FreshGenesisSourceIdentity
    parent = 1
    CF6    = 1

RamResidentAdamMvCanaryBudgetMustBeTwo
    parent = 1
    CF6    = 1

RamResidentAdamMvN8BudgetMustBeEight
    parent = 1
    CF6    = 1
```

CF6 does not relax identity or budget admission.

## 12. Physical classification matrix

The next CANARY execution can now distinguish:

```text
PRE-CACHE invalid
    → source selection / R1A binding defect

PRE-CACHE exact, POST-CACHE drift
    → genesis-cache source identity drift

source exact, parent binding differs
    → parent-binding drift

pre-cache/post-cache/parent exact, pre-Adam differs
    → local pre-hydration identity drift

all source axes exact, budget not exact
    → CF5 budget drift

all witnesses exact and hydration continues
    → CF6 attribution boundary crossed

all witnesses exact but existing identity guard fails
    → STATIC / PHYSICAL CONFLICT preserved
```

No branch auto-repairs the observed mismatch.

## 13. Actual source delta

Relative to exact CF5 parent:

```text
ADD 0
MOD 1
DEL 0
```

Changed file:

```text
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
```

CF5 parent source SHA-256:

```text
63006113b4316b491089be90b1e303d1f33e77f3cedbe8b90f0ff66e22fe4cd3
```

CF6 source SHA-256:

```text
144106ebbfed0cab14ee2501afe15c72648e0b32c85ca604303911be97d90bfa
```

Source-delta digest:

```text
5c0b4cd65948264cf94ba9b2961f7c74f30b2b9b6b70d3ea5ef1483b45956266
```

## 14. Archive seal

Full code-only archive:

```text
ASH_PASS3_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF6_N8_FRESH_GENESIS_SOURCE_IDENTITY_LIFETIME_ATTRIBUTION_CODE_ONLY.zip
SHA-256:
47696ffc52c8f29997ad3eae429dbc6194b7937e7685839da0fe8101e16e87e7
Files: 8424
CRC: PASS
```

Overlay code-only archive:

```text
ASH_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF6_N8_FRESH_GENESIS_SOURCE_IDENTITY_LIFETIME_ATTRIBUTION_OVERLAY_CODE_ONLY.zip
SHA-256:
84691c343bfb98d1dd0a043a689d7b415bced48a9738e1dea454345fafa54ca1
Files: 1
CRC: PASS
```

Archive policy:

```text
specs/ tree     = 0
artifacts/ tree = 0
runtime generated receipts/manifests are not added
this specification is not inside either ZIP
```

## 15. Static acceptance

```text
PASS pre-cache witness present
PASS post-cache witness present
PASS parent-binding witness present
PASS pre-Adam-hydration witness present
PASS pre-cache witness precedes scheduler FreshGenesis guard
PASS pre-Adam witness precedes RAM Adam FreshGenesis guard
PASS generation / optimizer step / cursor witnesses present
PASS source lineage digest present
PASS parent lineage digest present
PASS active-state digest parity witness present
PASS CF5 budget split preserved
PASS existing FreshGenesis identity guard preserved
PASS source mutation absent from CF6 delta
PASS archive CRC
```

## 16. Evidence boundary

Bake environment does not contain `cargo`, `rustc`, or `rustfmt`.

Therefore:

```text
SOURCE      CONFIRMED
STATIC      CONFIRMED
ARCHIVE     CONFIRMED
COMPILE     NOT VERIFIED
RUNTIME     NOT VERIFIED
PHYSICAL    NOT VERIFIED
PERFORMANCE NOT MEASURED
```

No compile or physical PASS is claimed by this bake.

## 17. Re-materialization contract

```text
dataset regeneration      NOT REQUIRED
R1A regeneration          NOT REQUIRED
R1A cursor regeneration   NOT REQUIRED
base_train rebuild         REQUIRED
Native CF1 reseal          REQUIRED
fresh CANARY output root   REQUIRED
full A/B/C                 NOT REQUIRED for CF6 attribution
```

## 18. Completion law

CF6 has completed its diagnostic purpose when one actual two-step CANARY run either:

```text
1. identifies the first lifecycle stage where source identity diverges,

or

2. shows all four lifecycle witnesses exact and proceeds beyond
   RamResidentAdamMvN8FreshGenesisSourceIdentity,

or

3. shows all four witnesses exact while the same deep guard still fails,
   preserving a concrete physical contradiction for the next revision.
```

## Final law

> CF6 does not change the source. It watches the source.

> FreshGenesis identity is observed at pre-cache, post-cache, parent-binding, and pre-Adam-hydration boundaries before the covered fail-closed guard can hide the values that caused rejection.

> Generation, optimizer step, cursor, lineage digests, and execution budget remain separate evidence axes.

> No source rewrite. No fake genesis repair. No identity guard relaxation.
