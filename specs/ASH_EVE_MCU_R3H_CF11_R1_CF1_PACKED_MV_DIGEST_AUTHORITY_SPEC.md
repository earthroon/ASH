# EVE-MCU-R3H-CF11-R1-CF1

## R3B DIRECT CF3A
## PACKED-ORDER CANDIDATE M/V DIGEST AUTHORITY CLOSURE

```text
+ PACKED PHYSICAL ORDER HASH AUTHORITY
+ CANONICAL PARAMETER IDENTITY LOOKUP PRESERVATION
+ PACKED-CANONICAL BRIDGE REUSE
+ OUTER PACK DIGEST EXACT PARITY
+ NO CANDIDATE VALUE CHANGE
+ NO OPTIMIZER NUMERICAL CHANGE
+ NO R3C ATOMIC PROMOTION CHANGE
+ CF11-R1 WORKSPACE CLOSURE PRESERVATION
```

---

## 0. Revision

```text
Patch ID:
EVE-MCU-R3H-CF11-R1-CF1

Class:
DIGEST AUTHORITY ORDERING CLOSURE
R3B DIRECT-CF3A IDENTITY RECONCILIATION
PACKED / CANONICAL ORDER SEPARATION
```

Direct parent:

```text
EVE-MCU-R3H-CF11-R1
+ successor-builder closure reborrow Compilefix-1
```

Parent full code-only SHA-256:

```text
85d09432d065e49af5ef998748c9b41cda386ce13d95251caad366c08809e1ff
```

---

## 1. Physical Parent Evidence

The first CF11-R1 canary reached the paged candidate terminal and proved:

```text
workspace_bound_bytes=285212672
workspace admitted=true
peak_dirty_ram_pages=4
peak_dirty_ram_bytes=268435456
verify_scratch_peak_bytes=16777216
full_candidate_heap_allocation_count=0
workspace_released=true
```

Parent CF11 candidate seal additionally reported:

```text
logical_weight_bytes=4666580992
page_count=70
dirty_page_count=70
inherited_page_count=0
spool_payload_bytes=4666580992
spool_write_bytes=4666580992
page_reload_count=0
dirty_page_reopen_count=0
dirty_page_rewrite_count=0
admitted=true
```

The run then failed at:

```text
E_MCU_EVE_R3B_OUTER_M_DIGEST_DRIFT
```

before source-retirement closure and successor full ResidentWeightPack promotion.

Evidence boundary:

```text
CF11-R1 workspace path       PHYSICAL-PARTIAL PASS
R3B packed M/V digest order  BLOCKER
CF11-R1 full physical        NOT YET PROMOTED
```

---

## 2. Root Cause

The candidate manifest M/V pack digests represent the physical packed byte stream emitted in source-record order.

The parent direct-CF3A seal instead traversed:

```text
for entry in &plan.entries
```

which is canonical parameter order.

The existing packed-canonical bridge explicitly preserves physical source order while mapping each source record to canonical parameter identity.

Therefore a legal non-identity mapping such as:

```text
packed/source order:  A C B D
canonical order:      A B C D
mapping:              [0, 2, 1, 3]
```

produces different streaming SHA-256 byte order despite identical candidate values.

Classification:

```text
R3B_DIRECT_CF3A_PACKED_CANONICAL_DIGEST_ORDER_MISMATCH
```

No evidence establishes candidate M/V numerical corruption.

---

## 3. Authority Separation

CF1 freezes two independent authorities:

```text
VALUE LOOKUP AUTHORITY
    canonical parameter identity

DIGEST TRAVERSAL AUTHORITY
    packed physical source-record order
```

The existing:

```text
RamAdamPackedCanonicalParameterBridgeR1A
```

is the single mapping authority between them.

No second mapping table is introduced.

---

## 4. Implementation

Primary code delta:

```text
MOD crates/base_train/src/ram_resident_adam_mv.rs
```

New private digest helper:

```text
hash_candidate_direct_cf3a_packed_order_cf11_r1_cf1(...)
```

The helper:

1. validates the route-sparse plan;
2. validates the packed-canonical bridge;
3. requires exact route-plan digest identity;
4. traverses `bridge.entries()` in packed physical order;
5. resolves the canonical plan entry through `canonical_parameter_index`;
6. checks parameter ID and element cardinality;
7. hashes Muon-inherited values from committed canonical M/V;
8. hashes ExplicitAdamW values from the sparse candidate overlay;
9. rejects packed gaps, overlaps, route drift and overlay-coordinate drift;
10. allocates no generation-sized M/V temporary.

The direct seal no longer uses canonical `plan.entries` as its primary hash traversal order.

---

## 5. Route-Specific Value Preservation

### MuonInherited

```text
hash order:
    packed bridge position

value source:
    self.m / self.v canonical committed ranges
```

### ExplicitAdamw

```text
hash order:
    packed bridge position

value source:
    candidate_m / candidate_v sparse overlay
```

Candidate values are not rewritten for digest parity.

---

## 6. Fail-Closed Geometry

New internal errors include:

```text
E_CF11_R1_CF1_PACKED_BRIDGE_MISSING
E_CF11_R1_CF1_PACKED_BRIDGE_ROUTE_PLAN_DIGEST_DRIFT
E_CF11_R1_CF1_PACKED_COVERAGE_GAP
E_CF11_R1_CF1_PACKED_COVERAGE_OVERLAP
E_CF11_R1_CF1_PACKED_CANONICAL_INDEX_INVALID
E_CF11_R1_CF1_PACKED_CANONICAL_INDEX_DRIFT
E_CF11_R1_CF1_PACKED_CANONICAL_PARAMETER_ID_DRIFT
E_CF11_R1_CF1_PACKED_ELEMENT_GEOMETRY_DRIFT
E_CF11_R1_CF1_PACKED_OVERLAY_START_MISSING
E_CF11_R1_CF1_PACKED_OVERLAY_COORDINATE_DRIFT
E_CF11_R1_CF1_PACKED_OVERLAY_RANGE_OOB
E_CF11_R1_CF1_PACKED_ROUTE_KIND_DRIFT
```

No fallback to canonical traversal is permitted.

---

## 7. Outer Exact-Parity Gate Preservation

The existing final gates remain unchanged:

```text
seal.candidate_m_sha256 == candidate.manifest.adam_m_pack_sha256
seal.candidate_v_sha256 == candidate.manifest.adam_v_pack_sha256
```

with the existing outer errors:

```text
E_MCU_EVE_R3B_OUTER_M_DIGEST_DRIFT
E_MCU_EVE_R3B_OUTER_V_DIGEST_DRIFT
```

CF1 does not copy expected manifest digests into the observed R3B seal.

R3B independently derives its M/V digest from candidate state.

---

## 8. Physical Diagnostic

New terminal line:

```text
[ASH-MCU-EVE-R3B-CF11-R1-CF1][packed-mv-digest]
```

Fields include:

```text
source_generation
target_generation
digest_order=PACKED_PHYSICAL
packed_entry_count
packed_element_count
candidate_m_sha256
candidate_v_sha256
admitted=true
```

The outer manifest parity check remains the authoritative exact-match gate.

---

## 9. Memory / Numerical Preservation

CF1 introduces no:

```text
full M generation temporary
full V generation temporary
full M/V packed reconstruction Vec
new RAM36 generation-sized reservation
candidate state rewrite
optimizer arithmetic change
```

Preserved CF11-R1 geometry:

```text
CF11 page bytes             = 64 MiB
CF11 max dirty RAM pages    = 4
CF11 max dirty RAM bytes    = 256 MiB
CF11-R1 verify scratch      = 16 MiB
CF11-R1 workspace admission = 272 MiB
full candidate W heap count = 0
```

No R3C atomic promotion source is modified.

---

## 10. Rust Tests Added

Test prefix:

```text
r3b_cf11_r1_cf1_
```

Added:

```text
r3b_cf11_r1_cf1_non_identity_mapping_hashes_packed_order
r3b_cf11_r1_cf1_candidate_values_unchanged_by_digest_seal
r3b_cf11_r1_cf1_identity_mapping_matches_parent_order
r3b_cf11_r1_cf1_m_digest_matches_manifest_packed_digest
r3b_cf11_r1_cf1_v_digest_matches_manifest_packed_digest
r3b_cf11_r1_cf1_packed_gap_rejected
r3b_cf11_r1_cf1_packed_overlap_rejected
```

The non-identity fixture freezes:

```text
packed:    A C B D
canonical: A B C D
mapping:   [0, 2, 1, 3]
```

and proves the new seal hashes packed order rather than canonical order.

---

## 11. Static Validator

Added:

```text
tools/validate_ash_eve_mcu_r3h_cf11_r1_cf1_packed_mv_digest_static.py
```

Bake result:

```text
PASS_EVE_MCU_R3H_CF11_R1_CF1_PACKED_MV_DIGEST_STATIC checks=27
```

Preserved validators:

```text
PASS_EVE_MCU_R3H_CF11_R1_BOUNDED_COW_WORKSPACE_STATIC checks=22
PASS_EVE_MCU_R3H_CF11_PAGED_COW_CANDIDATE_WEIGHT_SUCCESSOR_STATIC checks=64
PASS_EVE_MCU_R7A_CF9_CF3A_DIRECT_HOST_DEMOTION_STATIC
PASS_ASH_BASETRAIN_RAM36_HIMUON_ROUTE_SPARSE_TRANSACTIONAL_ADAM_AB_PACKED_OFFSET_TO_CANONICAL_PARAMETER_BRIDGE_AND_BIT_EXACT_INHERITANCE_CLOSURE_R1A_STATIC
PASS_ASH_MCU_EVE_ADAMW_ACTIVEDEVICE_TARGET_TO_BOUNDED_RAM_WRITEBACK_CIRCULATION_AND_EVE_CANDIDATE_COMPLETE_CLOSURE_R3B_STATIC
```

Python validator compilation and modified Rust delimiter scan also pass.

---

## 12. Source Delta

```text
MOD 1
ADD 1
DEL 0
```

Modified:

```text
crates/base_train/src/ram_resident_adam_mv.rs
SHA-256 d72380066e20cdb6dc860243fa68a2895a30f5ac785c3a1b0623f24a55314f7d
```

Added:

```text
tools/validate_ash_eve_mcu_r3h_cf11_r1_cf1_packed_mv_digest_static.py
SHA-256 a8aae2e18b5ebce5eba4b133b2d96b5bf347df4b561d28597346d98c4fa27da9
```

---

## 13. Code-Only Artifacts

Overlay:

```text
ASH_EVE_MCU_R3H_CF11_R1_CF1_PACKED_MV_DIGEST_AUTHORITY_OVERLAY_CODE_ONLY.zip
SHA-256 c4ed227174865fd470112e3db5c78c78206943e689fa32c1abefe01d6f912400
FILES 2
CRC PASS
```

Full:

```text
ASH_PASS3_EVE_MCU_R3H_CF11_R1_CF1_PACKED_MV_DIGEST_AUTHORITY_CODE_ONLY.zip
SHA-256 d9342a13bacf8a39c1170be54e15b74c8ca7c5bcd2d1f8ddcbe3affe5275b78a
FILES 8435
CRC PASS
```

Both archives exclude:

```text
specs/      0
artifacts/  0
manifests/  0
Markdown    0
__pycache__ 0
*.pyc       0
```

Normal build inputs such as `Cargo.toml` and `Cargo.lock` remain in the Full archive.

---

## 14. Evidence Status at Bake

```text
SOURCE        APPLIED
STATIC        PASS
ARCHIVE CRC   PASS
RUST COMPILE  NOT RUN - Rust toolchain unavailable in bake environment
RUST TEST     NOT RUN
RUNTIME       NOT RUN
PHYSICAL      NOT RUN
PERFORMANCE   UNMEASURED
```

No compile/runtime/physical promotion is claimed by this bake.

---

## 15. Compile Acceptance

Required:

```powershell
cargo check `
  -p base_train `
  --lib `
  --release `
  --locked `
  -j 1
```

Then:

```powershell
cargo test `
  -p base_train `
  --lib `
  --release `
  --locked `
  -j 1 `
  r3b_cf11_r1_cf1_ `
  -- `
  --nocapture
```

Zero discovered tests is not PASS.

Parent regression tests remain required:

```text
r3h_cf11_r1_
r3h_cf11_
```

---

## 16. Physical Acceptance

Re-enter the exact same canary fixture that produced:

```text
E_MCU_EVE_R3B_OUTER_M_DIGEST_DRIFT
```

First target:

```text
[ASH-MCU-EVE-R3B-CF11-R1-CF1][packed-mv-digest]
    digest_order=PACKED_PHYSICAL

E_MCU_EVE_R3B_OUTER_M_DIGEST_DRIFT
    ABSENT

E_MCU_EVE_R3B_OUTER_V_DIGEST_DRIFT
    ABSENT
```

The same run must preserve:

```text
workspace_bound_bytes=285212672
peak_dirty_ram_pages<=4
peak_dirty_ram_bytes<=268435456
verify_scratch_peak_bytes<=16777216
full_candidate_heap_allocation_count=0
workspace_released=true
```

Only then may execution continue into the previously blocked CF11-R1 source-retirement closure.

---

## 17. Completion Law

CF11-R1-CF1 is complete only when:

1. R3B direct-CF3A M/V digest traversal follows packed physical order.
2. Candidate value lookup remains canonical-identity based.
3. The existing packed-canonical bridge is the only mapping authority.
4. No candidate M/V value is changed for digest parity.
5. No generation-sized M/V temporary is introduced.
6. M digest exactly matches manifest packed M digest.
7. V digest exactly matches manifest packed V digest.
8. Existing outer exact-parity gates remain active and pass.
9. The same physical canary no longer fails at `E_MCU_EVE_R3B_OUTER_M_DIGEST_DRIFT`.
10. CF11-R1 memory bounds remain intact.
11. Execution proceeds beyond the previous outer-seal blocker.

---

## 18. Final Law

> CF11-R1-CF1 changes digest traversal order, not candidate state.

> Packed M/V digest identity follows physical source-record order; candidate value lookup follows canonical parameter identity.

> `RamAdamPackedCanonicalParameterBridgeR1A` is reused as the sole mapping authority between those domains.

> The manifest digest is not rewritten, copied or weakened. The outer M/V exact-parity gates remain fail-closed.

> No optimizer numerical semantics, candidate values, R3C atomic promotion semantics, CF11 COW semantics, CF11-R1 workspace semantics or source-retirement policy change in this revision.
