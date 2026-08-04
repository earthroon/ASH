# ASH-BASETRAIN-ATLAS-WAVE-02-R5-R6

Canonical specification index.

The exact UTF-8 specification is stored byte-sequentially in:

```text
specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_R6_SPEC_CANONICAL/part-00.md
specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_R6_SPEC_CANONICAL/part-01.md
specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_R6_SPEC_CANONICAL/part-02.md
specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_R6_SPEC_CANONICAL/part-03.md
specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_R6_SPEC_CANONICAL/part-04.md
specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_R6_SPEC_CANONICAL/part-05.md
specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_R6_SPEC_CANONICAL/part-06.md
```

Canonical reconstruction:

```powershell
$parts = 0..6 | ForEach-Object {
  "specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_R6_SPEC_CANONICAL/part-{0:D2}.md" -f $_
}

$bytes = foreach ($part in $parts) {
  [System.IO.File]::ReadAllBytes((Resolve-Path $part))
}

[System.IO.File]::WriteAllBytes(
  "specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_R6_SPEC.reconstructed.md",
  [byte[]]$bytes
)
```

Canonical UTF-8 byte length:

```text
37072
```

Canonical SHA-256:

```text
a0292b42f2d4064793326abf971f6aed33543b8a31767877eaa302fbf8173965
```

The reconstructed file is the normative specification.
