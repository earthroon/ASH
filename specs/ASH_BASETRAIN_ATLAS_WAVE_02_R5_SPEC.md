# ASH-BASETRAIN-ATLAS-WAVE-02-R5

Canonical specification index.

The exact UTF-8 specification is stored byte-sequentially in:

```text
specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_SPEC/part-00.md
specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_SPEC/part-01.md
specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_SPEC/part-02.md
specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_SPEC/part-03.md
specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_SPEC/part-04.md
specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_SPEC/part-05.md
specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_SPEC/part-06.md
specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_SPEC/part-07.md
```

Canonical reconstruction:

```powershell
$parts = 0..7 | ForEach-Object {
  "specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_SPEC/part-{0:D2}.md" -f $_
}

$bytes = foreach ($part in $parts) {
  [System.IO.File]::ReadAllBytes((Resolve-Path $part))
}

[System.IO.File]::WriteAllBytes(
  "specs/ASH_BASETRAIN_ATLAS_WAVE_02_R5_SPEC.reconstructed.md",
  [byte[]]$bytes
)
```

Canonical UTF-8 byte length:

```text
53346
```

Canonical SHA-256:

```text
a9e941bfabde7ceede4c0f944e91f7a0cafbb1c8d41b46492c4693b0040b593c
```

The split representation exists only to preserve exact byte content through the GitHub connector. The reconstructed file is the normative specification.
