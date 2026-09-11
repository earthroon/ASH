# ASH-EVE-MCU-CLOSE-R2-PHYS-R1B-CF1-R1A-CANDIDATE-MANIFEST-ABI-FIX

## Canonical candidate-manifest ABI closure

### Observed blocker

```text
R6CandidateManifestJson: candidate_parameter_manifest.json:
missing field `parameterId`
```

### Contract

R1A generation-zero source materialization and R6 production loading shall use one canonical candidate manifest JSON ABI.

Canonical key policy is camelCase, matching the existing R6 `ParameterStage` reader:

```text
parameterId
logicalShape
logicalElementCount
weightFile
mFile
vFile
coveredRanges
updateNonzeroElementCount
updateSumSquares
updateMaxAbs
candidateWeightDigest
candidateMDigest
candidateVDigest
weightByteOffset
mByteOffset
vByteOffset
packedLayout
```

`FreshParameterStageR1A` shall therefore use `#[serde(rename_all = "camelCase")]`.

The R6 historical reader remains strict. No snake_case alias is added to the production reader, and no historical manifest contract is weakened.

### Authority refresh law

Any R1A source generated before this correction is not an admitted R6 production source because its candidate manifest uses the wrong JSON key ABI. The R1A source must be regenerated from the same physically admitted checkpoint and dataset authority. Its payload bytes may remain identical, but the candidate manifest digest, active source SHA, and R1A receipt digest necessarily change.

R1B-CF1 shall consume only the regenerated R1A source and receipt. Native CF1 shall be regenerated after rebuilding the corrected binary.

### Scope

```text
MOD 1
crates/base_train/src/eve_mcu_close_r2_physical_campaign_r1a.rs
SHA-256 ac48e577ac9dd283093f6b7c92b592741bebd1222c71c0caffaa0aa70e1efeba
```

No model, optimizer, Muon, R13, dataset, checkpoint, WGPU graph, or historical resume semantics change.

### Bake identity

```text
Full ZIP SHA-256:
a62e2f3d81fde838420bf1f1c699937ebbd81db760d2bac41abae396f07689b0

Overlay ZIP SHA-256:
71818b448c813d956280c3d9da2766deb923087102e7525e32ec91081458d597
```
