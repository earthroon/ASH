# ASH-C08-ACTIVE-PHYSICAL-ADMISSION-CF1

## EVIDENCE-BACKED ACTIVE PHYSICAL ADMISSION BRIDGE

### Patch identity

- Patch ID: `ASH-C08-ACTIVE-PHYSICAL-ADMISSION-CF1`
- Physical receipt schema: `ASH_C08_ACTIVE_PHYSICAL_ADMISSION_CF1_V1`
- Physical receipt filename: `c08_active_physical_admission_cf1_receipt.json`
- PASS token: `PASS_ASH_C08_ACTIVE_PHYSICAL_ADMISSION_CF1`
- Parent authority: `ASH-WGPU-ASYNC-SUBMISSION-RETIREMENT-08` / `ASH_ASYNC_SUBMISSION_RETIREMENT_V1`

## 1. Problem

The existing C08 executable qualification is intentionally sealed with:

```rust
active_physical_admission: false,
```

while `ACTIVE_ASYNC` requires `active_physical_admission == true` before `assert_active_ready()` can pass. The runtime already contains `adopt_physical_qualification(...)`, but there was no production callsite that converted real executable WGPU evidence into a separately sealed physical-admission receipt and then adopted it.

CF1 closes only that missing authority edge. It does not change D09 promotion policy, R4D semantics, or the local C08 qualification contract.

## 2. Non-goals

CF1 SHALL NOT:

- replace the local `active_physical_admission: false` literal with `true`;
- derive ACTIVE authority from `AsyncRetirementRuntimeMode::ActiveAsync` alone;
- treat static contract presence as physical evidence;
- relax callback, map, retirement, parity, or upstream requirements;
- change D09 benchmark lane/promotion policy;
- change R4D-R0A/R0B/R1/R2/CF2/CF3/CLOSE semantics;
- remove the qualification-only exact wait parity fixture.

## 3. Authority split

The C08 authority chain is split into three distinct stages:

```text
LOCAL QUALIFICATION
AsyncCompletionQualificationReceipt
active_physical_admission=false

        +

PHYSICAL ADMISSION EVIDENCE
C08ActivePhysicalAdmissionReceiptCf1
physical_admission_pass=evidence-derived

        ↓ explicit adoption

ADOPTED C08 QUALIFICATION
AsyncCompletionQualificationReceipt
active_physical_admission=physical_admission_pass
receipt_hash=resealed
```

The local qualification remains non-authoritative for ACTIVE admission.

## 4. Physical receipt

`C08ActivePhysicalAdmissionReceiptCf1` binds at minimum:

- source local qualification receipt hash;
- B06 active state;
- C07 active state;
- segmented device successor state;
- aggregate active upstream admission;
- callback / parity / map submission device IDs;
- callback / parity / map queue IDs;
- submission ordinals;
- same-device and same-queue predicates;
- callback submission, arm, and observed completion deltas;
- map request, mapped-read, and unmap deltas;
- early reuse rejection delta;
- deferred retirement result and final queue length;
- hot-path exact-wait observation window count;
- measured hot-path exact-wait count;
- qualification-only exact-wait count;
- derived witness predicates;
- final `physical_admission_pass`;
- PASS token and receipt hash.

The receipt is hash-sealed and validates its own physical predicates.

## 5. Same device / queue authority

The callback-only, exact-wait parity, and map/deferred-retirement submissions SHALL share the same physical device and queue authority identities.

```text
callback.device_id == parity.device_id == map.device_id
callback.queue_id  == parity.queue_id  == map.queue_id
```

Any drift fails closed with dedicated CF1 failure attribution.

## 6. Callback completion witness

The callback-only fixture SHALL be physically observed using `submission_lease_telemetry_snapshot()` before and after the candidate-like callback path.

Required deltas:

```text
tracked_submission_count > 0
async_completion_callback_armed_count > 0
async_completion_callback_observed_count > 0
```

The tracked submission must also report completed nonblocking.

## 7. Map completion witness

The map path SHALL physically observe:

```text
map_requested_count > 0
mapped_read_count > 0
unmap_count > 0
map ticket final state == Unmapped
```

A static boolean is insufficient.

## 8. Deferred retirement witness

The physical receipt SHALL require:

```text
early_reclaim_rejected == true
early_reuse_reject_count_delta > 0
deferred_retirement_passed == true
deferred_retired_count > 0
deferred_retirement_final_len == 0
```

The early reclaim rejection and final retirement must come from the same fixture lineage.

## 9. Zero hot-path exact-wait witness

A literal zero is not physical evidence.

CF1 separates three telemetry windows:

```text
A. callback-only candidate-like path
B. qualification-only exact-wait parity path
C. map + deferred-retirement candidate-like path
```

The candidate-like exact-wait count is:

```text
callback_window.exact_wait_delta
+
map_window.exact_wait_delta
```

and SHALL equal zero with at least two measured candidate-like observation windows.

The qualification-only parity window SHALL independently observe one or more exact waits and retain exact-wait parity.

Therefore CF1 proves both:

```text
candidate-like async path exact waits == observed zero
qualification parity exact wait == physically exercised
```

## 10. Physical admission predicate

`physical_admission_pass` SHALL be a conjunction of:

```text
local qualification valid
local active_physical_admission == false
active upstream admitted
same device
same queue
callback completion witnessed
map completion witnessed
deferred retirement witnessed
hot-path exact-wait observation present
hot-path exact-wait count == 0
qualification-only exact wait observed
exact-wait parity passed
```

It SHALL NOT be assigned from runtime mode, capability presence, or a literal `true`.

## 11. Adoption bridge

`adopt_physical_qualification(...)` is the sole promotion edge.

Adoption SHALL:

1. validate the physical receipt;
2. require `ACTIVE_ASYNC` mode;
3. verify active upstream component parity;
4. require a current local qualification receipt;
5. validate the local receipt;
6. require local `active_physical_admission == false`;
7. bind `physical.source_qualification_receipt_hash == local.receipt_hash`;
8. require measured hot-path exact waits == 0;
9. set promoted `hot_path_wait_count` from the physical measurement;
10. set promoted `active_physical_admission` from `physical.physical_admission_pass`;
11. clear and recompute the local qualification receipt hash;
12. validate the promoted receipt;
13. retain the physical receipt in runtime state.

No literal `active_physical_admission: true` promotion is permitted.

## 12. Production callsite ordering

The base-train callsite SHALL execute:

```text
qualify_if_enabled()
→ Option<C08ActivePhysicalAdmissionReceiptCf1>
→ adopt_physical_qualification(receipt)
→ assert_active_ready()
```

For a runtime already carrying an adopted active qualification, requalification is skipped and `assert_active_ready()` may be repeated.

For ACTIVE mode, a missing physical receipt before first adoption fails closed with `FAIL_C08_CF1_ACTIVE_PHYSICAL_RECEIPT_MISSING`.

## 13. Receipt publication

On first successful ACTIVE physical qualification, the scheduler SHALL publish:

```text
c08_active_physical_admission_cf1_receipt.json
```

under the run output root and emit a compact success line containing the PASS token, receipt hash, source local qualification hash, identity predicates, measured telemetry deltas, exact-wait counts, and physical-admission result.

The JSON is an audit artifact. In-memory validated receipt authority remains the runtime admission source.

## 14. Preservation contracts

CF1 SHALL preserve:

- local C08 qualification default false;
- C08 OFF and MIRROR mode behavior;
- qualification-only exact-wait parity fixture;
- D09 semantic policy and lane selection;
- B06/C07 upstream policy;
- R4D semantic source files;
- Cargo dependency graph;
- WGSL tree.

## 15. Required failure attribution

At minimum:

```text
FAIL_C08_CF1_LOCAL_QUALIFICATION_MISSING
FAIL_C08_CF1_LOCAL_QUALIFICATION_ALREADY_ACTIVE
FAIL_C08_CF1_SOURCE_QUALIFICATION_HASH_MISMATCH
FAIL_C08_CF1_ACTIVE_UPSTREAM_ADMISSION_MISSING
FAIL_C08_CF1_DEVICE_IDENTITY_DRIFT
FAIL_C08_CF1_QUEUE_IDENTITY_DRIFT
FAIL_C08_CF1_CALLBACK_COMPLETION_UNOBSERVED
FAIL_C08_CF1_MAP_COMPLETION_UNOBSERVED
FAIL_C08_CF1_DEFERRED_RETIREMENT_UNOBSERVED
FAIL_C08_CF1_HOT_PATH_EXACT_WAIT_UNOBSERVED
FAIL_C08_CF1_HOT_PATH_EXACT_WAIT_NONZERO
FAIL_C08_CF1_QUALIFICATION_EXACT_WAIT_PARITY_MISSING
FAIL_C08_CF1_PHYSICAL_ADMISSION_INCOMPLETE
FAIL_C08_CF1_RECEIPT_HASH_MISMATCH
FAIL_C08_CF1_ACTIVE_PHYSICAL_RECEIPT_MISSING
```

## 16. Static gates

`tools/validate_ash_c08_active_physical_admission_cf1_static.py` SHALL verify:

- local `active_physical_admission: false` remains present;
- literal `active_physical_admission: true` promotion is absent;
- physical receipt schema and source receipt hash binding exist;
- device/queue identity predicates exist;
- callback/map/deferred-retirement telemetry witnesses exist;
- candidate-like exact-wait measurement and parity exact-wait separation exist;
- adoption callsite exists before `assert_active_ready()`;
- scheduler publishes the physical receipt;
- D09 remains byte-identical to the parent;
- R4D semantic source files remain byte-identical to the parent;
- Cargo manifests and WGSL tree remain unchanged.

## 17. Closure condition

CF1 closes only when a real ACTIVE run can produce a physical receipt satisfying all witnesses, the receipt is adopted into the local qualification with a resealed hash, and `assert_active_ready()` passes after adoption.

Source/static validation alone does not claim runtime or GPU physical PASS.

## Final invariant

```text
LOCAL QUALIFICATION != ACTIVE AUTHORITY

PHYSICAL EVIDENCE
+ EXPLICIT ADOPTION
= ACTIVE AUTHORITY
```

C08 ACTIVE_ASYNC may be admitted only after real queue submission, completion callback, map completion, deferred retirement, same device/queue identity, observed-zero candidate-path exact waits, and active upstream authority are all observed, hash-bound, and explicitly adopted.
