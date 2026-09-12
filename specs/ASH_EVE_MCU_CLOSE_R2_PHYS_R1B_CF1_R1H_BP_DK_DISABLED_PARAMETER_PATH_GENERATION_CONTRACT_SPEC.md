# ASH-EVE-MCU-CLOSE-R2-PHYS-R1B-CF1-R1H

## BP-DK R2A DISABLED-MODE PARAMETER-PATH GENERATION CONTRACT

### Revision

```text
Patch ID:
ASH-EVE-MCU-CLOSE-R2-PHYS-R1B-CF1-R1H

Class:
PRODUCTION CALLSITE CONTROL-FLOW CLOSURE
DISABLED-MODE PHYSICAL BOOKKEEPING RETIREMENT
NO OPTIMIZER-MATH CHANGE
NO DK-POLICY CHANGE
```

Direct semantic parent:

```text
EVE-MCU-CLOSE-R2-PHYS-R1B-CF1-R1G
BP-DK R2A DISABLED-MODE COMMIT / ABORT FINALIZE NO-OP SYMMETRY CLOSURE
```

## 1. Parent source identity

The locally supplied code-only archive is R1F. R1G modified the same production callsite file only. R1G was re-materialized from R1F using the committed R1G finalize-symmetry delta and checked against the authoritative R1G changed-source SHA-256.

```text
R1G authoritative SHA-256:
1e7e2a08f48f9942ef76773d49db5e29a68fe78623c9a6bd3707c8ba772c835c

R1G re-materialized SHA-256:
1e7e2a08f48f9942ef76773d49db5e29a68fe78623c9a6bd3707c8ba772c835c
```

**CONFIRMED:** the R1H delta is based on the exact R1G bytes for:

```text
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
```

## 2. Physical blocker

Observed production failure:

```text
PHYS_R1_PRODUCTION_ERROR:
RamAdamTransactionalCandidateExecutionFailed:
E_DK_R2A_PHYS_GENERATION_DRIFT
```

Disabled already establishes:

```text
mode.observes() = false
generation open = 0
scheduler cutover = false
outer disabled bypass witness = true
```

The legacy candidate path nevertheless issued generation-bound R2A physical bookkeeping calls.

```text
Disabled
→ no begin_generation
→ legacy parameter path
→ generation-bound record call
→ require_generation
→ E_DK_R2A_PHYS_GENERATION_DRIFT
```

R1H fixes the caller. It does not weaken the low-level guard.

## 3. Authority law

For BP-DK `Disabled`:

```text
generation open               = 0
legacy local phys record      = 0
legacy bridge phys record     = 0
inline plan phys record       = 0
legacy post phys record       = 0
prepared-plan freeze          = 0
physical commit resolve       = 0
physical abort resolve        = 0
scheduler cutover             = false
outer disabled bypass witness = true
```

Combined lifecycle law:

```text
No Open
→ No Parameter Record
→ No Freeze
→ No Resolve
```

ObserveOnly / Active keep their existing generation lifecycle.

## 4. R1H implementation

Changed file:

```text
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
```

R1H adds `match self.bpdk.perf_r1_mode.observes()` admission around exactly four R2A generation-bound bookkeeping seams:

```text
LOCAL       record_legacy_local_parameter(...)
BRIDGE      record_legacy_bridge_parameter(...)
INLINE PLAN record_inline_parameter_plan(...)
POST        record_legacy_post_parameter(...)
```

Dispatch contract:

```text
match perf_r1_mode.observes()
    true  → execute the pre-existing R2A physical record
    false → issue no generation-bound R2A physical record
```

Disabled still executes the surrounding candidate path. R1H does not retire planner computation, bridge evidence, Muon calculation, AdamW calculation, candidate assembly or optimizer transaction flow.

R1H adds no new `if` branch. The existing R1G finalize gates are preserved from the exact R1G parent.

## 5. R1G preservation

R1G remains authoritative for finalize:

```text
commit, observes=true:
    prepared-plan freeze
    record_prepared_plan_frozen(...)
    resolve_generation(..., true)

commit, observes=false:
    no R2A physical finalize

abort, observes=true:
    resolve_generation(..., false)

abort, observes=false:
    no R2A physical abort resolve
```

R1H does not modify these R1G regions.

## 6. Low-level guard preservation

Unmodified file:

```text
crates/base_train/src/bp_delta_k_r2a_phys_runtime.rs
```

SHA-256:

```text
2b56af36c95a2654dc50d7eb4c0ade743bd78714f31d5946097d7f589e2d2c3a
```

Preserved guards:

```text
E_DK_R2A_PHYS_DISABLED_GENERATION_OPEN
E_DK_R2A_PHYS_GENERATION_DRIFT
```

R1H does not synthesize a Disabled generation, silently succeed without a generation, catch-and-ignore generation drift, or auto-promote Disabled to ObserveOnly/Active.

## 7. Optimizer and policy preservation

R1H changes no:

```text
Muon arithmetic
AdamW arithmetic
Adam M/V authority
HiMuon routing
route digest
canonical parameter ordering
successor weight reservation
RAM36 policy
checkpoint format
model geometry
micro-batch / accumulation geometry
DK thresholds / proposal policy
Device / Queue ownership
```

Existing route contract remains:

```text
Muon parameters  = 154
AdamW parameters = 47
Mixed parameters = 0
```

## 8. Exact source delta

Relative to exact R1G:

```text
ADD 0
MOD 1
DEL 0
```

```text
R1G source SHA-256:
1e7e2a08f48f9942ef76773d49db5e29a68fe78623c9a6bd3707c8ba772c835c

R1H source SHA-256:
aa794ac09a6a8043e1f3e98605e6bcbfd2d735e1ec9a75455daebaf162473c66

source-delta digest:
b5cafd8612faf62be489d8a59065b258404f7f91cbdfda9dc6d33a238f2a636f
```

Key baked lines:

```text
Disabled outer bypass          5255
R1H local observes gate        6908
R1H local physical record      6910
R1H bridge observes gate       7214
R1H bridge physical record     7216
R1H inline observes gate       7320
R1H inline physical record     7322
R1H post observes gate         9641
R1H post physical record       9643
R1G commit observes gate      13735
R1G commit physical resolve   13759
R1G abort observes gate       13905
R1G abort physical resolve    13906
```

## 9. Code-only archive seal

Full:

```text
ASH_PASS3_EVE_MCU_CLOSE_R2_PHYS_R1B_CF1_R1H_BP_DK_DISABLED_PARAMETER_PATH_GENERATION_CONTRACT_CODE_ONLY.zip
SHA-256:
a4bebb2ae2932b3428da28501d4a73031eb291b7131e6b20d2039816e581af59
Files: 8423
CRC: PASS
```

Overlay:

```text
ASH_EVE_MCU_CLOSE_R2_PHYS_R1B_CF1_R1H_BP_DK_DISABLED_PARAMETER_PATH_GENERATION_CONTRACT_OVERLAY_CODE_ONLY.zip
SHA-256:
1e42363c581e9cfb6315f9d3b3b977e2d452aea1f12f73718fa6c24abd6a499a
Files: 1
CRC: PASS
```

The full archive preserves the exact R1F archive inventory and changes only the single production source file. Generated manifests, generated artifacts, reports and this specification are not included in either ZIP. No top-level `artifacts/` or `specs/` tree is present.

## 10. Static acceptance

```text
R1G exact parent source identity              PASS
R1H changed file count relative R1G           1
local mode parity                             PASS_STATIC
bridge mode parity                            PASS_STATIC
inline-plan mode parity                       PASS_STATIC
post mode parity                              PASS_STATIC
R1G commit finalize preservation              PASS_STATIC
R1G abort finalize preservation               PASS_STATIC
low-level runtime preservation                PASS_STATIC
Disabled-open guard preservation              PASS_STATIC
Generation-drift guard preservation           PASS_STATIC
full ZIP CRC                                  PASS
overlay ZIP CRC                               PASS
```

## 11. Evidence boundary

This bake environment has no `cargo`, `rustc` or `rustfmt` executable.

```text
SOURCE      CONFIRMED
STATIC      CONFIRMED
ARCHIVE     CONFIRMED
COMPILE     NOT VERIFIED
RUNTIME     NOT VERIFIED
PHYSICAL    NOT VERIFIED
PERFORMANCE NOT MEASURED
```

No compile, Native CF1, A/B/C or performance PASS is claimed.

## 12. Re-materialization contract

```text
dataset regeneration       NOT REQUIRED
R1A regeneration           NOT REQUIRED
R1A cursor regeneration    NOT REQUIRED
base_train rebuild          REQUIRED
Native CF1 reseal           REQUIRED
fresh R1B campaign root     REQUIRED
A/B/C reentry               REQUIRED
```

## 13. Physical acceptance

R1H first crosses its blocker when Disabled candidate execution no longer terminates with:

```text
RamAdamTransactionalCandidateExecutionFailed:
E_DK_R2A_PHYS_GENERATION_DRIFT
```

Strong admission requires the same physical run to establish:

```text
mode                            = Disabled
observes                        = false
DK begin_generation attempts    = 0
legacy local phys records       = 0
legacy bridge phys records      = 0
inline plan phys records        = 0
legacy post phys records        = 0
prepared-plan freeze attempts   = 0
commit resolve attempts         = 0
abort resolve attempts          = 0
scheduler cutover               = false
outer disabled bypass witness   = true
```

A new first failure after that boundary is a new attribution boundary and is not automatically folded into R1H.

## 14. Completion law

R1H may issue:

```text
PASS_EVE_MCU_CLOSE_R2_PHYS_R1B_CF1_R1H
```

only when Disabled physical execution demonstrates:

```text
no R2A generation opened
no local / bridge / inline / post generation-bound R2A bookkeeping issued
candidate execution reached post and returned
R1G Disabled finalize remained no-op
optimizer transaction continued beyond the previous generation-drift boundary
```

Until physical execution proves that:

```text
HOLD_EVE_MCU_CLOSE_R2_PHYS_R1B_CF1_R1H_PHYSICAL_PENDING
```

## Final law

> Disabled BP-DK owns no R2A physical generation. A generation that does not exist cannot legally receive local, bridge, planner, post, commit or abort physical bookkeeping.

> R1H removes the four invalid parameter-path caller operations under Disabled. It does not weaken generation guards, alter optimizer arithmetic, or change DK policy.

> R1G closes Disabled finalize symmetry. R1H closes Disabled parameter-path symmetry. Together: **No Open → No Record → No Freeze → No Resolve.**
