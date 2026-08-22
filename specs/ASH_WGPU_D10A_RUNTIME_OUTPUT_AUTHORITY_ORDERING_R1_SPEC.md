# ASH-WGPU-D10A-RUNTIME-OUTPUT-AUTHORITY-ORDERING-R1

## 1. Patch identity

```text
ASH-WGPU-D10A-RUNTIME-OUTPUT-AUTHORITY-ORDERING-R1

Fresh Run Output Non-Existence Authority /
D10 Runtime Admission Before Physical Output Ownership /
Post-Admission Output Directory Acquisition /
Single Canonical Output Directory Creator /
Admission Receipt Write-After-Create Ordering /
No Receipt Into Nonexistent Directory /
No Caller Pre-Creation /
No Empty Failed-Preflight Run Directory /
No Existing-Directory Reuse /
No Automatic Cleanup or Suffix Fallback /
D10A Mirror Qualification Entry Closure /
No TensorCube / HiMuon Semantic Mutation
```

Parent:

```text
ASH-WGPU-D10-MIRROR-QUALIFICATION-ADMISSION-CLOSURE-10A
```

Observed runtime blocker:

```text
R6OutputAlreadyExists:<run-output>
D10A_ADMISSION_NOT_REACHED exit=1
```

R0 owns only the runtime output lifecycle ordering that precedes D10A physical qualification.
It does not promote D10A Mirror execution and does not alter B04/B05/B06/C07/C08 runtime modes.

## 2. Failure being repaired

The parent source had the following effective order:

```text
fresh-output rejection
    -> D10 runtime admission
    -> write output/d10_runtime_admission_receipt.json
    -> later fs::create_dir_all(output)
```

The ordering is contradictory:

```text
fresh gate requires output absent
receipt write requires output present
physical output creation occurred after receipt write
```

The parent static validator proved symbol presence and pre-B04 receipt ordering but did not prove that the output directory physically existed before the receipt writer.

## 3. Canonical R0 ordering

For a D10/Muon admitted run the only legal ordering is:

```text
FreshOutputCheck
    -> ParentDirectoryCheck
    -> existing storage/source/runtime preflight
    -> D10RuntimeAdmission
    -> AcquireFreshRunOutputDirectory
    -> D10RuntimeAdmissionReceiptWrite
    -> ProductionMuonRuntimeConstruction
    -> B04/B05/B06 runtime execution
```

Canonical inequality:

```text
fresh_check
< d10_admission
< output_create
< d10_receipt_write
< ProductionMuonRuntime::load_or_initialize_with_admission
```

For a non-Muon run the D10 admission/receipt nodes are absent, but the same single output creator remains authoritative.

## 4. Fresh output authority

The existing early invariant remains fail-closed:

```rust
ensure!(!output.exists(), "R6OutputAlreadyExists:{}", output.display());
```

R0 does not reuse, delete, truncate, rename, or suffix an existing run directory.

Forbidden:

```text
existing output -> reuse
existing output -> delete and recreate
existing output -> output_1/output_2
empty existing output -> adopt
```

An output path collision before admission remains `R6OutputAlreadyExists`.
A race detected by the physical create operation is a separate `R6OutputAlreadyExistsRace` failure.

## 5. Parent directory authority

The final run directory is not responsible for creating its workspace ancestry.
The canonical parent must already be an existing directory.

```text
output.parent exists and is directory = required
output itself exists = forbidden
```

Failure:

```text
R6OutputParentMissing:<parent>
```

This prevents a mistyped storage root from being silently materialized by `create_dir_all`.

## 6. Single physical creator

R0 introduces one canonical helper:

```rust
acquire_fresh_run_output_directory(output)
```

Physical ownership is arbitrated by:

```rust
fs::create_dir(output)
```

not by the earlier `exists()` observation.

The early existence check is diagnostic/preflight evidence.
The successful `create_dir` is the physical ownership acquisition.

The canonical run output must no longer be created by a later:

```rust
fs::create_dir_all(&output)
```

call.

Subdirectories below the acquired output remain free to use their existing creation logic.

## 7. D10 admission authority

When `admit_tensorcube_local_muon_production_callsite` is true, R0 resolves:

```rust
enforce_runtime_publication_authority_from_environment()
```

before acquiring the final output directory.

Therefore a D10 admission failure leaves no canonical run directory behind.

R0 does not reinterpret D10 profile classes. The exact existing Mirror and D09 candidate classifiers remain authoritative.

## 8. Admission receipt ordering

The D10 runtime admission receipt is written only after output ownership succeeds:

```text
D10 admission
-> output create
-> d10_runtime_admission_receipt.json
-> ProductionMuonRuntime construction
```

The existing receipt writer remains create-new:

```rust
OpenOptions::new().create_new(true).write(true)
```

No canonical D10 admission receipt may be overwritten.

## 9. Runtime construction boundary

`ProductionMuonRuntime::load_or_initialize_with_admission` remains after the D10 receipt write.
This preserves the diagnostic distinction:

```text
receipt absent
= D10 admission/output ownership was not completed

receipt present + runtime construction failure
= admission and output ownership completed, failure occurred later
```

R0 deliberately preserves a run directory and D10 receipt after a post-admission runtime failure.
It performs no automatic cleanup.

## 10. Non-Muon route preservation

When production Muon admission is false:

```text
D10 admission object = None
D10 runtime admission receipt = absent
```

The canonical output directory is still acquired exactly once before normal run artifacts are written.
No D10 authority is fabricated for non-Muon runs.

## 11. Optimizer and attention non-mutation

R0 changes none of the following:

```text
TensorCube attention Stage10/11/12 math
Headwise writer selection
W9A decode policy
Muon numerical algorithm
HiMuon fusion planner
FUSED_RIGHT/FUSED_DOWN executor math
First-candidate eligibility registry
B04 mode semantics
B05 Mirror/Active semantics
B06 Mirror/Active semantics
DeviceTrainableConsumerCapability
AdamW ownership
checkpoint/resume numerical state
```

In particular R0 must not replace:

```text
DeviceTrainableConsumerCapability::None
```

with `DeviceSegmentedGenerationV1`. That belongs to the later optimizer-generation roadmap.

## 12. Failure attribution

R0 makes these phases distinguishable:

```text
PRE_ADMISSION_FAILURE
D10_ADMISSION_FAILURE
OUTPUT_OWNERSHIP_FAILURE
POST_ADMISSION_RUNTIME_CONSTRUCTION_FAILURE
D10A_PHYSICAL_EXECUTION_FAILURE
```

The wrapper may continue to report its existing high-level failure, but the presence of `d10_runtime_admission_receipt.json` must not be interpreted as admission-not-reached.

## 13. Runtime diagnostic

When D10 admission and output ownership succeed, the scheduler emits:

```text
[ASH-D10A-RUNTIME-OUTPUT-AUTHORITY-ORDERING-R1]
fresh=true
d10_admitted=true
output_authority=acquired
directory_created=true
admission_receipt_written=true
```

The diagnostic is evidence of ordering, not D10A Mirror physical promotion.

## 14. Static validation

New validator:

```text
tools/validate_ash_wgpu_d10a_runtime_output_authority_ordering_r1_static.py
```

It must prove at minimum:

```text
fresh-output gate exists
parent-directory gate exists
D10 admission exists
single canonical output creator helper exists
physical creator uses fs::create_dir
canonical fs::create_dir_all(&output) is absent
D10 admission occurs before physical output acquisition
physical output acquisition occurs before D10 receipt write
D10 receipt write occurs before ProductionMuonRuntime construction
receipt writer remains create_new
no automatic remove_dir_all(output)
no automatic output suffix fallback
D10A parent validator imports the R0 ordering relationship
```

## 15. Negative structural cases

The R0 validator must reject source equivalent to:

```text
receipt write -> output create
output create -> D10 admission
existing output -> remove_dir_all -> recreate
existing output -> suffix allocation
canonical output create_dir_all
```

## 16. Physical acceptance matrix

### Existing output

```text
output exists
-> R6OutputAlreadyExists
-> D10 admission not executed
```

### Invalid D10 admission

```text
output absent
D10 admission fails
-> output remains absent
-> D10 receipt absent
```

### Valid D10 admission

```text
output absent
D10 admission succeeds
-> create_dir succeeds
-> D10 receipt written
-> ProductionMuonRuntime construction reached
```

### Post-admission runtime failure

```text
D10 admission succeeds
output ownership succeeds
D10 receipt succeeds
ProductionMuonRuntime fails
-> output preserved
-> D10 receipt preserved
```

### Same-path race

```text
two processes observe absent
-> one create_dir succeeds
-> the other fails R6OutputAlreadyExistsRace
```

## 17. Promotion boundary

R0 promotion means only:

```text
D10A_ENTRY_REACHABLE
R0_RUNTIME_OUTPUT_AUTHORITY_PASS
```

It does not mean:

```text
D10A_MIRROR_PHYSICAL_PASS
HiMuon physical execution PASS
B06 ActiveVerified PASS
D09 Full Active PASS
```

Those require later physical receipts.

## 18. Required invariants

```text
FreshOutputGate = true
ParentDirectoryGate = true
D10AdmissionBeforeOutputCreate = true
OutputCreateBeforeD10Receipt = true
D10ReceiptBeforeProductionMuonRuntime = true
CanonicalOutputCreatorCount = 1
CanonicalCreateDirAllOutputCount = 0
ExistingOutputReuse = false
AutomaticOutputDelete = false
AutomaticSuffixFallback = false
D10ReceiptCreateNew = true
TensorCubeMathChanged = false
HiMuonMathChanged = false
B05ModeChanged = false
B06ModeChanged = false
```

## 19. Natural next step

After R0 is physically confirmed, the next patch is not another filesystem revision.
The next authority is:

```text
ASH-D10A-TENSORCUBE-HIMUON-MIRROR-PHYSICAL-CLOSURE-R1
```

which must prove that the already-existing Local Muon and FUSED_RIGHT/FUSED_DOWN HiMuon routes actually execute under the D10A Mirror profile with planned/physical parity and zero unauthorized mutation.

## 20. Final seal

```text
R0 does not make TensorCube faster.
R0 does not promote HiMuon.
R0 removes the contradictory doorway that prevented their D10A physical qualification from being reached.

Fresh Check
-> D10 Admission
-> Physical Output Ownership
-> D10 Receipt
-> Production Runtime

One run path.
One creator.
No silent reuse.
No pre-admission empty run directory.
```
