# ASH-BASETRAIN-ATLAS-WAVE-02-R5-R2

Canonical specification index.

The exact UTF-8 specification is stored byte-sequentially in:

```text
specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_R2_SPEC_CANONICAL/part-00.md
specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_R2_SPEC_CANONICAL/part-01.md
specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_R2_SPEC_CANONICAL/part-02.md
specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_R2_SPEC_CANONICAL/part-03.md
```

Canonical reconstruction:

```powershell
$parts = 0..3 | ForEach-Object {
  "specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_R2_SPEC_CANONICAL/part-{0:D2}.md" -f $_
}

$bytes = foreach ($part in $parts) {
  [System.IO.File]::ReadAllBytes((Resolve-Path $part))
}

[System.IO.File]::WriteAllBytes(
  "specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_R2_SPEC.reconstructed.md",
  [byte[]]$bytes
)
```

Canonical UTF-8 byte length:

```text
23644
```

Canonical SHA-256:

```text
5ab07c9952154a259ea46949c8d0508fb6ca28842752d18bf79a4e19d41d5f10
```

The earlier directory `specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_R2_SPEC/` contains a superseded partial upload and is not normative. Only the `_CANONICAL` directory above reconstructs the specification.
