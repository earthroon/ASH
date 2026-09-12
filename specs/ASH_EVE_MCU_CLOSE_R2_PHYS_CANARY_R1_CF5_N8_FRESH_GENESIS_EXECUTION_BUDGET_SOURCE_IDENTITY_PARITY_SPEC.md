# ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF5

## N8 FRESH-GENESIS EXECUTION-BUDGET / SOURCE-IDENTITY PARITY

### Revision

```text
Patch ID:
ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF5

Class:
CANARY EXECUTION-HORIZON CONTRACT FIX
N8 FRESH-GENESIS SOURCE-IDENTITY DECONFOUNDING
NO OPTIMIZER-STATE SEMANTIC CHANGE
```

Direct execution lineage:

```text
ASH-EVE-MCU-CLOSE-R2-PHYS-R1B-CF1-R1K
ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1
ASH-EVE-MCU-CLOSE-R2-PHYS-R1B-CF1-R1K-CF1..CF4 compile closures
```

Current physical first failure before CF5:

```text
EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_FIRST_FAILURE:
RamResidentAdamMvN8FreshGenesisSourceIdentity
```

## 1. Confirmed parent state

Before the N8 failure, physical execution already demonstrated:

```text
R1K preflight:
r3b_admitted=true
r3a_admitted=true
hybrid_mode=ActiveVerified
parity_admitted=true

native WGPU bootstrap reached successfully
```

The previous CF4 parent also compiled successfully in the user's environment.

CF5 itself is not compiled in the bake environment.

## 2. Root cause

The RAM-resident Adam N8 admission combined two independent authorities in one expression:

```text
FreshGenesisR1A source identity
AND
historical full-R1B execution budget == 8
```

Previous source:

```text
FreshGenesisR1A:
    budget == 8
    source generation == 0
    source optimizer step == 0
    source cursor next batch == 0

failure:
RamResidentAdamMvN8FreshGenesisSourceIdentity
```

CANARY-R1 intentionally selects:

```text
production_loop_optimizer_steps = 2
```

Therefore a canonical fresh 0:0:0 source was rejected only because its future execution horizon was two steps rather than eight.

## 3. CF5 authority law

Fresh source identity and execution horizon are independent.

FreshGenesisR1A source identity remains exactly:

```text
source.generation = 0
source.optimizer_step = 0
source.cursor.next_batch_ordinal = 0
```

Execution budget becomes mode-dependent:

```text
CANARY-R1=true  -> expected budget = 2
CANARY-R1=false -> expected budget = 8
```

No other budget is admitted by CF5 for this fresh source seam.

## 4. Implementation

Changed file only:

```text
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
```

Changed block:

```text
N8SourceRole::FreshGenesisR1A
```

The implementation now performs, in order:

```text
1. canonical source 0:0:0 validation
2. explicit CANARY/full execution-mode budget selection
3. budget parity validation
4. existing RAM Adam hydration
```

The source-identity error retains one meaning:

```text
RamResidentAdamMvN8FreshGenesisSourceIdentity
```

Budget errors are now separate:

```text
RamResidentAdamMvCanaryBudgetMustBeTwo
RamResidentAdamMvN8BudgetMustBeEight
```

## 5. Explicit match authority

CF5 uses the existing execution-mode authority:

```text
cfg.training.admit_eve_mcu_close_r2_phys_canary_r1
```

and explicit match dispatch:

```text
true  -> expected_budget = 2
false -> expected_budget = 8
```

The code does not infer CANARY from `budget == 2`.

No integer cast or budget rewrite is introduced.

## 6. Physical witness

CF5 materializes one compact admission witness:

```text
[ASH-EVE-MCU-CANARY-CF5][n8-fresh-admission]
```

Fields:

```text
source_role
source_generation
source_optimizer_step
source_cursor
canary_mode
requested_budget
expected_budget
source_identity_admitted
budget_admitted
```

Expected CANARY witness:

```text
source_role=FreshGenesisR1A
source_generation=0
source_optimizer_step=0
source_cursor=0
canary_mode=true
requested_budget=2
expected_budget=2
source_identity_admitted=true
budget_admitted=true
```

## 7. Full R1B preservation

Full R1B fresh-genesis execution preserves:

```text
canary_mode=false
requested_budget=8
expected_budget=8
```

CF5 does not change:

```text
A leg = 8 optimizer steps
B leg = 8 optimizer steps
C leg = 8 optimizer steps
```

No A/B/C promotion semantics are changed.

## 8. Other N8 role preservation

These branches are unchanged:

```text
N8SourceRole::PromotedParent
N8SourceRole::LegacyMigrationDescendant
resume-cut role admission
```

Their existing budget/source contracts remain authoritative.

CF5 does not create a `CanaryFreshGenesis` source role.

## 9. Adam hydration preservation

CF5 does not modify:

```text
RamResidentAdamMv::hydrate
RamResidentAdamMv::hydrate_inventory_probe
Adam M/V allocation
Adam M/V bytes
transactional A/B enablement
RAM36 reservations
Adam arithmetic
```

The change occurs before hydration and changes admission only.

## 10. Parent closure preservation

The following latest-parent files are byte-preserved by CF5:

```text
R1K + Atlas preflight campaign:
crates/base_train/src/eve_mcu_close_r2_physical_campaign_r1b.rs
SHA-256:
e3274a7829c7edb5ed099ce822dfa1757affe5cbe5d8b850a09d56534c02d4a4

CANARY module after CF3:
crates/base_train/src/eve_mcu_close_r2_physical_canary_r1.rs
SHA-256:
fb340867dde08756484a6fe0603e0fba9b2f1f51eadb29496ee87079da86d544

Pipeline config literal after CF4:
crates/base_train/src/pipeline.rs
SHA-256:
fce437f129a2ca1fd4d2e899076eda81f3e1c78bc19808a66bfe861e19b11455
```

Scheduler parent SHA-256:

```text
47d009aea934f024f3629c46fdbe4c1afe7224c02a4d2e8ec5f2caeb74dda008
```

CF5 scheduler SHA-256:

```text
63006113b4316b491089be90b1e303d1f33e77f3cedbe8b90f0ff66e22fe4cd3
```

Source-delta digest:

```text
18eacf6985c7dc839c7982e991110974d1a88facab63c5b65ee47c4ff5194ac0
```

## 11. Baked source locations

```text
FreshGenesis branch              line 9149
source identity check            lines 9150-9155
mode-specific budget selection   lines 9157-9163
CF5 witness                      lines 9165-9175
CANARY budget guard              lines 9176-9180
full R1B budget guard            lines 9181-9184
```

## 12. Actual source delta

Relative to the latest R1K + CF1..CF4 parent:

```text
ADD 0
MOD 1
DEL 0
```

Only:

```text
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
```

is modified.

## 13. Code-only archive seal

Full code-only archive:

```text
ASH_PASS3_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF5_N8_FRESH_GENESIS_EXECUTION_BUDGET_SOURCE_IDENTITY_PARITY_CODE_ONLY.zip
SHA-256:
5ad51020fd7af1ce1179ca86a7da99b57818ca1e874e9372172d15788906ae2d
Files: 8424
CRC: PASS
```

Overlay:

```text
ASH_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF5_N8_FRESH_GENESIS_EXECUTION_BUDGET_SOURCE_IDENTITY_PARITY_OVERLAY_CODE_ONLY.zip
SHA-256:
2ad08e1c99b4dea6e4437c993933fb262cabb254290f87e9943c8e973a71ffa4
Files: 1
CRC: PASS
```

Neither archive contains:

```text
specs/
artifacts/
generated runtime manifests
generated receipts
this specification
```

## 14. Static acceptance

Confirmed in bake source:

```text
FreshGenesis source identity separated from budget
CANARY=true  -> expected budget 2
CANARY=false -> expected budget 8
source generation 0 preserved
source optimizer step 0 preserved
source cursor 0 preserved
CANARY budget has dedicated error
full-R1B budget has dedicated error
no numeric cast introduced
no source role added
other N8 source-role branch unchanged
RAM Adam hydration implementation unchanged
```

## 15. Evidence boundary

```text
SOURCE       CONFIRMED
STATIC       CONFIRMED
ARCHIVE      CONFIRMED
PARENT COMPILE  CONFIRMED BY USER
CF5 COMPILE     NOT VERIFIED IN BAKE ENVIRONMENT
RUNTIME      NOT VERIFIED
PHYSICAL     NOT VERIFIED
PERFORMANCE  NOT MEASURED
```

No CF5 compile or physical PASS is claimed by this specification.

## 16. Re-materialization

```text
dataset regeneration      NOT REQUIRED
R1A regeneration          NOT REQUIRED
R1A cursor regeneration   NOT REQUIRED
base_train rebuild         REQUIRED
Native CF1 reseal          REQUIRED
fresh CANARY output root   REQUIRED
full A/B/C                 NOT REQUIRED FOR CF5 ATTRIBUTION
```

## 17. Physical acceptance

CF5 crosses its target boundary when CANARY reports:

```text
[ASH-EVE-MCU-CANARY-CF5][n8-fresh-admission]
...
canary_mode=true
requested_budget=2
expected_budget=2
source_identity_admitted=true
budget_admitted=true
```

and the previous:

```text
RamResidentAdamMvN8FreshGenesisSourceIdentity
```

no longer terminates a canonical fresh canary run.

Any later error becomes a new attribution boundary.

## 18. Completion law

CF5 may be locally considered physically crossed only when the actual CANARY source demonstrates:

```text
FreshGenesisR1A identity = exact 0:0:0
requested budget = 2
expected budget = 2
RAM Adam hydration proceeds beyond admission
```

Full R1B must continue to require budget 8.

## Final law

> Fresh genesis describes source identity, not future execution length.

> CANARY-R1 and full R1B use the same FreshGenesisR1A source authority while requesting different horizons.

> CF5 preserves exact 0:0:0 genesis identity, admits two steps only under explicit CANARY mode, and preserves eight steps for full R1B.

> No new source role, no fake eight-step budget, no Adam hydration rewrite, no A/B/C promotion change.
