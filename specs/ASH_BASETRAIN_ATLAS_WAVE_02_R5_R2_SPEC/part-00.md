# ASH-BASETRAIN-ATLAS-WAVE-02-R5-R2

## R5-R1 Overlay Lineage Receipt /
## Immutable Parent ZIP Digest /
## Changed-File Exact Set /
## Full Package SHA Recalculation /
## Physical PASS Evidence Reclassification /
## Stale Receipt Rejection /
## No In-Place Receipt Mutation Seal

> Status: SPEC RELEASE rev.1  
> Patch ID: `ASH-BASETRAIN-ATLAS-WAVE-02-R5-R2`  
> Direct code parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R5-R1`  
> Direct semantic parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R5`  
> Parent physical execution: PASS observed on external RTX 3080 runtime  
> Parent evidence admission: HOLD  
> Patch class: lineage, package integrity, receipt correction, and evidence reclassification only  
> Runtime compute mutation authority: none  
> Shader mutation authority: none  
> Model-shape mutation authority: none  
> Existing receipt mutation authority: none  
> R6 admission after this patch alone: forbidden

---

# 0. Purpose

`ASH-BASETRAIN-ATLAS-WAVE-02-R5-R2` repairs the artifact and receipt lineage surrounding AW-02 R5 and R5-R1.

The patch does not claim to repair:

```text
ModelSpec -> Params tensor-shape authority
GQA Q/K/V geometry
RoPE pairing convention
runtime-derived physical counters
proof-ledger failure recording
negative-mutation class coverage
repository-wide WGSL debt
```

Those remain explicit blockers.

R5-R2 exists because the current package contains a physically successful R5 execution but an evidence package whose declared SHA inventory is stale.

The required result is:

```text
immutable R5 parent ZIP
  -> immutable R5-R1 overlay ZIP
  -> exact three-file R5-R1 delta
  -> full R5-R1 body tree rehash
  -> new R5-R1 overlay lineage receipt
  -> stale parent receipt retained as historical evidence
  -> physical PASS reclassified independently from evidence admission
```

No prior receipt, manifest, ZIP, closure document, or runtime artifact may be edited in place.

---

# 1. Confirmed parent identities

The following SHA-256 values are normative inputs to R5-R2.

## 1.1 R5 full body

```text
artifact:
ash_pass3_ASH-BASETRAIN-ATLAS-WAVE-02-R5_same_process_live_residency_staged_oracle_code_baked.zip

sha256:
d97aa65906c958553f22b7042ba679bb7e072b57954a6025ebc2389e2220e64c
```

## 1.2 R5 overlay

```text
artifact:
ash_pass3_ASH-BASETRAIN-ATLAS-WAVE-02-R5_same_process_live_residency_staged_oracle_overlay_baked.zip

sha256:
6e8d31af08d3935202e5c89185008c27ab346e9bee5f067f9e7feaff9a37d972
```

## 1.3 R5-R1 full body

```text
artifact:
ash_pass3_ASH-BASETRAIN-ATLAS-WAVE-02-R5-R1_host_staging_type_boundary_closure_code_baked.zip

sha256:
efb5a6e5fc3d4703d0bdae8a6ca4e21ef8577f4b714eae5de3a34094efe95ec5
```

## 1.4 R5-R1 overlay

```text
artifact:
ash_pass3_ASH-BASETRAIN-ATLAS-WAVE-02-R5-R1_host_staging_type_boundary_closure_overlay_baked.zip

sha256:
0812c3a63962183f2be9d4c24d4720af6e1fbed9eb7704c7de8b9b46d2346673
```

## 1.5 R5 specification

```text
path:
specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_SPEC.md

sha256:
a9e941bfabde7ceede4c0f944e91f7a0cafbb1c8d41b46492c4693b0040b593c

byte_length:
53346
```

R5-R2 must reject any invocation where any supplied parent artifact has a different digest.

---

# 2. Confirmed stale digest inventory

The existing file:

```text
ASH_BASETRAIN_ATLAS_WAVE_02_R5_OVERLAY_RECEIPT.json
```

contains 27 changed-file entries.

A full SHA-256 recalculation against the R5-R1 body produces:

```text
matching entries     24
stale entries         3
total entries        27
```

The three stale entries are normative evidence for R5-R2.

## 2.1 Inherited stale entry

This mismatch already exists relative to the R5 package and is not introduced by the R5-R1 overlay.

| Path | Existing declared SHA-256 | Actual R5-R1 body SHA-256 | Classification |
|---|---|---|---|
| `ASH_BASETRAIN_ATLAS_WAVE_02_R5_CODE_BAKE.md` | `f89b6200ebb62649d266442752162bde2331236b3d5c45fd2057188e9aa64e85` | `a0dca90dc0d9087378d2f00c518e85c4c7f2fa9114e6777e181f4e843f5a6e98` | `InheritedParentReceiptStale` |

R5-R2 must not falsely list this file as modified by R5-R1.

## 2.2 R5-R1 introduced stale entries

These files were changed by R5-R1 but the R5 receipt naturally still contains the R5-era digests.

| Path | Existing declared SHA-256 | Actual R5-R1 body SHA-256 | Classification |
|---|---|---|---|
| `crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r5_physical_gate.rs` | `9e7c6390486ac1c2d9f71154d6a34e72c19b7164829acef00d77f2e1d5d49069` | `8cd01aafa212b4e8c4ee06b9ab5d8a4a4b223589581629f65b720cb44aa84d8b` | `ExpectedChildDeltaButMissingChildReceipt` |
| `tools/repair_aw02_r5_compile_and_run.ps1` | `c710640112cef8756f7af35cd86e92b1653c5e5166a4bded05b47d7d0d92f514` | `44a932784c0c3b2064e8e0193d9a31ee78ec28ce378b91f844f3ee89241e70e9` | `UndeclaredR5R1ChangedFile` |

The repair script change must be included in the R5-R1 exact delta even though the R5-R1 closure document does not describe it.

---

# 3. Exact R5-R1 changed-file set

A bytewise comparison of the immutable R5 full body and immutable R5-R1 full body yields exactly three changed paths.

```text
added:
ASH_BASETRAIN_ATLAS_WAVE_02_R5_R1_HOST_STAGING_TYPE_CLOSURE.md

modified:
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r5_physical_gate.rs

modified:
tools/repair_aw02_r5_compile_and_run.ps1
```

No other path is part of the R5-R1 delta.

The exact expected set is:

```json
[
  {
    "path": "ASH_BASETRAIN_ATLAS_WAVE_02_R5_R1_HOST_STAGING_TYPE_CLOSURE.md",
    "kind": "added",
    "parentSha256": null,
    "childSha256": "5967870dac1863169a712064d3e719ef2ba3466117b22ba19d87f371fc250100"
  },
  {
    "path": "crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r5_physical_gate.rs",
    "kind": "modified",
    "parentSha256": "9e7c6390486ac1c2d9f71154d6a34e72c19b7164829acef00d77f2e1d5d49069",
    "childSha256": "8cd01aafa212b4e8c4ee06b9ab5d8a4a4b223589581629f65b720cb44aa84d8b"
  },
  {
    "path": "tools/repair_aw02_r5_compile_and_run.ps1",
    "kind": "modified",
    "parentSha256": "c710640112cef8756f7af35cd86e92b1653c5e5166a4bded05b47d7d0d92f514",
    "childSha256": "44a932784c0c3b2064e8e0193d9a31ee78ec28ce378b91f844f3ee89241e70e9"
  }
]
```

Required assertions:

```text
actual changed path count == 3
expected changed path count == 3
actual changed path set == expected changed path set
added path count == 1
modified path count == 2
removed path count == 0
undeclared changed path count == 0
missing declared changed path count == 0
```

Set equality must be used.

