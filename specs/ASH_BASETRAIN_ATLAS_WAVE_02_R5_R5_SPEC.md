# ASH-BASETRAIN-ATLAS-WAVE-02-R5-R5

Canonical specification index.

The exact UTF-8 specification is stored byte-sequentially in:

```text
specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_R5_SPEC_CANONICAL/part-00.md
specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_R5_SPEC_CANONICAL/part-01.md
specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_R5_SPEC_CANONICAL/part-02.md
specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_R5_SPEC_CANONICAL/part-03.md
specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_R5_SPEC_CANONICAL/part-04.md
specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_R5_SPEC_CANONICAL/part-05.md
specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_R5_SPEC_CANONICAL/part-06.md
```

Canonical reconstruction:

```powershell
$parts = 0..6 | ForEach-Object {
  "specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_R5_SPEC_CANONICAL/part-{0:D2}.md" -f $_
}

$bytes = foreach ($part in $parts) {
  [System.IO.File]::ReadAllBytes((Resolve-Path $part))
}

[System.IO.File]::WriteAllBytes(
  "specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_R5_SPEC.reconstructed.md",
  [byte[]]$bytes
)
```

Canonical UTF-8 byte length:

```text
41023
```

Canonical SHA-256:

```text
965e0afb88d7c83fad8928533d2c168445e1807b9af3fd2c739f03eaf79cd424
```

The reconstructed file is the normative specification.
