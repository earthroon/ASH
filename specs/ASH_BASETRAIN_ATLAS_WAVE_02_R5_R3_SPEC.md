# ASH-BASETRAIN-ATLAS-WAVE-02-R5-R3

Canonical specification index.

The exact UTF-8 specification is stored byte-sequentially in:

```text
specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_R3_SPEC_CANONICAL/part-00.md
specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_R3_SPEC_CANONICAL/part-01.md
specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_R3_SPEC_CANONICAL/part-02.md
specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_R3_SPEC_CANONICAL/part-03.md
specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_R3_SPEC_CANONICAL/part-04.md
specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_R3_SPEC_CANONICAL/part-05.md
specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_R3_SPEC_CANONICAL/part-06.md
```

Canonical reconstruction:

```powershell
$parts = 0..6 | ForEach-Object {
  "specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_R3_SPEC_CANONICAL/part-{0:D2}.md" -f $_
}

$bytes = foreach ($part in $parts) {
  [System.IO.File]::ReadAllBytes((Resolve-Path $part))
}

[System.IO.File]::WriteAllBytes(
  "specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_R3_SPEC.reconstructed.md",
  [byte[]]$bytes
)
```

Canonical UTF-8 byte length:

```text
35904
```

Canonical SHA-256:

```text
3a74d1bf30b85a581a1f087945d2d7a09e10cc22e4fcf260c1361bee1998ce8b
```

The reconstructed file is the normative specification.
