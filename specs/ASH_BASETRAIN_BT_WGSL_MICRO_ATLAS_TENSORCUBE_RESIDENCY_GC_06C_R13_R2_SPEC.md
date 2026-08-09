# `BT-WGSL-MICRO-ATLAS-TENSORCUBE-RESIDENCY-GC-06C-R13-R2`

## Revision identity

```text
Patch ID:
ASH-BASETRAIN-BT-WGSL-MICRO-ATLAS-TENSORCUBE-RESIDENCY-GC-06C-R13-R2

Build revision:
bt-wgsl-micro-atlas-tensorcube-residency-gc-06c-r13-r2

Physical parent:
BT-STRUCTURAL-BRANCH-ATTENTION-BACKWARD-06C-R12

Corrected code parents:
BT-WGSL-OPROJ-FFN-BACKWARD-06C-R13
BT-WGSL-BACKPROP-FAIL-CLOSED-NUMERICS-06C-R13-R1

Proof ledger:
HOLD
```

## Scope seal

```text
R12 Physical Parent /
R13-R1 Fail-Closed Numerics Code Parent /
1D Logical Surface Authority /
Workgroup-Bounded Chunk Decomposition /
Micro Atlas Page Authority /
2D TensorCube Residency Map /
Zero-Copy Raw Buffer Views /
Zero Tensor Payload Replication /
Bounded Per-Page Dispatch /
HeadwiseOutputParity TensorCube Adoption /
Linear Backward TensorCube Adoption /
FFN Gradient Tile TensorCube Adoption /
Deterministic Page-Index Commit /
Compact Page Receipt Reduction /
Commit-Before-GC Discipline /
Consumed Page Lease Garbage Collection /
Completion-Fence-Bound Release /
Reference-Count-Bound Release /
Canonical Output Ownership Transfer /
No Premature Payload Free /
No Mega Comparison Buffer /
No Mega Gradient Staging Atlas /
Zero Host Shuttle /
Production Gradient Payload Readback Zero /
R13-R1 Fail-Closed Numerics Preservation /
Future G205D Gradient Atlas Compatible /
Proof Ledger HOLD Seal
```

## 1. Triggering physical failure

Observed physical failure:

```text
HeadwiseOutputParityPipeline::compare_exact

dispatch = [90112, 1, 1]
physical max_compute_workgroups_per_dimension = 65535
```

The failing surface contains 5,767,168 f32 elements:

```text
5,767,168 / 64 = 90,112 logical workgroups
```

R13-R2 retires whole-surface direct dispatch as the execution authority.

## 2. One-line SSOT

> A one-dimensional logical surface is split into workgroup-bounded Micro Atlas pages. TensorCube provides deterministic two-dimensional residency coordinates for those zero-copy page views. Each page dispatch writes directly into its canonical output range, and page-owned scheduling/scratch resources become garbage-collection candidates only after GPU completion and logical commit.

## 3. Logical versus physical geometry

The tensor/gradient/parity surface remains logically one-dimensional:

```text
logical index = 0 .. element_count - 1
```

TensorCube does not change tensor semantics.

```text
logical authority  = 1D scalar surface
execution authority = Micro Atlas page plan + TensorCube residency coordinates
```

The `(tensorcube_x, tensorcube_y)` coordinate is scheduling metadata only.

## 4. Canonical planner

Backend public planner:

```text
plan_micro_atlas_tensorcube_1d(...)
```

Inputs:

```text
logical_element_count
workgroup_size
physical device workgroup limit
policy group cap
```

Default policy:

```text
workgroup_size = 64
policy_group_cap = min(16384, device limit)
```

Derived values:

```text
logical_workgroup_count = ceil(element_count / workgroup_size)
page_count = ceil(logical_workgroup_count / policy_group_cap)
```

TensorCube dimensions use deterministic ceil-square packing.

## 5. Current regression geometry

For the physically failing surface:

```text
logical elements = 5,767,168
logical groups   = 90,112
page group cap   = 16,384
page count       = 6
TensorCube       = 3 x 2
last page groups = 8,192
```

Required:

```text
direct [90112,1,1] dispatch = 0
max page dispatch = 16384 <= physical limit
```

## 6. Micro Atlas page contract

Each page carries metadata only:

```text
page_id
logical_element_start
logical_element_count
logical_group_start
logical_group_count
tensorcube_x
tensorcube_y
generation
```

It does not carry a copied tensor payload.

## 7. Zero-copy residency

The source/reference/candidate/canonical-output buffer remains in place.

Forbidden:

```text
copyBufferToBuffer(source -> micro atlas payload)
CPU payload shuttle
whole-surface repack
mega comparison mirror
mega gradient staging atlas
```

Page WGSL receives the logical page start and count and indexes the already-bound canonical buffer.

Required counters:

```text
payload_copy_count = 0
host_shuttle_count = 0
mega_atlas_payload_count = 0
```

## 8. TensorCube role

TensorCube is a residency and execution-address map:

```text
page p
  -> tensorcube_x
  -> tensorcube_y
  -> generation
  -> logical source/output range
```

TensorCube is not a second copy of tensor bytes.

## 9. HeadwiseOutputParity canonical adoption

`HeadwiseOutputParityPipeline::compare_exact()` and envelope comparison modes must use Micro Atlas pages.

Retired:

```text
whole surface -> one dispatch
```

Canonical:

```text
whole surface
-> Micro Atlas plan
-> page 0 bounded dispatch
-> compact page decision readback
-> page commit / page GC
-> page 1 ...
-> deterministic aggregate receipt
-> logical comparison transaction commit
```

Candidate/reference tensor payload readback remains zero.

## 10. Page parity receipt

Each page receipt contains:

```text
page identity
logical range
TensorCube coordinate
generation
compared count
nonfinite count
envelope violation count
max absolute error
max relative error
first fault index
completion evidence
GC transition
```

Page execution commit requires:

```text
complete logical page coverage
nonfinite count = 0
```

A numerical comparison mismatch is not a transport/page execution fault. This distinction is required because the R13 nonzero audit intentionally compares a zero surface against a nonzero gradient and expects mismatch evidence.

Final parity PASS still requires:

```text
full compared count
nonfinite = 0
envelope violation = 0
```

## 11. R13 linear backward adoption

The same planner is used by:

```text
linear dX
linear dW tile pages
SwiGLU elementwise backward
FFN add/merge
fixture seed generation
```

R13's old 2D dispatch-grid linearization is superseded as the canonical R13-R2 transport.

The logical dW tile remains unchanged, including the existing 1024-row tile identity.

```text
Canonical dW tile
  -> MicroPage 0
  -> MicroPage 1
  -> ...
```

Micro pages are execution fragments, not separate gradient authorities.

## 12. Canonical output writes

Each page writes directly into the canonical output buffer at:

```text
logical_index = page_element_start + page_local_index
```

No page-output consolidation copy is required.

## 13. Lifecycle

Canonical lifecycle:

```text
PLANNED
-> RESIDENT
-> DISPATCHED
-> GPU_COMPLETED
-> COMMITTED
-> GC_ELIGIBLE
-> RELEASED
```

Fault branch:

```text
FAULTED
-> FAULTED_RELEASED
```

## 14. Commit semantics

Page commit means:

```text
GPU work completed
page numerical execution did not fault
page logical output range exists in canonical output authority
compact proof has been admitted
```

Page commit is distinct from whole-transaction commit.

## 15. Transaction semantics

One transaction represents one logical operation such as:

```text
one parity comparison
one logical dW tile
one dX surface
```

Whole transaction authority is promoted only if all required pages complete and the operation-level policy passes.

No partial logical operation may be promoted.

## 16. Garbage collection semantics

The page does not own the canonical tensor payload.

Commit-time GC primarily releases:

```text
page descriptor / lease metadata
TensorCube residency cell ownership
page uniform parameters
page bind group lifetime
compact status / temporary scratch
```

Canonical source, forward tape, resident decoder weights, canonical gradient output, and downstream-owned gradient tiles are not page garbage.

Required:

```text
premature_release_count = 0
orphan_resident_page_count = 0
```

## 17. Completion and reference boundaries

GC eligibility requires:

```text
page committed or fault terminal state
GPU completion observed
page-local reference count = 0
no downstream temporary reference
```

In the Headwise parity path each page's compact mapped decision wait is the physical completion boundary before page scratch is released.

## 18. Generation seal

Each plan carries a generation, and every page records that generation.

A stale-generation page may not commit.

Future slot reuse must change generation identity before the slot can represent another page.

## 19. R13-R1 numerical discipline preservation

R13-R2 preserves:

```text
G204D no gradient zeroing
whole-row invalidation
no partial row-dot continuation
DKDV preflight hoist
zero inner-loop return
stable SwiGLU derivative
explicit nonfinite status
no NaN clamp
no gradient clamp
host hard-fail before publication
live-BQHD CPU-f64 oracle
live-BQHD directional finite difference
production gradient payload readback zero
```

Changing execution transport must not weaken numerical fail-closed semantics.

## 20. R13-R1 transport supersession

R13-R1's direct 2D dispatch-grid workaround is no longer canonical after R13-R2.

R13-R2 preserves the R13-R1 dispatch-limit safety property but implements it through bounded Micro Atlas page dispatches:

```text
repairMode = MICRO_ATLAS_TENSORCUBE_PAGES
twoDimensionalGridLinearization = false
```

## 21. Required runtime receipts

```text
r13_r2_micro_atlas_plan_receipt.json
r13_r2_tensorcube_residency_receipt.json
r13_r2_headwise_parity_page_receipt.json
r13_r2_headwise_parity_transaction_receipt.json
r13_r2_gradient_page_commit_receipt.json
r13_r2_gc_ledger_receipt.json
r13_r2_dispatch_limit_regression_receipt.json
bt_wgsl_micro_atlas_tensorcube_residency_gc_06c_r13_r2_final.json
```

## 22. CLI gates

```text
--require-bt-wgsl-r13-r2-one-d-logical-authority
--require-bt-wgsl-r13-r2-workgroup-bounded-chunking
--require-bt-wgsl-r13-r2-micro-atlas-pages
--require-bt-wgsl-r13-r2-tensorcube-residency
--require-bt-wgsl-r13-r2-zero-copy-page-views
--require-bt-wgsl-r13-r2-zero-payload-replication
--require-bt-wgsl-r13-r2-headwise-parity-adoption
--require-bt-wgsl-r13-r2-linear-backward-adoption
--require-bt-wgsl-r13-r2-deterministic-page-commit
--require-bt-wgsl-r13-r2-transaction-commit
--require-bt-wgsl-r13-r2-completion-bound-gc
--require-bt-wgsl-r13-r2-reference-bound-gc
--require-bt-wgsl-r13-r2-zero-premature-payload-free
--require-bt-wgsl-r13-r2-zero-direct-giant-dispatch
--require-bt-wgsl-r13-r2-zero-mega-comparison-buffer
--require-bt-wgsl-r13-r2-zero-mega-gradient-staging-atlas
--require-bt-wgsl-r13-r2-zero-host-shuttle
--require-bt-wgsl-r13-r2-production-gradient-readback-zero
--require-bt-wgsl-r13-r2-r13-r1-fail-closed-preserved
```

All are required `true` in both standard and full response files.

## 23. Physical target

```text
[bt-wgsl-micro-atlas-tensorcube-residency-gc-06c-r13-r2]
r12_physical_parent=1
r13_r1_code_parent=1
logical_surface_1d=1
physical_dispatch_limit=65535
original_failing_logical_groups=90112
direct_90112_dispatch=0
micro_atlas_page_count>0
max_page_workgroups<=65535
tensorcube_residency=1
payload_copy=0
host_shuttle=0
headwise_parity_tensorcube=1
parity_transaction_commit=1
gradient_tensorcube=1
gradient_transaction_commit=1
page_commit_count>0
page_gc_eligible_count>0
page_release_count>0
premature_release=0
orphan_resident_page=0
production_gradient_payload_readback=0
production_parity_payload_readback=0
g204d_gradient_zeroing=0
partial_rowdot_continuation=0
dkdv_inner_loop_return=0
explicit_nonfinite_status=1
host_fail_before_publication=1
optimizer=0
weight_mutation=0
proof_ledger=HOLD
```

## 24. Regression seal

The invocation must physically encounter the old failing logical geometry:

```text
originalLogicalWorkgroups = 90112
```

and prove:

```text
originalFailingSurfaceObserved = true
directDispatchAttemptCount = 0
representative micro page count >= 2
maxPageWorkgroups <= physicalLimit
```

## 25. Changed source surface

Relative to R13-R1, R13-R2 changes exactly 12 files:

```text
crates/burn_webgpu_backend/src/base_train_r13_oproj_ffn_backward.rs
crates/burn_webgpu_backend/src/headwise_output_parity.rs
crates/burn_webgpu_backend/src/lib.rs
crates/burn_webgpu_backend/src/micro_atlas_tensorcube_1d.rs
crates/burn_webgpu_backend/src/shaders/base_train_r13_add2.wgsl
crates/burn_webgpu_backend/src/shaders/base_train_r13_linear_backward.wgsl
crates/burn_webgpu_backend/src/shaders/base_train_r13_seed.wgsl
crates/burn_webgpu_backend/src/shaders/base_train_r13_swiglu_backward.wgsl
crates/burn_webgpu_backend/src/shaders/headwise_output_parity.wgsl
crates/orchestrator_local/src/base_train_structural_lookahead_decoder_coupling_06c.rs
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c.args
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c_full.args
```

## 26. Bake-time verification boundary

The bake environment does not contain `cargo`, `rustc`, `rustfmt`, or `naga`.

Therefore bake-time authority is limited to source/static verification:

```text
changed source surface exactness
CLI policy cardinality
logical planner arithmetic
old direct giant-dispatch pattern removal from adopted paths
page dispatch pattern presence
zero payload-copy code in the planner/parity page path
archive CRC and overlay/full byte parity
```

Rust compile, WGSL validation, actual 90,112 regression execution, GPU completion/GC receipts, and final PASS token remain operator-machine physical authority.

## 27. PASS token

```text
PASS_ASH_BASETRAIN_BT_WGSL_MICRO_ATLAS_TENSORCUBE_RESIDENCY_GC_06C_R13_R2
R12_PHYSICAL_PARENT /
R13_R1_FAIL_CLOSED_NUMERICS_CODE_PARENT /
ONE_DIMENSIONAL_LOGICAL_SURFACE_AUTHORITY /
WORKGROUP_BOUNDED_CHUNK_DECOMPOSITION /
MICRO_ATLAS_PAGE_AUTHORITY /
TWO_DIMENSIONAL_TENSORCUBE_RESIDENCY_MAP /
ZERO_COPY_RAW_BUFFER_PAGE_VIEW /
ZERO_TENSOR_PAYLOAD_REPLICATION /
BOUNDED_PER_PAGE_DISPATCH /
HEADWISE_OUTPUT_PARITY_TENSORCUBE_ADOPTION /
R13_LINEAR_BACKWARD_TENSORCUBE_ADOPTION /
FFN_GRADIENT_TILE_TENSORCUBE_ADOPTION /
DETERMINISTIC_PAGE_INDEX_COMMIT /
COMPACT_PAGE_RECEIPT_REDUCTION /
LOGICAL_TRANSACTION_COMMIT /
COMMIT_BEFORE_GC /
GPU_COMPLETION_FENCE_BOUND_GC /
REFERENCE_COUNT_BOUND_GC /
CANONICAL_OUTPUT_OWNERSHIP_TRANSFER /
ZERO_PREMATURE_CANONICAL_PAYLOAD_FREE /
CONSUMED_MICRO_ATLAS_PAGE_GARBAGE_COLLECTION /
TENSORCUBE_SLOT_REUSE_GENERATION_SEALED /
ZERO_DIRECT_GIANT_DISPATCH /
ZERO_MEGA_COMPARISON_BUFFER /
ZERO_MEGA_GRADIENT_STAGING_ATLAS /
ZERO_PAYLOAD_COPY /
ZERO_HOST_SHUTTLE /
PRODUCTION_GRADIENT_PAYLOAD_READBACK_ZERO /
PRODUCTION_PARITY_PAYLOAD_READBACK_ZERO /
R13_R1_FAIL_CLOSED_NUMERICS_PRESERVED /
ZERO_OPTIMIZER /
ZERO_WEIGHT_MUTATION /
PROOF_LEDGER_HOLD_SEALED
```
