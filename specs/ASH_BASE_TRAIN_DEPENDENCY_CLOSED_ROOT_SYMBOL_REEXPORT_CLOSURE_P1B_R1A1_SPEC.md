# ASH-BASE-TRAIN-DEPENDENCY-CLOSED-ROOT-SYMBOL-REEXPORT-CLOSURE-P1B-R1A1

## DEPENDENCY-CLOSED ROOT SYMBOL / RE-EXPORT CLOSURE
## + INVALID-SLICE AUTHORITY REPAIR
## + RUST-SIDE GATE / MANIFEST CONSISTENCY
## + NO PRODUCTION RUNTIME SEMANTIC CHANGE

---

# 0. Revision

```text
Patch ID:
ASH-BASE-TRAIN-DEPENDENCY-CLOSED-ROOT-SYMBOL-REEXPORT-CLOSURE-P1B-R1A1

Short name:
P1B-R1A1

Class:
RELEASE DIAGNOSTIC CORRECTNESS REPAIR
DEPENDENCY-CLOSURE AUTHORITY REPAIR
INVALID-SLICE ADMISSION REPAIR
RUST-SIDE DIAGNOSTIC CLOSURE
NO PRODUCTION RUNTIME CHANGE

Direct code parent:
ASH_PASS3_BASE_TRAIN_CORE_COMPOSITION_BISECTION_P1B_R1A_CODE_ONLY.zip

Supplied parent SHA-256:
b2bb43a30c193455d5a86aeb3deb75186c66d4a91c1c84696b8ae2d6f63ed5a3
```

The repository specification lineage before this commit ends at:

```text
ASH-BASE-TRAIN-RELEASE-TRAIT-DEMAND-ATTRIBUTION-P1B-R1
```

The R1A code parent was supplied as the bake input for this revision.

---

# 1. Preserved Evidence

R1A1 preserves the prior diagnostic evidence:

```text
burn-wgpu-local --lib --release
    PASS

burn_webgpu_backend --lib --release
    PASS

base_train --lib --release
    SAME_E0275

P1B-R1 gpu-all cut
    SAME_E0275
```

Canonical fingerprint remains:

```text
error[E0275]
validation::NumericDimension: Sync

ShaderModule
RenderPipeline / BindGroupLayout
Device / Queue
LifetimeTracker
PendingWrites
```

R1A1 does not reinterpret these controls.

---

# 2. Confirmed R1A Closure Defect

The supplied R1A source contains the compile dependency:

```text
dataset::BaseBatchCpu
    ↓
crate root pub use dataset::{ ..., BaseBatchCpu, ... }
    ↓
base_train_atlas_wave_02_r5_r3_geometry_authority
    ↓
use crate::BaseBatchCpu;
```

The R1A CurrentProduction cut removed `dataset` and the root re-export while retaining `base_train_atlas_wave_02_r5_r3_geometry_authority`.

Therefore the original CurrentProduction slice was not root-symbol dependency closed.

A disappearance of E0275 from such a structurally broken slice is not attribution evidence.

Required classification:

```text
INVALID_SLICE
```

not:

```text
E0275_ABSENT
```

---

# 3. Purpose

R1A1 establishes the ordering:

```text
CUT IDENTITY
    ↓
ROOT-SYMBOL / RE-EXPORT CLOSURE
    ↓
MODULE GATE / MANIFEST EQUALITY
    ↓
STRUCTURAL SLICE VALIDITY
    ↓
RELEASE FINGERPRINT CLASSIFICATION
```

No family attribution may bypass structural validity.

---

# 4. Diagnostic Meaning Change

A result previously representable as:

```text
E0275_ABSENT
```

is demoted to:

```text
INVALID_SLICE
```

when the diagnostic cut removes a required root symbol, re-export, alias, type/signature surface, or another cut-owned dependency observed in the compiler diagnostic.

This is a diagnostic evidence-admission change only.

---

# 5. Production Non-Goals

R1A1 changes none of:

```text
McuSessionRuntimeR7 ownership
McuSessionRuntimeR7B ownership
Rc<RefCell<...>>
ProductionMuonRuntime
TrainBackend
PhysicalWgpuRuntimeBindingR1
DeviceAuthorityId
QueueAuthorityId
Soft Tensor Matrix
Adam / HiMuon mathematics
R3C / R3C1 semantic commit
Atlas runtime semantics
checkpoint format
```

R1A1 introduces no:

```text
Arc<Mutex<_>> conversion
unsafe impl Send
unsafe impl Sync
recursion_limit increase
stub module
fake BaseBatchCpu
placeholder re-export
```

---

# 6. Rust-Side Dependency Edge Taxonomy

Materialized in:

```text
crates/base_train/src/core_composition_bisection_p1b_r1a.rs
```

Enums:

```text
P1bR1a1DependencyEdgeKind
P1bR1a1RootExportKind
P1bR1a1RootSymbolUseKind
P1bR1a1SliceValidity
```

The edge taxonomy includes:

```text
ModuleDeclaration
DirectModulePath
RootReExport
RootReExportAlias
RootSymbolImport
RootSymbolQualifiedUse
TypeAlias
FunctionSignature
TraitImplSurface
StaticInitializer
ConstInitializer
SourceVisibleMacroReference
```

No boolean-only edge meaning is introduced.

---

# 7. Root Symbol Origin Authority

Materialized:

```text
P1bR1a1RootSymbolOrigin
P1BR1A1_ROOT_SYMBOL_ORIGINS
```

Current confirmed cross-boundary origin:

```text
root_symbol   = BaseBatchCpu
origin_module = dataset
origin_symbol = BaseBatchCpu
export_kind   = DirectPubUse
```

This table records diagnostic closure-relevant root-symbol origin identity.

---

# 8. Root Symbol Consumer Authority

Materialized:

```text
P1bR1a1RootSymbolConsumer
P1BR1A1_ROOT_SYMBOL_CONSUMERS
```

Current confirmed cross-boundary consumer:

```text
consumer_module = base_train_atlas_wave_02_r5_r3_geometry_authority
root_symbol     = BaseBatchCpu
use_kind        = UseImport
```

---

# 9. Dependency Edge Authority

Materialized:

```text
P1bR1a1DependencyEdge
P1BR1A1_DEPENDENCY_EDGES
```

Confirmed edge:

```text
dataset
    → BaseBatchCpu
    → base_train_atlas_wave_02_r5_r3_geometry_authority
```

The reverse cut closure law is:

```text
origin cut
+
consumer retained
    → INVALID_UNRESOLVED_ROOT_SYMBOL
```

whereas:

```text
origin cut
+
mandatory consumer cut
    → root-symbol closure may remain DependencyClosed
```

---

# 10. CurrentProduction Closure Repair

R1A CurrentProduction module count:

```text
126
```

R1A1 repaired CurrentProduction closure:

```text
127
```

Added member:

```text
base_train_atlas_wave_02_r5_r3_geometry_authority
```

Reason:

```text
dataset is removed by the CurrentProduction cut
→ crate::BaseBatchCpu root export disappears
→ geometry authority is a mandatory consumer
→ geometry authority must enter the reverse cut closure
```

---

# 11. lib.rs Gate Repair

Modified:

```text
crates/base_train/src/lib.rs
```

Previous geometry gate:

```text
not(p1br1a-cut-atlas-checkpoint-support)
```

R1A1 gate:

```text
not(any(
    p1br1a-cut-current-production,
    p1br1a-cut-atlas-checkpoint-support
))
```

The same predicate is applied to both:

```text
pub mod base_train_atlas_wave_02_r5_r3_geometry_authority
pub use self::base_train_atlas_wave_02_r5_r3_geometry_authority::*
```

Normal feature-OFF production compilation remains unchanged.

---

# 12. AtlasCheckpoint Closure

The AtlasCheckpointSupport closure remains:

```text
147 modules
```

Because geometry authority was already present in the Atlas cut, no Atlas total-count increase is needed.

`P1BR1A_ATLAS_CHECKPOINT_ONLY` is repaired from:

```text
21
```

to:

```text
20
```

by removing geometry from the Atlas-only classification because it is now also required by the CurrentProduction reverse closure.

This revision does not claim that CurrentProduction and AtlasCheckpointSupport are semantically independent families.

Family-overlap semantics remain deferred.

---

# 13. Gate / Manifest Single-Line Check

R1A1 materializes Rust tests that embed `lib.rs` using:

```rust
include_str!("lib.rs")
```

and compare actual `pub mod` cfg gates against the explicit Rust closure arrays.

Required equalities:

```text
CurrentProduction cfg-gated modules
    == P1BR1A_CURRENT_PRODUCTION_CLOSURE

AtlasCheckpointSupport cfg-gated modules
    == P1BR1A_ATLAS_CHECKPOINT_CLOSURE
```

No Python or PowerShell loader is required for this check.

---

# 14. Current Materialized Equality

Source inspection of the baked tree gives:

```text
CurrentProduction actual cfg module count = 127
CurrentProduction Rust manifest count     = 127
membership equality                        = true

AtlasCheckpoint actual cfg module count    = 147
AtlasCheckpoint Rust manifest count        = 147
membership equality                        = true
```

This is SOURCE / STATIC evidence only.

The Rust tests are materialized but were not executed in the bake environment because Cargo/rustc are unavailable.

---

# 15. Slice Validity Authority

Materialized states:

```text
Unknown
DependencyClosed
InvalidMissingModule
InvalidMissingReExport
InvalidUnresolvedRootSymbol
InvalidMissingType
InvalidMissingFunction
InvalidMissingTraitImpl
InvalidSignatureDependency
InvalidClosureManifestDrift
InvalidCutGateDrift
InvalidOtherCutInducedStructuralFailure
```

`dependency_closed: bool` is no longer the sole receipt authority.

---

# 16. Invalid-Slice Precedence

Materialized helper:

```text
p1br1a1_classify_with_slice_validity
```

Law:

```text
DependencyClosed
    → preserve fingerprint classification

Unknown
    → Unclassified

any structural invalid state
    → InvalidSlice
```

Therefore:

```text
InvalidUnresolvedRootSymbol
+
E0275Absent
    → InvalidSlice
```

---

# 17. Cut-Induced Structural Diagnostic Detection

Materialized:

```text
p1br1a1_detect_cut_induced_structural_failure
p1br1a1_classify_release_stderr
```

Recognized structural diagnostic markers include:

```text
unresolved import
could not find
cannot find type
cannot find function
cannot find value
failed to resolve
not found in the crate root
```

A diagnostic is classified as cut-induced only when it also binds to:

```text
a cut-owned root symbol
or
a cut-owned module identity
```

An unrelated compiler error is not automatically promoted to InvalidSlice.

---

# 18. R1A1 vs R1A2 Boundary

R1A1 repairs structural validity precedence.

It does not yet close full process observation authority.

Deferred to R1A2:

```text
process exit status authority
exact cargo invocation identity
target/profile/features binding
empty-log rejection
wrong-target rejection
feature-combination runtime admission
caller-selected receipt promotion retirement
```

Thus:

```text
DependencyClosed + no canonical E0275
```

is a necessary structural condition but not yet the final family-promotion authority.

---

# 19. Receipt Extension

`P1bR1aCoreCompositionBisectReceipt` now carries:

```text
slice_validity
root_symbol_origin_digest
root_symbol_consumer_digest
dependency_edge_digest
closure_manifest_digest
cut_gate_digest
invalid_reason
invalid_subject
```

Promotable receipt validation rejects:

```text
slice_validity != DependencyClosed
missing structural digests
closure_manifest_digest != cut_gate_digest
fingerprint classification == InvalidSlice
```

---

# 20. Structural Identity Digests

Materialized Rust helpers:

```text
p1br1a1_root_symbol_origin_digest
p1br1a1_root_symbol_consumer_digest
p1br1a1_dependency_edge_digest
p1br1a1_source_set_digest
```

R1A1 source-set identity binds:

```text
R1A parent identity
cut feature
sorted excluded module set
root-symbol origin graph
root-symbol consumer graph
dependency-edge graph
```

Timestamps are not identity.

---

# 21. Regression Fixtures Materialized in Rust

The library test module now covers:

```text
CurrentProduction subset relation
Atlas-only disjointness after repair
BaseBatchCpu origin/consumer identity
CurrentProduction BaseBatchCpu closure
AtlasCheckpoint BaseBatchCpu closure
origin-only invalid cut
origin+consumer valid cut
alias reverse-closure law
signature reverse-closure law
InvalidSlice precedence over E0275Absent
unrelated Unclassified preservation
known root-symbol compile failure → InvalidSlice
canonical SAME_E0275 preservation for a structurally closed slice
lib.rs CurrentProduction gate/manifest exact equality
lib.rs AtlasCheckpoint gate/manifest exact equality
dataset root re-export source binding
geometry BaseBatchCpu source binding
structural digest non-emptiness
cut digest distinction
```

These tests are Rust-side only.

---

# 22. No External Diagnostic Loader

R1A1 adds:

```text
Python loader:    0
PowerShell loader: 0
new .ps1 files:   0
```

No new Python file is added by this revision.

The full source bake preserves pre-existing repository tools unchanged; they are not R1A1 additions or R1A1 authority.

All new diagnostic logic introduced by R1A1 is in Rust source.

---

# 23. Actual Source Delta

```text
ADD 0
MOD 2
DEL 0
```

Modified:

```text
crates/base_train/src/core_composition_bisection_p1b_r1a.rs
crates/base_train/src/lib.rs
```

No Cargo feature change is required.

No production runtime implementation file is modified.

---

# 24. ZIP Exclusion Law

Both delivered code ZIPs exclude newly generated:

```text
specification documents
external manifest files
artifact/receipt directories
validation-log packages
Python loaders
PowerShell loaders
```

The specification is committed separately to GitHub and is not embedded into either code ZIP.

The full bake contains the parent repository source tree with only the two R1A1 Rust source modifications applied.

---

# 25. Bake Artifacts

Overlay code-only bake:

```text
ASH_BASE_TRAIN_DEPENDENCY_CLOSED_ROOT_SYMBOL_REEXPORT_CLOSURE_P1B_R1A1_OVERLAY_CODE_ONLY.zip
SHA-256: 9fb0d2865ab5d12ded921a79c54d5ddb6e56111154f3ed0b9012c2b6a6d1d957
Bytes: 16,939
Files: 2
CRC: PASS
```

Full applied code-only bake:

```text
ASH_PASS3_BASE_TRAIN_DEPENDENCY_CLOSED_ROOT_SYMBOL_REEXPORT_CLOSURE_P1B_R1A1_CODE_ONLY.zip
SHA-256: 8bbade931dc46659bc393fa2cc869d4ed923bceb9fad43ede6a86e2e68a364e0
Bytes: 21,508,400
Files: 8,425
CRC: PASS
```

Overlay members:

```text
crates/base_train/src/core_composition_bisection_p1b_r1a.rs
crates/base_train/src/lib.rs
```

---

# 26. Bake Qualification

Bake environment:

```text
cargo unavailable
rustc unavailable
```

Therefore:

```text
SOURCE MATERIALIZED                CONFIRMED
SOURCE DELTA = 2 MODIFICATIONS     CONFIRMED
ZIP CRC                            PASS
GATE/MANIFEST SOURCE COUNT         MATCH
ROOT-SYMBOL KNOWN DEFECT           REPAIRED IN SOURCE
RUST TESTS                         MATERIALIZED, NOT RUN
cargo check                        NOT RUN
release build                      NOT RUN
native tests                       NOT RUN
WGPU execution                     NOT RUN
```

No COMPILE / RUNTIME / PHYSICAL PASS is claimed.

---

# 27. Required User-Side Compile Sequence

Normal baseline:

```powershell
cargo build -p base_train --lib --release -j 1
```

Expected diagnostic baseline remains:

```text
SAME_E0275
```

First repaired cut:

```powershell
cargo build -p base_train --lib --release -j 1 `
  --no-default-features `
  --features p1br1a-cut-current-production
```

Interpretation order:

```text
cut-induced structural failure
    → INVALID_SLICE

structurally valid + SAME_E0275
    → VALID_SAME_E0275

structurally valid + no canonical E0275
    → VALID_E0275_ABSENT_CANDIDATE
```

Only if the R1A branch law requires the second coarse cut:

```powershell
cargo build -p base_train --lib --release -j 1 `
  --no-default-features `
  --features p1br1a-cut-atlas-checkpoint-support
```

---

# 28. Promotion Boundary

R1A1 may establish:

```text
PASS_P1B_R1A1_DEPENDENCY_CLOSED_ROOT_SYMBOL_CLOSURE
```

at SOURCE/STATIC level when:

```text
known BaseBatchCpu root-symbol defect is closed
CurrentProduction gate set == Rust closure set
AtlasCheckpoint gate set == Rust closure set
InvalidSlice precedence exists
normal feature-OFF graph is unchanged
```

Release family attribution remains:

```text
HOLD
```

until the repaired cut is compiled in the user's Rust toolchain.

---

# 29. R1A3 Boundary

R1A1 does not hide the existing overlap:

```text
CurrentProduction closure
⊂
AtlasCheckpointSupport closure
```

After the repair:

```text
127
⊂
147
```

R1A1 repairs structural validity only.

Primary class / SharedCore / cross-class dependency semantics remain a later revision.

---

# 30. Completion Law

R1A1 source bake is complete when:

```text
BaseBatchCpu root-symbol consumer is included in CurrentProduction reverse closure
geometry lib.rs gate matches the repaired closure
CurrentProduction Rust manifest and cfg module set are identical
AtlasCheckpoint Rust manifest and cfg module set are identical
root symbol origin/consumer/edge authorities exist in Rust
InvalidSlice dominates E0275Absent for structural failures
receipt contains structural identity fields
no production runtime semantics are changed
no Python or PowerShell loader is added
code ZIPs contain no generated spec/manifest/artifact package
```

Release attribution remains unpromoted until user-side Cargo release evidence exists.

---

# 31. Final Law

> A module cut is not dependency closed merely because retained source does not directly name the removed module.
>
> A crate-root re-export is a compile dependency edge. `origin module → root symbol → consumer` must remain intact or the consumer must enter the reverse cut closure.
>
> Removing E0275 while simultaneously breaking a required root symbol is `INVALID_SLICE`, not evidence that the removed family caused the trait proof.
>
> R1A1 keeps this authority inside Rust. No Python loader or PowerShell loader is introduced.
>
> R1A1 changes diagnostic evidence admission only. It does not change MCU ownership, WGPU physical authority, optimizer semantics, Soft Matrix, Atlas execution, or checkpoint behavior.
>
> Rust compilation remains above source/static evidence. The repaired slice must still be compiled by the user's toolchain before release attribution is promoted.
