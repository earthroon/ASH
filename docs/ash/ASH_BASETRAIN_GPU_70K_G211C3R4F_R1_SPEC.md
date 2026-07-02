# ASH-BASETRAIN-GPU-70K-G211C3R4F-R1

## R4E Next Gate Authority Reader Hotfix / Entry Packet To-Gate Accept Repair / No Normalization Logic Mutation

Seal: Entry Authority Reader Hotfix Only / No Normalization Logic Mutation / No Runtime Splice / No Promotion Reopen.

## SSOT

`70K-G211C3R4F-R1` repairs only the R4F entry validation reader for the R4E to R4F next-gate authority.

The observed failure was:

```text
ERR_70K_G211C3R4F_R4E_NEXT_GATE_MISMATCH
```

The valid current R4E transition authority is:

```text
ASH-BASETRAIN-GPU-70K-G211C3R4E -> ASH-BASETRAIN-GPU-70K-G211C3R4F
```

R4F-R1 must accept that transition when it is expressed by the R4E next entry packet as:

```json
{
  "to_gate": "ASH-BASETRAIN-GPU-70K-G211C3R4F"
}
```

R4F-R1 must not require a single `next_gate` root field when an explicit entry packet `to_gate` already exists.

`70K-G211C3R4F-R1` must not mutate readback/poll/map split logic, contamination ratio logic, attribution normalization logic, verdict selection, R4E retention audit logic, R4F output schemas, runtime route, `tensorcube_runtime_splice`, production WGSL, production tile/workgroup/padding policy, model weights, checkpoints, optimizer/training state, promotion state, or G211C4 entry state.

## Scope

Included:

```text
1. Update R4F Rust entry validation next gate reader.
2. Accept R4E next entry packet to_gate.
3. Accept R4E next entry packet next_gate.
4. Accept R4E main receipt next.next_gate.
5. Accept R4E main receipt root next_gate.
6. Record resolved_r4e_next_gate.
7. Record resolved_r4e_next_gate_source.
8. Write R4F-R1 next gate reader hotfix receipt.
9. Preserve main R4F PASS marker.
```

Excluded:

```text
1. Readback/poll/map timing split changes.
2. Contamination ratio calculation changes.
3. Normalization verdict or class selection changes.
4. R4E verdict retention logic changes.
5. R4F artifact schema changes except optional R1 hotfix reference fields.
6. Runtime splice or promotion reopen.
7. G211C4 entry generation.
```

## R4E Next Gate Authority Resolve Order

R4F-R1 must resolve R4E next gate authority from the following ordered candidate paths:

```text
1. artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_NEXT_ENTRY_PACKET_G211C3R4F.json::to_gate
2. artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_NEXT_ENTRY_PACKET_G211C3R4F.json::next_gate
3. artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_KERNEL_TILE_PADDING_ATTRIBUTION.json::next.next_gate
4. artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_KERNEL_TILE_PADDING_ATTRIBUTION.json::next_gate
```

The resolved value must be exactly:

```text
ASH-BASETRAIN-GPU-70K-G211C3R4F
```

Allowed source labels:

```text
R4E_ENTRY_PACKET_TO_GATE
R4E_ENTRY_PACKET_NEXT_GATE
R4E_MAIN_RECEIPT_NEXT_NEXT_GATE
R4E_MAIN_RECEIPT_ROOT_NEXT_GATE
MISSING
```

## Local Rust Binary

```text
crates/base_train/src/bin/ash_basetrain_gpu_70k_g211c3r4f_readback_poll_map_split.rs
```

Suggested command from ASH root:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g211c3r4f_readback_poll_map_split
```

Expected R1 hotfix stdout fields:

```text
PASS_ASH_BASETRAIN_GPU_70K_G211C3R4F_R1_NEXT_GATE_READER_HOTFIX
r4f_r1_next_gate_reader_hotfix=true
resolved_r4e_next_gate=ASH-BASETRAIN-GPU-70K-G211C3R4F
resolved_r4e_next_gate_source=<...>
entry_packet_to_gate_accepted=<true|false>
next_gate_reader_repaired=true
normalization_logic_mutated=false
```

Expected final R4F PASS marker remains:

```text
PASS_ASH_BASETRAIN_GPU_70K_G211C3R4F_READBACK_POLL_MAP_SPLIT
```

## Required Output Addendum

R4F-R1 may add this hotfix receipt:

```text
artifacts/g211c3r4f/ASH_BASETRAIN_GPU_70K_G211C3R4F_R1_NEXT_GATE_READER_HOTFIX.json
```

Forbidden output:

```text
artifacts/g211c3r4f/ASH_BASETRAIN_GPU_70K_G211C3R4F_NEXT_ENTRY_PACKET_G211C4.json
```

## PASS Criteria

```text
PASS-01 R4E next entry packet found.
PASS-02 R4E main attribution receipt found.
PASS-03 R4E next gate authority resolved from allowed candidate paths.
PASS-04 resolved_r4e_next_gate = ASH-BASETRAIN-GPU-70K-G211C3R4F.
PASS-05 resolved_r4e_next_gate_source recorded.
PASS-06 R4F entry validation no longer rejects valid R4E to R4F packet.
PASS-07 R1 hotfix receipt written.
PASS-08 normalization_logic_mutated=false.
PASS-09 readback_poll_map_logic_mutated=false.
PASS-10 contamination_ratio_logic_mutated=false.
PASS-11 artifact_schema_mutated=false.
PASS-12 runtime_splice_allowed=false.
PASS-13 promotion_allowed=false.
PASS-14 G211C4 entry packet not generated.
PASS-15 main R4F normalization execution continues after entry validation.
PASS-16 main R4F PASS marker remains unchanged.
```

## PASS Meaning

PASS means R4F-R1 repaired the R4E next gate authority reader so that a valid R4E next entry packet using `to_gate = ASH-BASETRAIN-GPU-70K-G211C3R4F` is accepted by R4F.

PASS does not mean R4F normalization succeeded unless the main R4F PASS marker is printed. PASS does not mean TensorCube is faster. PASS does not mean readback/poll/map split is correct by itself. PASS does not mean promotion is reopened. PASS does not mean G211C4 is allowed.

## Recommended Commit Message

```text
ASH-BASETRAIN-GPU-70K-G211C3R4F-R1 accept R4E to_gate authority

- Repair R4F entry validation for R4E next gate authority
- Accept R4E next entry packet to_gate as valid transition authority
- Preserve fallback reads from next_gate, next.next_gate, and root next_gate
- Record resolved next gate source in R1 hotfix receipt
- Preserve readback, poll, map, contamination, and normalization logic
- Preserve R4F artifact schema and main PASS marker
- Preserve no runtime splice, no G211C4 entry, no production route, no promotion
```
