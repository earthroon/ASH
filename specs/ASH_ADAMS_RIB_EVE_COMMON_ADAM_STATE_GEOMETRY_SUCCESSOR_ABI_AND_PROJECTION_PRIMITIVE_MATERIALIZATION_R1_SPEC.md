# ASH-ADAMS-RIB-EVE-COMMON-ADAM-STATE-GEOMETRY-SUCCESSOR-ABI-AND-PROJECTION-PRIMITIVE-MATERIALIZATION-R1

## `아담의_갈비뼈_이브` Common Crate / Canonical Adam Range Geometry / Model+Optimizer Successor ABI / Authority-Neutral State Views / Projection Classification / B06-P1-02 Adoption / No Mutable Authority Migration

## 0. Revision identity

Revision:

`ASH-ADAMS-RIB-EVE-COMMON-ADAM-STATE-GEOMETRY-SUCCESSOR-ABI-AND-PROJECTION-PRIMITIVE-MATERIALIZATION-R1`

Human-readable component name:

`아담의 갈비뼈_이브 / Adam's Rib: Eve`

Cargo package identity:

`아담의_갈비뼈_이브`

Rust library target / dependency import identity:

`adam_rib_eve`

Reserved static PASS:

`PASS_ASH_ADAMS_RIB_EVE_COMMON_ADAM_STATE_GEOMETRY_SUCCESSOR_ABI_PROJECTION_PRIMITIVE_MATERIALIZATION_R1_STATIC`

Full release/physical PASS is not claimed by this source bake.

## 1. Purpose

ASH now carries Adam-family semantics across several execution and durability domains:

- B06 AdamW device-generation ledger;
- P1 ActiveDevice pending-generation scheduler;
- AdamW segmented G→G+1 successor ownership;
- RAM-resident Adam M/V;
- 02 bounded device-to-R6 durable projection;
- inactive Adam M/V compatibility copy-forward;
- future RAM candidate generation and exact durability work.

The same structural concepts were beginning to repeat independently: canonical parameter index, logical element start/count, exact source/target generation identity, Weight/M/V component identity, device successor projection, resident projection and inactive copy-forward projection.

This revision extracts only that semantic anatomy into one dependency-neutral common crate.

## 2. Center invariant

`아담의_갈비뼈_이브` owns Adam-family semantic anatomy.

It does not own mutable optimizer state.

It does not own GPU execution.

It does not own RAM M/V.

It does not own B06 pending-generation state.

It does not own R6 packs.

It does not own `active_training_state.json`.

The authority split remains:

```text
Adam semantic anatomy
    = 아담의_갈비뼈_이브

Adam mutable runtime authority
    = current device / RAM owner

Adam durable authority
    = existing R6 / P3 training-state authority
```

## 3. Materialized crate

New workspace crate:

`crates/아담의_갈비뼈_이브/`

Files:

```text
Cargo.toml
src/lib.rs
src/geometry.rs
src/generation.rs
src/state_view.rs
src/projection.rs
src/validation.rs
src/receipt.rs
```

The package is private to the workspace:

`publish = false`

The package keeps the canonical Korean identity while its Rust library target is explicitly ASCII:

```toml
[package]
name = "아담의_갈비뼈_이브"
publish = false

[lib]
name = "adam_rib_eve"
```

This prevents the human/package identity from leaking into consumer import syntax.

## 4. Dependency boundary

The Eve crate depends only on:

- `serde`;
- `sha2`.

It has no dependency on:

- `base_train`;
- `burn_webgpu_backend`;
- `wgpu`;
- Burn;
- MCU runtime;
- Tokio;
- filesystem pack writers.

Dependency direction is one-way:

```text
아담의_갈비뼈_이브
        ↑
burn_webgpu_backend
        ↑
base_train
        ↑
production / MCU orchestration
```

No cycle is admitted.

## 5. Canonical Adam range geometry

New canonical type:

```rust
pub struct AdamRangeR1 {
    pub canonical_parameter_index: u32,
    pub element_start: u64,
    pub element_count: u64,
}
```

The common type owns:

- nonzero range validation;
- checked exclusive end;
- deterministic ordering;
- exact equality;
- same-parameter overlap semantics.

All ranges use half-open interval semantics:

`[element_start, element_start + element_count)`

This is range-level rather than whole-parameter-level because current production supports `PARTITIONED_MUON_ADAMW` parameters.

## 6. Canonical range ordering

`AdamRangeR1` derives total ordering by:

```text
canonical_parameter_index
→ element_start
→ element_count
```

This ordering is usable by BTreeMap/BTreeSet ledgers without relying on submission order, completion order or physical allocation order.

## 7. Range-set validation

New common validator:

`validate_adam_range_set_r1(...)`

It emits `AdamRangeSetReceiptR1` with:

- range count;
- unique parameter count;
- element count;
- overlap count;
- duplicate count;
- canonical SHA-256 digest.

It does not decide whole-model Muon+Adam coverage. That remains a higher-level FullTrainable/router authority.

## 8. Common generation ordinal

Actual ASH B06 generation identity has two dimensions:

- model generation;
- optimizer generation.

Eve therefore materializes:

```rust
pub struct AdamGenerationOrdinalR1 {
    pub model_generation: u64,
    pub optimizer_generation: u64,
}
```

This avoids flattening the existing `TrainableGenerationId` semantics into one scalar.

## 9. Source-to-successor ABI

New:

```rust
pub struct AdamGenerationIdentityR1 {
    pub source: AdamGenerationOrdinalR1,
    pub target: AdamGenerationOrdinalR1,
}
```

Both model and optimizer generations must advance exactly once.

A generation gap, rewind or overflow fails closed.

New range-bound successor identity:

```rust
pub struct AdamSuccessorIdentityR1 {
    pub generation: AdamGenerationIdentityR1,
    pub range: AdamRangeR1,
}
```

This identity is storage-neutral.

## 10. State view ABI

New borrowed semantic views:

```rust
AdamSourceStateViewR1<'a, W, M, V>
AdamSuccessorStateViewR1<'a, W, M, V>
```

The generic W/M/V types remain consumer-owned.

The common crate does not introduce a CPU/GPU buffer enum and does not allocate optimizer storage.

## 11. Adam component vocabulary

New:

```rust
pub enum AdamComponentR1 {
    Weight,
    FirstMoment,
    SecondMoment,
}
```

This creates one stable vocabulary for Weight / M / V semantics across execution and durable projection.

## 12. Projection source vocabulary

New:

```rust
pub enum AdamProjectionSourceR1 {
    DeviceSuccessorWeight,
    DeviceSuccessorFirstMoment,
    DeviceSuccessorSecondMoment,
    ResidentFirstMoment,
    ResidentSecondMoment,
    InactiveFirstMomentCopyForward,
    InactiveSecondMomentCopyForward,
}
```

This explicitly distinguishes newly produced successor state from compatibility copy-forward state.

## 13. Projection identity

New:

```rust
pub struct AdamProjectionRangeR1 {
    pub range: AdamRangeR1,
    pub component: AdamComponentR1,
    pub source: AdamProjectionSourceR1,
}

pub struct AdamProjectionIdentityR1 {
    pub generation: AdamGenerationIdentityR1,
    pub projection: AdamProjectionRangeR1,
}
```

Component/source compatibility is validated centrally.

For example:

```text
Weight + DeviceSuccessorWeight                       valid
FirstMoment + DeviceSuccessorFirstMoment             valid
SecondMoment + DeviceSuccessorSecondMoment           valid
FirstMoment + InactiveFirstMomentCopyForward         valid
SecondMoment + InactiveSecondMomentCopyForward       valid
Weight + DeviceSuccessorFirstMoment                  invalid
```

## 14. Inactive copy-forward semantics

`InactiveFirstMomentCopyForward` and `InactiveSecondMomentCopyForward` mean schema-preserving source-state carry-forward only.

They do not mean that AdamW executed on the range.

They do not become warm Adam authority.

They do not alias Muon momentum.

## 15. B06 geometry adoption

`burn_webgpu_backend::hybrid_optimizer_device_commit` no longer owns an independent AdamW segment geometry struct.

Historical public compatibility name remains:

`AdamWDeviceCandidateSegmentKeyR1`

but it is now a type alias to:

`AdamRangeR1`

Therefore B06 callers retain their existing public name while the actual geometry SSOT lives in Eve.

## 16. B06 range-set adoption

`AdamWDeviceCandidateGenerationLedgerR1::validate()` now invokes the Eve range-set validator before the existing B06-specific physical checks.

It requires:

- zero overlap;
- zero duplicate range;
- exact segment count;
- exact element count.

B06 continues independently to own:

- real SubmissionEpoch union;
- physical Weight/M/V backing IDs;
- B06 coverage/ledger digests;
- staging and commit semantics.

## 17. B06 successor ABI adoption

B06 segment and generation ticket validation now materializes the Eve model+optimizer source/target generation identity and requires exact successor semantics.

The existing `TrainableGenerationId` remains the B06 runtime type.

Eve does not replace B06 generation ownership.

## 18. P1 scheduler geometry adoption

`AdamWActiveDevicePendingGenerationSchedulerR1` now owns:

```text
BTreeMap<AdamRangeR1, PendingAdamWActiveDeviceCandidateR1>
BTreeSet<AdamRangeR1>
```

instead of a separately defined AdamW key geometry.

Segment admission constructs `AdamRangeR1` directly.

Overlap rejection uses Eve's checked range semantics.

## 19. P1 terminal range-set validation

After all pending submissions have been collected, P1 validates its entire submitted range set through Eve before the generation may be taken.

Required:

```text
overlap_count = 0
duplicate_count = 0
range_count = submitted_segment_count
element_count = expected_element_count
```

Physical pending ownership, SubmissionEpoch and nonblocking collect remain P1 responsibilities.

## 20. Full-model AdamW generation adoption

`AdamWDeviceSegmentedGenerationR1` now owns:

`BTreeMap<AdamRangeR1, AdamWActiveDeviceCandidateSegmentR1>`

Publication constructs the common range type and uses common overlap semantics.

The FullTrainable owner itself remains in `base_train` because it combines Muon and AdamW domains.

## 21. 02 durable projection adoption

The existing full-trainable bounded projection now creates one Eve generation identity from:

```text
source model generation
source optimizer step
→
target model generation
target optimizer step
```

Each routed logical range is materialized as an `AdamRangeR1` before Adam-state projection classification.

## 22. AdamW device successor classification in 02

For an AdamW-owned route, 02 validates:

```text
Weight       → DeviceSuccessorWeight
Adam M       → DeviceSuccessorFirstMoment
Adam V       → DeviceSuccessorSecondMoment
```

The existing GPU buffer copy/readback path remains unchanged.

Eve only validates the semantic classification.

## 23. Muon-owned compatibility M/V classification in 02

For a Muon-owned logical route, 02 validates:

```text
Adam M compatibility state
→ InactiveFirstMomentCopyForward

Adam V compatibility state
→ InactiveSecondMomentCopyForward
```

Muon weight itself remains outside Eve's Adam projection classification.

This preserves the current R6 M/V compatibility contract without falsely classifying Muon as Adam execution.

## 24. No backend mechanics moved into Eve

Eve does not contain:

- `wgpu::Buffer`;
- Queue submission;
- SubmissionEpoch;
- map_async;
- P5 completion state;
- pending maps;
- device source leases.

These remain consumer responsibilities.

## 25. No durable mechanics moved into Eve

Eve does not contain:

- `SequentialPackWriter`;
- `PackedRuntimeStateManifestV1`;
- R6 filenames;
- filesystem operations;
- active training-state publication.

02 and P3 retain those authorities.

## 26. No optimizer routing moved into Eve

Eve does not decide whether a range is Muon-owned or AdamW-owned.

The existing routing registry remains SSOT.

The consumer first obtains routing classification and only then creates the corresponding Eve Adam range/projection identity.

## 27. No Adam mathematical extraction in R1

R1 does not move or rewrite:

- beta1 / beta2 math;
- M update math;
- V update math;
- bias correction;
- epsilon handling;
- AdamW weight decay;
- learning-rate policy.

Therefore R1 is intended to be numerical-output-neutral.

## 28. Structural receipt

New:

`AdamsRibEveStructuralReceiptR1`

It records:

- geometry materialized;
- generation identity materialized;
- source/successor views materialized;
- projection primitive materialized;
- B06 adoption;
- P1 adoption;
- 02 durable projection adoption;
- mutable-state migration flag;
- execution-authority migration flag;
- durable-head migration flag;
- deterministic receipt digest.

All authority migration flags are false.

## 29. BaseTrain adoption receipt

New module:

`crates/base_train/src/adams_rib_eve_common_adam_state_r1.rs`

It seals the actual current adoption state:

```text
B06 geometry adopted       true
P1 scheduler adopted       true
02 projection adopted      true
```

No per-step runtime artifact is required.

## 30. Workspace integration

The new crate is added to both workspace `members` and `default-members`.

`base_train` and `burn_webgpu_backend` depend on it through:

```toml
adam_rib_eve = {
    package = "아담의_갈비뼈_이브",
    path = "../아담의_갈비뼈_이브"
}
```

`Cargo.lock` is updated to bind the new local package and consumer dependencies.

## 31. Historical validator evolution

The B06 and P1 historical validators previously required exact source spelling of locally owned AdamW key types.

This revision broadens them to accept either:

- the historical local key structure; or
- the evolved Eve-backed canonical geometry.

The new Eve validator separately requires that current R1 source actually adopts Eve.

This preserves historical revision intent without forcing semantic duplication to survive forever.

## 32. New static validator

New:

`tools/validate_ash_adams_rib_eve_common_adam_state_geometry_successor_abi_projection_primitive_materialization_r1_static.py`

It verifies:

- exact package identity;
- private package policy;
- ASCII Rust lib target;
- dependency-minimal crate;
- workspace and lock integration;
- common geometry/generation/state/projection types;
- no execution/durable authority leakage into Eve;
- B06 alias and range-set adoption;
- B06 successor identity adoption;
- P1 common geometry and range-set adoption;
- FullModel common geometry adoption;
- 02 common projection classification;
- base-train adoption receipt;
- authority migration flags remain false.

## 33. Observed static regression state

The bake environment observed PASS for:

```text
Eve R1 common semantic materialization
P1 AdamW pending generation scheduler
B06 multi-segment generation ledger
Full-model AdamW device segmented successor
02 full-trainable bounded durable projection
SubmissionEpoch active-async completion
P3 active transactional commit/restart
Unified Atlas MCU control plane
```

These are static/source validators only.

## 34. Compile boundary

A real Cargo compile remains mandatory because this revision changes:

- workspace graph;
- a new local package;
- Cargo.lock;
- public B06 type aliasing;
- cross-crate imports;
- P1 map key types;
- 02 projection validation imports.

The assistant bake environment exposes no `cargo`, `rustc` or `rustfmt`.

Therefore release compile is not claimed.

## 35. Physical boundary

No new GPU math is introduced by Eve itself.

Nevertheless the production regression campaign must eventually prove the refactor does not alter:

- AdamW GPU successor bits;
- B06 ledger identity;
- P1 pending ownership;
- 02 projected weight/M/V bytes;
- R6 restart behavior.

No RTX physical PASS is claimed by this source bake.

## 36. Packaging policy

Baked implementation ZIP excludes:

- this specification;
- all Markdown;
- `specs/`;
- bake manifests;
- generated manifests/receipts/evidence;
- qualification artifacts;
- runtime JSON/JSONL;
- runtime packs;
- logs;
- `target/` and `target_*`;
- `.git/`;
- Python bytecode caches;
- backup files.

Implementation source includes the new crate, Cargo integration and validator source.

## 37. GitHub publication policy

GitHub publication for this revision is specification-only.

Implementation source remains in the baked source ZIP unless implementation publication is separately requested.

## 38. Source truth after successful code bake

```text
아담의_갈비뼈_이브 package                         true
ASCII Rust lib target adam_rib_eve                  true
canonical AdamRangeR1                               true
model+optimizer successor ABI                       true
source/successor state-view ABI                     true
projection source vocabulary                        true
inactive M/V copy-forward vocabulary                true
B06 geometry adoption                               true
P1 scheduler geometry adoption                      true
02 durable projection adoption                      true
mutable Adam state moved into Eve                   false
GPU execution moved into Eve                        false
RAM authority moved into Eve                        false
R6 writer moved into Eve                            false
commit/head authority moved into Eve                false
Adam mathematical kernel moved into Eve             false
release compile                                     not claimed
physical GPU PASS                                   not claimed
```

## 39. Exact next child

Only after this structural commonization compiles and regresses cleanly should the project consider:

`ASH-ADAMS-RIB-EVE-CANONICAL-ADAM-MATHEMATICAL-UPDATE-PRIMITIVE-AND-BACKEND-PARITY-MATERIALIZATION-R2`

That later child may evaluate extraction of Adam mathematical semantics.

It must not be folded into R1.

## 40. Center sentence

**`아담의_갈비뼈_이브`는 Adam의 M/V를 소유하는 새 관리자도 아니고 GPU·RAM·checkpoint를 집어삼키는 새 runtime도 아니다. B06, P1, 02에 반복되던 “어느 logical range가 Adam 상태인가, model/optimizer 세대가 정확히 G→G+1인가, 이 Weight/M/V가 device successor인지 resident인지 inactive copy-forward인지”라는 공통 골격만 하나의 dependency-neutral crate로 뽑는다. 상태와 실행과 commit은 기존 owner에게 남고, 뼈의 의미만 이브가 SSOT가 된다.**
